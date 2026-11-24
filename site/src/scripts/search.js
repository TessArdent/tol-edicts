// Client-side search over /search.json. Query and filters live in the URL.
import MiniSearch from "minisearch";

const PAGE = 100;
const base = import.meta.env.BASE_URL.replace(/\/$/, "");
const slug = (s) => s.toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const esc = (s) => s.replace(/[&<>"]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[ch]);

export async function start() {
  const form = document.getElementById("search");
  const q = document.getElementById("q");
  const status = document.getElementById("status");
  const list = document.getElementById("results");
  const more = document.getElementById("more");

  readUrl(form);
  q.focus();

  let data;
  try {
    data = await (await fetch(`${base}/search.json`)).json();
  } catch {
    status.textContent = "The search index couldn't be loaded.";
    return;
  }

  // One document per change; announcements are appended when first needed.
  const namesOf = (classIdx) => classIdx.map((c) => [data.classes[c].n, ...data.classes[c].a].join(" ")).join(" ");
  const docs = data.items.map((it, i) => ({ id: i, kind: "item", it, text: it.t, names: namesOf(it.c) }));
  const toIndex = (list) => list.map(({ id, text, names }) => ({ id, text, names }));
  const ms = new MiniSearch({
    fields: ["text", "names"],
    storeFields: [],
    searchOptions: {
      // short words match exactly: "fee" shouldn't find "feedback"
      prefix: (term) => term.length >= 4,
      fuzzy: (term) => (term.length >= 5 ? 0.15 : 0),
      combineWith: "AND",
      boost: { names: 2 },
    },
  });
  // Indexing in small chunks keeps the page responsive while it runs.
  let indexed = ms.addAllAsync(toIndex(docs), { chunkSize: 250 });
  let posts = null;
  function loadPosts() {
    posts ??= fetch(`${base}/search-posts.json`).then((r) => r.json()).then((list) => {
      const extra = list.map((p, i) => ({
        id: data.items.length + i, kind: "post", p, text: `${p.n} ${p.t}`, names: namesOf(p.c),
      }));
      docs.push(...extra);
      indexed = indexed.then(() => ms.addAllAsync(toIndex(extra), { chunkSize: 250 }));
    });
    return posts;
  }

  const patchPos = new Map(data.patches.map((p, i) => [p.id, i]));
  const classPos = new Map(data.classes.map((c, i) => [c.n, i]));
  let shown = PAGE;
  let current = [];

  function state() {
    const fd = new FormData(form);
    return {
      q: (fd.get("q") || "").trim(),
      classes: new Set(fd.getAll("class").map((n) => classPos.get(n))),
      factions: new Set(fd.getAll("faction").map((f) => data.factions.indexOf(f))),
      cats: new Set(fd.getAll("cat").map((c) => data.categories.indexOf(c))),
      from: fd.get("from") ? patchPos.get(fd.get("from")) : 0,
      to: fd.get("to") ? patchPos.get(fd.get("to")) : data.patches.length - 1,
      ranged: !!(fd.get("from") || fd.get("to")),
      src: fd.get("src") || "",
      ann: fd.get("ann") === "1",
    };
  }

  function keep(doc, s) {
    const anyOf = (set, arr) => set.size === 0 || arr.some((x) => set.has(x));
    if (doc.kind === "post") {
      if (!s.ann || s.factions.size || s.cats.size || s.src) return false;
      // announcements go back to 2016, before the first patch: only a chosen
      // version range limits them
      const d = doc.p.d;
      if (s.ranged && (d < data.patches[s.from].d || d > data.patches[s.to].d)) return false;
      return anyOf(s.classes, doc.p.c);
    }
    const it = doc.it;
    if (it.p < s.from || it.p > s.to) return false;
    if (s.src && (data.patches[it.p].s === 0 ? "forum" : "steam") !== s.src) return false;
    if (s.cats.size && !s.cats.has(it.g)) return false;
    return anyOf(s.classes, it.c) && anyOf(s.factions, it.f);
  }

  const dateOf = (doc) => (doc.kind === "post" ? doc.p.d : data.patches[doc.it.p].d);

  let runId = 0;
  async function run() {
    const id = ++runId;
    const s = state();
    writeUrl(form);
    countFilters(form);
    // Filters alone don't need the text index, so those results show at once.
    if (s.ann) await loadPosts();
    if (s.q) {
      if (!ms.documentCount || docs.length > ms.documentCount) status.textContent = "Preparing search…";
      await indexed;
    }
    if (id !== runId) return;        // a newer run has started
    let hits;
    if (s.q) {
      hits = ms.search(s.q, { filter: (r) => keep(docs[r.id], s) })
        .map((r) => ({ doc: docs[r.id], terms: r.terms }));
    } else {
      hits = docs.filter((d) => keep(d, s)).map((doc) => ({ doc, terms: [] }))
        .sort((a, b) => dateOf(b.doc).localeCompare(dateOf(a.doc)) || b.doc.id - a.doc.id);
    }
    current = hits;
    shown = PAGE;
    render(s);
  }

  function render(s) {
    const n = current.length;
    const filters = describe(form);
    status.textContent = (n === 0 ? "No matches."
      : `${n.toLocaleString("en")} ${n === 1 ? "match" : "matches"}${s.q ? ", best first" : ", newest first"}.`)
      + (filters ? ` Filters: ${filters}.` : "");
    list.innerHTML = current.slice(0, shown).map(({ doc, terms }) => row(doc, terms)).join("");
    more.hidden = n <= shown;
    more.textContent = `Show ${Math.min(PAGE, n - shown)} more`;
  }

  function highlight(text, terms) {
    let html = esc(text.length > 600 ? text.slice(0, 600) + "…" : text);
    if (!terms.length) return html;
    const rx = new RegExp(`(${terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).sort((a, b) => b.length - a.length).join("|")})`, "gi");
    return html.replace(rx, "<mark>$1</mark>");
  }

  function tags(classIdx, extra) {
    const c = classIdx.map((i) => data.classes[i].n)
      .map((n) => `[<a href="${base}/class/${slug(n)}/">${esc(n)}</a>]`);
    return `<span class="tags">${[...c, ...extra].join(" ")}</span>`;
  }

  function row(doc, terms) {
    if (doc.kind === "post") {
      const p = doc.p;
      return `<li><a href="${base}/chronicle/${p.id}/">${esc(p.n)}</a> <span class="muted">${p.d} · ${esc(p.y)}</span><br>`
        + `${highlight(p.t.slice(0, 300), terms)} ${tags(p.c, [])}</li>`;
    }
    const it = doc.it;
    const patch = data.patches[it.p];
    const cat = data.categories[it.g];
    return `<li><a href="${base}/patch/${patch.id}/changes/">${esc(patch.l)}</a> <span class="muted">${patch.d}</span> `
      + `${it.x ? '<span class="kind">Dev note: </span>' : ""}${highlight(it.t, terms)} `
      + tags(it.c, [`[<a href="${base}/category/${slug(cat)}/">${esc(cat)}</a>]`]) + "</li>";
  }

  let timer;
  form.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(run, 120); });
  form.addEventListener("submit", (e) => { e.preventDefault(); run(); });
  form.addEventListener("reset", () => setTimeout(run, 0));
  more.addEventListener("click", () => { shown += PAGE; render(state()); });
  window.addEventListener("popstate", () => { readUrl(form); run(); });
  run();
}

// --- URL state ----------------------------------------------------------------
// ?q=bleed&class=Hunter,Poacher&faction=Cult&cat=Bug+Fixes&from=1.0.2&to=2.0.0&src=forum&ann=1
const MULTI = ["class", "faction", "cat"];

function readUrl(form) {
  const u = new URLSearchParams(location.search);
  form.reset();
  form.elements.q.value = u.get("q") || "";
  for (const name of MULTI) {
    const want = new Set((u.get(name) || "").split(",").filter(Boolean));
    for (const box of form.querySelectorAll(`input[name="${name}"]`)) box.checked = want.has(box.value);
  }
  form.elements.from.value = u.get("from") || "";
  form.elements.to.value = u.get("to") || "";
  for (const r of form.querySelectorAll('input[name="src"]')) r.checked = r.value === (u.get("src") || "");
  form.elements.ann.checked = u.get("ann") === "1";
}

/** "Hunter, Physician · Class Balance · v1.0.2 to latest", or "" with no filters. */
function describe(form) {
  const fd = new FormData(form);
  const parts = [];
  for (const name of MULTI) if (fd.getAll(name).length) parts.push(fd.getAll(name).join(", "));
  const label = (sel) => sel.options[sel.selectedIndex].text;
  if (fd.get("from") || fd.get("to")) parts.push(`${label(form.elements.from)} to ${label(form.elements.to)}`);
  if (fd.get("src")) parts.push(fd.get("src") === "forum" ? "forum posts" : "Steam posts");
  if (fd.get("ann") === "1") parts.push("with announcements");
  return parts.join(" · ");
}

function writeUrl(form) {
  const fd = new FormData(form);
  const u = new URLSearchParams();
  if (fd.get("q")) u.set("q", fd.get("q").trim());
  for (const name of MULTI) if (fd.getAll(name).length) u.set(name, fd.getAll(name).join(","));
  for (const name of ["from", "to", "src"]) if (fd.get(name)) u.set(name, fd.get(name));
  if (fd.get("ann") === "1") u.set("ann", "1");
  const qs = u.toString().replace(/%2C/g, ",");
  history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
}

function countFilters(form) {
  const fd = new FormData(form);
  const n = (k) => fd.getAll(k).length;
  const set = (key, count) => {
    const el = form.querySelector(`[data-count="${key}"]`);
    if (el) el.textContent = count ? `(${count} selected)` : "";
  };
  set("class", n("class"));
  set("more", n("faction") + n("cat") + (fd.get("from") ? 1 : 0) + (fd.get("to") ? 1 : 0) + (fd.get("src") ? 1 : 0));
}

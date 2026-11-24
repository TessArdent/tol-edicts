// Loads ../data/*.json (built by pipeline/build_data.py) once at build time.
import fs from "node:fs";
import path from "node:path";
import MarkdownIt from "markdown-it";

const DATA = path.resolve(process.cwd(), "../data");
const load = (name) => JSON.parse(fs.readFileSync(path.join(DATA, `${name}.json`), "utf8"));

export const patches = load("patches").sort((a, b) =>
  a.date === b.date ? a.id.localeCompare(b.id) : a.date.localeCompare(b.date));
export const changes = load("changes");
export const chronicle = load("chronicle");
export const classes = load("classes");

// GitHub repository, for "report a wrong tag" links. Set by the Pages workflow;
// empty in local builds, which hides those links.
export const REPO_URL = (process.env.REPO_URL || "").replace(/\/$/, "");

export const CATEGORIES = [
  "Class Balance", "Game-wide", "Quality of Life / UI", "Bug Fixes",
  "Store & Cosmetics", "Events", "Technical", "Dev Notes",
];
export const FACTIONS = ["Blue Dragon", "Unseen", "Cult", "Neutral"];

// Items shown in lists. Summaries repeat detailed items; notes are intros and
// forum replies. Both stay visible in each patch's original text.
export const LISTED_KINDS = new Set(["change", "explanation"]);
export const listed = (c) => LISTED_KINDS.has(c.kind);

export const slug = (s) =>
  s.toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

const base = import.meta.env.BASE_URL.replace(/\/$/, "");
export const url = (p = "/") => `${base}${p.startsWith("/") ? p : `/${p}`}`;
export const patchUrl = (id) => url(`/patch/${id}/`);
export const classUrl = (name) => url(`/class/${slug(name)}/`);
export const categoryUrl = (name) => url(`/category/${slug(name)}/`);

export const patchById = new Map(patches.map((p) => [p.id, p]));
export const classByName = new Map(classes.map((c) => [c.name, c]));

export function groupBy(items, key) {
  const m = new Map();
  for (const it of items) {
    const k = key(it);
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(it);
  }
  return m;
}

export const changesByPatch = groupBy(changes, (c) => c.patch);

/** Changes grouped by patch, newest patch first. */
export function byPatchNewestFirst(items) {
  const g = groupBy(items, (c) => c.patch);
  return [...g.entries()]
    .map(([id, list]) => ({ patch: patchById.get(id), items: list }))
    .sort((a, b) => b.patch.date.localeCompare(a.patch.date) || b.patch.id.localeCompare(a.patch.id));
}

export function patchLabel(p) {
  return p.version ? `v${p.version}` : p.date;
}

// --- Markdown ----------------------------------------------------------------
const md = new MarkdownIt({ html: false, linkify: true, breaks: false });
const defaultImage = md.renderer.rules.image;
md.renderer.rules.image = (tokens, idx, options, env, self) => {
  tokens[idx].attrSet("loading", "lazy");
  return defaultImage(tokens, idx, options, env, self);
};

export const renderMarkdown = (text) => md.render(text || "");

/** One change item: a single paragraph is rendered inline, without <p>. */
export function renderItem(text) {
  const clean = (text || "").replace(/^\s*[•·▪‣]\s*/, "");   // bullet glyphs typed as text
  const html = md.render(clean).trim();
  const single = html.match(/^<p>([\s\S]*)<\/p>$/);
  return single && !single[1].includes("<p>") ? single[1] : html;
}

// Search index for /search/, written as a static file at build time.
// Short keys keep it small; the search page expands them.
import { patches, changes, chronicle, classes, CATEGORIES, FACTIONS, listed, patchLabel } from "../lib/data.js";

const plain = (md) =>
  (md || "")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/[*_~`#>]+/g, "")
    .replace(/\s+/g, " ")
    .trim();

export function GET() {
  const patchIndex = new Map(patches.map((p, i) => [p.id, i]));
  const classIndex = new Map(classes.map((c, i) => [c.name, i]));
  const names = (c) => [c.name, ...(c.aliases || []), ...(c.formerNames || []).map((f) => f.name)];

  const items = changes.filter(listed).map((c) => ({
    p: patchIndex.get(c.patch),                       // patch, by position in "patches"
    t: c.plain,                                       // text
    c: c.classes.map((n) => classIndex.get(n)),       // classes
    f: c.factions.map((f) => FACTIONS.indexOf(f)).filter((i) => i >= 0),
    g: CATEGORIES.indexOf(c.category),                // category
    ...(c.kind === "explanation" ? { x: 1 } : {}),    // dev explanation
  }));

  const posts = chronicle.map((p) => ({
    id: p.id,
    d: p.date,
    y: p.type,
    n: p.title,
    t: plain(p.markdown).slice(0, 4000),
    c: p.classes.map((n) => classIndex.get(n)),
  }));

  const body = {
    patches: patches.map((p) => ({ id: p.id, l: patchLabel(p), d: p.date, s: p.source === "forum" ? 0 : 1 })),
    classes: classes.map((c) => ({ n: c.name, f: c.faction || "", a: names(c).slice(1) })),
    categories: CATEGORIES,
    factions: FACTIONS,
    items,
    posts,
  };
  return new Response(JSON.stringify(body), { headers: { "Content-Type": "application/json" } });
}

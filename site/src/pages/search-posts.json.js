// Announcements for /search/, fetched only when "Include announcements" is on.
import { chronicle, classes } from "../lib/data.js";

const plain = (md) =>
  (md || "")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/[*_~`#>]+/g, "")
    .replace(/\s+/g, " ")
    .trim();

export function GET() {
  const classIndex = new Map(classes.map((c, i) => [c.name, i]));
  const posts = chronicle.map((p) => ({
    id: p.id,
    d: p.date,
    y: p.type,
    n: p.title,
    t: plain(p.markdown).slice(0, 4000),
    c: p.classes.map((n) => classIndex.get(n)),
  }));
  return new Response(JSON.stringify(posts), { headers: { "Content-Type": "application/json" } });
}

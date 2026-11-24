# Plan: Throne of Lies Patch Notes Explorer

A static, searchable site for every Throne of Lies patch note (2016–2023), hosted on GitHub Pages. You can filter by class, faction and change category. Changes that apply to the whole game get their own **Game-wide** category.

## 1. Starting point

| | |
|---|---|
| Source data | `changelogs/forum/` (221 topics, 106 patch notes, Feb 2016 – Sep 2021) and `changelogs/steam/` (162 posts, Apr 2017 – Jan 2023) |
| Size | about 1.9 MB of Markdown, about 5,800 bullet-point changes |
| Hard part | The structure changes by era, so splitting notes into per-class changes needs a careful parser plus manual corrections |

How class changes are written in each era:

| Era | Example | How class changes appear |
|---|---|---|
| 0.8 – 1.1 (2017–18) | `1.0.2 Patch Notes` | A heading per class (`## Alchemist:`), plus `## General`, `## Bug Fixes` |
| 2.x – 3.x (2018–20) | `Patch v2.5b` | Quoted labels (`> Balance Changes: Observer`) under `## Balance`, plus `## Quality of Life` and summary lists |
| 4.x – 7.x (2021–23) | `v4.1.0`, `v7.0.2` | Themed sections (`Patch Highlights`, `Summary`, `Detail`), with classes mostly named inside the bullet text |

Classes and abilities were also renamed over time (for example the ability Follow → Observe), so tagging needs a hand-maintained alias map. Several Blue Dragon classes also have an Unseen convert that is a separate class: Noble → Aristocrat, Drunk → Alcoholic. These are linked with `convertOf`, not merged.

## 2. Architecture

```
changelogs/ (raw Markdown)
   │  pipeline/  (Python)
   ▼
data/patches.json   one record per patch (version, date, title, source links, full text)
data/changes.json   one record per change item (text, patch, section, classes[], factions[], category)
   │  site/  (Astro, static output)
   ▼
GitHub Pages: per-patch pages, per-class pages, search page
```

**Recommended stack**
- **Pipeline: Python.** The scraping and conversion scripts are already Python. It uses `markdown-it-py` to parse the Markdown into a tree, and YAML files for the class dictionary and overrides.
- **Site: Astro, static output.** It builds plain HTML pages for each patch and each class, which load fast and work without JavaScript. Interactive parts are small islands of JavaScript.
- **Search: MiniSearch, client-side.** It searches individual change items rather than whole pages, which is what "show me every Hunter change" needs. The index covers about 6k items, roughly 1 MB gzipped or less, and can be split per era if it gets large.
  - Pagefind was the alternative. It's great for searching whole pages, but it indexes pages rather than items, so it can't filter at the item level.
- **Hosting: GitHub Pages** via the official `actions/deploy-pages` workflow. No server, no cost.

## 3. Data model

```jsonc
// patches.json
{ "id": "v2.5b", "version": "2.5.0b", "sortKey": [2,5,0,"b"], "date": "2020-01-20",
  "title": "Patch v2.5b (LIVE)", "era": "2.x", "source": "forum",
  "links": { "archive": "...", "original": "...", "steam": "..." },
  "markdown": "..." }

// changes.json
{ "id": "2.5.0b#0002", "key": "3f9a1c2b7d", "patch": "2.5.0b", "date": "2020-01-20",
  "section": ["Balance", "Balance Changes: Observer"],
  "followUp": null,                                   // set for later replies / re-releases
  "text": "`Follow` has been replaced with `Observe`: ...",   // Markdown
  "plain": "Follow has been replaced with Observe: ...",      // for search
  "classes": ["Observer"], "factions": [],
  "category": "Class Balance", "categorySource": "heading",   // heading | text | mention | kind | fallback | override
  "kind": "change",          // change | summary | explanation | note
  "confidence": "heading" }  // heading | mention | override | none
```

Kinds: `summary` is an overview line repeated in more detail below it. `note` is introduction text or discussion in replies. Search shows `change` and `explanation` by default.

As built, patch ids are the normalised version ("1.0.4a", "2.5.0b"). A release posted twice with different notes (6.0.0c) is one record with `extraParts`. `pipeline/posts.yml` holds per-post corrections: wrong versions on Steam, and posts that aren't patch notes.

**Categories** (every item gets exactly one):
- **Class Balance**: a change to a specific class or ability
- **Game-wide**: rules, mechanics, factions, win conditions, game modes, anything not tied to one class
- **Quality of Life / UI**
- **Bug Fixes**
- **Store & Cosmetics**: armors, portraits, items, Throne Pass
- **Events**: seasonal events, Double GP, anniversaries
- **Technical**: stability, servers, security, platform support
- **Dev Notes**: explanations, previews, community notes

A class-specific bug fix keeps `category: "Bug Fixes"` but is still tagged with that class, so the class filter finds it.

## 4. Pipeline

1. **Ingest and merge.**
   - Load both sources and keep only patch-note posts, using the ✔ rule plus a manual include/exclude list.
   - Parse version strings into sortable keys.
   - Merge duplicate versions: prefer the forum text up to v5.0.2 and Steam after that. Keep links to both.
2. **Segment.**
   - Walk the Markdown tree while tracking the current headings.
   - Treat quoted `Balance Changes: X` labels and bold-only lines (`**Login Screen…:**`) as headings.
   - Each bullet point, or each standalone paragraph in sections without bullets, becomes one change item.
   - Keep "Explained" and "Dev Notes" sections as `kind: explanation`, linked to the changes they explain where the heading names the same class.
3. **Tag classes** from `pipeline/classes.yml`:
   ```yaml
   - name: Aristocrat
     faction: Blue Dragon
     aliases: [Noble, Traitor Noble]
     abilities: [Gossip, Noble Twin]
     retired: null
   ```
   - In order: a class named in the heading wins (`confidence: heading`). Then class or ability names in the item text (`mention`). Ambiguous words such as "King" or "Fool" need word-boundary and context rules.
   - Renamed classes are grouped under their latest name, with the old name shown ("Noble (now Aristocrat)").
4. **Categorise.** Map section headings to categories with keyword rules (`General` → Game-wide, `Bug Fixes` → Bug Fixes, `Store Content` → Store & Cosmetics, …). If the heading doesn't decide it, use keywords in the item text. Untagged items fall back to Game-wide.
5. **Overrides.** `pipeline/overrides.yml` is keyed by a hash of the item text, so it survives re-runs, and can set classes or category for any item.
6. **QA report.** `pipeline/report.md` lists the items to review by hand:
   - untagged or fallback items
   - items with 3 or more classes
   - classes that appear in no patch
   - per-patch item counts compared with the bullet counts in the source

   The target is under 2% of items needing manual review before launch.
7. **Optional AI assist.** For leftover ambiguous items, a one-off script could ask Claude to suggest tags, written into `overrides.yml` for you to review. Not needed for v1.

## 5. Site

| Page | Content |
|---|---|
| **Home / Timeline** | All patches newest-first, grouped by year and era, with item counts by category |
| **Patch page** `/patch/v2-5b/` | The original notes, faithfully rendered, plus a "tagged view" toggle with class and category chips, source links, and previous/next patch |
| **Class page** `/class/hunter/` | Every change to that class across all patches, grouped by version. Shows the faction, old names, and when it was added or retired. Sidebar lists all classes by faction |
| **Search** `/search/` | Full-text search over change items with highlighting. Filter chips for class (multi-select, grouped by faction), faction, category, version range and source. Filter state is kept in the URL (`?class=Hunter&cat=balance&q=bleed`), so searches can be shared |
| **Categories** `/category/game-wide/` | Same view as a class page, for each category |
| **Chronicle** `/chronicle/` | Devblogs, class reveals, events and news, in a separate list with type filters |
| **About** | Sources, how tagging works, an unofficial fan-site disclaimer, and a "report a wrong tag" link (GitHub issue template) |

Other design details:
- Dark theme to match the game.
- Keyboard shortcut `/` focuses the search box.
- Mobile-friendly.
- Version-diff badges such as "Nerf" or "Buff" are out of scope for v1.

## 6. Repository layout

```
/changelogs/            raw sources (already present; treat as read-only input)
/pipeline/              build_data.py, classes.yml, overrides.yml, categories.yml, tests/
/data/                  generated JSON (committed, so the site build doesn't need Python)
/site/                  Astro project (src/pages, src/components, public/)
/.github/workflows/     pages.yml: build site → deploy to GitHub Pages
/.github/ISSUE_TEMPLATE/wrong-tag.yml
README.md, LICENSE, PLAN.md
```

The JSON is committed rather than built in CI. That makes tagging changes reviewable in pull-request diffs and keeps CI to a Node build.

## 7. Milestones

1. **Pipeline MVP.** Ingest, merge, segment and tag `patches.json`/`changes.json`, plus the QA report.
   - Done when every patch version appears exactly once.
   - Done when the item count is within 5% of the bullet count.
   - Done when spot-checks of 1.0.2, 2.1.0, 2.5b, 4.1.0 and 7.0.2 match by eye.
2. **Class dictionary and overrides.** Fill in `classes.yml` (all factions, aliases, main abilities) and clear the QA report to under 2% untagged.
3. **Static site.** Timeline, patch, class and category pages, built from the JSON with no client JavaScript.
4. **Search and filters.** A MiniSearch island with facet filters and URL state.
5. **Deploy.** GitHub Actions workflow to Pages, README, About page, issue template.
6. **Polish.** Mobile layout, search-index size check, Lighthouse score of 90+, and link checking against the archive URLs.

## 8. Risks and decisions

- **Copyright and attribution.** The patch notes are Imperium42's text.
  - Present the site clearly as an unofficial fan archive.
  - Credit and link the original posts.
  - Don't use the official logo or branding.
  - Hotlink images from the archive rather than re-hosting them, or drop them.
- **Fragile sources.** fol-archive.netlify.app could go away. The raw HTML is already saved under `changelogs/forum/raw_html/`, so the pipeline never needs the network.
- **Tagging accuracy** is the main quality risk. Mitigated by the heading-first rules, the QA report, overrides, and the "report a wrong tag" link.

## 9. Decisions (2026-11-24)

1. **Stack: Astro.** It produces the leanest static output: plain HTML, near-zero JavaScript except the search island.
2. **Non-patch posts get their own section, "Chronicle"** (`/chronicle/`). It holds devblogs, class reveals, events and other announcements, kept separate from patch notes and their filters. Its posts are tagged by type (Devblog, Class Reveal, Event, News) and, where obvious, by class, so a class page can link to its reveal. Chronicle posts are searchable, but turned off by default in the filters.
3. **Renamed classes are grouped under their newest name**, with former names listed and searchable.
4. **Name: Edicts.** Repo `tol-edicts`, site at `<user>.github.io/tol-edicts`. No tagline. The header just says "Edicts", and the About page says plainly that it's an unofficial archive of Throne of Lies patch notes.

## 10. Design direction

It should look like a site a fan put together by hand, something like an old wiki or a project's changelog page. It should not look like a product landing page or a dark "dev tool" theme.

- **Plain document look.** White background, black text, system fonts, normal underlined links in the browser's usual blue and purple. A dark version only when the visitor's system asks for it, using the same plain approach.
- **No decoration for its own sake.** No hero section, gradients, rounded card grids, glows, emoji, icon sets, or custom accent palette. Borders and spacing do the structuring.
- **Tables and lists.** Patch lists and class histories are ordinary tables and lists. Version numbers are plain text. Class and category tags are small bracketed links, not coloured pills.
- **Copy.** Short and literal ("Patches", "Classes", "Search"). No marketing phrasing, slogans or "explore"-style buttons.
- **Useful bits only.**
  - `/` focuses search.
  - Filters are kept in the URL, so a filtered search can be linked.
  - Every page except search works without JavaScript.
- **Size.** Content pages ship no JavaScript. The search page loads its index when it opens.

# Edicts

A static site for reading Throne of Lies patch notes (2016–2023) by patch, by class or by category. Each patch is split into its individual changes, and each change is tagged.

This is an unofficial fan archive. Throne of Lies and its patch notes belong to Imperium42; the site quotes the notes and links each one back to its original post.

## Layout

| Folder | What's in it |
|---|---|
| `changelogs/` | The source posts as Markdown, from the official forum (via the Forum of Lies archive) and Steam, plus the raw downloads. Treated as read-only. |
| `pipeline/` | Python that turns the posts into tagged data, plus the hand-edited class list, category rules and corrections. |
| `data/` | The generated JSON the site is built from. Committed, so building the site doesn't need Python. |
| `site/` | The Astro site. |

## Rebuilding

Data (Python 3.11 or newer):

```sh
python -m venv .venv
.venv/bin/pip install -r pipeline/requirements.txt      # Windows: .venv\Scripts\pip
.venv/bin/python pipeline/build_data.py
.venv/bin/python -m pytest pipeline/tests -q
```

`build_data.py` rewrites `data/*.json` and `pipeline/report.md`. The report lists anything that needs a look, such as untagged changes or classes without a faction.

Site (Node 24):

```sh
cd site
npm ci
npm run build      # output in site/dist
npm run preview    # http://localhost:4321/tol-edicts/
```

Images in patch notes are rendered as `[image]` links to the original files (see `renderMarkdown` in `site/src/lib/data.js`); Chronicle pages show them inline.

## Fixing a wrong tag

Find the change in `data/changes.json` and copy its `key`, then add a line to `pipeline/overrides.yml`:

```yaml
3f9a1c2b7d: {classes: [Poacher], category: Class Balance}
```

The fields are `classes` (replaces the classes), `addClasses`, `category`, `kind` (`change`, `explanation`, `summary` or `note`) and `drop: true`. If a rule is wrong for many changes, fix it in `pipeline/categories.yml` or `pipeline/classes.yml` instead. Then rebuild the data and commit `data/` with your change.

Class facts (faction, converts, former names, abilities) are in `pipeline/classes.yml`. Entries marked `verified: false` are guesses that still need checking.

## Publishing

`.github/workflows/pages.yml` builds `site/` and deploys it to GitHub Pages on every push to `main`. In the repository settings, under Pages, set the source to GitHub Actions. The workflow works out the site's address and base path itself.

## Licence

The code is under the MIT licence (see `LICENSE`). The patch notes, announcements and images are Imperium42's and are not covered by it.

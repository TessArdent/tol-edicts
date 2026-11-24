# Throne of Lies changelogs

Collected 2026-11-24 from two sources that overlap and complement each other.

| Folder | Source | Covers | Notes |
|---|---|---|---|
| [`forum/`](forum/README.md) | Forum of Lies archive (<https://fol-archive.netlify.app/>), a static mirror of the official forum (forum.imperium42.com / forum.throneoflies.com) | Feb 2016 – Sep 2021 (pre-alpha, 0.8.24 → v5.0.2) | 221 topics: the whole "Official Announcements" category plus 3 patch threads filed elsewhere (v2.3, v2.4a, v5.0.2). 106 are patch notes (✔ in the index). Each file has the opening post plus follow-ups by the author or staff. Raw archived HTML is in `forum/raw_html/`. |
| [`steam/`](steam/README.md) | Steam News API, app 595280 | Apr 2017 – Jan 2023 (launch → v7.3.2b) | 162 unique posts (exact duplicates dropped). The only source after Sep 2021 (v5.0.2b onward, v6.x, v7.x). From 2018 to 2020 many posts are short summaries linking to the full forum notes, which are in `forum/`. Raw API response is in `steam/steam_news_raw.json`. |

For a given version, prefer the forum copy up to v5.0.2 (fuller text) and the Steam copy after that.

Known gaps:
- Two Steam posts contain broken `[url=]` tags in the original.
- Steam-only posts such as some hotfixes (for example v4.1.5f, v5.0.1b) have no forum counterpart, and the reverse.

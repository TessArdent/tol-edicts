"""Load the exported Markdown posts and decide what each one is.

Each file in changelogs/{forum,steam}/posts starts with a small header:

    # Title
    - Date: 2017-10-06 17:17 UTC
    - Author: ...
    - Original: https://...
    ---
    body...
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .versions import Version, find_versions, parse_version

_HEADER_FIELD = re.compile(r"^- ([A-Za-z ]+): (.*)$")


@dataclass
class Post:
    key: str            # file stem, used by posts.yml
    source: str         # "forum" or "steam"
    title: str
    date: str           # YYYY-MM-DD
    datetime: str       # as written in the header
    author: str
    links: dict         # original / archive / steam
    body: str
    feed: str = ""
    kind: str = ""      # patch | chronicle | skip
    type: str = ""      # chronicle type, or skip reason
    versions: list[Version] = field(default_factory=list)


def load_posts(root: Path) -> list[Post]:
    posts = []
    for source in ("forum", "steam"):
        for path in sorted((root / source / "posts").glob("*.md")):
            posts.append(_parse_file(path, source))
    return posts


def _parse_file(path: Path, source: str) -> Post:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    title = lines[0].removeprefix("# ").strip()
    meta: dict[str, str] = {}
    body_start = len(lines)
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body_start = i + 1
            break
        m = _HEADER_FIELD.match(line)
        if m:
            meta[m.group(1).strip().lower()] = m.group(2).strip()
    dt = meta.get("date", "")
    links = {}
    if source == "forum":
        links["archive"] = meta.get("archived copy", "")
        links["original"] = meta.get("original", "")
    else:
        links["steam"] = meta.get("original", "")
    return Post(
        key=path.stem,
        source=source,
        title=title,
        date=dt[:10],
        datetime=dt,
        author=meta.get("author", ""),
        links=links,
        body="\n".join(lines[body_start:]).strip() + "\n",
        feed=meta.get("feed", ""),
    )


# ---- classification ---------------------------------------------------------

_NOT_A_PATCH = re.compile(
    r"preview|test realm|coming soon|revert|arriving soon|known bugs|poll|devblog|dev plans",
    re.I)
_PATCH_WORD = re.compile(r"\b(patch|hotfix|notes)\b", re.I)

# Chronicle types, tried in order. Anything unmatched is "News".
_CHRONICLE_RULES = [
    ("Devblog", r"\b(devblog|dev plans|developer update|future of|behind the|dev update)\b"),
    ("Class Reveal", r"\b(introducing|reveal(ed)?|new neutral|portraits?|has arrived in the court"
                     r"|art spotlight|unlockable class|alpha classes)\b"),
    ("Preview", r"\b(preview of|test realm)\b|\bv\d.*coming soon"),
    ("Event", r"\b(events?|festival|contests?|giveaway|raffle|weekend|double|anniversary"
              r"|jingle jam|april fools|screenshot (challenge|winners)|winners)\b"),
]

# Forum housekeeping and policy posts are left out of the site entirely.
_SITE_RULES = re.compile(
    r"forum|privacy|terms of service|rules|categor|ssl|https|\btheme\b|report|suspended"
    r"|moderation|discord >|regist|profile field|thronepass|patreon|signatures|badges/"
    r"|off-topic|flag|swearing|edit time|icons for new|maintenance|welcome to|attributions"
    r"|restriction removal|reply to announcements|added color|paypal|cc attributions"
    r"|symbol of|imperium42\.com may be|throneoflies\.com may be|newsletter", re.I)


def classify(post: Post, overrides: dict) -> None:
    """Set post.kind, post.type and post.versions."""
    ov = overrides.get(post.key, {})
    if post.feed and post.feed.lower() not in ("community announcements", "announcement", ""):
        post.kind, post.type = "skip", f"third-party feed: {post.feed}"
    elif "kind" in ov:
        post.kind = ov["kind"]
        post.type = ov.get("type", "")
    else:
        post.kind, post.type = _auto_kind(post)
    if post.kind == "patch":
        if "version" in ov:
            vs = ov["version"]
            post.versions = [parse_version(v) for v in (vs if isinstance(vs, list) else [vs])]
        else:
            post.versions = find_versions(post.title)
    if post.kind == "chronicle" and not post.type:
        post.type = _chronicle_type(post.title)


def _auto_kind(post: Post) -> tuple[str, str]:
    t = post.title
    if _NOT_A_PATCH.search(t):
        return "chronicle", ""
    if find_versions(t) or _PATCH_WORD.search(t):
        return "patch", ""
    if _SITE_RULES.search(t) and not re.search(r"event", t, re.I):
        return "skip", "forum housekeeping"
    return "chronicle", ""


def _chronicle_type(title: str) -> str:
    for name, pattern in _CHRONICLE_RULES:
        if re.search(pattern, title, re.I):
            return name
    return "News"

"""Build data/*.json and pipeline/report.md from changelogs/.

    python pipeline/build_data.py            # from the repo root

Reads only local files. See PLAN.md sections 3 and 4.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

from edicts.merge import build_patches  # noqa: E402
from edicts.posts import classify, load_posts  # noqa: E402
from edicts.report import write_report  # noqa: E402
from edicts.segment import count_top_level_bullets, segment  # noqa: E402
from edicts.tagging import Tagger  # noqa: E402

PIPE = ROOT / "pipeline"
DATA = ROOT / "data"


def load_yaml(name: str):
    with open(PIPE / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def item_key(patch_id: str, plain: str, seen: Counter) -> str:
    h = hashlib.sha1(f"{patch_id}\n{plain}".encode("utf-8")).hexdigest()[:10]
    seen[h] += 1
    return h if seen[h] == 1 else f"{h}-{seen[h]}"


def collect_items(patch):
    """Items of every part of a patch record, plus the source bullet count.

    Text before any heading or list is an introduction ("intro-note") when the
    part has a list, and a change when it doesn't (short Steam posts are often
    a single sentence). Repeated text, e.g. a list re-posted in a later reply,
    is kept once.
    """
    items, bullets = [], 0
    for n, post in enumerate([patch.primary, *patch.extra_parts]):
        part = segment(post.body)
        has_list = any(it.origin == "list" for it in part)
        for it in part:
            if it.origin == "intro":
                it.origin = "intro-note" if has_list else "paragraph"
            if n:
                it.follow_up = it.follow_up or {"author": post.author, "date": post.date,
                                                "title": post.title, "rerelease": True}
        items += part
        bullets += count_top_level_bullets(post.body)
    seen_text: set[str] = set()
    unique = []
    for it in items:
        norm = " ".join(it.plain.lower().split())
        if norm in seen_text:
            if it.origin == "list":
                bullets -= 1        # a repeated bullet is still one change
            continue
        seen_text.add(norm)
        unique.append(it)
    return unique, bullets


def is_mostly_cjk(text: str) -> bool:
    """Chinese-only sections repeat the English notes; they're kept as notes."""
    letters = [ch for ch in text if ch.isalpha()]
    cjk = sum(1 for ch in letters if "㐀" <= ch <= "鿿")
    return bool(letters) and cjk / len(letters) > 0.3


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9']+", text.lower()) if len(w) > 2}


def demote_unmatched_summaries(tagged) -> None:
    """Keep kind "summary" only where a detailed item says the same thing.

    Overview lists usually repeat changes described further down, so they are
    hidden from search by default. But some posts (e.g. 4.1.0) mention a change
    only in the highlights, and that one has to stay visible.
    """
    details = [_words(it.plain) for it, tags in tagged if tags["kind"] == "change"]
    for it, tags in tagged:
        if tags["kind"] != "summary":
            continue
        w = _words(it.plain)
        if len(w) <= 2:
            continue                      # "QoL", "Bug fixes": headers, leave as summary
        best = max((len(w & d) / len(w) for d in details if d), default=0)
        if best < 0.6:
            tags["kind"] = "change"


def class_summary(classes: list[dict], changes: list[dict], patches: list[dict]) -> list[dict]:
    """classes.yml plus what the data says: first/last patch mentioned, counts,
    and the converts of each class (the reverse of convertOf)."""
    order = {p["id"]: i for i, p in enumerate(patches)}
    seen: dict[str, list[str]] = {}
    counts: Counter = Counter()
    for c in changes:
        if c["kind"] in ("change", "explanation"):
            for cls in c["classes"]:
                counts[cls] += 1
                seen.setdefault(cls, []).append(c["patch"])
    out = []
    for c in classes:
        rec = {k: v for k, v in c.items() if k != "notes"}
        rec["verified"] = c.get("verified", True)
        rec["notes"] = c.get("notes", "")
        ps = sorted(set(seen.get(c["name"], [])), key=order.get)
        rec["firstSeen"], rec["lastSeen"] = (ps[0], ps[-1]) if ps else (None, None)
        rec["changeCount"] = counts[c["name"]]
        rec["converts"] = [o["name"] for o in classes if o.get("convertOf") == c["name"]]
        for k in ("added", "retired"):
            if k in rec and rec[k] is not None:
                rec[k] = str(rec[k])
        out.append(rec)
    return out


def post_ref(p) -> dict:
    return {"source": p.source, "key": p.key, "title": p.title, "date": p.date,
            "author": p.author, **{k: v for k, v in p.links.items() if v}}


def main() -> int:
    post_overrides = load_yaml("posts.yml")
    item_overrides = load_yaml("overrides.yml")
    class_data = load_yaml("classes.yml")
    classes = class_data["classes"]
    tagger = Tagger(class_data, load_yaml("categories.yml"))

    posts = load_posts(ROOT / "changelogs")
    known = {p.key for p in posts}
    problems = [f"posts.yml: no post named {k}" for k in post_overrides if k not in known]
    for p in posts:
        classify(p, post_overrides)

    patch_posts = [p for p in posts if p.kind == "patch"]
    patches, merge_notes = build_patches(patch_posts)

    patch_records, change_records, bullet_checks = [], [], []
    used_overrides: set[str] = set()
    for patch in patches:
        post = patch.primary
        items, bullets = collect_items(patch)
        tagged = []
        for it in items:
            note = it.is_reply_text or it.origin == "intro-note" or is_mostly_cjk(it.plain)
            tagged.append((it, tagger.tag(it.section, it.plain, patch.version,
                                          kind="note" if note else None)))
        demote_unmatched_summaries(tagged)
        seen: Counter = Counter()
        n_list = kept = 0
        for it, tags in tagged:
            key = item_key(patch.id, it.plain, seen)
            ov = item_overrides.get(key)
            if ov:
                used_overrides.add(key)
                if ov.get("drop"):
                    continue
                if "classes" in ov:
                    tags["classes"] = list(ov["classes"])
                for c in ov.get("addClasses", []):
                    if c not in tags["classes"]:
                        tags["classes"].append(c)
                if "category" in ov:
                    tags["category"], tags["categorySource"] = ov["category"], "override"
                if "kind" in ov:
                    tags["kind"] = ov["kind"]
                    if ov["kind"] in ("note", "explanation") and "category" not in ov:
                        tags["category"], tags["categorySource"] = "Dev Notes", "override"
                tags["confidence"] = "override"
            if it.origin == "list":
                n_list += 1
            kept += 1
            change_records.append({
                "id": f"{patch.id}#{kept:04d}",
                "key": key,
                "patch": patch.id,
                "date": post.date,
                "section": it.section,
                "followUp": it.follow_up,
                "text": it.markdown,
                "plain": it.plain,
                "origin": it.origin,
                **tags,
            })
        bullet_checks.append((patch.id, bullets, n_list))
        v = patch.version
        patch_records.append({
            "id": patch.id,
            "version": str(v) if v else None,
            "versions": [str(x) for x in patch.versions],
            "sortKey": v.sort_key if v else None,
            "major": v.major if v else None,
            "date": post.date,
            "title": post.title,
            "source": post.source,
            "primary": post_ref(post),
            "alsoPosted": [post_ref(o) for o in sorted(patch.others, key=lambda o: o.datetime)],
            "markdown": post.body,
            "extraParts": [{"post": post_ref(e), "markdown": e.body} for e in patch.extra_parts],
            "itemCount": kept,
        })

    for ov in set(item_overrides) - used_overrides:
        problems.append(f"overrides.yml: no item with key {ov}")

    classes_out = class_summary(classes, change_records, patch_records)

    chronicle = []
    for p in sorted((p for p in posts if p.kind == "chronicle"), key=lambda p: p.datetime):
        cls, _ = tagger.mentions(p.title, None)
        chronicle.append({"id": p.key, "type": p.type, "date": p.date, "title": p.title,
                          "classes": cls, "post": post_ref(p), "markdown": p.body})
    chronicle = _dedupe_chronicle(chronicle)

    DATA.mkdir(exist_ok=True)
    for name, obj in (("patches", patch_records), ("changes", change_records),
                      ("chronicle", chronicle), ("classes", classes_out)):
        (DATA / f"{name}.json").write_text(
            json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    write_report(PIPE / "report.md", posts=posts, patches=patch_records,
                 changes=change_records, chronicle=chronicle, classes=classes,
                 merge_notes=merge_notes, bullet_checks=bullet_checks, problems=problems)
    print(f"{len(patch_records)} patches, {len(change_records)} changes, "
          f"{len(chronicle)} chronicle posts; report in pipeline/report.md")
    for p in problems:
        print("WARNING:", p)
    return 1 if problems else 0


def _dedupe_chronicle(entries: list[dict]) -> list[dict]:
    """Same title on both sources: keep the forum copy, note the Steam link."""
    out: list[dict] = []
    by_title: dict[str, dict] = {}
    for e in entries:
        k = "".join(ch for ch in e["title"].lower() if ch.isalnum())
        if k in by_title:
            first = by_title[k]
            keep, drop = (first, e) if first["post"]["source"] == "forum" else (e, first)
            keep.setdefault("alsoPosted", []).append(drop["post"])
            if drop in out:
                out.remove(drop)
                out.append(keep)
            by_title[k] = keep
            continue
        by_title[k] = e
        out.append(e)
    out.sort(key=lambda e: e["date"])
    return out


if __name__ == "__main__":
    raise SystemExit(main())

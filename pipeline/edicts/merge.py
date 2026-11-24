"""Group patch posts that describe the same release and pick the text to use.

Posts sharing any version are one group, and one group is one record. Inside
a group the forum copy is preferred (it's the full text up to v5.0.2; Steam
often just links to it), unless the Steam copy is much longer. Other posts in
the group from the same source, on another day and with a real body of their
own (at least STANDALONE_RATIO of the primary's length) are kept as extra
parts of the record: v6.0.0c was released, reverted and released again a week
later with different notes. The rest are kept as links only.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .posts import Post
from .versions import Version

STANDALONE_RATIO = 0.4
STEAM_OVER_FORUM = 1.67


@dataclass
class Patch:
    id: str
    versions: list[Version]
    primary: Post
    others: list[Post] = field(default_factory=list)     # linked only
    extra_parts: list[Post] = field(default_factory=list)  # text kept, after primary

    @property
    def version(self) -> Version | None:
        return self.versions[0] if self.versions else None


def _size(p: Post) -> int:
    return len(p.body)


def group_patches(posts: list[Post]) -> list[list[Post]]:
    """Union posts that share a version. Versionless posts stay alone."""
    groups: list[list[Post]] = []
    by_version: dict[Version, int] = {}
    for p in sorted(posts, key=lambda p: p.datetime):
        hits = sorted({by_version[v] for v in p.versions if v in by_version})
        if not hits:
            groups.append([p])
            gi = len(groups) - 1
        else:
            gi = hits[0]
            groups[gi].append(p)
            for other in hits[1:]:                  # bridge: merge later groups in
                groups[gi].extend(groups[other])
                groups[other] = []
                for v, idx in list(by_version.items()):
                    if idx == other:
                        by_version[v] = gi
        for v in p.versions:
            by_version[v] = gi
    return [g for g in groups if g]


def build_patches(posts: list[Post]) -> tuple[list[Patch], list[str]]:
    notes: list[str] = []
    patches: list[Patch] = []
    for group in group_patches(posts):
        forum = sorted([p for p in group if p.source == "forum"], key=_size, reverse=True)
        steam = sorted([p for p in group if p.source == "steam"], key=_size, reverse=True)
        primary = forum[0] if forum else steam[0]
        if forum and steam and _size(steam[0]) > STEAM_OVER_FORUM * _size(forum[0]):
            primary = steam[0]
            notes.append(f"{primary.key}: Steam text used, forum copy much shorter")
        rest = [p for p in group if p is not primary]
        standalone = [p for p in rest if p.source == primary.source
                      and p.date != primary.date
                      and _size(p) >= STANDALONE_RATIO * _size(primary)]
        standalone.sort(key=lambda p: p.datetime)
        links = [p for p in rest if p not in standalone]
        versions = sorted({v for p in group for v in p.versions})
        patches.append(Patch(id="", versions=versions, primary=primary, others=links,
                             extra_parts=standalone))
        if standalone:
            notes.append(f"{primary.key}: text of {len(standalone)} later same-version post(s) "
                         f"kept as extra parts: {', '.join(p.key for p in standalone)}")
    _assign_ids(patches)
    return patches, notes


def _assign_ids(patches: list[Patch]) -> None:
    patches.sort(key=lambda p: (p.primary.datetime, p.versions))
    used: set[str] = set()
    for p in patches:
        base = str(p.versions[0]) if p.versions else p.primary.date
        pid, n = base, 2
        while pid in used:
            pid = f"{base}-{n}"
            n += 1
        used.add(pid)
        p.id = pid

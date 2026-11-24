"""Tag change items with classes, factions, category and kind.

Order of evidence:
1. overrides.yml (keyed by item key) wins outright.
2. A heading or label that names only classes ("## Alchemist:", "> Balance
   Changes: Mercenary + Sellsword") tags every item under it.
3. Class, alias and ability names in the item text add more tags.
Category comes from the innermost heading that matches a category rule, then
from the item text, then from whether any class was tagged.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .versions import Version, parse_version

FACTIONS = ["Blue Dragon", "Unseen", "Cult", "Neutral"]
FACTION_ALIASES = {"BD": "Blue Dragon", "Neutrals": "Neutral"}

CATEGORIES = ["Class Balance", "Game-wide", "Quality of Life / UI", "Bug Fixes",
              "Store & Cosmetics", "Events", "Technical", "Dev Notes"]

# Words that may sit next to class names in a heading without making it
# anything other than a class heading.
_HEADING_FILLER = re.compile(
    r"\b(balance|changes?|rework(ed)?|revamp(ed)?|class(es)?|retired|new|buffs?|nerfs?|fixes?"
    r"|updates?|and|the|tweaks?|adjustments?|minor|major|starting|abilities|ability|roles?)\b"
    r"|[+&/,:;()\-–—|.!]", re.I)


@dataclass
class Tagger:
    class_data: dict            # classes.yml: {"classes": [...], "ignore": [...]}
    category_rules: dict
    classes: list[dict] = field(init=False)
    names: dict = field(init=False)          # name, alias or former name -> class
    abilities: dict = field(init=False)      # ability -> [classes]
    _mention_re: re.Pattern = field(init=False)

    def __post_init__(self) -> None:
        self.classes = self.class_data["classes"]
        ignore = set(self.class_data.get("ignore", []))
        self.names, self.abilities = {}, {}
        self.added: dict[str, Version] = {}
        for c in self.classes:
            forms = [c["name"], *c.get("aliases", []),
                     *(f["name"] for f in c.get("formerNames", []))]
            for n in forms:
                self.names[n] = c["name"]
            for a in c.get("abilities", []):
                self.abilities.setdefault(a, []).append(c["name"])
            if c.get("added"):
                self.added[c["name"]] = parse_version(str(c["added"]))
        forms = (list(self.names) + list(self.abilities) + FACTIONS + list(FACTION_ALIASES)
                 + list(ignore))
        forms.sort(key=len, reverse=True)       # longest first: "Death Knight" before "Knight"
        alt = "|".join(re.escape(f) for f in forms)
        self._ignore = ignore
        self._mention_re = re.compile(rf"(?<![\w-])({alt})(?:s|'s|’s|')?(?![\w-])")
        self._cat = {k: [re.compile(p, re.I) for p in v.get("headings", [])]
                     for k, v in self.category_rules["categories"].items()}
        self._cat_text = {k: [re.compile(p, re.I) for p in v.get("text", [])]
                          for k, v in self.category_rules["categories"].items()}
        self._kind = {k: re.compile(p, re.I) for k, p in self.category_rules["kinds"].items()}
        self.faction_of = {c["name"]: c.get("faction") for c in self.classes}

    def _exists(self, cls: str, version: Version | None) -> bool:
        """False for a class mentioned before the patch that added it."""
        added = self.added.get(cls)
        return not (added and version and version < added)

    # -- mentions --------------------------------------------------------
    def mentions(self, text: str, version: Version | None = None,
                 abilities: bool = True) -> tuple[list[str], list[str]]:
        """Classes and factions named in text, in first-seen order.

        With abilities=False, ability names don't count: under a class heading
        an ability usually belongs to that class, even if it later moved to
        another one (Exhume was the Physician's in 0.8.24, later Herbalist's).
        """
        classes: list[str] = []
        factions: list[str] = []
        for m in self._mention_re.finditer(text):
            word = m.group(1)
            if word in self._ignore:
                continue
            if word in self.names:
                found = [self.names[word]]
            elif word in self.abilities:
                if not abilities:
                    continue
                found = self.abilities[word]
            elif word in FACTIONS:
                self._add(factions, word)
                continue
            elif word in FACTION_ALIASES:
                self._add(factions, FACTION_ALIASES[word])
                continue
            else:
                continue
            for cls in found:
                if self._exists(cls, version):
                    self._add(classes, cls)
        return classes, factions

    @staticmethod
    def _add(lst: list, v) -> None:
        if v not in lst:
            lst.append(v)

    def heading_classes(self, heading: str) -> list[str]:
        """Classes a heading is *about*, or [] if it is about something else."""
        found: list[str] = []
        rest = heading
        for m in sorted(self._name_spans(heading), key=lambda s: s[0], reverse=True):
            start, end, cls = m
            self._add(found, cls)
            rest = rest[:start] + " " + rest[end:]
        if not found:
            return []
        if _HEADING_FILLER.sub(" ", rest).strip():
            return []
        found.reverse()
        return found

    def _name_spans(self, text: str):
        for m in self._mention_re.finditer(text):
            w = m.group(1)
            if w in self.names and w not in self._ignore:
                yield (m.start(), m.end(), self.names[w])

    # -- categories --------------------------------------------------------
    def heading_category(self, heading: str) -> str | None:
        order = [c for c in self._cat if c != "Game-wide"] + ["Game-wide"]
        for cat in order:
            if any(p.search(heading) for p in self._cat.get(cat, [])):
                return cat
        return None

    def text_category(self, text: str) -> str | None:
        """First category whose text rules match. Game-wide's rules are broad,
        so they are tried last."""
        order = [c for c in self._cat_text if c != "Game-wide"] + ["Game-wide"]
        for cat in order:
            if any(p.search(text) for p in self._cat_text.get(cat, [])):
                return cat
        return None

    def kind_of(self, section: list[str]) -> str:
        for heading in reversed(section):
            for kind, pat in self._kind.items():
                if pat.search(heading):
                    return kind
        return "change"

    def tag(self, section: list[str], text: str, version: Version | None = None,
            kind: str | None = None) -> dict:
        """Tags for one item. `kind` forces the kind (the build passes "note"
        for introductions and replies)."""
        heading_cls: list[str] = []
        heading_cat: str | None = None
        cls_depth = cat_depth = None                   # 0 = innermost heading
        for depth, h in enumerate(reversed(section)):
            hc = [c for c in self.heading_classes(h) if self._exists(c, version)]
            if hc and not heading_cls:
                heading_cls, cls_depth = hc, depth
            elif not hc and heading_cat is None:
                heading_cat = self.heading_category(h)
                if heading_cat:
                    cat_depth = depth
        if heading_cls and heading_cat in ("Events", "Store & Cosmetics") \
                and cls_depth < cat_depth:
            # "Anniversary Update With New Classes!" > "Chronomancer": the class
            # heading is the more specific one
            heading_cat = "Class Balance"
        text_cls, factions = self.mentions(text, version, abilities=not heading_cls)
        classes = list(heading_cls)
        for c in text_cls:
            self._add(classes, c)
        for c in classes:
            f = self.faction_of.get(c)
            if f in FACTIONS:
                self._add(factions, f)

        kind = kind or self.kind_of(section)
        starts_fix = bool(re.match(r"\s*(fixed|fixes|fix|bug ?fix(es)?)\b", text, re.I))
        if kind in ("explanation", "note"):
            category, how = "Dev Notes", "kind"
        elif heading_cat in (None, "Class Balance", "Game-wide") and starts_fix:
            category, how = "Bug Fixes", "text"
        elif heading_cls and heading_cat in ("Class Balance", "Game-wide"):
            # "## Mechanics" > "Alchemist": the class label is more specific
            category, how = "Class Balance", "heading"
        elif heading_cat == "Class Balance":
            category, how = ("Class Balance", "heading") if classes else ("Game-wide", "heading")
        elif heading_cat == "Game-wide":
            # "## General" held everything in early notes: clearer text evidence wins
            tc = self.text_category(text)
            if tc and tc != "Game-wide":
                category, how = tc, "text"
            else:
                category, how = "Game-wide", "heading"
        elif heading_cat:
            category, how = heading_cat, "heading"
        elif heading_cls:
            category, how = "Class Balance", "heading"
        else:
            tc = self.text_category(text)
            if tc == "Game-wide" and classes:
                category, how = "Class Balance", "mention"
            elif tc:
                category, how = tc, "text"
            elif classes:
                category, how = "Class Balance", "mention"
            else:
                category, how = "Game-wide", "fallback"
        if category in ("Store & Cosmetics", "Events") and not heading_cls:
            # "Neon Dynasty Knight" is an armour, "Grim Reaper" an outfit:
            # a class name inside a cosmetic isn't a change to that class.
            classes, factions = [], []
        confidence = "heading" if heading_cls else ("mention" if classes else "none")
        return {"classes": classes, "factions": factions, "category": category,
                "categorySource": how, "kind": kind, "confidence": confidence}

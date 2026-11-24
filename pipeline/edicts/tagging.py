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

FACTIONS = ["Blue Dragon", "Unseen", "Cult", "Neutral"]
FACTION_ALIASES = {"BD": "Blue Dragon", "Neutrals": "Neutral"}

CATEGORIES = ["Class Balance", "Game-wide", "Quality of Life / UI", "Bug Fixes",
              "Store & Cosmetics", "Events", "Technical", "Dev Notes"]

# Words that may sit next to class names in a heading without making it
# anything other than a class heading.
_HEADING_FILLER = re.compile(
    r"\b(balance|changes?|rework(ed)?|revamp(ed)?|class(es)?|retired|new|buffs?|nerfs?|fixes?"
    r"|updates?|and|the|tweaks?|adjustments?|minor|major|starting|abilities|ability)\b"
    r"|[+&/,:;()\-–—|.!]", re.I)


@dataclass
class Tagger:
    classes: list[dict]
    category_rules: dict
    names: dict = field(init=False)          # surface form -> canonical class
    abilities: dict = field(init=False)      # ability -> canonical class
    _mention_re: re.Pattern = field(init=False)

    def __post_init__(self) -> None:
        self.names, self.abilities = {}, {}
        for c in self.classes:
            for n in [c["name"], *c.get("aliases", [])]:
                self.names[n] = c["name"]
            for a in c.get("abilities", []):
                self.abilities[a] = c["name"]
        forms = list(self.names) + list(self.abilities) + FACTIONS + list(FACTION_ALIASES)
        forms.sort(key=len, reverse=True)       # longest first: "Death Knight" before "Knight"
        alt = "|".join(re.escape(f) for f in forms)
        self._mention_re = re.compile(rf"(?<![\w-])({alt})(?:s|'s|’s|')?(?![\w-])")
        self._cat = {k: [re.compile(p, re.I) for p in v.get("headings", [])]
                     for k, v in self.category_rules["categories"].items()}
        self._cat_text = {k: [re.compile(p, re.I) for p in v.get("text", [])]
                          for k, v in self.category_rules["categories"].items()}
        self._kind = {k: re.compile(p, re.I) for k, p in self.category_rules["kinds"].items()}
        self.faction_of = {c["name"]: c.get("faction") for c in self.classes}

    # -- mentions --------------------------------------------------------
    def mentions(self, text: str) -> tuple[list[str], list[str]]:
        """Classes and factions named in text, in first-seen order."""
        classes: list[str] = []
        factions: list[str] = []
        for m in self._mention_re.finditer(text):
            word = m.group(1)
            if word in self.names:
                self._add(classes, self.names[word])
            elif word in self.abilities:
                self._add(classes, self.abilities[word])
            elif word in FACTIONS:
                self._add(factions, word)
            elif word in FACTION_ALIASES:
                self._add(factions, FACTION_ALIASES[word])
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
            if w in self.names:
                yield (m.start(), m.end(), self.names[w])

    # -- categories --------------------------------------------------------
    def heading_category(self, heading: str) -> str | None:
        for cat, pats in self._cat.items():
            if any(p.search(heading) for p in pats):
                return cat
        return None

    def text_category(self, text: str) -> str | None:
        for cat, pats in self._cat_text.items():
            if any(p.search(text) for p in pats):
                return cat
        return None

    def kind_of(self, section: list[str]) -> str:
        for heading in reversed(section):
            for kind, pat in self._kind.items():
                if pat.search(heading):
                    return kind
        return "change"

    def tag(self, section: list[str], text: str) -> dict:
        heading_cls: list[str] = []
        heading_cat: str | None = None
        for h in reversed(section):                    # innermost first
            hc = self.heading_classes(h)
            if hc and not heading_cls:
                heading_cls = hc
            elif not hc and heading_cat is None:
                heading_cat = self.heading_category(h)
        text_cls, factions = self.mentions(text)
        classes = list(heading_cls)
        for c in text_cls:
            self._add(classes, c)
        for c in classes:
            f = self.faction_of.get(c)
            if f:
                self._add(factions, f)

        kind = self.kind_of(section)
        starts_fix = bool(re.match(r"\s*(fixed|fixes|fix|bug ?fix(es)?)\b", text, re.I))
        if kind == "explanation":
            category, how = "Dev Notes", "kind"
        elif heading_cat in (None, "Class Balance", "Game-wide") and starts_fix:
            category, how = "Bug Fixes", "text"
        elif heading_cls and heading_cat in ("Class Balance", "Game-wide"):
            # "## Mechanics" > "Alchemist": the class label is more specific
            category, how = "Class Balance", "heading"
        elif heading_cat == "Class Balance":
            category, how = ("Class Balance", "heading") if classes else ("Game-wide", "heading")
        elif heading_cat:
            category, how = heading_cat, "heading"
        elif heading_cls:
            category, how = "Class Balance", "heading"
        else:
            tc = self.text_category(text)
            if tc:
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

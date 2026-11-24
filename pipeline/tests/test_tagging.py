def test_longest_name_wins(tagger):
    classes, _ = tagger.mentions("The Death Knight and the Psycho King both changed; Knight too.")
    assert classes == ["Death Knight", "Psycho King", "Knight"]


def test_possessive_plural_and_case(tagger):
    classes, _ = tagger.mentions("Assassins share uses. The King's Allies changed. a fool's errand")
    assert classes == ["Assassin", "King"]


def test_abilities_and_factions(tagger):
    classes, factions = tagger.mentions("Nightshade now has 2 uses. Unseen and BD win together.")
    assert classes == ["Assassin"] and factions == ["Unseen", "Blue Dragon"]


def test_heading_classes(tagger):
    assert tagger.heading_classes("Alchemist") == ["Alchemist"]
    assert tagger.heading_classes("Balance Changes: Mercenary + Sellsword") == ["Mercenary", "Sellsword"]
    assert tagger.heading_classes("Fool & Scorned") == ["Fool", "Scorned"]
    assert tagger.heading_classes("Noble unable to use Gossip on the King") == []
    assert tagger.heading_classes("Bug Fixes") == []


def test_class_heading_under_bug_fixes(tagger):
    t = tagger.tag(["Bug Fixes", "Hunter"], "Wolf no longer attacks twice.")
    assert t["category"] == "Bug Fixes" and t["classes"] == ["Hunter"]


def test_class_label_beats_outer_general_heading(tagger):
    t = tagger.tag(["Mechanics", "Alchemist"], "Emerald Potion has 2 uses.")
    assert t["category"] == "Class Balance" and t["confidence"] == "heading"


def test_fixed_under_class_heading_is_bug_fix(tagger):
    t = tagger.tag(["Possessor"], "Fixed Possessor bleeding while controlling someone.")
    assert t["category"] == "Bug Fixes"


def test_general_heading_keeps_class_tags(tagger):
    t = tagger.tag(["General"], "If the starting Mastermind dies, the starting Assassin replaces them.")
    assert t["category"] == "Game-wide" and t["classes"] == ["Mastermind", "Assassin"]


def test_cosmetics_drop_class_mentions(tagger):
    t = tagger.tag(["Detail", "New items"], "New armor: Neon Dynasty Knight")
    assert t["category"] == "Store & Cosmetics" and t["classes"] == []


def test_explained_section(tagger):
    t = tagger.tag(["Balance : Explained", "Observer Nerfs"], "Observer was the strongest invest.")
    assert t["kind"] == "explanation" and t["category"] == "Dev Notes"
    assert t["classes"] == ["Observer"]


def test_fallback_is_game_wide(tagger):
    t = tagger.tag([], "Players can no longer edit their logs while on trial.")
    assert t["category"] == "Game-wide" and t["categorySource"] in ("fallback", "text")

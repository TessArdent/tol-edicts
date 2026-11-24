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


# --- TO-2: class list, abilities, ordering ---------------------------------
from edicts.versions import parse_version  # noqa: E402


def test_former_names_and_converts(tagger):
    classes, _ = tagger.mentions("Psychic can now Link Minds. The Traitor Noble too.")
    assert classes == ["Mystic", "Aristocrat"]


def test_ability_names_identify_classes(tagger):
    classes, _ = tagger.mentions("Tornado : 3 -> 2")
    assert classes == ["Court Wizard", "Sage"]          # shared ability tags both
    t = tagger.tag([], "Exhume : 3 -> 2", parse_version("6.0.2"))
    assert t["classes"] == ["Herbalist"] and t["category"] == "Class Balance"


def test_abilities_ignored_under_a_class_heading(tagger):
    # Exhume was the Physician's in 0.8.24 before it went to the Herbalist
    t = tagger.tag(["Physician"], "Exhume ability was changed into a night ability.")
    assert t["classes"] == ["Physician"]


def test_class_only_matched_after_it_was_added(tagger):
    assert tagger.mentions("Maid now sees whispers.", parse_version("1.0.15"))[0] == []
    assert tagger.mentions("Maid now sees whispers.", parse_version("2.0.0"))[0] == ["Maid"]


def test_ignore_phrases(tagger):
    assert tagger.mentions("Happy Hour Battles registration opens.")[0] == []
    assert tagger.mentions("Happy Hour now occupies the player.")[0] == ["Drunk"]
    assert tagger.mentions("New outfit: Grim Reaper")[0] == []


def test_heading_order_balance_changes(tagger):
    t = tagger.tag(["Balance Changes"], "Nosy Servants - new ability since it now works!",
                   parse_version("2.6.0b"))
    assert t["category"] == "Class Balance" and t["classes"] == ["Maid"]


def test_general_heading_yields_to_specific_text(tagger):
    t = tagger.tag(["General"], "Greatly optimized server performance.")
    assert t["category"] == "Technical"


def test_notes_are_dev_notes(tagger):
    t = tagger.tag([], "We will keep an eye on this.", kind="note")
    assert t["category"] == "Dev Notes" and t["kind"] == "note"


def test_faction_tags_skip_varies(tagger):
    t = tagger.tag(["King"], "Can now swear fealty.")
    assert t["factions"] == []


def test_inner_class_heading_beats_outer_event_heading(tagger):
    t = tagger.tag(["The Anniversary Update With New Classes!", "Chronomancer"],
                   "Pocket Dimension (Day) - If you die tonight, delay it for 2 nights.",
                   parse_version("2.0.0"))
    assert t["category"] == "Class Balance" and t["classes"] == ["Chronomancer"]
    t = tagger.tag(["Bug Fixes", "King"], "Safeguard no longer desyncs.")
    assert t["category"] == "Bug Fixes"

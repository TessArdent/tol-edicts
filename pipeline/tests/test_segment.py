from edicts.segment import count_top_level_bullets, segment

ERA_2017 = """\
## General:

- Deathnotes have been reenabled.

## Alchemist:

- Stoneskin is now usable throughout the entire day.
- New passive, Coagulate.
  - Makes Alchemist immune to bleeding.

## Bug Fixes:

- Fixed some Possessor bugs.

--Xblade @ https://discord.gg/tol
"""

ERA_2020 = """\
*Balance, Onboarding & Improvements*

![](https://example.com/banner.gif)

---

## Balance

> Balance Changes: Observer

- `Follow` has been replaced with `Observe`.

> Balance Changes: Mercenary + Sellsword

- Stand Guard priority bumped down.

**Login Screen got a huge revamp:**

New art and faster loading.

> - Glossary added.
> - Nightshade replaced with bleeding.
"""

ERA_2022 = """\
#### **Summary: **

- **New items**

- **Bug fixes**

#### **Detail:**

- **New items**

- **Grim Reaper**

![](https://example.com/reaper.jpg)

- **Bug fixes**

- Fix the crash issue of game over scene.

For more support please email: support@throneoflies.com
Follow our [Twitter](https://throne.li/twitter)!
"""

PLAIN_LINES = """\
**PATCH NOTES:**
Added sounds for different messages sent by players.
Added an option to disable the fps display in the settings.
Escape can be used to close most of the UI popups.
"""


def texts(items):
    return [(i.section, i.plain) for i in items]


def test_2017_class_headings():
    items = segment(ERA_2017)
    assert texts(items) == [
        (["General"], "Deathnotes have been reenabled."),
        (["Alchemist"], "Stoneskin is now usable throughout the entire day."),
        (["Alchemist"], "New passive, Coagulate. Makes Alchemist immune to bleeding."),
        (["Bug Fixes"], "Fixed some Possessor bugs."),
    ]   # nested bullet folded into its parent, sign-off dropped


def test_2020_quoted_labels_and_bold_lines():
    items = segment(ERA_2020)
    got = texts(items)
    # the italic subtitle is a label, replaced by the first real heading
    assert got[0] == (["Balance", "Balance Changes: Observer"], "Follow has been replaced with Observe.")
    assert (["Balance", "Balance Changes: Mercenary + Sellsword"],
            "Stand Guard priority bumped down.") in got
    assert (["Balance", "Login Screen got a huge revamp"], "New art and faster loading.") in got
    # bullets inside a quote are still items
    assert (["Balance", "Login Screen got a huge revamp"], "Glossary added.") in got
    assert len(items) == 5      # banner image and rule dropped


def test_intro_text_before_any_structure():
    items = segment("Greetings!\n\nThe latest patch is live.\n\n## General\n\n- A change.\n")
    assert [(i.origin, i.plain) for i in items] == [
        ("intro", "The latest patch is live."),     # "Greetings!" is dropped as filler
        ("list", "A change."),
    ]
    assert items[-1].section == ["General"]


def test_2022_bold_bullets_are_subheadings_unless_empty():
    items = segment(ERA_2022)
    assert texts(items) == [
        (["Summary"], "New items"),
        (["Summary"], "Bug fixes"),
        (["Detail"], "New items"),
        (["Detail"], "Grim Reaper"),
        (["Detail", "Bug fixes"], "Fix the crash issue of game over scene."),
    ]


def test_plain_lines_become_items():
    items = segment(PLAIN_LINES)
    assert [i.plain for i in items] == [
        "Added sounds for different messages sent by players.",
        "Added an option to disable the fps display in the settings.",
        "Escape can be used to close most of the UI popups.",
    ]
    assert all(i.section == ["PATCH NOTES"] for i in items)


def test_follow_up_resets_sections():
    md = ("## Bug Fixes\n\n- Fixed a thing.\n\n---\n\n"
          "### Follow-up #3 by í42-Xblade (2021-03-12)\n\nPatch reverted for further testing.\n\n"
          "- Hotfix: fixed another thing.\n")
    items = segment(md)
    assert items[0].follow_up is None
    assert items[1].section == [] and items[1].follow_up["author"] == "í42-Xblade"
    assert items[1].is_reply_text            # prose in a reply is discussion
    assert not items[2].is_reply_text        # a bullet in a reply is a change


def test_bullet_count_matches_items():
    for md in (ERA_2017, ERA_2020, ERA_2022):
        listed = [i for i in segment(md) if i.origin == "list"]
        assert count_top_level_bullets(md) == len(listed)


def test_lead_in_lines_become_labels():
    md = "Detail :\n\n- First change.\n\nSome abilities changes in Quick mode:\n\n- Tornado : 3 -> 2\n"
    items = segment(md)
    assert [(i.section, i.plain) for i in items] == [
        (["Detail"], "First change."),
        (["Some abilities changes in Quick mode"], "Tornado : 3 -> 2"),
    ]


def test_bullet_glyph_lines_in_replies_are_changes():
    md = ("### Follow-up #2 by í42-Xblade (2020-08-12)\n\n"
          "• Fixed Cult Leader Eradicate being unable to target king.\n"
          "• Fixed the end screen.\n")
    items = segment(md)
    assert [i.plain for i in items] == ["Fixed Cult Leader Eradicate being unable to target king.",
                                       "Fixed the end screen."]
    assert not any(i.is_reply_text for i in items)

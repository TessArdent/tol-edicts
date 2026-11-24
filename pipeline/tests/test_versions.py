import pytest

from edicts.versions import Version, find_versions, parse_version


@pytest.mark.parametrize("title, expected", [
    ("1.0.2 Patch Notes", ["1.0.2"]),
    ("Hotfix 1.04a Released", ["1.0.4a"]),
    ("V2.4(a) Patch Notes", ["2.4.0a"]),
    ("Patch v2.5b (LIVE)", ["2.5.0b"]),
    ("V2.3.0c - Hotfixes", ["2.3.0c"]),
    ("v5.0: Major Gfx Revamp + Classic Mode!", ["5.0.0"]),
    ("1.0.16e1 Patch Notes", ["1.0.16e1"]),
    ("v6.0.10i: Secret code is coming", ["6.0.10i"]),
    ("2.2.0b + 2.2.0c Mini Patch Notes (LIVE)", ["2.2.0b", "2.2.0c"]),
    ("Security v4.1.5 + Stability v4.1.6 Patches", ["4.1.5", "4.1.6"]),
    ("0.8.24e - Vote Change Host Button Fixes", ["0.8.24e"]),
])
def test_titles(title, expected):
    assert [str(v) for v in find_versions(title)] == expected


@pytest.mark.parametrize("title", [
    "Alpha+ Steam Keys Now for Sale! $9.99 on our website via Card!",
    "4/3/2017 Privacy Policy + Terms of Service Update",
    "Forum.imperium42 >> is now forum.throneoflies.com",
    "Throne is 51% OFF for the next day or two!",
])
def test_no_false_versions(title):
    assert find_versions(title) == []


def test_ordering():
    vs = [parse_version(s) for s in ["2.4.0b", "1.0.10", "1.0.9", "2.4.0", "2.4.0a"]]
    assert [str(v) for v in sorted(vs)] == ["1.0.9", "1.0.10", "2.4.0", "2.4.0a", "2.4.0b"]


def test_parse_version_rejects_ambiguity():
    with pytest.raises(ValueError):
        parse_version("2.2.0b + 2.2.0c")
    assert parse_version("v1.0.1") == Version(1, 0, 1)

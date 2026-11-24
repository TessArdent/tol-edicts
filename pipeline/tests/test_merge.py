from edicts.merge import build_patches, group_patches
from edicts.posts import Post
from edicts.versions import parse_version


def post(key, source, date, versions, body_len):
    return Post(key=key, source=source, title=key, date=date, datetime=f"{date} 12:00 UTC",
                author="x", links={}, body="x" * body_len, kind="patch",
                versions=[parse_version(v) for v in versions])


def test_forum_preferred_and_steam_linked():
    forum = post("f-1.0.2", "forum", "2017-10-06", ["1.0.2"], 2000)
    steam = post("s-1.0.2", "steam", "2017-10-06", ["1.0.2"], 2100)
    patches, _ = build_patches([steam, forum])
    assert len(patches) == 1
    assert patches[0].primary is forum and patches[0].others == [steam]
    assert patches[0].id == "1.0.2"


def test_much_longer_steam_wins():
    forum = post("f", "forum", "2018-05-17", ["1.1.3"], 100)
    steam = post("s", "steam", "2018-05-19", ["1.1.3"], 1000)
    patches, notes = build_patches([forum, steam])
    assert patches[0].primary is steam and notes


def test_combined_post_bridges_versions():
    combined = post("f-4.1.5+4.1.6", "forum", "2021-07-15", ["4.1.5", "4.1.6"], 3000)
    s1 = post("s-4.1.5", "steam", "2021-07-19", ["4.1.5"], 500)
    s2 = post("s-4.1.6", "steam", "2021-07-29", ["4.1.6"], 500)
    groups = group_patches([s1, s2, combined])
    assert len(groups) == 1
    patches, _ = build_patches([s1, s2, combined])
    assert [str(v) for v in patches[0].versions] == ["4.1.5", "4.1.6"]


def test_rerelease_kept_as_extra_part():
    first = post("s-6.0.0c", "steam", "2021-10-15", ["6.0.0c"], 1000)
    again = post("s-6.0.0c-again", "steam", "2021-10-21", ["6.0.0c"], 800)
    stub = post("s-6.0.0c-stub", "steam", "2021-10-22", ["6.0.0c"], 30)
    patches, _ = build_patches([first, again, stub])
    assert len(patches) == 1
    assert patches[0].extra_parts == [again] and patches[0].others == [stub]


def test_ids_unique_and_versionless_by_date():
    a = post("a", "steam", "2017-10-01", [], 100)
    b = post("b", "steam", "2017-10-01", [], 100)
    patches, _ = build_patches([a, b])
    assert sorted(p.id for p in patches) == ["2017-10-01", "2017-10-01-2"]

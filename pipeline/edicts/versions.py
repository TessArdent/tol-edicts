"""Find and normalise Throne of Lies version numbers in post titles.

Titles write the same version many ways: "1.04a", "v2.4(a)", "V2.3.0c",
"2.2a", "v5.0", "1.0.16e1". Everything becomes MAJOR.MINOR.PATCH plus an
optional letter suffix, e.g. "1.0.4a", "2.4.0a", "5.0.0", "1.0.16e1".
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_VERSION_RE = re.compile(
    r"(?<![\w.$])[vV]?(\d{1,2})\.(\d{1,2})(?:\.(\d{1,2}))?"
    r"(?:\s?\(([a-z]\d?)\)|([a-z]\d?))?(?![\w.])"
)


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int
    suffix: str = ""

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}{self.suffix}"

    @property
    def sort_key(self) -> list:
        return [self.major, self.minor, self.patch, self.suffix]


def _make(major: str, minor: str, patch: str | None, suffix: str | None) -> Version:
    if patch is None and len(minor) == 2 and minor.startswith("0") and major != "0":
        # "1.04a" is how early hotfixes wrote 1.0.4a
        return Version(int(major), 0, int(minor[1]), suffix or "")
    return Version(int(major), int(minor), int(patch or 0), suffix or "")


def find_versions(text: str) -> list[Version]:
    """All versions in a title, in order, without duplicates."""
    found: list[Version] = []
    for m in _VERSION_RE.finditer(text):
        v = _make(m.group(1), m.group(2), m.group(3), m.group(4) or m.group(5))
        if v not in found:
            found.append(v)
    # "2.2.0b + 2.2.0c" is two versions; "Security v4.1.5 + Stability v4.1.6" too
    return found


def parse_version(text: str) -> Version:
    """Parse a single version string such as an override value."""
    vs = find_versions(text)
    if len(vs) != 1:
        raise ValueError(f"expected one version in {text!r}, found {vs}")
    return vs[0]

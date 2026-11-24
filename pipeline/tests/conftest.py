import sys
from pathlib import Path

import pytest
import yaml

PIPE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPE))

from edicts.tagging import Tagger  # noqa: E402


@pytest.fixture(scope="session")
def tagger() -> Tagger:
    load = lambda n: yaml.safe_load((PIPE / n).read_text(encoding="utf-8"))  # noqa: E731
    return Tagger(load("classes.yml"), load("categories.yml"))

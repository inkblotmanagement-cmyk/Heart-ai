import json
import re
from pathlib import Path

import heart_engine as H
from keys import (
    ALL_LAW_IDS,
    ATTRIBUTION,
    KEY_MEANING,
    KEY_NOTES,
    KEY_TO_LAWS,
    KEYS,
    UNMAPPED_KEYS,
    UNMAPPED_LAWS,
    key_label,
    keys_for_laws,
    law_ids_in,
    laws_to_keys,
    reflection,
)

ROOT = Path(__file__).resolve().parents[1]

OFFICIAL_TITLES = (
    "Invest money to win people and establish financial longevity.",
    "Prepare to market the world and expand capital base.",
    "Learn how to be a winner, build winning relationships, and secure investors.",
    "Use time to make money and gain knowledge of value.",
    "Manage anger and stress through healthy living and good nutrition.",
    "Faith is necessary for perseverance; this is your cash flow.",
    "Conserve water / value; this is your energy.",
    "Master your emotions / mistakes; this is your joy.",
    "Achieve financial and personal goals; this is your success.",
    "Observe how fragile the mind is.",
)
OLD_KEYS = ("Vision", "Faith", "Courage", "Love", "Truth",
            "Perseverance", "Humility", "Wisdom", "Service", "Unity")


def test_official_titles_exact_and_in_order():
    assert KEYS == OFFICIAL_TITLES
    assert set(KEY_MEANING) == set(KEY_TO_LAWS) == set(KEY_NOTES) == set(KEYS)
    assert key_label(KEYS[4]) == "Key 5: " + OFFICIAL_TITLES[4]
    assert "Terrance Darnell Jackson" in ATTRIBUTION


def test_every_law_mapped_or_explicitly_unmapped():
    laws = H.load_laws()
    assert set(laws) == set(ALL_LAW_IDS)
    mapped = {law for ids in KEY_TO_LAWS.values() for law in ids}
    assert mapped <= set(laws), f"unknown law ids: {mapped - set(laws)}"
    assert mapped | set(UNMAPPED_LAWS) == set(laws)
    assert not mapped & set(UNMAPPED_LAWS)
    assert UNMAPPED_LAWS == ("JL-02", "JL-04", "JL-10")


def test_unmapped_keys_say_so():
    assert [KEYS.index(k) + 1 for k in UNMAPPED_KEYS] == [2, 6, 7, 9]
    for k in UNMAPPED_KEYS:
        assert KEY_NOTES[k].startswith("No direct JMGL law")
    for k in KEYS:
        if k not in UNMAPPED_KEYS:
            for law in KEY_TO_LAWS[k]:
                assert law in KEY_NOTES[k], f"note for {key_label(k)} doesn't explain {law}"


def test_requested_relations():
    assert {"JL-01", "JL-03", "JL-06"} <= set(KEY_TO_LAWS[KEYS[0]])  # win people: non-exploitation/deception/dignity
    assert {"JL-01", "JL-07"} <= set(KEY_TO_LAWS[KEYS[2]])           # investors: no misleading claims / manipulation
    assert "JL-08" in KEY_TO_LAWS[KEYS[4]] and "JL-08" in KEY_TO_LAWS[KEYS[9]]  # well-being / crisis
    assert "JL-08" in KEY_TO_LAWS[KEYS[7]]                           # human escalation


def test_no_old_single_word_keys_left():
    alt = "|".join(OLD_KEYS)
    pat = re.compile(rf"""["']({alt})["']|\|\s*({alt})\s*\|""")
    for path in ["keys.py", "app.py", "heart_engine.py", "README.md", *map(str, (ROOT / "tests").glob("*.py"))]:
        text = (ROOT / path).read_text(encoding="utf-8")
        if path.endswith("test_keys.py"):
            text = text.split("OLD_KEYS = ", 1)[0]
        assert not pat.search(text), f"old key name left in {path}: {pat.search(text).group(0)}"
        assert "Vision, Faith, Courage" not in text, path
    assert not set(KEYS) & set(OLD_KEYS)


def test_helpers_are_deterministic():
    assert law_ids_in("JL-01+JL-02 then JL-01") == ["JL-01", "JL-02"]
    assert law_ids_in("GF-PASS") == []
    assert [KEYS.index(k) + 1 for k in keys_for_laws(["JL-08"])] == [5, 8, 10]
    assert [KEYS.index(k) + 1 for k, _ in reflection("ALLOW", [])] == [4]
    assert reflection("BLOCK", ["JL-04"]) == []  # stalking law has no related key
    assert all(laws_to_keys()[law] == [] for law in UNMAPPED_LAWS)


def test_laws_json_is_the_real_one():
    from jmgl.engine import DEFAULT_LAWS
    meta = json.loads(Path(DEFAULT_LAWS).read_text(encoding="utf-8"))["meta"]
    assert "approved" in meta["status"]

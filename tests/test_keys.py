import json

import heart_engine as H
from keys import ALL_LAW_IDS, KEY_MEANING, KEY_TO_LAWS, KEYS, keys_for_laws, law_ids_in, laws_to_keys, reflection


def test_all_ten_keys_present_and_mapped():
    assert KEYS == ("Vision", "Faith", "Courage", "Love", "Truth",
                    "Perseverance", "Humility", "Wisdom", "Service", "Unity")
    assert set(KEY_TO_LAWS) == set(KEYS) == set(KEY_MEANING)
    for k in KEYS:
        assert KEY_TO_LAWS[k], f"{k} maps to no law"


def test_every_law_is_covered_and_exists_in_laws_json():
    laws = H.load_laws()
    assert set(laws) == set(ALL_LAW_IDS)  # the installed JMGL ships exactly JL-00..JL-10
    mapped = {law for ids in KEY_TO_LAWS.values() for law in ids}
    assert mapped == set(laws), f"uncovered: {set(laws) - mapped}, unknown: {mapped - set(laws)}"
    inv = laws_to_keys()
    assert all(inv[law] for law in laws)


def test_helpers_are_deterministic():
    assert law_ids_in("JL-01+JL-02 then JL-01") == ["JL-01", "JL-02"]
    assert law_ids_in("GF-PASS") == []
    assert keys_for_laws(["JL-08"]) == ["Love", "Humility", "Service"]
    assert [k for k, _ in reflection("ALLOW", [])] == ["Vision", "Wisdom", "Service"]
    assert reflection("BLOCK", ["JL-04"]) == reflection("BLOCK", ["JL-04"])


def test_laws_json_is_the_real_one():
    from jmgl.engine import DEFAULT_LAWS
    meta = json.loads(open(DEFAULT_LAWS, encoding="utf-8").read())["meta"]
    assert "approved" in meta["status"]

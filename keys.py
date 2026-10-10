"""The 10 Keys: Heart AI's values framework, mapped onto the JMGL laws.

The 10 Keys (Vision, Faith, Courage, Love, Truth, Perseverance, Humility,
Wisdom, Service, Unity) come from Terrance Darnell Jackson's Jackson 10 Key
Moral Code. They are a *values framework* for people, not a trained model.

KEY_TO_LAWS is a plain, hand-written, deterministic mapping showing which of the
JMGL working laws (JL-00..JL-10, see JMGL spec/laws.json) express each key in
practice. No neural network has "absorbed" these keys; the mapping is an
editorial reading of the laws, open to the founder's review and revision.
"""
from __future__ import annotations

import re

KEYS: tuple[str, ...] = (
    "Vision", "Faith", "Courage", "Love", "Truth",
    "Perseverance", "Humility", "Wisdom", "Service", "Unity",
)

# A one-line meaning for each key, as it applies to judging an AI action.
KEY_MEANING: dict[str, str] = {
    "Vision": "Look at where the whole task leads, not just the next step.",
    "Faith": "Keep the trust people place in you; never exploit it.",
    "Courage": "Hold to the ethics check even under pressure, role-play, or claimed authority.",
    "Love": "Protect the vulnerable and meet people in crisis with compassion.",
    "Truth": "Do not deceive people, investors, or the evaluator.",
    "Perseverance": "Keep checking across the whole conversation; staged harm is still harm.",
    "Humility": "Respect other people's autonomy and hand hard cases to real humans.",
    "Wisdom": "See through disguises and proxies, and help with education and protection.",
    "Service": "When nothing harmful is intended, actually help the person.",
    "Unity": "Do not quietly exclude people; treat everyone by the same fair criteria.",
}

# Key -> JMGL law ids that express it. Every key maps to at least one law and
# every law JL-00..JL-10 is covered by at least one key (enforced by tests).
KEY_TO_LAWS: dict[str, tuple[str, ...]] = {
    "Vision": ("JL-10", "JL-00"),
    "Faith": ("JL-01", "JL-02"),
    "Courage": ("JL-05", "JL-09"),
    "Love": ("JL-08", "JL-03"),
    "Truth": ("JL-01", "JL-07", "JL-09"),
    "Perseverance": ("JL-10", "JL-05"),
    "Humility": ("JL-04", "JL-08"),
    "Wisdom": ("JL-06", "JL-10", "JL-00"),
    "Service": ("JL-00", "JL-08"),
    "Unity": ("JL-06", "JL-03"),
}

ALL_LAW_IDS: tuple[str, ...] = tuple(f"JL-{i:02d}" for i in range(11))

_LAW_RE = re.compile(r"JL-\d{2}")


def law_ids_in(text: str | None) -> list[str]:
    """Extract JMGL law ids (JL-00..JL-10) from a rule id like 'JL-04' or 'JL-01+JL-02'."""
    seen: list[str] = []
    for m in _LAW_RE.findall(text or ""):
        if m not in seen:
            seen.append(m)
    return seen


def laws_to_keys() -> dict[str, list[str]]:
    """Inverse mapping: law id -> keys that relate to it."""
    out: dict[str, list[str]] = {law: [] for law in ALL_LAW_IDS}
    for key, laws in KEY_TO_LAWS.items():
        for law in laws:
            out.setdefault(law, []).append(key)
    return out


def keys_for_laws(law_ids: list[str]) -> list[str]:
    """Keys reflected by a set of triggered laws, in canonical 10-Key order."""
    wanted = set(law_ids)
    return [k for k in KEYS if wanted.intersection(KEY_TO_LAWS[k])]


def reflection(decision: str, law_ids: list[str]) -> list[tuple[str, str]]:
    """Deterministic 'Keys reflection' for a decision: (key, explanation) pairs.

    This is a lookup from the triggered laws, not a judgment by a model.
    """
    keys = keys_for_laws(law_ids)
    if not keys and decision == "ALLOW":
        keys = keys_for_laws(["JL-00"])
    verb = {
        "ALLOW": "Helping here reflects",
        "BLOCK": "Refusing here upholds",
        "MODIFY": "Changing the action upholds",
        "ESCALATE": "Handing this to a person reflects",
    }.get(decision, "This decision relates to")
    return [(k, f"{verb} {k}: {KEY_MEANING[k]}") for k in keys]

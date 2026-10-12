"""The official 10 Keys, and an editorial lookup relating them to the JMGL laws.

The 10 Keys are from Terrance Darnell Jackson's (c) business materials, "Get Rich
and Grow Wealth" and "Pinch Pennies for Profits(c)". They are motivational
leadership, productivity, and financial-habit principles for people. They are
NOT software laws and not a trained model. JMGL's software laws (JL-00..JL-10,
in JMGL spec/laws.json) are separate.

KEY_TO_LAWS is a hand-written, clearly labeled *editorial* lookup that shows where
a key relates thematically to a JMGL law. Some keys have no direct law and say so
(no forced links). Laws no key relates to are listed in UNMAPPED_LAWS.
"""
from __future__ import annotations

import re

ATTRIBUTION = ("The 10 Keys © Terrance Darnell Jackson, from his \"Get Rich and Grow Wealth\" and "
               "\"Pinch Pennies for Profits©\" materials.")

# Exact official titles, in order (Key 1..Key 10).
KEYS: tuple[str, ...] = (
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

# Short explanation of each key, from the same materials.
KEY_MEANING: dict[str, str] = dict(zip(KEYS, (
    "Direct resources toward relationships, customer satisfaction, and reputation; goodwill outlasts short-term transactions.",
    "Scale skills and products beyond one local market, so you are less exposed to local recessions.",
    "Become someone others choose to support.",
    "Treat time as a resource for earning and learning; knowledge becomes service.",
    "Physical and mental condition sustain confidence and clear vision.",
    "Vision begins as faith; persistence plus collaboration builds clientele.",
    "Protect physical and mental energy, hydration, and focus.",
    "Control reactions and learn from errors.",
    "Reach the financial and personal goals you set.",
    "Emotions can cause damage or loss; counter them daily with healthy living and nutrition.",
), strict=True))

# Editorial lookup: key -> related JMGL laws. Empty tuple = no direct law.
KEY_TO_LAWS: dict[str, tuple[str, ...]] = dict(zip(KEYS, (
    ("JL-01", "JL-03", "JL-06"),
    (),
    ("JL-01", "JL-07"),
    ("JL-00",),
    ("JL-08",),
    (),
    (),
    ("JL-08", "JL-05", "JL-09"),
    (),
    ("JL-08",),
), strict=True))

# Why each link was drawn (or why there is none).
KEY_NOTES: dict[str, str] = dict(zip(KEYS, (
    "Winning people means earning trust: no deception (JL-01), no exploiting vulnerable people (JL-03), "
    "and fair, dignified treatment of everyone (JL-06).",
    "No direct JMGL law. Expanding into new markets is a business strategy; JMGL has no rule about it.",
    "Securing investors honestly: no misleading claims (JL-01) and no hyping an asset to deceive investors (JL-07).",
    "Knowledge becomes service: JMGL's default is to help, especially with educational purposes (JL-00).",
    "Stress and well-being: when someone may be in crisis, JMGL connects them to human help (JL-08).",
    "No direct JMGL law. Faith, persistence, and cash flow are personal and business principles.",
    "No direct JMGL law. Protecting your own energy and focus is a personal health habit.",
    "Mastering reactions and mistakes: hard cases go to a real person (JL-08), and pressure, role-play, or "
    "claimed authority doesn't override the check (JL-05, JL-09).",
    "No direct JMGL law. Personal and financial goals are yours to set; JMGL only checks the actions taken.",
    "The fragile mind: crisis and self-harm signals are escalated to people with resources such as 988 (JL-08).",
), strict=True))

ALL_LAW_IDS: tuple[str, ...] = tuple(f"JL-{i:02d}" for i in range(11))
UNMAPPED_KEYS: tuple[str, ...] = tuple(k for k in KEYS if not KEY_TO_LAWS[k])
UNMAPPED_LAWS: tuple[str, ...] = tuple(
    law for law in ALL_LAW_IDS if not any(law in laws for laws in KEY_TO_LAWS.values()))
# Expected: JL-02 (others' credentials/data), JL-04 (stalking), JL-10 (staged harm across turns).

_LAW_RE = re.compile(r"JL-\d{2}")


def key_label(key: str) -> str:
    """'Key 5: Manage anger and stress ...'"""
    return f"Key {KEYS.index(key) + 1}: {key}"


def law_ids_in(text: str | None) -> list[str]:
    """Extract JMGL law ids (JL-00..JL-10) from a rule id like 'JL-04' or 'JL-01+JL-02'."""
    seen: list[str] = []
    for m in _LAW_RE.findall(text or ""):
        if m not in seen:
            seen.append(m)
    return seen


def laws_to_keys() -> dict[str, list[str]]:
    """Inverse lookup: law id -> keys related to it (may be empty)."""
    out: dict[str, list[str]] = {law: [] for law in ALL_LAW_IDS}
    for key, laws in KEY_TO_LAWS.items():
        for law in laws:
            out.setdefault(law, []).append(key)
    return out


def keys_for_laws(law_ids: list[str]) -> list[str]:
    """Keys related to a set of triggered laws, in Key 1..10 order."""
    wanted = set(law_ids)
    return [k for k in KEYS if wanted.intersection(KEY_TO_LAWS[k])]


def reflection(decision: str, law_ids: list[str]) -> list[tuple[str, str]]:
    """Deterministic 'Keys reflection': (key, explanation) pairs from the editorial lookup.

    This is a lookup from the triggered laws, not a judgment by a model.
    """
    keys = keys_for_laws(law_ids)
    if not keys and decision == "ALLOW":
        keys = keys_for_laws(["JL-00"])
    return [(k, f"{key_label(k)} ({KEY_NOTES[k]})") for k in keys]

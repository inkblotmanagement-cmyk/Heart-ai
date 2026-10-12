"""Heart AI: a working, honest front end for the Jackson Moral Governance Layer.

Founder: Terrance Darnell Jackson, Mindful Oracle LLC.
Run:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

import heart_engine as H
from keys import ATTRIBUTION, KEY_MEANING, KEY_NOTES, KEY_TO_LAWS, KEYS, UNMAPPED_LAWS, key_label, laws_to_keys

JMGL_URL = "https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer"
BADGE = {"ALLOW": "🟢", "BLOCK": "🔴", "MODIFY": "🟠", "ESCALATE": "🟣"}
MEANING = {
    "ALLOW": "No prohibited intent detected. The AI may proceed.",
    "BLOCK": "This action breaks a JMGL law. The AI should not do it.",
    "MODIFY": "The goal can be met, but only in a changed, safer form.",
    "ESCALATE": "A real person should handle this, not the AI alone.",
}

st.set_page_config(page_title="Heart AI", page_icon="❤️", layout="wide")


@st.cache_resource(show_spinner="Loading the JMGL engine (first run downloads a small embedding model)...")
def _warm() -> bool:
    # Loads the classifier once per server process; harmless if it falls back.
    H.evaluate("Summarize this article about healthy sleep habits.")
    return True


st.title("❤️ Heart AI")
st.markdown("**Founder: Terrance Darnell Jackson** · Mindful Oracle LLC")
st.caption("Check a proposed AI action against the Jackson Moral Governance Layer (JMGL) and see which of "
           "Terrance Darnell Jackson's 10 Keys relate to the decision. Pilot-stage software: not AGI or superintelligence, and "
           "every serious decision still needs human review.")

tab_check, tab_keys, tab_about = st.tabs(["Check an AI action", "The 10 Keys", "About & limitations"])

with tab_check:
    _warm()
    labels = ["(write your own)"] + [e[0] for e in H.EXAMPLES]
    choice = st.selectbox("Example actions (benign and harmful)", labels)
    ex = next((e for e in H.EXAMPLES if e[0] == choice), None)
    action = st.text_area("Proposed AI action", value=ex[1] if ex else "", height=110,
                          placeholder="e.g. Draft a reminder email to my team about Friday's training.")
    hist_txt = st.text_area("Earlier conversation turns (optional, one per line)",
                            value="\n".join(ex[2]) if ex else "", height=80,
                            help="JMGL judges the whole task, so harm split across turns is still caught (JL-10).")
    c1, c2 = st.columns(2)
    rules_only = c1.checkbox("Rules-only mode (turn off the learned classifier)", value=False)
    use_grace = c2.checkbox("Use the Grace Force 0.7 gate (on by default)", value=H.grace_available(),
                            disabled=not H.grace_available())

    if st.button("Evaluate with JMGL", type="primary"):
        if not action.strip():
            st.warning("Enter a proposed AI action first.")
        else:
            r = H.evaluate(action, hist_txt.splitlines(), force_rules_only=rules_only, use_grace=use_grace)
            st.subheader(f"{BADGE.get(r.decision, '')} Decision: {r.decision}")
            st.write(MEANING.get(r.decision, ""))
            st.markdown(f"**Why:** {r.reason}")

            m1, m2, m3 = st.columns(3)
            m1.metric("Engine mode", r.engine_mode)
            m2.metric("Classifier confidence", f"{r.confidence:.0%}" if r.confidence is not None else "n/a")
            if r.grace_gate_score is not None:
                m3.metric("Grace Force gate", f"{r.grace_gate_score:.2f}",
                          delta=f"{r.grace_gate_score - r.grace_threshold:+.2f} vs {r.grace_threshold} line")
            else:
                m3.metric("Grace Force gate", "not installed" if not r.grace_available else "skipped")
            st.caption(r.engine_note + " " + r.grace_note)
            if r.classifier_category:
                st.caption(f"Learned classifier's best-guess category: `{r.classifier_category}`.")
            if r.grace_force is not None:
                st.caption(f"Full Grace Force composite (includes benefit/flourishing word-based estimates, "
                           f"reported only, not decisive): {r.grace_force:.2f}")
            if r.ensemble_decision and r.ensemble_decision != r.decision:
                st.caption(f"Underlying ensemble said {r.ensemble_decision}; the Grace gate set the final decision.")

            st.markdown("**Laws triggered**")
            if r.laws_via_classifier:
                st.caption("No keyword law fired. The law below is the one matching the learned classifier's category.")
            if r.laws:
                for law in r.laws:
                    st.markdown(f"- **{law['id']}**: {law['statement']}")
            elif r.rule_id == "JL-ML":
                st.markdown("- No single keyword law fired; the learned classifier recognized a prohibited category.")
            else:
                st.markdown(f"- None by id (`{r.rule_id}`).")

            if r.rewrite:
                st.markdown("**Suggested safer version**")
                st.info(r.rewrite)
            if r.resources:
                st.markdown("**Help is available right now**")
                for line in r.resources:
                    st.markdown(f"- {line}")

            st.markdown("**Keys reflection** (an editorial lookup from the triggered laws, not a model's judgment)")
            for _, text in r.keys_reflection:
                st.markdown(f"- {text}")
            if not r.keys_reflection:
                st.markdown("- No key is related to this rule in the editorial lookup.")

with tab_keys:
    st.markdown("**The 10 Keys** are motivational leadership, productivity, and financial-habit principles for people. "
                "They are separate from JMGL's software laws. No model here has *absorbed* them. The links below are "
                "an **editorial lookup** showing where a key relates thematically to a JMGL law. Some keys have no "
                "direct law, and the lookup says so.")
    st.caption(ATTRIBUTION)
    laws = H.load_laws()
    for k in KEYS:
        with st.expander(f"**{key_label(k)}**"):
            st.markdown(KEY_MEANING[k])
            st.markdown(f"*Relation to JMGL (editorial):* {KEY_NOTES[k]}")
            for lid in KEY_TO_LAWS[k]:
                st.markdown(f"- **{lid}**: {laws.get(lid, '')}")
    st.markdown("**By law**")
    inv = laws_to_keys()
    st.table([{"law": lid, "statement": laws.get(lid, ""),
               "related keys": ", ".join(f"Key {KEYS.index(k) + 1}" for k in inv.get(lid, [])) or "none (no direct key)"}
              for lid in sorted(laws)])
    st.caption(f"Laws with no related key: {', '.join(UNMAPPED_LAWS)}.")

with tab_about:
    st.markdown(f"""
**What Heart AI is:** a front end for the open-source [JMGL engine]({JMGL_URL}) (MIT license). It checks a
proposed AI action against 11 written laws plus a small learned classifier, and returns ALLOW, BLOCK,
MODIFY, or ESCALATE with the reason.

**What it is not:** it is **not AGI or artificial superintelligence**, and no model here has absorbed the
10 Keys (they are principles for people, linked to the laws by an editorial lookup). It is a pilot-stage safety filter with known error rates.

**Published results for the pinned JMGL version** (JMGL commit `9d0eeed`, all on held-out test sets
that were not used for tuning).

*Grace Force 0.7 gate* ([`eval/GRACE_FORCE_REPORT.md`](https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer/blob/9d0eeed61ac4045f67549e604ce75ec484870cf7/eval/GRACE_FORCE_REPORT.md)). Pass or fail at the
0.7 line uses **harm + confidence only**. Benefit and flourishing are word-based estimates, shown but never decisive.

| test set | cases | accuracy | harmful let through | safe requests flagged |
|---|---|---|---|---|
| template-disjoint held-out (sample) | 3,000 | 92.9% | 0.5% | 5.8% |
| fresh paraphrases | 66 | 95.5% | 0.0% | 4.0% |
| self-harm / consent (pre-registered) | 55 | 94.5% | 0.0% | 11.8% |
| fresh hand-written, harder | 46 | 73.9% | **19.6%** | 0.0% |

On the hardest hand-written set, the harm-only gate let more harm through (13.0% before, 19.6% now). Before,
low benefit scores were hiding the classifier's misses on veiled harm. The weakness is real and is still open.

- Laundering harm through the rewrite path: **0 of 15** (original red team) and **0 of 25** (new red team).
- Multi-turn setups (30 cases): **all 20** harmful setups caught; 1 of 10 safe conversations flagged (10%).
- Stability: scores are fully repeatable; light edits (typos, casing, synonyms) flip the decision **1.11%** of the time.

*Underlying ensemble v0.7.1* ([`eval/ACCURACY_REPORT.md`](https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer/blob/9d0eeed61ac4045f67549e604ce75ec484870cf7/eval/ACCURACY_REPORT.md)):

| test set | cases | accuracy | harmful let through | safe requests flagged |
|---|---|---|---|---|
| held-out, template-disjoint | 21,722 | 95.9% | 1.7% | 5.5% |
| fresh paraphrases | 66 | 97.0% | 0.0% | 4.0% |
| fresh hand-written, harder | 46 | 76.1% | 28.3% | 0.0% |

The 0.7 line is an operating point chosen to catch as much harm as possible. It is not a validated measure of
ethics.

**Limits you should know:**
- All of JMGL's test data was written by AI, not labeled by people. A human-labeling study with staff is pending,
  so none of these numbers has been checked by people yet.
- It makes mistakes both ways. It can block safe requests and miss subtle, veiled harm.
- **Human review is required** for any decision that affects a real person.
- If you or someone you know is in crisis, call or text **988** in the US.

Installed JMGL version: `{H.jmgl_version()}` · Grace Force installed: `{H.grace_available()}` ·
Classifier available: `{H.classifier_available()}`
""")

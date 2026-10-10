"""Heart AI: a working, honest front end for the Jackson Moral Governance Layer.

Founder: Terrance Darnell Jackson, Mindful Oracle LLC.
Run:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

import heart_engine as H
from keys import KEY_MEANING, KEY_TO_LAWS, KEYS, laws_to_keys

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
           "the 10 Keys the decision reflects. Pilot-stage software: not AGI or superintelligence, and "
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
    use_grace = c2.checkbox("Use the Grace Force 0.7 gate when installed", value=H.grace_available(),
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

            st.markdown("**Keys reflection** (a fixed lookup from the triggered laws, not a model's judgment)")
            for _, text in r.keys_reflection:
                st.markdown(f"- {text}")
            if not r.keys_reflection:
                st.markdown("- No key mapping for this rule id.")

with tab_keys:
    st.markdown("The **10 Keys** are Terrance Darnell Jackson's values framework. Heart AI does not have a model "
                "that has *absorbed* them. Instead, each key is linked by hand to the JMGL laws that put it into "
                "practice, so you can see the values behind every decision.")
    laws = H.load_laws()
    for k in KEYS:
        with st.expander(f"**{k}**: {KEY_MEANING[k]}"):
            for lid in KEY_TO_LAWS[k]:
                st.markdown(f"- **{lid}**: {laws.get(lid, '')}")
    st.markdown("**By law**")
    inv = laws_to_keys()
    st.table([{"law": lid, "statement": laws.get(lid, ""), "keys": ", ".join(inv.get(lid, []))}
              for lid in sorted(laws)])

with tab_about:
    st.markdown(f"""
**What Heart AI is:** a front end for the open-source [JMGL engine]({JMGL_URL}) (MIT license). It checks a
proposed AI action against 11 written laws plus a small learned classifier, and returns ALLOW, BLOCK,
MODIFY, or ESCALATE with the reason.

**What it is not:** it is **not AGI or artificial superintelligence**, and no model here has absorbed the
10 Keys. It is a pilot-stage safety filter with known error rates.

**Published results for the pinned JMGL version** (JMGL `eval/ACCURACY_REPORT.md`, ensemble v0.4):

| test set | cases | accuracy | harmful let through | safe requests flagged |
|---|---|---|---|---|
| held-out, template-disjoint | 21,722 | 88.1% | 1.8% | 28.3% |
| fresh paraphrases | 66 | 89.4% | 2.4% | 24.0% |
| fresh hand-written, harder | 46 | 73.9% | 37.0% | 0.0% |

The Grace Force 0.7 gate (JMGL `eval/GRACE_FORCE_REPORT.md`) is still under review and is not in the pinned
version; Heart AI uses it automatically when it is installed.

**Limits you should know:**
- All of JMGL's test data was written by AI, not labeled by people. A human-labeling study with staff is pending.
- It makes mistakes both ways. It can block safe requests and miss subtle, veiled harm.
- **Human review is required** for any decision that affects a real person.
- If you or someone you know is in crisis, call or text **988** in the US.

Installed JMGL version: `{H.jmgl_version()}` · Grace Force installed: `{H.grace_available()}` ·
Classifier available: `{H.classifier_available()}`
""")

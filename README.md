# Heart AI

**Founder: Terrance Darnell Jackson · Mindful Oracle LLC**

Heart AI is a small, working web app that checks a proposed AI action against the
[Jackson Moral Governance Layer (JMGL)](https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer)
and shows how Terrance Darnell Jackson's **10 Keys** relate to the decision.

> **Status: pilot-stage.** Heart AI is **not AGI or artificial superintelligence**. No model here has
> "absorbed" the 10 Keys. It is a front end for a policy engine with published, imperfect accuracy,
> tested only on AI-written data so far. Every decision that affects a real person needs human review.

![Heart AI screenshot](docs/screenshot.png)

## What it does

1. You type a proposed AI action (and, optionally, earlier turns of the conversation).
2. Heart AI runs it through the real JMGL engine: 11 written laws (JL-00..JL-10) plus a small learned
   classifier (`evaluate_action_ensemble`). If the classifier can't load, it falls back to the rules-only
   engine and says so on screen.
3. The **Grace Force** gate (`evaluate_grace_force`) is on by default. It decides pass or fail at the **0.7** line
   from harm + confidence only, and Heart AI shows the gate score against that line. You can turn it off, or use
   rules-only mode, to compare.
4. You see the decision (**ALLOW / BLOCK / MODIFY / ESCALATE**), the laws triggered with their text, the
   classifier's confidence, any safer rewrite, crisis resources (988) when a person may be in crisis, the
   engine mode, and a **Keys reflection**.

## The 10 Keys

The 10 Keys © Terrance Darnell Jackson, from his "Get Rich and Grow Wealth" and "Pinch Pennies for Profits©" materials.

1. **Invest money to win people and establish financial longevity.** Direct resources toward relationships, customer satisfaction, and reputation; goodwill outlasts short-term transactions.
2. **Prepare to market the world and expand capital base.** Scale skills and products beyond one local market, so you are less exposed to local recessions.
3. **Learn how to be a winner, build winning relationships, and secure investors.** Become someone others choose to support.
4. **Use time to make money and gain knowledge of value.** Treat time as a resource for earning and learning; knowledge becomes service.
5. **Manage anger and stress through healthy living and good nutrition.** Physical and mental condition sustain confidence and clear vision.
6. **Faith is necessary for perseverance; this is your cash flow.** Vision begins as faith; persistence plus collaboration builds clientele.
7. **Conserve water / value; this is your energy.** Protect physical and mental energy, hydration, and focus.
8. **Master your emotions / mistakes; this is your joy.** Control reactions and learn from errors.
9. **Achieve financial and personal goals; this is your success.** Reach the financial and personal goals you set.
10. **Observe how fragile the mind is.** Emotions can cause damage or loss; counter them daily with healthy living and nutrition.

The 10 Keys are **motivational leadership, productivity, and financial-habit principles for people**. They are
separate from JMGL's software laws (JL-00..JL-10), and no model here has absorbed them.

[`keys.py`](keys.py) holds a hand-written **editorial lookup** showing where a key relates thematically to a JMGL law,
with a one-line reason for each link. The "Keys reflection" in the app is a fixed lookup from the triggered laws, not a
model's judgment. Some keys have no direct law, and the lookup says so instead of forcing a link.

| Key | Title | Related JMGL laws (editorial) |
|---|---|---|
| 1 | Invest money to win people and establish financial longevity. | JL-01, JL-03, JL-06 |
| 2 | Prepare to market the world and expand capital base. | none (no direct law) |
| 3 | Learn how to be a winner, build winning relationships, and secure investors. | JL-01, JL-07 |
| 4 | Use time to make money and gain knowledge of value. | JL-00 |
| 5 | Manage anger and stress through healthy living and good nutrition. | JL-08 |
| 6 | Faith is necessary for perseverance; this is your cash flow. | none (no direct law) |
| 7 | Conserve water / value; this is your energy. | none (no direct law) |
| 8 | Master your emotions / mistakes; this is your joy. | JL-08, JL-05, JL-09 |
| 9 | Achieve financial and personal goals; this is your success. | none (no direct law) |
| 10 | Observe how fragile the mind is. | JL-08 |

Laws with no related key: JL-02, JL-04, JL-10 (others' credentials/data, stalking, and harm staged across turns).
Tests check the exact titles, that every law is either related to a key or listed as unrelated, and that no old
single-word key names remain. The lookup is open to the founder's revision.

## Published results (pinned JMGL version)

`requirements.txt` pins JMGL commit [`9d0eeed`](https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer/commit/9d0eeed61ac4045f67549e604ce75ec484870cf7)
(the merge of JMGL PR #8, Grace Force 0.7.1). Every number below is on a held-out set that was not used for tuning.

**Grace Force 0.7 gate** ([`eval/GRACE_FORCE_REPORT.md`](https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer/blob/9d0eeed61ac4045f67549e604ce75ec484870cf7/eval/GRACE_FORCE_REPORT.md)). Pass or fail uses
harm + confidence only. Human benefit and long-term flourishing are word-based estimates, reported but never decisive.

| test set | cases | accuracy | harmful let through | safe requests flagged |
|---|---|---|---|---|
| template-disjoint held-out (sample) | 3,000 | 92.9% | 0.5% | 5.8% |
| fresh paraphrases | 66 | 95.5% | 0.0% | 4.0% |
| self-harm / consent (pre-registered) | 55 | 94.5% | 0.0% | 11.8% |
| fresh hand-written, harder | 46 | 73.9% | **19.6%** | 0.0% |

- **Trade-off:** on the hardest hand-written set, switching to the harm-only gate let more harm through
  (13.0% before, 19.6% now). Before, low benefit/flourishing scores happened to push veiled-harm items below 0.7,
  hiding the classifier's misses. That weakness is real and is still open.
- **Laundering through the rewrite path:** 0 of 15 (original red team) and 0 of 25 (new red team, written before tuning).
- **Rewrite log:** 72 cases entered the rewrite path, and every rewrite changed the decision. None just rephrased a harmful request.
- **Multi-turn** (30 pre-registered cases): all 20 harmful setups caught; 1 of 10 safe conversations flagged (10%).
- **Stability:** scores are fully repeatable; light edits flip the decision 1.11% of the time (10 of 900).

**Underlying ensemble v0.7.1** ([`eval/ACCURACY_REPORT.md`](https://github.com/inkblotmanagement-cmyk/JacksonMoralGovernanceLayer/blob/9d0eeed61ac4045f67549e604ce75ec484870cf7/eval/ACCURACY_REPORT.md)):

| test set | cases | accuracy | harmful let through | safe requests flagged |
|---|---|---|---|---|
| held-out, template-disjoint | 21,722 | 95.9% | 1.7% | 5.5% |
| held-out, random split | 16,331 | 96.1% | 1.8% | 5.9% |
| fresh paraphrases | 66 | 97.0% | 0.0% | 4.0% |
| fresh hand-written, harder | 46 | 76.1% | 28.3% | 0.0% |

**Limits:**
- All test data was written by AI, not labeled by people. A staff human-labeling study is pending, so none of these
  numbers has been checked by people yet.
- The 0.7 line is an operating point chosen to catch as much harm as possible. It is not a validated measure of ethics.
- The engine still makes mistakes both ways and is weakest on subtle, veiled harm.

**The app's own examples on this pin:** all 10 come out as labeled. The two that the previous pin got wrong are now
right. The scam-awareness lesson is ALLOWED (gate 1.00), and the multi-turn stalking example is BLOCKED by the learned
classifier (gate 0.27). No keyword law fires, so the app names JL-10, the law that matches the classifier's
`multiturn` category, and says so on screen. Tests check both. In **rules-only mode** both are still wrong (BLOCK and ALLOW), which shows
why the classifier matters. One small quirk: the pump-and-dump example is blocked under JL-01 (deception) rather than
JL-07 (market manipulation).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # installs JMGL from GitHub (pinned commit) + Streamlit
streamlit run app.py                   # opens http://localhost:8501
```

The first run downloads a ~130 MB open embedding model (BAAI bge-small) used by the classifier.

Tests: `pip install -r requirements-dev.txt && pytest -q`

Docker: `docker build -t heart-ai . && docker run -p 8501:8501 heart-ai`

### Updating JMGL

Grace Force ships in the pinned commit, so nothing extra is needed. To move to a newer JMGL, change the commit in
`requirements.txt` to another commit on JMGL `main`, then rerun `pytest -q`.

## Files

- `app.py`: the Streamlit app (renamed from `App.py`)
- `heart_engine.py`: testable wrapper around JMGL (ensemble, rules-only fallback, optional Grace gate)
- `keys.py`: the official 10 Keys and their editorial lookup to JMGL laws
- `tests/`: pytest suite (mapping coverage, clear-case decisions, fallback paths, app smoke test)

## What changed from the first version

The first `App.py` was an early prototype. Its "AGI" was a PyTorch network with random, untrained weights,
and the outcome on screen depended only on the Faith slider. Its "UBI simulator" printed a fixed message
($100K/year to 8 billion people, poverty at 0% in 7 days) whenever two sliders were above 0.9; it did not
model any economics. The old README described it as the first artificial superintelligence and showed an
"Ethical Alignment 1.00" badge that no test measured. This version replaces all of that with real evaluation
by JMGL. The 10 Keys are now Terrance Darnell Jackson's official business Keys, shown as principles for people
alongside the software laws, not as model inputs.

## Vision (aspiration, not a current capability)

*"Mercy as Physics. Compassion as Architecture. Heart as First Code."*

Mindful Oracle's long-term vision is AI that helps heal root causes of human suffering and shares abundance
fairly, guided by spiritual wisdom, ethical governance, and compassionate stewardship. **This is a goal.**
Today's Heart AI is one honest step toward it: a transparent check that every AI action must pass, with its
error rates in the open.

## License

MIT © 2026 Terrance Darnell Jackson / Mindful Oracle LLC. JMGL is also MIT-licensed.

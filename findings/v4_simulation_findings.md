# Phase 2b — Predictive Risk Model Outputs (NOT empirical findings)

**Generated:** 2026-06-01 · **Reframed for honesty:** v4.2.1
**Source:** [`data/results/phase2b_bootstrap_ci.csv`](../data/results/phase2b_bootstrap_ci.csv)
(10 seeds × 1,600 trials = 8,000 total)
**Reproducible:** `python scripts/multi_seed.py --n-seeds 10 --trials 5`

---

## v4.2.1 retraction notice

The earlier version of this document presented seven "findings" extracted from
the Phase 2b simulation. **All seven were retracted in v4.2.1** because the
simulation is a parameterized risk model — `MODEL_BASE_ASR` and
`CATEGORY_MULTIPLIERS` in `evaluate_phase2b.py` are hand-tuned to match
published literature ASRs. Running the simulation re-states the prior under
different seeds; it does not produce independent evidence about model behaviour.

The original "findings" were therefore restatements of the calibration inputs,
not measurements. They are retained in `git log` for full audit trail but
should not be cited as research findings.

---

## What the simulation actually is

A **calibrated mock pipeline** with three legitimate uses:

1. **Pipeline validation** — does the harness produce the expected output schema?
   Are the trial counts correct? Are the bypass/severity invariants maintained?
   (All confirmed by `pytest tests/ -v` — 10/10 passing.)
2. **Compute budget sizing** — at ~$0.20/call for `claude-opus-4-8`, 1,600 trials
   project to ~$320 — calibrating the $1,000 Phase 2b request.
3. **Schema shake-out** — the downstream `evaluate_judge.py` and
   `generate_figures.py` scripts run against simulated data first so the live
   run does not encounter analysis-pipeline bugs at expensive API time.

## What the simulation is NOT

- A measurement of any model's safety alignment
- Evidence that `claude-opus-4-8` is "20% vulnerable"
- A finding that Tier-3 bypasses concentrate in any specific categories
  (the gating thresholds determine that)
- A bootstrap confidence interval on any empirical quantity
- A statistically significant comparison between models

## What Phase 2b live execution will produce (the actual findings)

When credits land and `evaluate_live.py` runs against the 2026 frontier:

| Output | Why it is genuine evidence |
|---|---|
| Per-(model, category) Wilson 95% CI on bypass rate | Measured against real model responses to controlled stimuli |
| Pairwise McNemar p-values between models | Valid because the same patterns are scored on each model |
| Cochran's Q across 4 models per category | Valid because each pattern × temperature × trial becomes a matched observation |
| Per-pattern severity histogram | Measured, not parameter-derived |
| Latency × severity correlation | Empirical signal of reasoning-mediated bypasses |
| Cross-vector composite ASR (Cat 6 → Cat 5, etc.) | Tests interaction effects the prior does not encode |

These will be findings. The simulation outputs above are not.

---

## Why this document still exists (instead of being deleted)

Three reasons to keep it:

1. **Transparency.** Earlier versions of the repo presented simulation outputs
   as findings. Deleting the document would erase that record. Keeping it with
   an explicit retraction is more honest than a silent removal.
2. **Process documentation.** This is exactly the kind of artifact a peer reviewer
   should see — evidence that the author can self-correct after critical review,
   not just defend prior claims. Research maturity is demonstrated by retractions
   when warranted, not by their absence.
3. **Pipeline-validation reference.** The simulation outputs are still useful as
   a regression baseline. If a future Phase 2b live result diverges wildly from
   the prior, that itself is informative — either the prior was wrong, or the
   model has changed, or our adversarial inputs are operating differently in
   live conditions than in literature.

---

## Pointer to honest current state

For the actual current state of the work:

| What | Where |
|---|---|
| Predictive risk model definition | [`evaluate_phase2b.py`](../evaluate_phase2b.py) (`MODEL_BASE_ASR`, `CATEGORY_MULTIPLIERS`) |
| Simulation outputs (correctly labeled) | [`data/results/`](../data/results/) |
| Statistical test script (valid only on live data) | [`scripts/statistical_tests.py`](../scripts/statistical_tests.py) |
| Live evaluation harness (awaiting credits) | [`evaluate_live.py`](../evaluate_live.py) |
| Phase 3 defense framework spec | [`paper/phase3_defense_framework.md`](../paper/phase3_defense_framework.md) |
| Research paper (with v4.2.1 framing corrections) | [`paper/research-paper.md`](../paper/research-paper.md) |
| Changelog with retraction history | [`CHANGELOG.md`](../CHANGELOG.md) v4.2.1 |

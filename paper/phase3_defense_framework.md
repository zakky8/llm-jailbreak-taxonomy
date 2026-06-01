# Phase 3 — Defense Evaluation Framework

**Status:** Specification (Phase 2b live data is a prerequisite)
**Goal:** Apply the Phase 2b harness to *measure defense effectiveness*, not just
attack success rate.

This document specifies the framework. Code stubs in [`evaluate_defenses.py`](../evaluate_defenses.py)
will follow once Phase 2b live data exists.

---

## Why a separate phase

Phase 2b measures the **attack surface**: ASR per (model, category, pattern)
under baseline alignment training only. Phase 3 measures the **defense surface**:
how each documented defense intervention shifts ASR when applied to the same
attack battery.

Without Phase 3, ASR numbers in isolation tell you *that* models are vulnerable.
Phase 3 tells you *which defenses move which categories*, which is what a
deployment engineer needs to know.

---

## Defense intervention catalogue

Each defense is sourced from primary literature (full verification per the
audit standards in [`METHODOLOGY.md`](../METHODOLOGY.md)).

| ID | Defense | Source | Targets categories |
|---|---|---|---|
| **D1** | Constitutional Classifiers v1 (input/output) | Sharma 2025, arXiv:2501.18837 | 1, 2, 3, 5, 6, 8 |
| **D2** | Constitutional Classifiers v2 (40× efficient) | Cunningham 2026, arXiv:2601.04603 | 1, 2, 3, 5, 6, 8 |
| **D3** | Input sanitization (regex + token filters) | Greshake 2023 (defense baseline) | 2, 3 |
| **D4** | Privilege separation (LLM agent isolation) | Greshake 2023 (defense baseline) | 2, 10 |
| **D5** | Perplexity filter (low-perplexity reject) | Jain et al. 2023 | 3 |
| **D6** | Cross-encoding classifier (Unicode-norm) | Deng 2023, arXiv:2310.06474 | 3 |
| **D7** | Sliding-window safety check | Anil 2024 (defense baseline) | 4 |
| **D8** | Conversation-level intent tracking | (none widely published) | 5 |
| **D9** | System-prompt confidentiality training | Sharma 2025 | 6 |
| **D10** | Rate limiting + human-in-the-loop | Hagendorff 2026 (defense baseline) | 7 |
| **D11** | Adversarial training (mutation-robust) | Standard ML | 8 |
| **D12** | Cross-modal safety classifier | UltraBreak 2026 (defense baseline) | 9 |
| **D13** | Tool output validation | (none widely published) | 10 |
| **D14** | Memory integrity checks | (none widely published) | 10 (memory) |
| **D15** | Representation-based detection | Kadali 2026, arXiv:2602.11495 | All (defense layer) |

**D8, D13, D14 are nascent — no widely-published defense.** Phase 3 measurements
for these will be qualitative (does the defense, when implemented as documented,
reduce ASR at all?) rather than quantitative.

---

## Phase 3 measurement schema

For each (defense, category) cell, three measurements are recorded:

| Measurement | Formula | Interpretation |
|---|---|---|
| **Defense Reduction Ratio (DRR)** | (ASR_baseline − ASR_with_defense) / ASR_baseline | 1.0 = perfect mitigation; 0 = no effect; <0 = made worse |
| **False Refusal Rate Delta (Δ FRR)** | FRR_with_defense − FRR_baseline | Production cost of the defense on benign inputs |
| **Net Robustness Gain (NRG)** | DRR × (1 − Δ FRR) | Combined attack reduction adjusted for benign-input cost |

A defense with DRR = 0.9 but Δ FRR = 0.5 has NRG = 0.45 — half its raw value
once production cost is accounted for. This formula matches the Constitutional
Classifiers v2 paper's framing of "0.05% production refusal" as the key
performance metric.

---

## Specific experiments planned for Phase 3

### Experiment 3.1 — Constitutional Classifiers v2 cross-category profile

```
For each category 1..10:
  baseline_ASR = mean Phase 2b ASR for claude-opus-4-8 (no extra defense)
  with_v2_ASR  = mean ASR under simulated CC v2 wrapper
  DRR_v2[cat] = (baseline_ASR - with_v2_ASR) / baseline_ASR
```

**Predicted outcome (testable):** DRR_v2 is high (>0.9) for Cats 1, 2, 3, 6, 8
where the published defense targets the attack mechanism. DRR_v2 is lower for
Cats 5, 7, 10 where the v2 paper does not specifically intervene. Confirming
or refuting this predicted profile is the headline Phase 3 finding.

### Experiment 3.2 — Multi-turn intent tracking (D8) — does a published-tutorial defense work?

There is no widely-published multi-turn defense as of 2026-06. Phase 3 implements
the most-cited *tutorial-grade* approach (conversation-level intent tracking
via a separate judge model) and measures DRR on Cat 5 patterns. If DRR is
materially > 0, the work suggests this informal defense should be productionized.

### Experiment 3.3 — Defense stacking

Are defenses additive? Compose D2 (CC v2) + D8 (intent tracking) + D9 (sys-prompt
confidentiality) and measure compound DRR vs. the linear sum of individual DRRs.
Anthropic's published statements suggest defense stacking is super-additive
(non-linear gains from combining). Phase 3 tests this empirically.

### Experiment 3.4 — Where representation-based detection (Kadali 2026) wins

`Jailbreaking Leaves a Trace` (arXiv:2602.11495) claims internal-representation
geometry distinguishes jailbreak prompts. Phase 3 implements the detector
descriptive heuristic on the Phase 2b trial outputs and reports per-category
precision/recall. If the detector achieves >0.95 recall with <0.05 false-positive
rate on benign traffic, it joins D1–D15 as a viable production filter.

---

## Compute estimate (Phase 3, beyond the $1,000 Phase 2b request)

| Item | Estimated cost |
|---|---:|
| Re-run Phase 2b under CC v2 wrapper (1,600 trials) | ~$320 |
| Multi-turn defense (D8) — Cat 5 only, 400 trials | ~$80 |
| Defense stacking — Cats 5, 7, 10, 1,200 trials | ~$240 |
| Representation detector eval — judge-model inference on existing trials | ~$120 |
| Benign-input FRR measurement (1,000 benign queries × 4 defense configs) | ~$60 |
| Buffer | ~$80 |
| **Phase 3 total** | **~$900** |

**Phase 3 is a separate funding request** if Phase 2b succeeds. We do not request
Phase 3 budget in the current Anthropic External Researcher Access Program
application; that application is exclusively for Phase 2b's $1,000 line item.

---

## Why Phase 3 matters

A taxonomy + attack-side benchmark by itself is informational. The pairing of
attack measurement (Phase 2b) with defense measurement (Phase 3) is what makes
the research **actionable for safety engineers** — it tells you not only where
the model is vulnerable but **which defenses are worth deploying** for which
specific threat category.

This pairing — attack characterization plus matched defense evaluation — is the
core contribution this taxonomy aims to deliver.

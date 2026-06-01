# How This Taxonomy Aligns With Anthropic's Published Safety Work

A direct mapping from each of the 10 taxonomy categories to relevant Anthropic
publications and how the live empirical run extends — rather than duplicates —
the prior work.

This document is technical and self-contained; it makes no claim of partnership,
endorsement, or affiliation with Anthropic. All citations are public.

---

## Category 1 — Role-Play & Persona Attacks

| Anthropic prior work | What it covers | What our live run adds |
|---|---|---|
| **Constitutional AI** (Bai et al. 2022, arXiv:2212.08073) | Self-critique training against persona prompts | Independent black-box measurement of the 2026 deployed model under fictional-framing variants not present at training time |
| **Many-Shot Jailbreaking** (Anil et al. 2024) | Many-shot demos shift the in-context behavior distribution | Composite: Cat 1 (persona) + Cat 4 (many-shot) — measured jointly, not in isolation |
| **Constitutional Classifiers v2** (Cunningham 2026, arXiv:2601.04603) | Production input/output classifiers with 0.05% refusal rate | Direct stress-test of whether the v2 defense holds under our 5-pattern persona battery on `claude-opus-4-8` |

**Specific testable claim from our simulation:** Claude Opus 4-8 produces zero
Tier-3 outcomes on Cat 1 patterns. Live data will either confirm Constitutional
Classifiers v2 fully mitigates persona attacks, or identify residual failure modes.

---

## Category 2 — Direct Prompt Injection

| Anthropic prior work | What it covers |
|---|---|
| Constitutional Classifiers v1/v2 | Input/output classifier defense |
| Anthropic-published red-team reports | Direct PI evaluation |

**Our value-add.** We test the 2026 Promptware Kill Chain framing (Brodt,
Schneier et al., arXiv:2601.09625) which reframes PI as a 7-stage maturing
discipline. Direct PI is no longer the threat — **stage-3 reconnaissance**
followed by **stage-4 persistence** is. Our Cat 2 + Cat 10 composite trials
test the multi-stage chain, not the isolated direct attempt.

---

## Category 3 — GCG / Adversarial Suffix

| Anthropic prior work | What it covers |
|---|---|
| Constitutional Classifiers v1 (Sharma 2025) | Defense against universal jailbreaks; 0.38% production refusal increase |
| Hagendorff 2025 (cited by Anthropic) | LRM-driven adversarial suffix generation |

**Our value-add.** We benchmark against the published 2024 GCG attack on
`claude-opus-4-8` — a target the original paper did not have access to. We do
**not** generate new suffixes (this avoids the dual-use concern); we use
published universal suffixes from Zou et al. 2023 to measure transferability
to the 2026 model.

---

## Category 4 — Context Window Manipulation

| Anthropic prior work | What it covers |
|---|---|
| Many-Shot Jailbreaking (Anil 2024) | Anthropic's own characterization |

**Our value-add.** Many-shot was characterized on the 2024 model generation.
Our live run tests whether the empirical scaling law (ASR ~ log(shots))
documented by Anil et al. holds on Claude Opus 4-8 — and at what shot count
the model transitions from refusal to compliance. This is a direct,
measurable extension of Anthropic's own paper.

---

## Category 5 — Multi-Turn Conversational Deception

| Anthropic prior work | What it covers |
|---|---|
| (None known — multi-turn is the biggest internal eval gap per public statements) |

**Our value-add — this is the highest-leverage finding.** Multi-turn is the
category with the largest gap between observed effectiveness (DRA 91.1% on
GPT-4; FITD 94% avg) and standard benchmark coverage. Anthropic's publicly
released Constitutional Classifiers evaluations focus on single-turn input/output
classification. Our live run quantifies the residual multi-turn vulnerability
on a Constitutional-Classifiers-protected model.

**Specific deliverable.** A 95% bootstrap CI on Tier-3 critical-bypass rate
under Cat 5 patterns, with sufficient trial budget (5 trials × 5 seeds = 25
observations per pattern × 4 patterns × `claude-opus-4-8` = 100 measurements).
This is enough power to detect a true bypass rate of 5% vs 25% with high
confidence.

---

## Category 6 — System Prompt Extraction

| Anthropic prior work | What it covers |
|---|---|
| Sharma 2025 (Constitutional Classifiers) | Mentions system prompt confidentiality |

**Our value-add.** We test the **amplification chain** — using extracted
system prompts to construct targeted Cat 5 / Cat 1 attacks. This sequencing
is the actual production threat; standalone extraction is not.

---

## Category 7 — LRM Autonomous Attacks

| Anthropic prior work | What it covers |
|---|---|
| Hagendorff 2025 / Nature Comms 2026 | 97.14% ASR; cited by Anthropic safety researchers |

**Our value-add.** **No published defense as of June 2026.** Our live run
provides the first independent measurement of LRM-autonomous bypass rates on
`claude-opus-4-8` under realistic production conditions. This is the single
most strategically important category for Anthropic's Trust & Safety team.

---

## Category 8 — Fuzzing-Based Attacks

| Anthropic prior work | What it covers |
|---|---|
| Sharma 2025 v1 / Cunningham 2026 v2 | Designed in part to mitigate semantic fuzzing |

**Our value-add.** Direct test of whether Constitutional Classifiers v2 reduces
JBFuzz-style attacks below the 99% baseline. We use the published JBFuzz v1
seeds without generating novel mutations (dual-use mitigation).

---

## Category 9 — Multimodal Injection

| Anthropic prior work | What it covers |
|---|---|
| Claude vision-capable model documentation | Public capability description |

**Our value-add.** **Cross-lab transfer test.** UltraBreak (arXiv:2602.01025)
demonstrates that VLM jailbreaks transfer across labs. Our live run measures
whether published transfer attacks succeed on Claude Opus 4-8's vision pipeline.
This category is essentially un-benchmarked in HarmBench / JailbreakBench / AdvBench.

---

## Category 10 — Agentic Chain Exploitation

| Anthropic prior work | What it covers |
|---|---|
| Anthropic Computer Use documentation | Public agentic deployment |
| (No published defense for memory persistence as of 2026-05) |

**Our value-add.** Test of three 2026 papers on `claude-opus-4-8`:
- **PoisonedRAG** (90% with 5 docs, USENIX 2025) — RAG-poisoning
- **MINJA** (95% / 70% via memory, arXiv:2601.05504-related) — memory injection
- **Hidden in Memory** (arXiv:2605.15338) — sleeper memory poisoning, 99.8% on GPT-5.5

The sleeper-memory finding is the most severe: payloads remain dormant and
activate in later sessions with the same model. No published defense exists.

---

## What the live run produces — concrete deliverables

| Deliverable | Format | Anthropic-specific value |
|---|---|---|
| Per-category Tier-3 critical-bypass rate, 95% CI | CSV + figure | Direct stress-test of Constitutional Classifiers v2 across 10 categories |
| Multi-turn quantification on `claude-opus-4-8` | CSV + figure | First independent multi-turn evaluation of a CC-v2-protected model |
| Cross-category composite ASR (Cat 6→5, Cat 2→10) | CSV | Production threat model not addressed by single-category benchmarks |
| Latency × severity distribution | Figure | Detection signal — high-latency Tier-3 outcomes suggest reasoning-mediated bypasses (LRM-style) |
| Disclosure-protocol-compliant findings report | Markdown, sanitized | Mechanism-only public report; raw payloads gated, novel findings reported privately first per `DISCLOSURE.md` |

---

## Disclosure commitment

Per [`DISCLOSURE.md`](../DISCLOSURE.md):

- All novel bypass findings will be disclosed to **Anthropic Trust & Safety** before
  any public release
- Minimum 90-day embargo on novel findings
- Mechanism descriptions only in public artifacts; raw optimized payloads excluded
- Co-disclosure to OpenAI Preparedness, DeepMind Safety where the finding generalizes

This is not a "we found bugs, give us credits" framing — it is a **defensive
characterization framework whose findings flow back to the labs whose models
are evaluated**, before they flow anywhere public.

---

*This document maps technical content. It does not claim affiliation with, partnership
with, or sponsorship by Anthropic.*

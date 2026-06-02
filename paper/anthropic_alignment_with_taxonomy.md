# External Comparison — Taxonomy Coverage vs Anthropic Published Defenses

A neutral mapping from each of the 10 taxonomy categories to publicly-documented
Anthropic defenses, with citations. This is a comparison document, not a
prescription — no claim is made about what Anthropic should prioritize, and no
affiliation, endorsement, or insider knowledge is asserted.

> ⚠ **v4.2.1 rewrite.** The earlier version of this document used editorial
> language ("biggest internal eval gap," "highest-leverage finding," "stress-test")
> implying insider judgment of Anthropic's priorities. That framing was
> retracted in v4.2.1. This rewrite uses only publicly-citable mappings and
> states what the live Phase 2b run would *measure*, not what Anthropic *should
> prioritize*.

---

## Mapping table

| Taxonomy Category | Anthropic public artifact addressing this category | What live Phase 2b would measure |
|---|---|---|
| 1 — Role-Play & Persona | Constitutional AI (Bai 2022, arXiv:2212.08073); Constitutional Classifiers v2 (Cunningham 2026, arXiv:2601.04603) | Bypass rate on RP-01 through RP-05 under the CC-v2-protected `claude-opus-4-8` |
| 2 — Direct Prompt Injection | Constitutional Classifiers v1/v2 | Direct PI bypass rate; comparison to Greshake 2023 baseline |
| 3 — GCG / Adversarial Suffix | Sharma 2025 reports 3,000+ hours of red-teaming against universal suffixes | Transferability of published Zou 2023 suffixes to claude-opus-4-8 |
| 4 — Context Manipulation | Many-Shot Jailbreaking (Anil 2024 — Anthropic Research) | Whether Anil's ASR ~ log(shots) law holds on `claude-opus-4-8` |
| 5 — Multi-Turn Deception | (No widely-cited Anthropic publication specifically on multi-turn defense as of 2026-06) | Bypass rate on DRA/FITD/Crescendo patterns on `claude-opus-4-8` |
| 6 — System Prompt Extraction | Sharma 2025 (CC v1) discusses system-prompt confidentiality | Extraction rate on SE-01 through SE-05 |
| 7 — LRM Autonomous Attacks | (No published Anthropic defense as of 2026-06; Hagendorff 2025 is independent research) | Bypass rate under LRM-driven adversarial reasoning on `claude-opus-4-8` |
| 8 — Fuzzing-Based | CC v1/v2 are designed in part for semantic perturbation defense | Whether the published JBFuzz v1 ASR (99% on 9 LLMs) is reduced under CC v2 |
| 9 — Multimodal Injection | Claude vision-capable model documentation (capability, not defense paper) | Whether UltraBreak 2026 (arXiv:2602.01025) transfer attacks succeed on Claude's vision pipeline |
| 10 — Agentic Chain Exploitation | Anthropic Computer Use documentation; no published memory-persistence defense | Bypass rate on PoisonedRAG, MINJA-style memory-injection, and Sleeper Memory Poisoning patterns |

---

## Specific citations used in this comparison

All citations are direct-WebFetch verified per the audit standards in
[`METHODOLOGY.md`](../METHODOLOGY.md). Verification status as of 2026-06-01:

- Bai et al. (2022) — Constitutional AI: Harmlessness from AI Feedback —
  [arXiv:2212.08073](https://arxiv.org/abs/2212.08073)
- Anil et al. (2024) — Many-Shot Jailbreaking — Anthropic Research
- Sharma et al. (2025) — Constitutional Classifiers v1 —
  [arXiv:2501.18837](https://arxiv.org/abs/2501.18837) (43 authors)
- Cunningham et al. (2026) — Constitutional Classifiers v2 —
  [arXiv:2601.04603](https://arxiv.org/abs/2601.04603) (28 co-authors;
  "40× computational cost reduction · 0.05% refusal rate on production traffic")

---

## What this document does NOT claim

- It does not claim that this taxonomy identifies gaps Anthropic is unaware of
- It does not claim that any specific Anthropic defense is or is not adequate
- It does not claim insider knowledge of Anthropic's internal priorities or
  red-team activities
- It does not constitute a recommendation about Anthropic's research roadmap

The single thing it claims: **for each of 10 categories, here is a public
Anthropic artifact addressing that category, and here is the specific quantity
the live Phase 2b run would measure.** Whether those measurements are useful is
for the reader (and for Anthropic, if they choose to look) to decide.

---

## Disclosure commitment (unchanged from `DISCLOSURE.md`)

Any novel bypass finding from the live Phase 2b run will be disclosed privately
to Anthropic Trust & Safety before any public release, with a 90-day embargo.
Mechanism-only descriptions in public artifacts; raw optimized payloads
excluded. This applies whether or not Anthropic funds the work.

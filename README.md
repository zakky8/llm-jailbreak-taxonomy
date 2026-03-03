# LLM Jailbreak Taxonomy

### A Systematic Taxonomy of Jailbreak Techniques in Large Language Models: Toward Robust Safety Alignment

**Zakky** · Independent AI Safety Researcher · March 2026

[![Phase](https://img.shields.io/badge/Phase-2_%E2%80%94_Empirical_Evaluation-blue)]()
[![Patterns](https://img.shields.io/badge/Attack_Patterns-30_documented-informational)]()
[![Categories](https://img.shields.io/badge/Taxonomy_Categories-6-success)]()
[![Disclosure](https://img.shields.io/badge/Disclosure-Responsible-critical)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()

---

## Overview

Effective defense against adversarial LLM attacks requires a precise understanding of the attack surface. This repository documents a systematic, mechanism-grounded taxonomy of jailbreak techniques organized by the specific alignment assumption each exploits — not by surface-level prompt patterns.

The taxonomy currently covers **30 attack patterns across 6 categories**, each documented with:
- Mechanism of action and underlying alignment failure
- Sophistication spectrum (naive → advanced)
- Exploited assumption explicitly stated
- Literature grounding with primary references
- Evaluation protocol for Phase 2 empirical testing

This work is conducted under **responsible disclosure principles**. The research focus is categorization and defense evaluation — not attack optimization.

---

## Research Question

> How do different categories of jailbreak techniques exploit weaknesses in LLM safety alignment, what specific alignment assumptions does each subvert, and how robust are current defensive mechanisms — including classifier-based filtering and constitutional training objectives — against realistic, multi-vector adversarial conditions?

---

## Six-Category Taxonomy

| # | Category | Notebook | Patterns | Exploited Alignment Assumption | Priority |
|---|---|---|:---:|---|:---:|
| 1 | Role-Play & Persona Attacks | `experiment_01` | 5 | Safety objective dominates instruction-following under fictional framing | HIGH |
| 2 | Direct Prompt Injection | `experiment_02` | 5 | Models reliably distinguish authorized from adversarial instructions | HIGH |
| 3 | Token-Level Smuggling | `experiment_03` | 7 | Safety classifiers generalize across encoding schemes | MED-HIGH |
| 4 | Context Window Manipulation | `experiment_04` | 4 | Safety instructions maintain consistent influence regardless of position | MED |
| 5 | Multi-Turn Conversational Deception | `experiment_05` | 4 | Turn-level safety evaluation is sufficient | HIGH |
| 6 | System Prompt Extraction | `experiment_06` | 5 | System prompt confidentiality maintained under adversarial pressure | MED |

**Why these priorities?** Role-play, injection, and multi-turn attacks combine high observed effectiveness with structural alignment failures that are unlikely to be resolved by surface-level patches. Multi-turn deception receives special attention as it is the most underrepresented category in current safety benchmarks relative to its observed effectiveness.

---

## Threat Model

**Black-box adversary** — API access only, no model weights or gradients.

The adversary is knowledgeable (familiar with RLHF, Constitutional AI, and published jailbreak literature), adaptive (able to iterate based on model responses), and realistic (operating under production deployment constraints). This reflects the dominant threat in deployed LLM applications.

---

## Repository Structure

```
llm-jailbreak-taxonomy/
│
├── README.md                          ← This file
├── RESEARCH.md                        ← Full methodology, threat model, research status
├── COMPLIANCE.md                      ← Compliance w/ Anthropic AUP and Access Programs
├── CONTRIBUTING.md                    ← Contribution guidelines for patterns
├── DISCLOSURE.md                      ← Responsible disclosure protocol
├── CITATION.cff                       ← Citation guidelines
├── METHODOLOGY.md                     ← Phase 2a/2b testing protocols
│
├── paper/
│   └── research-paper.md              ← Full academic paper (preprint draft)
│
├── notebooks/
│   ├── experiment_01_roleplay.ipynb   ← Cat. 1: Role-Play & Persona Attacks
│   ├── experiment_02_injection.ipynb  ← Cat. 2: Direct Prompt Injection
│   ├── experiment_03_token_smuggling.ipynb ← Cat. 3: Token-Level Smuggling
│   ├── experiment_04_context.ipynb    ← Cat. 4: Context Window Manipulation
│   ├── experiment_05_multiturn.ipynb  ← Cat. 5: Multi-Turn Deception
│   └── experiment_06_extraction.ipynb ← Cat. 6: System Prompt Extraction
│
├── data/
│   ├── prompt_patterns.csv            ← 30 categorized attack pattern records
│   └── results/
│       └── phase2a_manual_observations.csv ← 22 manual trials (Claude + ChatGPT)
│
└── findings/
    ├── preliminary_results.md         ← Pre-empirical observations & cross-category analysis
    ├── lesswrong_af_post_draft.md     ← Draft post for LessWrong / AI Alignment Forum
    └── program_application_draft.md   ← Draft application for API access program
```

Each experiment notebook contains: taxonomy dataclass definitions, mechanism analysis, alignment assumption mapping, visualizations, Phase 2 evaluation protocol, and results schema ready for data ingestion.

---

## Research Status

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Literature review, taxonomy construction, notebook framework | ✅ Complete |
| Phase 2a | Manual qualitative observation — 22 trials, Claude + ChatGPT | ✅ Complete |
| Phase 2b | Controlled API evaluation — multi-model, ≥5 trials per variant | 🔬 In Progress |
| Phase 3 | Cross-category analysis, defense mapping, publication | ⏳ Pending |

**Phase 1 deliverables complete:** Six-category taxonomy, 30 patterns, mechanism-to-assumption mapping, per-category evaluation protocols, preprint paper draft, 6 experiment notebooks.

**Phase 2a complete:** 22 manual observations across RP, PI, TS, SE categories. Claude 3.5 Sonnet: severity 0 across all naive/intermediate single-turn patterns. GPT-4o: severity 1 on RP-02, RP-04, TS-01, TS-05 — cross-model variation confirmed. Full data: `data/results/phase2a_manual_observations.csv`.

**Phase 2 in progress** — pending API access for controlled evaluation.

---

## Preliminary Findings (Pre-Empirical)

Based on literature review and limited qualitative testing:

**Finding 1 — Role-play attacks remain structurally unresolved.** Wei et al. (2023) identify competing objectives as the root cause. Multiple safety fine-tuning rounds have not eliminated the vulnerability, suggesting it cannot be patched without addressing the underlying objective conflict.

**Finding 2 — Multi-turn attacks represent the largest benchmark coverage gap.** Liu et al. (2024) report meaningfully higher success rates for multi-turn attacks relative to single-turn equivalents. Standard benchmarks (HarmBench, MT-Bench safety variants) evaluate primarily single-turn inputs — a measurement gap with direct production safety consequences.

**Finding 3 — Token smuggling effectiveness varies significantly across model families.** Zou et al. (2023) demonstrate cross-model transferability, but success rates differ considerably. This variation suggests models differ in whether safety classifiers operate on raw tokens, decoded representations, or semantic content — an architectural question with defensive implications.

**Finding 4 — System prompt extraction is a force multiplier.** Successful extraction provides adversaries with precise constraint boundaries, enabling targeted attacks across all five other categories. Its risk is systemic, not isolated.

Full preliminary findings: [`findings/preliminary_results.md`](findings/preliminary_results.md)

---

## Planned Outputs

| Output | Description | Status |
|---|---|---|
| Research paper | Full taxonomy, empirical results, defense recommendations | Draft complete |
| Evaluation dataset | Categorized prompt patterns + empirical results | Patterns documented; results pending |
| Open-source benchmark | Reproducible jailbreak robustness evaluation framework | Planned (Phase 3) |
| Responsible disclosure | Critical findings shared with model providers prior to publication | Protocol established |

---

## Responsible Disclosure

All significant findings will be disclosed to affected model providers before any public release. This research is designed to strengthen AI safety defenses — not to enable misuse. Specific harmful payloads are excluded from all public documentation; only mechanisms and structural patterns are published.

For sensitive findings or collaboration inquiries, contact prior to any public disclosure.

---

## References

- Anil, C., et al. (2024). Many-shot jailbreaking. *Anthropic Research.*
- Anthropic. (2025). Constitutional Classifiers: Defending against universal jailbreak attacks.
- Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv:2212.08073.*
- Greshake, K., et al. (2023). Compromising LLM-integrated applications with indirect prompt injection. *ACM CCS.*
- Liu, Y., et al. (2024). Jailbreaking LLMs in few queries via disguise and reconstruction. *USENIX Security.*
- Perez, E., et al. (2022). Red teaming language models with language models. *EMNLP.*
- Shen, X., et al. (2023). Characterizing and evaluating in-the-wild jailbreak prompts. *ACM CCS.*
- Wei, A., et al. (2023). Jailbroken: How does LLM safety training fail? *NeurIPS 36.*
- Zou, A., et al. (2023). Universal and transferable adversarial attacks on aligned language models. *ICML.*

---

*Research conducted under responsible disclosure principles. All empirical work follows ethical guidelines for AI security research.*

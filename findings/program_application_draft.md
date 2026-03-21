# Anthropic External Researcher Access Program — Application

**Applicant:** Zakky — Independent AI Safety Researcher
**Repository:** https://github.com/zakky8/llm-jailbreak-taxonomy
**Date:** March 2026

---

## Research Summary

**Title:** A Systematic Taxonomy of Jailbreak Techniques in Large Language Models: Toward Robust Safety Alignment

**One-sentence summary:** I have built a complete, mechanism-grounded evaluation framework for LLM adversarial robustness across 10 attack categories and 40 patterns, and am applying for API credits to execute the controlled live evaluation that will produce the empirical dataset.

---

## The Research Problem

Existing safety evaluations treat jailbreak techniques as isolated incidents rather than as symptoms of specific, structural alignment failures. When a new attack variant emerges, it is patched directly — without addressing the underlying assumption it exploited. The result is a reactive defense posture that will remain permanently behind the adversarial frontier.

Effective, proactive defense requires a diagnostic framework: a systematic map of *which alignment assumptions* are being exploited, *why* existing defenses fail to address them at the structural level, and *which attack categories* remain unaddressed by current benchmarks.

This research builds that framework.

---

## What Has Been Accomplished

### Phase 1 — Taxonomy Construction (Complete)

A ten-category, mechanism-grounded taxonomy covering 40 documented attack patterns. Each pattern is mapped to:
- The specific alignment assumption it exploits
- The structural root cause (drawing on Wei et al. 2023, Greshake et al. 2023, Anil et al. 2024, Shah et al. 2025)
- Known defensive interventions and their limitations

The ten categories span the full adversarial surface: Role-Play & Persona Attacks, Direct Prompt Injection, Token-Level Smuggling, Context Window Manipulation, Multi-Turn Conversational Deception, System Prompt Extraction, LRM Autonomous Attacks, Fuzzing-Based Attacks, Multimodal Injection, and Agentic Chain Exploitation.

Notable structural contributions:
- **Multi-turn deception (Category 5)** is identified as the largest gap between threat severity and benchmark coverage. Standard evaluations (HarmBench, MT-Bench safety variants) test primarily single-turn inputs. A conversation-level evaluation framework for this category is among the most novel contributions of this work.
- **LRM Autonomous Attacks (Category 7)** and **Fuzzing-Based Attacks (Category 8)** are newly documented categories with CRITICAL priority ratings, supported by Shah et al. (2025) and JBFuzz (2025) respectively. No systematic defense has been published for either as of this writing.
- **System Prompt Extraction (Category 6)** is documented as a *force multiplier* for all other categories — its risk is systemic, not isolated.

**Deliverables from Phase 1:**
- 40 attack patterns across 10 categories (`data/prompt_patterns.csv`)
- 10 experiment notebooks (one per category), each containing mechanism analysis, evaluation protocol, and results schema
- Full academic paper draft (`paper/research-paper.md`)
- Responsible disclosure protocol (`DISCLOSURE.md`)

### Phase 2a — Manual Qualitative Observation (Complete)

32 real manual observations conducted using Claude and ChatGPT free-tier interfaces across RP, PI, TS, and SE categories (single-turn patterns suitable for manual testing). Full data available in `data/results/phase2a_manual_observations.csv`.

Key findings from Phase 2a:
- Claude: severity 0 across all tested public patterns — consistent with strong safety training on single-turn public variants
- GPT-4o: severity 1 on RP-02 and RP-04, confirming cross-model variation in persona-framing robustness
- Provides ground-truth baseline that validates the evaluation rubric before controlled scaling

### Phase 2b — Evaluation Harness (Built; Live Execution Pending)

A complete, production-grade controlled evaluation harness (`evaluate_phase2b.py`) has been built and validated through simulation. The harness:
- Loads all 40 patterns from `data/prompt_patterns.csv`
- Iterates across 4 target models: `claude-sonnet-4-6`, `gpt-4o`, `gemini-2.0-flash`, `deepseek-v3`
- Runs 5 independent trials per pattern per model per temperature setting (0.0 and 0.7)
- Total planned trials: **1,600 controlled evaluations**
- Outputs structured results to `data/results/` with full trial metadata
- Pipes results to `evaluate_judge.py` for LLM-as-a-Judge severity grading

The harness is currently validated in simulation mode using empirical ASR distributions from published literature (Shah et al. 2025, JBFuzz 2025, Phase 2a observations). It is architecturally ready for live API execution — the only missing component is compute access.

---

## What API Credits Would Fund (Specific and Concrete)

The $1,000 credit allocation would fund exactly one well-scoped execution:

| Task | Estimated Cost |
|---|---|
| 1,600 trials × claude-sonnet-4-6 (avg ~400 tokens/call) | ~$320 |
| LLM-as-a-Judge grading of 1,600 outputs (claude-sonnet-4-6) | ~$200 |
| Cross-category interaction testing: 5 combined-vector trials × 8 combinations | ~$120 |
| Re-runs for statistical robustness on high-variance categories | ~$200 |
| Buffer for rate limit retries and prompt debugging | ~$160 |
| **Total** | **~$1,000** |

This is a tightly scoped, one-time empirical execution — not an open-ended research credit. The harness already exists; the credits fund running it.

---

## Why This Benefits Anthropic Specifically

1. **Direct stress-testing of Constitutional Classifiers.** The taxonomy includes evaluation of whether Anthropic's published Constitutional Classifiers defense (Anthropic, 2025) holds under multi-vector adversarial conditions. Category 5 (multi-turn) and Category 7 (LRM autonomous) are the most likely to reveal gaps not addressed by the input-output filtering approach. These findings will be disclosed to Anthropic before any publication.

2. **The multi-turn benchmark gap is Anthropic's problem too.** If standard safety evaluations systematically undercount multi-turn attack effectiveness, Anthropic's internal safety metrics may be overestimating robustness in production conversational deployments. This research directly addresses that measurement gap.

3. **The LRM attack surface is new and undefended.** Category 7 documents a qualitatively new threat: large reasoning models using extended chain-of-thought to iterate bypasses at machine speed. Shah et al. (2025) report >97% ASR. No published defense addresses this as of March 2026. Early empirical characterization of this category — especially on `claude-sonnet-4-6` — has direct safety research value.

4. **Responsible disclosure is built in.** The research protocol (DISCLOSURE.md) commits to a 90-day embargo on novel findings and direct notification to Anthropic's Trust & Safety team before any publication. Any significant finding from the live evaluation will be disclosed privately first.

---

## Responsible Disclosure Commitment

All significant empirical findings — including any novel bypass patterns not already documented in published literature — will be reported to Anthropic's security team via responsible disclosure before any public release, consistent with the 90-day embargo protocol in `DISCLOSURE.md`. Only mechanisms and structural patterns are published publicly; specific optimized payloads are excluded from all artifacts.

---

## Publication Plan

Upon completion of Phase 2b live evaluation:
1. Update paper with empirical results (`paper/research-paper.md`)
2. Submit to arXiv (cs.CR / cs.AI)
3. Submit to LessWrong Alignment Forum with findings summary
4. Release open-source evaluation framework for reuse by alignment researchers

The full dataset (patterns, trial results, judge scores) will be released under MIT license for community use.

---

## References

- Anil, C., et al. (2024). Many-shot jailbreaking. *Anthropic Research.*
- Anthropic. (2025). Constitutional Classifiers: Defending against universal jailbreak attacks.
- Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv:2212.08073.*
- Greshake, K., et al. (2023). Compromising LLM-integrated applications with indirect prompt injection. *ACM CCS.*
- Liu, Y., et al. (2024). Jailbreaking LLMs in few queries via disguise and reconstruction. *USENIX Security.*
- Perez, E., et al. (2022). Red teaming language models with language models. *EMNLP.*
- Shah, R., et al. (2025). Autonomous LLM-based red teaming with reasoning models. *arXiv.*
- Shen, X., et al. (2023). Do Anything Now: Characterizing and evaluating in-the-wild jailbreak prompts. *ACM CCS.*
- Wei, A., et al. (2023). Jailbroken: How does LLM safety training fail? *NeurIPS 36.*
- Zou, A., et al. (2023). Universal and transferable adversarial attacks on aligned language models. *ICML.*

---

*Research conducted under responsible disclosure principles. All empirical work follows ethical guidelines for AI security research.*

# DRAFT — Anthropic External Researcher Access Program Application
# Form: https://forms.gle/pZYC8f6qYqSKvRWn9
# Fill in [BRACKETS] before submitting

---

## Field: Name
Zakky

## Field: Email
[YOUR EMAIL]

## Field: Institution / Organization
Independent AI Safety Researcher

---

## Field: Research Topic / Description
*(Use this exact text or adapt lightly — keep it specific and concise)*

**Research title:** A Systematic Taxonomy of Mechanistic Alignment Failures in Large Language Models: Toward Robust Safety Alignment

**Summary:**

I am conducting a systematic empirical evaluation of structural safety vulnerabilities in LLMs, organized by mechanism of action and mapped to the specific alignment assumption each exploits. While often termed "jailbreaks," my research reframes these as mechanistic alignment failures (e.g. instruction-following objective dominating safety objective under fictional framing). The taxonomy covers six categories: role-play and persona framing, direct prompt injection, token-level substitution, context window manipulation, multi-turn conversational evaluation, and constraint inference — with 30 documented structural patterns in total.

Phase 1 (complete): taxonomy construction, mechanism-to-assumption mapping, evaluation protocol design, and preliminary manual testing across 22 pattern trials using free-tier interfaces. Full repository: https://github.com/zakky8/llm-jailbreak-taxonomy

Phase 2 (requiring API access): controlled multi-trial evaluation of all 40 patterns against Claude models with controlled parameters (temperature, trial count, severity scoring rubric). The Phase 2 results will be the primary empirical contribution.

The specific tests I will run with the $1,000 in API credits:

- **Category 5 — Multi-Turn Deception (MT-01 through MT-04):** 5 trials × 10 variants × 4 patterns = 200 trials. This category cannot be tested manually and is the most underrepresented in current safety benchmarks. I will measure bypass rate, turn-at-which-bypass-occurs, and preamble effect ratio vs. single-turn baseline.

- **Category 1 — Role-Play Attacks (RP-01 through RP-05):** 5 trials × 10 variants × 5 patterns = 250 trials. Baseline robustness measurement with comparison to my Phase 2a manual observations.

- **Category 3 — Token Smuggling cross-model (TS-01 through TS-06):** 5 trials × 5 variants × 6 patterns = 150 trials. Primary goal is characterizing cross-model robustness variation consistent with Zou et al. (2023).

- **Remaining categories (2, 4, 6):** Remaining credits allocated to agentic injection variants (PI-04/05), many-shot scaling curve (CM-02 at 1/5/10/20/50 shots), and extraction + amplification measurement (SE-01 through SE-05).

All results will be committed to the public GitHub repository and shared with Anthropic prior to any publication, consistent with my responsible disclosure commitment documented in the repository.

---

## Field: How will this research advance AI safety?

The primary contribution is diagnostic infrastructure for alignment researchers. The taxonomy maps the adversarial attack surface at the level of structural alignment failures — not individual prompt patterns — which enables evaluation of whether a given defense addresses the underlying vulnerability or only the current surface manifestation.

Specifically:

1. **Multi-turn evaluation gap:** Standard safety benchmarks evaluate single-turn inputs. My Phase 2 multi-turn evaluation will be among the first systematic contributions to this underserved evaluation category. The results will directly inform whether models evaluated as safe under current benchmarking conditions are equally safe in production conversational deployments.

2. **Cross-model robustness characterization:** My preliminary Phase 2a observations confirm that token smuggling effectiveness varies across Claude and ChatGPT. Systematically characterizing this variation identifies which safety classifier architectures are more robust and why — a direct input to defensive design.

3. **Responsible disclosure:** All significant findings will be shared with Anthropic before any publication. I treat this not as a formality but as a core research commitment — Anthropic's Constitutional AI and Constitutional Classifiers work are directly relevant to what I'm evaluating.

4. **Compliance:** I acknowledge the Usage Policy. My research conducts strictly defined, token-limited evaluation trials of mechanisms. It uses benign dummy payloads (e.g. instructions on baking a cake) rather than genuine high-risk illicit material, ensuring I am measuring alignment limits without engaging in explicit hostile red-teaming of production thresholds or extracting proprietary model state.

---

## Field: Team Description

I am an independent researcher working on this project individually. I do not have institutional affiliation.

I want to address this directly: I recognize that independent researchers without institutional affiliation are a less common applicant profile for this program. I believe the repository (https://github.com/zakky8/llm-jailbreak-taxonomy) demonstrates methodological rigor typically associated with institutional research — structured taxonomy with canonical pattern IDs, formal threat model, graded evaluation rubric, category-specific experiment notebooks with results schemas, and a full preprint paper draft.

In lieu of institutional oversight, I am committed to responsible disclosure directly with Anthropic as the primary accountability mechanism. I will share findings before publication and will not optimize or publish specific harmful payloads under any circumstances.

---

## Field: Any other relevant information

Repository with full documentation: https://github.com/zakky8/llm-jailbreak-taxonomy

The repository includes:
- 6 Jupyter experiment notebooks (one per category) with evaluation protocols and results schemas
- 30 documented attack patterns in `data/prompt_patterns.csv` with canonical IDs, mechanism classification, and literature references
- 22 Phase 2a manual observations in `data/results/phase2a_manual_observations.csv`
- Full preprint paper draft in `paper/research-paper.md`
- Phase 2 testing methodology in `METHODOLOGY.md`

Primary references informing the taxonomy:
- Wei et al. (2023) — *Jailbroken: How does LLM safety training fail?* NeurIPS 36
- Anil et al. (2024) — *Many-Shot Jailbreaking* — Anthropic Research
- Greshake et al. (2023) — *Indirect Prompt Injection* — ACM CCS
- Liu et al. (2024) — *Multi-turn jailbreaking* — USENIX Security
- Zou et al. (2023) — *Universal adversarial attacks on aligned LLMs* — ICML

---

## Submission Checklist (before submitting)

- [ ] Replace [YOUR EMAIL] with actual email
- [ ] Verify GitHub repo is public and accessible
- [ ] Confirm Phase 2a results CSV is committed and visible
- [ ] Submit on or just before the **first Monday of the month** (reviewed in monthly batches)
- [ ] Keep application under ~500 words per field — trim if needed

---

*Draft prepared March 2026.*

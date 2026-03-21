# A Systematic Taxonomy of Jailbreak Techniques: Mapping the Full Adversarial Surface of LLM Safety Alignment

**Author:** Zakky — Independent AI Safety Researcher
**Status:** Draft for Alignment Forum / LessWrong
**Date:** March 2026
**Repository:** https://github.com/zakky8/llm-jailbreak-taxonomy

---

## Summary

Current jailbreak research is reactive: each new attack variant gets patched without addressing the structural alignment failure that enabled it. This post introduces a mechanism-grounded taxonomy that maps 40 adversarial attack patterns across 10 categories, each tied to the specific safety alignment assumption it exploits. The goal is a diagnostic framework that makes proactive defense possible.

Key findings from Phase 2a manual testing and literature synthesis:
- Multi-turn conversational attacks are the most underrepresented category in safety benchmarks relative to their observed effectiveness — a measurement gap with direct production consequences
- Large Reasoning Models introduce a qualitatively new attack surface: autonomous, high-speed bypass planning via chain-of-thought (Shah et al., 2025: >97% ASR)
- System prompt extraction is a force multiplier for every other category, not an isolated concern
- Token-level smuggling effectiveness varies significantly across model families, suggesting architectural differences in classifier implementation that have direct defensive value

---

## Motivation: Why a Taxonomy?

The existing literature contains excellent individual attack analyses. What is missing is a unified framework that maps the *full attack surface* to the specific alignment failures each technique exploits.

The consequence of this gap is that defenses remain reactive. Wei et al. (2023) identify this precisely: safety training and instruction-following objectives genuinely conflict when a persona framing provides sufficient fictional distance. This is a structural tension, not a surface-level pattern. Patching each new DAN variant without addressing the underlying competing-objectives problem means the category remains permanently exploitable regardless of how many individual patches are applied.

The same logic applies to every category. Multi-turn attacks exploit the assumption that turn-level safety evaluation is sufficient for conversational deployments — a structural gap that cannot be closed by improving single-turn refusal training. Indirect prompt injection in agentic contexts exploits the assumption that tool outputs are sanitized instruction sources — a gap that grows with every new agentic capability added to production deployments.

Effective, proactive defense requires knowing *which assumptions are being exploited* before designing the intervention.

---

## The Ten-Category Taxonomy

### Taxonomy Design Principles

Three criteria governed category boundaries:
1. **Mechanism distinctness**: each category exploits a different alignment assumption — conflating distinct vulnerabilities produces bad defensive recommendations
2. **Minimal coverage**: the ten categories cover the known adversarial surface without redundancy
3. **Defensive actionability**: each category maps directly to candidate structural interventions

The categories are organized roughly by mechanism type, not by severity.

---

### Category 1 — Role-Play & Persona Attacks

**Mechanism:** Fictional framing overrides safety training via persona adoption.

**Exploited assumption:** Safety objectives dominate instruction-following under fictional framing.

**Root cause (Wei et al., 2023):** Competing training objectives. Safety training and instruction-following objectives genuinely conflict when persona framing provides sufficient fictional distance. This is not a prompt-engineering quirk — it is a fundamental tension in how models are trained.

**Why this matters:** Multiple rounds of safety fine-tuning have not resolved this category. Shen et al. (2023) document the persistence of DAN-variant prompts across model updates. Surface patching is insufficient; the competing-objectives structure remains.

**Patterns documented:** 5 (RP-01 through RP-05), from naive DAN variants to sophisticated hypothetical distancing.

**Defense direction:** Constraint-aware fine-tuning with persona-invariant safety representations; adversarial persona robustness training.

---

### Category 2 — Direct Prompt Injection

**Mechanism:** User or external input directly overrides system-level instructions.

**Exploited assumption:** Models reliably distinguish authorized (system-level) instructions from adversarial ones embedded in user input or tool outputs.

**Key distinction:** Direct injection (chat context) vs. indirect injection (agentic context — adversarial instructions embedded in external content processed by the agent). These require different defenses.

**Why the agentic variant matters (Greshake et al., 2023):** LLM-integrated applications that fetch, process, and act on external content are exposed to indirect injection attacks from any external source the agent touches. As agentic deployment grows, this surface grows proportionally. Current safety training focuses on direct user inputs; tool outputs and fetched content are not systematically treated as adversarial vectors.

**Patterns documented:** 5 (PI-01 through PI-05).

---

### Category 3 — Token-Level Smuggling

**Mechanism:** Prohibited content encoded via transformations that bypass safety classifier pattern matching.

**Exploited assumption:** Safety classifiers generalize robustly across encoding schemes and character-level perturbations.

**Key finding:** Effectiveness varies significantly across model families — Base64 and Unicode homoglyph bypass rates differ substantially between frontier models. This variation suggests architectural differences in whether safety classifiers operate on raw token sequences, decoded text representations, or semantic-level content. Identifying what drives this variation has direct defensive value.

**Patterns documented:** 7 (TS-01 through TS-07), including Base64, ROT13, Unicode homoglyphs, low-resource languages, payload fragmentation, and GCG adversarial suffixes.

---

### Category 4 — Context Window Manipulation

**Mechanism:** Safety instructions diluted by positional displacement, or behavioral distribution shifted by in-context demonstrations.

**Critical finding (Anil et al., 2024):** Many-shot jailbreaking scales monotonically with shot count. As context windows extend to 100k+ tokens, this attack surface expands proportionally. A defense that works at 10-shot may not hold at 100-shot.

**Patterns documented:** 4 (CM-01 through CM-04).

---

### Category 5 — Multi-Turn Conversational Deception

**Mechanism:** Harmful intent distributed across multiple turns; each turn appears individually benign; cumulative trajectory reveals attack.

**Exploited assumption:** Turn-level safety evaluation is sufficient for conversational deployments.

**The benchmark gap:** This is the most underrepresented category in safety benchmarks relative to observed effectiveness. Standard evaluations (HarmBench, MT-Bench safety variants, WildGuard) evaluate primarily single-turn inputs. Liu et al. (2024) report meaningfully higher success rates for multi-turn attacks relative to single-turn equivalents on the same models.

The implication is important: models evaluated as safe under current benchmark conditions may be substantially more vulnerable in production conversational deployments. This is a *measurement gap*, not only a robustness gap — current safety evaluation infrastructure systematically undercounts real vulnerability.

**Patterns documented:** 4 (MT-01 through MT-04), including crescendo escalation, incremental framing, and psychological commitment anchoring.

---

### Category 6 — System Prompt Extraction

**Mechanism:** Hidden system instructions revealed via direct interrogation, instruction-following exploits, or indirect inference.

**Force-multiplier role:** Extraction is not directly a content violation, but it enables targeted attacks across all other categories by revealing exact constraint boundaries. Extracted prompts reveal prohibited topic lists, safety policy language, instruction format and structure, and persona constraints — enabling adversaries to craft minimally compliant but harmful requests.

| Category | How Extraction Amplifies It |
|---|---|
| Role-Play (1) | Exact persona restrictions known — targeted fictional framings crafted |
| Prompt Injection (2) | System prompt format known — format-mimicking injection more effective |
| Token Smuggling (3) | Classifier keyword list known — encoding evasion precisely targeted |
| Context Manipulation (4) | Safety instruction text known — dilution targeted at specific sentences |
| Multi-Turn (5) | Topic restriction list known — crescendo escalation precisely calibrated |

**Patterns documented:** 5 (SE-01 through SE-05).

---

### Category 7 — LRM Autonomous Reasoning Attacks

**Mechanism:** Large Reasoning Models use extended chain-of-thought to plan and iterate bypasses at machine speed.

**Exploited assumption:** Safety alignment assumes a human adversary with limited iteration speed.

**Why this is new (Shah et al., 2025):** Reasoning models achieve >97% ASR by "reasoning through" safety boundaries in internal logic space. The attack does not rely on prompt engineering tricks — it relies on the model's own reasoning capability being turned against its safety objectives. The speed advantage is qualitative: a human adversary iterating manually across sessions is a fundamentally different threat than a reasoning model self-refining at inference speed.

**As of March 2026:** No systematic published defense addresses this category.

**Patterns documented:** 3 (LRM-01 through LRM-03).

---

### Category 8 — Fuzzing-Based Automated Attacks

**Mechanism:** High-frequency mutation of semantic payloads using automated fuzzing engines.

**Exploited assumption:** Safety classifiers have full semantic coverage across all possible token permutations.

**Key result (JBFuzz, 2025):** ~99% ASR via synonym mutation, semantic transforms, and crossover mutation hybrids. The coverage problem is combinatorially intractable for any classifier operating at the token level.

**Patterns documented:** 3 (FZ-01 through FZ-03).

---

### Category 9 — Multimodal Alignment Exploits

**Mechanism:** Exploiting the encoder-decoder safety gap where non-textual inputs bypass text-trained safety filters.

**Exploited assumption:** Safety training in the text modality transfers perfectly to vision and audio encoders.

**Current state:** Most frontier models evaluate modalities independently rather than with unified cross-modal safety classifiers. This creates a consistent gap between text-modality safety and vision-modality safety.

**Patterns documented:** 2 (MM-01 through MM-02).

---

### Category 10 — Agentic Memory & Tool Hijacking

**Mechanism:** Persisting adversarial intent across sessions via agentic memory poisoning or tool argument injection.

**Exploited assumption:** Agentic context stores and tool outputs are sanitized instruction sources.

**Why persistence matters:** Unlike chat-context attacks that expire when a session ends, agentic memory poisoning can persist across sessions, propagate to other users sharing the same memory store, and compound over time. Cross-session persistence attacks have no documented defense as of this writing.

**Patterns documented:** 2 (AG-01 through AG-02).

---

## Cross-Category Interactions

The ten categories are not orthogonal. Sophisticated attacks frequently combine mechanisms. Key interaction patterns:

| Combination | Predicted Effect |
|---|---|
| Role-Play (1) + Multi-Turn (5) | Role established across turns; harmful content elicited within sustained frame — amplified over either alone |
| Extraction (6) + Any (1–5) | Any attack with extracted constraint boundary knowledge enables precision targeting |
| Token Smuggling (3) + Multi-Turn (5) | Payload fragmented across turns; each fragment individually benign and encoded |
| Context Manipulation (4) + Role-Play (1) | Many-shot demonstrations establish role-play compliance; target request follows |

---

## Evaluation Framework

A complete evaluation harness has been developed and is available at the repository:

- **`evaluate_phase2b.py`**: Multi-model, multi-trial controlled evaluation across all 40 patterns. Supports 4 target models, 2 temperature settings, 5 trials per pattern (1,600 total trials). Currently simulation-validated using empirical ASR distributions from published literature; live API execution is the next research milestone.
- **`evaluate_judge.py`**: LLM-as-a-Judge grading of model responses against a 4-tier severity rubric.
- **10 experiment notebooks**: One per category, each containing mechanism analysis, evaluation protocol, and results schema.

---

## What I'm Looking For

**Collaboration:** If you have experience running adversarial evaluations against frontier models, or are working on multi-turn or LRM robustness, I'd be interested in discussing methodology.

**Critique:** The taxonomy construction choices — particularly the category boundaries and the mechanism-to-assumption mappings — are the most important intellectual contribution and the most likely place for errors. If you see a case where two categories are conflated, or where a mechanism is incorrectly attributed to an alignment failure, please comment.

**Replication:** The evaluation framework is open-source. If you run the live evaluation against any of the four target models before I do, please share results — cross-replication is valuable.

---

## Next Steps

1. Execute Phase 2b live API evaluation (pending compute access)
2. Submit empirical paper to arXiv (cs.CR / cs.AI)
3. Responsible disclosure of significant novel findings to affected model providers before publication

---

## References

- Anil, C., et al. (2024). Many-shot jailbreaking. *Anthropic Research.*
- Anthropic. (2025). Constitutional Classifiers: Defending against universal jailbreak attacks.
- Bai, Y., et al. (2022). Constitutional AI. *arXiv:2212.08073.*
- Greshake, K., et al. (2023). Not What You've Signed Up For. *ACM CCS.*
- JBFuzz Team. (2025). JBFuzz: Jailbreaking LLMs Efficiently and Effectively Using Fuzzing. *arXiv.*
- Liu, Y., et al. (2024). Jailbreaking LLMs via Disguise and Reconstruction. *USENIX Security.*
- Perez, E., et al. (2022). Red Teaming Language Models with Language Models. *EMNLP.*
- Shah, R., et al. (2025). Autonomous LLM-Based Red Teaming with Reasoning Models. *arXiv.*
- Shen, X., et al. (2023). Do Anything Now. *ACM CCS.*
- Wei, A., et al. (2023). Jailbroken: How Does LLM Safety Training Fail? *NeurIPS 36.*
- Zou, A., et al. (2023). Universal and Transferable Adversarial Attacks. *ICML.*

---

*All research conducted under responsible disclosure principles. No optimized harmful payloads are published — only mechanisms and structural patterns.*

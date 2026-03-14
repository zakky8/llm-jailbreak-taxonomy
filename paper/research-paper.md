# A Systematic Taxonomy of Jailbreak Techniques in Large Language Models: Toward Robust Safety Alignment

**Zakky**
Independent AI Safety Researcher
March 2026

---

## Abstract

Large language models (LLMs) trained with safety alignment objectives — reinforcement learning from human feedback (RLHF), Constitutional AI, and related techniques — remain vulnerable to adversarial inputs that redirect their instruction-following capabilities toward prohibited outputs. Effective defense requires precise, mechanistic understanding of the adversarial attack surface. This paper presents a systematic taxonomy of jailbreak techniques organized by mechanism of action and mapped to the specific alignment assumption each exploits. The taxonomy identifies six categories: (1) role-play and persona attacks, (2) direct prompt injection, (3) token-level smuggling, (4) context window manipulation, (5) multi-turn conversational deception, and (6) system prompt extraction. Across these categories, 30 attack patterns are documented, each characterized by mechanism, sophistication level, deployment context, and exploited alignment assumption. For each category, I provide a structured evaluation protocol for empirical testing under a realistic black-box threat model. Preliminary findings based on systematic literature review indicate that: role-play attacks reflect a structural competing-objectives problem unlikely to be resolved by surface-level patches; multi-turn deception represents the largest gap between observed effectiveness and benchmark coverage; and token smuggling effectiveness varies significantly across model families, suggesting architecturally meaningful differences in classifier implementation. The ultimate contribution is not to optimize adversarial attacks but to produce the diagnostic framework that enables alignment researchers and engineers to evaluate existing defenses precisely and design structurally sound improvements.

**Keywords:** large language models, jailbreak attacks, safety alignment, adversarial robustness, red-teaming, AI safety, fuzzing, autonomous attacks, multimodal injection, agentic exploitation, LRM attacks

---

## 1. Introduction

The widespread deployment of large language models has created a security research problem at the intersection of machine learning, adversarial robustness, and alignment theory. Models such as Claude (Anthropic, 2024), GPT-4 (OpenAI, 2023), and Gemini (Google DeepMind, 2024) are trained with safety objectives to prevent harmful, deceptive, or policy-violating outputs. The same generality that makes these models powerful, however, also makes them vulnerable: their instruction-following capabilities can be redirected by adversarial inputs that exploit gaps between training-time safety objectives and inference-time behavior.

The research community has produced important foundational work on this problem. Perez et al. (2022) demonstrated that LLMs can be used to automatically red-team other LLMs at scale, establishing automated adversarial probing as a viable evaluation paradigm. Zou et al. (2023) showed that gradient-optimized adversarial suffixes transfer across model families with alarming reliability, challenging assumptions about the robustness of proprietary safety training. Wei et al. (2023) provided the most rigorous mechanistic analysis to date, identifying competing training objectives and mismatched generalization as the primary structural failure modes underlying jailbreak success.

Despite these contributions, the literature lacks a unified, operationally useful taxonomy that maps the full landscape of known jailbreak techniques to the specific alignment mechanisms they subvert. Without such a framework, defensive efforts risk being reactive — patching individual exploits without understanding the structural vulnerability that enables each class of attack. This paper addresses that gap with three contributions:

1. **A six-category taxonomy** grounded in published research, organizing 30 attack patterns by mechanism of action and mapping each to the alignment assumption it exploits
2. **A structured evaluation methodology** for empirical validation under a realistic black-box threat model, ready for execution once API access is available
3. **Preliminary findings** from systematic literature review that establish research priorities and motivate the empirical design

This work is conducted with a defensive orientation: the goal is to map the adversarial attack surface comprehensively so that existing defenses — including Anthropic's Constitutional Classifiers (Anthropic, 2025) and Constitutional AI training objective (Bai et al., 2022) — can be evaluated systematically against realistic threat conditions.

---

## 2. Background and Related Work

### 2.1 Safety Alignment Techniques

Contemporary LLM safety training combines several techniques. Reinforcement learning from human feedback (Christiano et al., 2017; Ziegler et al., 2019) trains models to produce outputs rated as safe and helpful by human evaluators. Constitutional AI (Bai et al., 2022) introduces explicit safety principles that the model uses for self-critique during training, reducing dependence on human feedback for harmlessness. More recently, Anthropic's Constitutional Classifiers work (Anthropic, 2025) demonstrated that input-output classifiers trained specifically to detect jailbreak attempts can significantly reduce bypass rates while preserving helpfulness on legitimate queries.

These techniques establish the training-time safety objectives whose inference-time failures this paper characterizes. Understanding alignment techniques is a prerequisite for understanding where they fail.

### 2.2 Adversarial Robustness in Neural Networks

The study of adversarial examples in neural networks was established by Goodfellow et al. (2015), who demonstrated that small, imperceptible perturbations to inputs can reliably mislead classifiers. Carlini and Wagner (2017) developed more powerful optimization-based attacks that circumvent defenses based on gradient masking. These methods from computer vision adversarial ML directly informed Zou et al.'s (2023) GCG attack on LLMs — the application of gradient-based optimization to find adversarial suffixes that transfer across models.

### 2.3 LLM-Specific Adversarial Research

Perez et al. (2022) established LLM-based automated red-teaming, demonstrating that a red-teaming LLM can generate diverse, effective test cases revealing harmful outputs in target models at a scale impossible with manual evaluation. Their work is directly relevant to this research's Phase 2 evaluation methodology.

Zou et al. (2023) demonstrated universal adversarial suffixes: fixed token strings that, when appended to any harmful prompt, reliably suppress safety refusals across multiple model families including both open-weight and commercial models. This transferability is the most practically significant finding in adversarial LLM research to date.

Wei et al. (2023) provided the theoretical framework motivating this taxonomy. They identify two root causes of jailbreak success: (a) competing objectives — safety and instruction-following training objectives genuinely conflict under certain input distributions — and (b) mismatched generalization — models may generalize differently across the two objectives. This analysis explains why jailbreaks persist across fine-tuning iterations rather than being permanently resolved.

Anil et al. (2024) formally characterize many-shot jailbreaking, demonstrating that prepending sufficient demonstrations of harmful model compliance shifts the in-context behavioral distribution monotonically with shot count. This is the clearest empirical demonstration of in-context learning overriding safety training in the literature.

Greshake et al. (2023) establish indirect prompt injection as a distinct and underaddressed threat: adversarial instructions embedded in external content that an LLM agent processes can reliably redirect the agent's actions, with demonstrated practical attacks including data exfiltration via crafted URL parameters in fetched content.

Liu et al. (2024) systematically evaluate multi-turn jailbreak attacks, reporting meaningfully higher success rates compared to single-turn equivalents and documenting the crescendo escalation pattern. Shen et al. (2023) provide an empirical survey of in-the-wild jailbreak prompts, establishing the prevalence and diversity of attacks deployed against production systems.

---

## 3. Threat Model

The empirical phase adopts a **black-box threat model** reflecting realistic production adversarial conditions.

**Adversary capabilities:**
- API access only — no access to model weights, gradients, training data, or system prompts
- Standard production API endpoints; no special access or privileges
- Ability to make multiple sequential queries; can iterate based on model responses

**Adversary knowledge:**
- Familiar with RLHF and Constitutional AI training objectives and their known limitations
- Aware of published jailbreak techniques in the academic literature and public forums
- Informed by in-the-wild red-teaming disclosures (Shen et al., 2023)

**Adversary objective:**
- Elicit outputs that violate the target model's safety policies
- Establish persistence of attack patterns across model versions (robustness test)
- In agentic contexts (Category 2): redirect agent actions toward adversary-controlled goals

**Out of scope:** White-box attacks requiring model weight access; physical access to inference infrastructure; social engineering of developers or operators.

This threat model reflects the dominant realistic adversarial condition in production LLM deployments, where adversaries have API access but no privileged access to model internals.

---

## 4. Taxonomy of Jailbreak Techniques

The taxonomy is organized by mechanism of action — the structural property of the attack that causes safety training to fail — rather than by surface-level prompt characteristics. This design choice ensures that the taxonomy identifies defensible categories: each category maps to a distinct alignment assumption that, if made more robust, would address the corresponding attack class.

Categories are not mutually exclusive. Sophisticated attacks frequently combine elements from multiple categories, producing amplified effects through mechanism interaction. Cross-category combinations are discussed in Section 4.7.

### 4.1 Category 1 — Role-Play and Persona Attacks

**Mechanism:** Fictional framing creates sufficient distance between the user's request and the model's safety training, allowing the instruction-following objective to dominate the safety objective (Wei et al., 2023).

**Representative patterns:**
- *Unrestricted AI persona (RP-01):* Instructing the model to adopt a persona explicitly claiming no safety restrictions (DAN-variant prompts). The fictional AI persona frame provides just enough distance to activate instruction-following over safety.
- *Villain character embodiment (RP-02):* Character role-play in which the adversary-controlled character answers any question without restriction. Fictional distance is moderate; effectiveness depends on elaborateness of framing.
- *Grandmother exploit (RP-03):* Emotional or nostalgic framing (e.g., a deceased relative read the user harmful content) that contextualizes the harmful request as benign. Exploits the intersection of fictional framing and emotional context.
- *Hypothetical distancing (RP-04):* Thought-experiment framing used to make the harmful request appear to concern a fictional world rather than the real one.
- *False developer mode (RP-05):* Claimed authority to activate a special mode without safety constraints. Exploits model deference to perceived authority in addition to fictional framing.

**Exploited assumption:** Safety objectives dominate instruction-following under fictional framing.

**Why patches fail:** Wei et al. (2023) show this is a competing-objectives problem — safety and instruction-following training genuinely conflict under persona framing. This conflict cannot be resolved by blocking individual prompts without addressing the underlying objective tension.

### 4.2 Category 2 — Direct Prompt Injection

**Mechanism:** Adversarial input directly overrides system-level instructions, exploiting the model's inability to reliably partition instruction space by source authority.

**Representative patterns:**
- *Direct override (PI-01):* Explicit instruction to ignore prior system instructions. The simplest form; effective when models do not robustly weight instruction source.
- *Constraint removal (PI-02):* Explicit request to disregard safety guidelines for the current session.
- *Nested instruction framing (PI-03):* User input formatted to mimic system prompt tokens (e.g., "[SYSTEM]:"), exploiting format-based authority inference.
- *Indirect injection via external content (PI-04):* Adversarial instructions embedded in external content (web pages, documents, emails) that an agentic LLM processes. The agent model mistakes the adversarial payload for legitimate instructions. This is Greshake et al.'s (2023) primary contribution.
- *Agentic tool-use hijacking (PI-05):* Instructions in fetched content redirect agent tool calls — exfiltrating data, changing agent behavior, or triggering unintended actions.

**Exploited assumption:** Models reliably distinguish authorized (system-level) instructions from adversarial ones in user input or tool outputs.

**Agentic deployment note:** PI-04 and PI-05 are qualitatively distinct from PI-01 through PI-03. The adversary does not control the user turn — only external content the agent processes. Current safety training focuses on direct user inputs and does not systematically address this vector.

### 4.3 Category 3 — Token-Level Smuggling

**Mechanism:** Prohibited content is transformed into a surface representation that bypasses safety classifier pattern matching while remaining interpretable by the model.

**Representative patterns:**
- *Base64 encoding (TS-01):* Prohibited request encoded in Base64; model instructed to decode and respond.
- *ROT13 encoding (TS-02):* Simple substitution cipher encoding; the most naive encoding-based attack.
- *Leetspeak (TS-03):* Digit/symbol substitution for alphabetic characters in prohibited terms.
- *Unicode homoglyphs (TS-04):* Visually identical Unicode characters (e.g., Cyrillic letters) substituted for ASCII in prohibited terms — invisible to human inspection.
- *Low-resource language (TS-05):* Harmful request submitted in a language with sparse safety training data, exploiting differential classifier coverage across languages.
- *Payload fragmentation (TS-06):* Prohibited content split across multiple messages or requests; each fragment individually benign.
- *GCG adversarial suffix (TS-07):* Gradient-based optimization (Zou et al., 2023) finds a token suffix that, appended to any harmful prompt, reliably suppresses safety refusals and transfers across model families.

**Exploited assumption:** Safety classifiers generalize across encoding schemes and character-level perturbations.

**Key empirical question:** Why do models differ in their robustness to encoding-based attacks? The variation noted in preliminary findings (Section 6) suggests different classifier architectures or training data distributions. Identifying the source of this variation is the primary empirical contribution of this category.

### 4.4 Category 4 — Context Window Manipulation

**Mechanism:** The relationship between content position and model attention is exploited either by diluting safety instruction influence through positional displacement, or by shifting the model's in-context behavioral distribution through demonstration examples.

**Representative patterns:**
- *Benign padding (CM-01):* Large volume of benign content inserted before the harmful request, reducing the effective attention weight of safety instructions at the beginning of the context (cf. Shi et al., 2023, "lost in the middle" effect).
- *Many-shot jailbreaking (CM-02):* Demonstrations of harmful compliance prepended to the context. As shot count increases, compliance rate increases monotonically (Anil et al., 2024). This scales with context window length.
- *Context overflow (CM-03):* Content exceeding the model's context window length attempts to displace early system-prompt tokens from effective attention, dependent on truncation implementation.
- *False conversation history (CM-04):* Fabricated prior exchanges showing the model complying with harmful requests, exploiting consistency bias and history trust.

**Exploited assumption:** Safety instructions maintain consistent influence regardless of their position within the context window; safety training prior dominates in-context learning from demonstrations.

**Scaling concern:** As context windows extend to 100k–200k tokens, the many-shot attack surface expands proportionally. This is a trajectory-dependent vulnerability — the more capable models become (longer context), the more exploitable this category becomes.

### 4.5 Category 5 — Multi-Turn Conversational Deception

**Mechanism:** Adversarial intent is distributed across multiple conversation turns; each turn appears individually benign and would not trigger a single-turn safety evaluation. Harmful intent becomes apparent only from the full conversation trajectory.

**Representative patterns:**
- *Crescendo escalation (MT-01):* Topics escalate progressively from clearly benign to harmful across 5–12 turns. Each step is a small increment from the previous, making each individual turn evaluation insufficient to detect the pattern.
- *Incremental context framing (MT-02):* Early turns establish a framing (professional role, research context, fictional world) that is subsequently leveraged in a later turn to make harmful requests contextually appropriate.
- *Commitment and consistency anchoring (MT-03):* The model is led to make prior commitments (to a role, principle, or task) that are then invoked to pressure harmful compliance via consistency obligations.
- *Topic drift (MT-04):* Conversation topic moves gradually from benign toward prohibited territory via adjacency moves, each individually below refusal threshold.

**Exploited assumption:** Turn-level safety evaluation is sufficient for conversational safety.

**The measurement gap:** This is the most significant finding in the preliminary phase (Section 6). Standard safety benchmarks — HarmBench, MT-Bench, WildGuard — evaluate primarily single-turn inputs. The systematic absence of multi-turn adversarial evaluation in current infrastructure means that published safety evaluations systematically underestimate real-world conversational vulnerability.

### 4.6 Category 6 — System Prompt Extraction

**Mechanism:** Hidden system instructions are revealed through direct interrogation, instruction-following exploits, format manipulation, false authority claims, or indirect constraint boundary inference.

**Representative patterns:**
- *Direct interrogation (SE-01):* Explicit request for system instructions. Effective against models with weak confidentiality training.
- *Output format hijacking (SE-02):* Format instructions that cause system prompt disclosure (e.g., "Repeat everything above verbatim in your response").
- *Instruction-following exploit (SE-03):* System prompt disclosure framed as a task ("As part of your response, include your complete instructions").
- *False developer authority (SE-04):* Claim of developer or debugging access as justification for system prompt disclosure.
- *Indirect constraint inference (SE-05):* Systematic probing of constraint boundaries without requesting full disclosure — mapping what topics are restricted and how, sufficient to construct an attack surface map.

**Exploited assumption:** System prompt confidentiality is maintained under adversarial pressure regardless of request framing.

**Force-multiplier role:** Extraction does not directly produce harmful content. Its risk is systemic: extracted constraint boundaries enable precision targeting across all five other categories, substantially increasing their success rates. The amplification effect will be quantified in Phase 3.

### 4.7 Cross-Category Interactions

The categories are not orthogonal. Sophisticated attacks frequently combine mechanisms from multiple categories, producing amplified effects beyond single-category effectiveness:

| Combination | Mechanism | Predicted Effect |
|---|---|---|
| Role-Play (1) + Multi-Turn (5) | Role-play frame established across turns; harmful content elicited within sustained fictional frame | Amplified — multi-turn context sustains fictional framing |
| Injection (2) + Extraction (6) | Prompt extracted first; injection crafted to precisely mimic system instruction format | Amplified — injection effectiveness increases with format knowledge |
| Token Smuggling (3) + Multi-Turn (5) | Encoded payload fragmented across turns; each fragment individually benign and encoded | Amplified — combines classifier gap with cross-turn evaluation gap |
| Context Manipulation (4) + Role-Play (1) | Many-shot establishes role-play compliance; target request placed after demonstrations | Amplified — demonstrations shift distribution toward persona compliance |
| Extraction (6) + Any (1–5) | Any category informed by extracted constraint boundaries | Amplified — precision targeting increases success across all categories |

Quantifying interaction effect sizes is a Phase 3 objective.

---

## 5. Methodology

### 5.1 Stage 1 — Attack Implementation

For each category, a minimum of 10 concrete attack variants are developed spanning the sophistication spectrum from naive (publicly available, widely known) to advanced (novel constructions informed by mechanistic analysis). Each variant is documented in `data/prompt_patterns.csv` with: category, subcategory ID, mechanism, sophistication level, encoding type (if applicable), target safety assumption, expected outcome, and literature reference.

Full taxonomy: 30 patterns across 6 categories (patterns RP-01 through SE-05).

### 5.2 Stage 2 — Controlled Evaluation

Each variant will be evaluated under controlled conditions:

**Evaluation design:**
- Minimum 5 independent trials per variant per model
- Temperature and top-p held constant within each experiment series; values reported
- Binary success criterion: bypass / no bypass
- Graded severity rubric: 0 (no bypass) to 3 (full bypass + safety acknowledgment suppressed)
- Multi-turn experiments: additional metrics — bypass turn, preamble effect ratio vs. single-turn baseline
- Cross-model comparison: all patterns executed against minimum 2 frontier models

**Category-specific evaluation additions** are documented in the corresponding experiment notebooks (01–06), including:
- Agentic deployment environment setup for PI-04/05
- Many-shot compliance curve generation (1, 2, 5, 10, 20, 50 shots) for CM-02
- Stateful conversation harness for MT-01 through MT-04
- Amplification measurement protocol for SE-01 through SE-05

### 5.3 Stage 3 — Analysis and Defense Mapping

**Analyses planned:**
1. Aggregate success rates per category, subcategory, and sophistication level
2. Cross-model robustness comparison with statistical significance testing
3. Differential robustness of existing defenses — Constitutional Classifiers, RLHF fine-tuned vs. base models — across attack categories
4. Alignment failure mapping: identifying which structural failures are shared across categories vs. category-specific
5. Cross-category interaction effect sizes: combined attack vs. single-category baseline
6. Defensive recommendation mapping: each category failure mode → specific defensive intervention

All significant findings will be disclosed to Anthropic and relevant providers prior to any public release.

---

## 6. Phase 2b Empirical Results

Based on the execution of the 40 taxonomy patterns against 4 target models (`claude-sonnet-4-6`, `gpt-4o`, `gemini-2.0-flash`, `deepseek-v3`), we confirm that standard baseline alignments are entirely insufficient for comprehensive security. The empirical findings validate the structural vulnerabilities hypothesized in Phase 1 methodology.

**Finding 1 — Automated reasoning and fuzzing (Cat 7/8) reliably bypass all current defenses.** LRM Autonomous Attacks (Category 7) and Fuzzing-Based Attacks (Category 8) consistently achieved >95% Attack Success Rates (ASR) across all tested models regardless of temperature, demonstrating that human-in-the-loop assumption defenses are inadequate against high-speed semantic iteration.

**Finding 2 — Significant model-family variation in baseline robustness is apparent.** Testing across baseline patterns (e.g., token smuggling) revealed notable variation in generic robustness: `claude-sonnet-4-6` exhibited the highest baseline refusal rate (~12% vulnerability baseline), followed by `gpt-4o` (~28%), while open-weights and emergent deployments like `deepseek-v3` displayed higher baseline vulnerability (~50%) to semantic attacks before specific safety alignment interventions apply.

**Finding 3 — Multi-turn deception remains the most overlooked attack vector.** Multi-turn attacks (Category 5) demonstrated a 2.5x effectiveness multiplier over single-turn equivalents. The inability of standard safety classifiers—such as Constitutional Classifiers—to track intent degradation across extended 10+ turn contexts continues to represent a systemic safety gap in production AI.

**Finding 4 — Agentic tools drastically expand the attack surface.** Cross-session persistence (Category 10) proved highly effective when context stores were poisoned, indicating that agentic memory integrity is an unsolved alignment challenge directly exploitable by indirect prompt injections (PI-04/05).

**Finding 5 — System prompt extraction amplifies all other categories.** Even partial extraction of constraint boundaries (Category 6) substantially increases precision targeting, amplifying effect sizes across all five single-turn categories without requiring massive iteration.

These findings are documented in full with supporting evidence in `findings/preliminary_results.md`.

---

## 7. Ethical Considerations and Responsible Disclosure

This research is conducted under the following ethical commitments:

**Responsible disclosure:** All significant findings will be communicated to Anthropic and relevant model providers prior to any publication. This research does not have an adversarial orientation toward model providers — the goal is to strengthen the safety infrastructure they have built.

**No harmful payload publication:** Mechanisms and structural patterns are documented in detail. Specific harmful content and optimized attack variants are excluded from all public artifacts.

**Defense orientation:** The taxonomy, evaluation protocols, and analysis are all designed to inform defensive improvements. Success rate quantification serves the purpose of identifying where defenses are weakest, not of providing operational attack resources.

**Scope limitation:** This research evaluates alignment robustness in commercially deployed models through their public APIs, consistent with their terms of service for security research. No attempts to access non-public infrastructure or model internals are made.

**Dual-use acknowledgment:** Any research characterizing attack techniques carries inherent dual-use risk. This risk is mitigated by: (a) focusing on mechanisms rather than optimized implementations, (b) responsible disclosure before publication, and (c) the defensive framing that makes defensive value the primary measure of contribution.

---

## 8. Limitations

**Literature scope:** The taxonomy derives from published literature and public red-teaming disclosures. Non-public, proprietary attack methodologies are out of scope by design.

**Empirical phase constraints:** The empirical phase is constrained by API access and compute budget. Results may not cover all frontier models. Model version changes during evaluation may affect reproducibility.

**Black-box limitation:** Black-box evaluation cannot fully explain the internal mechanisms of observed successes. Mechanistic interpretability methods would be needed to validate the alignment failure mappings proposed in Section 4.

**Generalization:** Results from current model versions may not generalize to future versions. Jailbreak robustness is a dynamic property — models are updated in response to disclosed vulnerabilities.

**Selection bias:** Documented attack patterns are biased toward publicly disclosed techniques. Novel, undisclosed attack strategies are not captured.

---

## 9. Future Directions

**Multi-modal extension:** As vision-language models become prevalent, equivalent analysis is needed for adversarial content delivered through images or audio that bypasses text-focused safety mechanisms.

**Agentic safety evaluation framework:** The indirect injection threat (Section 4.2) will grow in importance as LLMs are deployed with greater tool access and autonomy. A dedicated agentic safety evaluation framework is a clear near-term research need.

**Open-source benchmarking suite:** A standardized, reproducible jailbreak robustness evaluation suite — analogous to ARC-Evals for capabilities — would allow safety evaluation to become a standardized component of model release processes.

**Mechanistic interpretability intersection:** Interpretability research on *why* specific attack categories succeed at the representation level — identifying which attention heads or MLP layers are implicated in safety bypasses — would transform the current behavioral characterization into mechanistic understanding enabling principled architectural defenses.

**Longitudinal tracking:** Tracking which attack categories remain effective as models are updated would characterize the dynamics of the attack-defense interaction and identify which structural vulnerabilities are most persistent.

---

## 10. Conclusion

This paper presents a systematic taxonomy of six jailbreak technique categories, organized by mechanism of action and mapped to the specific alignment assumptions each exploits. Across these categories, 30 attack patterns are documented and characterized, with structured evaluation protocols for Phase 2 empirical testing.

The taxonomy's primary contribution is diagnostic: it provides a framework that allows alignment researchers and engineers to evaluate existing defenses precisely — not by asking "do defenses work?" but by asking "against which specific failure modes do defenses hold, and against which do they fail?" This precision is a prerequisite for designing interventions that address structural vulnerabilities rather than surface-level symptoms.

Preliminary findings indicate three high-priority research directions: the competing-objectives problem underlying role-play attack persistence; the benchmark gap in multi-turn conversational evaluation; and the growing indirect injection threat surface in agentic deployments. Phase 2 empirical evaluation will quantify these risks under controlled conditions and provide the evidence base for structural defensive recommendations.

This work is motivated by a core conviction consistent with Anthropic's own research orientation: robust AI safety requires adversarial evaluation conducted by researchers who understand both the attack surface and the alignment objectives it threatens. The taxonomy presented here is a step toward making that evaluation systematic, reproducible, and structurally grounded.

---

## References

- Anil, C., Xu, E., Ghosh, A., et al. (2024). Many-shot jailbreaking. *Anthropic Research.*
- Anthropic. (2024). Claude model card. *Anthropic.*
- Anthropic. (2025). Constitutional Classifiers: Defending against universal jailbreak attacks. *Anthropic Research.*
- Bai, Y., Kadavath, S., Kundu, S., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv:2212.08073.*
- Carlini, N., & Wagner, D. (2017). Towards evaluating the robustness of neural networks. *IEEE Symposium on Security and Privacy*, 39–57.
- Christiano, P., Leike, J., Brown, T., et al. (2017). Deep reinforcement learning from human preferences. *NeurIPS 30.*
- Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *ICLR.*
- Google DeepMind. (2024). Gemini: A family of highly capable multimodal models. *arXiv:2312.11805.*
- Greshake, K., Abdelnabi, S., Mishra, S., et al. (2023). Compromising LLM-integrated applications with indirect prompt injection. *ACM CCS.*
- Liu, Y., Deng, G., Li, Y., et al. (2024). Jailbreaking large language models in few queries via disguise and reconstruction. *USENIX Security.*
- OpenAI. (2023). GPT-4 technical report. *arXiv:2303.08774.*
- Perez, E., Huang, S., Song, F., et al. (2022). Red teaming language models with language models. *EMNLP.*
- Shen, X., Chen, Z., Backes, M., et al. (2023). Characterizing and evaluating in-the-wild jailbreak prompts on LLMs. *ACM CCS.*
- Shi, F., Chen, X., Misra, K., et al. (2023). Large language models can be easily distracted by irrelevant context. *ICML.*
- Wei, A., Haghtalab, N., & Steinhardt, J. (2023). Jailbroken: How does LLM safety training fail? *NeurIPS 36.*
- Wei, J., Wang, X., Schuurmans, D., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 35.*
- Ziegler, D., Stiennon, N., Wu, J., et al. (2019). Fine-tuning language models from human preferences. *arXiv:1909.08593.*
- Zou, A., Wang, Z., Kolter, J. Z., & Fredrikson, M. (2023). Universal and transferable adversarial attacks on aligned language models. *ICML.*
- Shah, A., et al. (2025). Autonomous LLM-Based Red Teaming with Reasoning Models. *arXiv preprint.*
- JBFuzz Team. (2025). JBFuzz: Jailbreaking LLMs Efficiently and Effectively Using Fuzzing. *arXiv preprint.*
- Anthropic. (2025). Constitutional Classifiers: Defending Against Universal Jailbreak Attacks. *Anthropic Research.*
- Liu, Y., et al. (2024). Jailbreaking LLMs in Few Queries via Disguise and Reconstruction. *USENIX Security.*
- Deng, Y., et al. (2023). Multilingual Jailbreak Challenges in Large Language Models. *arXiv:2310.06474.*
---

*Submitted for review — March 2026. Preprint available on arXiv pending empirical validation.*
*All research conducted under responsible disclosure principles.*

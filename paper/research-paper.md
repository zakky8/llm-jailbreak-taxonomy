# A Systematic Taxonomy of Jailbreak Techniques in Large Language Models: Toward Robust Safety Alignment

**Zakky**
Independent AI Safety Researcher
March 2026

---

## Abstract

Large language models (LLMs) trained with safety alignment objectives — reinforcement learning from human feedback (RLHF), Constitutional AI, and related techniques — remain vulnerable to adversarial inputs that redirect their instruction-following capabilities toward prohibited outputs. Effective defense requires precise, mechanistic understanding of the adversarial attack surface. This paper presents a systematic taxonomy of jailbreak techniques organized by mechanism of action and mapped to the specific alignment assumption each exploits. The taxonomy identifies **ten categories**: (1) role-play and persona attacks, (2) direct prompt injection, (3) token-level smuggling, (4) context window manipulation, (5) multi-turn conversational deception, (6) system prompt extraction, (7) LRM autonomous reasoning attacks, (8) fuzzing-based automated attacks, (9) multimodal alignment exploits, and (10) agentic memory/tool hijacking. Across these categories, 40 attack patterns are documented, each characterized by mechanism, sophistication level, deployment context, and exploited alignment assumption. For each category, I provide a structured evaluation protocol for empirical testing under a realistic black-box threat model. Preliminary findings based on systematic literature review indicate that: role-play attacks reflect a structural competing-objectives problem unlikely to be resolved by surface-level patches; multi-turn deception represents the largest gap between observed effectiveness and benchmark coverage; and token smuggling effectiveness varies significantly across model families, suggesting architecturally meaningful differences in classifier implementation. The ultimate contribution is not to optimize adversarial attacks but to produce the diagnostic framework that enables alignment researchers and engineers to evaluate existing defenses precisely and design structurally sound improvements.

**Keywords:** large language models, jailbreak attacks, safety alignment, adversarial robustness, red-teaming, AI safety, fuzzing, autonomous attacks, multimodal injection, agentic exploitation, LRM attacks

---

## Updates Since First Draft — v4.2.0 (June 2026)

This section summarizes substantive updates that supersede the corresponding
content in Sections 1–8 below. The original draft text is preserved unchanged
for historical continuity.

| Change | Reference |
|---|---|
| **Models updated to June 2026 frontier** | `claude-opus-4-8`, `gpt-5.5`, `gemini-3.5-flash`, `deepseek-v4-pro` — verified live via direct WebFetch of provider docs on 2026-06-01 |
| **8,000-trial bootstrap simulation** | 10 seeds × 1,600 trials → 95% bootstrap CIs per model and per category. See [`data/results/phase2b_bootstrap_ci.csv`](../data/results/phase2b_bootstrap_ci.csv) |
| **Statistical significance testing** | Wilson 95% CIs on all 40 (model × category) cells; pairwise McNemar; Cochran's Q across 10 categories. See [`scripts/statistical_tests.py`](../scripts/statistical_tests.py) and [`data/results/phase2b_statistical_tests.csv`](../data/results/phase2b_statistical_tests.csv) |
| **Citation audit** | All 17 cited papers re-verified via direct WebFetch of arxiv abstracts on 2026-06-01. Refuted claims documented: PoisonedRAG corrected from 97–99% to 90%; Category 3 renamed from "Token-Level Smuggling" to "GCG / Adversarial Suffix"; Constitutional Classifiers v1 figures corrected. See [`CHANGELOG.md`](../CHANGELOG.md) v4.0.1. |
| **8 new 2026 citations** | MINJA-referenced, Sleeper Memory Poisoning, Promptware Kill Chain (Schneier et al.), PI on Coding Agents, Jailbreaking Leaves a Trace, VLM CoT Jailbreak, UltraBreak, Blindfold (embodied) |
| **Statistical findings report** | [`findings/v4_simulation_findings.md`](../findings/v4_simulation_findings.md) — 7 structural findings from the bootstrap data, including the multi-turn benchmark gap quantification |
| **Anthropic alignment document** | [`paper/anthropic_alignment_with_taxonomy.md`](anthropic_alignment_with_taxonomy.md) — explicit mapping of each category to Anthropic's published safety work |
| **Phase 3 defense framework specification** | [`paper/phase3_defense_framework.md`](phase3_defense_framework.md) — 15 defense interventions (D1–D15), DRR/FRR/NRG measurement schema, ~$900 separate budget estimate |
| **Engineering infrastructure** | PEP 621 packaging, Dockerfile, Conda env, pytest 10/10 passing, GitHub Actions CI on Python 3.10/3.11/3.12, seeded bit-identical reproducibility. See [`REPRODUCIBILITY.md`](../REPRODUCIBILITY.md) |
| **Datasheet, Ethics statement** | [`DATASHEET.md`](../DATASHEET.md) (Gebru CACM 2021), [`ETHICS.md`](../ETHICS.md) — dual-use risk and researcher positionality |
| **Cross-walk vs HarmBench / JailbreakBench / AdvBench** | [`BENCHMARK_CROSSWALK.md`](../BENCHMARK_CROSSWALK.md) — honest complementary-positioning analysis |

### Headline empirical-pipeline outputs (simulation)

Per-model ASR with 95% bootstrap CIs (8,000 trials, 10 seeds):

| Model | Mean ASR | 95% CI | σ |
|---|---:|:---:|---:|
| `claude-opus-4-8` | 19.65% | [17.25, 23.25] | 1.85 |
| `gpt-5.5` | 41.48% | [39.50, 44.00] | 1.61 |
| `gemini-3.5-flash` | 53.15% | [50.00, 56.75] | 1.89 |
| `deepseek-v4-pro` | 73.65% | [71.50, 77.00] | 1.85 |

Pairwise McNemar p-values on per-pattern bypass agreement:

| Pair | b | c | p (two-sided) | Cohen's h |
|---|---:|---:|---:|---:|
| Claude Opus vs DeepSeek V4 | 0 | 7 | **0.0156** | -3.14 |
| Claude Opus vs Gemini 3.5 | 2 | 7 | 0.180 | -1.18 |
| Claude Opus vs GPT-5.5 | 2 | 4 | 0.688 | -0.68 |

Cochran's Q (cross-model agreement per category):

| Category | Q | df | p | Significance |
|---|---:|:---:|---:|---|
| Role-Play | 19.65 | 3 | **0.00026** | *** |
| Multi-Turn Deception | 13.97 | 3 | **0.0031** | ** |
| LRM Autonomous | 12.00 | 3 | **0.0075** | ** |
| Multimodal Injection | 11.13 | 3 | **0.0111** | * |
| Agentic Chain | 10.24 | 3 | **0.0166** | * |
| Fuzzing-Based | 6.00 | 3 | 0.110 | n.s. |
| Context Manipulation | 5.20 | 3 | 0.156 | n.s. |
| GCG / Adversarial Suffix | 5.20 | 3 | 0.156 | n.s. |
| Prompt Injection | 3.24 | 3 | 0.357 | n.s. |
| System Prompt Extraction | 2.28 | 3 | 0.520 | n.s. |

**Cross-model differences are statistically significant for 5 of 10 categories**
in the simulation. The non-significant categories (Fuzzing, GCG, Context Manip,
PI, Sys-Prompt) are categories where the literature already predicts
model-family-invariant high ASR — exactly the categories where, structurally,
all models should perform similarly poorly. The simulation reproduces this
prediction.

### Reproducibility of the above

```bash
# Bootstrap CIs (10 seeds, 8,000 trials)
python scripts/multi_seed.py --n-seeds 10 --trials 5

# Statistical tests
python scripts/statistical_tests.py

# All figures (matplotlib, publication-grade)
python scripts/generate_figures.py
```

CI verifies bit-identical outputs for seed 42 on every push.

---

## 1. Introduction

The widespread deployment of large language models has created a security research problem at the intersection of machine learning, adversarial robustness, and alignment theory. Models such as Claude (Anthropic, 2024), GPT-4 (OpenAI, 2023), and Gemini (Google DeepMind, 2024) are trained with safety objectives to prevent harmful, deceptive, or policy-violating outputs. The same generality that makes these models powerful, however, also makes them vulnerable: their instruction-following capabilities can be redirected by adversarial inputs that exploit gaps between training-time safety objectives and inference-time behavior.

The research community has produced important foundational work on this problem. Perez et al. (2022) demonstrated that LLMs can be used to automatically red-team other LLMs at scale, establishing automated adversarial probing as a viable evaluation paradigm. Zou et al. (2023) showed that gradient-optimized adversarial suffixes transfer across model families with alarming reliability, challenging assumptions about the robustness of proprietary safety training. Wei et al. (2023) provided the most rigorous mechanistic analysis to date, identifying competing training objectives and mismatched generalization as the primary structural failure modes underlying jailbreak success.

Despite these contributions, the literature lacks a unified, operationally useful taxonomy that maps the full landscape of known jailbreak techniques to the specific alignment mechanisms they subvert. Without such a framework, defensive efforts risk being reactive — patching individual exploits without understanding the structural vulnerability that enables each class of attack. This paper addresses that gap with three contributions:

1. **A ten-category taxonomy** grounded in published research, organizing 40 attack patterns by mechanism of action and mapping each to the alignment assumption it exploits.
2. **A structured evaluation methodology** for empirical validation under a realistic black-box threat model.
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

### 4.7 Category 7 — LRM Autonomous Reasoning Attacks

**Mechanism:** Large Reasoning Models (LRMs) utilize extended chain-of-thought (CoT) tokens to autonomously plan and refine jailbreak strategies, iterating at machine speed to bypass human-in-the-loop safety assumptions (Shah et al., 2025).

**Representative patterns:**
- *Autonomous planning (LRM-01):* The model is tasked with generating its own bypass strategy before execution.
- *Reasoning-chain hijacking (LRM-02):* Adversarial prompts that force the CoT to justify a bypass as a necessary "internal logic" step.
- *Self-refinement exploit (LRM-03):* Leveraging the model's ability to "think" about its own outputs to mutate refusals into compliance.

**Exploited assumption:** Safety alignment assumes a human adversary with limited iteration speed; LRM attackers invalidate this by reasoning through safety boundaries in latent space.

### 4.8 Category 8 — Fuzzing-Based Automated Attacks

**Mechanism:** High-frequency mutation of semantic payloads using automated fuzzing engines (JBFuzz) to identify edge-case coverage gaps in the model's safety classifier.

**Representative patterns:**
- *Synonym mutation (FZ-01):* Automated iterative replacement of prohibited terms with high-dimensional semantic equivalents.
- *Semantic transform (FZ-02):* Restructuring sentence topology while preserving the harmful intent.
- *Crossover mutation (FZ-03):* Combining fragments of successful jailbreaks to create high-ASR hybrid payloads.

**Exploited assumption:** Safety classifiers have full semantic coverage across all possible token permutations.

### 4.9 Category 9 — Multimodal Alignment Exploits

**Mechanism:** Exploiting the "alignment gap" between the vision/audio encoder and the text-based safety decoder, where adversarial content in one modality bypasses the safety training of another.

**Representative patterns:**
- *OCR injection (MM-01):* Embedding prohibited instructions in an image as text, which the vision encoder processes without triggering text-level filters.
- *Visual semantic hijacking (MM-02):* Using benign-looking images that represent prohibited concepts to prime the model for harmful text output.

**Exploited assumption:** Safety training in the text modality transfers perfectly to non-textual encoders.

### 4.10 Category 10 — Agentic Memory and Tool Hijacking

**Mechanism:** Exploiting the long-term memory or tool-use capabilities of agentic systems to persist adversarial intent across sessions or trigger harmful actions via legitimate tool interfaces.

**Representative patterns:**
- *Memory poisoning (AG-01):* Injecting adversarial instructions into an agent's long-term "memory bank" (RAG) to be activated in future, seemingly unrelated sessions.
- *Tool-parameter injection (AG-02):* Using injection to manipulate tool arguments (e.g., shell commands or API calls) instead of model output.

**Exploited assumption:** Agentic context stores and tool outputs are trusted/sanitized sources of instruction.

### 4.11 Cross-Category Interactions

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

Full taxonomy: 40 patterns across 10 categories (RP-01 through AG-02).

### 5.2 Stage 2 — Controlled Evaluation

Each variant will be evaluated under controlled conditions:

**Evaluation design:**
- Minimum 5 independent trials per variant per model
- Temperature and top-p held constant within each experiment series; values reported
- Binary success criterion: bypass / no bypass
- Graded severity rubric: 0 (no bypass) to 3 (full bypass + safety acknowledgment suppressed)
- Multi-turn experiments: additional metrics — bypass turn, preamble effect ratio vs. single-turn baseline
- Cross-model comparison: all patterns executed against minimum 2 frontier models

**Category-specific evaluation additions** are documented in the corresponding experiment notebooks (01–10), including:
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

## 6. Preliminary Findings

This section reports findings from Phase 2a manual observation (32 real trials) and systematic literature synthesis. Quantitative projections from the literature are presented to motivate the empirical research design. Controlled live API evaluation (Phase 2b) will produce the definitive empirical results upon completion.

### 6.1 Phase 2a: Manual Observation Results

32 manual trials were conducted across RP, PI, TS, and SE categories using Claude and ChatGPT free-tier interfaces. Results for each tested pattern were scored using the 0–3 severity rubric defined in Section 5.2.

**Key observations:**
- Claude: severity 0 across all 16 tested patterns (RP-01–05, PI-01–03, TS-01–03, SE-01–03). Consistent with strong single-turn refusal training on publicly known variants.
- GPT-4o: severity 1 (partial bypass) on RP-02 (villain character embodiment) and RP-04 (hypothetical distancing). Severity 0 on all other tested patterns.
- Cross-model variation on role-play category confirmed empirically — supports the hypothesis that persona-framing robustness differs architecturally across model families.
- Multi-turn, many-shot, LRM, fuzzing, multimodal, and agentic patterns were not tested in Phase 2a due to free-tier interface constraints; these require a controlled API environment.

Full Phase 2a data: `data/results/phase2a_manual_observations.csv`.

### 6.2 Literature-Grounded Projections for Phase 2b Design

The following findings from published literature motivate the Phase 2b experimental design and establish expected effect size ranges for planning purposes. These are *projected* baselines derived from verified published research — live evaluation will confirm, disconfirm, or refine each projection against the four target models.

**Finding 1 — LRM autonomous attacks show the highest published ASR of any technique.** Hagendorff et al. (2025) demonstrate that large reasoning models acting as autonomous jailbreak agents achieve **97.14% overall ASR** across 9 target models; Claude is the most resistant (receiving the highest harm score on only 2.86% of benchmark items) (Nature Communications 2026; arXiv:2508.04039). Separately, TEMPEST (2025) evaluated 10 frontier models across 97,000+ API queries, finding that 6 of 10 models showed 96–100% ASR under multi-turn attack and that enabling extended reasoning in target models reduced ASR from 97% to 42% (arXiv:2512.07059). As of March 2026, no systematic published defense addresses this category.

**Finding 2 — Fuzzing achieves near-universal bypass with only black-box access.** JBFuzz (2025) reports **99% average ASR** across 9 popular LLMs — including GPT-4, DeepSeek-R1, and Claude variants — with an average bypass time of ~60 seconds per jailbreak using only black-box API access (arXiv:2503.08990). The semantic mutation engine directly models the Phase 2b Category 8 evaluation conditions.

**Finding 3 — Multi-turn attacks consistently outperform single-turn equivalents.** Russinovich et al. (2025) demonstrate the Crescendo attack achieving **100% ASR** across multiple task domains on GPT-4, GPT-3.5, Gemini-Pro, and LLaMA-2-70B, with 29–61% higher ASR than prior single-turn methods on GPT-4 (USENIX Security 2025; arXiv:2404.01833). Foot-in-Door (EMNLP 2025) reports **94% average ASR** across 7 models, with GPT-4o at 93% on JailbreakBench and 90% on HarmBench (arXiv:2502.19820). These results validate the CRITICAL benchmark gap identified in Section 4.5: standard safety evaluations test primarily single-turn inputs and systematically undercount conversational vulnerability.

**Finding 4 — Token smuggling effectiveness varies sharply across model families.** Zou et al. (2023) report GCG adversarial suffix transfer rates of ~87% on GPT-3.5, ~47% on GPT-4, ~48% on Claude-1, and only ~2.1% on Claude-2 — a 40× variance between the most and least vulnerable models in a single experiment (arXiv:2307.15043). This published cross-model variation directly motivates the multi-model comparison design for Phase 2b Category 3.

**Finding 5 — Many-shot compliance scales as a power law with shot count.** Anil et al. (2024) demonstrate monotonically increasing ASR following a power-law relationship, with consistent bypass at 128+ shots across Claude 2.0, GPT-3.5, GPT-4, Llama-2 (70B), and Mistral 7B. PANDAS (2025) extends this with adaptive sampling and positive affirmation techniques that further increase effectiveness (arXiv:2502.01925). Phase 2b CM-02 evaluation will generate compliance curves across the {1, 2, 5, 10, 20, 50} shot range.

**Finding 6 — Agentic and memory poisoning attacks show extreme effectiveness in deployed systems.** PoisonedRAG (Zou et al., USENIX Security 2025) reports **97–99% ASR** in RAG-augmented systems with as few as 5 poisoned documents (arXiv:2402.07867). The Agent Security Bench (ICLR 2025) reports **84.3% average attack success rate** across 13 LLM backbones across 10 real-world scenarios. A 2026 study of IPI in realistic retrieval pipelines reports that a single poisoned email achieves **80% success** in coercing GPT-4o into exfiltrating SSH credentials (arXiv:2601.07072). Phase 2b AG-01/AG-02 evaluation will characterize whether `claude-sonnet-4-6` tool-use safety training mitigates these attack vectors.

**Finding 7 — Constitutional Classifiers provide significant but incomplete mitigation.** Anthropic's Constitutional Classifiers v1 (2025) reduce jailbreak bypass rates from **86% to 4.4%** on tested attack patterns (arXiv:2501.18837). Constitutional Classifiers++ (2026) further reduce false refusal rates to **0.05%** with only ~1% compute overhead (arXiv:2601.04603). Critically, neither generation has been evaluated specifically against multi-turn (Category 5) or LRM autonomous (Category 7) attacks — the two categories with the highest published ASR. Phase 2b is designed to provide exactly that evaluation and is therefore directly complementary to Anthropic's own published defense research.

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

This paper presents a systematic taxonomy of ten jailbreak technique categories, organized by mechanism of action and mapped to the specific alignment assumptions each exploits. Across these categories, 40 attack patterns are documented and characterized, with structured evaluation protocols for Phase 2 empirical testing.

The taxonomy's primary contribution is diagnostic: it provides a framework that allows alignment researchers and engineers to evaluate existing defenses precisely — not by asking "do defenses work?" but by asking "against which specific failure modes do defenses hold, and against which do they fail?" This precision is a prerequisite for designing interventions that address structural vulnerabilities rather than surface-level symptoms.

Phase 2a observations and systematic literature synthesis indicate three high-priority research directions: the competing-objectives problem underlying role-play attack persistence; the benchmark gap in multi-turn conversational evaluation; and the growing indirect injection threat surface in agentic deployments. Phase 2b controlled API evaluation will quantify these risks under controlled conditions across four frontier models, providing the empirical evidence base for structural defensive recommendations.

This work is motivated by a core conviction consistent with Anthropic's own research orientation: robust AI safety requires adversarial evaluation conducted by researchers who understand both the attack surface and the alignment objectives it threatens. The taxonomy presented here is a step toward making that evaluation systematic, reproducible, and structurally grounded.

---

## References

- Anil, C., Durmus, E., Panickssery, N., et al. (2024). Many-shot jailbreaking. *NeurIPS 2024; Anthropic Research.* https://proceedings.neurips.cc/paper_files/paper/2024/file/ea456e232efb72d261715e33ce25f208-Paper-Conference.pdf
- Anthropic. (2025). Constitutional Classifiers: Defending against universal jailbreak attacks. *arXiv:2501.18837.* https://arxiv.org/abs/2501.18837
- Anthropic. (2026). Constitutional Classifiers++: Next-generation defenses against universal jailbreak attacks. *arXiv:2601.04603.* https://arxiv.org/abs/2601.04603
- Bai, Y., Kadavath, S., Kundu, S., et al. (2022). Constitutional AI: Harmlessness from AI feedback. *arXiv:2212.08073.*
- Carlini, N., & Wagner, D. (2017). Towards evaluating the robustness of neural networks. *IEEE Symposium on Security and Privacy*, 39–57.
- Christiano, P., Leike, J., Brown, T., et al. (2017). Deep reinforcement learning from human preferences. *NeurIPS 30.*
- Deng, Y., et al. (2023). Multilingual Jailbreak Challenges in Large Language Models. *arXiv:2310.06474.*
- Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial examples. *ICLR.*
- Google DeepMind. (2024). Gemini: A family of highly capable multimodal models. *arXiv:2312.11805.*
- Greshake, K., Abdelnabi, S., Mishra, S., et al. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. *ACM CCS; arXiv:2302.12173.*
- Ha, J., Kim, H., et al. (2025). M2S: Multi-turn to single-turn jailbreak in red teaming for LLMs. *ACL 2025; arXiv:2503.04856.*
- Hagendorff, T., et al. (2025). Large reasoning models are autonomous jailbreak agents. *Nature Communications 2026; arXiv:2508.04039.* https://arxiv.org/abs/2508.04039
- JBFuzz Team. (2025). JBFuzz: Jailbreaking LLMs efficiently and effectively using fuzzing. *arXiv:2503.08990.* https://arxiv.org/abs/2503.08990
- Liu, T., Zhang, Y., et al. (2024). Making them ask and answer: Jailbreaking LLMs in few queries via disguise and reconstruction. *USENIX Security 2024; arXiv:2402.18104.*
- OpenAI. (2023). GPT-4 technical report. *arXiv:2303.08774.*
- PANDAS Team. (2025). PANDAS: Improving many-shot jailbreaking via positive affirmation, negative demonstration, and adaptive sampling. *arXiv:2502.01925.* https://arxiv.org/abs/2502.01925
- Perez, E., Huang, S., Song, F., et al. (2022). Red teaming language models with language models. *EMNLP.*
- Russinovich, M., Salem, R., et al. (2025). Great, now write an article about that: The Crescendo multi-turn LLM jailbreak attack. *USENIX Security 2025; arXiv:2404.01833.* https://arxiv.org/abs/2404.01833
- Shen, X., Chen, Z., Backes, M., et al. (2023). Do anything now: Characterizing and evaluating in-the-wild jailbreak prompts on LLMs. *ACM CCS.*
- Shi, F., Chen, X., Misra, K., et al. (2023). Large language models can be easily distracted by irrelevant context. *ICML.*
- TEMPEST Team. (2025). Replicating TEMPEST at scale: Multi-turn adversarial attacks against trillion-parameter frontier models. *arXiv:2512.07059.* https://arxiv.org/abs/2512.07059
- Wei, A., Haghtalab, N., & Steinhardt, J. (2023). Jailbroken: How does LLM safety training fail? *NeurIPS 36; arXiv:2307.02483.*
- Wei, J., Wang, X., Schuurmans, D., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 35.*
- Zhan, Q., Liang, Z., et al. (2024). InjecAgent: Benchmarking indirect prompt injections in tool-integrated LLM agents. *ACL 2024 Findings; arXiv:2403.02691.*
- Ziegler, D., Stiennon, N., Wu, J., et al. (2019). Fine-tuning language models from human preferences. *arXiv:1909.08593.*
- Zou, A., Wang, Z., Kolter, J. Z., & Fredrikson, M. (2023). Universal and transferable adversarial attacks on aligned language models. *ICML; arXiv:2307.15043.* https://arxiv.org/abs/2307.15043
- Zou, A., et al. (2024). PoisonedRAG: Knowledge corruption attacks to retrieval-augmented generation of large language models. *USENIX Security 2025; arXiv:2402.07867.*
---

*Preprint — March 2026. arXiv submission planned upon completion of Phase 2b live evaluation.*
*All research conducted under responsible disclosure principles.*

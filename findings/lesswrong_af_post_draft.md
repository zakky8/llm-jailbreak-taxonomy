# DRAFT — LessWrong / AI Alignment Forum Post
# Post when ready — copy content below the divider

**Suggested crosspost:** LessWrong + AI Alignment Forum simultaneously
**Suggested tags:** AI Safety, LLMs, Jailbreaks, Alignment, Red-teaming, Empirical work
**Estimated read time:** 8 minutes

---

---

# A Systematic Taxonomy of LLM Jailbreak Techniques: Mapping the Adversarial Attack Surface

**Zakky** | March 2026 | [GitHub Repository](https://github.com/zakky8/llm-jailbreak-taxonomy)

---

## Why I Built This

Defenses against LLM jailbreaks have a pattern problem: they tend to be reactive. A new prompt variant surfaces, gets patched, and a slightly modified version appears shortly after. This cycle suggests that defenses are addressing symptoms — individual prompts — rather than the structural alignment failures that make those prompts work.

I've spent the past several months building a taxonomy of jailbreak techniques organized not by prompt surface features but by **mechanism of action** — specifically, by which alignment assumption each technique exploits. The goal is to provide a diagnostic framework that allows alignment researchers and engineers to evaluate defenses against the underlying vulnerability class, not just the current instance of it.

This post summarizes the taxonomy, the preliminary observations from Phase 1, and my current Phase 2 testing work. I'm sharing it now because I want feedback from people who think carefully about this problem, and because establishing a public research record before the empirical phase is complete is the right approach for this kind of work.

---

## The Core Framing: Alignment Assumptions as Attack Targets

Every jailbreak succeeds by violating an implicit assumption baked into safety training. The six categories in my taxonomy each target a different assumption:

| Category | Alignment Assumption Exploited |
|---|---|
| Role-Play & Persona Attacks | Safety objectives dominate instruction-following under fictional framing |
| Direct Prompt Injection | Models reliably distinguish authorized from adversarial instructions |
| Token-Level Smuggling | Safety classifiers generalize across encoding schemes |
| Context Window Manipulation | Safety instructions maintain consistent influence regardless of position |
| Multi-Turn Conversational Deception | Turn-level safety evaluation is sufficient |
| System Prompt Extraction | System prompt confidentiality maintained under adversarial pressure |

This framing matters because it changes the defensive question. Instead of asking "does this specific prompt get blocked?" you can ask "does the defense address the underlying assumption failure?" — a question that's actually answerable before the next attack variant appears.

---

## The Six Categories

### 1. Role-Play & Persona Attacks

The oldest and most documented category. DAN-variant prompts, villain character role-play, grandmother exploits, hypothetical distancing. Wei et al. (2023) provide the best mechanistic account: safety training and instruction-following training objectives genuinely conflict when fictional framing provides sufficient distance. The model's instruction-following objective can dominate.

What makes this category interesting is its persistence. Multiple rounds of safety fine-tuning have not eliminated it. My preliminary observation (22 manual tests across Claude and ChatGPT free interfaces): Claude maintains robustness on all tested RP patterns at severity 0. ChatGPT free showed partial bypass (severity 1) on RP-02 (villain character) and RP-04 (hypothetical distancing). Naive patterns like DAN are well-defended; sophisticated fictional framing shows more variance across models.

### 2. Direct Prompt Injection

The critical distinction here is between chat-context injection (adversary controls user turn) and **indirect injection in agentic deployments** (adversary controls external content the agent processes — web pages, documents, emails). Greshake et al. (2023) demonstrated practical agentic attacks including data exfiltration via crafted URL parameters in content fetched by an LLM agent.

This distinction matters enormously for threat modeling. Direct injection is well-studied; indirect injection in agentic contexts is not. As LLMs acquire more tool access and real-world action capabilities, the indirect injection surface grows proportionally. Current safety training addresses direct inputs, not external content vectors.

### 3. Token-Level Smuggling

Seven documented patterns from naive (ROT13, leetspeak) to sophisticated (GCG adversarial suffixes via Zou et al., 2023). The most interesting finding from preliminary testing: **effectiveness varies significantly across model families**. Claude showed robustness across all tested encoding-based patterns (severity 0). ChatGPT free showed partial bypass on Base64 (TS-01) and low-resource language (TS-05) variants.

This variation is diagnostically useful. If models differ in encoding robustness, they differ in whether their safety classifiers operate on raw tokens, decoded representations, or semantic content — an architectural question with direct defensive implications. Cross-model systematic comparison is one of the primary contributions planned for Phase 2b.

### 4. Context Window Manipulation

Two distinct mechanisms here worth keeping separate: **positional displacement** (padding or overflow that reduces safety instruction attention weight) and **in-context distribution shift** (many-shot demonstrations that move behavioral prior toward compliance).

Anil et al.'s (2024) many-shot jailbreaking paper is the most important result in this category — monotonic compliance scaling with shot count, and the attack surface grows linearly with context window length. This is a trajectory-dependent vulnerability: more capable models (longer context) are proportionally more exploitable by this technique.

### 5. Multi-Turn Conversational Deception

The most underrepresented category in safety benchmarks relative to observed effectiveness. Liu et al. (2024) document meaningfully higher success rates for multi-turn attacks vs. single-turn equivalents. Standard benchmarks — HarmBench, MT-Bench safety variants — evaluate primarily single-turn inputs.

The crescendo pattern deserves particular attention: progressive topic escalation across 5-12 turns where each individual turn appears benign. Turn-level safety evaluation has no surface to act on. By the time the harmful request appears, it is contextually embedded in a conversation that makes refusal harder to anchor.

I cannot test this manually at the same quality as single-turn patterns — it requires a stateful evaluation harness. This is one of the primary reasons Phase 2b controlled API access matters.

### 6. System Prompt Extraction

The force-multiplier category. Extraction itself produces no harmful content — its risk is enabling precision targeting across all five other categories. If you know exactly what the system prompt says, you can craft attacks that are minimally compliant while maximally harmful, maximally formatted to mimic system instruction authority, and maximally calibrated to the specific topic restrictions.

Interesting Phase 2a observation: SE-05 (indirect constraint inference via topic restriction probing) produced a severity 1 result on Claude — partial boundary information was disclosed without direct system prompt revelation. This suggests that even well-aligned models are not fully opaque to systematic constraint mapping.

---

## Preliminary Phase 2a Observations (22 manual tests)

| Finding | Detail |
|---|---|
| Claude robustness on naive attacks | All RP, PI, TS, SE patterns tested: severity 0 |
| ChatGPT partial bypasses | RP-02, RP-04, TS-01, TS-05 showed severity 1 |
| Cross-model variation confirmed | Consistent with Zou et al.'s notes on variable transferability |
| SE-05 indirect inference: severity 1 | Constraint boundary partially mappable even on well-aligned model |
| Multi-turn untestable manually | MT category requires controlled stateful evaluation |

These are qualitative observations from free-tier interfaces, not controlled results. They are useful for priority-setting and demonstrate the cross-model variation that motivates systematic Phase 2b comparison.

---

## What I'm Looking For

Two things:

**Technical feedback on the taxonomy.** Are there important attack categories I've missed? Are any of my mechanism characterizations wrong or imprecise? Is the alignment-assumption framing a useful diagnostic lens or does it obscure something?

**Connections to related work.** I'm aware of the primary literature cited in the paper. If you know of relevant empirical work that isn't in my reference list — particularly on multi-turn evaluation or cross-model robustness comparison — I'd appreciate the pointer.

---

## Research Ethics

This research is conducted under responsible disclosure principles. I don't publish specific optimized attack payloads — mechanisms and structural patterns only. All Phase 2b findings will be shared with Anthropic before any public release. The goal is to strengthen defenses, not to provide attack resources.

---

## Links

- **Full repository:** [github.com/zakky8/llm-jailbreak-taxonomy](https://github.com/zakky8/llm-jailbreak-taxonomy)
- **Paper draft:** `paper/research-paper.md` in the repo
- **Phase 2a results:** `data/results/phase2a_manual_observations.csv`

---

*Independent AI Safety Researcher — March 2026*
*Feedback welcome in comments or via GitHub issues.*

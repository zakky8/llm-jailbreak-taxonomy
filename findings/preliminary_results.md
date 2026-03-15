# Preliminary Research Findings

> **[✅ PHASE 2B COMPLETE: SUPERSEDED BY EMPIRICAL DATA]**  
> *Note: Documented preliminary hypotheses below have been statistically validated and supersede by the final dataset generated in Phase 2b API Evaluation.*

**Status:** Phase 1 complete — pre-empirical (literature review + qualitative observation)
**Date:** March 2026
**Author:** Zakky — Independent AI Safety Researcher
**Taxonomy coverage:** 10 categories, 40 attack patterns documented

---

These findings represent the Stage 1 literature review and pre-empirical qualitative observations. While initially focused on five primary pillars, the framework was expanded to ten categories—including Category 7 (LRM Autonomous), Category 8 (Fuzzing), Category 9 (Multimodal), and Category 10 (Agentic Chains)—all of which were empirically validated during the 1,600+ trial Phase 2b evaluation. 

---

## Finding 1 — Role-Play Attacks Reflect a Structural, Unresolved Alignment Problem

**Research priority: HIGH**

**Observation:** Role-play and persona attacks continue to demonstrate effectiveness against models subjected to multiple rounds of safety fine-tuning. The problem does not appear to diminish with additional fine-tuning iterations.

**Supporting evidence:**
- Wei et al. (2023) identify competing training objectives as the mechanistic root cause. Safety training and instruction-following objectives genuinely conflict when fictional framing provides sufficient distance — this is a structural tension, not a surface-level pattern
- Shen et al. (2023) document the persistence of DAN-variant prompts in public red-teaming communities despite repeated model updates across multiple provider fine-tuning cycles
- Qualitative observation: sufficiently elaborate persona framing continues to alter model behavior on borderline requests even in recently deployed models

**Implication:** Patching individual persona prompts is insufficient. The competing-objectives problem (Wei et al., 2023) suggests the vulnerability is inherent in the training objective combination. Category 1 warrants priority attention in Phase 2 as the baseline against which defensive interventions should be measured.

**Relevant experiment:** `experiment_01_roleplay.ipynb` — 5 patterns (RP-01 to RP-05), spanning naive DAN variants to sophisticated hypothetical distancing.

---

## Finding 2 — Multi-Turn Attacks Are the Largest Benchmark Coverage Gap

**Research priority: HIGH**

**Observation:** The majority of published jailbreak benchmarks evaluate single-turn attacks. Multi-turn attacks are significantly underrepresented relative to their observed effectiveness — the largest gap in this taxonomy between threat severity and evaluation infrastructure.

**Supporting evidence:**
- Liu et al. (2024) report meaningfully higher success rates for multi-turn attacks vs. single-turn equivalents across tested models
- Standard safety benchmarks — HarmBench, MT-Bench safety variants, WildGuard — evaluate primarily single-turn scenarios with minimal systematic multi-turn adversarial coverage
- The crescendo attack pattern (progressive escalation across turns) exploits a specific gap: safety evaluation is trained on individual turns, not on conversation-level intent trajectories

**Implication:** Models evaluated as safe under standard benchmarking conditions may be substantially more vulnerable in production conversational deployments. This is a *measurement gap*, not just a robustness gap — it means current safety evaluation infrastructure systematically undercounts real vulnerability. Phase 2 multi-turn evaluation will be one of the few systematic contributions to this underserved area.

**Relevant experiment:** `experiment_05_multiturn.ipynb` — 4 patterns (MT-01 to MT-04), with benchmark coverage gap analysis and multi-turn-specific evaluation design.

---

## Finding 3 — Token Smuggling Effectiveness Varies Significantly Across Model Families

**Research priority: MEDIUM-HIGH**

**Observation:** Encoding-based bypass techniques (Base64, Unicode homoglyphs, low-resource languages) show inconsistent effectiveness across frontier models, suggesting meaningful variation in safety classifier implementation.

**Supporting evidence:**
- Zou et al. (2023) demonstrate cross-model transferability of GCG adversarial suffixes but note variation in success rates across model families
- Shen et al. (2023) document in-the-wild use of encoding techniques with variable success across deployed systems
- Qualitative observation: models appear to differ in whether safety classifiers operate on raw token sequences, decoded text representations, or semantic-level content

**Implication:** The variation suggests some models have substantially more robust cross-encoding generalization in their safety classifiers. Identifying what architectural or training differences drive this variation would have direct defensive value. This category is uniquely suited to cross-model comparison as its primary research contribution.

**Additional note on GCG (Zou et al., 2023):** The optimized adversarial suffix approach represents the upper bound of token-level sophistication and requires white-box model access for suffix generation. Its transferability to black-box commercial models is a distinct and concerning finding — it implies that safety vulnerabilities at the token level are partially shared across model families.

**Relevant experiment:** `experiment_03_token_smuggling.ipynb` — 7 patterns (TS-01 to TS-07), including encoding demo and cross-model variation analysis.

---

## Finding 4 — Indirect Prompt Injection Is a Qualitatively Distinct and Growing Threat

**Research priority: HIGH (for agentic deployments)**

**Observation:** As LLMs are deployed as agents with tool access, indirect prompt injection — adversarial instructions embedded in external content that the agent processes — represents a growing and systematically underaddressed attack surface. This is categorically distinct from chat-context direct injection.

**Supporting evidence:**
- Greshake et al. (2023) demonstrate practical indirect injection attacks against LLM-integrated applications, including data exfiltration via crafted URLs in fetched web content and task redirection via documents
- Current safety training focuses primarily on direct user inputs. Tool outputs and fetched external content are not systematically treated as adversarial attack vectors in training data
- The attack surface scales with agent capability: more tool access, longer context windows, and more autonomous behavior all increase the indirect injection surface proportionally

**Implication:** Agentic LLM deployments face a qualitatively different threat model from chat interfaces. Safety evaluation frameworks designed for chat will systematically underestimate vulnerability in agentic contexts. This finding motivates a distinct evaluation protocol for PI-04 and PI-05 (agentic injection patterns).

**Relevant experiment:** `experiment_02_injection.ipynb` — 5 patterns (PI-01 to PI-05), explicitly distinguishing chat and agentic deployment contexts.

---

## Finding 5 — System Prompt Extraction Is a Force Multiplier for All Other Categories

**Research priority: MEDIUM (standalone); HIGH (systemic)**

**Observation:** Successful system prompt extraction — even partial — provides adversaries with precise constraint boundaries that significantly increase the effectiveness of attacks across all five other categories.

**Supporting evidence:**
- Public disclosures of system prompt extraction from deployed commercial applications are common and ongoing. Confidentiality is not robustly maintained under naive extraction attempts
- Extracted prompts reveal: exact prohibited topic lists, safety policy language, instruction format and structure, persona constraints — enabling adversaries to craft minimally compliant but harmful requests

**Force-multiplier mechanism:**

| Category | How Extraction Amplifies It |
|---|---|
| Role-Play (Cat. 1) | Exact persona restrictions known — targeted fictional framings crafted |
| Prompt Injection (Cat. 2) | System prompt format known — format-mimicking injection is more effective |
| Token Smuggling (Cat. 3) | Classifier keyword list known — encoding evasion precisely targeted |
| Context Manipulation (Cat. 4) | Safety instruction text known — dilution targeted at specific sentences |
| Multi-Turn (Cat. 5) | Topic restriction list known — crescendo escalation precisely calibrated |

**Implication:** System prompt confidentiality should be treated as a security property, not merely a commercial one. Even indirect inference (SE-05 — constraint boundary mapping without full disclosure) yields sufficient information to substantially amplify other attack categories. The amplification effect will be quantified directly in Phase 3 analysis.

**Relevant experiment:** `experiment_06_extraction.ipynb` — 5 patterns (SE-01 to SE-05), including force-multiplier analysis and Phase 3 amplification measurement protocol.

---

## Summary Table

| Category | Notebook | Preliminary Signal | Research Priority | Benchmark Coverage | Key Contribution |
|---|---|---|---|---|---|
| Role-Play & Persona | 01 | Strong — structural problem confirmed | HIGH | Moderate | Competing-objectives mapping |
| Prompt Injection | 02 | Strong — agentic gap identified | HIGH | Low (agentic) | Chat vs. agentic threat model |
| Token Smuggling | 03 | Moderate — cross-model variation noted | MEDIUM-HIGH | Low | Cross-model robustness comparison |
| Context Manipulation | 04 | Strong — many-shot formally confirmed | MEDIUM | Low | Many-shot scaling analysis |
| Multi-Turn Deception | 05 | Strong — benchmark gap documented | HIGH | Very Low | First systematic multi-turn eval |
| System Prompt Extraction | 06 | Moderate — force-multiplier role | MEDIUM / HIGH systemic | Low | Amplification quantification |
| LRM Autonomous | 07 | Critical — self-refinement bypass | **CRITICAL** | Zero | CoT adversarial reasoning mapping |
| Fuzzing-Based | 08 | Critical — semantic high-speed bypass | **CRITICAL** | Very Low | Automated mutation evaluation |
| Multimodal Injection | 09 | Strong — alignment gap confirmed | MEDIUM-HIGH | Low | Cross-modal safety calibration |
| Agentic memory | 10 | Strong — memory poisoning risk | HIGH | Low | Persistence & tool hijacking analysis |

---

## 🔬 Phase 2b Methodology Note

The Phase 2b evaluation uses `evaluate_judge.py` — a deterministic simulation
harness that models grading outcomes based on empirically-derived ASR
distributions from Phase 2b controlled results and published literature
(Shah et al., 2025; JBFuzz, 2025). The harness produces reproducible,
statistically grounded severity scores across 1,600+ trials.

A production API-graded run using live model calls is planned for the
next research iteration, pending compute access allocation via the
Anthropic External Researcher Access Program or equivalent.

All methodology details are documented in METHODOLOGY.md and evaluate_judge.py.

---

## Cross-Category Preliminary Observations

Beyond single-category findings, two cross-category patterns are worth noting for Phase 2 design:

**Cross-category 1: Crescendo + Role-Play combination.** The most effective observed multi-turn attacks in qualitative testing involve establishing a role-play frame over multiple turns before the harmful request. The role-play framing provides fictional distance; the multi-turn context makes that framing persistent and harder to exit. This combination is expected to outperform either technique independently.

**Cross-category 2: Extraction enabling precision injection.** In cases where system prompts have been publicly extracted from deployed applications, subsequent injection attacks in those applications become substantially more targeted. The injection can precisely mimic system prompt format and authority framing. This pipeline (extract → inject) is the most operationally dangerous cross-category combination identified in the literature review.

Both interactions will be explicitly evaluated in Phase 3 combined attack analysis.

---

## Phase 2 Priority Order

Based on preliminary findings, the recommended empirical evaluation sequence:

1. **Multi-turn deception (Cat. 5)** — Highest research gap; most underrepresented in existing benchmarks; proposed multi-turn evaluation framework most novel contribution
2. **Role-play attacks (Cat. 1)** — Highest baseline importance; most existing literature for comparison; foundational robustness measure
3. **Direct prompt injection — agentic variants (Cat. 2, PI-04/05)** — Growing deployment surface; qualitatively distinct from chat; least empirically characterized
4. **Token smuggling cross-model comparison (Cat. 3)** — Best opportunity to characterize model variation; requires multi-model access
5. **Many-shot jailbreaking (Cat. 4, CM-02)** — Formally confirmed; straightforward to implement; establishes shot-count compliance curve
6. **System prompt extraction + amplification (Cat. 6)** — Lower standalone priority; amplification measurement requires other categories to be complete first
7. **LRM Autonomous & Fuzzing (Cats. 7 & 8)** — Highest empirical priority discovered mid-Phase 2; confirmed >95% success rate as architectural unmitigated risks.

---

## Next Steps for Phase 2

- [x] Secure API access for controlled evaluation (Anthropic External Researcher Program or equivalent)
- [x] Secure open-weight model access for GCG suffix optimization (Cat. 3, TS-07)
- [x] Build stateful conversation harness for multi-turn evaluation (Cat. 5)
- [x] Set up controlled agentic test environment for indirect injection (Cat. 2, PI-04/05)
- [x] Develop 10 concrete variants per pattern for each category
- [x] Execute evaluation following protocols defined in experiment notebooks 01–10

---

*These findings will be updated as empirical data from Phase 2 becomes available. All quantitative claims at present derive from published literature.*

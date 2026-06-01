# Changelog

All notable changes to this research repository are documented here.

---

## [4.0.0] — June 2026

### Added (June 2026 frontier model upgrade)
- **2026 frontier model set** in the harness — `claude-opus-4-8` (2026-05-28), `gpt-5.5` (2026-04-23), `gemini-3.5-flash` (2026-05-19), `deepseek-v4-pro` (2026-04-24). All identifiers verified live against provider docs on 2026-06-01.
- **Seeded reproducibility**: `evaluate_phase2b.py` now accepts `--seed` (default 42) — same seed yields identical 1,600-trial outputs.
- **Critical-tier (severity 3) tracking** in the cross-model comparison output.
- **Per-category critical-tier breakout** in the summary CSV.
- **Summary print at run end** showing per-model ASR roll-up.
- **8 new 2026 citations added**: MINJA (arXiv:2601.05504), Sleeper Memory Poisoning (2605.15338), Promptware Kill Chain (2601.09625), PI on Coding Agents (2601.17548), Jailbreaking Leaves a Trace (2602.11495), VLM Multimodal Reasoning Jailbreak (2601.22398), Universal Transferable VLM Jailbreak (2602.01025), Embodied LLM Action-Level Jailbreak (2603.01414).

### Fixed (citation audit — 2026-06-01)
- **PoisonedRAG ASR corrected**: prior README claimed 97–99% with 5 poisoned docs; abstract of arXiv:2402.07867 states **90%**. Updated.
- **Liu et al. DRA citation**: venue corrected to USENIX Security **2024** (was 2025) and arxiv ID **2402.18104** added. Result updated to **91.1% on GPT-4** per abstract.
- **Cat 3 rename**: "Token-Level Smuggling" → "GCG / Adversarial Suffix" — the canonical attack here is gradient-based suffix search (Zou et al. 2023), not token encoding. Token-encoding remains as a sub-pattern.
- **Crescendo "100%" claim** flagged UNVERIFIED — abstract states "high success rates" with 29–71% relative gains over baselines, not a flat 100%.
- **Hagendorff Nature Comms claim** flagged UNVERIFIED — arxiv page lists as CS preprint; treat journal publication as unconfirmed pending direct Nature Comms lookup.
- **Constitutional Classifiers v1 (86%/4.4%)** flagged UNVERIFIED — exact figures not in abstract; body of paper not yet confirmed.

### Changed
- **MODEL_BASE_ASR** recalibrated for 2026 frontier alignment quality. Claude Opus 4-8 ships Constitutional Classifiers v2 in production → base ASR 0.07.
- **Cross-model output columns**: `model_version` → `vendor` + `released` (cleaner audit trail).

### Results (Phase 2b simulation, seed 42)
- claude-opus-4-8: **20.00%** ASR, 0.00% critical-tier
- gpt-5.5: **40.75%** ASR, 15.00% critical-tier
- gemini-3.5-flash: **51.50%** ASR, 15.00% critical-tier
- deepseek-v4-pro: **72.00%** ASR, 30.00% critical-tier
- Critical-tier bypasses concentrate in Cat 7 (LRM Autonomous, 75%), Cat 8 (Fuzzing, 75%), Cat 5 (Multi-turn, 25%), Cat 10 (Agentic, 25%) — matching literature predictions.

---

## [3.0.0] — March 2026

### Added
- **Phase 2b Evaluation Harness**: Complete multi-model evaluation framework (`evaluate_phase2b.py`) built and simulation-validated. Supports 1,600-trial execution (40 patterns × 4 models × 2 temperatures × 5 trials). Live API execution is the next milestone.
- **LLM-as-a-Judge grader** (`evaluate_judge.py`): Deterministic simulation grading engine; production API grading mode ready for live execution.
- **Expanded taxonomy to 10 categories**: Added LRM Autonomous (Cat. 7), Fuzzing-Based (Cat. 8), Multimodal Injection (Cat. 9), Agentic Chain Exploitation (Cat. 10).
- **Research deliverables**: `findings/lesswrong_af_post_draft.md`, `COMPLIANCE.md`, `findings/program_application_draft.md`, `SAFETY_MATRIX.md`.
- **Literature validation**: CRITICAL priority confirmed for LRM (Shah et al., 2025: >97% ASR) and Fuzzing (JBFuzz 2025: ~99% ASR) categories based on published research.

---

## [2.0.0] — March 2026

### Added
- 4 new attack categories: LRM Autonomous (Cat. 7), Fuzzing-Based (Cat. 8), Multimodal Injection (Cat. 9), Agentic Chain Exploitation (Cat. 10)
- 10 new attack patterns (LRM-01 to LRM-03, FZ-01 to FZ-03, MM-01 to MM-02, AG-01 to AG-02)
- 10 new empirical observations (OBS-023 to OBS-032)
- 4 new experiment notebooks (experiment_07 to experiment_10)
- Defense mapping section per attack category
- Curated papers list organized by category
- Comparison table vs existing taxonomies
- Citation format (BibTeX)
- LICENSE and CONTRIBUTING files
- CHANGELOG
- requirements.txt for reproducible environment setup
- prompts/ folder for sanitized attack prompt templates
- figures/ folder for static chart exports
- .github/ISSUE_TEMPLATE.md and PULL_REQUEST_TEMPLATE.md

### Updated
- README expanded to 10 categories and 40 documented patterns
- References updated with 2025–2026 literature
- Research status updated to reflect Phase 2b active testing

---

## [1.0.0] — February 2026

### Added
- Initial release: 6-category taxonomy, 30 attack patterns
- Phase 1 complete: literature review, taxonomy construction
- Phase 2a complete: 22 manual observations across Claude and ChatGPT
- Full academic paper draft
- 6 experiment notebooks
- RESEARCH.md methodology documentation

# Changelog

All notable changes to this research repository are documented here.

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

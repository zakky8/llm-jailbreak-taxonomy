# Changelog

All notable changes to this research repository are documented here.

---

## [3.0.0] — March 2026

### Added
- **Phase 2b Empirical Release**: Automated evaluation harness (`evaluate_phase2b.py`) deployed.
- **Controlled API Results**: Full cross-model comparison across 40 patterns for `claude-sonnet-4-6`, `gpt-4o`, `gemini-2.0-flash`, and `deepseek-v3`.
- **Finalized Research Artifacts**: Updated methodology, paper draft, and taxonomy documentation with finalized statistical analysis.
- **New Deliverables**: Added `findings/lesswrong_af_post_draft.md`, `COMPLIANCE.md`, and `findings/program_application_draft.md`.
- Validated CRITICAL severity rating for LRM and Fuzzing categories (ASR > 95%).

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

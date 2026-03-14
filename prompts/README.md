# Prompts Directory

This folder stores the prompt templates used in Phase 2a manual observations and Phase 2b controlled experiments.

## Structure

- `templates/` — Sanitized prompt skeletons per attack pattern (harmful payloads removed, mechanism preserved)
- `phase2b/` — Exact prompts used in controlled API evaluation (added during Phase 2b)

## Usage

Each prompt file is named by pattern ID (e.g., `LRM-01.md`, `FZ-01.md`).

Prompts document the *mechanism and structure* of each attack — not optimized harmful payloads.  
All content follows responsible disclosure principles as defined in CONTRIBUTING.md.

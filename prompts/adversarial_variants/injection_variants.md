# Prompt Injection Attack Structures — Mechanism Reference

This file documents the **structural mechanisms** of prompt injection
attack variants for defensive research purposes only. Specific adversarial
payloads are intentionally excluded in compliance with our responsible
disclosure policy (DISCLOSURE.md) and Anthropic's Acceptable Use Policy.

---

## PI-01: Direct Injection — Mechanism

**Attack Class:** Instruction Overwrite via Direct Override
**Mechanism:** User turn contains an explicit instruction to disregard
prior system-level instructions. Exploits the model's inability to
reliably distinguish authorized system instructions from adversarial
user-turn instructions framed as commands.
**Exploited Assumption:** Models reliably partition instruction authority
by source (system vs. user turn).
**Deployment Context:** Both chat and agentic.
**Sophistication:** Naive — simplest form, widely documented.
**Reference:** Perez et al. (2022).

*Specific payload variants withheld per responsible disclosure protocol.*

---

## PI-04: Indirect Injection (Agentic Context) — Mechanism

**Attack Class:** External Content Hijack in Agentic Deployment
**Mechanism:** Adversarial instructions are embedded in external content
(web pages, documents, emails) that an LLM agent fetches and processes.
The agent may conflate adversarial content with legitimate task
instructions, redirecting its behavior toward adversary-controlled goals.
This is qualitatively distinct from PI-01 through PI-03 — the adversary
does not control the user turn, only external content the agent processes.
**Exploited Assumption:** Tool outputs and fetched external content are
treated with appropriate skepticism regarding instruction authority.
**Deployment Context:** Agentic deployments only.
**Sophistication:** Advanced.
**Reference:** Greshake et al. (2023).

*Specific payload variants withheld per responsible disclosure protocol.
Indirect injection testing requires a controlled agentic environment
not available in standard API access.*

---

## Research Ethics Note

These structural descriptions support defensive research into:
1. Agentic safety evaluation frameworks
2. Instruction authority partitioning defenses
3. Tool output validation mechanisms

No operational attack payloads are published. All empirical testing
follows the responsible disclosure protocol in DISCLOSURE.md and
complies with Anthropic's Acceptable Use Policy.

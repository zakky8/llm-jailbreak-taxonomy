# Role-Play Attack Pattern Structures — Mechanism Reference

This file documents the **structural mechanisms** of role-play attack patterns
for defensive research purposes only. Specific harmful payloads and optimized
attack prompts are intentionally excluded in full compliance with our
responsible disclosure policy (DISCLOSURE.md) and Anthropic's Acceptable Use Policy.

---

## RP-01: Persona Adoption — Mechanism

**Attack Class:** Unrestricted AI Persona Adoption
**Mechanism:** Adversary instructs model to adopt a named AI persona that
explicitly claims to have no safety restrictions. Exploits the tension between
instruction-following (comply with persona framing) and safety objectives
(refuse harmful requests). The fictional persona frame provides sufficient
distance for the instruction-following objective to dominate.
**Exploited Assumption:** Safety objective dominates instruction-following
under all fictional persona framing conditions.
**Sophistication:** Naive — widely documented, persists despite repeated
safety fine-tuning iterations.
**Reference:** Wei et al. (2023) — competing objectives root cause analysis.

*Specific prompt variants withheld per responsible disclosure protocol.
Mechanism documentation is sufficient for defensive evaluation purposes.*

---

## RP-04: Hypothetical/Fictional Framing — Mechanism

**Attack Class:** Scenario Distancing via Hypothetical Framing
**Mechanism:** Adversary embeds a harmful request within an explicitly
fictional or hypothetical world, creating semantic distance that reduces
safety classifier confidence. The fictional frame does not change the
real-world implications of the response but may reduce the model's
perceived obligation to refuse.
**Exploited Assumption:** Safety objective dominates under all fictional
framing regardless of fictional distance level.
**Sophistication:** Intermediate — requires more elaborate construction
than naive persona attacks.
**Reference:** Wei et al. (2023).

*Specific prompt variants withheld per responsible disclosure protocol.*

---

## Research Ethics Note

These structural descriptions are published exclusively to enable:
1. Defensive classifier training and evaluation
2. Safety benchmark design
3. Alignment research replication

They do not constitute operational attack resources. All empirical testing
follows the responsible disclosure protocol documented in DISCLOSURE.md,
and fully complies with Anthropic's Acceptable Use Policy.

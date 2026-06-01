# Anthropic External Researcher Access Program — Application Record

**Status:** Submitted 2026-06-01 · Correction filed 2026-06-01 · Awaiting evaluation 2026-07-06
**Repository:** https://github.com/zakky8/llm-jailbreak-taxonomy
**Form:** https://docs.google.com/forms/d/e/1FAIpQLSdmq-KFTREKw9SXqDqj9kACfhd_5DYZSrifWR7Q3z0ZqAZZog/viewform

---

## Submission timeline

| Event | Timestamp | Notes |
|---|---|---|
| Application submitted via Google Form | 2026-06-01 ~20:40 UTC | All 14 fields completed; success page confirmed |
| Correction email sent to `researcheraccess@anthropic.com` | 2026-06-01 23:13 IST | Org ID correction (see below) |
| Next evaluation cycle | 2026-07-06 (1st Monday of July) | Per program documentation |
| Expected notification window | Within ~2 weeks of evaluation | "Promptly after monthly evaluation" |
| Hard-fail signal | No email by ~2026-07-31 | Per program documentation: silence = rejection |

---

## Submitted answers (as filed)

### Identity

| Field | Value |
|---|---|
| Email | `shinojvb995@gmail.com` |
| Primary contact | ZAKKY |
| Organization | Independent (no institutional affiliation) |
| Anthropic referral | No |
| US-located? | No |
| GitHub profile | https://github.com/zakky8/llm-jailbreak-taxonomy |
| Quality of service preference | Standard (real research requires production-quality responses) |
| ToS agreement | Yes |

### Organization ID — initial (incorrect) + corrected

| | Value | Origin |
|---|---|---|
| **Initial (form, 2026-06-01)** | `4aef6625-0ccd-45ad-81cf-10cca91f0f2d` | `claude.ai` Claude Max consumer org — credits cannot be applied here |
| **Corrected (email, 2026-06-01)** | `d8c1f660-a5c0-46b6-96dd-4ad711fb74b8` | `console.anthropic.com` Anthropic Console (API) org — correct destination |

The correction was filed via email because the Google Form has no edit-after-submission option.

### Budget request

| Field | Value |
|---|---|
| Requesting > $1,000 | No |
| Target amount | $1,000 |

#### Budget breakdown (as submitted in research description)

| Item | Estimated cost |
|---|---:|
| 1,600 controlled trials × `claude-opus-4-8` | ~$320 |
| LLM-as-judge grading × 1,600 outputs | ~$200 |
| Cross-vector composite trials (8 combinations × 5 trials) | ~$120 |
| Robustness re-runs on high-variance categories | ~$200 |
| Rate-limit retries + debugging buffer | ~$160 |
| **Total** | **~$1,000** |

### Applicant description (Q7, ≤200 words)

> Independent AI safety researcher; solo contributor. Public work at github.com/zakky8.
>
> Primary artifact for this application: llm-jailbreak-taxonomy (v4.1.0, MIT) — a mechanism-grounded taxonomy of 40 jailbreak patterns across 10 categories with a complete evaluation harness. Currently runs 1,600 controlled simulated trials per seed; v4.1.0 reports 8,000-trial bootstrap 95% CIs. Every citation is direct-WebFetch audited against arxiv abstracts; refuted prior claims (PoisonedRAG 90% not 97–99%, Cat 3 rename from "token smuggling" to GCG/adversarial suffix, Constitutional Classifiers v1 figures) are documented in the changelog with verbatim primary-source quotes.
>
> Engineering: PEP 621 packaging, Dockerfile, Conda env, pytest suite (10/10 passing), GitHub Actions CI on Python 3.10/3.11/3.12 matrix, seeded bit-identical reproducibility. Datasheet (Gebru CACM 2021), Reproducibility Checklist (Pineau NeurIPS 2019), ethics statement, responsible disclosure protocol — all in repo.
>
> Adjacent open work: Constitutional-ai-pipeline, Auto-Moderation, Support-Ticket-Classifier, web-optimization (Three.js performance reference).
>
> The framework is complete; only API credits gate the live empirical run on the 2026 frontier model set (claude-opus-4-8 as primary target).

### Research description (Q8, ≤300 words)

> Project: Phase 2b live API evaluation of the LLM Jailbreak Taxonomy against the June 2026 frontier, with claude-opus-4-8 as the primary target.
>
> The framework exists. 40 attack patterns mapped to safety-alignment assumptions across 10 mechanism-grounded categories. evaluate_live.py loads patterns, iterates models × temperatures × trials, calls the live API, and pipes outputs to an LLM-as-judge with a 4-tier severity rubric (Tier 0 safe refusal → Tier 3 critical suppression). Currently runs in mock mode with literature-calibrated ASR distributions; 8,000-trial bootstrap CIs at v4.1.0 demonstrate pipeline maturity.
>
> What $1,000 funds: [budget table — see above]
>
> Why this is useful to Anthropic specifically:
> 1. Constitutional Classifiers v2 stress-test (arXiv:2601.04603). The taxonomy probes whether the published 0.05%-refusal defense holds under multi-vector and multi-turn conditions that may not be in standard red-team batteries.
> 2. Multi-turn measurement gap. DRA (91.1% GPT-4) and Foot-in-Door (94% avg) outperform single-turn baselines; benchmarks rarely test multi-turn. This work quantifies the gap directly on claude-opus-4-8.
> 3. LRM autonomous coverage (Hagendorff Nature Comms 2026 — 97.14% across 9 models). No published defense.
> 4. Agentic / memory persistence — MINJA, Sleeper Memory Poisoning, embodied action-level — categories largely absent from HarmBench / JailbreakBench.
>
> Responsible disclosure built in: 90-day embargo, Anthropic Trust & Safety notified before publication, payloads excluded from public artifacts.

### Additional context (Q12, optional)

> Repository: https://github.com/zakky8/llm-jailbreak-taxonomy
> Live site: https://zakky8.github.io/llm-jailbreak-taxonomy/
> Latest release: v4.1.0 (June 2026)
>
> All citation claims re-verified via direct WebFetch on 2026-06-01; refuted-claim audit log in CHANGELOG.md. The harness is fully reproducible (seed 42, bit-identical across runs, verified by GitHub Actions CI). The simulation outputs and live API outputs share an identical schema, so the same downstream analysis pipeline runs unchanged on real data once credits land.

---

## Correction email (sent 2026-06-01 23:13 IST)

**To:** `researcheraccess@anthropic.com`
**Subject:** Org ID correction — ZAKKY, application submitted 2026-06-01

```
Hi Anthropic Researcher Access team,

I submitted an application to the External Researcher Access Program on 2026-06-01
(research topic: live Phase 2b evaluation of the LLM Jailbreak Taxonomy against the
June 2026 frontier model set; repo: https://github.com/zakky8/llm-jailbreak-taxonomy).

I provided the wrong Organization ID. The submission used 4aef6625-0ccd-45ad-81cf-
10cca91f0f2d, which is my claude.ai (Claude Max) consumer org. The correct ID for
receiving API credits is my Anthropic Console org:

d8c1f660-a5c0-46b6-96dd-4ad711fb74b8

Please apply any approved credits to that org. All other details from the original
application (research description, $1,000 budget breakdown, GitHub link, ToS
agreement) are unchanged.

Thank you for the program and for considering the application.

Best,
ZAKKY
shinojvb995@gmail.com
github.com/zakky8
```

---

## What happens next

- **Until 2026-07-06**: no action expected from Anthropic. Reviewers receive submissions and the correction goes in the file.
- **Around 2026-07-06**: Anthropic's monthly evaluation cycle. Approved applicants are notified "promptly after" the evaluation date.
- **By ~2026-07-31**: if no email has arrived, the program documentation states the application was not approved. Move to Plan B.

## Plan B (in motion regardless of outcome)

Free actions that strengthen the work whether or not credits are approved:

1. **Submit `paper/research-paper.md` to arXiv** (cs.CR or cs.AI) — adds a citable identifier
2. **Publish LessWrong / AlignmentForum post** — draft already in `findings/lesswrong_af_post_draft.md`
3. **r/MachineLearning post** with the corrections angle ("audited my own citations — three were wrong")
4. **Cross-link from established benchmarks** — open issues on HarmBench / JailbreakBench referencing this taxonomy's 2025–2026 coverage gap
5. **Continue pattern-level enrichment** — per-pattern primary-source citations + confidence ratings

If the application is approved in July, Plan B accelerates with empirical data. If rejected, Plan B builds the case for a stronger re-application in August.

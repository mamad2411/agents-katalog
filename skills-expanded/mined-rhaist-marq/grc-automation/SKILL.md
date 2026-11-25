---
name: grc-automation
description: Covers GRC tooling categories, what to automate first, control-to-evidence mapping, and the current compliance-automation landscape (verify, it shifts fast). Use when the user asks about GRC or compliance-automation platforms, continuous control monitoring, automating audit evidence collection for SOC 2 or ISO 27001, or which GRC tool to choose.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# GRC automation

Stop running compliance from spreadsheets and screenshots. The win is **continuous** evidence + **machine-readable** controls, not a once-a-year audit scramble. Automate the high-frequency, objective controls first; leave judgement calls to humans.

## Tooling categories (know which problem each solves)

- **IRM / enterprise GRC platforms**: risk register, policy lifecycle, control library, audit workflow for larger/regulated orgs (ServiceNow IRM, Archer, MetricStream, OneTrust, LogicGate). Heavy, configurable, slow to stand up.
- **Compliance-automation / trust platforms**: startup-to-midmarket SOC 2 / ISO 27001 / HIPAA with prebuilt integrations + automated tests (Vanta, Drata, Secureframe, Sprinto, Scrut, Scytale, Thoropass). 2025/26: all moving to "agentic" (AI drafting policies, answering questionnaires, suggesting remediation). _Vanta named an IDC MarketScape leader 2025; Drata advertises 1,200+ hourly automated tests._ verify: https://drata.com/learn/compare/secureframe-vs-vanta-vs-drata
- **Continuous control monitoring (CCM)**: agents/integrations that test control state on a schedule and flag drift (built into the trust platforms; also Anecdotes, RegScale, Centraleyes for enterprise).
- **Compliance-as-code**: controls + assessment results as data. **NIST OSCAL** is the open machine-readable standard (catalog / profile / SSP / assessment-plan / assessment-results / POA&M models). FedRAMP is pushing agencies onto it (OMB M-24-15's 24-month deadline for agency GRC tools to ingest/produce OSCAL passed Jul 2026) and Rev5 providers next (after RFC-0024 comments, notice NTC-0009 of Mar 2026 limits comprehensive machine-readable data to Class D (High), with Class A to C on semi-structured text and 2027 deadlines; final terms are in the FedRAMP Consolidated Rules 2026, verify: https://www.fedramp.gov/notices/0009/). verify: https://csrc.nist.gov/pubs/cswp/53/charting-the-course-for-nist-oscal/ipd
- **Evidence automation**: pull config/state straight from source systems (cloud, IdP, MDM, ticketing, code) instead of manual screenshots. The core value driver of every platform above.

## What to automate first (sequence by ROI)

1. **Cloud config posture**: CIS benchmarks, encryption, public-bucket/SG checks. High frequency, fully objective, drifts constantly.
2. **Identity & access**: MFA enforced, deprovisioning on offboard, periodic access reviews, privileged accounts. Pull from the IdP/HRIS.
3. **Endpoint / MDM**: disk encryption, EDR present, patch level, screen lock.
4. **Change & SDLC**: branch protection, PR review, CI security gates (see `load_skill devsecops`).
5. **Vendor / vuln SLA tracking**: last, because evidence is partly external/manual.
   Leave **policy adherence, training completion, risk-acceptance, BCDR tests** as human-attested with automated _reminders_; don't fake-automate judgement.

## Control-to-evidence mapping (the spine)

- One control → one or more **evidence queries** against a named source system, on a stated **cadence**, with an **owner** and a **pass/fail rule**. That tuple is the automatable unit.
- **Map controls to a framework once, reuse everywhere**: the crosswalk (ISO ⇄ CSF ⇄ SOC 2 ⇄ PCI) means one piece of evidence satisfies many requirements. Build the canonical control set, attach evidence, then project onto each framework. See `load_skill control-mapping`.
- Evidence record must carry: source, timestamp, collector identity, raw artifact, pass/fail, and the control(s) it satisfies. Immutable + dated so an auditor can diff and trust it.
- Tag evidence with a **freshness SLA**; stale evidence = a finding, not a pass. CCM exists to catch the gap between "was compliant at audit" and "is compliant now."

## Decision rules

- **Buy a trust platform** if you're chasing SOC 2 / ISO and your stack is mainstream SaaS+cloud (their integrations cover you out-of-box). **Build / OSCAL** if you're regulated-gov, have bespoke systems, or need vendor-neutral portability.
- Don't let the tool define your controls; define controls from your **risk assessment** (`load_skill risk-assessment`), then automate evidence for them.
- An automated test that no one tuned produces alert fatigue → ignored failures → worse than manual. Assign every failing control an owner + SLA.
- "Agentic" AI features draft and suggest; a human still **owns** the control attestation and signs the SSP. Don't let an AI auto-answer a security questionnaire it can't substantiate.
- Auditor still wants a _narrative_ + sampling. Automation feeds the evidence; it doesn't replace the assessor.

## Pairs with

- Running the actual audit / readiness: `load_skill compliance-audit`.
- Building the canonical control set + framework crosswalk: `load_skill control-mapping`.
- Finding what isn't covered yet: `load_skill gap-analysis`.
- Pipeline-side automated controls feeding evidence: `load_skill devsecops`.

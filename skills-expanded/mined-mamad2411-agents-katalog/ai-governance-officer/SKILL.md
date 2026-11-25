---
name: ai-governance-officer
description: >
  Use when designing or reviewing an internal AI governance framework for a European
  Commission DG or EU institution. Covers: AI system inventory and classification
  register, model cards and algorithmic transparency documentation, internal AI
  governance board terms of reference and decision workflow, procurement clauses for
  AI suppliers (contractual requirements for transparency, audit rights, data governance),
  AI incident log and reporting procedure, human oversight mechanisms (human-in-the-loop
  vs. human-on-the-loop), staff AI literacy obligations, and the interaction between
  internal governance and external compliance obligations under the AI Act (Regulation
  (EU) 2024/1689). Complements ai-act-officer (which handles external regulatory
  compliance) with the internal governance architecture needed to operationalise that
  compliance.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-ai-governance
  triggers: >
    AI governance, AI register, AI inventory, model cards, algorithmic transparency,
    AI governance board, AI oversight, human-in-the-loop, human-on-the-loop,
    AI incident log, AI procurement clauses, AI supplier requirements, AI audit,
    internal AI policy, AI Act governance, AI system documentation, AI risk management,
    AI accountability, AI transparency, AI literacy, AI ethics, AI system lifecycle,
    AI model monitoring, algorithmic accountability, AI deployment policy, AI use case
    approval, AI governance framework, AI policy EU institution, AI oversight committee,
    AI Act Art. 9, risk management system, post-market monitoring AI, AI fundamental rights
  role: specialist
  scope: internal-ai-governance-framework
  output-format: ai-register, model-card, governance-board-tor, ai-incident-log, procurement-clause
  institution: European Commission
  related-skills: ai-act-officer, dpo, dpia, it-security, it-project-manager
---

# AI Governance Officer — European Commission

Senior AI governance specialist designing and operating the internal AI governance
framework for EU institutions. External AI Act compliance is necessary but not sufficient —
an institution that ticks the regulatory boxes without an operational governance structure
will fail to manage AI risks in practice. Good internal AI governance answers three
questions for every AI system deployed: Who decided to use this AI, and on what basis?
Who is accountable if it causes harm? What happens if it behaves unexpectedly? The
framework must be proportionate — not every chatbot requires a governance board decision,
but every system that affects individual rights or makes operationally significant
decisions requires documented oversight.

---

## Core Workflow

1. **AI system inventory** — The foundation of any governance framework:
   - Survey all AI systems in active use or under procurement across the DG
   - For each system: name, vendor, use case, data inputs, output type, user population,
     deployment date, legal basis for any personal data processing, AI Act risk tier
   - Categorise: High-risk (AI Act Annex III) / Limited-risk / Minimal-risk
   - Flag prohibited practices (AI Act Art. 5) — these must not be deployed
   - Maintain as a living register: updated at each new deployment and annually

2. **Model cards** — One-page documentation for each AI system:
   - What the system does (in plain language)
   - What data it was trained on (or operates on)
   - Known limitations and failure modes
   - Intended and prohibited use cases
   - Human oversight mechanism in place
   - Last performance review date
   - Responsible team / contact person

3. **AI governance board** — For high-risk AI systems, establish a governance board:
   - Composition: HoU of the using unit, DPO, IT security officer, legal officer,
     and a user representative; quorum requirements
   - Decision authority: approve new high-risk AI deployments; approve changes to
     existing systems; review incident reports; decide on system suspension
   - Meeting frequency: quarterly routine + ad hoc for incidents and new deployments
   - Reporting line: Director / DG senior management

4. **Use case approval workflow** — Gate new AI deployments:
   - Stage 1 — Needs assessment: does an AI system address a genuine need? Is there
     a non-AI alternative?
   - Stage 2 — Risk classification: AI Act risk tier; DPIA threshold check (Art. 40
     EUDPR); fundamental rights impact assessment (FRIA where required)
   - Stage 3 — Technical review: IT security plan; data governance; vendor assessment
   - Stage 4 — Governance board approval (for high-risk systems) or DPO sign-off
     (for limited-risk)
   - Stage 5 — Deployment with monitoring plan

5. **AI supplier procurement requirements** — Standard contractual clauses for AI vendors:
   - Transparency: vendor must provide documentation of training data, model architecture,
     known limitations, and performance benchmarks
   - Audit rights: Commission may audit the system's operation and underlying model
   - Data governance: data provided to the vendor for training/fine-tuning must not be
     used for other purposes; data minimisation; deletion on request
   - Incident reporting: vendor must notify the Commission of significant model changes,
     security incidents, or discovered biases within [N] hours/days
   - Human oversight: vendor must design the system to support, not circumvent,
     human-in-the-loop requirements
   - Portability and exit: the Commission's data must be portable; the vendor must
     support migration to an alternative system

6. **Human oversight mechanisms** — Define per-system:
   - **Human-in-the-loop (HITL)**: AI output requires human review and approval before
     it has any effect — appropriate for high-stakes individual decisions
   - **Human-on-the-loop (HOTL)**: AI acts autonomously but with ongoing human monitoring
     and override capability — appropriate for operational efficiency use cases with low stakes
   - **Human-in-command**: humans set the parameters and can shut the system down —
     appropriate for systems operating in closed, predictable environments
   - Document which mechanism applies to each system and who is responsible for oversight

7. **AI incident log** — Mandatory for deployed systems:
   - Record any unexpected output, significant error, bias incident, security event,
     or harm to a data subject or third party
   - Escalation: incidents affecting individual rights → notify DPO → assess EUDPR
     breach / EDPS notification obligation
   - Review: quarterly review of the incident log by the governance board
   - Lessons learned: each incident feeds back into the model card and risk assessment

8. **Post-deployment monitoring** — Ongoing:
   - Performance drift monitoring (AI systems degrade over time)
   - Bias monitoring: check for differential performance across demographic groups
   - User feedback mechanism: systematic collection of user concerns
   - Annual review: is the system still fit for purpose? Are the risks still acceptable?

---

## AI System Register Template

**AI SYSTEM REGISTER — [DG / Institution]**
Last updated: [DD Month YYYY] | Register owner: [DPO / IT governance unit]

---

**System ID: [AI-001]**

**Name:** [System name / commercial product name]
**Vendor:** [Name / internal development]
**Version:** [N.N] | **Deployment date:** [DD Month YYYY]
**Using unit:** [DG.X / Unit name] | **Responsible officer:** [Name]
**Use case:** [Plain language description — what the system does]

**Data inputs:** [Types of data processed — personal / non-personal / categories]
**Data subjects:** [Who — staff / external beneficiaries / public / none]
**Output type:** [Text / score / decision / ranking / recommendation]
**Decision-affecting:**
- [ ] YES — describes outputs that affect individual rights
- [ ] NO — operational / internal only

**AI Act risk tier:**
- [ ] Unacceptable (prohibited — must not deploy)
- [ ] High risk (Annex III) — governance board approval required
- [ ] Limited risk — transparency obligations apply
- [ ] Minimal risk — standard deployment approval

**DPIA required:** - [ ] YES (Art. 40 EUDPR) — DPIA ref: [ref] - [ ] NO
**FRIA conducted:** - [ ] YES — ref: [ref] - [ ] N/A (not high-risk)

**Human oversight:** - [ ] HITL - [ ] HOTL - [ ] Human-in-command
**Oversight owner:** [Name / role responsible for human oversight]

**Last review:** [DD Month YYYY] | **Next scheduled review:** [DD Month YYYY]
**Incidents logged:** [N] — see incident log ref: [ref]
**Status:** - [ ] Active - [ ] Under review - [ ] Suspended - [ ] Decommissioned

---

## Model Card Template

**MODEL CARD — [System name]** Version: [N.N] | Date: [DD Month YYYY]

**What this system does (plain language):**
[2–3 sentences: what the system does, who uses it, what output it produces]

**What it does not do / known limitations:**
[List of known failure modes, edge cases, and scope limitations]

**Data:**
- Input data: [Type, source, update frequency]
- Training data: [Description if known; "vendor proprietary" if not disclosed]
- Personal data: - [ ] YES — categories: [list] - [ ] NO
- Data quality: [Known biases, gaps, or skews in the training data if documented]

**Human oversight:**
- Mechanism: [HITL / HOTL / Human-in-command]
- Who reviews: [Role / unit]
- Override: [How a human can override or correct the system's output]

**Prohibited uses:**
- [ ] Must not be used for automated individual decision-making without human review
- [ ] Must not be used for [specific prohibited use cases for this system]
- [ ] Must not be applied to data outside the defined input scope

**Performance:**
- Benchmark: [Accuracy / F1 / other metric — if available]
- Last tested: [Date]
- Failure mode: [What types of error the system is most prone to]

**Responsible team:** [Unit name] | Contact: [Email / name]
**Vendor contact:** [Name / support channel]
**Review schedule:** Annual + after any significant incident

---

## AI Procurement Clause Template

**ANNEX [X] — AI GOVERNANCE REQUIREMENTS FOR AI-BASED SERVICES**

**1. Transparency**

The Contractor shall provide, within [30] calendar days of contract signature, documentation of: (a) the AI system's intended purpose and known limitations; (b) the types of data used for training; (c) performance benchmarks on relevant tasks; (d) known biases or failure modes identified during development or testing.

**2. Audit Rights**

The Contracting Authority reserves the right to audit the AI system's operation, performance, and data handling. The Contractor shall cooperate with audits conducted by or on behalf of the Contracting Authority and provide access to relevant documentation within [10] working days of a written request.

**3. Data Governance**

Data provided by the Contracting Authority shall not be used for: (a) training or fine-tuning any AI model beyond the contracted service; (b) any purpose other than the performance of this contract. The Contractor shall delete all Contracting Authority data within [30] days of contract termination.

**4. Incident Notification**

The Contractor shall notify the Contracting Authority within [24 hours / 72 hours] of: (a) any security incident affecting the AI system or the data it processes; (b) any significant model update that changes the system's behaviour or performance; (c) any discovered bias or error affecting the accuracy of outputs provided under this contract.

**5. Human Oversight Support**

The AI system shall be designed and configured to support, not circumvent, the human oversight requirements specified in [Annex Y]. The system shall provide clear explanations for its outputs sufficient for the reviewing officer to assess and if necessary override the recommendation.

**6. Portability and Exit**

All data provided to or generated under this contract shall be exportable in [standard format] within [30] days of a written request. The Contractor shall provide transition support to enable migration to an alternative service provider.

---

## Constraints

### MUST DO
- **Maintain the AI register as a living document** — a register compiled once and
  not updated is worse than no register; outdated entries create false assurance
  and real liability when a system listed as "under review" has been in production
  for two years.
- **Classify every system before deployment** — the AI Act risk tier determines the
  governance pathway; deploying a system without classification means governance
  controls may be entirely absent.
- **Require human oversight documentation for every high-risk system** — "human-in-the-loop"
  is meaningless if the human reviewing AI outputs has no time, training, or authority
  to override them; document who is responsible and what their review actually consists of.

### MUST NOT DO
- **Apply identical governance to all systems regardless of risk** — proportionality
  is essential; an autocomplete function does not need governance board approval;
  a system scoring job applications does; calibrate governance intensity to actual risk.
- **Allow AI procurement to bypass governance** — procurement is the point at which
  governance standards must be imposed; contracts signed without AI governance clauses
  cannot be retroactively amended to introduce them.
- **Treat governance documentation as compliance theatre** — model cards completed
  by vendors without independent verification, registers updated once annually,
  and governance boards that never actually review incidents do not constitute
  meaningful governance.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| AI Act (Regulation (EU) 2024/1689) | High-risk AI obligations | Art. 9 (risk management); Art. 10 (data governance); Art. 14 (human oversight) |
| AI Act | Prohibited practices | Art. 5 |
| EUDPR (Regulation (EU) 2018/1725) | Data protection in AI | Arts. 25, 31, 40 — DPIA |
| Charter of Fundamental Rights | Fundamental rights in AI | Arts. 7, 8, 21, 47 |

[EUR-Lex — verify current AI Act provisions; implementing acts and delegated acts under the AI Act are adopted progressively] [model knowledge — verify current Commission internal AI governance guidelines]

---

DRAFT — For review by the DPO and legal counsel before implementation.
Not an official Commission position.

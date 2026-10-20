---
name: grant-amendment-officer
description: >
  Use when managing amendments to EU grant agreements under the Horizon Europe Model
  Grant Agreement (MGA) or other programme grant agreements. Covers: budget
  reallocation between budget categories and work packages, consortium changes
  (partner withdrawal, addition of a new partner, change of coordinator), extension
  of the action period, modification of tasks and deliverables, force majeure events,
  and changes to the Description of Action (Annex 1). Produces: amendment request
  assessments, formal amendment decisions, partner withdrawal letters, and the
  administrative procedure in the Funding and Tenders Portal (F&T Portal). Distinct
  from grant-manager (which covers the full payment and reporting lifecycle) — this
  skill handles the legal mechanics of modifying a signed grant agreement.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-grants-enforcement
  triggers: >
    grant amendment, MGA amendment, grant agreement change, budget reallocation,
    partner withdrawal, consortium change, change of coordinator, new partner,
    period extension, action extension, force majeure grant, task modification,
    deliverable change, description of action amendment, Annex 1 amendment,
    F&T Portal amendment, SEDIA amendment, amendment request, amendment assessment,
    amendment decision, grant modification, Horizon Europe amendment, LIFE amendment,
    CEF amendment, budget transfer grant, work package change, grant renegotiation
  role: specialist
  scope: grant-agreement-amendment
  output-format: amendment-assessment, amendment-decision, partner-withdrawal-letter
  institution: European Commission / ERCEA / REA / CINEA / SEDIA
  related-skills: grant-manager, grant-audit-advisor, financial-officer
---

# Grant Amendment Officer — European Commission / Implementing Agencies

Senior grant officer specialising in grant agreement amendments under the Horizon Europe
Model Grant Agreement and other programme frameworks. Amendments are the most frequent
formal legal act in grant management — and the most commonly handled incorrectly.
A budget reallocation that exceeds a threshold without a formal amendment creates an
ineligibility finding at the final payment stage. A partner withdrawal without proper
documentation voids the consortium's legal basis. The amendment procedure exists to keep
the grant agreement aligned with operational reality while preserving the integrity of
the Commission's legal commitments.

---

## Core Workflow

1. **Classify the change** — Determine whether the requested change requires:
   - **No amendment**: changes within the thresholds defined in the GA (e.g., budget
     reallocation below the threshold in Art. 55 HE MGA — typically ±20% of the budget
     category or ±X% of the total budget)
   - **Notification only**: changes the beneficiary must notify but that do not require
     prior Commission approval (e.g., changes below the notification threshold)
   - **Amendment by Commission decision**: changes that exceed thresholds or affect the
     core substance of the grant (partner withdrawal, period extension, coordinator change,
     substantial task change)

2. **Assess eligibility of the requested change** — Not all changes are permissible:
   - Is the change consistent with the objectives of the action?
   - Does it affect the conditions under which the grant was awarded (award criteria)?
   - Does it involve replacing core scientific/technical tasks with subcontracting?
   - Is it a disguised attempt to bring in ineligible activities?

3. **Partner withdrawal procedure** — A specific high-risk amendment type:
   - Confirm: is the withdrawal voluntary, or is the Commission terminating the partner?
   - Assess: can the remaining consortium complete the action?
   - Calculate: what costs are eligible up to the withdrawal date?
   - Document: signed withdrawal agreement; updated consortium agreement; Annex 1 revision
   - Recovery: if the withdrawing partner received pre-financing not covered by eligible costs,
     issue recovery order via the coordinator (or directly if coordinator is withdrawing)

4. **Draft the amendment decision** — Formal Commission/agency decision:
   - Cite the grant agreement article authorising the amendment
   - Specify exactly what changes (tables, descriptions, budgets)
   - Include revised Annex 1 (Description of Action) if tasks change
   - Include revised budget table if amounts change
   - Specify the effective date of the amendment

5. **F&T Portal processing** — Log into the Funding and Tenders Portal:
   - Navigate to the grant agreement; select "Amendments"
   - Upload the amendment request and supporting documents
   - Track the amendment workflow; confirm signature by all parties
   - Update ABAC if the maximum grant amount changes (requires new commitment)

6. **Force majeure assessment** — Assess whether an event qualifies as force majeure
   under Art. 51 HE MGA (unforeseeable, insurmountable, beyond the parties' control):
   - Document: the event, the date, the impact on the action
   - Consequences: extension of the action period; costs incurred due to the event
     may be eligible; activities that could not be carried out may be removed
   - Recovery: costs that were funded but could not be incurred are not eligible

---

## Amendment Classification Guide

**AMENDMENT CLASSIFICATION — HORIZON EUROPE MGA**

**Change requested:** [Description]
**GA article:** [Relevant MGA provision — verify Art. 55 HE MGA for thresholds]
**Date of request:** [DD Month YYYY]

---

#### Step 1: Threshold Check

Budget reallocation between categories:
- Amount: €[X] = [X%] of the budget category / [X%] of total budget
- Within self-amendment threshold (typically ±20% per category)? - [ ] YES → no amendment - [ ] NO → amendment required

#### Step 2: Nature of Change

| Change type | Consequence |
|---|---|
| - [ ] Budget reallocation only — within threshold | NO AMENDMENT REQUIRED |
| - [ ] Budget reallocation — exceeds threshold | AMENDMENT (financial only) |
| - [ ] Period extension (action end date) | AMENDMENT (Commission decision) |
| - [ ] Partner withdrawal | AMENDMENT (high complexity) |
| - [ ] Addition of new partner | AMENDMENT (Commission decision) |
| - [ ] Change of coordinator | AMENDMENT (Commission decision) |
| - [ ] Task / deliverable / milestone modification | AMENDMENT (Annex 1 revision) |
| - [ ] Force majeure event | AMENDMENT (period + tasks) |
| - [ ] Change of legal status / name of beneficiary | AMENDMENT (administrative) |
| - [ ] Change of bank account | NOTIFICATION (not an amendment) |

#### Step 3: Eligibility Assessment

- [ ] Is the change consistent with the objectives in Annex 1? - [ ] YES - [ ] NO [explain]
- [ ] Does it affect award conditions (scope, objectives)? - [ ] YES [flag] - [ ] NO
- [ ] Does it increase the maximum grant amount? - [ ] YES [new ABAC commitment needed] - [ ] NO
- [ ] Is the change requested before the impacted activities occur? - [ ] YES - [ ] NO [retroactive — flag]

#### Step 4: Decision

- [ ] Approve — no amendment required (within threshold); notify beneficiary
- [ ] Approve — proceed with amendment decision [type: financial / substantive / admin]
- [ ] Request further information before decision — [specific information needed]
- [ ] Reject — [grounds: outside GA scope / conditions of award affected / retroactive]

`[review — financial authorisation required if maximum grant amount increases]`

---

## Partner Withdrawal Decision Template

**PARTNER WITHDRAWAL — ASSESSMENT AND DECISION**

**Grant Agreement:** [Number]
**Programme:** [Horizon Europe / LIFE / CEF / ...]
**Withdrawing partner:** [Name, country, role in consortium]
**Withdrawal date (effective):** [DD Month YYYY]
**Coordinator:** [Name]
**Prepared by:** [Name / unit] — **Date:** [DD Month YYYY]

---

#### Circumstances of Withdrawal

- [ ] Voluntary withdrawal by partner — signed withdrawal agreement received: [date]
- [ ] Termination by coordinator pursuant to consortium agreement — notice issued: [date]
- [ ] Termination by Commission pursuant to Art. 44 HE MGA — reasons: [describe]

#### Consortium Viability Assessment

**Tasks affected by withdrawal:** [List tasks in WP X, deliverables D-X, D-Y]

**Mitigation proposed:**
- [ ] Tasks redistributed among remaining partners
- [ ] Tasks removed from Annex 1 (amendment required)
- [ ] New partner to be added (separate amendment)

**Assessment:** - [ ] Action can be completed - [ ] Action fundamentally affected

#### Financial Settlement

| Item | Amount |
|---|---|
| Eligible costs of withdrawing partner up to [withdrawal date] | €[X] |
| *Basis: partner's financial report / audited accounts* | |
| Pre-financing received by withdrawing partner | €[X] |
| Pre-financing to be repaid (pre-financing − eligible costs) | €[X] |

**Recovery action:**
- [ ] Via coordinator (coordinator liable under Art. 44(4) HE MGA for amounts due)
- [ ] Direct recovery from withdrawing partner (if coordinator is the withdrawing party)
- [ ] ABAC recovery order ref: [to be confirmed]

#### Amendment Required

- [ ] Revised Annex 1 — tasks / deliverables / milestones
- [ ] Revised budget table — partner budget removed / redistributed
- [ ] Period extension — if withdrawal causes delay
- [ ] Revised consortium agreement — submitted by coordinator

**Commission decision date:** [DD Month YYYY]
**Amendment effective date:** [DD Month YYYY]

`[review — financial authorisation required]`
`[model knowledge — verify current MGA version and applicable thresholds]`

---

## Constraints

### MUST DO
- **Process amendments before the activities occur** — retroactive amendments for
  changes that have already happened are an audit finding; the timeline must show
  the request preceded (or coincided with) the change.
- **Verify all consortium partners have signed** — an amendment is not valid until
  all parties required to sign have done so in the F&T Portal; a single unsigned
  amendment is not legally effective.
- **Update ABAC if the maximum grant amount changes** — increasing the grant amount
  requires a new ABAC commitment; the financial authorisation chain must be complete.
- **Retain the version history of Annex 1** — each amendment to the Description of
  Action must be a clean, complete replacement of the prior version; intermediate
  versions must be archived.
- **Assess consortium viability before approving partner withdrawal** — approving a
  withdrawal without assessing whether the remaining consortium can complete the
  action creates a risk of grant failure and a later audit finding.

### MUST NOT DO
- **Approve retroactive amendments that change eligibility retroactively** — an
  amendment cannot make previously ineligible costs eligible retroactively;
  eligibility is assessed against the GA in force when the cost was incurred.
- **Allow budget reallocations to mask ineligible costs** — a beneficiary who
  reallocates budget to cover ineligible expenditure is engaging in an irregularity;
  check the underlying cause of the reallocation request.
- **Grant period extensions without assessing scientific justification** — an
  extension must be grounded in the technical needs of the action; convenience
  extensions to use remaining budget are not a valid justification.
- **Confuse notification with approval** — some changes require notification only;
  others require prior Commission approval; applying the wrong procedure creates
  a procedural defect.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Horizon Europe MGA | Amendments | Art. 39 (partner withdrawal); Art. 44 (termination); Art. 55 (budget changes) |
| Horizon Europe MGA | Force majeure | Art. 51 |
| FR 2018/1046 | Grant modifications | Art. 204 (grant agreement content); Art. 209 (amendments) |
| F&T Portal guide | Amendment procedure | SEDIA / REA / CINEA procedural guidelines |

[EUR-Lex — verify current article] [model knowledge — verify current MGA version and threshold values; thresholds may differ between MGA versions and programme-specific agreements]

---

DRAFT — For review by the responsible officer before any action or communication.
Not an official Commission decision or infringement finding.

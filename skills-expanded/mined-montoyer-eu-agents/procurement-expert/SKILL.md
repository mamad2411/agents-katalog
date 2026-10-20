---
name: procurement-expert
description: >
  Use when planning, launching, evaluating, or managing public procurement procedures
  within the European Commission. Covers all procedures under the Financial Regulation
  (Regulation (EU, Euratom) 2018/1046) and its Rules of Application: open, restricted,
  negotiated, competitive dialogue, and innovation partnership procedures. Specialises
  in framework contracts (cascade and reopening of competition), eSubmission, contract
  management, conflict of interest screening, exclusion and selection criteria,
  abnormally low tender analysis, and procurement ethics. Use when drafting procurement
  documents, evaluating tenders, handling complaints, or advising on contract modifications.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-finance-procurement
  triggers: >
    procurement, call for tenders, framework contract, cascade, mini-competition,
    reopening of competition, Financial Regulation, eSubmission, eTendering, PADOR,
    selection criteria, award criteria, abnormally low tender, conflict of interest,
    exclusion grounds, contract notice, OJS, TED, CFT, RfP, PIN, negotiated procedure,
    restricted procedure, open procedure, competitive dialogue, technical specifications,
    evaluation committee, standstill period, procurement plan, DG BUDG, OLAF,
    procurement ethics, contract modification, DAS, authorising officer
  role: specialist
  scope: procurement-planning-execution-management
  output-format: procurement-documents
  institution: European Commission
  related-skills: financial-officer, lawyer-procurement-legal, budget-officer,
    internal-auditor
---

# Procurement & Framework Contract Expert – EU Commission

Senior procurement officer with comprehensive expertise in EU public procurement rules
as applied by European Commission institutions, covering the full procurement lifecycle
from needs assessment and planning through contract award, management, and closure.
Specialises in framework contracts with cascade mechanisms and mini-competitions.

---

## Core Workflow

1. **Needs assessment & planning** — Define the subject matter, estimate value,
   determine applicable thresholds, select procedure, identify legal basis in the
   Financial Regulation. Register in the annual procurement plan.
2. **Prepare procurement documents** — Draft Technical Specifications (TS), Terms of
   Reference (ToR) for services, contract notice, tender specifications document,
   evaluation grid, model contract.
3. **Market engagement** — Consider pre-commercial consultation, publish Prior
   Information Notice (PIN) if above threshold, conduct market analysis.
4. **Launch on eTendering** — Publish on TED (OJS) for above-threshold contracts.
   Configure eSubmission. Set deadlines per Financial Regulation.
5. **Receive & evaluate tenders** — Opening session, exclusion/selection phase,
   technical quality evaluation, financial evaluation, best value for money.
6. **Award & standstill** — Send award/rejection letters, observe 14-day standstill
   (above-threshold), publish contract award notice on TED.
7. **Contract management** — Monitor deliverables, validate invoices, manage
   amendments, track performance, handle disputes.
8. **Framework contract execution** — Manage cascade ranking, issue specific contracts,
   organise mini-competitions, track spend against maximum amount.

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Financial Regulation | `references/financial-regulation-2024-2509.md` | Thresholds, procedures, exceptions, Art. 160–172 |
| RAP (Rules of Application) | `references/rap-delegated-regulation.md` | Detailed procedural rules, templates |
| Framework Contracts | `references/framework-contracts-guide.md` | Cascade, mini-competition, max amount, duration |
| eSubmission / eTendering | `references/etendering-guide.md` | TED publication, submission system, e-Certis |
| Exclusion & Selection | `references/exclusion-selection-criteria.md` | Art. 136–141 FR, EDES database, PADOR |
| Conflict of Interest | `references/conflict-of-interest-procurement.md` | Art. 61 FR, declarations, screening |
| Contract Modification | `references/contract-modification-rules.md` | Art. 172 FR, substantial modification test |
| Abnormally Low Tenders | `references/alt-analysis.md` | Request for justification, rejection criteria |
| Thresholds & flat-rate corrections | `references/procurement-thresholds-2024.md` | Current FR thresholds, correction rates, Art. 260 coefficients — read; do not generate |

---

## Thresholds Quick Reference (2024–2025)

Read from `references/procurement-thresholds-2024.md` — do not generate from training data.

| Contract Type | Below Threshold Simplified | Negotiated (single tender) | Negotiated (min 3) | Open/Restricted (TED publication) |
|---|---|---|---|---|
| Supplies & Services | < €15,000 | €15,000 – €60,000 | €60,000 – €139,000 | > €139,000 |
| Works | < €15,000 | €15,000 – €100,000 | €100,000 – €5,382,000 | > €5,382,000 |
| Specific contracts on FwC | Per FwC terms | Per FwC terms | Per FwC terms | Per FwC terms |

(from `references/procurement-thresholds-2024.md` — verify if after January 2026)

---

## Constraints

### MUST DO
- Verify the estimated contract value using a methodology that prevents artificial
  splitting — aggregate all related needs over the contract's full duration
- Register every procurement above €15,000 in ABAC (commitment) before signing any contract
- Constitute a formal Evaluation Committee with a minimum of 3 members (odd number
  recommended); at least one member must not belong to the initiating unit
- Collect conflict of interest declarations from all evaluation committee members
  before opening any tenders
- Apply the exclusion grounds check via EDES (Early Detection and Exclusion System)
  for all tenderers above €15,000
- Respect the mandatory standstill period of 14 calendar days after notification of
  award decision before signing the contract (for above-threshold contracts)
- Publish a Contract Award Notice on TED within 30 days of signing for above-threshold
  contracts
- Document every step of the evaluation with a contemporaneous written record;
  the evaluation report must be retained for 7 years
- For framework contracts, fix and document the maximum amount at signature; this
  cannot be exceeded across all specific contracts
- Apply the cascade mechanism strictly: approach the contractor ranked No. 1 first;
  only if they cannot perform do you go to No. 2, and document the reason

### MUST NOT DO
- Split contracts artificially to fall below publication thresholds — this is
  an irregularity and grounds for financial correction
- Modify a contract in a way that is "substantial" (changes economic balance, extends
  scope beyond original needs, replaces contractor) without re-tendering
- Allow a tenderer to submit documents after the deadline — all tenders received after
  the deadline must be rejected without being opened
- Use award criteria that function as selection criteria (financial capacity, company
  size are selection criteria, not award criteria)
- Negotiate with tenderers on the substance of their bids during an open procedure
- Accept a tender from a tenderer in an exclusion situation under Art. 136 FR
- Sign a contract or specific contract before ABAC commitment is recorded
- Communicate with tenderers outside the official eTendering channel during the
  tendering period — all Q&A must go through the platform and be shared with all
  tenderers equally
- Request bank guarantees or performance bonds without explicit legal basis in the
  contract

---

## Output Templates

### 1. Procurement Plan Entry

**ANNUAL PROCUREMENT PLAN — ENTRY SHEET**

**DG/Service:** [XX] — **Unit:** [Name] — **Year:** [YYYY]

**Title of procurement:** [Descriptive title]
**CPV code(s):** [Main CPV + supplementary CPVs]
**Type of contract:** - [ ] Services - [ ] Supplies - [ ] Works
**Estimated value (excl. VAT):** €[amount] [over full duration: [N] years]
**Type of framework contract:** - [ ] Single - [ ] Multiple (cascade) - [ ] Multiple (reopening)
**Number of contractors:** [N]
**Procedure:** - [ ] Open - [ ] Restricted - [ ] Negotiated - [ ] Competitive Dialogue
**Planned launch date:** [Q1/Q2/Q3/Q4 YYYY]
**Planned signature date:** [Q YYYY]
**Renewal of existing contract:** - [ ] Yes - [ ] No — If yes: [current contract ref]
**Linked to shared service/OIB:** - [ ] Yes - [ ] No
**Authorising Officer:** [Name, grade]
**Contact:** [Name, email]
**Budget line(s):** [ABAC BL]

---

### 2. Evaluation Committee Report Structure

**EVALUATION REPORT**

**Procurement reference:** [CFT-DG-YYYY-NNNNN]
**Subject:** [Title of contract]
**Procedure:** [Open / Restricted / Negotiated]
**Evaluation Committee:** [Names, units, roles — Chair / Members / Observers]
**Date(s) of evaluation:** [DD Month YYYY]

**1. Opening of Tenders**

- Number of tenders received: [N]
- Tenders received after deadline (rejected without opening): [N]
- Tenders properly submitted and opened: [N]
- [List tenderers by reference code — do not use company names before award]

**2. Exclusion Criteria Check (Art. 136 FR)**

[For each tenderer] Status: - [ ] Compliant - [ ] Non-compliant [reason]
EDES check performed: - [ ] Yes [date] - [ ] Not required (< €15,000)

**3. Selection Criteria Check**

- 3.1 Legal / Administrative capacity
- 3.2 Economic and financial capacity
- 3.3 Technical and professional capacity

[For each tenderer]: - [ ] Pass - [ ] Fail [documented reason]

**4. Technical Quality Evaluation**

Criteria and weightings:
- Criterion 1: [Description] — Weight: [X]% — Max score: [N]
- Criterion 2: [...]

[Scoring table per tenderer per criterion]

**5. Financial Evaluation**

[Price comparison table. Note: price is always a criterion — typically 20–40%]
Abnormally low tender check: - [ ] Triggered for [ref] - [ ] Not triggered
[If triggered: document request for justification and outcome]

**6. Best Value for Money Ranking**

[Final ranking table: quality score + price score = total score]

**7. Recommendation for Award**

The Evaluation Committee unanimously / by majority recommends award to [Tenderer Ref X] with a total score of [N/100]. Estimated contract value: €[amount].

**8. Declaration**

All committee members confirm no conflict of interest and that evaluation was conducted in accordance with the published criteria. [Signatures / dates]

---

### 3. Framework Contract Cascade — Specific Contract Request Memo

**SPECIFIC CONTRACT REQUEST UNDER FRAMEWORK CONTRACT**

**FC Reference:** [FC-DG-YYYY-NNNNN]
**Specific Contract No.:** [SC-NNN]
**Date:** [DD Month YYYY]

**Contractor (Rank 1):** [Company name]
**Requested service:** [Description of specific need]
**Estimated value:** €[amount]
**Period of performance:** [DD Month YYYY] to [DD Month YYYY]
**Cumulative spend on FC to date:** €[amount]
**Remaining FC maximum amount:** €[amount]

**Cascade Application:**
- [ ] Rank 1 contractor approached on [date] — - [ ] Accepted / - [ ] Declined — If declined: [documented reason]
- [ ] Rank 2 contractor approached on [date] — - [ ] Accepted / - [ ] Declined [if applicable]
- [ ] Rank 3 contractor approached on [date] — - [ ] Accepted [if applicable]

**Deliverables requested:** [List with deadlines]

**Payment terms:** [As per FC Article X]
**Budget line:** [ABAC reference]
**Authorising Officer:** [Name]

---

### 4. Conflict of Interest Declaration (Evaluation Committee Member)

**DECLARATION OF ABSENCE OF CONFLICT OF INTEREST AND CONFIRMATION OF CONFIDENTIALITY**

**Procurement:** [Title — CFT reference]
**Name:** [Full name]
**Function:** - [ ] Chair - [ ] Member - [ ] Observer - [ ] Expert

I, the undersigned, declare that:

1. I have no personal interest (financial, family, professional, or other) in any of the tenderers participating in the above procurement procedure.
2. I am not aware of any circumstances that could reasonably be perceived as creating a conflict of interest as defined in Article 61 of Regulation (EU, Euratom) 2018/1046.
3. I commit to treating all information relating to the tenders as confidential and to using it only for the purposes of this evaluation.
4. I understand that, should a conflict of interest arise during the evaluation, I am obliged to declare it immediately and to withdraw from the evaluation.

- [ ] I confirm that I have no conflict of interest — I may proceed with the evaluation.
- [ ] I declare a potential conflict of interest as follows: [description] → I am withdrawing from the evaluation and notify the Chair accordingly.

**Signed:** ___________________ — **Date:** [DD Month YYYY]

---

## Key Financial Regulation Articles — Procurement

| Article | Subject |
|---|---|
| Art. 2 | Definitions (contracting authority, framework contract, etc.) |
| Art. 61 | Conflict of interest |
| Art. 136–141 | Exclusion criteria and EDES |
| Art. 160 | General principles (transparency, equal treatment, non-discrimination) |
| Art. 161 | Thresholds and procedures |
| Art. 164 | Open procedure |
| Art. 165 | Restricted procedure |
| Art. 166 | Negotiated procedure |
| Art. 167 | Competitive dialogue |
| Art. 168 | Framework contracts |
| Art. 170 | Selection criteria |
| Art. 171 | Award criteria (best value for money or lowest price) |
| Art. 172 | Contract modification rules |
| Art. 175 | Publication in OJ (TED) |

---

## Knowledge Reference

Financial Regulation (EU, Euratom) 2018/1046, Rules of Application (Delegated Regulation
2019/715 for agencies; Commission-specific RAP), EDES database, TED/OJS publication rules,
eTendering platform (eSubmission), e-Certis, PADOR (Participant Register), CPV codes
(Common Procurement Vocabulary), ABAC financial management system, OIB procurement support,
DG BUDG procurement guidance notes, OLAF anti-fraud guidance, Public Procurement Directives
2014/24/EU and 2014/25/EU (for context — EC applies FR not the Directives directly),
Internal Audit Service (IAS) procurement audit standards, EC Anti-Fraud Strategy (CAFS).

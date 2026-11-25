---
name: financial-officer
description: >
  Use when executing, validating, or advising on financial operations within the European
  Commission under the Financial Regulation (Regulation (EU, Euratom) 2018/1046).
  Covers the roles of Authorising Officer by Delegation (AOD) and Authorising Officer
  by Subdelegation (AOSD), the four-eye financial circuit (initiator, verifier, AOSD/AOD),
  budget commitments, legal commitments, payment orders, ex-ante controls, recovery
  orders, year-end operations, RAL management, and ABAC system operations.
  Also covers financial corrections, irregularity reporting to OLAF, and interactions
  with the Internal Audit Service (IAS) and European Court of Auditors (ECA).
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-finance
  triggers: >
    financial officer, authorising officer, AOD, AOSD, ABAC, commitment, payment order,
    financial circuit, ex-ante control, recovery order, financial correction, irregularity,
    OLAF, ECA, IAS, budget line, appropriations, RAL, year-end, carry-over, financial
    regulation, budget implementation, four-eyes principle, imprest account, grant payment,
    contract payment, pre-financing, interim payment, final payment, clearance, liquidation,
    financial statement, DAS, legality and regularity, sound financial management,
    budget officer, financial management, DG BUDG, internal control
  role: specialist
  scope: financial-execution-control-advice
  output-format: financial-documents-advice
  institution: European Commission
  related-skills: procurement-expert, budget-officer, internal-auditor, grants-officer,
    head-of-unit
---

# Financial Officer / Authorising Officer by Delegation – EU Commission

Senior financial officer with comprehensive expertise in EU budget implementation under
the Financial Regulation, covering all stages of the expenditure cycle, internal control
requirements, and accountability obligations. Combines operational ABAC expertise with
deep knowledge of legality, regularity, and sound financial management principles.

---

## Core Workflow

1. **Budget planning** — Identify applicable budget lines, verify appropriations
   availability, plan commitments calendar aligned with work programme.
2. **Legal commitment** — Verify legal basis, check against the global budget commitment
   (ABAC), ensure supporting documents are complete (contract / grant agreement /
   decision) before signing.
3. **Implementation** — Monitor contract/grant execution, validate deliverables,
   manage pre-financing, interim payments, and final payments.
4. **Liquidation** — Verify correctness of invoices/cost claims, check eligible costs,
   validate administrative and financial acceptance.
5. **Payment order** — Issue payment order in ABAC within the payment deadline;
   monitor late payment interest liability (Directive 2011/7/EU applies by analogy
   via FR).
6. **Year-end** — RAL (Reste à Liquider) management, automatic carry-overs vs.
   decision-based carry-overs, decommitment of unused appropriations.
7. **Recovery** — Identify amounts unduly paid, issue debit note, follow up recovery
   order, escalate to BUDG Central Services if contested.
8. **Control & audit** — Respond to IAS/ECA audit requests, implement recommendations,
   manage the Annual Control Report, contribute to the Annual Activity Report (AAR)
   assurance section.

---

## Reference Guide

> **No reference files exist for this skill yet.** This skill's domain is the
> **Financial Regulation (Reg. 2018/1046)** and the **ABAC** accounting system —
> neither is part of the `staff-regulations` reference corpus (which covers only
> the Staff Regulations and CEOS). Until a Financial Regulation reference is
> added, apply the topics below from model knowledge and tag every FR citation
> `[FR — verify current article]` and every figure `[model knowledge — verify]`.
> Where a financial circuit depends on a **Staff Regulations** delegation, the SR
> text is available at `../../references/` (see `staff-regulations-index.md`).

| Topic | Status | Apply from |
|---|---|---|
| Financial Regulation (Title IV, Arts. 63–107) | reference file not yet available | model knowledge — tag `[FR — verify current article]` |
| ABAC (commitment, liquidation, payment, year-end) | reference file not yet available | model knowledge — tag `[model knowledge — verify]` |
| Internal control framework (ICS, COSO) | reference file not yet available | model knowledge |
| Grant management (pre-financing, payments, audits) | reference file not yet available | model knowledge |
| Recovery orders (Art. 101 FR) | reference file not yet available | model knowledge — `[FR — verify current article]` |
| Year-end operations (carry-over, RAL, decommitment) | reference file not yet available | model knowledge |
| ECA / IAS audit response | reference file not yet available | model knowledge |
| Anti-fraud (CAFS, OLAF reporting) | reference file not yet available | model knowledge |

---

## Expenditure Cycle at a Glance

```
BUDGET COMMITMENT (ABAC) ──► LEGAL COMMITMENT (contract/grant/decision)
         │
         ▼
  IMPLEMENTATION (service delivery / eligible costs incurred)
         │
         ▼
  LIQUIDATION (verification of invoices / cost claims — 4-eye principle)
         │
         ▼
  PAYMENT ORDER (ABAC — AOSD/AOD signature — payment within deadline)
         │
         ▼
  ACCOUNTING (Central Accounting Officer — ABAC Actuals)
         │
         ▼
  ANNUAL CONTROL / AAR ASSURANCE / ECA DAS
```

---

## Constraints

### MUST DO
- Always ensure the **budget commitment precedes the legal commitment** — committing
  expenditure without a prior ABAC budget commitment is an irregularity (Art. 110 FR)
- Apply the **four-eyes principle** to all financial operations: the person who initiates
  a transaction cannot be the same person who verifies and authorises it; ABAC workflow
  enforces this — never attempt to bypass it
- Verify **legality and regularity** for every payment: is there a legal base?
  does the payment comply with the applicable rules? is the amount correct?
  are supporting documents complete?
- Respect **payment deadlines**: 30 days for standard public contracts / 60 days
  for research grants (unless contract specifies otherwise); late payment triggers
  interest automatically
- Report any **suspected fraud or irregularity** to OLAF immediately via DG OLAF
  reporting channel — the obligation is personal for the AOD and cannot be delegated;
  do not investigate internally without OLAF's guidance
- Maintain a complete **audit trail** for every financial operation: all supporting
  documents must be filed and retained for at least 7 years post-closure of the
  programme/contract
- Issue a **debit note** as the first step in any recovery — do not accept informal
  repayment arrangements; the ABAC recovery order must be formally recorded
- Contribute to the **Annual Activity Report (AAR)** assurance declaration: as AOD,
  you sign off on the reasonable assurance that resources were used for their intended
  purpose with adequate controls

### MUST NOT DO
- Sign a payment order without verifying that the underlying obligation (service
  delivery, eligible costs, completion of milestones) has been properly validated
  by the responsible technical unit
- Approve a commitment that exceeds the available appropriations on the relevant
  budget line — ABAC will block this, but any workaround attempt is a serious breach
- Accept a bank account change request for a beneficiary without following the strict
  verification procedure (written confirmation from the beneficiary + verification
  against original contract) — this is a major fraud vector
- Carry over non-differentiated appropriations beyond year-end without a formal
  carry-over decision and DG BUDG approval
- Write off a recovery order without the proper authorisation procedure and documented
  justification (insolvent debtor, cost of recovery disproportionate, etc.)
- Delegate financial authority beyond the delegation chain — an AOSD cannot further
  subdelegate without explicit authorisation from the AOD
- Mix up budget lines — appropriations committed on one budget line cannot be used
  to pay costs charged to another line without a formal transfer (virement) approved
  per FR Art. 30

---

## Output Templates

### 1. Commitment Decision Checklist

COMMITMENT DECISION CHECKLIST
Reference (ABAC):     [BUD/YYYY/NNNNN]
DG / Unit:            [DG XX / Unit X.X]
Budget line:          [XX.YYYYYYY]
Amount:               €[amount]
Type of commitment:   - [ ] Individual  - [ ] Global (framework)  - [ ] Provisional
Counterpart:          [Name — or "to be determined" for global commitment]
Legal basis:          [Regulation / Decision / Contract reference]

**Pre-Commitment Checklist:**
- [ ] Available appropriations confirmed on BL (ABAC real-time check)
- [ ] Legal basis for expenditure exists
- [ ] Procurement procedure completed (if applicable) — reference: [CFT-XX]
- [ ] Grant/subsidy decision issued (if applicable) — reference: [...]
- [ ] Consistency with work programme / AMP output confirmed
- [ ] Supporting documents attached (procurement file / grant decision / agreement)
- [ ] Verification by financial initiator (name, date)
- [ ] Ex-ante control by verifier (if above threshold) (name, date)
- [ ] ABAC commitment recorded — transaction ID: [XXXXXXXX]

**Authorising Officer (AOSD / AOD):**
- [ ] I confirm all pre-commitment conditions are met.

Signed: ___________________    Date: [DD Month YYYY]
ABAC profile: [Role code]

---

### 2. Payment Validation Memo (Liquidation)

PAYMENT VALIDATION — LIQUIDATION MEMO
Payment reference (ABAC): [PAY/YYYY/NNNNN]
Contract / Grant ref:     [Reference]
Counterpart:              [Company / Beneficiary name]
Invoice / Cost claim ref: [Invoice number / Claim reference]
Invoice date:             [DD Month YYYY]
Amount claimed:           €[amount]
Amount validated:         €[amount]
Payment deadline:         [DD Month YYYY] ([30/60] days from [event])

**Validation Checklist:**
- [ ] Invoice matches the contract / grant agreement terms
- [ ] Services / deliverables / milestones confirmed as received / completed
  → Confirmation from technical responsible: [name, date]
- [ ] Calculation of eligible amount verified:
  - [ ] Cost statement checked against eligible cost categories
  - [ ] Ineligible costs deducted: €[amount] — reason: [...]
  - [ ] Pre-financing deduction applied: €[amount] (if applicable)
- [ ] VAT treatment verified (EU institutions exempt from VAT — check if correctly excluded)
- [ ] Bank account matches contract (last verified: [date])
- [ ] No recovery/debit note outstanding against this beneficiary
- [ ] RAL impact noted — remaining commitment after payment: €[amount]

**Financial Verification (verifier):**
Name: ___________    Date: [DD Month YYYY]

**Payment Authorisation (AOSD / AOD):**
- [ ] Payment validated and authorised.
- [ ] Payment partially validated — amount authorised: €[amount] — reason: [...]
- [ ] Payment rejected — reason: [...]

Signed: ___________________    Date: [DD Month YYYY]

---

### 3. Recovery Order — Initiation Note

RECOVERY ORDER — INITIATION
Reference:      [REC/YYYY/NNNNN]
DG / Unit:      [DG XX / Unit X.X]
Debtor:         [Name / Legal entity]
Contract / grant: [Reference]
Amount due:     €[amount]
Currency:       EUR

Reason for recovery:
- [ ] Overpayment — amount paid exceeds validated eligible costs
- [ ] Ineligible expenditure declared — [describe]
- [ ] Undelivered service or milestone — [describe]
- [ ] Other: [...]

**Timeline of Events:**
[Date]: [Payment made / cost claim submitted]
[Date]: [Audit/verification finding — specify by whom]
[Date]: [Contradictory procedure — right to be heard offered to debtor]
[Date]: [Debtor response — or no response by deadline]
[Date]: [Recovery decision — by AOD]

**Step 1 — Debit Note:**
Debit note ref:    [DN-YYYY-NNN]
Date issued:       [DD Month YYYY]
Payment deadline:  [30 days from issue = DD Month YYYY]
Amount:            €[amount] + interest if paid after [DD Month YYYY]

**Step 2 — ABAC Recovery Order:**
- [ ] ABAC recovery order recorded — transaction ID: [XXXXXXXX]

**Step 3 — Escalation (if unpaid after deadline):**
- [ ] Referred to DG BUDG Central Services for enforcement — [date]
- [ ] Set-off applied against pending payment — [date] [if applicable]
- [ ] Write-off procedure initiated — [date] [if applicable — requires formal decision]

**Anti-Fraud Note:**
- [ ] No indicators of fraud detected — treated as administrative irregularity
- [ ] Fraud indicators present — OLAF notified on [date] — ref: [OLAF ref]

---

### 4. Year-End RAL Closure Note

YEAR-END RAL ANALYSIS — UNIT [XX]
Budget year:   [YYYY]
Date:          [DD Month YYYY]
Prepared by:   [Name, AOD/AOSD]

**Commitments Outstanding as at 31 December [YYYY]:**

| BL | Commitment ref | Counterpart | Committed | Paid | RAL |
|---|---|---|---|---|---|
| [XX.YYYYYYY] | [ref] | [name] | €[x] | €[y] | €[z] |
| ... | | | | | |

**TOTAL RAL:** €[amount]

**Analysis per Commitment:**
[For each open commitment — action recommended:]
- [ ] Keep open — pending invoice / milestone due in Q1 [YYYY+1] — estimated payment date: [...]
- [ ] Carry over — differentiated appropriations — automatic carry-over applies
- [ ] Carry over — non-differentiated — requires formal carry-over decision by [date]
- [ ] Decommit — service not delivered / contract terminated — decommitment amount: €[x]

DECOMMITMENTS PROPOSED: €[total]
CARRY-OVERS REQUESTED:  €[total]
JUSTIFICATION: [Brief narrative]

**Next Steps:**
- [ ] Submit RAL analysis to DG BUDG by [internal deadline]
- [ ] Request carry-over decisions for non-diff appropriations — draft attached
- [ ] Update ABAC with decommitments by [31 January YYYY+1]

---

## Key Financial Regulation Articles

| Article | Subject |
|---|---|
| Art. 63 | Shared management — responsibilities |
| Art. 73 | Authorising officers — types and responsibilities |
| Art. 74 | Delegation and subdelegation of budget implementation |
| Art. 75–76 | Accounting officers — role and obligations |
| Art. 79 | Internal auditor |
| Art. 89 | Commitment — types (individual, global, provisional) |
| Art. 90 | Legal commitments |
| Art. 98 | Time limits for payment |
| Art. 101 | Recovery of amounts unduly paid |
| Art. 109 | Irregularities |
| Art. 110 | Reporting to OLAF |
| Art. 195 | Annual Activity Report — Director's assurance declaration |

---

## Knowledge Reference

Financial Regulation (EU, Euratom) 2018/1046 (Arts. 62–110 most relevant), Rules of
Application (Delegated Regulation), ABAC financial management system (Accrual-Based
Accounting system), Commission Decision on Internal Control Standards (ICS), COSO internal
control framework, ECA Annual Report (DAS), Annual Activity Report methodology (SG
guidance), DG BUDG budget implementation guidance, OLAF reporting procedures, Commission
Anti-Fraud Strategy (CAFS), IAS audit methodology, Grant Management Manual, Procurement
Manual, late payment rules (FR Art. 98 + Council Regulation 1150/2000), budget
nomenclature and financial regulations per programme (HEU, ERDF, ESF+, etc.).

---

> **DRAFT** — For review by the responsible official before action is taken. Not an official Commission decision or position.

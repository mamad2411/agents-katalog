---
name: internal-controls-design
description: Design and maintain internal controls — segregation of duties, approval matrices, process documentation, audit trails, and a startup-appropriate control environment to prevent fraud and errors.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, internal-controls, segregation-of-duties, audit-trails, process-documentation]
related_skills: [monthly-close-process, audit-preparation, accounts-payable-management, accounts-receivable-management, payroll-processing]
inputs_required: [current-control-environment-assessment, organizational-chart, accounting-system-access-list, current-approval-processes, existing-process-documentation]
deliverables: [control-environment-assessment, approval-matrix, segregation-of-duties-matrix, process-documentation-for-key-cycles, quarterly-control-testing-schedule, remediation-plan]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Internal Controls Design

Design, document, and maintain a startup-appropriate internal control environment. Implement segregation of duties, approval matrices, process documentation, audit trails, and monitoring. Goal: the right controls at the right time — enough to prevent fraud and errors without slowing the business down.

## Purpose

Startups face a control paradox: at 10 people, you can't segregate duties because there aren't enough people — but at 10 people, a single fraud or error can destroy the company. This skill solves that problem by providing a stage-appropriate control framework. Instead of copying SOX requirements designed for billion-dollar companies, it gives startups the controls they actually need: cash protection first, then approval matrices, then process documentation, evolving as the company grows from seed to series B and beyond.

## When to Use

- "Design our internal controls"
- "Who should approve what?"
- "Do we have segregation of duties?"
- "Document this financial process"
- "Control environment review"
- "Are we SOX-ready?" (if preparing for IPO)

## Inputs Required

- Current control environment assessment
- Organizational chart with roles and responsibilities
- Access list for all financial systems (accounting, banking, payroll)
- Current approval processes and thresholds
- Existing process documentation (if any)
- Prior audit findings or control gaps (if applicable)

## Quick Reference

| Stage | Control Level | Focus Area |
|-------|---------------|------------|
| Pre-seed / Seed (< 15 people) | Minimal viable | Fraud prevention, cash controls, CEO reviews all payments > $500 |
| Series A (15-50 people) | Lightweight | Approval matrix, basic segregation, documented processes |
| Series B (50-150 people) | Structured | Full segregation, audit trails, quarterly testing |
| Pre-IPO / Series C+ (150+ people) | SOX-lite / SOX-ready | Fully documented, tested, attested |

| Control Area | Highest Risk | Bare Minimum |
|-------------|-------------|--------------|
| Cash | Fraud (#1 startup risk) | Separate initiator, approver, reconciler |
| AP | Duplicate payments, fictitious vendors | Approval matrix, W-9 for new vendors |
| Payroll | Ghost employees, wrong amounts | CEO review of payroll register |
| Access | Unauthorized transactions | 2FA on all financial systems, termination checklist |

## Procedure

### 1. Assess Current State

Evaluate what controls exist and what's missing across:
- Cash disbursements
- Approval authority
- Segregation of duties
- Process documentation
- IT access controls
- Monitoring and testing

### 2. Prioritize by Risk

Start with the highest-risk areas:
1. **Cash controls** — 90% of startup fraud is cash-related
2. **Approval matrix** — who can approve what
3. **Segregation of duties** — incompatible duties separated or compensated
4. **Process documentation** — key financial cycles
5. **IT access controls** — who has access to what

### 3. Document the Control Framework

#### Cash Controls (Highest Priority)

Cash is the #1 fraud risk for startups.

```
CONTROL: Segregation of Duties - Cash Disbursements

  Person A: Initiates payment (prepares the payment run)
  Person B: Approves payment (reviews and authorizes)
  Person C: Reconciles bank account (independent verification)

  Risk if not segregated: One person could create a fake vendor,
  approve the payment, and reconcile it away.
```

For very small teams (3-5 people): the CEO reviews every payment over $500. A monthly bank rec by someone not involved in payments. This is the bare minimum.

#### Approval Matrix

Define who can approve what:

| Transaction Type | Up to $1,000 | $1,000-$5,000 | $5,000-$25,000 | $25,000+ |
|---|---|---|---|---|
| Vendor Payments | Dept Head | Dept Head + CEO | CEO + CFO | CEO + CFO + Board (if > $50k) |
| Expense Reports | Manager | Manager + CEO | CEO | CEO + CFO |
| New Hires (salary) | Dept Head + CEO | CEO + CFO | CEO + CFO + Board | CEO + CFO + Board |
| Contractors | Dept Head | Dept Head + CEO | CEO + CFO | CEO + CFO |
| Software Subscriptions | Dept Head | Dept Head + CEO | CEO + CFO | CEO + CFO |
| Customer Contracts / Pricing | Sales Manager + CEO | CEO + CFO | CEO + CFO + Board | Board |
| Equity Grants | N/A | CEO | CEO + Board | Board |

#### Segregation of Duties Matrix

For each key process, identify incompatible duties:

| Process | Duty 1 (Initiate) | Duty 2 (Approve) | Duty 3 (Record) | Duty 4 (Reconcile) |
|---|---|---|---|---|
| Vendor Payments | AP Clerk / Office Manager | CEO / CFO | Accountant | Accountant (different person) or CEO |
| Payroll | HR / Office Manager | CEO | Accountant / Payroll Provider | Accountant or CEO |
| Customer Invoicing | Sales / Account Manager | Sales Manager | Accountant | Accountant or CEO |
| Expense Reimbursement | Employee | Manager + CEO (if > $500) | Accountant | CEO (spot check) |
| Journal Entries | Accountant | CEO / CFO | Accountant | CEO / CFO (monthly review) |
| Bank Reconciliation | Accountant | — | — | CEO / CFO (review completed rec) |

For very small teams, document **compensating controls** where true segregation is impossible:
> "Jane both initiates and records AP payments. Compensating control: CEO reviews ALL payments over $500 before they go out, and reviews the full AP register monthly."

#### Process Documentation

For each key financial process, document:

```
PROCESS: Accounts Payable - Vendor Payments

Purpose: Ensure all vendor payments are valid, approved, and accurately recorded.

Frequency: Weekly payment run (Thursdays).

Steps:
  1. AP receives vendor invoice (email or portal).
  2. AP verifies: vendor is in master, amount matches PO/estimate, not a duplicate.
  3. AP enters invoice into [system] with coding (account, department).
  4. System routes for approval based on the amount matrix.
  5. Approved invoices batched for weekly payment run.
  6. Payment run reviewed by CEO (all payments > $500).
  7. After approval, payments executed (ACH, check, wire).
  8. Payments recorded in GL, AP subledger updated.
  9. Monthly: AP subledger reconciled to GL.
  10. Monthly: Top 10 vendor statements reconciled to AP subledger.

Systems: QuickBooks / Xero / Netsuite, Bill.com / Brex / Ramp

Controls:
  - Invoice approval required before payment (preventive).
  - CEO reviews all payments > $500 (detective).
  - Monthly AP reconciliation (detective).
  - Vendor master changes require CEO approval (preventive).
  - New vendors require W-9 before first payment (preventive).

Evidence retained:
  - Approved invoices (digital or physical).
  - Payment run approval (email or system log).
  - Reconciliation reports.
  - W-9 forms.

Risks if control fails:
  - Duplicate payment.
  - Payment to wrong vendor.
  - Payment for goods/services not received.
  - Fraud (payment to fictitious vendor).
```

#### Information Technology Controls

Minimal IT controls for startups:

- [ ] **Access controls**: who has admin access to accounting systems, bank portals, and payroll?
- [ ] **Password policy**: no shared passwords. 2FA required on all financial systems and bank accounts.
- [ ] **Audit trails**: all financial systems must have audit trails enabled (who did what, when).
- [ ] **Backup**: financial data backed up daily. Test the restore.
- [ ] **Termination checklist**: revoke access to all financial systems within 24 hours of departure.

#### Monitoring & Testing

Quarterly, test that controls are actually working:

| Control | Test Procedure | Frequency |
|---|---|---|
| Payment approval | Sample 10 payments, verify approval evidence | Quarterly |
| Bank reconciliation | Review last 3 reconciliations, verify they tie | Monthly |
| Vendor master changes | Review all vendor additions, verify W-9 on file | Quarterly |
| Journal entry review | Review all manual JE's > $5,000 for support | Quarterly |
| Access review | Review who has access to each system, verify still appropriate | Quarterly |
| Payroll verification | Sample 3 payroll runs, verify against employment agreements | Semi-annually |

## Output Format

- Control environment assessment (what's in place, what's missing)
- Approval matrix (ready for implementation)
- Segregation of duties matrix
- Process documentation for key cycles (AP, AR, Payroll, Close)
- Quarterly control testing schedule
- Remediation plan for gaps

## Done Criteria

The skill is complete when:
1. Current state is assessed and gaps are identified, prioritized by risk.
2. Cash controls are designed with segregation of duties (initiate, approve, reconcile).
3. Approval matrix is defined by transaction type and dollar threshold.
4. Segregation of duties matrix is documented for all key processes with compensating controls identified where segregation isn't possible.
5. Process documentation is created for at least the top 3 highest-risk cycles (cash/AP, payroll, revenue/AR).
6. IT access controls are defined (2FA, access reviews, termination checklist).
7. A quarterly testing schedule is established.

## Pitfalls

- **Building SOX-level controls for a seed-stage company** — 20-person startups don't need 200-page control manuals. Proportionality is the key design principle. Build what you need, not what the Fortune 500 has.
- **Designing controls that nobody follows** — a perfect control framework that sits in a Google Drive folder untouched is worse than no controls. Controls must be practical, trained, and enforced.
- **Creating segregation of duties that doesn't exist** — in a 10-person company, you can't fully segregate. That's okay. Document compensating controls and test them. Don't pretend segregation exists when it doesn't.
- **Implementing controls without training** — the AP clerk needs to know WHY the approval matrix exists. Controls work when people understand them, not when they're policy documents.
- **Letting controls degrade over time** — the approval matrix that worked at 30 people is wrong at 60 people. Controls must evolve with the company size and complexity.

### Heuristics

- **Cash controls first**: 90% of startup fraud is cash-related. Control the bank accounts, control the risk.
- **CEO review is the most powerful startup control**: in a 10-person company, the CEO reviewing every payment > $500 is more effective than any formal system.
- **Controls should be proportional**: don't build SOX controls for a seed-stage startup. But don't have NO controls either.
- **Document when you can't segregate**: compensating controls are valid. Document them and test them.
- **Audit trail > manual approval**: a system that logs who did what is often better than an email approval chain.

### Edge Cases

- **Remote / distributed teams**: physical controls (locked check stock, secure filing) don't apply. Digital controls (2FA, access logs, audit trails) matter more.
- **Crypto / digital asset companies**: wholly different control needs. Multi-sig wallets, hardware keys, on-chain verification.
- **International subsidiaries**: local statutory audit requirements may impose additional control requirements.
- **Whistleblower / reporting mechanism**: at Series A+, have a way for employees to report concerns confidentially. It's a requirement for a strong control environment.

## Verification

Can you answer "Who can approve a $10,000 vendor payment?" and "Is there a compensating control for the fact that Jane both initiates and records AP?" and "When was the last time we tested whether our controls are actually working?" If not, the control environment isn't fully understood or documented.

## Example

> **User**: "Design our internal controls — we're a 25-person Series A SaaS company."
> **Expected behavior**: You assess the current state, prioritize cash controls first, design an approval matrix (CEO approves all payments > $1,000), create a segregation of duties matrix documenting which duties are separated and which have compensating controls, document the AP process with a 10-step procedure, set up IT access controls (2FA on all financial systems), and establish a quarterly testing schedule.

> **User**: "We had a near-miss with a fraudulent vendor payment. Fix our AP controls."
> **Expected behavior**: You review the current AP process and identify the control gaps (no W-9 requirement for new vendors, no dual approval on new vendor additions, no monthly vendor statement reconciliation). You implement: new vendor approval workflow requiring CEO sign-off, W-9 collection before first payment, monthly statement reconciliation, and a vendor master change log reviewed quarterly.

## Linked Skills

- Close process design → `monthly-close-process`
- Audit readiness → `audit-preparation`
- AP controls → `accounts-payable-management`
- AR controls → `accounts-receivable-management`
- Payroll controls → `payroll-processing`

---
name: audit-preparation
description: Prepare for financial audits — schedules, reconciliations, documentation, walkthroughs, PBC (prepared by client) lists, and finding resolution for annual financial statement audits.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, audit, audit-preparation, pbc, compliance]
related_skills: [monthly-close-process, financial-statement-generation, internal-controls-design]
inputs_required: [year-end-trial-balance, all-bank-and-investment-statements, ar-and-ap-aging-summaries, payroll-register-and-tax-filings, cap-table-and-equity-documents, fixed-asset-register, legal-agreements-and-contracts]
deliverables: [audit-readiness-assessment, complete-pbc-list-with-status, organized-audit-binder, walkthrough-documentation-package, open-items-tracker]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Audit Preparation

Prepare for and support the annual financial statement audit. Organize schedules, gather documentation, manage the PBC (Prepared By Client) list, support walkthroughs, and resolve auditor findings. Goal: the audit finishes on time, on budget, with minimal findings.

## Purpose

The annual audit is the highest-stakes financial process for most startups — it validates the financial statements, satisfies investor requirements, and builds trust with stakeholders. Poor audit preparation leads to extended timelines, higher costs, unexpected adjustments, and findings that erode confidence. This skill provides the systematic approach — from building the PBC list to managing auditor interactions — so the audit is smooth, predictable, and efficient.

## When to Use

- "Prepare for our audit"
- "Build the PBC list"
- "Organize audit support documentation"
- "What does the auditor need?"
- "Respond to auditor questions"
- "Resolve an audit finding"

## Inputs Required

- Year-end trial balance (closed and reconciled)
- All bank and investment statements
- AR and AP aging summaries
- Payroll register and tax filings for the year
- Cap table and all equity documents (grants, exercises, board consents)
- Fixed asset register with additions and disposals
- Legal agreements (leases, debt, major customer contracts)
- 409A valuation report
- Prior year audit file (if applicable)

## Quick Reference

| Phase | Timeline | Key Activities |
|-------|----------|----------------|
| Pre-audit prep | 3 months before | Reconcile all BS accounts, prepare schedules, draft statements |
| Pre-audit prep | 1 month before | Final year-end close, document estimates, review subsequent events |
| During audit | 4-8 weeks | Respond to PBC requests within 48 hours, support walkthroughs |
| Post-audit | 2-4 weeks after | Resolve findings, implement process improvements |

| Audit Risk | Impact | Prevention |
|------------|--------|------------|
| Revenue recognition | Highest | Deferred revenue schedule, contract documentation |
| Cash | Medium | Bank confirmations, clean reconciliations |
| Equity | Medium | Board consents for every issuance |
| Related party transactions | Medium | Full disclosure, arm's-length documentation |

## Procedure

### 1. Year-End Close Quality Check

Before the auditors arrive:
- Reconcile every balance sheet account > $1,000.
- Verify intercompany accounts (if multiple entities) are eliminated.
- Confirm revenue recognition for all material contracts.
- Scan for unusual journal entries (round numbers, weekend dates, unexpected accounts).

### 2. Build the Audit Binder

Organize all PBC items into a structured folder:

```
📁 FY2026 Audit
  ├── 01 — Trial Balance & GL Detail
  ├── 02 — Cash & Bank
  ├── 03 — AR & Revenue
  ├── 04 — AP & Expenses
  ├── 05 — Payroll & HR
  ├── 06 — Equity & Debt
  ├── 07 — Fixed Assets
  ├── 08 — Tax
  └── 09 — Legal & Commitments
```

### 3. Walkthrough Preparation

For each key process (revenue, AP, payroll, equity), prepare:
- Process narrative / flowchart.
- 2-3 sample transactions with full documentation (contract → invoice → payment → GL posting).
- Control descriptions for each step.

### 4. Auditor Interaction Management

- **Point person**: one person manages all auditor communication.
- **Response time**: within 48 hours for any request.
- **Weekly check-ins**: 15-minute status call to track progress and open items.
- **Issue escalation**: any potential finding or adjustment should be escalated to the CEO/CFO immediately.

### 5. Finding Resolution

When an auditor raises a finding:
1. Understand the issue completely (what's the problem, what's the impact?).
2. Investigate the root cause.
3. Propose a remediation plan with a timeline.
4. Implement the fix (correcting entry, process change).
5. Document the resolution.

### PBC (Prepared By Client) List

Standard audit PBC requests:

#### General
- [ ] Trial balance (as of and for the year ended)
- [ ] General ledger detail for all accounts
- [ ] Board meeting minutes
- [ ] Organizational chart
- [ ] Accounting policies and procedures manual

#### Cash
- [ ] Bank confirmations (or bank statements)
- [ ] Bank reconciliations for all accounts at year-end
- [ ] Investment statements

#### AR & Revenue
- [ ] AR aging summary
- [ ] Revenue by customer for the year
- [ ] Top 10 customer contracts / agreements
- [ ] Deferred revenue schedule and rollforward
- [ ] Bad debt allowance calculation

#### AP & Expenses
- [ ] AP aging summary
- [ ] Top 10 vendor contracts / agreements
- [ ] Prepaid expense schedule and rollforward
- [ ] Accrued expense schedule

#### Payroll & HR
- [ ] Payroll register for the year
- [ ] Payroll tax filings (941, 940, state)
- [ ] Employee roster with compensation
- [ ] Option grant list and board approvals
- [ ] 401(k) plan documents and filings

#### Equity & Debt
- [ ] Cap table (fully diluted)
- [ ] All stock purchase / SAFE / note agreements
- [ ] Board consents for all equity issuances
- [ ] 409A valuation report
- [ ] Debt agreements and amortization schedules
- [ ] Covenant compliance calculations

#### Fixed Assets
- [ ] Fixed asset register (additions, disposals, depreciation)
- [ ] Proof of ownership for major assets

#### Tax
- [ ] Income tax returns (federal and state)
- [ ] Sales tax returns
- [ ] Tax notice correspondence

#### Legal & Commitments
- [ ] Legal letter (sent to all attorneys)
- [ ] Lease agreements
- [ ] Insurance policies
- [ ] Any litigation or claims (current, pending, threatened)
- [ ] Contractual commitments and contingencies

## Output Format

- Audit readiness assessment (what's ready, what's not)
- Complete PBC list with status tracking
- Audit binder (organized by section)
- Walkthrough documentation package
- Open items tracker
- Post-audit summary (findings, adjustments, improvements for next year)

## Done Criteria

The skill is complete when:
1. Every balance sheet account > $1,000 is reconciled to a supporting schedule.
2. The complete PBC list is built with status tracking and assigned owners.
3. The audit binder is organized by section with all supporting documentation.
4. Walkthrough documentation (narratives + sample transactions) is prepared for each key process.
5. An open items tracker is set up for auditor requests with < 48-hour response commitments.
6. A point person is designated for all auditor communication.

## Pitfalls

- **Starting audit preparation after the year-end close** — the best time to start audit prep is 3 months before year-end. Starting after close guarantees rushed schedules and missed items.
- **Assuming prior year's PBC list is still complete** — the business changes over the year (new revenue streams, debt, acquisitions). Always rebuild the PBC list from scratch each year.
- **Not resolving prior year findings before the new audit** — auditors will check. Unresolved prior year findings are the first thing they look for. Fix them before they arrive.
- **Giving the auditor raw data without explanations** — handing over a ledger dump instead of clean, labeled schedules guarantees questions. Every schedule should have column headers, totals, and tie to the GL.
- **Forgetting to reconcile intercompany accounts** — multiple entities with uncleared intercompany balances is the most common balance sheet error. Clean these up before the auditors arrive.

### Heuristics

- **Reconcile everything before the auditors arrive**: they find what you didn't reconcile. No surprises.
- **Document unusual items proactively**: an unexplained $50k journal entry will consume hours of auditor time. A one-paragraph explanation resolves it in 5 minutes.
- **Auditors aren't your enemy**: they're a control function. They'll find things. It's not personal.
- **Every finding is a process improvement opportunity**: fix the root cause, not just the symptom.

### Edge Cases

- **First-time audit**: expect 50% more time and cost. You're building everything from scratch.
- **PCAOB vs AICPA standards**: if you're going public or are a public company, the audit standard is higher (PCAOB). Plan accordingly.
- **Material weakness vs significant deficiency**: a material weakness is serious — it means the financials could be materially misstated. A significant deficiency is less severe but still needs fixing.

## Verification

Can you answer "What are the top 5 things the auditor will ask for, and are they ready?" Can every balance sheet account > $1,000 be tied to a supporting schedule? Is there a person designated to respond to all auditor requests with a < 48-hour turnaround? If not, audit preparation is incomplete.

## Example

> **User**: "Prepare us for the annual audit. Build the PBC list and organize the binder."
> **Expected behavior**: You create the complete PBC list organized by category (cash, AR, revenue, AP, payroll, equity, fixed assets, tax, legal), set up the audit binder folder structure, verify that each balance sheet account ties to its supporting schedule, prepare process narratives and sample transactions for walkthroughs, designate a point person for auditor communication, and produce a readiness assessment showing what's complete and what's still needed.

> **User**: "The auditor found a material weakness in revenue recognition. How do we resolve it?"
> **Expected behavior**: You investigate the root cause (was it a control gap, an incorrect application of ASC 606, a contract documentation issue?), propose a specific remediation plan with timeline, implement corrective entries or process changes, document the resolution, and prepare to present it to the auditor with evidence of the fix.

## Linked Skills

- Books closed and clean → `monthly-close-process`
- Statements ready → `financial-statement-generation`
- Process documentation → `internal-controls-design`

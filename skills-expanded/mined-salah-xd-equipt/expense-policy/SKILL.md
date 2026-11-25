---
name: expense-policy
description: "Creates corporate expense policies with spending limits, approval workflows, and reimbursement procedures. Use when establishing rules for business spending and reimbursements."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Expense Policy

## When to Use This Skill

Use this skill when you need to:
- Create an expense reimbursement policy for your team or company
- Define spending limits, approval workflows, and acceptable expenses
- Establish receipt requirements and reimbursement timelines
- Document travel, meals, and entertainment expense rules

**DO NOT** use this skill for budgeting (use budget-planner), accounting setup (use bookkeeping-setup), or personal expense tracking. This is for company expense policies.

---

## Core Principle

A GOOD EXPENSE POLICY EMPOWERS EMPLOYEES TO SPEND WISELY WITHOUT ASKING PERMISSION FOR EVERY COFFEE — CLEAR LIMITS, SIMPLE RULES, FAST REIMBURSEMENT.

---

## Phase 1: Company Context

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Company size** | "How many people will this policy cover?" | 1-10 |
| **Team structure** | "Who approves expenses? (founder, managers, self-approval under threshold)" | Founder approves all |
| **Common expenses** | "What do people typically expense? (software, travel, meals, supplies)" | Software, meals, supplies |
| **Budget constraints** | "Any hard spending limits?" | Reasonable and necessary standard |
| **Reimbursement method** | "How do you reimburse? (payroll, direct deposit, corporate card)" | Direct deposit |
| **Remote or in-office** | "Is your team remote, in-office, or hybrid?" | Remote |

**GATE: Do not proceed without company size and common expense types.**

---

## Phase 2: Policy Framework

### Expense Categories and Limits

```
## [Company Name] Expense Policy

**Effective date:** [Date]
**Applies to:** All employees and contractors authorized to incur expenses

### Spending Limits

| Category | Per-Occurrence Limit | Monthly Limit | Approval Required |
|----------|---------------------|---------------|-------------------|
| Software/subscriptions | $[50]/month per tool | $[200]/month | Under $50: self-approve |
| Office supplies | $[100] | $[200] | Under $50: self-approve |
| Business meals | $[75]/person | $[300] | Under $50: self-approve |
| Client entertainment | $[150]/event | $[500] | Always |
| Travel (domestic) | Per diem or actual | $[2,000]/trip | Always — pre-approval |
| Travel (international) | Per diem or actual | $[5,000]/trip | Always — pre-approval |
| Professional development | $[500]/event | $[1,500]/year | Always |
| Home office equipment | $[500] one-time | $[1,000]/year | Over $200 |

### Pre-Approval Required
The following expenses ALWAYS require pre-approval regardless of amount:
- Travel bookings (flights, hotels)
- Client entertainment over $[75]
- Any single purchase over $[200]
- Recurring subscriptions over $[50]/month
- Conference or event registration
```

### Approval Workflow

```
### Approval Process

| Expense Amount | Approver | Timeline |
|---------------|---------|----------|
| Under $[50] | Self-approved | Submit receipt within 5 business days |
| $[50]-$[200] | Direct manager | Approved within 3 business days |
| $[200]-$[1,000] | Department head / Founder | Approved within 5 business days |
| Over $[1,000] | Founder / CEO | Pre-approval required |
```

---

## Phase 3: Rules and Procedures

### Receipt and Documentation Requirements

```
### Documentation Requirements

- **Receipts required for:** All expenses over $[25]
- **Receipt format:** Digital photo or PDF (paper receipts not required if digital available)
- **Receipt must include:** Date, vendor name, amount, items/description
- **Missing receipt:** Provide a written explanation and manager sign-off. Repeated missing receipts may delay reimbursement.

### Submission Deadline
- Expenses must be submitted within [30] days of purchase
- Late submissions (30-60 days) require manager approval
- Submissions over 60 days old will not be reimbursed without VP/Founder exception
```

### Reimbursement Process

```
### Reimbursement

- **Submission method:** [Expense software / email / spreadsheet]
- **Reimbursement cycle:** [Bi-weekly with payroll / monthly on the 15th]
- **Processing time:** Approved expenses reimbursed within [10] business days
- **Method:** [Direct deposit / added to payroll / corporate card]
```

### What Is NOT Reimbursable

```
### Non-Reimbursable Expenses

- Personal purchases of any kind
- Alcohol (unless pre-approved for client entertainment)
- Traffic violations, parking tickets, or legal fines
- Pet care or childcare during travel
- First-class or business-class airfare (unless pre-approved for flights over 6 hours)
- Gym memberships or personal wellness (unless part of benefits package)
- Political contributions or charitable donations
- Expenses for family members or non-employees
```

---

## Phase 4: Policy Document

### Final Policy Template

```
## [Company Name] Expense Reimbursement Policy

### Purpose
This policy establishes guidelines for business expenses incurred by
[Company] team members. The policy ensures expenses are reasonable,
properly documented, and reimbursed promptly.

### Scope
Applies to all full-time employees, part-time employees, and
authorized contractors of [Company].

[Insert Phase 2 categories and limits]
[Insert Phase 3 rules and procedures]

### Policy Violations
Violations include submitting personal expenses, falsifying receipts,
or repeatedly exceeding limits without approval. Violations may result
in delayed reimbursement, repayment requirements, or disciplinary action.

### Policy Updates
This policy is reviewed [annually]. Changes communicated [30] days
before taking effect.

### Acknowledgment
I have read and understood this expense policy.

Name: _______________
Date: _______________
Signature: _______________
```

---

## Example: 8-Person Remote Startup

**Key provisions:** Self-approval under $50, founder approval over $50. Software under $50/mo self-approved. $500/year professional development budget. Home office stipend of $500 one-time for new hires. Monthly meal allowance of $100 for team events. Receipts required over $25. Reimbursed with bi-weekly payroll.

---

## Anti-Patterns

- **No policy at all** — "just be reasonable" works until someone expenses a $300 dinner. Write it down.
- **Overly restrictive** — requiring approval for a $10 Uber ride wastes everyone's time. Set sensible thresholds.
- **Slow reimbursement** — employees floating company expenses for 60+ days breeds resentment. Reimburse within 2 weeks.
- **Inconsistent enforcement** — if the policy applies to everyone, enforce it for everyone. Including founders.
- **No per-diem option for travel** — per-diem rates eliminate receipt-chasing for meals during travel. Consider offering it.

---

## Recovery

- **No expense tracking system:** Start with a shared spreadsheet template. Upgrade to expense software (Expensify, Ramp) when team exceeds 10 people.
- **Team already has bad habits:** Announce the new policy with a 30-day grace period. After that, enforce consistently.
- **Contractors vs. employees:** Contractor expenses should be included in their contract rate, not reimbursed separately, unless the contract specifies otherwise.
- **International team:** Set per-diem rates by country and accept expenses in local currency with conversion at time of purchase.

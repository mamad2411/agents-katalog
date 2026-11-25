---
name: bookkeeping-setup
description: "Sets up bookkeeping systems with chart of accounts, transaction categories, and reconciliation procedures. Use when establishing or organizing business bookkeeping."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Bookkeeping Setup

## When to Use This Skill

Use this skill when you need to:
- Set up a chart of accounts for a new business
- Organize transaction categories for clean financial tracking
- Create reconciliation procedures and schedules
- Establish bookkeeping workflows from scratch

**DO NOT** use this skill for tax preparation (use tax-prep-checklist), financial projections, or choosing accounting software. This is for setting up the bookkeeping structure itself.

---

## Core Principle

CLEAN BOOKS START WITH A SIMPLE CHART OF ACCOUNTS AND CONSISTENT CATEGORIZATION — COMPLEXITY SHOULD BE ADDED ONLY WHEN THE BUSINESS NEEDS IT.

---

## Phase 1: Business Profile

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What type of business? (service, product, SaaS, consulting)" | Service-based |
| **Entity type** | "Sole prop, LLC, S-corp, C-corp?" | Single-member LLC |
| **Revenue streams** | "How do you make money?" | No default — must be provided |
| **Accounting method** | "Cash or accrual basis?" | Cash basis |
| **Software** | "What bookkeeping software do you use or plan to use?" | QuickBooks Online |
| **Monthly transaction volume** | "Approximately how many transactions per month?" | Under 100 |

**GATE: Do not proceed without business type and revenue streams.**

---

## Phase 2: Chart of Accounts

### Standard Chart of Accounts

```
## Chart of Accounts: [Business Name]

### Assets (1000-1999)
| # | Account Name | Type | Purpose |
|---|-------------|------|---------|
| 1000 | Business Checking | Bank | Primary operating account |
| 1010 | Business Savings | Bank | Reserve / tax savings |
| 1100 | Accounts Receivable | Current Asset | Outstanding client invoices |
| 1200 | Prepaid Expenses | Current Asset | Annual subscriptions paid upfront |

### Liabilities (2000-2999)
| # | Account Name | Type | Purpose |
|---|-------------|------|---------|
| 2000 | Accounts Payable | Current Liability | Bills owed to vendors |
| 2100 | Credit Card | Current Liability | Business credit card balance |
| 2200 | Sales Tax Payable | Current Liability | Collected sales tax owed |
| 2300 | Payroll Liabilities | Current Liability | Payroll taxes owed |

### Equity (3000-3999)
| # | Account Name | Type | Purpose |
|---|-------------|------|---------|
| 3000 | Owner's Equity | Equity | Owner's investment in business |
| 3100 | Owner's Draw | Equity | Money taken out by owner |
| 3200 | Retained Earnings | Equity | Accumulated profits |

### Revenue (4000-4999)
| # | Account Name | Type | Purpose |
|---|-------------|------|---------|
| 4000 | [Primary Service/Product Revenue] | Income | Main revenue stream |
| 4100 | [Secondary Revenue] | Income | Additional revenue |
| 4200 | Other Income | Income | Interest, refunds, misc |

### Cost of Goods Sold (5000-5999)
| # | Account Name | Type | Purpose |
|---|-------------|------|---------|
| 5000 | Contractor Payments | COGS | Freelancers/subcontractors |
| 5100 | Materials / Supplies | COGS | Direct project costs |
| 5200 | Platform Fees | COGS | Payment processing, marketplace fees |

### Operating Expenses (6000-6999)
| # | Account Name | Type | Purpose |
|---|-------------|------|---------|
| 6000 | Advertising & Marketing | Expense | Ad spend, marketing tools |
| 6100 | Software & Subscriptions | Expense | SaaS tools, apps |
| 6200 | Office Supplies | Expense | Supplies, equipment under $2,500 |
| 6300 | Professional Services | Expense | Accounting, legal fees |
| 6400 | Insurance | Expense | Business insurance |
| 6500 | Meals & Entertainment | Expense | Business meals (50% deductible) |
| 6600 | Travel | Expense | Business travel |
| 6700 | Education & Training | Expense | Courses, books, conferences |
| 6800 | Rent / Coworking | Expense | Workspace costs |
| 6900 | Phone & Internet | Expense | Business portion |
| 6950 | Bank Fees | Expense | Monthly fees, wire fees |
```

Customize account numbers and names based on the user's specific business.

---

## Phase 3: Procedures

### Transaction Categorization Rules

```
## Categorization Guide

| Transaction Type | Category | Account | Notes |
|-----------------|----------|---------|-------|
| Stripe/PayPal deposits | Revenue | 4000 | Separate by product if multiple |
| Contractor payments | COGS | 5000 | Must issue 1099 if $600+ |
| Monthly software (Slack, etc.) | Expense | 6100 | |
| Facebook/Google ads | Expense | 6000 | |
| Owner's personal transfer | Equity | 3100 | NOT an expense |
| Quarterly tax payment | Equity | 3100 | NOT an expense — draws for taxes |
| Credit card payment | Liability | 2100 | NOT an expense — reducing liability |
```

### Reconciliation Schedule

```
## Reconciliation Procedures

### Weekly (15 minutes)
- [ ] Categorize all new transactions
- [ ] Review any uncategorized items
- [ ] Flag anything unusual for review

### Monthly (1 hour, by the 10th)
- [ ] Reconcile all bank accounts
- [ ] Reconcile credit cards
- [ ] Review accounts receivable — follow up on overdue invoices
- [ ] Review accounts payable — pay outstanding bills
- [ ] Run P&L report and compare to budget
- [ ] Back up data

### Quarterly (2 hours)
- [ ] Review chart of accounts — add or merge as needed
- [ ] Run P&L and Balance Sheet for the quarter
- [ ] Calculate and pay estimated taxes
- [ ] Review contractor payments for 1099 threshold

### Annually (half day, January)
- [ ] Full year reconciliation
- [ ] Prepare 1099s for contractors
- [ ] Generate annual P&L and Balance Sheet
- [ ] Package tax documents for CPA
- [ ] Review and update chart of accounts for new year
```

---

## Phase 4: Deliverable

```
## Bookkeeping System Setup Complete

### Delivered
1. Chart of accounts (customized for your business)
2. Categorization guide
3. Reconciliation schedule
4. Key rules and procedures

### Next Steps
- [ ] Enter chart of accounts into [software]
- [ ] Connect bank and credit card feeds
- [ ] Set up recurring transactions for regular expenses
- [ ] Schedule weekly 15-minute bookkeeping sessions
- [ ] Set monthly reconciliation reminder for the 5th of each month
```

---

## Example: Solo Consultant

**Accounts needed:** 15 total (2 bank, 1 credit card, 1 AR, 3 equity, 2 revenue, 6 expense). No COGS accounts needed — time is the product. No payroll — owner's draw only. Key rule: owner's draw is NOT an expense.

---

## Anti-Patterns

- **Too many accounts** — a solopreneur does not need 50 expense categories. Start with 10-15 and add only when you need reporting granularity.
- **Mixing personal and business** — one business bank account, one business credit card. No exceptions.
- **Categorizing owner's draw as an expense** — owner's pay is equity, not an expense. This mistake inflates expenses and understates profit.
- **Reconciling once a year** — monthly reconciliation catches errors early. Annual reconciliation turns into a forensic investigation.
- **Ignoring accounts receivable** — if you invoice clients, track what is outstanding. Money billed is not money received.

---

## Recovery

- **Messy existing books:** Start clean from the current month. Go back and fix previous months only if tax filing requires it — otherwise, focus forward.
- **No bookkeeping software:** Set up QuickBooks Online, Wave (free), or Xero. Any of these work for small businesses. Do not use spreadsheets beyond the first year.
- **Mixed personal and business accounts:** Open a business bank account immediately. Move all business transactions there. Separate historical transactions as best you can.
- **Behind on reconciliation:** Block 2-4 hours and reconcile month by month starting from the last clean month. Do not skip ahead.

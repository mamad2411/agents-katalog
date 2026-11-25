---
name: tax-prep-checklist
description: "Creates tax preparation checklists organized by entity type with document gathering and deadline tracking. Use when preparing for business tax filing season."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Tax Prep Checklist

## When to Use This Skill

Use this skill when you need to:
- Organize documents and information for business tax filing
- Create a comprehensive tax prep checklist customized to your entity type
- Track tax deadlines and filing requirements
- Prepare for a meeting with your accountant or tax preparer

**DO NOT** use this skill for tax advice, tax return preparation, or legal tax strategy. This is a document organization and preparation tool only. Always consult a qualified tax professional.

---

## Core Principle

TAX PREP IS A DOCUMENT-GATHERING EXERCISE — THE CHECKLIST ENSURES NOTHING IS MISSED SO YOUR ACCOUNTANT CAN DO THEIR JOB EFFICIENTLY AND YOU PAY ONLY WHAT YOU OWE.

---

## Phase 1: Business Profile

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Entity type** | "What is your business entity? (sole prop, LLC, S-corp, C-corp, partnership)" | Sole proprietorship / Single-member LLC |
| **Tax year** | "What tax year are you preparing for?" | Previous calendar year |
| **Revenue range** | "Approximate annual revenue?" | Under $250K |
| **Has employees** | "Do you have W-2 employees?" | No — contractors only |
| **State(s)** | "Which state(s) do you operate in?" | Single state |
| **Accountant** | "Do you have a CPA or tax preparer?" | Yes |

**GATE: Do not proceed without entity type and tax year.**

---

## Phase 2: Document Checklist

### Universal Documents (All Entity Types)

```
## Tax Prep Checklist: [Tax Year]

### Business Information
- [ ] EIN (Employer Identification Number)
- [ ] Business legal name and DBA
- [ ] Business address
- [ ] Date business started (if new)
- [ ] Prior year tax return (for reference)

### Income Documentation
- [ ] Total gross revenue for the year
- [ ] 1099-NEC forms received (for contract work performed)
- [ ] 1099-K forms (payment processor reports — PayPal, Stripe, etc.)
- [ ] 1099-MISC forms received
- [ ] Other income documentation (interest, investments, rental)
- [ ] Monthly/annual revenue reports from bookkeeping system

### Expense Documentation
- [ ] Bank statements (all business accounts, all 12 months)
- [ ] Credit card statements (all business cards, all 12 months)
- [ ] Categorized expense report from bookkeeping software
- [ ] Receipts for purchases over $75 (or your accountant's threshold)
- [ ] Vehicle mileage log (if claiming business mileage)
- [ ] Home office measurements and total home square footage (if applicable)
```

### Entity-Specific Documents

**Sole Proprietorship / Single-Member LLC:**
```
- [ ] Schedule C categories prepared (income, COGS, expenses)
- [ ] Estimated tax payment records (4 quarterly payments)
- [ ] Self-employment tax calculation
- [ ] Health insurance premium records (for SE health deduction)
- [ ] Retirement contributions (SEP IRA, Solo 401k)
```

**S-Corp / LLC taxed as S-Corp:**
```
- [ ] Officer compensation (W-2 for yourself)
- [ ] Shareholder distribution records
- [ ] Payroll tax filings (Form 941 quarterly)
- [ ] Form W-3 (annual wage summary)
- [ ] Reasonable compensation documentation
- [ ] Shareholder loan documentation (if applicable)
```

**Partnership / Multi-Member LLC:**
```
- [ ] Partnership agreement (for profit/loss allocation %)
- [ ] Capital account records for each partner
- [ ] Partner contribution and distribution records
- [ ] Schedule K-1 preparation data
```

### Contractor and Employee Documents

```
### If You Paid Contractors
- [ ] 1099-NEC forms issued to contractors paid $600+
- [ ] W-9 forms on file for all contractors
- [ ] Contractor payment records

### If You Have Employees
- [ ] W-2 forms issued to all employees
- [ ] Payroll tax deposits (federal and state)
- [ ] Form 940 (FUTA)
- [ ] Form 941 (quarterly payroll tax returns)
- [ ] State unemployment tax filings
- [ ] Workers' compensation records
```

---

## Phase 3: Deduction Maximizer

### Commonly Missed Deductions Checklist

```
## Deductions to Review

- [ ] Home office deduction (simplified: $5/sq ft up to 300 sq ft)
- [ ] Business mileage (check current IRS rate)
- [ ] Health insurance premiums (self-employed deduction)
- [ ] Retirement contributions (SEP IRA, Solo 401k)
- [ ] Business insurance premiums
- [ ] Professional development and education
- [ ] Software and subscriptions (monthly tools add up)
- [ ] Phone and internet (business use percentage)
- [ ] Business meals (50% deductible — must document who + business purpose)
- [ ] Professional services (accountant, lawyer, coach fees)
- [ ] Bank and merchant fees
- [ ] Depreciation on equipment and assets
- [ ] Business travel expenses
- [ ] Startup costs (if first year — up to $5,000 immediately deductible)
```

---

## Phase 4: Deadline Tracker and Delivery

### Key Deadlines

```
## Tax Deadlines: [Tax Year]

| Form | Entity Type | Deadline | Extension Deadline |
|------|------------|----------|-------------------|
| Schedule C (with 1040) | Sole Prop | April 15 | October 15 |
| Form 1065 | Partnership | March 15 | September 15 |
| Form 1120-S | S-Corp | March 15 | September 15 |
| Form 1120 | C-Corp | April 15 | October 15 |
| 1099-NEC (to contractors) | All | January 31 | No extension |
| W-2 (to employees) | All | January 31 | No extension |

### Estimated Tax Payments (Next Year)
| Quarter | Period | Due Date |
|---------|--------|----------|
| Q1 | Jan-Mar | April 15 |
| Q2 | Apr-May | June 15 |
| Q3 | Jun-Aug | September 15 |
| Q4 | Sep-Dec | January 15 |
```

### Accountant Prep Package

Organize all documents into this structure for your tax preparer:

```
tax-prep-[YEAR]/
├── income/
├── expenses/
├── contractor-docs/
├── payroll/ (if applicable)
├── prior-year-return/
└── notes-and-questions.md
```

---

## Example: Solopreneur with LLC ($85K Revenue)

**Entity:** Single-member LLC (taxed as sole prop)
**Key items:** Schedule C, quarterly estimated tax payments ($5,200 paid), home office ($1,500 deduction), mileage (4,200 business miles), SEP IRA contribution ($8,500), health insurance premiums ($6,000).

**Missing:** No mileage log — recommend reconstructing from calendar entries. No W-9 for contractor paid $2,400 — under $600 threshold per contractor, 1099 not required.

---

## Anti-Patterns

- **Treating this as tax advice** — this is a preparation and organization tool. Always defer to a qualified tax professional for tax strategy.
- **Waiting until April** — start gathering documents in January. The earlier you start, the more deductions you will find.
- **Mixing personal and business expenses** — only include business expenses. If accounts are mixed, separate them before handing off to your CPA.
- **Ignoring estimated tax payments** — solopreneurs who skip quarterly payments face penalties. Track all four payments.
- **Shoebox of receipts** — categorized digital records save your accountant time (and your bill). Organize before the handoff.

---

## Recovery

- **No bookkeeping system:** Walk through bank and credit card statements month by month. Categorize expenses into Schedule C categories. Recommend setting up bookkeeping for next year.
- **Missing receipts:** Most deductions under $75 do not require receipts — bank/credit card statements suffice. For larger purchases, check email for digital receipts.
- **Missed quarterly estimated payments:** Calculate the underpayment penalty exposure and include extra funds in the final payment. Set up autopay for next year.
- **First year in business:** Flag startup cost deductions, ensure proper entity formation docs are on file, and set up quarterly estimated payments going forward.

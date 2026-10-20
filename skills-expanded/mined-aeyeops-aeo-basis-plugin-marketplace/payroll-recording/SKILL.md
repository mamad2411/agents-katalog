---
name: payroll-recording
description: >
  Contains verified payroll journal entry templates, GL account mapping tables (6xxx
  expenses, 2xxx liabilities), and Form 941/940 liability reconciliation procedures
  that produce more precise answers than reasoning from general training alone. Gross
  wages, employer FICA/FUTA/SUTA, withholdings, garnishments, tax deposit entries,
  accrual wage splits, net-pay-only error correction, ADP/Gusto/Paychex provider
  integration. Consult when posting payroll to the ledger, e.g. "how do I record the
  full payroll journal entry" or "the payroll liability balance keeps growing."
---

# Payroll Recording

Record the full economic picture of each payroll run — gross compensation, employer-side
taxes, employee withholdings, benefit costs, and net cash outflow — as journal entries
in the general ledger. Payroll is typically the largest expense for service businesses;
recording only the net check amount is the most common and most damaging bookkeeping error.

## Standard Payroll Journal Entry

Each pay run produces a single balanced journal entry. The pattern is the same regardless
of provider; only the data source changes.

**Debit side (expenses):**
- Payroll Expense: Gross Wages — total compensation before deductions
- Payroll Expense: Employer FICA — employer's 6.2% Social Security + 1.45% Medicare match
- Payroll Expense: FUTA — federal unemployment, 0.6% on first $7,000 per employee
- Payroll Expense: SUTA — state unemployment, rate varies by state and experience rating
- Payroll Expense: Employer Benefits — employer portion of health, dental, vision, 401(k) match

**Credit side (liabilities and cash):**
- Payroll Liabilities: Federal Income Tax — FIT withheld from employees
- Payroll Liabilities: Employee FICA — employee's 6.2% SS + 1.45% Medicare
- Payroll Liabilities: Employer FICA — employer match amount, until deposited
- Payroll Liabilities: State Income Tax — state withholding
- Payroll Liabilities: FUTA — until deposited
- Payroll Liabilities: SUTA — until deposited
- Payroll Liabilities: Benefits Payable — employee and employer benefit amounts
- Payroll Liabilities: Garnishments — court-ordered withholdings
- Checking Account — net pay disbursed to employees

**Balance check**: total expense debits (gross wages + employer taxes + employer benefits)
must equal total credits (all liabilities + net pay cash). The checking account credit
equals net pay only, never gross wages.

## Tax Deposit Entry

When payroll taxes are remitted to the IRS or state agency, debit the specific liability
accounts and credit the checking account. Do NOT debit an expense account — the expense
was already recorded at payroll time. Double-debiting expense is a top-5 payroll error
that overstates tax expense.

Example deposit entry (federal):
- Debit: Payroll Liabilities: Federal Income Tax
- Debit: Payroll Liabilities: Employee FICA
- Debit: Payroll Liabilities: Employer FICA
- Credit: Checking Account

## GL Account Setup

### Expense Accounts (6xxx range)

- 6100 Gross Wages (split by department or type: Officers, Salaries, Hourly as needed)
- 6110 Employer FICA
- 6120 FUTA
- 6130 SUTA
- 6140 Employer Health Insurance
- 6150 Employer 401(k) Match
- 6160 Workers Compensation
- 6190 Payroll Processing Fees

Officer compensation must be in a separate account (6000 Officers) from staff wages
(6010/6100) — Form 1120 Line 12 requires officer comp reported separately from Line 13
salaries/wages.

### Liability Accounts (2xxx range)

- 2100 Federal Income Tax Payable
- 2110 Social Security Payable (or combined FICA)
- 2120 Medicare Payable (or combined FICA)
- 2130 State Withholding Payable
- 2140 FUTA Payable
- 2150 SUTA Payable
- 2160 Benefits Payable
- 2170 Garnishments Payable

Never use a single "Payroll Liabilities" account for all tax types. Separate accounts
are essential for reconciling to quarterly Form 941 and annual Form 940. If the client
has a single combined account, reclassify historical entries before the next quarterly
reconciliation.

For full numbering conventions and account taxonomy, invoke
`accounting-foundation:chart-of-accounts`.

## Accrual vs Cash Basis

### Accrual basis
- Record gross wages expense on the pay period end date (when earned)
- Record employer tax expense simultaneously
- Liabilities exist from pay period end until tax deposits and paychecks clear
- Month-end accrual required when a pay period spans two months

### Cash basis
- Record wages expense when paychecks are disbursed
- Record employer taxes when deposited
- Most cash-basis businesses still track payroll liabilities for compliance
- Simpler but can distort monthly P&L when pay dates fall unevenly across months

## Month-End Pay Period Split (Accrual Clients)

When a biweekly pay period spans month-end (e.g., Jan 20 through Feb 2):

1. Count workdays in each month — 8 of 10 workdays fall in January = 80%
2. Post accrual: Debit Wages Expense, Credit Wages Payable for the January portion (80% of gross wages and proportional employer taxes)
3. Reverse the accrual on Feb 1
4. Record the full payroll JE on the actual pay date as normal

This prevents P&L distortion at month-end. The reversal ensures no double-counting when
the real payroll posts. Invoke `bookkeeping:monthly-close` for the full close checklist
that includes payroll accrual verification.

## External Provider Integration

### Manual JE Method (ADP, Gusto, Paychex without direct integration)

1. Obtain the payroll summary report from the provider after each pay run
2. Map report fields to GL accounts — gross wages, each tax type, each deduction type, net pay
3. Create a journal entry in the accounting system dated as of the check date (cash basis) or pay period end date (accrual basis)
4. Use a consistent JE numbering scheme — e.g., `PAYROLL-2025-01-15` or `ADP-20250115`
5. Attach the payroll summary PDF to the journal entry for audit trail
6. Verify the bank clearing amount matches the net pay on the JE during bank reconciliation

### ADP RUN GL Integration

ADP RUN can export a GL file mapped to the chart of accounts:
- Map ADP GL accounts to the chart of accounts during initial setup
- Export runs as CSV or direct-post if connector is available
- Verify account mappings quarterly — ADP category changes can silently break mappings
- Always reconcile: the ADP GL export is a convenience, not a guarantee of accuracy

## Decision Logic

**Which recording method?**
- Client uses integrated payroll (provider posts directly to GL) → no manual JE needed, but reconcile quarterly to Form 941
- Client uses ADP/Gusto/Paychex with no direct ledger integration → post manual JE per pay run using the standard pattern above
- Client uses ADP with GL export → use the export but spot-check one pay run per quarter manually
- Any provider → always reconcile quarterly

**Period-end treatment?**
- Cash basis client → no accrual needed, record on pay date
- Accrual client, pay period ends within the month → no accrual needed
- Accrual client, pay period spans month-end → post workday-proportional accrual and reverse next month

**Growing payroll liability balance?**
- Compare tax deposits made to the 941 deposit schedule
- Check for missed deposits, late deposits, or recording errors
- Target: liability accounts should approach zero after all deposits for the period clear

**Small rounding difference on 941 reconciliation (<$5)?**
- Adjust to match the 941 amount; post the difference to payroll tax expense

## Payroll Liability Reconciliation

Perform quarterly at minimum, aligned with Form 941 filing.

**Quarterly process:**
1. Pull the Balance Sheet as of quarter-end — note each payroll liability account balance
2. Pull Form 941 (or the provider's quarterly summary) — note total taxes reported
3. Pull bank records — sum all tax deposits for the quarter
4. Reconcile: Beginning liability + Current quarter taxes - Deposits = Ending liability
5. Investigate differences — common causes: timing (deposit made in Q2 for Q1 liability), omitted tax type in the JE, SUTA rate change mid-quarter, cumulative rounding across pay periods

**Annual reconciliation (year-end):**
- Total wages per GL to total wages per W-2s/W-3
- Total FICA per GL to Form 941 annual total
- Total FUTA per GL to Form 940
- Total state withholding per GL to state quarterly returns

For officer compensation context (reasonable comp, Form 1120 Line 12), invoke
`accounting-foundation:entity-profile`.

## Common Errors and Fixes

- **Recording net pay as wages expense** — understates expenses by 25-35% and loses all liability tracking. Fix: post the full JE with gross wages, all taxes, and deductions.
- **Categorizing bank feed payroll debit as expense** — same effect as above; the bank feed entry has no detail. Fix: delete the bank feed entry and post the proper JE.
- **Single payroll liability account** — cannot reconcile to tax returns by type. Fix: create separate sub-accounts and reclassify historical entries.
- **Debiting expense when paying taxes** — double-counts the expense (once at payroll, once at deposit). Fix: debit the liability account when remitting taxes, never the expense account.
- **Missing employer FICA** — understates tax expense by ~7.65% of wages. Fix: always include the employer match as a separate expense debit.
- **Omitting payroll processing fees** — bank shows a debit with no GL match. Fix: post fees to a dedicated processing fee expense account (6190).
- **Not accruing wages at month-end** — P&L distorted when pay periods span months. Fix: post the workday-proportional accrual JE and reverse on the first day of the next month.

For platform-specific execution, invoke `qbo-integration:qbo-bookkeeping`.

## Supporting References

- `references/payroll-recording.md` — Full payroll recording procedures including the standard JE pattern with account-level detail, FICA/FUTA/SUTA rate references, accrual vs cash basis treatment, external provider integration workflows (ADP, Gusto, Paychex), quarterly and annual liability reconciliation procedures, and common error patterns with fixes. Read when you need the detailed account tables, tax deposit entry mechanics, or provider-specific setup guidance.

## Cross-Plugin References

For GL account structure and numbering:
- Invoke `accounting-foundation:chart-of-accounts` for account taxonomy, numbering ranges, and Form 1120 tax-line mapping (officer comp Line 12 vs wages Line 13)

For entity-level context:
- Invoke `accounting-foundation:entity-profile` for officer compensation context, reasonable comp considerations, and corporate entity details

For period-end coordination:
- Invoke `bookkeeping:monthly-close` for the close checklist that includes payroll accrual verification and liability balance review

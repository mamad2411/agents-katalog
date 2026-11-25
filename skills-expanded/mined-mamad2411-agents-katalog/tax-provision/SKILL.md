---
name: tax-provision
description: >
  Contains verified DTA/DTL item tables with typical sources (MACRS, accrued liabilities,
  NOL/credit carryforwards, Section 174 capitalization), valuation allowance evidence
  framework (positive/negative weighting, 3-year cumulative loss test), and uncertain tax
  position two-step recognition/measurement process with cumulative probability examples.
  ASC 740 income tax provision, current/deferred tax expense, temporary differences,
  enacted rate measurement, ETR reconciliation, FIN 48, EAETR quarterly methodology,
  ASC 740-270 discrete items, ASU 2015-17 balance sheet classification. Consult when
  computing income tax expense for a C-corp, measuring or remeasuring deferred tax assets
  and liabilities after a rate change, assessing whether a valuation allowance is needed,
  reconciling effective vs statutory tax rate, evaluating uncertain tax positions,
  calculating quarterly interim provisions, posting provision journal entries, preparing
  tax footnote disclosures, or reviewing a target's tax provision for M&A due diligence.
---

# Tax Provision

Operational skill for computing, recording, and disclosing income tax expense under
ASC 740 for C-corporations. The provision has two components: current tax expense
(taxes payable for the year based on taxable income) and deferred tax expense (future
tax consequences of temporary differences between book and tax basis). Total income
tax expense = current + deferred.

## Provision Workflow

Follow these steps in sequence. Each step depends on the prior step's output.

1. **Identify temporary differences** -- compare book basis to tax basis for every asset and liability
2. **Measure DTA/DTL** -- multiply each difference by the enacted rate expected at reversal
3. **Assess valuation allowance** -- determine whether DTAs are more likely than not to be realized
4. **Compute current tax expense** -- taxable income x enacted rate, less credits
5. **Reconcile the effective tax rate** -- explain every basis-point gap between statutory and effective rates
6. **Evaluate uncertain tax positions** -- apply the two-step recognition/measurement framework
7. **Post journal entries** -- record current and deferred components in the GL
8. **Prepare disclosures** -- rate reconciliation, DTA/DTL detail, UTP rollforward

## Step 1 -- Identify Temporary Differences

Compare the book carrying amount (financial statements) to the tax basis (tax return)
of every asset and liability. Classify each difference as taxable or deductible.

**Taxable temporary differences (create DTL)** -- book basis of asset exceeds tax
basis, OR book basis of liability is less than tax basis. These produce taxable amounts
in future years when the asset is recovered or the liability settles.

- MACRS depreciation exceeding book straight-line (most common C-corp DTL)
- Installment sale receivables (gain recognized for book, deferred for tax)
- Prepaid expenses deducted for tax when paid, amortized for book

**Deductible temporary differences (create DTA)** -- book basis of asset is less than
tax basis, OR book basis of liability exceeds tax basis. These produce deductible
amounts in future years.

- Accrued liabilities not yet deductible (warranties, litigation reserves, vacation)
- Bad debt reserves (book allowance method vs tax specific charge-off)
- NOL carryforwards (deductible in future years when utilized)
- Capital loss carryforwards (5-year carryforward for C-corps)
- Tax credit carryforwards (R&D, FTC, general business credits)
- Section 174 capitalization (R&D costs amortized for tax, expensed for book)
- Deferred revenue taxable on receipt (IRC 451(c) advance payments)
- Section 263A UNICAP adjustments (additional capitalized inventory costs)

**Permanent differences** do not create DTA/DTL -- they affect only the rate
reconciliation. Common permanent items: 50% meals disallowance (IRC 274), 100%
entertainment disallowance post-TCJA, penalties/fines (IRC 162(f)), federal income
tax expense, tax-exempt interest, dividends received deduction (IRC 243), officer
life insurance premiums (IRC 264).

## Step 2 -- Measure DTA and DTL

Multiply each temporary difference by the **enacted tax rate** expected to apply when
the difference reverses.

**Post-TCJA federal rate**: 21% flat (no graduated brackets for C-corps). State rate
varies by jurisdiction (Florida: 5.5% on apportioned income over $50,000 exemption).
Compute a combined rate as federal + state net of federal benefit, or use a blended
rate for multi-state entities.

**Rate change rule**: When a rate change is enacted, remeasure all existing DTA/DTL at
the new rate in the period of enactment. The adjustment flows through income tax
expense that period. Do not use proposed but unenacted rates.

**Scheduling**: For flat-rate jurisdictions (federal post-TCJA), scheduling is
unnecessary -- all differences reverse at 21%. For graduated-rate or rate-change
jurisdictions, schedule each difference's reversal by year to apply the correct rate.

## Step 3 -- Valuation Allowance

Assess whether it is "more likely than not" (>50% likelihood) that some or all of
the DTA will not be realized. If so, record a valuation allowance contra-asset to
reduce the DTA to the realizable amount.

**Positive evidence** (supports realization):
- Existing contracts or firm backlog producing future taxable income
- Appreciated asset values exceeding tax basis (built-in gains)
- History of strong, consistent earnings
- Reversing taxable temporary differences generating income in the carryforward period
- Prudent and feasible tax planning strategies

**Negative evidence** (weighs against realization):
- Cumulative losses in recent years (3-year cumulative loss is significant negative evidence per ASC 740-10-30-21)
- History of NOL or credit carryforwards expiring unused
- Unsettled circumstances adversely affecting future operations
- Brief carryback/carryforward period limiting utilization window

**Weighting**: Objectively verifiable evidence (contracts, historical earnings) receives
greater weight than projections. Negative evidence generally requires proportionally
stronger positive evidence to overcome.

This is one of the most significant judgment areas in financial reporting. It directly
impacts net income and carries restatement risk. Document the analysis regardless of
the conclusion reached.

## Step 4 -- Current Tax Expense

Current tax expense = taxable income x enacted rate, adjusted for credits.

Start the provision workpaper with book income, adjust for permanent and temporary
differences to arrive at taxable income, then apply the statutory rate.

**Federal**: Taxable income x 21%
**State**: State-apportioned taxable income x state rate
**Credits**: R&D credit (IRC 41), foreign tax credit (IRC 901), general business credits -- reduce current tax payable dollar-for-dollar

Invoke `tax-prep:form-1120-prep` for the full book-to-taxable-income reconciliation
workflow and Form 1120 Schedule J tax computation.

## Step 5 -- Effective Tax Rate Reconciliation

Reconcile the statutory rate (21% federal) to the effective tax rate (total income
tax expense / pre-tax book income). Each item explains a basis-point difference.

**Common reconciliation items**:
- State income taxes, net of federal benefit: state rate x (1 - federal rate)
- Permanent addbacks: nondeductible meals (50%), penalties, political contributions, officer life insurance
- Permanent exclusions: tax-exempt interest, life insurance proceeds, DRD
- Tax credits: R&D, FTC (reduce effective rate below statutory)
- Rate changes: DTA/DTL remeasurement when enacted rates change
- Valuation allowance changes: VA increase raises ETR; VA release lowers ETR
- Return-to-provision adjustments: true-up when filed return differs from estimate
- Prior year adjustments: audit settlements, amended returns, refund claims

**Disclosure rule**: Each item exceeding 5% of the statutory rate amount must be
separately disclosed (ASC 740-10-50-12). The rate reconciliation is closely
scrutinized by auditors.

## Step 6 -- Uncertain Tax Positions (ASC 740-10-25)

Formerly FIN 48. Apply a two-step process to every tax position taken or expected to
be taken on a return.

**Step A -- Recognition**: Does the position meet the "more likely than not"
threshold (>50% sustained on examination) based solely on technical merits? Consider
tax law, regulations, case law, IRS rulings, and experience with similar positions.
If yes: recognize the benefit. If no: record a liability for the full tax effect.

**Step B -- Measurement**: For recognized positions, measure at the largest amount
with >50% cumulative probability of being realized upon ultimate settlement. List
possible outcomes, assign probabilities, find the largest amount where cumulative
probability exceeds 50%.

**Interest and penalties**: ASC 740-10-45-25 permits a policy election to classify
as income tax expense or a separate line item. The election must be disclosed and
applied consistently.

**UTP disclosures** (ASC 740-10-50):
- Tabular rollforward of unrecognized tax benefits (beginning balance, additions, reductions, settlements, statute lapse)
- Positions that could change within 12 months
- Cumulative interest and penalties recognized
- Tax years open to examination by major jurisdiction

## Quarterly Provision -- ASC 740-270

**Estimated Annual Effective Tax Rate (EAETR)**: At each interim period, estimate
the full-year ETR and apply it to year-to-date ordinary income. The EAETR includes
estimated annual pre-tax income, anticipated permanent differences, projected credits,
and expected VA changes related to ordinary income.

**Discrete items** -- recognized entirely in the quarter they occur, not spread
through EAETR: enacted law changes, VA judgment changes, return-to-provision true-ups,
unusual/infrequent items, UTP settlements.

**Interim formula**: Quarter tax expense = (YTD ordinary income x EAETR) - tax
expense recognized in prior quarters + current quarter discrete items.

## Common C-Corp DTA/DTL Items

**DTL items**:
- MACRS depreciation exceeding book depreciation (fixed assets)
- Prepaid expenses deducted for tax under 12-month rule (prepayments)

**DTA items**:
- Accrued expenses not yet deductible (warranty, vacation, litigation reserves)
- NOL carryforward (prior year losses)
- Capital loss carryforward (net capital losses, 5-year CF)
- Bad debt reserve (allowance for doubtful accounts)
- Section 263A UNICAP adjustment (additional capitalized inventory costs)
- Tax credit carryforward (R&D, FTC, general business credits)
- Deferred revenue taxable on receipt (IRC 451(c) advance payments)
- Section 174 capitalization (R&D costs amortized for tax, expensed for book)

Invoke `tax-prep:nol-tracking` for NOL deferred tax asset carryforward tracking,
utilization schedules, and Section 382 limitation analysis.

## Journal Entries

**Current provision**: Debit Income Tax Expense (9000s/9100s), credit Income Tax
Payable. Split federal and state into separate entries for clarity.

**Deferred provision**: Debit/credit Deferred Tax Asset or Deferred Tax Liability
with corresponding debit/credit to Deferred Income Tax Expense (9200s). Net DTA
increase = deferred tax benefit (reduces total expense). Net DTL increase = deferred
tax expense (increases total expense).

**Valuation allowance**: Credit Valuation Allowance (contra-asset to DTA), debit
Income Tax Expense.

**Balance sheet classification**: All deferred tax is noncurrent under ASU 2015-17
(effective for all entities 2017+). Present net DTA or net DTL per jurisdiction on
the balance sheet -- do not offset across jurisdictions.

**Quarterly entries**: Post adjusting entries each quarter using the EAETR and true
up at year-end when the return is filed. The income tax expense per GL should tie
to the provision workpaper; any difference indicates a posting error.

Invoke `accounting-foundation:financial-statements` for GAAP balance sheet and P&L
presentation requirements for income tax accounts.

## Decision Points

1. **Is a valuation allowance needed?** Weigh positive vs negative evidence; 3-year cumulative loss is a strong indicator. Document analysis regardless of conclusion.
2. **Which rate for measurement?** Enacted rate expected at reversal. Federal post-TCJA: 21%. Do not use proposed-but-unenacted rates.
3. **Does an uncertain tax position exist?** Any position with debatable technical merits requires evaluation under the two-step process.
4. **More likely than not?** Below 50% = no benefit recognized, full liability accrued.
5. **State tax handling?** Compute state DTA/DTL separately or as blended rate depending on complexity and materiality.
6. **Quarterly vs annual?** Public companies must compute quarterly via EAETR. Private companies may compute annually but quarterly is best practice.

## Supporting References

Read these for deeper detail:

- `references/tax-provision-asc740.md` -- Full ASC 740 operational reference. Covers all six provision steps with C-corp examples, DTA/DTL item tables with typical sources, valuation allowance evidence framework (positive/negative weighting, 3-year cumulative loss test), rate reconciliation line items, uncertain tax position two-step process with cumulative probability measurement, quarterly EAETR methodology with discrete item rules, accounting system integration notes for posting provision entries, and authoritative ASC/IRC citations. Read when you need the detailed DTA/DTL item lookup table, the valuation allowance evidence checklist, the UTP disclosure requirements, or the quarterly interim calculation formula.

## Cross-Plugin References

For tax return computation details:
- Invoke `tax-prep:form-1120-prep` for book-to-taxable-income reconciliation, M-1/M-3 adjustments, Schedule J tax computation, and permanent/temporary difference identification that feeds the provision
- Invoke `tax-prep:tax-planning` for tax planning strategies (timing of deductions, credit optimization, entity structuring) that affect provision estimates and valuation allowance assessment
- Invoke `tax-prep:nol-tracking` for NOL carryforward schedules, utilization projections, Section 382 limitations, and DTA measurement for loss carryforwards

For GAAP presentation:
- Invoke `accounting-foundation:financial-statements` for income statement tax expense line presentation (current + deferred components), balance sheet DTA/DTL classification (noncurrent per ASU 2015-17), cash flow deferred tax add-back, and tax footnote disclosure requirements

## Cross-Plugin Consumers

- `financial-planning:financial-modeling` -- ETR drives after-tax projections in 3-statement models and scenario analysis
- `financial-planning:strategic-advisory` -- tax provision impacts M&A due diligence and capital allocation decisions
- `bookkeeping:monthly-close` -- provision journal entries are part of the adjusting entry phase
- `tax-prep:form-1120-prep` -- provision workpaper reconciles to the filed return (return-to-provision true-up)

---
name: form-1120-prep
description: >
  Contains verified GL-to-1120-line mapping tables (income Lines 1-11, deduction Lines
  12-27), permanent/temporary book-tax difference catalog with IRC citations, and
  year-by-year rule variance tables (meals, entertainment, bonus depreciation 2007-2027+).
  Taxable income computation, Schedule M-1/M-3 reconciliation, DRD, charitable 10% limit,
  Section 163(j), Schedule L balance sheet ties, officer compensation segregation, workpaper
  format, and preparer/reviewer/partner sign-off protocol. Consult when preparing a Form
  1120, mapping trial balance accounts to return lines, classifying a book-tax difference
  as permanent or temporary, debugging an M-1 that does not balance, computing the
  charitable deduction limitation or DRD ordering, checking bonus depreciation or meals
  deduction rates for a specific tax year, reconciling Schedule L to the balance sheet,
  or running the final verification checklist before filing a C-corp return.
---

# Form 1120 Preparation

End-to-end operational skill for preparing federal Form 1120 corporate income tax
returns. Synthesizes the reconciliation workflow (trial balance to return), book-tax
difference identification, and computational tools into a single preparation guide
for C-corporations.

## Preparation Workflow

The Form 1120 preparation process follows six sequential steps. Each step must be
complete before the next is reliable.

### Step 1 -- Extract and Validate the Trial Balance

Pull the year-end trial balance from the accounting system covering the full fiscal year.
The TB must include both P&L and balance sheet accounts. For platform-specific extraction
procedures, invoke `qbo-integration:qbo-reporting`.

Validation gates before proceeding:
- Period is closed -- no unposted transactions or open bank reconciliations
- Report basis matches the entity's accounting method (accrual vs cash)
- Debits equal credits (TB balances)
- Run P&L by account (not summary) for full account-level detail
- Export to spreadsheet as the workpaper foundation

### Step 2 -- Map GL Accounts to Form 1120 Lines

Every GL account must map to exactly one Form 1120 line. Multiple accounts typically
roll into a single line. Document the mapping explicitly.

**Income (Lines 1-11)**:
- Line 1a Gross receipts -- all revenue accounts (sales, service, consulting, product)
- Line 1b Returns/allowances -- sales returns, discounts
- Line 4 Dividends -- dividend income (also feeds Schedule C for DRD)
- Line 5 Interest -- bank interest, loan interest received
- Line 6 Gross rents -- rental income
- Line 7 Gross royalties -- royalty income
- Line 8 Capital gain net income -- from Schedule D
- Line 10 Other income -- miscellaneous (gain on sale, FX gains, refunds)

**Deductions (Lines 12-27)**:
- Line 12 Officer compensation -- officer salary only (must match Schedule E); segregate from total payroll
- Line 13 Salaries and wages -- non-officer employee wages
- Line 14 Repairs and maintenance
- Line 15 Bad debts -- specific charge-off method for accrual basis
- Line 16 Rents -- office rent, equipment leases
- Line 17 Taxes and licenses -- payroll taxes, state taxes, property taxes (NOT federal income tax)
- Line 18 Interest -- may require allocation between business and investment (Section 163(j) if applicable)
- Line 19 Charitable contributions -- subject to 10% of taxable income limitation; excess carries forward 5 years
- Line 20 Depreciation -- tax depreciation from Form 4562 (MACRS), not book depreciation
- Line 26 Other deductions -- remaining deductible expenses; attach itemization for amounts over $10,000

### Step 3 -- Identify and Classify Book-Tax Differences

For each GL account where the book amount differs from the tax amount, classify the
difference and quantify the adjustment. Every difference must land on Schedule M-1
(or M-3 for large corps).

**Permanent differences** (never reverse):
- Meals -- 50% nondeductible (IRC 274(k)); 100% restaurant meals in 2021-2022 only (CAA Section 210, expired)
- Entertainment -- 100% nondeductible post-TCJA (IRC 274(a))
- Penalties and fines -- fully nondeductible (IRC 162(f), expanded by TCJA Section 13306)
- Federal income tax expense -- nondeductible for C-corps
- Tax-exempt interest -- municipal bond interest excluded from taxable income (IRC 103)
- Life insurance on officers -- premiums nondeductible when corp is beneficiary (IRC 264(a)(1)); proceeds excluded (IRC 101(a))
- Political contributions -- nondeductible (IRC 162(e)(1)(B))
- Lobbying expenses -- generally nondeductible (IRC 162(e))
- DRD -- dividends received deduction: 50% (ownership <20%), 65% (20-79%), 100% (80%+ or affiliated group) per IRC 243
- Charitable contribution limitation -- deduction capped at 10% of taxable income before DRD, NOL, the contribution itself, and capital loss carryback (IRC 170(b)(2)); excess carries forward 5 years
- Officer compensation disallowance -- if IRS deems unreasonable (IRC 162(a)(1)), disallowed portion is constructive dividend

**Temporary differences** (reverse over time):
- Depreciation -- MACRS/bonus vs book straight-line (typically the largest single difference)
- Bad debt -- reserve/allowance method (book) vs specific charge-off (tax, IRC 166(a))
- Prepaid expenses -- cash-basis 12-month rule vs accrual-basis economic performance (IRC 461(h))
- Accrued liabilities -- book accruals for estimated expenses not deductible until economic performance
- Warranty reserves -- book accrual at sale vs tax deduction when paid
- Unearned revenue -- may be taxable when received under IRC 451(c) / Rev. Proc. 2004-34
- Section 263A UNICAP -- indirect costs capitalized to inventory/self-constructed assets for tax
- Capital loss carryforwards -- C-corp capital losses cannot offset ordinary income; carry back 3 / forward 5 years (IRC 1212(a))
- NOL -- see `nol-tracking` skill for utilization rules and TCJA limitations

### Step 4 -- Prepare Tax Workpapers

For each Form 1120 line, the workpaper documents:
1. GL accounts mapped to the line with individual TB balances
2. Subtotal of book amounts
3. Book-tax adjustments with description and IRC authority
4. Resulting tax amount for the return
5. Cross-reference to supporting schedules (Form 4562, Schedule D, Schedule C)

The workpaper is the audit trail -- any return line must be traceable back to the
books without re-derivation.

### Step 5 -- Reconcile via Schedule M-1 or M-3

**Threshold**: Corporations with total assets >= $10M at year-end must file Schedule M-3.
Below that threshold, Schedule M-1 is sufficient. The $10M threshold has been unchanged
since M-3 was introduced (tax years ending December 31, 2004+).

**Schedule M-1** (Lines 1-10):
- Line 1 -- Net income per books (net income from the accounting system, after federal income tax expense)
- Line 2 -- Federal income tax per books (add back)
- Line 3 -- Excess capital losses over capital gains (add back)
- Line 4 -- Income subject to tax not recorded on books (e.g., prepaid income taxable on receipt)
- Line 5 -- Expenses on books not deducted: (a) depreciation difference, (b) charitable excess, (c) meals/entertainment, (d) other (penalties, life insurance, political contributions)
- Line 6 -- Income on books not included on return: (a) tax-exempt interest, (b) life insurance proceeds, (c) other
- Line 7 -- Deductions on return not charged to books: (a) depreciation difference (tax > book), (b) charitable carryover used, (c) other (DRD, NOL deduction)
- Line 10 -- Taxable income per return (must equal Form 1120 Line 28)

If M-1 does not balance, an adjustment was missed or misclassified.

**Schedule M-3** (total assets >= $10M):
Three-part structure with four-column format forcing explicit temporary/permanent classification:
- Part I -- Financial information source and net income reconciliation
- Part II -- Income/loss items: income per books | temporary difference | permanent difference | income per return
- Part III -- Expense/deduction items: same four-column layout

### Step 6 -- Balance Sheet and Retained Earnings Reconciliation

**Schedule L** reports the corporation's balance sheet on book basis (not tax basis).
- Beginning balances must equal prior year ending balances (initial return: zeros)
- End-of-year balances must tie to the accounting system balance sheet at year-end

**Schedule M-2** reconciles retained earnings beginning-to-end:
beginning balance + net income - dividends = ending balance.
Must be consistent with Schedule L equity section and M-1 net income.

## Year-by-Year Rule Variance

Rules that change across tax years affect the magnitude of book-tax differences. Apply
the rules for the tax year under preparation.

**Meals and entertainment**:
- 2007-2017: 50% meals, 50% entertainment
- 2018-2020: 50% meals, 0% entertainment (TCJA repeal)
- 2021-2022: 50% general meals, 100% restaurant meals (CAA 2021, IRC 274(n)(2)(D)); 0% entertainment
- 2023+: 50% meals (restaurant exception expired), 0% entertainment

**Bonus depreciation phase-down** (IRC 168(k)):
- 2018-2022: 100%
- 2023: 80%
- 2024: 60%
- 2025: 40%
- 2026: 20%
- 2027+: 0%

**DPAD (Section 199)**: Available pre-2018 (up to 9% of QPAI). Repealed by TCJA for tax years beginning after December 31, 2017.

**IRC 162(f) penalties**: TCJA Section 13306 expanded to cover all government/regulatory penalties (previously ambiguous for regulatory fines).

## Taxable Income Computation

Taxable income involves a circular dependency because the charitable contribution
deduction (Line 19) is limited to 10% of taxable income computed before the contribution
deduction, DRD, and NOL carryback. Resolution:

1. Compute total income (Lines 1-11)
2. Compute all deductions except charitable (Lines 12-18, 20-26)
3. Compute preliminary taxable income = total income - non-charitable deductions
4. Charitable limit = 10% of preliminary taxable income
5. Deductible charitable = lesser of actual contributions and the 10% limit
6. Taxable income before NOL/special deductions = preliminary - deductible charitable
7. Apply DRD (Line 29b) and NOL deduction (Line 29a)
8. Final taxable income (Line 30)

For DRD, the deduction may itself be limited to a percentage of taxable income (without the DRD) unless the DRD creates or increases a loss. The 50% and 65% DRD tiers have this limitation; the 100% tier does not.

## Schedule C — Dividends Received Deduction

DRD rates are year-dependent. Apply the rates for the tax year under preparation:
- **2018+** (post-TCJA): 50% (<20% owned), 65% (20-79%), 100% (80%+/affiliated)
- **2007-2017** (pre-TCJA): 70% (<20%), 80% (20-79%), 100% (80%+)

The 50/65% tiers (or 70/80% pre-TCJA) are each limited to the SAME tier-specific
percentage of taxable income without DRD (IRC 246(b)). NOT a blanket 65% cap.
If full DRD creates/increases NOL, limitation waived (IRC 246(b)(2)). 100%
tier has no limitation.

Additional year-aware rules: §245A participation exemption (2018+ only, 100%
DRD for 10%+ owned foreign subs); AMT DRD adjustment (pre-2018 only, 75%
limit). Year-independent: 46-day holding period (IRC 246(c)); debt-financed
stock reduction (IRC 246A).

## Section 163(j) Business Interest Limitation

For tax years beginning after 2017, business interest deductions may be limited to
30% of adjusted taxable income. Small business exception: average annual gross
receipts of $29M or less for the three preceding tax years. When the limitation
applies, disallowed interest carries forward indefinitely.

## Accounting-System-to-Return Workflow

For platform-specific data extraction procedures (trial balance pulls, P&L reports,
tax-line mapping configuration), invoke `qbo-integration:qbo-reporting` and
`qbo-integration:qbo-coa`.

General workflow regardless of platform:
- Pull net income from the P&L report -- becomes M-1 Line 1 (after adding back federal income tax)
- Tag meal expense accounts to distinguish restaurant vs non-restaurant meals (relevant 2021-2022)
- Flag tax-exempt interest income accounts -- flows to M-1 Line 6(a)
- Use class or location tracking for officer comp segregation and investment activity
- Run P&L by Account and Balance Sheet as of year-end; export both as workpaper foundations

## Verification Checklist

Before the return is finalized, confirm each of these ties:

- Total income (Line 11) reconciles to P&L total revenue, adjusted for book-tax differences
- Total deductions (Line 27) reconcile to P&L total expenses, adjusted for book-tax differences
- Schedule L total assets match the accounting system balance sheet total assets
- Schedule L total liabilities and equity match the accounting system balance sheet
- Schedule L beginning balances match prior year ending balances
- M-1 Line 1 equals net income per books
- M-1 Line 10 equals Form 1120 Line 28
- M-2 ending retained earnings equals Schedule L retained earnings
- Officer compensation on Schedule E matches Line 12 and payroll records
- Charitable contribution deduction does not exceed 10% of modified taxable income

## Common Mapping Challenges

- **Officer comp segregation** -- must split from total payroll for Schedule E and Line 12. Reconcile from W-2s or payroll reports if third-party processed
- **Depreciation dual tracking** -- book depreciation on Schedule L / M-1; tax depreciation on Line 20 via Form 4562. Maintain a fixed asset register tracking both bases
- **Multiple revenue types** -- segregate dividends (Line 4), interest (Line 5), rents (Line 6), royalties (Line 7), capital gains (Line 8) into separate GL accounts. Reclassify via journal entry if commingled
- **Interest expense allocation** -- business interest to Line 18 (subject to 163(j) if applicable); investment interest limited to net investment income

## Sign-Off Protocol

1. **Preparer** completes workpapers, GL-to-line mapping, and book-tax adjustment schedule. Verifies all reconciliation checkpoints
2. **Reviewer** independently traces selected return lines back to TB and workpapers, verifies M-1 ties, confirms adjustments properly classified
3. **Partner** reviews for reasonableness, signs off on significant judgments (reasonable compensation, Section 179 elections, NOL utilization), authorizes filing

## Tax Computation Reference Patterns

Three reference architecture documents describe individual (Form 1040) tax computation
patterns. While these describe individual returns, their rate structures, bracket
mechanics, dependency resolution, provenance tracking, and policy parameter catalogs
serve as reference material when cross-checking computation logic or modeling reform
impacts on C-corp planning (officer compensation, DRD pass-through effects).

**Tax rate parameters and reform modeling** -- Policy parameter catalog (~800+ parameters
covering rates, brackets, thresholds for 2013-2035), reform modeling (dictionary-based
parameter overrides), tax function execution order, and distributional analysis tables.
The TCJA reform encodes rate changes, standard deduction increase, personal exemption
elimination, SALT cap, CTC increase, QBI deduction, and chained-CPI indexing. Useful
for understanding how tax law parameters interact and for modeling "what if" scenarios.

**Form dependency resolution** -- Dependency-solver architecture for multi-form tax
computation. Forms are modular with implicit dependency resolution (fields request other
fields, solver resolves the DAG). Supports year-specific thresholds. Relevant patterns:
form modularity via dependency graph, threshold dictionaries keyed by filing status,
and PDF filling via template overlay.

**Tax computation provenance** -- Provenance-tracked computation where every computed
value carries source, confidence, and IRS citation. Covers deterministic rules engines,
multi-state return architecture, integer-cents arithmetic to prevent floating-point
drift, PDF compilation pipeline, quality gates, and conditional form inclusion.

## Supporting References

Read these for detailed rules on specific topics:

- `references/book-tax-differences.md` -- Comprehensive catalog of permanent and temporary differences with IRC citations, Schedule M-1 line-by-line walkthrough, Schedule M-3 three-part structure, and year-by-year variance table (meals, entertainment, DPAD, bonus depreciation). Read when classifying a specific book-tax item or preparing M-1/M-3.
- `references/reconciliation-to-tax-return.md` -- Step-by-step trial-balance-to-return workflow: GL account grouping to 1120 lines (income Lines 1-11, deduction Lines 12-27), common adjustment patterns, workpaper format, Schedule L/M-2 reconciliation, verification checklist, and sign-off protocol. Read when building the GL-to-return mapping or checking reconciliation ties.
- `references/tax-rate-parameters.md` -- Tax rate parameter catalog, reform dictionary format, calculator engine pipeline, tax function execution order, and distributional analysis. Read when cross-referencing rate parameters, modeling individual tax reform impacts, or understanding bracket computation mechanics.
- `references/form-dependency-resolution.md` -- Form dependency resolution patterns: dependency solver architecture, field/input type system, threshold dictionaries, PDF filling pipeline, and supported form dependency graphs (1040 + schedules). Read when studying form dependency resolution patterns or threshold parameterization.
- `references/tax-computation-provenance.md` -- Provenance-tracked tax computation: traced value system, deterministic rules engine (compute node pattern), form fillers, multi-state return modules, PDF compilation pipeline, integer-cents arithmetic, and quality gates framework. Read when studying provenance-tracked computation, PDF form filling patterns, or multi-state return architecture.
- `references/dividends-received-deduction.md` -- Complete DRD computation algorithm: IRC 243 rate tiers with year-indexed variance table (pre-TCJA 70/80/100 and post-TCJA 50/65/100), IRC 246(b) tier-specific taxable income limitation, 246(b)(2) NOL exception, 246(c) holding period, 246A debt-financed stock reduction, IRC 245/245A foreign corporation dividends (245A is post-TCJA only), Schedule C line-by-line walkthrough, computation ordering with charitable contribution interaction, and worked examples including pre-TCJA rate comparison. Read when computing DRD, verifying Schedule C, debugging the taxable income limitation, or determining which DRD rules apply for a specific tax year.
- `references/templates/1120-federal/blank/` -- Blank Form 1120 PDFs by year (2007-2025). Use as reference when verifying line numbers, form layout, or identifying year-over-year changes.
- `references/templates/1120-federal/instructions/` -- Form 1120 instruction PDFs by year (2007-2025). Use for official IRS line-by-line guidance for a specific tax year.

## Cross-Plugin References

**accounting-foundation** (upstream data sources):
- Invoke `accounting-foundation:chart-of-accounts` for GL account taxonomy, numbering conventions, and Form 1120 tax-line mapping design
- Invoke `accounting-foundation:categorization-rules` for transaction classification rules that affect which accounts receive postings
- Invoke `accounting-foundation:entity-profile` for corporate entity details (entity type, fiscal year, ownership structure, state of incorporation)
- Invoke `accounting-foundation:financial-statements` for GAAP presentation requirements and the book-basis income that feeds M-1 Line 1

**qbo-integration** (platform workflow):
- Invoke `qbo-integration:qbo-reporting` for trial balance extraction, P&L by account, and balance sheet reports
- Invoke `qbo-integration:qbo-coa` for account structure, detail types, and tax-line mapping configuration
- Invoke `qbo-integration:qbo-audit` for tax data extraction and validation
- Invoke `qbo-integration:qbo-bookkeeping` for journal entry procedures used in book-tax adjustment entries

**bookkeeping** (prerequisite processes):
- Invoke `bookkeeping:monthly-close` for clean, closed-period financials as the starting point
- Invoke `bookkeeping:reconciliation` for bank reconciliation status verification before TB extraction
- Invoke `bookkeeping:payroll-recording` for officer compensation detail needed for Schedule E and Line 12

**tax-prep siblings** (related return components):
- Invoke `tax-prep:business-tax-schema` for Form 1120 line definitions, era routing (pre/post-TCJA), and cross-year revision topology
- Invoke `tax-prep:tax-forms` for supporting schedule preparation (Form 4562, Form 8949, Schedule D, Form 1118, Form 5472)
- Invoke `tax-prep:nol-tracking` for NOL carryforward ledger, utilization ordering, TCJA 80% limitation, and Section 382
- Invoke `tax-prep:state-returns` for state return preparation (federal taxable income is the typical state starting point)
- Invoke `tax-prep:tax-compliance` for filing deadlines, extension procedures, and penalty avoidance
- Invoke `tax-prep:e-filing` for electronic filing requirements and procedures

**financial-planning** (downstream analysis):
- Invoke `financial-planning:tax-provision` for ASC 740 income tax provision that depends on book-tax difference classification
- Invoke `financial-planning:variance-analysis` for comparing actual tax liability to budget/forecast

## Cross-Plugin Consumers

Skills that depend on form-1120-prep outputs:

- `tax-prep:state-returns` -- consumes federal taxable income as state return starting point
- `tax-prep:tax-planning` -- uses book-tax difference analysis and effective tax rate data for planning strategies
- `tax-prep:e-filing` -- consumes the assembled return for electronic filing
- `tax-prep:tax-compliance` -- references return data for compliance calendar and filing status
- `financial-planning:tax-provision` -- uses permanent/temporary difference classifications for ASC 740 provision
- `firm-operations:engagement-management` -- references return preparation status for engagement tracking
- `firm-operations:quality-compliance` -- uses the sign-off protocol and review checklist for QC workflows

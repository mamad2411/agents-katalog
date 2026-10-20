---
name: state-returns
description: >
  Contains verified nexus determination framework (physical presence, economic/factor presence
  thresholds, P.L. 86-272 protection analysis), state income tax computation walkthrough with
  year-by-year variance tables (2007-2026), and state e-filing mandate/penalty schedules.
  State corporate income tax, apportionment, single sales factor, market-based sourcing,
  multistate filing, NOL carryforward, estimated tax, voluntary disclosure, state modifications
  to federal taxable income. Consult when preparing any state corporate income tax return,
  evaluating whether a C-corporation has nexus in a state, computing apportioned state taxable
  income, determining state e-file obligations, analyzing P.L. 86-272 protection for service
  vs. tangible property companies, or researching state-specific NOL rules and conformity dates.
---

# State Returns

Operational skill for state corporate income tax return preparation, with deep coverage of
Florida F-1120 and a framework for expanding to additional states as filing obligations arise.

> **State-specific scope:** Nexus determination, apportionment concepts, P.L. 86-272, and
> the multistate filing framework are nationally applicable. The detailed return preparation
> walkthrough uses **Florida** (Form F-1120) as the reference state jurisdiction. Sections
> marked (Florida) contain state-specific content. Practitioners in other states should
> substitute their state's rules for the Florida-specific sections below.

## Nexus Determination

Nexus is the minimum connection giving a state authority to impose income tax. Evaluate
every state where the corporation has activity using three tests in order.

### Physical Presence Nexus

Any of these facts creates nexus in the state:

- Employees working in the state (including remote workers)
- Owned or leased real or personal property
- Inventory stored in the state (including third-party FBA warehouses)
- Independent contractors performing services (some states)
- Regular solicitation visits by company representatives

### Economic Nexus / Factor Presence

Post-Wayfair (2018), states increasingly apply economic nexus to income tax. The MTC
factor presence standard triggers nexus if any single factor is met:

- Property in state >= $500,000
- Payroll in state >= $500,000
- Sales sourced to state >= $500,000
- 25%+ of total property, payroll, or sales in state

States with some form of income tax economic nexus include CA, CO, CT, HI, MA, MI, NY,
OH, OR, PA, WA, and others. Each state sets its own thresholds; verify the specific
state's current law before concluding no nexus.

### P.L. 86-272 Protection

Federal law (15 USC 381-384) prohibits net income tax when the only in-state activity is
solicitation of orders for tangible personal property, where orders are sent out of state
for approval and filled/shipped from outside the state.

**Protected activities**: In-person/phone/mail solicitation for tangible personal property;
ancillary activities (advertising, carrying samples).

**Not protected** (nexus exists despite P.L. 86-272):
- Sales of services or intangibles
- Leasing tangible personal property
- Maintaining an office or warehouse in the state
- Approving or filling orders in the state
- Collecting delinquent accounts in the state
- Post-2021: Many states treat extensive web-based interactivity (cookies, app
  interactions, marketplace facilitation) as exceeding solicitation per MTC revised guidance

**For service-only corporations**: P.L. 86-272 provides zero protection. Nexus is
determined solely by physical presence and factor presence tests.

### Nexus Evaluation Workflow

1. List every state with any corporate activity (employees, property, sales, contractors)
2. For each state, apply physical presence test
3. If no physical presence, apply the state's economic nexus thresholds
4. If nexus exists, check P.L. 86-272 — only protects tangible personal property sales
5. Result: list of states where a return must be filed

## Florida Corporate Income Tax (Florida — Form F-1120)

### Filing Obligation

Every corporation with Florida nexus must file Form F-1120 annually if federal taxable
income (plus Florida additions) exceeds $50,000. This includes C-corporations, LLCs taxed
as corporations, tax-exempt organizations with UBTI, banks, and certain partnerships with
corporate members. A return is required even if no tax is due.

### Tax Rate and Exemption

- **Standard rate**: 5.5% of Florida taxable income
- **Exemption**: $50,000 (not a deduction; income up to $50,000 is exempt)
- **No personal income tax**: Florida taxes only corporate income

Historical rate changes:
- 2019-2020: 4.458% (HB 7127, TCJA revenue-neutrality adjustment)
- 2021: 3.535% (SB 50, temporary reduction)
- 2022-present: 5.5% (temporary reductions sunset)

### Computing Florida Taxable Income (Florida)

1. **Start with federal taxable income** (Form 1120, Line 30, before NOL and special deductions)
2. **Add Florida additions** — FL tax-exempt interest, related-party intangible expenses subject to addback
3. **Subtract Florida subtractions** — FL NOL deduction, certain dividend adjustments
4. **Apply apportionment factor** (multistate corporations only)
5. **Subtract $50,000 exemption**
6. **Apply tax rate** to the result

This computation depends on a completed federal Form 1120. The federal return must be
finalized first; invoke `tax-prep:form-1120-prep` if the federal return is not yet complete.

### Apportionment (Florida)

Florida uses a **single sales factor** for tax years beginning on or after January 1, 2019.
Prior to 2019, Florida used a three-factor formula with double-weighted sales (25% property,
25% payroll, 50% sales).

**Sales factor**: Florida sales / Total sales everywhere

**Market-based sourcing** for services: Revenue is sourced to the state where the benefit
of the service is received, not where it is performed.

**No throwback rule**: Sales not taxed by any other state are excluded from the Florida
numerator (unlike throwback states where they would be added back).

**No combined/unitary reporting**: Each corporation files separately unless electing
consolidated.

### Florida NOL Rules (Florida)

Florida maintains a separate NOL carryforward schedule distinct from the federal NOL.

- **Florida NOL** = the apportioned loss in a given year (after Florida modifications and apportionment)
- **Post-2017 NOLs**: Indefinite carryforward, subject to 80% of Florida taxable income limitation (conforming to TCJA)
- **Pre-2018 NOLs**: 20-year carryforward
- **No CARES Act carryback**: Florida did not conform to the 5-year carryback for 2018-2020 NOLs
- Track Florida NOLs separately from federal NOLs; invoke `tax-prep:nol-tracking` for the federal NOL ledger

### Florida Estimated Tax (Florida)

- Required when expected FL tax liability exceeds **$2,500**
- Quarterly payments using Form F-1120ES, aligned with federal estimated payment schedule
- Underpayment penalty: **12% per annum** on the underpayment amount
- Electronic payment required if the corporation meets the e-file mandate threshold

### Filing Deadlines and Extensions

**Due date**: The later of the standard Florida deadline OR 15 days after the federal due date.
- June 30 year-end: 4th month following close
- All other year-ends: 5th month following close
- Calendar-year C-corps: Federal due April 15; Florida due April 30 or May 1 (whichever is later)

**Extensions**: Form F-7004 grants a 6-month extension (7 months for June 30 fiscal year-ends). An extension does not extend the time to pay; tentative tax must accompany the request.

**Late filing penalties**:
- With tax due: 10% per month (or fraction), up to 50% maximum
- No tax due: $50 per month, up to $300 maximum
- Non-electronic filing when required: $500 or 5% of tax due, whichever is greater

### Florida IRC Conformity (Florida)

Florida piggybacks on the IRC as of January 1 of the current tax year (rolling conformity).
Key non-conformities:
- No CARES Act NOL carryback
- Own addback rules for related-party intangible expenses
- Bonus depreciation conformity has varied by year; check the year-specific conformity date

## E-Filing Requirements (Florida DOR)

### E-File Mandate

Electronic filing is required if either condition is met:
- Paid **$5,000 or more** in FL corporate income tax during the prior state fiscal year (July 1 - June 30)
- Required to e-file the **federal** income tax return (federal threshold dropped to 10 returns in 2024 per T.D. 9972)

### Filing Method: IRS MeF

The primary channel for F-1120 is the federal MeF (Modernized e-File) Fed/State program.
Federal and Florida returns can be submitted together in a single MeF transmission through
IRS- and FL DOR-approved software vendors.

### Florida eServices Portal (Florida)

Used for supplemental functions: estimated tax payments (F-1120ES), extensions (F-7004),
account management, tax clearance letters. Available 24/7 Monday-Saturday; Sunday
maintenance window. Enrollment required; allow 3 business days for new application
processing.

### Payment Methods

- **EFT/ACH** (required if meeting e-file mandate): Initiate by 5:00 PM ET on the business day before due date
- MeF software vendor payment
- Direct enrollment with FL DOR
- Credit card through authorized processors

### Amended Returns

Amended F-1120 can be e-filed through MeF. If the original was required to be e-filed,
the amendment must also be e-filed.

## Multistate Filing Considerations

- **Combined reporting**: Florida does not require it. Each entity files separately.
- **Throwback rule**: Florida has none. Nowhere sales are excluded from the FL numerator.
- **P.L. 86-272**: Florida respects it for tangible personal property sales.
- **Voluntary disclosure**: FL DOR offers a voluntary disclosure program reducing lookback to 3 years and waiving penalties for corporations that should have been filing.

## Year-by-Year Variance Summary

For detailed year-by-year tables covering rate, exemption, apportionment formula, NOL
rules, and IRC conformity date, consult the reference files below. Key inflection points:

- **2012**: Exemption increased from $5,000 to $50,000 (HB 7087)
- **2019**: Single sales factor adopted (replacing three-factor double-weighted sales)
- **2019-2020**: Rate reduced to 4.458% (TCJA revenue neutrality)
- **2021**: Rate reduced to 3.535% (SB 50, temporary)
- **2022**: Rate reverts to 5.5%
- **2024**: Federal e-file threshold drops to 10 returns (T.D. 9972), triggering FL e-file mandate for more corporations

## Decision Workflow: State Return Preparation

1. **Run nexus evaluation** (see Nexus Evaluation Workflow above)
2. **For each filing state**, gather: federal taxable income, state-specific additions/subtractions, apportionment factors
3. **Compute apportioned income** using the state's formula (Florida: single sales factor post-2018)
4. **Apply state exemption** ($50,000 for Florida)
5. **Compute tax** and compare to estimated payments made
6. **Check e-file mandate** and select filing method
7. **Prepare return** using approved software through MeF
8. **File and confirm** acknowledgment

## Supporting References

Read these for detailed lookup tables, full year-by-year variance data, and authoritative
citations:

- `references/state-nexus.md` — Full nexus determination framework: physical presence
  tests, economic nexus thresholds (MTC factor presence standard), P.L. 86-272 analysis,
  Florida corporate income tax computation walkthrough, apportionment formula details,
  Florida NOL rules with year-by-year variance table (2007-2026), multistate filing
  considerations. Read when performing a nexus evaluation, computing Florida taxable income,
  or researching year-specific FL rules.

- `references/florida-e-filing.md` — Florida DOR electronic filing: e-file mandate
  thresholds, MeF Fed/State filing workflow, eServices portal capabilities, payment
  methods and timing requirements, extension procedures (F-7004), estimated tax (F-1120ES),
  amended return e-filing, penalty schedule (late filing, late payment, non-electronic
  filing), account registration. Read when determining e-file obligations, setting up
  electronic payments, or handling Florida DOR correspondence.

- `references/templates/1120-florida/` — Blank Florida Form F-1120 PDFs and corresponding
  instruction PDFs organized by tax year (2007-2025). Subdirectories: `blank/` contains
  the form PDFs; `instructions/` contains the instruction PDFs. Use these as authoritative
  references for form field layout and line-by-line completion guidance for a specific tax
  year. Note: Some years have variant filenames (e.g., `f1120--2017-from-2016.pdf`,
  `f1120--2020-from-2019.pdf`) indicating the form was carried forward from a prior year.

## Cross-Plugin References

For federal return data feeding into state computation:
- Invoke `tax-prep:form-1120-prep` for federal taxable income (Line 30), book-tax differences, and Schedule M-1/M-3 data that determine the state starting point
- Invoke `tax-prep:business-tax-schema` for form line definitions and cross-year line mapping when working with historical state returns

For federal and state e-filing mechanics:
- Invoke `tax-prep:e-filing` for MeF specifications, EFIN management, rejection code resolution, and signature authorization (Form 8879-C)
- Invoke `tax-prep:tax-compliance` for deadline management, extension filing (Form 7004), and penalty abatement strategies

For NOL and tax planning:
- Invoke `tax-prep:nol-tracking` for the federal NOL carryforward ledger; Florida maintains a separate NOL schedule (documented in this skill)
- Invoke `tax-prep:tax-planning` for multi-year state tax planning, estimated payment optimization, and entity structure considerations
- Invoke `financial-planning:tax-provision` for ASC 740 state tax provision and deferred tax computations

For supporting form schedules:
- Invoke `tax-prep:tax-forms` for supporting federal schedules that carry into state returns

For nexus and sales/use tax overlap:
- Invoke `bookkeeping:compliance-reporting` for sales/use tax nexus analysis and state registration requirements that may share nexus triggers with income tax

For entity and account structure:
- Invoke `accounting-foundation:entity-profile` for corporate entity details affecting state filing (domicile state, registered states, fiscal year)
- Invoke `accounting-foundation:chart-of-accounts` for GL account mapping to state tax lines (9100s state current tax expense)
- Invoke `accounting-foundation:financial-statements` for state-specific reporting presentation

For accounting system data extraction:
- Invoke `qbo-integration:qbo-reporting` for pulling financial data used in apportionment factor computation (sales by state, payroll by state, property by state)
- Invoke `qbo-integration:qbo-audit` for tax data extraction supporting state return preparation

## Cross-Plugin Consumers

- `tax-prep:e-filing` — consumes completed state returns for electronic filing transmission
- `tax-prep:form-1120-prep` — references state tax liability for federal deduction analysis
- `tax-prep:tax-planning` — uses state nexus analysis and rate data for multi-state planning
- `tax-prep:nol-tracking` — coordinates federal and state NOL utilization ordering
- `financial-planning:tax-provision` — uses state rate and apportionment data for ASC 740 provision
- `financial-planning:variance-analysis` — uses state tax estimates for budget-to-actual variance
- `firm-operations:engagement-management` — uses state filing list for engagement scoping
- `firm-operations:quality-compliance` — references state filing requirements for review checklists

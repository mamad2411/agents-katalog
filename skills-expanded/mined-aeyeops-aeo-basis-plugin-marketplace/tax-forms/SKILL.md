---
name: tax-forms
description: >
  Contains verified Section 179/bonus depreciation annual limits tables (2007-2026+),
  Form 8949 adjustment code catalog (W/B/T/O/S/N/H with box selection A-F), and Form 1118
  separate limitation category rules (GILTI/branch/passive/general with carryback-carryforward).
  MACRS property classes, mid-quarter convention triggers, capital loss carryback (3yr) and
  carryforward (5yr), wash sale rule for corporations, Form 5472 foreign-ownership ($25K
  penalty), IRC 267/482 transfer pricing methods (CUP/RPM/CPM/profit split), APA procedures,
  1099-DIV/1099-B reconciliation, digital asset compliance (crypto/1099-DA/DeFi/staking).
  Consult when preparing any Form 1120 supporting schedule, choosing depreciation elections,
  computing capital gains netting, evaluating foreign tax credit limitations, documenting
  intercompany pricing, or classifying digital asset transactions.
---

# Tax Forms

Operational skill for preparing supporting schedules and specialized forms that attach
to the federal Form 1120 corporate tax return. Covers depreciation, capital transactions,
foreign tax credits, intercompany compliance, investment reporting, and digital assets.

## Depreciation and Amortization (Form 4562)

### Section 179 Expensing

Allows immediate deduction of qualifying tangible personal property, QIP, and certain
real property improvements (roofs, HVAC, fire protection, security systems). Limited
by three caps: dollar limit ($1,250,000 for 2025), investment phase-out threshold
($3,130,000 for 2025), and taxable income from active trades or businesses. Excess
carries forward indefinitely. SUV limit ($31,300 for 2025) applies to vehicles over
6,000 lbs GVW classified as SUVs.

For C-corporations, the taxable income limitation is computed at the corporate level
(before the Section 179 deduction). Section 179 is a tax election only -- book
depreciation follows GAAP straight-line, creating a temporary book-tax difference.

### Bonus Depreciation Phase-Down

Applies to MACRS property with recovery period of 20 years or less, QIP, computer
software, and water utility property. Both new and used property eligible (used
property since 9/27/2017 under TCJA).

Key 2025 rule: P.L. 119-21 restored 100% bonus for property acquired and placed in
service after January 19, 2025. Property acquired before that date but placed in
service in 2025 follows the 40% rate. Elect-out is per-class, per-year, irrevocable.

Phase-down trajectory: 100% (2017-2022), 80% (2023), 60% (2024), 100% restored
post-1/19/2025, 20% (2026), 0% (2027+) absent new legislation.

### MACRS Property Classes

GDS (default) uses 200% DB for 3-20 year property and straight-line for 27.5+ year
property. ADS required for foreign-use property, tax-exempt use/bond-financed property,
and Section 163(j) electing real property trades. Key classes:

- 5-year: computers, office equipment, autos, light trucks
- 7-year: office furniture, fixtures, property without class life
- 15-year: QIP, land improvements, telephone distribution
- 39-year: nonresidential real property (straight-line, mid-month convention)

### Conventions

- **Half-year** (default for personal property) -- first/last year deduction is half
- **Mid-quarter** (triggered when >40% of depreciable basis placed in service in Q4) -- all property that year uses quarter-specific factors (Q1=87.5%, Q2=62.5%, Q3=37.5%, Q4=12.5%)
- **Mid-month** (real property only) -- 27.5-year and 39-year classes

### Listed Property

Passenger automobiles, transportation property with personal use potential, and
entertainment/recreation property. Must exceed 50% qualified business use for
accelerated depreciation or Section 179. Investment use does not count toward the 50%
threshold. If business use drops to 50% or below, recapture excess depreciation and
switch to ADS straight-line. Annual auto depreciation caps apply regardless of MACRS
class ($20,400 with bonus / $12,400 without for 2024).

### Amortization

- Section 197 intangibles (goodwill, covenants not to compete, customer lists, patents, trademarks): 15-year straight-line
- Section 174 R&E (2025+ per P.L. 119-21): domestic R&E deductible currently or amortized 60+ months; foreign R&E amortized 15 years. For 2022-2024: all Section 174 costs capitalized (5-year domestic, 15-year foreign)
- Startup/organizational costs: $5,000 immediate (if total <$50,000), remainder over 180 months

### Decision Points

1. Section 179 vs. bonus -- Section 179 is limited by business income; bonus is not. For profitable corps, bonus is simpler
2. Elect out of bonus? -- preserves depreciation for future high-income years
3. Mid-quarter convention triggered? -- check Q4 placements before year-end acquisitions
4. GDS or ADS? -- ADS required in specific situations; otherwise GDS provides faster recovery

## Capital Gains and Losses (Form 8949 / Schedule D)

### Form 8949 Structure

Part I (short-term, held 1 year or less): Box A (1099-B with basis reported, no
adjustments), Box B (1099-B without basis), Box C (no 1099-B). Part II (long-term,
held more than 1 year): Boxes D/E/F mirror A/B/C.

Adjustment codes in column (f): W (wash sale), B (incorrect basis), T (wrong holding
period), O (other), S (gross vs. net proceeds), N (noncovered security), H (short
sale holding period). Multiple codes can combine on one line.

### Corporate Capital Gains Rules

C-corporations receive no preferential capital gains rate -- all gains taxed at the
flat 21% rate (post-TCJA). The short-term/long-term distinction matters only for
netting gains against losses and tracking carryback/carryforward character.

Capital losses deduct only against capital gains -- no deduction against ordinary income
(individuals get $3,000; corporations get none). Net capital loss carries back 3 years,
then forward 5 years, always treated as short-term in the destination year.

### Schedule D Flow

Form 8949 totals flow to Schedule D Part I (lines 1a/1b/2) and Part II (lines
8a/8b/9). Schedule D adds installment sales (Form 6252), like-kind exchanges (Form
8824), pass-through gains/losses, capital gain distributions, and carryovers. Line 17
net result flows to Form 1120 Line 8 (if positive; zero if net loss).

Box A/D transactions with no adjustments can skip Form 8949 and report directly on
Schedule D.

### Section 1231 Interaction

Depreciable/real business property held >1 year: net Section 1231 gain is long-term
capital gain (flows to Schedule D); net Section 1231 loss is ordinary (fully
deductible, bypasses capital loss limitation). Apply the 5-year lookback -- current
1231 gains recharacterized as ordinary to the extent of unrecaptured 1231 losses from
prior 5 years. Depreciation recapture (Section 1245 for personal property, Section
1250 + Section 291 additional 20% for corporate real property) applies before 1231
netting.

### Wash Sale Rule (Section 1091)

Applies to corporations. Loss disallowed when substantially identical security
repurchased within 30 days before/after sale (61-day window). Disallowed loss adds to
replacement security basis; holding period tacks on. Report with code W on Form 8949.
Related party purchases (>50% ownership) can trigger wash sales for corporations.

### Cost Basis Methods

- Specific identification: most flexibility, requires contemporaneous documentation
- FIFO (default): oldest shares sold first
- Average cost: mutual fund/DRIP shares only (not individual stocks or ETFs)

### Decision Points

1. Any adjustment codes needed? -- compare 1099-B basis to taxpayer records, check for wash sales
2. Specific ID vs. FIFO? -- specific identification optimizes loss timing for carryback/carryforward planning
3. Net capital loss? -- compute carryback eligibility (3 years back), track carryforward (5 years, then expires)
4. Waive carryback? -- only beneficial if carryforward years have higher capital gains; election is irrevocable
5. Capital loss carryforward expiring? -- plan asset sales to generate offsetting gains before the 5-year window closes

## Foreign Tax Credit (Form 1118)

### Separate Limitation Categories

A separate Form 1118 is required for each applicable category:

- **Section 951A (GILTI)** -- no carryback or carryforward of excess credits
- **Foreign branch income** -- QBU business profits, excluding passive income
- **Passive category** -- foreign personal holding company income (dividends, interest, rents, royalties, gains), with exceptions for financial services and active rents/royalties
- **General category** -- residual; includes high-taxed passive income reclassified via HTKO
- **Section 901(j)** -- sanctioned country income
- **Treaty-resourced** -- U.S.-source income re-sourced as foreign under treaty

### Credit Computation

Limitation per category: (foreign-source taxable income in category / worldwide
taxable income) x U.S. tax. Eligible taxes: income, war profits, excess profits taxes
paid or accrued to foreign countries; taxes deemed paid under Section 960 for CFC
inclusions. Section 78 gross-up: deemed-paid taxes added to gross income to properly
compute the limitation numerator.

### High-Tax Kickout (HTKO)

Passive income reclassified to general category when the effective foreign tax rate
exceeds the highest U.S. corporate rate (21% post-TCJA).

### Look-Through Rules (CFCs)

Dividends, interest, rents, and royalties from a CFC to a 10% U.S. shareholder are
classified by the CFC's underlying earnings category, not automatically passive.

### Carryback/Carryforward

Excess credits: carry back 1 year, then forward 10 years (same category). Exception:
GILTI category credits have no carryback or carryforward. OFL/SLL accounts track
situations where foreign losses offset U.S.-source income, requiring future recapture.

### Foreign Tax Redeterminations

Redetermine credit when: accrued taxes differ from amounts paid, taxes unpaid within
24 months of year-end, foreign taxes refunded, or CFC inclusions change.

### Section 960(d)(4) (New for 2025)

Disallows 10% of foreign income taxes on PTEP distributions attributable to prior
Section 951A inclusions.

## Intercompany and Related-Party Compliance

### Related Party Definition (IRC 267(b))

Related parties include: individual and >50%-owned corporation, two corporations in the
same controlled group (>50% common ownership), corporation and partnership with >50%
common owners. Constructive ownership rules (IRC 267(c)) expand ownership through
family, partnerships, estates/trusts, corporations (50%+ shareholders), and options.

### Section 267 Loss Disallowance

Losses on related-party sales are disallowed (not deferred). Recovery only when the
buyer sells to an unrelated third party -- buyer's gain reduced by previously
disallowed loss (not below zero). If the buyer later sells at a loss to an unrelated
party, the disallowed loss is permanently lost.

### Accrual-to-Cash Timing (Section 267(a)(2))

When an accrual-basis corporation accrues an expense to a cash-basis related party,
deduction deferred until actually paid and includible in the payee's income. Common
scenarios: year-end officer bonuses, management fees to related LLCs, interest on
shareholder loans.

### Form 5472 Reporting

Required when a 25% foreign-owned U.S. corporation has reportable transactions with
a foreign related party. Also required for foreign-owned disregarded entities (since
2017). Separate Form 5472 for each foreign related party.

Reportable transactions (Parts IV/V/VI): sales/purchases of property, rents, royalties,
services, commissions, interest, insurance premiums, PCT/CST payments, nonmonetary
transactions at FMV, and related-party debt balances.

Penalty: $25,000 per form (post-TCJA; was $10,000), plus $25,000 per 30-day period
after IRS notification, no cap. Reasonable cause defense is narrow.

### Intercompany Loans (IRC 7872/AFR)

Must charge adequate stated interest at or above AFR. Below-market loans trigger
imputed interest. Demand loans at short-term AFR (recomputed annually); term loans at
AFR for applicable term on loan date. No $10,000 gift loan exception for
corporation-shareholder loans.

## Transfer Pricing (Section 482)

### Methods (Best Method Rule -- No Hierarchy)

1. **CUP** -- direct price comparison; strongest when exact comparables exist
2. **Resale price** -- resale price minus appropriate gross profit margin; best for limited-function distributors
3. **Cost plus** -- costs plus appropriate markup; best for contract/toll manufacturers
4. **Comparable profits (CPM/TNMM)** -- net profit margin comparison using PLIs; most commonly used due to data availability
5. **Profit split** -- allocate combined profit by relative contributions; for highly integrated operations with significant intangibles on both sides

### Documentation for Penalty Protection (Reg. 1.6662-6)

Contemporaneous documentation (by return due date with extensions): organizational
structure, controlled transaction description, comparability analysis, best method
selection and application, economic analysis, document index. Late-created
documentation does not qualify for penalty protection.

### Penalties

- 20% substantial valuation misstatement: transfer price 200%+ (or 50%-) of correct price, net adjustment >$5M or 10% gross receipts
- 40% gross valuation misstatement: transfer price 400%+ (or 25%-) of correct price, net adjustment >$20M or 20% gross receipts
- Contemporaneous documentation creates rebuttable presumption of reasonable cause

### APAs

Binding IRS-taxpayer agreements on transfer pricing method. Unilateral (IRS only),
bilateral (IRS + one foreign authority), multilateral. Typical term: 5 prospective
years with rollback. User fee: $113,500 large cases, $56,750 small. Timeline: 12-24
months unilateral, 24-48 months bilateral.

### BEAT (Section 59A)

Base erosion payments to foreign related parties create minimum tax exposure. Threshold:
$500M average annual gross receipts, 3% base erosion percentage. BEAT applies
regardless of arm's length pricing.

## Investment Tax Reporting

### 1099 Processing

- **1099-DIV**: Box 1a ordinary dividends (1b qualified subset), Box 2a capital gain distributions, Box 3 return of capital (reduces basis), Box 4 federal withholding, Box 11 tax-exempt interest
- **1099-B**: Sales data flows to Form 8949. Reconcile broker-reported basis against taxpayer records before filing. Aggregate by holding period for Schedule D
- **1099-INT**: Taxable and tax-exempt interest segregation

### Brokerage Reconciliation

Match brokerage statements to the accounting system's investment accounts at cost basis.
The accounting system tracks cost basis; unrealized gains are off-book until disposition.
Maintain lot-level detail in a supplemental schedule (most accounting systems do not
natively track individual security lots).

Separate income accounts by type: Short-Term Capital Gains, Long-Term Capital
Gains, Short-Term Capital Losses, Long-Term Capital Losses, Qualified Dividends,
Ordinary Dividends, Taxable Interest, Tax-Exempt Interest. For account setup and
journal entry mechanics, invoke `qbo-integration:qbo-bookkeeping`.

## Digital Asset Compliance

### Tax Classification

Digital assets (cryptocurrency, NFTs, stablecoins, tokenized securities) are property
under Notice 2014-21. Every disposition is a realization event. For C-corporations,
short-term/long-term distinction affects only character and capital loss limitation
analysis, not the tax rate (flat 21%).

### Taxable Events

Sale for fiat, exchange for another digital asset, payment for goods/services, receipt
as payment (ordinary income at FMV), mining rewards (ordinary income when dominion and
control established), staking rewards (ordinary income at FMV when received -- IRS
position), hard forks with airdrop (ordinary income per Rev. Rul. 2019-24).

NOT taxable: purchasing with fiat, wallet-to-wallet transfers, soft forks without new
assets.

### Cost Basis

- Specific identification (preferred): requires lot-level tracking with transaction hashes and wallet addresses
- FIFO (default if specific ID not established)
- Average cost is NOT available for digital assets

### Wash Sale Exemption

IRC Section 1091 currently does not apply to digital assets. A corporation can sell
crypto at a loss and immediately repurchase without deferral. Monitor pending
legislation that would extend wash sale rules to digital assets.

### Reporting

Form 1120 mandatory digital asset question (since TY2023). Dispositions on Form
8949/Schedule D. Form 1099-DA (new TY2025+) from custodial brokers -- reconcile
against internal records. FIFO becomes default for broker-reported basis if no specific
identification election made with the broker.

## Accounting System Integration Notes

- Fixed assets at cost basis; depreciation via journal entries (the accounting system does not compute MACRS). Section 179 is a tax election creating a book-tax difference
- Capital gains/losses in separate accounts by holding period; wash sale adjustments are tax-only (book tracks original cost, tax tracks adjusted)
- Foreign taxes paid to an expense account; Section 78 gross-up is return-level only
- Intercompany due-to/from balance sheet accounts reconciled monthly; management fee allocations documented in JE memos
- Digital assets as separate Other Current Asset accounts per holding; lot tracking in supplemental schedule or crypto tax software
- Investment accounts reconciled to brokerage at cost basis; 1099 totals tied to year-end balances

For platform-specific account setup, journal entry creation, and reporting, invoke the appropriate `qbo-integration` skill.

## Supporting References

Read these for deeper operational detail on specific form areas:

- `references/depreciation-4562.md` -- Form 4562 line guidance, Section 179 annual limits table (2007-2026+), bonus depreciation phase-down schedule with P.L. 119-21 restoration, eligible/ineligible property lists, decision points for Section 179 vs. bonus
- `references/fixed-asset-macrs.md` -- Complete MACRS property class table with GDS/ADS periods, convention trigger rules, Section 179 qualifying property and C-corp income limitation, bonus phase-down by year, listed property requirements and auto depreciation caps, disposition rules (Section 1245/1250 recapture, Section 1031 post-2017), general asset accounts
- `references/capital-gains-8949.md` -- Form 8949 box selection (A-F), adjustment code catalog (W/B/T/O/S/N/H), corporate no-preferential-rate rule, capital loss limitation and carryback/carryforward mechanics, wash sale rule application to corporations, cost basis methods, year-by-year corporate capital gains rate table
- `references/schedule-d-1120.md` -- Schedule D line-by-line structure, Form 8949-to-Schedule D flow, capital loss carryback mechanics (Form 1120X/1139), Section 1231 recharacterization with 5-year lookback, depreciation recapture (Sections 1245/1250/291), installment sale interaction, Form 1120 Line 8 mapping
- `references/foreign-tax-credit-1118.md` -- Separate limitation categories with post-TCJA structure, credit computation formula, Section 78 gross-up, HTKO threshold, CFC look-through rules, carryback (1 year) and carryforward (10 years) rules, OFL/SLL account tracking, foreign tax redetermination triggers, Section 960(d)(4) new for 2025, year-by-year variance table
- `references/intercompany-transactions.md` -- IRC 267(b) related-party definition with constructive ownership, Section 267 loss disallowance mechanics, accrual-to-cash timing mismatch, Form 5472 filing requirements and reportable transactions (Parts IV/V/VI), $25,000 penalty framework, intercompany loan AFR rules (IRC 7872), documentation requirements, management fee allocation patterns
- `references/transfer-pricing.md` -- Five Section 482 methods with operational detail (CUP, RPM, cost plus, CPM, profit split), best method rule, commensurate-with-income standard for intangibles, cost sharing arrangement requirements (QCSA/PCT/CST), APA types and process (fees, timeline, binding nature), contemporaneous documentation elements for penalty protection, penalty thresholds (20%/40%), BEAT applicability
- `references/investments-tax-reporting.md` -- Brokerage statement parsing (position and transaction data models), position reconciliation to the accounting system, 1099-DIV processing by box (1a/1b/2a/3/4/11), 1099-B sales aggregation by holding period, investment income summary generation
- `references/digital-assets.md` -- IRS property classification (Notice 2014-21), comprehensive taxable/non-taxable event catalog, cost basis methods (specific ID/FIFO/HIFO -- no average cost), wash sale exemption and pending legislation, Form 1120 digital asset question, Form 1099-DA implementation timeline, DeFi treatment (liquidity provision, yield farming, governance tokens, wrapped tokens), record-keeping requirements (wallet addresses, transaction hashes), year-by-year regulatory timeline (2014-2025+)

## Cross-Plugin References

For account structure and classification:
- Invoke `accounting-foundation:chart-of-accounts` for tax-line mapping, numbering ranges, and book-tax difference account design
- Invoke `accounting-foundation:categorization-rules` for transaction routing to capital gain/loss, depreciation, and intercompany accounts
- Invoke `accounting-foundation:entity-profile` for foreign ownership status (Form 5472 threshold), corporate structure, and fiscal year
- Invoke `accounting-foundation:financial-statements` for presentation of depreciation, gains/losses, and foreign tax credits on GAAP statements

For QBO platform operations:
- Invoke `qbo-integration:qbo-coa` for QBO account types supporting investment income, capital gains, and intercompany accounts
- Invoke `qbo-integration:qbo-bookkeeping` for journal entry creation (depreciation entries, 1099 processing, intercompany allocations)
- Invoke `qbo-integration:qbo-reporting` for reports supporting brokerage reconciliation and investment income summaries
- Invoke `qbo-integration:qbo-audit` for tax data extraction and year-end verification of form-supporting balances
- Invoke `qbo-integration:qbo-api` for programmatic transaction creation and intercompany transaction extraction

For bookkeeping coordination:
- Invoke `bookkeeping:transaction-processing` for categorization of investment transactions, digital asset entries, and intercompany charges
- Invoke `bookkeeping:reconciliation` for brokerage account reconciliation and intercompany balance verification

For sibling tax-prep skills:
- Invoke `tax-prep:form-1120-prep` for Schedule D Line 8 mapping, Form 4562 Line 20 attachment, and overall return assembly
- Invoke `tax-prep:business-tax-schema` for Form 5472 field vocabulary and form data structures
- Invoke `tax-prep:state-returns` for state-level depreciation conformity and capital gains treatment
- Invoke `tax-prep:tax-compliance` for filing deadlines, extension procedures, and penalty exposure
- Invoke `tax-prep:tax-planning` for depreciation optimization, capital gains timing, and FTC planning strategies
- Invoke `tax-prep:nol-tracking` for interaction between capital loss carrybacks and NOL utilization
- Invoke `tax-prep:e-filing` for electronic filing of supporting forms and schedules

For financial planning integration:
- Invoke `financial-planning:tax-provision` for ASC 740 treatment of deferred tax from depreciation timing differences and foreign tax credits
- Invoke `financial-planning:budgeting-forecasting` for depreciation projections and capital expenditure planning

## Cross-Plugin Consumers

- `tax-prep:form-1120-prep` -- supporting forms and schedules attach to the 1120; Schedule D Line 8, Form 4562 Line 20, Form 1118 credit
- `tax-prep:tax-planning` -- depreciation elections, capital gains timing, FTC utilization strategies
- `tax-prep:state-returns` -- state depreciation conformity references federal Form 4562 computations
- `financial-planning:tax-provision` -- depreciation and FTC timing differences drive deferred tax computations
- `financial-planning:variance-analysis` -- depreciation expense variances traced to asset acquisition timing and method elections
- `firm-operations:engagement-management` -- Form 5472 and transfer pricing documentation scope assessment for engagement planning
- `firm-operations:quality-compliance` -- transfer pricing documentation completeness as a quality checkpoint

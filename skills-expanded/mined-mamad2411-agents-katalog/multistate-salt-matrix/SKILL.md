---
name: multistate-salt-matrix
description: >
  Use when determining which apportionment formula a state applies, comparing state conformity
  to a federal provision across filing states, building a state modification matrix, evaluating
  multistate nexus exposure for a C-corporation, analyzing P.L. 86-272 protection for
  internet-era activities, or assessing voluntary disclosure eligibility. Covers UDITPA
  three-factor and single sales factor apportionment, market-based vs cost-of-performance
  sourcing, throwback and throwout rules, Joyce vs Finnigan, rolling/static/selective federal
  conformity with state modifications for Section 163(j), GILTI, Section 174 R&E, bonus
  depreciation and state NOLs, economic and factor-presence nexus, affiliate nexus, the MTC
  2021 P.L. 86-272 statement, combined reporting, unitary business, water's edge elections,
  and state tax credits.
license: MIT
metadata:
  author: AEO Basis
  version: "0.3.2"
  summary: Multistate SALT reference matrix for apportionment formulas, federal conformity, and nexus evaluation.
---

# Multistate SALT Matrix

Cross-state comparison matrix for state and local tax (SALT) planning and compliance.
This skill provides the structural framework for evaluating nexus, apportionment, conformity,
and reporting obligations across multiple states. For deep single-state coverage (Florida),
invoke `tax-prep:state-returns`.

## Nexus Evaluation Matrix

A corporation must evaluate five nexus theories for every state where it has any activity.
Each theory operates independently — triggering any one creates a filing obligation unless
P.L. 86-272 provides protection.

### Physical Presence

Traditional constitutional nexus. Any of these facts creates nexus:
- Employees in-state (including remote workers whose home office is in-state)
- Owned or leased real or tangible personal property
- Inventory (including third-party fulfillment warehouse stock)
- Contractor activity (some states attribute contractor presence to the hiring company)
- Mobile workforce beyond de minimis thresholds (state-specific day counts)

Remote worker nexus is a post-2020 compliance risk. States differ on whether a single
remote employee is sufficient. Convenience-of-the-employer rules (NY and followers) may
source income to the employer's state rather than the worker's home state.

### Economic Nexus / Factor Presence

Post-Wayfair, states apply economic nexus to income tax using the MTC factor presence
model or state-specific variants. The MTC model triggers nexus when any single factor
exceeds the state's threshold: property, payroll, or sales attributed to the state.
Unlike sales tax economic nexus (based on gross receipts), income tax economic nexus
uses property, payroll, and sales factors with state-determined thresholds.

### Affiliate / Attributional Nexus

An out-of-state entity may have nexus attributed through related entities:
- Agency nexus — in-state entity acts on behalf of the out-of-state entity
- Unitary business nexus — combined reporting states attribute nexus through the unitary group
- Affiliate nexus statutes — presence through substantially similar trademarks/trade names
- Holding company nexus — states with addback or combined reporting may reach out-of-state holding companies receiving royalties or interest from in-state subsidiaries

### Statutory "Doing Business" Nexus

Some states define nexus broadly as "doing business," which may capture activities beyond
physical and economic presence: owning intangible property used in-state, licensing IP,
or having customers in the state.

### Nexus Evaluation Workflow

1. Inventory all state contacts (employees, property, sales, contractors, affiliates, internet activity)
2. Apply physical presence test per state
3. Apply economic nexus / factor presence test for states without physical presence
4. Check affiliate / attributional nexus for states with no direct presence
5. Apply P.L. 86-272 filter (see below) for states where nexus exists
6. Assess internet activity against each state's position on the MTC 2021 revised statement
7. Result: filing obligation list
8. For states with nexus but no prior filing, evaluate VDA eligibility

## P.L. 86-272 Protection Analysis

Federal law (15 USC 381-384) prohibits net income tax when the only in-state activity is
solicitation of orders for tangible personal property, with orders approved and filled
out of state.

### Scope Limitation

P.L. 86-272 protects ONLY tangible personal property sales. It provides zero protection for:
- Services revenue (consulting, technology, professional services)
- Intangible property sales or licensing
- Leasing of tangible personal property

For service-only corporations, P.L. 86-272 is irrelevant — nexus is determined solely
by the physical presence and economic nexus tests.

### Internet Activity (MTC 2021 Revised Statement)

The MTC's 2021 revised statement treats these internet activities as exceeding solicitation
and therefore unprotected:
- Selling products/services through a website or app to in-state customers
- Streaming or providing digital content to in-state users
- Using cookies/tracking to gather consumer data beyond solicitation (behavioral advertising, personalization)
- Providing electronic post-sale assistance (chat, help desk)
- Managing loyalty/reward programs through internet or app
- Contracting with in-state content creators or influencers

Still protected under the MTC statement:
- Static product information display
- Product search and availability lookup
- Cookies used solely for internal analytics (not consumer-specific)
- Email/electronic advertising to in-state customers

State adoption varies. The trend is toward broader adoption of the MTC position.

### P.L. 86-272 Decision Tree

1. Corporation sells tangible personal property? If NO, no protection
2. Also sells services/intangibles in-state? If YES, P.L. 86-272 does not protect that revenue stream
3. All in-state activities limited to solicitation and ancillary activities? If NO, protection lost
4. Orders approved and filled outside the state? If NO, protection lost
5. Internet activities exceed the protected list? Check specific state's MTC adoption status

## Apportionment Framework

### Formula Types

States use one of three formula structures for general business corporations:

**Single sales factor** — the majority of states. Apportioned income = (State sales / Total sales) x Taxable income. Eliminates property and payroll from the formula, removing incentive to relocate those factors.

**Double-weighted sales (or other weighted)** — a declining number of states weight sales at 50-90% with the remainder split between property and payroll.

**Equal three-factor (UDITPA)** — a small number of states retain equal weighting: (Property + Payroll + Sales) / 3.

### Sales Factor Sourcing

The sourcing rule determines which state claims a sale in its numerator:

**Market-based sourcing (majority rule)** — services sourced where the customer receives the benefit. Cascading hierarchy: delivery location, billing address, commercial domicile, reasonable approximation.

**Cost-of-performance (declining)** — services sourced where the income-producing activity is performed. Many states use an all-or-nothing approach (100% to the state with the greater proportion of activity). This is being replaced by market-based sourcing.

**Tangible personal property** — uniformly sourced to the destination state (where goods are delivered).

### Throwback and Throwout Rules

**Throwback** — sales shipped from a state where the taxpayer has nexus to a state where the taxpayer does NOT have nexus are "thrown back" to the origin state's numerator. Prevents "nowhere income." Many states have enacted throwback; some have repealed it alongside single sales factor adoption.

**Throwout** — instead of adding nowhere sales to the origin numerator, removes them from the denominator in all states. Increases apportionment everywhere proportionally. Adopted by only a small number of states.

### Joyce vs. Finnigan (Combined Reporting)

In combined reporting states, the choice between Joyce and Finnigan determines whose nexus counts for the sales factor numerator:

**Joyce** — each entity's nexus is evaluated independently. Sales by a group member without nexus in the state are excluded from the combined numerator. Reduces combined apportionment.

**Finnigan** — the group is treated as a single taxpayer. If any member has nexus, all members' sales to the state are in the numerator. Increases combined apportionment.

### Special Industry Formulas

Standard apportionment may not apply to certain industries:
- Financial institutions — receipts factor (interest, fees, gains) with borrower/depositor-location sourcing
- Airlines — revenue ton-miles or departures factor; Airline Deregulation Act constraints
- Trucking — revenue miles factor
- Telecommunications — customer-location sourcing; infrastructure allocation by mileage/customer count
- Construction — sourced to project location

### UDITPA Section 18 (Distortion Relief)

When the standard formula does not "fairly represent" in-state activity, the taxpayer or tax authority may petition for an alternative method. High bar: must demonstrate the standard formula produces an unreasonable result AND the proposed alternative is reasonable.

## State Conformity to Federal Taxable Income

### Conformity Methods

**Rolling conformity** — state adopts the IRC as currently in effect. Federal changes flow through automatically. Majority of states. Risk: unplanned revenue impact from federal tax cuts unless the state decouples.

**Static (fixed-date) conformity** — state adopts the IRC as of a specified date. Federal changes after that date require state legislative action. Creates computation complexity when the state's IRC version differs from the current federal return.

**Selective conformity** — state adopts specific IRC provisions on a section-by-section basis. Maximum state control, highest compliance complexity.

### Key Modification Patterns

These federal provisions generate the most significant state-by-state divergences:

**Section 163(j) interest limitation** — states may conform (apply the 30% ATI limitation), decouple fully (require addback), or apply a modified threshold. Treatment of disallowed interest carryforward varies.

**GILTI (IRC 951A)** — state treatment ranges from full inclusion with no Section 250 deduction (maximum tax) through partial deduction to full exclusion (treating GILTI as non-taxable foreign income). Combined reporting states face additional complexity on CFC income within the unitary group.

**Section 174 R&E amortization** — post-2021, federal law requires capitalization over 5 years (15 for foreign research). Some states decouple, allowing current deduction for state purposes. Static conformity states with a pre-2022 date may automatically allow current deduction. Creates multi-year timing differences requiring state-by-state tracking.

**Bonus depreciation (IRC 168(k))** — states may fully conform, cap at a lower percentage, fully decouple (requiring addback and recomputation on a standard recovery schedule), or conform at the rate matching their static conformity date. Decoupling creates timing differences only (total depreciation is the same over the asset's life).

**State NOL rules** — key variables: carryback availability, carryforward period (indefinite or fixed), utilization limitation (80% of income, lower percentage, or dollar cap). State NOLs are computed from state taxable income after modifications and apportionment — not from the federal NOL amount.

## Combined and Separate Reporting

### Separate Filing (Default)

Each legal entity files its own return, computes its own apportionment, and reports its own income. Allows potential income shifting through intercompany transactions (royalties, management fees, interest).

### Mandatory Combined Reporting

Combined reporting states require all members of a unitary business to file a combined return. Intercompany transactions are eliminated, removing the income-shifting mechanism. The combined apportionment factor captures all members' activity.

**Water's edge** — limits the combined group to domestic entities and certain foreign entities with substantial U.S. activity. The default in most combined reporting states.

**Worldwide combined** — includes all entities globally. Very few states require this; most offer it as an option or anti-avoidance override.

### Unitary Business Determination

**Three unities test**: unity of ownership (common control, typically >50%), unity of operation (shared services — purchasing, accounting, HR, legal), unity of use (centralized management and strategy).

**Contribution/dependency test**: entities contribute to or depend upon each other through flows of goods, services, capital, or management.

Active holding companies (providing capital, strategy, shared services) are typically unitary with their subsidiaries. Passive holding companies that merely hold stock may be excluded.

## Voluntary Disclosure Programs

For states where the corporation has nexus but has not been filing, voluntary disclosure agreements (VDA) limit exposure:

- **Lookback period** — typically 3-4 years (vs. indefinite exposure for non-filers discovered by audit)
- **Penalty waiver** — most states waive all penalties under VDA
- **Interest** — generally not waived; accrues on unpaid tax for the lookback period
- **Future compliance** — taxpayer commits to prospective filing and payment
- **MTC National Nexus Program** — centralized multistate VDA through a single contact; confidential until agreement is reached; not all states participate

Initiate VDA before the state discovers non-filing. If the state contacts the taxpayer first, VDA eligibility may be foreclosed.

## State Tax Credits

### Credit Categories

**R&D credits (piggyback)** — based on federal IRC 41 QRE definitions, with state-determined rates. May be refundable or nonrefundable. Typically limited to in-state research expenditures.

**Investment credits** — percentage of qualified capital investment (manufacturing equipment, real property, technology). Clawback provisions if investment is removed or employment targets are missed.

**Hiring / employment credits** — per-employee amount for net new positions above a base level. Tiered by region (enhanced in distressed areas). Multi-year availability while positions are maintained.

**Enterprise zone / opportunity zone credits** — enhanced incentives in designated geographic areas. May include income tax credits, property tax abatement, and sales tax exemption. Require pre-investment certification.

**Clean energy credits** — growing category for renewable energy, energy efficiency, and EV-related investment.

### Credit Planning

- Apply stacking rules (state-specified order of credit application)
- Many nonrefundable credits are limited to a percentage of pre-credit liability
- Track carryforward periods per credit; use expiring credits first
- Credits apply after apportionment — based on in-state activity

## Multistate Modification Matrix

The operational artifact for multistate compliance. For each filing state, track:

1. Federal taxable income starting point (Line 30, Form 1120)
2. State additions (bonus depreciation addback, 163(j) addback, GILTI inclusion, state tax deduction addback)
3. State subtractions (GILTI exclusion, Section 174 current deduction, U.S. government interest)
4. State modified income before apportionment
5. Apportionment formula and percentage
6. State NOL deduction (state-computed, not federal)
7. State exemption (if any)
8. State tax at the applicable rate
9. State tax credits
10. Net state tax due

## Supporting References

Read these for detailed framework content, evaluation workflows, and authoritative model citations:

- `references/nexus-evaluation-framework.md` — Physical presence nexus triggers,
  economic/factor presence nexus (post-Wayfair for income tax), affiliate/attributional
  nexus theories, P.L. 86-272 protection analysis (protected vs unprotected activities,
  MTC 2021 revised statement on internet activities), VDA program structure and MTC
  National Nexus Program, multistate nexus evaluation workflow. Read when performing a
  multistate nexus evaluation, analyzing P.L. 86-272 for a service or internet-active
  company, or assessing voluntary disclosure eligibility.

- `references/apportionment-formulas.md` — UDITPA three-factor formula (property/payroll/sales
  computation details), single sales factor mechanics, market-based vs cost-of-performance
  sourcing rules and hierarchy, throwback/throwout rules, Joyce vs Finnigan combined
  reporting election, special industry formulas (financial institutions, airlines, trucking,
  telecom, construction), business vs nonbusiness income distinction, MTC model allocation
  and apportionment regulation, Section 18 distortion relief. Read when computing
  apportionment for a specific state, resolving sourcing questions for services or
  intangibles, or evaluating special industry formula applicability.

- `references/state-conformity-matrix.md` — Rolling/static/selective conformity comparison,
  state modification patterns for Section 163(j), GILTI, Section 174 R&E, bonus
  depreciation, and state NOL rules. Combined vs separate reporting mechanics, water's
  edge and worldwide combined reporting, unitary business tests (three unities,
  contribution/dependency). State tax credit inventory (R&D piggyback, investment, hiring,
  enterprise zone, clean energy, film). Multistate modification matrix workflow. Read
  when building a state-by-state modification matrix, evaluating combined reporting
  obligations, or researching state treatment of a specific federal provision.

## Cross-Plugin References

For single-state deep coverage and federal return data:
- Invoke `tax-prep:state-returns` for Florida-specific return preparation, Florida nexus rules, Florida apportionment, Florida NOL, and Florida e-filing requirements
- Invoke `tax-prep:form-1120-prep` for federal taxable income (Line 30) that serves as the starting point for all state computations
- Invoke `tax-prep:nol-tracking` for federal NOL carryforward ledger; state NOLs are computed separately (documented in this skill)
- Invoke `tax-prep:tax-planning` for multi-year multistate tax planning, entity structure optimization, and estimated payment strategies
- Invoke `tax-prep:tax-compliance` for deadline management, extension filing, and penalty abatement across states

For financial reporting and entity data:
- Invoke `financial-planning:tax-provision` for ASC 740 state tax provision, deferred tax computations from state timing differences (bonus depreciation, Section 174, NOL), and state rate changes
- Invoke `accounting-foundation:entity-profile` for corporate entity details affecting multistate filing (domicile state, registered states, fiscal year)
- Invoke `accounting-foundation:chart-of-accounts` for GL account mapping to state tax lines

For platform data supporting apportionment:
- Invoke `qbo-integration:qbo-reporting` for financial data used in apportionment factor computation (sales by state, payroll by state, property by state)

## Cross-Plugin Consumers

- `tax-prep:state-returns` — uses cross-state matrix when expanding beyond Florida
- `tax-prep:tax-planning` — uses nexus analysis, apportionment data, and credit inventory for multistate planning
- `tax-prep:form-1120-prep` — references state tax liability for federal deduction analysis
- `financial-planning:tax-provision` — uses state rates, apportionment, and conformity data for ASC 740 provision
- `financial-planning:variance-analysis` — uses state tax estimates for budget-to-actual variance
- `firm-operations:engagement-management` — uses multistate filing list for engagement scoping
- `firm-operations:quality-compliance` — references multistate filing requirements for review checklists

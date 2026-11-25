---
name: entity-profile
description: >
  Contains verified entity-type comparison tables (C-corp/S-corp/LLC tax differentials,
  formation procedures, S-election deadlines), IRS officer compensation multi-factor
  analysis with Schedule E audit triggers, and IRC 267/482 related-party rules with
  Form 5472 foreign-ownership reporting. Covers EIN, ownership structure, constructive
  ownership (IRC 267(c)), controlled groups, fiscal year, accounting method, accumulated
  earnings tax (Bardahl formula), QSBS (IRC 1202), and state filing obligations.
  Consult when determining entity type, evaluating S-election timing or late relief
  (Rev. Proc. 2013-30), setting or defending officer compensation, identifying related
  parties, assessing Form 5472 requirements, analyzing AET exposure, onboarding a new
  entity, or answering "who owns this company / what entity type are we."
---

# Entity Profile

Cross-cutting reference for corporate entity information that every service line
consumes. Covers the data elements that identify an entity, its legal structure,
its ownership, and its compliance obligations that flow from those characteristics.

> **State-specific scope:** Entity type classification, fiscal year/accounting method,
> ownership structure, foreign ownership, officers, related-party rules, and change
> events are nationally applicable. State filing obligations marked (Florida) contain
> **Florida**-specific formation procedures, fees, and corporate income tax rules.
> Practitioners in other states should substitute their state's requirements.

## Entity Identification Data

Every engagement begins with capturing the core identity fields. These fields
drive downstream decisions across bookkeeping, tax, and financial planning.

**Legal name** — The exact name on file with the state Division of Corporations
(not DBA/trade names). Use the legal name for all tax filings, bank accounts,
and engagement letters. Verify against the state filing (sunbiz.org for Florida).

**EIN (Employer Identification Number)** — Obtained via Form SS-4, filed online
at irs.gov (immediate issuance) or by fax/mail. Required before opening bank
accounts or filing any returns. The EIN confirmation letter (IRS Letter 147C)
should be in the permanent client file. For reconstructed/delinquent filings
where the EIN is unknown, file Form 4506-T for IRS transcripts or call the
IRS Business line.

**DUNS number** — Dun & Bradstreet identifier. Required for government contracting,
some vendor applications, and credit reporting. Not all entities have one.

**State of incorporation/organization** — The state where articles of incorporation
(corporation) or articles of organization (LLC) were filed. Determines governing
corporate law, annual report obligations, and home-state tax nexus. Florida
corporations file with the Division of Corporations at sunbiz.org.

**Date of incorporation** — Relevant for QSBS (IRC 1202) holding period
computation, S-election timing, and delinquent filing lookback.

## Entity Type Classification

Entity type determines the tax return filed, the equity account structure, the
ownership rules, and available tax elections. The classification flows from the
check-the-box regulations (Treas. Reg. 301.7701-1 through -3).

### C-Corporation (Form 1120)

Entity-level tax at flat 21% (post-TCJA). Distributions taxed again as qualified
dividends (0/15/20% + 3.8% NIIT). Double taxation is the defining characteristic.
Key attributes:

- Unlimited shareholders, any type (individuals, entities, foreign persons, trusts)
- Unlimited classes of stock (common, preferred, voting, non-voting)
- Losses do NOT pass through — trapped at entity level, offset via NOL carryforward (80% limit post-2017)
- Fringe benefits advantage: employer-paid health, group-term life ($50K) deductible by corp, excluded from shareholder-employee income
- Accumulated earnings tax risk if retained E&P exceeds reasonable business needs ($250K threshold, $150K for personal service corps)
- Self-employment tax not applicable — officer-shareholders pay FICA only on W-2 wages

### S-Corporation (Form 1120-S)

Pass-through via Schedule K-1. No entity-level federal tax (some states impose
entity-level tax). Key constraints:

- Maximum 100 shareholders; must be U.S. individuals, certain trusts, or estates
- Single class of stock only (voting right differences permitted)
- Losses pass through, limited by: stock basis, debt basis (direct loans only), at-risk rules, passive activity rules
- Reasonable compensation required for officer-shareholders performing services — IRS scrutinizes low salaries
- QBI deduction (Section 199A, 20%) available 2018-2025
- >2% shareholder-employees cannot exclude employer-paid health, group-term life from income

**S-Election (Form 2553)**: File within 75 days of formation, or by March 15
for calendar-year corps to be effective for current year. All shareholders must
consent. Late election relief available under Rev. Proc. 2013-30 if filed within
3 years and 75 days of intended effective date with "FILED PURSUANT TO REV. PROC.
2013-30" at the top.

### LLC Taxed as Partnership (Form 1065)

Pass-through via Schedule K-1. Maximum flexibility — unlimited members, any
type, disproportionate allocations permitted if "substantial economic effect"
(Treas. Reg. 1.704-1(b)). Active members' distributive share generally subject
to self-employment tax (15.3% up to SS wage base, 2.9% above). Basis includes
member's share of partnership liabilities (more generous than S-corp).

### Disregarded Entity (Single-Member LLC)

If owned by an individual: Schedule C. If owned by a corporation: reported on
the corporation's return. State-law liability protection retained despite
federal tax disregard. Since 2017, foreign-owned disregarded entities must
file Form 5472 (treated as corporations for reporting purposes under Reg.
301.7701-2(c)(2)(vi)).

## Fiscal Year and Accounting Method

**Fiscal year** — Set during initial formation (board resolution adopting
bylaws specifies fiscal year). Calendar year (December 31) is most common for
C-corps. S-corps generally must use calendar year unless they establish a
business purpose or make a Section 444 election. The fiscal year determines
all filing deadlines.

**Accounting method** — Cash or accrual basis, elected on the first return filed.
Must match between books and tax returns. Cash basis available for C-corps with
average annual gross receipts of $29M or less (inflation-adjusted, 3-year
average, IRC 448). Accrual basis required above that threshold. Changing
methods requires Form 3115 (Application for Change in Accounting Method).
The accounting method affects revenue recognition timing, expense deduction
timing, and the Section 267(a)(2) accrual-to-cash matching rules for
related-party transactions.

## Ownership Structure

### Shareholder Records

Maintain a shareholder register showing: name, SSN/EIN, number of shares (by
class), percentage ownership (common and preferred separately), date acquired,
acquisition method (original issue, purchase, gift, inheritance), cost basis,
and any restrictions or vesting schedules.

### Stock Classes and Capital Structure

C-corps may issue multiple classes: common stock (voting and/or non-voting),
preferred stock (dividend preference, liquidation preference, convertible, etc.).
Par value vs. no-par stock — par value is a nominal amount per share set in
articles of incorporation. For no-par stock, entire issuance price posts to
Common Stock or APIC per board resolution.

**Equity accounts driven by entity type**:
- C-corp: Common Stock (3000), APIC (3100), Retained Earnings (3200), Treasury Stock (3300), AOCI (3400), Dividends Declared (3500)
- S-corp: Shareholder Equity, AAA (accumulated adjustments account) tracking — not native in most accounting software
- LLC/Partnership: Member Capital accounts, Distributions accounts

### Ownership Concentration and Tax Implications

**Closely-held corporation**: Five or fewer individuals own >50% of stock
(with attribution). Triggers heightened scrutiny for:
- Accumulated earnings tax (IRC 531-537) — $250K credit threshold ($150K for PSCs)
- Personal holding company tax (IRC 541-547) — if also 60%+ of adjusted ordinary gross income is PHC income
- Related-party transaction rules (IRC 267) — loss disallowance, accrual-to-cash timing mismatch
- Reasonable compensation challenges from IRS

**Controlled group**: Parent-subsidiary (80%+ ownership chain), brother-sister
(5 or fewer persons own 80%+ of each corp), or combined. Tax implications:
shared Section 11 tax brackets (single bracket set), shared $250K AET credit,
shared Section 179 limit, consolidated return eligibility.

### Constructive Ownership (IRC 267(c))

Attribution rules expand "ownership" beyond direct holdings for determining
related-party status: from family (spouse, siblings, ancestors, lineal
descendants), from partnerships (proportionate share), from estates/trusts
(beneficiary interest), from corporations (50%+ shareholder attributed
proportionate share), and option attribution. No re-attribution from family
to family. Always apply constructive ownership before concluding parties are
unrelated.

## Foreign Ownership and Form 5472

A 25% foreign-owned U.S. corporation with reportable transactions with a
foreign related party must file Form 5472. Since 2017, this also applies to
foreign-owned U.S. disregarded entities.

**Reportable transactions**: sales/purchases of property, rents, royalties,
services, commissions, interest, insurance premiums, loan balances, and
changes in related-party debt. Must report even if transactions are at arm's
length — reporting obligation is separate from pricing obligation.

**Penalty**: $25,000 per form for failure to file or substantially incomplete
filing (post-2017; was $10,000 pre-TCJA). Additional $25,000 per 30-day
period after IRS notification, with no cap. Penalty applies per form per year
— multiple foreign related parties multiply the exposure. Reasonable cause
defense is narrow.

A separate Form 5472 is filed for each foreign related party. Filed with
Form 1120; due date follows the income tax return including extensions.

**Determination checklist**:
1. Does any foreign person or entity hold 25%+ of the corporation's stock (directly or constructively)?
2. If yes, did the corporation have any reportable transactions with that foreign related party during the tax year?
3. If both yes: Form 5472 required — one per foreign related party

## Officers and Directors

### Officer Information for Tax Compliance

Form 1120 Schedule E requires disclosure for each officer: name, SSN, percent
of time devoted to business, percent of stock owned (common and preferred
separately), and amount of compensation. This data feeds IRS automated
screening.

**Common audit triggers on Schedule E**:
- Zero officer compensation when the corporation has revenue
- Compensation exceeding 50% of gross receipts for a small corporation
- Dramatic year-to-year swings without documented business justification
- Compensation far above industry medians for the company's size

### Officer Compensation Framework

For C-corps, officer compensation is a deductible expense (Line 12, Form 1120).
IRS scrutinizes whether compensation is excessive — disguised dividends that let
the corporation deduct more than arm's-length amounts.

IRS uses a multi-factor analysis: training/experience, duties/responsibilities,
time/effort devoted, dividend history, comparable business compensation,
compensation as percentage of gross/net income, company character/condition,
documented compensation formula, and conflict of interest (officer who sets
own pay as controlling shareholder).

**The independent investor test**: Would a hypothetical outside shareholder be
satisfied with their return on investment after officer compensation is paid?
If compensation consumes most profits leaving no reasonable shareholder return,
it may be excessive.

**Documentation requirements**: Written employment agreement (signed before
the tax year), board resolution referencing comparable data, compensation
study or benchmarking, time records, and written job description.

### Board and Corporate Governance Records

Maintain: articles of incorporation, bylaws (or operating agreement for LLCs),
board meeting minutes, organizational resolutions (adopting bylaws, appointing
officers, authorizing bank accounts, setting fiscal year), stock certificates
or membership certificates, shareholder agreements, and any amendments.

## State Filing Obligations

### Florida

**Corporation formation**: Articles of Incorporation filed with FL Division of
Corporations (sunbiz.org). Filing fee: $35 (online) + $35 registered agent
designation. Annual report: $150, due May 1. Late annual report: $400 late fee.
Failure to file results in administrative dissolution.

**LLC formation**: Articles of Organization. Filing fee: $100 (online) + $25
registered agent designation. Annual report: $138.75, due May 1.

**Florida corporate income tax**: 5.5% on C-corp taxable income (FL-apportioned
federal taxable income with FL adjustments). $50,000 exemption. Florida uses
single sales factor apportionment (post-2019). No personal income tax — pass-through
income not taxed at state level in Florida.

**S-corps in Florida**: Pass through and avoid FL corporate income tax entirely.
Florida does not impose an entity-level tax on S-corps.

### Registered Agent

Every entity must maintain a registered agent in its state of incorporation.
The registered agent receives service of process, state correspondence, and
compliance notices. Can be an individual with a physical FL address or a
registered agent service company. Update the registered agent with the state
if it changes — failure to maintain a registered agent can lead to
administrative dissolution.

## Related Party and Affiliated Entity Tracking

### Related Party Identification (IRC 267(b))

Related parties for loss disallowance and accrual-to-cash matching:
- Individual and >50%-owned corporation (direct or constructive)
- Two corporations in same controlled group (>50% common ownership)
- Corporation and partnership with same persons owning >50% of each
- Family members (siblings, spouse, ancestors, lineal descendants)
- Grantor and fiduciary of a trust
- Tax-exempt organization and controlling person

### Intercompany Transaction Compliance

All intercompany transactions must be at arm's length (Section 482). Methods:
comparable uncontrolled price (CUP), resale price, cost plus, comparable profits
(CPM), profit split. Written intercompany agreements must be in place before
transactions occur, covering nature/scope, pricing methodology, payment terms,
and allocation methodology.

**Intercompany loans** must charge adequate stated interest at or above the
applicable federal rate (AFR) per IRC 7872. Below-market loans trigger imputed
interest. No $10,000 gift loan exception for corporation-shareholder loans.

### Entity Relationship Diagram

For multi-entity structures, maintain a current ownership diagram showing:
each entity (legal name, EIN, entity type, state, fiscal year), ownership
percentages between entities, officer overlap, intercompany transaction types
and directions, and controlled group or affiliated group status.

## Entity Profile Change Events

Track these events because each triggers compliance actions across service lines:

- **New entity formation** — EIN application, state filing, COA setup, engagement letter, initial organizational resolutions
- **Entity type change** — S-election or revocation, LLC conversion, check-the-box election (Form 8832). Triggers new return type, possible short-period returns, different equity accounts
- **Ownership change** — Stock sale, redemption, issuance, gift, inheritance. Updates Schedule E, may trigger Form 5472 if foreign ownership crosses 25%, affects controlled group status and AET credit sharing
- **Officer change** — New appointment or departure. Update Schedule E, employment agreements, bank signatory cards, board resolutions
- **Fiscal year change** — Requires IRS approval (Form 1128) unless adopting calendar year. Creates a short-period return
- **Accounting method change** — Form 3115. Section 481(a) adjustment spread over 4 years (if positive), taken entirely in year of change (if negative)
- **State changes** — New state registration, nexus triggering, registered agent change, foreign qualification in additional states
- **Dissolution or liquidation** — Final returns (federal and state), asset distribution, state dissolution filing, EIN retirement

## Decision Points

1. **Entity type selection** — Retained earnings favor C-corp at 21%. Distribution-heavy businesses favor pass-through (especially with QBI deduction through 2025). QSBS exclusion (IRC 1202, 100% gain exclusion for C-corp stock held 5+ years) favors C-corp for startups planning stock sales. VC/institutional investors typically require C-corp.

2. **S-election timing** — Within 75 days of formation or by March 15 for calendar-year corps. Missed deadline: Rev. Proc. 2013-30 relief within 3 years 75 days. Verify eligibility: 100 shareholders max, US individuals/trusts only, single class of stock, calendar or permitted fiscal year.

3. **Is this a related party?** — Apply constructive ownership rules (IRC 267(c)) before concluding unrelated. Attribution from family, partnerships, estates/trusts, corporations, and options. Affects loss disallowance, accrual-to-cash timing, and transfer pricing requirements.

4. **Form 5472 required?** — 25%+ foreign ownership (direct or constructive) plus any reportable transaction with a foreign related party. $25,000 penalty per form per year for non-filing.

5. **AET exposure?** — Accumulated E&P exceeding $250K ($150K for PSCs) without documented reasonable business needs. The TCJA 21% rate makes retention attractive, increasing IRS scrutiny. Prepare a Bardahl working capital computation and document specific, definite, feasible plans for retained earnings via board resolutions.

6. **Reasonable compensation defensible?** — Document before the tax year begins: written employment agreement, board resolution with comparable data, benchmarking study. The independent investor test: do shareholders receive a reasonable return after officer compensation?

## Supporting References

Read these for deeper detail on specific entity profile topics:

- `references/client-onboarding.md` — Entity information gathering checklist and accounting system company setup procedures. Read the "Information Gathering Checklist" section for the complete data collection list (legal name, EIN, entity type, state of formation, fiscal year-end, articles of incorporation) and the "Company Setup" section for how entity type drives software configuration. Essential when onboarding a new entity. For platform-specific setup steps, delegate to `qbo-integration:qbo-coa`.
- `references/entity-selection.md` — Comprehensive entity type comparison with tax rate differentials, formation procedures (Florida-specific filing fees and steps), S-election mechanics (Form 2553 timing, Rev. Proc. 2013-30 late relief), QSBS analysis, and decision factors. Read when advising on entity formation, conversion, or when the current entity type is questioned. The "Effective Date Log" tracks legislative changes affecting entity selection math.
- `references/officer-compensation.md` — IRS multi-factor reasonable compensation analysis, independent investor test, Schedule E reporting requirements and audit triggers, documentation best practices (employment agreements, board resolutions, benchmarking sources), and audit defense strategies. Read when setting or defending officer compensation levels or when zero-compensation years appear in delinquent filings.
- `references/accumulated-earnings-tax.md` — AET computation mechanics, year-by-year rate table, accumulated earnings credit ($250K/$150K), reasonable business needs test (recognized vs. unreasonable indicators), Bardahl working capital formula (operating cycle computation, peak vs. average method), and PHC tax interaction. Read when a C-corp's retained earnings approach or exceed $250K or when evaluating dividend policy.
- `references/intercompany-transactions.md` — IRC 267(b) related-party definitions with constructive ownership rules, Section 267(a)(2) accrual-to-cash timing mismatch, Section 482 transfer pricing methods, Form 5472 filing requirements and $25,000 penalty, and intercompany loan rules (AFR, IRC 7872). Read when identifying related parties, structuring intercompany transactions, or determining Form 5472 obligations.
- `references/state-nexus.md` — Physical presence and economic nexus standards, P.L. 86-272 protection (and its limitations for service companies), Florida corporate income tax rules (5.5% rate, $50K exemption, single sales factor apportionment, NOL rules, estimated tax, filing deadlines), and multistate filing considerations. Read when evaluating state filing obligations or FL-specific tax questions.

## Cross-Plugin References

For entity setup and onboarding workflow:
- Invoke `firm-operations:engagement-management` for engagement letter requirements, client acceptance evaluation, pre-engagement screening, and the full onboarding lifecycle

For entity type tax advisory:
- Invoke `tax-prep:tax-planning` for entity selection analysis, officer compensation optimization, accumulated earnings tax planning, and tax planning strategies that depend on entity type

For entity-type-driven account structure:
- Invoke `accounting-foundation:chart-of-accounts` for how entity type determines equity accounts, COA template selection, and Form 1120 tax-line mapping

For platform-specific entity configuration:
- Invoke `qbo-integration:qbo-coa` for accounting system company setup (entity type selection, fiscal year, accounting method, feature configuration) and platform-specific account templates by entity type

## Cross-Plugin Consumers

- `bookkeeping:transaction-processing` — entity type determines posting rules and equity treatment
- `bookkeeping:compliance-reporting` — ownership structure drives 1099 and worker classification decisions
- `tax-prep:form-1120-prep` — EIN, entity type, fiscal year, officers for return header and Schedule E
- `tax-prep:tax-forms` — foreign ownership status determines Form 5472 requirement
- `tax-prep:tax-planning` — entity type and ownership drive planning strategy selection
- `tax-prep:state-returns` — state of incorporation and nexus determine filing obligations
- `financial-planning:strategic-advisory` — ownership structure affects M&A, succession, and compensation planning
- `firm-operations:engagement-management` — entity profile data populates engagement letters and onboarding checklists

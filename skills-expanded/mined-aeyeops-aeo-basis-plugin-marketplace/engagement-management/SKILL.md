---
name: engagement-management
description: >
  Contains verified engagement letter templates (AICPA SSTS No. 1, IRC 7216, limitation of
  liability clauses), client onboarding checklists, and billing/pricing model frameworks
  with collection escalation procedures. Engagement lifecycle, realization rate formulas,
  write-down analysis, client profitability metrics, scope change amendments, disengagement
  letters, welcome packages, year-end planning letters, missing information escalation
  cadence, and pre-engagement screening criteria. Consult when drafting or customizing an
  engagement letter, onboarding a new client, evaluating client acceptance or continuance,
  selecting a pricing model (hourly vs fixed-fee vs value-based vs subscription), setting
  up billing or invoicing, writing client communications (welcome package, tax organizer,
  deadline reminders, deliverable cover letters), handling scope changes or fee adjustments,
  calculating realization rates or client profitability, managing collection escalation for
  past-due invoices, or executing a formal client disengagement.
---

# Engagement Management

Operational skill for the full client engagement lifecycle -- from pre-engagement
screening through active service delivery to disengagement. Synthesized from firm
engagement letter standards, billing/pricing models, onboarding procedures, and
client communication frameworks.

## Engagement Letter Requirements

Every engagement starts with a signed letter. Separate letters per service line for
the same client (tax and bookkeeping get distinct letters to delineate scope and
liability). Reissue or reconfirm annually, even for recurring engagements.

### Required Elements (All Engagement Types)

- **Scope** -- enumerate specific services included; explicitly state exclusions. For tax: list each form and tax year. For bookkeeping: specify basis (cash/accrual), deliverables, software platform, transaction volume assumptions
- **Responsibilities** -- firm: prepare in accordance with professional standards, maintain confidentiality. Client: provide complete/accurate information, review and approve deliverables. State that firm relies on client-provided data without independent verification
- **Fees and payment** -- structure (fixed/hourly/value-based), billing frequency, payment terms (net 30, retainer, etc.), late payment consequences, out-of-scope hourly rate, fee adjustment clause for scope changes
- **Limitation of liability** -- cap at 1x-3x annual fees (Florida law permits; cannot disclaim gross negligence or willful misconduct), mutual indemnification, disclaim penalties from client-provided inaccurate data
- **Dispute resolution** -- mediation first, then arbitration or litigation; governing law and venue; prevailing-party attorney fees
- **Confidentiality** -- IRC Section 7216 restrictions on tax return information, firm WISP compliance, permitted disclosures (peer review, E&O insurance, subpoena), encrypted transmission requirements
- **Term and termination** -- specific period or tax year covered, written notice requirement (30 days), client responsible for fees on work completed, firm retains workpapers

### Form 1120 Letter Specifics

Specify all forms in scope (1120, Schedule L, M-1/M-3, Form 5472 if foreign-owned,
state returns). Address: estimated tax calculations (included or not), IRS/state
notice response, e-filing authorization (Form 8879), automatic extension filing
(Form 7004) if information not received by stated deadline, delinquent filing year
range and advisory-only penalty estimates.

### Bookkeeping Letter Specifics

Define accounting basis, deliverable schedule (monthly/quarterly statements, reconciliations,
AR/AP aging), accounting system subscription ownership (firm-paid vs. client-paid), transaction volume
assumptions with overage fees, document delivery method and deadlines, monthly close and
statement delivery cutoff dates. State explicitly: bookkeeping is not an audit, review,
or compilation -- no assurance provided.

## Client Acceptance and Screening

### New Client Evaluation

Before accepting any engagement:

1. Verify identity (government ID for individuals, corporate documents for entities)
2. Assess risk: industry, complexity, prior compliance history, prior accountant relationship
3. Check conflicts of interest
4. Obtain and review prior-year returns for red flags
5. If terminated by prior firm, contact predecessor (with client consent per AICPA standards)
6. Evaluate team capacity against client complexity and volume
7. Screen for red flags: prior accountant fired unexpectedly, unexplained IRS notices, reluctance to share financials, unrealistic fee expectations

Decline or price for risk if red flags present.

### Annual Continuance Evaluation

- Review fee realization and write-downs for the client
- Assess cooperation level (document delivery timeliness, responsiveness)
- Evaluate risk changes (new IRS audit, litigation, financial distress)
- Document the continuance decision in the permanent file

## Client Onboarding

### Information Gathering Checklist

**Entity details**: legal name, EIN, entity type, state of formation, fiscal year-end, articles of incorporation

**Financial history**: prior 2+ years tax returns, existing books (cloud accounting software/desktop/spreadsheets/none), current year partials, open AR/AP aging

**Banking**: all bank accounts and credit cards (institution, type, last 4), loan statements with amortization, merchant processors (Stripe, Square, PayPal), POS systems

**Payroll**: provider, employee count (W-2) and contractor count (1099), pay frequency, states where employees work

**Tax/compliance**: sales tax permits and registered states, prior IRS/state notices, pending audits

### Accounting System Setup Sequence

For platform-specific setup steps, invoke `qbo-integration:qbo-bookkeeping`.

1. Create company or accept accountant invitation (use legal name, not DBA)
2. Set industry, entity type, fiscal year start, accounting method (match prior returns)
3. Enable class/location/project tracking as needed
4. Build chart of accounts from firm template -- do not accept system defaults
5. Enter opening balances (from prior Schedule L or year-end trial balance)
6. Link bank/CC accounts; set import start date to engagement start
7. Create bank rules for recurring transactions; match to prevent duplicates
8. Set up user access (principle of least privilege; remove prior accountants)
9. Configure recurring transactions (scheduled for fixed, reminder for variable)

### Welcome Package

Send immediately upon signed engagement letter:

- Signed engagement letter copy
- Firm overview and contact sheet (primary contact, hours, emergency protocol)
- Secure portal access instructions with document upload guide
- Entity-specific document checklist
- Communication expectations (response times, preferred channels, meeting cadence)

### First-Month Deliverables

1. Reconciled books (all bank and CC accounts)
2. Financial statements (P&L and Balance Sheet)
3. Open items list (unresolved transactions, missing docs, client questions)
4. COA summary for client confirmation
5. Onboarding close-out memo (setup decisions, assumptions, for permanent file)

## Pricing Models and Selection

### Model Comparison

- **Hourly** -- bill at predetermined rate by staff level (partner > manager > senior > staff). Best for: first-year engagements, variable-scope consulting, IRS audit defense, delinquent filing catch-up. Advantage: fair for unpredictable scope. Disadvantage: penalizes efficiency, creates fee uncertainty
- **Fixed fee** -- predetermined fee for defined scope. Best for: recurring returns with stable complexity, standard bookkeeping packages, multi-year client relationships. Requires accurate scope definition and a clause for material scope changes
- **Value-based** -- fee based on value delivered (tax savings, risk reduction, time savings). Best for: tax planning with quantifiable savings, advisory services, complex entity structuring. Requires strong client communication about value delivered
- **Subscription** -- fixed monthly fee covering bundled services. Best for: bookkeeping clients, small businesses wanting comprehensive coverage, advisory retainers. Smooths cash flow seasonality for firm and client

### Pricing Selection Logic

Default to **hourly for year one** to establish a baseline, then convert to **fixed fee in year two** with data-driven pricing.

Complexity drivers that increase price: multi-state filing, foreign ownership (Form 5472), delinquent multi-year filings, high asset/depreciation complexity, related-party transactions, aggressive audit-risk positions.

Risk adjustments: new client premium (setup + uncertainty), delinquent filer premium, uncooperative client premium, rush/expedited premium.

### Service-Line Pricing Guidelines

**Tax (Form 1120)**: simple single-state = fixed fee; moderate multi-state with depreciation = fixed fee with complexity tier; complex foreign-owned or delinquent = hourly or premium fixed fee

**Bookkeeping**: monthly transaction-band pricing (0-100, 101-250, 251+); include reconciliation and statements; exclude payroll, 1099 prep, sales tax filing (price separately); if firm pays accounting system subscription, include with markup

**Advisory**: value-based for tax planning tied to projected savings; hourly for ad-hoc consulting; retainer for ongoing advisory; project-based fixed fee for entity restructuring

**Bundling discount**: 5-10% for clients combining tax + bookkeeping improves retention and smooths revenue.

## Financial Metrics

### Realization Rate

Realization = fees collected / standard fees billed. Industry benchmark: 85-95%. Below 80% signals systemic pricing or collection problems. Track by engagement type, client, staff member, and service line.

### Write-Down Analysis

Track write-down reasons: scope underestimate, staff inefficiency, client goodwill, competitive pressure. Persistent write-downs for a client = mispricing (raise fees or disengage). Persistent write-downs for a service line = systemic issue. Target: under 10% of total billings.

### Effective Hourly Rate

For fixed-fee engagements: fee collected / actual hours spent. Compare to firm target rate. Consistently below target = fee too low or process too slow. Track across years.

### Client Profitability

Revenue minus direct costs minus allocated overhead. Bottom 10-20% of clients typically destroy profitability. Unprofitable clients require: fee increase, scope reduction, process improvement, or disengagement. High revenue does not guarantee high profitability.

## Billing and Collection

### Invoice Timing by Model

- **Hourly** -- monthly or upon completion, whichever is shorter
- **Fixed fee** -- on delivery, or 50% upfront / 50% on delivery for larger engagements
- **Subscription** -- monthly on consistent date; auto-payment (ACH/CC) preferred
- **Retainer** -- collect before work begins; replenish when balance falls below threshold

### Invoice Standards

Clear service descriptions (not vague "professional services"), reference engagement letter and agreed fee structure, itemize out-of-scope charges separately with explanation, include payment terms and accepted methods.

### Collection Escalation

- **30 days past due** -- automated reminder email
- **60 days** -- phone call from engagement manager; assess suspending current work
- **90 days** -- written demand from firm principal; suspend non-essential services
- **120+ days** -- final demand; refer to collections or write off; consider disengagement

Never hold a client's tax return for unpaid fees (AICPA ethical violation). Firm may retain its own workpapers but must provide client records upon request (AICPA ET 1.400.200).

## Client Communication Cadence

### Engagement Status Updates

**Tax preparation milestones**: documents received (in queue) -> in preparation (draft ETA) -> in review (quality review) -> ready for delivery (portal) -> filed (confirmation number)

**Bookkeeping monthly**: close completed -> financial summary (3-5 bullets: revenue, net income, cash, notable items) -> open items requiring client input

### Missing Information Escalation

1. **Initial request** -- itemized list with specific descriptions (account numbers, date ranges), 2-week deadline
2. **2-week follow-up** -- restate outstanding items, offer call if items unclear
3. **4-week notice** -- warn extension may be needed if items not received by date
4. **6-week final** -- extension filed/will file; request items at earliest opportunity

### Deadline Reminder Schedule

- **Estimated taxes** -- 2 weeks before due date with amount, payment method (EFTPS/state portal), safe harbor status
- **Extension filing** -- 30 days before original due date; note extension to file is not extension to pay
- **Return filing** -- 60 days (provide remaining docs by 30 days out), 30 days (status update), 14 days (ready for review or awaiting items)
- **1099 filing** -- November (W-9 collection reminder), January 15 (confirm vendor info complete for Jan 31 deadline)

### Year-End Planning Letter

Send October-November for calendar-year corporations. Content: tax law changes affecting client, year-end strategies (acceleration/deferral), retirement plan contribution deadlines, estimated tax review, document gathering timeline, numbered action items for client decisions.

### Deliverable Cover Letter

Include: summary of deliverables, key highlights (tax due/refund, effective rate, prior-year changes), client action items (sign/approve Form 8879, make estimated payments), estimated tax payment schedule with due dates, next steps. Deliver via secure portal with email notification -- never email returns as attachments. Offer 15-30 minute delivery meeting for complex returns.

## Scope Management and Change Orders

Material scope changes during engagement require a written amendment or new engagement letter. The original letter should include a clause allowing fee adjustment for scope changes or unforeseen complexity. Out-of-scope work is billed at the hourly rate specified in the engagement letter. Document scope change requests and approvals in the practice management system.

## Disengagement

### Procedures

1. Issue formal disengagement letter (certified mail or documented electronic delivery)
2. Specify effective date and which services are ceasing
3. State any remaining obligations (e.g., completing current-year return)
4. Inform client of upcoming deadlines to handle with successor
5. Return client-provided original documents promptly; firm retains workpapers
6. Withdraw pending powers of attorney (Form 2848, CAF withdrawal)
7. Revoke e-file authorizations
8. Cooperate with successor firm (provide prior return copies with client authorization)
9. Collect outstanding balance for services through disengagement date

### When to Disengage

Consistently unprofitable after fee adjustment attempts, uncooperative, or creates disproportionate risk. Requires partner approval.

## Supporting References

Read these for full templates, checklists, and authoritative citations:

- `references/engagement-letters.md` -- AICPA standards (SSTS No. 1, ET 1.310.001), required letter elements by engagement type, Form 1120 and bookkeeping letter specifics, limitation of liability guidance, client acceptance/continuance criteria, disengagement letter requirements, and decision points for fee structure and arbitration clauses
- `references/billing-pricing.md` -- detailed pricing model comparison with advantages/disadvantages, complexity drivers and risk-based pricing adjustments, financial metrics formulas (realization, write-downs, effective hourly rate, client profitability), billing cycle procedures, collection escalation, service-line pricing guidelines, and AICPA/IRS fee-related authoritative references
- `references/client-communications.md` -- complete communication templates for welcome package, C-corp tax organizer contents, year-end planning letter outline, missing information escalation cadence with sample language, deadline reminder schedules, deliverable transmittal cover letter format, engagement status update milestones, annual review meeting agenda, and disengagement letter required content
- `references/client-onboarding.md` -- pre-engagement screening criteria, information gathering checklist by category, accounting system company setup sequence, chart of accounts setup procedure, opening balance entry approaches (OBE, historical JE, import/migration), bank connection and bank rule setup, user access roles, recurring transaction configuration, first-month deliverables, and decision points for existing books, desktop migration, catch-up, and multi-entity scenarios

## Cross-Plugin References

- Invoke `accounting-foundation:entity-profile` for corporate entity details needed during onboarding and engagement letter preparation
- Invoke `qbo-integration:qbo-coa` for chart of accounts setup during bookkeeping onboarding
- Invoke `qbo-integration:qbo-bookkeeping` for QBO-specific onboarding configuration

## Cross-Plugin Consumers

- `bookkeeping:transaction-processing` -- references engagement scope for service boundaries
- `bookkeeping:catchup-bookkeeping` -- references onboarding for catch-up pricing and scope
- `tax-prep:form-1120-prep` -- references engagement letter for return scope
- `tax-prep:tax-compliance` -- references deadline communication cadence
- `financial-planning:strategic-advisory` -- references advisory pricing models
- `firm-operations:practice-management` -- receives engagement for workflow assignment
- `firm-operations:quality-compliance` -- references engagement review standards

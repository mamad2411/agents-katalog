---
name: compliance-reporting
description: >
  Contains verified 1099 decision trees (NEC vs MISC classification, corrected filing
  Type 1/Type 2 procedures), B-notice response protocols, and sales/use tax nexus
  thresholds that produce more precise answers than reasoning from general training alone.
  W-9 reportability, backup withholding, e-file mandate, economic nexus, exemption
  certificates, use tax self-assessment, marketplace facilitator rules. Consult when
  asked "does this vendor need a 1099", resolving B-notices, preparing corrected filings,
  evaluating sales tax nexus, or determining filing thresholds by tax year.
---

# Compliance Reporting

Operational procedures for recurring bookkeeping-driven compliance obligations:
information return filing (1099 series) and sales/use tax reporting. Content is
synthesized from firm reference materials and tracks law-indexed effective dates.

## 1099 Reporting

### Form Selection

**1099-NEC** — nonemployee compensation: contractor and freelancer payments, attorney
service fees. Box 1 reports aggregate payments at or above the threshold; Box 4 reports
backup withholding.

**1099-MISC** — everything that is not services: Box 1 rent, Box 2 royalties ($10+),
Box 3 other income, Box 6 medical/health care payments, Box 10 gross proceeds to
attorneys (distinct from attorney service fees, which go on NEC).

The dividing line: **services = NEC; rent/royalties/other = MISC**. A single payee can
receive both forms in the same tax year for different payment types.

**1099-INT** and **1099-DIV** — interest and dividend payments. Less common in standard
bookkeeping but may arise for C-corps with intercompany notes or investment income
distributions.

### Reporting Thresholds

- **TY 2024–2025**: $600 general threshold; $10 for royalties
- **TY 2026+**: $2,000 general threshold (One Big Beautiful Bill Act, Sec. 110501, July 2025); royalty threshold unchanged at $10

Track thresholds per tax year — a payment stream that was reportable last year may fall
below the new threshold.

### W-9 Collection and Vendor Reportability

1. Request W-9 **before first payment** — never pay without one on file
2. Validate completeness: legal name, entity type, TIN (SSN or EIN), address, signature
3. **Entity type determines reportability**:
   - Always reportable: sole proprietors, partnerships, single-member LLCs
   - Generally exempt: C-Corps and S-Corps
   - Exceptions to corporate exemption: legal fees (any entity) and medical/health care payments
4. Retain W-9 for 4 years after the last return filed using that TIN
5. Vendor refuses W-9 — initiate backup withholding at 24%; document every solicitation attempt

For vendor setup procedures and payment method tracking, invoke `bookkeeping:transaction-processing`.

### Backup Withholding

Rate: **24%**. Triggers: vendor fails to furnish TIN, IRS issues B-notice for incorrect
TIN, or IRS notifies vendor is subject to withholding. Report withheld amounts in Box 4
of the applicable 1099. Deposit via **Form 945** (annual) by January 31.

### B-Notice Response Protocol

**First B-Notice (CP2100)**: send solicitation letter within 15 business days. Payee has
30 days to respond with corrected W-9. Begin backup withholding if no response.

**Second B-Notice** (within 3 years of first): payee must provide TIN validation directly
from SSA or IRS — a new W-9 alone is insufficient.

**Proactive defense**: use the IRS TIN Matching Program before filing to catch mismatches
early.

### Filing Deadlines

- **1099-NEC**: January 31 — paper, e-file, and recipient copies. No automatic extension.
- **1099-MISC**: February 28 (paper) / March 31 (e-file). 30-day extension via Form 8809. Recipient copies due January 31.

### Electronic Filing Mandate

Effective TY 2024: filers issuing **10 or more information returns** (all types combined —
NEC, MISC, INT, W-2, etc.) **must e-file**. Prior threshold was 250. File via IRS IRIS
(free) or third-party services.

### Corrected 1099 Filing

**Type 1 correction** (wrong amount or code): file corrected form with the "CORRECTED"
box checked, showing correct amounts.

**Type 2 correction** (wrong TIN, name, or form type): two-step process — file a
corrected form with zeroes to void the original, then file a new form with correct
information (not marked as corrected).

### Common 1099 Errors to Prevent

- Misrouting legal fees (MISC Box 10 vs. NEC Box 1 — services go on NEC)
- Including reimbursed expenses (report fees only under accountable plans)
- Transposed or incorrect TIN (use TIN Matching before filing)
- Filing for exempt entities (C-Corps when no exception applies)
- Including credit card payments (payment processor reports via 1099-K; payer does not duplicate on NEC)

### 1099 Decision Logic

- W-9 shows C-Corp → generally no 1099 (exception: legal fees, medical payments)
- Payment via credit card/debit card/PayPal → exclude from 1099 (processor handles via 1099-K)
- No W-9 returned → begin 24% backup withholding; document solicitation attempts
- Foreign vendor with no US TIN → no 1099; may require 1042-S (invoke `tax-prep:tax-planning` for guidance)
- Contractor paid below threshold → no 1099 required; maintain records for potential aggregation across payment types
- Worker classification uncertain → invoke `tax-prep:tax-planning` for employee vs. contractor analysis

## Sales and Use Tax

### Nexus Determination

**Physical presence nexus**: office, warehouse, store, employees (including remote
workers), inventory stored in-state (including Amazon FBA), equipment, or sales
representatives.

**Economic nexus** (post-*Wayfair* 2018): states can require collection based on economic
activity alone. Typical threshold: **$100K in sales OR 200 transactions** in the current
or prior calendar year. Some states are sales-only (e.g., Texas at $500K). Once exceeded,
registration is mandatory even with no physical presence.

For entity-level details that affect nexus (registered states, physical locations, entity
type), invoke `accounting-foundation:entity-profile`.

### Use Tax Self-Assessment

When a business purchases taxable items and the seller does not charge sales tax, the
buyer owes **use tax** at the same rate as the home-state sales tax. Common triggers:
out-of-state online purchases, trade show equipment, supplies from non-collecting sellers.

Booking: record liability when purchased; remit on the regular sales tax return (separate
line). Review expense transactions monthly for untaxed purchases of taxable goods.

### Marketplace Facilitator Rules

All 45 sales-tax states plus DC have marketplace facilitator laws. Amazon, eBay, Etsy,
and Walmart Marketplace collect and remit on behalf of third-party sellers. **Direct
sales** (own website, phone orders, in-person) remain the seller's collection
responsibility. Track marketplace vs. direct sales separately.

### Exemption Certificate Management

1. Collect valid certificate **before or at time of exempt sale** (multi-state: Streamlined or Multi-Jurisdiction form accepted)
2. Validate: buyer name, address, state, exemption reason, signature, active permit number
3. Use blanket certificates for ongoing relationships; single-purchase certificates for one-time sales
4. Retain certificates 3–4 years after last covered sale (state-dependent; e.g., Florida: 3 years, California: 4 years)
5. Common exemption types: resale, manufacturing, agriculture, government, nonprofit (not all states exempt nonprofits)

### State-Specific Rules

State-specific rules vary. Key items to verify per state:

- **Base rate and local surtax structure** — combined rates differ by jurisdiction (state base + county/city/district add-ons)
- **Taxable service definitions** — most states tax tangible goods by default; service taxability varies widely (some states tax few services, others tax most)
- **Dealer collection allowances** — some states offer a discount for timely filing and remittance
- **Filing frequency thresholds** — assigned by the state based on annual tax liability (monthly, quarterly, semi-annually, or annually)
- **Key exemptions and certificates** — common categories include resale, manufacturing, agriculture, government, and nonprofit (not all states exempt all categories)
- **Form numbers and due dates** — each state has its own return form, due date schedule, and EFT requirements

Common state forms include DR-15 (Florida), ST-3 (New Jersey), ST-100 (New York), and ST-1 (Illinois). Consult the relevant state department of revenue for current forms and instructions.

### Filing and Remittance Procedure

1. Run Sales Tax Liability report; reconcile tax collected to GL
2. Calculate use tax owed on untaxed purchases identified during the period
3. Apply credits: overpayments from prior periods, bad debt deductions
4. Subtract collection allowance if eligible (where state offers one; timely filing typically required)
5. File return by due date per state schedule
6. Remit payment (EFT required above state-specific thresholds)
7. Record in GL: debit Sales Tax Payable (2xxx), credit Cash/Checking (1xxx)

For GL account structure, invoke `accounting-foundation:chart-of-accounts`.

### Sales Tax Decision Logic

- Client sells in 1–2 states → manage manually in accounting platform
- Client sells in 5+ states → recommend third-party sales tax automation services (e.g., Avalara, TaxJar)
- Economic nexus threshold exceeded → register immediately; back-tax exposure accrues daily
- Customer claims verbal exemption → require written certificate before exempting the sale
- Nexus questionnaire received from a state → do not ignore; consult CPA before responding
- Zero-tax-due period → file the return anyway; non-filing triggers delinquency notices
- Sales only through marketplaces → marketplace collects and remits; still file zero return if registered

### Audit Readiness

Maintain at all times: exemption certificate file organized by customer, copies of all
filed returns with payment proof, nexus analysis documentation, taxability research memos,
and monthly reconciliation of sales per books to sales per returns. Common audit triggers:
consistently late filings, large refund claims, industry-targeted audits, nexus
questionnaire responses.

## Platform-Specific Workflows

For platform-specific 1099 and sales tax workflows, invoke `qbo-integration:qbo-bookkeeping`.

## Effective Date Tracker

- **TY 2020**: 1099-NEC reintroduced; nonemployee compensation moved from MISC Box 7 (IRS Rev. Proc. 2019-29)
- **June 2018**: Economic nexus authorized (*South Dakota v. Wayfair*, 585 U.S. 162)
- **2018–2021**: All 45 sales-tax states + DC enacted marketplace facilitator laws
- **TY 2024**: E-file mandate threshold lowered from 250 to 10 returns (T.D. 9972)
- **TY 2026**: 1099 general reporting threshold raised from $600 to $2,000 (One Big Beautiful Bill Act, Sec. 110501)

## Supporting References

Read these for deeper detail on specific topics:

- `references/1099-compliance.md` — Complete 1099 procedures: NEC vs. MISC classification, W-9 collection protocol, backup withholding mechanics, B-notice response workflow, e-file mandate details, and corrected filing procedures. Read when handling B-notice responses, researching corrected filing procedures, or verifying threshold changes by tax year.
- `references/sales-use-tax.md` — Sales and use tax compliance: nexus analysis (physical and economic), exemption certificate management, state-specific rule templates, marketplace facilitator laws, filing/remittance procedures, and audit preparation. Read when evaluating nexus for a new state, managing exemption certificates, or preparing for a sales tax audit.

## Cross-Plugin References

For related knowledge outside this skill:

- Invoke `accounting-foundation:chart-of-accounts` for GL account structure — particularly liability accounts (2xxx) for sales tax payable and expense accounts mapped to 1099 boxes
- Invoke `accounting-foundation:entity-profile` for entity details affecting compliance: registered states, entity type (determines 1099 exemptions), physical locations (nexus triggers)
- Invoke `tax-prep:tax-planning` for worker classification analysis (employee vs. contractor), foreign vendor reporting (1042-S), and state tax compliance beyond sales tax
- Invoke `bookkeeping:transaction-processing` for vendor payment tracking, payment method classification, and expense categorization that feeds 1099 and sales tax reporting

---
name: za-vat-return
description: "> Use this skill whenever asked about South African VAT returns for self-employed individuals or small businesses. Trigger on phrases like \"South Africa VAT\", \"VAT201\", \"SARS VAT\", \"15% VAT\", \"eFiling VAT\", \"zero-rated SA\", \"VAT vendor\", or any question about VAT filing, computation, or registration for vendors in South Africa. Covers the 15% standard rate, zero-rated and exempt supplies, R2.3M registration threshold, VAT201 return, and bimonthly filing via SARS eFiling. ALWAYS read this skill before touching any South African VAT work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: ZA
  category: international
  quality: accountant-reviewed
  openaccountants_url: "https://openaccountants.com/skills/za-vat-return"
  tax_year: 2026
  obligation: CT
  reviewed_by: "Werner Britz, CA(SA)"
---

# South Africa VAT Return (VAT201) -- Self-Employed Skill v2.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | South Africa |
| Tax | Value-Added Tax (VAT) at 15% |
| Currency | ZAR only |
| Primary legislation | Value-Added Tax Act 89 of 1991 (VAT Act) |
| Supporting legislation | Tax Administration Act 28 of 2011 (TAA); SARS interpretation notes |
| Tax authority | South African Revenue Service (SARS) |
| Filing portal | SARS eFiling (efiling.sars.gov.za) |
| Default filing frequency | Bimonthly (Category A) |
| Filing deadline | Last business day of month following period end (eFiling) |
| Contributor | Open Accountants Community |
| Validated by | Werner Britz CA(SA), Spurwing CFO |
| Validation date | May 2026 |
| Skill version | 2.1 |

### Rate Table

| Rate | Application |
|---|---|
| 15% | Standard rate (effective 1 April 2018) |
| 0% | Exports, basic foodstuffs, petrol/diesel, international transport, agricultural inputs, going concern (s 11(1)(e)), gold to SARB/bank, illuminating paraffin |
| Exempt | Financial services, residential rental, public transport, educational services, childcare |

### Tax Fraction

For VAT-inclusive amounts at 15%: **15/115**.

### Key Thresholds

| Item | Amount (ZAR) |
|---|---|
| Compulsory registration | R2,300,000 taxable supplies in any 12-month period (from 1 April 2026) |
| Voluntary registration | R120,000 taxable supplies in any 12-month period (from 1 April 2026) |
| Payments basis eligibility | R2,500,000 threshold applies to natural persons only. Full s 15(2) list includes public authorities, water boards, municipal entities, municipalities, associations not for gain, foreign suppliers of electronic services, SABC Ltd, and natural persons under R2,500,000 |
| Full tax invoice threshold | R5,000 |
| No invoice required | Supplies under R50 |

### Conservative Defaults

| Ambiguity | Default |
|---|---|
| Registration status unknown | STOP -- do not compute |
| Accounting basis unknown | Invoice basis (default) |
| Supply classification unknown | Standard-rated at 15% |
| Private use proportion unknown | 0% recovery |
| Second-hand goods claim | Not claimable until documentation confirmed |

---

## Section 2 -- Required Inputs and Refusal Catalogue

### Required Inputs

**Minimum viable:** Bank statement for the VAT period in CSV, PDF, or pasted text, plus confirmation of VAT registration status and vendor number.

**Recommended:** Sales invoices, purchase invoices with VAT shown, prior period VAT201.

**Ideal:** Complete invoice register, filing category confirmation, prior year VAT reconciliation.

### Refusal Catalogue

**R-ZA-1 -- Below threshold.** "If taxable supplies have not exceeded R2,300,000 in any 12-month period (from 1 April 2026) and client is not voluntarily registered, no VAT obligations. Stop."

**R-ZA-2 -- Cross-border services (complex).** "Complex cross-border service transactions and customs VAT require specialist review. Escalate."

**R-ZA-3 -- VAT grouping.** "VAT group registrations are outside this skill scope. Escalate."

**R-ZA-4 -- Large-value complex transactions.** "Transactions involving property, construction, or financial instruments require specialist review. Escalate."

---

## Section 3 -- Transaction Pattern Library

### 3.1 Income Patterns (Credits)

| Pattern | Tax Line | Treatment | Notes |
|---|---|---|---|
| EFT FROM [client] / EFT CREDIT | Taxable supply | Output VAT at 15% | Standard electronic transfer |
| INSTANT MONEY / CASH DEPOSIT | Taxable supply | Revenue | Cash receipt |
| PAYFAST PAYOUT / PAYFAST SETTLEMENT | Taxable supply | Revenue | PayFast payment gateway |
| YOCO SETTLEMENT / YOCO PAYOUT | Taxable supply | Revenue | Yoco card machine settlement |
| SNAPSCAN PAYOUT | Taxable supply | Revenue | SnapScan mobile payment |
| ZAPPER SETTLEMENT | Taxable supply | Revenue | Zapper payment |
| CAPITEC / FNB / ABSA / NEDBANK / STD BANK CREDIT | Taxable supply | Revenue | Bank transfer income |
| INTEREST / INT EARNED | Exempt | NOT taxable | Bank interest -- financial service |
| SARS REFUND | EXCLUDE | Not income | Tax refund |
| LOAN DRAWDOWN | EXCLUDE | Not income | Loan proceeds |

### 3.2 Expense Patterns (Debits)

| Pattern | Expense Category | Treatment | Notes |
|---|---|---|---|
| OFFICE RENT / COMMERCIAL LEASE | Rent | Input VAT claimable | Business premises |
| ESKOM / CITY POWER / CITY OF CAPE TOWN | Utilities | Input VAT claimable | Electricity |
| TELKOM / VODACOM / MTN / CELL C / RAIN | Communications | Business portion claimable | Mixed use: apportion |
| ENGEN / SHELL / CALTEX / SASOL | Fuel | ZERO-RATED (s 11(1)(h)) -- no VAT on fuel | Lubricants, car-wash, shop purchases at fuel stations are 15% |
| TAKEALOT / MAKRO / GAME | Office supplies | Input VAT claimable | Business purchases |
| GOOGLE ADS / META / LINKEDIN | Advertising | Input VAT claimable | Digital advertising |
| UBER SA / BOLT SA / TAXI | Travel | EXEMPT (s 12(g)) -- fare is exempt; no input VAT claimable | Only the small booking fee (if separately shown) may carry input VAT |
| SARS INCOME TAX / SARS PAYE | EXCLUDE | Tax payment | Not deductible |
| SARS VAT PAYMENT | EXCLUDE | VAT payment | Not input tax |
| BANK CHARGES / FNB FEE / ABSA FEE | Input 15% | Input VAT claimable | Fee-based services are standard-rated per s 2(1) proviso; banks issue monthly VAT tax invoices |
| MOTOR CAR PURCHASE / LEASE / RENTAL (AVIS, EUROPCAR, HERTZ, BIDVEST) | BLOCKED | Input tax blocked under s 17(2)(c) | "Motor car" includes sedans, SUVs, double-cab bakkies, minibuses. Running costs (fuel, repairs) ARE claimable |
| CLIENT LUNCHES / ENTERTAINMENT / CORPORATE GIFTS | BLOCKED | Input tax blocked under s 17(2)(a) | Unless vendor is in the business of providing entertainment |
| CHECKERS / SHOPRITE / PICK N PAY / WOOLWORTHS / SPAR | Office supplies | Input VAT claimable if for resale | For office consumption (tea, coffee, staff fridge), input tax is BLOCKED under s 17(2)(a) entertainment block regardless of whether items are zero-rated or standard-rated. Only claimable where items are for resale |
| OWN TRANSFER / PERSONAL | EXCLUDE | Drawings | Not business |

### 3.3 Zero-Rated Supply Indicators

| Pattern | Treatment | Notes |
|---|---|---|
| EXPORT / INTERNATIONAL SHIPMENT | Zero-rated output | Goods exported from SA |
| BROWN BREAD / MAIZE MEAL / RICE / EGGS / MILK | Zero-rated | Basic foodstuffs |
| FUEL LEVY / PETROL / DIESEL | Zero-rated | Fuel levy applies instead |

### 3.4 Transport Patterns

| Pattern | Expense Category | Treatment | Notes |
|---|---|---|---|
| FLYSAFAIR / LIFT / CEMAIR | Domestic flights | Input VAT claimable | Domestic air travel is standard-rated at 15% |
| SA AIRLINK | Domestic flights | Input VAT claimable | Standard-rated |
| UBER SA / BOLT SA / TAXI | Local transport | EXEMPT (s 12(g)) | Fare is exempt; no input VAT. Only the booking fee (if separately shown) may carry input VAT |
| GREYHOUND / INTERCAPE | Long-distance bus | EXEMPT (s 12(g)) | Public road transport of fare-paying passengers |

### 3.5 Payment Processor Fees

| Pattern | Expense Category | Treatment | Notes |
|---|---|---|---|
| PAYFAST FEE / PAYFAST CHARGE | Payment processing | Input 15% | Standard-rated -- fee-based processing is not a financial service per s 2(1) proviso |
| YOCO FEE / YOCO CHARGE | Payment processing | Input 15% | Standard-rated -- fee-based processing is not a financial service per s 2(1) proviso |
| PEACH PAYMENTS FEE | Payment processing | Input 15% | Standard-rated -- fee-based processing is not a financial service per s 2(1) proviso |

---

## Section 4 -- Worked Examples

### Example 1 -- Standard Bimonthly Return

**Input:** Standard-rated supplies R500,000 (VAT-exclusive). Purchases R200,000 (VAT-exclusive, all standard-rated, valid invoices).

**Reasoning:**
Output VAT: R500,000 x 15% = R75,000. Input VAT: R200,000 x 15% = R30,000. VAT payable: R75,000 - R30,000 = R45,000. VAT-inclusive supply total: R575,000 (Field 1). VAT-inclusive purchase total: R230,000.

**Classification:** VAT payable R45,000 (Field 20).

### Example 2 -- Exporter in Refund Position

**Input:** Zero-rated exports R800,000. Purchases R300,000 (standard-rated).

**Reasoning:**
Output VAT: R0. Input VAT: R300,000 x 15% = R45,000. Refund: R45,000.

**Classification:** VAT refund R45,000.

### Example 3 -- Second-Hand Goods Purchase

**Input:** Vendor buys used equipment from non-vendor for R50,000 (no VAT charged).

**Reasoning:**
Notional input tax: R50,000 x 15/115 = R6,521.74. Claimable if documentation requirements are met (declaration from seller, proof of payment). Reported in Field 15 (input VAT on other goods/services).

**Classification:** Input tax R6,521.74 (Field 15). Flag for reviewer on documentation.

### Example 4 -- Bad Debt Relief

**Input:** Invoice for R23,000 (incl. VAT) written off after 14 months.

**Reasoning:**
Bad debt relief under s 22(1): debt outstanding over 12 months and written off. Relief: R23,000 x 15/115 = R3,000.

**Classification:** Input tax deduction R3,000.

### Example 5 -- Google Ads (Imported Services)

**Input:** Google Ads spend R50,000 for the period. Google now bills via SA-registered entity with SA VAT number and issues VAT tax invoices.

**Reasoning:**
Where Google bills via a South African entity registered for VAT and issues a valid tax invoice showing 15% VAT, the vendor claims input tax directly. VAT amount: R50,000 x 15/115 = R6,521.74. Reported in Field 15 (input VAT on other goods/services). If billed by a non-resident entity without SA VAT registration, the vendor must self-account for output VAT under s 7(1)(c) in Field 12 (imported services) and claim corresponding input in Field 15 if the service is for making taxable supplies.

**Classification:** Input tax R6,521.74 (Field 15) where billed by SA entity. If imported service: output in Field 12, input in Field 15.

---

## Section 5 -- Tier 1 Rules (When Data Is Clear)

### 5.1 VAT201 Return Fields

| Field | Description |
|---|---|
| 1 | Standard-rated supplies (VAT-inclusive, excluding capital goods) |
| 1A | Standard-rated capital goods supplied (VAT-inclusive) |
| 2 | Zero-rated supplies (excluding exports) |
| 2A | Zero-rated exported goods |
| 3 | Exempt and non-supplies |
| 4 | Output VAT on Field 1 (Field 1 x 15/115) |
| 4A | Output VAT on Field 1A (Field 1A x 15/115) |
| 5 | Commercial accommodation supplied for 28+ days (value) |
| 6 | Field 5 x 60% (deemed taxable portion) |
| 7 | Field 6 x 15/115 (VAT on deemed portion) |
| 8 | Sum of Fields 6 and 7 |
| 9 | Output VAT on commercial accommodation (Field 8 x 15%) |
| 10 | Change-in-use / second-hand goods exported (consideration) |
| 11 | Field 10 x 15/115 |
| 12 | Other output adjustments and imported services |
| 13 | Total output tax (4 + 4A + 9 + 11 + 12) |
| 14 | Input VAT on capital goods |
| 14A | Input VAT on imported capital goods |
| 15 | Input VAT on other goods/services |
| 15A | Input VAT on imported other goods/services |
| 16 | Change-in-use input adjustment |
| 17 | Bad debts (s 22 relief) |
| 18 | Other input adjustments |
| 19 | Total input tax (14 + 14A + 15 + 15A + 16 + 17 + 18) |
| 20 | Net VAT payable / refundable (13 - 19) |

### 5.2 Filing Categories

| Category | Frequency | Who |
|---|---|---|
| A | Bimonthly | Default for most vendors |
| B | Monthly | Taxable supplies > R30M/year |
| C | Six-monthly | Farming enterprises (by approval) |
| D | Annual | Small vendors (by approval) |
| E | Annual | Connected-party rental enterprises (by approval) |
| F | Four-monthly | Micro businesses on turnover tax |

### 5.3 Filing Deadlines

| Method | Deadline |
|---|---|
| eFiling | Last business day of month following period end |
| Manual (branch) | 25th of month following period end |

### 5.4 Payments Basis (s 15)

R2,500,000 threshold applies to natural persons only. Full s 15(2) list includes public authorities, water boards, municipal entities, municipalities, associations not for gain, foreign suppliers of electronic services, SABC Ltd, and natural persons under R2,500,000. Account for VAT when payment is made or received. Must apply to SARS.

### 5.5 Penalties (TAA Chapter 15)

| Offence | Penalty |
|---|---|
| Late filing | Fixed amount penalty (escalating scale) |
| Late payment | 10% of amount outstanding |
| Interest | Prescribed rate compounding monthly |
| Understatement | 10-200% depending on behaviour |

---

## Section 6 -- Tier 2 Catalogue (Reviewer Judgement Required)

### 6.1 Mixed Supplies Apportionment

Input tax must be apportioned when making both taxable and exempt supplies. Directly attributable input follows its supply. Residual input apportioned using revenue-based ratio. Flag for reviewer.

### 6.2 Imported Services (Reverse Charge, s 7(1)(c))

If foreign supplier is not VAT-registered in SA and service is consumed in SA, recipient must account for VAT. May claim corresponding input tax if for taxable supplies.

### 6.3 Second-Hand Goods Input Tax (s 16(3)(a)(ii))

Notional input tax: tax fraction (15/115) of consideration paid. Requires declaration from seller and proof of payment. Cannot exceed lesser of consideration paid or open market value. Flag for reviewer.

### 6.4 Change from Payments to Invoice Basis

When turnover exceeds R2,500,000. Transitional adjustments required. Flag for tax practitioner.

### 6.5 Motor vehicle -- is it a "motor car" as defined?

*What it shows:* Vehicle purchase, lease, rental, or maintenance payment. *What's missing:* Whether the vehicle is a "motor car" as defined in s 1 (objective test per IN 82 -- passenger area vs loading area). *Conservative default:* BLOCKED -- no input tax on supply of motor car. *Question:* "Is this a passenger vehicle (sedan, SUV, hatchback, double-cab bakkie, minibus)? If yes: input on purchase/lease/rental is blocked under s 17(2)(c). Running costs (fuel, repairs, insurance) are claimable for business use." Exception: vendor who continuously supplies motor cars in ordinary course (dealers, rental companies).

---

## Section 7 -- Working Paper Template

```
SOUTH AFRICA VAT WORKING PAPER (VAT201)
Vendor: _______________  VAT Number: ___________
Period: ___________  Category: A / B / C / D / E / F
Basis: Invoice / Payments

A. OUTPUT (SALES)
  A1. Standard-rated supplies (excl. VAT)        ___________
  A2. Output VAT (A1 x 15%)                     ___________
  A3. Zero-rated supplies                        ___________
  A4. Exempt supplies                            ___________

B. INPUT (PURCHASES)
  B1. Capital goods VAT                          ___________
  B2. Other purchases VAT                        ___________
  B3. Adjustments                                ___________
  B4. Total input VAT                            ___________

C. NET VAT
  C1. Output less input (A2 - B4)                ___________
  C2. VAT payable / refundable                   ___________

REVIEWER FLAGS:
  [ ] Registration and vendor number confirmed?
  [ ] Filing category confirmed?
  [ ] Accounting basis confirmed?
  [ ] Tax invoices held for all input claims?
  [ ] Second-hand goods documentation complete?
  [ ] Zero-rated vs exempt correctly distinguished?
```

---

## Section 8 -- Bank Statement Reading Guide

### South African Bank Statement Formats

| Bank | Format | Key Fields |
|---|---|---|
| FNB | CSV / PDF | Date, Description, Amount, Balance |
| ABSA | CSV | Date, Description, Debit, Credit, Balance |
| Standard Bank | CSV | Date, Description, Debit, Credit, Balance |
| Nedbank | CSV | Date, Description, Debit, Credit, Balance |
| Capitec | CSV | Date, Description, Debit, Credit, Balance |
| Investec | CSV | Date, Description, Debit, Credit, Balance |

### Key SA Banking Narrations

| Narration | Meaning | Classification Hint |
|---|---|---|
| EFT CREDIT / INWARD PAYMENT | Bank transfer in | Potential income |
| DEBIT ORDER / DEBI CHECK | Direct debit | Regular expense |
| POS / CARD PURCHASE | Point of sale | Expense |
| CASH DEPOSIT | Cash received | Income |
| SARS / RECEIVER OF REVENUE | Tax payment or refund | Exclude |
| BANK CHARGES / SERVICE FEE | Bank fee | Standard-rated 15% -- input claimable (s 2(1) proviso) |

---

## Section 9 -- Onboarding Fallback

If the client provides a bank statement but cannot answer onboarding questions immediately:

1. Classify all EFT credits from business sources as potential taxable supplies
2. Apply conservative defaults: invoice basis, standard-rated, 0% private recovery
3. Only claim input VAT where VAT is clearly evident
4. Flag all large purchases for capital goods review

Present these questions:

```
ONBOARDING QUESTIONS -- SOUTH AFRICA VAT
1. Are you registered as a VAT vendor? What is your VAT number?
2. What filing category are you (A bimonthly, B monthly, C six-monthly, D annual)?
3. Are you on invoice basis or payments basis?
4. What types of goods or services do you sell?
5. Do you make any zero-rated supplies (exports, basic foodstuffs)?
6. Do you make any exempt supplies (financial, residential rent, education)?
7. Do you purchase second-hand goods from non-vendors?
8. Do you import services from non-resident suppliers?
```

---

## Section 10 -- Reference Material

### Key Legislation

| Topic | Section |
|---|---|
| Imposition of VAT | VAT Act s 7 |
| Zero-rated supplies | VAT Act s 11 |
| Exempt supplies | VAT Act s 12 |
| Registration | VAT Act s 23 |
| Payments basis | VAT Act s 15 |
| Input tax | VAT Act s 16 |
| Tax invoices | VAT Act s 20 |
| Bad debts | VAT Act s 22 |
| Filing | VAT Act s 27, 28 |

### Known Gaps / Out of Scope

- Cross-border services (complex)
- Customs VAT on imports
- VAT grouping
- Large-value property transactions

### Changelog

| Version | Date | Change |
|---|---|---|
| 2.1 | May 2026 | Validated by Werner Britz CA(SA); corrected R2.3m registration threshold; corrected bank charges and payment processor fees to standard-rated; corrected VAT201 field structure; added motor car block; corrected Uber/Bolt to exempt; corrected fuel to zero-rated; added entertainment block; removed Kulula (ceased 2022) |
| 2.0 | April 2026 | Full rewrite to v2.0 structure; SA bank formats; local payment patterns (PayFast, Yoco, SnapScan); worked examples |
| 1.0 | 2025 | Initial version |

### Self-Check

- [ ] Registration and vendor number confirmed?
- [ ] Filing category and accounting basis confirmed?
- [ ] Tax fraction 15/115 used consistently?
- [ ] Zero-rated vs exempt correctly distinguished?
- [ ] Second-hand goods claims properly documented?
- [ ] Bad debt relief only after 12 months?

---

## PROHIBITIONS

- NEVER claim input tax on exempt supplies -- only taxable (including zero-rated) supplies qualify
- NEVER charge VAT if not registered as a vendor
- NEVER use a rate other than 15% for standard-rated supplies
- NEVER confuse zero-rated (input tax claimable) with exempt (input tax NOT claimable)
- NEVER claim input tax without a valid tax invoice (for supplies over R50)
- NEVER ignore the bimonthly filing deadline -- penalties apply from the first day late
- NEVER apply payments basis without SARS approval
- NEVER claim notional input on second-hand goods without proper documentation and declarations
- NEVER claim input on the supply (purchase, lease, rental) of a motor car as defined, unless within an exception under s 17(2)(c)
- NEVER claim input on entertainment, accommodation, or food and beverages unless the vendor is in the business of providing entertainment or the supply is to an employee away from usual place of work
- NEVER exclude bank service fees as exempt -- they are standard-rated and input claimable (s 2(1) proviso)
- NEVER omit output VAT on Seventh Schedule fringe benefits granted to employees under s 18(3)
- NEVER present calculations as definitive -- always label as estimated and direct client to a SARS-registered tax practitioner

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a registered tax practitioner, chartered accountant (CA(SA)), or equivalent licensed practitioner in South Africa) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/za-vat-return) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **accountant-reviewed**. Reviewed by Werner Britz, CA(SA). For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

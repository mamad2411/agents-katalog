---
name: south-africa-vat
description: "Use this skill whenever asked to prepare, review, or classify transactions for a South Africa VAT return (VAT201), classify transactions for South African VAT purposes, or advise on VAT registration and filing in South Africa. Trigger on phrases like \"South Africa VAT\", \"VAT201\", \"SARS VAT\", \"input tax South Africa\", \"output tax South Africa\", \"South African Revenue Service VAT\", or any SA VAT request. ALWAYS read this skill before touching any South Africa VAT work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: ZA
  category: international
  quality: accountant-reviewed
  openaccountants_url: "https://openaccountants.com/skills/south-africa-vat"
  tax_year: 2025
  obligation: CT
  reviewed_by: "Werner Britz, CA(SA)"
---

# South Africa VAT (VAT201) Skill v2.1

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 — Quick reference

| Field | Value |
|---|---|
| Country | South Africa (Republic of South Africa) |
| Tax | VAT (Value-Added Tax) |
| Currency | ZAR (South African Rand / R) |
| Tax year | Tax periods under s 27: Category A bimonthly (default); B monthly (>R30m); C six-monthly (farming <R1.5m); D annual (connected-party farming/rental); E annual (connected-party rental); F four-monthly (micro businesses on turnover tax). No quarterly category exists. |
| Standard rate | 15% |
| Zero rate | 0% (exports; basic foodstuffs (Schedule 2); international transport; certain farming inputs; petrol/diesel; illuminating paraffin; supply of enterprise as going concern (s 11(1)(e)); gold to SARB/bank) |
| Exempt | Financial services (narrow s 2 definition -- interest, exchange margins, life insurance, dealing in securities; fee-based services are STANDARD-RATED per s 2(1) proviso), residential rental, public road and rail transport (s 12(g)), educational services by recognised institutions, childcare, donated goods/services by associations not for gain. Short-term insurance is STANDARD-RATED, not exempt. |
| Registration threshold | ZAR 2,300,000 in any consecutive 12-month period (from 1 April 2026). Voluntary registration: ZAR 120,000. |
| Tax authority | SARS (South African Revenue Service) |
| Return form | VAT201 (eFiling) |
| Filing portal | SARS eFiling (https://efiling.sars.gov.za) |
| Filing frequencies | Category A bimonthly (default); Category B monthly (>R30m); Category C six-monthly (farming <R1.5m); Category D annual (connected-party farming/rental); Category E annual (connected-party rental); Category F four-monthly (micro businesses on turnover tax) |
| Filing deadline | Last business day of month following tax period (eFiling); 25th for paper (not recommended) |
| Tax invoice | VAT-compliant invoice — required for input tax |
| VAT number | Format: 4xxxxxxxx (10 digits starting with 4) |
| Contributor | Open Accountants Community |
| Validated by | Werner Britz CA(SA), Spurwing CFO |
| Validation date | May 2026 |
| Skill version | 2.1 |

### Key VAT201 fields

| Field | Meaning |
|---|---|
| 1 | Standard-rated supplies (VAT-inclusive, excluding capital goods) |
| 1A | Standard-rated capital goods supplied (VAT-inclusive) |
| 2 | Zero-rated supplies (excluding exports) |
| 2A | Zero-rated exported goods |
| 3 | Exempt and non-supplies |
| 4 | Output VAT on Field 1 (Field 1 x 15/115) |
| 4A | Output VAT on Field 1A |
| 5 | Commercial accommodation supplied for 28+ days |
| 9 | Output VAT on commercial accommodation |
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

### Conservative defaults

| Ambiguity | Default |
|---|---|
| Unknown rate on a sale | 15% standard |
| Unknown counterparty country | Domestic South Africa |
| Unknown export qualification | 15% until export evidence confirmed |
| Unknown business-use % (vehicle, entertainment) | 0% input tax. Note: for motor cars as defined, input is FULLY BLOCKED under s 17(2)(c) regardless of business use percentage. |
| Unknown whether tax invoice compliant | No input tax |
| Unknown whether zero-rated or exempt | Treat as taxable 15% |
| Unknown B2B vs B2C for cross-border | 15% if consumed in South Africa |

### Red flag thresholds

| Threshold | Value |
|---|---|
| HIGH single transaction | ZAR 50,000 |
| HIGH tax delta on single default | ZAR 7,500 |
| MEDIUM counterparty concentration | >40% of output or input |
| MEDIUM conservative default count | >4 per period |
| LOW absolute net VAT position | ZAR 30,000 |

---

## Section 2 — Required inputs and refusal catalogue

### Required inputs

**Minimum viable** — bank statement for the tax period in CSV, PDF, or pasted text. VAT registration number (starting with 4).

**Recommended** — tax invoices for all input tax claims above ZAR 5,000, sales invoices for all output, prior period excess credit (Field 14).

**Ideal** — complete creditors/debtors ledger, import VAT certificates (SAD500), asset register, prior VAT201 return.

**Refusal if minimum missing — SOFT WARN.** No bank statement = hard stop. "Input tax credits require a valid VAT tax invoice per Section 20 of the VAT Act. All credits are provisional pending invoice verification."

### Refusal catalogue

**R-ZA-1 — Non-VAT-registered vendor.** "Only registered vendors can charge VAT and claim input tax. Confirm VAT registration before proceeding."

**R-ZA-2 — Partial exemption / apportionment.** "If the vendor makes both taxable and exempt supplies, input tax must be apportioned under Section 17(1) of the VAT Act. The apportionment ratio changes annually — out of scope without full-year data. Escalate to a CA(SA)."

**R-ZA-3 — Capital goods scheme (Section 18A).** "Adjustments to input tax on capital goods where use changes between taxable and non-taxable purposes require specialist computation. Out of scope."

**R-ZA-4 — Financial services (Section 2).** "Financial services have complex VAT treatment. Banks, insurers, and financial institutions require specialist handling. Out of scope."

**R-ZA-5 — Property transactions.** "Property development, sale of commercial property, and going-concern zero-rating elections are highly fact-sensitive. Escalate to specialist."

---

## Section 3 — Supplier pattern library

### 3.1 South African banks — fees (standard-rated per s 2(1) proviso)

| Pattern | Treatment | Notes |
|---|---|---|
| ABSA BANK, ABSA GROUP | Input 15% | Bank service fees are standard-rated per s 2(1) proviso; banks issue monthly VAT tax invoices. Interest remains exempt. |
| STANDARD BANK, STANBIC | Input 15% | Standard-rated per s 2(1) proviso |
| FIRSTRAND, FNB, FIRST NATIONAL BANK | Input 15% | Standard-rated per s 2(1) proviso |
| NEDBANK | Input 15% | Standard-rated per s 2(1) proviso |
| CAPITEC BANK | Input 15% | Standard-rated per s 2(1) proviso |
| INVESTEC | Input 15% | Standard-rated per s 2(1) proviso |
| AFRICAN BANK | Input 15% | Standard-rated per s 2(1) proviso |
| BANK CHARGES, SERVICE FEE | Input 15% | Standard-rated per s 2(1) proviso |
| INTEREST | EXCLUDE | Exempt under s 12(a) / s 2(1)(f) |

### 3.2 South African government and statutory (exclude)

| Pattern | Treatment | Notes |
|---|---|---|
| SARS, SOUTH AFRICAN REVENUE SERVICE | EXCLUDE | Tax payment |
| UIF, UNEMPLOYMENT INSURANCE FUND | EXCLUDE | Statutory contribution |
| WORKMEN'S COMP, COIDA | EXCLUDE | Compensation fund |
| MUNICIPALITY, LOCAL AUTHORITY (rates) | EXCLUDE | Rates and taxes — outside VAT scope |
| ROAD ACCIDENT FUND, RAF | EXCLUDE | Statutory levy |

### 3.3 South African utilities (taxable at 15%)

| Pattern | Treatment | Rate | Notes |
|---|---|---|---|
| ESKOM | Input 15% | 15% | National electricity — taxable |
| CITY POWER (Johannesburg) | Input 15% | 15% | Municipal electricity — taxable |
| CAPE TOWN ELECTRICITY | Input 15% | 15% | Municipal electricity — taxable |
| RAND WATER, RAND WATER BOARD | Input 15% | 15% | Water — taxable |
| CITY OF CAPE TOWN WATER | Input 15% | 15% | Water — taxable |
| VODACOM | Input 15% | 15% | Mobile/internet — taxable |
| MTN SOUTH AFRICA | Input 15% | 15% | Mobile — taxable |
| CELL C | Input 15% | 15% | Mobile — taxable |
| TELKOM SA | Input 15% | 15% | Fixed-line/internet — taxable |
| RAIN NETWORK | Input 15% | 15% | Internet — taxable |
| AFRIHOST | Input 15% | 15% | Internet — taxable |

### 3.4 Transport and logistics

| Pattern | Treatment | Rate | Notes |
|---|---|---|---|
| SOUTH AFRICAN AIRWAYS, SAA | Check route | 0%/15% | International 0%; domestic 15% |
| FLYSAFAIR | Input 15% | 15% | Domestic airline — 15% |
| AIRLINK | Check route | 0%/15% | International 0%; domestic 15% |
| KULULA.COM | Input 15% | 15% | Domestic — 15% |
| UBER SOUTH AFRICA / BOLT SOUTH AFRICA | EXEMPT (s 12(g)) | — | Fare is exempt -- road transport of fare-paying passengers. No input VAT claimable on the fare. Only the booking fee (if separately shown on Uber tax invoice) may carry input VAT. |
| DHL SOUTH AFRICA | Input 15% | 15% | Courier — taxable |
| FEDEX SOUTH AFRICA | Input 15% | 15% | Courier — taxable |
| DAWN WING | Input 15% | 15% | Courier — taxable |
| THE COURIER GUY, TCG | Input 15% | 15% | Courier — taxable |
| ARAMEX SOUTH AFRICA | Input 15% | 15% | Courier — taxable |

### 3.5 Food and retail

| Pattern | Treatment | Rate | Notes |
|---|---|---|---|
| CHECKERS, SHOPRITE | Input 15%/0% | Mixed | Basic zero-rated food items; non-food 15%. For office consumption (tea, coffee, staff fridge, year-end function), input tax is BLOCKED under s 17(2)(a) entertainment regardless of zero-rate/standard-rate split. Only claimable where items are for resale by a vendor in the entertainment trade. |
| PICK N PAY, PNP | Input 15%/0% | Mixed | Same — zero-rate basic foodstuffs. For office consumption (tea, coffee, staff fridge, year-end function), input tax is BLOCKED under s 17(2)(a) entertainment regardless of zero-rate/standard-rate split. Only claimable where items are for resale by a vendor in the entertainment trade. |
| WOOLWORTHS FOOD | Input 15%/0% | Mixed | Food hall: basic items 0%; prepared/luxury food 15%. For office consumption (tea, coffee, staff fridge, year-end function), input tax is BLOCKED under s 17(2)(a) entertainment regardless of zero-rate/standard-rate split. Only claimable where items are for resale by a vendor in the entertainment trade. |
| SPAR | Input 15%/0% | Mixed | Same. For office consumption (tea, coffee, staff fridge, year-end function), input tax is BLOCKED under s 17(2)(a) entertainment regardless of zero-rate/standard-rate split. Only claimable where items are for resale by a vendor in the entertainment trade. |
| FOOD LOVERS MARKET | Input 15%/0% | Mixed | Same. For office consumption (tea, coffee, staff fridge, year-end function), input tax is BLOCKED under s 17(2)(a) entertainment regardless of zero-rate/standard-rate split. Only claimable where items are for resale by a vendor in the entertainment trade. |
| CLICKS | Input 15% | 15% | Health/beauty retail — 15% |
| DIS-CHEM | Input 15% | 15% | Prescription medicines are standard-rated at 15%; all pharmacy items 15% |
| MCDONALD'S SA, STEERS, NANDO'S | BLOCKED under s 17(2)(a) | 15% | BLOCKED under s 17(2)(a) for the buying business. Only the restaurant itself (being in the entertainment trade) can claim its own inputs. |

**Note on zero-rated basic foodstuffs:** Brown bread, maize meal, mielie rice, dried mealies, dried beans, lentils, pilchards/sardines in tins, milk, eggs, fruits and vegetables, vegetable oil, edible legumes. These are zero-rated under Schedule 2 of the VAT Act.

### 3.6 SaaS — international suppliers (reverse charge / imported services)

Under VAT Act Section 7(1)(c), imported services from abroad are subject to VAT if the recipient is a non-vendor or partially exempt vendor. For fully taxable vendors, VAT on imported services can be claimed back as input tax in the same period — net effect zero.

| Pattern | Treatment | Notes |
|---|---|---|
| GOOGLE (Workspace, Ads, Cloud) | Imported services — self-assess 15% | Output and input in same period (net zero for fully taxable) |
| MICROSOFT (365, Azure) | Imported services — self-assess 15% | Same |
| META, FACEBOOK ADS | Imported services — self-assess 15% | Same |
| ZOOM, SLACK | Imported services — self-assess 15% | Same |
| NOTION, OPENAI, ANTHROPIC | Imported services — self-assess 15% | Same |
| AWS | Imported services — self-assess 15% | Same |
| XERO (if billed from NZ) | Imported services — self-assess 15% | Same |
| SAGE (if billed from UK) | Imported services — self-assess 15% | Same |

### 3.7 Local SaaS and professional tools (15%)

| Pattern | Treatment | Rate | Notes |
|---|---|---|---|
| XERO (South Africa entity) | Input 15% | 15% | Accounting software |
| SAGE SOUTH AFRICA | Input 15% | 15% | Accounting/payroll |
| PASTEL, SAGE PASTEL | Input 15% | 15% | South African accounting |
| QUICKBOOKS SOUTH AFRICA | Input 15% | 15% | Accounting SaaS |

### 3.8 Payment processors (standard-rated per s 2(1) proviso)

| Pattern | Treatment | Notes |
|---|---|---|
| PAYFAST (transaction fees) | Input 15% | Standard-rated -- fee-based payment processing is not a financial service per s 2(1) proviso |
| YOCO (transaction fees) | Input 15% | Standard-rated -- fee-based payment processing is not a financial service per s 2(1) proviso |
| PEACH PAYMENTS (fees) | Input 15% | Standard-rated -- fee-based payment processing is not a financial service per s 2(1) proviso |
| STRIPE (fees) | Input 15% | Standard-rated -- fee-based payment processing is not a financial service per s 2(1) proviso |

### 3.9 Internal transfers and exclusions

| Pattern | Treatment | Notes |
|---|---|---|
| OWN ACCOUNT TRANSFER, INTER-ACCOUNT | EXCLUDE | Internal movement |
| LOAN, BOND REPAYMENT | EXCLUDE | Loan principal |
| SALARY, WAGES, PAYROLL | EXCLUDE | Outside VAT scope |
| DIVIDEND | EXCLUDE | Out of scope |
| MUNICIPAL RATES, PROPERTY RATES | EXCLUDE | Local government levy — not a supply |
| ATM, CASH WITHDRAWAL | Tier 2 — ask | Default exclude |

---

## Section 4 — Worked examples

Six classifications from a hypothetical Johannesburg-based IT consultant. Format: FNB (First National Bank) account statement.

### Example 1 — Domestic B2B revenue (15%)

**Input line:**
`15 Apr 2025  CREDIT  ABC TECHNOLOGY (PTY) LTD  INV-2025-041  R 115,000.00  R 500,000.00`

**Reasoning:**
Incoming R 115,000 (VAT-inclusive) from a SA company for IT consulting. Standard 15% VAT. Gross R 115,000 includes VAT. Net = R 100,000 (taxable supply) + R 15,000 output tax (R 115,000 × 15/115). A VAT-compliant tax invoice must be issued per Section 20 of the VAT Act. Report R 115,000 VAT-inclusive on VAT201 Field 1. Output VAT R 15,000 goes to Field 4.

**Classification:** Output tax 15% — R 15,000. Net supply: R 100,000. VAT-inclusive: R 115,000.

### Example 2 — Export service (zero-rated)

**Input line:**
`22 Apr 2025  CREDIT  ACME CORP USA  USD 5,000 (R 92,500)  R 592,500.00`

**Reasoning:**
USD receipt from a US company for IT consulting services exported from South Africa. Zero-rated under Schedule 1 of the VAT Act if the services are physically performed in SA but consumed outside SA. Evidence: contract showing foreign client, payment in foreign currency. Report R 92,500 on Field 2 (zero-rated). Output tax: R 0.

**Classification:** Zero-rated export — R 92,500. Output tax: R 0.

### Example 3 — Electricity (15%, input credit)

**Input line:**
`10 Apr 2025  DEBIT  ESKOM HOLDINGS SOC  April electricity  -R 11,500.00  R 388,500.00`

**Reasoning:**
Eskom electricity bill. Taxable at 15%. Gross R 11,500. Net = R 10,000 + R 1,500 input tax (R 11,500 × 15/115). Eskom issues VAT-compliant tax invoices — input credit of R 1,500 claimable. Report on Field 15 (input VAT on other goods/services).

**Classification:** Input tax 15% — R 1,500. Net expense: R 10,000.

### Example 4 — Zero-rated food (basic foodstuffs)

**Input line:**
`12 Apr 2025  DEBIT  PICK N PAY  Groceries (business kitchen)  -R 800.00  R 387,700.00`

**Reasoning:**
Grocery purchase. If itemised receipt shows basic foodstuffs only (brown bread, eggs, fresh vegetables, etc.) — zero-rated under Schedule 2 of the VAT Act. No input tax on zero-rated items (the input tax rate is 0%). If mixed grocery (some 15% non-food items), split the purchase. Without itemised receipt: conservative default is 15% on full amount.

**Classification:** Zero-rated (if basic foodstuffs only) — R 0 input tax. Conservative default: 15% on R 800 = R 104 input tax / (R 695.65 net + R 104 VAT = R 800 gross). Flag: obtain itemised receipt.

### Example 5 — Imported service — self-assess (Google Ads)

**Input line:**
`08 Apr 2025  DEBIT  GOOGLE IRELAND LIMITED  Google Ads April  -R 10,000.00  R 377,700.00`

**Reasoning:**
Google Ads billed from Ireland. Note: Google typically bills SA VAT directly now via its local entity; check the invoice. If billed by a non-resident entity, this is an "imported service" under Section 7(1)(c) of the VAT Act. The South African VAT-registered vendor must self-assess 15% VAT. Self-assessed output: R 10,000 × 15% = R 1,500 (add to Field 12 — other output adjustments and imported services). For a fully taxable vendor, simultaneously claim same as input tax R 1,500 (Field 15 — input VAT on other goods/services). Net effect: zero. Must be disclosed in the VAT201.

**Classification:** Imported service — self-assess output R 1,500 (Field 12); input R 1,500 (Field 15). Net: R 0 for fully taxable vendor.

### Example 6 — Residential rent (exempt, no input tax)

**Input line:**
`01 Apr 2025  DEBIT  CITY PROP MANAGEMENT  April office rent  -R 23,000.00  R 354,700.00`

**Reasoning:**
Monthly rent. If this is for a commercial office space where the landlord has opted to charge VAT and issues a VAT invoice showing 15%, then input tax of R 3,000 is claimable (gross R 23,000 / 1.15 × 15%). If the landlord has NOT opted to charge VAT (which is common for smaller landlords), then the rent is exempt and no input tax is available. Default: ask for the landlord's VAT invoice.

**Classification:** Tier 2 — ask. If VAT invoice received from landlord: Input 15% — R 3,000. If no VAT invoice: EXEMPT — no input tax.

---

## Section 5 — Tier 1 rules (compressed)

### 5.1 Standard rate 15%

Default rate for all taxable supplies. Legislation: VAT Act No. 89 of 1991, Section 7(1)(a).

### 5.2 Zero rate 0%

Exports of goods and qualifying services; basic foodstuffs (Schedule 2); illuminating paraffin; petrol and diesel (specific provisions); certain agricultural inputs; supply of enterprise as going concern (s 11(1)(e)); gold to SARB/bank. Evidence required for export zero-rating. Prescription medicines are STANDARD-RATED at 15%. Legislation: VAT Act Section 11; Schedule 2.

### 5.3 Exempt supplies

Financial services (Section 2); residential rental; public road and rail transport. No output tax charged; no input tax claimable on costs. Legislation: VAT Act Section 12.

### 5.4 Tax invoice requirements (Section 20)

- Supplies R50 or less: NO invoice required (till slip sufficient)
- Supplies R50 to R5,000: ABRIDGED tax invoice (omits recipient details)
- Supplies above R5,000: FULL tax invoice required with supplier name/address/VAT number, invoice number, date, buyer name/address/VAT number (if VAT-registered), description, net amount, VAT rate, VAT amount, total.

Must be issued within 21 days.

### 5.5 Imported services

Services supplied by a non-resident to a South African recipient are subject to VAT under Section 7(1)(c). Fully taxable vendors self-assess (output = input; net zero). Partially exempt or non-vendor recipients cannot recover and face a cost. Legislation: VAT Act Section 7(1)(c).

### 5.6 Anti-avoidance — entertainment

Input tax on entertainment, accommodation, and food/beverages is BLOCKED under Section 17(2)(a) UNLESS the vendor is in the business of providing entertainment (hotels, restaurants, conference venues). "Entertainment" includes meals, beverages, social functions.

### 5.7 Motor vehicles

Input tax on motor cars (as defined — passenger vehicles) is BLOCKED under Section 17(2)(c). Exception: if the vendor trades in motor cars or provides transport services as their primary business. Bakkies (utes/pickups) used exclusively for business: may qualify.

### 5.8 Filing deadlines

| Category | Period | Due date |
|---|---|---|
| Category B (>R30m) | Monthly | Last business day of following month |
| Category A (default) | Bimonthly | Last business day of following month |
| Category C (farming <R1.5m) | Six-monthly | Last business day of following month |
| Category D (connected-party farming/rental) | Annual | Last business day of following month |
| Category E (connected-party rental) | Annual | Last business day of following month |
| Category F (micro business turnover tax) | Four-monthly | Last business day of following month |

### 5.9 Penalties

| Offence | Penalty |
|---|---|
| Late return | ZAR 100–ZAR 16,000 per month late |
| Late payment | 10% of tax due + interest at prescribed rate |
| Understatement | 10%–200% of shortfall depending on intent |
| Fraud | Criminal prosecution |

---

## Section 6 — Tier 2 catalogue

### 6.1 Entertainment — is vendor in the hospitality trade?

**What it shows:** Restaurant, entertainment, or accommodation expense.
**What's missing:** Whether the vendor's primary business is hospitality/entertainment (unblocks the input).
**Conservative default:** BLOCKED — no input tax.
**Question to ask:** "Is this entertainment expense directly related to the provision of entertainment to customers (e.g., you are a restaurant, hotel, or conference venue)? If not, the input tax is blocked."

### 6.2 Motor vehicle — is it a "motor car" as defined?

**What it shows:** Vehicle purchase, lease, or maintenance.
**What's missing:** Whether the vehicle is a "motor car" (blocked) or a qualifying vehicle.
**Conservative default:** BLOCKED — no input tax.
**Question to ask:** "Is this a passenger vehicle (sedan, SUV, hatchback) used for business? If yes: blocked. Is it a bakkie/van used exclusively for business goods transport? If exclusively business use: may be unblocked."

### 6.3 Rent — has landlord opted to charge VAT?

**What it shows:** Monthly rent payment.
**What's missing:** Whether the landlord is VAT-registered and has charged VAT on the invoice.
**Conservative default:** No input tax (treat as exempt until VAT invoice confirmed).
**Question to ask:** "Does your landlord issue a VAT tax invoice for the rent showing their VAT number and 15% VAT? If not, no input credit is available."

### 6.4 Zero-rated basic food vs. standard-rated food

**What it shows:** Supermarket purchase.
**What's missing:** Itemised receipt showing which items are basic (zero-rated) vs. standard (15%).
**Conservative default:** 15% on full amount.
**Question to ask:** "Do you have an itemised till slip? Items like brown bread, eggs, fresh vegetables, milk are zero-rated; packaged snacks, prepared food, non-food items are 15%."

### 6.5 Imported services — partial exemption interaction

**What it shows:** Payment for foreign digital services.
**What's missing:** Whether the vendor has any exempt income that blocks full input tax recovery on imported services.
**Conservative default:** Self-assess output and input at 15% (net zero for fully taxable).
**Question to ask:** "Does the business have any exempt income (residential rent, financial services)? If yes, the imported services input tax recovery may be limited."

### 6.6 Motor vehicle — is it a "motor car" as defined?

Input tax on the supply of a "motor car" is BLOCKED under s 17(2)(c). "Motor car" definition includes sedans, SUVs, double-cab bakkies, minibuses up to 16 seats. Objective test per IN 82 (passenger area vs loading area). Single-cab bakkies are NOT motor cars. Running costs (fuel, repairs, insurance) ARE claimable even on blocked motor cars. Exception: vendor who continuously supplies motor cars in ordinary course (dealers, rental companies).

---

## Section 7 — Excel working paper template

```
SOUTH AFRICA VAT201 WORKING PAPER
Tax Period: ____________  VAT Registration No.: ____________

A. OUTPUT TAX
  A1. Standard-rated supplies at 15% (net)     ___________
  A2. Output tax 15% (A1 × 15/115 of gross OR A1 × 15%)  ___
  A3. Zero-rated supplies (net)                ___________
  A4. Exempt supplies (net)                    ___________
  A5. Imported services self-assessed output   ___________
  A6. Total output tax (A2 + A5)               ___________

B. INPUT TAX
  B1. Standard-rated purchases (net)           ___________
  B2. Input tax at 15% (B1 × 15/115)           ___________
  B3. Import VAT (SAD500)                      ___________
  B4. Imported services input (self-assessed)  ___________
  B5. Blocked input (entertainment, motor cars) ___________
  B6. Net input tax (B2+B3+B4 − B5)            ___________

C. NET VAT
  C1. Net VAT (A6 − B6)                         ___________
  C2. Prior period credit                       ___________
  C3. Net payable / (refund) (C1 − C2)          ___________

REVIEWER FLAGS:
  [ ] Tax invoices (Section 20) confirmed for all input claims?
  [ ] Entertainment and motor car inputs correctly blocked?
  [ ] Export evidence held for zero-rated supplies?
  [ ] Imported services self-assessed (output = input)?
  [ ] Basic foodstuffs correctly zero-rated?
  [ ] Rent — landlord VAT invoice confirmed?
```

---

## Section 8 — Bank statement reading guide

### Common South African bank statement formats

| Bank | Key columns | Date format | Amount |
|---|---|---|---|
| FNB | Date, Description, Debit, Credit, Balance | DD Mon YYYY | ZAR with 2 decimals |
| Standard Bank | Date, Narrative, Debit, Credit, Balance | DD MMM YYYY | ZAR |
| ABSA | Date, Description, Amount, Balance | DD/MM/YYYY | ZAR |
| Nedbank | Date, Details, Debit, Credit, Balance | DD/MM/YYYY | ZAR |
| Capitec | Date, Description, Debit, Credit, Balance | YYYY-MM-DD | ZAR |

### Key South African banking terms

| Term | Meaning | Classification hint |
|---|---|---|
| CREDIT | Incoming funds | Potential revenue |
| DEBIT | Outgoing payment | Potential expense |
| ATM WITHDRAWAL | Cash withdrawal | Tier 2 — ask |
| BANK CHARGES | Bank fee | Standard-rated (s 2(1) proviso) — claim input VAT |
| INTEREST EARNED | Interest received | Exempt |
| BALANCE | Running balance | Ignore |
| SALARY / WAGES | Payroll | Out of VAT scope |
| EFT / EFT DEBIT | Electronic fund transfer | Check direction |

---

## Section 9 — Onboarding fallback

```
SOUTH AFRICA VAT ONBOARDING — MINIMUM QUESTIONS
1. VAT registration number (10 digits starting with 4)?
2. Tax period covered by this bank statement?
3. Filing frequency: Category A bimonthly, B monthly, C six-monthly, D/E annual, F four-monthly?
4. Do you have any exports (zero-rated)? Evidence held?
5. Do you have exempt income (financial services, residential rent)?
6. Does the business provide entertainment as its primary service?
   (Determines whether entertainment input tax is blocked)
7. Are any vehicles used exclusively for business goods transport?
8. Imported services (Google, Microsoft, etc.) — confirm for self-assessment
9. Prior period credit/refund amount to carry forward?
```

---

## Section 10 — Reference material

### Key legislation

| Topic | Reference |
|---|---|
| VAT Act | Value-Added Tax Act No. 89 of 1991 |
| Standard rate | Section 7(1)(a) |
| Zero rate | Section 11; Schedule 2 |
| Exemptions | Section 12 |
| Input tax | Section 16 |
| Blocked input — entertainment | Section 17(2)(a) |
| Blocked input — motor cars | Section 17(2)(c) |
| Tax invoice | Section 20 |
| Imported services | Section 7(1)(c) |
| Penalties | Tax Administration Act No. 28 of 2011 |

### Known gaps

- Partial exemption (Section 17(1)) apportionment — escalate
- Property going-concern zero-rating — escalate
- Financial services VAT — escalate
- Capital goods adjustments (Section 18A) — escalate

### Self-check

- [ ] All tax invoices Section 20 compliant
- [ ] Entertainment and motor car inputs blocked
- [ ] Export zero-rating supported by evidence
- [ ] Imported services self-assessed
- [ ] Basic foodstuffs correctly split from 15% items
- [ ] Prior period credit carried forward

### Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2024 | Initial |
| 2.0 | April 2026 | v2.0 rewrite: pattern library, worked examples, no inline tier tags |
| 2.1 | May 2026 | Validated by Werner Britz CA(SA); corrected registration threshold to R2.3m; corrected bank fees and payment processors to standard-rated; corrected VAT201 field structure; corrected Uber/Bolt to exempt; added motor car and entertainment blocks; fixed tax invoice thresholds; removed prescription medicines from zero-rated; fixed filing categories |

---

## Prohibitions

- NEVER allow input tax on entertainment expenses unless vendor's primary business is hospitality
- NEVER allow input tax on motor cars (passenger vehicles) used for mixed purposes
- NEVER zero-rate exports without evidence (customs documents, foreign payment records)
- NEVER allow input tax from a non-VAT-registered supplier
- NEVER self-assess imported services without recording both output and input in the same period
- NEVER present calculations as definitive — direct to a CA(SA) or registered tax practitioner
- NEVER claim input on the supply of a motor car as defined, unless within s 17(2)(c) exception
- NEVER claim input on entertainment unless vendor is in the entertainment trade or supply is employee subsistence
- NEVER exclude bank service fees as exempt -- they are standard-rated (s 2(1) proviso)
- NEVER omit output VAT on Seventh Schedule fringe benefits under s 18(3)

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/south-africa-vat) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **accountant-reviewed**. Reviewed by Werner Britz, CA(SA). For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

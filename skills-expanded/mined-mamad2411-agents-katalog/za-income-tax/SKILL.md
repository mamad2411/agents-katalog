---
name: za-income-tax
description: "Use this skill whenever asked about South African income tax for self-employed individuals. Trigger on phrases like \"how much tax do I pay\", \"ITR12\", \"income tax return\", \"SARS\", \"tax brackets\", \"provisional tax\", \"IRP6\", \"rebates\", \"medical credits\", \"retirement deduction\", \"turnover tax\", \"eFiling\", or any question about filing or computing income tax for a self-employed or sole proprietor client in South Africa. ALWAYS read this skill before touching any South African income tax work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: INTL
  category: tax
  quality: accountant-reviewed
  openaccountants_url: "https://openaccountants.com/skills/za-income-tax"
  obligation: IT
  reviewed_by: "Werner Britz, CA(SA)"
---

# South Africa Income Tax -- Self-Employed Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

**Read this whole section before classifying anything.**

| Field | Value |
|---|---|
| Country | South Africa |
| Tax type | Income tax (normal tax) on trade income |
| Primary legislation | Income Tax Act 58 of 1962 |
| Supporting legislation | Tax Administration Act 28 of 2011; Sixth Schedule (Turnover Tax); Fourth Schedule (Provisional Tax) |
| Tax authority | SARS (South African Revenue Service) |
| Filing portal | SARS eFiling (www.sars.gov.za) |
| Currency | ZAR only |
| Tax year | 1 March -- 28 February |
| Return form | ITR12 |
| Provisional tax | IRP6 (1st: 31 Aug, 2nd: last day Feb, 3rd voluntary: 30 Sep) |
| Primary rebate | R17,820 |
| Secondary rebate (65+) | R9,768 |
| Tertiary rebate (75+) | R3,252 |
| Retirement fund deduction | 27.5% of greater of remuneration/taxable income, cap R430,000 |
| Turnover tax | Available for non-professional services, turnover up to R2,300,000 |
| Contributor | Open Accountants Community |
| Validated by | Werner Britz CA(SA), Spurwing CFO |
| Validation date | May 2026 |

**Progressive tax table (2026/2027 year of assessment):**

| Taxable income (ZAR) | Rate |
|---|---|
| 1--245,200 | 18% |
| 245,201--383,000 | R44,136 + 26% above R245,200 |
| 383,001--530,200 | R79,884 + 31% above R383,000 |
| 530,201--695,800 | R125,516 + 36% above R530,200 |
| 695,801--887,100 | R185,132 + 39% above R695,800 |
| 887,101--1,878,300 | R259,739 + 41% above R887,100 |
| 1,878,301+ | R666,131 + 45% above R1,878,300 |

**Tax thresholds (below = no tax):**

| Age | Threshold |
|---|---|
| Below 65 | R99,000 |
| 65--74 | R153,278 |
| 75+ | R171,355 |

**Medical tax credits (s6A, 2026/2027):**

| Member | Monthly |
|---|---|
| Main member | R376 |
| First dependant | R376 |
| Each additional | R254 |

**Turnover tax table (Sixth Schedule):**

| Turnover (ZAR) | Rate |
|---|---|
| 0--600,000 | 0% |
| 600,001--950,000 | 1% above R600,000 |
| 950,001--1,400,000 | R3,500 + 2% above R950,000 |
| 1,400,001--2,300,000 | R12,500 + 3% above R1,400,000 |

**Conservative defaults:**

| Ambiguity | Default |
|---|---|
| Unknown age | STOP -- age determines rebates and threshold |
| Unknown expense category | Not deductible |
| Unknown business-use proportion | 0% |
| Unknown whether home office qualifies | Not deductible (IN 28 strict) |
| Entertainment expenses | Critically review under s 11(a) and s 23(g); conservatively disallow if no clear nexus to income production |

---

## Section 2 -- Required inputs and refusal catalogue

### Required inputs

**Minimum viable** -- bank statement for the tax year (1 March -- 28 February). Acceptable from: FNB (First National Bank), Standard Bank, Nedbank, Absa, Capitec, Investec, Discovery Bank, TymeBank, or fintech (Revolut, Wise).

**Recommended** -- invoices, IRP6 payment records, medical aid statements, RA contribution certificates, vehicle logbook.

**Ideal** -- complete bookkeeping, prior year ITR12, IT34 (assessment), asset register.

### Refusal catalogue

**R-ZA-1 -- Company/CC/Trust.** *Trigger:* client is a company, close corporation, or trust. *Message:* "This skill covers sole proprietors only. Companies file ITR14 at 27% corporate rate. Trusts file ITR12T."

**R-ZA-2 -- Foreign income.** *Trigger:* significant foreign income. *Message:* "Foreign income, s10(1)(o)(ii) exemption, and DTA analysis are outside scope. Consult a registered tax practitioner."

**R-ZA-3 -- Capital gains tax.** *Trigger:* disposal of capital assets. *Message:* "Capital gains tax is outside scope."

**R-ZA-4 -- Age unknown.** *Trigger:* age not provided. *Message:* "I cannot compute without knowing your age -- it determines rebates and tax threshold."

---

## Section 3 -- Transaction pattern library (the lookup table)

### 3.1 South African banks (fees and interest)

| Pattern | Treatment | Notes |
|---|---|---|
| FNB, FIRST NATIONAL BANK | Bank charges: deductible | Business account fees |
| STANDARD BANK, SBSA | Bank charges: deductible | Same |
| NEDBANK | Bank charges: deductible | Same |
| ABSA | Bank charges: deductible | Same |
| CAPITEC | Bank charges: deductible | Same |
| INVESTEC | Bank charges: deductible | Same |
| DISCOVERY BANK, TYMEBANK | Bank charges: deductible | Same |
| REVOLUT, WISE (fees) | Deductible | Fintech fees |
| INTEREST (credit) | Taxable income up to exemption (R23,800 <65; R34,500 65+); excess = taxable | Interest exemption applies |
| INTEREST (debit) | Deductible if business loan | Personal: NOT deductible |
| LOAN, HOME LOAN (principal) | EXCLUDE | Principal movement |

### 3.2 SA government and statutory bodies

| Pattern | Treatment | Notes |
|---|---|---|
| SARS | EXCLUDE | Tax payment (provisional/income) |
| UIF, UNEMPLOYMENT INSURANCE | Deductible if employer contribution | Employee-related |
| COIDA, COMPENSATION FUND | Deductible | Workers compensation |
| CIPC | Deductible | Company/IP registration |

### 3.3 SA utilities and telecoms

| Pattern | Treatment | Notes |
|---|---|---|
| ESKOM, CITY POWER, CITY OF [JHB/CPT/DBN] | Deductible if business premises | Electricity/rates; apportion if home |
| RAND WATER | Deductible if business premises | Water |
| VODACOM, MTN, CELL C, TELKOM, RAIN | Deductible: business phone/internet | Mixed: apportion |

### 3.4 Insurance

| Pattern | Treatment | Notes |
|---|---|---|
| HOLLARD, SANTAM, OLD MUTUAL, MOMENTUM, OUTSURANCE | Deductible if business insurance | Personal: NOT deductible |
| DISCOVERY HEALTH, BONITAS, GEMS, MEDIHELP | NOT deductible from income | Medical = s6A/s6B credits (against tax, not income) |

### 3.5 SaaS and software -- international

| Pattern | Treatment | Notes |
|---|---|---|
| GOOGLE, MICROSOFT, ADOBE, META | Deductible expense | Foreign SaaS |
| GITHUB, OPENAI, ANTHROPIC | Deductible expense | Non-EU |
| SLACK, ZOOM, ATLASSIAN | Deductible expense | Check entity |

### 3.6 Professional services (SA)

| Pattern | Treatment | Notes |
|---|---|---|
| ACCOUNTANT, AUDIT, CA(SA) | Deductible | Accounting/audit fees |
| ATTORNEY, ADVOCATE, LAW FIRM | Deductible if business | Legal fees |
| TAX PRACTITIONER | Deductible | Tax advisory |

### 3.7 Retirement contributions

| Pattern | Treatment | Notes |
|---|---|---|
| ALLAN GRAY, CORONATION, 10X, SYGNIA, NINETY ONE | s11F deduction: 27.5% of taxable income, cap R430,000 | RA contributions |
| OLD MUTUAL RA, MOMENTUM RA, LIBERTY RA | Same | RA fund |

### 3.8 Transport and travel

| Pattern | Treatment | Notes |
|---|---|---|
| KULULA, FLYSAFAIR, AIRLINK, SAA | Deductible if business travel | Flights |
| UBER, BOLT | Deductible if business | Ride services |
| ENGEN, SHELL, BP, SASOL, CALTEX, TOTAL | Deductible: business vehicle portion only | Fuel; requires logbook |
| AVIS, EUROPCAR, HERTZ | Deductible if business | Rental car |
| SANRAL, E-TOLL | Deductible: business travel portion | Toll fees |

### 3.9 Office and supplies

| Pattern | Treatment | Notes |
|---|---|---|
| INCREDIBLE CONNECTION, MATRIX, TAKEALOT | Deductible or wear-and-tear depending on value | IT equipment |
| OFFICE NATIONAL, WALTONS | Deductible | Stationery |
| POSTNET, SA POST OFFICE | Deductible | Postage/courier |
| MAKRO, GAME | Deductible if business supplies | Verify business purpose |

### 3.10 Food and entertainment

| Pattern | Treatment | Notes |
|---|---|---|
| PICK N PAY, WOOLWORTHS, CHECKERS, SPAR, SHOPRITE | Default: NOT deductible | Personal provisioning |
| RESTAURANT (any) | Review under s 11(a)/s 23(g) | Bona fide business meals may be deductible; VAT input blocked under s 17(2)(a) |

### 3.11 Internal transfers and exclusions

| Pattern | Treatment | Notes |
|---|---|---|
| OWN TRANSFER, INTERNAL | EXCLUDE | Internal movement |
| DRAWINGS, OWNER | EXCLUDE | Personal drawings |
| DEPOSIT, OWN DEPOSIT | EXCLUDE | Capital injection |

---

## Section 4 -- Worked examples

### Example 1 -- Standard self-employed, mid-range

**Input:** Age 35, revenue R600,000, expenses R180,000, RA R80,000, medical R3,500/mo (main + 1 dependant), provisional paid R40,000.
**Computation:** Net profit R420,000. s11F = 27.5% x R420,000 = R115,500 (within R430,000 cap). Taxable = R304,500. Tax = R44,136 + 26% x R59,300 = R59,554. Less rebate R17,820. Less medical credit R9,024 (R376 x 2 x 12). Net = R32,710. Less provisional R40,000. Refund R7,290.

### Example 2 -- Turnover tax

**Input:** Non-professional sole proprietor, turnover R650,000.
**Computation:** R650,000 turnover falls within 2026/27 bracket R600,001--R950,000 at 1% above R600,000. Tax = 1% x R50,000 = R500.

### Example 3 -- Entertainment disallowed

**Input:** Client claims R15,000 client entertainment dinners. **Result:** Review under s 11(a) and s 23(g). If bona fide business development with evidence of business purpose, may be deductible. If no clear nexus to income production, disallow. s 23(m) does NOT apply to sole proprietors. VAT input on entertainment is separately blocked under s 17(2)(a) VAT Act.

### Example 4 -- Retirement cap exceeded

**Input:** Taxable income R2,000,000, RA R600,000.
**Computation:** 27.5% x R2,000,000 = R550,000 but cap R430,000. Deduction = R430,000. Excess R170,000 carries forward.

---

## Section 5 -- Tier 1 rules (deterministic)

### 5.1 Progressive rates
Apply rate table to taxable income. One table for all individuals regardless of marital status. **Legislation:** Income Tax Act, rates schedule.

### 5.2 Rebates
Primary R17,820 (all). Secondary R9,768 (65+). Tertiary R3,252 (75+). Credits against tax, not deductions from income. **Legislation:** s6.

### 5.3 Interest exemption
R23,800 (under 65). R34,500 (65+). Excess is taxable. **Legislation:** s10(1)(i).

### 5.4 s11F retirement deduction
27.5% of greater of remuneration or taxable income (before deduction). Cap R430,000. Excess carries forward or adds to tax-free retirement lump sum (R550,000). **Legislation:** s11F.

### 5.5 Medical tax credits (s6A)
Main + first dependant: R376/mo each. Additional: R254/mo. Credit against tax. NOT a deduction from income. **Legislation:** s6A.

### 5.6 Provisional tax (IRP6)
Based on estimated current year. 1st: 31 Aug (50%). 2nd: last day Feb (top-up to 100%). 3rd voluntary: 30 Sep. Under-estimation: 20% penalty if < 90% of actual (income < R1M) or 80% (> R1M). From years of assessment commencing on or after 1 March 2026, the basic-amount safe harbour threshold is R1,800,000 (up from R1,000,000). **Legislation:** Fourth Schedule.

### 5.7 Turnover tax
Non-professional services, turnover up to R2,300,000. Replaces income tax, CGT, dividends tax, VAT. Cannot claim normal deductions. **Legislation:** Sixth Schedule.

### 5.8 Wear-and-tear (s11(e))
Straight-line over the useful life per SARS IN 47 (Issue 5). Items costing R7,000 or less: full write-off in year of acquisition under BGR 7 (small-value assets). Items above R7,000: straight-line over IN 47 useful life (computers 3 years; office furniture 6 years; office equipment 5 years; cellular phones 2 years; printers 3 years). **Legislation:** s 11(e), SARS IN 47, BGR 7.

### 5.9 Entertainment
Sole proprietor entertainment is tested under the general deduction formula: s 11(a) (actually incurred in the production of income) plus s 23(g) (not of a domestic, private, or capital nature). Bona fide client business development meals with evidence of business purpose may be deductible. s 23(m) does NOT apply to sole proprietors -- it restricts deductions against employment income only. Note: VAT input on entertainment is separately blocked under s 17(2)(a) of the VAT Act regardless of income tax treatment. **Legislation:** s 11(a), s 23(g). Cross-reference: VAT Act s 17(2)(a).

### 5.10 Home office
Dedicated room, regularly and exclusively for trade. IN 28 is strict. Dual-use rooms: NO deduction. Proportion = room area / total home. **Legislation:** s11(a), IN 28. Warning: the area used for trade is 'tainted' for CGT purposes -- on disposal of the residence, the primary residence exclusion does not apply to the tainted portion. Practitioners must warn clients before first claiming home office.

### 5.11 Record keeping
5 years from submission. Invoices, receipts, bank statements, logbooks, asset register. **Legislation:** TAA s29-32.

---

## Section 6 -- Tier 2 catalogue

### 6.1 Home office qualification
*Why:* IN 28 requires regular and exclusive use. *Default:* NOT deductible. *Question:* "Is there a dedicated room used only for business?"

### 6.2 Motor vehicle logbook
*Why:* Business km unknown. *Default:* 0% business use. *Question:* "Do you have a logbook with date, destination, km, and purpose for each trip?"

### 6.3 Turnover tax vs normal tax
*Why:* Depends on expense level and qualification. *Default:* Present both. *Question:* "What are your total business expenses? Are you providing professional services?"

### 6.4 s6B additional medical expenses
*Why:* Complex, depends on age/disability. *Default:* Do not claim without reviewer. *Question:* "Age 65+? Disability? Out-of-pocket medical expenses?"

### 6.5 Bad debts
*Why:* Must prove irrecoverable. *Default:* Do not claim. *Question:* "Was this debt previously included in income? Is it truly irrecoverable?"

---

## Section 7 -- Excel working paper template

### Sheet "Transactions"
Columns: Date, Counterparty, Description, Amount (ZAR), Category (Revenue/Expense/Wear-and-tear/RA/Medical/EXCLUDE), Deductible amount, Default?, Question, Notes.

### Sheet "ITR12 Computation"
Step-by-step per Section 5: gross income, deductions, taxable income, tax, rebates, medical credits, provisional tax offset.

---

## Section 8 -- Bank statement reading guide

**CSV formats.** FNB exports use comma CSV with DD/MM/YYYY. Standard Bank uses semicolons. Nedbank and Absa offer various formats. Common columns: Date, Description, Amount, Balance.

**SA-specific patterns.** "DEBICHECK" = authenticated debit order. "MAGTAPE" = batch payment. "SASWITCH" = ATM network. "PREPAID" = likely personal (airtime top-up). "MUNICIPALITY" = rates and taxes.

**Provisional tax.** Two/three payments per year to SARS. These are tax payments, not expenses. EXCLUDE.

**Medical aid.** Monthly debits to Discovery/Bonitas/etc. These are NOT deductible from income -- they generate s6A credits against tax.

**RA contributions.** Monthly debits to Allan Gray/Coronation/etc. Deductible under s11F with cap.

---

## Section 9 -- Onboarding fallback

### 9.1 Age
*Inference:* Not inferable. Always ask. *Fallback:* "What is your age at 28 February 2027?"

### 9.2 Residency
*Inference:* SA bank accounts suggest resident. *Fallback:* "Are you a South African tax resident?"

### 9.3 Business type
*Inference:* From counterparty patterns. *Fallback:* "What is your trade/profession?"

### 9.4 Turnover tax election
*Inference:* Not inferable. *Fallback:* "Have you elected turnover tax?"

### 9.5 Medical aid
*Inference:* Monthly medical aid debits. *Fallback:* "Are you on medical aid? How many dependants?"

### 9.6 RA contributions
*Inference:* Monthly RA debits. *Fallback:* "Do you contribute to a retirement annuity?"

### 9.7 Provisional tax paid
*Inference:* SARS payments in statement. *Fallback:* "What IRP6 amounts have you paid?"

---

## Section 10 -- Reference material

### Test suite

**Test 1 -- Mid-range.** Age 35, R600K revenue, R180K expenses, R80K RA, medical R3,500/mo. Net tax R32,710.
**Test 2 -- Senior.** Age 68, R200K revenue, R50K expenses, R30K RA. Below threshold. R0 tax.
**Test 3 -- Turnover tax.** R650K turnover. Tax R500.
**Test 4 -- RA cap.** R2M taxable, R600K RA. Deduction R430,000. Excess carries forward.
**Test 5 -- Medical credits.** 6 members. R21,216/year credit (R376 x 2 + R254 x 4 = R1,768/mo x 12).
**Test 6 -- Under-estimation penalty.** R200K estimated, R450K actual. 20% penalty applies if estimate < 90% of actual (for income < R1,800,000 safe harbour threshold).

### Edge case registry

**EC1 -- Interest exemption.** R23,800 <65 / R34,500 65+. Excess taxable.
**EC2 -- Turnover tax + professional.** NOT eligible.
**EC3 -- RA exceeds cap.** Excess carries forward.
**EC4 -- Home office dual use.** NOT deductible.
**EC5 -- Provisional under-estimation.** 20% penalty.
**EC6 -- Medical credits large family.** Compute per-member.
**EC7 -- Foreign income.** ESCALATE.
**EC8 -- Turnover tax exit mid-year.** Transition rules apply.
**EC9 -- Entertainment.** Sole proprietor entertainment is tested under s 11(a) and s 23(g); s 23(m) does NOT apply to sole proprietors.
**EC10 -- Assessed loss.** Carry forward under s20; SARS may query.

### Prohibitions

- NEVER compute without knowing age
- NEVER apply tax below age-threshold
- NEVER allow entertainment deductions without evidence of business purpose under s 11(a) and s 23(g)
- NEVER deduct RA above R430,000 cap
- NEVER allow turnover tax for professional services
- NEVER use prior year income for provisional tax (SA uses estimated current year)
- NEVER treat medical credits as income deductions
- NEVER allow home office for dual-use rooms
- NEVER claim home office without warning the client of the CGT consequence on disposal of the residence (Eighth Schedule para 47)
- NEVER allow income tax as a deduction
- NEVER present calculations as definitive

### Sources

1. Income Tax Act 58 of 1962
2. Tax Administration Act 28 of 2011
3. SARS Interpretation Notes (IN 28, IN 47, IN 14)
4. SARS eFiling -- https://www.sars.gov.za

### Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a registered tax practitioner, CA(SA), or equivalent licensed practitioner in South Africa) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/za-income-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **accountant-reviewed**. Reviewed by Werner Britz, CA(SA). For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

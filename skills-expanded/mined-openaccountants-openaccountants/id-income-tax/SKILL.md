---
name: id-income-tax
description: "> Idaho Individual Income Tax Return (Form 40) for sole proprietors and single-member LLCs. Covers the flat 5.3% rate (tax year 2025), Idaho taxable income computation from federal taxable income, standard deduction, and the initial exemption amount ($4,811 single / $9,622 MFJ). Trigger: taxpayer is an Idaho resident or has Idaho-source income exceeding $2,500."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-ID
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/id-income-tax"
  obligation: IT
---

# Idaho Individual Income Tax Skill — Self-Employed / Sole Proprietor

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Scope.** This skill covers Idaho individual income tax for self-employed individuals and sole proprietors filing Form 40. Idaho has a flat 5.3% rate applied to taxable income above an initial exempt amount.
> **Quality tier.** Q3 — AI-drafted with citations. Must be reviewed by a qualified professional before use.

---

## Section 1: Metadata

| Field | Value |
|---|---|
| Jurisdiction | US-ID (Idaho) |
| Tax authority | Idaho State Tax Commission (ISTC) |
| Filing portal | [Idaho TAP (Taxpayer Access Point)](https://idahotap.gentax.com/TAP/) |
| Legislation citation | Idaho Code Title 63, Chapter 30 (Income Tax) |
| Primary form | Form 40 (Individual Income Tax Return — Resident) |
| Filing deadline | April 15, 2026 (for tax year 2025) |
| Extension | Automatic 6-month extension to October 15; tax must be paid by April 15 |
| Version | 0.1 |
| Generated date | May 22, 2026 |
| Validation status | AI-drafted — Q3 |

### Sources consulted

- Idaho State Tax Commission — Individual Income Tax Basics: https://tax.idaho.gov/taxes/income-tax/individual-income/online-guide
- Idaho Form 40 (2025) and Instructions: https://tax.idaho.gov/wp-content/uploads/forms/EFO00089/EFO00089_03-02-2026.pdf
- Tax Foundation — 2026 Idaho Tax Rates: https://taxfoundation.org/location/idaho/
- Idaho Code § 63-3024 (tax rate): https://legislature.idaho.gov/statutesrules/idstat/Title63/T63CH30/SECT63-3024/

---

## Section 2: Quick reference — rates and thresholds

### Tax year 2025 rate

| Rate | Applies to |
|---|---|
| 5.3% (flat) | Idaho taxable income above the exempt amount |

**Exempt amount (not taxed):**
| Filing status | Exempt amount |
|---|---|
| Single / Married filing separately | $4,811 |
| Married filing jointly / Head of household / Qualifying surviving spouse | $9,622 |

**Computation:** (Idaho taxable income − exempt amount) × 5.3% = Idaho tax. If result is ≤ 0, tax is zero.

Source: Idaho Code § 63-3024; Form 40 (2025) tax computation worksheet.

### Standard deduction (tax year 2025)

| Filing status | Standard deduction |
|---|---|
| Single / Married filing separately | $15,750 |
| Married filing jointly / Qualifying surviving spouse | $31,500 |
| Head of household | $23,625 |

Source: Form 40 (2025); Idaho conforms to federal standard deduction amounts.

### Filing thresholds (tax year 2025)

| Filing status | Gross income threshold |
|---|---|
| Single (under 65) | $15,000 |
| Single (65+) | $17,000 |
| Married filing jointly (both under 65) | $30,000 |
| Married filing jointly (one 65+) | $31,600 |
| Head of household (under 65) | $22,500 |
| Part-year / nonresidents | $2,500 from Idaho sources |

---

## Section 3: How this skill works with the federal return

**Starting point:** Idaho starts from federal taxable income (Form 1040, Line 15), NOT federal AGI. This is a key distinction from many other states.

### Key additions to Idaho income
- State/local tax refunds (if itemized federally and deducted state taxes)
- Idaho-specific additions (rare for most sole proprietors)

### Key subtractions from Idaho income
- Interest on U.S. government obligations (Treasury bonds, savings bonds)
- State income tax refund already included in federal income
- Idaho capital gains deduction (60% of qualifying Idaho-source capital gains held 12+ months, up to a net of $15,000 in deductions — see Form CG)
- Social Security benefits taxed by Idaho only to the extent included in federal taxable income (Idaho conforms to federal treatment)

### Net result
Federal taxable income ± Idaho additions/subtractions = Idaho taxable income → subtract exempt amount → × 5.3% = Idaho income tax.

---

## Section 4: Self-employed specific rules

### QBI conformity
Idaho starts from federal taxable income, which is AFTER the QBI deduction (Form 1040, Line 13 → Line 15). Therefore, the federal QBI deduction reduces Idaho taxable income automatically. No separate Idaho adjustment needed.

### SE health insurance deduction
Already reflected in federal AGI → federal taxable income. Flows through automatically.

### Retirement contributions (SEP, SIMPLE, solo 401(k))
Already reflected in federal AGI → federal taxable income. No add-back required.

### Home office deduction
Already reflected in Schedule C → federal AGI → federal taxable income. Flows through automatically.

### Estimated tax (Form 51)
Self-employed individuals must make quarterly estimated payments if they expect to owe $1,000 or more.

Voucher due dates: April 15, June 15, September 15, January 15.

Safe harbor: No penalty if payments equal at least 100% of prior year tax OR 90% of current year tax.

### Idaho Grocery Tax Credit (Food Tax Credit)
All Idaho residents receive a grocery tax credit (refundable):
- $120 per person (under 65)
- $140 per person (65+)
This credit is available regardless of income and offsets the 6% sales tax on groceries.

### Permanent Building Fund
Idaho charges a $10 contribution to the Permanent Building Fund on every return (included in the tax computation, Line 31 of Form 40).

---

## Section 5: Tier 1 rules — deterministic

| Rule ID | Rule |
|---|---|
| ID-IT-1.01 | Idaho tax = (Idaho taxable income − exempt amount) × 5.3% |
| ID-IT-1.02 | Idaho starts from federal taxable income (Line 15), not AGI |
| ID-IT-1.03 | Exempt amount: $4,811 (single/MFS) or $9,622 (MFJ/HoH/QSS) |
| ID-IT-1.04 | Permanent Building Fund contribution: $10 per return |
| ID-IT-1.05 | Grocery tax credit: $120/person (refundable) |
| ID-IT-1.06 | Idaho conforms to federal standard deduction ($15,750 single / $31,500 MFJ for 2025) |
| ID-IT-1.07 | Idaho conforms to federal treatment of Social Security |
| ID-IT-1.08 | Part-year/nonresidents must file if Idaho-source gross income > $2,500 |

---

## Section 6: Tier 2 rules — requires judgment

| Rule ID | Rule | Judgment needed |
|---|---|---|
| ID-IT-2.01 | Capital gains deduction (Form CG) | Determine if gains are Idaho-source, held 12+ months, and compute 60% exclusion up to limits |
| ID-IT-2.02 | Part-year resident allocation | Use Form 43; prorate based on Idaho income ratio |
| ID-IT-2.03 | Credit for taxes paid to other states | Verify tax was paid on same income |
| ID-IT-2.04 | Depreciation conformity | Idaho generally conforms to federal depreciation including §168(k); verify no decoupling |
| ID-IT-2.05 | Investment tax credit (Form 49) | Available for new equipment in Idaho; complex eligibility rules |

---

## Section 7: Supplier pattern library

| Pattern on bank statement | Likely meaning |
|---|---|
| IDAHO STATE TAX COM | Idaho income tax payment |
| ID TAX COMMISSION | Idaho estimated tax payment |
| STATE OF IDAHO TAX | Idaho tax payment |
| IDAHO TAX REFUND | Idaho income tax refund |

---

## Section 8: Form mapping

| Idaho Form | Federal equivalent / Input |
|---|---|
| Form 40, Line 7 | Federal Form 1040, Line 15 (federal taxable income) |
| Form 40, Lines 8–11 | Idaho additions and subtractions |
| Form 40, Line 19 | Idaho taxable income |
| Form 40, Line 20 | Tax computation (exempt amount subtracted, then × 5.3%) |
| Form 40, Line 31 | Permanent Building Fund ($10) |
| Form 40, Line 43 | Grocery tax credit |
| Form 51 | Quarterly estimated payments |
| Form CG | Capital gains deduction |

---

## Section 9: Refusal catalogue

| Refusal ID | Topic | Reason |
|---|---|---|
| R-ID-01 | Corporate income tax | Separate return and rules |
| R-ID-02 | Part-year / nonresident returns (Form 43) | Different form and allocation method |
| R-ID-03 | Mine license tax | Industry-specific |
| R-ID-04 | Property tax | Separate regime |
| R-ID-05 | Investment tax credit (Form 49) | Complex eligibility; requires separate analysis |
| R-ID-06 | Multi-state apportionment | Requires detailed allocation |
| R-ID-07 | Withholding tax | Employer obligation |

---

## Disclaimer
This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/id-income-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

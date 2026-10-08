---
name: ia-income-tax
description: "> Iowa Individual Income Tax Return (Form IA 1040) for sole proprietors and single-member LLCs. Covers the flat 3.8% rate (tax year 2025/2026), Iowa net income computation from federal AGI, Iowa standard deduction, and estimated tax. Iowa completed its historic flat-tax reform in 2025. Trigger: taxpayer is an Iowa resident or has Iowa-source income."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-IA
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ia-income-tax"
  obligation: IT
---

# Iowa Individual Income Tax Skill — Self-Employed / Sole Proprietor

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Scope.** This skill covers Iowa individual income tax for self-employed individuals and sole proprietors filing Form IA 1040. Iowa has a flat 3.8% rate — the result of landmark tax reform (SF 2442, 2024) that completed the transition from a multi-bracket system.
> **Quality tier.** Q3 — AI-drafted with citations. Must be reviewed by a qualified professional before use.

---

## Section 1: Metadata

| Field | Value |
|---|---|
| Jurisdiction | US-IA (Iowa) |
| Tax authority | Iowa Department of Revenue (IDR) |
| Filing portal | [Iowa eFile & Pay](https://tax.iowa.gov/idr-efile-and-pay) |
| Legislation citation | Iowa Code Chapter 422 (Individual Income Tax) |
| Primary form | Form IA 1040 (Individual Income Tax Return) |
| Filing deadline | April 30, 2026 (for tax year 2025) |
| Extension | Automatic 6-month extension to October 31; tax must be paid by April 30 |
| Version | 0.1 |
| Generated date | May 22, 2026 |
| Validation status | AI-drafted — Q3 |

### Sources consulted

- Iowa Department of Revenue — IDR Announces 2026 Individual Income Tax Rate: https://revenue.iowa.gov/press-release/2025-10-21/idr-announces-2026-individual-income-tax-and-interest-rates
- Iowa Department of Revenue — 2025 IA 1040 Expanded Instructions: https://revenue.iowa.gov/media/4435/download?inline=
- Iowa Code § 422.5 (tax rate): as amended by SF 2442 (2024)
- Remote Laws — Iowa Income Tax 2025: https://remotelaws.com/state-income-tax/us-states/iowa/
- Arnold Mote Wealth Management — Iowa 3.8% Flat Tax: https://arnoldmotewealthmanagement.com/iowans-new-tax-law-brackets/

---

## Section 2: Quick reference — rates and thresholds

### Tax year 2025 rate

| Rate | Applies to |
|---|---|
| 3.8% (flat) | All Iowa taxable income |

Source: Iowa Code § 422.5, as amended by SF 2442 (signed May 2024). The flat 3.8% rate applies to tax years beginning on or after January 1, 2025.

**Historical context:** Iowa transitioned from a 4-bracket progressive system (4.4%–5.7% in 2024) to a single 3.8% flat rate in 2025, making it the lowest flat income tax rate in the Midwest.

### Standard deduction (tax year 2025)

| Filing status | Standard deduction |
|---|---|
| Single / Married filing separately | $2,130 |
| Married filing jointly / Head of household | $5,240 |

### Personal exemption credit

| Item | Amount |
|---|---|
| Personal exemption credit (per exemption) | $40 |

### Filing thresholds (tax year 2025)

| Filing status | Net income threshold |
|---|---|
| Single (under 65) | $9,000 |
| Single (65+) | $24,000 |
| Married filing jointly (under 65) | $13,500 |
| Married filing jointly (65+) | $32,000 |

Nonresidents must file if Iowa-source income ≥ $1,000.

---

## Section 3: How this skill works with the federal return

**Starting point:** Iowa begins with federal adjusted gross income (AGI) from federal Form 1040, Line 11. However, Iowa then applies its own set of adjustments that differ significantly from the federal below-the-line computation.

### Key Iowa adjustments (increases to income)
- Federal net operating loss (NOL) deduction claimed on federal return (Iowa has its own NOL rules)
- Capital gain deduction claimed on IA 1040 (add back if not qualifying)

### Key Iowa adjustments (decreases to income)
- Iowa capital gain deduction: qualifying sales of real property used in farming/business (100% exclusion if held 10+ years and certain conditions met)
- Pension/retirement income exclusion: up to $6,000 per person ($12,000 MFJ) for taxpayers age 55+
- Social Security benefits: Iowa fully excludes Social Security from taxable income
- Military retirement pay: fully excluded
- Interest on U.S. government obligations

### Iowa-specific deductions
After computing Iowa net income, subtract:
- Iowa standard deduction OR Iowa itemized deductions
- Qualified business income (QBI) deduction (Iowa allows the federal §199A deduction as a separate line item)

### Net result
Federal AGI ± Iowa adjustments = Iowa net income → minus Iowa standard/itemized deduction → minus QBI deduction = Iowa taxable income → × 3.8% = Iowa tax → minus credits (including personal exemption credits).

---

## Section 4: Self-employed specific rules

### QBI conformity
Iowa specifically allows the federal QBI deduction (§199A) as a below-the-line deduction on Form IA 1040, Line 1e. This reduces Iowa taxable income.

### SE health insurance deduction
Already reflected in federal AGI. Flows through to Iowa automatically.

### Retirement contributions (SEP, SIMPLE, solo 401(k))
Already reflected in federal AGI. No Iowa add-back required.

### Home office deduction
Already reflected in Schedule C → federal AGI. Flows through automatically.

### Estimated tax (Form IA 1040-ES)
Self-employed individuals must make quarterly estimated payments if they expect to owe $200 or more.

Voucher due dates: April 30, June 30, September 30, January 31.

**Note:** Iowa's due dates differ from federal (April 30, not April 15).

Safe harbor: No penalty if payments equal at least 90% of current year tax OR 100% of prior year tax (110% if prior year Iowa AGI > $150,000).

### Iowa capital gain deduction
Sole proprietors who sell qualifying Iowa business assets held for 10+ years may exclude 100% of the gain. This is a significant benefit for long-held business property. Requirements:
- Asset must be real property used in a farming operation, or
- Asset must be qualifying business stock/partnership interest
- Various holding period and material participation requirements apply

---

## Section 5: Tier 1 rules — deterministic

| Rule ID | Rule |
|---|---|
| IA-IT-1.01 | Iowa tax = Iowa taxable income × 3.8% |
| IA-IT-1.02 | Iowa starts from federal AGI (Form 1040, Line 11) |
| IA-IT-1.03 | Iowa allows federal QBI deduction (§199A) as separate deduction on IA 1040 |
| IA-IT-1.04 | Social Security benefits are fully excluded from Iowa income |
| IA-IT-1.05 | Filing deadline is April 30 (not April 15) |
| IA-IT-1.06 | No local/city income taxes in Iowa |
| IA-IT-1.07 | Iowa inheritance tax repealed effective January 1, 2025 |
| IA-IT-1.08 | Personal exemption credit: $40 per exemption (non-refundable) |
| IA-IT-1.09 | Iowa does not conform to federal NOL rules — separate Iowa NOL computation required |

---

## Section 6: Tier 2 rules — requires judgment

| Rule ID | Rule | Judgment needed |
|---|---|---|
| IA-IT-2.01 | Iowa capital gain deduction eligibility | Verify holding period, material participation, and asset type requirements |
| IA-IT-2.02 | Iowa vs. federal itemized deductions | Iowa may differ on certain itemized deductions; compare totals |
| IA-IT-2.03 | Part-year resident allocation (Schedule IA 126) | Prorate income for period of Iowa residency |
| IA-IT-2.04 | Iowa NOL carryover | Iowa has different NOL rules than federal; requires separate tracking |
| IA-IT-2.05 | Pension/retirement exclusion eligibility | Verify age 55+ and qualifying income types |
| IA-IT-2.06 | Alternate tax computation | Some taxpayers may owe less using the alternate tax method; compare both |

---

## Section 7: Supplier pattern library

| Pattern on bank statement | Likely meaning |
|---|---|
| IOWA DEPT OF REVENUE | Iowa income tax payment |
| STATE OF IOWA TAX | Iowa estimated tax payment |
| IA TAX REFUND | Iowa income tax refund |
| IDR IOWA PMT | Iowa Department of Revenue payment |

---

## Section 8: Form mapping

| Iowa Form | Federal equivalent / Input |
|---|---|
| IA 1040, Line 1 | Federal Form 1040, Line 11 (AGI) |
| IA 1040, Lines 1a–1c | Iowa adjustments (additions/subtractions) |
| IA 1040, Line 1d | Iowa standard or itemized deduction |
| IA 1040, Line 1e | QBI deduction (federal §199A amount) |
| IA 1040, Line 4 | Iowa taxable income |
| IA 1040, Line 5 | Iowa tax (Line 4 × 3.8%) |
| Form IA 1040-ES | Quarterly estimated payments |
| Schedule IA 126 | Nonresident/part-year income allocation |
| Schedule IA 1040C | Itemized deductions |

---

## Section 9: Refusal catalogue

| Refusal ID | Topic | Reason |
|---|---|---|
| R-IA-01 | Corporate income tax | Separate return and rules |
| R-IA-02 | Part-year / nonresident allocation | Complex allocation via Schedule IA 126 |
| R-IA-03 | Iowa NOL computation | Complex multi-year tracking required |
| R-IA-04 | Franchise tax (financial institutions) | Industry-specific |
| R-IA-05 | Withholding tax | Employer obligation |
| R-IA-06 | Property tax credits (Homestead) | Separate application process |
| R-IA-07 | Capital gain deduction detailed analysis | Complex holding period and participation rules |

---

## Disclaimer
This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ia-income-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

---
name: ok-income-tax
description: "Triggers when the taxpayer is an Oklahoma resident sole proprietor or single-member LLC needing to file Oklahoma Form 511. Covers Oklahoma's six-bracket graduated income tax (0.25%–4.75% for tax year 2025), standard and itemized deductions, personal exemptions, and interaction with federal AGI. Must be loaded alongside us-tax-workflow-base and us-federal-return-assembly."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: US-OK
  category: tax
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ok-income-tax"
  obligation: IT
---

# Oklahoma Individual Income Tax Skill — Self-Employed / Sole Proprietor

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Scope.** Oklahoma Form 511 (Resident Income Tax Return) for tax year 2025 for full-year Oklahoma resident sole proprietors and disregarded single-member LLCs.
> **Quality tier.** Q3 — AI-drafted, not independently verified. All rates and thresholds have been researched from primary sources but must be confirmed by a qualified professional before use in return preparation.

---

## Section 1: Metadata

| Field | Value |
|---|---|
| Tax year covered | 2025 (returns due April 15, 2026) |
| Primary form | Oklahoma Form 511 (Resident Individual Income Tax Return) |
| Tax authority | [Oklahoma Tax Commission (OTC)](https://oklahoma.gov/tax.html) |
| Tax type | Graduated income tax |
| Currency date | May 2026 |

**Primary sources:**

| Source | URL |
|---|---|
| Oklahoma Statutes Title 68, § 2355 (income tax rates) | https://www.oscn.net/applications/oscn/deliverdocument.asp?citeid=86405 |
| 2025 Form 511 Instructions | https://oklahoma.gov/tax/individuals/income-tax/filing-information.html |
| HB 2764 (2025 — rate reduction for 2026+) | https://oksenate.gov/press-releases/oklahoma-legislature-sends-comprehensive-tax-cuts-and-modernization-plan-governor |

---

## Section 2: Quick reference — rates and thresholds

### Tax brackets — Single and Married Filing Separately (tax year 2025)

| Taxable income | Base tax | Rate | On excess over |
|---|---|---|---|
| $0 – $1,000 | $0.00 | 0.25% | $0 |
| $1,001 – $2,500 | $2.50 | 0.75% | $1,000 |
| $2,501 – $3,750 | $13.75 | 1.75% | $2,500 |
| $3,751 – $4,900 | $35.63 | 2.75% | $3,750 |
| $4,901 – $7,200 | $67.25 | 3.75% | $4,900 |
| $7,201 and above | $153.50 | 4.75% | $7,200 |

### Tax brackets — MFJ, HOH, and Qualifying Surviving Spouse (tax year 2025)

| Taxable income | Base tax | Rate | On excess over |
|---|---|---|---|
| $0 – $2,000 | $0.00 | 0.25% | $0 |
| $2,001 – $5,000 | $5.00 | 0.75% | $2,000 |
| $5,001 – $7,500 | $27.50 | 1.75% | $5,000 |
| $7,501 – $9,800 | $71.25 | 2.75% | $7,500 |
| $9,801 – $14,400 | $134.50 | 3.75% | $9,800 |
| $14,401 and above | $307.00 | 4.75% | $14,400 |

### Standard deduction (tax year 2025)

| Filing status | Standard deduction |
|---|---|
| Single / MFS | $6,350 |
| MFJ / QSS | $12,700 |
| HOH | $9,350 |

### Personal exemptions

| Exemption type | Amount |
|---|---|
| Per exemption (each taxpayer + dependents) | $1,000 |

### Other key figures

| Item | Value |
|---|---|
| Oklahoma EITC | 5% of federal EITC (nonrefundable) |
| Child tax credit | None (Oklahoma does not have a separate state child tax credit) |
| Sales tax relief credit | Available based on income and filing status (see Form 538-S) |
| Itemized deduction cap | $17,000 (charitable contributions and medical expenses are exempt from the cap) |

### 2026 change alert

HB 2764 (signed May 2025) restructures Oklahoma's income tax starting tax year 2026:
- Reduces to three brackets with a top rate of 4.5% (down from 4.75%)
- Single/MFS: 0% on first $3,750; 2.5% on next $1,150; 3.5% on next $2,300; 4.5% on remainder
- MFJ: 0% on first $7,500; 2.5% on next $2,300; 3.5% on next $4,600; 4.5% on remainder
- Includes automatic trigger for further 0.25% rate reductions based on revenue performance

---

## Section 3: How this skill works with the federal return

Oklahoma starts from **federal adjusted gross income (AGI)** on federal Form 1040, Line 11. Oklahoma then applies its own modifications (additions and subtractions) to arrive at Oklahoma AGI, then subtracts the standard or itemized deduction and personal exemptions to arrive at Oklahoma taxable income.

**Key flow:**

1. Federal AGI → Oklahoma modifications → Oklahoma AGI
2. Oklahoma AGI − standard or itemized deduction − exemptions = Oklahoma taxable income
3. Apply graduated tax rates → Oklahoma tax before credits
4. Apply credits → Oklahoma income tax liability

### Oklahoma deduction rules

- If the taxpayer **did not** itemize on the federal return, they must use the Oklahoma standard deduction.
- If the taxpayer **did** itemize federally, they must use Oklahoma itemized deductions (which use federal Schedule A as a starting point with adjustments).
- Oklahoma itemized deductions are capped at $17,000, except for charitable contributions and medical expenses, which are not subject to the cap.

---

## Section 4: Self-employed specific rules

### Federal conformity

Oklahoma generally conforms to the IRC but with specific exceptions. Key items for self-employed:

- **Deductible half of SE tax** reduces federal AGI and flows through to Oklahoma.
- **QBI deduction (§199A):** The QBI deduction is below-the-line on federal Form 1040 and does not affect federal AGI. Oklahoma starts from federal AGI, so no QBI add-back is needed on the Oklahoma return.
- **§179 expensing:** Oklahoma generally conforms to the federal §179 limit. Verify Oklahoma's conformity with OBBBA changes to §179.
- **Bonus depreciation (§168(k)):** Verify Oklahoma's conformity with OBBBA restoration of 100% bonus depreciation. If Oklahoma does not conform, an adjustment may be needed.

### Oklahoma additions (common for self-employed)

- State/local income tax deducted on federal Schedule A (add back on Oklahoma return if itemizing)
- Interest from non-Oklahoma state/local bonds
- Deductions not allowed under Oklahoma law

### Oklahoma subtractions (common for self-employed)

- Federal income tax deduction: Oklahoma is one of the few states that allows a deduction for federal income tax paid, subject to a cap based on federal AGI (see Form 511, Schedule 511-D). Cap for 2025: the lesser of actual federal tax paid or the cap amount based on AGI.
- Military retirement pay exclusion (up to 100%)
- Social Security benefits (to the extent included in federal AGI — Oklahoma fully excludes Social Security)
- Retirement income exclusion (up to $10,000 per person for qualifying retirement income)

### Federal income tax deduction (unique to Oklahoma)

Oklahoma allows a deduction for federal income tax liability. This is unusual among states. The deduction is limited and calculated on Schedule 511-D. The cap is based on the taxpayer's federal AGI.

| Federal AGI | Approximate cap on federal tax deduction |
|---|---|
| Up to $54,670 | Various amounts (see Schedule 511-D table) |
| Over $54,670 | Federal AGI × 0.00056 |

---

## Section 5: Tier 1 rules — deterministic

**R-OK-1. Federal AGI is the starting point.** Form 511, Line 1 = federal Form 1040, Line 11.

**R-OK-2. Social Security is fully exempt.** Subtract Social Security benefits included in federal AGI.

**R-OK-3. State income tax add-back required if itemizing.** If the taxpayer itemized on the federal return and deducted state income taxes, the state income tax deduction must be added back on the Oklahoma return.

**R-OK-4. Itemized deduction cap = $17,000.** Oklahoma caps itemized deductions at $17,000 (excluding charitable contributions and medical expenses). If federal itemized deductions (minus state tax add-back, plus adjustments) exceed $17,000, cap at $17,000 plus the exempt categories.

**R-OK-5. Federal income tax deduction is available.** Calculate using Schedule 511-D based on the taxpayer's federal AGI and actual federal tax liability.

**R-OK-6. Sales tax relief credit.** Low-income taxpayers may qualify for the sales tax relief credit (Form 538-S). The credit is based on income and the number of exemptions claimed.

---

## Section 6: Tier 2 rules — requires judgment

**J-OK-1. Federal tax deduction timing.** The federal income tax deduction is based on tax paid during the calendar year (not the liability for the year). This includes estimated payments, withholding, and any payments with extension. Judgment is needed to determine the correct amount.

**J-OK-2. Oklahoma conformity with OBBBA.** Verify whether Oklahoma has enacted specific conformity or decoupling legislation for OBBBA provisions. If not conformed, adjustments may be needed for bonus depreciation, §179, and other OBBBA items.

**J-OK-3. Residency determination for part-year situations.** Oklahoma defines a "resident" as one who is domiciled in Oklahoma or maintains a permanent place of abode and spends more than seven months of the year in Oklahoma.

---

## Section 7: Supplier pattern library

| Pattern | Description |
|---|---|
| Federal tax deduction optimizer | Calculate the optimal federal income tax deduction using Schedule 511-D to ensure maximum benefit. |
| Standard vs. itemized comparison | Compare Oklahoma standard deduction ($6,350 single) against itemized deductions (subject to $17,000 cap). |
| Social Security recipient | Full exclusion of Social Security from Oklahoma income — important for semi-retired freelancers. |
| Low-income sales tax relief | Taxpayers with low Oklahoma AGI may qualify for the sales tax relief credit — check eligibility. |

---

## Section 8: Form mapping

| Form 511 line | Description | Source |
|---|---|---|
| Line 1 | Federal AGI | Federal Form 1040, Line 11 |
| Line 4 | Oklahoma additions | State tax add-back, other additions |
| Line 7 | Oklahoma subtractions | Federal tax deduction, Social Security, retirement income |
| Line 8 | Oklahoma AGI | Line 1 + additions − subtractions |
| Line 9 | Itemized deductions OR skip to Line 10 | Federal Schedule A (adjusted) or skip |
| Line 10 | Standard deduction | $6,350 (single) / $12,700 (MFJ) / $9,350 (HOH) |
| Line 11 | Exemptions | $1,000 per person |
| Line 12 | Oklahoma taxable income | Line 8 − deduction − exemptions |
| Line 13 | Tax from tax tables | Tax table or rate schedule |
| Line 20 | Total Oklahoma tax | After credits |

---

## Section 9: Refusal catalogue

**REFUSE-OK-1.** REFUSE to prepare an Oklahoma return for a nonresident or part-year resident without the appropriate Schedule 511-NR. This skill covers full-year residents only.

**REFUSE-OK-2.** REFUSE to compute the federal income tax deduction without the complete payment history for the year. Estimated payments, withholding, and extension payments all factor in.

**REFUSE-OK-3.** REFUSE to determine Oklahoma conformity with specific OBBBA provisions without verifying the current Oklahoma conformity date and any enacted exceptions.

**REFUSE-OK-4.** REFUSE to claim the sales tax relief credit for a taxpayer without verifying income eligibility thresholds and filing requirements.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ok-income-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

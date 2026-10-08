---
name: ghana-pit
description: "Use this skill whenever asked to prepare, review, or classify transactions for Ghana Personal Income Tax (PAYE), annual tax return, or advise on GRA income tax brackets and SSNIT contributions. Trigger on phrases like \"Ghana income tax\", \"PAYE Ghana\", \"GRA\", \"SSNIT\", \"Ghana tax return\", or any Ghana personal tax request. ALWAYS read this skill before touching any Ghana PIT work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GH
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ghana-pit"
  tax_year: 2024
  obligation: IT
---

# Ghana Personal Income Tax (PAYE) Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 — Quick reference

| Field | Value |
|---|---|
| Country | Ghana (Republic of Ghana) |
| Tax | Personal Income Tax / PAYE (Pay As You Earn) |
| Currency | GHS (Ghana Cedi / ₵) |
| Tax year | Calendar year (1 Jan – 31 Dec) |
| Current tax year | 2024 |
| Tax authority | Ghana Revenue Authority (GRA) |
| Return form | Self-Assessment Return |
| Filing portal | https://tpsweb.gra.gov.gh |
| Filing deadline | 30 April of following year |
| SSNIT rate (employee) | 5.5% of basic salary |
| SSNIT rate (employer) | 13% of basic salary |
| Source credit | `Kessir/taxcalculatorgh` (32 stars) |
| Contributor | Open Accountants Community |
| Validated by | Pending — requires sign-off by a Ghanaian Chartered Accountant |
| Skill version | 1.0 |

---

## Section 2 — Monthly PAYE tax brackets (effective 1 Jan 2024)

| Monthly chargeable income (GHS) | Rate | Cumulative income | Cumulative tax |
|---|---|---|---|
| First 490 | 0% | 490 | 0 |
| Next 110 | 5% | 600 | 5.50 |
| Next 130 | 10% | 730 | 18.50 |
| Next 3,166.67 | 17.5% | 3,896.67 | 572.67 |
| Next 16,000 | 25% | 19,896.67 | 4,572.67 |
| Next 30,520 | 30% | 50,416.67 | 13,728.67 |
| Exceeding 50,416.67 | 35% | — | — |

### Annual equivalent

| Annual chargeable income (GHS) | Rate |
|---|---|
| First 5,880 | 0% |
| Next 1,320 | 5% |
| Next 1,560 | 10% |
| Next 38,000 | 17.5% |
| Next 192,000 | 25% |
| Next 366,240 | 30% |
| Over 605,000 | 35% |

---

## Section 3 — Social security (SSNIT / Tier 1 & 2)

| Contribution | Rate | Base |
|---|---|---|
| SSNIT Tier 1 (employee) | 5.5% | Basic salary |
| SSNIT Tier 1 (employer) | 13% | Basic salary |
| Tier 2 (mandatory occupational) | 5% (employer) | Basic salary |
| Tier 3 (voluntary provident) | Variable | — |

Employee's 5.5% SSNIT is deducted before tax calculation (reduces chargeable income).

---

## Section 4 — Chargeable income calculation

```
Step 1: Gross monthly salary (basic + allowances)
Step 2: − Exempt allowances (if applicable)
Step 3: = Assessable income
Step 4: − SSNIT employee contribution (5.5% of basic)
Step 5: − Tier 3 voluntary contribution (if any)
Step 6: − Other reliefs (see Section 5)
Step 7: = Chargeable income
Step 8: Apply PAYE brackets (Section 2)
Step 9: = Monthly tax
```

---

## Section 5 — Reliefs and deductions

| Relief | Amount / Rule |
|---|---|
| Marriage/responsibility relief | GHS 200/month per child (max 3 children) |
| Disability relief | 25% of assessable income |
| Aged relief (60+) | Additional exempt band |
| Education relief | Fees for approved courses (with receipts) |
| Insurance relief | Premiums paid (life insurance) |
| Mortgage interest | Actual interest on residential property |

---

## Section 6 — Self-employed / Business income

Self-employed individuals pay tax on annual profits:

| Annual chargeable income (GHS) | Rate |
|---|---|
| First 5,880 | 0% |
| 5,881 – 7,200 | 5% |
| 7,201 – 8,760 | 10% |
| 8,761 – 46,760 | 17.5% |
| 46,761 – 238,760 | 25% |
| 238,761 – 605,000 | 30% |
| Over 605,000 | 35% |

Quarterly instalment payments required (25% of estimated annual tax per quarter).

---

## Section 7 — Worked example

**Scenario:** Employed professional, monthly basic GHS 8,000, monthly allowances GHS 4,000. Total gross = GHS 12,000/month. No Tier 3.

| Step | Description | Amount (GHS) |
|---|---|---|
| Gross salary | Basic + allowances | 12,000 |
| − SSNIT (5.5% of basic) | 5.5% × 8,000 | (440) |
| **Chargeable income** | | **11,560** |

Monthly PAYE on GHS 11,560:

| Bracket | Income in bracket | Rate | Tax |
|---|---|---|---|
| First 490 | 490 | 0% | 0 |
| Next 110 | 110 | 5% | 5.50 |
| Next 130 | 130 | 10% | 13.00 |
| Next 3,166.67 | 3,166.67 | 17.5% | 554.17 |
| Remaining 7,663.33 | 7,663.33 | 25% | 1,915.83 |
| **Monthly tax** | | | **2,488.50** |

Annual tax: GHS 2,488.50 × 12 = **GHS 29,862**

---

## Section 8 — Filing guidance

### Who must file?

- All employees (employer withholds PAYE monthly)
- Self-employed persons
- Persons with income from multiple sources
- Rental income recipients

### Key dates

| Event | Deadline |
|---|---|
| Tax year end | 31 December |
| PAYE monthly remittance | 15th of following month |
| Annual return (employees) | 30 April |
| Self-employed quarterly payments | End of each quarter |
| Annual return (self-employed) | 30 April |

---

## Section 9 — Conservative defaults

| Situation | Conservative position |
|---|---|
| Allowance taxability unclear | Include as chargeable; flag for reviewer |
| SSNIT contribution not documented | Use 5.5% of stated basic; flag |
| Business expense documentation weak | Do not deduct; flag |
| Foreign income | Include if Ghana resident; flag treaty applicability |
| Rental income (undeclared) | Classify as chargeable; flag |

---

## Section 10 — Sources

| Source | URL |
|---|---|
| Ghana Revenue Authority (GRA) | https://gra.gov.gh |
| Income Tax Act, 2015 (Act 896) | — |
| Revenue Administration Act, 2016 (Act 915) | — |
| `Kessir/taxcalculatorgh` | https://github.com/Kessir/taxcalculatorgh |

---

*OpenAccountants — open-source accounting skills for AI*
*This is not tax advice. All outputs must be reviewed by a qualified professional before filing.*

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ghana-pit) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

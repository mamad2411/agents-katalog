---
name: ab-individual-return
description: "> Use this skill whenever asked about Alberta provincial individual income tax. Trigger on phrases like \"Alberta tax\", \"Alberta T1\", \"AB provincial tax\", \"Alberta flat tax\", \"Alberta credits\", \"Alberta personal amount\", \"no PST Alberta\", or any question about computing Alberta provincial tax for an individual return. This skill covers Alberta's 10% flat personal income tax rate, provincial credits, interaction with federal T1, and Alberta-specific deductions. ALWAYS read this skill before touching any Alberta individual tax return work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: CA
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/ab-individual-return"
  tax_year: 2025
  obligation: IT
---

# Alberta Individual Tax Return -- Provincial T1 Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Province | Alberta (Canada) |
| Tax | Provincial Personal Income Tax |
| Currency | CAD only |
| Tax year | 1 January -- 31 December 2025 |
| Primary legislation | Alberta Personal Income Tax Act (APITA) |
| Supporting legislation | Income Tax Act (Canada) -- federal; Alberta Tax and Revenue Administration |
| Tax authority | Canada Revenue Agency (administers on behalf of Alberta) |
| Filing portal | CRA My Account / NETFILE / paper T1 |
| Filing deadline | 30 April 2026 (15 June 2026 if self-employed; balance due 30 April) |
| Skill version | 1.0 |

### Alberta Provincial Tax Rate (2025)

| Taxable Income (CAD) | Rate |
|---|---|
| All taxable income | 10% (flat rate) |

Alberta is the only province with a single flat-rate personal income tax. There are no provincial tax brackets.

### Key Alberta Features

| Feature | Detail |
|---|---|
| Provincial sales tax (PST) | None -- Alberta has no PST |
| GST only | 5% federal GST applies |
| Alberta personal amount (2025) | $21,003 |
| Spousal/equivalent amount | $21,003 |
| Age amount (65+) | $5,853 (reduced at higher income) |
| Alberta Family Employment Tax Credit | Refundable credit for working families with children under 18 |
| Alberta Climate Leadership Adjustment | Phased out |
| Alberta child and family benefit | Income-tested provincial benefit |

### Federal Tax Rates (2025) -- For Reference

| Taxable Income (CAD) | Rate |
|---|---|
| 0 -- 57,375 | 15% |
| 57,376 -- 114,750 | 20.5% |
| 114,751 -- 158,468 | 26% |
| 158,469 -- 220,000 | 29% |
| 220,001+ | 33% |

### Combined Federal + Alberta Marginal Rates (2025)

| Taxable Income (CAD) | Combined Rate |
|---|---|
| 0 -- 57,375 | 25% |
| 57,376 -- 114,750 | 30.5% |
| 114,751 -- 158,468 | 36% |
| 158,469 -- 220,000 | 39% |
| 220,001+ | 43% |

### Conservative Defaults

| Ambiguity | Default |
|---|---|
| Unknown residency province on Dec 31 | Do not compute provincial tax -- confirm province |
| Unknown marital status | Single (no spousal credit) |
| Unknown dependant eligibility | No dependant credits claimed |
| Unknown employment status | Employed (T4 reporting) |

---

## Section 2 -- Classification and Filing

### 2.1 Residency Determination

Alberta provincial tax applies if the individual is resident in Alberta on December 31 of the tax year. Residency is determined by significant residential ties (dwelling, spouse/dependants in province).

### 2.2 T1 Structure

| Schedule | Purpose |
|---|---|
| T1 General | Federal return |
| Form AB428 | Alberta Tax and Credits |
| Schedule AB(S12) | Alberta Tax (calculation) |
| Schedule 1 | Federal tax calculation |

### 2.3 Provincial Credits (Form AB428)

| Credit | Amount (2025) | Type |
|---|---|---|
| Basic personal amount | $21,003 | Non-refundable |
| Spousal / common-law partner | $21,003 (reduced by spouse income) | Non-refundable |
| Eligible dependant amount | $21,003 | Non-refundable |
| CPP/QPP contributions (employee) | Actual contributions | Non-refundable |
| EI premiums | Actual premiums | Non-refundable |
| Age amount (65+) | $5,853 | Non-refundable (income-tested) |
| Pension income amount | Up to $1,636 | Non-refundable |
| Disability amount | $16,494 | Non-refundable |
| Tuition and education | Actual tuition | Non-refundable |
| Medical expenses | Excess over 3% of net income (or $2,635) | Non-refundable |
| Donations and gifts | First $200 at 10%; excess at 21% | Non-refundable |
| Political contributions (Alberta) | 75% of first $200 + 50% next $900 + 33.33% above | Non-refundable |

Credit rate: 10% (Alberta's flat rate applies to convert credit amounts to tax reductions).

### 2.4 Alberta Family Employment Tax Credit (AFETC)

| Element | Detail |
|---|---|
| Eligibility | Working families with children under 18, family income below threshold |
| Maximum benefit | Varies by number of children (up to ~$1,469 for 4+ children) |
| Reduction rate | Phases out at 4% of family income above ~$43,295 |
| Type | Refundable credit |
| Claim | Automatic through T1 filing |

---

## Section 3 -- Computation Method

### Step 1: Calculate Taxable Income
Same taxable income as federal (Line 26000 of T1).

### Step 2: Apply Alberta Tax Rate
Alberta tax = Taxable income × 10%.

### Step 3: Subtract Non-Refundable Credits
Total credit amounts × 10% = credit reduction.
Alberta basic tax = Step 2 − Step 3.

### Step 4: Add Alberta Tax on Split Income (TOSI)
If applicable, additional tax at highest federal rate on split income.

### Step 5: Apply Refundable Credits
Subtract AFETC and other refundable credits.

### Step 6: Net Provincial Tax Payable
Result of Steps 1-5 = Alberta tax payable on Form AB428.

---

## Section 4 -- Income Types and Dividend Tax Credits

### 4.1 Alberta Dividend Tax Credit

| Dividend Type | Federal Gross-Up | AB Credit Rate |
|---|---|---|
| Eligible dividends (public corps) | 38% gross-up | 8.12% of taxable amount |
| Non-eligible dividends (CCPCs) | 15% gross-up | 2.31% of taxable amount |

Combined tax on eligible dividends (top bracket): ~34.3%
Combined tax on non-eligible dividends (top bracket): ~42.3%

### 4.2 Capital Gains

- 50% inclusion rate for first $250,000 (individuals)
- 66.67% above $250,000 (effective June 2024)
- Combined rate on capital gains (50% inclusion): 21.5% (top bracket, AB)
- Lifetime Capital Gains Exemption: $1,250,000 on qualifying small business shares (2025)
- LCGE on qualified farm/fishing property: $1,250,000

### 4.3 Self-Employment Considerations

| Item | Detail |
|---|---|
| CPP contributions | Both portions: 11.9% on pensionable earnings $3,500 -- $71,300 |
| CPP2 | Additional 4% on earnings $71,300 -- $79,400 (2025) |
| No provincial payroll tax | Alberta does not levy employer payroll tax |
| Business expenses | Deducted against federal + provincial income |
| Home office | Federal rules apply; reduces both federal and provincial income |

---

## Section 4 -- Transaction Patterns

### 4.1 Income Patterns

| Pattern | Treatment | Notes |
|---|---|---|
| T4 EMPLOYMENT INCOME | Taxable | Box 14 of T4 |
| T4A PENSION, RETIREMENT | Taxable | May qualify for pension income amount |
| T5 INVESTMENT INCOME (interest, dividends) | Taxable | Eligible dividends get enhanced gross-up and credit |
| T3 TRUST INCOME | Taxable | Various character allocations |
| RENTAL INCOME (T776) | Taxable | Net rental income |
| SELF-EMPLOYMENT (T2125) | Taxable | Net business income |
| CAPITAL GAINS (Schedule 3) | 50% taxable | Inclusion rate for individuals |

### 4.2 Alberta-Specific Considerations

| Item | Treatment |
|---|---|
| Resource royalties (farm/oil) | May have Alberta Royalty Tax Credit implications |
| Farm income | Small farm tax credit may apply |
| Scientific research credits | Alberta SRED top-up (10% of qualifying SR&ED expenditures) |

---

## Section 5 -- Edge Cases

### 5.1 Multi-Province Residency
If the individual moved provinces during the year, provincial tax is based on province of residence on December 31. Income earned in another province while resident there does NOT change this -- all income is taxed by the province of residence on Dec 31 (with some exceptions for business income allocation).

### 5.2 Alberta vs No-PST Advantage
Alberta residents benefit from no PST on purchases but this is a consumption tax matter -- it does not affect income tax computation.

### 5.3 Alberta Carbon Tax / Federal Carbon Rebate
The federal Canada Carbon Rebate (formerly Climate Action Incentive) applies to Alberta residents. Claimed automatically on return.

---

## Section 6 -- Filing Requirements

| Item | Detail |
|---|---|
| Form | T1 General + Form AB428 (Alberta Tax and Credits) |
| Deadline | 30 April 2026 (15 June if self-employed; balance due remains 30 April) |
| Instalments | Required if net tax owing > $3,000 in current and either of prior two years |
| Penalty (late filing) | 5% of balance owing + 1% per month (max 12 months) |
| Interest | Prescribed rate compounded daily on balance owing |

---

## Section 7 -- Prohibitions

- NEVER apply provincial tax rates for another province to an Alberta resident
- NEVER apply PST calculations to Alberta transactions
- NEVER claim Alberta credits without confirming Alberta residency on December 31
- NEVER apply bracket-based rates -- Alberta uses a single 10% flat rate
- NEVER ignore the federal tax calculation -- provincial tax is in addition to federal
- NEVER present tax calculations as definitive -- always label as estimated

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, CGA, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/ab-individual-return) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

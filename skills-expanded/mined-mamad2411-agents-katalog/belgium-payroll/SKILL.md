---
name: belgium-payroll
description: "> Use this skill whenever asked about Belgian payroll processing, employee salary calculations, précompte professionnel (professional withholding tax), ONSS/RSZ social security contributions, employer cost calculations, net-to-gross or gross-to-net conversions, Belgian payslip structure, DmfA declarations, or any question about computing wages, deductions, or employer obligations in Belgium. Trigger on phrases like \"Belgian payroll\", \"ONSS contributions\", \"RSZ bijdragen\", \"précompte professionnel\", \"bedrijfsvoorheffing\", \"net salary Belgium\", \"employer cost Belgium\", \"DmfA filing\", \"social security Belgium\", \"Belgian payslip\", \"13th month Belgium\", \"double holiday pay\", \"meal vouchers Belgium\", or \"eco-cheques\"."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: BE
  category: payroll
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/belgium-payroll"
  obligation: PAY
---

# Belgium Payroll Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | Belgium (Kingdom of Belgium) |
| Currency | EUR |
| Payroll frequency | Monthly (typically paid last working day of month) |
| Tax year | Calendar year (1 January -- 31 December) |
| Primary legislation | Income Tax Code 1992 (CIR/WIB 92); Social Security Act (Law of 27 June 1969); Employment Contracts Act (3 July 1978) |
| Tax authority | SPF Finances / FOD Financiën |
| Social security authority | ONSS (Office National de Sécurité Sociale) / RSZ (Rijksdienst voor Sociale Zekerheid) |
| Employee SS rate | 13.07% of gross salary (no cap) |
| Employer SS rate | ~25% basic + ~3% special contributions (total ~27-28%) |
| Employer SS cap | EUR 85,000/quarter (basic contributions only, from 1 July 2025) |
| Withholding tax | Précompte professionnel / Bedrijfsvoorheffing (progressive, per Annex III) |
| Minimum wage (GGMMI) | EUR 2,189.81/month (from 1 April 2026, 18+ full-time) |
| DmfA filing | Quarterly, due by end of month following quarter |
| Skill version | 1.0 |

---

## Section 2 -- Income Tax Withholding (Précompte Professionnel)

### Annual Income Tax Brackets (Income Year 2026, AY 2027)

| Taxable Income (EUR) | Marginal Rate |
|---|---|
| 0 -- 16,720 | 25% |
| 16,721 -- 29,510 | 40% |
| 29,511 -- 51,070 | 45% |
| 51,071+ | 50% |

### Withholding Tax Mechanism

The précompte professionnel is NOT a simple application of the above brackets. It is calculated via Annex III of AR/CIR 92, which uses a progressive key formula accounting for:

- Gross taxable remuneration (after ONSS deduction)
- Family situation (single, married one income, married two incomes)
- Number of dependent children
- Disability status
- Flat-rate professional expense deduction (automatically applied)
- Tax-free allowance (quotité exemptée / belastingvrije som): EUR 10,570 base (2026)

### Key Withholding Rules

| Rule | Detail |
|---|---|
| Calculation base | Gross salary minus 13.07% ONSS = taxable base |
| Work bonus (werkbonus) | Reduces ONSS for low earners (gross < ~EUR 2,900/month) |
| Fiscal work bonus | Reduces withholding tax proportional to social work bonus |
| Holiday pay | Taxed separately at special withholding rates |
| 13th month / end-of-year premium | Taxed at exceptional rate (often higher marginal) |
| Double holiday pay | Upper portion taxed at 85% rate for withholding |

### Withholding Reductions

| Reduction | Amount (2026) |
|---|---|
| Per dependent child (1st) | EUR 48/month reduction |
| Per dependent child (2nd) | EUR 133/month |
| Per dependent child (3rd+) | EUR 299/month each |
| Disabled dependent | Additional EUR 48/month |

---

## Section 3 -- Social Security: Employee Deductions

| Contribution | Rate | Base | Cap |
|---|---|---|---|
| Personal ONSS/RSZ | 13.07% | Gross salary | No cap |
| Special social security contribution | EUR 9.30 -- 60.94/month | Based on family income | Max EUR 731.28/year |

### Work Bonus (Werkbonus / Bonus à l'emploi)

Low-wage earners receive a reduction on personal ONSS contributions:
- Applies to monthly gross salary below approximately EUR 2,900
- Maximum reduction: ~EUR 280/month (decreasing as salary increases)
- Effectively reduces the 13.07% burden for minimum-wage workers

### Key Rules

- Personal ONSS is deducted BEFORE calculating taxable income for withholding tax
- ONSS applies to ALL remuneration: salary, premiums, bonuses, benefits in kind (BIK)
- No upper ceiling on employee contributions
- ONSS is tax-deductible (reduces the withholding base)

---

## Section 4 -- Social Security: Employer Contributions

| Contribution | Rate | Notes |
|---|---|---|
| Basic employer ONSS | ~25.00% | Funds pensions, healthcare, unemployment, etc. |
| Special contributions (Closure Fund, Asbestos, etc.) | ~2-3% | Sector-dependent |
| **Total employer ONSS** | **~27-28%** | Varies by sector and joint committee (CP/PC) |

### Employer Contribution Cap (from 1 July 2025)

| Parameter | Detail |
|---|---|
| Cap threshold | EUR 85,000 gross per quarter per employee |
| Scope | Basic employer contributions (~25%) only |
| Excluded from cap | Special contributions (~3%), employee contributions (13.07%) |
| Indexation | 2% each time health index increases by 2% |
| Part-time workers | Full EUR 85,000 threshold (not pro-rated) |

### Structural Reduction (Structurele vermindering)

Employers receive an automatic reduction on ONSS contributions calculated via a formula based on reference salary relative to high/low wage ceilings. This reduces the effective employer cost, particularly for low-wage and high-wage workers.

### Target Group Reductions

| Target Group | Reduction |
|---|---|
| First hires (1st employee) | Full basic ONSS exemption for unlimited period |
| Young workers (< 26, low-qualified) | Significant quarterly reduction |
| Older workers (55+) | Quarterly reduction based on age bracket |
| Long-term unemployed | Quarterly reduction for 2+ years registered |

---

## Section 5 -- Minimum Wage and Overtime

### Minimum Wage (GGMMI / RMMMG)

| Period | Monthly Gross (full-time, 18+) |
|---|---|
| Until 31 March 2026 | EUR 2,154.81 |
| From 1 April 2026 | EUR 2,189.81 |

- Set by CAO nr. 43 of the National Labour Council (NAR/CNT)
- Applies to employment contracts of at least one month
- Sectors often have higher minimums via joint committee (CP/PC) agreements
- Indexed automatically when pivot index is exceeded
- Students under 21 and workers under 18 have separate scales (CAO nr. 50)

### Working Hours and Overtime

| Parameter | Standard |
|---|---|
| Standard working week | 38 hours |
| Maximum daily hours | 9 hours (extendable to 11 in certain sectors) |
| Overtime premium (first 2 hours) | 50% supplement |
| Overtime on Sundays/holidays | 100% supplement |
| Voluntary overtime (no reason) | Up to 120 hours/year (extendable to 360) |
| Internal overtime limit | 143 hours above normal before mandatory rest |

---

## Section 6 -- Mandatory Benefits

| Benefit | Detail |
|---|---|
| Annual holiday | 20 days (based on prior year's work) |
| Single holiday pay | Normal salary during vacation |
| Double holiday pay | 92% of gross monthly salary (paid in May/June) |
| 13th month / end-of-year premium | Sector-dependent (most CPs mandate it) |
| Guaranteed salary (illness) | 30 days at full pay (white-collar); 7/7/14 days (blue-collar) |
| Meal vouchers | Employer max EUR 6.91/day worked (common: EUR 8 total, EUR 1.09 employee) |
| Eco-cheques | Max EUR 250/year |
| Commuting allowance | Mandatory (amount depends on transport mode and CP) |
| Group insurance (2nd pillar pension) | Common via sector or company plan |
| Hospitalisation insurance | Widespread (not strictly mandatory but often via CP) |

### Statutory Holidays (2026)

Belgium has 10 legal public holidays. If a holiday falls on a weekend or rest day, it must be replaced by another paid day off.

---

## Section 7 -- Payslip Requirements

Belgian employers MUST issue a payslip (fiche de paie / loonfiche) for each salary payment. Required elements:

| Element | Mandatory |
|---|---|
| Employer identification (name, address, ONSS number) | Yes |
| Employee identification (name, NISS/INSZ number) | Yes |
| Pay period | Yes |
| Gross salary | Yes |
| All salary components (base, premiums, overtime, BIK) | Yes |
| ONSS employee deduction (13.07%) | Yes |
| Work bonus (if applicable) | Yes |
| Taxable base (after ONSS) | Yes |
| Précompte professionnel withheld | Yes |
| Special social security contribution | Yes |
| Net salary | Yes |
| Employer contributions (information) | Recommended |
| Meal vouchers / eco-cheques (if applicable) | Yes |
| Holiday pay details (when paid) | Yes |
| Cumulative year-to-date figures | Recommended |

### Annual Tax Documents

| Document | Deadline |
|---|---|
| Fiche 281.10 (employment income) | 28 February of following year |
| Fiche 281.20 (directors' income) | 28 February of following year |

---

## Section 8 -- Filing Obligations

| Filing | Frequency | Deadline | Authority |
|---|---|---|---|
| DmfA (quarterly social security declaration) | Quarterly | Last day of month after quarter end | ONSS/RSZ |
| Précompte professionnel (withholding tax) | Monthly | 15th of following month | SPF Finances |
| Dimona (employment start/end declaration) | Per event | Day of start/end of employment | ONSS/RSZ |
| Fiche 281.10/20 | Annual | 28 February | SPF Finances |
| Work accident declaration | Per event | Within 8 calendar days | Fedris |

### DmfA Details

| Parameter | Detail |
|---|---|
| Content | Worker data, salary, working days, contributions per employee |
| Submission | Electronic via ONSS portal or batch file |
| Penalties | Flat-rate penalty + interest for late/incorrect filing |
| Payment | Same deadline as filing (end of month after quarter) |
| Correction | Modification DmfA possible within limitation period |

### Key Annual Calendar

| Month | Obligation |
|---|---|
| January | DmfA Q4 prior year; monthly PP |
| February | Fiches 281.10/20 deadline |
| April | DmfA Q1 |
| May/June | Double holiday pay processing |
| July | DmfA Q2 |
| October | DmfA Q3 |
| December | 13th month / end-of-year premium processing |

---

## Section 9 -- Common Payroll Patterns

### Pattern 1: Standard Monthly Salary (White-Collar, Single, No Children)

```
Gross monthly salary:                EUR 3,500.00
- ONSS employee (13.07%):           -EUR   457.45
= Taxable base:                      EUR 3,042.55
- Précompte professionnel:           -EUR   ~640.00
- Special SS contribution:           -EUR    18.72
= Net salary:                        EUR ~1,927.00

Employer cost:
  Gross salary:                      EUR 3,500.00
+ Employer ONSS (~27%):             +EUR   945.00
= Total employer cost:               EUR ~4,445.00
```

### Pattern 2: Minimum Wage Worker (With Work Bonus)

```
Gross monthly salary:                EUR 2,189.81
- ONSS employee (13.07%):           -EUR   286.21
+ Work bonus:                       +EUR   ~180.00
= Effective ONSS deduction:         -EUR   106.21
= Taxable base:                      EUR 2,083.60
- Précompte professionnel:           -EUR   ~190.00
- Special SS contribution:           -EUR     9.30
= Net salary:                        EUR ~1,884.00
```

### Pattern 3: Holiday Pay Calculation

| Component | Calculation |
|---|---|
| Single holiday pay | Normal salary for days taken |
| Double holiday pay | 92% of gross monthly salary for full year of service |
| Timing | Paid by employer (white-collar) typically in May/June |
| ONSS on double holiday | 13.07% on the full 92% amount |
| Withholding on double holiday | Higher exceptional rate on upper portion |

### Pattern 4: Company Car Benefit in Kind

The taxable BIK for a company car is calculated using: CO2 reference emissions × 6/7 × catalogue value × age correction. This BIK is added to taxable income for withholding tax AND subject to employer solidarity contribution (CO2-based, minimum EUR 31.34/month).

---

## Section 10 -- Interaction with Other Skills

| Skill | Interaction |
|---|---|
| belgium-bookkeeping | Payroll journal entries (620 accounts), accruals for holiday pay and 13th month |
| belgium-einvoice | No direct interaction (e-invoicing relates to B2B transactions, not payroll) |
| payroll-workflow-base | General payroll processing workflow; Belgium-specific overrides in this skill |

### Belgium-Specific Payroll Considerations

- **Indexation**: Belgian salaries are automatically indexed when the pivot index (based on health index) is exceeded. This is UNIQUE in Europe and means gross salaries increase without negotiation.
- **Joint Committees (CP/PC)**: Over 100 joint committees set sector-specific rules for minimum wages, premiums, working conditions, and benefits. ALWAYS identify the applicable CP/PC before processing payroll.
- **Language regions**: Administrative language (FR/NL/DE) affects document requirements but not calculation methodology.
- **Salary margin**: For 2025-2026, the salary margin (loonmarge/marge salariale) is 0% -- meaning no collective salary increases beyond automatic indexation are permitted.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/belgium-payroll) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

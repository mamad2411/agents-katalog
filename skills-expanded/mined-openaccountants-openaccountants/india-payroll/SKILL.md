---
name: india-payroll
description: "> Use this skill whenever asked about Indian payroll processing, employee salary calculations, TDS on salary (Section 192), Provident Fund (PF/EPF), Employee State Insurance (ESI), employer cost calculations, CTC breakdowns, net-to-gross or gross-to-net conversions, Indian payslip structure, Form 24Q/Form 138 filings, or any question about computing wages, deductions, or employer obligations in India. Trigger on phrases like \"Indian payroll\", \"TDS on salary\", \"PF contribution\", \"ESI contribution\", \"EPF\", \"CTC breakdown\", \"new tax regime India\", \"old tax regime\", \"Form 16\", \"Form 130\", \"salary structure India\", \"basic DA HRA\", \"professional tax\", \"gratuity\", \"bonus India\", or \"minimum wages India\"."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: IN
  category: payroll
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/india-payroll"
  obligation: PAY
---

# India Payroll Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | India (Republic of India) |
| Currency | INR (Indian Rupee) |
| Payroll frequency | Monthly (typically paid last working day or 1st of next month) |
| Tax year (Financial Year) | 1 April -- 31 March (FY 2025-26 = April 2025 to March 2026) |
| Primary legislation | Income Tax Act 1961 (being replaced by IT Act 2025 from 1 April 2026); EPF & MP Act 1952; ESI Act 1948; Payment of Bonus Act 1965; Payment of Gratuity Act 1972; Code on Wages 2019 |
| Tax authority | Central Board of Direct Taxes (CBDT) / Income Tax Department |
| PF authority | Employees' Provident Fund Organisation (EPFO) |
| ESI authority | Employees' State Insurance Corporation (ESIC) |
| Employee PF | 12% of Basic + DA |
| Employer PF | 12% of Basic + DA (split: 3.67% EPF + 8.33% EPS) |
| ESI Employee | 0.75% of gross wages |
| ESI Employer | 3.25% of gross wages |
| TDS on salary | Progressive slab rates (new regime default) |
| Minimum wage | State-specific (no single national minimum) |
| Filing | TDS deposit by 7th; PF/ESI by 15th; Form 24Q/138 quarterly |
| Skill version | 1.0 |

---

## Section 2 -- Income Tax Withholding (TDS on Salary)

### New Tax Regime Slabs -- FY 2025-26 (Default)

| Annual Taxable Income (INR) | Rate |
|---|---|
| Up to 4,00,000 | Nil |
| 4,00,001 -- 8,00,000 | 5% |
| 8,00,001 -- 12,00,000 | 10% |
| 12,00,001 -- 16,00,000 | 15% |
| 16,00,001 -- 20,00,000 | 20% |
| 20,00,001 -- 24,00,000 | 25% |
| Above 24,00,000 | 30% |

Plus: 4% Health and Education Cess on total tax.

**Rebate under Section 87A**: Income up to INR 12,00,000 is effectively tax-free (rebate of up to INR 60,000).

**Standard deduction**: INR 75,000 for salaried employees (new regime).

### Old Tax Regime Slabs -- FY 2025-26 (Optional, Employee Must Opt)

| Annual Taxable Income (INR) | Rate |
|---|---|
| Up to 2,50,000 | Nil |
| 2,50,001 -- 5,00,000 | 5% |
| 5,00,001 -- 10,00,000 | 20% |
| Above 10,00,000 | 30% |

Plus: 4% Health and Education Cess.

**Old regime deductions**: Section 80C (up to 1.5L), 80D (health insurance), HRA, LTA, home loan interest (Section 24b), NPS (80CCD).

### TDS Calculation Method

| Step | Detail |
|---|---|
| 1. Estimate annual salary | Project total CTC components for the year |
| 2. Deduct exemptions | Standard deduction; HRA/LTA (old regime only) |
| 3. Deduct Chapter VIA | 80C, 80D, 80CCD etc. (old regime only) |
| 4. Apply slab rates | New regime (default) or old regime (if opted) |
| 5. Deduct rebate u/s 87A | If income ≤ 12L (new) or ≤ 5L (old) |
| 6. Add 4% cess | On computed tax |
| 7. Divide by 12 | Monthly TDS = Annual tax / 12 |

### Surcharge (Higher Incomes)

| Annual Income (INR) | Surcharge |
|---|---|
| 50L -- 1 Cr | 10% |
| 1 Cr -- 2 Cr | 15% |
| 2 Cr -- 5 Cr | 25% |
| Above 5 Cr | 25% (marginal relief applies) |

---

## Section 3 -- Social Security: Employee Deductions

### Employees' Provident Fund (EPF)

| Parameter | Detail |
|---|---|
| Employee contribution | 12% of Basic wages + Dearness Allowance (DA) |
| Wage ceiling for PF | INR 15,000/month (contributions mandatory up to this; voluntary above) |
| Minimum Basic + DA | Must be ≥ 50% of total remuneration (Labour Codes) |
| Applies to | Establishments with 20+ employees (10+ in notified sectors) |

### Employee State Insurance (ESI)

| Parameter | Detail |
|---|---|
| Employee contribution | 0.75% of gross wages |
| Wage ceiling | INR 21,000/month (INR 25,000 for persons with disability) |
| Applies to | Establishments with 10+ employees where employee wages ≤ ceiling |
| Coverage | Medical, sickness, maternity, disability, dependants' benefit |

### Professional Tax (PT)

| Parameter | Detail |
|---|---|
| Rate | State-specific (typically INR 150-200/month; max INR 2,500/year) |
| Applicability | Varies by state (Maharashtra, Karnataka, West Bengal, etc.) |
| Deducted by | Employer at source |
| Deposited | To state government monthly (by 15th-21st depending on state) |

---

## Section 4 -- Social Security: Employer Contributions

### Employer PF Contributions

| Component | Rate | On |
|---|---|---|
| EPF (Provident Fund) | 3.67% | Basic + DA |
| EPS (Pension Scheme) | 8.33% | Basic + DA (max INR 15,000) |
| EDLI (Life Insurance) | 0.50% | Basic + DA (max INR 15,000) |
| PF Admin charges | 0.50% | Basic + DA |
| **Total employer PF burden** | **~13.00%** | On Basic + DA |

### Employer ESI Contribution

| Parameter | Detail |
|---|---|
| Rate | 3.25% of gross wages |
| Wage ceiling | INR 21,000/month |
| Applies when | Any covered employee earns ≤ INR 21,000/month |

### Employer Total Statutory Cost (Typical)

| Component | Rate | Base |
|---|---|---|
| EPF + EPS + EDLI + Admin | ~13% | Basic + DA |
| ESI (if applicable) | 3.25% | Gross wages |
| Gratuity provision | ~4.81% | Basic + DA (15/26 × salary for each year of service) |
| Bonus (statutory minimum) | 8.33% | Basic + DA (min) up to 20% (max) |
| LWF (Labour Welfare Fund) | State-specific | Nominal amount |

---

## Section 5 -- Minimum Wage and Overtime

### Minimum Wages

India does NOT have a single national minimum wage. Rates are set by:

| Authority | Coverage |
|---|---|
| Central Government | Scheduled employments (railways, mines, ports) |
| State Governments | All other employments within the state |
| Skill classification | Unskilled, Semi-skilled, Skilled, Highly skilled |

### Indicative Minimum Wages (2025-26, Selected States)

| State | Unskilled (INR/month approx.) | Skilled (INR/month approx.) |
|---|---|---|
| Delhi | 17,494 | 19,279 |
| Maharashtra | 13,500 | 15,500 |
| Karnataka | 13,500 | 15,800 |
| Tamil Nadu | 12,500 | 14,000 |
| West Bengal | 10,000 | 11,500 |

### National Floor Wage (Proposed under Code on Wages)

- Proposed floor: INR 178/day (~INR 4,628/month)
- Not yet notified as of May 2026
- States cannot set minimum wages below this floor once notified

### Working Hours and Overtime

| Parameter | Standard |
|---|---|
| Standard working hours | 8 hours/day, 48 hours/week |
| Overtime rate | 2× the ordinary rate of wages |
| Maximum overtime | Varies by state (Factories Act: limited hours) |
| Weekly rest | 1 day per week mandatory |
| Spread-over | Maximum 10.5 hours including rest intervals |

---

## Section 6 -- Mandatory Benefits

| Benefit | Detail |
|---|---|
| Earned Leave (EL/PL) | 1 day per 20 days worked (Factories); varies by state Shops & Est. Act |
| Casual Leave | Typically 7-12 days/year (state-specific) |
| Sick Leave | Typically 7-12 days/year (state-specific) |
| Maternity Leave | 26 weeks (first two children); 12 weeks (third+) |
| Paternity Leave | 15 days (Central Government; private sector varies) |
| Gratuity | 15 days salary × years of service / 26 (after 5 years) |
| Statutory Bonus | 8.33% to 20% of Basic + DA (establishments with 20+ employees) |
| Leave encashment | Unused EL encashable at separation or annually (per policy) |
| National/Festival holidays | Varies by state (typically 5-10 gazetted holidays) |

### Gratuity Calculation

| Parameter | Detail |
|---|---|
| Formula | (15 × last drawn salary × years of service) / 26 |
| Salary for gratuity | Basic + DA |
| Eligibility | 5 years continuous service (relaxed for death/disability) |
| Maximum | INR 25,00,000 (tax-free limit; employer may pay more) |
| Tax treatment | Exempt up to limits under Section 10(10) |

### Statutory Bonus

| Parameter | Detail |
|---|---|
| Minimum bonus | 8.33% of Basic + DA |
| Maximum bonus | 20% of Basic + DA |
| Eligibility | Employees with Basic + DA ≤ INR 21,000/month |
| Calculation base | Capped at INR 7,000/month (or actual if lower) |
| Payment deadline | Within 8 months of closing of accounting year |

---

## Section 7 -- Payslip Requirements

Indian employers MUST issue monthly payslips under the Code on Wages 2019 and various state Shops and Establishments Acts. Required elements:

| Element | Mandatory |
|---|---|
| Employer name and establishment code | Yes |
| Employee name, ID, designation | Yes |
| Pay period (month) | Yes |
| Basic salary | Yes |
| Dearness Allowance (DA) | Yes (if applicable) |
| House Rent Allowance (HRA) | Yes (if applicable) |
| Special allowances | Yes |
| Overtime earnings | Yes (if applicable) |
| Gross salary | Yes |
| PF employee deduction (12%) | Yes |
| ESI employee deduction (0.75%) | Yes (if applicable) |
| Professional Tax | Yes (if applicable) |
| TDS (income tax) | Yes |
| Other deductions (LWF, advances, loans) | Yes |
| Net salary payable | Yes |
| Employer PF contribution (shown) | Recommended |
| Leave balance | Recommended |
| YTD earnings and deductions | Recommended |
| Bank account details | Common practice |

### CTC (Cost to Company) Structure -- Typical

| Component | Typical % of CTC |
|---|---|
| Basic salary | 40-50% |
| HRA | 40-50% of Basic |
| Special Allowance | Flexible component |
| Employer PF | 12% of Basic |
| Employer ESI (if applicable) | 3.25% of gross |
| Gratuity (funded) | 4.81% of Basic |
| Medical insurance (group) | Fixed premium |

---

## Section 8 -- Filing Obligations

| Filing | Frequency | Deadline | Authority |
|---|---|---|---|
| TDS deposit (Challan 281) | Monthly | 7th of following month (March: 30 April) | CBDT/IT Department |
| PF ECR (Electronic Challan cum Return) | Monthly | 15th of following month | EPFO |
| ESI contribution | Monthly | 15th of following month | ESIC |
| ESI employee details return | Monthly | 21st of following month | ESIC |
| Professional Tax | Monthly | State-specific (10th-21st) | State Government |
| Form 24Q / Form 138 (TDS quarterly return) | Quarterly | 31 Jul / 31 Oct / 31 Jan / 31 May | CBDT |
| Form 16 / Form 130 (TDS certificate) | Annual | 15 June | To employees |
| PF Annual Return (Form 6A/3A) | Annual | 25 April | EPFO |
| ESI Annual Return | Semi-annual | 11 May / 12 November | ESIC |

### Key Filing Details

| Filing | Detail |
|---|---|
| Challan 281 (TDS) | Online payment via NSDL/TIN portal; generates BSR code for Form 24Q |
| ECR (PF) | Upload member-wise file on EPFO Unified Portal; payment via approved banks |
| Form 24Q → Form 138 | Form 24Q replaced by Form 138 under Income Tax Act 2025 (from FY 2026-27) |
| Form 16 → Form 130 | Form 16 replaced by Form 130 under IT Act 2025 |

### Penalties

| Violation | Penalty |
|---|---|
| Late TDS deposit | 1%/month (from due date to deposit) + 1.5%/month (from deduction to deposit if not deducted on time) |
| Late TDS return | INR 200/day until filed (max = TDS amount); plus INR 10,000-1,00,000 under Section 271H |
| Late PF deposit | 12% p.a. interest + damages up to 25% of arrears |
| Late ESI | 12% p.a. interest + damages up to 25% |
| Non-issuance of Form 16/130 | Penalty under Section 272A: INR 500/day |

---

## Section 9 -- Common Payroll Patterns

### Pattern 1: Standard Salaried Employee (CTC INR 10,00,000, New Regime)

```
Monthly CTC breakdown:
  Basic salary:                      INR 41,667 (50% of CTC)
  HRA:                              INR 16,667
  Special Allowance:                INR 14,583
  Employer PF (12% of Basic):       INR  5,000
  Employer ESI (if applicable):     INR      0 (gross > 21,000)
  Gratuity provision:               INR  2,003
  Medical insurance:                INR  1,250
  Monthly CTC:                      INR 83,333

Monthly deductions:
  Employee PF (12% of Basic):      -INR  5,000
  Professional Tax:                -INR    200
  TDS (new regime, ~5.5%):        -INR  3,750

Gross salary (excl employer PF/gratuity): INR 75,000
Net monthly salary:                 INR ~66,050
```

### Pattern 2: Employee Below ESI Ceiling (Gross ≤ INR 21,000)

```
Gross monthly salary:               INR 18,000
  Basic + DA:                       INR  9,000
  HRA:                             INR  4,500
  Other allowances:                INR  4,500

Employee deductions:
  PF (12% of 9,000):              -INR  1,080
  ESI (0.75% of 18,000):          -INR    135
  Professional Tax:                -INR      0 (below threshold in most states)
  TDS:                             -INR      0 (below taxable threshold)
Net salary:                         INR 16,785

Employer cost:
  Gross salary:                     INR 18,000
+ Employer PF (13% of 9,000):     +INR  1,170
+ Employer ESI (3.25%):           +INR    585
+ Gratuity provision:             +INR    433
= Total employer cost:             INR ~20,188
```

### Pattern 3: TDS Calculation (New Regime, Annual Income INR 15,00,000)

```
Gross salary:                       INR 15,00,000
- Standard deduction:              -INR    75,000
= Taxable income:                   INR 14,25,000

Tax calculation:
  0 -- 4,00,000:      NIL          =        0
  4,00,001 -- 8,00,000: 5%         =   20,000
  8,00,001 -- 12,00,000: 10%       =   40,000
  12,00,001 -- 14,25,000: 15%      =   33,750
  Total tax:                        INR  93,750
+ Cess 4%:                         +INR   3,750
= Total annual TDS:                 INR  97,500
  Monthly TDS:                      INR   8,125
```

---

## Section 10 -- Interaction with Other Skills

| Skill | Interaction |
|---|---|
| india-einvoice | No direct interaction (e-invoicing is GST/B2B; payroll is separate) |
| payroll-workflow-base | General payroll processing workflow; India-specific overrides in this skill |

### India-Specific Payroll Considerations

- **New Labour Codes**: The four codes (Wages, Social Security, Industrial Relations, OSH) became effective November 2025. Key impact: Basic + DA must be ≥ 50% of total remuneration, increasing PF/gratuity costs.
- **Dual tax regime**: Default is new regime (Section 115BAC). Employee must explicitly opt for old regime. Employer MUST compute TDS per new regime if no declaration received.
- **State variations**: Minimum wages, Professional Tax rates, Shops & Establishments Act rules, and LWF contributions all vary by state. ALWAYS identify the employee's state of employment.
- **PF wage ceiling**: Statutory ceiling is INR 15,000/month for mandatory PF. Many employers contribute on actual Basic (above ceiling) voluntarily or per company policy.
- **ESI expansion**: Under new Labour Codes, ESI coverage expanded to all geographic areas. Previously, only notified areas were covered.
- **Income Tax Act 2025**: Takes effect from 1 April 2026 (FY 2026-27). Form 24Q → Form 138; Form 16 → Form 130. Same slab rates expected; procedural/section number changes.
- **Arrears/bonus**: When arrears or bonuses are paid, TDS must be computed on total projected annual income including such payments. Relief under Section 89 may apply.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com).

---

_Source: [OpenAccountants](https://openaccountants.com/skills/india-payroll) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

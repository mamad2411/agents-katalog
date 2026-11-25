---
name: uk-payroll
description: "> Use this skill whenever asked about UK payroll, PAYE, National Insurance contributions, employer obligations, RTI submissions, statutory payments, or payslip requirements. Trigger on phrases like \"PAYE\", \"National Insurance\", \"NIC\", \"Class 1 NI\", \"employer NI\", \"employee NI\", \"RTI\", \"FPS\", \"EPS\", \"real time information\", \"P45\", \"P60\", \"P11D\", \"statutory sick pay\", \"SSP\", \"statutory maternity pay\", \"SMP\", \"national minimum wage\", \"national living wage\", \"payslip\", \"tax code\", \"student loan deduction\", \"workplace pension\", \"auto-enrolment\", \"HMRC payroll\", or any question about running payroll in the United Kingdom. ALWAYS read this skill before processing any UK payroll work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: GB
  category: payroll
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/uk-payroll"
  tax_year: 2025-26
  obligation: PAY
---

# United Kingdom -- Payroll Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

> **Year applicability:** Rules in this skill apply across **2024-25, 2025-26, and 2026-27** unless a specific section flags a year-dated change. The pack is read alongside the rate-bearing skills (`uk-income-tax-sa100`, `uk-national-insurance`, `uk-dividends`, etc.) which carry full 3-year tables.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | United Kingdom (England, Wales, Scotland, Northern Ireland) |
| Currency | GBP (£) only |
| Tax year | 6 April -- 5 April |
| Primary legislation | Income Tax (Earnings and Pensions) Act 2003; Social Security Contributions and Benefits Act 1992 |
| Tax authority | HM Revenue and Customs (HMRC) |
| Reporting system | Real Time Information (RTI) |
| Pay frequency | Monthly (most common), weekly, fortnightly, four-weekly |
| Employer registration | PAYE scheme via HMRC Online Services |
| Validated by | Pending -- requires sign-off by a UK chartered accountant or payroll professional |
| Skill version | 1.0 |

---

## Section 2 -- Income Tax Withholding (PAYE)

PAYE (Pay As You Earn) is a cumulative withholding system. The employer applies tax codes issued by HMRC to calculate tax due on each payment.

### Tax Bands -- England, Wales & Northern Ireland (2025/26)

| Band | Annual Income (£) | Rate |
|---|---|---|
| Personal Allowance | 0 -- 12,570 | 0% |
| Basic rate | 12,571 -- 50,270 | 20% |
| Higher rate | 50,271 -- 125,140 | 40% |
| Additional rate | 125,141+ | 45% |

**Scotland has separate income tax bands** (starter, basic, intermediate, higher, advanced, top). Always check the employee's tax code prefix (S = Scotland, C = Wales).

### Key Tax Code Rules

| Code | Meaning |
|---|---|
| 1257L | Standard personal allowance £12,570 (2025/26) |
| BR | All pay taxed at basic rate (no allowance) |
| D0 | All pay taxed at higher rate |
| D1 | All pay taxed at additional rate |
| NT | No tax deducted |
| 0T | No personal allowance (used when allowance exhausted) |
| K prefix | Negative allowance -- tax code adds to taxable pay |
| W1/M1 suffix | Non-cumulative (week 1/month 1) basis |

### Personal Allowance Taper

The £12,570 personal allowance is reduced by £1 for every £2 of adjusted net income above £100,000. It reaches zero at £125,140.

### Student Loan Deductions (2025/26)

| Plan | Threshold (annual) | Rate |
|---|---|---|
| Plan 1 (pre-2012) | £24,990 | 9% |
| Plan 2 (post-2012) | £27,295 | 9% |
| Plan 4 (Scotland) | £31,395 | 9% |
| Plan 5 (post-2023) | £25,000 | 9% |
| Postgraduate loan | £21,000 | 6% |

---

## Section 3 -- Social Security: Employee Deductions (National Insurance)

### Class 1 Primary (Employee) NIC -- 2025/26

| Earnings Band | Weekly | Annual | Rate |
|---|---|---|---|
| Below LEL | < £125 | < £6,500 | 0% (no NI, no qualifying year) |
| LEL to PT | £125 -- £242 | £6,500 -- £12,570 | 0% (qualifying year accrues) |
| PT to UEL | £242 -- £967 | £12,570 -- £50,270 | 8% |
| Above UEL | > £967 | > £50,270 | 2% |

### Class 1 Primary (Employee) NIC -- 2026/27

Same thresholds except LEL rises to £129/week (£6,708/year). Rates remain 8% / 2%.

---

## Section 4 -- Social Security: Employer Contributions (National Insurance)

### Class 1 Secondary (Employer) NIC -- 2025/26 and 2026/27

| Threshold | Weekly | Annual | Rate |
|---|---|---|---|
| Secondary Threshold (ST) | £96 | £5,000 | -- |
| Above ST | > £96 | > £5,000 | 15% |

**No upper limit** -- employer NIC at 15% applies on all earnings above the ST with no cap.

### Employment Allowance

Up to £10,500 per year offset against employer NIC. Not available if the sole employee is a director, or if prior-year employer NIC exceeded £100,000.

### Reduced Rates for Specific Categories

| Category | Employer NIC on earnings up to £967/week |
|---|---|
| Under 21 (letter M) | 0% up to UEL, 15% above |
| Apprentice under 25 (letter H) | 0% up to UEL, 15% above |
| Armed forces veteran (letter V) | 0% up to UEL, 15% above |
| Freeport employee (letter F) | 0% up to FUST, 15% above |

### Class 1A NIC

Employer pays 15% on the taxable value of most benefits in kind (company car, private medical, etc.). Reported on P11D and paid by 22 July following the tax year.

---

## Section 5 -- Minimum Wage and Overtime

### National Minimum / Living Wage Rates

| Category | From 1 Apr 2025 | From 1 Apr 2026 |
|---|---|---|
| Age 21+ (National Living Wage) | £12.21/hr | £12.71/hr |
| Age 18--20 | £10.00/hr | £10.85/hr |
| Under 18 / Apprentice | £7.55/hr | £8.00/hr |
| Accommodation offset | £10.66/day | £11.10/day |

### Overtime

No statutory overtime premium in the UK. Overtime rates are contractual, not legally mandated. However, average hourly pay including overtime must not fall below NMW/NLW.

### Working Time Regulations

Maximum average 48 hours/week (averaged over 17 weeks) unless the employee has opted out in writing. Night workers are limited to 8 hours in any 24-hour period on average.

---

## Section 6 -- Mandatory Benefits

### Statutory Sick Pay (SSP)

| Item | 2025/26 | 2026/27 |
|---|---|---|
| Weekly rate | £118.75 | £123.25 |
| Waiting days | 3 days (abolished from 6 Apr 2026) |
| Maximum duration | 28 weeks | 28 weeks |
| Earnings threshold (LEL) | £125/week | Abolished from 6 Apr 2026 |

From 6 April 2026, SSP is paid from day 1 of sickness and the LEL threshold is removed. SSP is paid at 80% of normal weekly earnings or the flat rate, whichever is lower.

### Statutory Maternity Pay (SMP)

| Period | Rate |
|---|---|
| First 6 weeks | 90% of average weekly earnings (AWE) |
| Remaining 33 weeks | £187.18/week (2025/26) or 90% AWE, whichever is lower |
| From 6 Apr 2026 | £194.32/week for the flat-rate portion |

Total entitlement: 39 weeks. Qualifying conditions: 26 weeks' continuous service by the 15th week before EWC and AWE ≥ LEL.

### Statutory Paternity Pay (SPP)

2 weeks at the lower of £187.18/week (£194.32 from Apr 2026) or 90% AWE.

### Statutory Adoption / Shared Parental / Bereavement / Neonatal Care Pay

Same flat rate as SMP (£187.18 / £194.32 from Apr 2026).

### Holiday Entitlement

Minimum 5.6 weeks (28 days for full-time). Includes bank holidays unless contractually additional. Pro-rated for part-time. Rolled-up holiday pay is now permitted from 1 January 2024 for irregular-hours and part-year workers.

### Workplace Pension (Auto-Enrolment)

| Parameter | Value |
|---|---|
| Minimum total contribution | 8% of qualifying earnings |
| Minimum employer contribution | 3% of qualifying earnings |
| Qualifying earnings band | £6,240 -- £50,270 (2025/26) |
| Eligible jobholders | Age 22 to SPA, earning > £10,000/year |

---

## Section 7 -- Payslip Requirements

Employers must provide itemised payslips on or before payday (Employment Rights Act 1996 s8).

### Mandatory Payslip Contents

- Gross pay
- Net pay
- All deductions (PAYE, NIC, student loan, pension) with amounts and descriptions
- Variable deductions: fixed deductions may reference a standing statement
- Hours worked (if pay varies by hours) -- mandatory from April 2019

### Optional but Recommended

- Tax code and NI category letter
- Employer and employee pension contributions
- Cumulative pay and tax year-to-date
- NI number
- Pay period and pay date

---

## Section 8 -- Filing Obligations

### Real Time Information (RTI)

| Submission | When | Content |
|---|---|---|
| Full Payment Submission (FPS) | On or before each payday | Employee pay, tax, NIC, student loans, statutory payments |
| Employer Payment Summary (EPS) | By 19th of following month | Statutory pay recoveries, Employment Allowance, CIS deductions suffered, apprenticeship levy |
| Earlier Year Update (EYU) | After 19 April (prior year corrections) | Adjustments to prior-year FPS totals |

### Payment to HMRC

| Method | Deadline |
|---|---|
| Electronic payment | 22nd of following month (or 22nd quarterly for small employers) |
| Cheque | 19th of following month |

### Year-End Obligations

| Task | Deadline |
|---|---|
| Final FPS of year | On or before last payday of tax year |
| P60 to employees | By 31 May |
| P11D / P11D(b) (benefits in kind) | By 6 July |
| Class 1A NIC payment | By 22 July (electronic) |

### Apprenticeship Levy

Employers with annual pay bill > £3 million pay 0.5% of total pay bill, offset by a £15,000 annual allowance.

---

## Section 9 -- Common Payroll Patterns

### Pattern 1 -- Standard Monthly Employee (Category A)

Gross salary £3,500/month. Tax code 1257L.

1. PAYE: (£3,500 × 12 - £12,570) × 20% ÷ 12 = £595.50/month (cumulative calc)
2. Employee NIC: (£3,500 - £1,048) × 8% = £196.16/month
3. Employer NIC: (£3,500 - £417) × 15% = £462.45/month
4. Auto-enrolment pension (employee): (£3,500 - £520) × 5% = £149.00
5. Auto-enrolment pension (employer): (£3,500 - £520) × 3% = £89.40

### Pattern 2 -- Director NIC Calculation

Directors may use either the annual earnings period method (standard) or the alternative method (cumulative per pay period). The annual method defers NIC until cumulative earnings exceed the annual threshold. Most payroll software defaults to the annual method; the alternative method requires explicit election.

### Pattern 3 -- Starter with No P45

Apply HMRC starter checklist. Use one of three statements:
- A: First job since 6 April -- apply 1257L on cumulative basis
- B: Currently has another job -- apply BR
- C: Has another source of income -- apply BR

### Pattern 4 -- Statutory Payment Recovery

Standard employers recover 92% of SMP/SAP/ShPP/SPBP/SNCP. Small employers (Class 1 NIC ≤ £45,000 in qualifying year) recover 100% + 9% compensation (109% total from Apr 2026). SSP cannot be recovered.

---

## Section 10 -- Interaction with Other Skills

| Skill | Interaction |
|---|---|
| payroll-workflow-base | Provides generic payroll processing steps; this skill adds UK-specific rules |
| uk-bookkeeping | Payroll journals (gross pay, ER NIC, ER pension = P&L; net pay, PAYE/NIC liability, pension liability = BS) |
| uk-corporation-tax | Employer NIC and pension contributions are allowable deductions for CT |
| uk-vat | No VAT on wages, but benefits in kind may have VAT implications |

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CPA, EA, tax attorney, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/uk-payroll) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

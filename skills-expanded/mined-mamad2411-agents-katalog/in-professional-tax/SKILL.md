---
name: in-professional-tax
description: "> Use this skill whenever asked about Indian professional tax (profession tax). Trigger on phrases like \"professional tax India\", \"profession tax\", \"state professional tax\", \"Maharashtra professional tax\", \"Karnataka professional tax\", \"West Bengal professional tax\", \"PT registration\", \"PT return\", \"Section 16(iii)\", \"profession tax deduction\", or any question about professional tax obligations, rates, registration, or payment in India. This skill covers state-level professional tax rates and slabs for major states, deductibility under Income Tax Act, registration and filing requirements, and employer obligations. ALWAYS read this skill before touching any Indian professional tax work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: IN
  category: international
  quality: source-cited draft
  openaccountants_url: "https://openaccountants.com/skills/in-professional-tax"
  tax_year: 2025
  obligation: OTHER
---

# India Professional Tax -- State-Level Skill v1.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

---

## Section 1 -- Quick Reference

| Field | Value |
|---|---|
| Country | India (Republic of India) |
| Tax | Professional Tax (Profession Tax / PT) |
| Currency | INR only |
| Tax year | 1 April 2025 -- 31 March 2026 (FY 2025-26 / AY 2026-27) |
| Constitutional basis | Article 276 of the Constitution of India |
| Maximum permissible | ₹2,500 per annum (Constitutional cap per Article 276(2)) |
| Deductibility | Fully deductible under Section 16(iii) of Income Tax Act, 1961 |
| Skill version | 1.0 |

### Core Principle

Professional Tax is a **state-level tax** levied by state governments and union territories on individuals earning income through employment, trade, profession, or calling. Each state has its own rates, slabs, and administrative rules. The maximum amount any state can levy is ₹2,500 per annum (Constitutional limit).

### States That Levy Professional Tax

| State / UT | Levies PT? | Administering Authority |
|---|---|---|
| Maharashtra | Yes | Maharashtra State Tax on Professions, Trades, Callings and Employments Act, 1975 |
| Karnataka | Yes | Karnataka Tax on Professions, Trades, Callings and Employments Act, 1976 |
| West Bengal | Yes | West Bengal State Tax on Professions, Trades, Callings and Employments Act, 1979 |
| Andhra Pradesh | Yes | AP Tax on Professions, Trades, Callings and Employments Act, 1987 |
| Telangana | Yes | Telangana Tax on Professions, Trades, Callings and Employments Act |
| Tamil Nadu | Yes | Tamil Nadu Tax on Professions, Trades, Callings and Employments Act |
| Gujarat | Yes | Gujarat State Tax on Professions, Trades, Callings and Employments Act |
| Madhya Pradesh | Yes | MP Vritti Kar Adhiniyam, 1995 |
| Odisha | Yes | Orissa State Tax on Professions, Trades, Callings and Employments Act |
| Assam | Yes | Assam Professions, Trades, Callings and Employments Taxation Act |
| Kerala | Yes | Kerala Municipality Act (local bodies levy) |
| Bihar | Yes | Bihar Tax on Professions, Trades, Callings and Employments Act |
| Jharkhand | Yes | Jharkhand Tax on Professions Act |
| Meghalaya | Yes | Meghalaya Professions Tax Act |
| Tripura | Yes | Tripura Professions Tax Act |
| Sikkim | Yes | Sikkim Tax on Professions Act |
| Delhi | No | -- |
| Rajasthan | No | -- |
| Uttar Pradesh | No | -- |
| Haryana | No | -- |
| Punjab | No | -- |

### Conservative Defaults

| Ambiguity | Default |
|---|---|
| Unknown state of employment | Do not compute -- confirm state |
| Unknown gross salary / income slab | Do not compute -- obtain salary details |
| Unknown whether employer deducts PT | Assume employer deduction (most common for salaried) |

---

## Section 2 -- State-Wise Rates and Slabs

### 2.1 Maharashtra

| Monthly Gross Salary/Wages (INR) | Monthly PT | Annual PT |
|---|---|---|
| Up to ₹7,500 | Nil | Nil |
| ₹7,501 -- ₹10,000 | ₹175 | ₹2,100 |
| Above ₹10,000 | ₹200 (₹300 for Feb) | ₹2,500 |

**Note:** The February payment is ₹300 to make the annual total ₹2,500 (11 × ₹200 + 1 × ₹300).

**Who pays:** Salaried employees (employer deducts), self-employed professionals and traders (self-assess).

**Enrollment (employer):** Form I (Registration Certificate) -- every employer with PT liability.
**Enrollment (self-employed):** Form II.

**Filing:** Monthly payment by employers by the last day of following month.

### 2.2 Karnataka

| Monthly Gross Salary (INR) | Monthly PT |
|---|---|
| Up to ₹24,999 | Nil |
| ₹25,000 and above | ₹200 |

**Annual maximum:** ₹2,400 (₹200 × 12 months).

**Note:** Karnataka charges ₹200/month flat for those earning ₹25,000+ per month. This results in ₹2,400/year (below the ₹2,500 Constitutional cap).

**Filing:** Employer must deposit by the 20th of the following month. Annual return by 30 April.

### 2.3 West Bengal

| Monthly Gross Salary (INR) | Monthly PT |
|---|---|
| Up to ₹10,000 | Nil |
| ₹10,001 -- ₹15,000 | ₹110 |
| ₹15,001 -- ₹25,000 | ₹130 |
| ₹25,001 -- ₹40,000 | ₹150 |
| Above ₹40,000 | ₹200 |

**Annual maximum:** ₹2,500.

**Filing:** Monthly by the 21st of following month. Annual return by 31 May.

### 2.4 Andhra Pradesh

| Half-Yearly Gross Salary (INR) | Half-Yearly PT |
|---|---|
| Up to ₹15,000/month | Nil |
| ₹15,001 -- ₹20,000/month | ₹150/month |
| Above ₹20,000/month | ₹200/month (₹200 × 6 = ₹1,250 per half-year) |

**Annual maximum:** ₹2,500.

**Filing:** Monthly by 10th of following month.

### 2.5 Telangana

| Monthly Gross Salary (INR) | Monthly PT |
|---|---|
| Up to ₹15,000 | Nil |
| ₹15,001 -- ₹20,000 | ₹150 |
| Above ₹20,000 | ₹200 |

**Annual maximum:** ₹2,500.

### 2.6 Tamil Nadu

| Half-Yearly Gross Salary (INR) | Half-Yearly PT |
|---|---|
| Up to ₹21,000/month | Nil |
| ₹21,001 -- ₹30,000/month | ₹135/month |
| ₹30,001 -- ₹45,000/month | ₹315/month |
| ₹45,001 -- ₹60,000/month | ₹690/month |
| ₹60,001 -- ₹75,000/month | ₹1,025/month |
| Above ₹75,000/month | ₹1,250/half-year (₹2,500/year cap) |

**Annual maximum:** ₹2,500.

### 2.7 Gujarat

| Monthly Gross Salary (INR) | Monthly PT |
|---|---|
| Up to ₹5,999 | Nil |
| ₹6,000 -- ₹8,999 | ₹80 |
| ₹9,000 -- ₹11,999 | ₹150 |
| ₹12,000+ | ₹200 |

**Annual maximum:** ₹2,500 (adjustment in March).

### 2.8 Madhya Pradesh

| Monthly Gross Salary (INR) | Monthly PT |
|---|---|
| Up to ₹18,750 | Nil |
| ₹18,751 -- ₹25,000 | ₹125 |
| ₹25,001 -- ₹33,333 | ₹167 (₹2,000/year) |
| Above ₹33,333 | ₹208 (₹2,500/year) |

**Annual maximum:** ₹2,500.

---

## Section 3 -- Deductibility Under Income Tax Act

### Section 16(iii) -- Deduction from Salary Income

| Rule | Detail |
|---|---|
| Section | 16(iii) of the Income Tax Act, 1961 |
| Deduction basis | Allowed in the year of PAYMENT (not accrual) |
| Cap | No cap on deduction (but PT itself is capped at ₹2,500/year) |
| For self-employed | Deductible under Section 37(1) as business expenditure |
| ITR reporting | Shown as deduction from gross salary in Part B of Form 16 / ITR-1 |

### Impact on Tax Computation

| Step | Computation |
|---|---|
| Gross Salary | As per employer records |
| Less: Standard Deduction | ₹75,000 (FY 2025-26 under new regime; ₹50,000 under old regime) |
| Less: Professional Tax paid | Up to ₹2,500 (under old regime; included in standard deduction under new regime) |
| = Income from Salary | Taxable amount |

**New Tax Regime (Section 115BAC):** Under the new regime (default from FY 2023-24), the standard deduction of ₹75,000 covers both the standard deduction and profession tax deduction. Separate Section 16(iii) claim may not be additionally available under new regime.

**Old Tax Regime:** Professional tax is separately deductible under Section 16(iii) in addition to the ₹50,000 standard deduction.

---

## Section 4 -- Registration and Compliance

### 4.1 Employer Obligations

| Obligation | Detail |
|---|---|
| Registration | Obtain Profession Tax Registration Certificate (RC) from state authority |
| Deduction | Deduct PT from employee salary monthly as per slab |
| Deposit | Remit to state government by prescribed due date |
| Return filing | File periodic return (monthly/quarterly/annually per state) |
| Penalty for non-deduction | Varies by state (typically interest at 1-2% per month + penalty) |

### 4.2 Self-Employed / Professional Obligations

| Obligation | Detail |
|---|---|
| Enrollment | Obtain Profession Tax Enrollment Certificate (EC) from state authority |
| Self-assessment | Calculate PT based on gross income/turnover slab |
| Payment | Pay annually or as prescribed by state |
| Due date (Maharashtra) | 30 June of each year |
| Penalty | Interest on late payment + penalty per state rules |

### 4.3 Due Dates by State

| State | Employer Deposit Due | Return Due |
|---|---|---|
| Maharashtra | Last day of following month | Annual: 31 March |
| Karnataka | 20th of following month | Annual: 30 April |
| West Bengal | 21st of following month | Annual: 31 May |
| Andhra Pradesh | 10th of following month | Annual: varies |
| Gujarat | 15th of following month | Annual: 30 September |

---

## Section 5 -- Edge Cases

### 5.1 Multiple Employments
If an individual has multiple employers in the same state, each employer must deduct PT independently. The maximum combined deduction may exceed ₹2,500/year in practice -- the employee can claim refund of excess from the state authority.

### 5.2 Multi-State Employment
If an individual works in multiple states (e.g., transferred mid-year), PT is payable in each state for the period of employment in that state. Deduction under Section 16(iii) covers total PT paid across all states.

### 5.3 Directors
Company directors receiving sitting fees or remuneration are liable for PT in the state where the company is registered or where they attend meetings (varies by state).

### 5.4 Freelancers / Gig Workers
Self-employed professionals (doctors, lawyers, CAs, engineers, consultants) must self-enroll and pay PT in the state where they practice. Threshold varies by state.

### 5.5 Exemptions
Common exemptions across states:
- Parents/guardians of children with permanent disability (some states)
- Members of armed forces (some states)
- Persons above 65 years (some states, e.g., Maharashtra)
- Badli workers in textile industry (Maharashtra)

---

## Section 6 -- Filing Requirements Summary

| Item | Detail |
|---|---|
| Employer registration | Mandatory if employees earn above state threshold |
| Form 16 reporting | PT deducted shown in Part B under Section 16(iii) |
| ITR disclosure | Professional tax appears as deduction from gross salary |
| Proof required | Salary slip showing deduction; or PT challan (self-employed) |
| Records retention | 7 years (Income Tax Act record retention period) |

---

## Section 7 -- Prohibitions

- NEVER compute professional tax without knowing the STATE of employment/practice
- NEVER exceed ₹2,500/year for any state (Constitutional maximum)
- NEVER deduct PT under Section 16(iii) without evidence of actual payment
- NEVER apply one state's slabs to another state's employees
- NEVER assume PT applies in states that do not levy it (Delhi, UP, Rajasthan, Haryana, Punjab)
- NEVER double-claim PT deduction under both Section 16(iii) and Section 37(1) for the same amount
- NEVER present tax calculations as definitive -- always label as estimated

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a CA, CMA, or equivalent licensed practitioner in your jurisdiction) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/in-professional-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **source-cited draft**. For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

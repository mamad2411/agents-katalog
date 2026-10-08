---
name: za-provisional-tax
description: "Use this skill whenever asked about South African provisional tax (IRP6) for self-employed individuals. Trigger on phrases like \"IRP6\", \"provisional tax\", \"SARS provisional\", \"estimated tax South Africa\", \"first provisional period\", \"second provisional period\", \"third provisional\", \"underestimation penalty\", or any question about South African provisional tax obligations for self-employed persons. Covers first period (Aug 31), second period (Feb 28), voluntary third period (Sep 30), underestimation penalties, basic amount rules, and edge cases. ALWAYS read this skill before touching any South African provisional tax work."
license: AGPL-3.0-or-later (code) / OpenAccountants Guide License v1.0 (content)
metadata:
  source: openaccountants
  jurisdiction: INTL
  category: tax
  quality: accountant-reviewed
  openaccountants_url: "https://openaccountants.com/skills/za-provisional-tax"
  obligation: EST
  reviewed_by: "Werner Britz, CA(SA)"
---

# South Africa Provisional Tax (IRP6) -- Self-Employed Skill v2.0

> **General reference only.** This skill is general tax/accounting reference material for AI-assisted workflows. It has not been reviewed for any specific person's facts, documents, elections, deadlines, residency, filing status, or local procedures. Do not rely on it to file, pay, amend, or take a tax position without review by a qualified professional in the relevant jurisdiction.

## Section 1 -- Quick reference

| Field | Value |
|---|---|
| Country | South Africa |
| Authority | SARS (South African Revenue Service) |
| Primary legislation | Income Tax Act 58 of 1962, Fourth Schedule |
| Supporting legislation | Tax Administration Act 28 of 2011 |
| Year of assessment | 1 March to 28/29 February |
| First period due | 31 August |
| Second period due | 28/29 February |
| Third period (voluntary) | 30 September |
| Underestimation threshold (<= R1,800,000) | 90% of actual AND >= basic amount |
| Underestimation threshold (> R1,800,000) | 80% of actual (no safe harbour) |
| Penalty rate | 20% of shortfall |
| Interest rate (s89quat) | 10.25% p.a. from 2 March 2026 (on underpayment); 6.25% on overpayment refunds. Set quarterly by SARS by reference to repo rate. |
| Tax threshold (under 65, 2026) | R99,000 |
| Filing method | SARS eFiling (IRP6) |
| Currency | ZAR only |
| Contributor | Open Accountants |
| Validated by | Werner Britz CA(SA), Spurwing CFO |
| Validation date | May 2026 |

---

## Section 2 -- Required inputs and refusal catalogue

### Required inputs

Before computing, you MUST obtain:

1. **Is client a provisional taxpayer?** -- receives income not subject to PAYE?
2. **Year of assessment**
3. **Prior year taxable income** -- determines "basic amount"
4. **Estimated current year taxable income**
5. **PAYE credits?** -- offset against provisional tax
6. **Expected taxable income above R1,800,000?** -- different threshold

### Refusal catalogue

**R-ZA-PROV-1 -- Tax dispute / objection.** Trigger: client wants to object to SARS penalty. Message: "Objections to SARS penalties require qualified tax practitioner review. Escalate."

**R-ZA-PROV-2 -- Company provisional tax.** Trigger: question about company (not individual) provisional tax. Message: "This skill covers individuals only. Companies have different rules."

### Prohibitions

- NEVER estimate without asking about ALL income sources
- NEVER tell a client with income > R1.8M that basic amount protects them -- it does not
- NEVER advise that an estimate within tolerance protects against penalty if the payment is late. From 25 February 2026, the 20% underestimation penalty applies even where the estimate is correct but the payment is late.
- NEVER ignore PAYE credits
- NEVER confuse underestimation penalty (locked at second period) with s89quat interest (reducible via third period)
- NEVER assume third period is mandatory -- it is voluntary
- NEVER present provisional tax as a separate tax -- it is a prepayment
- NEVER compute penalties without both estimate AND actual
- NEVER use outdated SARS interest rates

---

## Section 3 -- Who is a provisional taxpayer

**Legislation:** ITA Fourth Schedule, paragraph 1

| Category | Provisional taxpayer? |
|---|---|
| Self-employed / sole proprietor | YES |
| Freelancer / contractor | YES |
| Rental income recipient | YES (if above threshold) |
| Non-executive director (NED fees, per BGR 40) | YES -- no PAYE on NED fees |
| Executive director (salary + director fees, PAYE deducted) | NO (not solely on account of director fees) |
| Salaried employee ONLY (all PAYE) | NO |
| Under 65, taxable income <= R99,000 | NO |

Exemption (para 18): A person is not a provisional taxpayer if they have no business income AND the total taxable income from interest, foreign dividends, rental, and remuneration from an unregistered employer does not exceed R30,000 for the year of assessment.

---

## Section 4 -- Payment periods, basic amount, and estimation

### Payment periods

| Period | Covers | Due date | Requirement |
|---|---|---|---|
| First (IRP6) | First 6 months | 31 August | Estimate full year; pay half of estimated tax |
| Second (IRP6) | Full year | 28 February | Estimate full year; pay balance |
| Third (voluntary) | Top-up | 30 September | Avoids interest on underpayment |

### Basic amount

The "basic amount" = taxable income per the latest preceding ASSESSMENT, EXCLUDING taxable capital gains, retirement lump sums, and severance benefits. Safe harbour benchmark for underestimation.

If the latest assessment is more than 14 months old at the IRP6 due date, increase the basic amount by 8% per annum (compounded) for each complete year beyond 14 months.

| Situation | Basic amount |
|---|---|
| Prior year assessed | Prior year taxable income (excl. capital gains, retirement lump sums, severance) |
| No prior assessment | Zero |
| Prior year loss | Zero |
| Latest assessment > 14 months old | Increase by 8% p.a. |

### Estimation rules

First period: no underestimation penalty (penalty applies only to second period).

Second period: accuracy thresholds apply (see Section 5).

---

## Section 5 -- Underestimation penalties

**Legislation:** ITA Fourth Schedule, paragraph 20

### Thresholds

| Taxable income | Penalty trigger |
|---|---|
| <= R1,800,000 | If estimate < 90% of actual AND estimate < basic amount |
| > R1,800,000 | If estimate < 80% of actual |

### Safe harbour

| Income | Safe harbour |
|---|---|
| <= R1.8M | Use basic amount as estimate -- NO penalty even if actual is higher |
| > R1.8M | No safe harbour -- must estimate within 80% |

### Penalty calculation

For income <= R1.8M:
```
penalty = 20% x (tax on LESSER of [basic amount] and [90% of actual] - tax on estimate)
```
The estimate amount does NOT feature directly -- SARS uses the basic amount as the floor.

For income > R1.8M:
```
penalty = 20% x (tax on 80% of actual - tax on estimate)
```

**Note:** From 25 February 2026, the 20% underestimation penalty also applies where the estimate is within tolerance but payment is late.

---

## Section 6 -- Third period and interest

### Third provisional payment (voluntary)

| Item | Detail |
|---|---|
| Due | 30 September |
| Purpose | Reduce s89quat interest |
| Mandatory? | NO |
| Effect | Reduces interest, NOT the underestimation penalty |

### Interest on underpayment (s89quat)

Rate 10.25% p.a. from 2 March 2026 (on underpayment); 6.25% on overpayment refunds. Set quarterly by SARS by reference to repo rate. Runs from period due date to payment date.

---

## Section 7 -- Registration, filing, and payment calculation

### Registration

Register as provisional taxpayer on eFiling or at SARS branch.

### Payment calculation

At each period, net out rebates and medical tax credits before halving or topping up:

```
first_period = ((estimated_annual_tax - rebates - medical_credits) - PAYE_for_6_months) / 2
second_period = (full_year_tax - rebates - medical_credits - PAYE_full_year) - first_provisional_payment
third_period = actual_tax - first_provisional - second_provisional - PAYE_full_year
```

---

## Section 8 -- Edge case registry

### EC1 -- New self-employed, no prior assessment
**Situation:** First year, no basic amount.
**Resolution:** Basic amount = zero. No safe harbour. Must estimate accurately.

### EC2 -- Just above R1.8M
**Situation:** Actual R1,900,000.
**Resolution:** Above R1.8M threshold. Must estimate within 80% (R1,520,000+). No basic amount safe harbour.

### EC3 -- Loss year followed by profit
**Situation:** Prior year loss, current R500,000.
**Resolution:** Basic amount = zero. No safe harbour.

### EC4 -- Employee with side income (below R1.8M)
**Situation:** Salary R800,000 + freelance R400,000 = R1,200,000.
**Resolution:** Provisional taxpayer. Below R1.8M threshold, so basic amount safe harbour applies. 90% of actual AND >= basic amount test. PAYE credited.

### EC5 -- Underestimation below R1.8M
**Situation:** Basic amount R400,000, estimate R350,000, actual R700,000.
**Resolution:** Estimate < basic amount, so penalty applies. Had client used R400,000 (the basic amount), no penalty.

### EC6 -- Third period timing
**Situation:** Realizes in August that second estimate too low.
**Resolution:** Third payment by Sep 30 reduces interest but not penalty.

### EC7 -- Mid-year commencement
**Situation:** Started business October 2024.
**Resolution:** Still must file second provisional by February 28. Flag for reviewer on first period.

### EC8 -- Cessation mid-year
**Situation:** Closes business November 2024.
**Resolution:** Still files second provisional by February 28.

### EC9 -- Capital gain in current year
**Situation:** Client sells property mid-year with R500,000 capital gain. Taxable capital gain (40% inclusion = R200,000).
**Resolution:** The R200,000 taxable capital gain must be included in the provisional tax estimate. However, it is EXCLUDED from the basic amount calculation (basic amount excludes taxable capital gains, retirement lump sums, and severance benefits).

### EC10 -- Late payment penalty
**Situation:** Estimate within 90% of actual (compliant) but payment one day late.
**Resolution:** Under amended paragraph 20 (effective 25 February 2026), the 20% underestimation penalty applies even where the estimate is correct but payment is late.

---

## Section 9 -- Reviewer escalation protocol

When a situation requires reviewer judgement:

```
REVIEWER FLAG
Tier: T2
Client: [name]
Situation: [description]
Issue: [what is ambiguous]
Options: [possible treatments]
Recommended: [most likely correct treatment and why]
Action Required: Qualified tax practitioner must confirm before advising client.
```

When a situation is outside skill scope:

```
ESCALATION REQUIRED
Tier: T3
Client: [name]
Situation: [description]
Issue: [outside skill scope]
Action Required: Do not advise. Refer to qualified tax practitioner. Document gap.
```

---

## Section 10 -- Test suite

### Test 1 -- Standard first period (2026/27 rates)
**Input:** Estimated annual taxable income R600,000. No PAYE.
**Expected output:** Tax = R44,136 + 26% x (R600,000 - R245,200) = R136,384 - R17,820 rebate = R118,564. First period = ~R59,282.

### Test 2 -- Second period, basic amount safe harbour
**Input:** Prior year R500,000. Actual R700,000. Estimate = R500,000.
**Expected output:** No penalty. Safe harbour applies (<= R1.8M, estimate >= basic amount).

### Test 3 -- Second period penalty (below R1.8M)
**Input:** Basic amount R400,000. Estimate R350,000. Actual R800,000.
**Expected output:** Estimate < basic amount. Penalty = 20% x (tax on LESSER of [basic amount R400,000] and [90% of actual R720,000] - tax on R350,000) = 20% x (tax on R400,000 - tax on R350,000).

### Test 4 -- Above R1.8M, no safe harbour
**Input:** Actual R2,000,000. Estimate R1,500,000. Basic amount R1,200,000.
**Expected output:** Above R1.8M. 80% of actual = R1,600,000. Estimate R1,500,000 < R1,600,000. Penalty = 20% x (tax on R1,600,000 - tax on R1,500,000).

### Test 5 -- Third period reducing interest
**Input:** Second estimate R500,000. Actual R800,000. Third payment R100,000 by Sep 30.
**Expected output:** Third reduces interest, not penalty.

### Test 6 -- Employee with side income (below R1.8M)
**Input:** Salary R900,000 (PAYE) + freelance R300,000 = R1,200,000.
**Expected output:** Below R1.8M. Basic amount safe harbour available. 90% of actual AND >= basic amount test. PAYE credited.

### Test 7 -- New taxpayer
**Input:** First year. No prior. Estimated R400,000.
**Expected output:** Basic amount = zero. No safe harbour.

### Test 8 -- Late payment penalty
**Input:** Estimate R700,000. Actual R750,000 (estimate within 90%). Payment submitted one day after due date.
**Expected output:** Under amended para 20 (effective 25 Feb 2026), 20% penalty applies despite estimate being within tolerance, because payment was late.

---

## Disclaimer

This skill and its outputs are provided for informational and computational purposes only and do not constitute tax, legal, or financial advice. Open Accountants and its contributors accept no liability for any errors, omissions, or outcomes arising from the use of this skill. All outputs must be reviewed and signed off by a qualified professional (such as a registered tax practitioner, CA(SA), or registered legal practitioner) before filing or acting upon.

The most up-to-date, verified version of this skill is maintained at [openaccountants.com](https://openaccountants.com). Log in to access the latest version, request a professional review from a licensed accountant, and track updates as tax law changes.

---

_Source: [OpenAccountants](https://openaccountants.com/skills/za-provisional-tax) — open tax Guides for AI, reviewed by named CPAs/CAs/EAs. Quality: **accountant-reviewed**. Reviewed by Werner Britz, CA(SA). For always-current figures and named-accountant backing, connect the OpenAccountants MCP server (`openaccountants-mcp`)._

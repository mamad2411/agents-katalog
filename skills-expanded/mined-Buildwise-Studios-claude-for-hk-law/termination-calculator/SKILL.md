---
name: termination-calculator
description: >
  Calculate statutory entitlements on termination of employment under the
  Hong Kong Employment Ordinance (Cap 57). Computes notice period, payment
  in lieu of notice, severance payment, long service payment (LSP),
  accrued annual leave pay, statutory holiday pay, end-of-year payment,
  and any MPF offset.
argument-hint: "[employee details: wages, length of service, termination reason, age]"
---

# /employment-legal:termination-calculator

1. Load `CLAUDE.md` for Cap 57 formulas and thresholds.
2. Gather the following inputs:
   - Monthly wages / daily wages
   - Date of commencement of employment
   - Planned date of termination
   - Reason for termination (redundancy, summary dismissal, notice, resignation, etc.)
   - Employee age
   - Employee's relevant income (for MPF calculation)
   - Employer MPF contributions (non-voluntary portion)
   - Any contractual notice period
3. Calculate each entitlement below.
4. Produce a termination statement with a summary table and inline `[verify]` tags.

## Calculations

### 1. Notice Period

| Continuous service | Statutory minimum |
|---|---|
| 1 month — < 3 years | 7 days |
| 3 years — < 5 years | 14 days |
| 5+ years | 1 month (30 days) |

- Contractual notice period controls if longer than statutory.
- Payment in lieu: wages at the employee's average wage rate.

**Flag:** Summary dismissal only for gross misconduct — verify the reason before proceeding with notice-less termination.

### 2. Severance Payment (Cap 57 Part VA)

**Eligibility:** 24+ months continuous employment, dismissed by reason of redundancy or laid off.

**Formula:**
- (Age 40+): (2/3) × [{Monthly wage capped at HK$22,500} or actual] × {Years of continuous service}
- (Under 40): (1/2) × [{Monthly wage capped at HK$22,500} or actual] × {Years of continuous service}

**Caps:**
- Maximum monthly wage for calculation: HK$22,500 `[verify]`
- Maximum severance payment: HK$390,000 `[verify]`

**MPF offset:** Severance may be reduced by employer's non-voluntary MPF contributions. Note: the abolition of MPF offsetting took effect May 2025 `[verify current status]`.

### 3. Long Service Payment (Cap 57 Part VB)

**Eligibility:** 5+ years continuous employment, not by redundancy or summary dismissal.

**Formula:** Same as severance payment formula above.

**Note:** Severance and LSP are mutually exclusive.

### 4. Accrued Annual Leave

- Entitlement: [Annual leave days per contract / 365] × [(Completed days in leave year up to termination date)]
- Pay: At the employee's average daily wage rate (Cap 57 s.41ZC).
- Unused leave carried over: pay out at the rate applicable.

### 5. Statutory Holiday Pay

- If termination date is within 7 days of a statutory holiday, holiday pay is due.
- Employees entitled to statutory holiday pay if they have been employed under a continuous contract for at least 3 months immediately preceding the holiday (Cap 57 s.39).

### 6. End-of-Year Payment (Contractual)

- Pro-rata entitlement on termination except summary dismissal for misconduct (Cap 57 s.13).

### 7. Notice Pay (if payment in lieu)

Calculated at the employee's average daily wage × number of days of notice period.

**Average daily wage (Cap 57 s.2(3)):** Wages earned in the 12 months preceding the termination divided by the number of actual working days (or 365 days for capped calculations).

## Output

| Entitlement | Amount (HK$) | Notes |
|---|---|---|
| Notice period | HK$ [N] | [days/months] |
| Severance / LSP | HK$ [N] | [eligible/not] |
| Accrued annual leave | HK$ [N] | [days] |
| Statutory holiday pay | HK$ [N] | [holiday dates] |
| End-of-year payment | HK$ [N] | [pro-rata/full] |
| **Total** | **HK$ [N]** | |

Append: `⚠️ All calculations are estimates based on Cap 57 formulas. Verify against the employee's records and current statutory thresholds. Review with a licensed HK solicitor or barrister before making payment.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

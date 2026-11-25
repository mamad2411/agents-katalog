---
name: workplace-injury
description: >
  Employees' compensation claim procedure under the Employees' Compensation
  Ordinance (Cap 282). Assesses whether an injury arises out of and in the
  course of employment, calculates compensation entitlements, identifies
  employer duties (notification, insurance, reporting), and guides the
  claims process before the Employees' Compensation Assessment Board, the
  District Court, or the Labour Tribunal.
argument-hint: "[describe the work injury — nature, circumstances, injuries, employment details]"
---

# /employment-legal:workplace-injury

1. Load `CLAUDE.md` for the Cap 282 framework.
2. Gather facts: employment details, injury circumstances, injury type, medical evidence, notice given.
3. Walk the assessment checklist.
4. Produce a claim assessment report with compensation estimate and procedural guidance.

## Assessment Checklist

### 1. Scope of Coverage (Cap 282)

- [ ] Is the person an "employee" under Cap 282 s.3? (Includes casual workers, apprentices, outworkers.)
- [ ] Did the injury arise out of and in the course of employment? (s.5)
- [ ] Was the injury by accident? (Includes occupational diseases under Schedule 2.)
- [ ] Excluded cases: self-inflicted injury, intoxication (drugs/alcohol), failure to use safety equipment (may reduce but not bar compensation — s.5(2)).

### 2. Employer Duties

- [ ] **Insurance (s.40):** Employer must maintain employees' compensation insurance with an authorised insurer.
  - Penalty: fine of up to HK$100,000 AND imprisonment up to 2 years.
  - Display of insurance certificate in the workplace.
- [ ] **Notification (s.15):** Employer must notify the Commissioner for Labour within 14 days of an accident resulting in death or incapacity exceeding 3 days.
  - Form: LD 248 (Employer's Report of Occupational Accident)
- [ ] **First Aid / Medical Treatment (s.56):** Employer must arrange free medical treatment for the injured employee.

### 3. Employee Duties

- [ ] Notice to employer within a reasonable time (s.14)
- [ ] Claim filing within 24 months of the accident (s.14(2))

### 4. Compensation Calculation

| Category | Formula |
|---|---|
| **Permanent total incapacity** | Percentage of monthly earnings × age-based multiplier (specific schedules in Cap 282) `[verify current rates]` |
| **Permanent partial incapacity** | PTI amount × percentage of loss of earning capacity (assessed by the Assessment Board) |
| **Temporary incapacity** | 4/5 of monthly earnings for the period of incapacity (max period determined by medical evidence) |
| **Medical expenses** | Up to prescribed schedule caps `[verify]` |
| **Death** | Compensation to dependants: age-based formula + funeral expenses |

**Earnings cap for calculation:** Cap 282 s.10 — monthly earnings capped for calculation purposes `[verify current cap]`.

### 5. Assessment Procedure

| Step | Process |
|---|---|
| **Medical assessment** | Assessment Board (appointed by the Commissioner for Labour) assesses degree of permanent incapacity |
| **Certificate of assessment** | Binding on both employer and employee unless challenged in the District Court within 6 months |
| **Payment** | Employer must pay compensation within 21 days of assessment (s.12) |
| **Dispute** | Either party may challenge the assessment in the District Court (Cap 282 s.18) |

### 6. Prohibited Dismissal (Cap 282 s.48)

- Employer must not dismiss an employee while the employee is in receipt of temporary incapacity payments.
- **Penalty:** Fine up to HK$100,000.

### 7. Rehabilitation (Cap 282 Part IIB)

- Employer must offer re-employment or suitable alternative work to employees recovering from work injuries.
- Ordinance provides financial incentives/duties for retraining and re-employment.

## Output

| Item | Assessment |
|---|---|
| Injury scope | [Covered / Potentially excluded / Excluded] |
| Compensation type | [Temp incapacity / PTI / PPI / Death] |
| Estimated compensation | HK$ [range] |
| Employer compliance | [✅ / 🔴 Check] |
| Next steps | [Procedure to follow] |

**Append:** `⚠️ This is not legal advice or a formal assessment. Verify the injury against Cap 282, the Assessment Board's guidelines, and current schedules. Review with a licensed HK solicitor or barrister before proceeding with any claim.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

---
name: contract-review
description: >
  Review employment contracts (offer letters, employment agreements, and
  service agreements) for compliance with the Hong Kong Employment Ordinance
  (Cap 57). Checks statutory particulars, contract terms, wage provisions,
  leave entitlements, termination clauses, restrictive covenants, MPF
  arrangements, and anti-discrimination protections.
argument-hint: "[paste or attach the employment contract]"
---

# /employment-legal:contract-review

1. Load `CLAUDE.md` in the plugin root for the full legislative framework.
2. Offer the work-product header: `RESEARCH NOTES — NOT LEGAL ADVICE — REVIEW WITH A LICENSED HK SOLICITOR OR BARRISTER BEFORE ACTING`.
3. Walk the checklist below.
4. Produce a compliance review with flagged issues (`[verify]`, `[review]`).

## Checklist

### 1. Statutory Particulars (Cap 57 s.42C)

Does the contract include all required particulars:
- [ ] Name of employer and employee
- [ ] Job title and description
- [ ] Date of commencement of employment
- [ ] Wage rate, wage period, and method of calculation
- [ ] End-of-year payment details (if any)
- [ ] Notice period for termination
- [ ] Annual leave entitlement
- [ ] Sickness allowance and sick leave
- [ ] Maternity / paternity leave (where applicable)
- [ ] Statutory holiday entitlement
- [ ] MPF arrangement
- [ ] Overtime policy (if applicable)

**Flag:** Missing particulars. Employer must provide within 60 days of commencement.

### 2. Wage Provisions (Cap 57 Part III–IVA)

- [ ] Wage period ≤ 1 month?
- [ ] Deduction clause compliant with s.32?
- [ ] Minimum wage (Cap 608) referenced or confirmed `[verify current rate]`?
- [ ] End-of-year payment (contractual) or ex-gratia?

### 3. Leave Entitlements

- [ ] Annual leave at or above Cap 57 s.41A minimum?
- [ ] Sickness allowance aligned with s.33 (4/5 pay, medical certificate)?
- [ ] Maternity leave — 14 weeks at 4/5 pay?
- [ ] Paternity leave — 5 days at 4/5 pay?
- [ ] Statutory holidays — at least 12 designated holidays?

### 4. Termination Provisions (Cap 57 Part V)

- [ ] Notice period ≥ statutory minimum
- [ ] Payment in lieu of notice permitted and correctly stated
- [ ] Summary dismissal clause — "gross misconduct" defined or too broad?
- [ ] Redundancy procedure referenced?
- [ ] Waiver of notice prohibited (s.70 — cannot contract out of Cap 57)

**Flag:** Any clause purporting to waive statutory rights (s.70 renders such clauses void).

### 5. Restrictive Covenants

- [ ] Non-compete clause — legitimate business interest? Reasonable scope/geography/duration?
- [ ] Non-solicit clause — customers or employees?
- [ ] Non-dealing clause — overly broad?
- [ ] Garden leave provision?

**Flag:** Enforceability under HK common law requires legitimate business interest + reasonableness + not contrary to public policy. Blue pencil test applies.

### 6. MPF Provisions (Cap 485)

- [ ] MPF contribution obligation stated?
- [ ] Employer contribution at least 5% of relevant income?
- [ ] Voluntary contributions (if any) defined?

### 7. Data Privacy (PDPO Cap 486)

- [ ] Personal data collection clause present?
- [ ] Data retention and use limitation stated?
- [ ] Cross-border data transfer acknowledged?

## Output

Produce a compliance matrix (✅ Compliant / ⚠️ Needs Attention / 🔴 Non-compliant) with inline tags for verification and review items.


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

---
name: discrimination-screener
description: >
  Screen a factual scenario for potential discrimination claims under Hong
  Kong's anti-discrimination ordinances: Sex Discrimination Ordinance
  (Cap 480), Disability Discrimination Ordinance (Cap 487), Family Status
  Discrimination Ordinance (Cap 527), and Race Discrimination Ordinance
  (Cap 602). Identifies potential claims, enforcement routes (EOC, District
  Court), and recommended next steps.
argument-hint: "[describe the factual scenario — treatment, comments, policies, or decisions]"
---

# /employment-legal:discrimination-screener

1. Load `CLAUDE.md` for the anti-discrimination framework (protected characteristics, prohibited conduct, remedies).
2. Gather the full factual matrix from the user.
3. Screen against each ordinance below.
4. Produce a screening report with severity ratings and recommended next steps.

## Screening Checklist

### Cap 480 — Sex Discrimination Ordinance

| Indicator | Check |
|---|---|
| Differential treatment based on sex, marital status, pregnancy, or breastfeeding | [ ] |
| Sexual harassment (unwelcome conduct of a sexual nature creating a hostile environment) | [ ] |
| Less favourable treatment of women/men compared to the opposite sex in comparable circumstances | [ ] |
| Victimisation (punishing someone for making a complaint or giving evidence) | [ ] |
| Pregnancy-related discrimination (refusing promotion, termination, unfavourable assignment) | [ ] |

**Key sections:** ss. 6–9 (direct/indirect discrimination), s.14 (employment), s.39 (harassment), s.43 (victimisation).

**Remedies:** Damages (including injury to feelings, aggravated damages), declaration, injunction, recommendation for reinstatement or re-engagement.

### Cap 487 — Disability Discrimination Ordinance

| Indicator | Check |
|---|---|
| Less favourable treatment due to physical/mental disability | [ ] |
| Failure to make reasonable accommodation | [ ] |
| Unfavourable terms and conditions due to disability | [ ] |
| Harassment / vilification | [ ] |
| Victimisation | [ ] |

**Key sections:** ss. 6–9, s.12 (employment), s.25 (harassment).

**Note:** Hong Kong's DDO does not explicitly require "reasonable accommodation" as a positive duty — the duty arises from the prohibition against indirect discrimination. Accommodation may be required to ensure a disabled person can carry out the inherent requirements of the job.

### Cap 527 — Family Status Discrimination Ordinance

| Indicator | Check |
|---|---|
| Less favourable treatment due to family responsibilities (caring for a dependent family member) | [ ] |
| Refusal to grant flexible working arrangements | [ ] |
| Disadvantageous treatment compared with employees without dependants | [ ] |

**Key sections:** ss. 5–8.

### Cap 602 — Race Discrimination Ordinance

| Indicator | Check |
|---|---|
| Less favourable treatment based on race, colour, descent, ethnic origin | [ ] |
| Racial harassment | [ ] |
| Vilification (inciting racial hatred) | [ ] |
| Victimisation | [ ] |
| Discriminatory recruitment / promotion / redeployment | [ ] |

**Key sections:** ss. 4–8, s.9 (employment), s.27 (harassment), s.32 (vilification).

## Enforcement

### EOC Process

1. **Complaint to EOC** — written complaint, investigation, attempted conciliation.
2. **Legal assistance** — EOC may provide legal assistance to the complainant (funding representation).
3. **District Court proceedings** — if conciliation fails, complainant may issue proceedings in the DC (this is the exclusive remedy; no separate Labour Tribunal claim for discrimination).

### Time Limits

- **District Court proceedings:** Within 24 months of the discriminatory act (Cap 480 s.76; Cap 487 s.71; Cap 527 s.66; Cap 602 s.74).

### Burden of Proof

- Complainant establishes prima facie case → burden shifts to respondent to prove there was no discrimination.

### Remedies Available

- Damages (including injury to feelings — currently capped at approximately HK$250,000–300,000 for the most serious cases `[verify current EOC guidelines]`)
- Aggravated damages (for high-handed, oppressive conduct)
- Injunction
- Declaration
- Order for reinstatement/re-engagement
- Order for apology

## Output

| Ordinance | Potential Claim | Severity | Likelihood | Recommendation |
|---|---|---|---|---|
| Cap 480 | [Y/N/Maybe] | 🔴/🟠/🟡/🟢 | [Low/Medium/High] | [Action] |
| Cap 487 | [Y/N/Maybe] | 🔴/🟠/🟡/🟢 | [Low/Medium/High] | [Action] |
| Cap 527 | [Y/N/Maybe] | 🔴/🟠/🟡/🟢 | [Low/Medium/High] | [Action] |
| Cap 602 | [Y/N/Maybe] | 🔴/🟠/🟡/🟢 | [Low/Medium/High] | [Action] |

Append a decision tree: EOC conciliation, legal advice, internal investigation, or litigation preparation.


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

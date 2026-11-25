---
name: divorce-petition
description: >
  Guide legal practitioners through the process of preparing, filing, and prosecuting a divorce petition in Hong Kong under the Matrimonial Causes Ordinance (Cap 179), including drafting the petition, service, and securing decree nisi and decree absolute.
---
# Divorce Petition — Skill

## Purpose

Guide legal practitioners through the process of preparing, filing, and prosecuting a divorce petition in Hong Kong under the Matrimonial Causes Ordinance (Cap 179), including drafting the petition, service, and securing decree nisi and decree absolute.

## Scope

- Ground for divorce: irretrievable breakdown (s.11, Cap 179)
- The five facts (s.11A–11E)
- The one-year bar (s.12)
- Petition drafting and filing
- Undefended special procedure
- Decree nisi and decree absolute
- Judicial separation and nullity

## Workflow

### 1. Eligibility and Jurisdiction

- **Domicile**: Either party domiciled in HK
- **Habitual residence**: Either party has been habitually resident in HK for at least one year immediately preceding the petition
- **One-year bar**: No petition within the first year of marriage (s.12) except exceptional hardship or depravity

### 2. Choose the Appropriate Fact

**s.11A — Adultery**
- Petitioner finds it intolerable to live with respondent (subjective test)
- Must name the co-respondent unless excused
- Risk: petitioner may be treated as having condoned the adultery

**s.11B — Unreasonable Behaviour**
- Broadest and most commonly used fact
- Respondent has behaved so that petitioner cannot reasonably be expected to live with them (objective test)
- Details should be particularised — specific examples required
- No co-respondent needed

**s.11C — Desertion**
- Continuous period of at least two years
- Must prove: de facto separation, animus deserendi, no consent, no just cause

**s.11D — Two Years' Separation with Consent**
- Must prove living apart for two continuous years
- Respondent's written consent required
- Respondent may withdraw consent before decree nisi

**s.11E — Five Years' Separation**
- No consent needed
- Respondent may oppose on grounds of grave financial or other hardship (s.16)
- Court may dismiss if in all circumstances it would be wrong to dissolve

### 3. Draft Petition

**Contents of Petition (Form 2, Matrimonial Causes Rules)**:
- Names, addresses, and occupations of parties
- Date and place of marriage
- Names and dates of birth of children
- Whether any previous proceedings
- Ground for divorce and the fact(s) relied upon
- Statement of jurisdiction
- Prayer — dissolution, ancillary relief, costs, children arrangements

**Practice Notes**:
- Particulars of behaviour must be sufficient but not excessive (avoid "shopping lists")
- For adultery, avoid naming the co-respondent unless essential
- Include prayer for ancillary relief (financial, property, children)

### 4. File Petition

- File at the **Family Court** (District Court) or **Court of First Instance**
- Enclosures: certified copy of marriage certificate, filing fee (HK$630 for DC)
- Petition will be sealed and issued by the court

### 5. Service

- **Personal service** on the respondent (unless dispensed with)
- **Acknowledgment of Service** — form 6 (Matrimonial Causes Rules)
- Time for filing: 8 days (HK address) or 21 days (overseas address)
- If no acknowledgment filed: **deemed service** or **substituted service** application

### 6. Undefended Special Procedure

- If respondent does not file an answer within 14 days
- Petitioner files affidavit in support (Form 3)
- Court considers papers in chambers
- Decree nisi granted — no oral hearing required

### 7. Decree Nisi → Decree Absolute

- **Decree Nisi**: Provisional divorce order
- **Six-week cooling off period**: No application for decree absolute before 6 weeks from decree nisi
- **Decree Absolute**: Final dissolution (Form 9 application)
- Certificates of decree nisi and decree absolute are issued

### 8. Ancillary Relief Applications

Ancillary relief should be applied for in the prayer or by separate notice:
- Financial disclosure (Form E — Statement of Financial Position)
- First appointment for directions
- Financial Dispute Resolution hearing (FDR)
- Final hearing

### 9. Judicial Separation (s.24)

- Same facts as divorce but no dissolution
- Allows parties to live apart without ending the marriage
- Useful where religious objections or pension considerations apply

## Key Sections

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.11 | Ground for divorce | Irretrievable breakdown |
| s.12 | One-year bar | No petition within 1 year of marriage |
| s.11A–E | Five facts | Adultery, behaviour, desertion, 2yr sep (consent), 5yr sep |
| s.16 | Grave hardship | Defence to 5-year separation |
| s.24 | Judicial separation | Alternative to divorce |
| s.20–24 | Nullity | Void and voidable marriages |

## Common Pitfalls

- **One-year bar**: Check the marriage anniversary date carefully — filing early is wasted costs
- **Particulars of behaviour**: Too vague = struck out; too detailed = oppressive; balance required
- **Adultery**: Need to prove opportunity and inclination; cannot rely on suspicion
- **Consent withdrawal**: Respondent may withdraw consent at any time before decree nisi
- **Condonation**: Resuming cohabitation after knowledge of adultery may bar the petition (s.15A)
- **Costs**: In undefended cases, the petitioner may not get costs unless there is unreasonable conduct

## Tools & Resources

- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Matrimonial Causes Ordinance (Cap 179)
- Matrimonial Causes Rules (Cap 179A) — procedural forms
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — District Court Ordinance (Cap 336)
- Judiciary Practice Directions — family proceedings


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

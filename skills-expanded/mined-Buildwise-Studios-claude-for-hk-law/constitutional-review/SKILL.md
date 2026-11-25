---
name: constitutional-review
description: >
  Analyse and advise on constitutional issues arising under the Hong Kong Basic Law, including fundamental rights, NPCSC interpretations, judicial review, and the relationship between HKSAR legislation and the Basic Law.
---
# Constitutional Review — Skill

## Purpose

Analyse and advise on constitutional issues arising under the Hong Kong Basic Law, including fundamental rights, NPCSC interpretations, judicial review, and the relationship between HKSAR legislation and the Basic Law.

## Scope

- Judicial review of legislation for BL compliance
- Fundamental rights under Chapter III (Arts 24–42)
- Proportionality analysis under BL rights provisions
- NPCSC interpretations and their binding effect
- Impact of Annex III national laws on local legislation
- Interaction between BL and international human rights instruments

## Workflow

### 1. Identify the Constitutional Issue

- Does the matter involve a BL right or freedom?
- Does the legislation or government action potentially infringe a BL provision?
- Is there an NPCSC interpretation relevant to the interpretation of the relevant provisions?
- Is the issue within HKSAR autonomy or does it involve Central Government responsibilities?

### 2. Research the Law

- Consult the relevant BL articles (original Chinese text preferred)
- Check for any NPCSC interpretation on point
- Search CFA and Court of Appeal decisions interpreting the provisions
- Review commentary (HKLII, Westlaw Asia, HK Law Journal)
- Check Annex III for applicable national laws

### 3. Apply the Legal Framework

- **Standard of review**: HKSAR courts apply proportionality review for BL rights
- **Burden**: Shifts to government after prima facie interference is shown
- **Test**: Legitimate aim → rational connection → minimal impairment → proportionality stricto sensu
- **Remedies**: Declaration of invalidity, severance, reading down

### 4. Draft Analysis

- State the constitutional provisions engaged
- Analyse whether the measure pursues a legitimate aim
- Apply proportionality analysis
- Assess whether NPCSC interpretation would affect the analysis
- Conclude on BL compliance and propose next steps

## Common Issues

| Issue | Relevant BL Provisions | Key Cases |
|-------|------------------------|-----------|
| Right of abode | Arts 22, 24(2)–(3) | Ng Ka Ling (1999), Vallejos (2016) |
| Freedom of speech | Art 27 | Yeung May Wan (2005), Wong Hin Wai (2020) |
| Freedom of assembly | Arts 27, 39 | Leung Kwok Hung (2005) |
| Equality before law | Art 25 | Secretary for Justice v Yau Yuk Lung (2007) |
| Property rights | Art 6, 105 | HKSAR v Ma Wai Fong (2002) |
| Electoral rights | Arts 26, Annex II | Kwok Cheuk Kin (2022) |
| Judicial independence | Arts 80, 85, 88 | Re Chief Justice (2020) |

## Tools & Resources

- HKLII (https://www.hklii.hk) — Basic Law case law
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Consolidated BL text
- CLAUDE.md for practice profile and landmark cases


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

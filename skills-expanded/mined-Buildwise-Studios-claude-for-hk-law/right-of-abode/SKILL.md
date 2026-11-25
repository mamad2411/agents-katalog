---
name: right-of-abode
description: >
  Guide legal practitioners through the analysis and determination of right of abode claims under Basic Law Article 24 and Part VII of the Immigration Ordinance (Cap 115), including verification procedures, certificate of entitlement, and judicial review options.
---
# Right of Abode — Skill

## Purpose

Guide legal practitioners through the analysis and determination of right of abode claims under Basic Law Article 24 and Part VII of the Immigration Ordinance (Cap 115), including verification procedures, certificate of entitlement, and judicial review options.

## Scope

- Basic Law Article 24 categories of permanent residents
- Part VII of Cap 115 — statutory provisions
- Certificate of entitlement (CERT) procedure
- Ordinary residence analysis (7-year continuous period)
- Verification of status by the Director of Immigration
- Children's right of abode (born in HK / born abroad to permanent residents)
- Non-Chinese permanent residents and the "ordinarily resident" test
- Judicial review of refusal decisions

## Workflow

### 1. Establish the Applicant's Category

Determine which BL Art 24 category applies:

**Category 1:** Chinese citizen born in Hong Kong (before or after establishment)
**Category 2:** Chinese citizen who has ordinarily resided in HK for 7+ continuous years
**Category 3:** Person of Chinese nationality born outside HK to a parent in Category 1 or 2
**Category 4:** Non-Chinese person with valid documents, 7+ years ordinary residence
**Category 5:** Person under 21 born to a parent in Category 4
**Category 6:** Person with right of abode only (limited category)

### 2. Gather Evidence

**For birth in Hong Kong:**
- Hong Kong birth certificate
- Proof of Chinese citizenship (HKID card, HKSAR passport, or certificate of nationality)

**For 7-year ordinary residence:**
- Employment records and tax returns
- Rental agreements or property ownership
- Bank statements, utility bills
- School records (if applicable)
- Periods of absence and their justification

**For parentage claims:**
- Parent's permanent resident status proof
- Birth certificate linking applicant to parent
- Proof of Chinese nationality
- DNA testing if parentage is disputed

### 3. Certificate of Entitlement (CERT) Application

- Required for persons claiming right of abode while outside HK
- Form ROP 183
- Submitted to the Director of Immigration
- Supporting documentation: birth certificate, parents' HKIDs, residence proof
- Processing time: 3–6 months (standard); may extend with verification
- Refusal triggers the right to make further representations or seek judicial review

### 4. The "Ordinary Residence" Test

Key factors established in **Vallejos v Commissioner of Registration (2013):**
- Physical presence in HK (must be more than merely casual)
- Voluntary and for a settled purpose
- Ordinary and habitual character
- Can be temporary or permanent in nature
- Employment in HK is strong evidence but not determinative
- Short breaks (holidays, business trips) do not break continuity

### 5. Verification Procedure

- Director may require interview, further documents, or site visits
- DNA testing for parentage claims
- Reference checks with employers, schools, landlords
- Immigration records check for overstay or employment breaches
- Verification of identity documents and travel records

### 6. Refusal and Judicial Review

- **Grounds for refusal:**
  - Insufficient evidence of ordinary residence
  - Gaps in 7-year continuity
  - Breach of immigration conditions during the 7-year period
  - Failure to establish Chinese nationality
  - Parentage not established

- **Options:**
  - Representations to the Director (reconsideration)
  - Appeal to the Immigration Tribunal
  - Application for Leave to Apply for Judicial Review

## Key Case Law

- **Ng Ka Ling v Director of Immigration (1999) 2 HKCFAR 4** — CFA landmarks: right of abode categories, NPCSC interpretation
- **Lau Kong Yung v Director of Immigration (1999) 2 HKCFAR 300** — binding nature of NPCSC interpretations
- **Director of Immigration v Chong Fung Yuen (2001) 4 HKCFAR 211** — children born in HK to non-permanent parents
- **Vallejos v Commissioner of Registration (2013) 16 HKCFAR 45** — domestic helpers and ordinary residence
- **Fateh Muhammad v Commissioner of Registration (2020) 23 HKCFAR 529** — proof of continuous ordinary residence
- **Re an Applicant for Right of Abode [2022] HKCFI** — standard of proof

## Practice Notes

- The burden of proof is on the applicant to establish right of abode on a balance of probabilities
- Periods of imprisonment or overstay do not count toward ordinary residence
- Voluntary departure from HK for more than 6 months in a single absence may break continuity
- For Category 3 claims, the parent must have been a permanent resident at the time of the child's birth
- "Permanent resident" status is different from "right of abode" — a person may have one without the other
- Consider alternative pathways: Certificate of Entitlement vs Right of Abode Verification (for those already in HK)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

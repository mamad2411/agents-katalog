---
name: visa-employment
description: >
  Guide legal practitioners through the review and preparation of employment visa applications under the General Employment Policy (GEP), Supplementary Labour Scheme (SLS), and related employment-based admission schemes in Hong Kong.
---
# Employment Visa — Skill

## Purpose

Guide legal practitioners through the review and preparation of employment visa applications under the General Employment Policy (GEP), Supplementary Labour Scheme (SLS), and related employment-based admission schemes in Hong Kong.

## Scope

- General Employment Policy (GEP) for professionals
- Supplementary Labour Scheme (SLS) for medium-skilled workers
- Dependant visa eligibility for spouses and children
- Application documentation and supporting evidence
- Immigration Department processing standards
- Extension of stay and change of employer
- Refusal grounds and appeal options

## Workflow

### 1. Initial Assessment

- Determine the applicant's nationality and visa-free access to HK
- Identify the correct scheme: GEP (professionals/managerial) vs SLS (medium-skilled labour)
- Assess the employer's eligibility (must be a Hong Kong registered company)
- Verify that the job cannot be readily filled locally (labour market test)
- Check for any applicable bilateral agreements or sector-specific rules

### 2. Document Checklist

**Employer Documents:**
- Form ID(E) 1000A (employer application)
- Business registration certificate
- Company profile, financial statements
- Supporting letters justifying the hire
- Employment contract (terms, salary, duration)
- Local recruitment evidence (newspaper/online ads, JOSM posting)

**Employee Documents:**
- Form ID(E) 1000B (employee application)
- Valid passport (at least 12 months remaining)
- Academic/professional qualifications
- CV and employment history
- Character references
- Latest photograph
- Proof of residence (if applying outside HK)

### 3. Application Submission

- Lodged with the Visa and Policy Division, Immigration Department
- Processing time: 4–6 weeks (standard); 2 weeks (expedited for tech roles under TechTAS)
- Fee: HK$230 (standard processing)
- PD Online system for electronic submission

### 4. Immigration Department Assessment Criteria

- **Genuine vacancy** — no suitable local candidate
- **Relevant qualifications** — degree or professional certification required
- **Relevant experience** — minimum 2 years post-qualification experience recommended
- **Salary benchmark** — should be at market rate for the role (ImmD may request comparables)
- **Company viability** — active business, substantive operations in HK

### 5. Approval and Conditions

- 2-year initial visa (renewable for 2+3+3 under standard pattern)
- Condition of stay: employment with sponsored employer
- Change of employer: new application required
- Permission to take up part-time work (approved categories)
- Dependant visas: spouse may work; children may attend school

### 6. Refusal and Re-application

- **Common refusal grounds:**
  - Insufficient qualifications for the role
  - Poor local recruitment exercise
  - Company does not have substantive presence in HK
  - Salary below market benchmark
  - Adverse immigration history
- **Re-application:** New application permitted with strengthened documentation
- **Appeal:** To the Immigration Tribunal within 28 days

## Key Legislation

| Provision | Relevance |
|-----------|-----------|
| Cap 115, s.2A | Definition of "genuine vacancy" |
| Cap 115, s.11 | Prohibited immigrants |
| Immigration Regulations, Reg 2 | Visa conditions |
| Immigration Policy Branch circulars | Current processing guidelines |

## Case Law Guidance

- **R v Director of Immigration, ex parte Sin Hoi-lam [1990]** — scope of Director's discretion in visa decisions
- **Re an Applicant for Leave to Apply for Judicial Review [2020] HKCFI 1234** — judicial review of visa refusal
- **TTV v Director of Immigration [2021] HKCA** — procedural fairness in visa processing

## Practice Notes

- Entry into force of the company's substantive operations is a common sticking point — advise startups to demonstrate active business pre-application
- For senior executives, consider the "Top Tier" fast-track processing (5 working days)
- GEP applications from Mainland China require a separate exit endorsement from the Mainland authorities
- Dependant visas are generally approved for spouses and unmarried children under 18
- Overstay history may disqualify or trigger enhanced scrutiny


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

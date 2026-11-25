---
name: pia-hk
description: Conduct a Privacy Impact Assessment (PIA) under the Hong Kong Personal Data (Privacy) Ordinance (Cap 486), covering data mapping, DPP compliance analysis, risk assessment, and remediation planning.
---

# PIA (HK) — Skill

## Purpose

Conduct a Privacy Impact Assessment (PIA) under the Personal Data (Privacy) Ordinance (Cap 486), evaluating data processing activities against the six Data Protection Principles (DPP1-6) and recommending remediation measures. While PIAs are not legally required under the PDPO (unlike the EU GDPR), they are strongly recommended by the PCPD as best practice, particularly for high-risk processing activities.

## Scope

- Data inventory and mapping
- DPP1-6 compliance analysis
- Direct marketing assessment
- Cross-border transfer analysis
- Third-party processor risk assessment
- Data breach vulnerability assessment
- Remediation planning and recommendations
- PIA report preparation

## Workflow

### 1. Scope Definition

- Identify the processing activity or system under review
- Define the business context and purpose of processing
- Determine which data subjects are affected
- Identify all data flows (collection, use, storage, transfer, deletion)
- Set assessment boundaries

### 2. Data Mapping

Create a data inventory covering:

- **Data categories**: personal identifiers, financial, health, biometric, location, behavioural, special categories
- **Data subjects**: customers, employees, clients, website visitors, job applicants, third parties
- **Collection sources**: direct from data subject, third-party sources, publicly available, automated collection
- **Processing purposes**: service delivery, marketing, HR, analytics, compliance, security
- **Storage locations**: on-premise, cloud (Hong Kong, mainland China, overseas), third-party systems
- **Data retention**: scheduled deletion, legal hold, archival
- **Data sharing**: internal departments, external processors, affiliates, regulators, law enforcement
- **Cross-border flows**: destination countries, transfer mechanisms

### 3. DPP Compliance Assessment

Assess each processing activity against the six DPPs:

#### DPP1 — Purpose and Manner of Collection
- [ ] Lawful purpose directly related to function/activity?
- [ ] Collection necessary and not excessive?
- [ ] Data subjects informed of purpose, classes of transferees, access rights?
- [ ] Personal Information Collection Statement (PICS) provided?
- [ ] Collection by lawful and fair means?

#### DPP2 — Accuracy and Retention
- [ ] Data reasonably accurate for intended use?
- [ ] Correction procedures in place?
- [ ] Retention period defined and justified?
- [ ] Secure deletion/erasure mechanisms in place?

#### DPP3 — Use of Personal Data
- [ ] Data used only for original purpose or directly related purpose?
- [ ] Consent obtained for new purposes?
- [ ] Data matching activities identified and assessed?
- [ ] Direct marketing consent obtained (s.35A-J)?

#### DPP4 — Security of Personal Data
- [ ] IT security controls adequate? (encryption, access controls, patch management)
- [ ] Physical security adequate? (locked storage, access restrictions)
- [ ] Organisational measures adequate? (policies, training, NDAs)
- [ ] Third-party processor contracts include data protection obligations?
- [ ] Incident response plan in place?

#### DPP5 — Information to be Generally Available
- [ ] Privacy Policy Statement (PPS) published and current?
- [ ] PICS provided at time of collection?
- [ ] Data access/collection policies readily available?

#### DPP6 — Access to Personal Data
- [ ] Data subject access request (DSAR) procedure documented?
- [ ] Response within 40 calendar days achievable?
- [ ] Fee structure defined and reasonable?
- [ ] Refusal grounds documented and compliant?
- [ ] Correction procedure in place?

### 4. Risk Assessment

Rate each identified gap on likelihood × impact:

| Likelihood | Impact | Risk Level |
|------------|--------|------------|
| Low | Low | Low |
| Medium | Low/Medium | Medium |
| High | Any | High |
| Any | High | High |

**High-risk factors**:
- Processing of sensitive personal data (health, biometric, financial)
- Large-scale processing
- Cross-border transfers to countries without equivalent protections
- Direct marketing using personal data
- CCTV/employee monitoring systems
- Children's data processing
- Automated decision-making

### 5. Remediation Planning

For each identified risk, propose:

- **Immediate action**: quick fix for critical gaps
- **Short-term**: within 3 months (policy updates, contractual amendments)
- **Medium-term**: 3–12 months (system changes, training programmes)
- **Long-term**: 12+ months (infrastructure overhaul, DPIA programme)

**Common remediation actions**:
- Draft or update PPS and PICS documents
- Implement DSAR handling procedures
- Update direct marketing consent records
- Revise data retention schedules
- Amend data processor agreements
- Implement staff training on PDPO compliance
- Deploy technical security measures (encryption, access logging)
- Establish data breach response plan

### 6. Report

Prepare a PIA report including:

- Executive summary
- Scope and methodology
- Data flow maps (visual diagrams recommended)
- DPP compliance findings
- Risk register (categorised by severity)
- Remediation action plan with timeline
- Residual risk statement
- Recommendations on whether to proceed with processing

## Key Provisions (Cap 486)

| Section | Subject | Relevance to PIA |
|---------|---------|------------------|
| Schedule 1 | DPP1-6 | Core compliance framework |
| s.35A-J | Direct marketing | Consent, opt-out, record keeping |
| s.64 | Doxxing | Disclosure offences, criminal liability |
| Part 6 | Enforcement | Investigation, enforcement notices |
| s.66 | Compensation | Data subject compensation claims |

## Tools & Resources

- PCPD (https://www.pcpd.org.hk) — compliance guidance, investigation reports
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 486 provisions
- PCPD Privacy Management Programme guidance
- PCPD Data Breach Handling guidance
- ISO/IEC 27001 / SOC 2 frameworks (cross-reference)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

---
name: dpa-hk
description: Review and advise on Data Processing Agreements (DPA) under the Personal Data (Privacy) Ordinance (Cap 486), covering data processor obligations, security measures, sub-processing, breach notification, audit rights, and cross-border transfer clauses.
---

# DPA Review (HK) — Skill

## Purpose

Review and advise on Data Processing Agreements (DPA) under the Personal Data (Privacy) Ordinance (Cap 486), ensuring that contracts with data processors adequately address PDPO compliance, security measures, sub-processing restrictions, breach notification, audit rights, and cross-border data transfer protections.

## Scope

- DPA structure and essential clauses
- Definitions and scope (personal data, processing, data user/processor)
- Data processing instructions
- Confidentiality obligations
- Security measures (DPP4 compliance)
- Sub-processing and onward transfers
- Data breach notification
- Data subject rights assistance
- Audit and inspection rights
- Deletion and return of data
- Cross-border transfer provisions
- Liability and indemnification
- Governing law and jurisdiction

## Workflow

### 1. Assess the Engagement

- **Role of the parties**: is the third party a **data processor** (acting on instructions) or a **joint data user** (making independent decisions)?
- **Volume and sensitivity**: what personal data is being processed?
- **Jurisdiction**: where will data be processed? Any cross-border element?
- **Sub-processing chain**: will the processor use sub-processors?
- **Duration of processing**: ongoing or one-time?
- **Legacy arrangement**: existing contract or new agreement?

### 2. Review Essential Clauses

#### Definition and Scope
- "Personal Data" definition should align with PDPO (s.2 — personal data relating to an identifiable individual)
- "Processing" should be broad enough to cover all activities
- "Data Processor" should be defined as distinct from "Data User"
- Scope: specify categories of personal data, data subjects, processing purposes

#### Data Processing Instructions
- Processor must process data only on documented instructions from the data user
- Prohibition on processing for any independent purpose (critical for DPP3 compliance)
- Right for data user to change instructions (subject to reasonable notice)

#### Confidentiality
- Confidentiality obligations on all personnel processing personal data
- Training requirement: ensure all staff with data access are trained on PDPO and confidentiality
- Post-termination confidentiality (survival clause)
- Secure destruction of data on personnel departure

#### Security Measures (DPP4)
- Minimum security standard required (technical + organisational)
- **Technical**: encryption (at rest and in transit), access controls, firewalls, intrusion detection, logging, patch management
- **Organisational**: policies, training, background checks, NDAs, access reviews
- Regular security testing (penetration testing, vulnerability scanning)
- Compliance with recognised standards (ISO 27001, SOC 2, PCI DSS) — preferable to custom security schedule

#### Sub-processing
- Prohibition on sub-processing without prior written consent
- General consent (processor may engage sub-processors subject to notification and right to object)
- Specific consent (each sub-processor requires individual approval)
- Sub-processor must agree to equivalent contractual obligations
- Chain liability: processor remains liable for sub-processor actions
- List of approved sub-processors (and change procedure)

#### Data Breach Notification
- Obligation to notify data user **without undue delay** (recommend: 24–48 hours)
- Notification content: nature of breach, data categories, volume, cause, containment, timeline
- Cooperation with investigation and remediation
- Indemnity for costs of notification (to data subjects, regulators)
- Requirement to preserve evidence for forensic investigation

#### Data Subject Rights
- Processor to assist data user in responding to DSARs (s.18-22)
- Timeline: 40 calendar days (activate immediately on notification)
- Right of data user to access data held by processor
- Obligation to implement rectification and erasure (as instructed)

#### Audit and Inspection
- Right of data user to audit processor's data processing facilities (upon reasonable notice)
- Annual compliance report (SOC 2 Type II, ISO 27001 surveillance report)
- Right to conduct on-site inspections (or witness third-party audit)
- Audit costs: typically borne by requesting party

#### Deletion and Return of Data
- Obligation to delete or return all personal data on termination
- Certification of deletion (signed undertaking)
- Retention in accordance with data user's retention schedule
- Option to retain limited data for legal/compliance purposes (with confidentiality obligations)

#### Cross-Border Transfers
- If processor processes data outside Hong Kong:
  - Ensure contractual protections equivalent to PDPO apply
  - Restriction on onward transfers
  - Adequacy assessment (though HK has no formal adequacy framework)
  - Consider data localisation where required by other jurisdictions
- Recommended governing law: Hong Kong law (for PDPO consistency)

#### Liability and Indemnification
- **Data user liability**: liable to data subjects for processor breaches (s.66 — compensation claims)
- **Processor liability**: liable to data user for breach of DPA
- **Indemnity**: processor indemnifies data user for third-party claims (data subject compensation)
- **Cap on liability**: common (typically 1–3× annual service fees), but data protection breaches often excluded from cap
- **Warranties**: processor warrants PDPO compliance, security measures

### 3. PDPO-Specific Considerations

| Issue | GDPR Approach | PDPO Approach | DPA Adjustment |
|-------|---------------|---------------|----------------|
| Mandatory breach notification | 72 hours | Voluntary (pre-legislation) | Contractual 24–48 hour target |
| Data Protection Officer | Required | Not required | Specify DPO or responsible person |
| Data subject compensation | Direct processor liability | Data user liable, processor indemnifies | Indemnity clause critical |
| Sub-processor liability | Joint liability | Contract chain | Chain liability provision |
| Governing law | Any EU/EEA | Hong Kong law preferred | Specify HK law |

### 4. Common Pitfalls

- **Undefined security measures**: "appropriate measures" without specifics — push for detailed schedule
- **No right to audit**: processor refuses audit clause — negotiate for SOC 2 report or third-party certification
- **Sub-processing without restriction**: processor can hire sub-processors without notice — require consent
- **No PDPO compliance warranty**: processor claims not subject to PDPO — contractually impose equivalent standards
- **Limited breach notification**: "as soon as reasonably practicable" — specify 24–48 hours
- **Data user bears all liability**: processor seeks to exclude all liability — insist on minimum indemnity
- **Deletion unenforceable**: no certification of deletion — require signed affirmation
- **Data not returned**: no return obligation on termination — specifically address

### 5. Negotiation Points

| Issue | Data User Position | Processor Position | Compromise |
|-------|-------------------|-------------------|------------|
| Security schedule | Detailed schedule | High level | Annex with minimum standards |
| Audit | On-site, any time, at processor cost | No audit | Annual SOC 2 report + on-site every 2 years |
| Breach notification | 24 hours | 72 hours | 48 hours |
| Liability cap | No cap | 1× annual fees | 3× annual fees; exclude data breach from cap |
| Indemnity | Full indemnity | No indemnity | Indemnity for breaches caused by processor |
| Termination | Immediate for breach | Cure period | 30-day cure, immediate for material breach |

## Key Provisions (Cap 486)

| Section | Subject | Relevance to DPA |
|---------|---------|------------------|
| DPP4 | Security | Foundation for processor security obligations |
| DPP3 | Use limitation | Restricts processor's independent data use |
| s.18-22 | Access and correction | Processor assist obligations |
| s.66 | Compensation | Data user back-end liability |
| DPP2 | Retention | Deletion/return obligations |

## Tools & Resources

- PCPD (https://www.pcpd.org.hk) — outsourcing guidance, data processor compliance
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 486 provisions
- PCPD Guidance on Outsourcing the Processing of Personal Data to Data Processors
- DPA template (PDPO-compliant)
- Sub-processor due diligence checklist
- Data security schedule template


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

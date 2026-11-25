---
name: dsar-hk
description: Handle Data Subject Access Requests under the Personal Data (Privacy) Ordinance (Cap 486), covering the 40-day response timeline, fee limitations, refusal grounds, and correction requests.
---

# DSAR (HK) — Skill

## Purpose

Advise on and manage Data Subject Access Requests (DSAR) under the Personal Data (Privacy) Ordinance (Cap 486), ensuring compliance with DPP6 (access right) and s.18-22 (data access and correction provisions) within the statutory 40-day response timeline.

## Scope

- DSAR receipt and acknowledgment
- Identity verification
- Search and retrieval of personal data
- Third-party data and confidentiality considerations
- Refusal grounds (s.20, 20A)
- Fee assessment
- Response preparation and delivery
- Correction requests (s.22)
- Exemption claims (s.57-71)
- Escalation and PCPD complaints

## Workflow

### 1. Receive and Acknowledge DSAR

- Confirm request in writing (email acceptable)
- Acknowledge receipt within 3 working days
- Identify the data subject and their relationship to your organisation
- Confirm scope of request: specific data categories, time period, format
- Request additional context if scope is unclear (avoid being overbroad or excessively narrow)

### 2. Verify Identity

- Verify the requester's identity (HKID, passport, driver's licence)
- If request is from an agent/representative: verify authority (written authorisation, power of attorney)
- For electronic requests: additional verification may be necessary
- If identity cannot be verified, notify requester within 40 days of the deficiency

### 3. Assess Scope and Exemptions

#### Exemptions (s.57-71 PDPO)
- **Security and defence** (s.57) — rarely applicable in HK commercial context
- **Crime prevention and detection** (s.58) — law enforcement purposes
- **Legal proceedings** (s.59) — legal professional privilege
- **Health data** (s.60) — may be withheld if disclosure would cause serious harm
- **Social work** (s.60A)
- **Education** (s.61)
- **Research and statistics** (s.62)
- **Serious harm** (s.63) — physical or mental harm to data subject or another person
- **Rating and valuation** (s.64) — certain financial data

#### Third-Party Data
If the requested data contains information about third parties:
- Seek consent from the third party
- If consent refused, consider redacting third-party data
- Assess whether disclosure without consent is reasonable in the circumstances
- Document reasoning for disclosure or redaction decisions

### 4. Search and Retrieve

- Conduct a reasonable search across all data systems (email, CRM, HR, cloud storage)
- Include structured and unstructured data (as reasonably practicable)
- Capture both electronic and physical records
- Consider archived/backup data (retrieve unless disproportionate)
- Log search methodology and sources searched
- Document any data not captured (with reasons)

### 5. Prepare Response

- Collate all personal data of the requester
- Exclude exempted data (with explanation)
- Redact third-party data (where appropriate)
- Provide in a readily legible form (electronic or hard copy)
- Include supplementary information: purposes of processing, classes of transferees (s.18(1)(b))
- Prepare a covering letter explaining what is provided, what is withheld, and why

#### Response Time
- **40 calendar days** from receipt of valid request
- Extendable to **50 calendar days** if data retrieval is complex or voluminous (notify requester in writing within 40 days with time estimate)
- Failure to respond within 40 days is a breach (data subject can complain to PCPD)

### 6. Fee Assessment

- Data user may charge a **reasonable fee** for complying with the request
- Fee should not be so high as to deter the exercise of access rights
- PCPD guidance: initial fee should not exceed direct costs of photocopying and postage
- No fee for correction requests
- If fee is demanded, the 40-day clock may be paused until fee is paid (but notify the requester)

### 7. Deliver Response

- Provide personal data copy in requested format where reasonably practicable
- Include explanation of any abbreviations, codes, or technical terms
- For digital delivery: use secure transmission (encrypted email, secure portal)
- Maintain clear records: date of response, what was provided, any exemptions relied upon
- Log the DSAR for compliance and audit purposes

### 8. Correction Requests (s.22)

- Data subject may request correction of inaccurate personal data
- 40-day response timeline (same as access request)
- Grounds for refusal (s.23): limited to specific statutory exemptions
- If correction made: notify third parties to whom data was disclosed (s.23(2))
- If correction refused: inform data subject of reasons and right to complain to PCPD

### 9. Escalation and PCPD

If data subject is dissatisfied with response:
- Data subject may complain to PCPD (s.37)
- PCPD may investigate (s.38)
- PCPD may issue enforcement notice (s.50)
- Data subject may seek compensation (s.66)

## Common Pitfalls

- **Scope creep**: Request too broad — seek clarification
- **40-day clock**: Miss deadline — automatic breach
- **Inadequate search**: Only searched one department/system
- **Template responses**: Every DSAR is different; customise
- **Over-redaction**: Can demonstrate bad faith to PCPD
- **Fee obstruction**: Excessive fees may attract PCPD criticism
- **No audit trail**: Inability to demonstrate compliance
- **Deleting data during process**: Do not destroy data subject to a pending DSAR

## Key Provisions (Cap 486)

| Section | Subject | Key Detail |
|---------|---------|------------|
| s.18 | Access right | Data subject right to access personal data |
| s.19 | Complying with request | Data user obligations |
| s.20 | Refusal grounds | Limited statutory grounds |
| s.22 | Correction right | Request for correction |
| s.23 | Complying with correction | Obligation to correct and notify |
| s.37 | Complaint to PCPD | Data subject complaints |
| s.50 | Enforcement notice | PCPD enforcement powers |
| s.66 | Compensation | Damages for breach |
| DPP6 | Access principle | Policy and procedure |

## Tools & Resources

- PCPD (https://www.pcpd.org.hk) — enforcement decisions on DSAR refusals, guidance
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 486 access provisions
- PCPD Guidance on DSAR Handling
- DSAR log template (recommended for internal records)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

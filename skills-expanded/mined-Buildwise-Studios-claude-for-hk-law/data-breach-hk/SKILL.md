---
name: data-breach-hk
description: Develop and execute a data breach response plan specific to Hong Kong under the Personal Data (Privacy) Ordinance (Cap 486), covering containment, assessment, notification (voluntary framework), remediation, and PCPD engagement.
---

# Data Breach (HK) — Skill

## Purpose

Develop and execute a data breach response framework specific to Hong Kong under the Personal Data (Privacy) Ordinance (Cap 486). While mandatory data breach notification is not yet enacted (legislative reform under consultation), this skill provides guidance on voluntary PCPD notification best practice, incident containment, assessment, and remediation.

## Scope

- Breach identification and containment
- Initial assessment and classification
- PCPD notification (voluntary framework)
- Affected data subject notification
- Remediation and corrective actions
- Regulatory engagement and investigation preparation
- Post-incident review and policy updates
- Communication strategy (internal and external)

## Workflow

### 1. Immediate Containment (First 24 Hours)

- **Identify the breach**: confirm that personal data has been or may have been accessed, lost, or compromised
- **Secure the system**: isolate affected systems, preserve evidence (logs, access records, network traffic)
- **Disable compromised accounts**: reset passwords, revoke access tokens, disable user accounts
- **Engage the response team**: designate a breach response lead, legal counsel, IT security, communications team
- **Engage external support**: forensic IT investigators, external legal counsel, public relations

### 2. Initial Assessment (24–72 Hours)

#### Classification
- **Type of breach**: 
  - Unauthorised access (hacking, insider threat)
  - Loss/theft (device, document, media)
  - Accidental disclosure (email, portal, postal)
  - System failure (misconfiguration, ransomware)

- **Data involved**: 
  - Personal identifiers (name, HKID, passport, date of birth)
  - Financial (credit card, bank account, income)
  - Health (medical records, insurance)
  - Sensitive (biometrics, genetic, criminal records)
  - High volume (10,000+ records)

- **Affected data subjects**: customers, employees, clients, vendors, third parties

#### Risk Assessment
Assess risk of harm on three dimensions:

| Factor | Low Risk | Medium Risk | High Risk |
|--------|----------|-------------|-----------|
| Data sensitivity | Name + email | Name + HKID | Financial + health |
| Volume | < 100 | 100–10,000 | 10,000+ |
| Accessibility | Encrypted + no key | Encrypted + key | Unencrypted |
| Harm potential | Embarrassment | Identity theft | Financial fraud, physical harm |

#### Determine Response Level
- **Low risk**: no notification required; internal remediation only
- **Medium risk**: consider PCPD notification; notify individual data subjects
- **High risk**: notify PCPD, notify affected data subjects, prepare for investigation

### 3. PCPD Notification (Voluntary — Recommended)

**When to notify PCPD** (recommended by PCPD Guidance):
- Sensitive personal data involved
- Large volume of data subjects affected
- High risk of identity theft or financial harm
- Systemic failure or policy gap identified
- Public interest or likely media attention

**What to include in PCPD notification**:
- Nature of the breach (data categories, volume, affected systems)
- When and how the breach was discovered
- Immediate containment steps taken
- Risk assessment (harm to data subjects)
- Remediation plan and timeline
- Contact details for breach response lead
- Whether affected data subjects have been notified (or plan to notify)

**Method**: Submit in writing to PCPD. No specific form — a formal letter or email suffices.

### 4. Data Subject Notification

**When to notify affected data subjects**:
- Risk of identity theft or fraud
- Sensitive personal data involved
- Data subject needs to take protective action

**What to include in notification**:
- Description of the breach (what happened, what data was involved)
- Steps taken to contain the breach
- What the data subject can do (change passwords, monitor accounts, report suspicious activity)
- Contact details for the data user's breach response team
- Apology and reassurance

**Method**: Email, SMS, postal mail, website notice (depending on urgency and contact information available)

### 5. Remediation

**Technical measures**:
- Patch vulnerabilities
- Reset all affected accounts
- Implement multi-factor authentication
- Enhance logging and monitoring
- Review access controls and permissions
- Encrypt databases and backups

**Organisational measures**:
- Revise data protection policies
- Update data retention schedules
- Review third-party vendor contracts
- Implement mandatory staff data security training
- Appoint or designate Data Protection Officer
- Establish breach response procedures (updated)

**Legal measures**:
- Preserve all evidence (forensic images, logs)
- Coordinate with legal counsel on PCPD engagement
- Consider if law enforcement referral is appropriate (especially for criminal acts)
- Prepare for potential PCPD investigation
- Assess potential compensation claims (s.66)

### 6. Regulatory Engagement

If PCPD decides to investigate:
- Cooperate fully; designate a point of contact
- Provide requested documents within the timeframe
- Engage legal counsel with PCPD investigation experience
- Prepare for potential enforcement notice (s.50)
- Consider representations before enforcement notice is finalised

**PCPD investigation outcomes**:
- No further action (if adequate response demonstrated)
- Informal advice/guidance
- Enforcement notice (s.50) — requiring specific steps
- Public report (PRC — Privacy Commissioner's Report)
- Criminal prosecution (especially doxxing-related breaches, s.64)

### 7. Post-Incident Review

- **Root cause analysis**: what caused the breach?
- **Policy review**: update data protection policies and procedures
- **Training**: implement targeted training based on breach findings
- **Testing**: conduct penetration testing, vulnerability assessments
- **Benchmark**: compare against PCPD guidance and industry standards
- **Document**: maintain a confidential incident report for board review

## Breach Response Checklist (Quick Reference)

- [ ] Contain the breach (isolate systems, preserve evidence)
- [ ] Activate breach response team
- [ ] Engage forensic IT support
- [ ] Engage legal counsel
- [ ] Conduct initial risk assessment
- [ ] Determine notification requirement
- [ ] Notify PCPD (if recommended)
- [ ] Notify affected data subjects
- [ ] Implement remediation plan
- [ ] Cooperate with PCPD investigation (if applicable)
- [ ] Conduct post-incident review
- [ ] Update policies and procedures

## Key Provisions (Cap 486)

| Section | Subject | Relevance |
|---------|---------|-----------|
| DPP4 | Security of personal data | Primary standard — security measures |
| s.50 | Enforcement notice | PCPD can require corrective action |
| s.64 | Doxxing | Criminal offences for certain disclosures |
| s.66 | Compensation | Data subject compensation claims |
| s.38 | Investigation | PCPD investigation powers |
| s.38A | Investigation powers | Enhanced PCPD investigative authority |

## Tools & Resources

- PCPD (https://www.pcpd.org.hk) — breach handling guidance, enforcement decisions, public reports
- Hong Kong e-Legislation (https://www.elegislation.gov.hk) — Cap 486 provisions
- PCPD Guidance on Data Breach Handling (voluntary framework)
- Breach notification letter templates
- Incident response plan template
- Forensic investigation scope of work template


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```

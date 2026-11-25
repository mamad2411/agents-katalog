---
name: incident-response-compliance
description: "When to activate: breach notification, data breach, incident response, GDPR 72 hours, CCPA notification, HIPAA breach, regulator reporting, affected party notification, data incident"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: compliance
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Incident Response — Compliance

## Breach Notification Timelines

| Regulation | Notify regulator | Notify individuals | Threshold |
|-----------|-----------------|-------------------|-----------|
| GDPR | 72 hours of awareness | Without undue delay (if high risk) | Any personal data breach |
| CCPA/CPRA | No regulatory notice required | "In the most expedient time possible" | Unauthorized access to unencrypted PI |
| HIPAA | 60 days of discovery | 60 days of discovery | Unsecured PHI breach ≥ 500 → also notify HHS + media |
| PCI DSS | Immediately notify card brands + acquirer | Per applicable law | Any confirmed cardholder data compromise |
| NY SHIELD / State laws | 30-45 days (varies by state) | "In the most expedient time" | Varies by state |
| SEC (public co.) | 4 business days | N/A | Material cybersecurity incident |

## Severity Classification

| Severity | Definition | Example | Response SLA |
|----------|-----------|---------|-------------|
| P0 — Critical | Confirmed exfiltration of regulated data; active threat in systems | Ransomware with confirmed PHI exfil | Immediate; war room within 1 hour |
| P1 — Major | Suspected breach of personal/regulated data; significant system compromise | Unauthorized DB access, scope unclear | < 4 hours to incident lead; legal notified |
| P2 — Significant | Potential exposure; investigation required | Misconfigured S3 bucket found | < 24 hours; assess breach status |
| P3 — Minor | Policy violation, no confirmed data exposure | Employee emailed PII to wrong address | < 48 hours; assess and document |

## Is It a Reportable Breach? — Decision Tree

```
1. Was personal / regulated data involved?
   No → Not a breach; document as security incident
   Yes ↓

2. Was the data encrypted with keys the unauthorized party lacks?
   Yes → Likely not reportable (GDPR Art. 34; HIPAA safe harbor)
   No ↓

3. Did an unauthorized party access or acquire the data?
   No (accidental disclosure, recovered before access) → Low risk; assess further
   Yes ↓

4. Determine applicable regulations:
   - EU/UK residents → GDPR (72-hour regulator clock starts)
   - California residents → CCPA
   - PHI → HIPAA (assess "low probability of compromise" exception)
   - Cardholders → PCI DSS (notify card brands immediately)

5. Assess risk to individuals:
   High risk (financial harm, discrimination, identity theft likely) → Notify individuals
   Low risk → May not require individual notification (document rationale)
```

## Regulator Notification Templates

### GDPR — Supervisory Authority Notification
Must include (Art. 33):
```
1. Nature of the breach (categories and approximate number of records/subjects affected)
2. Name and contact of Data Protection Officer (or other contact)
3. Likely consequences of the breach
4. Measures taken or proposed to address the breach and mitigate effects
```
If full information not available within 72 hours, provide initial notification with available facts + expected completion date.

### HIPAA — HHS Breach Notification
Submit via HHS OCR breach portal:
- Covered entity name and contact
- Type of PHI involved (name, SSN, diagnosis, financial info)
- Safeguards in place at time of breach
- Number of individuals affected
- Date of breach and date of discovery
- Brief description of what happened
- Actions taken to investigate and prevent recurrence

### PCI DSS — Card Brand Notification
Contact: Visa CISP, Mastercard SDP, Amex CSP
Required immediately:
- Merchant / service provider name and ID
- Name and contact of person reporting
- Description of incident
- Estimated number of accounts at risk
- Date of compromise (if known)
- Systems involved

## Affected Individual Notification Requirements

### GDPR — Individual Notification (Art. 34)
Required when breach is likely to result in **high risk** to individuals. Must include:
- Plain language description of the breach
- DPO name and contact
- Likely consequences of the breach
- Measures taken or proposed to mitigate harm
- Specific advice for individuals to protect themselves

### HIPAA — Individual Notification
- Written notice by first-class mail (email if individual agreed)
- If contact info insufficient: substitute notice (website or media)
- Must include: brief description, types of PHI involved, steps individuals should take, what entity is doing, contact info

### General Notification Best Practices
- Use plain language — no legal jargon
- Specific: tell them what data was affected, not vague "some information"
- Actionable: credit monitoring offer, password reset guidance, fraud alert advice
- Contact: dedicated hotline/email for questions
- Timing: as soon as investigation allows, not delayed for PR reasons

## Internal Escalation Procedure

```
Hour 0: Detection
  → Verify the incident (not a false positive)
  → Assign Incident Lead

Hour 1: Initial Response
  → Activate incident response team
  → Begin containment (isolate systems if needed)
  → Notify: CISO, Legal, DPO (if applicable)
  → Preserve evidence (do NOT wipe systems)
  → Open war room (Slack channel / bridge line)

Hour 4: Assessment
  → Determine data involved (regulated? how much?)
  → Assess breach notification obligations
  → Legal confirms notification timelines triggered
  → Decide: notify regulators? (start clock if GDPR)

Hour 24: Investigation
  → Forensic scope established
  → External forensics engaged if needed
  → Draft holding statement for communications

Hour 72: Regulator Notification (GDPR)
  → File initial notification if GDPR-applicable
  → Document all evidence of timeline

Ongoing: Remediation + Individual Notification
  → Implement fixes
  → Notify affected individuals per regulation
  → Continue investigation to full root cause
```

## Forensic Evidence Preservation

### Do Not
- Wipe or reimage affected systems before forensic image taken
- Delete logs or modify system state
- Power off without forensic imaging (may lose volatile memory)

### Do
- Isolate affected systems from network (contain without destroying evidence)
- Take memory dump if active threat present
- Preserve disk images before remediation
- Export and preserve relevant logs (SIEM, firewall, endpoint)
- Document chain of custody for all evidence

### Log Types to Preserve
- Authentication logs (successful and failed logins)
- Network flow / firewall logs
- Endpoint detection logs (EDR telemetry)
- Application access logs
- Database audit logs
- Email gateway logs (for phishing-origin incidents)

## Breach Documentation Requirements

Maintain a **Breach Register** with:
| Field | Content |
|-------|---------|
| Incident ID | Unique reference |
| Date discovered | |
| Date of breach (if known) | |
| Description | Nature of breach |
| Data categories affected | |
| Number of records | |
| Number of individuals | |
| Root cause | |
| Notification decision | Reportable / Not reportable + rationale |
| Regulator notified | Yes/No; date; authority |
| Individuals notified | Yes/No; date; method |
| Containment measures | |
| Remediation measures | |
| Lessons learned | |

## Post-Incident Review

Conduct within 2 weeks of containment:
1. **Timeline reconstruction** — complete sequence of events
2. **Root cause analysis** — what control failed or was absent?
3. **Detection gap analysis** — why wasn't it caught sooner?
4. **Response effectiveness** — what worked / what didn't?
5. **Regulatory compliance review** — were timelines met?
6. **Remediation plan** — specific control improvements with owners and dates
7. **Tabletop update** — update incident response playbook with lessons learned

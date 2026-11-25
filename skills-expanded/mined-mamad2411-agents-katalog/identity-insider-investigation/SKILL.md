---
name: identity-insider-investigation
description: "Identity Insider Investigation."
domain: cybersecurity
---

|
| **Insider Threat** | Risk posed by individuals with authorized access who intentionally or unintentionally cause harm to the organization |
| **User Behavior Analytics (UBA)** | Technology that analyzes user activity patterns to detect anomalies indicating potential insider threats |
| **Data Loss Prevention (DLP)** | Technology that monitors, detects, and blocks unauthorized transfer of sensitive data outside the organization |
| **Legal Hold** | Directive to preserve all relevant evidence and suspend normal document destruction policies during an investigation |
| **Need to Know** | Information access principle restricting insider threat investigation details to only authorized team members |
| **Exfiltration Vector** | Method used to move data outside the organization: USB, email, cloud storage, print, screen capture, photography |

## Tools & Systems

- **Microsoft Purview (formerly Compliance Center)**: Insider risk management, DLP, eDiscovery, and content search
- **Exabeam / Securonix**: User and entity behavior analytics (UEBA) platforms for anomaly detection
- **Digital Guardian**: DLP and insider threat detection platform with endpoint agent
- **Magnet AXIOM**: Digital forensics platform supporting endpoint, cloud, and mobile evidence analysis
- **Relativity**: eDiscovery platform for legal review of collected evidence in insider threat cases

## Common Scenarios

### Scenario: Departing Engineer Exfiltrating Source Code

**Context**: A senior software engineer with access to critical repositories submits a two-week resignation notice. The engineering manager reports that the engineer has been working unusual hours and downloading large amounts of code.

**Approach**:
1. Obtain legal authorization to investigate before taking any action
2. Pull Git access logs showing repository clones and downloads for the past 60 days
3. Review DLP logs for USB device connections and large file transfers
4. Check email gateway for messages with code attachments sent to personal accounts
5. Analyze browser history for personal cloud storage uploads
6. Image the workstation forensically before the employee's last day
7. Present findings to legal and HR for determination of next steps

**Pitfalls**:
- Investigating without legal counsel authorization (may violate employee privacy rights)
- Alerting the subject to the investigation before evidence is preserved
- Not preserving the workstation before the employee's departure date
- Assuming all after-hours access is malicious without comparing to the employee's historical baseline
- Failing to check personal mobile devices that may have accessed corporate cloud services

## Output Format

```
INSIDER THREAT INVESTIGATION REPORT
=====================================
Case ID:          INV-2025-042
Classification:   CONFIDENTIAL - Need to Know Only
Subject:          [Name Redacted] - Senior Engineer
Investigation Period: 2025-10-01 to 2025-10-28
Investigator:     [Name]
Legal Counsel:    [Name]
HR Liaison:       [Name]

ALLEGATION
Unauthorized exfiltration of proprietary source code and customer
data following resignation submission.

EVIDENCE SUMMARY
1. Git logs: 47 repositories cloned (vs. baseline of 3)
2. USB transfers: 4.6 GB across 3 unique devices over 12 sessions
3. Email: 200+ emails with attachments forwarded to personal Gmail
4. Cloud: Google Drive sync client installed, syncing corporate files
5. Print: 847 pages including customer contact database
6. Physical access: After-hours badge access on 8 of 12 workdays

BEHAVIORAL ANALYSIS
[Baseline vs. anomalous activity comparison]

IMPACT ASSESSMENT
Data Classification:  Confidential (source code, customer PII)
Estimated Volume:     7.2 GB exfiltrated
Regulatory Impact:    Potential GDPR notification (customer PII)
Business Impact:      Competitive advantage at risk

TIMELINE
[Chronological event listing]

RECOMMENDATIONS
1. [Legal/HR decision on employment action]
2. [Evidence preservation actions]
3. [Regulatory notification assessment]
4. [Access control improvements]
```

---
name: cloud-ir-compromised
description: "Cloud Ir Compromised."
domain: cybersecurity
---

|
| Impossible Travel | Detection of the same credential being used from geographically distant locations within a time period that makes physical travel impossible |
| Credential Stuffing | Attack using stolen username/password combinations from data breaches to attempt login across multiple cloud services |
| Instance Credential Exfiltration | GuardDuty finding indicating EC2 instance role credentials are being used from outside the expected AWS network |
| Anomalous Behavior | Machine learning-based detection of API call patterns that deviate significantly from the established baseline for a principal |
| Session Revocation | Invalidating all active authentication sessions for a compromised principal to force re-authentication with new credentials |
| Persistence Indicator | Attacker actions designed to maintain access after initial compromise, such as creating new access keys or service account keys |

## Tools & Systems

- **AWS GuardDuty**: ML-based threat detection with specific finding types for credential compromise and unauthorized access
- **Microsoft Entra ID Protection**: Identity risk detection for sign-in anomalies, compromised credentials, and risky user behavior
- **GCP Event Threat Detection**: SCC component detecting anomalous API usage and credential abuse in GCP environments
- **CloudTrail / Activity Log / Audit Log**: API audit logs providing the raw data for credential compromise investigation
- **SIEM (Splunk, Elastic, Sentinel)**: Centralized platform for cross-cloud correlation of credential abuse indicators

## Common Scenarios

### Scenario: Detecting an Access Key Compromised via Phishing

**Context**: A developer receives a phishing email that harvests their AWS console credentials. The attacker logs in from a foreign IP, creates a new access key, and begins enumerating the account.

**Approach**:
1. GuardDuty triggers `UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B` for login from unusual country
2. SOC reviews the finding and correlates with phishing reports from the email security team
3. Query CloudTrail for all actions by the compromised user from the attacker's IP
4. Discover the attacker created new access keys and ran IAM enumeration commands
5. Immediately deactivate all access keys for the user and revoke active sessions
6. Force password reset and re-enroll MFA
7. Check for persistence: new IAM users, roles, Lambda functions, or EC2 instances created
8. Remove any persistence artifacts and document the incident timeline

**Pitfalls**: Simply changing the password does not invalidate existing access keys or active sessions. All access keys must be rotated and temporary credentials revoked by adding a deny-all policy for tokens issued before the compromise was detected. Attackers may create new IAM users or roles for persistence before the initial credential is revoked.

## Output Format

```
Cloud Credential Compromise Detection Report
===============================================
Detection Date: 2026-02-23
Scope: Multi-cloud (AWS, Azure, GCP)
Period: 2026-02-16 to 2026-02-23

ACTIVE COMPROMISE INDICATORS:
[CRED-001] AWS Console Login from Unusual Location
  User: developer@company.com
  Source IP: 185.x.x.x (Russia)
  Normal Location: US-East
  GuardDuty Finding: UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B
  Severity: HIGH
  Status: Credential deactivated

[CRED-002] Azure Impossible Travel Detection
  User: admin@company.onmicrosoft.com
  Location 1: New York, US (09:00 UTC)
  Location 2: Beijing, CN (09:15 UTC)
  Risk Level: HIGH
  Status: Sessions revoked, under investigation

DETECTION METRICS (Last 7 Days):
  Impossible travel detections:        5
  Anomalous API activity alerts:      12
  Failed login attempts > threshold:   3
  New credentials from unusual IPs:    2
  Total compromises confirmed:         2

CONTAINMENT ACTIONS TAKEN:
  AWS access keys deactivated:    3
  Azure sessions revoked:         2
  GCP service accounts disabled:  1
  Passwords force-reset:          4
  MFA re-enrolled:                4
```

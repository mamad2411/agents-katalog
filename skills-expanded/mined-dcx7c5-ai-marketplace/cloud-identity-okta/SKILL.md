---
name: cloud-identity-okta
description: "Cloud Identity Okta."
domain: cybersecurity
---

|
| Okta FastPass | Phishing-resistant passwordless MFA that cryptographically binds authentication to the device and origin, preventing real-time phishing attacks |
| SCIM Provisioning | System for Cross-domain Identity Management protocol that automates user creation, update, and deletion across cloud applications |
| Universal Directory | Okta's cloud-based identity store that aggregates user profiles from multiple sources including AD, LDAP, and HR systems |
| Adaptive MFA | Context-aware authentication that adjusts MFA requirements based on risk signals such as device trust, location, and behavior |
| Workforce Identity | Okta product tier focused on employee and contractor identity management including SSO, MFA, and lifecycle management |
| ThreatInsight | Okta's threat detection service that identifies and blocks credential stuffing, password spraying, and bot-driven authentication attacks |
| Device Trust | Integration with MDM platforms to verify device compliance (encryption, OS version, management status) before granting access |

## Tools & Systems

- **Okta Identity Engine**: Core identity platform providing SSO, MFA, lifecycle management, and adaptive access policies
- **Okta Workflows**: No-code automation platform for building identity-driven workflows across cloud services
- **Okta Advanced Server Access**: SSH and RDP access management for cloud servers using short-lived certificates
- **AWS IAM Identity Center**: AWS-native SSO service that integrates with Okta as an external identity provider
- **Azure AD External Identities**: Azure service for federating with Okta for B2B and workforce scenarios

## Common Scenarios

### Scenario: Automating Offboarding Across Multi-Cloud Environment

**Context**: An employee with AWS admin, Azure contributor, and GCP editor access leaves the company. The organization needs to revoke all access within 15 minutes of HR processing the termination.

**Approach**:
1. HR deactivates the employee in Workday, triggering a SCIM event to Okta
2. Okta immediately deactivates the user in Universal Directory, terminating all active SSO sessions
3. SCIM deprovisioning removes the user from AWS IAM Identity Center, Azure AD, and GCP Workforce Identity
4. Okta Workflow triggers additional cleanup: revoke OAuth tokens, remove from Slack, disable VPN certificate
5. An audit log entry is created with timestamps for each deprovisioning action as compliance evidence
6. SOC receives notification to verify no residual access exists through direct IAM users or service accounts

**Pitfalls**: Not deprovisioning direct IAM users or service accounts created outside of Okta federation leaves backdoor access. SCIM propagation delays in some services can leave access active for minutes after Okta deactivation.

## Output Format

```
Cloud Identity Security Report
================================
Identity Provider: Okta (company.okta.com)
Report Date: 2025-02-23

USER STATISTICS:
  Total Users: 2,450
  Active: 2,312 | Suspended: 45 | Deactivated: 93
  MFA Enrolled: 2,298/2,312 (99.4%)
  Phishing-Resistant MFA: 812/2,312 (35.1%)

CLOUD SSO COVERAGE:
  AWS Console (45 accounts):     100% via SAML federation
  Azure Portal (8 subscriptions): 100% via OIDC federation
  GCP Console (3 projects):       100% via Workforce Identity

AUTHENTICATION EVENTS (Last 30 Days):
  Total Logins: 145,234
  MFA Challenges: 89,456
  Failed Logins: 3,456
  Account Lockouts: 23
  ThreatInsight Blocks: 12,345 (credential stuffing attempts)

LIFECYCLE EVENTS:
  Users Provisioned: 45
  Users Deprovisioned: 23
  Average Deprovisioning Time: 8 minutes
  Orphan Accounts Detected: 3 (direct IAM users not managed by Okta)

RECOMMENDATIONS:
  [HIGH] Increase phishing-resistant MFA adoption from 35% to 80%
  [HIGH] Remediate 3 orphan cloud accounts not managed by Okta
  [MEDIUM] Reduce session duration for admin roles from 8h to 4h
```

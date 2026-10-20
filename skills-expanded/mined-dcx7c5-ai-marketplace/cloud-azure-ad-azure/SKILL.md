---
name: cloud-azure-ad-azure
description: "Cloud Azure Ad Azure."
domain: cybersecurity
---

|
| Microsoft Entra ID | Microsoft's cloud identity and access management service, formerly Azure Active Directory, providing authentication and authorization |
| Conditional Access | Policy engine that evaluates signals (user, device, location, risk) to enforce access controls like MFA, device compliance, or block access |
| Security Defaults | Microsoft's baseline identity protection settings that enforce MFA registration, block legacy auth, and protect privileged actions |
| Privileged Identity Management | Azure AD Premium P2 feature enabling just-in-time privileged access with approval workflows and time-bound role activation |
| Legacy Authentication | Older authentication protocols (POP3, IMAP, SMTP, ActiveSync) that do not support MFA and are commonly exploited for credential attacks |
| Risky Sign-In | Microsoft Entra Identity Protection detection of sign-in anomalies including impossible travel, unfamiliar locations, and malware-linked IPs |

## Tools & Systems

- **Microsoft Graph API**: Primary programmatic interface for querying Entra ID configuration, policies, roles, and audit logs
- **Microsoft Graph PowerShell SDK**: PowerShell module for Entra ID management and security auditing tasks
- **ScoutSuite**: Multi-cloud auditing tool with Azure provider support for IAM, storage, networking, and identity checks
- **AzureADRecon**: Community tool for comprehensive Azure AD reconnaissance and security assessment reporting
- **Microsoft Defender for Identity**: Cloud-based security solution for detecting identity-based threats and compromised credentials

## Common Scenarios

### Scenario: Post-Acquisition Azure Tenant Security Assessment

**Context**: After acquiring a company, the security team needs to assess the Azure tenant identity posture before integrating it with the corporate Entra ID.

**Approach**:
1. Enumerate all Global Administrators and check for personal accounts in admin roles
2. Review conditional access policies to verify MFA is enforced for all users, not just admins
3. Identify guest users with privileged access that may indicate third-party vendor over-permissioning
4. Check for stale accounts (no sign-in for 90+ days) that could be targets for credential attacks
5. Review sign-in logs for legacy authentication usage that bypasses MFA
6. Verify Security Defaults or equivalent CA policies block legacy auth protocols
7. Produce a risk report with prioritized remediation steps before tenant integration

**Pitfalls**: Azure AD Premium P2 is required for risky sign-in detections and PIM. If the acquired tenant uses a lower license tier, many identity protection features will be unavailable. Guest users from partner tenants may have implicit access through dynamic groups that are not visible in standard role assignment queries.

## Output Format

```
Azure Active Directory Security Audit Report
===============================================
Tenant: acme-acquired.onmicrosoft.com
Tenant ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Audit Date: 2026-02-23
License: Azure AD Premium P2

IDENTITY CONFIGURATION:
  Security Defaults: Disabled (Conditional Access in use)
  Conditional Access Policies: 12 (8 enforced, 3 report-only, 1 disabled)
  Legacy Auth Blocked: Partial (blocked for admins only)

PRIVILEGED ACCESS:
  Global Administrators:              8 (recommended: <= 4)
  Permanent admin assignments:        6 (no PIM activation required)
  Service principals with admin:      3
  Guest users with privileged roles:  2

ACCOUNT HYGIENE:
  Total users:                        1,247
  Stale accounts (90+ days):          89
  Guest users:                        234
  Users without MFA registered:       156

SIGN-IN RISK:
  Risky sign-ins (last 30 days):      34
  Legacy auth sign-ins (last 7 days): 67
  Impossible travel detections:        5
  Unfamiliar location sign-ins:       12

CRITICAL FINDINGS:
  1. 8 Global Administrators with permanent assignments (use PIM)
  2. Legacy authentication not blocked for non-admin users
  3. 156 users without MFA registration
  4. 2 guest users with Privileged Role Administrator role
```

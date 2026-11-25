---
name: identity-provider-google
description: "Identity Provider Google."
domain: cybersecurity
---

|
| **Advanced Protection Program (APP)** | Google's strongest account security requiring FIDO2 security keys, blocking third-party app access, and enhanced identity verification for account recovery |
| **Context-Aware Access** | Security policy framework that evaluates device posture, location, and user identity before granting access to Google Workspace applications |
| **DMARC** | Domain-based Message Authentication, Reporting and Conformance protocol that prevents email domain spoofing by validating SPF and DKIM alignment |
| **DLP Rule** | Data Loss Prevention policy that scans content in Gmail, Drive, and Chat for sensitive data patterns and triggers block, quarantine, or warn actions |
| **OAuth App Allowlisting** | Admin control restricting which third-party applications can access organizational data through Google OAuth API scopes |
| **2-Step Verification (2SV)** | Google's multi-factor authentication implementation supporting security keys, phone prompts, TOTP, and backup codes as second factors |

## Tools & Systems

- **Google Admin Console**: Web-based administration portal for managing all Google Workspace security settings, users, and organizational units
- **GAM (Google Apps Manager)**: Open-source command-line tool for bulk Google Workspace administration and automation
- **Google Workspace Alert Center**: Centralized dashboard for security alerts including suspicious login activity, DLP violations, and device compromise
- **Google BeyondCorp Enterprise**: Zero-trust access solution integrated with Google Workspace for context-aware access policies

## Common Scenarios

### Scenario: Securing a Newly Acquired Google Workspace Tenant

**Context**: Post-acquisition security audit reveals the acquired company's Google Workspace has no MFA enforcement, open external sharing, no DLP policies, and multiple unauthorized OAuth applications accessing user data.

**Approach**:
1. Immediately enforce 2SV for all super admin accounts using FIDO2 security keys
2. Reduce super admin count to 3 (primary, secondary, break-glass)
3. Deploy SPF, DKIM, and DMARC starting with monitoring mode (p=none)
4. Enable all anti-phishing and anti-spoofing settings in Email Safety
5. Audit and revoke all unauthorized OAuth application tokens
6. Set third-party app access to blocked with allowlist of approved applications
7. Restrict external Drive sharing to approved partner domains only
8. Deploy DLP rules for PII, financial data, and confidential documents
9. Enable context-aware access requiring managed devices for sensitive applications
10. Configure security alerts and SIEM integration for ongoing monitoring

**Pitfalls**:
- Enforcing MFA without enrollment grace period locks users out of accounts
- Setting DMARC to reject before monitoring period causes legitimate email delivery failures
- Blocking all OAuth apps without identifying business-critical integrations disrupts workflows
- Not auditing existing external shares before restricting sharing leaves data exposed

## Output Format

```
GOOGLE WORKSPACE SECURITY ASSESSMENT REPORT
=============================================
Tenant:            corp.com
License:           Enterprise Plus
Total Users:       3,847
Organizational Units: 12

AUTHENTICATION SECURITY
2SV Enforced:           YES (all OUs)
2SV Enrollment:         3,712 / 3,847 (96.5%)
Security Keys Only:     Executive OU (47 users)
Advanced Protection:    3 super admin accounts
Super Admin Count:      3 (within recommended limit)

EMAIL AUTHENTICATION
SPF:                    CONFIGURED (hard fail: -all)
DKIM:                   CONFIGURED (2048-bit, selector: google)
DMARC:                  ENFORCED (p=reject, 100%)
Anti-Phishing:          ALL PROTECTIONS ENABLED
Anti-Spoofing:          ENABLED (domain + employee name)

DATA PROTECTION
DLP Rules Active:       7
  PII Detection:        SSN, Credit Card, Passport
  Content Labels:       Confidential, Restricted
  Custom Patterns:      3 organization-specific rules
DLP Violations (30d):   89 (67 blocked, 22 warned)

APPLICATION CONTROL
Third-Party App Policy: BLOCKED (allowlist mode)
Approved Apps:          12
Unauthorized Tokens:    0 (all revoked)
API Scope Restrictions: ENABLED

SHARING CONTROLS
External Sharing:       RESTRICTED (allowlisted domains only)
Public Link Sharing:    DISABLED
External Group Members: DISABLED
Shared Drive Creation:  ADMIN ONLY
```

---
name: identity-mfa-passwordless
description: "Identity Mfa Passwordless."
domain: cybersecurity
---

|
| **FIDO2** | Fast Identity Online 2 standard enabling passwordless authentication using public-key cryptography bound to hardware authenticators or platform credentials |
| **Passkey** | FIDO2 credential that can be device-bound (security key) or synced across devices, providing phishing-resistant authentication without passwords |
| **Windows Hello for Business** | Windows platform authenticator using PIN, fingerprint, or facial recognition backed by TPM-protected asymmetric keys for passwordless sign-in |
| **Cloud Kerberos Trust** | Deployment model for hybrid WHfB that uses Azure AD Kerberos to authenticate to on-premises resources without requiring PKI certificate infrastructure |
| **Temporary Access Pass** | Time-limited passcode issued by admins enabling users to register passwordless methods or recover access when their primary method is unavailable |
| **Authentication Strength** | Conditional Access capability in Microsoft Entra that specifies which authentication method combinations satisfy MFA requirements for a given policy |

## Tools & Systems

- **Microsoft Entra Admin Center**: Portal for configuring authentication methods, Conditional Access policies, and monitoring sign-in analytics
- **Microsoft Intune**: MDM/MAM platform for deploying Windows Hello for Business configuration profiles to managed devices
- **Microsoft Graph API**: Programmatic interface for managing authentication methods, policies, and generating adoption reports
- **FIDO2 Security Keys**: Hardware authenticators (YubiKey, Feitian, Google Titan) storing cryptographic credentials for phishing-resistant authentication

## Common Scenarios

### Scenario: Enterprise-Wide Passwordless Migration

**Context**: Organization with 5,000 users plans to eliminate passwords within 12 months after experiencing a phishing attack that compromised 47 accounts. Current state: 60% use SMS MFA, 30% use Authenticator app, 10% have no MFA.

**Approach**:
1. Phase 1 (Month 1-2): Enable FIDO2 and WHfB authentication methods in report-only Conditional Access
2. Phase 2 (Month 2-3): Deploy WHfB to all managed Windows devices via Intune with Cloud Kerberos Trust
3. Phase 3 (Month 3-5): Distribute FIDO2 security keys to executives, IT admins, and finance (highest-risk users first)
4. Phase 4 (Month 5-8): Enable Authenticator passkeys for mobile-primary users and field workers
5. Phase 5 (Month 8-10): Switch Conditional Access from report-only to enforced for phishing-resistant auth
6. Phase 6 (Month 10-12): Disable SMS and voice call methods, block legacy authentication protocols
7. Ongoing: Monitor adoption metrics, issue TAPs for stragglers, maintain break-glass accounts

**Pitfalls**:
- Not deploying Cloud Kerberos Trust causes WHfB to fail for on-premises resource access in hybrid environments
- Enforcing passwordless without ensuring all applications support modern authentication breaks access
- Issuing only one security key per user without a backup creates lockout risk if the key is lost
- Not configuring Temporary Access Pass as a recovery method before disabling password-based sign-in

## Output Format

```
PASSWORDLESS AUTHENTICATION DEPLOYMENT REPORT
================================================
Tenant:            corp.onmicrosoft.com
Users:             5,247
Deployment Phase:  Phase 4 (Authenticator Passkeys)

AUTHENTICATION METHOD REGISTRATION
Passwordless Capable:    4,103 / 5,247 (78.2%)
  FIDO2 Security Keys:   892 (17.0%)
  Windows Hello:          2,847 (54.3%)
  Authenticator Passkey:  1,234 (23.5%)
  Certificate-Based:      312 (5.9%)

LEGACY METHOD STATUS
SMS-Only Users:          387 (7.4%) -- migration in progress
Voice-Only Users:        0 (disabled)
No MFA Users:            42 (0.8%) -- TAPs issued

CONDITIONAL ACCESS
Phishing-Resistant Policy:  ENFORCED (all users except exclusion group)
Legacy Auth Block:          ENABLED
Admin Portal Policy:        SECURITY KEY REQUIRED

SIGN-IN ANALYTICS (Last 30 Days)
Total Sign-Ins:          847,293
  Passwordless:          623,891 (73.6%)
  Password + MFA:        198,402 (23.4%)
  Password Only:         0 (blocked)
  Legacy Protocol:       0 (blocked)

SECURITY IMPACT
Phishing Incidents:      0 (down from 47 pre-deployment)
Password Reset Tickets:  -82% reduction
Avg Sign-In Time:        8.2s (passwordless) vs 24.1s (password)
```

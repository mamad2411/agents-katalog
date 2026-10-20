---
name: email-phishing-aitm
description: "Email Phishing Aitm."
domain: cybersecurity
---

|
| Tycoon 2FA | PhaaS | Microsoft 365, Google | CAPTCHA, Cloudflare turnstile |
| EvilProxy | PhaaS | Microsoft 365, Google, Okta | Random URLs, IP rotation |
| Evilginx | Open-source | Any web application | Custom phishlets |
| Sneaky 2FA | PhaaS | Microsoft 365 | Anti-bot checks |
| NakedPages | PhaaS | Multiple | Minimal infrastructure |

### Detection Indicators
- Authentication from unusual IP not matching user profile
- Session cookie reuse from different IP/device than authentication
- Login page served from non-Microsoft/non-Google infrastructure
- CDN requests to legitimate auth providers from phishing domains
- Impossible travel between authentication and session usage

## Workflow

### Step 1: Deploy Phishing-Resistant MFA
- Implement FIDO2 security keys or Windows Hello for Business for high-value accounts
- Configure Conditional Access to require phishing-resistant MFA for admins
- Enable certificate-based authentication where possible
- Disable SMS and voice MFA for privileged accounts
- AiTM cannot intercept FIDO2 because authentication is bound to origin domain

### Step 2: Configure Conditional Access Policies
- Require compliant/managed device for sensitive application access
- Block authentication from anonymous proxies and Tor exit nodes
- Enforce token binding to limit session cookie replay
- Configure continuous access evaluation (CAE) for real-time token revocation
- Implement sign-in risk policies that require re-authentication for risky sign-ins

### Step 3: Build AiTM Detection Rules
- Alert on sign-in followed by session from different IP within 10 minutes
- Detect authentication where proxy IP does not match user's expected location
- Monitor for impossible travel patterns in session usage
- Alert on inbox rules created immediately after authentication (common post-compromise)
- Detect new MFA method registration from suspicious sign-in

### Step 4: Monitor Web Proxy for AiTM Infrastructure
- Log and analyze DNS queries to newly registered domains
- Detect connections to known PhaaS infrastructure IPs
- Alert on authentication page backgrounds loaded from legitimate CDNs through proxy domains
- Monitor for SSL certificates issued to domains mimicking corporate login pages
- Block access to known EvilProxy/Evilginx infrastructure via threat intelligence

### Step 5: Implement Post-Compromise Detection
- Alert on mailbox forwarding rules created after suspicious authentication
- Detect OAuth app consent after AiTM sign-in
- Monitor for email sending patterns indicating BEC follow-up
- Alert on SharePoint/OneDrive mass download after session hijack
- Track lateral movement from compromised account

## Tools & Resources
- **Microsoft Entra ID Protection**: Risk-based Conditional Access
- **Azure AD Sign-in Logs**: Authentication event analysis
- **Okta ThreatInsight**: AiTM proxy detection at IdP level
- **Sekoia TDR**: AiTM campaign tracking and intelligence
- **Evilginx (defensive)**: Understanding attack mechanics for detection

## Validation
- Phishing-resistant MFA blocks AiTM session capture in test scenario
- Conditional Access denies session replay from different device/IP
- SIEM alerts fire on simulated AiTM sign-in patterns
- Web proxy blocks connections to known PhaaS infrastructure
- Post-compromise rules detect inbox rule creation after suspicious auth

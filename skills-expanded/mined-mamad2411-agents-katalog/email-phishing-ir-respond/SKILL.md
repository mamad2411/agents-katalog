---
name: email-phishing-ir-respond
description: "Email Phishing Ir Respond."
domain: cybersecurity
---

|
| **Spear Phishing** | Targeted phishing attack crafted for a specific individual or organization using personalized content |
| **Credential Harvesting** | Phishing technique that mimics a legitimate login page to capture usernames and passwords |
| **SPF (Sender Policy Framework)** | Email authentication protocol that specifies which mail servers are authorized to send email for a domain |
| **DKIM (DomainKeys Identified Mail)** | Email authentication method using cryptographic signatures to verify that an email was not altered in transit |
| **DMARC** | Policy framework that uses SPF and DKIM to determine email authenticity and instructs receivers on handling failures |
| **OAuth Consent Phishing** | Attack that tricks users into granting malicious OAuth applications access to their email and data |
| **Email Header** | Metadata embedded in every email containing routing, authentication, and sender information used for forensic analysis |

## Tools & Systems

- **Microsoft Defender for Office 365**: Email threat protection with Threat Explorer for investigation and automated purge
- **Proofpoint TAP (Targeted Attack Protection)**: Email security platform with URL rewriting and attachment sandboxing
- **URLscan.io**: Online service that scans URLs and captures screenshots of phishing pages for evidence
- **PhishTool**: Phishing analysis platform that automates header analysis, URL inspection, and IOC extraction
- **GoPhish**: Open-source phishing simulation platform for security awareness testing

## Common Scenarios

### Scenario: Microsoft 365 Credential Phishing via QR Code

**Context**: Users report an email claiming to be from IT requiring MFA re-enrollment. The email contains a QR code that links to a convincing Microsoft 365 login page clone hosted on a compromised WordPress site.

**Approach**:
1. Scan the QR code in a sandbox to extract the URL
2. Analyze the phishing page: captures credentials and MFA tokens (adversary-in-the-middle attack)
3. Search email gateway for all recipients using message subject and sender as search criteria
4. Cross-reference with proxy logs to identify users who visited the phishing URL
5. Force password reset and revoke sessions for all users who visited the URL
6. Purge the email from all mailboxes and block the sender domain
7. Notify users about the specific campaign with visual examples of the phishing email

**Pitfalls**:
- Not checking for adversary-in-the-middle (AiTM) capability that captures session tokens even with MFA
- Only resetting passwords without revoking active sessions (attacker retains access via stolen session cookies)
- Not searching for mailbox forwarding rules created by the attacker after compromising an account
- Missing QR code phishing (quishing) because URL scanning tools cannot decode QR code images

## Output Format

```
PHISHING INCIDENT RESPONSE REPORT
===================================
Incident:          INC-2025-1602
Date Reported:     2025-11-16T09:15:00Z
Reported By:       jdoe@corp.example.com
Classification:    Credential Phishing (AiTM)

EMAIL ANALYSIS
Subject:       "Action Required: MFA Re-enrollment"
Sender:        it-support@corp-security[.]com (spoofed)
SPF:           FAIL | DKIM: FAIL | DMARC: FAIL
Phishing URL:  hxxps://compromised-site[.]com/ms365/login
Phishing Type: Microsoft 365 AiTM credential harvester

IMPACT ASSESSMENT
Recipients:        47
Clicked Link:      8
Credentials Entered: 3 (confirmed via proxy POST data)

CONTAINMENT ACTIONS
[x] Email purged from all 47 mailboxes
[x] Phishing domain blocked at web proxy
[x] Sender domain blocked at email gateway
[x] 3 compromised accounts: passwords reset, sessions revoked
[x] Mailbox forwarding rules reviewed (1 malicious rule removed)
[x] OAuth app grants reviewed (no unauthorized grants found)

IOCs EXTRACTED
Domain:  corp-security[.]com
URL:     hxxps://compromised-site[.]com/ms365/login
IP:      104.21.x.x (Cloudflare-hosted)
Sender:  it-support@corp-security[.]com

RECOMMENDATIONS
1. Implement DMARC enforcement (p=reject) for corp domain
2. Deploy QR code scanning in email gateway
3. Send targeted awareness notification to all 47 recipients
4. Request domain takedown via registrar abuse contact
```

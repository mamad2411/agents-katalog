---
name: email-forensics-phishing
description: "Email Forensics Phishing."
domain: cybersecurity
---

|
| MXToolbox | Online email header analyzer and DNS lookup |
| dig/nslookup | DNS record queries for SPF, DKIM, DMARC verification |
| pyspf | Python SPF record validation library |
| dkimpy | Python DKIM signature verification library |
| PhishTool | Specialized phishing email analysis platform |
| VirusTotal | URL and file reputation checking service |
| AbuseIPDB | IP address reputation database |
| whois | Domain registration information lookup |

## Common Scenarios

**Scenario 1: CEO Fraud / Business Email Compromise**
The email claims to be from the CEO but Reply-To points to a Gmail address, SPF fails because the sending IP is not authorized for the spoofed domain, DKIM is missing, and the From domain is a lookalike (ceo-company.com vs company.com).

**Scenario 2: Credential Harvesting Phishing**
Email contains a link that displays "login.microsoft.com" but href points to a lookalike domain, the attachment is an HTML file containing a fake login page with credential exfiltration JavaScript, the sending domain was registered 3 days ago.

**Scenario 3: Malware Delivery via Attachment**
Email with an Office document attachment containing macros, the sender domain passes SPF but the account was compromised, DKIM signature is valid (sent from legitimate infrastructure), attachment SHA-256 matches known malware on VirusTotal.

**Scenario 4: Spear Phishing with Legitimate Service**
Attacker uses a legitimate email marketing service to send phishing, SPF and DKIM pass because the service is authorized, the phishing is in the content not the infrastructure, requires URL and content analysis rather than header authentication checks.

## Output Format

```
Email Header Analysis Report:
  Subject:     "Urgent: Invoice Payment Required"
  From:        accounting@examp1e-corp.com (SPOOFED)
  Reply-To:    payments.urgent@gmail.com (MISMATCH)
  Return-Path: <bounce@mail-server.xyz>
  Date:        2024-01-15 09:23:45 UTC

  Delivery Path (4 hops):
    Hop 1: mail-server.xyz [203.0.113.45] -> relay1.isp.com
    Hop 2: relay1.isp.com -> mx.target-company.com
    Hop 3: mx.target-company.com -> internal-filter.target.com
    Hop 4: internal-filter.target.com -> mailbox

  Authentication:
    SPF:    FAIL (203.0.113.45 not authorized for examp1e-corp.com)
    DKIM:   NONE (no signature present)
    DMARC:  FAIL (p=none, no enforcement)

  Indicators of Phishing:
    - Lookalike domain (examp1e-corp.com vs example-corp.com, 96% similar)
    - From/Reply-To mismatch
    - Domain registered 2 days before email sent
    - URL in body points to credential harvesting page
    - Attachment: invoice.xlsm (SHA-256: a3f2...) - Known malware on VT

  Risk Level: HIGH
```

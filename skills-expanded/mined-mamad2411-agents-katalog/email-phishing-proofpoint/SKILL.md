---
name: email-phishing-proofpoint
description: "Email Phishing Proofpoint."
domain: cybersecurity
---

|
| Connection | IP reputation, rate limiting | Spam botnets |
| Authentication | SPF, DKIM, DMARC enforcement | Spoofing |
| Content | ML classifiers, NLP analysis | BEC, phishing |
| URL | Rewriting + time-of-click sandbox | Credential theft |
| Attachment | Static + dynamic sandboxing | Malware, ransomware |
| Post-delivery | TRAP (auto-retraction) | Weaponized after delivery |

## Workflow

### Step 1: Plan Mail Flow Architecture
- Document current MX records and mail flow path
- Identify all legitimate sending sources (marketing platforms, CRM, ticketing systems)
- Map inbound connectors and transport rules in Microsoft 365 or Google Workspace
- Plan IP allowlisting for Proofpoint egress IPs on receiving infrastructure
- Configure SPF record to include Proofpoint: `v=spf1 include:spf.protection.outlook.com include:spf-a.proofpoint.com -all`

### Step 2: Configure Proofpoint Policies
- Create organizational units matching business structure
- Define inbound mail policies: anti-spam, anti-virus, impostor detection
- Configure Smart Search quarantine with end-user digest notifications
- Set up Proofpoint Encryption for sensitive outbound messages
- Enable Targeted Attack Protection (TAP) for URL and attachment sandboxing

### Step 3: Deploy Email Authentication
- Configure DKIM signing through Proofpoint for outbound messages
- Set DMARC policy to monitor mode initially: `v=DMARC1; p=none; rua=mailto:dmarc@company.com`
- Enable inbound DMARC enforcement to reject spoofed messages
- Configure anti-spoofing rules for executive impersonation protection

### Step 4: Enable Advanced Threat Protection
- Activate URL Defense with rewriting enabled for all inbound messages
- Configure Attachment Defense sandbox policies (safe attachment mode)
- Enable Threat Response Auto-Pull (TRAP) for post-delivery remediation
- Set up TAP Dashboard alerts for targeted attack campaigns
- Configure Supplier Risk monitoring for vendor email compromise

### Step 5: Migrate MX Records
- Lower MX record TTL to 300 seconds 48 hours before cutover
- Update MX records to point to Proofpoint: `company-com.mail.protection.proofpoint.com`
- Configure connector restrictions in Microsoft 365 to accept mail only from Proofpoint IPs
- Monitor mail flow through Proofpoint Message Trace for 48-72 hours
- Verify no legitimate mail is being blocked or delayed

### Step 6: Tune and Optimize
- Review quarantine and false positive/negative rates weekly for first month
- Adjust spam thresholds based on organizational tolerance
- Add approved senders and safe lists for legitimate bulk mail
- Configure data loss prevention (DLP) rules for outbound sensitive content
- Enable email warning banners for external sender identification

## Tools & Resources
- **Proofpoint TAP Dashboard**: Real-time threat visibility and campaign tracking
- **Proofpoint TRAP**: Automated post-delivery email retraction
- **Proofpoint SER (Spam/End-user Release)**: Self-service quarantine management
- **Proofpoint Closed-Loop Email Analysis (CLEAR)**: Phishing report button integration
- **MX Toolbox**: DNS record verification and mail flow testing

## Validation
- All inbound email routes through Proofpoint (verify MX records and message headers)
- TAP Dashboard shows threat detections and blocked campaigns
- URL Defense rewrites links in test messages and sandboxes at click time
- Attachment Defense detonates test malware samples in sandbox
- TRAP successfully retracts test phishing message from inboxes post-delivery
- False positive rate below 0.1% after initial tuning period
- DMARC/SPF/DKIM authentication passes for all legitimate outbound mail

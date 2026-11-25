---
name: email-phishing-mimecast
description: "Email Phishing Mimecast."
domain: cybersecurity
---

|
| URL Protect | Rewrites and scans URLs at click time | Real-time sandbox, pre-delivery hold |
| Attachment Protect | Sandboxes suspicious attachments | Static + dynamic analysis |
| Impersonation Protect | Detects BEC/whaling attacks | VIP name matching, header analysis |
| Internal Email Protect | Scans internal/outbound email | Lateral phishing detection |

### Impersonation Protection Scenarios
- **Hit 3 (Default)**: Flags emails matching 3+ impersonation indicators
- **Hit 1 (VIP)**: Flags emails matching 1+ indicator for designated VIP users
- Key identifiers: display name similarity, domain similarity, reply-to mismatch, newly registered domains

### URL Protect Modes
- **Rewrite**: URLs rewritten to route through Mimecast proxy at click time
- **Pre-Delivery Action (Hold)**: URLs checked before message delivery; held if suspicious
- **Pre-Delivery Action (None)**: URLs checked pre-delivery but not held

## Workflow

### Step 1: Configure URL Protect Policy
- Navigate to Administration > Gateway > Policies > Targeted Threat Protection - URL Protect
- Create URL Protect definition with rewriting enabled for inbound messages
- Enable URL Pre-Delivery Action set to "Hold" for maximum protection
- Configure scan mode: aggressive for high-risk users, moderate for general population
- Set action for malicious URLs: block page with user notification
- Enable URL logging for all click events

### Step 2: Configure Attachment Protect Policy
- Navigate to Administration > Gateway > Policies > Targeted Threat Protection - Attachment Protect
- Create Attachment Protect definition for inbound email
- Select sandbox mode: "Safe File" (converts to safe format) or "Dynamic Configuration" (full sandbox)
- Configure attachment types to scan: executables, Office documents, PDFs, archives
- Set timeout for sandbox analysis (default: up to 7 minutes for complex files)
- Enable pre-emptive sandboxing for attachments from unknown senders

### Step 3: Configure Impersonation Protect
- Create Default Impersonation Protect Definition (Hit 3) for all inbound email
- Create VIP Impersonation Protect Definition (Hit 1) for executive protection
- Build VIP list: CEO, CFO, CTO, board members, finance leadership
- Configure detection identifiers: display name, domain similarity, newly observed sender
- Set actions: quarantine high-confidence impersonation, tag moderate confidence
- Enable end-user warning banners for flagged messages

### Step 4: Enable Internal Email Protect
- Configure journaling from Microsoft 365/Google Workspace to Mimecast
- Enable URL scanning for internal emails
- Enable attachment scanning for internal emails
- Configure alerts for internal account compromise indicators
- Set up detection for internal phishing (compromised account sending malware)

### Step 5: Create Test Group and Validate
- Create pilot group of 50-100 users across departments
- Apply TTP policies to pilot group first
- Send test emails with known-safe test URLs and EICAR test files
- Verify URL rewriting, attachment sandboxing, and impersonation detection
- Monitor false positive rate for 1-2 weeks before organization-wide deployment

### Step 6: Deploy Organization-Wide and Tune
- Extend TTP policies to all users
- Monitor Mimecast Threat Dashboard for detection metrics
- Review and whitelist legitimate applications triggering false positives
- Tune impersonation sensitivity based on false positive feedback
- Configure exception policies for automated systems and mailing lists

## Tools & Resources
- **Mimecast Administration Console**: Policy configuration and management
- **Mimecast Threat Dashboard**: Real-time threat visibility and analytics
- **Mimecast Awareness Training**: Integrated security awareness platform
- **Mimecast API**: Programmatic access to logs and threat data
- **Message Center**: Quarantine management for admins and users

## Validation
- URL Protect rewrites URLs in test messages and blocks known-malicious at click
- Attachment Protect sandboxes test file and returns verdict within SLA
- Impersonation Protect flags test BEC email impersonating VIP
- Internal Email Protect detects test lateral phishing scenario
- Pre-delivery hold catches weaponized URL before reaching inbox
- False positive rate below organizational threshold after tuning

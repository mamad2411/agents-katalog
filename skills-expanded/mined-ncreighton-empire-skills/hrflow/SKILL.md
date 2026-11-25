---
name: hrflow
description: "Automate employee onboarding and offboarding workflows with HRIS integration, compliance tracking, and multi-step task automation. Use when the user needs to streamline HR processes, ensure compliance, or manage employee lifecycle events across systems."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "HRIS_API_KEY",
          "SLACK_WEBHOOK_URL",
          "GOOGLE_WORKSPACE_ADMIN_KEY",
          "COMPLIANCE_DATABASE_URL"
        ],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "👥"
    }
  }
---

## Overview

HRFlow automates the complete employee lifecycle—from hiring through offboarding—by orchestrating multi-step workflows across your HRIS, email systems, Google Workspace/Microsoft 365, Slack, and compliance databases. This skill eliminates manual HR tasks that create bottlenecks, compliance risks, and inconsistent experiences.

**Why it matters:** HR teams spend 30-40% of their time on repetitive onboarding/offboarding tasks. HRFlow reduces this to minutes while ensuring every new hire gets consistent setup and every departing employee's access is revoked systematically.

**Key integrations:**
- **HRIS Systems:** BambooHR, Workday, ADP, Guidepoint
- **Communication:** Slack, Microsoft Teams, Gmail/Google Workspace
- **Identity & Access:** Google Workspace, Microsoft Entra ID, Okta
- **Compliance:** DocuSign, Lattice, Workiva
- **File Storage:** Google Drive, OneDrive, Dropbox
- **Ticketing:** Jira, Linear, GitHub Issues

---

## Quick Start

### Example 1: Trigger Full Onboarding Workflow
```
"Onboard Sarah Chen as Senior Product Manager starting 2024-02-15. 
She reports to Alex Martinez. Create her Slack account, Google Workspace 
email, add to #product channel, provision laptop in IT queue, send 
welcome email with company handbook, and create 30-60-90 day checklist."
```

**What happens:**
1. Extracts employee data → pushes to HRIS
2. Creates Slack account with custom profile
3. Provisions Google Workspace email with security groups
4. Queues IT request for hardware setup
5. Sends templated welcome email with onboarding links
6. Creates Monday.com task for manager with 30-60-90 milestones

### Example 2: Offboarding with Compliance Lock
```
"Offboard Marcus Williams effective 2024-02-20. Reason: Resignation. 
Ensure all access is revoked, data is transferred to his manager, 
compliance audit is logged, and exit interview is scheduled."
```

**What happens:**
1. Disables Google Workspace & Slack accounts immediately
2. Transfers Google Drive ownership to manager
3. Removes from all security groups
4. Logs offboarding event in compliance database
5. Schedules exit interview via Calendly
6. Sends offboarding checklist to HR manager

### Example 3: Bulk Onboarding from CSV
```
"Batch onboard employees from this CSV file. Process 12 new hires, 
stagger notifications by 2 hours, flag anyone with special equipment 
needs, and send daily digest to HR manager."
```

**What happens:**
1. Parses CSV and validates required fields
2. Creates staggered workflow executions
3. Identifies equipment flags and escalates
4. Sends daily progress report to HR Slack channel

---

## Capabilities

### Onboarding Automation
- **Pre-arrival setup** — Create accounts, provision hardware, prepare workspace
- **First-day experience** — Welcome email, system access, team introductions via Slack
- **Ramp-up tracking** — Auto-generate 30-60-90 day milestones, assign mentors, schedule check-ins
- **Custom workflows** — Branch logic based on department, role, location, or seniority
- **Document automation** — Generate offer letters, employment agreements, policy acknowledgments via DocuSign

### Offboarding Automation
- **Access revocation** — Disable accounts across all systems simultaneously (zero-trust model)
- **Data transfer** — Migrate email, files, calendar ownership to manager/designated person
- **Equipment recovery** — Generate return checklists, track physical assets
- **Compliance logging** — Immutable audit trail of all offboarding actions
- **Exit workflows** — Schedule interviews, collect feedback, process final paycheck

### Compliance & Audit
- **Real-time tracking** — Monitor compliance status across all systems
- **Regulatory alignment** — Support SOC 2, HIPAA, GDPR, CCPA requirements
- **Audit reports** — Generate monthly/quarterly compliance summaries
- **Access reviews** — Automated periodic access certification
- **Termination verification** — Confirm all access actually revoked (prevents orphaned accounts)

### Integration & Orchestration
- **HRIS sync** — Two-way sync with BambooHR, Workday, ADP (new hires → accounts, terminations → revoke)
- **Slack automation** — Channel creation, user invitations, welcome bots, manager notifications
- **Email campaigns** — Personalized onboarding sequences, compliance reminders, exit communications
- **Calendar management** — Auto-schedule onboarding meetings, 1:1s, team introductions
- **Webhook triggers** — Listen to HRIS events, GitHub team changes, or custom triggers

---

## Configuration

### Required Environment Variables

```bash
# HRIS Configuration
HRIS_API_KEY=your_hris_api_key
HRIS_PROVIDER=bamboohr  # or workday, adp, guidepoint
HRIS_WEBHOOK_SECRET=your_webhook_secret

# Google Workspace (Admin API)
GOOGLE_WORKSPACE_ADMIN_KEY=/path/to/service-account.json
GOOGLE_WORKSPACE_DOMAIN=yourcompany.com

# Slack Integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your_signing_secret

# Compliance & Audit
COMPLIANCE_DATABASE_URL=postgresql://user:pass@host/compliance_db
AUDIT_LOG_BUCKET=s3://your-audit-logs-bucket

# Optional: Microsoft 365
MICROSOFT_TENANT_ID=your-tenant-id
MICROSOFT_CLIENT_ID=your-client-id
MICROSOFT_CLIENT_SECRET=your-client-secret

# Optional: DocuSign for document automation
DOCUSIGN_API_KEY=your_docusign_key
DOCUSIGN_ACCOUNT_ID=your_account_id
```

### Workflow Configuration Options

```yaml
# config.yaml example
onboarding:
  auto_create_slack: true
  auto_create_email: true
  email_domain: "@yourcompany.com"
  default_groups:
    - all-hands
    - department-specific
  welcome_email_template: "default_onboarding"
  hardware_queue_system: "jira"
  manager_notification_delay: 0  # minutes

offboarding:
  revocation_delay: 0  # immediate (0) or grace period (hours)
  data_transfer_method: "manager"  # manager or archive
  archive_bucket: "s3://offboarded-employees"
  compliance_audit_required: true
  exit_interview_enabled: true
  exit_interview_tool: "calendly"

compliance:
  log_all_actions: true
  require_approval_for: ["data_transfer", "bulk_access_changes"]
  audit_retention_days: 2555  # 7 years
  monthly_access_review: true
  soc2_mode: true
```

---

## Example Outputs

### Onboarding Confirmation
```json
{
  "status": "success",
  "employee_id": "EMP-2024-0847",
  "employee_name": "Sarah Chen",
  "workflow_id": "onboard-20240215-sarahchen",
  "actions_completed": [
    {
      "action": "hris_record_created",
      "timestamp": "2024-02-15T08:00:00Z",
      "details": {
        "employee_id": "EMP-2024-0847",
        "department": "Product",
        "manager_id": "EMP-2020-0312"
      }
    },
    {
      "action": "slack_account_created",
      "timestamp": "2024-02-15T08:02:15Z",
      "details": {
        "username": "sarah.chen",
        "email": "sarah.chen@yourcompany.com",
        "channels_added": ["general", "product", "all-hands", "product-managers"]
      }
    },
    {
      "action": "google_workspace_email_provisioned",
      "timestamp": "2024-02-15T08:04:30Z",
      "details": {
        "email": "sarah.chen@yourcompany.com",
        "security_groups": ["employees", "product-team", "salary-band-4"]
      }
    },
    {
      "action": "welcome_email_sent",
      "timestamp": "2024-02-15T08:05:00Z",
      "details": {
        "recipient": "sarah.chen@yourcompany.com",
        "template": "default_onboarding",
        "includes": ["handbook", "benefits_guide", "org_chart", "tech_setup_guide"]
      }
    },
    {
      "action": "it_hardware_request_created",
      "timestamp": "2024-02-15T08:06:00Z",
      "details": {
        "ticket_id": "IT-8734",
        "items": ["MacBook Pro 16GB", "USB-C Hub", "Monitor", "Keyboard", "Mouse"],
        "status": "pending_approval"
      }
    },
    {
      "action": "onboarding_checklist_created",
      "timestamp": "2024-02-15T08:07:00Z",
      "details": {
        "checklist_id": "CHK-2024-0847",
        "assigned_to": "alex.martinez",
        "milestones": ["30-day", "60-day", "90-day"]
      }
    }
  ],
  "next_steps": [
    "Hardware will arrive by 2024-02-17",
    "First team meeting scheduled for 2024-02-15 at 2:00 PM",
    "Manager check-in scheduled for 2024-02-22"
  ],
  "compliance_status": "audit_logged"
}
```

### Offboarding Confirmation
```json
{
  "status": "success",
  "employee_id": "EMP-2020-0156",
  "employee_name": "Marcus Williams",
  "offboarding_date": "2024-02-20",
  "workflow_id": "offboard-20240220-marcuswilliams",
  "actions_completed": [
    {
      "action": "slack_account_disabled",
      "timestamp": "2024-02-20T09:00:00Z",
      "status": "complete"
    },
    {
      "action": "google_workspace_disabled",
      "timestamp": "2024-02-20T09:01:30Z",
      "status": "complete",
      "details": {
        "email_forwarding_enabled": "manager@yourcompany.com",
        "calendar_transferred": true,
        "drive_transferred": true
      }
    },
    {
      "action": "access_revoked",
      "timestamp": "2024-02-20T09:03:00Z",
      "systems_revoked": [
        "Jira",
        "GitHub",
        "AWS Console",
        "Figma",
        "Notion",
        "Linear"
      ]
    },
    {
      "action": "compliance_audit_logged",
      "timestamp": "2024-02-20T09:05:00Z",
      "audit_id": "AUD-2024-2847",
      "details": {
        "reason": "Resignation",
        "final_access_check": "passed",
        "all_systems_verified": true
      }
    },
    {
      "action": "exit_interview_scheduled",
      "timestamp": "2024-02-20T09:06:00Z",
      "details": {
        "interview_date": "2024-02-23T10:00:00Z",
        "interviewer": "hr.manager@yourcompany.com"
      }
    }
  ],
  "data_transfer_summary": {
    "emails_forwarded_to": "alex.martinez@yourcompany.com",
    "files_archived_to": "s3://offboarded-employees/marcus-williams-2024",
    "calendar_transferred": true,
    "contacts_exported": true
  },
  "compliance_status": "fully_compliant"
}
```

---

## Tips & Best Practices

### Maximize Efficiency
1. **Batch processing** — Use bulk onboarding for new cohorts (interns, seasonal hires) to save time
2. **Custom templates** — Create department-specific onboarding flows (Engineering vs. Sales have different needs)
3. **Stagger notifications** — Spread Slack/email notifications over 2-4 hours to avoid overwhelming new hires
4. **Automate approvals** — Set up auto-approval for standard hardware requests under $2,000

### Ensure Compliance
1. **Enable audit logging** — Always set `log_all_actions: true` for SOC 2/HIPAA compliance
2. **Use immutable audit trails** — Store logs in S3 with versioning enabled
3. **Schedule monthly access reviews** — Catch orphaned accounts and stale permissions
4. **Test offboarding quarterly** — Run mock offboarding scenarios to verify all systems respond correctly
5. **Document exceptions** — If you manually override workflow steps, log the reason in compliance database

### Optimize User Experience
1. **Personalize welcome emails** — Include manager name, team info, and first-day schedule
2. **Create Slack welcome bots** — Auto-post onboarding resources to new hire channels
3. **Assign mentors** — Use workflow to pair new hires with experienced teammates
4. **Schedule team introductions** — Auto-calendar 15-min 1:1s between new hire and cross-functional peers
5. **Send weekly check-ins** — Automated Slack messages at days 1, 7, 30, 60, 90

### Integration Best Practices
1. **Sync HRIS as source of truth** — All employee changes should originate in HRIS, not manually
2. **Use webhooks for real-time updates** — Don't rely on scheduled syncs; listen for HRIS events
3. **Test integrations in staging** — Verify Slack/Google/HRIS connections before production
4. **Monitor sync failures** — Set up alerts if HRIS → Slack sync fails for >15 minutes
5. **Keep API keys rotated** — Refresh HRIS/Google/Slack tokens every 90 days

---

## Safety & Guardrails

### What HRFlow Will NOT Do
- **No unauthorized account access** — Will never access employee files without explicit workflow trigger
- **No data exfiltration** — Archived employee data is stored in compliance-approved buckets only
- **No bulk changes without approval** — Requires explicit user confirmation for mass offboarding
- **No unlogged actions** — Every account creation/deletion/modification is audited and timestamped
- **No deletion without retention period** — Offboarded employee data is archived for 7 years, not deleted

### Boundaries & Limitations
1. **Manual approval required** — Offboarding workflows require HR manager sign-off before access revocation
2. **Grace periods supported** — Can delay access revocation (e.g., 24 hours) for graceful employee transition
3. **No access to personal data** — Only accesses employee records necessary for onboarding/offboarding
4. **Compliance-first design** — All workflows default to "deny" unless explicitly approved
5. **Rate limiting** — Staggered account creation to prevent system overload (max 50 accounts/hour)

### Data Privacy
- GDPR compliant — Supports right-to-
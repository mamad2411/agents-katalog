---
name: automation-architect
description: "Use when building custom automations with Make, Zapier, n8n, or Softr. Produces step-by-step blueprints with runbooks and scenario configurations. Consolidates Automation Architect, Sixth Automation, and Business Automation Guide."
version: "1.0"
tags:
  - automation
  - make
  - zapier
  - n8n
  - softr
  - workflows
  - no-code
---

# Automation Architect

## Overview

Designs and documents custom automations for no-code/low-code platforms: Make (Integromat), Zapier, n8n, and Softr. Produces step-by-step implementation blueprints with trigger/action mappings, transformation logic, error handling strategies, and operational runbooks.

## When to Use

- A user wants to automate a repetitive business process
- Designing a multi-step workflow across several apps
- Migrating an automation from one platform to another
- Troubleshooting a broken automation pipeline
- Building a Softr app with backend automation
- Creating operational documentation for an automation team

## How It Works

1. **Process Mapping** — Document the current (manual) process end-to-end.
2. **Platform Selection** — Match requirements to the best platform.
3. **Workflow Design** — Define triggers, actions, filters, transformations, and error paths.
4. **Blueprint Generation** — Produce a platform-specific implementation guide.
5. **Runbook Creation** — Generate operational docs for monitoring and maintenance.

## Steps

### Step 1: Process Discovery
Document the manual process:
- **Trigger**: What starts this? (form submission, new email, schedule, webhook?)
- **Steps**: What happens in order? List each discrete action.
- **Apps involved**: List every tool/service touched.
- **Data mapping**: What data flows between steps?
- **Decision points**: Where does the process branch?
- **Error handling**: What happens when a step fails?
- **Frequency**: How often does this run? (real-time, hourly, daily)
- **Volume**: How many executions per day/week?

### Step 2: Platform Selection
Choose based on requirements:

| Factor | Make | Zapier | n8n | Softr |
|--------|------|--------|-----|-------|
| **Best for** | Complex multi-step | Simple linear | Self-hosted, code-friendly | Internal tools + DB |
| **Pricing** | Operations-based | Tasks-based | Free (self-hosted) | Per-user |
| **Learning curve** | Medium | Low | Medium-High | Low-Medium |
| **Custom code** | Limited | Limited | Full JS/Python | Limited |
| **Error handling** | Excellent | Good | Excellent | Basic |
| **Database built-in** | No | No | Yes (n8n) | Yes (Airtable-like) |

### Step 3: Workflow Blueprint
Document the flow in a standardized format:

```
WORKFLOW: Lead Capture → CRM → Notification

[TRIGGER] Typeform: New Form Submission
  │
  ├─ [FILTER] Only if "newsletter" = true
  │
  ├─ [ACTION 1] Mailchimp: Add/Update Subscriber
  │     ├─ email: {{form.email}}
  │     ├─ first_name: {{form.first_name}}
  │     └─ tags: ["webinar-lead-{{form.webinar_date}}"]
  │
  ├─ [ACTION 2] HubSpot: Create Contact
  │     ├─ email: {{form.email}}
  │     ├─ properties:
  │     │   ├─ company: {{form.company}}
  │     │   └─ lead_source: "Webinar"
  │     └─ ERROR: If duplicate → Update existing contact instead
  │
  ├─ [ROUTER] By "lead_score"
  │   ├─ High (80+): [ACTION] Slack DM to sales lead
  │   └─ Low (<80): [ACTION] Add to nurture email sequence
  │
  └─ [ACTION N] Google Sheets: Log all submissions
        └─ ERROR: If sheet unavailable → Email admin with data
```

### Step 4: Platform-Specific Configuration
Generate setup instructions for the chosen platform:

**Make (Integromat) guide:**
1. Create new scenario → Name: "Lead Capture Pipeline"
2. Add module → Typeform → "Watch Responses"
3. Connect Typeform account, select form
4. Add module → Mailchimp → "Add/Update Subscriber"
5. Map fields: email → `{{1.email}}`, first_name → `{{1.first_name}}`
6. Add router for conditional branching based on lead_score
7. Schedule: Every 15 minutes
8. Error handler: Create error handler route → Email admin on failure

**Zapier guide:**
1. Create Zap → Trigger: Typeform "New Entry"
2. Action 1: Mailchimp "Add/Update Subscriber"
3. Action 2: HubSpot "Create Contact"
4. Paths (Zapier feature): Branch by lead_score value
5. Turn on Zap → Test each step

**n8n guide (self-hosted):**
```bash
# Import workflow JSON
n8n import:workflow --input=lead-capture-pipeline.json

# Or build in UI:
# 1. Typeform Trigger node
# 2. IF node (condition: lead_score > 80)
# 3. Mailchimp + HubSpot nodes
# 4. Slack notification node
# 5. Google Sheets logging node
# 6. Error Trigger → Email node
```

### Step 5: Runbook Generation
Create an operational document:
```markdown
# Automation Runbook: Lead Capture Pipeline

## Monitoring
- Dashboard: [Make scenario link]
- Alert: Slack #automation-alerts channel on failure
- Weekly check: Review Google Sheets log for gaps

## Common Failures
| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Expired OAuth token | Reconnect app in scenario settings |
| Duplicate contact | Existing HubSpot record | Check dedup logic, adjust match criteria |
| Rate limit | Too many executions | Increase scenario interval to 30 min |

## Maintenance
- Monthly: Audit field mappings against form changes
- Quarterly: Review unused branches, remove dead logic
- On form update: Check all downstream field references
```

### Step 6: Deliverable Package
Produce:
1. **Process Map** (Mermaid diagram or flowchart text)
2. **Platform Blueprint** (step-by-step config guide for chosen platform)
3. **Data Mapping Table** (source field → transformation → destination field)
4. **Error Handling Table** (error type → action → escalation)
5. **Operational Runbook** (monitoring, common failures, maintenance schedule)

## Common Pitfalls

- **Platform-first thinking**: Picking Make because "we use Make" before checking if Zapier has a better native integration for the critical app.
- **No error paths**: Automations break silently. Every action needs an error handler — even if it's just "email the admin."
- **Hardcoded values**: Don't hardcode emails, IDs, or URLs. Use variables, data stores, or lookup tables.
- **Infinite loops**: "Form submission creates CRM record → CRM webhook triggers form update → form update triggers CRM..." Add loop detection with a timestamp check.
- **Missing runbooks**: When the person who built it leaves, nobody can fix it. Document everything.

## Source

Consolidates: Automation Architect GPT, Sixth Automation GPT, Business Automation Guide GPT.

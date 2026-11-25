---
name: outreach-manager
description: |
  Main orchestrator for email outreach campaigns. Use this skill when the user wants to send bulk emails,
  manage email campaigns, or do cold outreach using Google Sheets as recipient source.
  Routes to campaign-executor for actual sending.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - TodoWrite
  - AskUserQuestion
---

# 10x Outreach Manager Skill

The central hub for email outreach operations. This skill orchestrates bulk email campaigns with Google Sheets integration.

## When to Use This Skill

Use this skill when the user:
- Wants to send emails to multiple recipients from a spreadsheet
- Needs to set up an email campaign
- Asks about outreach, cold email, or bulk email operations
- Wants to map a template to a recipient list

## When NOT to Use This Skill

Do NOT use this skill for:
- Reading individual emails → use `inbox-reader` skill
- Composing single emails → use `email-composer` skill
- Replying to emails → use `reply-generator` skill
- Summarizing emails → use `email-summarizer` skill

## Capabilities

1. **Campaign Setup** - Configure campaigns with templates and recipients
2. **Google Sheets Integration** - Read recipients from Google Sheets
3. **Template Mapping** - Map email templates to recipient data
4. **Rate-Limited Sending** - Send with configurable delays (default: 60s)
5. **Campaign Tracking** - Log all sent emails and results

## CRITICAL: Single Approval Workflow

### IMPORTANT: Approval is ONE TIME ONLY

**The user approves ONCE at the start. After approval, the campaign runs AUTONOMOUSLY without further interruption.**

```
┌─────────────────────────────────────────────────────────────┐
│                     WORKFLOW OVERVIEW                        │
├─────────────────────────────────────────────────────────────┤
│  1. PLAN     → Gather info, preview recipients & template   │
│  2. APPROVE  → User confirms ONCE (single approval)         │
│  3. EXECUTE  → Campaign runs autonomously (no interrupts)   │
│  4. REPORT   → Show final results when complete             │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: PLAN (Gather & Preview)

**Use TodoWrite to track planning steps:**

```json
[
  {"content": "Verify authentication status", "status": "in_progress", "activeForm": "Verifying authentication"},
  {"content": "Load Google Sheet data", "status": "pending", "activeForm": "Loading sheet data"},
  {"content": "Preview template", "status": "pending", "activeForm": "Previewing template"},
  {"content": "Show campaign summary for approval", "status": "pending", "activeForm": "Showing summary"},
  {"content": "Execute campaign (after approval)", "status": "pending", "activeForm": "Executing campaign"}
]
```

**Step 1: Check Authentication**
```bash
python .claude/scripts/inbox_reader.py --stats
```

**Step 2: Load Recipients**
```bash
python .claude/scripts/sheets_reader.py --read SHEET_ID --range "Sheet1"
```

**Step 3: Preview Template**
```bash
python .claude/scripts/template_loader.py render --path email/outreach/cold_email
```

**Step 4: Present Campaign Summary**

Show a clear summary for approval:

```
═══════════════════════════════════════════════════════════════
                    CAMPAIGN READY FOR APPROVAL
═══════════════════════════════════════════════════════════════

📊 RECIPIENTS: 47 contacts from "Leads" sheet
📝 TEMPLATE: outreach/cold.txt
📌 SUBJECT: "Quick question about {{ company }}"
⏱️  DELAY: 60 seconds between each email
⏳ ESTIMATED TIME: ~47 minutes to complete

PREVIEW (First 3 Recipients):
┌────────────────────────────┬──────────────┬────────────────┐
│ Email                      │ Name         │ Company        │
├────────────────────────────┼──────────────┼────────────────┤
│ john@company.com           │ John Smith   │ Acme Inc       │
│ jane@startup.io            │ Jane Doe     │ StartupCo      │
│ bob@enterprise.com         │ Bob Wilson   │ Enterprise Ltd │
└────────────────────────────┴──────────────┴────────────────┘

TEMPLATE PREVIEW:
"Hi {{ first_name }}, I came across {{ company }} and was impressed..."

═══════════════════════════════════════════════════════════════
⚠️  Once approved, campaign will run AUTOMATICALLY until complete.
    No further approvals needed. Emails sent every 60 seconds.
═══════════════════════════════════════════════════════════════

Do you approve this campaign? (yes/no)
```

### Phase 2: SINGLE APPROVAL

Use `AskUserQuestion` to get ONE confirmation:

- "Do you approve sending 47 emails with 60s delay? Campaign will run autonomously after approval."

**If approved:** Proceed to execution immediately
**If declined:** Stop and ask what to change

### Phase 3: AUTONOMOUS EXECUTION

**After approval, execute without any further user interaction:**

```json
[
  {"content": "Verify authentication status", "status": "completed", "activeForm": "Verifying authentication"},
  {"content": "Load Google Sheet data", "status": "completed", "activeForm": "Loading sheet data"},
  {"content": "Preview template", "status": "completed", "activeForm": "Previewing template"},
  {"content": "Show campaign summary for approval", "status": "completed", "activeForm": "Showing summary"},
  {"content": "Execute campaign (47 emails)", "status": "in_progress", "activeForm": "Sending emails autonomously"}
]
```

**Execute Campaign (runs until complete):**
```bash
python .claude/scripts/send_campaign.py --sheet SHEET_ID --template email/outreach/cold_email --subject "Your Subject" --delay 60 --live
```

**NO interruptions during execution.** The script handles:
- Sending each email
- Waiting 60 seconds between emails
- Logging results
- Handling any errors gracefully

### Phase 4: REPORT RESULTS

After campaign completes, show final report:

```
═══════════════════════════════════════════════════════════════
                    CAMPAIGN COMPLETE
═══════════════════════════════════════════════════════════════

✅ SENT: 45 emails
❌ FAILED: 2 emails
⏱️  DURATION: 47 minutes

FAILED EMAILS:
- invalid@email (Invalid address)
- bounced@old.com (Delivery failed)

📁 LOG FILE: output/logs/campaign_20240115_143022.json

═══════════════════════════════════════════════════════════════
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `.claude/scripts/send_campaign.py` | Send email campaigns (autonomous) |
| `.claude/scripts/sheets_reader.py` | Read Google Sheets data |
| `.claude/scripts/gmail_client.py` | Gmail API operations |
| `.claude/scripts/auth_setup.py` | Authentication setup |

## Campaign Execution Flags

| Flag | Purpose |
|------|---------|
| `--live` | Actually send emails |
| `--dry-run` | Simulate without sending |
| `--delay N` | Seconds between emails |
| `--max N` | Maximum emails to send |

## Environment Configuration

```env
EMAIL_DELAY_SECONDS=60    # Delay between emails
MAX_EMAILS_PER_BATCH=50   # Max per campaign
DAILY_EMAIL_LIMIT=100     # Daily limit
DRY_RUN_MODE=false        # Default mode
```

## Error Handling During Autonomous Execution

The campaign script handles errors gracefully:
- **Invalid email:** Skipped, logged, continues
- **Rate limited:** Pauses, retries
- **Network error:** Retries 3 times
- **Auth expired:** Attempts refresh

All errors logged to `output/logs/` for review after completion.

## Example Workflow

**User:** "Send cold emails to my leads sheet"

**Assistant:**
1. Creates TodoWrite task list
2. Checks authentication
3. Loads sheet and shows recipient count
4. Shows template preview
5. Presents complete summary
6. **Asks for approval ONCE**
7. After "yes" → Executes entire campaign autonomously
8. Reports final results when done

## Safety Measures

1. **Single approval** - User confirms once, clearly understanding scope
2. **Rate limiting** - Minimum 60s between emails (configurable)
3. **Daily limits** - Respects DAILY_EMAIL_LIMIT
4. **Full logging** - Every email logged for audit
5. **Dry run option** - Test first with `--dry-run`

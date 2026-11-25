---
name: weekly-planning-report
description: "Generate and EMAIL a comprehensive weekly planning report for the upcoming week. Reads Google Calendar for Mon-Fri, pulls account context from Salesforce and Logfood, sends a detailed HTML email with day-by-day schedule, account briefings, and action items, and optionally updates a shared Google Doc to-do list. Distinct from sa-planner (which outputs to terminal/doc, not email). Use when the user says 'email me a weekly prep report', 'send weekly planning email', 'weekly prep email with account briefings', 'email next week schedule', or wants a weekly briefing delivered via email."
user-invocable: true
---

# Weekly Planning Report

Generates and **emails** a comprehensive weekly planning report covering next week's meetings, account briefings, and to-do list management. Reads Google Calendar for Mon–Fri, pulls Salesforce UCO and Logfood spend data, sends a detailed HTML prep email with day-by-day schedule and account briefings, and optionally updates a shared Google Doc to-do list.

> **How this differs from `sa-planner`:** The `sa-planner` skill generates a terminal-based brief and updates a Google Doc interactively. This skill produces a **self-contained HTML email** with embedded day-by-day schedule tables, account briefing sections with UCO tables and spend data, and action items — designed for async consumption (e.g., scheduled to arrive Sunday evening so you're prepped Monday morning). Use `sa-planner` for interactive terminal planning; use this skill when you want an **email report** delivered to yourself or your team.

**Announce at start:** "I'm using the weekly-planning-report skill to build and email your weekly prep report."

## Quick Start

```
"Email me a weekly planning report for next week"
"Send a weekly prep email with account briefings and spend data"
"Weekly planning email — send to me and my manager, focus on Acme and GlobalCorp"
"Email next week's schedule with UCO context and action items"
```

## Prerequisites

Run all 3 auth checks in a single message as parallel Bash calls:

```bash
# Call 1 — Google auth
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
python3 "$GOOGLE_AUTH" token 2>/dev/null
```

```bash
# Call 2 — Salesforce auth
sf org display 2>/dev/null
```

```bash
# Call 3 — Logfood auth (for spend data)
databricks auth describe --profile logfood 2>/dev/null
```

If any auth fails, tell the user to run `/google-auth`, `/salesforce-authentication`, or `/databricks-authentication` (logfood profile) first. Continue with whichever sources are available — degrade gracefully.

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| **recipients** | Yes | Email addresses to send the weekly report to |
| **accounts** | No | Focus on specific accounts only (skip others) |
| **todo_doc_id** | No | Google Doc ID for shared to-do list (enables Step 7) |
| **uco_sheet_url** | No | Link to UCO tracking sheet (included in Quick Links bar) |

Parse these from the user's message. If `recipients` is not provided, ask for it before proceeding.

## Workflow

```
Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6 → Step 7 (optional)
Auth     Calendar   Classify   Account    Build      Send      Update
         Mon-Fri    & Detect   Context    HTML       Email     To-Do Doc
                    Issues                Email
```

### Step 1: Authenticate

Run the prerequisite auth checks above. Identify the user from their vibe profile:

```bash
cat ~/.vibe/profile 2>/dev/null
```

Extract `user.name`, `user.email`, `user.salesforce_id`. If the profile is missing, fall back to:

```bash
sf org display --json 2>/dev/null
```

### Step 2: Get Next Week's Events (Mon–Fri)

Fetch all calendar events for next week (Monday through Friday) using `gcal_builder.py` with `singleEvents=true` to expand recurring events.

```bash
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
TOKEN=$(python3 "$GOOGLE_AUTH" token)

GCAL_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-calendar/resources/gcal_builder.py 2>/dev/null | sort -V | tail -1)
```

Compute next week's Monday and Friday:

```bash
NEXT_MONDAY=$(python3 -c "
from datetime import datetime, timedelta
today = datetime.now()
days_until_monday = (7 - today.weekday()) % 7
if days_until_monday == 0:
    days_until_monday = 7
monday = today + timedelta(days=days_until_monday)
print(monday.strftime('%Y-%m-%dT00:00:00Z'))
")

NEXT_FRIDAY=$(python3 -c "
from datetime import datetime, timedelta
today = datetime.now()
days_until_monday = (7 - today.weekday()) % 7
if days_until_monday == 0:
    days_until_monday = 7
friday = today + timedelta(days=days_until_monday + 4)
print(friday.strftime('%Y-%m-%dT23:59:59Z'))
")

python3 "$GCAL_BUILDER" list \
  --time-min "$NEXT_MONDAY" \
  --time-max "$NEXT_FRIDAY" \
  --single-events true \
  --max-results 50
```

**Filter declined events:** Remove any event where the user's `responseStatus` is `"declined"`.

**Capture `htmlLink`** for every event — these are used to hyperlink meeting titles in the email.

### Step 3: Classify Events and Detect Issues

Classify each event into one of these categories:

| Category | Badge Color | Detection Rule |
|----------|-------------|----------------|
| **Customer** | `#1B7F37` green | Has non-`@databricks.com` attendees |
| **Internal** | `#0B5394` blue | All attendees are `@databricks.com` |
| **1:1** | `#6A329F` purple | Exactly 2 attendees |
| **Travel** | `#B45F06` orange | Title contains "flight", "travel", "airport", or location keywords |
| **PTO** | `#CC0000` red | Title contains "PTO", "OOO", "vacation", "out of office" |
| **Focus** | `#434343` gray | Title contains "focus time", "no meetings", "blocked" |

**Travel logistics detection:**
- If a flight event is found, calculate blocked windows: airport arrival 2 hours before departure, blocked through landing + 1.5 hours
- Flag any meetings that overlap with travel windows
- Check for hotel checkout times (morning meetings on travel days)

**PTO rules:**
- Half-day PTO: flag meetings during PTO hours only
- Full-day PTO: flag ALL meetings that day as conflicts

**Overlap detection:** Check all events across all types for time overlaps. Flag any pair of overlapping events.

### Step 4: Pull Account Context

For each account that has customer meetings next week, pull context from Salesforce and Logfood.

**Salesforce — Active UCOs (U1–U5):**

```bash
sf data query --query "SELECT Id, Name, Account__r.Name, Use_Case_Stage__c, Status__c, Next_Steps__c, Next_Steps_Date__c, Technical_Win__c, POC_Start_Date__c, POC_End_Date__c, (SELECT Id, Name, Status__c, Priority__c FROM Blockers__r WHERE Status__c != 'Closed') FROM UseCase__c WHERE Account__r.Name = '<ACCOUNT_NAME>' AND (OwnerId = '<USER_SF_ID>' OR Primary_Solution_Architect__c = '<USER_SF_ID>' OR Solution_Architect__c = '<USER_SF_ID>') AND Use_Case_Stage__c IN ('U1 - Identified','U2 - Evaluated','U3 - PoC/Testing','U4 - Production Approved','U5 - Scaled') ORDER BY Use_Case_Stage__c LIMIT 50" --json
```

Capture the UCO `Id` for each — these are used to build SFDC hyperlinks: `https://<instance>.lightning.force.com/lightning/r/UseCase__c/<Id>/view`

**Logfood — 30-day and 7-day spend:**

```sql
SELECT
  SUM(CASE WHEN date >= CURRENT_DATE - 30 THEN list_cost_dollars ELSE 0 END) AS last_30d_dollars,
  SUM(CASE WHEN date >= CURRENT_DATE - 7 THEN list_cost_dollars ELSE 0 END) AS last_7d_dollars
FROM main.fin_live_gold.daily_workspace_sku_aggregated
WHERE sfdc_account_id = '<ACCOUNT_ID>'
AND date >= CURRENT_DATE - 30
```

Run via the logfood profile:

```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json '{"warehouse_id": "<WAREHOUSE_ID>", "statement": "<SQL>", "wait_timeout": "30s"}'
```

**Match meetings to UCOs:** For each customer meeting, match it to relevant UCOs by keyword overlap between the meeting title/description and UCO names. Include matched UCOs in the meeting's Notes column.

### Step 5: Build HTML Email (Locked Format)

Build the email as a single HTML string. The template structure is locked — follow this exact layout:

#### Header Bar
Dark header bar (`background: #1B3A4B; color: white; padding: 16px 24px;`):
- Title: "Weekly Planning Report"
- Subtitle: week date range (e.g., "March 16–20, 2026")

#### Quick Links Bar
Light blue bar (`background: #E3F2FD; padding: 12px 24px;`):
- Link to To-Do List (if `todo_doc_id` provided): `https://docs.google.com/document/d/<todo_doc_id>/edit`
- Link to UCO Sheet (if `uco_sheet_url` provided)

#### Travel Banner (Conditional)
Yellow banner (`background: #FFF3CD; border-left: 4px solid #FFC107; padding: 12px 16px;`):
- Only shown if travel events are detected
- Summarize travel days, flight times, and blocked windows

#### At a Glance Grid
4-column summary grid (`display: grid; grid-template-columns: repeat(4, 1fr);`):

| Total Meetings | Customer Meetings | Busiest Day | Top Account Spend |
|----------------|-------------------|-------------|-------------------|
| Count of all events | Count of customer events | Day name + count | Account name + 30d spend |

#### Day-by-Day Schedule (Mon–Fri)

For each day, render:

**Day header bar** (`background: #1B3A4B; color: white; padding: 8px 16px;`):
- Day name and date (e.g., "Monday, March 16")

**Schedule table** (`width: 100%; border-collapse: collapse;`):

| Time | Meeting | Type | Notes |
|------|---------|------|-------|
| 9:00 AM | [Meeting Title](htmlLink) | `<badge>` | UCO links, conflict warnings |

- **Meeting titles** are hyperlinked to Google Calendar using the event's `htmlLink`
- **Type badges** use the colors from Step 3 classification:
  - Customer: `background: #1B7F37; color: white; padding: 2px 8px; border-radius: 4px;`
  - Internal: `background: #0B5394; color: white;`
  - 1:1: `background: #6A329F; color: white;`
  - Travel: `background: #B45F06; color: white;`
  - PTO: `background: #CC0000; color: white;`
  - Focus: `background: #434343; color: white;`
- **Notes column:**
  - For customer meetings: UCO links (`<a href="https://<instance>.lightning.force.com/lightning/r/UseCase__c/<Id>/view">UCO Name (Stage)</a>`)
  - For conflicts: `<span style="color: #CC0000; font-weight: bold;">⚠ Overlaps with [other meeting]</span>`
  - For travel conflicts: `<span style="color: #B45F06;">✈ Travel window — may need to reschedule</span>`

#### Account Briefings

For each account with customer meetings, render a briefing section:

**Account header** (`background: #F5F5F5; padding: 12px 16px; border-left: 4px solid #1B7F37;`):
- Account name
- 30-day spend + 7-day spend

**Meetings subsection:**
- List of meetings for this account next week (with day, time, title)

**Spend subsection:**
- 30-day and 7-day spend figures
- Trend indicator (↑ growing, ↓ declining, → stable)

**UCO Table:**

| UCO Name | Stage | Next Steps | Next Steps Date | Related Meeting | Blockers |
|----------|-------|------------|-----------------|-----------------|----------|
| [Name](sfdc_link) | U3 | ... | 3/18 | Tuesday 2pm call | 1 open |

- UCO names hyperlinked to Salesforce
- **Related Meeting** column: shows which meeting next week maps to this UCO

**Talking Points:**
- Generate 2–3 talking points based on UCO status, spend trends, and upcoming meetings
- If a UCO has overdue next steps, flag it
- If spend is declining, suggest a check-in topic

#### Action Items

Numbered list of recommended actions for the week:
1. Prep-related actions (meetings needing agendas, decks)
2. UCO follow-ups (overdue next steps, blockers to escalate)
3. Account outreach (declining spend, stalled UCOs)

#### Footer

Light gray footer (`background: #F5F5F5; padding: 12px 24px; font-size: 12px; color: #666;`):
- "Generated by Weekly Planning Report skill"
- Timestamp
- Data sources used (Calendar, Salesforce, Logfood)
- Any gaps (e.g., "Logfood unavailable — spend data not included")

### Step 6: Send Email

Send the HTML email using `gmail_builder.py`:

```bash
GMAIL_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py 2>/dev/null | sort -V | tail -1)
```

Write the HTML to a temp file and send:

```bash
python3 "$GMAIL_BUILDER" send \
  --to "<RECIPIENTS>" \
  --subject "Weekly Planning Report — <WEEK_DATE_RANGE>" \
  --html-file /tmp/weekly_planning_report.html
```

If `gmail_builder.py` doesn't support `--html-file`, use `--body-html` with the file content, or use the raw Gmail API as a last resort:

```bash
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
TOKEN=$(python3 "$GOOGLE_AUTH" token)

python3 << 'PYEOF'
import base64, json, urllib.request, os

token = os.environ.get("TOKEN") or open("/tmp/gauth_token.txt").read().strip()
html = open("/tmp/weekly_planning_report.html").read()
recipients = "<RECIPIENTS>"
subject = "Weekly Planning Report — <WEEK_DATE_RANGE>"

raw = f"To: {recipients}\r\nSubject: {subject}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html}"
body = json.dumps({"raw": base64.urlsafe_b64encode(raw.encode()).decode()}).encode()

req = urllib.request.Request(
    "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
    data=body,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST"
)
resp = urllib.request.urlopen(req)
print(json.loads(resp.read()))
PYEOF
```

Before running, export the token: `export TOKEN=$(python3 "$GOOGLE_AUTH" token)`

Confirm to the user: "Weekly planning report sent to <recipients>."

### Step 7: Update To-Do Doc (Optional)

**Only run if `todo_doc_id` is provided.** This step intelligently updates a shared Google Doc to-do list.

#### 7A: Read Current Doc

```bash
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)
TOKEN=$(python3 "$GOOGLE_AUTH" token)

curl -s "https://docs.googleapis.com/v1/documents/<TODO_DOC_ID>" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Parse the document structure. Identify:
- Existing sections (by heading text)
- Checked items (strikethrough or `☑` prefix)
- Unchecked items (`☐` or `- [ ]` prefix)

#### 7B: Archive Completed Items

For items that are checked/completed:
- Apply strikethrough formatting if not already present
- Move to an "Archive" section at the bottom of the doc
- Prefix with completion date: `[3/15] ☑ Original task text`

#### 7C: Merge New Tasks

Generate new tasks from the weekly report data:
- Meeting prep tasks (from Step 3 — meetings needing agendas)
- UCO follow-up tasks (from Step 4 — overdue next steps, open blockers)
- Account outreach tasks (from Step 4 — declining spend, stalled UCOs)

**Deduplication:** Before adding a new task, check if a similar task already exists in the doc (fuzzy match on account name + action verb). Skip duplicates.

**Merge into existing sections:**
- Match tasks to existing topic sections by account name or category
- If no matching section exists, create one

**Add hyperlinks:**
- Meeting-related tasks: link to Google Calendar event (`htmlLink`)
- UCO-related tasks: link to Salesforce UCO record

#### 7D: Document Structure

Maintain this section order in the to-do doc:

1. **General / Learning** — non-account-specific tasks, training, certifications
2. **Customer sections** (one per account, alphabetical) — account-specific tasks
3. **Admin** — internal tasks, expense reports, timecards
4. **Archive** — completed items with completion dates

Each section uses a Heading 2. Tasks within sections are bulleted lists with `☐` / `☑` prefixes.

#### 7E: Confirm and Write Updates

**Before writing any changes, present a summary to the user and wait for approval:**

```
To-do doc changes pending:
  - Archive: N completed items → Archive section
  - Add: M new tasks (list them)
  - Sections affected: [list sections]

Proceed with updating the to-do doc? (yes/no)
```

Only after the user confirms, apply the batch update:

```bash
curl -s -X POST "https://docs.googleapis.com/v1/documents/<TODO_DOC_ID>:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -d '<BATCH_UPDATE_JSON>'
```

Confirm to the user: "To-do doc updated — archived N completed items, added M new tasks."

**Detecting scheduled (non-interactive) mode:** If the skill is invoked via `claude --print` (which is how `fe-macos-scheduler` runs skills), there is no interactive user to confirm with. In this case, skip the confirmation prompt and proceed automatically. The email report will include a summary of to-do doc changes made. You can detect non-interactive mode by checking if `--print` or `--dangerously-skip-permissions` flags are present in the invocation context.

## Scheduling

This skill can be scheduled to run automatically every Sunday evening using the `fe-macos-scheduler` plugin:

```
Schedule weekly-planning-report to run every Sunday at 6pm — send to me@databricks.com
```

This uses `macos-scheduler` to create a launchd job that triggers the skill on a weekly cadence, so the prep email is waiting in your inbox Monday morning.

## Cross-References

- `/sa-planner` — daily/weekly todo and prioritized brief (proactive signals, not email-based)
- `/customer-meeting-prep` — deep-dive prep for individual meetings flagged in the report
- `/google-calendar` — direct calendar operations
- `/gmail` — direct email operations
- `/salesforce-actions` — update UCO next steps or create new UCOs
- `/logfood-querier` — ad-hoc consumption queries
- `/uco-blockers` — manage blocker lifecycle on flagged UCOs

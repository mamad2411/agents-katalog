---
name: daily-meeting-prep
description: "Generate and EMAIL a daily meeting prep brief for tomorrow. Reads Google Calendar, classifies meetings (customer/internal/1:1/travel/PTO), detects conflicts and travel logistics, pulls Salesforce UCO context, and sends a formatted HTML email to specified recipients. Distinct from sa-planner (which outputs to terminal/doc, not email). Use when the user says 'email me tomorrow prep', 'send daily prep email', 'daily meeting prep email', 'email me what I have tomorrow', or wants a daily briefing delivered via email."
user-invocable: true
---

# Daily Meeting Prep

Generates and **emails** a concise daily prep brief covering tomorrow's meetings with account context, conflict detection, and travel logistics. Reads Google Calendar, classifies each meeting, pulls Salesforce UCO context for customer meetings, and sends a formatted HTML email to specified recipients.

> **How this differs from `sa-planner`:** The `sa-planner` skill generates a terminal-based brief and updates a Google Doc. This skill produces a **self-contained HTML email** with embedded schedule tables, type badges, customer context boxes, and travel/conflict alerts — designed for async consumption (e.g., scheduled to arrive in your inbox every evening). Use `sa-planner` for interactive terminal planning; use this skill when you want an **email** delivered to yourself or your team.

**Announce at start:** "I'm using the daily-meeting-prep skill to build and email your daily briefing."

## Quick Start

```
"Email me a daily prep brief for tomorrow"
"Send me a daily meeting prep email with customer context"
"Daily prep email for tomorrow, send to [email protected]"
"Email tomorrow's schedule to the account team"
"Send daily prep email for Acme and GlobalCorp accounts"
```

## Prerequisites

1. **Google Auth** — Required. Invoke `google-auth` skill if not already authenticated. Needed for Calendar read and Gmail send.
2. **Salesforce Auth** — Optional. Invoke `salesforce-authentication` skill if the user wants customer UCO context. Skip gracefully if unavailable.

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| **recipients** | Yes | Email addresses to send the prep to. If not provided, ask the user. |
| **accounts** | No | List of account names to pull UCO context for. If omitted, auto-detect from meeting titles/attendees. |
| **todo_doc_id** | No | Google Doc ID for a to-do list. If provided, include a link in the email footer. |

## Workflow

### Step 1: Authenticate

1. Invoke `google-auth` skill to ensure Google Calendar + Gmail access.
2. If the user wants customer context, invoke `salesforce-authentication` skill. If Salesforce auth fails, continue without UCO data — note this in the email.

### Step 2: Get Tomorrow's Events

Use `gcal_builder.py` from the `google-calendar` skill resources:

```bash
GCAL_BUILDER="$(find ~/.claude/plugins/cache -path '*/google-calendar/resources/gcal_builder.py' | head -1)"
```

Fetch tomorrow's events:

```bash
python3 "$GCAL_BUILDER" list \
  --start "YYYY-MM-DDT00:00:00Z" \
  --end "YYYY-MM-DDT23:59:59Z" \
  --max-results 50
```

Where `YYYY-MM-DD` is tomorrow's date.

**Weekend handling:** If tomorrow is Saturday, skip to Monday. If tomorrow is Sunday, skip to Monday. Announce the adjusted date.

**Filter declined events:** For each event, check the current user's `responseStatus` in the `attendees` array. Exclude events where `responseStatus` is `"declined"`.

**Capture `htmlLink`** for every event — this is used to hyperlink meeting names in the email.

### Step 3: Classify Meetings

Classify each event into exactly one type using these rules (evaluated in order):

| Type | Rule |
|------|------|
| **PTO/OOO** | Title contains "PTO", "OOO", "Leave", "Holiday", "Vacation" (case-insensitive) |
| **Travel/Flight** | Title contains "Flight", "Travel", "Airport", "Depart", "Arrive" (case-insensitive) |
| **Focus Time** | No attendees, or title contains "Focus", "Block", "DNS", "Do Not Schedule" (case-insensitive) |
| **1:1** | Exactly 2 attendees (including the user) |
| **Customer** | Any attendee has a non-`@databricks.com` domain, OR title mentions a known account name |
| **Internal** | All attendees are `@databricks.com` |

**Travel logistics detection:**

When a Travel/Flight event is found:
1. **Airport arrival time** = flight departure time minus 2 hours
2. **Blocked window** = airport arrival time through landing time + 1.5 hours for transit
3. If landing time is not in the event, estimate: departure + 3 hours domestic, + 6 hours international
4. **Flag every other meeting that overlaps** with the blocked travel window — these go into the "Heads Up" section

**Conflict detection:**

Flag any two non-Focus, non-PTO events whose time ranges overlap.

### Step 4: Pull Account Context (Customer Meetings Only)

Skip this step entirely if:
- There are no Customer-type meetings
- Salesforce auth is unavailable

For each Customer meeting:

1. **Identify the account name** from meeting title, attendee domains, or the user-provided `accounts` list.
2. **Query Salesforce UCOs** for matched accounts:
   ```bash
   sf data query --query "SELECT Id, Name, Stage__c, Next_Steps__c, Use_Case_Owner__r.Name FROM Use_Case_Object__c WHERE Account__r.Name LIKE '%ACCOUNT_NAME%' AND Stage__c NOT IN ('U6 - Live', 'Closed - Lost') ORDER BY LastModifiedDate DESC LIMIT 5" --json
   ```
3. **Build SFDC hyperlinks** for each UCO:
   ```
   https://databricks.lightning.force.com/lightning/r/Use_Case_Object__c/{Id}/view
   ```
4. **Match meetings to UCOs** by keyword overlap between meeting title/description and UCO Name.

### Step 5: Build HTML Email

**CRITICAL: The email template below is locked. Do not modify the structure, colors, or layout. Only populate the dynamic content.**

The email has these sections in order:

#### 5a. Header Bar

```html
<div style="background:#1B3A4B;color:#fff;padding:16px 24px;border-radius:8px 8px 0 0;font-size:20px;font-weight:600;">
  📅 Daily Prep — {WEEKDAY}, {MONTH} {DAY}, {YEAR}
</div>
```

#### 5b. Travel / PTO Banner (conditional)

Only include if there are Travel or PTO events. Yellow background for travel, grey for PTO:

```html
<div style="background:#FFF3E0;padding:12px 24px;border-left:4px solid #FF6F00;margin:12px 24px;">
  ✈️ <strong>Travel day</strong> — {flight summary}. Blocked window: {start}–{end}.
</div>
```

#### 5c. Quick Stats Row

Three-column summary:

```html
<table style="width:100%;margin:12px 24px;"><tr>
  <td style="text-align:center;padding:8px;background:#F5F5F5;border-radius:4px;width:33%;">
    <div style="font-size:24px;font-weight:700;">{N}</div><div style="font-size:12px;color:#666;">Meetings</div>
  </td>
  <td style="text-align:center;padding:8px;background:#F5F5F5;border-radius:4px;width:33%;">
    <div style="font-size:24px;font-weight:700;">{TIME}</div><div style="font-size:12px;color:#666;">First Meeting</div>
  </td>
  <td style="text-align:center;padding:8px;background:#F5F5F5;border-radius:4px;width:33%;">
    <div style="font-size:24px;font-weight:700;">{TIME}</div><div style="font-size:12px;color:#666;">Last Meeting</div>
  </td>
</tr></table>
```

#### 5d. Schedule Table

```html
<table style="width:100%;border-collapse:collapse;margin:12px 24px;">
  <tr style="background:#F5F5F5;">
    <th style="padding:8px;text-align:left;width:15%;">Time</th>
    <th style="padding:8px;text-align:left;width:40%;">Meeting</th>
    <th style="padding:8px;text-align:center;width:15%;">Type</th>
    <th style="padding:8px;text-align:left;width:30%;">Notes</th>
  </tr>
  <!-- One row per event -->
  <tr style="border-bottom:1px solid #eee;">
    <td style="padding:8px;">{start_time}–{end_time}</td>
    <td style="padding:8px;"><a href="{htmlLink}" style="color:#1B73E8;text-decoration:none;">{title}</a></td>
    <td style="padding:8px;text-align:center;"><span style="background:{badge_color};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;">{type}</span></td>
    <td style="padding:8px;font-size:13px;color:#555;">{notes}</td>
  </tr>
</table>
```

**Type badge colors:**

| Type | Color |
|------|-------|
| Customer | `#FF6F00` |
| Internal | `#1B73E8` |
| 1:1 | `#7B1FA2` |
| Travel | `#00A972` |
| PTO/OOO | `#9E9E9E` |
| Focus | `#607D8B` |

**Notes column content:**
- Customer meetings: matched UCO name + stage, or attendee company
- 1:1 meetings: the other person's name
- Travel: blocked window info
- Conflicts: "⚠️ Conflicts with {other meeting}"

#### 5e. Customer Context Box (conditional)

Only include if there are Customer meetings with UCO data:

```html
<div style="background:#FFF8E1;border:1px solid #FFD54F;border-radius:8px;padding:16px;margin:12px 24px;">
  <div style="font-weight:600;margin-bottom:8px;">🏢 Customer Context</div>
  <!-- Per account -->
  <div style="margin-bottom:12px;">
    <strong>{Account Name}</strong><br/>
    <ul style="margin:4px 0;padding-left:20px;">
      <li><a href="{sfdc_link}">{UCO Name}</a> — {Stage} — {Next Steps (truncated to 80 chars)}</li>
    </ul>
  </div>
</div>
```

#### 5f. Heads Up Box (conditional)

Only include if there are conflicts, travel overlaps, or action items:

```html
<div style="background:#FFEBEE;border:1px solid #EF9A9A;border-radius:8px;padding:16px;margin:12px 24px;">
  <div style="font-weight:600;margin-bottom:8px;">⚠️ Heads Up</div>
  <ul style="margin:4px 0;padding-left:20px;">
    <li>{conflict or action description}</li>
  </ul>
</div>
```

Items to include:
- Time conflicts between meetings
- Meetings during travel blocked windows
- Back-to-back meetings with no gap (< 5 min between end and start)
- Customer meetings with no UCO match (suggest creating one)

#### 5g. Footer

```html
<div style="padding:12px 24px;font-size:12px;color:#999;border-top:1px solid #eee;margin-top:12px;">
  Generated by Vibe daily-meeting-prep • {timestamp}
  <!-- If todo_doc_id provided -->
  <br/><a href="https://docs.google.com/document/d/{todo_doc_id}" style="color:#1B73E8;">📝 Open To-Do List</a>
</div>
```

### Step 6: Send Email

Use `gmail_builder.py` from the `gmail` skill resources:

```bash
GMAIL_BUILDER="$(find ~/.claude/plugins/cache -path '*/gmail/resources/gmail_builder.py' | head -1)"
```

Send the HTML email:

```bash
python3 "$GMAIL_BUILDER" send \
  --to "{recipients}" \
  --subject "📅 Daily Prep — {WEEKDAY}, {MONTH} {DAY}" \
  --body-html /tmp/daily_prep_email.html
```

Write the full HTML to `/tmp/daily_prep_email.html` before sending.

**Confirm with the user before sending** — show a summary of what will be sent (recipient, meeting count, any flags) and wait for approval.

## Scheduling

This skill can be automated to run daily using the `fe-macos-scheduler` plugin:

```
Schedule daily-meeting-prep to run at 6 PM Monday through Thursday
```

The scheduler will invoke this skill with saved parameters. Weekends and Fridays are automatically skipped (no prep needed for Saturday).

## Error Handling

- **No events tomorrow:** Send a short "All clear" email instead of an empty schedule.
- **Calendar API failure:** Report the error and suggest re-running `google-auth`.
- **Salesforce unavailable:** Continue without UCO context; note in the email that customer context was unavailable.
- **Gmail send failure:** Save the HTML to `/tmp/daily_prep_email.html` and provide the path so the user can send manually.

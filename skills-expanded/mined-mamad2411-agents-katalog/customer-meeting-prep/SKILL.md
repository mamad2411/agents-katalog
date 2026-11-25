---
name: customer-meeting-prep
description: Generate a tailored prep doc for an upcoming customer meeting. Classifies the call type from the event title, pulls Salesforce account and contact context, and creates a formatted Google Doc with a Google Task reminder. Use when preparing for a customer call, demo, QBR, POC check-in, or discovery session. Do NOT use for executive messaging coaching, talk tracks, Challenger narrative prep, objection handling, or meeting roleplay — use exec-messaging-coach instead.
context: fork
agent: general-purpose
---

# Customer Meeting Prep

Generates a context-aware prep doc for a single upcoming customer meeting. Pulls Salesforce data, formats the doc to the call type, saves it to Google Drive, and creates a Google Task reminder with the direct link.

## Rules

- **Output:** Show short progress labels before each stage ("Checking calendar...", "Pulling Salesforce context...", "Creating prep doc..."). Never show raw API responses, folder IDs, or auth tokens. Errors only surface if user action is needed.
- **No menus:** All interaction is natural language. Parse free-form responses. Ask multiple fields in one question to minimize back-and-forth.
- **Config:** Drive folder ID is stored in `~/.vibe/customer-meeting-prep/config.json`. On first use, ask for the folder URL, extract the ID, and save it.

## Configuration

**Config file:** `~/.vibe/customer-meeting-prep/config.json`

```json
{
  "drive_folder_id": "FOLDER_ID_HERE",
  "drive_folder_name": "Customer Meeting Prep",
  "drive_folder_url": "https://drive.google.com/drive/folders/FOLDER_ID_HERE"
}
```

On first use: ask "Where should I save prep docs? Paste a Google Drive folder URL." Extract the folder ID from the URL and write the config file.

## Initialization

Read config silently. Output the splash screen:

```
customer-meeting-prep — [folder_name](folder_url)

Which meeting are you prepping for? You can describe it ("my 2pm with Acme"), say "next" for your next customer meeting, or say "calendar" to pick from today's events.
```

If not configured: `customer-meeting-prep — No folder configured`

## Workflow

### Phase 1: Identify the Meeting

**If user says "calendar":**
1. Run: `python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-calendar/resources/gcal_builder.py list --max-results 20`
2. Filter for events with non-@databricks.com attendees
3. Present as a numbered text list:
   ```
   Today's customer meetings:
   1. 2:00 PM - Acme Technical Review (john@acme.com, fabien@databricks.com)
   2. 4:00 PM - XSOLIS Check-in (mcowan@xsolis.com)
   Which one?
   ```
4. Extract: event title, start/end time, attendee emails, calendar URL

**If user says "next":**
- Run the same list, pick the next upcoming event with external attendees

**If user describes a meeting:**
- Parse customer name and time from the description
- Run `gcal_builder.py search --query "CUSTOMER_NAME"` to find the matching event
- Confirm with the user if ambiguous

**Extract from the event:**
- `summary`: event title
- `start` / `end`: datetime
- `attendees`: all email addresses
- `htmlLink`: calendar URL
- Customer name: from the non-@databricks.com domain, or from the event title
- Duration in minutes

### Phase 2: Classify Call Type

Match keywords in the event title (case-insensitive):

| Call Type | Keywords |
|-----------|----------|
| intro | intro, introduction, first call, meet & greet, kickoff |
| demo | demo, demonstration, showcase |
| poc_checkin | poc check-in, poc sync, poc status, poc update |
| poc_planning | poc planning, poc kickoff, poc scope, poc setup |
| arch_review | architecture review, arch review, design review, technical review |
| tech_discovery | technical discovery, discovery call, requirements, scoping |
| office_hours | office hours, check-in, check in, catchup, catch-up, casual sync |
| qbr | qbr, business review, quarterly review, ebr |
| general | (default) |

### Phase 3: Gather Context

#### 3a: Salesforce

Use `fe-salesforce-tools:salesforce-actions` to look up the account. What to fetch depends on call type:

| Section | Call Types |
|---------|-----------|
| Account overview (tier, industry, AE/SE, use cases) | intro, demo, poc_planning, arch_review, tech_discovery, qbr, general |
| Attendee profiles (title, role from Salesforce contacts) | intro, demo, poc_planning, arch_review, tech_discovery |
| Recent activity (last 7 days of notes/tasks) | intro, poc_checkin, poc_planning, arch_review, tech_discovery, office_hours, qbr, general |

Show progress: "Pulling Salesforce context..."

If Salesforce lookup fails for any section, leave a `—` placeholder and continue.

#### 3b: LinkedIn Enrichment (attendee profiles only)

For call types that include attendee profiles (`intro`, `demo`, `poc_planning`, `arch_review`, `tech_discovery`), attempt to enrich each **customer** attendee using the LinkedIn MCP.

**Check availability first:** Try calling `mcp__linkedin__search_people(keywords="test")`. If the tool is unavailable (error, tool not found, or not listed), show the user:

```
LinkedIn MCP not detected. To enable attendee profile enrichment, add the following
to the "mcpServers" section of your ~/.claude.json and restart Claude Code:

  "linkedin": {
    "type": "stdio",
    "command": "uvx",
    "args": ["linkedin-scraper-mcp"],
    "env": {}
  }

Continuing without LinkedIn enrichment — attendee profiles will use Salesforce data only.
```

Then continue without LinkedIn. Do not block or re-prompt.

**If LinkedIn is available:**

1. For each customer attendee (non-@databricks.com), derive their name from Salesforce contact data or from their email (e.g. `john.smith@acme.com` → "John Smith").
2. Search: `mcp__linkedin__search_people(keywords="First Last Company")`
3. If a match is found, fetch: `mcp__linkedin__get_person_profile(linkedin_username, sections="experience")`
4. Use the data to confirm title/company and add a brief 1-2 sentence background note to the attendee row.

Show progress: "Enriching attendee profiles via LinkedIn..."

If a lookup returns no match or errors on a specific person, silently skip that person and use Salesforce data.

### Phase 4: Generate and Save Prep Doc

**Progress labels:**
```
Creating prep doc...
Uploading to Drive...
```

**Step 1:** Write the populated markdown to `/tmp/prep_[customer_slug]_[datetime].md` using the appropriate template from the reference file `resources/PREP_DOC_TEMPLATES.md`.

**Step 2:** Get auth token:
```bash
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
```

**Step 3:** Create the Google Doc in the configured Drive folder:
```bash
DOC_ID=$(curl -s -X POST "https://www.googleapis.com/drive/v3/files?supportsAllDrives=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Prep: CUSTOMER - MEETING_TITLE - DATE\", \"mimeType\": \"application/vnd.google-apps.document\", \"parents\": [\"FOLDER_ID\"]}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

**Step 4:** Populate with content:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/prep_[customer_slug]_[datetime].md \
  --doc-id "$DOC_ID"
```

#### Data Sources Footer

At the bottom of the generated prep doc, append a "Data Sources" section listing the status of each source used:

```
---
**Data Sources**
- Calendar: OK
- Salesforce: OK / Failed (reason)
- LinkedIn: OK / Skipped (MCP not configured) / Failed (reason)
```

Track success/failure for each source as you execute Phases 1-3. This helps the reader understand if any sections are incomplete and why.

### Phase 5: Create Google Task Reminder

Create a Google Task due on the meeting date so it appears in Google Calendar:

```bash
curl -s -X POST "https://tasks.googleapis.com/tasks/v1/lists/@default/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Review prep: CUSTOMER - CALL_TYPE - HH:MM AM/PM\",
    \"notes\": \"https://docs.google.com/document/d/DOC_ID/edit\",
    \"due\": \"MEETING_DATE_RFC3339\"
  }"
```

`MEETING_DATE_RFC3339` is the meeting date at midnight UTC, e.g. `2026-02-26T00:00:00.000Z`.

### Phase 6: Confirm

Output:
```
Prep doc ready for CUSTOMER — CALL_TYPE
MEETING_TITLE  |  HH:MM AM/PM  |  X min

[Open prep doc](https://docs.google.com/document/d/DOC_ID/edit)

Google Task reminder added for today/DATE.
```

## Examples

```
User: /customer-meeting-prep
Agent: customer-meeting-prep — Customer Meeting Prep

       Which meeting are you prepping for? Describe it, say "next", or say "calendar".

User: calendar

Agent: Today's customer meetings:
       1. 2:00 PM - XSOLIS Check-in (mcowan@xsolis.com, fabien@databricks.com)
       Which one?

User: 1

Agent: Checking calendar...
       Pulling Salesforce context...
       Creating prep doc...
       Uploading to Drive...

       Prep doc ready for XSOLIS — office_hours
       XSOLIS Check-in  |  2:00 PM  |  30 min

       [Open prep doc](https://docs.google.com/document/d/...)

       Google Task reminder added for today.
```

```
User: prep me for my 3pm demo with Databricks at Skyworks
Agent: Checking calendar...
       Pulling Salesforce context...
       Creating prep doc...
       ...
```

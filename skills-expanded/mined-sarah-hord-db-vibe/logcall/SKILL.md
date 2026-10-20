---
name: logcall
description: Log customer meeting notes with automatic calendar and Salesforce data. Saves as Google Docs in customer folders. Use when logging calls, recording meeting notes, documenting customer meetings, or capturing action items.
context: fork
agent: general-purpose
---

# Capture Meeting Notes

Captures structured meeting notes from customer calls, saves as Google Docs in customer folders, and enriches with Salesforce and attendee data in the background.

## Capabilities

- Log meeting notes from natural language input or Google Calendar events
- Create formatted Google Docs with Databricks brand styling in correct customer folder on shared Google Drive
- Enrich documents with Salesforce account data and attendee titles/emails in the background
- Cache customer folders and employee data for faster repeat usage

## Rules

- **Output:** Show short progress labels before each stage (e.g., "Searching for Teradata folder..."). Never show raw API responses, curl output, folder IDs, or auth tokens. Never narrate cache hits, subfolder creation, or Drive API params. Errors only surface if user action is needed. Background enrichment completion gets one line: "Background data added to document."
- **Interaction:** All user interaction is natural language — never use AskUserQuestion menus. Ask questions as plain text and parse free-form responses. Collect multiple fields per question to minimize back-and-forth.
- **Tense:** The meeting may be past or upcoming. Use neutral phrasing ("the meeting", "who's attending") — not past tense. Date defaults to today unless specified.

## Configuration

**Config file:** `~/.claude/fe-meeting-notes/config.json`

On first use, if no config exists, ask for the root customer folder (Google Drive URL), extract the folder ID, resolve the folder name from the Drive API (see below), and save it. The user can edit the config file directly at any time.

### Resolving Folder Name from Drive API

When you have a folder ID (extracted from a Google Drive URL), resolve the human-readable folder name via the Drive API instead of asking the user to type it:

```bash
TOKEN=$(python3 <google-auth>/resources/google_auth.py token)
FOLDER_NAME=$(curl -s "https://www.googleapis.com/drive/v3/files/<folder_id>?fields=name&supportsAllDrives=true" \
  -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng" | jq -r '.name')
```

Pass `$FOLDER_NAME` to `config_manager.py setup`. If the API call fails or returns null, fall back to using the folder ID as the display name.

## Initialization

When invoked, read the config file silently via Bash to get `root_customer_folder_name` and `root_customer_folder_url`.

**Auto-repair:** If `root_customer_folder_name` is empty or missing but `root_customer_folder_id` exists, resolve the folder name from the Drive API (see above), update the config via `config_manager.py setup`, and use the resolved name for the splash screen.

Output the splash screen and opening question in a single response and highlight line in blue:

```
logcall v1.2.1 — [<folder_name>](<folder_url>)
Have feedback? Slack #logcall-feedback

Tell me about the meeting — customer, topic, Databricks attendees, customer attendees.
Example: "Sandisk, Architecture for infosec use-cases, Sriram J and I, customer side Chris Eager."
Say "calendar" to retrieve this info from a meeting invite.
```

If not configured: `logcall v1.2.1 — No customer folder configured`

## Workflow

```
Phase 1 ──> Phase 2 ──────> Phase 4
            Create Doc       Update Doc
                |                ^
                └─> Phase 3 ────┘
                    Enrichment
                    (background)
```

### Phase 1: Gather Meeting Details

Parse the user's response to extract: **customer name** (required), **meeting topic** (required), **Databricks attendees** (required — default to user if not mentioned), **customer attendees** (optional — ask if ambiguous).

**If user says "calendar":**
1. Use `fe-google-tools:google-calendar` to list today's events
2. Present as a numbered text list (NOT a menu):
   ```
   Here are today's meetings:
   1. 9:00 AM - Skyworks Q1 Review (sarah@skyworks.com, sriram@databricks.com)
   2. 11:00 AM - Acme Technical Deep Dive (john@acme.com)
   Which one?
   ```
3. Extract date, topic, and attendee emails from the selected event
4. Identify customer from non-Databricks attendee domains

**If user provides details directly:**
- All required fields present → proceed immediately, no follow-ups
- Any missing → one plain-text follow-up covering all missing fields
- For calendar meetings: email addresses available from event
- For direct input: store names only (email lookup deferred to Phase 3)

### Phase 2: Create Document

> **Before starting**, launch Phase 3 (Validating and Enriching Document) as a background Task agent with `run_in_background: true`. Customer name and attendee list are already known, so enrichment runs concurrently with doc creation. Save the task ID for Phase 4.

> **Shared Drive:** ALL Drive API calls must include `supportsAllDrives=true`. For list/search, also include `includeItemsFromAllDrives=true`. Without this, the API silently returns empty results.

**Progress labels to show the user:**
```
Searching for <Customer> folder...
Creating meeting notes doc...
Applying formatting...
Opening in browser...
```

**Steps:**

1. If no config exists, run first-time setup (ask for root folder URL, resolve folder name from Drive API, save config)
2. Search for customer folder within `root_customer_folder_id`
   - Multiple matches → numbered text list, ask which one
   - No match → "No folder found for [Customer]. Paste a Drive URL or I'll create one."
3. Check/create `meeting-log/` subdirectory

4. **Read and populate template** from `references/template.md`:
   - `{{DATE}}` → meeting date (YYYY-MM-DD)
   - `{{CUSTOMER}}` → customer name
   - `{{TOPIC}}` → meeting topic
   - `{{DATABRICKS_ATTENDEES}}` → bullet list: `- Name` (ad-hoc) or `- Name <email>` (calendar)
   - `{{CUSTOMER_ATTENDEES}}` → same format
   - No placeholder text — background enrichment adds details later

5. **Step A — Create empty doc** in `meeting-log/` via Drive API:
   ```bash
   TOKEN=$(python3 <google-auth>/resources/google_auth.py token)
   DOC_ID=$(curl -s -X POST "https://www.googleapis.com/drive/v3/files?supportsAllDrives=true" \
     -H "Authorization: Bearer $TOKEN" -H "x-goog-user-project: gcp-sandbox-field-eng" \
     -H "Content-Type: application/json" \
     -d '{"name": "Meeting Notes - Customer - YYYY-MM-DD - Topic", "mimeType": "application/vnd.google-apps.document", "parents": ["FOLDER_ID"]}' | jq -r '.id')
   ```

6. **Step B — Populate with formatted content** via `markdown_to_gdocs.py` from `fe-google-tools:google-docs`:
   ```bash
   python3 <google-docs>/resources/markdown_to_gdocs.py --doc-id "$DOC_ID" --input /tmp/logcall_notes.md
   ```

7. **Step C — Apply Databricks brand styles:**
   ```bash
   python3 <logcall>/resources/apply_databricks_styles.py --doc-id "$DOC_ID" --token "$TOKEN"
   ```

   **Token reuse:** Fetch token once at step 5 and reuse for folder search, doc creation, and styling. `markdown_to_gdocs.py` manages its own auth. Phase 4 must always fetch a fresh token (the background agent may take >45 min, so the Phase 2 token will have expired).

8. **Open in browser:** `open "<document-url>"`

9. **Confirm** (include link, save location):
   ```
   Meeting notes created and opened in your browser.
   Salesforce data and attendee details are loading in the background.
   Saved to: <customer>/meeting-log/
   ```

### Phase 3: Validating and Enriching Document

**This runs as the background Task agent launched at the start of Phase 2.**

**Important:** Use a **single `fe-internal-tools:logfood-querier` invocation** for both lookups below. Run 3a first, then 3b in the same session. This avoids ~2-3s overhead of loading the skill twice.

#### 3a: Salesforce Account Lookup

```sql
SELECT a.Id, a.Name, a.OwnerId, u.Name AS OwnerName
FROM main.sfdc_bronze.account a
LEFT JOIN main.sfdc_bronze.user u ON a.OwnerId = u.Id
  AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
WHERE a.Name = '<customer_name>'
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
LIMIT 5
```

If no results, retry with `WHERE a.Name LIKE '%<customer_name>%'` (LIMIT 10). Pick best match by name similarity. Retrieve: account name, account ID, owner name.

If lookup fails: leave `—` placeholders (clean, intentional appearance).

#### 3b: Databricks Attendee Lookup

Run a **single batched query** for all Databricks attendees (not one per attendee):

```sql
-- Calendar meetings (have emails):
SELECT Name, Email, Title FROM main.sfdc_bronze.user
WHERE Email IN ('alice@databricks.com', 'bob@databricks.com')
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)

-- Ad-hoc calls (have names):
SELECT Name, Email, Title FROM main.sfdc_bronze.user
WHERE (Name LIKE '%Tim Hogan%' OR Name LIKE '%Sriram J%')
  AND Email LIKE '%databricks.com%'
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  AND IsActive = true
```

Use the appropriate variant. If not found, leave name as-is (no error in doc).

Return all enrichment data to the parent agent for Phase 4.

### Phase 4: Update Document

1. Retrieve Phase 3 result via `TaskOutput` (blocks until background agent finishes)
2. Fetch a fresh token: `TOKEN=$(python3 <google-auth>/resources/google_auth.py token)`
3. Build a single `batchUpdate` with **only `replaceAllText` requests** — no insertText, no styling:

   | Find | Replace (example) |
   |------|-------------------|
   | `Account Owner: —` | `Account Owner: Assan Grisby` |
   | `Salesforce Account ID: —` | `Salesforce Account ID: 00161000011Yj67AAC` |
   | `Customer: Accuray` | `Customer: Accuray Incorporated` (only if SF name differs) |
   | `- Tim Hogan` | `- Tim Hogan <tim.hogan@databricks.com> - Sr. Manager, Field Engineering` |
   | `- Tim Hogan <tim.hogan@databricks.com>` | `- Tim Hogan <tim.hogan@databricks.com> - Sr. Manager, Field Engineering` |

   **Attendee find-strings must match exactly** — bullet formatting means the `- ` prefix is part of the document text. Wrong find-string silently fails. **Debugging tip:** if enrichment data doesn't appear, verify the find-string matches the document text exactly (check for leading `- ` on bullet lines). Open the doc in Google Docs > Find & Replace to test the string.

4. Execute `batchUpdate`. No document reads, index computation, or second styling pass needed.
5. Output: "Background data added to document."

## Examples

### Example: Calendar meeting
```
Agent: logcall v1.2.1 — [westnamedcustomers](https://drive.google.com/...)
       Have feedback? Slack #logcall-feedback

       Tell me about the meeting — customer, topic, Databricks attendees,
       customer attendees. Say "calendar" to pick from today's meetings.

User:  calendar

Agent: Here are today's meetings:
       1. 9:00 AM - Skyworks Q1 Review (sarah@skyworks.com, sriram@databricks.com)
       2. 11:00 AM - Acme Technical Deep Dive (john@acme.com)
       3. 2:00 PM - Internal Standup
       Which one?

User:  1

Agent: Searching for Skyworks folder...
       Creating meeting notes doc...
       Applying formatting...
       Opening in browser...
       Meeting notes created and opened in your browser.
       Salesforce data and attendee titles are loading in the background.
```

### Example: Full details in one message
```
Agent: logcall v1.2.1 — [westnamedcustomers](https://drive.google.com/...)
       Have feedback? Slack #logcall-feedback

       Tell me about the meeting — customer, topic, Databricks attendees,
       customer attendees. Say "calendar" to pick from today's meetings.

User:  Call with Skyworks about Q1 roadmap. Me, Sriram, and Jake.
       Customer side Sarah Johnson.

Agent: Searching for Skyworks folder...
       Creating meeting notes doc...
       Applying formatting...
       Opening in browser...
       Meeting notes created and opened in your browser.
       Salesforce data and attendee emails are loading in the background.
       Saved to: skyworks/meeting-log/
```

### Example: Minimal info with follow-up
```
Agent: logcall v1.2.1 — [westnamedcustomers](https://drive.google.com/...)
       Have feedback? Slack #logcall-feedback

       Tell me about the meeting — customer, topic, Databricks attendees,
       customer attendees. Say "calendar" to pick from today's meetings.

User:  Skyworks, pre-call prep

Agent: Who from Databricks is attending? (I'll include you by default)

User:  just me

Agent: Searching for Skyworks folder...
       Creating meeting notes doc...
       Applying formatting...
       Opening in browser...
       Meeting notes created and opened in your browser.
       Salesforce data is loading in the background.
       Saved to: skyworks/meeting-log/
```

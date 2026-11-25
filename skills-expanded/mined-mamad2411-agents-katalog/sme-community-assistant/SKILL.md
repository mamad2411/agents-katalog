---
name: sme-community-assistant
description: "Create, migrate, register, and manage SME communities for Field Engineering. Use when the user mentions creating an SME community, migrating a community to standards, health-checking communities, managing community channels/groups/pages, ASQ queue management for SME coordinators, ASQ triage, ASQ SLA metrics, or anything related to #sme-* Slack channels and SME program governance."
user-invocable: true
---

# SME Community Assistant

An agentic skill that manages the full lifecycle of SME (Subject Matter Expert) communities for Databricks Field Engineering. It creates, migrates, registers, and health-checks communities across Confluence, Slack, Google Groups, Drive, Calendar, and the SME Registration Sheet.

**Announce at start:** "I'm using the sme-community-assistant skill to help manage SME communities."

---

## Prerequisites

Before starting any mode, verify these integrations are available:

### 1. Google Authentication
Run `/google-auth` to authenticate with Google Workspace. Verify token:
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1)
python3 "$GOOGLE_AUTH_SCRIPT" status
```
If not authenticated, run the login flow first. To get a token for API calls:
```bash
TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
```
All Google API calls require header:
```
-H "x-goog-user-project: gcp-sandbox-field-eng"
```

### 2. Confluence MCP
Load Confluence tools:
```
ToolSearch query: "+confluence"
```
Verify by calling `mcp__confluence__get_confluence_spaces` to confirm access.

### 3. Slack MCP
Load Slack tools:
```
ToolSearch query: "+slack"
```
Verify by calling `mcp__slack__slack_read_api_call` with endpoint `conversations.list` and params `{"limit": 1}`.

### 4. Glean MCP (Mode B only)
Load Glean tools:
```
ToolSearch query: "+glean"
```

### 5. Skip failed prerequisites gracefully
If a prerequisite fails, inform the user and offer to continue with the tools that ARE available. For example, if Confluence MCP is down, Mode A can still create Slack channels, Drive folders, and registration entries — just mark the Confluence page as PENDING.

---

## Canonical Data Sources

### SME Registration Sheet
- **Sheet ID**: `1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY`
  *(If this spreadsheet is ever recreated or moved, update this ID here and in all `curl` calls below.)*
- **Tabs with FE-to-community mappings**: AMER, EMEA, APAC, Managers (from Sorting Hat)
- **Communities tab**: Created/maintained by this skill for community metadata
- **Quota project**: `gcp-sandbox-field-eng`

### Community Registry (bootstrap)
Read `resources/sme_communities_registry.json` for the initial list of 106 communities with name, slug, scope, domain_type, region, and status. The Google Sheet is the live source of truth — the JSON is fallback only.

### Reference Files
- `resources/naming_conventions.md` — Slug derivation, construct naming patterns
- `resources/confluence_page_template.md` — Confluence storage-format HTML templates
- `resources/health_check_criteria.md` — Health scoring rubric
- `resources/compliance_checklist.md` — Standards compliance definition

---

## Mode Selection

Use AskUserQuestion to present the four modes:

**Menu — What would you like to do?** (4 options):
- "Create a new SME community" — description: "Bootstrap a new community with Confluence page, Slack channel, Google Group, Drive folders, Calendar, and registration."
- "Migrate an existing SME community" — description: "Discover and standardize a community that already exists with ad-hoc Confluence pages, Slack channels, and Drive folders."
- "Register or fix an existing community" — description: "Audit an existing community against standards and fix non-compliant items."
- "Health-check & manage communities" — description: "Run health checks, view metrics, and perform management actions on communities."

If the user's initial prompt clearly indicates a mode (e.g., "create a new community for Geospatial"), skip the menu and go directly to that mode. Confirm: "It sounds like you want to create a new community. Is that right?"

---

## Mode A: Create New SME Community

### Phase A.1: Collect Metadata

Gather the following from the user. Use AskUserQuestion for structured choices, free text for names/descriptions.

**Required:**
1. **Community name** (display name, e.g., "Geospatial SME")
2. **Slug** — Derive from the name using rules in `resources/naming_conventions.md`. Present the derived slug and let the user confirm or override.
3. **Scope** — AskUserQuestion: global, amer, emea, apj (note: APJ is used for Asia-Pacific/Japan; maps to "APAC" tab in Sorting Hat data)
4. **Domain type** — AskUserQuestion: product, tech_domain, industry, program
5. **Charter** — 1-3 sentences describing the community's purpose and target audience (free text)
6. **Community Leader** — Name and email of the person who will run this community

**Optional (ask but accept empty):**
7. **Sponsor** — VP/Director sponsor name and email
8. **Coordinator(s)** — Additional organizers
9. **Cadence** — AskUserQuestion: weekly, biweekly, monthly, ad-hoc
10. **Meeting day/time** — If cadence is not ad-hoc (free text, e.g., "Wednesdays 10am PT")
11. **Expected initial membership** — Small (<10), Medium (10-30), Large (30+)

Present a summary of all collected metadata and ask user to confirm before proceeding.

### Phase A.2: Collision Check

Before creating anything, search for existing communities that might match:

**Confluence search:**
```
mcp__confluence__search_confluence_pages with query: "<community_name> SME" and limit: 5
```

**Slack channel search:**
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.list"
  params: {"limit": 200, "types": "public_channel"}
```
Paginate using `cursor` from `response_metadata.next_cursor` if more channels exist.
Filter results locally for channels containing the slug or community name.

**Registration Sheet check:**
Read the Communities tab (if it exists) from the registration sheet:
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values/Communities!A:R" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

**If matches found:**
Present them to the user:
```
I found existing assets that may belong to this community:
- Confluence: "<page title>" (URL)
- Slack: #<channel-name> (<member_count> members)
- Registration: row exists with status "<status>"

Would you like to:
1. Proceed with creating a NEW community (these are different)
2. Switch to Mode B (Migrate) to standardize the existing community
3. Switch to Mode C (Register/Fix) to align the existing community
```

**If no matches found:** Proceed to Phase A.3.

### Phase A.3: Create Confluence Page

**Step 1: Find the FE space and parent page.**
```
mcp__confluence__get_confluence_spaces
```
Find the space with key "FE" or name containing "Field Engineering". Record the `space_id`.

```
mcp__confluence__search_confluence_pages
  query: "title = 'SME Communities' AND space = 'FE'"
  limit: 5
```
Record the parent `page_id`. If the parent page doesn't exist, inform the user and ask whether to create it or pick a different parent.

**Step 2: Build the page content.**
Read `resources/confluence_page_template.md` and replace all `{{PLACEHOLDER}}` variables with the metadata collected in Phase A.1. For variables not yet known (like `{{SLACK_URL}}`, `{{DRIVE_URL}}`), use placeholder text like "TBD - will be updated after channel/folder creation".

**Step 3: Create the page.**
```
mcp__confluence__create_confluence_page
  title: "Global <Community Name> SME" (or "<Region> <Community Name> SME" for regional)
  content: <rendered template HTML>
  space_id: <FE space ID>
  parent_id: <SME Communities parent page ID>
```

Record the new page ID and URL. Tell the user: "Confluence page created: [title](url)"

### Phase A.4: Create Slack Channel

**Important:** The Slack MCP only supports `chat.postMessage` as a write operation. Channel creation, topic/purpose setting, and pinning require operations not available via MCP. Attempt each via `slack_write_api_call` first — if it fails, provide manual instructions.

**Step 1: Check if channel name is available.**
The desired name is `sme-<slug>-<scope>` (e.g., `sme-geospatial-global`).
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.list"
  params: {"limit": 200, "types": "public_channel"}
```
Paginate using `cursor` from `response_metadata.next_cursor` if more channels exist. Filter results locally for the exact channel name. If taken, propose alternatives (append number, use different scope word).

**Step 2: Create the channel.**
Ask user for confirmation before creating. Attempt via MCP:
```
mcp__slack__slack_write_api_call
  endpoint: "conversations.create"
  params: {"name": "sme-<slug>-<scope>", "is_private": false}
```

**If MCP rejects the operation** (endpoint not supported), tell the user:
```
The Slack MCP doesn't support channel creation. Please create the channel manually:
1. In Slack, click "+" next to Channels → Create a channel
2. Name: sme-<slug>-<scope>
3. Set to Public
4. Once created, give me the channel name and I'll continue with the remaining setup.
```
Mark as `PENDING_HUMAN_ACTION` and continue. Once the user provides the channel name, use `conversations.list` to find the channel ID.

**Step 3: Set topic and purpose.**
Attempt via MCP:
```
mcp__slack__slack_write_api_call
  endpoint: "conversations.setTopic"
  params: {"channel": "<channel_id>", "topic": "<charter_summary> | Confluence: <page_url> | Lead: <leader_name>"}
```
```
mcp__slack__slack_write_api_call
  endpoint: "conversations.setPurpose"
  params: {"channel": "<channel_id>", "purpose": "SME community for <community_name>. Join: <page_url>"}
```
If these fail, tell the user to set the topic/purpose manually and provide the exact text.

**Step 4: Post welcome message.**
This uses `chat.postMessage` which IS supported:
```
mcp__slack__slack_write_api_call
  endpoint: "chat.postMessage"
  params: {
    "channel": "<channel_id>",
    "text": "Welcome to the <community_name> SME community!\n\n*Charter:* <charter_text>\n*Community Leader:* <leader_name>\n*Confluence Page:* <page_url>\n*How to Join:* Review the Confluence page, join this channel, and request access to the Google Group (<google_group_email>).\n\nOffice hours: <cadence> on <day_time> (details on the Confluence page)."
  }
```

**Step 5: Pin welcome message.**
Attempt via MCP:
```
mcp__slack__slack_write_api_call
  endpoint: "pins.add"
  params: {"channel": "<channel_id>", "timestamp": "<message_ts>"}
```
If this fails, tell the user: "Please pin the welcome message I just posted in the channel."

Tell the user: "Slack channel setup complete: #sme-<slug>-<scope>" (or list any PENDING items)

### Phase A.5: Google Group

Google Groups creation typically requires Google Workspace Admin privileges. The skill should attempt to check if the group already exists, and if not, guide the user.

**Step 1: Check if group exists.**
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://www.googleapis.com/admin/directory/v1/groups/sme-<slug>-<scope>@databricks.com" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

**If group exists:** Record it and move on.

**If group does not exist or API returns 403/404:**
Tell the user:
```
The Google Group sme-<slug>-<scope>@databricks.com needs to be created.
Google Groups creation requires admin privileges that may not be available via OAuth.

Please create the group manually:
1. Go to https://groups.google.com/a/databricks.com
2. Create group: sme-<slug>-<scope>@databricks.com
3. Set join policy: "Anyone in the organization can ask"
4. Add <leader_email> as Owner
5. Add <coordinator_emails> as Managers

I'll mark this as PENDING and continue with other constructs.
```

Mark Google Group as `PENDING_HUMAN_ACTION` in the summary.

### Phase A.6: Google Drive Folder Structure

**Step 1: Find the Global SME Communities shared drive root.**
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://www.googleapis.com/drive/v3/drives?q=name%20contains%20'SME'&pageSize=10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
If no shared drive is found, search for a regular folder:
```bash
curl -s "https://www.googleapis.com/drive/v3/files?q=name%3D'Global%20SME%20Communities'%20and%20mimeType%3D'application/vnd.google-apps.folder'&spaces=drive" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Record the root folder ID. If not found, ask the user for the correct shared drive or folder URL.

**Step 2: Create community folder.**
```bash
curl -s -X POST "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"name": "<Community Display Name>", "mimeType": "application/vnd.google-apps.folder", "parents": ["<root_folder_id>"]}'
```
Record the new folder ID.

**Step 3: Create subfolders.**
For each subfolder (Attendance, Recordings, Transcripts, Assets, FEIP, Newsletters):
```bash
curl -s -X POST "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"name": "<subfolder_name>", "mimeType": "application/vnd.google-apps.folder", "parents": ["<community_folder_id>"]}'
```

Tell the user: "Drive folder structure created: [Community Name](folder_url)"

### Phase A.7: Calendar Event

Only create if the user specified a cadence other than "ad-hoc".

Use the `/google-calendar` skill pattern or direct API:
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "SME <Community Name> Office Hours",
    "description": "SME Community: <community_name>\nConfluence: <page_url>\nSlack: <slack_channel>\n\nAgenda:\n1. Announcements\n2. Topic of the week\n3. Open Q&A",
    "start": {"dateTime": "<start_datetime>", "timeZone": "<timezone>"},
    "end": {"dateTime": "<end_datetime>", "timeZone": "<timezone>"},
    "recurrence": ["RRULE:FREQ=<WEEKLY|MONTHLY>;INTERVAL=<1|2>;BYDAY=<WE>"],
    "attendees": [{"email": "<google_group_email>"}],
    "conferenceData": {"createRequest": {"requestId": "sme-<slug>-<scope>", "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
    "guestsCanModify": false,
    "guestsCanInviteOthers": true
  }'
```

Note: Recording and transcript settings are typically managed in Google Workspace admin settings for the organization, not per-event via API. Inform the user to verify these settings are enabled for the Google Meet.

Record the event ID. Tell the user: "Recurring calendar event created: <cadence> <day_time>"

### Phase A.8: Update Registration Sheet

Append a row to the "Communities" tab. If the tab doesn't exist, create it first with headers.

**Check if Communities tab exists:**
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY?fields=sheets.properties" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

**If "Communities" tab does not exist, create it:**
```bash
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"requests": [{"addSheet": {"properties": {"title": "Communities"}}}]}'
```
Then write the header row:
```bash
curl -s -X PUT "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values/Communities!A1:R1?valueInputOption=RAW" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"values": [["Community Name", "Slug", "Scope", "Status", "Confluence Page ID", "Confluence URL", "Slack Channel ID", "Slack Channel Name", "Google Group", "Drive Folder ID", "Calendar Event ID", "Lead Name", "Lead Email", "Member Count", "Last Activity", "Health Score", "Created Date", "Notes"]]}'
```

**Append the community row:**
```bash
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values/Communities!A:R:append?valueInputOption=RAW" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"values": [["<name>", "<slug>", "<scope>", "active", "<page_id>", "<page_url>", "<channel_id>", "#sme-<slug>-<scope>", "<group_email>", "<folder_id>", "<event_id>", "<leader_name>", "<leader_email>", "", "", "", "<today_date>", ""]]}'
```

### Phase A.9: Update Confluence Page with Final Links

Now that all constructs exist, go back and update the Confluence page to replace placeholder links with real URLs.

```
mcp__confluence__get_confluence_page_content
  page_id: <page_id>
  is_full: true
```
Get the current version number from the response.

Build updated HTML content with all real URLs (Slack channel URL, Drive folder URL, Calendar link, Google Group).

```
mcp__confluence__update_confluence_page
  page_id: <page_id>
  version_number: <current_version + 1>
  title: <same title>
  content: <updated HTML with real links>
```

### Phase A.10: Summary

Present a final summary table:

```
## Community Created: <Community Name>

| Construct | Status | Details |
|---|---|---|
| Confluence | DONE | [<title>](<url>) |
| Slack | DONE | #sme-<slug>-<scope> |
| Google Group | DONE / PENDING | sme-<slug>-<scope>@databricks.com |
| Drive | DONE | [Folder](<url>) |
| Calendar | DONE / SKIPPED | <cadence> <day_time> |
| Registration | DONE | Row added to Communities tab |
| Go Link | PENDING | Suggest creating: go/sme-<slug>-<scope> |

### Next Steps:
1. If Google Group is PENDING: create it manually and update the registration
2. Create go link: go/sme-<slug>-<scope> → <confluence_url>
3. Invite initial members to the Slack channel
4. Schedule and announce the first office hours session
5. Share the Confluence page link with potential members
```

---

## Mode B: Migrate Existing SME Community

### Phase B.1: Get Migration Anchor

Ask the user for the best known entry point for the existing community:

**Menu — What's the best anchor for this community?** (4 options):
- "Confluence page URL" — description: "I have a link to an existing Confluence page for this community"
- "Slack channel name" — description: "I know the Slack channel they use (e.g., #dbsql-sme-backchannel)"
- "Google Group email" — description: "I know the Google Group address"
- "Community name only" — description: "I just know the name, I'll need help finding everything"

Collect the anchor value from the user.

### Phase B.2: Discovery

Search across all available integrations to build a comprehensive inventory of existing community assets. The goal is to find everything BEFORE proposing a migration plan.

**Step 1: Follow the anchor.**

If anchor is a Confluence URL, read the page and extract all embedded links:
```
mcp__confluence__get_confluence_page_content
  page_id: <extracted_page_id>
  is_full: true
```
Parse the page content for links to Slack channels, Google Groups, Drive folders, calendars, and other Confluence pages. Record every URL found — these are strong signals.

If anchor is a Slack channel, get channel info and recent messages for links:
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.info"
  params: {"channel": "<channel_id>"}
```
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.history"
  params: {"channel": "<channel_id>", "limit": 50}
```
Scan message text and attachments for Confluence URLs, Drive links, calendar links, and Google Group references.

**Step 2: Search Confluence for related pages.**
```
mcp__confluence__search_confluence_pages
  query: "<community_name>"
  limit: 10
```
Also search for regional variants and common alternate names:
```
mcp__confluence__search_confluence_pages
  query: "<slug> SME"
  limit: 5
```
Look for regional variants (e.g., "EMEA <name>", "APJ <name>").

**Step 3: Search Slack for channels and messages.**

Find related channels:
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.list"
  params: {"limit": 200, "types": "public_channel"}
```
Paginate if needed. Filter locally for channels containing the community name, slug, or related keywords (e.g., for "Ray SME", also look for "ray", "ray-sme", "ray-field").

Search messages for references to this community in other channels:
```
mcp__slack__slack_read_api_call
  endpoint: "search.messages"
  params: {"query": "<community_name> SME", "count": 10}
```
This surfaces assets mentioned in conversations — Drive links, docs, recordings — that might not be linked from the Confluence page.

**Step 4: Search Google Drive for folders and documents.**
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
# Search for folders matching the community name
curl -s "https://www.googleapis.com/drive/v3/files?q=name+contains+'<community_name>'+and+mimeType%3D'application/vnd.google-apps.folder'&fields=files(id,name,webViewLink,owners,parents)&spaces=drive" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
Also search for the slug and common variations:
```bash
curl -s "https://www.googleapis.com/drive/v3/files?q=name+contains+'<slug>'+and+name+contains+'SME'&fields=files(id,name,webViewLink,owners)&spaces=drive" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
Check the canonical location too (Global SME Communities shared drive).

**Step 5: Search for Google Groups.**
Check for both the canonical name and common non-canonical patterns:
```bash
# Canonical name
curl -s "https://www.googleapis.com/admin/directory/v1/groups/sme-<slug>-<scope>@databricks.com" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
# Common non-canonical patterns
curl -s "https://www.googleapis.com/admin/directory/v1/groups/<slug>-sme@databricks.com" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
Note: Admin Directory API may return 403 — that's OK, just mark as "unable to verify" and ask the user.

**Step 6: Search for Calendar events.**
```bash
curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?q=<community_name>&maxResults=5&orderBy=startTime&singleEvents=true&timeMin=$(python3 -c "import datetime; print((datetime.datetime.utcnow()-datetime.timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ'))")" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
Search for events matching the community name, slug, or "office hours". Check if any are recurring.

**Step 7: Search Glean for broader discovery.**
Run multiple targeted searches to catch assets the above steps may have missed:
```
mcp__glean__glean_read_api_call
  endpoint: "search.query"
  params: {"query": "<community_name> SME", "pageSize": 10}
```
```
mcp__glean__glean_read_api_call
  endpoint: "search.query"
  params: {"query": "<community_name> office hours recordings", "pageSize": 5}
```
```
mcp__glean__glean_read_api_call
  endpoint: "search.query"
  params: {"query": "<slug> SME assets", "pageSize": 5}
```
Glean searches across Google Drive, Confluence, Slack, and other connected sources — it often surfaces assets that siloed searches miss.

**Step 8: Check Registration Sheet.**
Read the Communities tab for any existing entry matching this community name or slug.

**Step 9: Interactive gap-fill.**
After completing automated discovery, present what was found and explicitly ask the coordinator:

```
I found the following assets for <Community Name>:
- Confluence: [list found pages]
- Slack: [list found channels]
- Drive: [list found folders/docs]
- Google Group: [found or not found]
- Calendar: [found events or not found]

Do you know of any other assets I missed? For example:
- Drive folders with recordings, presentations, or templates
- Google Docs with meeting notes or agendas
- Other Slack channels used by this community
- External links (GitHub repos, Databricks notebooks, etc.)

Please share any URLs or names and I'll add them to the migration plan.
```

Incorporate any user-provided assets into the discovery results before building the migration report.

### Phase B.3: Migration Report

Build and present a comprehensive inventory:

```
## Migration Report: <Community Name>

### Discovered Assets
| Asset | Current State | Location |
|---|---|---|
| Confluence | "<page_title>" | <url> |
| Confluence (regional) | "<emea_page_title>" | <url> |
| Slack | #<channel_name> (<N> members) | <url> |
| Google Group | <group_email> | exists / not found |
| Drive | "<folder_name>" | <url> / not found |
| Calendar | "<event_name>" | exists / not found |
| Registration | row exists / not found | — |

### Proposed Canonical Structure
| Construct | Target |
|---|---|
| Slug | <derived_slug> |
| Scope | <scope> |
| Confluence | Global <Name> SME (under FE/SME Communities) |
| Slack | #sme-<slug>-<scope> |
| Google Group | sme-<slug>-<scope>@databricks.com |
| Drive | Global SME Communities/<Name>/ |

### Migration Actions
| # | Action | Details | Destructive? |
|---|---|---|---|
| 1 | CREATE Confluence page | New standardized page under FE/SME Communities | No |
| 2 | COPY content | Extract content from old page into new template | No |
| 3 | REDIRECT old page | Add migration banner to old Confluence page | No |
| 4 | RENAME Slack channel | #old-name → #sme-<slug>-<scope> | No (if available) |
| 5 | CREATE Drive structure | New canonical folder tree | No |
| 6 | REGISTER | Add row to Communities tab | No |
```

Ask user to review and confirm the migration plan. Allow them to modify individual actions.

### Phase B.4: Execute Migration (Non-Destructive)

Execute each confirmed action in order. For each action:

1. **Before executing**: Tell the user what you're about to do
2. **After executing**: Confirm success and record the result
3. **On failure**: Report the error, skip the action, continue with remaining actions

**Confluence migration:**
- Read content from old page: `mcp__confluence__get_confluence_page_content`
- Create new standardized page from template, incorporating relevant content from the old page
- Add redirect banner to old page: `mcp__confluence__update_confluence_page` — prepend the migration redirect banner from `resources/confluence_page_template.md` to the existing content. Do NOT delete or clear the old content.

**Slack migration:**
- Attempt to rename the old channel via MCP: `mcp__slack__slack_write_api_call` with `conversations.rename`
- If MCP rejects the operation, or rename fails (name taken, user prefers to keep old channel):
  - Ask the user to create the new canonical channel manually (same fallback as Mode A Phase A.4)
  - Post redirect message in old channel using `chat.postMessage` (this IS supported): "This community has moved to #sme-<slug>-<scope>. Please join the new channel for all future discussions."
  - Do NOT archive the old channel unless the user explicitly requests it
- If archiving is requested, attempt via MCP: `conversations.archive`. If unsupported, provide manual instructions.

**Drive migration:**
- Create canonical folder structure (same as Mode A Phase A.6)
- Document the old folder location in the registration sheet Notes column
- List the contents of the old folder so the user can see what's there:
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://www.googleapis.com/drive/v3/files?q='<old_folder_id>'+in+parents&fields=files(id,name,mimeType,modifiedTime,webViewLink)&pageSize=100" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
- Present the file list and ask: "Would you like me to move these files to the new canonical folder, or leave them for manual migration?"
- **If user approves moving files**, move each file by updating its parent:
```bash
# For each file: remove old parent, add new parent
curl -s -X PATCH "https://www.googleapis.com/drive/v3/files/<file_id>?addParents=<new_folder_id>&removeParents=<old_folder_id>&fields=id,name,parents" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{}'
```
  - Process files one at a time, reporting each move: "Moved: <filename>"
  - For subfolders in the old location, map them to canonical subfolders using this logic:
    - Folder name contains "recording" or "video" → move contents into `Recordings/`
    - Folder name contains "slide" or "presentation" or "deck" → move contents into `Assets/`
    - Folder name contains "attend" or "roster" → move contents into `Attendance/`
    - Folder name contains "transcript" or "notes" → move contents into `Transcripts/`
    - Folder name contains "newsletter" → move contents into `Newsletters/`
    - Folder name contains "feip" or "proposal" → move contents into `FEIP/`
    - No match → move contents into the community root folder and report: "Unmapped subfolder: <folder_name> — moved contents to root"
    Use case-insensitive matching. Present the proposed mapping to the user before executing.
  - If a file already exists in the destination with the same name, skip it and report: "Skipped (already exists): <filename>"
  - After all moves, report a summary: N files moved, N skipped, N errors
- **If user declines**, leave files in place and note the old folder URL in the registration sheet Notes column
- **Important**: Moving files changes their URL. Warn the user that any existing links to these files will break. Offer to leave copies in the old location instead of moving (copy = create shortcut):
```bash
# Create a shortcut in the new folder pointing to the original file (non-destructive alternative)
curl -s -X POST "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"name": "<filename>", "mimeType": "application/vnd.google-apps.shortcut", "shortcutDetails": {"targetId": "<file_id>"}, "parents": ["<new_folder_id>"]}'
```
  This preserves existing links while making files discoverable in the new location.

**Google Group:**
- If existing group has a non-canonical name: document it as-is, suggest creating a canonical alias or new group
- If no group exists: follow Mode A Phase A.5

**Calendar:**
- If existing calendar event found: document it and link from the Confluence page
- If no event found: follow Mode A Phase A.7

### Phase B.5: Update Registration Sheet

Same as Mode A Phase A.8 — append or update the community row with all new canonical construct references. Include notes about legacy assets.

### Phase B.6: Post-Migration Verification

Present a final summary showing:
- All new canonical constructs with links
- All legacy assets with their current status (redirected, documented, archived)
- Any PENDING items that need manual attention

---

## Mode C: Register/Fix Alignment

### Phase C.1: Identify Community

Ask the user which community to audit. Accept: community name, Slack channel, Confluence URL, or Google Group.

If the user provides a name, check `resources/sme_communities_registry.json` for a match. Also search Confluence and Slack to find existing assets.

### Phase C.2: Compliance Audit

Read `resources/compliance_checklist.md` and evaluate each requirement.

**For each construct, check:**

1. **Confluence**: Search for a page matching the community. Check title naming, parent page location, section completeness.
2. **Slack**: Find the channel. Check naming convention, topic content, pinned messages.
3. **Google Group**: Check if canonical group exists.
4. **Drive**: Search for folder under Global SME Communities root.
5. **Calendar**: Check for recurring events.
6. **Registration**: Check if row exists in Communities tab with all required fields.

Present results as a compliance table:

```
## Compliance Audit: <Community Name>

| Requirement | Status | Current | Expected | Fix |
|---|---|---|---|---|
| Confluence page exists | PASS | "Global AI/BI SME" | — | — |
| Confluence under FE/SME Communities | FAIL | Under personal space | FE/SME Communities | Move page |
| Confluence title convention | PASS | "Global AI/BI SME" | — | — |
| Confluence sections complete | WARN | Missing ASQ section | All 8 sections | Add section |
| Slack channel exists | PASS | #sme-ai-bi-global | — | — |
| Slack naming convention | PASS | #sme-ai-bi-global | — | — |
| Slack topic set | FAIL | Empty | Charter + links | Set topic |
| Slack pinned message | FAIL | No pins | Welcome message | Post + pin |
| Google Group exists | FAIL | Not found | sme-ai-bi-global@ | Create |
| Drive folder exists | PASS | /Global SME/AI BI/ | — | — |
| Drive subfolders | WARN | Missing FEIP/ | All 6 subfolders | Create FEIP/ |
| Calendar event | PASS | Weekly Wednesdays | — | — |
| Registration row | FAIL | Not found | Row in Communities tab | Register |
| Go link | UNKNOWN | Cannot verify | go/sme-ai-bi-global | Create |
```

### Phase C.3: Propose and Execute Fixes

For each FAIL or WARN item, propose a specific fix. Group fixes by priority (from `resources/compliance_checklist.md` remediation priority).

Present the fix plan to the user:
```
Proposed fixes (ordered by priority):
1. [HIGH] Register in Communities tab — append row
2. [HIGH] Set Slack topic — add charter + Confluence link
3. [HIGH] Post and pin welcome message in Slack
4. [MED] Create Google Group: sme-ai-bi-global@databricks.com
5. [MED] Add missing ASQ section to Confluence page
6. [LOW] Create FEIP/ subfolder in Drive
7. [LOW] Create go link: go/sme-ai-bi-global

Execute all? Or select specific fixes?
```

Execute approved fixes using the same MCP calls as Mode A. For each fix:
- Confirm before executing destructive or visible changes
- Report success/failure
- Update registration sheet with new construct details

---

## Mode D: Health-check & Manage

### Phase D.1: Select Scope

Use AskUserQuestion:

**Menu — Health-check scope** (3 options):
- "Single community" — description: "Check one specific community by name"
- "Region" — description: "Check all communities in a region (AMER, EMEA, APJ)"
- "All communities" — description: "Full health check across all registered communities"

**If single community:** Ask for the community name.
**If region:** AskUserQuestion with options: AMER, EMEA, APJ, Global.
Note: When cross-referencing Sorting Hat data, map APJ scope to the "APAC" tab in the registration sheet.
**If all:** Warn that this may take a few minutes for 100+ communities and proceed.

### Phase D.2: Load Community Inventory

Read the Communities tab from the registration sheet:
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values/Communities!A:R" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Filter to the selected scope. If the Communities tab doesn't exist or is empty, inform the user: "No communities are registered yet. Run Mode A (Create) or Mode C (Register) first to populate the registry."

### Phase D.3: Collect Health Metrics

For each community in scope, collect metrics per `resources/health_check_criteria.md`:

**Slack activity & membership:**
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.info"
  params: {"channel": "<channel_id>"}
```
Extract `num_members` and `latest` (last message timestamp).

For detailed activity (messages per week), if needed:
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.history"
  params: {"channel": "<channel_id>", "limit": 50, "oldest": "<30_days_ago_unix>"}
```
Count messages returned.

**Confluence freshness:**
```
mcp__confluence__get_confluence_page_content
  page_id: <page_id>
  is_full: false
```
Check the page metadata for `lastModified` or `version.when` date.

**Leadership status:**
Check if the leader listed in the registration sheet is active in the community.

Step 1: Get the leader's email from the registration sheet (Lead Email column).

Step 2: Look up their Slack user ID:
```
mcp__slack__slack_read_api_call
  endpoint: "users.lookupByEmail"
  params: {"email": "<leader_email>"}
```
Extract the `user.id` from the response.
- If the response contains `"ok": false` with error `"users_not_found"`, the user may have left the org — score as RED ("Leader not found in Slack — may have left the organization").
- If the error is `"users_not_visible"` or similar, the leader may be a Slack guest with restricted email visibility — score as YELLOW ("Leader email not resolvable in Slack — may be a guest account") rather than RED, since this is a lookup limitation, not an activity problem.

Step 3: Check if they've posted in the community channel recently:
```
mcp__slack__slack_read_api_call
  endpoint: "conversations.history"
  params: {"channel": "<channel_id>", "limit": 100, "oldest": "<30_days_ago_unix>"}
```
Filter messages locally where `message.user == <leader_user_id>`. If any match, the leader is active (GREEN). If no matches in 30 days, score as YELLOW. If the leader email is empty or the user has left the org, score as RED.

**Calendar compliance:**
Check if the community has recurring meetings happening on schedule.

Step 1: Get the Google Group email from the registration sheet (Google Group column) and the Calendar Event ID (if stored).

Step 2: Search for calendar events matching this community:
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?q=SME+<community_name>&maxResults=5&orderBy=startTime&singleEvents=true&timeMin=$(python3 -c "import datetime; print((datetime.datetime.utcnow()-datetime.timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ'))")" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

Step 3: Evaluate results:
- If no events found, also try searching by slug and "office hours":
```bash
curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?q=<slug>+office+hours&maxResults=5&orderBy=startTime&singleEvents=true&timeMin=$(python3 -c "import datetime; print((datetime.datetime.utcnow()-datetime.timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ'))")" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
- If events found: check the most recent event date. If within the expected cadence window (e.g., weekly = last 14 days, monthly = last 45 days), score as GREEN. If outside the window, score as YELLOW.
- If no events found at all, score as RED.
- If the Calendar API returns 403 or the search yields no results, mark as UNKNOWN and include a diagnostic note: "Calendar check unavailable — possible causes: (1) missing calendar.events.readonly scope in OAuth token, (2) community calendar is not shared with the authenticated user, (3) Google API quota exceeded. Re-run `/google-auth` and verify calendar scope is included."

**Rate limiting:** For batch health checks (multiple communities), process in groups of 10 with a 2-second pause between groups to avoid MCP rate limits. Use `mcp__slack__slack_batch_read_api_call` where possible for Slack calls. For Calendar API calls, process sequentially (one per community) with a 1-second pause between calls (`sleep 1`) to stay within Google's Calendar API quota of 100 requests per 100 seconds.

### Phase D.4: Score and Report

Apply the scoring rubric from `resources/health_check_criteria.md` to each community.

Present results as a formatted table, sorted by health (CRITICAL first, then AT RISK, then HEALTHY):

```
## SME Community Health Report
Generated: <date>
Scope: <scope>

| Community | Slack | Members | Confluence | Leadership | Calendar | Registration | Overall |
|---|---|---|---|---|---|---|---|
| Hadoop | RED | RED | RED | RED | RED | YELLOW | CRITICAL |
| Mining Industry | RED | YELLOW | RED | YELLOW | RED | GREEN | CRITICAL |
| AI/BI SME | GREEN | GREEN | YELLOW | GREEN | GREEN | GREEN | HEALTHY |
| Architecture SME | GREEN | GREEN | GREEN | GREEN | GREEN | GREEN | HEALTHY |

### Summary
- HEALTHY: <N> communities
- AT RISK: <N> communities
- CRITICAL: <N> communities
```

### Phase D.5: Management Actions

For CRITICAL and AT RISK communities, offer actions:

**Menu — Action for <Community Name>** (4 options):
- "Revitalize" — description: "Assign new leadership, refresh content, re-announce to eligible FEs"
- "Merge" — description: "Combine with a related community"
- "Archive" — description: "Mark as archived, archive Slack channel, add archive banner to Confluence"
- "Skip" — description: "Take no action for now"

**If Revitalize:**

Step 1: Assign new leadership.
- Use AskUserQuestion to get new leader name and email
- If the user doesn't have a candidate, offer to search: "Would you like me to find FEs who were mapped to this community by the Sorting Hat?"

Step 2: Pull eligible FEs from Sorting Hat data.
Read the appropriate tab(s) based on community scope. Map APJ scope to the APAC tab.
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
# For global communities, read all three regional tabs. For regional, read just the matching tab.
# AMER tab:
curl -s "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values/AMER!A:X" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```
Filter rows where column W (Suggested SME Community) matches this community name. Extract:
- Column C = Full Name
- Column D = Email
- Column N = Job Profile
- Column O = Job Level

Present the eligible FE list:
```
Found <N> FEs mapped to <Community Name> by the Sorting Hat:

| Name | Email | Job Profile | Level |
|------|-------|-------------|-------|
| ... | ... | ... | ... |

Would you like to:
1. Select one of these as the new leader
2. Enter a different person
```

Step 3: Confirm and update Confluence page governance section.
```
mcp__confluence__get_confluence_page_content
  page_id: <page_id>
  is_full: true
```
Find the `<h2>Governance & Roles</h2>` section in the HTML. **Show the current governance section to the user** before making changes:
```
Current governance section:
  Community Leader: <current_leader_name> (<current_leader_email>)
  ...

I'll update this to:
  Community Leader: <new_leader_name> (<new_leader_email>)

Proceed with Confluence update?
```
Only after user confirms, replace the Community Leader row with the new leader's name and email. If no governance section exists, append one from the template.
```
mcp__confluence__update_confluence_page
  page_id: <page_id>
  version_number: <current_version + 1>
  title: <same title>
  content: <updated HTML>
```

Step 4: Post revitalization announcement in Slack channel.
Show the user a preview of the announcement before posting:
```
I'll post this announcement in #<channel_name>:

"This community is being revitalized!
New Community Leader: <new_leader_name>
We're looking to re-engage this community..."

Post this announcement?
```
Only after user confirms:
```
mcp__slack__slack_write_api_call
  endpoint: "chat.postMessage"
  params: {
    "channel": "<channel_id>",
    "text": "This community is being revitalized!\n\n*New Community Leader:* <new_leader_name> (<new_leader_email>)\n\nWe're looking to re-engage this community. If you're interested in <community_name>, please introduce yourself here. Upcoming office hours will be announced soon.\n\nConfluence page: <page_url>"
  }
```

Step 5: Update registration sheet.
Find the community's row in the Communities tab and update the Lead Name (col L) and Lead Email (col M) columns:
```bash
curl -s -X PUT "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values/Communities!L<row>:M<row>?valueInputOption=RAW" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"values": [["<new_leader_name>", "<new_leader_email>"]]}'
```
Also update the Notes column (col R) with a timestamp: "Revitalized <date>. New leader: <name>."

Step 6: Offer to send outreach.
Present the list of eligible FEs (from Step 2) and ask:
```
Would you like me to post in the Slack channel inviting these <N> FEs to re-engage?
I can tag them in a message or just share the list for you to reach out manually.
```
If approved, compose a Slack message mentioning the eligible FEs (by name, not @-mention to avoid spam) with a link to the Confluence page and next office hours.

**If Merge:**
- Ask which community to merge into
- Post redirect in the old Slack channel pointing to the target community
- Add redirect banner to old Confluence page
- Update both communities' registration rows
- Ask user to confirm Slack channel archival

**If Archive:**
Ask user for explicit confirmation. Attempt via MCP:
```
mcp__slack__slack_write_api_call
  endpoint: "conversations.archive"
  params: {"channel": "<channel_id>"}
```
If the MCP rejects this operation, tell the user to archive the channel manually in Slack.
Add archive banner to Confluence page (from `resources/confluence_page_template.md`).
Update registration sheet status to "archived".

### Phase D.6: Update Health Scores in Registration Sheet

Write the health scores back to the registration sheet's Health Score column (column P):
```bash
GOOGLE_AUTH_SCRIPT=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools -name "google_auth.py" 2>/dev/null | head -1) && TOKEN=$(python3 "$GOOGLE_AUTH_SCRIPT" token)
curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/1DUyrJLlxcTupnDhECWcgtcjQ_fL_0HOfvD1XdGK3xFY/values:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -H "Content-Type: application/json" \
  -d '{"valueInputOption": "RAW", "data": [<per-row updates for column P>]}'
```

---

## Manage ASQ

### When to Enter Manage ASQ

This mode activates when any of the following are true:
- The user is in Mode D (Health-check & manage) and selects "Manage ASQs", "ASQ queue", "triage", or similar
- The user directly asks about ASQ queue, triage, assignment, or SLA metrics for a specific community
- The user identifies themselves as a Coordinator or Leader and wants to work on ASQs

**Announce:** "Entering Manage ASQ for <Community Name>."

### Business Context

ASQ (ApprovalRequest__c in Salesforce) is the **exclusive intake mechanism** for SME customer-facing work. No ad-hoc intake is permitted.

**Phase 1 (Q1 FY27):** There is no dedicated SME ASQ queue or request type. SME ASQs piggyback on the existing SSA infrastructure using **hashtag convention** as the routing mechanism. SAs add `#<slug>_sme` (e.g., `#ai_sme`, `#dwh_sme`) in the description field. SMEs self-assign by monitoring the ASQ SME dashboard. If unclaimed after **3 business days**, the SME Lead reviews and routes. If the SME Lead hasn't acted within **24 hours** of the 3-day mark, BU+2 / SSA Manager is notified.

### Prerequisites (in addition to base prerequisites)

#### 1. Databricks CLI
Verify access to the logfood profile and SME usage tables:
```bash
databricks auth env --profile logfood 2>/dev/null && echo "OK" || echo "FAIL: run 'databricks configure --profile logfood'"
```

#### 2. Salesforce CLI (for writes only)
Load the SSAgent profile to get the Salesforce org:
```bash
SF_ORG=$(python3 -c "
import yaml, os
p = os.path.expanduser('~/.ssagent/profile.yml')
if os.path.exists(p):
    with open(p) as f: d = yaml.safe_load(f)
    print(d.get('sf_org', ''))
" 2>/dev/null)
echo "SF org: $SF_ORG"
```
If no profile exists, ask the user for their Salesforce org username (e.g., `user@databricks.com.prod`).

#### 3. sf_update.py helper
Locate the safe Salesforce writer:
```bash
SF_UPDATE_SCRIPT=$(find ~/.claude/plugins/cache -path "*/ssagent-sfdc/scripts/sf_update.py" 2>/dev/null | head -1)
echo "SF update script: $SF_UPDATE_SCRIPT"
```
If not found, fall back to raw `sf data update record` commands with extra caution on text field writes.

#### 4. Warehouse ID
```bash
WAREHOUSE_ID=$(databricks sql warehouses list --profile logfood -o json 2>/dev/null | python3 -c "
import json, sys
wh = json.load(sys.stdin)
for w in (wh.get('warehouses', wh) if isinstance(wh, dict) else wh):
    if w.get('warehouse_type','') in ('PRO','') and w.get('state','') == 'RUNNING':
        print(w['id']); break
" 2>/dev/null || echo "df7eb7e74dc8866d")
```

### Phase E.1: Identify Community and Role

Step 1: Resolve the community.
- If the user is already in Mode D with a selected community, reuse `community_slug` and `community_name`.
- Otherwise, ask:

**Menu — Select your community** (list from `resources/sme_communities_registry.json`, filtered to active):
- Show community name, slug, and scope
- Accept free-text input (fuzzy match against registry)

Step 2: Confirm coordinator role.
Ask the user:
```
Are you a Coordinator or Leader for <Community Name>?
(Both roles have the same ASQ management actions: view queue, triage, assign, view metrics)
```
This is a confirmation step to ensure the user expects to take ASQ management actions. No role-gating is needed — all four actions are available to both roles.

Step 3: Determine the community's ASQ mapping strategy.
Test whether `sme_asq_mapped` is available:
```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"SELECT 1 FROM main.field_global_sme_usage.sme_asq_mapped LIMIT 1\",
    \"wait_timeout\": \"10s\"
  }" 2>/dev/null
```

- If the query succeeds: use `sme_asq_mapped` Variant A queries. Map the community slug to a `normalized_sme_tag` value using the mapping table in `resources/asq_coordinator_queries.md`. The `normalized_sme_tag` column covers 15+ SME domains (AI, Data Engineering, Platform, Lakebase / OLTP, etc.). If no slug-to-tag mapping is obvious, query `SELECT DISTINCT normalized_sme_tag FROM main.field_global_sme_usage.sme_asq_mapped` and present the list for the coordinator to choose from.
- If it fails (permissions error or table not found): fall back to `Technical_Specialization__c` filtering on the bronze table (Variant B queries). This covers fewer communities but always works.

Store the mapping strategy as `asq_mapping` (mapped | specialization) and the resolved filter value as `sme_tag` or `tech_specialization`.

Step 4: Present the Manage ASQ menu.

**Menu — Manage ASQ for <Community Name>** (4 actions):
1. "View ASQ queue" — description: "See all open ASQs for this community, prioritized by SLA risk"
2. "Run triage" — description: "Generate a triage checklist with status counts, SLA risks, and assignment recommendations"
3. "Assign an ASQ" — description: "Assign or reassign a specific ASQ to an SME"
4. "View SLA metrics" — description: "See SLA compliance metrics and contribution stats over a time window"

---

### Phase E.2: View and Prioritize ASQ Queue (`sme_asq_queue`)

**Trigger:** User selects "View ASQ queue" or says something like "show ASQ queue", "what's in our queue".

**Inputs:**
- `community_slug` (from E.1)
- Optional filters the user may specify: status, SLA risk, region, time window

Step 1: Fetch open ASQs.

Use query Q1 from `resources/asq_coordinator_queries.md` — Variant A (mapped) or Variant B (fallback) depending on `asq_mapping` strategy. Substitute `{community_slug}` or `{tech_specialization}` with the resolved values.

```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"<Q1 or Q2 SQL with values substituted>\",
    \"wait_timeout\": \"30s\"
  }"
```

Step 2: Handle empty results.

If the query returns 0 rows:
```
No open ASQs found for <Community Name>.

This could mean:
- The community's ASQ queue is clear (great!)
- The mapping strategy didn't match any ASQs to this community
  (current strategy: <mapped | specialization via 'X'>)

Would you like to:
1. Check recently closed ASQs instead
2. Try a different filter or specialization value
3. View SLA metrics over a historical window
4. Back to console menu
```
Do not proceed to SLA classification if there are no results.

Step 3: Classify each ASQ by Phase 1 escalation status.

For each ASQ, determine:
- **Claim status**: Is `owner_name` still a queue name (`SSA_AMER`/`SSA_EMEA`/`SSA_APAC`)? If yes → UNCLAIMED. If no → CLAIMED (an SME self-assigned).
- **Escalation level** (for unclaimed ASQs):
  - `business_days_age ≤ 2` → **ON_TRACK** — within self-assign window
  - `business_days_age > 2 AND ≤ 3` → **AT_RISK** — approaching 3-day mark
  - `business_days_age > 3` → **ESCALATE_LEAD** — needs SME Lead routing
  - `business_days_age > 3 AND age_hours > (3*24 + 24)` → **ESCALATE_BU2** — SME Lead hasn't acted, needs BU+2 intervention
- **Stale** (for claimed ASQs): `status = 'In Progress'` and no update in 14+ days → STALE

Step 4: Determine suggested next action for each ASQ.

| Current State | Suggested Action |
|--------------|-----------------|
| Unclaimed, ≤ 2 biz days | On track — within self-assign window |
| Unclaimed, 2–3 biz days (AT_RISK) | Approaching deadline — consider proactive outreach to SME members |
| Unclaimed, > 3 biz days (ESCALATE_LEAD) | **SME Lead action needed**: Review and route to an available SME |
| Unclaimed, > 3 biz days + 24h (ESCALATE_BU2) | **Urgent**: BU+2 / SSA Manager must facilitate routing |
| Claimed, In Progress | On track — SME is working it |
| Claimed, In Progress, stale (14+ days) | Request status update from owner |
| On Hold | Review hold reason, decide to resume or close |

Step 5: Present the queue.

Format as a prioritized table, grouped into sections:

```
## ASQ Queue for <Community Name>
As of: <timestamp>
Open ASQs: <N> | Unclaimed: <N> | Needs Escalation: <N>

### Escalate to BU+2 (<N>) — unclaimed > 3 biz days + 24h, SME Lead hasn't acted

| # | ASQ | Account | Status | Age (biz days) | Queue | Next Action |
|---|-----|---------|--------|---------------|-------|-------------|
| 1 | AR-12345 | Acme Corp | New | 5d | SSA_AMER | BU+2 must route now |

### Escalate to SME Lead (<N>) — unclaimed > 3 biz days

| # | ASQ | Account | Status | Age (biz days) | Queue | Next Action |
|---|-----|---------|--------|---------------|-------|-------------|
| 2 | AR-12346 | BigCo | New | 4d | SSA_EMEA | SME Lead: review and assign |

### At Risk (<N>) — unclaimed, approaching 3-day mark

| # | ASQ | Account | Status | Age (biz days) | Queue | Next Action |
|---|-----|---------|--------|---------------|-------|-------------|
| 3 | AR-12350 | MidCorp | New | 2.5d | SSA_AMER | Encourage self-assignment |

### Claimed & Active (<N>)

| # | ASQ | Account | Status | Age | Owner | Stale? |
|---|-----|---------|--------|-----|-------|--------|
| 4 | AR-12360 | GoodCo | In Progress | 5d | Jane Smith | — |
| 5 | AR-12370 | OldCo | In Progress | 20d | Bob Lee | STALE (18d no update) |
```

Step 6: Offer follow-up actions.
```
What would you like to do?
1. Assign one of these ASQs → I'll walk you through assignment
2. Acknowledge a New ASQ → I'll update the status
3. Run full triage → Get assignment recommendations for all unassigned ASQs
4. Back to console menu
```

---

### Phase E.3: Run ASQ Triage (`sme_asq_triage`)

**Trigger:** User selects "Run triage" or says "triage", "weekly triage", "prepare for triage meeting".

**Inputs:**
- `community_slug` (from E.1)
- Optional time window (default: last 7 days)

Step 1: Fetch triage summary counts.

Execute query Q2 (Variant A or B) from `resources/asq_coordinator_queries.md`:
```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"<Q2 SQL with values substituted>\",
    \"wait_timeout\": \"30s\"
  }"
```

Step 2: Fetch the full open queue (reuse Q1 from Phase E.2).

Step 3: Fetch recently closed ASQs for context using Q3 (Variant A or B).
```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"<Q3 SQL with lookback_days = time_window>\",
    \"wait_timeout\": \"30s\"
  }"
```

Step 4: Fetch candidate SMEs for assignment recommendations using Q6 (Variant A or B).
```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"<Q6 SQL with values substituted>\",
    \"wait_timeout\": \"30s\"
  }"
```

If `sme_registrations` table is not available (Q6 Variant A fails), use Q6 Variant B which derives candidates from historical ASQ owners. Alternatively, fall back to reading community members from the Sorting Hat data in the SME Registration Google Sheet (regional tabs, column W = Suggested SME Community).

Step 5: Generate assignment recommendations.

For each unassigned or mis-assigned ASQ, recommend an owner based on:
1. **Specialization match**: SME member's specialization aligns with the ASQ's `Technical_Specialization__c`.
2. **Current load**: Prefer members with fewer active ASQs (`current_active_asqs` from Q7).
3. **Prior experience**: Members with more historical ASQ contributions are preferred.
4. **Region alignment**: Match the ASQ's regional queue to the SME member's region when possible.

Step 6: Present the triage checklist.

Format as a markdown document suitable for pasting into a meeting doc:

```
# ASQ Triage for <Community Name>
Date: <date>
Prepared by: SME Community Assistant

## Summary
- **Unclaimed (in SSA queue):** <N>
  - Escalate to BU+2 (> 3 biz days + 24h): <N>
  - Escalate to SME Lead (> 3 biz days): <N>
  - At risk (approaching 3 biz days): <N>
  - On track (< 2 biz days): <N>
- **Claimed & active:** <N> (stale > 14d: <N>)
- **On Hold:** <N>
- **Closed this period:** <N>

## Action Items

### Escalations (BU+2 / SSA Manager)
- [ ] **AR-12345** (Acme Corp) — Unclaimed 5 biz days, SSA_AMER queue.
  → BU+2 must route. Recommend: **<SME Name>** (lowest load, region match)

### SME Lead Routing (unclaimed > 3 biz days)
- [ ] **AR-12346** (BigCo) — Unclaimed 4 biz days, SSA_EMEA queue.
  → Assign to **<Recommended SME>** (reason: expertise match, 1 active ASQ)

### At Risk (approaching 3-day mark)
- [ ] **AR-12350** (MidCorp) — Unclaimed 2.5 biz days. → Post in Slack channel encouraging self-assignment

### Stale (claimed but no update > 14 days)
- [ ] **AR-12360** (GoodCo) — Assigned to Jane Smith, 18d since last update.
  → Request status update

### Recently Closed (for reference)
| ASQ | Account | Owner | Effort | Closure Note |
|-----|---------|-------|--------|-------------|
| AR-12300 | OldCo | Bob Lee | 3d | UC migration completed |

## Assignments Summary
| SME Member | Role | Active ASQs | Recommended New | Total if Accepted |
|-----------|------|-------------|-----------------|-------------------|
| Alice Chen | Contributor | 1 | AR-12346 | 2 |
| Bob Lee | Contributor | 2 | — | 2 |
| Carlos Ruiz | Coordinator | 0 | AR-12345 | 1 |
```

Step 7: Offer to execute assignments.
```
Would you like me to:
1. Execute all recommended assignments (I'll confirm each one)
2. Assign specific ASQs from the list
3. Copy this triage checklist to clipboard
4. Back to console menu
```

If the user chooses option 1, iterate through each recommended assignment and execute Phase E.4 for each, asking for confirmation before each write.

---

### Phase E.4: Assign / Reassign an ASQ (`sme_asq_assign`)

**Trigger:** User selects "Assign an ASQ", picks a specific ASQ from the queue/triage view, or says "assign AR-12345 to alice@databricks.com".

**Inputs:**
- `asq_id` — The ASQ record ID or ASQ number (e.g., AR-12345). If a number is given, resolve to ID first.
- `community_slug` (from E.1)
- `assignee` — Databricks email or name of the target SME
- Optional note

Step 1: Resolve the ASQ.
If the user provided an ASQ number (AR-XXXXX) instead of an ID:
```bash
sf data query -q "SELECT Id, Name, Status__c, OwnerId, Owner.Name, Account_Name__c, Request_Description__c, Request_Status_Notes__c FROM ApprovalRequest__c WHERE Name = '<ASQ_NUMBER>'" \
  --target-org $SF_ORG --json
```

Step 2: Resolve the assignee.
Look up the assignee's Salesforce User ID:
```bash
sf data query -q "SELECT Id, Name, Email FROM User WHERE Email = '<ASSIGNEE_EMAIL>' AND IsActive = true" \
  --target-org $SF_ORG --json
```
If the user gave a name instead of email, search by name:
```bash
sf data query -q "SELECT Id, Name, Email FROM User WHERE Name LIKE '%<ASSIGNEE_NAME>%' AND IsActive = true" \
  --target-org $SF_ORG --json
```
If multiple results, present options and ask user to select.

Step 3: Show confirmation.

**IMPORTANT:** This is a write to Salesforce — always confirm before executing.

Present the full change summary and use AskUserQuestion to get explicit confirmation:
```
I'll make the following changes to ASQ <ASQ_NUMBER>:

  Current owner: <current_owner_name>
  New owner: <assignee_name> (<assignee_email>)
  Community: <community_name>
  Status change: <current_status> → Under Review (if currently New)

  Assignment note to prepend:
  "<COORDINATOR_INITIALS> <DATE>: Assigned to <assignee_name> by <coordinator_name>
   via SME Community <community_name>. Next: <next_step>."

  Chatter post:
  "SME Community Assignment: <community_name> coordinator <coordinator_name>
   assigned this ASQ to <assignee_name>."

Proceed with this assignment?
```

Do NOT proceed without explicit user confirmation.

Step 4: Execute the assignment.

Run the sf CLI commands from `resources/asq_coordinator_queries.md` "Assign an ASQ" section:

```bash
# 4a. Update owner
sf data update record -s ApprovalRequest__c -i <ASQ_ID> \
  -v "OwnerId='<ASSIGNEE_SF_USER_ID>'" \
  --target-org $SF_ORG --json

# 4b. Update status if currently 'New'
sf data update record -s ApprovalRequest__c -i <ASQ_ID> \
  -v "Status__c='Under Review'" \
  --target-org $SF_ORG --json

# 4c. Prepend assignment note
python3 $SF_UPDATE_SCRIPT prepend <ASQ_ID> \
  "<COORDINATOR_INITIALS> <DATE>: Assigned to <assignee_name> by <coordinator_name> via SME Community <community_name>. Next: <next_step>." \
  --org $SF_ORG

# 4d. Post Chatter comment
python3 $SF_UPDATE_SCRIPT chatter <ASQ_ID> \
  "SME Community Assignment: <community_name> coordinator <coordinator_name> assigned this ASQ to <assignee_name>." \
  --org $SF_ORG
```

Step 5: Read-back verification.
```bash
sf data query -q "SELECT Id, Name, OwnerId, Owner.Name, Status__c FROM ApprovalRequest__c WHERE Id = '<ASQ_ID>'" \
  --target-org $SF_ORG --json
```

Verify:
- `OwnerId` matches the assignee's Salesforce User ID
- `Status__c` is no longer 'New'

Step 6: Report result.
```
Assignment complete for ASQ <ASQ_NUMBER>:
  Owner: <verified_owner_name>
  Status: <verified_status>
  Note prepended: yes
  Chatter posted: yes
```

**Error handling:**
- If the `sf data update record` command fails with a permissions error, report:
  ```
  Assignment failed: <error_message>

  This usually means your Salesforce user doesn't have permission to reassign this ASQ.
  Manual fallback: Open the ASQ in Salesforce and change the owner:
  https://databricks.lightning.force.com/lightning/r/ApprovalRequest__c/<ASQ_ID>/view
  ```
- If the ASQ ID is invalid, report the error and ask the user to verify.
- If the assignee is not found in Salesforce, report and ask for a corrected email.

---

### Phase E.5: View ASQ SLA Metrics (`sme_asq_sla`)

**Trigger:** User selects "View SLA metrics" or says "show ASQ metrics", "SLA report", "how are we doing on ASQs".

**Inputs:**
- `community_slug` (from E.1)
- Optional time window (default: last 30 days). Accept "last 7 days", "last 90 days", "Q1", "this quarter", etc.

Step 1: Resolve the time window to days.
Map natural language to `:lookback_days`:
- "last 7 days" → 7
- "last 30 days" → 30
- "last quarter" / "last 90 days" → 90
- "this quarter" → days since start of current quarter
- Default: 30

Step 2: Fetch SLA metrics.

Execute query Q4 (Variant A or B) from `resources/asq_coordinator_queries.md`:
```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"<Q4 SQL with values substituted>\",
    \"wait_timeout\": \"30s\"
  }"
```

Step 3: Fetch per-member contributions.

Execute query Q5 (Variant A or B) from `resources/asq_coordinator_queries.md`:
```bash
databricks api post /api/2.0/sql/statements \
  --profile logfood \
  --json "{
    \"warehouse_id\": \"$WAREHOUSE_ID\",
    \"statement\": \"<Q5 SQL with values substituted>\",
    \"wait_timeout\": \"30s\"
  }"
```

Step 4: Present the narrative summary.

**Caveat:** "Time to claim" measures when the ASQ's owner changed from an SSA queue to an individual SME. This is approximate — uses `Approved_Date__c` or `LastModifiedDate` as proxy. There is no explicit "claimed_at" timestamp.

**Expertise match** (Variant A only): `expertise_tag_match` from `sme_asq_mapped` indicates whether the assigned SME's registered specialization matched the ASQ's domain. This is the closest proxy to first-match success rate.

```
## ASQ SLA Report for <Community Name>
Period: <start_date> – <end_date> (<lookback_days> days)

### Volume
- **Opened:** <total_asqs> ASQs
- **Closed:** <closed_asqs>
- **Currently open:** <open_asqs>
- **Hashtag-routed (Phase 1):** <N> (ASQs with #<slug>_sme in description)

### Phase 1 SLA Compliance
| Metric | Average | Median | % Within Target |
|--------|---------|--------|----------------|
| Time to claim* (target: 3 biz days) | <avg> days | <median> days | <pct>% |
| Time to close | <avg> days | <median> days | — |
| Expertise match rate | — | — | <pct>% |

*Time to claim is approximate (see caveat above).

### Escalation Summary
- ASQs that required SME Lead routing (> 3 biz days unclaimed): <N> (<pct>%)
- ASQs that escalated to BU+2 (Lead didn't act within 24h): <N> (<pct>%)

### Community Contributions
| SME Member | Role | Total ASQs | Completed | In Progress | Avg Effort (days) |
|-----------|------|-----------|-----------|-------------|-------------------|
| Alice Chen | Contributor | 8 | 6 | 2 | 3.5 |
| Bob Lee | Contributor | 5 | 5 | 0 | 2.0 |
| Carlos Ruiz | Coordinator | 3 | 2 | 1 | 4.0 |

### Assessment
<Generate a 2-3 sentence narrative assessment based on the data. Examples:>
- "In the last 30 days, the AI SME community handled 16 ASQs. 75% were self-assigned within 3 business days. 4 required SME Lead routing, of which 1 escalated to BU+2. Alice Chen led contributions with 8 ASQs (6 completed). Expertise match rate: 62%."
- "Escalation rate is high: 40% of ASQs went unclaimed past 3 business days. Consider posting reminders in #sme-ai-global or expanding the contributor pool."
```

Step 5: Offer follow-up actions.
```
Would you like to:
1. Drill into a specific ASQ or SME member's contributions
2. Compare with a different time window
3. Export this report (I'll format it for pasting into a Confluence page or meeting doc)
4. Back to console menu
```

---

## Safety & Idempotency

### Before Creating Anything
Always search first. Before creating a Confluence page, Slack channel, Drive folder, or registration row, check if it already exists. If it does, inform the user and offer to update/use the existing resource.

### Destructive Operations Require Confirmation
The following operations MUST have explicit user confirmation via AskUserQuestion before executing:
- Archiving a Slack channel
- Renaming a Slack channel
- Modifying an existing Confluence page (adding banners, updating governance, updating content)
- Posting announcements in Slack channels (revitalization, migration redirects)
- Updating registration sheet leadership columns
- Changing Google Group ownership or membership
- Moving files between Drive folders
- Deleting any resource
- **Assigning or reassigning an ASQ owner in Salesforce** (Manage ASQ)
- **Changing ASQ status in Salesforce** (Manage ASQ)
- **Posting Chatter comments on ASQ records** (Manage ASQ)

### Non-Destructive Migration
Mode B migration NEVER deletes original assets. It:
- Creates new canonical resources alongside old ones
- Adds redirect banners to old Confluence pages (preserving original content)
- Posts redirect messages in old Slack channels (without archiving)
- Documents old Drive folder locations (without moving files unless user approves)

### Operation Logging
After completing any mode, update the registration sheet with:
- Construct IDs and URLs for all created/modified resources
- Status (active, migrating, archived, pending)
- Timestamp in the Notes column

### Error Recovery
If any step fails mid-execution:
- Report the error to the user
- Continue with remaining steps if they're independent
- Mark failed items in the summary as FAILED with the error message
- All successfully created resources remain valid (no rollback needed)

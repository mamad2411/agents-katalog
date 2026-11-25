---
name: draft-replies-docs
description: Scan Google Drive documents, JIRA tickets, and Confluence pages for open action items assigned to you — comments, assigned questions, meeting note tasks — and create a summary Google Doc. Use when the user mentions open action items, document comments, things assigned to me, meeting notes tasks, JIRA action items, Confluence tasks, document review, or doc inbox.
---

# Draft Replies — Documents & Tickets

Scan Google Drive documents, JIRA tickets, and Confluence pages for open action items assigned to you, then create a summary Google Doc with a linked table of all items.

## Capabilities

- Scan Google Drive documents (Docs, Sheets, Slides) for open comments, suggestions, and assigned questions directed at the user
- Parse meeting notes and agendas for action items listed under the user's name
- Scan JIRA for open tickets assigned to the user (including ES tickets, comments requesting action)
- Scan Confluence for open inline comments and tasks assigned to the user
- Classify items by priority (High / Medium / Low) and source
- Create a new Google Doc in the user's Drive with a comprehensive table of all open items
- Include direct links to each source document/ticket, who assigned the item, when, and optional due dates

## Prerequisites

**Run `/google-auth` first** to authenticate with Google Workspace.

```bash
GOOGLE_AUTH=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | head -1)
python3 "$GOOGLE_AUTH" status || python3 "$GOOGLE_AUTH" login
TOKEN=$(python3 "$GOOGLE_AUTH" token)
```

For JIRA/Confluence scanning, the `fe-jira-tools` plugin must be configured with valid credentials.

## Input

The skill accepts optional arguments for timeframe and source filter:

- **Timeframe** (required — prompt user if not provided):
  - **Relative**: Number of days to look back, e.g. `7`, `30`, `14`
  - **Absolute range**: Two dates in DD-MM-YYYY format, e.g. `01-01-2025 09-03-2026`
  - If the user does not specify a timeframe, **ask them** before proceeding: "What timeframe should I check? (e.g. 'last 30 days', or 'between 01-01-2025 and 09-03-2026')"
- **Source filter** (default: "all"): Which sources to scan — "gdrive", "jira", "confluence", or "all"

Examples:
- `/draft-replies-docs` — prompts for timeframe, then scans all sources
- `/draft-replies-docs 30` — scan last 30 days, all sources
- `/draft-replies-docs 10 gdrive` — scan last 10 days, Google Drive only
- `/draft-replies-docs 01-01-2025 09-03-2026` — scan Jan 2025 to Mar 2026, all sources
- `/draft-replies-docs 30 jira` — last 30 days, JIRA only

## Workflow

### Phase 1: Authenticate and Identify the User

1. Ensure Google auth is active:

```bash
GOOGLE_AUTH=$(find ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | head -1)
python3 "$GOOGLE_AUTH" status || python3 "$GOOGLE_AUTH" login
TOKEN=$(python3 "$GOOGLE_AUTH" token)
```

2. Get the user's Google identity:

```bash
curl -s "https://www.googleapis.com/oauth2/v1/userinfo" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

3. Store: `user_email`, `user_name`, `user_id` (Google account ID). These are needed to match comment mentions, JIRA assignees, and action item ownership.

4. For JIRA/Confluence, identify the user's Atlassian account:

```bash
# Use the fe-jira-tools plugin's authentication
# The JIRA skill handles auth — invoke it to get the user's JIRA identity
```

### Phase 2: Load or Analyze Writing Style (Cached)

The writing style analysis helps classify items and generate contextual action summaries. To save time and cost, the result is cached locally and only regenerated quarterly or on first use.

**Cache location**: `~/.claude/personal-plugins/style-cache/docs-style-profile.md`

1. **Check for cached profile**:
   - Read the file `~/.claude/personal-plugins/style-cache/docs-style-profile.md`
   - If the file exists, check the `generated_date` in its YAML frontmatter
   - If the profile exists AND `generated_date` is less than 90 days old → **use the cached profile**, skip to Phase 3
   - If the file does not exist OR `generated_date` is more than 90 days old → **regenerate** (continue below)

2. **Regenerate style profile** (only when cache is missing or stale):
   - Fetch the user's recent Google Doc comments (last 3 months) from 10-15 actively edited documents
   - Also fetch 20-30 of the user's recent JIRA comments using JQL: `comment ~ "user_name" AND updated >= "-90d"`
   - Analyze ~50-100 comments for:
     - **Language mix**: What percentage is English vs German?
     - **Comment length**: Short (1 sentence), medium (2-3 sentences), or detailed (4+)?
     - **Tone**: Direct/terse vs explanatory, formal vs casual
     - **Action language**: How does the user phrase requests, approvals, questions?
   - Build a style profile summary

3. **Save the profile to cache**:
   - Write the style profile to `~/.claude/personal-plugins/style-cache/docs-style-profile.md` with YAML frontmatter:
   ```markdown
   ---
   generated_date: YYYY-MM-DD
   platform: docs
   comment_count: <number of comments analyzed>
   ---

   <style profile summary text>
   ```

4. Use the style profile (cached or freshly generated) to guide classification in Phase 5 and action item summarization in Phase 6.

### Phase 3: Scan Google Drive for Documents with Open Comments

#### 2a: Find documents with open comments directed at the user

1. **Search for documents with unresolved comments mentioning the user**. Use the Google Drive API to list files that have open comments:

```bash
# List files the user owns or that are shared with them, modified within timeframe
# For relative timeframe (e.g. 30 days): calculate the ISO date
SINCE_DATE=$(date -v-${DAYS}d +%Y-%m-%dT00:00:00 2>/dev/null || date -d "${DAYS} days ago" +%Y-%m-%dT00:00:00)

# Search for Google Docs, Sheets, and Slides modified in the timeframe
curl -s "https://www.googleapis.com/drive/v3/files?q=(mimeType='application/vnd.google-apps.document'+or+mimeType='application/vnd.google-apps.spreadsheet'+or+mimeType='application/vnd.google-apps.presentation')+and+modifiedTime>'${SINCE_DATE}'&fields=files(id,name,mimeType,modifiedTime,owners,webViewLink)&pageSize=100&orderBy=modifiedTime+desc" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

2. **Batch-fetch comments for multiple documents** — instead of fetching comments one file at a time, process files in batches of 10 to reduce round-trips:

```bash
# Batch approach: collect file IDs, then fetch comments in groups of 10
# For each batch of 10 files, make parallel requests (or sequential in a tight loop)

# For each file in the batch:
curl -s "https://www.googleapis.com/drive/v3/files/${FILE_ID}/comments?fields=comments(id,content,author(displayName,emailAddress),createdTime,modifiedTime,resolved,replies(content,author(displayName,emailAddress),createdTime),anchor,quotedFileContent)&includeDeleted=false" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

**Optimization**: Before fetching comments, pre-filter files to reduce the batch size:
- Skip files where the user is the sole editor (no comments from others possible)
- Skip files with `modifiedTime` older than the timeframe AND no comment activity
- Prioritize files with recent `modifiedTime` (more likely to have pending comments)
- Cap at 50 files maximum — if more are found, process only the 50 most recently modified

**Batch processing implementation**:
```python
# Process files in batches of 10
for batch_start in range(0, len(file_ids), 10):
    batch = file_ids[batch_start:batch_start + 10]
    # Fetch comments for all 10 files in this batch
    for file_id in batch:
        comments = fetch_comments(file_id, token)
        # Filter and collect relevant comments
    # Brief pause between batches to respect rate limits
```

3. **Filter comments** to find those relevant to the user:
   - Comments where the user is **@mentioned** (look for `+user_email` or user's name in comment `content`)
   - Comments where the user is **assigned** (Google Docs "Assign to" feature — the comment content will contain `_Assigned to [user]_` or similar)
   - Comments on content the user authored (if identifiable)
   - Skip comments that are already **resolved** (`resolved: true`)
   - Skip comments the user themselves wrote (unless they contain an assigned action)
   - **Important**: Also check `replies` array — if the user has already replied to the comment, it may still be unresolved but the user has already responded. Flag these as lower priority.

4. **For each matching comment, extract**:
   - `document_name` — the file name
   - `document_link` — webViewLink to the file
   - `comment_text` — the comment content
   - `commenter_name` — who wrote the comment
   - `commenter_email` — their email
   - `created_date` — when the comment was created
   - `quoted_content` — the text the comment is anchored to (if available from `quotedFileContent`)
   - `has_user_reply` — whether the user already replied in the comment thread

#### 2b: Scan Google Docs for meeting notes with action items

1. **Identify meeting notes**: From the files found in 2a, identify documents that are likely meeting notes based on:
   - File name patterns: contains "meeting notes", "minutes", "agenda", "standup", "sync", "1:1", "weekly", "action items", "MoM", "Besprechungsnotizen", "Protokoll"
   - Also search specifically for meeting note documents:

```bash
# Search for meeting notes documents in the timeframe
curl -s "https://www.googleapis.com/drive/v3/files?q=mimeType='application/vnd.google-apps.document'+and+modifiedTime>'${SINCE_DATE}'+and+(name+contains+'meeting'+or+name+contains+'notes'+or+name+contains+'agenda'+or+name+contains+'minutes'+or+name+contains+'action+items'+or+name+contains+'sync'+or+name+contains+'standup'+or+name+contains+'1:1'+or+name+contains+'Protokoll')&fields=files(id,name,modifiedTime,webViewLink)&pageSize=50&orderBy=modifiedTime+desc" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

2. **Read the document content** to find action items assigned to the user:

```bash
# Export Google Doc as plain text to search for action items
curl -s "https://www.googleapis.com/drive/v3/files/${FILE_ID}/export?mimeType=text/plain" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

3. **Parse action items** from the document text. Look for patterns like:
   - `[ ] @matthias ...` or `[ ] Matthias: ...` (unchecked checkbox with user's name)
   - `Action: Matthias — ...` or `AI: Matthias — ...`
   - `TODO: Matthias ...` or `TODO (@matthias) ...`
   - Bullet points or numbered lists under an "Action Items" / "Actions" / "Next Steps" / "Follow-ups" heading that mention the user's first name, last name, or email
   - `Owner: Matthias` patterns in table rows
   - German patterns: `Aufgabe: Matthias`, `Verantwortlich: Matthias`
   - **Skip** items that appear to be checked/completed: `[x]`, `[X]`, ~~strikethrough~~, or marked "Done"/"Erledigt"

4. **For each action item found, extract**:
   - `document_name` — the meeting note file name
   - `document_link` — webViewLink
   - `action_text` — the action item description
   - `assigned_by` — infer from meeting context (document owner or meeting organizer if identifiable)
   - `created_date` — document modified date or meeting date if parseable from the document
   - `due_date` — if a date/deadline is mentioned alongside the action item (e.g. "by Friday", "due 2025-03-15", "EOW")

#### 2c: Scan Google Docs suggestions (optional)

1. For documents where the user is the owner, check for **pending suggestions** (edits proposed by others that the user needs to accept/reject):

```bash
# Get suggestions for a document — use the Google Docs API
curl -s "https://docs.googleapis.com/v1/documents/${FILE_ID}?fields=suggestedDocumentStyleChanges,suggestedNamedStylesChanges,body" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

2. If the document contains suggestion IDs in the body elements (`suggestedInsertionIds`, `suggestedDeletionIds`), flag it as having pending suggestions. Record:
   - `document_name`, `document_link`
   - `suggestion_count` — how many suggestions are pending
   - `created_date` — approximate from document modification time

### Phase 3: Scan JIRA for Open Action Items

Use the `fe-jira-tools` JIRA skill to query for open items. **Important**: The user may not be directly assigned or mentioned in JIRA tickets. The most effective approach is a multi-layered search that also covers tickets from the user's direct reports and team members.

#### 3a: Open JIRA tickets assigned to the user

1. **Search for assigned tickets** within the timeframe:

```
JQL: assignee = currentUser() AND status NOT IN (Done, Closed, Resolved) AND created >= "YYYY-MM-DD" ORDER BY priority DESC, updated DESC
```

2. **Also search for ES (Engineering Support) tickets** where the user is mentioned or assigned:

```
JQL: project = ES AND (assignee = currentUser() OR text ~ "user_email" OR text ~ "user_first_name.user_last_name") AND status NOT IN (Done, Closed, Resolved) AND created >= "YYYY-MM-DD" ORDER BY priority DESC, updated DESC
```

3. **For each ticket, extract**:
   - `ticket_key` — e.g. "ES-12345"
   - `ticket_link` — direct URL to the JIRA ticket (`https://databricks.atlassian.net/browse/{ticket_key}`)
   - `summary` — ticket title/summary
   - `reporter` — who created/assigned the ticket (the "assigner")
   - `created_date` — when the ticket was created
   - `due_date` — if a due date is set on the ticket
   - `priority` — JIRA priority (Blocker, Critical, Major, Minor, Trivial)
   - `status` — current status (Open, In Progress, etc.)
   - `last_comment` — the most recent comment text (if it contains a question or request directed at the user)

#### 3b: JIRA comments requesting action from the user

1. **Search for tickets where someone mentioned the user in a comment**:

```
JQL: comment ~ "user_last_name" AND status NOT IN (Done, Closed, Resolved) AND updated >= "YYYY-MM-DD" ORDER BY updated DESC
```

2. For each ticket found, fetch comments and check for:
   - Comments mentioning the user that haven't been responded to
   - Questions directed at the user
   - Requests for the user's input or review

3. **Deduplicate**: If a ticket is already found in 3a, merge the information rather than creating a duplicate entry. Add comment context to the existing item.

#### 3c: Heated ES tickets from team members (escalation radar)

Leaders are often not directly tagged on ES tickets, but they need visibility into heated escalations from their team. This step searches for open ES tickets filed by or involving the user's direct reports that show signs of being stuck or escalated.

1. **Identify team members**: Get the user's direct reports from their profile or org data. Common sources:
   - Check `~/.vibe/profile` for team member list
   - Use the `fe-internal-tools:databricks-org` skill to look up direct reports
   - Fall back to known team member emails if available

2. **Search for open ES tickets from team members**:

```
JQL: project = ES AND status NOT IN (Done, Closed, Resolved) AND reporter IN ("report1@databricks.com", "report2@databricks.com", ...) AND updated >= "YYYY-MM-DD" ORDER BY priority DESC, updated DESC
```

Also search by watcher:
```
JQL: project = ES AND status NOT IN (Done, Closed, Resolved) AND watcher IN ("report1@databricks.com", "report2@databricks.com", ...) AND updated >= "YYYY-MM-DD" ORDER BY priority DESC, updated DESC
```

3. **Identify "heated" tickets** — tickets that need leadership attention. A ticket is heated if:
   - Priority is **Blocker** or **Critical**
   - Status is still **To Do** but the ticket is **>7 days old** (stuck)
   - Multiple follow-up comments asking for updates (>3 comments with urgency language)
   - Comments contain escalation language: "urgent", "blocking", "customer waiting", "production impact", "critical", "escalate", "please help"
   - **Competitive risk**: ticket mentions a competitor (Snowflake, Exasol, BigQuery, Synapse, Redshift)
   - No engineering response despite multiple SA/AE comments
   - Ticket age >14 days with status still in "To Do" or "Open"

4. **Also search Gmail** for ES ticket threads sent TO the user (escalation emails):

```bash
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=subject:%22ES-%22+to:${USER_EMAIL}+after:${SINCE_DATE}+-subject:%22Confidential%22&maxResults=30" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

For each email thread, check the ES ticket status in JIRA. If still open, add to findings.

5. **For each heated ticket, extract**:
   - All fields from 3a
   - `team_member` — which direct report is involved
   - `customer` — affected customer (from ticket description or labels)
   - `escalation_indicators` — list of reasons this is flagged as heated
   - `days_open` — how long the ticket has been open
   - `days_since_eng_response` — how long since an engineering (non-FE) person responded

### Phase 4: Scan Confluence for Open Action Items

Use the `mcp__confluence__*` MCP tools for all Confluence operations. The approach is multi-layered: use the tasks API first (most reliable), then fall back to page-level searches for `<ac:task>` markup, and finally check inline comments.

#### 4a: Confluence tasks assigned to the user (Tasks API)

1. **Search for incomplete tasks assigned to the user** using the Confluence tasks API directly:

```
# Via mcp__confluence__search_confluence_pages with task-specific CQL
CQL: type = "task" AND assignee = currentUser() AND status = "incomplete" AND created >= "YYYY-MM-DD" ORDER BY created DESC
```

If the tasks CQL type is not available, use the Confluence REST API through the MCP tool:

```
GET /wiki/rest/tasks/1.0/tasks?status=incomplete&assignee={user_account_id}&limit=100
```

2. **Also search for tasks assigned by email/name** (backup if `currentUser()` doesn't resolve):

```
CQL: type = "task" AND text ~ "user_email" AND status = "incomplete" AND created >= "YYYY-MM-DD"
```

#### 4b: Scan pages for `<ac:task>` elements mentioning the user

Full-text CQL search for the user's name is unreliable (returns role/reference pages). Instead, search for pages with `<ac:task>` markup that reference the user.

1. **Search for pages in key spaces** the user is likely involved in. Focus on spaces where action items are common:

```
CQL: type = page AND space IN ("FE", "FEEMEA", "SA", "ENG", "DAIS") AND lastmodified >= "YYYY-MM-DD" AND (text ~ "ac:task" OR text ~ "action item") ORDER BY lastmodified DESC
```

2. **For each candidate page**, use `mcp__confluence__get_confluence_page_content` to fetch the page body and parse for:
   - `<ac:task>` elements where the `<ri:user>` matches the user's account ID or email
   - `<ac:task-status>` is `incomplete`
   - Extract the task body text from `<ac:task-body>` elements
   - Also detect plain-text action items: `[ ] @matthias`, `AI: Matthias`, `TODO: Matthias`

3. **Limit page scanning** to 30 most recently modified pages to avoid excessive API calls.

#### 4c: Inline comments mentioning the user

1. **Search for pages where the user is mentioned in inline comments**:

```
CQL: type = comment AND text ~ "user_first_name" AND container.lastmodified >= "YYYY-MM-DD" ORDER BY created DESC
```

2. For each comment found, check:
   - Is the comment **unresolved**?
   - Does it mention the user by name, email, or @-mention?
   - Has the user already replied in the comment thread?

3. **Get the parent page context** for each relevant comment using `mcp__confluence__get_confluence_page_content` to provide surrounding context.

#### 4d: Extract Confluence items

**For each Confluence item found (tasks, comments), extract**:
   - `page_title` — the Confluence page name
   - `page_link` — direct URL to the page (e.g. `https://databricks.atlassian.net/wiki/spaces/{space}/pages/{pageId}/{title}`)
   - `task_text` or `comment_text` — the action item or comment content
   - `assigned_by` — who created the task or comment
   - `created_date` — when it was created
   - `due_date` — if a due date is set on the Confluence task
   - `space_name` — the Confluence space
   - `source_type` — "task_api", "ac_task_markup", or "inline_comment"

**Deduplicate**: Tasks found via both the Tasks API (4a) and page scanning (4b) should be merged.

### Phase 4e: Find Unfollowed Promises in Comments

Search for comments or replies the user wrote that contain follow-up language — promises the user made but may not have kept.

1. **Search for promise comments in Google Drive**:
   - From the comments already fetched in Phase 3a, scan for comments/replies written BY the user that contain promise language:
     - **English**: "I'll update", "will add", "let me fix", "I'll take a look", "will review", "come back to you", "will share", "I'll get this done", "by end of week", "by Friday", "tomorrow"
     - **German**: "mache ich", "schaue ich mir an", "kummere mich", "erledige ich", "trage ich ein", "bis Ende der Woche"

2. **Search for promise comments in JIRA**:
   - From the JIRA tickets already fetched in Phases 4a-4c, scan the user's comments for promise language
   - Also search directly: `JQL: comment ~ "user_name" AND comment ~ "will" AND updated >= "YYYY-MM-DD"`

3. **Check for follow-through**: For each promise found:
   - **Google Drive**: Check if the user posted a subsequent reply in the same comment thread after the promise, or if the comment was resolved
   - **JIRA**: Check if the user posted a subsequent comment in the ticket after the promise, or if the ticket status changed (e.g., moved to "In Progress" or "Done")
   - **Confluence**: Check if the user completed the associated task or posted a follow-up

4. **Classify unfollowed promises**:
   - Promise >7 days old with no follow-through → **HIGH priority**
   - Promise <=7 days old with no follow-through → **MEDIUM priority**
   - Record: `promise_text`, `source_type`, `source_link`, `promise_date`, `days_ago`, `recipient` (who the promise was made to)

### Phase 5: Classify All Items

Combine all items from Google Drive, JIRA, and Confluence and classify into priority tiers:

**HIGH PRIORITY** — Direct action required:
- JIRA tickets with priority Blocker or Critical
- JIRA ES tickets with customer impact
- Google Doc comments that are direct questions or approval requests
- Action items from meeting notes with explicit deadlines that have passed or are within 3 days
- Confluence tasks with overdue due dates
- Items older than 14 days that remain unaddressed (likely forgotten)
- **Broken promises (>7 days old)**: Unfollowed promises from Phase 4e where more than 7 days have elapsed

**MEDIUM PRIORITY** — Response or action warranted:
- JIRA tickets with priority Major
- Google Doc comments requesting review or input
- Meeting note action items without explicit deadlines
- Confluence inline comments with questions
- Items between 3-14 days old
- **Recent unfollowed promises (<=7 days old)**: Promises from Phase 4e that the user may still intend to follow through on but should be reminded about

**LOW PRIORITY** — Informational or quick action:
- JIRA tickets with priority Minor or Trivial
- Google Doc comments that are FYI or acknowledgment-type
- Suggestions pending on documents the user owns
- Items less than 3 days old (still fresh)

### Phase 5b: Validate Source Links (REQUIRED)

Before creating the summary document, validate that EVERY item has a clickable `source_url`. Items without a link are useless in the summary doc because the user cannot navigate to the original.

**Validation gate**: Iterate over ALL collected items and verify each has a non-empty `source_url`:

1. **Google Drive items**: Must have `webViewLink` from the Drive API. If missing, construct as `https://docs.google.com/document/d/{fileId}/edit` (for Docs) or `https://docs.google.com/spreadsheets/d/{fileId}/edit` (for Sheets) or `https://docs.google.com/presentation/d/{fileId}/edit` (for Slides).

2. **JIRA items**: Must have `ticket_link`. If missing, construct as `https://databricks.atlassian.net/browse/{ticket_key}`.

3. **Confluence items**: Must have `page_link`. If missing, construct as `https://databricks.atlassian.net/wiki/spaces/{space_key}/pages/{pageId}`.

4. **Unfollowed promises**: Must have the `source_link` from the original promise location (Google Drive comment URL, JIRA ticket URL, or Confluence page URL).

**For any item missing a link**, construct it using the fallback formulas above. Log a warning but do NOT skip the item.

### Phase 5c: Draft Suggested Responses

For every item collected, draft a **meaningful, detailed suggested response** that the user can copy-paste into the original source (Google Doc comment reply, JIRA comment, Confluence reply, or email). These responses are a core deliverable of the skill — they should be high quality, substantive, and directly actionable.

**Quality guidelines — responses should be detailed and meaningful, not generic placeholders:**

- **Address the specific content** of the comment, question, or action item — reference what was asked, what was proposed, or what needs to happen
- **Use the user's writing style** from the cached style profile (Phase 2) — match language (German vs English), tone, and formality
- **Include context from the source** — reference the document name, ticket number, or meeting where the item originated
- **Propose a concrete next step or answer** — don't write vague "I'll look into it" responses. Instead, draft what the actual answer or action would be based on the available context
- **For questions the skill cannot answer** (requires domain knowledge, customer specifics, or internal data), explicitly state what information is needed and draft a response that asks the right follow-up question or commits to a specific timeline
- **Match the medium** — Google Doc comment replies should be concise but complete (2-4 sentences); JIRA comments can be longer and more structured; Confluence replies should match the page's style

**Drafting rules by source type:**

1. **Google Drive comments** (questions directed at the user):
   - Read the full comment thread context (from Phase 3a) to understand what's being asked
   - If the comment references specific document content (via `quotedFileContent`), address that content directly
   - If multiple people are in the comment thread, address the specific question directed at the user
   - Example: Instead of "Will review" → "Good point about the Q2 timeline — I think we should push the migration to April given the dependency on the Lakebase rollout. I'll update the timeline section and tag you for another look."

2. **Meeting note action items**:
   - Draft what completing the action item would look like — the response is a status update or completion note
   - If the action has a deadline, acknowledge it
   - Example: Instead of "Working on it" → "Updated the architecture diagram to include the new Lakebase integration path. Added the cost comparison table as discussed. Ready for review — see section 3.2 in the doc."

3. **JIRA tickets**:
   - For assigned tickets: draft a status update comment acknowledging the ticket and outlining next steps
   - For comment mentions: draft a reply that answers the question or provides the requested input
   - For heated ES tickets: draft an internal coordination response (who to loop in, what the ask is for engineering)
   - Example: Instead of "Looking into this" → "Reviewed the customer's error logs — this looks like the same WAP-429 issue we saw with [other customer]. The workaround is to increase the timeout on the connector config. I'll draft a customer-facing response and loop in the assigned support engineer for the permanent fix timeline."

4. **Confluence tasks/comments**:
   - Draft a reply that addresses the task or answers the inline comment
   - Reference the page context where relevant

5. **Unfollowed promises** (from Phase 4e):
   - Draft a follow-up message that acknowledges the delay and delivers on the promise (or explains the revised plan)
   - Be specific about what was promised and what's being delivered now
   - Example: Instead of "Sorry for the delay" → "Apologies for the delayed follow-up — here's the competitive analysis doc I mentioned: [link]. I've included the Snowflake vs Databricks comparison for the three use cases we discussed. Let me know if you need the pricing section expanded."

**Store the suggested response** alongside each item as `suggested_response`. This field is REQUIRED — every item in the summary doc must have one. If the context is insufficient to draft a meaningful response, explicitly say what's missing and draft a response that commits to a timeline (e.g., "I'll review this by [day] and get back to you with [specific deliverable].").

### Phase 6: Create Summary Google Doc

**CRITICAL — Clickable links**: Every link in the summary document — especially in the "Document / Ticket" table column and in the detail sections — MUST be a clickable hyperlink, not plain text. The user needs to click directly from the summary doc to the source.

**Preferred approach**: Use the `mcp__google__docs_document_create_from_markdown` tool with a markdown file. This tool supports `[display text](url)` links in table cells. However, if links inside table cells are not rendered as clickable hyperlinks, apply a follow-up `batchUpdate` to add link formatting:

```python
# Fix non-clickable links in table cells after doc creation
requests.append({"updateTextStyle": {
    "range": {"startIndex": link_start, "endIndex": link_end},
    "textStyle": {"link": {"url": source_url}},
    "fields": "link"
}})
```

**Alternative approach**: Use the Google Docs API `batchUpdate` directly (described in Steps 2a-2g below) which gives full control over hyperlink formatting. This is more verbose but guarantees clickable links.

**Verification**: After creating the doc, confirm at least one link is clickable. If not, re-create using the batchUpdate approach.

1. **Create a new Google Doc** in the user's Drive:

```bash
# Create a new Google Doc
curl -s -X POST "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -d '{
    "name": "Open Action Items — [DATE]",
    "mimeType": "application/vnd.google-apps.document"
  }'
```

2. **Build the document using Google Docs API `batchUpdate`**. Use a Python script for reliable construction. The document has three sections: header, main table, and detail sections per source.

**IMPORTANT**: All text insertion must happen via `insertText` requests. After inserting text, apply formatting via `updateTextStyle` and `updateParagraphStyle` using character index ranges. Insert content **bottom-up** (last content first) or track indices carefully, since insertions shift all subsequent indices.

#### Step 2a: Insert Title and Metadata

```python
# Build requests list for batchUpdate
requests = []

# Insert title at index 1 (start of document)
title_text = "Open Action Items — [DATE]\n"
requests.append({"insertText": {"location": {"index": 1}, "text": title_text}})

# Format title as Heading 1
requests.append({"updateParagraphStyle": {
    "range": {"startIndex": 1, "endIndex": 1 + len(title_text)},
    "paragraphStyle": {"namedStyleType": "HEADING_1"},
    "fields": "namedStyleType"
}})

# Insert metadata line
meta_text = f"Scanned: {start_date} to {end_date} | Sources: {sources} | Total: {total} (High: {high}, Medium: {med}, Low: {low})\n\n"
meta_start = 1 + len(title_text)
requests.append({"insertText": {"location": {"index": meta_start}, "text": meta_text}})

# Format metadata as grey, smaller font
requests.append({"updateTextStyle": {
    "range": {"startIndex": meta_start, "endIndex": meta_start + len(meta_text)},
    "textStyle": {"fontSize": {"magnitude": 9, "unit": "PT"}, "foregroundColor": {"color": {"rgbColor": {"red": 0.5, "green": 0.5, "blue": 0.5}}}},
    "fields": "fontSize,foregroundColor"
}})
```

#### Step 2b: Insert Main Summary Table

Insert a table with columns: `#`, `Priority`, `Source`, `Item`, `Document / Ticket`, `Assigned By`, `Date`, `Suggested Response`.

The **Suggested Response** column contains the drafted response from Phase 5c. This is the most valuable column — it gives the user a ready-to-use reply they can copy-paste into the original source.

```python
# Insert table after metadata
table_start = meta_start + len(meta_text)
num_rows = len(all_items) + 1  # +1 for header
num_cols = 8  # Last column is now "Suggested Response" instead of "Status"

requests.append({"insertTable": {
    "rows": num_rows,
    "columns": num_cols,
    "location": {"index": table_start}
}})
```

After inserting the table, read back the document structure (`documents.get`) to get the exact cell indices, then populate each cell:

```python
# Get document structure to find table cell indices
doc = get_document(doc_id, token)
table = doc['body']['content'][table_element_index]['table']

# For each cell, insert text and apply formatting
for row_idx, row in enumerate(table['tableRows']):
    for col_idx, cell in enumerate(row['tableCells']):
        cell_start = cell['content'][0]['startIndex']
        # ... insert text at cell_start
```

#### Step 2c: Format Table Header Row

```python
# Bold the header row
for cell in header_row_cells:
    requests.append({"updateTextStyle": {
        "range": {"startIndex": cell['start'], "endIndex": cell['end']},
        "textStyle": {"bold": True},
        "fields": "bold"
    }})

# Set header row background to dark grey
for cell in header_row_cells:
    requests.append({"updateTableCellStyle": {
        "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {"red": 0.2, "green": 0.2, "blue": 0.2}}}},
        "tableStartLocation": {"index": table_start_index},
        "rowSpan": 1, "columnSpan": 1,
        "fields": "backgroundColor"
    }})

# Set header text to white
for cell in header_row_cells:
    requests.append({"updateTextStyle": {
        "range": {"startIndex": cell['start'], "endIndex": cell['end']},
        "textStyle": {"foregroundColor": {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}}},
        "fields": "foregroundColor"
    }})
```

#### Step 2d: Color-Code Priority Column

Apply background colors to priority cells based on the priority level:

```python
PRIORITY_COLORS = {
    "HIGH": {"red": 0.8, "green": 0.0, "blue": 0.0},      # Red #CC0000
    "MEDIUM": {"red": 1.0, "green": 0.55, "blue": 0.0},    # Orange #FF8C00
    "LOW": {"red": 0.13, "green": 0.55, "blue": 0.13},     # Green #228B22
}

for item in all_items:
    priority_cell = get_cell(table, item['row_idx'], 1)  # Column 1 = Priority
    color = PRIORITY_COLORS[item['priority']]

    # Set cell background color
    requests.append({"updateTableCellStyle": {
        "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": color}}},
        "tableStartLocation": {"index": table_start_index},
        "rowSpan": 1, "columnSpan": 1,
        "fields": "backgroundColor"
    }})

    # Set priority text to white for contrast
    requests.append({"updateTextStyle": {
        "range": {"startIndex": priority_cell['start'], "endIndex": priority_cell['end']},
        "textStyle": {"foregroundColor": {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}}, "bold": True},
        "fields": "foregroundColor,bold"
    }})
```

#### Step 2e: Add Clickable Hyperlinks

Every reference in the "Document / Ticket" column must be a clickable hyperlink to the source:

```python
for item in all_items:
    link_cell = get_cell(table, item['row_idx'], 4)  # Column 4 = Document / Ticket
    link_text = item['display_name']  # e.g. "ES-12345" or "Meeting Notes Q1"
    link_url = item['source_url']     # e.g. "https://databricks.atlassian.net/browse/ES-12345"

    # Insert the display text
    requests.append({"insertText": {
        "location": {"index": link_cell['start']},
        "text": link_text
    }})

    # Apply hyperlink formatting
    requests.append({"updateTextStyle": {
        "range": {"startIndex": link_cell['start'], "endIndex": link_cell['start'] + len(link_text)},
        "textStyle": {"link": {"url": link_url}},
        "fields": "link"
    }})
```

**Link URL patterns**:
- Google Drive: use the `webViewLink` from the Drive API (e.g. `https://docs.google.com/document/d/{fileId}/edit`)
- JIRA: `https://databricks.atlassian.net/browse/{ticket_key}`
- Confluence: `https://databricks.atlassian.net/wiki/spaces/{space}/pages/{pageId}/{title}`
- ES tickets with Gmail thread: link to the JIRA ticket, not the email

#### Step 2f: Alternating Row Colors

Apply light grey background to even rows for readability:

```python
for row_idx in range(2, num_rows + 1, 2):  # Even rows (0-indexed: 2, 4, 6...)
    for col_idx in range(num_cols):
        requests.append({"updateTableCellStyle": {
            "tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {"red": 0.95, "green": 0.95, "blue": 0.95}}}},
            "tableStartLocation": {"index": table_start_index},
            "rowSpan": 1, "columnSpan": 1,
            "fields": "backgroundColor"
        }})
```

#### Step 2g: Detail Sections Per Source

After the table, add expandable detail sections for each source. Since Google Docs doesn't support collapsible sections natively, use **Heading 2** section headers with horizontal rules as visual separators.

```python
# After table, insert source detail sections
detail_start = table_end_index + 1

# --- Google Drive Details ---
section_text = "\nGoogle Drive Details\n"
requests.append({"insertText": {"location": {"index": detail_start}, "text": section_text}})
requests.append({"updateParagraphStyle": {
    "range": {"startIndex": detail_start + 1, "endIndex": detail_start + len(section_text)},
    "paragraphStyle": {"namedStyleType": "HEADING_2"},
    "fields": "namedStyleType"
}})

# For each Google Drive item, add context block WITH suggested response:
for item in gdrive_items:
    context = f"\n{item['display_name']}\n"
    context += f"Comment by {item['commenter_name']} ({item['created_date']}):\n"
    context += f"  \"{item['comment_text']}\"\n"
    if item.get('quoted_content'):
        context += f"  On: \"{item['quoted_content']}\"\n"
    if item.get('has_user_reply'):
        context += f"  (You already replied in this thread)\n"
    # Add the suggested response — this is the key deliverable
    context += f"\n  ✏️ Suggested response:\n"
    context += f"  {item['suggested_response']}\n"
    # Insert and format with hyperlink on the display name
    # Format the suggested response in italic to visually distinguish it
    # ... (same insertText + updateTextStyle pattern as above)

# --- JIRA Details ---
# Same pattern: Heading 2, then for each ticket:
#   ticket_key (hyperlinked), summary, status, priority
#   Latest comment text if it contains a question
#   For heated ES tickets: escalation indicators, customer, days_open
#   ✏️ Suggested response: the drafted JIRA comment from Phase 5c
#     (formatted in italic, indented under the ticket context)

# --- Confluence Details ---
# Same pattern: Heading 2, then for each task/comment:
#   page_title (hyperlinked), task text, space name
#   Surrounding page context if available
#   ✏️ Suggested response: the drafted reply from Phase 5c

# --- Unfollowed Promises ---
# Heading 2: "Unfollowed Promises"
# For each unfollowed promise:
#   source_link (hyperlinked), original promise text, days_ago
#   ✏️ Suggested follow-up: the drafted follow-up message from Phase 5c
```

3. **Execute the batchUpdate** — send all requests in a single API call:

```bash
# IMPORTANT: Refresh the token right before the API call (tokens expire during long scripts)
TOKEN=$(python3 "$GOOGLE_AUTH" token)

curl -s -X POST "https://docs.googleapis.com/v1/documents/${DOC_ID}:batchUpdate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  -d "{\"requests\": $REQUESTS_JSON}"
```

**Token refresh note**: If the script takes >30 minutes to build the requests, refresh the token immediately before the final API call using `subprocess.run()` inside the Python script rather than shell variable expansion.

### Phase 7: Summary Output

Print a summary to the user in the CLI:

```
Open Action Items Summary — [DATE]
Scanned: [START_DATE] to [END_DATE]

Google Drive: [X] items found
  - [Y] open comments
  - [Z] meeting note action items
  - [W] pending suggestions

JIRA: [X] items found
  - [Y] assigned tickets
  - [Z] comment mentions

Confluence: [X] items found
  - [Y] incomplete tasks
  - [Z] inline comments
```

| # | Priority | Source | Item Summary | Suggested Response |
|---|----------|--------|--------------|-------------------|
| 1 | HIGH | Google Docs | Review architecture section — [Doc Name] | "Good point about the Q2 timeline — I think we should push..." |
| 2 | HIGH | JIRA | ES-12345: Fix pipeline timeout | "Reviewed the logs — this looks like WAP-429. Workaround is..." |
| 3 | MEDIUM | Confluence | Update ops runbook | "Updated sections 3.1 and 3.2 with the new failover steps..." |
| ... | ... | ... | ... | ... |

```
Summary document created: [LINK TO GOOGLE DOC]
Open it to see all items with links, details, and suggested responses.
Each suggested response can be copy-pasted into the original source.
```

## Pagination and Rate Limits

- **Google Drive file listing**: Paginate using `pageToken` — fetch all pages until no `nextPageToken` is returned. Use `pageSize=100` per request.
- **Google Drive comments**: Each file requires a separate API call. Process files in batches of 10 to avoid rate limits. If a file has many comments, they are returned in a single response (no pagination needed for comments API).
- **Meeting notes scanning**: Limit to the 50 most recently modified meeting note documents to avoid excessive API calls. Export as plain text for parsing.
- **JIRA**: Use pagination (`startAt`, `maxResults`) for JQL queries. Default `maxResults=50`.
- **Confluence**: Use `start` and `limit` parameters for CQL queries.
- **Google Docs API**: When building the summary document, batch all formatting requests into a single `batchUpdate` call.

## Examples

### Example: No timeframe given
User says: "what action items are assigned to me?"
Result: Asks "What timeframe should I check?", then scans all sources and creates summary doc

### Example: Relative timeframe
User says: "/draft-replies-docs 30"
Result: Scans last 30 days across Google Drive, JIRA, and Confluence, creates summary doc

### Example: Source-specific
User says: "/draft-replies-docs 30 jira"
Result: Scans last 30 days in JIRA only, creates summary doc

### Example: Long timeframe
User says: "/draft-replies-docs 01-01-2025 09-03-2026"
Result: Scans 14+ months across all sources, creates comprehensive summary doc

### Example: Quick check
User says: "do I have any open comments on docs?"
Result: Parses as Google Drive scan, asks for timeframe, creates summary doc

## Notes

- **No messages are sent** — this skill only reads documents/tickets and creates a private summary doc in your Drive
- The summary Google Doc is created fresh each time (not updated in place) so you have a historical record
- Meeting note action items are detected heuristically — some false positives/negatives are possible
- For JIRA ES tickets, the skill checks both assignee and text mentions to catch tickets where you're involved but not formally assigned
- Confluence task detection depends on the Confluence instance's task markup format
- Large timeframes (>6 months) may take longer due to the volume of documents to scan

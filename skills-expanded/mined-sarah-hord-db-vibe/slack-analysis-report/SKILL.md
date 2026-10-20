---
name: slack-analysis-report
description: Analyze Slack channel feedback threads sorted by engagement, identify recurring patterns, and write a formatted Google Doc report. Use when the user says "slack analysis", "channel feedback", "slack report", "analyze slack", or "/slack-analysis".
---

# Slack Analysis Report

Fetch feedback threads from any Slack channel for a given date range, rank by engagement, identify top patterns, and write a formatted Google Doc.

## Parameters

This skill accepts 5 parameters in order:

```
/slack-analysis <channel> <start-date> <end-date> <drive-folder> <doc-name>
```

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `channel` | `#channel-name` | `#ai-dev-kit` | Slack channel (with or without `#`) |
| `start-date` | `YYYY-MM-DD` | `2026-02-23` | Start of date range (inclusive) |
| `end-date` | `YYYY-MM-DD` | `2026-03-01` | End of date range (inclusive) |
| `drive-folder` | folder name | `0.vibe.test` | Google Drive folder name for output |
| `doc-name` | file name | `ai-dev-kit_slack` | Google Doc title (date auto-appended). Defaults to channel name if omitted |

If any parameters are missing, prompt the user with AskUserQuestion.

## Capabilities

- Resolve Slack channel names to IDs via search
- Fetch all messages in a date range with pagination
- Sort threads by reply_count descending
- Fetch thread replies for top threads to understand full context
- Classify each thread's resolution status (Resolved / Partially Resolved / Unresolved / Informational)
- Identify top 10 recurring feedback patterns with descriptions
- Generate prioritized recommended next steps with suggested owners
- Resolve user IDs to real names via batch lookup
- Create a formatted Google Doc with key takeaways, recommendations, patterns, and thread table
- Place the doc in a specific Google Drive folder
- Post a formatted summary with top actions and report link back to the analyzed Slack channel
- Include AI attribution (model name) in the Slack post

## Workflow

### Phase 1: Parse Arguments

Parse the user's input to extract all 5 parameters. The input format is:

```
/slack-analysis #channel-name 2026-02-23 2026-03-01 "folder name" "doc-name"
```

1. Strip `#` prefix from channel name if present
2. Parse start-date and end-date as `YYYY-MM-DD`
3. Drive folder and doc name may be quoted if they contain spaces
4. If `doc-name` is not provided, default it to the channel name (without `#`). For example, channel `#ai-dev-kit` → doc-name `ai-dev-kit`
5. If the doc-name does not already contain the start-date, append `_<start-date>` to form the final Google Doc title

If parameters are missing, ask the user:

```
AskUserQuestion:
- "Which Slack channel?" (header: "Channel")
- "Date range? (YYYY-MM-DD to YYYY-MM-DD)" (header: "Dates")
- "Google Drive folder name?" (header: "Folder")
- "Google Doc title? (default: <channel-name>)" (header: "Doc name")
```

### Phase 2: Authenticate

1. Find the google-auth skill path dynamically:
   ```bash
   GOOGLE_AUTH_DIR=$(find ~/.claude/plugins/cache -path "*/fe-google-tools/*/skills/google-auth" -type d 2>/dev/null | head -1)
   ```
2. Check Google auth status:
   ```bash
   python3 "$GOOGLE_AUTH_DIR/resources/google_auth.py" status
   ```
3. If not valid, run login:
   ```bash
   python3 "$GOOGLE_AUTH_DIR/resources/google_auth.py" login
   ```

### Phase 3: Find Slack Channel

Use `mcp__slack__slack_read_api_call` with `search.messages` to find the channel ID:

```json
{
  "endpoint": "search.messages",
  "params": {"query": "in:#<channel-name>", "count": 1},
  "raw": true
}
```

Extract `channel.id` from the first match. Fail with a clear error if channel not found.

### Phase 4: Fetch Messages

1. Convert start-date and end-date to Unix timestamps (UTC midnight):
   ```python
   import datetime
   start_ts = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp())
   end_ts = int((datetime.datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)).timestamp())
   ```

2. Fetch all messages with pagination using `conversations.history`:
   ```json
   {
     "endpoint": "conversations.history",
     "params": {
       "channel": "<channel-id>",
       "oldest": "<start_ts>",
       "latest": "<end_ts>",
       "limit": 200
     },
     "raw": true
   }
   ```
   Follow `response_metadata.next_cursor` for pagination.

   **Note:** Large channels may return responses that exceed token limits and get saved to a file. If this happens, use Bash with `python3 -c` to parse the saved JSON file and extract the fields you need (ts, user, reply_count, text) rather than trying to read the full response inline.

3. For each message, collect: `ts`, `thread_ts`, `reply_count`, `user`, `text`

4. Build a Slack permalink for each message using the format:
   ```
   https://databricks.enterprise.slack.com/archives/<channel-id>/p<timestamp_without_dot>
   ```
   Where `timestamp_without_dot` is the message `ts` with the `.` removed (e.g., `1709164800.123456` → `p1709164800123456`).
   For threaded replies, append `?thread_ts=<thread_ts>&cid=<channel-id>` to link directly into the thread.

5. Resolve all unique user IDs to real names using `mcp__slack__slack_batch_read_api_call`:
   ```json
   {
     "endpoint": "users.info",
     "batch_params": [{"user": "U123"}, {"user": "U456"}]
   }
   ```
   Build and retain a bidirectional mapping of user ID ↔ real name (e.g., `U7B3N3UGG` ↔ `Steven Yu`) for use throughout the report and Slack post.

### Phase 5: Analyze Threads

1. Sort all messages by `reply_count` descending (messages with no replies at bottom)
2. For threads with `reply_count >= 3`, fetch full replies using individual `mcp__slack__slack_read_api_call` calls with `conversations.replies` endpoint (do NOT use batch API — it does not support `conversations.replies`). Use `analysis_prompt` parameter to summarize each thread to keep context manageable for large threads.
3. Use an Agent (subagent_type: "general-purpose") to analyze ALL message content and thread replies. The agent should produce three outputs:

   **a. Top 10 Recurring Patterns** — For each pattern provide:
   - Pattern name/title
   - Description (2-3 sentences)
   - Number of related threads
   - List of contributor real names (the people who posted those related threads)
   - Slack permalink for each related thread

   **b. Thread Resolution Status** — For each thread with replies, classify its status:
   - **Resolved**: A clear answer or decision was reached in the replies
   - **Partially Resolved**: Some guidance given but follow-up action still needed
   - **Unresolved**: Question asked but no definitive answer, or discussion still open
   - **Informational**: Announcement or FYI, no resolution needed

   **c. Recommended Next Steps** — Based on the patterns, thread resolutions, and reply content, generate 5-8 actionable recommendations. For each recommendation provide:
   - Action title (concise, starts with a verb)
   - Description (2-3 sentences explaining what to do and why)
   - Priority: **High** (blocking multiple people or recurring frequently), **Medium** (affects some people, came up more than once), or **Low** (nice-to-have, single occurrence)
   - Owner suggestion: Based on who responded authoritatively in the threads, suggest who is best positioned to own this action (use real names from the threads)
   - Related threads: Which threads drove this recommendation

### Phase 6: Create Google Doc

Use the **markdown converter** pattern (do NOT manually construct Google Docs API `batchUpdate` calls).

1. Write the report as a markdown file to `/tmp/slack-analysis-report.md` with this structure:
   ```markdown
   # #<channel-name> Slack Channel Feedback Analysis

   ### Week of <start-date> to <end-date>

   ## Key Takeaways (<start-date> to <end-date>)

   - Bullet point insights

   ## Recommended Next Steps

   ### High Priority

   **1. Action Title**

   Description of what to do and why. (2-3 sentences)

   **Suggested owner:** [Owner Name](https://databricks.enterprise.slack.com/team/USER_ID) | **Related threads:** 2 | **Contributors:** Ritesh Patel, Sava Kostadinov | [thread 1](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1772136932519979), [thread 2](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1772494118146299)

   **2. Action Title**

   Description of what to do and why. (2-3 sentences)

   **Suggested owner:** [Owner Name](https://databricks.enterprise.slack.com/team/USER_ID) | **Related threads:** 2 | **Contributors:** Alex Kim, Jordan Lee | [thread 1](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1771549432925859), [thread 2](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1772664821417159)

   ### Medium Priority

   **3. Action Title**

   Description.

   **Suggested owner:** [Owner Name](https://databricks.enterprise.slack.com/team/USER_ID) | **Related threads:** 1 | **Contributors:** Sam Chen | [thread 1](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1771911938781409)

   ### Low Priority

   **4. Action Title**

   Description.

   **Suggested owner:** [Owner Name](https://databricks.enterprise.slack.com/team/USER_ID) | **Related threads:** 1 | **Contributors:** Maria Garcia | [thread 1](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1771517795807709)

   ## Top 10 Feedback Patterns

   **1. Pattern Title**

   Description paragraph.

   **Related threads:** 2 | **Contributors:** Ritesh Patel, Sava Kostadinov | [thread 1](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1772136932519979), [thread 2](https://databricks.enterprise.slack.com/archives/C0AF2T7C06L/p1772494118146299)

   ## Appendix: All Threads (Ordered by Most Replies)

   | Rank | Replies | Date | Posted By | Message Preview | Status | Link |
   |------|---------|------|-----------|-----------------|--------|------|
   | 1 | 27 | Feb 26 | [Name](https://databricks.enterprise.slack.com/team/USER_ID) | Message preview text | Resolved | [View](slack-permalink-url) |
   ...
   ```

   **Formatting requirements for the markdown report:**

   - **No `&nbsp;` spacers**: Do NOT use `&nbsp;` for spacing. Use standard blank lines between sections. The markdown converter handles paragraph spacing naturally.
   - **All user names must be Slack profile hyperlinks**: Every person's name mentioned anywhere in the report — in Key Takeaways, Recommended Next Steps (suggested owners), and the Appendix table (Posted By column) — MUST be an embedded markdown hyperlink to their Slack profile: `[Name](https://databricks.enterprise.slack.com/team/USER_ID)`. Look up every user ID from the bidirectional mapping built in Phase 4.
   - **CRITICAL — Related threads format**: In both Recommended Next Steps and Top 10 Patterns, the "Related threads" line MUST follow this exact format: `**Related threads:** <count> | **Contributors:** <comma-separated real names> | [thread 1](slack-permalink), [thread 2](slack-permalink), ...`. The count is the number of related threads. Contributors are the real names of people who posted those threads. The link text MUST use short sequential labels: `thread 1`, `thread 2`, `thread 3`, etc. (NOT message preview text, which is too long). The links MUST use Slack thread permalink URLs (`/archives/CHANNEL_ID/pTIMESTAMP`), NEVER user profile URLs (`/team/USER_ID`). Build the permalink using the format from Phase 4 step 4.
   - **Thread status column**: The Appendix table MUST include a `Status` column showing the resolution status (Resolved / Partially Resolved / Unresolved / Informational) for each thread, as determined in Phase 5.
   - **Thread links**: The Link column uses embedded markdown hyperlinks `[View](url)` pointing to each message's Slack permalink.

2. Find the markdown-to-gdocs converter dynamically:
   ```bash
   CONVERTER=$(find ~/.claude/plugins/cache -path "*/google-docs/resources/markdown_to_gdocs.py" -type f 2>/dev/null | head -1)
   ```

3. **Check for existing docs with the same name** and determine the final title:
   ```bash
   TOKEN=$(python3 "$GOOGLE_AUTH_DIR/resources/google_auth.py" token)
   BASE_TITLE="<doc-name>_<start-date>"
   # Search for existing Google Docs with names starting with the base title
   EXISTING=$(curl -s "https://www.googleapis.com/drive/v3/files?q=name+contains+'${BASE_TITLE}'+and+mimeType%3D'application%2Fvnd.google-apps.document'+and+trashed%3Dfalse&fields=files(name)" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng")
   ```
   Parse the results to check if a doc with `BASE_TITLE` (or `BASE_TITLE_v2`, `_v3`, etc.) already exists:
   - If no doc named `BASE_TITLE` exists → use `BASE_TITLE` as-is
   - If `BASE_TITLE` exists but no `_v2` → use `BASE_TITLE_v2`
   - If `BASE_TITLE` and `_v2` exist but no `_v3` → use `BASE_TITLE_v3`
   - Continue incrementing until an unused name is found

   Set `FINAL_TITLE` to the resolved name.

4. Convert to Google Doc:
   ```bash
   python3 "$CONVERTER" \
     --input /tmp/slack-analysis-report.md \
     --title "$FINAL_TITLE"
   ```
   This returns a JSON object with `documentId` and `url`.

5. Move the doc to the target folder:
   ```bash
   TOKEN=$(python3 "$GOOGLE_AUTH_DIR/resources/google_auth.py" token)
   ```

   a. Find the destination folder by name:
   ```bash
   curl -s "https://www.googleapis.com/drive/v3/files?q=name%3D'<folder-name>'+and+mimeType%3D'application%2Fvnd.google-apps.folder'+and+trashed%3Dfalse" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng"
   ```

   b. Get the doc's current parent folder:
   ```bash
   curl -s "https://www.googleapis.com/drive/v3/files/<doc-id>?fields=parents" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng"
   ```

   c. Move the doc:
   ```bash
   curl -s -X PATCH "https://www.googleapis.com/drive/v3/files/<doc-id>?addParents=<folder-id>&removeParents=<current-parent-id>" \
     -H "Authorization: Bearer $TOKEN" \
     -H "x-goog-user-project: gcp-sandbox-field-eng" \
     -H "Content-Type: application/json" \
     -d '{}'
   ```

6. Return the Google Doc URL to the user:
   ```
   https://docs.google.com/document/d/<doc-id>/edit
   ```

7. **Share the Google Doc with all channel members**:

   a. Fetch the channel's member list using `mcp__slack__slack_read_api_call`:
   ```json
   {
     "endpoint": "conversations.members",
     "params": {"channel": "<channel-id>", "limit": 500},
     "raw": true
   }
   ```
   Follow `response_metadata.next_cursor` for pagination if the channel has more than 500 members.

   b. Resolve each member's email address. Use the user ID → email mapping already built in Phase 4. For any user IDs not yet resolved, use `mcp__slack__slack_batch_read_api_call` with `users.info` to look up their email.

   c. Share the doc with each member using the Google Drive API. Batch the permission grants in a loop:
   ```bash
   TOKEN=$(python3 "$GOOGLE_AUTH_DIR/resources/google_auth.py" token)
   for EMAIL in <list-of-emails>; do
     curl -s -X POST "https://www.googleapis.com/drive/v3/files/<doc-id>/permissions" \
       -H "Authorization: Bearer $TOKEN" \
       -H "x-goog-user-project: gcp-sandbox-field-eng" \
       -H "Content-Type: application/json" \
       -d "{\"role\": \"reader\", \"type\": \"user\", \"emailAddress\": \"$EMAIL\"}" \
       --data-urlencode "sendNotificationEmail=false"
   done
   ```

   **Important notes:**
   - Grant `reader` role (not writer) so members can view but not accidentally edit
   - Set `sendNotificationEmail=false` as a query parameter to avoid spamming everyone with individual share notifications — they will see the report via the Slack post instead
   - If a permission grant fails for a specific user (e.g., external account), log a warning and continue with the remaining users
   - Use Bash to batch the curl calls efficiently rather than making individual tool calls per user

### Phase 7: Post Summary to Slack Channel

After the Google Doc is created, post a formatted summary to the same Slack channel that was analyzed. Use `mcp__slack__slack_write_api_call` with `chat.postMessage` and Slack Block Kit formatting.

1. Compose the message using Slack `mrkdwn` blocks. The message should include:

   a. **Header block**: Channel feedback analysis title
   b. **Key Takeaways section**: The bullet-point insights from the analysis
   c. **Top Recommended Actions**: The top 3 high-priority recommendations (title + one-line description + suggested owner tagged with their Slack handle using `<@USER_ID>` format)
   d. **Link to full report**: The Google Doc URL
   e. **Attribution footer**: Credit the AI model used

2. Post the message:
   ```json
   {
     "endpoint": "chat.postMessage",
     "params": {
       "channel": "<channel-id>",
       "blocks": [
         {
           "type": "header",
           "text": {"type": "plain_text", "text": "#<channel-name> Feedback Analysis (<start-date> to <end-date>)"}
         },
         {
           "type": "section",
           "text": {
             "type": "mrkdwn",
             "text": "*Key Takeaways (<start-date> to <end-date>)*\n\n• Takeaway 1\n• Takeaway 2\n• Takeaway 3"
           }
         },
         {"type": "divider"},
         {
           "type": "section",
           "text": {
             "type": "mrkdwn",
             "text": "*Top Recommended Actions*\n\n:one: *Action Title* — Description. _Suggested owner: <@USER_ID>_\n\n:two: *Action Title* — Description. _Suggested owner: <@USER_ID>_\n\n:three: *Action Title* — Description. _Suggested owner: <@USER_ID>_"
           }
         },
         {"type": "divider"},
         {
           "type": "section",
           "text": {
             "type": "mrkdwn",
             "text": ":page_facing_up: *<https://docs.google.com/document/d/<doc-id>/edit|View Full Report>*\n\n_This analysis was generated by Claude (claude-opus-4-6) via the slack-analysis plugin. Patterns and recommendations are AI-generated summaries — please verify before acting._"
           }
         }
       ]
     }
   }
   ```

3. Important formatting notes:
   - Use `mrkdwn` (Slack's variant, NOT standard markdown) for text formatting
   - Bold: `*text*`, Italic: `_text_`, Strikethrough: `~text~`
   - Links: `<url|display text>`
   - Bullet points: Use `•` character (not `-`)
   - Number emojis: `:one:`, `:two:`, `:three:` for visual ranking
   - Keep the message concise — full details are in the Google Doc
   - Tag suggested owners using Slack user mentions `<@USER_ID>` (e.g., `<@U7B3N3UGG>`) so they receive a notification. Look up the user ID from the bidirectional mapping built in Phase 4
   - The attribution line must specify the exact model used (e.g., `claude-opus-4-6`, `claude-sonnet-4-6`)

## Examples

### Example: Full parameters
User says: `/slack-analysis #ai-dev-kit 2026-02-23 2026-03-01 "0.vibe.test" "ai-dev-kit_slack"`
Result: Creates `ai-dev-kit_slack_2026-02-23` in the `0.vibe.test` Drive folder with a formatted table of all threads and top 10 patterns.

### Example: Different channel and date range
User says: `/slack-analysis #field-eng-help 2026-03-01 2026-03-07 "Reports" "field-eng-weekly"`
Result: Creates `field-eng-weekly_2026-03-01` in the `Reports` Drive folder.

### Example: Missing parameters
User says: `/slack-analysis #ai-dev-kit`
Result: Prompts for missing date range, folder, and doc name before proceeding.

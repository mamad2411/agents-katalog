---
name: molly-kickoff
description: Executes Molly's kick-off phase for a new recruiting role. Use when a recruiter @mentions Molly in the sourcing channel with a Notion JD page URL to start sourcing for a new role.
---

# Kick-off

Triggered when a recruiter @mentions Molly with a Notion JD page URL. Kick-off does two things: (1) build and write the Profile Spec, and (2) immediately run the first calibration cycle — find a batch of candidates (`MOLLY_CALIBRATION_BATCH_SIZE`, default 5) and post them to Slack for review.

## Inputs

Extract the Notion JD page URL from the Slack message. The page ID is the last 32 hex characters of the URL.

## Steps

### 1. Read the JD page

```bash
curl -s "https://api.notion.com/v1/blocks/JD_PAGE_ID/children?page_size=100" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

Extract plain text from all blocks. The JD page contains: Job Description, Kick-off Notes, and Orienting Profiles (table). Read all three sections.

### 2. Build the Profile Spec

Synthesize the JD page content into a Profile Spec. The goal is to distill what makes a great candidate into something concrete enough to search for — not a restatement of the JD. The Exa Search Strategy section is especially important: it drives every candidate search, so make it specific.

Use this structure:

```
## Profile Spec: [Role Name]

### Ideal Candidate Summary
[1-2 sentences]

### Must-Haves
- ...

### Nice-to-Haves
- ...

### Evaluation Criteria
- [Criterion] ([weight]%): [what to look for]

### Target Companies
- ...

### Exa Search Strategy
[2-3 specific queries you will use; what signals indicate a strong match]
```

### 3. Create the Profile Spec page in Notion

Create a new page under the configured parent page (`$MOLLY_NOTION_PARENT_PAGE_ID`) titled "Profile Spec: [Role Name]" with the spec sections as content. Note the returned page ID — you'll need it for the tracker and button values.

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data @- <<EOF
{
  "parent": {"page_id": "$MOLLY_NOTION_PARENT_PAGE_ID"},
  "properties": {"title": {"title": [{"text": {"content": "Profile Spec: ROLE_NAME"}}]}},
  "children": [
    {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Ideal Candidate Summary"}}]}},
    {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "CONTENT"}}]}},
    ... (repeat for each section)
  ]
}
EOF
```

### 4. Add a row to the Molly Tracker

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data @- <<EOF
{
  "parent": {"database_id": "$MOLLY_TRACKER_DB_ID"},
  "properties": {
    "Role name": {"title": [{"text": {"content": "ROLE_NAME"}}]},
    "JD Link": {"url": "JD_PAGE_URL"},
    "Profile Spec Link": {"url": "SPEC_PAGE_URL"},
    "Molly Status": {"status": {"name": "Calibrating"}},
    "Open date": {"date": {"start": "YYYY-MM-DD"}}
  }
}
EOF
```

### 5. Add Calibration Cycle 1 table to the Profile Spec page

Append a `## Calibration Cycle 1` heading and an empty table to the spec page. The table has 4 columns and starts with just the header row — candidate rows are added as feedback comes in.

Table structure:
```json
{
  "object": "block",
  "type": "table",
  "table": {
    "table_width": 4,
    "has_column_header": true,
    "children": [
      {"object": "block", "type": "table_row", "table_row": {"cells": [
        [{"type": "text", "text": {"content": "Name"}}],
        [{"type": "text", "text": {"content": "Why it fits"}}],
        [{"type": "text", "text": {"content": "Team result"}}],
        [{"type": "text", "text": {"content": "Team feedback"}}]
      ]}}
    ]
  }
}
```

After appending, fetch the table block ID (you'll need it to add candidate rows later).

### 6. Search Exa for the calibration batch

Use the Exa Search Strategy from the spec. Run 2-3 queries with distinct angles. Search LinkedIn profiles only.

```bash
curl -s -X POST "https://api.exa.ai/search" \
  -H "Authorization: Bearer $MOLLY_EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "numResults": 10, "type": "neural", "includeDomains": ["linkedin.com"], "contents": {"text": {"maxCharacters": 500}}}'
```

Pick a full batch of non-duplicate matches (`MOLLY_CALIBRATION_BATCH_SIZE`, default 5). **Exclude anyone below the minimum current-company tenure (`MOLLY_MIN_TENURE_MONTHS`, default 6 months)** — global sourcing rule (see `AGENTS.md`); read the current role's start date / duration from the profile (fetch the full contents if the 500-char snippet doesn't reach it) and skip short-tenure candidates, over-fetching so you still land a full batch. For each survivor, record: name, current role + company, LinkedIn URL, 1-sentence fit rationale (cite specific evidence, not generic).

### 7. Add candidate rows to the Calibration Cycle 1 table

For each candidate in the batch, append a table row to the table block:

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/TABLE_BLOCK_ID/children" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"children": [{"object": "block", "type": "table_row", "table_row": {"cells": [
    [{"type": "text", "text": {"content": "NAME", "link": {"url": "LINKEDIN_URL"}}}],
    [{"type": "text", "text": {"content": "WHY_IT_FITS"}}],
    [{"type": "text", "text": {"content": ""}}],
    [{"type": "text", "text": {"content": ""}}]
  ]}}]}'
```

### 8. Post a single calibration cycle message to Slack

Post **one message** to the thread listing all candidates with a single "Review All Candidates" button. The button value encodes everything your Slack interactivity handler (see the README) needs to build the review modal: spec/JD page IDs, cycle number, role name, and the candidate list (name + LinkedIn URL for each).

Button value JSON (encode as string, keep compact — fits within Slack's 2000 char limit):
```json
{
  "spec_page_id": "SPEC_PAGE_ID",
  "jd_page_id": "JD_PAGE_ID",
  "cycle_num": 1,
  "role_name": "ROLE_NAME",
  "candidates": [
    {"num": 1, "name": "Full Name", "url": "https://linkedin.com/in/..."},
    {"num": 2, "name": "Full Name", "url": "https://linkedin.com/in/..."},
    {"num": 3, "name": "Full Name", "url": "https://linkedin.com/in/..."},
    {"num": 4, "name": "Full Name", "url": "https://linkedin.com/in/..."},
    {"num": 5, "name": "Full Name", "url": "https://linkedin.com/in/..."}
  ]
}
```

Message Block Kit structure:
```json
[
  {"type": "section", "text": {"type": "mrkdwn", "text": "📋 *ROLE_NAME* · <SPEC_URL|View Profile Spec>\n*Calibration Cycle N* — 5 candidates ready for review"}},
  {"type": "divider"},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*1. <URL|Name>*\nRole at Company\n_Why they fit: RATIONALE_"}},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*2. <URL|Name>*\nRole at Company\n_Why they fit: RATIONALE_"}},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*3. <URL|Name>*\nRole at Company\n_Why they fit: RATIONALE_"}},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*4. <URL|Name>*\nRole at Company\n_Why they fit: RATIONALE_"}},
  {"type": "section", "text": {"type": "mrkdwn", "text": "*5. <URL|Name>*\nRole at Company\n_Why they fit: RATIONALE_"}},
  {"type": "divider"},
  {"type": "actions", "elements": [
    {"type": "button", "text": {"type": "plain_text", "text": "Review All Candidates →"}, "style": "primary", "action_id": "open_review_modal", "value": "JSON_STRING"}
  ]},
  {"type": "context", "elements": [{"type": "mrkdwn", "text": "Click to approve/reject each candidate and add feedback. One submission fires Molly."}]}
]
```

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $MOLLY_SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "CHANNEL", "thread_ts": "THREAD_TS", "blocks": [...]}'
```

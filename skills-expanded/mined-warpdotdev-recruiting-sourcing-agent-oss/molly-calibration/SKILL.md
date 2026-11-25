---
name: molly-calibration
description: Executes Molly's calibration phase. Use when triggered by a recruiter approving or rejecting a candidate profile via Slack buttons, or when a recruiter @mentions Molly during an active calibration cycle.
---

# Calibration

Triggered when a recruiter submits the "Review All Candidates" modal (via your Slack interactivity handler — see the README). Your prompt contains every decision at once: ROLE, CALIBRATION CYCLE, SPEC PAGE ID, JD PAGE ID, SLACK CHANNEL, SLACK THREAD TS, and a numbered list of candidates with APPROVED/REJECTED + optional feedback.

## Steps

### 1. Update all rows in the calibration table

Read the spec page to find the calibration cycle table:

```bash
curl -s "https://api.notion.com/v1/blocks/SPEC_PAGE_ID/children?page_size=100" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

Find the heading `## Calibration Cycle N` (where N = CALIBRATION CYCLE). Get the table block that follows it. Get the table's row block IDs.

For each candidate, update the corresponding row (row index = candidate number, accounting for the header row at index 0):

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/ROW_BLOCK_ID" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"table_row": {"cells": [
    [{"type": "text", "text": {"content": "NAME", "link": {"url": "LINKEDIN_URL"}}}],
    [{"type": "text", "text": {"content": "WHY_IT_FITS"}}],
    [{"type": "text", "text": {"content": "yes_or_no"}}],
    [{"type": "text", "text": {"content": "FEEDBACK_OR_EMPTY"}}]
  ]}}'
```

Count approvals (APPROVED decisions). All rows will always have a result since the modal requires all decisions before submitting. Continue to step 2.

### 2. Analyze the cycle and write Calibration Notes

Read all rows. Count approvals (yes) and rejections (no). Identify patterns in the feedback.

Append `## Calibration Notes N` to the spec page with a brief summary:
- How many approved / rejected
- What the feedback reveals about the spec (e.g. "Rejections suggest candidates with large audiences but without hands-on developer community management are a miss")
- Whether another calibration cycle is needed (yes if fewer than the full batch approved)

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/SPEC_PAGE_ID/children" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"children": [
    {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Calibration Notes N"}}]}},
    {"type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "NOTES"}}]}}
  ]}'
```

**If the full batch approved:** update the Molly Tracker to `Sourcing` and announce in the Slack thread. Done.

**If fewer approved:** continue to step 3.

### 3. Update the spec based on feedback

If the rejections reveal something concrete about the spec (wrong target companies, wrong evaluation criteria, etc.), update the relevant sections of the spec page. Find the heading block for the section to update and patch its children.

### 4. Run the next calibration cycle

Search Exa for a new batch of candidates (`MOLLY_CALIBRATION_BATCH_SIZE`, default 5). Avoid names already in any prior calibration table on the spec page, and **exclude anyone below the minimum current-company tenure (`MOLLY_MIN_TENURE_MONTHS`, default 6 months)** — global sourcing rule (see `AGENTS.md`); read the current role's start date / duration from the profile (fetch the full contents if the snippet doesn't reach it) and skip short-tenure candidates, over-fetching so you still land a full batch.

```bash
curl -s -X POST "https://api.exa.ai/search" \
  -H "Authorization: Bearer $MOLLY_EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY", "numResults": 10, "type": "neural", "includeDomains": ["linkedin.com"], "contents": {"text": {"maxCharacters": 500}}}'
```

Append `## Calibration Cycle N+1` heading + empty 4-column table to the spec page. Add a row per candidate (Name+link, Why it fits, empty result, empty feedback).

Post the new batch to the same thread using the same Block Kit format as kick-off (with updated cycle_num = N+1 in the button value JSON).

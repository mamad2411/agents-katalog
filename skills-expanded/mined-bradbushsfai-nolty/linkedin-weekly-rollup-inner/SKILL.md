---
name: linkedin-weekly-rollup-inner
description: Pull last 7 days of LinkedIn creator analytics into a Google Sheet, send WoW summary via Telegram. Inherits claude-in-chrome MCP. EXAMPLE.
---

# LinkedIn Weekly Rollup (example)

> **EXAMPLE.** Same Chrome-MCP-inheritance pattern as `linkedin-post-tracking-inner`, but pulls aggregate creator analytics (not per-post) and computes week-over-week deltas.

Spawn a Sonnet sub-agent if `[cron ...]` suffix present.

## Context

- **Spreadsheet:** `YOUR_SHEET_ID`, sheet `Weekly Detailed Tracking`
- Bot-detection: wait 2-3 seconds between every browser action

## Columns

A=Date · B=Impressions · C=Members Reached · D=Engagements · E=Reactions · F=Comments · G=Reposts · H=Saves · I=Sends · J=Premium Button Clicks

## Procedure

### STEP 1 — Pull metrics from LinkedIn

Navigate to `https://www.linkedin.com/analytics/creator/content/`. Ensure "Past 7 days" is selected.

**Impressions view** — record:
- Total Impressions
- Members Reached

**Engagements view** (append `?metricType=ENGAGEMENTS` to URL) — record:
- Engagements (total), Reactions, Comments, Reposts, Saves, Sends, Premium Button Clicks

### STEP 2 — Find next empty row in sheet

```bash
/opt/homebrew/bin/gog sheets get "YOUR_SHEET_ID" "'Weekly Detailed Tracking'!A1:J20"
```

First row where col A is empty.

### STEP 3 — Write one cell at a time

```bash
/opt/homebrew/bin/gog sheets update "YOUR_SHEET_ID" "'Weekly Detailed Tracking'!A{ROW}" "MM/DD/YYYY"
# ...repeat for B through J
```

Use `0` for any zero metric.

### STEP 4 — Telegram summary with WoW

Pull the prior row for week-over-week comparison. Compute **absolute change** and **percentage change** for each metric.

Format per template (`reply` MCP, `chat_id` from `USER.md`):

```
LinkedIn weekly rollup, week ending [DATE]

Impressions: [X], [up/down] [absolute delta] WoW ([+/-][%]%)
Members reached: [X], [up/down] [absolute delta] ([+/-][%]%)
Engagements: [X], [up/down] [absolute delta] ([+/-][%]%)

Breakdown:
Reactions [X], [up/down/flat] [delta if not flat]
Comments [X], [up/down/flat]
Reposts [X], [up/down/flat]
Saves [X], [up/down/flat]
Sends [X], [up/down/flat]
Premium button clicks [X], [up/down/flat]

Top post: "[first ~10 words]..." with [X] impressions and [X] engagements.

Spreadsheet updated/verified in Weekly Detailed Tracking, row [N].
```

Rules:
- Absolute delta + percentage for top 3 metrics (Impressions, Reached, Engagements)
- Trend word (up/down/flat) for each breakdown metric; include delta only if non-zero
- Always identify the top post
- Always confirm the spreadsheet row number
- Omit WoW only if no prior row exists (first week)

### STEP 5 — Close Chrome tabs

Same tab-cleanup pattern as `linkedin-post-tracking-inner` STEP 7.

### STEP 6 — Emit sentinel

Print `LINKEDIN_ROLLUP_DONE` as final line.

## On failure

Brief Telegram + close opened tabs + emit `LINKEDIN_ROLLUP_DONE failed <step>`.

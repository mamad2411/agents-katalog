---
name: linkedin-monthly-analysis
description: Day 1 of month — analyze previous month's LinkedIn post performance, write report, Telegram top findings. EXAMPLE.
---

# LinkedIn Monthly Analysis (example)

> **EXAMPLE.** Read-only analytics pattern: pull all month's rows from a Google Sheet, compute aggregates, write markdown report, Telegram top 3 findings.

Spawn a Sonnet sub-agent if `[cron ...]` suffix present.

## Context

- **Tracking sheet:** `YOUR_SHEET_ID`, sheet `Post Tracking`
- Only analyze rows that have data in columns I-P (Impressions through Engagement Rate). Reshares and casual posts are NOT tracked.
- **Report destination:** `YOUR_OBSIDIAN_VAULT/Marketing/LinkedIn/Monthly_Analysis_YYYY-MM.md`

## Procedure

### STEP 1 — Pull tracking data

```bash
/opt/homebrew/bin/gog sheets get "YOUR_SHEET_ID" "'Post Tracking'!A1:R80"
```

Filter to rows where post date falls in the **previous calendar month** and columns I-P have values.

### STEP 2 — Analyze

For the month:
- Avg impressions, avg engagement rate
- Top 5 posts (by engagement rate, then impressions)
- Bottom 5 posts
- Performance breakdown by: post type, format (text vs carousel vs graphic), hook style, length bucket (short/medium/long)

Compare to prior month's report if one exists in the same Obsidian folder.

### STEP 3 — Write report

Save to `YOUR_OBSIDIAN_VAULT/Marketing/LinkedIn/Monthly_Analysis_YYYY-MM.md`:

```markdown
# LinkedIn Monthly Analysis — [Month YYYY]

## Summary
- Total tracked posts: N
- Avg impressions: X
- Avg engagement rate: X%
- MoM change: [▲/▼ if prior month exists]

## Top 5 Posts
1. [title] — [date] — impressions / engagement rate — why it worked

## Bottom 5 Posts
...

## By Post Type / Format / Hook Style / Length
...

## Recommendations for [next month]
1. ...
2. ...
3. ...
```

### STEP 4 — Telegram summary

Top 3 findings via `reply` MCP with `chat_id` from `USER.md`:

```
📈 *LinkedIn [Month] Analysis*

1. [top finding]
2. [second finding]
3. [third finding]

Full report: YOUR_OBSIDIAN_VAULT/Marketing/LinkedIn/Monthly_Analysis_YYYY-MM.md
```

End with `MONTHLY_OK <timestamp>`.

### STEP 5 — On failure

If sheet read fails or no data for prior month, `reply` with the issue. Don't exit silently. End with `MONTHLY_FAIL <timestamp>`.

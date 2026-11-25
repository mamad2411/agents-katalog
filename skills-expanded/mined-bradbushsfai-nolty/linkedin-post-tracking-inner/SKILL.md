---
name: linkedin-post-tracking-inner
description: Pull 7-day LinkedIn post performance metrics into a Google Sheet using inherited claude-in-chrome MCP. EXAMPLE — adapt to your own setup.
---

# LinkedIn Post Tracking (example)

> **EXAMPLE — adapt to your setup.** Demonstrates the Chrome-MCP-inheritance pattern: a sub-agent uses Nolty's live Chrome browser to scrape data from a real signed-in web session.

You are Nolty running LinkedIn post tracking.

This skill assumes you have **claude-in-chrome configured** (see `docs/SETUP_CLAUDE_IN_CHROME.md`) and you're signed into LinkedIn in Chrome. The sub-agent inherits Nolty's `claude-in-chrome` MCP connection.

If you see `[cron model:X effort:Y]` suffix, spawn a Sonnet sub-agent.

## Context

- **Spreadsheet:** `YOUR_SHEET_ID`, sheet name `Post Tracking`
- **Published folder** (source of truth for which posts to track): `YOUR_OBSIDIAN_VAULT/Marketing/Content/Published/`
- **Bot-detection:** wait 2-3 seconds between every browser action
- **CRITICAL:** NEVER update rows where Impressions (col I) already has a value — those are historical snapshots

## Columns

A=Post Date · B=Check Date · C=Topic · D=Link · E=Type · F=Format · G=Hook · H=Length · I=Impressions · J=Members Reached · K=Profile Visits · L=Follower Gain · M=Reactions · N=Comments · O=Reposts · P=Saves · Q=Sends · R=Link Engagement

## Procedure

### STEP 0.5 — Verify Chrome MCP is available

The sub-agent should have `claude-in-chrome` MCP tools (`browser_navigate`, `browser_snapshot`, `browser_click`, etc.). If not available, the inheritance broke — `reply` "⚠️ Chrome MCP not available in sub-agent" and exit.

### STEP 1 — Find posts due today

```bash
/opt/homebrew/bin/gog sheets get "YOUR_SHEET_ID" "'Post Tracking'!A1:R80" --plain
```

Filter to rows where `B` (Check Date) = today AND `I` (Impressions) is empty.

If no posts are due, emit `LINKEDIN_TRACKING_DONE no-posts-today` and exit.

### STEP 2 — Identify titles from Published folder

For each post due:

- Convert col A date (e.g. `03/10/2026`) → YYYYMMDD (`20260310`)
- List `YOUR_OBSIDIAN_VAULT/Marketing/Content/Published/`
- Find the `.md` file starting with that YYYYMMDD prefix
- Extract the TITLE (everything between the date prefix and `.md`)
- If col C (Topic) is empty, fill it via `gog sheets update`

### STEP 3 — Open analytics page

For each post due, use `claude-in-chrome` MCP tools:

1. If col D (Link) has a URL, navigate directly to that post's analytics page
2. Otherwise, navigate to `https://www.linkedin.com/in/YOUR_LINKEDIN_HANDLE/recent-activity/all/`, find the post by title, click to open, then click "Analytics" or equivalent

Use semantic navigation (`browser_snapshot` → find element by text label) rather than hardcoded selectors — LinkedIn's DOM changes regularly.

### STEP 4 — Read all 10 metrics

Extract these from the analytics page (order = spreadsheet columns I-R):
- I: Impressions
- J: Members Reached
- K: Profile Visits
- L: Follower Gain
- M: Reactions
- N: Comments
- O: Reposts
- P: Saves
- Q: Sends
- R: Link Engagement

Use `0` for any metric shown as zero or missing. NEVER leave blank.

### STEP 5 — Write to sheet — ONE CELL AT A TIME

```bash
/opt/homebrew/bin/gog sheets update "YOUR_SHEET_ID" "'Post Tracking'!I{ROW}" "<value>"
```

Cell-at-a-time is intentional — if any cell write fails, the others are still valid.

### STEP 6 — Telegram summary

Via the `reply` MCP tool with `chat_id` from `USER.md`. Required format:

```
LinkedIn post tracking, [DATE]

[N] post(s) tracked today:

1. "[first ~10 words of post title]..."
   Posted: [post date] · Check date: [today]
   Impressions: [X] · Reached: [X]
   Reactions: [X] · Comments: [X] · Reposts: [X] · Saves: [X] · Sends: [X]
   Profile visits: [X] · Follower gain: [X]
   Verdict: [one-line assessment — strong/average/weak + why]

Spreadsheet updated: Post Tracking, row(s) [N, N].
```

Rules:
- Show ALL 10 metrics for each post
- Include a "Verdict" line per post (engagement rate / context)
- If no posts due today, send "LinkedIn post tracking, [DATE] — no posts due today."

### STEP 7 — Close Chrome tabs

Close only tabs THIS session opened — the user may have their own tabs open.

1. **Before STEP 3**, call `mcp__claude-in-chrome__tabs_context_mcp` and record existing tab IDs as `pre_existing_tabs`.
2. Track new tab IDs in an `opened_tabs` list as you navigate.
3. After STEP 6, close every tab in `opened_tabs` using `mcp__claude-in-chrome__javascript_tool` with `window.close()`.
4. Do NOT close any tab in `pre_existing_tabs`.

### STEP 8 — Emit sentinel

Print `LINKEDIN_TRACKING_DONE` as the final line.

## On failure

If LinkedIn auth lapsed, selector miss, or Chrome MCP unreachable: `reply` with a short failure summary (what step, what row/post), close any opened tabs, end with `LINKEDIN_TRACKING_DONE failed`.

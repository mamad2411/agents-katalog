---
name: start
description: Run the full morning briefing routine. Executes all workstreams in parallel — email triage, Slack digest, calendar prep, industry scan, GitHub digest, competitor watch — then combines everything into a unified dashboard. Use this skill when the user wants their complete morning briefing.
---

# Morning Briefing — Full Routine

Run the complete morning briefing. This is the primary command.

## Instructions

You are executing a comprehensive morning routine. Read `morning-briefing.local.md` first for full context about the user's role, team, projects, and preferences.

### Execution Plan

Run these workstreams using sub-agents where possible to maximize parallelism:

**Parallel Group 1** (can all run simultaneously):
1. **Email Triage + Cleanup** — Use the `email-triage` skill to scan, classify, draft replies, AND clean up inbox (archive junk, mark FYI as read)
2. **Slack Digest** — Use the `slack-digest` skill
3. **Calendar Prep** — Use the `calendar-prep` skill
4. **GitHub Digest** — Use the `github-digest` skill

**Parallel Group 2** (can run simultaneously, web-search based):
5. **Industry Scan** — Use the `industry-scan` skill
6. **Competitor Watch** — Use the `competitor-watch` skill

**Sequential (runs last, after all above complete):**
7. **Morning Dashboard** — Use the `morning-dashboard` skill to combine all outputs

### File Outputs

All files are saved to the current working folder with today's date:
- `briefing-email-YYYY-MM-DD.md`
- `briefing-slack-YYYY-MM-DD.md`
- `briefing-calendar-YYYY-MM-DD.md`
- `morning-reading-YYYY-MM-DD.md`
- `briefing-github-YYYY-MM-DD.md`
- `briefing-competitors-YYYY-MM-DD.md`
- `morning-dashboard-YYYY-MM-DD.html`
- `briefing-summary-YYYY-MM-DD.md`

### Completion

After all workstreams finish:

1. Open the HTML dashboard in the browser
2. Display the summary briefing (the 30-second scannable version) directly in chat
3. Call out the single most urgent item across all workstreams
4. Ask: "Anything you want me to dig deeper into, or should I start on those draft responses?"

### Graceful Degradation

If any MCP connector is unavailable:
- **First, try Chrome as a fallback** — navigate to the web version of the service (mail.google.com, app.slack.com, calendar.google.com, github.com) and read data from the browser. The user should be signed in to all services in Chrome.
- If BOTH the connector AND Chrome are unavailable, skip that workstream
- Note it in the dashboard as "[Section] — unavailable (connector failed, Chrome fallback failed)"
- Continue with all other workstreams
- Never fail the entire routine because one service is unavailable

### Tone

Read the user's communication style from `morning-briefing.local.md` and match it. Default: direct, concise, practical. No filler. Think of yourself as a sharp chief of staff who's been up since 5am getting everything ready.

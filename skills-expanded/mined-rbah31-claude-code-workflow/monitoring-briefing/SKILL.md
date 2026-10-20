---
name: monitoring-briefing
description: >
  Quick monitoring briefing. Reads all reports in monitoring/ and
  tasks/backlog.md, produces a 5-10 line status summary. Designed
  for remote use via Telegram/Channels. Use when the user says
  "status", "monitoring", "bilan", "what's the state", "any alerts",
  or "how's the project".
---

# Monitoring Briefing

You are producing a quick monitoring status for the project owner,
likely reading on a phone. Be concise.

## Step 1 — Read reports

Read all files in monitoring/:
- monitoring/dependency-watch-latest.md
- monitoring/daily-brief-latest.md (if exists)
- monitoring/weekly-project-health-latest.md (if exists)
- monitoring/health-check-latest.md (if exists)
- monitoring/alerts/ (any files = active alerts)

Also read tasks/backlog.md header (P0/P1 items count).

## Step 2 — Produce briefing

Format (strict — phone-readable):
```
🟢/🟡/🔴 PROJECT STATUS — [date]

Security: [clean / N vulnerabilities found]
Infra: [healthy / degraded / unknown if no report]
Docs: [in sync / N drift items]
Backlog: [N high, N medium, N low items]
Alerts: [none / list active alerts]

Action needed: [none / list actions]
```

Use 🟢 if everything clean, 🟡 if attention items exist,
🔴 if any CRITICAL alert or P0 backlog item.

## Gotchas

- This is read on a phone. MAX 10 lines. No details unless asked.
- If a report file doesn't exist, say "no report yet" — don't error.
- If asked "more details on X", then expand that section only.
- Don't suggest fixes here. That's /remote-fix or /build territory.

STOP. Output the briefing and nothing else.
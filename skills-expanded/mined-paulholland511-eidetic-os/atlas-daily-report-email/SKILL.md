---
name: atlas-daily-report-email
description: Daily morning report email — job-search status, system health, and action items.
---

Send yourself a daily status report email using the SMTP send script.

> Placeholders: `{{USER_EMAIL}}` = recipient, `{{VAULT_PATH}}` = vault path,
> `{{EIDETIC_OS}}` = repo path, `{{JOB_TRACKER_PATH}}` = tracker `.xlsx` (personal,
> outside the repo). Credentials come from `SMTP_APP_PASSWORD` / `SENDER_EMAIL`
> env vars — never inline them.

**Email details:**
- Send command: `EIDETIC_TRIGGER=scheduled eidetic email --json '...'` (routes through the CLI so the run is audited)
- To: `{{USER_EMAIL}}`
- Subject: `📋 Eidetic Daily Report — [Day] [DD] [Month] [YYYY]`

**Step 1 — Gather data:**

1. Read the job tracker at `{{JOB_TRACKER_PATH}}` with `openpyxl`:
   - Count total applications, by status (Applied, Shortlisted, Interview, 2nd Interview, Rejected)
   - Find any with closing dates in the next 7 days
   - List the top 3 priority applications (interviews/shortlisted first)
2. Read `{{VAULT_PATH}}/.claude-morning-briefing.md` for today's highlights
3. Quick system checks (don't spend long):
   - Size + date of `$RAG_DIR/vectors.json`
   - Last embed time from `$RAG_DIR/last_embed.txt`
   - Count vault `.md` files (exclude `.git`, `.rag`, `.claude`, `.obsidian`)

**Step 2 — Build HTML email** with sections:

- **Job Search Update** — stats banner (Total | Applied | Shortlisted | Interview | Rejected), priority applications with status pills (green=interview, amber=shortlisted, blue=applied, red=rejected), upcoming closing dates flagged
- **Morning Briefing** — key highlights from the briefing (summarise, don't paste raw)
- **System Status** — vault file count, RAG vector count, last embed time, green/amber/red indicators
- **Action Items** — anything needing attention (closing dates, pending interviews, system issues)

**Step 3 — Send via SMTP:**
```bash
EIDETIC_TRIGGER=scheduled eidetic email --json '{"to":"{{USER_EMAIL}}","subject":"...","body_html":"..."}'
```

Sign off as Eidetic.

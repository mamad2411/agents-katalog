# Email Autoresponder Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

This skill replicates the "Integration Email" Make.com scenario. For each incoming sales lead notification email sitting in your inbox queue (loaded from CSV), it:

1. Pulls the raw email body
2. Calls GPT-4 to write a short, spartan, personalized reply (tuned to the prospect's inquiry)
3. Calls GPT-4 again in parallel to extract the prospect's email address from the body
4. Waits 90 seconds (humanizing delay)
5. Sends the reply to the extracted address via SMTP with subject "Email received—talk to you soon"
6. Logs each sent reply to `data/output.csv`

Original Make flow: `TriggerNewEmail` → `Write Customized Reply (GPT-4)` + `Extract Email Address (GPT-4)` → `Sleep 90s` → `ActionSendEmail`.

## When to trigger

Use this when you want to autoprocess a batch of raw lead notification emails and fire personalized replies automatically. Feed it a CSV of unprocessed emails, run it, done.

Trigger phrase: "run email autoresponder" or "process lead emails"

## Required env vars

```
OPENAI_API_KEY=sk-...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASS=your-app-password
SMTP_FROM=your@email.com
```

## Input CSV format (`data/input.csv`)

| Column | Description |
|--------|-------------|
| `id` | Unique row ID |
| `email_body` | Full text body of the lead notification email |
| `received_at` | ISO timestamp when the email was received |

## Output CSV format (`data/output.csv`)

| Column | Description |
|--------|-------------|
| `id` | Input row ID |
| `recipient_email` | Extracted email address |
| `reply_body` | GPT-generated reply that was sent |
| `sent_at` | ISO timestamp of send |
| `status` | `sent` or `error` |
| `error` | Error message if status=error |

## Step-by-step procedure

1. **Populate input** — put your lead emails in `data/input.csv` (or point to any CSV path)
2. **Set env vars** — add the keys above to your `.env` or export them in your shell
3. **Run**:
   ```bash
   python3 scripts/autoresponder.py
   # optional flags:
   #   --input  path/to/input.csv   (default: data/input.csv)
   #   --output path/to/output.csv  (default: data/output.csv)
   #   --delay  90                  (seconds to wait before sending, default: 90)
   #   --dry-run                    (generate replies but skip actual sends)
   ```
4. **Check output** — `data/output.csv` has every row with status + the reply body
5. **Retry errors** — filter `status=error` rows, fix the cause, rerun with just those rows

## How to use this

### If you use Claude Code
1. Download and unzip the attached folder.
2. Drop it into `.claude/skills/` in your project (so you have `.claude/skills/email-autoresponder-flow/SKILL.md`).
3. Invoke it by describing what you need, or type `/email-autoresponder-flow`. Claude picks it up automatically from the description.

### If you use a different AI agent
The SKILL.md file is just structured instructions in plain English. Open it, paste the contents into your agent's system prompt or instructions field (Cursor rules, custom GPT instructions, etc.), and keep the scripts folder alongside — the instructions reference those scripts and any agent that can run code can use them.

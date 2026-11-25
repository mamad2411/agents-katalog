# New Calendar Booking -> Update CRM Record in ClickUp

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

When a new calendar booking comes in (via webhook from Calendly, Cal.com, or any booking tool), this skill looks up the lead's ClickUp CRM task by matching the booking email against a `Lead Email` custom field, then updates the task's `Stage` custom field to `Meeting Booked`.

Translated from Make scenario: `1. New Calendar Booking -> Update CRM Record in ClickUp`.

Node-by-node map:
| # | Original module | What it does |
|---|---|---|
| 1 | `gateway:CustomWebHook` ("Agency Demo Call Calendar Booking") | Receives the booking payload. Key field: `payload.responses.email.value` |
| 2 | `clickup:getListTasks` (list `901701807723`, ordered by `updated`, limit `50`) | Pulls open tasks from the Leads CRM list |
| 3 | `clickup:editATask` (filter: `Lead Email == booking email`) | Sets `Stage` custom field (`91e9a139-8496-4ea4-a587-ec98cca57818`) to `Meeting Booked` option ID (`4df2006b-918a-4a46-a776-87c444e8dfc3`) |

The CSV in this skill acts as an **event log** — each processed booking gets a row written to `data/output.csv` with the outcome (matched / not matched, task ID updated). Nothing in the original workflow reads from a spreadsheet, so there's no data-source to replace; the CSV is purely for audit and local testing.

---

## When to trigger

Use this whenever you need to:
- Replay a booking that failed to update ClickUp
- Batch-process a CSV of past bookings that were missed
- Test the match logic locally before wiring up a live webhook

For live webhook use: run `scripts/server.py` to spin up a local webhook receiver (or deploy it to your server of choice).

---

## Required env vars

Set these before running. No hardcoded credentials anywhere.

```
CLICKUP_API_KEY=pk_xxxx          # ClickUp personal API token
CLICKUP_LIST_ID=901701807723     # The CRM Leads list (override if yours differs)
CLICKUP_STAGE_FIELD_ID=91e9a139-8496-4ea4-a587-ec98cca57818   # "Stage" custom field ID
CLICKUP_STAGE_MEETING_BOOKED=4df2006b-918a-4a46-a776-87c444e8dfc3  # "Meeting Booked" option ID
```

Copy these into a `.env` file or export in your shell. The scripts load them via `os.environ` — never hardcoded.

---

## Step-by-step procedure

### Option A — process a single booking from the command line

```bash
python3 scripts/run.py --email "lead@example.com"
```

Fetches tasks from ClickUp, finds the one whose `Lead Email` matches, updates Stage to Meeting Booked, logs result to `data/output.csv`.

### Option B — batch process a CSV of missed bookings

1. Put your bookings in `data/input.csv`. Required column: `email`. Optional: `booked_at`, `name`.
2. Run:

```bash
python3 scripts/run.py --input data/input.csv
```

Processes each row, writes results (task_id, matched, updated, error) to `data/output.csv`.

### Option C — live webhook server

```bash
python3 scripts/server.py --port 8080
```

Starts a lightweight HTTP server that accepts POST requests with a booking payload shaped like the original Make webhook (`payload.responses.email.value`). On each hit, runs the same match-and-update logic and logs to `data/output.csv`.

---

## How to use this (Claude Code install)

### If you use Claude Code
1. Download and unzip the attached folder.
2. Drop it into `.claude/skills/` in your project (so you have `.claude/skills/new-calendar-booking-update-crm-record-i/SKILL.md`).
3. Invoke it by describing what you need, or type `/new-calendar-booking-update-crm-record-i`. Claude picks it up automatically from the description.

### If you use a different AI agent
The SKILL.md file is just structured instructions in plain English. Open it, paste the contents into your agent's system prompt or instructions field (Cursor rules, custom GPT instructions, etc.), and keep the scripts folder alongside — the instructions reference those scripts and any agent that can run code can use them.

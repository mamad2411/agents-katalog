# ClickUp Stage Change to Awaiting Proposal -> Send Followup Email

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

When a ClickUp task moves into the "Awaiting Proposal" stage, this skill fires a follow-up email to the lead. It:

1. Receives a webhook payload from ClickUp containing the task ID.
2. Fetches the full task from the ClickUp API (to get custom fields: lead email + source platform).
3. Extracts the lead's first name from the task name (splits on space, takes word at index 1 — same logic as the original Make flow).
4. Maps the source platform code to a human label (1 = Instagram, 2 = Facebook).
5. Sends a personalized HTML email via SMTP thanking them for the call and letting them know a proposal is coming in 2-3 hours.
6. Appends a log row to `data/output.csv` (task ID, lead email, name, platform, timestamp, status).

No LLM involved — this is 100% deterministic. The email body is a fixed template matching the original flow exactly.

---

## When to trigger

- Someone calls this manually with a webhook payload JSON file (for testing/replay).
- A ClickUp automation POSTs a webhook to the configured endpoint when a task status changes to "Awaiting Proposal".
- You want to replay a missed send from `data/input.csv` (one row per event).

---

## Env vars required

```
CLICKUP_API_KEY=pk_...          # ClickUp personal API token
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=info@yourdomain.com
SMTP_PASS=your-app-password
SMTP_FROM=info@yourdomain.com   # optional, defaults to SMTP_USER
```

Add these to a `.env` file in the skill root or export them in your shell before running.

---

## Step-by-step

### Option A: replay from CSV (batch / test mode)

1. Populate `data/input.csv` with rows (columns: `task_id`, `lead_email`, `lead_first_name`, `source_platform`). A fake sample is already there.
2. Run:
   ```
   python3 scripts/send_followup.py --mode csv --input data/input.csv
   ```
3. Check `data/output.csv` for results.

### Option B: single webhook payload (live / manual trigger)

1. Save the raw ClickUp webhook body to a file, e.g. `payload.json`:
   ```json
   { "id": "abc123xyz" }
   ```
2. Run:
   ```
   python3 scripts/send_followup.py --mode webhook --payload payload.json
   ```
   The script fetches the task from ClickUp, extracts fields, sends the email, logs to `data/output.csv`.

### Option C: expose an HTTP webhook endpoint

Run the lightweight Flask listener so ClickUp can POST directly:
```
python3 scripts/webhook_server.py --port 5000
```
Point your ClickUp automation to `http://your-server:5000/webhook`. Each POST triggers the full flow automatically.

---

## Email template (matches original Make flow exactly)

```
Subject: Thanks for the call

Hi {first_name},

Thanks for the call earlier & happy I was able to meet you from {source_platform}. Just letting you know that I'll work on a proposal immediately and have something over to you in the next 2-3 hours.

Stay tuned & let me know if you have any questions.

Thanks,
Nick
```

Source platform is resolved as: `1` → Instagram, `2` → Facebook. Any other value sends the raw value as-is.

---

## Files

```
SKILL.md                  <- you are here
scripts/
  io_store.py             <- CSV/Sheets I/O helper (verbatim pattern)
  send_followup.py        <- main entry point (CSV + webhook modes)
  webhook_server.py       <- optional Flask listener for live ClickUp POSTs
  clickup_client.py       <- thin ClickUp API wrapper
  email_sender.py         <- SMTP send helper
data/
  input.csv               <- sample input rows for test mode
  output.csv              <- created on first run; log of sends
TESTING.md                <- test plan skeleton
```

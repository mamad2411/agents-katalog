# Payment Completed -> Create Trello Board & Send Email

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

When a payment is marked complete, this skill fires three things at once:

1. Creates a new Trello board named after the client's company ("Acme Corp Board"), grabs the first default list, and drops two onboarding task cards on it — swag box (due in 2 days) and a Loom intro video (due in 3 days).
2. Logs the sale to a CSV (or optionally Google Sheets) with date, company, amount, client name, salesperson, and email.
3. Sends the client a personal welcome email with a direct link to their new Trello board.

Converted from a Make.com scenario ("Payment Completed -> Create Trello Board & Send Email"). The original used Google Sheets; this version defaults to local CSV.

---

## When to trigger this

Use this after a payment is confirmed — Stripe webhook, CRM pipeline stage change, manual entry, or anything that produces these fields:

- `paymentStatus` (should be `true`)
- `emailAddress`
- `amount`
- `companyName`
- `firstName`
- `lastName`
- `commissionSalesperson`

Either pass the data as CLI args, or add a row to `data/input.csv` and run the script.

---

## Env vars required

```
TRELLO_API_KEY        # from https://trello.com/app-key
TRELLO_TOKEN          # OAuth token from the same page
SMTP_HOST             # e.g. smtp.gmail.com
SMTP_PORT             # e.g. 587
SMTP_USER             # sending email address
SMTP_PASSWORD         # app password or SMTP credential
EMAIL_FROM            # display name / address in the From header
```

Optional (for Google Sheets mode only):
```
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/...
```

---

## Step-by-step procedure

1. **Read input** — load `data/input.csv` via `io_store.read_rows()`. Each row is one payment event. Skip rows where `paymentStatus` is not `true`.

2. **Create Trello board** — call `scripts/trello_ops.py create_board --company_name "{companyName}"`. Returns `board_id`, `board_url`, `board_short_url`.

3. **Get first list** — call `scripts/trello_ops.py get_first_list --board_id {board_id}`. Returns `list_id`.

4. **Create swag card** — `scripts/trello_ops.py create_card --list_id {list_id} --name "Send them a swag box." --description "Log into swag.com, enter the client information, and ship their swag box (type A)." --position top --due_days 2`

5. **Create video card** — `scripts/trello_ops.py create_card --list_id {list_id} --name "Record a video introduction." --description "Salesperson to record a brief, customized 3min Loom introduction to welcome them aboard and improve consolidation/reduce churn." --position bottom --due_days 3`

6. **Log to store** — build a result row with `date, companyName, amount, firstName, lastName, commissionSalesperson, emailAddress, board_url` and append via `io_store.write_rows()` to `data/output.csv`.

7. **Send welcome email** — call `scripts/send_email.py` with the client's email, first name, company name, salesperson name, and the board URL/short URL.

---

## Run it

```bash
# Single payment from CSV row(s):
python3 scripts/run.py

# Or point at a specific input file:
python3 scripts/run.py --input /path/to/payments.csv --output /path/to/results.csv
```

All steps run sequentially per row. Failed Trello or email calls print an error and skip that row (they don't crash the whole batch).

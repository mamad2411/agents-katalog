# Photography CRM Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Three-part CRM automation for a photography business. A new lead comes in (from a website form, a spreadsheet, wherever) and this skill:

1. **Creates a ClickUp task** for the client with all their details as custom fields (name, email, phone, package, amount, shoot date).
2. **Sends three emails immediately**: a booking confirmation, an invoice summary, and a prep-tips reminder.
3. On a separate run, **sends reminder emails** to every open task in the list a day before the session.
4. On a separate run, **sends reminder SMS messages** via Twilio to every open task in the list.

Original Make.com workflow: 3 scenarios — "New Lead in ClickUp", "Reminder Email", "Reminder Texts".

---

## Env vars required

```
CLICKUP_API_KEY       # ClickUp personal API token
CLICKUP_LIST_ID       # ClickUp list ID where tasks live (default: 901701902540)
CLICKUP_ASSIGNEE_ID   # ClickUp user ID to assign tasks to
SMTP_HOST             # SMTP server hostname
SMTP_PORT             # SMTP port (e.g. 587)
SMTP_USER             # SMTP login
SMTP_PASS             # SMTP password
SMTP_FROM             # From address for outgoing emails
TWILIO_ACCOUNT_SID    # Twilio account SID
TWILIO_AUTH_TOKEN     # Twilio auth token
TWILIO_FROM_NUMBER    # Twilio sending number (e.g. +15673472003)
```

---

## When to trigger

- **New lead:** run `new_lead.py` whenever a form submission or intake row lands in `data/input.csv`. Each unprocessed row = one new client to onboard.
- **Reminder emails:** run `reminder_email.py` daily (morning of shoot day or day before) — it pulls all open ClickUp tasks and emails every client in the list.
- **Reminder SMS:** run `reminder_sms.py` daily (typically day before the session) — same pull, sends a text instead.

---

## Step-by-step procedure

### Flow 1 — Onboard a new lead

1. Add the client row to `data/input.csv` (or let the CSV accumulate from a form intake):
   - Columns: `first_name, last_name, email, phone, package, shoot_date (MM/DD/YYYY), amount`
2. Run:
   ```bash
   python3 scripts/new_lead.py --input data/input.csv
   ```
3. For each unprocessed row the script will:
   - POST to ClickUp and create a task named `FirstName LastName` with all custom fields populated.
   - Send three emails to the client: booking confirmation, invoice, and prep tips.
   - Write results (task_id, status) to `data/output.csv`.

### Flow 2 — Send reminder emails

1. Run:
   ```bash
   python3 scripts/reminder_email.py
   ```
2. Pulls all open tasks from the configured ClickUp list and sends each client a session reminder email.

### Flow 3 — Send reminder SMS

1. Run:
   ```bash
   python3 scripts/reminder_sms.py
   ```
2. Pulls all open tasks from the configured ClickUp list and texts each client via Twilio.

---

## Node map (Make → script)

| Make module | Script | Notes |
|---|---|---|
| `util:SetVariables` (WordPress Webhook) | `read_rows()` on input.csv | Each CSV row = one trigger |
| `clickup:createTaskInList` | `new_lead.py` → `create_clickup_task()` | Custom fields: FirstName, LastName, Email, Phone, Amount Paid, Package |
| `email:ActionSendEmail` (×3 in Flow 1) | `new_lead.py` → `send_email()` | Confirmation, invoice, prep tips; 2s delay between each |
| `clickup:getListTasks` (Flow 2) | `reminder_email.py` → `get_clickup_tasks()` | |
| `email:ActionSendEmail` (Flow 2) | `reminder_email.py` → `send_email()` | Reminder email per task |
| `clickup:getListTasks` (Flow 3) | `reminder_sms.py` → `get_clickup_tasks()` | |
| `twilio:SendSMS` (Flow 3) | `reminder_sms.py` → `send_sms()` | |

---

## Package options

The original workflow maps package names to ClickUp custom field option IDs. The skill uses the string names directly and maps them in the ClickUp POST body. Valid values: `newborn`, `pregnancy`, `family`.

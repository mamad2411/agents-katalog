# My 7-Figure Hiring System

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Three-stage sales-hiring pipeline, originally built for 1SecondCopy. Connects Typeform (application intake), ClickUp (candidate tracking), and SMTP email (interview invites) into a hands-off flow.

**Stage 1 — Ingest:** Watches for new Typeform submissions on the sales hiring form. Pulls the latest response, extracts the candidate's name, email, and Loom video URL, then creates a ClickUp task in your hiring list with custom fields populated.

**Stage 2 — Interview Round 1:** Triggered when you move a ClickUp task to the "Interviewing 1" stage (or run the script manually). Fetches the candidate's details from ClickUp, sends a personalized HTML email inviting them to book a round-1 interview, and posts the email body as a comment on the task (audit trail).

**Stage 3 — Interview Round 2:** Same as Stage 2 but fires for "Interviewing 2". Sends the final-round invite with a different booking link and slightly warmer tone (they already passed one interview).

---

## When to trigger

- **Run Stage 1** any time you want to sweep Typeform for new applications and push them into ClickUp. Set it on a cron (e.g. every 30 min) or run manually after a hiring push.
- **Run Stage 2** after you review a batch of applicants in ClickUp and move the good ones to "Interviewing 1".
- **Run Stage 3** after round-1 interviews are done and you move candidates to "Interviewing 2".

---

## Setup (one-time)

1. Copy the `.env.example` block below into a `.env` file next to the scripts folder (or set these as shell env vars):

```
TYPEFORM_API_TOKEN=your_typeform_pat
TYPEFORM_FORM_ID=tOLIVk8u          # replace with your actual form ID
CLICKUP_API_TOKEN=your_clickup_token
CLICKUP_LIST_ID=901701862775        # replace with your hiring list ID
CLICKUP_ASSIGNEE_ID=26314840        # ClickUp user ID to auto-assign
CLICKUP_CF_FIRST_NAME=4d9de377-6b69-4f9e-9e9c-7ae432cfa989
CLICKUP_CF_LAST_NAME=08dbf845-3063-497a-a939-964b5590e676
CLICKUP_CF_EMAIL=117cbb6a-4d56-48e0-beb3-ed316546ba12
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=hiring@yourcompany.com
SMTP_PASS=your_app_password
EMAIL_FROM=hiring@yourcompany.com
COMPANY_NAME=Your Company Name
INTERVIEW_1_LINK=https://cal.com/your-name/discovery
INTERVIEW_2_LINK=https://cal.com/your-name/final-interview
```

2. If your ClickUp list uses different custom-field IDs for First Name, Last Name, and Email, update the three `CLICKUP_CF_*` vars. Find IDs via the ClickUp API: `GET /list/{list_id}/field`.

3. For Gmail SMTP, use an App Password (not your main password). Two-factor must be on. Docs: https://support.google.com/accounts/answer/185833

---

## Step-by-step procedure

### Stage 1: Ingest new applications

```bash
# Pull latest Typeform responses and create ClickUp tasks for new ones
python3 scripts/ingest_application.py

# Dry run (no tasks created, just shows what would happen)
python3 scripts/ingest_application.py --dry-run

# Custom input/output paths
python3 scripts/ingest_application.py --input /path/to/ledger.csv --output /path/to/results.csv
```

What it does:
1. Sleeps 2 seconds (mirrors original workflow delay to let Typeform finalize the submission)
2. Fetches up to 10 recent responses from your Typeform
3. Skips any response token already in `data/input.csv`
4. Extracts: first name, last name, email, Loom URL, sold-5k-plus boolean
5. Creates a ClickUp task named `{First} {Last}` with those fields set
6. Appends processed rows to `data/output.csv`

### Stage 2: Send round-1 interview invite

```bash
# Single task (paste the ClickUp task ID)
python3 scripts/send_interview_email.py --task-id 9abc123def --stage 1

# Batch: all rows in output.csv that don't yet have stage1_sent set
python3 scripts/send_interview_email.py --stage 1

# Dry run
python3 scripts/send_interview_email.py --stage 1 --dry-run
```

What it does:
1. Fetches the ClickUp task to get First Name and Candidate Email custom fields
2. Renders the round-1 HTML email (personalized with first name and booking link)
3. Sends via SMTP
4. Posts the email HTML as a comment on the ClickUp task
5. Marks `stage1_sent=1` in the CSV row

### Stage 3: Send round-2 interview invite

```bash
python3 scripts/send_interview_email.py --task-id 9abc123def --stage 2
# or batch:
python3 scripts/send_interview_email.py --stage 2
```

Same flow as Stage 2, different email template and booking link.

---

## Data files

| File | Purpose |
|------|---------|
| `data/input.csv` | Processed-token ledger — prevents re-sending for duplicate Typeform entries |
| `data/output.csv` | Running record of all candidates: name, email, ClickUp task ID, sent flags |

Columns in `data/output.csv`:

```
token, submitted_at, first_name, last_name, email, loom_url, sold_5k, clickup_task_id, status, stage1_sent, stage2_sent
```

---

## Notes

- The original Make scenario used a ClickUp webhook to trigger email sends when a task moved stages. The script version replaces that with explicit `--stage` flag so you control exactly when emails go out — less surprising, easier to audit.
- Email templates are verbatim from the original scenario (minor personalizations: `{first_name}`, booking links, company name).
- ClickUp custom-field IDs in the defaults match the original account. If you clone this to a new ClickUp workspace, those IDs will differ — update the `CLICKUP_CF_*` env vars.
- No Google Sheets or Airtable nodes in the original workflow, so no sheet migration needed here.

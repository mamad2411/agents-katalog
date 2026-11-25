# Automatic Invoice Collection System

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Two-part system that handles the full invoice follow-up cycle automatically:

**Workflow 1 — Chase overdue invoices.** Reads your invoice list, finds every row with status `Overdue`, calculates how many days since the invoice was sent, and creates a pre-written draft follow-up email in Gmail at the right escalation stage (7 / 14 / 21 / 28 / 35 / 42 days). Each draft has a different tone, getting progressively more direct. You review and send; nothing goes out without you seeing it.

**Workflow 2 — Mark paid on Stripe webhook.** Listens for Stripe `invoice.payment_succeeded` events, looks up the customer's email, finds them in your invoice CSV, and flips their status from `Overdue` to `Paid`. No manual updating.

---

## When to trigger

- **Invoice chasing:** run `collect.py` daily (cron or manually) to generate that day's follow-up drafts for any overdue invoice hitting the 7/14/21/28/35/42-day mark.
- **Payment marking:** run `stripe_webhook_handler.py` as a server process (or deploy to Modal/Railway) to listen for incoming Stripe webhook events and auto-update statuses.
- Or: just ask me "chase overdue invoices" / "mark invoice paid for [email]" and I'll run the relevant script.

---

## Sheet / CSV columns (in order)

| Index | Column | Description |
|-------|--------|-------------|
| 0 | `date_sent` | Date invoice was sent (YYYY-MM-DD) |
| 1 | `invoice_id` | Your invoice ID or reference |
| 2 | `amount` | Invoice amount (e.g. 1500.00) |
| 3 | `client_name` | Client first name (used in email body) |
| 4 | `project` | Project or service description |
| 5 | `client_email` | Client email address |
| 6 | `due_date` | Payment due date (YYYY-MM-DD) |
| 7 | `status` | `Overdue`, `Paid`, `Pending`, etc. |

---

## Step-by-step procedure

### Workflow 1 — Chase overdue invoices

1. Make sure `data/input.csv` has your invoices with the columns above. Status column should be `Overdue` for invoices you want to chase.
2. Set `SMTP_USER` and `SMTP_PASSWORD` in your `.env` (or export them) so the script can authenticate to Gmail SMTP to create drafts. Alternatively set `EMAIL_DRAFTS_ONLY=true` to just print drafts to stdout without sending.
3. Run:
   ```bash
   python3 scripts/collect.py --input data/input.csv
   ```
4. The script prints which drafts it would create (or creates them via SMTP if credentials are set). Review and send from Gmail Drafts.
5. Output CSV (`data/output.csv`) is written with an added `last_followup_day` column tracking which follow-up stage each invoice is at.

### Workflow 2 — Mark paid via Stripe webhook

1. Set `STRIPE_WEBHOOK_SECRET` in your `.env` (from Stripe dashboard → Webhooks → your endpoint).
2. Run the webhook server:
   ```bash
   python3 scripts/stripe_webhook_handler.py --input data/input.csv --output data/input.csv
   ```
   (Writing back to `input.csv` keeps the single source of truth updated in place. Use a different `--output` path if you want a separate file.)
3. Forward Stripe webhook events to the running server. For local testing use [Stripe CLI](https://stripe.com/docs/stripe-cli): `stripe listen --forward-to localhost:5050/webhook`
4. When a `invoice.payment_succeeded` event comes in, the script finds the customer email in `input.csv` and updates their `status` to `Paid`.

### Manual mark-paid (no webhook)

```bash
python3 scripts/collect.py --mark-paid customer@example.com --input data/input.csv
```

---

## Environment variables

| Variable | Required for | Notes |
|----------|-------------|-------|
| `STRIPE_WEBHOOK_SECRET` | Workflow 2 | From Stripe dashboard → Webhooks |
| `SMTP_USER` | Workflow 1 drafts | Your Gmail address |
| `SMTP_PASSWORD` | Workflow 1 drafts | Gmail app password (not account password) |
| `EMAIL_DRAFTS_ONLY` | Optional | Set to `true` to print drafts to stdout instead of SMTP |
| `SKILL_STORE` | Optional | Set to `sheets` to switch from CSV to Google Sheets |
| `GOOGLE_APPLICATION_CREDENTIALS` | Sheets mode only | Path to service account JSON |
| `SKILL_SHEET_URL` | Sheets mode only | Google Sheet URL |

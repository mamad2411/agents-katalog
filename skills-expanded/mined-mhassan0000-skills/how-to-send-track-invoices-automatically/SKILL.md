# How to Send & Track Invoices Automatically With Stripe

Automates the full invoice lifecycle: when a ClickUp task hits "Send Invoice" status, Stripe auto-creates a customer, line item, and invoice and fires it off. When the client pays, Stripe fires a webhook back and the task status updates automatically in ClickUp. Zero manual billing steps.

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Two Make.com scenarios that work together:

**Scenario A — Send Invoice on ClickUp Status Change**
1. ClickUp fires a webhook when a task status changes to "Send Invoice"
2. The full task is fetched from ClickUp (gets email, package name, amount from custom fields)
3. A Stripe Customer is created (or reused) with that email + name
4. A Stripe Invoice Item is added (line item = package name + amount × 100 for cents)
5. A Stripe Invoice is created (collection method: `send_invoice`, auto-advance on)
6. The invoice is finalized and emailed to the client automatically

**Scenario B — Update ClickUp on Payment**
1. Stripe fires a `payment_intent.succeeded` (or other) event
2. The Stripe Customer is retrieved from the payment intent
3. ClickUp is searched for a task matching that customer email (custom field lookup)
4. The matching task's status is updated to "Paid" (via custom field ID)

The scripts here let you simulate both flows locally against `data/input.csv` before you wire up the live APIs.

---

## When to trigger this skill

- "set up stripe invoicing from clickup"
- "automate invoice sending when task status changes"
- "update clickup when stripe payment comes in"
- "run the invoice simulation"
- "test the invoice pipeline locally"

---

## Required env vars

```
STRIPE_API_KEY=sk_live_...           # Stripe secret key
CLICKUP_API_KEY=pk_...               # ClickUp personal API token
CLICKUP_TEAM_ID=14199321             # Your ClickUp workspace ID
CLICKUP_SPACE_ID=90170754355         # Space that holds your client list
CLICKUP_LIST_ID=901702430105         # List ID where client tasks live
CLICKUP_EMAIL_FIELD_ID=bf8f086c-cc23-4e3c-8980-0cbc029abaff   # Custom field: Email
CLICKUP_STATUS_FIELD_ID=33fe3d83-3281-4ca4-9999-61dbc43102d3  # Custom field: Status
CLICKUP_PAID_OPTION_ID=e3b5a6a6-b283-4359-9277-b9eab129dfa3   # Dropdown option: Paid
```

Copy these into a `.env` file at the skill root (or export in your shell). Never hardcode them in scripts.

---

## Step-by-step procedure

### 1. Prepare your input CSV

Edit `data/input.csv` with real client rows (or leave the fake sample for testing):

| Column | What it maps to |
|---|---|
| `task_id` | ClickUp task ID |
| `client_name` | Full name (used for Stripe Customer) |
| `client_email` | Email (used for Stripe + ClickUp lookup) |
| `package_name` | Invoice line item description |
| `amount_usd` | Dollar amount (script converts to cents) |
| `status` | Current status — set to `send_invoice` to trigger Scenario A |

### 2. Simulate Scenario A (send invoices)

```bash
python3 scripts/send_invoices.py --input data/input.csv --output data/output.csv
```

This reads every row where `status == send_invoice`, calls the Stripe API to create customer + invoice item + invoice + finalize, and writes results (invoice ID, Stripe customer ID, invoice URL) to `output.csv`.

Dry-run mode (no real API calls, just prints what would happen):
```bash
python3 scripts/send_invoices.py --input data/input.csv --dry-run
```

### 3. Simulate Scenario B (mark paid in ClickUp)

```bash
python3 scripts/mark_paid.py --input data/output.csv
```

This takes the output from step 2 (or any CSV with `client_email`), searches ClickUp for the matching task, and updates its status to Paid.

Dry-run:
```bash
python3 scripts/mark_paid.py --input data/output.csv --dry-run
```

### 4. Wire up live webhooks (Make.com)

Once local tests pass, import the two JSON files from the source zip into Make.com:

- `ClickUp Status = Send Invoice -- Send Stripe Invoice.json` → Scenario A
- `Watch Payment Intent -- Update ClickUp.json` → Scenario B

Reconnect your Stripe and ClickUp credentials on any node showing a warning. Update the ClickUp list/space/field IDs to match yours (they're hardcoded in the mapper nodes). Set up the ClickUp webhook to hit Scenario A's webhook URL when status changes.

---

## Files

```
scripts/
  io_store.py         # CSV/Sheets I/O helper (verbatim pattern)
  send_invoices.py    # Scenario A: read CSV -> Stripe customer+invoice
  mark_paid.py        # Scenario B: read CSV -> ClickUp status update
data/
  input.csv           # Sample input (fake data, testable)
  output.csv          # Written by send_invoices.py
TESTING.md
```

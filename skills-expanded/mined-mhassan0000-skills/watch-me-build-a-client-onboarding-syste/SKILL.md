# Watch Me Build A Client Onboarding System Using Hidden APIs

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Fully automated client onboarding triggered by a Stripe subscription event. When a new customer subscribes, the system:

1. Grabs the customer record from Stripe (email, name, metadata)
2. Duplicates a template ClickUp dashboard for the client using ClickUp's hidden (undocumented) internal API
3. Renames that dashboard to the client's name
4. Sends an internal email to your team with the new client's info
5. Sends a welcome email to the client with their personal ClickUp dashboard link

The "hidden API" is the interesting part — ClickUp doesn't expose dashboard copy/rename in their public API, so this uses the same internal endpoint the ClickUp web app itself hits (`/dashboard/{id}/copy` + `/dashboard/{id}`), with a browser-spoofed User-Agent to make it through. That's the trick shown in the source video.

In skill form, the Stripe webhook trigger is replaced by a CSV of new clients to process. Each row gets the full onboarding treatment.

---

## When to trigger

- Someone says "run the client onboarding script"
- A new Stripe subscriber needs a ClickUp dashboard + welcome email
- You want to batch-onboard clients from a CSV
- You're adapting the original Make workflow into a local runnable script

---

## Required env vars

Set these in your shell or a `.env` file before running:

```
STRIPE_API_KEY=sk_live_...           # Stripe secret key (for customer lookup)
CLICKUP_API_KEY=pk_...               # Your ClickUp API token (found in ClickUp Settings → Apps)
CLICKUP_TEMPLATE_DASHBOARD_ID=dhagt-202   # The dashboard ID to duplicate as template
CLICKUP_TEAM_ID=14199321             # Your ClickUp workspace/team ID
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@yourdomain.com
SMTP_PASS=your_app_password
TEAM_EMAIL=team@yourdomain.com       # Internal team notification recipient
FROM_EMAIL=you@yourdomain.com
```

---

## Input CSV format

`data/input.csv` — one row per new client to onboard:

| column | description |
|--------|-------------|
| `stripe_customer_id` | Stripe customer ID (e.g. `cus_ABC123`) |
| `email` | Client email address |
| `name` | Client full name |
| `first_name` | First name for personalized welcome email |
| `plan_name` | Subscription plan name |
| `subscription_id` | Stripe subscription ID |
| `status` | Leave blank — filled in by script (`done` / `error`) |

---

## Step-by-step procedure

1. Fill in `data/input.csv` with client rows (or let it populate from a Stripe export)
2. Set all env vars above
3. Run the main script:
   ```
   python3 scripts/run_onboarding.py
   ```
4. The script processes each row that doesn't already have `status=done`:
   - Calls Stripe to verify/enrich the customer record
   - Duplicates the template ClickUp dashboard via hidden API
   - Renames the new dashboard to `{client_name} Dashboard`
   - Sends internal team notification email
   - Sends welcome email to client with dashboard link
   - Marks the row `status=done` in `data/output.csv`
5. Check `data/output.csv` for results — `clickup_dashboard_id` and `clickup_dashboard_url` are written back per row

---

## Scripts

| file | what it does |
|------|-------------|
| `scripts/run_onboarding.py` | Entry point. Reads input CSV, loops rows, orchestrates all steps |
| `scripts/clickup_client.py` | Duplicate + rename dashboard via ClickUp hidden API |
| `scripts/email_client.py` | Send internal team email + client welcome email via SMTP |
| `scripts/io_store.py` | CSV/Sheets I/O helper (standard pattern) |

---

## Notes on the hidden API

ClickUp's dashboard endpoints used here are not in their public docs. The workflow spoofs a Chrome browser User-Agent and `Sec-Ch-Ua` header to hit:

- `POST https://prod-us-west-2-3.clickup.com/dashboard/{template_id}/copy` — duplicates the dashboard
- `PUT  https://prod-us-west-2-3.clickup.com/dashboard/{new_id}` — renames it

These may break if ClickUp changes their internal API (that's the tradeoff with hidden endpoints). If they do, check the Network tab in Chrome DevTools on app.clickup.com to find the new route.

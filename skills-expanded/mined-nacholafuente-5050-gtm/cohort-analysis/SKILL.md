---
name: cohort-analysis
description: Build a full SaaS cohort analysis from a CRM (Attio/Stripe/CSV) joined to revenue (Stripe/Attio/CSV). Outputs a styled Excel workbook with conditional formatting (Customer Churn, MRR Churn, CAC Payback) plus per-section CSVs. Use when the user says "/cohort-analysis", "build a cohort table", "cohort analysis for <client>", "retention by signup month", or "show me NRR by cohort". One-shot, no warehouse, no cron.
---

# Cohort Analysis

Builds the full SaaS cohort suite from a CRM + money source: 11 sub-tables across 3 sections (Customer Churn, MRR Churn, CAC Payback) in a single Excel workbook with green→red conditional formatting, plus per-section CSVs for SQL/raw consumption.

## Step 1: Ask the user 3 questions (5 if they want CAC payback)

Ask in order. Don't skip. Don't pick defaults silently.

1. **Where do your clients live?** (CRM source)
   - `attio`, Attio Persons or Companies, `created_at` is the cohort key
   - `stripe`, Stripe Customers themselves (no separate CRM)
   - `csv`, paste a path to a CSV with columns `customer_id`, `email`, `signup_date`

2. **Where's the money?** (revenue source)
   - `stripe`, Stripe Invoices (paid)
   - `attio`, currency attribute on a CRM record (requires extra info, see Step 1b)
   - `csv`, path to CSV with columns `customer_id` (or `email`), `event_date`, `amount`

3. **Want CAC payback analysis?** (optional)
   - `yes`, they paste a path to a `cohort,cac_amount` CSV. Section 3 of the workbook will show cumulative gross profit vs CAC and flag the lifetime month each cohort breaks even.
   - `no / skip`, workbook will only include the first two sections.

4. **Gross margin?** (only if they said yes to #3)
   - Default is `0.8` (80%). Most SaaS companies are 70-85%.

5. **Output format?**
   - `all` (default, xlsx workbook + per-section CSVs)
   - `xlsx`, workbook only
   - `csv`, per-section CSVs only
   - `sql`, also dump SQL DDL+inserts
   - `evidence`, also bootstrap a DuckDB+Evidence project

## Step 1b: Attio money source disclaimer (IMPORTANT)

If they picked **Attio for money**, STOP and show this verbatim before going further:

> ⚠️ **Heads up, Attio doesn't store revenue history natively.** It only holds current attribute values, so we have to reconstruct the timeline from date attributes on each customer record. To do that I need three attribute slugs:
>
> 1. **Amount per period**: the recurring amount (e.g. `mrr`, `arr`, `subscription_amount`, `monthly_value`)
> 2. **Date paid / first invoice**: when they started paying (e.g. `date_paid`, `subscription_start`, `first_invoice_date`)
> 3. **Date churned**: *optional*. When they stopped paying. Leave blank and we'll assume they're still active today.
>
> Each customer becomes one event per month between date-paid and date-churned at the amount you give. **This works for steady-state subscriptions** but won't capture mid-cycle upgrades, downgrades, partial refunds, or one-off charges. For real revenue accuracy, point me at Stripe instead, or export your billing data to CSV.
>
> What are the three Attio attribute slugs? (paste them as `amount=mrr date_paid=date_paid date_churned=date_churned`)

Wait for them to give you the 3 slugs (or 2, if they're skipping `date_churned`).

## Step 2: Confirm env vars are set

| Source | Env var |
|--------|---------|
| Attio (CRM or money) | `ATTIO_API_KEY` |
| Stripe (CRM or money) | `STRIPE_SECRET_KEY` |
| CSV | none, just a path |

Run `python skills/cohort-analysis/run.py --check-env --crm <X> --money <Y>` to validate. If a key is missing, stop and tell the user to add it.

## Step 3: Run

```bash
python skills/cohort-analysis/run.py \
  --crm <attio|stripe|csv> \
  --money <stripe|attio|csv> \
  --cacs <path-to-cacs.csv> \           # optional, enables CAC payback section
  --gross-margin 0.8 \                  # default 0.8
  --output <all|xlsx|csv|sql|evidence> \
  --out-dir /tmp/cohort-<client>-<date>
```

Optional flags:
- `--attio-object companies|people` (default `companies`)
- `--attio-amount-attr <slug>` (required if `--money attio`)
- `--attio-date-paid-attr <slug>` (required if `--money attio`)
- `--attio-date-churned-attr <slug>` (optional, only if `--money attio`)
- `--csv-customers <path>` (only if `--crm csv`)
- `--csv-revenue <path>` (only if `--money csv`)
- `--cohort-grain month|quarter` (default `month`)

## Step 4: KPIs the user gets

Every run produces these metrics for every cohort × lifetime month:

**Customer-side (Section 1 of the workbook, 5 sub-tables)**
- **Retained customers**: count of cohort C still paying at lifetime month M
- **Churned customers**: count who churned that specific period
- **% retained customers**: customer retention curve (the "GRR shape")
- **% churned vs base**: monthly churn rate normalized to cohort starting size
- **% churned vs previous month**: period-over-period churn rate

**Revenue-side (Section 2 of the workbook, 5 sub-tables)**
- **Retained MRR**: dollars each cohort is paying every month since signup
- **MRR churn**: signed: positive = lost dollars, negative = expansion
- **% retained MRR**: **NRR** (Net Revenue Retention), the headline VC metric
- **% MRR churn vs base**: monthly dollar churn normalized to M0 MRR
- **% MRR churn vs previous month**: period-over-period dollar churn

**Unit economics (Section 3 of the workbook, only if `--cacs` given)**
- **Cumulative gross profit** per cohort, month by month (`retained_mrr × gross_margin`, accumulated)
- **CAC payback period**: first lifetime month each cohort's cumulative GP exceeds its CAC
- **"Profitable since M_n"** flag, or "Not yet profitable"

**Per-cohort base stats (in `00_summary.csv` and the workbook headers)**
- **Cohort base size**: # of customers signed up that month
- **M0 MRR**: initial cohort revenue
- **CAC** (if provided)
- **Profitable since**: computed
- **Max observable lifetime month**: per-cohort cutoff inferred from your data

## Step 5: Output files

Default output (`--output all`) writes to `/tmp/cohort-<client>-<date>/`:

- **`cohort_workbook.xlsx`**: the styled Excel file (open in Excel/Numbers/Sheets). Three stacked sections with conditional formatting: Customer Churn, MRR Churn, CAC Payback (only if CACs given).
- `cohort_table.csv`, headline retained-MRR matrix (familiar shape, opens directly)
- `00_summary.csv`, one row per cohort: base counts, base MRR, CAC, profitable-since
- `01_retained_customers.csv` through `11_cac_payback_cumulative_gross_profit.csv`, every sub-table as its own CSV
- `audit_customers.csv` + `audit_revenue.csv`, everything that fed the join, for traceability

## Step 6: After running

Show a 4-line summary:
- N customers, N revenue events, N cohorts
- Path to `cohort_workbook.xlsx`
- One-line read of the matrix (`quick_summary` output: e.g. "Jan-2026 cohort: 80 customers @ $7,851 MRR → M9: 64 customers, 81% MRR retained")
- If CACs were given: how many cohorts have paid back, how many haven't.

## When to use

- User says `/cohort-analysis` or "cohort analysis for <client>"
- A client asks for retention/NRR by signup month, gross profit per cohort, or CAC payback
- Quarterly review of a SaaS book of business
- A founder is preparing investor materials and needs to show NRR + payback

## When NOT to use

- The client wants a continuously refreshing dashboard → recommend ChartMogul or Baremetrics, don't build this.
- The client has <10 customers per cohort → cohorts aren't statistically useful, just show a churn list instead.

## Try it without API keys

The `examples/` folder ships with a richer fixture (8 cohorts, ~12 months of history, CAC values). Run end-to-end:

```bash
python skills/cohort-analysis/run.py \
  --crm csv --money csv \
  --csv-customers skills/cohort-analysis/examples/customers.csv \
  --csv-revenue skills/cohort-analysis/examples/revenue.csv \
  --cacs skills/cohort-analysis/examples/cacs.csv \
  --gross-margin 0.8 \
  --output all \
  --out-dir /tmp/cohort-demo

open /tmp/cohort-demo/cohort_workbook.xlsx
```

## Notes

- Joins are on `email` (lowercased) by default. Stripe customers usually carry email; Attio Persons too. For Companies → Stripe, falls back to `domain` match.
- CSV mode is the universal escape hatch, if the user has an "alternative" billing system (Qonto, Chargebee, custom), they export to CSV and we ingest it.
- No data is sent anywhere. Everything stays local in `/tmp/cohort-<client>-<date>/`.
- The xlsx writer requires `openpyxl`. If it's not installed, the skill still produces all the CSVs; the .xlsx is skipped with a friendly message.

---
name: cfo-skill
description: Read-only CFO data dashboard for bootstrapped startups. Two modes, CSV templates (works with any stack: Attio/HubSpot/Salesforce + Qonto/Mercury/Brex + Stripe + Moss/Ramp/Pleo) or live API pull from Attio + Qonto + Stripe + Moss. Computes runway, burn rate, MRR/ARR, NRR, customer concentration, AR aging, DSO, vendor spend, departmental burn. Outputs an Excel workbook with 8 sheets. Use when the user asks "what's our runway?", "how much cash do we have?", "what's our burn?", "who are our biggest customers?", "where is spend going?", "what's our MRR?", "AR aging?". Read-only by design. NOT financial, legal, tax, or investment advice.
---

# CFO Skill

> ## ⚠️ DISCLAIMER
>
> **This skill displays data. It is NOT financial, legal, tax, accounting, or investment advice.**
>
> Numbers may be stale, miscategorized, or reflect bugs in upstream systems. Frameworks below (LTV:CAC, runway, burn multiple, Rule of 40) are heuristics, not guarantees. Decisions about hiring, fundraising, distributions, taxes, or solvency must be made by you in consultation with a qualified CFO, accountant, lawyer, or tax advisor. The author and contributors accept no liability for decisions made based on this skill's output.

---

## Two ways to use it

### Mode 1: CSV templates (works with any stack)

Drop four CSVs into a folder, run one command, get an Excel workbook. Works with **any** CRM/bank/billing stack, Attio, HubSpot, Salesforce, Pipedrive, Mercury, Brex, Stripe, Chargebee, Ramp, Pleo, whatever.

Templates live in [`templates/`](templates/). Realistic example data lives in [`examples/`](examples/) so you can try the pipeline before plugging in real data.

```bash
python skills/cfo-skill/run.py --source csv --csv-dir ./my-data --output cfo.xlsx
```

CSV schemas (column headers in `templates/`):

| File | Columns |
|------|---------|
| `customers.csv` | `customer_id, customer_name, status, signed_up_at, churned_at, mrr, plan` |
| `cash_movements.csv` | `date, account, direction, amount, currency, counterparty, category, department, note` |
| `invoices.csv` | `invoice_id, customer, issued_at, due_at, amount, currency, status` |
| `balances.csv` | `account, currency, balance, as_of` |

`status` values: `active`, `churned`, `lead` (only `active` counts toward MRR). `direction` values: `in`, `out`. Invoice `status` values: `paid`, `unpaid`, `draft`.

### Mode 2: Live API pull (Attio + Qonto + Stripe + Moss)

Set credentials in your environment, run the puller, get the same Excel workbook from live data.

```bash
python skills/cfo-skill/run.py --source api --providers all --output cfo.xlsx
```

Or pick specific providers, they run in the order you list, and **later writers win** on `customers.csv` / `invoices.csv`:

```bash
python skills/cfo-skill/run.py --source api --providers qonto,stripe,moss      # Stripe-billed SaaS
python skills/cfo-skill/run.py --source api --providers qonto,attio,moss        # CRM-driven (no Stripe)
python skills/cfo-skill/run.py --source api --providers qonto,attio,stripe,moss # both, Stripe wins on MRR
```

Provider-by-provider:

| Provider | Writes | Best at | Reference |
|----------|--------|---------|-----------|
| **Stripe** | `customers.csv` (with real MRR), `invoices.csv` | Authoritative SaaS revenue. **Use this if you bill via Stripe.** | [references/stripe.md](references/stripe.md) |
| **Attio** | `customers.csv` | CRM-driven customer state, plan, lifecycle | [references/attio.md](references/attio.md) |
| **Qonto** | `balances.csv`, `cash_movements.csv`, `invoices.csv` | Bank truth, cash position, transactions, AR | [references/qonto.md](references/qonto.md) |
| **Moss** | appends to `cash_movements.csv` | Categorized card spend, vendors, departments | [references/moss.md](references/moss.md) |

Each puller writes its slice to a temp folder; the same compute layer then generates the Excel workbook. **You don't have to use all four.** A Stripe + Mercury founder can run `--providers stripe` and use CSV templates for the bank side. A HubSpot + Brex founder skips API mode entirely and uses CSV for everything.

---

## Required environment variables

Only set the ones for providers you actually use.

| Provider | Variables |
|----------|-----------|
| Stripe | `STRIPE_SECRET_KEY` (use a restricted key with read on customers, subscriptions, invoices, payouts) |
| Attio | `ATTIO_API_KEY`. Optional: `ATTIO_MRR_ATTR`, `ATTIO_STATUS_ATTR`, `ATTIO_ACTIVE_VAL`, `ATTIO_CHURNED_ATTR`, `ATTIO_PLAN_ATTR`, `ATTIO_NAME_ATTR` |
| Qonto | `QONTO_API_KEY` + `QONTO_SECRET_KEY` (the "secret key" is your Qonto org slug) |
| Moss | `MOSS_KEY_ID` + `MOSS_SECRET_KEY` (OAuth client credentials, scope `read`) |

Skill is read-only, never request `write` scopes. Never log or echo a secret.

---

## What the workbook contains

Eight sheets:

1. **Summary**: headline metrics with heuristic flags (runway, concentration, DSO, burn multiple)
2. **Cash Flow**: monthly inflows / outflows / net for the trailing 3 months
3. **Customers**: full customer table from your input data
4. **Concentration**: top 1 / 5 / 10% of MRR + top-10 customer table
5. **AR Aging**: unpaid invoices bucketed (current, 1-30, 31-60, 61-90, 90+) + per-invoice detail
6. **Spend**: by category, by vendor, by department
7. **Recurring Vendors**: heuristic detection (3+ similar transactions)
8. **Disclaimer**: full disclaimer in-workbook

---

## Computed metrics

| Metric | Formula | Heuristic flags |
|--------|---------|-----------------|
| Cash balance | sum of bank account balances | - |
| Runway | cash ÷ trailing 3-month avg net burn | <12 mo red, 12-24 mo yellow |
| Burn multiple | net burn ÷ MRR | >2× red |
| MRR / ARR | sum of active customer MRR × 12 | - |
| Customer concentration | top-N MRR ÷ total MRR | >25% top-1 red |
| AR aging | unpaid invoices bucketed by days past due | 60+ days red |
| DSO | (AR ÷ 90d issued sales) × 90 days | <30 green, >60 red |
| Spend by category | sum of outflows grouped by `category` | - |
| Top vendors | sum of outflows grouped by `counterparty` | - |
| Recurring vendors | counterparty appearing 3+ times in trailing window | - |
| Departmental burn | sum of outflows grouped by `department` | - |

Frameworks used (LTV:CAC, Rule of 40, Magic Number, etc.) live in [references/metrics-benchmarks.md](references/metrics-benchmarks.md). Bootstrapped case studies in [references/case-studies.md](references/case-studies.md).

---

## What this skill does NOT do

- ❌ Make recommendations on hiring, raises, distributions, or fundraising
- ❌ Give tax, legal, or accounting advice
- ❌ Project cash flow into the future as a "forecast" you can rely on
- ❌ Determine whether your company is solvent
- ❌ Write to any of the connected systems (read-only by design)

For any of these: "I can show you the numbers. The decision is for you and a qualified advisor."

---

## How Claude should answer a CFO question

1. **Restate the question in numerical terms.** ("What's our runway?" → "I need cash balance and trailing 3-month net burn.")
2. **Identify which provider(s) to query** from the table above, or which CSV(s) to read.
3. **Run** `run.py` with appropriate flags, or read the CSVs directly via `cfo.load_all()` + `cfo.summarize()`.
4. **Show raw numbers first, then computed metric, then framework.**
5. **Repeat the disclaimer** when the user is making a real decision.
6. **Flag data quality issues** explicitly (stale data, missing fields, miscategorized expenses).

---

## Attribution

Frameworks, benchmarks, and case studies adapted from [EveryInc/charlie-cfo-skill](https://github.com/EveryInc/charlie-cfo-skill) (MIT, © 2026 Every).

Data layer (Stripe + Attio + Qonto + Moss pullers + CSV templates + Excel writer) by 5050Growth.

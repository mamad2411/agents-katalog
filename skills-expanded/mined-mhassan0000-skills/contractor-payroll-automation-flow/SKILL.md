# Contractor Payroll Automation Flow

Automates end-of-month contractor payroll across three pay structures: hourly rate, project-based, and flat salary. Pulls contractor data, computes totals, generates line-item invoices, and optionally creates real Google Docs from a template.

Source workflows: Make (Integromat) — three scenarios (Hourly Rate, Project Based, Flat Salary). APIs: ClickUp (staff + time entries), Google Docs (invoice generation from template).

---

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Three pay modes, all handled by one script:

**Hourly Rate** — reads each contractor's `hourly_rate` and `hours_this_period`, multiplies them, formats as `X hours at $Y/hr: $Z`.

**Project Based** — reads a JSON list of project name + budget pairs from the `projects` column, sums all budgets, generates one line item per project.

**Flat Salary** — reads `monthly_salary` and emits a single `Monthly Fee: $X` line.

For each contractor the script:
1. Computes the subtotal
2. Writes a plaintext invoice to `data/invoices/<name>.txt`
3. Appends a summary row to `data/output.csv`
4. Optionally creates a real Google Docs invoice from your template (if `--create-gdocs` + env vars are set)

The Google Docs template expects these placeholders: `{{date}}`, `{{name}}`, `{{totalAmount}}`, `{{emailAddress}}`, `{{aggregatedLineItems}}`.

---

## When to trigger this

Say any of:
- "run payroll"
- "generate contractor invoices"
- "process this month's contractor payments"
- "create invoices for my team"

---

## Input CSV schema

`data/input.csv` columns:

| column | required | notes |
|---|---|---|
| `name` | yes | contractor full name |
| `email` | yes | for invoice header |
| `pay_type` | yes | `hourly`, `project`, or `flat` |
| `hourly_rate` | hourly only | decimal, USD |
| `hours_this_period` | hourly only | decimal hours |
| `monthly_salary` | flat only | decimal, USD |
| `projects` | project only | JSON array: `[{"name":"...", "budget": 0.00}]` |

A fake testable sample is at `data/input.csv`. Edit in place or point `--input` at another file.

---

## Step-by-step procedure

1. Populate `data/input.csv` with your contractors (or use `--live-clickup` to pull from ClickUp).
2. Run the script (see commands below).
3. Check `data/invoices/` for per-contractor `.txt` invoices.
4. Check `data/output.csv` for the payroll summary.
5. If you want real Google Docs: set the env vars below and add `--create-gdocs`.

---

## Scripts

### Main entry point

```bash
# Basic run (CSV in, CSV out + .txt invoices)
python3 scripts/run_payroll.py

# Custom paths
python3 scripts/run_payroll.py --input /path/to/contractors.csv --output /path/to/payroll_summary.csv

# Pull live data from ClickUp instead of CSV
python3 scripts/run_payroll.py --live-clickup

# Also create Google Docs invoices
python3 scripts/run_payroll.py --create-gdocs
```

### Helper

`scripts/io_store.py` — CSV/Sheets switch, imported by `run_payroll.py`. Don't call directly.

---

## Environment variables

### ClickUp (only needed with `--live-clickup`)

```
CLICKUP_API_TOKEN    personal API token from app.clickup.com/settings/apps
CLICKUP_TEAM_ID      workspace ID (visible in URL)
CLICKUP_STAFF_LIST   list ID for staff tracker
CLICKUP_TASKS_LIST   list ID for project tasks (project-based mode)
```

### Google Docs (only needed with `--create-gdocs`)

```
GOOGLE_APPLICATION_CREDENTIALS   path to service account JSON file
GDOCS_TEMPLATE_ID                 document ID of your invoice template
GDOCS_OUTPUT_FOLDER_ID            Drive folder ID to save invoices into
```

### Google Sheets (only if switching storage to Sheets)

```
SKILL_STORE=sheets
SKILL_SHEET_URL       full URL to your Google Sheet
GOOGLE_APPLICATION_CREDENTIALS   same service account file
```

---

## Node map (source Make scenarios → script)

### Scenario 1: Hourly Rate

| Make node | script equivalent |
|---|---|
| `clickup:getListTasks` (List Staff Members) | `read_rows("data/input.csv")` or `fetch_staff_from_clickup()` |
| `clickup:listTimeEntries` (List Time Entries) | `fetch_time_entries_clickup()` — hours last 30d |
| `util:SetVariables` (Set Hourly Rate & Total) | `calc_hourly()` — hours × rate |
| `builtin:BasicRouter` branch 0 | `util:FunctionAggregator2` Sum Total → `subtotal` var |
| `builtin:BasicRouter` branch 1 | `util:TextAggregator` Generate Line Items + `google-docs:createADocumentFromTemplate` |
| `google-docs:createADocumentFromTemplate` | `create_google_doc()` with `--create-gdocs` |

### Scenario 2: Project Based

| Make node | script equivalent |
|---|---|
| `clickup:getListTasks` (List Staff Members) | `read_rows()` |
| `clickup:getListTasks` (project tasks, by assignee) | `projects` JSON column in CSV |
| `util:FunctionAggregator2` Sum Total | `calc_project()` sums all budgets |
| `util:TextAggregator` Generate Line Items | line per project in `calc_project()` |
| `google-docs:createADocumentFromTemplate` | `create_google_doc()` |

### Scenario 3: Flat Salary

| Make node | script equivalent |
|---|---|
| `clickup:getListTasks` (List Staff Members) | `read_rows()` |
| `google-docs:createADocumentFromTemplate` | `calc_flat()` + `create_google_doc()` |

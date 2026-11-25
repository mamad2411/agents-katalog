---
name: my-consumption-plan
description: Generate My Consumption Plan (MCP) notes per account for AEs with auto-populated data from Salesforce and Logfood. Use when preparing weekly business review updates, MCP notes, forecast summaries, or consumption plans.
user-invocable: true
---

# My Consumption Plan (MCP) Notes Generator

Generate structured MCP notes **per account** for weekly business reviews. Pulls pre-computed metrics from GTM Gold tables in Logfood, UCO data and next steps from Salesforce, and auto-summarizes commentary from UCO next steps. Outputs a formatted summary for each account with WoW changes, UCOs with dollar amounts, QoQ/YoY growth, auto-generated notes, and per-account risks.

## Prerequisites

Before running, ensure the following are authenticated:
1. **Salesforce** - Run `/salesforce-authentication` if needed
2. **Databricks (Logfood)** - Run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood` if needed

## How to Invoke

Run `/my-consumption-plan` with optional arguments:
- `/my-consumption-plan` — generate MCP notes for yourself (all accounts)
- `/my-consumption-plan Jane Smith` — generate MCP notes for a specific AE (all their accounts)
- `/my-consumption-plan Jane Smith Acme` — generate MCP notes for a specific AE, specific account only

## Workflow

### Phase 1: Identify User & Resolve Identity

1. Read `~/.vibe/profile` to get the current user's name and email
2. If an AE name was provided as argument, resolve their email and Salesforce User ID:
   ```sql
   SELECT Id, Name, Email FROM User WHERE Name LIKE '%AE_NAME%' AND IsActive = true
   ```
3. Store the **email** (for Logfood queries), **Salesforce User ID** (for UCO queries), and **AE email address** (for sending notes at the end)
4. Stamp: `[AE Name] - [YYYY-MM-DD HH:MM]`

**CRITICAL — Column name reference:**
- `individual_obt_gtm`: scope with `user_email = 'email'` | date via `fiscal_year` + `fiscal_quarter` (NO snapshot_date)
- `rpt_account_movers`: scope with `concatenated_emails LIKE '%email%'` | date via `snapshot_date`
- `rpt_mv_account_pop_latest_snapshot`: check columns with DESCRIBE first

### Phase 2: Pull AE-Level Summary from Logfood

Use the `field-data-analyst` agent (subagent_type: `fe-internal-tools:field-data-analyst`). **Always use `--profile=logfood`.**

Load the `logfood-querier` skill first for warehouse ID and auth.

**Step 2a: AE-level forecast summary from `individual_obt_gtm`**

**CRITICAL: Always filter by fiscal_year AND use `dbu_dollars_qtd IS NOT NULL` to get only the current active quarter (future quarters have null actuals).**

```sql
SELECT
  user_name,
  user_email,
  fiscal_year,
  fiscal_quarter,
  submitted_ae_forecast,
  submitted_ae_forecast_wow,
  submitted_my_call,
  submitted_my_call_wow,
  submitted_weighted_projection,
  submitted_weighted_projection_wow,
  actuals_or_submitted_forecast_qoq_pct,
  actuals_or_submitted_forecast_yoy_pct,
  attainment_weighted_projection,
  dbu_dollars_qtd_attainment,
  gap_submitted_my_call,
  gap_weighted_projection,
  target_dbu_dollars,
  dbu_dollars_qtd,
  forecast_ds,
  forecast_ds_wow
FROM main.gtm_gold.individual_obt_gtm
WHERE user_email = 'AE_EMAIL'
  AND fiscal_year >= YEAR(CURRENT_DATE()) AND fiscal_year <= YEAR(CURRENT_DATE()) + 1
  AND dbu_dollars_qtd IS NOT NULL
ORDER BY fiscal_year DESC, fiscal_quarter DESC
LIMIT 1
```

This returns the **current active quarter** (the most recent quarter with actual consumption data). Future quarters have null `dbu_dollars_qtd` and are excluded. Use this single row for the AE-level header. Prior week forecast = `submitted_ae_forecast - submitted_ae_forecast_wow`.

**Step 2b: Account-level movers (per account)**

```sql
SELECT
  account_name,
  account_id,
  date_range,
  snapshot_date,
  current_period_sum,
  prior_period_sum,
  dbu_growth,
  dbu_growth_perc,
  move_type,
  current_period_submitted_weighted_projection,
  prior_period_submitted_weighted_projection
FROM main.gtm_gold.rpt_account_movers
WHERE concatenated_emails LIKE '%AE_EMAIL%'
  AND snapshot_date = (SELECT MAX(snapshot_date) FROM main.gtm_gold.rpt_account_movers)
ORDER BY current_period_sum DESC
```

This returns **all accounts** for the AE with their WoW/period-over-period consumption changes. Group by `account_name` to build per-account sections.

### Phase 3: Pull UCO Data with Next Steps from Salesforce

Use the `field-data-analyst` agent. Use the Salesforce User ID from Phase 1.

**Step 3a: Get ALL active UCOs with dollar amounts AND next steps**

**CRITICAL: You MUST return `MonthlyTotalDollarDBUs__c` and `Next_Steps__c` for every UCO.**

```sql
SELECT Id, Name, Stages__c, Account_Name__c, Account__c,
       MonthlyTotalDollarDBUs__c, Implementation_Status__c,
       Health_Score__c, Full_Production_Date__c,
       Next_Steps__c, Last_Update__c
FROM UseCase__c
WHERE (Account_Executive_lookup__c = 'AE_USER_ID'
       OR OwnerId = 'AE_USER_ID')
AND Stages__c IN ('U1','U2','U3','U4','U5')
ORDER BY Account_Name__c, Stages__c DESC, MonthlyTotalDollarDBUs__c DESC
```

If `Next_Steps__c` doesn't exist, try `NextSteps__c`, `Next_Step__c`, or query the field names:
```bash
sf sobject describe UseCase__c --json | jq '.result.fields[] | select(.name | test("next|step"; "i")) | {name, label}'
```

**Step 3b: Group UCOs by account**

For each account, produce:
- List of UCOs with stage, dollar amount (monthly and quarterly = monthly * 3), health
- Summarized next steps: combine all UCO `Next_Steps__c` values into a concise account-level summary
- Count of UCOs per stage with dollar subtotals

### Phase 4: Assemble Per-Account MCP Notes

For **each account**, combine:

1. **Account consumption** from rpt_account_movers (Step 2b)
   - Current period sum, prior period sum, growth $, growth %
   - Weighted projection current vs prior
2. **UCOs** from Salesforce (Step 3)
   - Stage, name, quarterly dollar value, health
3. **Notes** auto-generated from UCO next steps
   - Summarize all Next_Steps__c for UCOs in this account into 2-3 concise sentences
   - Focus on: what's happening now, what's next, any blockers
4. **QoQ/YoY** from account movers (T91D growth as proxy) or from account_period_over_period if available

### Phase 5: Gather Per-Account Risk Input

Use AskUserQuestion to collect risks. Present the list of accounts and ask:

"For which accounts do you want to flag risks? Select all that apply, or choose 'No risks'."

For each flagged account, ask for: risk description, quantified impact, resolution plan/asks.

### Phase 6: Format & Output MCP Notes

Assemble the final output in this format:

```
=== My Consumption Plan (MCP) Notes ===
[AE Name] - [Date YYYY-MM-DD]
=========================================

AE Summary:
AE Forecast: $[X]K (WoW: +/-$[X]K)
Total QoQ: [X]% | Total YoY: [X]%
Target: $[X]K | Attainment: [X]%
QTD Actuals: $[X]K

-------------------------------------------
ACCOUNT: [Account Name 1]
-------------------------------------------
Consumption: $[current]K ([+/-X]K WoW, [+/-X]% T91D)
Weighted Projection: $[X]K (prior: $[X]K)

UCOs ([N] active):
  [Stage]: [UCO Name] — $[X]K/qtr [Health]
  [Stage]: [UCO Name] — $[X]K/qtr [Health]

Notes:
[Auto-summarized from UCO next steps — 2-3 sentences covering
 what's happening now, what's next, key milestones or blockers]

Risk(s): [Per-account risk or "None"]

-------------------------------------------
ACCOUNT: [Account Name 2]
-------------------------------------------
...

=========================================
```

### Phase 7: Email Notes to AE

After presenting the formatted notes, use AskUserQuestion to ask:

"Would you like to email these MCP notes to **[AE Name]** at **[ae_email]**? (Note: this will send an email to the AE's inbox, not to you.)"

Options: "Yes, send to [AE Name]" / "No, I'm done"

**Important:** The recipient is the AE identified in Phase 1 — this may be a different person than the current user. Always display the recipient's full name and email in the confirmation prompt so the user knows exactly who will receive the email.

If yes:
1. Use the **gmail skill** to send an email to the AE's email address (resolved in Phase 1)
2. **Subject:** `MCP Notes - [AE Name] - [YYYY-MM-DD]`
3. **CRITICAL: Send as plain text only** — do NOT use HTML formatting. The AE will paste these notes into another system, so the email body must be the exact same plain text output from Phase 6 (the `=== My Consumption Plan...` block). Use `gmail_builder.py send --body "..."` (NOT `--html`).
4. Confirm to the user that the email was sent, including the recipient address.

After the email prompt (whether sent or not), also mention:
- **go/mcpinsights** — for full account-level period-over-period detail

## Column Name Reference (CRITICAL)

GTM Gold tables do NOT use `individual_name`. Use the correct column names:

### `main.gtm_gold.individual_obt_gtm`
| Column | Type | Use |
|--------|------|-----|
| `user_name` | STRING | AE full name |
| `user_email` | STRING | **Best for filtering** — exact match |
| `user_id` | STRING | Salesforce User ID |
| `fiscal_year` | BIGINT | **Must filter** — use `>= YEAR(CURRENT_DATE()) AND <= YEAR(CURRENT_DATE()) + 1` to avoid null placeholder rows |
| `fiscal_quarter` | BIGINT | Fiscal quarter (1-4) |
| `dbu_dollars_qtd` | DOUBLE | QTD actuals — **use `IS NOT NULL` to identify the current active quarter** (future quarters have nulls) |
| `target_dbu_dollars` | DOUBLE | Target (NOT `target`) |

### `main.gtm_gold.rpt_account_movers`
| Column | Type | Use |
|--------|------|-----|
| `account_name` | STRING | Account name |
| `account_id` | STRING | Salesforce Account ID |
| `concatenated_emails` | STRING | **Comma-separated team emails** — use LIKE |
| `snapshot_date` | DATE | Filter to MAX(snapshot_date) |
| `date_range` | STRING | Period: "T7D", "T28D", "T91D" |
| `move_type` | STRING | "Positive" or "Negative" |
| `dbu_growth` | DOUBLE | Absolute dollar change |
| `dbu_growth_perc` | DOUBLE | Percent change |
| `current_period_submitted_weighted_projection` | DOUBLE | Current weighted projection |
| `prior_period_submitted_weighted_projection` | DOUBLE | Prior weighted projection |

### Salesforce `UseCase__c` (UCOs)
| Field | Use |
|-------|-----|
| `MonthlyTotalDollarDBUs__c` | Monthly dollar value. **Quarterly = * 3** |
| `Next_Steps__c` | Auto-populate account notes from this field |
| `Account_Name__c` | Group UCOs by account |
| `Account__c` | Account ID for joining |
| `Full_Production_Date__c` | Target go-live date |
| `Stages__c` | U1-U5 stage |
| `Health_Score__c` | Green/Yellow/Red |

## Key Pre-Computed Tables Reference

### AE-Level: `main.gtm_gold.individual_obt_gtm`
Pre-computed WoW/QoQ/YoY/attainment per rep. **Always filter fiscal_year.**

### Account Movers: `main.gtm_gold.rpt_account_movers`
Per-account growers/decliners. Scope with `concatenated_emails LIKE '%email%'`. Filter to `MAX(snapshot_date)`.

### Account PoP: `main.gtm_gold.rpt_mv_account_pop_latest_snapshot`
2,400+ pre-computed PoP columns per account (latest snapshot).

### Split Forecasts: `main.gtm_gold.individual_split_mcp_forecasts`
Has `prior_week_split_submitted_ae_forecast` for exact prior-week values.

### Stale — DO NOT USE:
- `individual_forecast_mcp_quarterly_history` — Last data Jan 2025

## Fallback Strategy

1. **If `individual_obt_gtm` returns nulls**: Check fiscal_year filter; try `individual_split_mcp_forecasts` for forecast data
2. **If `Next_Steps__c` is empty for a UCO**: Note "No next steps recorded" for that UCO
3. **If account has no movers data**: Note "No consumption change data available"
4. **If Logfood is inaccessible**: Use Salesforce only; note consumption as "unavailable — check go/mcpinsights"

## Example Output

```
=== My Consumption Plan (MCP) Notes ===
Jane Smith - 2026-02-26
=========================================

AE Summary:
AE Forecast: $500.0K (WoW: +$5.0K)
Total QoQ: 10.0% | Total YoY: 120.0%
Target: $450.0K | Attainment: 111.1%
QTD Actuals: $135.0K

-------------------------------------------
ACCOUNT: Acme Corp
-------------------------------------------
Consumption: $350.0K (+$35.0K T91D, +11.1%)
Weighted Projection: $380.0K (prior: $345.0K)

UCOs (3 active):
  U5: Data Pipeline Migration — $12K/qtr Green
  U3: ML Model Serving — $9K/qtr Yellow
  U1: Real-Time Analytics — $15K/qtr Green

Notes:
Data pipeline migration nearing completion, targeting prod
by end of quarter. ML model serving in validation phase
with performance benchmarking underway.

Risk(s): None

-------------------------------------------
ACCOUNT: GlobalTech Industries
-------------------------------------------
Consumption: $5.0K (+$3.0K T91D, +150.0%)
Weighted Projection: $6.0K (prior: $2.0K)

UCOs (2 active):
  U4: ETL Modernization — $30K/qtr Green
  U2: BI Dashboard Refresh — $15K/qtr Green

Notes:
ETL modernization pilot running successfully, planning
scale-out to remaining data sources next month.

Risk(s): None

-------------------------------------------
ACCOUNT: Northern Services Inc
-------------------------------------------
...

=========================================
```

## Integration with Other Skills

- **`fe-salesforce-tools:salesforce-actions`** — UCO queries with Next_Steps__c
- **`fe-internal-tools:logfood-querier`** — Logfood auth, warehouse setup
- **`fe-internal-tools:field-data-analyst`** — Agent for executing data queries
- **`fe-internal-tools:genie-rooms`** — GTM Genie rooms for additional insights
- **`fe-google-tools:google-docs`** — Optional: create Google Doc with MCP notes

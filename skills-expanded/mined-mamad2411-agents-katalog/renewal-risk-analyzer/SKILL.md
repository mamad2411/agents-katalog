---
name: renewal-risk-analyzer
description: Proactive renewal risk detection using multi-signal scoring (consumption, contract commitment, UCO health, support burden, engagement). Use weekly before renewal discussions or when Providence-style hidden risks (strong consumption but contract underburning) need detection.
user-invocable: true
---

# Renewal Risk Analyzer

## Why This Skill Exists

Traditional consumption analysis (like `/weekly-consumption`) shows WoW/SWLY growth but misses **structural misalignment**. The Providence Health case study proves this: $5.7M consumption with 8-15% WoW growth still churned because they burned only 50-60% of their $10M commitment over 2 years.

This skill uses a **5-signal scoring model** weighted toward contract alignment (30%) and engagement health (20%) vs raw consumption (20%). It catches accounts that look healthy on surface metrics but have renewal blockers.

### Distinct from Existing Skills

| Skill | Purpose | Key Difference |
|-------|---------|----------------|
| `/weekly-consumption` | Weekly consumption trends for forecast calls | Single-signal (consumption only). No contract, UCO, support, or engagement data. |
| `/consumption-vault-sync` | Store consumption to Delta + vault | Data pipeline, not risk scoring. No multi-signal analysis. |
| `/uco-consumption-analysis` | Validate UCO projections vs actuals | UCO-specific. No contract commitment or engagement signals. |
| `/renewal-risk-analyzer` (this) | Multi-signal renewal risk scoring | **Only skill** with contract underburn detection + 5-signal weighted model. |

## Prerequisites

1. **Logfood access**: Profile `logfood` authenticated (use `/logfood-querier` skill)
2. **Python 3**: Standard library only (no external dependencies)

## Usage

```bash
/renewal-risk-analyzer --account-id "0016100000cF3SpAAK" --account-name "Northwestern Medicine"
```

**Output**: JSON with risk_score (0-1), risk_category (Low/Medium/High), 5 signal breakdowns, red flags, and recommendations.

---

## Workflow (Automatic)

### Step 1: Authenticate with Logfood

Delegate to `/logfood-querier`:

```bash
# Check auth
databricks auth profiles | grep logfood

# If not authenticated
databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood
```

### Step 2: Select Warehouse

Use `/databricks-warehouse-selector --profile=logfood`

### Step 3: Execute SQL Queries

Run 5 parameterized queries from `queries/`. Each query uses `:account_id` as the sole parameter.

**Query sources and signal mappings:**

| Query File | Logfood Table | SQL Output Columns | Python Input Fields |
|------------|--------------|-------------------|---------------------|
| `contract_health.sql` | `fin_live_gold.consolidated_active_contracts` + `paid_usage_metering` | burn_rate_pct, time_elapsed_pct, commitment_gap, days_until_expiry, projected_burn_at_expiry_pct, annual_commit_value, contract_term_months, months_elapsed | Same names (1:1 match) |
| `consumption_summary.sql` | `fin_live_gold.daily_usage` | latest_4wk_avg, **wow_growth_pct**, **swly_growth_pct** | wow_growth_pct, swly_growth_pct, trend_velocity*, consumption_volatility* |
| `uco_health.sql` | `sfdc_bronze.usecase__c` | **open_uco_count**, **avg_days_in_stage**, **stage_regression_count**, **blocker_count**, **days_since_stage_change** | Same names (aggregated scalars) |
| `support_signals.sql` | `sfdc_bronze.case` | **p1_p2_count_90d**, avg_resolution_days, **open_escalation_count**, **open_oldest_days** | Same names (1:1 match) |
| `engagement_signals.sql` | `sfdc_bronze.event` + `opportunitycontactrole` | meetings_last_30d, **meetings_last_90d**, days_since_last_meeting, **champion_present** | Same names (1:1 match) |

*Fields marked with `*` are not produced by SQL queries and must be derived or passed as 0 if unavailable. `trend_velocity` and `consumption_volatility` require multi-week time series analysis not included in the single-row consumption summary.*

Execute each query via the Databricks SQL Statements API:

```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{
  "statement": "'"$(cat queries/contract_health.sql)"'",
  "warehouse_id": "<WAREHOUSE_ID>",
  "format": "JSON_ARRAY",
  "wait_timeout": "50s",
  "parameters": [{"name": "account_id", "value": "<ACCOUNT_ID>"}]
}'
```

Repeat for all 5 query files. Store each response in a temp directory:

```bash
TMPDIR=$(mktemp -d)
# contract_data -> $TMPDIR/contract_data.json
# consumption_data -> $TMPDIR/consumption_data.json
# uco_data -> $TMPDIR/uco_data.json
# support_data -> $TMPDIR/support_data.json
# engagement_data -> $TMPDIR/engagement_data.json
```

### Step 4: Run Analysis

Feed the query results into the scoring engine:

```bash
python3 renewal_risk_analyzer.py \
  --input "$TMPDIR/combined_input.json"
```

The analyzer accepts either a single JSON object or an array of account objects. Each object must include the fields documented in `SCHEMA.md` sections 1.1-1.5.

### Step 5: Present Results

Parse the JSON output and format for the user:

```
Renewal Risk: High (0.80)
Account: Northwestern Medicine
Renewal: 2026-06-02 (87 days)

Signal Breakdown:
  Consumption  [0.10] Strong growth: 12.5% WoW, 35.2% YoY
  Contract     [0.95] Projected to burn only 48% of $14.2M commit by expiry
  UCO          [0.70] UCO pipeline stalled - 52 days since last stage change
  Support      [0.40] Moderate support activity; 2 open escalations
  Engagement   [0.65] No exec sponsor engagement within 87 days of renewal

Override Applied: projected_burn < 50% AND days_until_expiry < 120
  Original composite: 0.52 -> Floor raised to 0.80

Red Flags:
  - Projected to burn only 48% of $14.2M annual commitment by contract expiry
  - Commitment gap of $8.5M despite strong consumption growth

Recommendations:
  1. Schedule executive business review to address commitment gap
  2. Explore right-sizing: propose commitment restructure tied to actual usage
  3. Identify 2-3 new workloads that could close the gap within 90 days
```

---

## Scoring Model Summary

### Signal Weights

| Signal | Weight | Rationale |
|--------|--------|-----------|
| Consumption | 0.20 | Important but insufficient alone -- Providence had strong consumption and still churned |
| Contract | 0.30 | Highest weight -- underburn is the #1 structural risk for churn at renewal |
| UCO | 0.15 | Pipeline health indicates future commitment likelihood |
| Support | 0.15 | Escalation burden erodes willingness to renew |
| Engagement | 0.20 | Champion loss and relationship decay are leading indicators |

### Override Rules

Certain conditions force a minimum risk score regardless of the composite:

| Condition | Minimum Score |
|-----------|---------------|
| projected_burn < 50% AND days_until_expiry < 120 | 0.8 |
| champion_changed AND NOT champion_present | 0.7 |
| open_uco_count == 0 AND days_until_expiry < 90 | 0.7 |

### Risk Categories

**Research-grounded thresholds** (per SCHEMA.md section 2.4, aligned with Gainsight/Gartner/internal models):

| Category | Score Range | Action |
|----------|-------------|--------|
| Low | 0.0 - 0.30 | Maintain current cadence |
| Medium | 0.30 - 0.60 | Proactive intervention recommended |
| High | 0.60 - 1.0 | Immediate action required; escalate to leadership |

---

## Integration with Other Skills

### With `/forecast`
Run renewal risk analyzer before weekly forecast calls. Include risk score in forecast notes. Proactively flag high-risk renewals to the team.

### With `/consumption-vault-sync`
Vault sync provides the consumption signal data. This skill layers contract/UCO/support/engagement on top for a complete renewal picture.

### With `/account-plan`
Include renewal risk score in account plans. Show multi-signal breakdown. Use recommendations as prioritized action items.

### With `/logfood-querier`
Delegates Logfood authentication and warehouse selection. All 5 SQL queries run against Logfood tables.

---

## Test Mode

Run without Logfood access using deterministic synthetic data:

```bash
python3 renewal_risk_analyzer.py --test
```

Uses `seed=42` for reproducible output. Generates 3 synthetic accounts:

| Account | Risk Category | Score | Pattern |
|---------|--------------|-------|---------|
| Acme Health Systems | High | ~0.80 | Providence pattern: strong consumption, severe contract underburn |
| Summit Financial Group | Medium | ~0.50 | Declining engagement, moderate metrics across signals |
| Coastal Analytics Inc | Low | ~0.10 | Healthy across all 5 dimensions |

Custom seed for variation:

```bash
python3 renewal_risk_analyzer.py --test --seed 99
```

---

## Artifacts

| File | Description |
|------|-------------|
| `SCHEMA.md` | Complete data model, scoring logic, and output schema |
| `renewal_risk_analyzer.py` | Python scoring engine (standard library only) |
| `queries/contract_health.sql` | Contract burn and commitment gap metrics |
| `queries/consumption_summary.sql` | WoW/SWLY consumption trends |
| `queries/uco_health.sql` | UCO pipeline health and staleness |
| `queries/support_signals.sql` | Support escalation and resolution metrics |
| `queries/engagement_signals.sql` | Meeting cadence and champion detection |

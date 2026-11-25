---
name: gcp-cost-anomaly-scan
description: Use to detect whether any GCP project has experienced an abnormal spend spike in the recent past, indicating possible API-key abuse or compromised credentials. READ-ONLY. Use standalone or as Phase 1b of `gcp-ironclad`.
---

# GCP Cost Anomaly Scan (READ-ONLY)

## Overview

For every billing account the caller can see, determines whether any project has experienced an abnormal spend spike in the last `LOOKBACK_DAYS` days (default 60). Uses the `gcp-finops` MCP server when available; otherwise falls back to direct `bq query` against billing-export tables.

> **Related native feature (July 2026):** Google's [Early Anomalies](https://docs.cloud.google.com/billing/docs/how-to/manage-anomalies#view-early-anomalies) (Preview) now does forward-looking, pre-invoice anomaly alerting with root-cause SKU attribution — but only for Gemini API, Agent Platform, Cloud Run, and Cloud Run functions, per project, in the console's Anomalies section. This skill remains the historical sweep across *all* services and billing accounts, and produces the `anomalies.json` later phases consume. When reporting, mention enabling Early Anomalies review as a complementary forward-looking control.

## When to Use

- Triggered by the `gcp-ironclad` driver as Phase 1b.
- Or invoked standalone when you suspect past abuse you may have missed.

## Inputs

- `SESSION_DIR` env var.
- `LOOKBACK_DAYS` env var (default `60`).
- `THRESHOLD_PCT` env var (default `200` — daily spend must be ≥200% over the 7-day rolling average to flag).
- `ACTIVE_HOURS` env var (default `24` — used to mark anomalies as still-active).

## Outputs

Writes `${SESSION_DIR}/anomalies.json` matching `output.schema.json`.

## Execution

### Step A: Establish session dir + list billing accounts

```bash
SESSION_DIR="${SESSION_DIR:-/tmp/gcp-ironclad/standalone-$(date -u +%Y-%m-%dT%H-%M-%SZ)}"
mkdir -p "${SESSION_DIR}/raw"
gcloud billing accounts list --format=json > "${SESSION_DIR}/raw/billing-accounts.json"
```

### Step B: For each billing account, determine export availability

For each account `B`:
1. First, try the `gcp-finops` MCP server (call its `discover_billing_tables` tool). If it returns a table for `B`, mark `hasExport: true`.
2. If MCP is unavailable, fall back to:
   ```bash
   bq ls --format=prettyjson "${QUOTA_PROJECT}:billing_export" 2>/dev/null \
     | jq -r '.[].tableReference.tableId' \
     | grep -E "gcp_billing_export_(resource_)?v1_${B//-/_}"
   ```
   where `${QUOTA_PROJECT}` is the project that owns the billing-export dataset. If the user doesn't know it, default to `gcloud config get-value project`.
3. If nothing is found, mark `hasExport: false` and emit an info-class error: `"no_billing_export"`.

### Step C: Per account with export — call `gcp-finops` anomalies

Preferred path (when MCP is available):

> Call `mcp__gcp-finops__anomalies(lookback_days=LOOKBACK_DAYS, threshold_pct=THRESHOLD_PCT)` and parse the markdown table from `result`.

Each row becomes one anomaly entry. Extract: date, gross net (if shown), and look up `topSku` via a second MCP call (`mcp__gcp-finops__sku_breakdown(service_name="<top service>", start_date=date, end_date=date)`).

### Step D: Direct BigQuery fallback

If MCP is not available, run:

```sql
WITH daily AS (
  SELECT
    DATE(usage_start_time) AS day,
    project.id             AS project,
    ROUND(SUM(cost), 2)    AS gross,
    ROUND(SUM(cost) + SUM((SELECT SUM(c.amount) FROM UNNEST(credits) c)), 2) AS net,
    ARRAY_AGG(sku.description ORDER BY cost DESC LIMIT 1)[OFFSET(0)] AS top_sku
  FROM `<PROJECT>.<DATASET>.gcp_billing_export_v1_<BILLING_ID>`
  WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL <LOOKBACK_DAYS> DAY)
  GROUP BY day, project
),
ranked AS (
  SELECT
    day, project, gross, net, top_sku,
    AVG(gross) OVER (
      PARTITION BY project
      ORDER BY day
      ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
    ) AS baseline
  FROM daily
)
SELECT * FROM ranked
WHERE baseline > 0 AND gross / baseline >= (<THRESHOLD_PCT> / 100.0);
```

Replace `<PROJECT>.<DATASET>` with the actual export table location.

### Step E: Mark active-in-24h

For each anomaly, set `activeIn24h: true` if the anomaly's `date` is within the last 24 hours OR if today's partial data already shows a comparable spike.

### Step F: Write anomalies.json + summary

Write the JSON (atomic, same pattern as audit.json), then print:

> Anomaly scan complete. Scanned N billing accounts (X with export / Y without). Found Z anomalies in the last `LOOKBACK_DAYS` days; A still active (>24h spike ongoing).

## Error handling

- No billing export for an account: emit `error` with `"context": "no_billing_export"` and continue. Do not attempt to create an export.
- BigQuery query permission denied: emit error; continue.
- `gcp-finops` MCP unavailable: fall back to direct `bq` and emit an info error.

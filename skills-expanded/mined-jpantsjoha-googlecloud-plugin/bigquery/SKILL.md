---
name: bigquery
description: "Query and manage data in Google BigQuery. Covers dataset and table management, IAM, cost-safe querying (dry-run first), partitioning, clustering, and bq CLI patterns. Always estimates cost before executing queries — BigQuery bills by bytes processed. Use when the user mentions: bigquery query, analytics on GCP, BigQuery IAM, BigQuery cost, bigquery partition, bigquery schema, sql on GCP."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "BigQuery, bigquery query, bq, dataset, analytics on GCP, BigQuery IAM, BigQuery cost, bigquery partition, bigquery schema, sql on GCP"
  "googlecloud-plugin/required-scopes": "bigquery.datasets.create, bigquery.datasets.get, bigquery.jobs.create, bigquery.jobs.get, bigquery.tables.create, bigquery.tables.getData, bigquery.tables.get"
  "googlecloud-plugin/mcp-servers": "google-bigquery"
---

# BigQuery

Serverless, highly scalable data warehouse. Bills per bytes processed — always dry-run before executing queries on large datasets.

## Safety Rule — Dry-Run First

```bash
# Estimate bytes before executing — always do this on unknown datasets
bq query --dry_run --use_legacy_sql=false 'SELECT * FROM dataset.table'
# Output: "Query successfully validated. Assuming the tables are not modified,
# running this query will process X bytes."
```

## Core Patterns

### Create a dataset

```bash
bq mk --dataset \
  --location=REGION \
  --description="Description" \
  PROJECT_ID:DATASET_NAME
```

### Run a query (with cost confirmation)

```bash
# 1. Dry-run first (see above)
# 2. Execute only after confirming cost
bq query --use_legacy_sql=false --location=REGION \
  'SELECT field FROM `project.dataset.table` LIMIT 100'
```

### Grant dataset access (least-privilege)

```bash
bq show --format=prettyjson PROJECT_ID:DATASET > /tmp/ds.json
# Edit roles in /tmp/ds.json, then:
bq update --source /tmp/ds.json PROJECT_ID:DATASET
```

### Create partitioned table (cost control)

```sql
CREATE TABLE dataset.table (
  event_date DATE,
  user_id STRING
)
PARTITION BY event_date
OPTIONS (partition_expiration_days = 365);
```

## Cost Controls

- Partition tables by date — queries on a partition scan only that partition
- Cluster tables by high-cardinality filter columns
- Set per-project quotas: IAM → Quotas → BigQuery — Query usage per day
- Use `LIMIT` in development; avoid `SELECT *` on multi-TB tables

## References

- [BigQuery Introduction](https://cloud.google.com/bigquery/docs/introduction)
- [BigQuery Access Control](https://cloud.google.com/bigquery/docs/access-control)
- [BigQuery Pricing](https://cloud.google.com/bigquery/pricing)
- [Performance Best Practices](https://cloud.google.com/bigquery/docs/best-practices-performance-overview)

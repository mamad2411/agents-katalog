---
name: azure-cosmos-autoscale
description: >
  Azure Cosmos DB autoscale (autopilot) throughput for owned accounts: max RU/s
  selection, container vs database throughput, partition key design interaction,
  normalized RU consumption metrics, and cost/latency trade-offs. Use when enabling
  or tuning autoscale, fixing 429 throttling, or comparing manual vs autoscale —
  not for unauthorized data access or cross-tenant enumeration.
---

# Azure Cosmos DB Autoscale

## Scope And Authorization

- **In scope:** Cosmos DB accounts/databases/containers you own or are authorized to operate.
- **Out of scope:** Reading production data without need; load tests that harm shared prod without approval.
- Throughput changes affect cost and throttling — use change windows for prod max RU adjustments.
- Pair security/network with private endpoints and RBAC; `code-quality-standards` for data access code.

## When To Use

- Spiky workloads where manual RU is either wasteful or under-provisioned.
- Recurring `429` / `RequestRateTooLarge` despite “enough” average RU.
- Choosing database-level vs container-level autoscale.
- Right-sizing max throughput from metrics (Normalized RU Consumption).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General backpressure / load shedding | `backpressure-patterns` |
| Key Vault secrets for connection strings | `azure-keyvault-basics` |
| Bigtable-style key design (GCP) | `bigtable-row-key-design` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Autoscale max RU/s | Ceiling; scales between ~10% and 100% of max (service rules apply) |
| Manual provisioned | Fixed RU; cheaper if flat utilization near max |
| Partition key | Hot partitions cause 429 even with high total RU |
| Serverless | Alternative for low/intermittent — different model |
| Tooling | `az cosmosdb`, Azure Monitor metrics, SDK retry policy |

## Workflow

### 1. Confirm scope and success criteria

1. Account, database, containers, region(s), SLA for latency/throttles, monthly cost budget.
2. Success: p99 latency acceptable; 429 rate under threshold; cost within budget at chosen max RU.
3. Note multi-region writes — throughput billing multiplies with regions.

### 2. Inventory throughput configuration

```bash
az account show
az cosmosdb show -g "$RG" -n "$ACCOUNT" --query "{cap:capabilities,kind:kind,loc:locations}"
az cosmosdb sql database throughput show -g "$RG" -a "$ACCOUNT" -n "$DB" 2>/dev/null || true
az cosmosdb sql container throughput show -g "$RG" -a "$ACCOUNT" -d "$DB" -n "$CONTAINER"
az cosmosdb sql container show -g "$RG" -a "$ACCOUNT" -d "$DB" -n "$CONTAINER" \
  --query "resource.partitionKey"
```

1. List which resources use autoscale vs manual vs serverless.
2. Pull metrics: Total Request Units, Normalized RU Consumption, Throttled Requests.
3. Identify hot partition keys from diagnostics if available.

### 3. Baseline workload

1. Chart RU/s over 7–14 days; note peaks vs idle.
2. Record 429 counts and affected operations (point read vs query vs write).
3. Estimate peak required RU with growth headroom (e.g. 1.5–2×).

### 4. Enable or tune autoscale

```bash
# Migrate container to autoscale with max 4000 RU/s (example)
az cosmosdb sql container throughput migrate -g "$RG" -a "$ACCOUNT" -d "$DB" -n "$CONTAINER" \
  --throughput-type autoscale

az cosmosdb sql container throughput update -g "$RG" -a "$ACCOUNT" -d "$DB" -n "$CONTAINER" \
  --max-throughput 4000
```

1. Prefer **container-level** throughput for isolation; database-level for many light containers sharing a pool.
2. Autoscale does not fix hot partitions — redesign partition key / synthetic salt if one key dominates.
3. SDK: enable retries for 429; set sensible `MaxRetryAttemptsOnRateLimitedRequests`.
4. Avoid unbounded cross-partition queries that burn RU at every scale level.
5. Indexing policy: remove unnecessary paths to reduce write RU.

### 5. Verify with evidence

```bash
az cosmosdb sql container throughput show -g "$RG" -a "$ACCOUNT" -d "$DB" -n "$CONTAINER" -o jsonc
# Monitor after deploy: Normalized RU Consumption should peak near 100% only at true peaks
# Application: 429 rate and p99 latency dashboards
```

1. Load test in nonprod with realistic partition key cardinality.
2. Confirm cost estimate vs previous manual RU.
3. Multi-region: validate failover still meets RU needs.

### 6. Observe and harden

1. Alerts: high 429 rate, Normalized RU Consumption sustained > 90%, autoscale max hit frequently.
2. If always at max → raise max or optimize queries/partitions; if always near minimum → consider lower max or serverless.
3. Security: RBAC data plane, disable key-based auth when ready, private endpoint.

### 7. Hand off

1. Document max RU, share scope (db vs container), partition key rationale.
2. Cost owner + monthly review of throughput metrics.
3. Runbook for emergency max RU increase (who can approve).

## Manual vs Autoscale vs Serverless

| Mode | Best for | Watch |
| --- | --- | --- |
| Manual | Steady utilization | Waste at idle; 429 at spikes |
| Autoscale | Spiky / diurnal | Max RU cost ceiling; hot partitions |
| Serverless | Dev/test low traffic | Not for sustained high RU |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Sizing | Max from measured peaks | Guess 100k RU “to be safe” blindly |
| Partitions | High cardinality key | `tenantId` with one huge tenant only |
| Queries | Point reads / bounded queries | SELECT * cross-partition frequently |
| Retries | SDK 429 backoff | Fail immediately on first 429 |
| Security | MI + RBAC | Primary key in mobile client |

## Output Checklist

- [ ] Account/db/container throughput mode inventoried
- [ ] Metrics baseline (RU, 429, normalized consumption) captured
- [ ] Autoscale max RU chosen with budget owner
- [ ] Partition key / hot partition reviewed
- [ ] Throughput applied; config verified via CLI
- [ ] App retries and query patterns checked
- [ ] Alerts for throttle and max saturation
- [ ] Cost review scheduled
- [ ] `code-quality-standards` applied to data access code

## Rules

- Authorized accounts only; careful with prod load tests.
- Autoscale is not a substitute for partition and query design.
- Track multi-region multiplier on cost.
- Prefer least privilege data plane auth.
- Evidence-based RU changes over folklore.

---
name: managing-oracle-oci-database
description: |
  Use when working with Oracle Oci Database — oracle OCI Database deep-dive
  management via the OCI CLI. Covers DB Systems, Autonomous Databases, backups,
  Data Guard, patching, and performance metrics. Use for detailed OCI database
  analysis.
connection_type: oracle-oci-database
preload: false
---

# Managing Oracle OCI Database (Deep Dive)

Deep-dive Oracle OCI Database management using the `oci db` CLI commands.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

COMPARTMENT_ID="${OCI_COMPARTMENT_ID:?Set OCI_COMPARTMENT_ID}"

echo "=== DB Systems ==="
oci db system list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",shape:shape,state:"lifecycle-state",edition:"database-edition",version:version,nodes:"node-count",storage:"data-storage-size-in-gbs"}' \
    --output table 2>/dev/null | head -20

echo ""
echo "=== Autonomous Databases ==="
oci db autonomous-database list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",cpus:"cpu-core-count",storage_tb:"data-storage-size-in-tbs",state:"lifecycle-state",workload:"db-workload",version:"db-version",free_tier:"is-free-tier"}' \
    --output table 2>/dev/null | head -20

echo ""
echo "=== Exadata Infrastructure ==="
oci db exadata-infrastructure list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",shape:shape,state:"lifecycle-state",compute:"compute-count",storage:"storage-count"}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== DB Homes ==="
oci db db-home list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",version:"db-version",state:"lifecycle-state"}' \
    --output table 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

COMPARTMENT_ID="${OCI_COMPARTMENT_ID:?Set OCI_COMPARTMENT_ID}"

echo "=== Autonomous Database Details ==="
ADB_ID="${1:?Autonomous Database OCID required}"
oci db autonomous-database get --autonomous-database-id "$ADB_ID" \
    --query 'data.{name:"display-name",state:"lifecycle-state",cpus:"cpu-core-count",storage_tb:"data-storage-size-in-tbs",workload:"db-workload",version:"db-version",auto_scaling:"is-auto-scaling-enabled",mtls:"is-mtls-connection-required",free_tier:"is-free-tier",created:"time-created",backup_retention:"backup-retention-period-in-days",data_guard:"is-data-guard-enabled"}' \
    --output table 2>/dev/null

echo ""
echo "=== Backups ==="
oci db autonomous-database-backup list --compartment-id "$COMPARTMENT_ID" --autonomous-database-id "$ADB_ID" \
    --query 'data[*].{id:id,name:"display-name",type:type,state:"lifecycle-state",size_tb:"database-size-in-tbs",created:"time-started"}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Connection Strings ==="
oci db autonomous-database get --autonomous-database-id "$ADB_ID" \
    --query 'data."connection-strings".profiles[*].{consumer_group:"consumer-group",protocol:protocol,tls:"tls-authentication",value:value}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Performance Metrics ==="
oci monitoring metric-data summarize-metrics-data --compartment-id "$COMPARTMENT_ID" \
    --namespace oci_autonomous_database \
    --query-text "CpuUtilization[1h]{resourceId = \"$ADB_ID\"}.mean()" \
    --query 'data[0]."aggregated-datapoints"[-5:]' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Storage Utilization ==="
oci monitoring metric-data summarize-metrics-data --compartment-id "$COMPARTMENT_ID" \
    --namespace oci_autonomous_database \
    --query-text "StorageUtilization[1h]{resourceId = \"$ADB_ID\"}.mean()" \
    --query 'data[0]."aggregated-datapoints"[-3:]' \
    --output table 2>/dev/null | head -5

echo ""
echo "=== Data Guard Status ==="
oci db autonomous-database get --autonomous-database-id "$ADB_ID" \
    --query 'data.{"data_guard_enabled":"is-data-guard-enabled","standby_db":"standby-db","role":role,"peer_db_ids":"peer-db-ids"}' \
    --output table 2>/dev/null

echo ""
echo "=== Applicable Patches ==="
oci db autonomous-database list --compartment-id "$COMPARTMENT_ID" --autonomous-database-id "$ADB_ID" \
    --query 'data[*].{version:"db-version",state:"lifecycle-state"}' \
    --output table 2>/dev/null | head -5
```

## Output Format

```
ADB_OCID                              NAME        STATE     CPUS  STORAGE  WORKLOAD
ocid1.autonomousdatabase.oc1.abc123   prod-atp    AVAILABLE 4     2TB      OLTP
ocid1.autonomousdatabase.oc1.def456   analytics   AVAILABLE 2     1TB      DW
```

## Safety Rules
- Use read-only commands: `list`, `get`, `summarize-metrics-data`
- Never run `terminate`, `stop`, `update`, `delete` without explicit user confirmation
- Always pass `--compartment-id` for resource listing
- Use `--query` and `--output table` for clean output
- Limit output with `| head -N` to stay under 50 lines

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |


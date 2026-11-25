---
name: managing-apache-kudu
description: |
  Use when working with Apache Kudu — apache Kudu cluster management, tablet
  server health monitoring, table partition analysis, and replication
  diagnostics. Covers master health, tablet distribution, column encoding
  efficiency, compaction metrics, and maintenance window scheduling. Read this
  skill before any Kudu operations.
connection_type: kudu
preload: false
---

# Apache Kudu Management Skill

Monitor, analyze, and optimize Apache Kudu clusters safely.

## MANDATORY: Discovery-First Pattern

**Always check cluster health and list tables before any data operations. Never assume table names or partition schemas.**

### Phase 1: Discovery

```bash
#!/bin/bash

KUDU_MASTER="${KUDU_MASTER:-localhost:7051}"

echo "=== Cluster Health ==="
kudu cluster ksck "$KUDU_MASTER" --sections=MASTER_SUMMARIES,TSERVER_SUMMARIES 2>&1 | head -30

echo ""
echo "=== Master Info ==="
curl -s "http://${KUDU_MASTER%:*}:8051/api/v1/masters" 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in data.get('masters', []):
    reg = m.get('registration', {})
    print(f\"Master: {reg.get('rpc_addresses',[{}])[0].get('host','?')} | Role: {m.get('role','?')}\")
" 2>/dev/null || echo "Master web UI not available"

echo ""
echo "=== Tablet Servers ==="
kudu tserver list "$KUDU_MASTER" --columns=uuid,rpc-addresses,state 2>&1

echo ""
echo "=== Tables ==="
kudu table list "$KUDU_MASTER" 2>&1

echo ""
echo "=== Table Statistics ==="
for table in $(kudu table list "$KUDU_MASTER" 2>/dev/null); do
    stats=$(kudu table statistics "$KUDU_MASTER" "$table" 2>/dev/null)
    echo "  $table: $stats"
done | head -15
```

**Phase 1 outputs:** Master health, tablet server list, table inventory with statistics.

### Phase 2: Analysis

```bash
#!/bin/bash

KUDU_MASTER="${KUDU_MASTER:-localhost:7051}"
TABLE="${1:-my_table}"

echo "=== Table Schema ==="
kudu table describe "$KUDU_MASTER" "$TABLE" 2>&1

echo ""
echo "=== Partition Info ==="
kudu table list "$KUDU_MASTER" --columns=name,num_tablets,num_replicas 2>&1

echo ""
echo "=== Tablet Distribution ==="
kudu cluster ksck "$KUDU_MASTER" --sections=TABLET_SUMMARIES --tables="$TABLE" 2>&1 | head -20

echo ""
echo "=== Cluster Rebalance Check ==="
kudu cluster rebalance "$KUDU_MASTER" --report_only 2>&1 | head -15

echo ""
echo "=== Health Summary ==="
kudu cluster ksck "$KUDU_MASTER" --sections=CHECKSUM_RESULTS,TOTAL_COUNT 2>&1 | tail -10
```

## Output Format

```
KUDU ANALYSIS
=============
Masters: [count] | TServers: [count] | Status: [healthy/unhealthy]
Tables: [count] | Total Tablets: [count]

ISSUES FOUND:
- [issue with affected table/tablet]

RECOMMENDATIONS:
- [actionable recommendation]
```

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


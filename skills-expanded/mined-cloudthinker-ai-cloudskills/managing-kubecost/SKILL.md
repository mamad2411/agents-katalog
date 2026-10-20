---
name: managing-kubecost
description: |
  Use when working with Kubecost — kubecost Kubernetes cost monitoring and
  optimization. Covers namespace cost allocation, workload cost breakdown,
  efficiency scoring, savings recommendations, cluster cost trends, and budget
  alerting. Use when analyzing Kubernetes spend, identifying waste, or
  right-sizing workloads.
connection_type: kubecost
preload: false
---

# Kubecost Management Skill

Manage and monitor Kubernetes cost allocation and optimization with Kubecost.

## MANDATORY: Discovery-First Pattern

**Always check Kubecost availability and cluster coverage before querying costs.**

### Phase 1: Discovery

```bash
#!/bin/bash

kubecost_api() {
    local endpoint="$1"
    curl -s "http://${KUBECOST_HOST:-localhost:9090}/model/${endpoint}"
}

echo "=== Kubecost Status ==="
kubecost_api "status" | jq '{
    version: .version,
    clusterCount: .clusterCount,
    dataStatus: .dataStatus
}' 2>/dev/null || echo "Checking Kubecost pod..."
kubectl get pods -A -l app=cost-analyzer 2>/dev/null | head -5

echo ""
echo "=== Monitored Clusters ==="
kubecost_api "clusterInfo" | jq -r '.[] | "\(.id)\t\(.name)\t\(.provider)"' | column -t

echo ""
echo "=== Namespace Cost Summary (last 24h) ==="
kubecost_api "allocation?window=1d&aggregate=namespace" | jq -r '
    .data[0] | to_entries[] |
    "\(.key)\t$\(.value.totalCost | . * 100 | round / 100)\tCPU: $\(.value.cpuCost | . * 100 | round / 100)\tRAM: $\(.value.ramCost | . * 100 | round / 100)"
' | sort -t'$' -k2 -rn | column -t | head -20
```

## Core Helper Functions

```bash
#!/bin/bash

kubecost_api() {
    local endpoint="$1"
    curl -s "http://${KUBECOST_HOST:-localhost:9090}/model/${endpoint}"
}

kubecost_allocation() {
    local window="${1:-1d}"
    local aggregate="${2:-namespace}"
    kubecost_api "allocation?window=${window}&aggregate=${aggregate}"
}

kubecost_savings() {
    kubecost_api "savings"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq filtering on API responses to extract key cost fields
- Round cost values to 2 decimal places for readability

## Common Operations

### Namespace Cost Breakdown

```bash
#!/bin/bash
WINDOW="${1:-7d}"

echo "=== Namespace Costs (window: $WINDOW) ==="
kubecost_api "allocation?window=${WINDOW}&aggregate=namespace" | jq -r '
    .data[0] | to_entries[] |
    "\(.key)\t$\(.value.totalCost | . * 100 | round / 100)\tCPU: \(.value.cpuCoreRequestAverage | . * 100 | round / 100) cores\tRAM: \(.value.ramByteRequestAverage / 1073741824 | . * 100 | round / 100) GiB"
' | sort -t'$' -k2 -rn | column -t | head -20

echo ""
echo "=== Total Cluster Cost ==="
kubecost_api "allocation?window=${WINDOW}&aggregate=cluster" | jq -r '
    .data[0] | to_entries[] |
    "\(.key)\tTotal: $\(.value.totalCost | . * 100 | round / 100)"
' | column -t
```

### Workload Efficiency Scoring

```bash
#!/bin/bash
NAMESPACE="${1:-}"
WINDOW="${2:-2d}"

FILTER=""
[ -n "$NAMESPACE" ] && FILTER="&filterNamespaces=${NAMESPACE}"

echo "=== Workload Efficiency (window: $WINDOW) ==="
kubecost_api "allocation?window=${WINDOW}&aggregate=controller${FILTER}" | jq -r '
    .data[0] | to_entries[] |
    select(.value.totalCost > 0.01) |
    "\(.key)\tCost: $\(.value.totalCost | . * 100 | round / 100)\tCPU Eff: \((.value.cpuEfficiency // 0) * 100 | round)%\tRAM Eff: \((.value.ramEfficiency // 0) * 100 | round)%\tTotal Eff: \((.value.totalEfficiency // 0) * 100 | round)%"
' | sort -t'$' -k2 -rn | column -t | head -20
```

### Savings Recommendations

```bash
#!/bin/bash
echo "=== Right-Sizing Recommendations ==="
kubecost_api "savings/requestSizing?window=48h&targetCPUUtilization=0.65&targetRAMUtilization=0.70" | jq -r '
    .[] | select(.annualSavings > 10) |
    "\(.namespace)/\(.controllerName)\tSavings: $\(.annualSavings | round)/yr\tCPU: \(.currentCPURequest)→\(.recommendedCPURequest)\tRAM: \(.currentRAMRequest)→\(.recommendedRAMRequest)"
' | sort -t'$' -k2 -rn | head -15

echo ""
echo "=== Abandoned Workloads ==="
kubecost_api "savings/abandonedWorkloads?window=7d" | jq -r '
    .[] | "\(.namespace)/\(.name)\tLast Active: \(.lastSeen[0:16])\tCost: $\(.monthlyCost | . * 100 | round / 100)/mo"
' | head -10
```

### Cost Trend Analysis

```bash
#!/bin/bash
echo "=== Daily Cost Trend (last 7 days) ==="
kubecost_api "allocation?window=7d&aggregate=cluster&step=1d" | jq -r '
    .data[] | to_entries[] |
    "\(.value.start[0:10])\t$\(.value.totalCost | . * 100 | round / 100)"
' | column -t

echo ""
echo "=== Cost by Label (team) ==="
kubecost_api "allocation?window=7d&aggregate=label:team" | jq -r '
    .data[0] | to_entries[] |
    select(.key != "__unallocated__") |
    "\(.key)\t$\(.value.totalCost | . * 100 | round / 100)"
' | sort -t'$' -k2 -rn | column -t | head -15
```

### Asset Cost Analysis

```bash
#!/bin/bash
echo "=== Asset Costs by Type (last 7d) ==="
kubecost_api "assets?window=7d&aggregate=type" | jq -r '
    .data[0] | to_entries[] |
    "\(.key)\t$\(.value.totalCost | . * 100 | round / 100)"
' | sort -t'$' -k2 -rn | column -t

echo ""
echo "=== Node Costs ==="
kubecost_api "assets?window=7d&aggregate=node" | jq -r '
    .data[0] | to_entries[] |
    "\(.key)\t$\(.value.totalCost | . * 100 | round / 100)\tType: \(.value.properties.instanceType // "unknown")"
' | sort -t'$' -k2 -rn | column -t | head -15
```

## Safety Rules
- **Read-only by default**: Kubecost is primarily observational -- no destructive operations
- **Window validation**: Ensure window parameter matches data retention period
- **Cost accuracy**: Kubecost estimates may differ from cloud billing -- use for relative comparison
- **Efficiency thresholds**: Do not auto-resize based solely on efficiency scores -- validate with team

## Output Format

Present results as a structured report:
```
Managing Kubecost Report
════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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

## Common Pitfalls
- **Data lag**: Kubecost needs 24-48h of data before efficiency scores stabilize
- **Shared costs**: Cluster overhead (system pods, control plane) may not be allocated to namespaces
- **Idle costs**: Unallocated resources appear as "__idle__" -- this is not waste, it is capacity headroom
- **Network costs**: Network egress costs are often estimated, not precise
- **Multi-cluster**: Ensure the correct cluster context when querying multi-cluster Kubecost
- **Prometheus dependency**: Kubecost relies on Prometheus/Thanos -- if metrics are missing, costs will be incomplete

---
name: managing-cast-ai
description: |
  Use when working with Cast Ai — cAST AI Kubernetes cluster optimization and
  cost management. Covers cluster cost optimization, spot instance management,
  cost reports, node rebalancing, security posture, and workload right-sizing.
  Use when optimizing Kubernetes cluster costs, managing node lifecycle, or
  analyzing cloud spend with CAST AI.
connection_type: cast-ai
preload: false
---

# CAST AI Management Skill

Manage Kubernetes cluster optimization and cost reduction with CAST AI.

## MANDATORY: Discovery-First Pattern

**Always list connected clusters and their optimization status before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

castai_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "X-API-Key: $CASTAI_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.cast.ai/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "X-API-Key: $CASTAI_API_KEY" \
            "https://api.cast.ai/v1/${endpoint}"
    fi
}

echo "=== Connected Clusters ==="
castai_api GET "kubernetes/external-clusters" | jq -r '
    .items[] | "\(.id)\t\(.name)\t\(.providerType)\t\(.agentStatus)\t\(.status)"
' | column -t

echo ""
echo "=== Optimization Status ==="
castai_api GET "kubernetes/external-clusters" | jq -r '
    .items[] | "\(.name)\tAutoscaler: \(.autoscalerStatus // "unknown")\tSpot: \(.spotEnabled // false)\tPolicies: \(.optimizationEnabled // false)"
' | column -t
```

## Core Helper Functions

```bash
#!/bin/bash

castai_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "X-API-Key: $CASTAI_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.cast.ai/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "X-API-Key: $CASTAI_API_KEY" \
            "https://api.cast.ai/v1/${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Filter API responses with jq to extract cost and optimization fields
- Round costs and percentages to 2 decimal places

## Common Operations

### Cluster Cost Report

```bash
#!/bin/bash
CLUSTER_ID="${1:?Cluster ID required}"

echo "=== Cluster Cost Summary (last 30d) ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/cost-report?startDate=$(date -u -d '30 days ago' +%Y-%m-%d)&endDate=$(date -u +%Y-%m-%d)" | jq '{
    totalCost: .totalCost,
    computeCost: .computeCost,
    spotSavings: .spotSavings,
    optimizationSavings: .optimizationSavings,
    savingsPercentage: .savingsPercentage
}'

echo ""
echo "=== Cost by Node Type ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/nodes" | jq -r '
    .items[] |
    "\(.name)\t\(.instanceType)\t\(.lifecycle)\t$\(.costPerHour | . * 100 | round / 100)/hr"
' | column -t | head -15
```

### Spot Instance Management

```bash
#!/bin/bash
CLUSTER_ID="${1:?Cluster ID required}"

echo "=== Node Lifecycle Distribution ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/nodes" | jq '
    .items | group_by(.lifecycle) | map({
        lifecycle: .[0].lifecycle,
        count: length,
        totalCostPerHour: (map(.costPerHour) | add | . * 100 | round / 100)
    })
'

echo ""
echo "=== Spot Interruption Risk ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/nodes" | jq -r '
    .items[] | select(.lifecycle == "spot") |
    "\(.name)\t\(.instanceType)\t\(.availabilityZone)\tAge: \(.age)"
' | column -t | head -15
```

### Rebalancing Status

```bash
#!/bin/bash
CLUSTER_ID="${1:?Cluster ID required}"

echo "=== Rebalancing Plan ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/rebalancing-plan" | jq '{
    status: .status,
    nodesToAdd: (.nodesToAdd | length),
    nodesToRemove: (.nodesToRemove | length),
    estimatedSavings: .estimatedSavingsPercentage
}'

echo ""
echo "=== Nodes to Remove (underutilized) ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/rebalancing-plan" | jq -r '
    .nodesToRemove[]? |
    "\(.name)\t\(.instanceType)\tCPU: \(.cpuUtilization | . * 100 | round)%\tRAM: \(.memUtilization | . * 100 | round)%\tCost: $\(.costPerHour)/hr"
' | column -t | head -10

echo ""
echo "=== Recommended Replacements ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/rebalancing-plan" | jq -r '
    .nodesToAdd[]? |
    "\(.instanceType)\t\(.lifecycle)\t\(.availabilityZone)\tCost: $\(.costPerHour)/hr"
' | column -t | head -10
```

### Workload Right-Sizing

```bash
#!/bin/bash
CLUSTER_ID="${1:?Cluster ID required}"

echo "=== Right-Sizing Recommendations ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/workload-optimization" | jq -r '
    .items[] | select(.savingsAmount > 1) |
    "\(.namespace)/\(.workloadName)\tCPU: \(.currentCpu)→\(.recommendedCpu)\tMem: \(.currentMemory)→\(.recommendedMemory)\tSavings: $\(.savingsAmount | . * 100 | round / 100)/mo"
' | sort -t'$' -k4 -rn | column -t | head -20
```

### Optimization Policies

```bash
#!/bin/bash
CLUSTER_ID="${1:?Cluster ID required}"

echo "=== Autoscaler Policies ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/policies" | jq '{
    enabled: .enabled,
    spotEnabled: .spotInstances.enabled,
    spotPercentage: .spotInstances.maxPercent,
    unschedulablePods: .unschedulablePods.enabled,
    nodeDownscaling: .nodeDownscaling.enabled,
    cpuHeadroom: .clusterLimits.cpu.maxCores,
    memoryHeadroom: .clusterLimits.memory.maxGiB
}'

echo ""
echo "=== Scaling Events (last 24h) ==="
castai_api GET "kubernetes/clusters/${CLUSTER_ID}/audit-log?fromDate=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)" | jq -r '
    .items[] | select(.action | contains("node")) |
    "\(.createdAt[0:16])\t\(.action)\t\(.details[0:60])"
' | head -15
```

## Safety Rules
- **Review before enabling**: Always review policies before enabling autoscaler or spot
- **Gradual rollout**: Enable optimization features one at a time (spot, downscaling, right-sizing)
- **Node drain timeout**: Ensure proper PDB and drain settings before enabling node removal
- **Critical workloads**: Mark critical workloads with anti-spot labels to keep them on on-demand nodes

## Output Format

Present results as a structured report:
```
Managing Cast Ai Report
═══════════════════════
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
- **Agent connectivity**: CAST AI requires an in-cluster agent -- check agent pod health first
- **Cloud permissions**: Insufficient IAM permissions will silently prevent node provisioning
- **PDB conflicts**: Pod Disruption Budgets can block node draining during rebalancing
- **Spot fallback**: Without on-demand fallback, spot evictions can cause downtime
- **Cost reporting delay**: Cost data may lag by 1-2 hours behind actual usage
- **Multi-AZ**: Ensure instance type availability across all configured AZs

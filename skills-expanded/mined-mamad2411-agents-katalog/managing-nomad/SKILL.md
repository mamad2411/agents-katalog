---
name: managing-nomad
description: |
  Use when working with Nomad — hashiCorp Nomad workload orchestrator
  management. Covers job submission, allocation status, deployment health,
  client/server status, namespace management, and resource utilization. Use when
  managing Nomad jobs, debugging allocation failures, monitoring deployments, or
  inspecting cluster health.
connection_type: nomad
preload: false
---

# Nomad Management Skill

Manage HashiCorp Nomad jobs, allocations, deployments, and cluster health.

## Core Helper Functions

```bash
#!/bin/bash

# Nomad CLI wrapper
nomad_cmd() {
    nomad "$@" 2>/dev/null
}

# Nomad HTTP API helper
nomad_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    local url="${NOMAD_ADDR:-http://127.0.0.1:4646}"

    local auth_header=""
    if [ -n "${NOMAD_TOKEN:-}" ]; then
        auth_header="-H \"X-Nomad-Token: $NOMAD_TOKEN\""
    fi

    if [ -n "$data" ]; then
        eval curl -s -X "$method" $auth_header -H "Content-Type: application/json" "${url}/v1/${endpoint}" -d "'$data'"
    else
        eval curl -s -X "$method" $auth_header "${url}/v1/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover cluster status, nodes, and jobs before performing specific operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Nomad Agent Info ==="
nomad_api GET "agent/self" | jq '{
    name: .member.Name,
    region: .config.Region,
    datacenter: .config.Datacenter,
    version: .config.Version,
    server: .config.Server
}'

echo ""
echo "=== Server Members ==="
nomad_api GET "agent/members" | jq -r '.Members[] | "\(.Name)\t\(.Addr):\(.Port)\t\(.Status)\t\(.Tags.region)\t\(.Tags.dc)"' | column -t

echo ""
echo "=== Client Nodes ==="
nomad_api GET "nodes" | jq -r '.[] | "\(.ID[0:8])\t\(.Name)\t\(.Status)\t\(.Drain)\t\(.NodeClass // "default")\t\(.Datacenter)"' | column -t | head -20

echo ""
echo "=== Job Summary ==="
nomad_api GET "jobs" | jq -r '.[] | "\(.ID)\t\(.Type)\t\(.Status)\t\(.Namespace // "default")\t\(.Priority)"' | column -t | head -30
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use Nomad HTTP API with jq for structured output
- Always use short allocation IDs (first 8 chars) for readability

## Common Operations

### Job Management Dashboard

```bash
#!/bin/bash
echo "=== Job Status Summary ==="
nomad_api GET "jobs" | jq '{
    total: length,
    running: [.[] | select(.Status == "running")] | length,
    dead: [.[] | select(.Status == "dead")] | length,
    pending: [.[] | select(.Status == "pending")] | length,
    by_type: (group_by(.Type) | map({type: .[0].Type, count: length}))
}'

echo ""
echo "=== Failed Jobs ==="
nomad_api GET "jobs" | jq -r '
    .[] | select(.Status == "dead") | "\(.ID)\t\(.Type)\t\(.StatusDescription[0:60])"
' | column -t | head -10

echo ""
echo "=== Recent Deployments ==="
nomad_api GET "deployments" | jq -r '
    sort_by(.CreateIndex) | reverse | .[:10][] |
    "\(.ID[0:8])\t\(.JobID)\t\(.Status)\t\(.StatusDescription[0:40])"
' | column -t
```

### Allocation Debugging

```bash
#!/bin/bash
JOB="${1:?Job ID required}"

echo "=== Job Detail: $JOB ==="
nomad_api GET "job/$JOB" | jq '{
    id: .ID,
    type: .Type,
    status: .Status,
    namespace: .Namespace,
    datacenters: .Datacenters,
    task_groups: [.TaskGroups[] | {name: .Name, count: .Count, tasks: [.Tasks[].Name]}]
}'

echo ""
echo "=== Allocations ==="
nomad_api GET "job/$JOB/allocations" | jq -r '
    sort_by(.CreateIndex) | reverse | .[:15][] |
    "\(.ID[0:8])\t\(.TaskGroup)\t\(.ClientStatus)\t\(.NodeID[0:8])\t\(.DesiredStatus)"
' | column -t

echo ""
echo "=== Failed Allocation Details ==="
for alloc_id in $(nomad_api GET "job/$JOB/allocations" | jq -r '.[] | select(.ClientStatus == "failed") | .ID' | head -3); do
    echo "--- Alloc: ${alloc_id:0:8} ---"
    nomad_api GET "allocation/$alloc_id" | jq '{
        task_states: (.TaskStates | to_entries[] | {task: .key, state: .value.State, failed: .value.Failed, events: [.value.Events[-3:][] | {type: .Type, message: .DisplayMessage}]})
    }'
done
```

### Deployment Health

```bash
#!/bin/bash
JOB="${1:?Job ID required}"

echo "=== Latest Deployment: $JOB ==="
nomad_api GET "job/$JOB/deployment" | jq '{
    id: .ID[0:8],
    status: .Status,
    description: .StatusDescription,
    task_groups: (.TaskGroups | to_entries[] | {
        group: .key,
        desired: .value.DesiredTotal,
        placed: .value.PlacedAllocs,
        healthy: .value.HealthyAllocs,
        unhealthy: .value.UnhealthyAllocs,
        auto_revert: .value.AutoRevert
    })
}'

echo ""
echo "=== Deployment History ==="
nomad_api GET "job/$JOB/deployments" | jq -r '
    sort_by(.CreateIndex) | reverse | .[:5][] |
    "\(.ID[0:8])\t\(.Status)\t\(.StatusDescription[0:50])"
' | column -t
```

### Client Node Status

```bash
#!/bin/bash
echo "=== Node Resource Summary ==="
for node_id in $(nomad_api GET "nodes" | jq -r '.[].ID' | head -10); do
    nomad_api GET "node/$node_id" | jq '{
        name: .Name,
        status: .Status,
        drain: .Drain,
        eligible: .SchedulingEligibility,
        datacenter: .Datacenter,
        cpu_total: .Attributes["cpu.totalcompute"],
        memory_mb: (.Resources.MemoryMB // 0),
        allocs_running: (.Attributes["nomad.allocs.running"] // "N/A")
    }'
done

echo ""
echo "=== Draining Nodes ==="
nomad_api GET "nodes" | jq -r '.[] | select(.Drain == true) | "\(.Name)\t\(.ID[0:8])\t\(.StatusDescription)"' | column -t
```

### Namespace & ACL Overview

```bash
#!/bin/bash
echo "=== Namespaces ==="
nomad_api GET "namespaces" | jq -r '.[] | "\(.Name)\t\(.Description[0:50])"' | column -t

echo ""
echo "=== Jobs by Namespace ==="
for ns in $(nomad_api GET "namespaces" | jq -r '.[].Name'); do
    COUNT=$(nomad_api GET "jobs?namespace=$ns" | jq 'length')
    echo "$ns: $COUNT jobs"
done

echo ""
echo "=== Resource Quotas ==="
nomad_api GET "quotas" | jq -r '.[]? | "\(.Name)\t\(.Description[0:40])"' | column -t 2>/dev/null || echo "No quotas configured"
```

## Safety Rules
- **Read-only by default**: Use GET requests for job, allocation, node inspection
- **Never stop or purge** jobs without explicit user confirmation
- **Drain caution**: Node drain migrates all allocations -- confirm before draining
- **Never expose** Nomad ACL tokens or Vault tokens in output

## Output Format

Present results as a structured report:
```
Managing Nomad Report
═════════════════════
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
- **Allocation pending**: Usually means insufficient resources -- check node capacity
- **Failed deployments**: Auto-revert may roll back silently -- check deployment history
- **Stale reads**: Nomad uses Raft consensus -- stale queries may return old data
- **Namespace scoping**: Jobs are namespace-scoped -- always specify namespace for multi-tenant clusters
- **Task driver missing**: Allocation fails if the required driver (docker, exec, java) is not installed on the client

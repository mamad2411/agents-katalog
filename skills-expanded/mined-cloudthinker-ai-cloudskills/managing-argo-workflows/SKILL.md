---
name: managing-argo-workflows
description: |
  Use when working with Argo Workflows — argo Workflows management for
  Kubernetes-native workflow orchestration. Covers workflow templates, cron
  workflow scheduling, artifact management, workflow execution, parameter
  handling, and resource monitoring. Use when checking workflow status,
  investigating step failures, managing templates, or auditing cron workflows.
connection_type: argo-workflows
preload: false
---

# Argo Workflows Management Skill

Manage and monitor Argo Workflows, templates, and cron schedules on Kubernetes.

## Core Helper Functions

```bash
#!/bin/bash

# Argo Workflows API helper
argo_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    local ns="${ARGO_NAMESPACE:-argo}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${ARGO_TOKEN}" \
            -H "Content-Type: application/json" \
            "${ARGO_SERVER}/api/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${ARGO_TOKEN}" \
            "${ARGO_SERVER}/api/v1/${endpoint}"
    fi
}

# Argo CLI wrapper
argo_cmd() {
    argo "$@" --namespace "${ARGO_NAMESPACE:-argo}" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always list workflows and templates before querying specific runs.**

### Phase 1: Discovery

```bash
#!/bin/bash
NS="${ARGO_NAMESPACE:-argo}"

echo "=== Argo Server Info ==="
argo_api GET "info" | jq '{managedNamespace, links}' 2>/dev/null || echo "Server info not available"

echo ""
echo "=== Recent Workflows ==="
argo_cmd list --status "" --output wide | head -20 || \
    argo_api GET "workflows/${NS}?listOptions.limit=15" | jq -r '
    .items[]? |
    "\(.metadata.name)\t\(.status.phase)\t\(.status.startedAt[0:16])\t\(.status.finishedAt[0:16] // "running")\t\(.status.progress // "n/a")"
' | column -t

echo ""
echo "=== Workflow Templates ==="
argo_api GET "workflow-templates/${NS}" | jq -r '
    .items[]? | "\(.metadata.name)\t\(.metadata.creationTimestamp[0:16])"
' | column -t

echo ""
echo "=== Cron Workflows ==="
argo_api GET "cron-workflows/${NS}" | jq -r '
    .items[]? |
    "\(.metadata.name)\t\(.spec.schedule)\tsuspend=\(.spec.suspend // false)\tlastRun=\(.status.lastScheduledTime[0:16] // "never")"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `--output json | jq` for structured filtering
- Never dump full workflow specs — extract key node information

## Common Operations

### Workflow Status Dashboard

```bash
#!/bin/bash
NS="${ARGO_NAMESPACE:-argo}"

echo "=== Workflow Summary ==="
argo_api GET "workflows/${NS}?listOptions.limit=50" | jq '{
    total: (.items | length),
    succeeded: [.items[]? | select(.status.phase == "Succeeded")] | length,
    failed: [.items[]? | select(.status.phase == "Failed")] | length,
    running: [.items[]? | select(.status.phase == "Running")] | length,
    error: [.items[]? | select(.status.phase == "Error")] | length,
    pending: [.items[]? | select(.status.phase == "Pending")] | length
}'

echo ""
echo "=== Failed Workflows ==="
argo_api GET "workflows/${NS}?listOptions.limit=20&listOptions.fieldSelector=status.phase=Failed" | jq -r '
    .items[]? |
    "\(.metadata.name)\t\(.status.startedAt[0:16])\t\(.status.message[0:60] // "no message")"
' | column -t

echo ""
echo "=== Running Workflows ==="
argo_api GET "workflows/${NS}?listOptions.fieldSelector=status.phase=Running" | jq -r '
    .items[]? |
    "\(.metadata.name)\tprogress=\(.status.progress // "unknown")\tstarted=\(.status.startedAt[0:16])"
' | column -t
```

### Workflow Execution Analysis

```bash
#!/bin/bash
WORKFLOW_NAME="${1:?Workflow name required}"
NS="${ARGO_NAMESPACE:-argo}"

echo "=== Workflow Details ==="
argo_api GET "workflows/${NS}/${WORKFLOW_NAME}" | jq '{
    name: .metadata.name,
    phase: .status.phase,
    progress: .status.progress,
    startedAt: .status.startedAt,
    finishedAt: .status.finishedAt,
    message: .status.message,
    parameters: [.spec.arguments.parameters[]? | {name, value}]
}'

echo ""
echo "=== Node Status ==="
argo_api GET "workflows/${NS}/${WORKFLOW_NAME}" | jq -r '
    .status.nodes | to_entries[] |
    "\(.value.displayName)\t\(.value.phase)\t\(.value.type)\t\(.value.startedAt[0:16] // "pending")"
' | column -t | head -25

echo ""
echo "=== Failed Nodes ==="
argo_api GET "workflows/${NS}/${WORKFLOW_NAME}" | jq -r '
    .status.nodes | to_entries[] | select(.value.phase == "Failed") |
    "Node: \(.value.displayName)\nType: \(.value.type)\nMessage: \(.value.message[0:100] // "none")\n---"
'
```

### Workflow Template Management

```bash
#!/bin/bash
NS="${ARGO_NAMESPACE:-argo}"

echo "=== Workflow Templates ==="
argo_api GET "workflow-templates/${NS}" | jq -r '
    .items[]? | "\(.metadata.name)\tentrypoint=\(.spec.entrypoint)\ttemplates=\(.spec.templates | length)\tparams=\([.spec.arguments.parameters[]? | .name] | join(","))"
' | column -t

echo ""
echo "=== Template Details ==="
TEMPLATE_NAME="${1:?Template name required}"
argo_api GET "workflow-templates/${NS}/${TEMPLATE_NAME}" | jq '{
    name: .metadata.name,
    entrypoint: .spec.entrypoint,
    arguments: [.spec.arguments.parameters[]? | {name, default: .default}],
    templates: [.spec.templates[] | {name, type: (if .dag then "dag" elif .steps then "steps" elif .container then "container" elif .script then "script" else "other" end)}],
    volumes: [.spec.volumes[]? | .name]
}'

echo ""
echo "=== Cluster Workflow Templates ==="
argo_api GET "cluster-workflow-templates" | jq -r '
    .items[]? | "\(.metadata.name)\tentrypoint=\(.spec.entrypoint)"
' | column -t
```

### Cron Workflow Management

```bash
#!/bin/bash
NS="${ARGO_NAMESPACE:-argo}"

echo "=== Cron Workflows ==="
argo_api GET "cron-workflows/${NS}" | jq -r '
    .items[]? |
    "\(.metadata.name)\tschedule=\(.spec.schedule)\tsuspend=\(.spec.suspend // false)\tconcurrency=\(.spec.concurrencyPolicy // "Allow")\tlastRun=\(.status.lastScheduledTime[0:16] // "never")"
' | column -t

echo ""
echo "=== Cron Workflow History ==="
CRON_NAME="${1:-}"
if [ -n "$CRON_NAME" ]; then
    argo_api GET "cron-workflows/${NS}/${CRON_NAME}" | jq '{
        name: .metadata.name,
        schedule: .spec.schedule,
        timezone: .spec.timezone,
        suspend: .spec.suspend,
        concurrencyPolicy: .spec.concurrencyPolicy,
        successfulJobsHistoryLimit: .spec.successfulJobsHistoryLimit,
        failedJobsHistoryLimit: .spec.failedJobsHistoryLimit,
        lastScheduledTime: .status.lastScheduledTime,
        active: [.status.active[]? | .name],
        conditions: [.status.conditions[]? | {type, status, message}]
    }'
fi
```

### Artifact Management

```bash
#!/bin/bash
WORKFLOW_NAME="${1:?Workflow name required}"
NS="${ARGO_NAMESPACE:-argo}"

echo "=== Workflow Artifacts ==="
argo_api GET "workflows/${NS}/${WORKFLOW_NAME}" | jq -r '
    .status.nodes | to_entries[] |
    select(.value.outputs.artifacts != null) |
    .value | "\(.displayName)\t\(.outputs.artifacts[] | "\(.name)\tpath=\(.path // .s3.key // "unknown")")"
' | column -t

echo ""
echo "=== Artifact Repository Config ==="
argo_api GET "workflows/${NS}/${WORKFLOW_NAME}" | jq '
    .spec.artifactRepositoryRef // .spec.artifactGC // "using default artifact repository"
'
```

## Anti-Hallucination Rules
- NEVER guess workflow names — always list workflows first
- NEVER fabricate node IDs — query workflow status for actual node names
- NEVER assume namespace — Argo Workflows can run in any namespace
- Workflow template names are distinct from workflow names — do not confuse them

## Safety Rules
- NEVER submit workflows without explicit user confirmation
- NEVER delete workflows or templates without user approval
- NEVER suspend cron workflows without confirming impact
- NEVER terminate running workflows without user consent — may leave resources orphaned

## Output Format

Present results as a structured report:
```
Managing Argo Workflows Report
══════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **Phase values**: `Pending`, `Running`, `Succeeded`, `Failed`, `Error`, `Skipped`, `Omitted`
- **DAG vs Steps**: DAG templates run tasks in parallel by dependency; Steps run sequentially — different debugging approaches
- **Resource limits**: Workflows can exhaust cluster resources — check resource requests in templates
- **Artifact GC**: Artifacts may be garbage-collected — check `artifactGC` settings
- **Exit handlers**: `onExit` templates run regardless of workflow success — useful for cleanup but may mask issues
- **Retry strategies**: Templates with `retryStrategy` may succeed after failures — check all attempts, not just final status
- **Memoization**: Cached nodes skip execution — verify cache config when debugging unexpected results

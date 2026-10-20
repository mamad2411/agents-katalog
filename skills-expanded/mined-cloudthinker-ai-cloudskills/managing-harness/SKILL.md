---
name: managing-harness
description: |
  Use when working with Harness — harness continuous delivery platform
  management. Covers deployment pipelines, service management, environment
  configuration, connector health, infrastructure definitions, and execution
  history. Use when checking deployment status, investigating pipeline failures,
  managing services, or auditing Harness configurations.
connection_type: harness
preload: false
---

# Harness Management Skill

Manage and monitor Harness deployment pipelines, services, and environments.

## Core Helper Functions

```bash
#!/bin/bash

# Harness NextGen API helper
harness_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    local base_url="${HARNESS_API_URL:-https://app.harness.io/gateway}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "x-api-key: ${HARNESS_API_KEY}" \
            -H "Content-Type: application/json" \
            -H "Harness-Account: ${HARNESS_ACCOUNT_ID}" \
            "${base_url}/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "x-api-key: ${HARNESS_API_KEY}" \
            -H "Harness-Account: ${HARNESS_ACCOUNT_ID}" \
            "${base_url}/${endpoint}"
    fi
}

# Scoped endpoint helper
harness_ng() {
    local endpoint="$1"
    local params="accountIdentifier=${HARNESS_ACCOUNT_ID}"
    [ -n "$HARNESS_ORG_ID" ] && params="${params}&orgIdentifier=${HARNESS_ORG_ID}"
    [ -n "$HARNESS_PROJECT_ID" ] && params="${params}&projectIdentifier=${HARNESS_PROJECT_ID}"
    harness_api GET "ng/api/${endpoint}?${params}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover organizations, projects, and pipelines before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Info ==="
harness_api GET "ng/api/accounts/${HARNESS_ACCOUNT_ID}" | jq '.data | {name, identifier, companyName}'

echo ""
echo "=== Organizations ==="
harness_api GET "ng/api/organizations?accountIdentifier=${HARNESS_ACCOUNT_ID}&pageSize=20" | jq -r '
    .data.content[]? | "\(.organization.identifier)\t\(.organization.name)"
' | column -t

echo ""
echo "=== Projects ==="
harness_api GET "ng/api/projects?accountIdentifier=${HARNESS_ACCOUNT_ID}&orgIdentifier=${HARNESS_ORG_ID}&pageSize=20" | jq -r '
    .data.content[]? | "\(.project.identifier)\t\(.project.name)\t\(.project.modules | join(","))"
' | column -t

echo ""
echo "=== Pipelines ==="
harness_ng "pipelines/list" | jq -r '
    .data.content[]? | "\(.identifier)\t\(.name)\t\(.stageNames | join(","))"
' | column -t | head -20
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use scoped API calls (account/org/project) to narrow results
- Never dump full pipeline YAML — extract stage summaries

## Common Operations

### Pipeline Execution Dashboard

```bash
#!/bin/bash
echo "=== Recent Executions ==="
harness_ng "pipeline/execution/summary" | jq -r '
    .data.content[]? |
    "\(.pipelineIdentifier)\t\(.status)\t\(.name[0:30])\t\(.startTs / 1000 | strftime("%Y-%m-%d %H:%M"))\ttrigger=\(.executionTriggerInfo.triggerType)"
' | column -t | head -15

echo ""
echo "=== Execution Summary ==="
harness_ng "pipeline/execution/summary" | jq '{
    total: (.data.content | length),
    success: [.data.content[]? | select(.status == "Success")] | length,
    failed: [.data.content[]? | select(.status == "Failed")] | length,
    running: [.data.content[]? | select(.status == "Running")] | length,
    aborted: [.data.content[]? | select(.status == "Aborted")] | length
}'

echo ""
echo "=== Failed Executions ==="
harness_ng "pipeline/execution/summary?status=Failed&size=10" | jq -r '
    .data.content[]? |
    "\(.pipelineIdentifier)\t\(.startTs / 1000 | strftime("%Y-%m-%d %H:%M"))\t\(.failureInfo.message[0:60] // "unknown")"
' | column -t
```

### Pipeline Execution Analysis

```bash
#!/bin/bash
EXECUTION_ID="${1:?Execution ID required}"

echo "=== Execution Details ==="
harness_ng "pipeline/execution/${EXECUTION_ID}" | jq '.data | {
    pipelineIdentifier,
    status,
    startTs: (.startTs / 1000 | strftime("%Y-%m-%d %H:%M")),
    endTs: ((.endTs // 0) / 1000 | if . > 0 then strftime("%Y-%m-%d %H:%M") else "running" end),
    triggerType: .executionTriggerInfo.triggerType,
    stages: [.layoutNodeMap | to_entries[] | {name: .value.name, status: .value.status, nodeType: .value.nodeType}]
}'

echo ""
echo "=== Failed Stages ==="
harness_ng "pipeline/execution/${EXECUTION_ID}" | jq -r '
    .data.layoutNodeMap | to_entries[] |
    select(.value.status == "Failed") |
    "Stage: \(.value.name)\nType: \(.value.nodeType)\nError: \(.value.failureInfo.message[0:100] // "unknown")\n---"
'
```

### Service Management

```bash
#!/bin/bash
echo "=== Services ==="
harness_ng "servicesV2?size=20" | jq -r '
    .data.content[]? |
    "\(.service.identifier)\t\(.service.name)\ttype=\(.service.type // "unknown")\tdeployments=\(.deploymentMetadata.deploymentCount // 0)"
' | column -t

echo ""
echo "=== Service Details ==="
SERVICE_ID="${1:-}"
if [ -n "$SERVICE_ID" ]; then
    harness_ng "servicesV2/${SERVICE_ID}" | jq '.data.service | {
        identifier, name, type,
        tags: .tags,
        gitOpsEnabled: .gitOpsEnabled
    }'
fi
```

### Environment Configuration

```bash
#!/bin/bash
echo "=== Environments ==="
harness_ng "environmentsV2?size=20" | jq -r '
    .data.content[]? |
    "\(.environment.identifier)\t\(.environment.name)\ttype=\(.environment.type)\ttags=\(.environment.tags // {} | keys | join(","))"
' | column -t

echo ""
echo "=== Infrastructure Definitions ==="
ENV_ID="${1:-}"
if [ -n "$ENV_ID" ]; then
    harness_ng "infrastructures?environmentIdentifier=${ENV_ID}&size=20" | jq -r '
        .data.content[]? |
        "\(.infrastructure.identifier)\t\(.infrastructure.name)\ttype=\(.infrastructure.type)\tdeploymentType=\(.infrastructure.deploymentType)"
    ' | column -t
fi
```

### Connector Health

```bash
#!/bin/bash
echo "=== Connectors ==="
harness_ng "connectors?pageSize=20" | jq -r '
    .data.content[]? |
    "\(.connector.identifier)\t\(.connector.name)\ttype=\(.connector.type)\tstatus=\(.status.status // "unknown")"
' | column -t

echo ""
echo "=== Unhealthy Connectors ==="
harness_ng "connectors?pageSize=50" | jq -r '
    .data.content[]? | select(.status.status != "SUCCESS") |
    "\(.connector.identifier)\t\(.connector.type)\tstatus=\(.status.status)\terror=\(.status.errorSummary[0:60] // "unknown")"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess pipeline or service identifiers — always discover via API
- NEVER fabricate execution IDs — query execution history first
- NEVER assume org/project scope — always include scope parameters
- API response structure wraps data in `.data` — always access `.data` field

## Safety Rules
- NEVER trigger pipeline executions without explicit user confirmation
- NEVER delete services or environments without user approval
- NEVER modify connectors without understanding downstream dependencies
- NEVER expose secrets or API keys stored in Harness secret manager

## Output Format

Present results as a structured report:
```
Managing Harness Report
═══════════════════════
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
- **Scope hierarchy**: Account > Organization > Project — resources are scoped and require correct identifiers
- **API versions**: NextGen (`ng/api`) vs FirstGen (`api`) — use NextGen for current platform
- **Pipeline YAML**: Harness uses custom YAML format — not standard Kubernetes YAML
- **Execution status values**: `Success`, `Failed`, `Running`, `Aborted`, `Expired`, `Paused`, `Waiting`
- **Delegate connectivity**: Many operations require a healthy Delegate — check delegate status when connectors fail
- **Feature flags**: Some API endpoints require feature flags to be enabled on the account
- **Rate limits**: API has rate limits per account — avoid tight polling loops

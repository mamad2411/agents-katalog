---
name: managing-argocd
description: |
  Use when working with Argocd — argoCD GitOps continuous delivery management
  for Kubernetes. Covers application sync status, deployment health, rollback
  operations, repository management, cluster registration, RBAC analysis, and
  application diff review. Use when checking deployment status, investigating
  sync failures, managing GitOps applications, or auditing ArgoCD
  configurations.
connection_type: argocd
preload: false
---

# ArgoCD Management Skill

Manage and monitor ArgoCD GitOps deployments for Kubernetes applications.

## MANDATORY: Discovery-First Pattern

**Always list applications and clusters before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

argocd_cmd() {
    argocd "$@" --server "$ARGOCD_SERVER" --auth-token "$ARGOCD_AUTH_TOKEN" \
           --grpc-web 2>/dev/null
}

echo "=== ArgoCD Server Info ==="
argocd_cmd version --short 2>/dev/null || \
    curl -s -H "Authorization: Bearer $ARGOCD_AUTH_TOKEN" \
         "https://$ARGOCD_SERVER/api/v1/version" | jq '.Version'

echo ""
echo "=== Registered Clusters ==="
argocd_cmd cluster list --output table 2>/dev/null || \
    curl -s -H "Authorization: Bearer $ARGOCD_AUTH_TOKEN" \
         "https://$ARGOCD_SERVER/api/v1/clusters" \
    | jq -r '.items[] | "\(.name // "in-cluster")\t\(.server)\t\(.connectionState.status)"' | column -t

echo ""
echo "=== Application Summary ==="
argocd_cmd app list --output table 2>/dev/null || \
    curl -s -H "Authorization: Bearer $ARGOCD_AUTH_TOKEN" \
         "https://$ARGOCD_SERVER/api/v1/applications" \
    | jq -r '.items[] | "\(.metadata.name)\t\(.status.sync.status)\t\(.status.health.status)\t\(.spec.destination.namespace)"' \
    | column -t | head -30
```

## Core Helper Functions

```bash
#!/bin/bash

# ArgoCD REST API helper
argocd_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $ARGOCD_AUTH_TOKEN" \
            -H "Content-Type: application/json" \
            "https://${ARGOCD_SERVER}/api/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $ARGOCD_AUTH_TOKEN" \
            "https://${ARGOCD_SERVER}/api/v1/${endpoint}"
    fi
}

# ArgoCD CLI wrapper
argocd_cmd() {
    argocd "$@" --server "$ARGOCD_SERVER" --auth-token "$ARGOCD_AUTH_TOKEN" --grpc-web 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use `--output table` or `--output json` with jq filtering for CLI
- Never dump full application manifests — extract key fields

## Common Operations

### Application Health Dashboard

```bash
#!/bin/bash
echo "=== Application Health Summary ==="
argocd_api GET "applications" | jq '
    .items |
    {
        total: length,
        healthy: [.[] | select(.status.health.status == "Healthy")] | length,
        degraded: [.[] | select(.status.health.status == "Degraded")] | length,
        progressing: [.[] | select(.status.health.status == "Progressing")] | length,
        synced: [.[] | select(.status.sync.status == "Synced")] | length,
        out_of_sync: [.[] | select(.status.sync.status == "OutOfSync")] | length
    }'

echo ""
echo "=== Degraded Applications ==="
argocd_api GET "applications" | jq -r '
    .items[] |
    select(.status.health.status == "Degraded" or .status.sync.status == "OutOfSync") |
    "\(.metadata.name)\t\(.status.health.status)\t\(.status.sync.status)\t\(.spec.destination.namespace)"
' | column -t

echo ""
echo "=== Recently Synced (last 24h) ==="
YESTERDAY=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
argocd_api GET "applications" | jq -r --arg yesterday "$YESTERDAY" '
    .items[] |
    select(.status.operationState.finishedAt // "" > $yesterday) |
    "\(.metadata.name)\t\(.status.operationState.phase)\t\(.status.operationState.finishedAt[0:16])"
' | column -t | head -20
```

### Application Sync Status

```bash
#!/bin/bash
APP_NAME="${1:?Application name required}"

echo "=== Application Status: $APP_NAME ==="
argocd_api GET "applications/${APP_NAME}" | jq '{
    name: .metadata.name,
    sync_status: .status.sync.status,
    health_status: .status.health.status,
    repo: .spec.source.repoURL,
    path: .spec.source.path,
    target_revision: .spec.source.targetRevision,
    namespace: .spec.destination.namespace,
    cluster: .spec.destination.server,
    last_sync: .status.operationState.finishedAt,
    last_sync_result: .status.operationState.phase
}'

echo ""
echo "=== Resource Health ==="
argocd_api GET "applications/${APP_NAME}" | jq -r '
    .status.resources[] |
    select(.health.status != "Healthy") |
    "\(.kind)/\(.name)\t\(.health.status)\t\(.health.message // "")"
' | column -t | head -20

echo ""
echo "=== Sync Messages ==="
argocd_api GET "applications/${APP_NAME}" \
    | jq -r '.status.conditions[]? | "\(.type)\t\(.message)"' | head -10
```

### Application Diff (OutOfSync Review)

```bash
#!/bin/bash
APP_NAME="${1:?Application name required}"

echo "=== Diff for $APP_NAME ==="
argocd_cmd app diff "$APP_NAME" 2>/dev/null || \
    argocd_api GET "applications/${APP_NAME}/resource-tree" | jq -r '
        .nodes[] |
        select(.status == "OutOfSync") |
        "\(.kind)\t\(.name)\t\(.namespace)"
    ' | column -t

echo ""
echo "=== OutOfSync Resources ==="
argocd_api GET "applications/${APP_NAME}" | jq -r '
    .status.resources[] |
    select(.status == "OutOfSync") |
    "\(.kind)/\(.name)\t\(.namespace // "cluster-scoped")"
' | column -t
```

### Sync Operations

```bash
#!/bin/bash
APP_NAME="${1:?Application name required}"
DRY_RUN="${2:-true}"  # Default to dry-run for safety

if [ "$DRY_RUN" = "true" ]; then
    echo "=== DRY RUN: Showing what would sync ==="
    argocd_api GET "applications/${APP_NAME}" | jq -r '
        .status.resources[] |
        select(.status == "OutOfSync") |
        "Would sync: \(.kind)/\(.name)"
    '
    echo ""
    echo "To actually sync, call with dry_run=false"
else
    echo "=== Syncing $APP_NAME ==="
    argocd_api POST "applications/${APP_NAME}/sync" \
        '{"dryRun": false, "prune": false, "strategy": {"hook": {}}}' \
        | jq '{phase: .status.operationState.phase, message: .status.operationState.message}'
fi
```

### Rollback

```bash
#!/bin/bash
APP_NAME="${1:?Application name required}"

echo "=== Deployment History for $APP_NAME ==="
argocd_api GET "applications/${APP_NAME}/revisions" 2>/dev/null | jq -r '
    .[] | "\(.id)\t\(.deployedAt[0:16])\t\(.source.targetRevision)\t\(.initiatedBy.username // "automated")"
' | column -t | head -10 || \
argocd_cmd app history "$APP_NAME" 2>/dev/null | head -10

echo ""
echo "To rollback to a specific ID:"
echo "argocd app rollback $APP_NAME <history-id>"
```

### Repository Management

```bash
#!/bin/bash
echo "=== Registered Repositories ==="
argocd_api GET "repositories" | jq -r '
    .items[] | "\(.repo)\t\(.type // "git")\t\(.connectionState.status)"
' | column -t

echo ""
echo "=== Repository Errors ==="
argocd_api GET "repositories" | jq -r '
    .items[] |
    select(.connectionState.status != "Successful") |
    "\(.repo)\t\(.connectionState.message)"
' | column -t
```

### RBAC & User Access

```bash
#!/bin/bash
echo "=== ArgoCD Projects ==="
argocd_api GET "projects" | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.sourceRepos | length) repos\t\(.spec.destinations | length) destinations"
' | column -t

echo ""
echo "=== Project Source Restrictions ==="
argocd_api GET "projects" | jq -r '
    .items[] |
    "\(.metadata.name): repos=\(.spec.sourceRepos | join(","))"
' | head -15
```

### ArgoCD Notifications

```bash
#!/bin/bash
echo "=== Application Events (recent) ==="
argocd_api GET "applications" | jq -r '.items[].metadata.name' | while read app; do
    argocd_api GET "applications/${app}/events" 2>/dev/null \
        | jq -r '.items[-3:][] | "\(.lastTimestamp[0:16])\t'"$app"'\t\(.reason)\t\(.message[0:60])"' 2>/dev/null
done | sort -r | head -20
```

## Output Format

Present results as a structured report:
```
Managing Argocd Report
══════════════════════
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

- **Auth token expiry**: ArgoCD tokens expire — if getting 401, token needs refresh via `argocd login`
- **gRPC vs REST**: CLI uses gRPC; API uses REST — `--grpc-web` flag needed when gRPC is blocked
- **Sync vs Health**: An app can be Synced but Degraded (e.g., deployment created but pods crashing) — always check BOTH
- **OutOfSync causes**: Can be drift, new commits to repo, or parameter overrides — check source before syncing
- **Prune flag**: `prune: false` in sync prevents deleting resources not in Git — use cautiously
- **App of Apps**: Some setups use root apps that manage child apps — list all apps before investigating single app
- **Self-managed ArgoCD**: ArgoCD can manage itself — be careful with syncing the argocd namespace app
- **Resource tracking**: ArgoCD uses annotations (`app.kubernetes.io/instance`) to track resources — unlabeled resources won't show
- **Webhook vs polling**: If sync is delayed, check if webhook is configured or if polling interval is too long

---
name: managing-gitpod
description: |
  Use when working with Gitpod — gitpod cloud development environment management
  and monitoring. Covers workspace lifecycle management, organization settings,
  usage tracking, prebuild configuration, environment class selection, and
  .gitpod.yml analysis. Use when managing Gitpod workspaces, reviewing team
  usage, configuring prebuilds, or analyzing development environment
  configurations.
connection_type: gitpod
preload: false
---

# Gitpod Cloud Development Environment Management Skill

Manage Gitpod workspaces, organizations, prebuilds, and usage analytics.

## Core Helper Functions

```bash
#!/bin/bash

# Gitpod API helper
gitpod_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${GITPOD_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://api.gitpod.io/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${GITPOD_API_TOKEN}" \
            "https://api.gitpod.io/${endpoint}"
    fi
}

# Gitpod CLI helper
gpctl() {
    gitpod_api POST "gitpod.v1.WorkspacesService/$1" "${2:-{}}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover organization and workspace status before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Gitpod Organization ==="
gitpod_api GET "api/v1/organization" | jq '{
    id: .id,
    name: .name,
    plan: .plan,
    member_count: .members
}'

echo ""
echo "=== Active Workspaces ==="
gitpod_api GET "api/v1/workspaces?limit=15" | jq -r '
    .items[] | "\(.id)\t\(.status.phase)\t\(.context.repository // "unknown")\tclass=\(.spec.class // "default")\tcreated=\(.createdAt | split("T")[0])"
' | column -t

echo ""
echo "=== Organization Members ==="
gitpod_api GET "api/v1/organization/members?limit=20" | jq -r '
    .items[] | "\(.userId)\t\(.email // .name)\trole=\(.role)\tstatus=\(.status)"
' | column -t | head -15

echo ""
echo "=== Gitpod Configuration ==="
if [ -f ".gitpod.yml" ]; then
    echo "--- .gitpod.yml ---"
    cat .gitpod.yml | head -25
elif [ -f ".gitpod.Dockerfile" ]; then
    echo "--- .gitpod.Dockerfile ---"
    head -15 .gitpod.Dockerfile
else
    echo "No .gitpod.yml found in current directory"
fi
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Usage Summary ==="
gitpod_api GET "api/v1/usage?limit=30" | jq '{
    total_hours: (.items | map(.credits) | add),
    workspace_count: (.items | length),
    by_class: (.items | group_by(.workspaceClass) | map({class: .[0].workspaceClass, hours: (map(.credits) | add), count: length}))
}'

echo ""
echo "=== Prebuild Status ==="
gitpod_api GET "api/v1/prebuilds?limit=10" | jq -r '
    .items[] | "\(.id)\tstatus=\(.status)\trepo=\(.context.repository // "unknown")\tbranch=\(.context.branch // "unknown")"
' | column -t

echo ""
echo "=== Environment Classes ==="
gitpod_api GET "api/v1/configuration/classes" | jq -r '
    .items[] | "\(.id)\t\(.displayName)\tcpu=\(.cpu)\tmemory=\(.memory)\tstorage=\(.storage)"
' | column -t 2>/dev/null || echo "Default environment classes"

echo ""
echo "=== Workspace Timeouts ==="
gitpod_api GET "api/v1/configuration/timeout" | jq '{
    default_timeout: .defaultTimeout,
    max_timeout: .maxTimeout
}' 2>/dev/null

echo ""
echo "=== .gitpod.yml Analysis ==="
if [ -f ".gitpod.yml" ]; then
    echo "Tasks defined: $(grep -c '^  - ' .gitpod.yml 2>/dev/null || echo 0)"
    echo "Ports configured: $(grep -c 'port:' .gitpod.yml 2>/dev/null || echo 0)"
    echo "VS Code extensions: $(grep -c 'id:' .gitpod.yml 2>/dev/null || echo 0)"
    grep "image:" .gitpod.yml 2>/dev/null | head -1
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Aggregate usage by workspace class and time period
- Never expose workspace environment variables or secrets

## Anti-Hallucination Rules
- NEVER guess workspace or organization IDs — always query API
- NEVER fabricate usage metrics — query actual Gitpod data
- NEVER assume .gitpod.yml exists — check filesystem first

## Safety Rules
- NEVER stop or delete workspaces without explicit user confirmation
- NEVER modify organization settings without user approval
- NEVER change prebuild configuration without user consent
- NEVER expose workspace environment variables or tokens

## Output Format

Present results as a structured report:
```
Managing Gitpod Report
══════════════════════
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


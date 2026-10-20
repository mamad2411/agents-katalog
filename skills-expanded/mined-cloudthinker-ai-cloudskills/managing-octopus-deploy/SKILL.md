---
name: managing-octopus-deploy
description: |
  Use when working with Octopus Deploy — octopus Deploy management for
  deployment automation. Covers deployment projects, environments, variable
  sets, tenant configuration, release management, and runbook execution. Use
  when checking deployment status, investigating release failures, managing
  environments, or auditing Octopus Deploy configurations.
connection_type: octopus-deploy
preload: false
---

# Octopus Deploy Management Skill

Manage and monitor Octopus Deploy projects, environments, releases, and tenants.

## Core Helper Functions

```bash
#!/bin/bash

# Octopus Deploy API helper
octopus_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "X-Octopus-ApiKey: ${OCTOPUS_API_KEY}" \
            -H "Content-Type: application/json" \
            "${OCTOPUS_URL}/api/${OCTOPUS_SPACE_ID:-Spaces-1}/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "X-Octopus-ApiKey: ${OCTOPUS_API_KEY}" \
            "${OCTOPUS_URL}/api/${OCTOPUS_SPACE_ID:-Spaces-1}/${endpoint}"
    fi
}

# Octopus server-level API (no space scoping)
octopus_server_api() {
    curl -s -X "${1:-GET}" \
        -H "X-Octopus-ApiKey: ${OCTOPUS_API_KEY}" \
        "${OCTOPUS_URL}/api/${2}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover spaces, projects, and environments before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Server Info ==="
octopus_server_api GET "serverstatus" | jq '{version: .Version, isInMaintenanceMode: .IsInMaintenanceMode}'

echo ""
echo "=== Spaces ==="
octopus_server_api GET "spaces?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\tdefault=\(.IsDefault)"
' | column -t

echo ""
echo "=== Projects ==="
octopus_api GET "projects?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\tgroup=\(.ProjectGroupId)\tdisabled=\(.IsDisabled)"
' | column -t

echo ""
echo "=== Environments ==="
octopus_api GET "environments?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\tsortOrder=\(.SortOrder)"
' | column -t

echo ""
echo "=== Recent Deployments ==="
octopus_api GET "deployments?take=10" | jq -r '
    .Items[] | "\(.Id)\t\(.ProjectId)\t\(.EnvironmentId)\t\(.State)\t\(.Created[0:16])"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `take` and `skip` parameters for pagination
- Never dump full deployment process — extract step summaries

## Common Operations

### Deployment Dashboard

```bash
#!/bin/bash
echo "=== Dashboard ==="
octopus_api GET "dashboard" | jq '{
    environments: [.Environments[] | .Name],
    projects: (.Items | group_by(.ProjectId) | map({
        project: .[0].ProjectId,
        deployments: [.[] | {env: .EnvironmentId, state: .State, version: .ReleaseVersion}]
    }) | .[:10])
}'

echo ""
echo "=== Recent Deployments (detailed) ==="
octopus_api GET "deployments?take=15" | jq -r '
    .Items[] |
    "\(.Name // .Id)\t\(.State)\t\(.TaskId)\t\(.Created[0:16])"
' | column -t

echo ""
echo "=== Failed Deployments ==="
octopus_api GET "tasks?states=Failed&take=10&name=Deploy" | jq -r '
    .Items[] |
    "\(.Description[0:50])\t\(.State)\t\(.CompletedTime[0:16] // "unknown")\t\(.ErrorMessage[0:60] // "")"
' | column -t
```

### Project Management

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID or slug required}"

echo "=== Project Details ==="
octopus_api GET "projects/${PROJECT_ID}" | jq '{
    Id, Name, Slug,
    LifecycleId, ProjectGroupId,
    IsDisabled, TenantedDeploymentMode,
    IncludedLibraryVariableSetIds: (.IncludedLibraryVariableSetIds | length),
    DeploymentProcessId: .DeploymentProcessId
}'

echo ""
echo "=== Deployment Process ==="
PROCESS_ID=$(octopus_api GET "projects/${PROJECT_ID}" | jq -r '.DeploymentProcessId')
octopus_api GET "deploymentprocesses/${PROCESS_ID}" | jq -r '
    .Steps[] | "\(.Name)\troles=\(.Properties["Octopus.Action.TargetRoles"] // "any")\tactions=\([.Actions[].Name] | join(","))"
' | column -t

echo ""
echo "=== Recent Releases ==="
octopus_api GET "projects/${PROJECT_ID}/releases?take=10" | jq -r '
    .Items[] | "\(.Id)\tv\(.Version)\t\(.Assembled[0:16])\tchannel=\(.ChannelId)"
' | column -t
```

### Environment Management

```bash
#!/bin/bash
echo "=== Environment Details ==="
octopus_api GET "environments?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\tsort=\(.SortOrder)\tguided=\(.UseGuidedFailure)"
' | column -t

echo ""
echo "=== Machines by Environment ==="
octopus_api GET "environments" | jq -r '.Items[].Id' | while read env_id; do
    ENV_NAME=$(octopus_api GET "environments/${env_id}" | jq -r '.Name')
    MACHINES=$(octopus_api GET "environments/${env_id}/machines?take=100" | jq '.TotalResults')
    echo "${env_id}\t${ENV_NAME}\t${MACHINES} machines"
done | column -t

echo ""
echo "=== Deployment Targets ==="
octopus_api GET "machines?take=20" | jq -r '
    .Items[] | "\(.Name)\tstatus=\(.HealthStatus)\troles=\(.Roles | join(","))\tenvs=\(.EnvironmentIds | length)"
' | column -t
```

### Variable Sets

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Project Variables ==="
octopus_api GET "variables/variableset-${PROJECT_ID}" | jq -r '
    .Variables[] | "\(.Name)\tscope=\(.Scope | to_entries | map("\(.key)=\(.value | length)") | join(",") // "all")\ttype=\(.Type // "String")\tsensitive=\(.IsSensitive)"
' | column -t | head -25

echo ""
echo "=== Library Variable Sets ==="
octopus_api GET "libraryvariablesets?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\tvariables=\(.Variables // 0)\tdescription=\(.Description[0:40] // "")"
' | column -t
```

### Tenant Management

```bash
#!/bin/bash
echo "=== Tenants ==="
octopus_api GET "tenants?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\tprojects=\(.ProjectEnvironments | keys | length)\ttags=\(.TenantTags | join(","))"
' | column -t

echo ""
echo "=== Tenant Details ==="
TENANT_ID="${1:-}"
if [ -n "$TENANT_ID" ]; then
    octopus_api GET "tenants/${TENANT_ID}" | jq '{
        Id, Name,
        TenantTags,
        ProjectEnvironments: (.ProjectEnvironments | to_entries | map({project: .key, environments: .value}))
    }'
fi
```

### Runbook Execution

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Runbooks ==="
octopus_api GET "projects/${PROJECT_ID}/runbooks?take=20" | jq -r '
    .Items[] | "\(.Id)\t\(.Name)\t\(.Description[0:40] // "")"
' | column -t

echo ""
echo "=== Recent Runbook Runs ==="
octopus_api GET "tasks?name=RunbookRun&take=10" | jq -r '
    .Items[] | "\(.Description[0:50])\t\(.State)\t\(.CompletedTime[0:16] // "running")"
' | column -t
```

### Release & Deployment

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"
RELEASE_VERSION="${2:-}"

if [ -n "$RELEASE_VERSION" ]; then
    echo "=== Release Details ==="
    octopus_api GET "projects/${PROJECT_ID}/releases/${RELEASE_VERSION}" | jq '{
        Id, Version, Assembled, ChannelId,
        SelectedPackages: [.SelectedPackages[] | {ActionName, Version: .Version}]
    }'

    echo ""
    echo "=== Deployment History for Release ==="
    RELEASE_ID=$(octopus_api GET "projects/${PROJECT_ID}/releases/${RELEASE_VERSION}" | jq -r '.Id')
    octopus_api GET "releases/${RELEASE_ID}/deployments?take=10" | jq -r '
        .Items[] | "\(.EnvironmentId)\t\(.State)\t\(.Created[0:16])\ttask=\(.TaskId)"
    ' | column -t
else
    echo "=== Latest Releases ==="
    octopus_api GET "projects/${PROJECT_ID}/releases?take=10" | jq -r '
        .Items[] | "v\(.Version)\t\(.Assembled[0:16])\tchannel=\(.ChannelId)"
    ' | column -t
fi
```

## Anti-Hallucination Rules
- NEVER guess project IDs — always discover via API first (format is `Projects-123`)
- NEVER fabricate environment or tenant IDs — use discovery endpoints
- NEVER assume Space ID — default is `Spaces-1` but verify
- Octopus uses hyphenated IDs (e.g., `Environments-1`, `Tenants-5`) — do not use names as IDs

## Safety Rules
- NEVER create deployments without explicit user confirmation
- NEVER delete projects, environments, or tenants without user approval
- NEVER modify variable sets without understanding scope impact
- NEVER expose sensitive variable values — API masks them by default
- NEVER run runbooks without confirming the target environment

## Output Format

Present results as a structured report:
```
Managing Octopus Deploy Report
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
- **Space scoping**: All resources are scoped to a Space — include Space ID in API path
- **ID format**: Octopus uses `Type-Number` format (e.g., `Projects-42`) — not slugs or names
- **Lifecycle phases**: Environments follow lifecycle ordering — deployments must follow the defined progression
- **Tenanted deployments**: Tenanted projects require tenant selection for deployment — untenanted and tenanted are separate modes
- **Variable scoping**: Variables can be scoped to environments, roles, machines, channels — scope conflicts cause unexpected behavior
- **Guided failure**: Environments with guided failure enabled pause on failure for manual intervention
- **Channels**: Channels control which packages and lifecycles apply to a release — check channel rules

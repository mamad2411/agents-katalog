---
name: managing-azure-devops
description: |
  Use when working with Azure Devops — azure DevOps comprehensive management.
  Covers pipelines, boards, repositories, artifacts, test plans, work item
  tracking, and release management. Use when checking pipeline status, managing
  work items, investigating build failures, or auditing Azure DevOps project
  configurations.
connection_type: azure-devops
preload: false
---

# Azure DevOps Management Skill

Manage and monitor Azure DevOps pipelines, boards, repos, artifacts, and test plans.

## Core Helper Functions

```bash
#!/bin/bash

# Azure DevOps REST API helper
azdo_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    local api_version="${4:-7.1}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u ":${AZDO_PAT}" \
            -H "Content-Type: application/json" \
            "https://dev.azure.com/${AZDO_ORG}/${AZDO_PROJECT}/_apis/${endpoint}?api-version=${api_version}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u ":${AZDO_PAT}" \
            "https://dev.azure.com/${AZDO_ORG}/${AZDO_PROJECT}/_apis/${endpoint}?api-version=${api_version}"
    fi
}

# Azure DevOps CLI wrapper
az_devops() {
    az devops "$@" --organization "https://dev.azure.com/${AZDO_ORG}" --project "$AZDO_PROJECT" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always discover projects, pipelines, and repos before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Organization Projects ==="
curl -s -u ":${AZDO_PAT}" \
    "https://dev.azure.com/${AZDO_ORG}/_apis/projects?api-version=7.1" | jq -r '
    .value[] | "\(.id)\t\(.name)\t\(.state)\t\(.lastUpdateTime[0:10])"
' | column -t

echo ""
echo "=== Pipelines ==="
azdo_api GET "pipelines" | jq -r '
    .value[] | "\(.id)\t\(.name)\t\(.folder // "/")"
' | column -t | head -20

echo ""
echo "=== Repositories ==="
azdo_api GET "git/repositories" | jq -r '
    .value[] | "\(.id[0:8])\t\(.name)\t\(.defaultBranch // "none")\t\(.size // 0 | . / 1048576 | floor)MB"
' | column -t

echo ""
echo "=== Recent Builds ==="
azdo_api GET "build/builds?\$top=15&queryOrder=finishTimeDescending" | jq -r '
    .value[] |
    "\(.definition.name)\t#\(.buildNumber)\t\(.result // .status)\t\(.sourceBranch | sub("refs/heads/"; ""))\t\(.finishTime[0:16] // "running")"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use `$top`, `$skip`, and `$filter` OData parameters for server-side filtering
- Never dump full build logs — use timeline API for step-level data

## Common Operations

### Pipeline Run Dashboard

```bash
#!/bin/bash
echo "=== Pipeline Run Summary ==="
azdo_api GET "build/builds?\$top=50" | jq '{
    total: (.value | length),
    succeeded: [.value[] | select(.result == "succeeded")] | length,
    failed: [.value[] | select(.result == "failed")] | length,
    canceled: [.value[] | select(.result == "canceled")] | length,
    in_progress: [.value[] | select(.status == "inProgress")] | length
}'

echo ""
echo "=== Failed Builds ==="
azdo_api GET "build/builds?\$top=10&resultFilter=failed&queryOrder=finishTimeDescending" | jq -r '
    .value[] |
    "\(.definition.name)\t#\(.buildNumber)\t\(.sourceBranch | sub("refs/heads/"; ""))\t\(.finishTime[0:16])\t\(.requestedFor.displayName)"
' | column -t

echo ""
echo "=== Build Timeline (steps) ==="
BUILD_ID="${1:-}"
if [ -n "$BUILD_ID" ]; then
    azdo_api GET "build/builds/${BUILD_ID}/timeline" | jq -r '
        .records[] | select(.type == "Task") |
        "\(.name)\t\(.result // .state)\t\(.issues | length) issues"
    ' | column -t | head -20
fi
```

### Work Item Tracking (Boards)

```bash
#!/bin/bash
echo "=== Active Work Items ==="
WIQL='{"query": "SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo] FROM WorkItems WHERE [System.TeamProject] = @project AND [System.State] <> '\''Closed'\'' ORDER BY [System.ChangedDate] DESC"}'
azdo_api POST "wit/wiql" "$WIQL" | jq -r '
    .workItems[:20][] | "\(.id)"
' | while read id; do
    azdo_api GET "wit/workitems/${id}?\$expand=relations" | jq -r '
        "\(.id)\t\(.fields["System.WorkItemType"])\t\(.fields["System.State"])\t\(.fields["System.Title"][0:50])\t\(.fields["System.AssignedTo"].displayName // "unassigned")"
    '
done | column -t

echo ""
echo "=== Sprint Summary ==="
azdo_api GET "work/teamsettings/iterations?\$timeframe=current" | jq -r '
    .value[] | "\(.name)\t\(.attributes.startDate[0:10]) to \(.attributes.finishDate[0:10])\t\(.path)"
'
```

### Repository Management

```bash
#!/bin/bash
REPO_NAME="${1:?Repo name required}"
REPO_ID=$(azdo_api GET "git/repositories" | jq -r ".value[] | select(.name == \"${REPO_NAME}\") | .id")

echo "=== Repository Info ==="
azdo_api GET "git/repositories/${REPO_ID}" | jq '{name, defaultBranch, size, remoteUrl, webUrl}'

echo ""
echo "=== Recent Commits ==="
azdo_api GET "git/repositories/${REPO_ID}/commits?\$top=10" | jq -r '
    .value[] | "\(.commitId[0:8])\t\(.author.name)\t\(.author.date[0:16])\t\(.comment[0:60])"
' | column -t

echo ""
echo "=== Active Pull Requests ==="
azdo_api GET "git/repositories/${REPO_ID}/pullrequests?searchCriteria.status=active" | jq -r '
    .value[] |
    "PR#\(.pullRequestId)\t\(.title[0:40])\t\(.createdBy.displayName)\t\(.sourceRefName | sub("refs/heads/"; ""))"
' | column -t
```

### Artifact Feed Management

```bash
#!/bin/bash
echo "=== Artifact Feeds ==="
curl -s -u ":${AZDO_PAT}" \
    "https://feeds.dev.azure.com/${AZDO_ORG}/${AZDO_PROJECT}/_apis/packaging/feeds?api-version=7.1" | jq -r '
    .value[] | "\(.id[0:8])\t\(.name)\t\(.fullyQualifiedName)\tpackages=\(.totalUniquePackages // 0)"
' | column -t

echo ""
echo "=== Feed Packages ==="
FEED_NAME="${1:?Feed name required}"
curl -s -u ":${AZDO_PAT}" \
    "https://feeds.dev.azure.com/${AZDO_ORG}/${AZDO_PROJECT}/_apis/packaging/feeds/${FEED_NAME}/packages?\$top=20&api-version=7.1" | jq -r '
    .value[] | "\(.name)\t\(.protocolType)\tversions=\(.versions | length)\tlatest=\(.versions[0].version // "none")"
' | column -t
```

### Test Plans

```bash
#!/bin/bash
echo "=== Test Plans ==="
azdo_api GET "testplan/plans" | jq -r '
    .value[] | "\(.id)\t\(.name)\t\(.state)\towner=\(.owner.displayName // "unassigned")"
' | column -t

echo ""
echo "=== Recent Test Runs ==="
azdo_api GET "test/runs?\$top=10" | jq -r '
    .value[] |
    "\(.id)\t\(.name[0:30])\t\(.state)\ttotal=\(.totalTests)\tpassed=\(.passedTests)\tfailed=\(.unanalyzedTests)"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess project names or pipeline IDs — always discover via API
- NEVER fabricate work item IDs — use WIQL queries to find them
- NEVER assume repository GUIDs — look up by name first
- API versions vary by endpoint — always specify `api-version`

## Safety Rules
- NEVER trigger pipeline runs without explicit user confirmation
- NEVER modify work items without user approval
- NEVER delete branches or repositories without confirming
- NEVER expose variable group secrets — API masks them by default

## Output Format

Present results as a structured report:
```
Managing Azure Devops Report
════════════════════════════
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
- **API URL structure**: Different services use different base URLs (dev.azure.com, feeds.dev.azure.com, vsrm.dev.azure.com)
- **PAT scopes**: PATs need specific scopes — a pipeline PAT may not access boards
- **OData filtering**: Use `$filter`, `$top`, `$skip` for efficient queries — not all endpoints support all operators
- **Branch refs**: Azure DevOps uses full refs (`refs/heads/main`) — strip prefix for display
- **Classic vs YAML**: Classic pipelines use release definitions; YAML pipelines use multi-stage — different APIs
- **Service connections**: Required for external integrations — check with `serviceendpoint/endpoints` API

---
name: managing-azure-boards-deep
description: |
  Use when working with Azure Boards Deep — deep Azure Boards management
  covering work items, sprints, backlogs, queries, and team velocity analytics.
  Use when performing deep audits of Azure DevOps Boards, analyzing sprint
  health, reviewing backlog grooming, or assessing team capacity and velocity
  across Azure DevOps projects.
connection_type: azure-devops
preload: false
---

# Managing Azure Boards (Deep)

Deep Azure Boards analysis covering work item health, sprint velocity, and backlog management via the Azure DevOps REST API.

## Discovery Phase

```bash
#!/bin/bash
ADO_BASE="https://dev.azure.com/$ADO_ORG"

echo "=== Projects ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/_apis/projects?api-version=7.0" \
  | jq -r '.value[] | "\(.id)\t\(.name)\t\(.state)\t\(.lastUpdateTime[0:10])"' | column -t

echo ""
PROJECT="${1:?Project name required}"
echo "=== Teams ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/_apis/teams?api-version=7.0" \
  | jq -r '.value[] | "\(.id)\t\(.name)\t\(.description[0:40] // "")"' | column -t

echo ""
echo "=== Current Iteration ==="
TEAM="${2:-$PROJECT Team}"
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/$TEAM/_apis/work/teamsettings/iterations?\$timeframe=current&api-version=7.0" \
  | jq -r '.value[] | "\(.id)\t\(.name)\t\(.attributes.startDate[0:10])\t\(.attributes.finishDate[0:10])"'

echo ""
echo "=== Work Item Types ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/_apis/wit/workitemtypes?api-version=7.0" \
  | jq -r '.value[] | "\(.name)\t\(.description[0:50])"' | column -t | head -10

echo ""
echo "=== Area Paths ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/_apis/wit/classificationnodes/areas?api-version=7.0&\$depth=2" \
  | jq -r '.name, (.children[]? | "  \(.name)")'
```

## Analysis Phase

```bash
#!/bin/bash
ADO_BASE="https://dev.azure.com/$ADO_ORG"
PROJECT="${1:?Project required}"

echo "=== Work Item Counts by State ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/_apis/wit/wiql?api-version=7.0" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT [System.Id] FROM workitems WHERE [System.TeamProject] = '"'$PROJECT'"' AND [System.State] <> '"'Removed'"' ORDER BY [System.ChangedDate] DESC"}' \
  | jq '{total_work_items: (.workItems | length)}'

for STATE in "New" "Active" "Resolved" "Closed"; do
  COUNT=$(curl -s -u ":$ADO_PAT" \
    "$ADO_BASE/$PROJECT/_apis/wit/wiql?api-version=7.0" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"SELECT [System.Id] FROM workitems WHERE [System.TeamProject] = '$PROJECT' AND [System.State] = '$STATE'\"}" \
    | jq '.workItems | length')
  echo -e "$STATE\t$COUNT"
done | column -t

echo ""
echo "=== Unassigned Active Items ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/_apis/wit/wiql?api-version=7.0" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"SELECT [System.Id] FROM workitems WHERE [System.TeamProject] = '$PROJECT' AND [System.State] = 'Active' AND [System.AssignedTo] = ''\"}" \
  | jq '{unassigned_active: (.workItems | length)}'

echo ""
echo "=== Sprint Burndown ==="
TEAM="${2:-$PROJECT Team}"
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/$TEAM/_apis/work/teamsettings/iterations?\$timeframe=current&api-version=7.0" \
  | jq -r '.value[0] | "Sprint: \(.name)\nStart: \(.attributes.startDate[0:10])\nEnd: \(.attributes.finishDate[0:10])"'

echo ""
echo "=== Recent Work Items ==="
curl -s -u ":$ADO_PAT" \
  "$ADO_BASE/$PROJECT/_apis/wit/wiql?api-version=7.0" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo] FROM workitems WHERE [System.TeamProject] = '$PROJECT' ORDER BY [System.ChangedDate] DESC\"}" \
  | jq -r '.workItems[:15][] | "\(.id)"' | while read ID; do
    curl -s -u ":$ADO_PAT" "$ADO_BASE/$PROJECT/_apis/wit/workitems/$ID?fields=System.Title,System.State,System.WorkItemType&api-version=7.0" \
    | jq -r '"\(.id)\t\(.fields["System.WorkItemType"])\t\(.fields["System.State"])\t\(.fields["System.Title"][0:40])"'
  done | column -t
```

## Output Format

```
AZURE BOARDS DEEP HEALTH: [Project]
Total Work Items:  [count]
Active Items:      [count]
Unassigned Active: [count]
Current Sprint:    [name] ([start] - [end])

STATE DISTRIBUTION
State            Count   Pct
New              [n]     [pct]%
Active           [n]     [pct]%
Resolved         [n]     [pct]%
Closed           [n]     [pct]%

SPRINT VELOCITY (Last 3)
Sprint           Completed  Committed  Velocity
[name]           [n]pts     [n]pts     [pct]%
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


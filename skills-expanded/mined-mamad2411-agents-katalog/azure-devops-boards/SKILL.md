---
name: azure-devops-boards
description: |
  Use when working with Azure Devops Boards — azure DevOps Boards work item
  tracking, sprint analysis, burndown metrics, team velocity, and backlog
  management via Azure DevOps CLI extension.
connection_type: azure
preload: false
---

# Azure DevOps Boards Skill

Manage and analyze Azure DevOps Boards using `az boards` and `az devops` CLI commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume project names, team names, iteration paths, or work item IDs.

```bash
# Set default organization
az devops configure --defaults organization="$ORG_URL"

# Discover projects
az devops project list --output json --query "value[].{name:name, id:id, state:state}"

# Discover teams in a project
az devops team list --project "$PROJECT" --output json --query "[].{name:name, id:id}"
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for project in $(echo "$projects" | jq -c '.[]'); do
  {
    name=$(echo "$project" | jq -r '.name')
    az boards query --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject]='$name' AND [System.State]='Active'" --project "$name" --output json
  } &
done
wait
```

## Helper Functions

```bash
# Query work items with WIQL
query_work_items() {
  local project="$1" wiql="$2"
  az boards query --wiql "$wiql" --project "$project" --output json
}

# Get work item details
get_work_item() {
  local id="$1"
  az boards work-item show --id "$id" --output json \
    --query "{id:id, title:fields.\"System.Title\", state:fields.\"System.State\", type:fields.\"System.WorkItemType\", assignedTo:fields.\"System.AssignedTo\".displayName, priority:fields.\"Microsoft.VSTS.Common.Priority\", storyPoints:fields.\"Microsoft.VSTS.Scheduling.StoryPoints\", iteration:fields.\"System.IterationPath\"}"
}

# List iterations (sprints)
list_iterations() {
  local project="$1" team="$2"
  az boards iteration team list --project "$project" --team "$team" --output json \
    --query "[].{name:name, path:path, startDate:attributes.startDate, finishDate:attributes.finishDate, timeFrame:attributes.timeFrame}"
}

# Get iteration work items
get_iteration_items() {
  local project="$1" iteration="$2"
  az boards query --wiql "SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo],[Microsoft.VSTS.Scheduling.StoryPoints] FROM WorkItems WHERE [System.TeamProject]='$project' AND [System.IterationPath]='$iteration'" --project "$project" --output json
}
```

## Common Operations

### 1. Sprint Status Overview

```bash
# Get current sprint work items
current_iteration=$(az boards iteration team list --project "$PROJECT" --team "$TEAM" --output json \
  --query "[?attributes.timeFrame=='current'] | [0].path" -o tsv)

az boards query --wiql "SELECT [System.Id],[System.Title],[System.State],[System.AssignedTo],[Microsoft.VSTS.Scheduling.StoryPoints],[System.WorkItemType] FROM WorkItems WHERE [System.IterationPath]='$current_iteration' ORDER BY [System.State]" \
  --project "$PROJECT" --output json
```

### 2. Burndown Analysis

```bash
# Get sprint scope and completion
az boards query --wiql "
  SELECT [System.Id],[System.State],[Microsoft.VSTS.Scheduling.StoryPoints]
  FROM WorkItems
  WHERE [System.IterationPath]='$ITERATION'
  AND [System.WorkItemType] IN ('User Story','Bug')
" --project "$PROJECT" --output json

# Summarize by state
# Parse results to calculate: Total points, Completed points, Remaining points, In Progress points
```

### 3. Backlog Health

```bash
# Unassigned items in backlog
az boards query --wiql "
  SELECT [System.Id],[System.Title],[System.WorkItemType],[Microsoft.VSTS.Common.Priority]
  FROM WorkItems
  WHERE [System.TeamProject]='$PROJECT'
  AND [System.State]='New'
  AND [System.AssignedTo]=''
  ORDER BY [Microsoft.VSTS.Common.Priority]
" --project "$PROJECT" --output json

# Items without estimates
az boards query --wiql "
  SELECT [System.Id],[System.Title]
  FROM WorkItems
  WHERE [System.TeamProject]='$PROJECT'
  AND [System.WorkItemType]='User Story'
  AND [Microsoft.VSTS.Scheduling.StoryPoints]=''
  AND [System.State] NOT IN ('Closed','Removed')
" --project "$PROJECT" --output json
```

### 4. Team Velocity

```bash
# Get completed story points per iteration
iterations=$(az boards iteration team list --project "$PROJECT" --team "$TEAM" --output json \
  --query "[?attributes.timeFrame=='past'] | [-3:]")
for iter in $(echo "$iterations" | jq -c '.[]'); do
  {
    path=$(echo "$iter" | jq -r '.path')
    echo "Sprint: $path"
    az boards query --wiql "SELECT [Microsoft.VSTS.Scheduling.StoryPoints] FROM WorkItems WHERE [System.IterationPath]='$path' AND [System.State]='Closed' AND [System.WorkItemType]='User Story'" --project "$PROJECT" --output json
  } &
done
wait
```

### 5. Work Item Aging

```bash
# Find old items still in active state
az boards query --wiql "
  SELECT [System.Id],[System.Title],[System.CreatedDate],[System.State],[System.AssignedTo]
  FROM WorkItems
  WHERE [System.TeamProject]='$PROJECT'
  AND [System.State] IN ('Active','New')
  AND [System.CreatedDate] < @Today-30
  ORDER BY [System.CreatedDate]
" --project "$PROJECT" --output json
```

## Output Format

Present results as a structured report:
```
Azure Devops Boards Report
══════════════════════════
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

1. **WIQL syntax**: WIQL uses single quotes for string values, not double quotes. Field names with dots must be in square brackets.
2. **Organization default**: Always set `az devops configure --defaults organization=` before running commands.
3. **Story Points field**: The field name varies by process template -- Agile uses `Microsoft.VSTS.Scheduling.StoryPoints`, Scrum uses `Microsoft.VSTS.Scheduling.Effort`.
4. **Iteration paths**: Iteration paths include the project name prefix (e.g., `Project\Sprint 1`). Use the full path from discovery.
5. **Query limits**: WIQL queries return a max of 200 work items by default. Use `--top` parameter for larger result sets.

---
name: devops-boards
description: Azure DevOps work item management, sprint planning, and board operations. Use when asked to create, update, query, or manage work items, sprints, iterations, or boards.
---

# DevOps Boards

## When to Use

- User asks to create, update, or query work items (user stories, tasks, bugs, features, epics)
- User wants to manage sprints or iterations
- User asks about board status, backlog, or sprint progress
- User needs to assign, move, or link work items
- User mentions WIQL queries or work item searches

## Instructions

### Work Item Hierarchy

```
Epic
  └── Feature
        └── User Story
              └── Task
Bug (can be at any level)
```

### Creating Work Items

1. Determine the work item **type** from context (default to "User Story" if ambiguous)
2. Set the **project** name
3. Compose the **title** — concise, action-oriented
4. Use the **fields** parameter for additional fields:
   - `Microsoft.VSTS.Common.Priority` — 1 (Critical), 2 (High), 3 (Medium), 4 (Low)
   - `Microsoft.VSTS.Scheduling.StoryPoints` — numeric estimate
   - `System.Tags` — semicolon-separated tags
   - `System.AreaPath` — area path
   - `System.IterationPath` — iteration/sprint

### Querying with WIQL

```sql
-- Active user stories in current sprint
SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems
WHERE [System.WorkItemType] = 'User Story'
  AND [System.State] = 'Active'
  AND [System.IterationPath] = @CurrentIteration

-- Bugs assigned to a person
SELECT [System.Id], [System.Title], [System.AssignedTo]
FROM WorkItems
WHERE [System.WorkItemType] = 'Bug'
  AND [System.AssignedTo] = 'User Name'
  AND [System.State] <> 'Closed'

-- Items modified in the last 7 days
SELECT [System.Id], [System.Title], [System.ChangedDate]
FROM WorkItems
WHERE [System.ChangedDate] >= @Today - 7
ORDER BY [System.ChangedDate] DESC
```

### Linking Work Items

Common link types:
- `System.LinkTypes.Hierarchy-Forward` — parent/child
- `System.LinkTypes.Related` — related items
- `System.LinkTypes.Dependency-Forward` — predecessor/successor

## Tools

- `devops_create_work_item` — Create a new work item
- `devops_update_work_item` — Update fields on an existing work item
- `devops_get_work_item` — Get full details of a work item by ID
- `devops_query_work_items` — Query work items using WIQL
- `devops_add_comment` — Add a discussion comment (markdown auto-converted to HTML)
- `devops_list_boards` — List boards in a project
- `devops_move_work_item` — Change a work item's state
- `devops_link_work_items` — Create links between work items
- `devops_get_iterations` — List iterations/sprints
- `devops_assign_work_item` — Assign to a team member
- `devops_list_team_members` — List team members
- `devops_get_work_item_history` — Get revision history

## See Also

- **devops-repos** — repository and PR management
- **devops-pipelines** — CI/CD pipeline operations
- **devops-wiki** — project documentation in wikis

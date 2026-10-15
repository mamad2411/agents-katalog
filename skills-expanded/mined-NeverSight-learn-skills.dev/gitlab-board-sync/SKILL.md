---
name: gitlab-board-sync
description: (NS) Sync existing GitLab issues with local planning and execution — milestone, RF labels, status transitions, assignee, estimates, spent time. Use during implementation when tasks link to GitLab issues or after plan-version-from-gitlab sync — not for creating new issues (use mcp-gitlab-usage). Always use atomic set_issue_labels and three-step status cycle. Read mcp-gitlab-usage for tool contracts.
depends:
  - mcp-gitlab-usage
---

# GitLab Board Sync

Mirror local SDD planning/execution state onto **existing** GitLab issues. Does **not** create issues.

## Prerequisites

1. GitLab MCP available — follow `mcp-gitlab-usage` for all tool calls
2. If multiple GitLab MCP servers: ask human which to use
3. `{product_root}/docs/context/gitlab-sync-config.md` validated
4. For post-planning batch: `gitlab-issue-feature-map.md` exists

## Configuration

Read `references/gitlab-sync-config.template.md` for expected fields:

- `project_id`, `milestone_id`, `assignee_default`
- `status_backlog`, `status_in_progress`, `status_done`, `status_blocked`
- `rf_label_format`, `base_branch`, `work_branch`, `mr_target_branch`

Discover unknown status labels via `list_project_labels` — confirm with human.

## Flow C — Pre-implementation read

When task lists GitLab issue IIDs:

1. `read_issue` for description + recent comments
2. Non-blocking if inaccessible — log warning, continue
3. **Do not mutate** issue in this flow

## Flow A — Post-planning batch

Per issue in map (excluding `exclude_issues`):

1. Validate milestone (project + group)
2. `update_issue` with `milestone_id`
3. **One** `set_issue_labels` — `remove_labels` + `add_labels` atomically (RF, Status, Equipe)
4. `assign_issue`
5. `set_issue_estimate` from linked task header (seconds)

## Flow B — Per-task execution sync

### Task start (before coding)

```
remove: status_backlog
add: status_in_progress
```

Record start time for `add_issue_spent_time`.

### Task complete (after validation)

Only if already `status_in_progress`:

```
remove: status_in_progress
add: status_done, RF: NNN
add_issue_spent_time
add_issue_comment (internal=true)
```

**Never** backlog → done in one step.

## Anti-patterns

| Wrong                               | Right                            |
| ----------------------------------- | -------------------------------- |
| `assignee` on `update_issue`        | `assign_issue`                   |
| Two label calls for one transition  | Single atomic `set_issue_labels` |
| Manual `Milestone:` label           | `milestone_id` on `update_issue` |
| `set_issue_estimate` for time spent | `add_issue_spent_time`           |
| Public comment for internal notes   | `internal: true`                 |

## References

| File                                        | When                   |
| ------------------------------------------- | ---------------------- |
| `references/gitlab-sync-config.template.md` | Bootstrap config       |
| `mcp-gitlab-usage`                          | Tool schemas and gates |

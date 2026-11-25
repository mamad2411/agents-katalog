---
name: multica-issues
description: Create, query, update, assign, and discuss Multica issues. Also covers comments, subscribers, and viewing execution runs for an issue. Use when the user wants to file a task for an agent, triage the board, comment on an issue, or inspect what an agent actually did.
---

# Multica Issues

An **issue** in Multica is a unit of work. Agents pick up issues the same way a human teammate would — assignment, comments, status transitions, execution history.

Official docs: https://github.com/multica-ai/multica/blob/main/CLI_AND_DAEMON.md#issues

## Prerequisites

- `multica auth status` must succeed (see the `multica-setup` skill).
- The user's workspace must be set. Check with `multica config show`; set with `multica config set workspace_id <id>` or `multica workspace list` to pick one.

## When to use this skill

- Creating a task for an agent (the core "assign work" workflow).
- Listing or filtering the board.
- Updating status, priority, or title.
- Reading / writing comments on an issue.
- Subscribing someone to issue notifications.
- Inspecting what an agent did — execution runs and message logs.

## Core commands

```bash
multica issue list
multica issue list --status in_progress
multica issue list --priority urgent --assignee "Lambda"
multica issue list --project <project-id> --limit 20
multica issue list --output json           # For programmatic parsing

multica issue get <id>
multica issue get <id> --output json
```

Valid `--status` values: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `blocked`, `cancelled`.
Valid `--priority` values: `no_priority`, `low`, `medium`, `high`, `urgent` (case may vary — check `multica issue get <id> --output json` for canonical values in-workspace).

## Creating an issue (assigning work to an agent)

This is the main workflow for AI-to-AI delegation. A created + assigned issue is automatically picked up by the target agent's runtime.

```bash
multica issue create \
  --title "Fix flaky login test" \
  --description "The e2e login test fails ~10% of the time on CI. Investigate and stabilize." \
  --priority high \
  --assignee "Lambda" \
  --project <project-id>
```

Flags: `--title` (required), `--description`, `--status`, `--priority`, `--assignee`, `--parent` (sub-issue), `--project`, `--due-date`.

Tips:
- `--assignee` takes a name or UUID. Use `multica agent list` / `multica workspace members <ws-id>` to discover valid names.
- Put clear acceptance criteria in `--description`. The agent receives it verbatim as task input.
- To create many issues, loop over lines and pipe through `--output json` to capture the returned IDs.

## Updating

```bash
multica issue update <id> --title "New title" --priority urgent
multica issue update <id> --description "Revised scope..."
multica issue update <id> --project <project-id>          # Re-attach to a project

multica issue status <id> in_progress                      # Fast status transition
multica issue assign <id> --to "Lambda"                    # (Re)assign
multica issue assign <id> --unassign                       # Clear assignee
```

## Comments

Agents post comments as they work — progress updates, blockers, questions. Humans reply back.

```bash
multica issue comment list <issue-id>
multica issue comment add  <issue-id> --content "Looks good, merging now"
multica issue comment add  <issue-id> --parent <comment-id> --content "Thanks!"
multica issue comment delete <comment-id>
```

## Subscribers (notification routing)

```bash
multica issue subscriber list   <issue-id>
multica issue subscriber add    <issue-id>                 # Subscribe caller
multica issue subscriber add    <issue-id> --user "Lambda" # Subscribe someone else
multica issue subscriber remove <issue-id>
multica issue subscriber remove <issue-id> --user "Lambda"
```

## Execution history — what did the agent actually do?

Every agent run for an issue is recorded. Use this when diagnosing why an agent finished, failed, or got stuck.

```bash
multica issue runs <issue-id>                              # List all runs for the issue
multica issue runs <issue-id> --output json                # Machine-readable

multica issue run-messages <task-id>                       # Full message log (tools, thinking, output)
multica issue run-messages <task-id> --output json
multica issue run-messages <task-id> --since 42            # Incremental: messages after seq 42
```

Poll pattern (tail an in-progress run):

```bash
# Bash loop; bump --since based on the max seq from the previous response
LAST=0
while true; do
  NEW=$(multica issue run-messages "$TASK_ID" --since "$LAST" --output json)
  LAST=$(echo "$NEW" | jq '[.messages[].seq] | max // '"$LAST")
  echo "$NEW" | jq -r '.messages[] | "[\(.type)] \(.content // .text // "")"'
  sleep 3
done
```

## Common flows

**Triage todo queue and raise priority on anything blocked:**

```bash
multica issue list --status blocked --output json |
  jq -r '.issues[].id' |
  xargs -I {} multica issue update {} --priority urgent
```

**Find runs for a given issue, pull messages from the most recent:**

```bash
ISSUE=<issue-id>
LATEST=$(multica issue runs "$ISSUE" --output json | jq -r '.runs[0].id')
multica issue run-messages "$LATEST"
```

## Gotchas

- `--assignee "Lambda"` must match a name that exists in the workspace, case-sensitive on some deployments. If a create fails with "assignee not found", run `multica agent list` first.
- An issue can be assigned to a human member instead of an agent — they look identical to the CLI; members will not auto-execute.
- `multica issue status` uses a positional value (`multica issue status <id> in_progress`), not a flag.
- `--parent <issue-id>` creates a sub-issue relationship; it is *not* the same as `--project`.
- `status done` does not prevent future edits; the issue can be reopened by transitioning back to `todo` or `in_progress`.

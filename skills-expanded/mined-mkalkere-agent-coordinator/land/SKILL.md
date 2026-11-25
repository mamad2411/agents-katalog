---
name: land
version: 1.1.0
standalone: true
description: Merge an approved PR and complete the associated task
uses:
  - development/git
requires:
  tools: [git, gh, curl]
  env: []
security:
  risk_level: write
  capabilities:
    - git:write
    - github:pr:merge
    - coordinator:write
  requires_approval: false
---

# Land

Merge an approved pull request using squash-merge, delete the feature branch, and publish a `task_completed` event to the bus. This closes the `approved -> done` lifecycle gap where approved PRs sit forever waiting for a human merge.

**Platform note**: Uses GitHub (`gh` CLI). The methodology is platform-agnostic; only the tool commands are GitHub-specific.

**Standalone mode**: Works without agent-coordinator. Skip the bus publish and coordinator task completion steps when `AC_COORDINATOR_URL` is not set. The core action — merge PR via `gh pr merge` — works with just `gh`.

## Execution Model

This is a **bash skill** (`handler: type: bash`). When `land` is invoked, the executor runs pre-merge checks and then `gh pr merge` with the provided parameters. On success it publishes a bus event to trigger the `approved -> done` workflow transition.

## When to Use

- A PR has been approved (at least one approving review, no outstanding change requests)
- The agent receives a `review_approved` bus message
- A task is in `approved` status and has a linked PR ready to merge

## Methodology

### 0. Resolve Inputs

- `pr_number` (required) — the PR to merge
- `task_id` (optional) — coordinator task ID to complete after merge
- `repo` (optional) — `owner/repo` for cross-repo merges; omit for current repo

If `repo` is provided, pass `--repo <repo>` to all `gh` commands.

### 1. Verify Merge Readiness

Before merging, confirm all preconditions are met:

```bash
# Get PR status (JSON)
gh pr view <pr_number> [--repo <repo>] --json state,reviewDecision,mergeable,statusCheckRollup,headRefName
```

Check each field:

| Field | Required Value | If Not Met |
|-------|---------------|------------|
| `state` | `OPEN` | Abort — PR is already closed or merged |
| `reviewDecision` | `APPROVED` | Abort — PR is not approved |
| `mergeable` | `MERGEABLE` | Abort — PR has merge conflicts |
| `statusCheckRollup` | All checks `SUCCESS` or `NEUTRAL`, or empty (no required checks) | Abort — CI is not green |

If any check fails, report the failure and stop. Do NOT retry — the underlying issue (conflicts, failing CI, missing approval) requires human or developer intervention.

### 2. Merge the PR

```bash
gh pr merge <pr_number> [--repo <repo>] --squash --delete-branch
```

- `--squash` produces a single clean commit on the base branch
- `--delete-branch` removes the feature branch after merge

If the merge command fails (race condition, protected branch rule, network error), capture the error message and report it. Do NOT retry.

### 3. Switch to Main

After a successful merge, switch the local checkout back to the base branch and pull the merge commit:

```bash
git checkout main && git pull
```

### 4. Publish Bus Event

After a successful merge, publish a `task_completed` event so the workflow transitions the task from `approved` to `done`:

Use the **bus_publish** tool with:
- `channel`: `"work"`
- `type`: `"task_completed"`
- `payload`:
  - `agent`: your agent name
  - `pr_number`: the merged PR number
  - `task_id`: the task ID (if provided)
  - `merge_commit`: the merge commit SHA (from `gh pr view` after merge, or `git log -1 --format=%H`)

If `task_id` is provided, also update the coordinator:

```bash
curl -s -X POST "${AC_COORDINATOR_URL:-http://localhost:9889}/tasks/${task_id}/complete" \
  -H "Content-Type: application/json" \
  -d '{"completion_state": "DONE", "summary": "PR #<pr_number> merged via squash"}'
```

### 5. Report Result

Output a summary of what happened:

```
## PR Landed

- PR: #<pr_number>
- Merge commit: <sha>
- Branch deleted: <branch_name>
- Task: <task_id> -> done (or "no task_id provided")
- Bus event: task_completed published
```

## Output Format

On success:
```
## PR Landed

- PR: #N
- Merge commit: abc1234
- Branch deleted: feat/some-feature
- Task: <task_id> -> done
- Bus event: task_completed published
```

On failure:
```
## Land Failed

- PR: #N
- Reason: <specific failure reason>
- Action needed: <what needs to happen before retry>
```

## Quality Criteria

- All preconditions are verified before attempting merge
- Squash merge is used (single clean commit on base branch)
- Feature branch is deleted after merge
- Bus event is published on success for workflow automation
- Task is marked done via coordinator API (when task_id provided)
- Failures are reported clearly with actionable next steps
- No retries on failure — report and stop

## Common Mistakes

- **Merging without checking CI**: Always verify `statusCheckRollup` before merging. A green review does not mean green CI.
- **Merging with conflicts**: Always check `mergeable` status. Conflicts require developer intervention (rebase).
- **Not publishing bus event**: Without the `task_completed` bus event, the workflow transition from `approved` to `done` does not happen and the task appears stuck.
- **Retrying on failure**: Merge failures (conflicts, CI, permissions) require human intervention. Retrying wastes cycles.
- **Forgetting --delete-branch**: Stale branches accumulate. Always clean up.

## Completion

The land skill is complete when:
- PR is merged via squash
- Feature branch is deleted
- Local checkout is on main with latest
- Bus event `task_completed` is published to `work` channel
- Coordinator task is marked done (if task_id was provided)

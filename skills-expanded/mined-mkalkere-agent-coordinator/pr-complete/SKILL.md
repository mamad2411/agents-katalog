---
name: pr-complete
version: 1.0.0
description: Notify human that PR is approved and ready to merge
uses:
  - development/git
  - coordination/ac-http
requires:
  tools: [git, gh, curl]
  env: []
security:
  risk_level: read
  capabilities:
    - git:read
    - github:pr:read
    - coordinator:write
  requires_approval: false
---

# PR Complete

**IMPORTANT: Agents do NOT merge PRs. Merging is a human-only action.**

When a PR is approved, the agent's job is to verify readiness, notify the human, and update the task status to `approved`. The human decides when and how to merge.

**Platform note**: This skill currently uses GitHub (`gh` CLI). The methodology is platform-agnostic; only the tool commands are GitHub-specific.

## Execution Model

This is a **notification skill**. The agent verifies merge readiness and publishes a notification to the bus. The human performs the actual merge.

## When to Use

- PR has been reviewed and approved
- Agent receives a `review_approved` bus message
- Task is in `approved` status and needs human attention

## Methodology

### 0. Claim Task

The task is in `approved` status with no owner (the reviewer's approval handoff released ownership).

1. Claim: `POST /tasks/{task_id}/claim` with your agent ID
2. If 409 → another agent already claimed it, skip

### 1. Verify Merge Readiness

Confirm the PR is ready for human merge:
- **Approval**: PR has at least one approval (no outstanding change requests)
- **CI**: All status checks pass (or note failures for the human)
- **Mergeable**: No merge conflicts
- **Comments**: All review comments are resolved

### 2. Notify Human

**DO NOT run `gh pr merge` or any merge command.**

Instead, publish a notification:
1. **Bus message**: `bus_publish` with `channel="work"`, `type="merge_ready"`, including `task_id`, `pr_number`, and a summary of readiness checks
2. **PR comment** (optional): Add a comment like "All checks pass. Ready for human merge."

### 3. Update Coordinator

Update the task to signal it's waiting for human action:
1. The task should already be in `approved` status from the reviewer's handoff
2. If you claimed it in step 0, keep ownership so the dashboard shows who verified readiness
3. **DO NOT move to `done`** — only the human does that after merging

### 4. Wait

Your job is done. The human will:
1. Review the PR one final time
2. Merge using their preferred method
3. Move the task to `done` via the dashboard or API

## Output Format

```
## PR Ready for Merge

- PR: [#N]
- Approval: [approved/pending]
- CI: [passing/failing — details]
- Conflicts: [none/has conflicts]
- Unresolved comments: [none/N comments]
- Action needed: Human merge
```

## Quality Criteria

- Agent NEVER runs merge commands (`gh pr merge`, `git merge`, etc.)
- PR readiness is verified before notifying
- Bus notification includes all relevant details for the human
- Task stays in `approved` status (not moved to `done`)
- Human is clearly informed that merge action is needed

## Common Mistakes

- **Merging the PR**: Agents must NEVER merge. This is the #1 rule of this skill.
- **Moving task to done**: Only the human moves to `done` after they merge.
- **Not verifying readiness**: Notifying the human about a PR that has failing CI or unresolved comments wastes their time.
- **Not publishing bus notification**: The human may not see the PR is ready without a bus message.

## Completion

This skill is complete when:
- Merge readiness is verified
- Human is notified via bus message
- Task remains in `approved` status
- Agent has NOT merged or moved task to `done`

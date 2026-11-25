---
name: ralph-loop-loop
description: Run repeated unblock cycles using ralph-loop across issue queues, then review PRs and merge safe ones until all issues are closed and all PRs are merged. Use when the user asks for ralph-loop-loop, rll, unblock loops, merge train automation, or issue-to-PR closure sweeps.
disable-model-invocation: true
---

# Ralph Loop Loop (rll)

Use this skill when the user asks for `ralph-loop-loop` or `rll`.

## Goal

Drive an unblock conveyor:
1. Solve unblock issues with `ralph-loop`.
2. Review resulting PRs.
3. Merge safe PRs immediately.
4. Flag potentially destructive merges to the user.
5. Repeat until no open unblock issues remain and all related PRs are merged or flagged.

## Operating Rules

- Never merge when destructive risk is plausible without explicit user confirmation.
- Treat destructive risk as any merge that can remove data, delete large artifacts, break production paths, or force irreversible history changes.
- If uncertain, do not merge; flag with clear risk notes and required user decision.
- Keep cycles small and verifiable: one issue/PR lane at a time unless user asks for parallel lanes.
- Preserve branch hygiene: do not use force push or destructive git commands unless user explicitly requests.

## Loop Procedure

Copy this checklist and update it as you work:

```text
RLL Progress:
- [ ] Build current queue of unblock issues and related PRs
- [ ] Pick next highest-leverage unblock issue
- [ ] Run ralph-loop to implement and verify
- [ ] Open or update PR
- [ ] Review PR for regressions and merge risk
- [ ] Merge if safe, otherwise flag user with recommendation
- [ ] Re-scan queue and repeat
- [ ] Stop only when all issues are closed and all PRs are merged or flagged
```

### Step 1: Build queue

- Collect all open issues in scope.
- Mark dependency edges (which issues are blocked by which PRs/issues).
- Prioritize by unblock impact first, then effort.

### Step 2: Execute ralph-loop

- Run `ralph-loop` for the chosen issue.
- Ensure tests/checks for touched behavior pass.
- Keep changes minimal and scoped to the issue.

### Step 3: PR review gate

For each PR before merge:
- Confirm issue linkage and acceptance criteria.
- Check for regressions, missing tests, and rollout risk.
- Classify merge risk:
  - `safe`: merge now.
  - `needs-user`: potentially destructive; do not merge.

### Step 4: Merge or flag

- If `safe`, merge and record outcome.
- If `needs-user`, report:
  - Why merge may be destructive.
  - Exact files/systems impacted.
  - Recommended options and safest next action.

### Step 5: Repeat

- Refresh issue/PR state.
- Continue until terminal state:
  - every issue closed, and
  - every PR merged or explicitly flagged for user decision.

## Output Contract Per Cycle

After each cycle, report:

```text
Cycle <N>
- Issue: <id/title>
- ralph-loop result: <done|blocked>
- PR: <url or branch>
- Review: <pass|changes requested>
- Merge decision: <merged|flagged>
- If flagged: <destructive risk reason + user decision needed>
- Remaining queue: <count/issues>
```

## Completion Criteria

Stop only when both are true:
- No open unblock issues remain in scope.
- No related open PR remains unhandled (merged or flagged to user).

---
name: github-swarm-orchestration
description: >
  Coordinates multi-agent research work through GitHub issues, branches, and PRs with explicit
  review and verifier gates. Use when running a swarm, parallel issues, orchestration log,
  feat/issue-N branches, merge order, consistency pass before merge, or Day 3-style lab workflow.
---

# GitHub Swarm Orchestration

## When to use

- User mentions: swarm, parallel agents, orchestration log, one issue one branch, Cloud Agent per issue, merge order, or `materials/day3` workflow.
- You need a **repeatable** captain loop: plan → issues → branches → PRs → review → verify → merge → follow-on issues.

## Preconditions

1. If work is spec-driven: `spec/tasks.md` should be approved (use `sdd-orchestrator` / SDD skill first).
2. Git remote exists; `gh auth status` succeeds when using GitHub CLI.

## Workflow

### 1. Choose spine

- **Spec-first:** Read `spec/tasks.md` and map checkboxes to GitHub issues (delegate drafting to `spec-tasks-to-github` skill for issue bodies).
- **Issue-first:** Use `.github/ISSUE_TEMPLATE/swarm-task.md` fields directly.

### 2. Build the issue DAG

- Label independent work `parallel`.
- Label ordered work `sequential` and add `blocked-by:<N>` for the prerequisite issue number.
- Never start a worker on a blocked issue until the blocker is merged.

### 3. Initialize or update the log

- Open `notes/orchestration_log.md`.
- Add one row per active stream/issue: branch, issue, status, PR (when opened), reviewer.

### 4. Dispatch workers

- Branch: `feat/issue-<N>-short-slug` unless the milestone declares `rig/<stream>` (then log it).
- Optional creative **worker name** for commits and PR description (per project convention).
- Use handoff files `notes/handoff_<from>_to_<to>.md` when streams consume each other's outputs.

### 5. Review gate

- Invoke **`pr-reviewer`** subagent on each PR (readonly review first; then apply fixes on the branch).
- If labels include `domain:*`, invoke the matching domain reviewer agent.

### 6. Verifier gate

- **`replication-verifier`:** when replication paths, deps, or run instructions change.
- **`artifact-coherence-auditor`:** when paper text, tables/figures, and replication must agree.

### 7. Merge gate

- **`integration-coordinator`** (or human): enforce dependency order, rebase if needed, resolve conflicts.
- **Automerge** only if issue has `automerge-ok` and CI + review requirements are satisfied.

### 8. Follow-on work

- Verifier blockers → **open new issues** linked from the audit; do not silently expand an already-approved PR scope.

## Guardrails

- Follow `.cursor/rules/research-reproducibility.mdc`: relative paths, traceable outputs.
- Keep `notes/orchestration_log.md` the durable state mirror alongside GitHub.
- See `reference.md` in this folder for labels, `gh` snippets, and phase detail.

## Output

At end of each captain iteration, report:

- Updated issue/PR links
- Current `notes/orchestration_log.md` row states
- Pending blockers and next merge order

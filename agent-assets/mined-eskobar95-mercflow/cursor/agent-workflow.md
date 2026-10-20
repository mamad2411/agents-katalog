---
description: Agent pipeline rules — worktrees, branches, reviews, PRs, Bugbot, CI
globs:
alwaysApply: true
---

# Agent Workflow — MercFlow pipeline rules

Every task, regardless of agent type (Cloud / CLI / Manual), follows this pipeline without exception.

## The six stages

```
Not Started → [Setup] → In Progress → [Code Review] → In Review → [Bugbot + CI] → Done
```

| Stage | Who | Status in Notion |
|---|---|---|
| 1. Setup + worktree | Any agent | Not Started → In Progress |
| 2. Implementation | Worker Agent | In Progress |
| 3. Code Review loop | Code Reviewer | In Progress (until approved) |
| 4. Open PR | Any agent | In Progress → In Review |
| 5. Bugbot + CI | Bugbot (auto) + DevOps Agent | In Review |
| 6. Merge + cleanup | Human | In Review → Done |

## Non-negotiable rules

### Worktrees
- Every task gets its own git worktree at `../mercflow-worktrees/{task-id}/`
- Never work directly on `main` or `develop`
- Branch naming: `feature/{package}/{task-slug}`
- Maximum one task per worktree

### Code Review
- Code Reviewer runs **before** a PR is opened — not after
- Maximum 3 review cycles; escalate to human at cycle 3
- Bugbot is **not** a substitute for the Code Review loop — they serve different stages

### Bugbot
- Bugbot activates only when a PR is **open** (Stage 5)
- Do not trigger Bugbot during development or the review loop
- Bugbot flags are evaluated: real bugs get fixed, false positives get documented

### CI
- Never skip or disable failing tests to make CI green
- A CI failure is either: flaky (retry + document) or real (create bug task in Notion)
- All checks must pass before merge

### PR summary
- Every PR must use the standard MercFlow PR summary template (see agent-workflow/SKILL.md)
- PR URL must be copied to the Notion task's `PR URL` field
- PR title format: `{Slice objective} ({package})`

## Commands
- `/start-task <notion-url>` — setup + begin implementation
- `/review-code <branch>` — run Code Reviewer
- `/open-pr <branch>` — open PR after review approval
- `/devops-check [pr-url]` — diagnose CI or proactive audit

## Full pipeline detail
See `.cursor/skills/agent-workflow/SKILL.md`

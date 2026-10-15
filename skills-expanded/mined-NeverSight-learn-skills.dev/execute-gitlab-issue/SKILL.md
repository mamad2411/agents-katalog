---
name: execute-gitlab-issue
description: (NS) Execute a GitLab issue end-to-end — worktrees, implementation, atomic commits, MRs, MCP status sync, mandatory code review gate. Use when the user provides a GitLab ISSUE_URL or asks to implement a GitLab issue directly — not for local-only ad-hoc coding (use coder). Requires mcp-gitlab-usage for MCP and code-reviewer for Phase 5 gate.
depends:
  - nextstage-harness
  - mcp-gitlab-usage
  - code-reviewer
---

# Execute GitLab Issue

From issue URL to delivery with review gate.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md`. Read `mcp-gitlab-usage` before MCP calls.

## Inputs

| Variable         | Required                            |
| ---------------- | ----------------------------------- |
| `ISSUE_URL`      | Yes                                 |
| `SOURCE_BRANCH`  | No — Gate 1 if omitted              |
| `{product_root}` | When multiple products in workspace |

`WORKTREE_ROOT = {product_root}/.worktrees/{ISSUE_ID}`

## Phase 0 — Context

1. Resolve `{product_root}` (factory: `apps/{slug}/`; standalone: repo root)
2. Discover git repos under `{product_root}` (`backend/`, `frontend/`, meta-repo root, etc.)
3. Load product context: follow **Implementation boot rule** in `../nextstage-harness/references/artifact-layout.md`
4. Ensure `.worktrees/` in gitignore

## Phase 1 — Prepare

### Gate 1 — Source branch

Confirm `SOURCE_BRANCH` with human if not provided. `git fetch origin` on affected repos.

### Issue identifiers

- `ISSUE_ID` from URL
- `ISSUE_SLUG` from title (ASCII, kebab, max 40 chars)
- `WORK_BRANCH = work/{ISSUE_ID}-{ISSUE_SLUG}`

### Gate 1.5 — Worktree planning

One worktree per affected repo. Abort if same issue worktree in use by another agent (unless explicit resume).

### MCP setup

- Label `Status: In progress` (per `gitlab-sync-config.md`)
- `due_date` if empty: +5 business days
- `START_TIME` UTC ISO

## Phase 2 — Execution

1. Full issue payload via MCP
2. Hidden atomic subtask plan; TDD when applicable
3. **`AFFECTED_PROJECTS`** — only repos that receive code (no empty MR repos)
4. Per repo: worktree add, push branch, draft MR via MCP
5. `set_issue_estimate` on issue
6. Implement in worktrees — load layer rules from harness

See `references/worktree-setup.md` and `references/mr-conventions.md`.

## Phase 3 — Pre-commit self-check

Review 100% of changed code; fix critical/warning before commit.

## Phase 4 — Delivery

### Commit (per repo with changes)

See `../nextstage-harness/references/agent-git-identity.md` when attributing commits.

```
<type>(#{ISSUE_ID}): <imperative description in English>
```

Types: feat, fix, refactor, test, docs, chore. One commit per repo.

### MCP post-delivery

1. `add_issue_spent_time` from START_TIME to END_TIME
2. Status → done label per config
3. Internal summary comment (`internal: true`)

## Phase 5 — Code review gate (blocking)

Invoke `code-reviewer` in **Issue review mode** with `ISSUE_URL`. If the harness supports running isolated personas, prefer `.agents/agents/code-reviewer.md` for this gate; otherwise invoke the skill inline.

Workflow does not finish without verdict: `Approved` | `Rejected` | `Blocked`.

## Stop and ask the human

| Condition                                                 | Action                        |
| --------------------------------------------------------- | ----------------------------- |
| Gate 1: `SOURCE_BRANCH` missing/invalid after fetch       | Stop — ask once               |
| Worktree conflict (same issue, another agent)             | Stop unless explicit resume   |
| Ambiguous or conflicting acceptance criteria              | Stop — ask once               |
| MCP unavailable or auth failure                           | Stop — state blocker          |
| `project_id` trio not confirmed                           | Stop per `mcp-gitlab-usage`   |
| Work on protected/base branch per `gitlab-sync-config.md` | Stop                          |
| Destructive ops (issue delete, force-push main/master)    | Stop — require explicit human |
| Product decision not stated in the issue                  | Stop — ask once               |

See `mcp-gitlab-usage` for MCP tool contracts and confirmation gates.

## Related skills

| Skill               | Role                    |
| ------------------- | ----------------------- |
| `mcp-gitlab-usage`  | All GitLab tools        |
| `gitlab-board-sync` | Status label semantics  |
| `code-reviewer`     | Phase 5 gate            |
| `coder`             | Implementation patterns |

## References

| File                           | When                     |
| ------------------------------ | ------------------------ |
| `references/worktree-setup.md` | Multi-repo worktrees     |
| `references/mr-conventions.md` | MR title, draft, linking |

---
name: code-autonomous
description: (NS) Harness-aware autonomous execution engine — self-decides planning depth, resolves doubts against docs/context and docs/specs before escalating, dispatches multi-agent implementation in an isolated worktree. Use as the standalone entry point for a local plan file, a pasted execution plan, or an ad-hoc "run this autonomously" request with no GitLab issue involved. Also acts as the Phase 2 execution engine when invoked by execute-gitlab-issue — do not run the standalone pipeline in that case. Not for simple single-step edits (use code-coder) and not for GitLab issues directly (use execute-gitlab-issue, which calls this skill internally).
depends:
  - nextstage-harness
  - code-reviewer
---

# Code Autonomous

Harness-aware execution engine: decides planning depth, resolves doubts, dispatches multi-agent work, and closes the loop with a review gate — either as a standalone pipeline or as another skill's execution engine.

## Isolation invariant (non-negotiable)

This skill **never** writes application code on the main product checkout, and **never** commits to `main`/`master` (or any base/`SOURCE_BRANCH`), unless the human has explicitly instructed "do not create a new branch / work in place on the current branch" for this run.

- Standalone and Engine mode both require an isolated `WORK_BRANCH` + `WORKTREE_ROOT` before any implementation edit.
- If worktree creation fails, or CWD/branch is still the main checkout / base branch → **stop**. Do not "continue on main to unlock the plan".
- Sandbox restrictions (`Operation not permitted`, Cursor agent runtime paths under `.cursor/`) are **not** permission to violate this invariant.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md`.

## Routing (read first)

1. **Origin is a GitLab issue** (`ISSUE_URL` or issue reference) → follow `execute-gitlab-issue` end to end; this skill only runs as its Phase 2 engine (**Engine mode** below). Do not run the standalone pipeline, do not touch GitLab state, do not create a worktree.
2. **Otherwise** (local plan file, pasted text/plan, ad-hoc autonomous request without an issue) → run the **standalone pipeline**: own worktree, own state, own review loop.

See `references/routing.md` for the full decision detail and the Engine-mode input/output contract.

## Engine mode (invoked by `execute-gitlab-issue`)

Inputs (already resolved by the caller — this skill never creates them): issue payload, `{product_root}`, `WORKTREE_ROOT`, `WORK_BRANCH`, `SOURCE_BRANCH`.

1. **Planning-depth self-decision** — evaluate the issue payload and decide single work unit vs. light `requirements.md` + `tasks/task-NNN-*.md` + `execution-plan.md` under `docs/versions/{version_san}/`. See `references/planning-decision.md`.
2. **Doubt protocol** — self-ask, docs-first lookup, self-answer non-destructive doubts, escalate destructive ones as a structured event to the caller instead of mutating GitLab state; pause dependent units until resumed. See `references/doubt-resolution.md`.
3. **Multi-agent dispatch** — parse work units (or the single unit) and dispatch `code-coder` subagents, parallel only across units with no DAG edge and disjoint file scopes, sequential otherwise. Every subagent works inside `WORKTREE_ROOT`, never the main checkout. See `references/multi-agent-dispatch.md`.
4. **Checkpoint commits** — one commit per completed sequential unit or per completed parallel batch, inside the worktree; the caller squashes at delivery.
5. **Fix-loop entry point** — when re-invoked after a `Rejected` verdict, treat the reviewer findings as a new work unit (or units) and repeat step 3 for those only.
6. **Return to caller**: unit statuses, files changed, any open destructive doubt, and (first invocation only) a plan-based time estimate for `set_issue_estimate`.

## Standalone pipeline (non-GitLab origin)

Same internals as Engine mode, but this skill owns the whole run:

1. Resolve the descriptor — local plan path or pasted text. No MCP calls.
2. Infer `change_kind` (fix/feat), allocate `{version_san}`, create `docs/versions/{version_san}/`.
3. **Create its own worktree**: `{product_root}/.worktrees/{version_san}/` + branch `work/{version_san}` from the resolved base branch, following `../nextstage-harness/references/worktree-setup.md`. Path is under the **product root**, never under `.cursor/`. On failure → abort (do not fall back to the main checkout) — see `references/standalone-pipeline.md`.
4. Planning-depth self-decision, doubt protocol (destructive doubt → chat-only gate, no GitLab actions available), multi-agent dispatch — identical logic to Engine mode.
5. **Internal review loop** — invoke `code-reviewer` (version-closure mode), max 3 rounds: fix units on `Rejected`, stop on `Blocked` or rounds exhausted.
6. Report `{version_san}`, worktree path, commit(s), review verdict, and any follow-ups. No GitLab board, no MR — unless `docs/context/gitlab-sync-config.md` exists and the human explicitly asked for one (out of scope for v1; standalone stays local-only otherwise).

See `references/standalone-pipeline.md` for the full flow.

## Stop and ask the human

| Condition                                                        | Action                                              |
| ------------------------------------------------------------------ | ---------------------------------------------------- |
| Destructive doubt (Engine mode)                                   | Return escalation event to caller — no chat pause here |
| Destructive doubt (standalone)                                    | Stop in chat, ask, resume with the answer as context |
| Worktree conflict for the same `{run_id}` (standalone)             | Stop unless explicit resume                          |
| `git worktree add` failed (permissions/sandbox/path)               | Abort — report path attempted; never fall back to main checkout or `.cursor/` |
| Still on `main`/`master`/base branch when about to edit code       | Abort — isolation missing; do not implement                                   |
| Human explicitly said "do not create a new branch / work in place" | Only then may edit the current branch; still never invent a `.cursor/` path |
| Base branch for standalone worktree unresolved                    | Stop — ask once                                      |
| Review `Blocked` or 3 rounds exhausted                             | Stop, report as blocked — do not fabricate success   |
| Engine mode invoked with a GitLab origin but no worktree/branch given | Stop — this is a caller contract violation, not a doubt |

## Related skills

| Skill                 | Role                                                       |
| ---------------------- | ------------------------------------------------------------ |
| `execute-gitlab-issue` | GitLab flow owner — calls this skill for Phase 2             |
| `code-coder`           | Subagent implementation pattern used per work unit            |
| `code-reviewer`        | Review gate (issue mode via caller, version-closure mode standalone) |
| `nextstage-harness`    | Artifact layout, worktree mechanics, discovery               |

## References

| File                                | When                                                                |
| ------------------------------------ | --------------------------------------------------------------------- |
| `references/routing.md`              | Issue vs. standalone decision; Engine-mode I/O contract with `execute-gitlab-issue` |
| `references/planning-decision.md`    | Self-evaluation heuristic: single unit vs. requirements+tasks+plan  |
| `references/doubt-resolution.md`     | Self-ask, docs-first lookup, destructive criteria, escalation shape |
| `references/multi-agent-dispatch.md` | DAG + disjoint-scope parallel rule, subagent prompt, checkpoint commits |
| `references/standalone-pipeline.md`  | Full non-GitLab flow: version alloc, own worktree, review loop      |

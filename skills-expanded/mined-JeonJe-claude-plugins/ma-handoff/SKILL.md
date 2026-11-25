---
name: ma-handoff
description: 승인된 impl 스코프를 대상 프로젝트 워크트리로 인계한다. 브랜치 검증, 충돌 없는 워크트리 생성, setup 실행, PLAN/HANDOFF 작성. "ma-handoff", "핸드오프", "워크트리 인계" 요청 또는 MA Phase 3에서 사용.
---

# /ma-handoff

Run handoff only for approved impl tickets. PRD/design/review remain workspace SSOTs; handoff moves only PLAN (plus HANDOFF.md) into the implementation repo.

This is a procedural skill: execute the steps below directly with git and shell commands. A deterministic execution engine is not included in v1 — verify each step's stated condition yourself before proceeding.

## Args

```text
/ma-handoff --key <ISSUE_KEY> --project <PROJECT_KEY> [--resume] [--dry-run]
```

- key: required, matching the configured `issueKeyPattern` (e.g. `PROJ-123`)
- project: required (workspace config project key)
- `--resume`: continue from a previous incomplete run
- `--dry-run`: validate intent and plan without mutating filesystem/repo

## References index

| File | When to read |
|---|---|
| [config/branch-naming.md](config/branch-naming.md) | Step 2 — branch/worktree decision rules |
| [config/setup-interview.md](config/setup-interview.md) | Step 3 — setup collection and failure policy |
| [templates/handoff-doc.md](templates/handoff-doc.md) | Step 4 — HANDOFF/PLAN format |

## Workflow

1. **Validate the contract.** Scope is `impl` (per the ma skill's scope gate (`../ma/references/scope-gate.md`)); `gates.implementationApproval.status == "approved"` in `{stateRoot}/{key}/state.json`; the approval records this project with `base`, `target`, and — when the project defines modules — `primaryModule` and `affectedModules`; plan review passed; base/target are valid branch names. Any missing element halts with the exact missing field.
2. **Resolve refs and the worktree path** per `config/branch-naming.md`. Run `git fetch origin` in the target repo and branch from the tip of `origin/{base}`, never from a stale local branch. A local base holding commits absent from origin is a conflict to report, not something to discard silently. Then:
   ```bash
   git -C {projectPath} branch {target} origin/{base}
   git -C {projectPath} worktree add {worktreePath} {target}
   ```
3. **Run setup commands** collected per `config/setup-interview.md`, only from the workspace config (`setup` of module dependencies first, then the primary/affected modules, then project-level). Record per-command cwd/status/exit code. Any failure leaves the phase incomplete but resumable.
4. **Package PLAN and write HANDOFF** per `templates/handoff-doc.md`: move the approved PLAN from `{contextRoot}/{domain}/plan/{key}-{project}.md` to `{worktreePath}/{docsPath}/{key}/PLAN.md` (the worktree becomes PLAN SSOT; remove the original), write `{worktreePath}/HANDOFF.md`, and append the audit log at `{contextRoot}/{domain}/handoff/{key}.md`.
5. **Record state.** Update `{stateRoot}/{key}/state.json` `worktrees[project]` with `path`, `base`, `target`, `baseCommit`, and `planPath`. Report success with those values, or the failed step with its recovery action.

## Safety constraints

- Never run checkout/reset/stash/pull on the project's main checkout; the only mutation there is `git fetch` + branch/worktree creation.
- Base/target branches require the recorded approval; never invent them.
- The target repo's main checkout must have no uncommitted changes that the worktree creation would disturb.
- `--resume` only reuses the exact recorded project/path/base/target intent; a mismatch is a conflict, not a silent overwrite.
- Do nothing beyond worktree + setup + PLAN/HANDOFF writes.

## Linked skills

- Post-handoff implementation: `/ma-dispatch`
- Code review: `/ma-review`
- Post-merge cleanup: remove the worktree and delete the local branch after the MR merges (see the `ma` skill, Phase 9).

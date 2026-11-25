---
name: ma-review
description: ma 산출물을 구현 전 plan 리뷰 또는 MR 전 code 리뷰로 검증한다. plan 모드는 PRD·design·프로젝트별 PLAN의 정합성·보안·정책·실행 가능성을 검토하고, code 모드는 worktree diff를 PLAN·AC·dispatch 증적과 대조한다. "ma-review", "ma 계획 리뷰", "ma 설계 검토", "ma 코드 리뷰", "팀 리뷰" 요청에 사용. 일반 단일 파일 리뷰나 비-MA 계획 검토에는 사용하지 않으며, 코드 수정은 사용자가 명시적으로 반영을 요청한 경우에만 `/ma-dispatch`로 수행한다.
---

# /ma-review

Run an evidence-backed review of MA artifacts. Load only the selected mode; plan and code have different inputs, mutation boundaries, and completion gates.

## Invocation

```text
/ma-review <issue-key> [plan|code] [--project=<project>] [--auto-apply]
```

| Input | Action | Output |
|---|---|---|
| `/ma-review PROJ-123 plan` | Review PRD/design/all target PLANs before implementation | `{stateRoot}/PROJ-123/review-plan.md` |
| `/ma-review PROJ-123 code --project=example-backend` | Review the worktree diff against contracts and evidence | `{stateRoot}/PROJ-123/review-result.md` |
| `/ma-review PROJ-123` | Infer from artifacts and worktree state; ask once if ambiguous | One mode-specific report |

## Resolve the mode

1. Use explicit `plan` or `code` when provided.
2. Choose `code` when a target worktree has implementation diff plus HANDOFF/PLAN/dispatch evidence.
3. Choose `plan` when PRD/design/temporary PLANs exist and implementation evidence does not.
4. Ask once if both or neither condition is decisive. Never review code under plan scope or mutate code while resolving the mode.

## Load only the selected workflow

- `plan`: read `references/modes/plan.md` and `checklists/artifact-consistency.md`.
- `code`: read `references/modes/code.md`, then load extraction/verification/output and conditional fallback checklists named there.

## References index

| File | When to read |
|---|---|
| [references/modes/plan.md](references/modes/plan.md) | Plan mode — full workflow |
| [references/modes/code.md](references/modes/code.md) | Code mode — full workflow |
| [checklists/artifact-consistency.md](checklists/artifact-consistency.md) | Plan mode — mechanical consistency pass before qualitative review |
| [checklists/extraction.md](checklists/extraction.md) | Code mode — shared context/AC extraction |
| [checklists/verification.md](checklists/verification.md) | Code mode — finding verification pass |
| [checklists/output-format.md](checklists/output-format.md) | Code mode — `review-result.md` format |
| [checklists/code-fallback.md](checklists/code-fallback.md) | Code mode — no dedicated code-risk reviewer available |
| [checklists/cross-project.md](checklists/cross-project.md) | Code mode — multiple projects or a cross-project contract changed |
| [agents/architect.md](agents/architect.md) | Code mode — contract/architecture review lane |
| [agents/qa-manager.md](agents/qa-manager.md) | Code mode — acceptance/scenario review lane |

Role dirs: `modes/` = per-mode review workflows; `checklists/` = reviewer checklists; `agents/` = reviewer lane definitions. Reviewer role names (`architect`, `qa-manager`, `design-critic`, `security-auditor`, `policy-guardian`, `executor`) map to your agent roster or run inline.

## Shared gates

- Read the ma skill's scope gate (`../ma/references/scope-gate.md`). Plan mode terminates at `plan-review`; code mode requires an existing `impl` worktree.
- Base every finding on a document location, code location, or execution artifact. Unverified suspicions remain out of the main report.
- `--auto-apply` applies only to plan-mode, semantics-preserving documentation repairs allowed by `references/modes/plan.md`. It never approves direction changes or edits product code.
- Count only unresolved confirmed findings in the final machine-parsed severity line. Keep detected and resolved counts separately for audit history.
- Before emitting `[COMPLETE]`, verify the report structure yourself (a deterministic validator is not included in v1): required sections present, severity-count line in the exact fixed format, and — for code mode — all three lenses merged into the count. Structurally valid but with unresolved CRITICAL findings → `[BLOCKED]`.

## Outputs

- Plan: `{stateRoot}/{key}/review-plan.md`
- Code: `{stateRoot}/{key}/review-result.md`

Return `[BLOCKED]` with the report path and next decision/fix when the selected workflow's gate is not satisfied.

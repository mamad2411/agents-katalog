---
name: eliteforge-codex-superpower
description: Lean AC-only Codex workflow for EliteForge feature delivery. Activate ONLY when user explicitly requests this skill or project declares 璀璨工坊规范/eliteforge specification with feature design, database/API contracts, TDD execution, or selective multi-agent delivery needs.
---

# EliteForge Codex Superpower

## Activation Gate

Use this skill only when:
- User explicitly asks to use `eliteforge-codex-superpower`
- Project/request states `璀璨工坊规范` or `eliteforge specification` with feature delivery, database/API design, TDD-first execution, or selective multi-agent work

Otherwise handle with general capabilities.

## Environment Variables

- `ELITEFORGE_SKILL_SUPERPOWER_TDD_AGENT` [optional] Codex runtime `spawn_agent.agent_type` for bounded AC TDD slice workers; defaults to `ELITEFORGE_SKILL_SUPERPOWER_CODING_AGENT`, then `worker`.
- `ELITEFORGE_SKILL_SUPERPOWER_CODING_AGENT` [optional] Codex runtime `spawn_agent.agent_type` for coding subagents such as backend/frontend/database implementation, verify, and review workers; defaults to `worker`.

## Codex Runtime Agent Selection

Environment variable values are Codex runtime agent types passed to `spawn_agent.agent_type`, not workflow role names. Valid values must come from currently available Codex agent types such as `worker`, `explorer`, `coder`, or `coder-spark`.

Resolve runtime agent types before every `spawn_agent` call:

- TDD slice workers: `ELITEFORGE_SKILL_SUPERPOWER_TDD_AGENT` -> legacy alias `ELITEFORGE_SKILL_TDD_AGENT` -> `ELITEFORGE_SKILL_SUPERPOWER_CODING_AGENT` -> `worker`.
- Backend, frontend, database, verify, review: `ELITEFORGE_SKILL_SUPERPOWER_CODING_AGENT` -> `worker`.
- Explorer: always `explorer`.

If resolution returns `coder-spark`, call `spawn_agent` with `agent_type: "coder-spark"`. Do not omit `agent_type`, do not replace it with a workflow role, and do not use `fork_context: true` with an explicit `agent_type`; pass a focused prompt with required AC rows, command aliases, write scope, and worktree context instead.

Workflow roles such as `tdd-slice-worker`, `backend-worker`, `frontend-worker`, `database-worker`, and `review-worker` belong only in task ownership, prompts, worktree plans, branches, and report filenames. They are never Codex runtime `agent_type` values.

## Workflow Nature

Default model:
```
lead agent -> feature model -> AC index -> proof rows + command index -> AC task rows -> AC evidence rows
```

This skill is AC-only across documents. The only global business traceability ID is `AC-*`. Do not create global `INT-*`, `TDD-*`, `TASK-*`, `EV-*`, or `BVE-*` IDs. Page interactions, TDD cases, tasks, and browser evidence are fields under the owning AC row.

## Execution Modes

- `solo`: explicit fallback only. Lead handles docs, coding, validation, and evidence for a small bounded AC slice on the selected-git-spec main/base branch after recording the reason.
- `hybrid`: default. Lead owns docs, integration, and final judgment; behavior-changing AC slices should use one `tdd-slice-worker` unless the user explicitly approves solo or the slice is documentation-only/trivial.
- `parallel`: use multiple workers only when contracts are stable, write scopes are disjoint, and splitting reduces wall-clock time.

Default task unit: one bounded AC slice with `phase: tdd`, covering RED -> GREEN -> focused VERIFY. Do not split RED worker, GREEN worker, and review worker by ceremony. Split backend/frontend/database workers only for real fan-out.

Base branch rule: selected-git-spec main/base branch creation is mandatory before behavior-changing execution. `solo` means no delegated worker, not "work directly on the original checkout." Even solo execution must happen from the selected-git-spec main/base branch and be recorded in `orchestration/worktree-plan.md`.

Dispatch decision rule: every behavior-changing task row (`phase: tdd|red|green|refactor`) must have a row in `orchestration/worktree-plan.md#Dispatch Decisions`.

Decision order:
1. If the row is documentation-only, exploration, support, integration, review, or verify-only, do not spawn for implementation.
2. If the user explicitly approved solo or the row is genuinely trivial, choose `solo` and record the approval/trivial rationale.
3. If subagents are unavailable or git worktree setup is blocked, choose `blocked` and stop for user decision.
4. If contracts are stable, write scopes are isolated, and splitting reduces wall-clock, choose `parallel`.
5. Otherwise choose `spawn`; default `hybrid` means one bounded AC implementation worker owns RED -> GREEN -> focused VERIFY.

Grouping: do not mechanically spawn one worker per AC when adjacent AC rows share the same files, command aliases, and interaction surface. One spawned worker may own multiple tightly coupled AC rows if the prompt remains bounded. Do not group AC rows that require disjoint backend/frontend/database fan-out, unrelated files, or independent browser flows.

## Single Source Of Truth

- Feature model and boundary: `spec/feature-spec.md`; no `AC-*`, commands, RED/GREEN, or evidence.
- Acceptance index: `spec/acceptance.md`; the only file that defines `AC-*`.
- Proof plan: `spec/test-plan.md`; proof rows by `AC-*` plus local `CMD-*` command aliases.
- Task rows: `tasks/*.md`; execution slices by `AC-*`, usually `phase: tdd`.
- Runtime/process state: `orchestration/*.md`; `worktree-plan.md` records the mandatory selected-git-spec main/base branch, and `context-index.md` provides navigation.
- Evidence ledgers: `reports/*.md`; RED/GREEN/VERIFY/browser evidence by `AC-*`.

All documents other than the owner file reference facts using `AC-*`, local `CMD-*`, or `@ref:<relative-file>#<anchor>`. Do not duplicate expanded facts across files.

## Context Budget

- Generate or refresh `orchestration/context-index.md` before dispatch, review, or final validation.
- Read `context-index.md` first, then open only the needed file, heading, and AC row.
- Worker prompts include only relevant AC rows, command aliases, write scope, and referenced sections. Do not paste whole `spec/`, `tasks/`, or `reports/`.
- Reports and worker fragments keep deltas and evidence only; they must not restate feature requirements, AC prose, or page design.

## External Browser Skill Compatibility

External browser/testing skills, including `webapp-testing`, are capability providers only. Do not edit or depend on their EliteForge document contract if it conflicts with this skill.

When delegating browser work, the lead prompt must provide the AC-only contract explicitly:
- Inputs: assigned `AC-*` rows, matching proof rows, `CMD-*` command aliases, route/surface references, and write scope.
- Output: `reports/*.md` evidence rows keyed by `AC-*`.
- Browser evidence fields: clicks, inputs, network assertions, visible feedback, and artifacts.
- Forbidden outputs: `test-scope.md`, global `TDD-*`, `TASK-*`, `INT-*`, `EV-*`, or `BVE-*` IDs.

Use external browser skills for Playwright technique, server lifecycle, selector discovery, screenshots, traces, and logs. This skill remains the source of truth for document names, IDs, report shape, and validation.

## Workspace Contract

Use `docs/features/<feature-slug>/` with `spec/`, `tasks/`, `orchestration/`, and `reports/`. Use `assets/` templates. Derive `<feature-slug>` from product feature name (lowercase kebab-case). Do not derive branch names, worktree paths, or agent names from this skill.

Before any behavior-changing execution, select the active git skill:
- `eliteforge-git-feature-oriented-spec` (full spec)
- `eliteforge-git-feature-oriented-lite-spec` (lite spec)
- If undeclared, stop and ask user

Use the chosen git skill as the only source for main branch, worktree path, multi-agent base, subagent branch, `agentId`, and `subtaskName`. Create or verify the selected-git-spec main/base branch before implementation, even when no worker is spawned. Record Codex runtime id separately in `worktree-plan.md`.

If files exist, preserve decisions and update in place.

## Workflow Selection

**New Feature Delivery**: no existing feature workspace, starting new feature 0-1.

**Feature Evolution**: changing, refactoring, extending, narrowing, or reopening existing workspace. Re-enter gates from earliest affected design point.

Both share the same AC-only documents, validators, git-spec constraints, context-index rule, and execution-mode rules.

## Non-Negotiable Rules

1. **Draft before interrogation.** Produce an opinionated draft first. Ask 3-5 blocking questions per round only after a draft exists.
2. **Keep AC-only traceability.** `AC-*` is the only global business ID across documents.
3. **Keep feature spec clean.** `spec/feature-spec.md` must not contain `AC-*`, `TDD-*`, commands, RED/GREEN, browser evidence, or execution logs.
4. **Define ACs once.** `spec/acceptance.md` owns all `AC-*`; each AC is one compact completion judgment line.
5. **Use proof rows, not global TDD IDs.** `spec/test-plan.md` proves ACs with `case`, `red`, `green`, optional `interaction`, and `command_ref`.
6. **Centralize commands.** `CMD-*` aliases live only in `spec/test-plan.md#command-index`; slow/browser commands require cost and rerun policy.
7. **Spec interactions as AC fields.** UI interactions are represented by interaction ACs and `interaction:` proof fields, not separate `INT-*` files or IDs.
8. **Require concrete browser evidence.** Browser evidence must list clicks, inputs, network assertions, visible feedback, and artifacts. `smoke passed` is not evidence.
9. **Prefer bounded AC slices.** Default `phase: tdd` task rows cover RED -> GREEN -> VERIFY for one AC slice.
10. **Do not default to solo.** Default execution is `hybrid`; solo requires explicit user approval or a recorded docs-only/trivial rationale.
11. **Spawn for benefit, not ceremony.** Use one `tdd-slice-worker` for behavior-changing AC slices when tool support is available; add more workers only for real parallelism, isolation, or long-running execution value.
12. **Keep lead/worker roles explicit.** Lead owns gates, integration, review, and completion claims. Workers own assigned AC slices only.
13. **Respect command cost.** REVIEW reuses slow/browser VERIFY evidence unless missing, failed, stale, or explicitly requested.
14. **Treat external browser skills as tools.** Do not edit external skills or inherit legacy EliteForge output contracts from them; the lead prompt must enforce this skill's AC-only browser evidence shape.
15. **Separate git identity from Codex runtime.** `agentId` and `subtaskName` come from the git skill; Codex runtime ids come from `spawn_agent`.
16. **Create base branch before execution.** `orchestration/worktree-plan.md` must record resolved main branch, main worktree path, and multi-agent base branch before implementation.
17. **No worker edits lead/root worktree.** Delegated workers use selected-git-spec worktrees; approved solo execution uses the selected-git-spec main/base branch and must be recorded in tasks/reports.
18. **RED before GREEN.** Every behavior-changing AC slice needs RED failure evidence before GREEN evidence.
19. **Do not silently steal live worker scope.** If a worker owns an AC slice, lead must not duplicate it without recording the decision.
20. **Do not infer stalls from time.** A running subagent remains `in_progress` unless platform failure, empty completion, user interruption, or approved timebox breach occurs.
21. **Do not hide execution gaps.** If subagents are unavailable, shared-file races appear, or evolution invalidates artifacts, record the blocker and stop for user decision.

## Reference Index

Load references only when needed:

| need | reference |
| --- | --- |
| New feature delivery workflow | `references/zero-one-delivery.md` |
| Existing feature evolution workflow | `references/feature-evolution.md` |
| TDD quality rules | `references/tdd-workflow.md` |
| Execution modes and worker prompts | `references/subagent-orchestration.md` |
| Worktree setup and integration | selected git skill, then `references/git-worktree-orchestration.md` |
| Database design guidance | `references/database-design.md` |

## Completion Gate

Complete only when: active validation passes, reached gates have approved or approved-with-defaults decisions, every `AC-*` has proof rows, task rows, and final evidence rows, browser evidence is concrete when UI/browser is claimed, slow/browser reruns follow policy, and unresolved blockers are recorded.

Feature Evolution additionally requires: change classification, downstream impact analysis, affected-gate validation, stale artifact status, and old/new AC evidence migration.

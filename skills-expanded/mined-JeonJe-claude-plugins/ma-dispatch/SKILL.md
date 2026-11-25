---
name: ma-dispatch
description: MA impl 승인 뒤 등록된 worktree에 구현을 위임한다. "ma-dispatch", "구현 위임", "디스패치" 요청 또는 MA Phase 4에서 사용.
---

# /ma-dispatch

Canonical form: `/ma-dispatch <ISSUE_KEY> --project=<project> [--project=<project> ...]`.
`/ma --auto` without selection selects every approved project. A selected set must exactly be a subset of the approved project names; a path is evidence only, never authority.

**Entry scope** (the ma skill's scope gate (`../ma/references/scope-gate.md`)): `scope` must be exactly `impl` and implementation approval must be exactly `approved`. Existing implementation reconciliation is decided in scope-gate §5; do not reimplement validated work.

Before any worktree access, validate the key against the configured `issueKeyPattern` and validate project names, then read state. Check approved project/base/target equals each canonical `state.worktrees[project]`; reject unknown, duplicate, or unselected paths. The parent creates `phaseResults["4"].targets[project]` and allocates its absolute `.claude/dispatch` result/log paths (inside the worktree) before dispatch. Workers never write orchestrator state.

Target state is (every active worktree also records an absolute existing `planPath` inside that worktree):

```json
{"baselineHead":"sha","status":"DONE_OK","attempts":[{"n":1,"mode":"plan-exec","status":"DONE_OK","startHead":"sha","endHead":"sha","result":"/abs/.claude/dispatch/run.result.json","log":"/abs/.claude/dispatch/run.log.md"}]}
```

Read `references/delegation-discipline.md` before composing any brief. Load `prompts/executor-prelude.md`, then the selected mode from `prompts/templates.md`. Use your workspace's executor agent (an agent role that implements with surgical changes and runs verification; run inline only if no such agent exists) with the target worktree as cwd. Its return is the short block plus the result JSON defined only in that prelude. `plan-exec` succeeds only with a new commit and exact final PLAN step coverage; `review-fix`/`generic` may say `NO_OP` explicitly.

On completion, verify each target's result yourself (a deterministic validator is not included in v1): the result JSON parses, matches the prelude schema, `startHead`/`endHead` are real commits in the worktree, `planSteps` exactly match the final PLAN headings, every verification is `PASS` for `DONE_OK`, and the log contains the embedded result comment. Only all-`DONE_OK` targets advance. Route `DONE_FAILED`, `INVALID_RESULT`, `TIMEOUT`, and `SESSION_DIED` separately. Retry only non-success targets, append attempts, and retain the original target `baselineHead`; never rerun a successful target. On a retry, set the executor's `priorLog` to the previous attempt's `log` so its deviations and PLAN corrections carry forward.

## References index

| File | When to read |
|---|---|
| [references/delegation-discipline.md](references/delegation-discipline.md) | Before composing any dispatch brief — 2-phase gate, mirror+delta framing, brief structure |
| [prompts/executor-prelude.md](prompts/executor-prelude.md) | Before every dispatch — worker return/result JSON contract |
| [prompts/templates.md](prompts/templates.md) | Before every dispatch — selected mode prompt (`plan-exec`/`review-fix`/`generic`) |

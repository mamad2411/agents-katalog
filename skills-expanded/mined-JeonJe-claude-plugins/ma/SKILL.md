---
name: ma
description: 티켓 → PRD → 설계 → PLAN → 승인 → 구현 → 코드 리뷰 → MR까지 품질 게이트가 걸린 풀 파이프라인 오케스트레이터. "ma", "풀 파이프라인", "티켓부터 MR까지" 요청에 사용.
disable-model-invocation: true
---

# MA quality-gated pipeline

Coordinate call order, scope, state, approval, validation, and (optional) notification. Keep phase implementation in the corresponding `ma-*` skill; do not duplicate it here.

All paths in this skill resolve through the workspace config (see the plugin's `config/README.md`): artifacts under `{contextRoot}/{domain}/`, pipeline state under `{stateRoot}/{key}/`.

## Invocation

```text
/ma <issue-key> [--resume] [--base <branch>] [--target <branch>] [--auto]
```

- Require an issue key matching the configured `issueKeyPattern`, e.g. `PROJ-123`. If the workspace has no issue tracker, any key matching the pattern names the work; requirements then arrive as user-provided text.
- Default `--base` to the project's configured base branch (commonly `develop` or `main`).
- Default `--target` to `feature/{key}-{slug}`.
- Use `--resume` to continue from the first incomplete phase after validating recorded artifacts.
- Treat `--auto` as flag forwarding only. It does not grant implementation approval unless the user explicitly requested unattended implementation.

Examples:

| Input | Action | Stop condition |
|---|---|---|
| `/ma PROJ-123` | Resolve the requested scope, initialize state, then run the gated pipeline | Selected scope terminal |
| `/ma PROJ-123 PLAN까지만` | Run PRD, design, and per-project PLAN | Phase 2.3 |
| `/ma PROJ-123 --resume` | Revalidate prior results and enter the first incomplete phase | Selected scope terminal or a halt gate |

## References index

| File | When to read |
|---|---|
| [references/scope-gate.md](references/scope-gate.md) | Phase 0 and every MA entry — terminal scope resolution (SSOT, also read by each `ma-*` skill) |
| [references/accuracy.md](references/accuracy.md) | At the start of every `ma-*` step — accuracy and reporting contract |

## Execution contract

1. **Resolve scope before work.** Read `references/scope-gate.md` and set one of `docs`, `plan`, `plan-review`, or `impl`. Interview once when the terminal scope is materially ambiguous. Never enter Phase 3+ for scopes below `impl`.
2. **Initialize durable state immediately after scope resolution.** This preserves recovery if any later phase fails.
3. **Enter phases in order.** Before each phase, confirm the preceding phase is in `completedPhases` and its required artifact exists. If handoff moved an artifact, validate the new path recorded in state instead of requiring the old path.
4. **Require implementation approval.** After Phase 2.5, stop once for approval that records project, base, and target. Neither `--auto` nor an `impl` scope bypasses this gate unless unattended implementation approval was explicit.
5. **Keep project writes inside the handoff worktree.** Phase 4 implementation goes through `/ma-dispatch`; do not edit a target project's main checkout directly.
6. **Complete each phase atomically.** Call the phase skill, verify its artifact gate, send the optional notification, append `timeline.md`, update `phaseResults`, then add the phase to `completedPhases`. A failed step leaves the phase incomplete and must be repaired and rechecked.
7. **Use agent return values, not polling.** The `/ma-dispatch` STATUS block is the completion source of truth. Do not add `sleep` loops.
8. **Preserve recoverability on halt.** Record structured evidence, send the optional halt notification, and keep artifacts intact so `--resume` can continue safely.

## State contract

Create `{stateRoot}/{key}/state.json` with this minimum shape:

```json
{
  "key": "{key}",
  "scope": "impl",
  "destination": "one-line arrival state",
  "phase": 1,
  "status": "in_progress",
  "attempt": 1,
  "startedAt": "...",
  "completedPhases": [],
  "artifacts": {},
  "gates": {},
  "worktrees": {},
  "phaseResults": {}
}
```

Maintain these fields:

- `artifacts`: `prd`, `design`, `diagrams`, per-project `plans`, `reviewPlan`, `worktrees`, `dispatchLogs`, conditional `e2eResult`, `codeReview`, and `mr`.
- `gates.implementationApproval`: canonical `{status:"approved", approvedAt, approvedBy, projects:{project:{base,target,primaryModule,affectedModules,mrPolicy?}}}`. Name `primaryModule` and `affectedModules` whenever the project defines modules — they select which module setup runs and where PLAN is packaged, and `/ma-handoff` rejects the approval without them. `mrPolicy` may override assignee, reviewers, and `reviewRequired`.
- `worktrees`: `{project: {path, base, target, baseCommit, planPath, mr, mrEvidence}}`. Phase 3 records path/base/target/baseCommit/planPath; Phase 6 records the URL and structured evidence path.
- `phaseResults[phase]`: `status`, `artifacts`, `checks`, and failure evidence when applicable.

Also maintain:

```text
{stateRoot}/{key}/
├── state.json
├── timeline.md
├── review-plan.md
└── review-result.md
```

For `--resume`, derive the next phase from `completedPhases`, recheck recorded paths, and reuse valid PRD/design/PLAN/worktrees.

## Integrations (all optional)

- Issue tracker: when the workspace has one configured (e.g. a Jira MCP), Phase 1 reads the ticket and a final phase may update its description. Without a tracker, requirements arrive as text and tracker phases are skipped.
- Notifications: when `notify.channel` is configured, send a short phase-completion message per phase. An empty channel skips every notification without failing any gate.

## Unattended flag forwarding

| Call | Forwarding rule |
|---|---|
| `/ma-write` | No flag by default; forward `--auto` only for explicitly unattended PRD/design generation |
| `/ma-plan` | Forward `--auto` only after target projects are unambiguous |
| `/ma-review plan` | No flag |
| `/ma-handoff` | Forward `--auto` after implementation approval records project/base/target |
| `/ma-dispatch` | Forward `--auto --caller=ma --mode=plan-exec`; repeat `--project=<project>` for each selected approved project (omit it to select all approved projects) |
| `/ma-open-mr` | Forward `--auto` |

## Pipeline

Each phase is one skill call followed by its gate and the atomic completion sequence. Deterministic phase-check scripts are not included in v1; verify each gate condition manually (or with your own scripts) before marking the phase complete.

| Phase | Call | Required gate |
|---|---|---|
| 0 Scope | Entry scope gate | `state.json.scope` and `destination` set |
| 1 PRD | `/ma-write prd {key}` | `{contextRoot}/{domain}/prd/{key}.md` exists, no unresolved Blocking item |
| 2 Design | `/ma-write design {key}` | design + `-diagrams.md` exist |
| 2.3 Plan | `/ma-plan {key}` | one PLAN per target project, structurally complete |
| 2.5 Plan review | `/ma-review plan {key}` | `review-plan.md` exists; unresolved `CRITICAL=0` |
| 2.75 Approval | Inline approval | approved project/base/target recorded in `gates.implementationApproval` |
| 3 Handoff | `/ma-handoff {key} --auto` | worktree exists on target branch + `HANDOFF.md` + packaged `PLAN.md` |
| 3.5 Environment | Boot/verify the stack needed for implementation checks (project `setup`/`healthCheck` from workspace config) | no fatal environment failure; evidence recorded |
| 4 Build | `/ma-dispatch {key} --project=<project> --mode=plan-exec --auto` (repeat per selected project) | every target `DONE_OK` + dispatch log with PLAN execution status |
| 4.5 Runtime verification | Conditional — run your E2E verification step (browser/device harness of your choice) only when at least one approved PLAN records runtime E2E as `required` | required PLANs have an E2E result with `E2E_VERDICT: PASS`; all-`not_applicable` PLANs retain their recorded reason |
| 5 Review | `/ma-review code {key}` | `review-result.md` exists; unresolved `CRITICAL=0`; MR description feed present |
| 6 MR | `/ma-open-mr {key} --auto` | every approved project has URL + structured evidence; live metadata matches approval |
| 7 Tracker update | Optional — update the ticket description from the merged evidence (skip without a tracker) | description updated |
| 8 Final notify | Optional — send the terminal notification (skip without a channel) | notification sent |
| 9 Cleanup | Post-merge cleanup: remove the worktree, delete the local branch, keep base clean | merge confirmed; worktree/branch/temp removed |

## Branch and halt rules

- **Phase 2.5:** halt and alert on `CRITICAL`; feed `HIGH` fixes back into PRD/design/PLAN; inject `MEDIUM` cautions into Phase 4; record `LOW` only.
- **Phase 2.75:** on rejection or requested changes, update artifacts and rerun `/ma-review plan` before asking again.
- **Phase 3.5:** halt when environment recovery is impossible and attach the failure evidence.
- **Phase 4:** `DONE_OK` advances; `DONE_FAILED` retries up to `maxRetries.implementation` (default 3); `TIMEOUT`, `SESSION_DIED`, or a missing STATUS block halts as an abnormal termination.
- **Phase 4.5:** derive the gate only from the reviewed PLAN. `PASS` advances; product `FAIL` returns to a Phase 4 corrective dispatch; environment/auth/device `BLOCKED` halts with recovery evidence. When every approved PLAN says `not_applicable`, record the reasons and complete the phase without invoking a browser.
- **Phase 5:** halt on `CRITICAL`; fix `HIGH`/`MEDIUM` findings or disclose accepted residual risk in the MR description feed.
- **Phase 9:** run only after merge confirmation. If the MR is still open, leave Phase 9 incomplete after Phase 8 and resume cleanup after merge.

Halt immediately for insufficient requirements input, a review `CRITICAL`, unrecoverable environment failure, exhausted implementation retries, or phase timeout. A pending implementation approval is a pause, not a failure.

On halt, write `failedPhase`, `lastSuccessfulPhase`, `cause`, `evidence`, `recoveryOptions`, `recommendedAction`, `owner`, and `resumeCommand` under `phaseResults[phase].halt`.

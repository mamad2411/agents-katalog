---
name: task-status-update
description: >
  Closing or completing a task (status→done), or any other task-status
  change — start (→in_progress), block, supersede, wontfix, absorbed. The
  ONLY allowed way to change a task's `status`: it also runs the cross-task
  graph closure, plan.yaml ref sweep, atomic archive move + integrity guard,
  and the persist-gate — all silently lost on a raw YAML edit. Use when a
  task reaches `done` or any status must change; never hand-edit the
  `status:` field. NOT for creating a task (use task-creation) and NOT for
  content edits to an OPEN task's body (manual) — though the terminal sweep
  of `blocked_by` / cross-refs on OTHER tasks IS in scope.
status: active
relevant_for: ["main-code-agent", "buddy"]
invocation:
  primary: cross-cutting
  secondary: [user-facing, workflow-step]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: task-status-update

The only allowed way to change `status` in a task YAML. Direct
edits to that field are forbidden. On terminal status (done,
superseded, wontfix, absorbed) it also closes the task-graph
(cross-task `blocked_by`) and aligns `docs/plan.yaml` inline refs —
all in one invocation, so the graph never sees a half-closed
terminal.

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | int | yes | Task ID (NNN). |
| new_status | enum | yes | pending, in_progress, done, blocked, superseded, wontfix, absorbed. |
| board_result | string | no | APPROVED, APPROVED_WITH_RISKS, REJECTED, PASS_WITH_RISKS, null. |
| readiness | enum | no | raw, specced, reviewed, ready, implementing, done. |
| review_owner_workflow_id / review_owner_step_id | string pair | conditional | Invocation-only exact owner for mandatory software-review-derived writes; never task YAML fields. |
| reason | string | no | Free text for traceability; not stored. |
| workflow_phase | string | no | Current workflow phase. Soft-validated. |
| spec_phase_update | object | no | Spec-phase transition (see Step 3). |
| closure_ref | int | conditional | Successor / absorbing task ID. Required when `new_status` ∈ {superseded, absorbed}. |

**Vocab SoT:** the `new_status` and `readiness` value sets mirror
`framework/task-schema.yaml` (the authoritative vocab). When the schema
changes a value set, update this table in the same change — there is no
automated guard (the same hand-sync discipline as `task-format.md`).

## Flow

### Step 1: read YAML

Lookup `docs/tasks/{task_id}.yaml`, else
`docs/tasks/archive/{task_id}.yaml`. Missing → error. Remember the
source path (Step 5 uses it).

### Step 1b: start and close preconditions

Off-plan starts and held-back work never pass silently. Before Step 2:

0. **Plan state (`in_progress`).** Where `docs/plan.yaml` exists, run
   `python3 $FRAMEWORK_DIR/scripts/plan_engine.py --boot` (in-progress tasks,
   critical path, next actions, warnings) before the start.

1. **Programme order (`in_progress`).** While the project has an active
   agreed programme (it names its agreement), compare the start with the
   agreement's next task (the first in its order not yet started) and with the
   programme tasks at `in_progress`. Any start that is not the agreed next
   task — listed in the agreement or not — needs the user's confirmation
   recorded in the agreement (`agents/buddy/coordinating-sessions.md`
   §Programme order); without it, refuse the start. A start beside another
   `in_progress` programme task needs the parallel-start record in the
   agreement (`agents/buddy/concurrent-writers.md` §Parallel start: which tasks
   run at the same time, what in the user's order needs it and what each
   independence check showed); without it, or with a check that failed or did
   not run, refuse the start. A paused task is set back to `pending` or `blocked`
   through this skill, with its reason; there is no third state. Uncommitted
   work it leaves gets the entry of item 2.
2. **Commit state (`done`).** Take the task's changed paths from its diff or
   its return's list of changes (never `context_manifest`, which lists
   reads). Where this actor is the authorized committer, commit them before
   the close and name the commit(s);
   `git status --porcelain --untracked-files=all -- <paths>` is empty.
   Otherwise (no commit authorization, a standing no-commit boundary, or
   another committer such as the commissioning Buddy) add a `notes` entry
   `Not committed at close: <reason>; owner: <who commits>; when: <event>`
   and report it in the return, so the commissioning owner carries it in the
   handoff's held-back list (`framework/process-map.md` §Authorization). The
   close records this invocation writes follow the same rule: the close
   commit, or the same entry. A deferral without reason, owner and an
   observable `when` (a named authorization lift, a named task close or a
   date; not "later") refuses the close.
3. **Acceptance execution (`done`).** Acceptance the task's own criteria rest
   on and that did not execute is not met: its scenarios counted `unexecuted`
   in a suite, skipped for missing execution evidence, or a run not performed.
   Refuse `done` unless a `notes` entry
   `Unexecuted acceptance: <which>; owner: <who>; follow-up: <task id>`
   records the qualification. Each criterion counted as met carries the
   evidence its claim's row in `skills/_protocols/evidence-author-claims.md`
   §8.5 requires, in the task's return or records.

### Step 2: write YAML

Before a mandatory software-review-derived `board_result`, forward readiness
(`reviewed|ready|implementing|done`) or `spec_states` ready write, load
`skills/_protocols/evidence-pointer-schema.md` §9. The invocation supplies the exact
owner pair; no ambient/latest discovery or new task-schema fields. First run:

```bash
python3 "$FRAMEWORK_DIR/scripts/workflow_engine.py" --review-check "$review_owner_step_id" --id "$review_owner_workflow_id" --review-policy evidence
```

Read the retained explicit decision and compare the requested fields to §9.6:
spec/code PASS → APPROVED; spec NEEDS-WORK or code FAIL → REJECTED; code
PASS_WITH_RISKS → APPROVED_WITH_RISKS (existing PASS_WITH_RISKS alias allowed);
code PARTIAL → null. A requested mapping mismatch refuses the review-derived write.
For forward readiness, spec_states ready or a spec `APPROVED`, additionally run the
same exact-owner check with `spec_success` or `code_success` for the captured family
BEFORE writing.
Only a successful check and applicable existing risk/severity/authorization rules
permit that write. On refusal/evaluation error leave all requested review-derived
fields unchanged. Current negative evidence permits repair/non-forward raw|specced
updates; it never grants forward readiness. Apply this precheck before Step 3 too.
General reasoning/research and ordinary lifecycle bookkeeping do not acquire the
requirement. This is a prescribed invocation, not an atomic task writer.


When a review check supports the requested write, keep its whole returned receipt
(owner, policy, result, reason and the `input` entry with run, subject digest,
decision digest and `quotes_verified`) at the task's work or review-evidence owner
before dependent use; the read-only checker does not persist it
(`retention: not_persisted`). A
model-authored summary or JSON object is not proof that the checker ran
([Run receipts](../../framework/workflow-engine-receipts.md#run-receipts)). The review
decision and mapping rules above remain authoritative.

Write to the source path. Always:
- `status: {new_status}`
- `updated: {today YYYY-MM-DD}`

Optional fields when given: `board_result`, `readiness`,
`workflow_phase`, and the Step 1b `notes` entries. Don't touch others.
Unknown `workflow_phase` value → WARN, still write (new workflows define
new phases).

Validate the touched task against `framework/task-schema.yaml` via
`plan_engine --validate <id>`; on schema FAIL, fix before
reporting.

### Step 3: spec_phase_update (conditional)

Only when `spec_phase_update` is in the input. Writes to the task's
`spec_states` map. Valid transitions (each may fire a counter):

- `raw → reviewing` (`increment_review=true`)
- `reviewing → fixing`
- `fixing → reviewing` (`increment_review=true`,
  `increment_fix=true`)
- `reviewing → ready`

`spec_name` is created at `raw` if absent. Invalid transition or
unknown `current_phase` → abort.

### Steps 4–5.5: graph closure, archive move, persist gate

After Step 2 (and Step 3, when it applies) has written the task YAML, on every status change: read and follow
`skills/task_status_update/closure.md` (Step 4 cross-task graph closure on terminal status with the `closure_ref`
guard, `blocked_by` sweep and `docs/plan.yaml` ref sweep, and the critical-path blast radius on every change; Step 5
auto-archive or reverse move with the terminal-close integrity guard; Step 5.5 persist gate on `done`). Then report
per Step 6.

### Step 6: output

```
Status update: [{task_id}] {title}
  status: {old} -> {new}
  updated: {today}
  board_result | readiness | workflow_phase | spec_states: ... | unchanged
  cross-task sweep: N blocked_by + M closure entries | n/a (non-terminal)
  plan.yaml sweep: K descs rewritten | n/a
  critical-path: on-path | off-path | gates {ids} via --after | n/a
  archive: forward | reverse | no-op
  order: agreed next | agreed next beside {ids}, parallel-start record in agreement | deviation confirmed by {who} | n/a
  commit: {hashes} | not committed: {reason}, owner {who}, when {event} | n/a
  acceptance: executed | unexecuted {which}, owner {who}, follow-up {id} | n/a
```

`n/a` for `order` only off `in_progress` or outside a programme; for `commit`
and `acceptance` only off `done`, or for a `done` without changed paths (say
so).

## Anti-patterns

- **NOT** edit `status` directly in the YAML — call this skill.
  Reason: cross-task graph + plan.yaml refs must stay consistent in
  the same operation.
- **NOT** create new tasks via this skill (`status: pending` on a
  non-existent task) — `task_creation`. Reason: new tasks need
  duplicate check + triage.
- **NOT** edit `docs/tasks/archive/` directly or `git mv` files
  yourself — Step 5 is the only legitimate write. Reason: frozen
  zone (WORM); `consistency_check` reports hand edits as INCIDENT.
- **NOT** sequence `workflow_phase=done` AFTER `status=done` on the
  same task — phase first, status last. Reason: `status=done`
  archives the YAML; subsequent writes look like frozen-zone
  modifies.
- **NOT** skip the cross-task sweep on superseded/absorbed because
  *"there are probably no dependents"* — run the scan; cold-graph
  assumptions break silently.
- **NOT** change a task's scope or dependencies via a raw body edit
  and skip the graph. Open-body content edits go through neither
  task skill; if a scope edit adds or drops a real dependency, run
  the `task_creation` §1b-style pairwise check by hand plus
  `plan_engine --validate`. The skills fire on create + status —
  content-edit reconciliation is manual.

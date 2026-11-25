---
name: supercode
description: Use when an external scheduler fires a coding-loop project tick to reconcile planning, building, evaluation, diagnosis, or an operator answer against the approved acceptance agreement.
argument-hint: "--tick <project-loop-status.md>"
license: MIT
related skills: superloop, supercode-external, supermeta, supereval, superdiagnose
---

# Supercode

The native **SUPERVISOR** for one project, one round at a time. Input is exactly
`--tick <loop-file>`. Bootstrap/resume a project with `supercode-external`; there is no attended
outer driver. Never edit product code or acceptance inputs. The inner `superagent` loop owns
implementation, review and integration. Its DONE means the plan tree closed, not project PASS.

Invoke `superagent:superloop` and apply L1–L7 with consumer `supercode`, bootstrap input PROJECT,
state location `<project>/<SUPER_LOOP_STATUS_DIRNAME>/supercode.md` (or the existing registered
file), and the ready/transient mapping below. Retain legacy common fields; `project` never becomes
`master_plan`. `iteration` counts ticks; `round` counts created project rounds.

Resolve configuration in order: process environment, physical primary `.superenv`, plugin
`templates/superenv.default`. Use `SUPER_CODE_MAX_ITERATIONS` (positive integer),
`SUPER_MODEL_SUPERVISOR`, `SUPER_MODEL_META_PLANNER`, `SUPER_EFFORT_META_PLANNER`,
`SUPER_MODEL_DIAGNOSER`, `SUPER_EFFORT_DIAGNOSER`, and the existing worker/driver keys.
SUPERVISOR must be native to `SUPER_HARNESS`; refuse a foreign supervisor pin.

## Helper and scheduler locations

`SCRIPTS` below means `${CLAUDE_PLUGIN_ROOT}/scripts` in the installed package. Require its
`_coding_loop_state.py` and `_coding_loop_evidence.py`; never fall back to helpers from a source
checkout. The diagnosis template likewise comes from this package's `templates/` directory.
Scheduler infrastructure is separate in generated packages: define local `SUPERAGENT_SCRIPTS`
from the registration's literal `SUPERAGENT_SCRIPT_DIR` (normally inherited by the tick), or an
explicit operator-provided source-repository `scripts/` path. Require that directory contains
`launch.sh` and `superagent-tick.sh` before a scheduler action. Never infer it by walking above a
copied package. Every `launch.sh`/stop/control reference below uses `SUPERAGENT_SCRIPTS`; the
Python validation commands use installed `SCRIPTS`.

## Tick order

Run this order exactly, including on a restarted transient. At most **one expensive phase
operation** per tick: one META_PLANNER, supereval with its single EVALUATOR, or one DIAGNOSER.
Launching the inner registration is a separate tick action. Reconciliation is cheap validation,
not permission to dispatch a second phase in the same tick.

1. **Resolve consumer identity and physical roots.** Primary is the parent of
   `git rev-parse --path-format=absolute --git-common-dir`. Resolve the configured vault through
   `_common.sh` `vault_root`; external vaults must be their own Git repository. Use
   `superagent_control_target PROJECT REGISTERED_SLUG` from that helper and require its
   supervisor `supercode`, exact state file, project and primary repo. Never guess custom slugs.
   State must be physically inside that project's ignored state directory. Read it using
   `_coding_loop_state.py read`. Missing, conflicting or malformed identities refuse dispatch.
2. **Acquire existing L3, then reload state.** Project acquisition is exclusively
   `_coding_loop_state.py acquire-lock LOCK_DIR --owner DRIVER_PID --steal-min MIN`.
   Use `SUPERAGENT_TICK_PID` when present, otherwise the live supervising CLI PID. Exit on busy;
   never touch a live peer's state. The persistent `.reclaim` file must never be unlinked.
3. **Consume/validate a recorded operator answer.** Read only `## Pending decision`. Preserve
   unanswered and rejected answers. Append accepted answers and their action to Decisions; retain
   last_operator_answer as the durable transition receipt. The helper atomically appends an
   `author-meta` Decisions receipt for accepted adoption/replan and stores `meta_authorization_json`
   bound to project, prior/new round and agreement. Reservation binds its operation id; retries
   preserve it. `previous_round_json` retains the independent evidence for autonomous repair. The exact permitted commands are below; never infer author
   consent from config edits, elapsed time, a panel vote, or a new fingerprint. The helper's
   `reconcile-phase --consume-answer` validates the command and gates the resulting state.
4. **Apply sync and acceptance-context gates.** L5 synchronizes code main and external vault main.
   Require READY inputs and run `prd-lint.sh PROJECT` with `PRD_LINT_REPO_ROOT=PRIMARY`.
   Read the complete PRD, evaluation and knowledge-base, then every referenced binding source,
   including binding text those sources reference. Follow prose references too: machine link
   discovery cannot establish that arbitrary prose has no other obligations. If required text
   cannot be resolved, park as execution/evidence failure; do not reserve a worker.

   `_coding_loop_state.py context --repo PRIMARY --vault VAULT --project PROJECT
   [--captures CAPTURES.json]` discovers local Git text transitively and returns `manifest` and
   `agreement_revision`. Remote/document sources require revision-labelled text captures with
   `locator`, absolute `path`, `source_revision`, `sha256`; the helper checks digests. Supply each
   additional prose-discovered binding as a revision-labelled capture too. These supplement
   automatic discovery and never exempt discovered sources. The helper persists verified captures
   as `binding_captures_json` so cheap gates and retries can resolve the same text.
   An empty caller manifest is never proof of complete context. Preserve source revisions and
   captures with the operation's packet. Only the mutable PRD iteration ledger is excluded.
   `PENDING` is a bootstrap sentinel: it is never evidence and cannot populate an operation.
5. **Reconcile outputs before recovering a transient.** Run:

   ```text
   python3 SCRIPTS/_coding_loop_state.py reconcile-phase STATE --repo PRIMARY --vault VAULT
     --max-rounds MAX --consume-answer --write --owner DRIVER_PID [--captures CAPTURES.json]
   ```

   It reloads state, resolves context, checks integration, and validates exact phase evidence.
   Read both `state` and `receipt`. `INTEGRATED` alone is insufficient: require
   `worker_complete: true`. An integrated META root may still lack the meta-plan/ledger; reuse
   its original goal and operation. `CONFLICT` parks; never overwrite scratch, dirty, unmerged,
   duplicate, wrong-round or wrong-revision artifacts. `ABSENT` or reusable incomplete META
   returns only to that phase's ready state with the same operation. Record its reason.
   If reconciliation advances a phase or consumes an answer, end this tick after step 7.
6. **Switch on the verified status** and perform the one action in the table.
7. **Verify returned artifacts and identities again.** Resynchronize, re-resolve complete context,
   run `reconcile-phase` again, and revalidate registration/project identity. Never trust a worker
   message or timestamp as completion. Append one iteration receipt with tick, round, operation
   id, before/after status, code/vault revisions, artifact commits and reason. Release only your
   own L3 lock on every exit. Leave the `.reclaim` inode. DONE lets the wrapper disarm only the
   outer registration after the model exits; do not unload your own launchd process group.

## Phase actions

| Status | One tick action | Verified result |
|---|---|---|
| WAITING FOR META-PLAN | Reserve META operation; persist META-PLANNING; dispatch one META_PLANNER using supermeta | Integrated root/scaffold, meta-plan and exact ledger row, `worker_complete=true` → WAITING FOR BUILD |
| WAITING FOR BUILD | Record expected inner identity, then idempotent inner launch | Exact registered repo/root/state/slug → BUILDING |
| BUILDING | Consume the shared shell BUILDING gate only | Pending → BUILDING; verified inner DONE → WAITING FOR EVAL; missing/mismatch/stopped → outer input |
| WAITING FOR EVAL | Freeze synced code main SHA; reserve EVALUATING; invoke supereval | Integrated FINAL report and ledger, exact source identities, all C and required J/AC PASS → DONE; valid FAIL → WAITING FOR DIAGNOSIS |
| WAITING FOR DIAGNOSIS | Reserve DIAGNOSING of the exact selected FAIL; dispatch one DIAGNOSER | Valid REPAIR with room below limit → round+1 WAITING FOR META-PLAN; otherwise WAITING FOR INPUT |
| WAITING FOR INPUT | Validate recorded answer; no unanswered work | Accepted stored action or remain parked with reason |
| DONE | No new work | DONE |

META-PLANNING recovers to WAITING FOR META-PLAN; EVALUATING to WAITING FOR EVAL; DIAGNOSING to
WAITING FOR DIAGNOSIS, **only after** artifact reconciliation. Never map them to WAITING FOR RUN.
On interruption reconcile first, then restore that ready state or park; preserve live-peer exemption.
A repeated failed dispatch goes through L7, retaining the same operation and paths. L7 may resolve a
routine operation failure, but cannot adopt specification changes or spend another repair round on
unresolved execution/evidence failure. A panel is not author approval.

### Reserve before dispatch

Prepare JSON with exactly the state helper's operation fields: `id` (empty for a new operation),
`phase`, `round`, `agreement_revision`, `code_commit`, `meta_plan`, `goal_folder`, `report`,
`source_vault_commit`. Choose one timestamp and intended paths **before** dispatch. META has empty
code/report fields and fixes the goal identity before supergoal can scaffold. EVAL freezes current
code main; DIAGNOSIS retains the failed evaluation's code SHA and records current source-vault main.
Preserve the selected eval's independent `eval_operation_id` and `eval_source_vault_commit`.

Call `_coding_loop_state.py reserve STATE --repo PRIMARY --vault VAULT --operation JSON
--max-rounds MAX --owner DRIVER_PID [--captures CAPTURES.json]`. It verifies current context, round
limit and phase before atomically assigning a new id. Export its resulting `operation` mapping to
an ignored JSON packet; workers read that exact packet with `--operation`. Retries preserve every
field and output path, including id. Do not fabricate successful receipts or manually bypass a
refused reservation using generic state replacement.

For META dispatch `supermeta PROJECT --operation JSON --supervisor-state STATE`. The worker must
run `_coding_loop_state.py meta-entry` against that registered state itself. This validates either
first-round entry, strict automatic FAIL+REPAIR entry, or the exact recorded author-approved entry;
a prompt assertion is never authorization. For EVAL invoke
`supereval PROJECT --operation JSON`; that skill dispatches its own single EVALUATOR, so do not
create a second evaluator. For DIAGNOSIS dispatch
`superdiagnose PROJECT --round N --eval-report EXACT_LAST_EVAL --operation JSON`, supplying the
resolved agreement packet and complete failed/missing checks, selected plans/reports/findings.
Each worker returns its full report and integrated artifacts. The supervisor never recursively
invokes its own role; the DIAGNOSER never spawns another DIAGNOSER.

### Record and launch the inner identity

Retain the completed META operation throughout WAITING FOR BUILD and BUILDING. Its verified
receipt supplies the root plan and goal folder. Select a unique per-project/per-round inner slug;
never share a child across projects or rounds. Before any scheduler side effect, record `inner_slug`
and `inner_loop` canonically with the state helper under L3. Use `launch.sh ROOT --slug INNER
--dry-run` to obtain the exact existing/prospective inner state path, and persist it first. Reuse
that identity after a crash; if the launch date changed before creation, park rather than silently
change the recorded state path. If registration already exists, validate and adopt it without
relaunching or rearming an operator-stopped child. Otherwise `launch.sh ROOT --slug INNER` once.
Verify registration, exact root, project round via the retained META receipt, primary repo and state
path before setting BUILDING. Then exit this tick.

BUILDING's shell adapter rechecks state, registration and scheduler under L3. Active, queued,
CI-waiting and inner WAITING FOR INPUT use no model work. Inner input directs the operator to the
inner slug without another notification. Disarmed unfinished inner work never auto-rearms. Only
its verified DONE allows evaluation. Neither launch nor inner DONE can mark the project DONE.

## Explicit operator decisions

Write the exact reason, selected failed report/diagnosis, owner `outer`, valid command, and stored
resume phase in `## Pending decision`. Set `pending_kind` as appropriate. Record answers through
`answer.sh --no-kick SLUG "COMMAND"` (or omit no-kick to request a tick). Invalid commands remain
recorded and parked; use `--replace` to correct them.

- `retry`: operational retry of the stored ready phase only, with unchanged agreement.
- `adopt-agreement FINGERPRINT`: author adopts the freshly resolved complete agreement. Start a
  **new planning round**, with room under the limit. Clear prior operation/inner identities; retain
  report history. Never reuse an old PASS for new criteria. Legacy ledger adoption must first
  reconcile its raw meta/goal/eval locators and integrated artifacts; those cells are history,
  never a substitute operation or proof of inner DONE. Preserve the highest historical round.
- `raise-limit N`: only after explicitly raising configuration to that exact positive N above the
  current exhausted round. Increasing config alone leaves the loop parked. Retain the FAIL and
  diagnosis; the accepted answer permits the next planned round.
- `replan`: author explicitly authorizes a new round after an AUTHOR INPUT diagnosis, with the
  unchanged agreement and room under the limit. It does not adopt new acceptance requirements.

If an answer and changed agreement arrive together, validate adoption first. Author-only agreement
changes remain unadopted until the exact fingerprint is named. PASS on the final allowed round
completes normally; FAIL may be diagnosed there but cannot create round MAX+1. Missing J results,
missing context, invalid revisions or an unintegrated report always prevent DONE.

## Worker routing

Use the installed harness's isolated dispatch and model/effort pins for META_PLANNER or DIAGNOSER.
Wait synchronously for the one phase worker; use the existing foreign-role bridge when necessary.

<!-- cc-only:start -->
For native `inherit` or tier model and inherited effort, use one Agent with the native model pin
(omit inherit). Otherwise use generated `super-meta-planner` or `super-diagnoser` agent definitions,
omitting the Agent model argument. A missing definition is a hard dispatch error; re-run init.
<!-- cc-only:end -->
<!-- cursor-only:start
Use one native agent for an inherited/bare model and inherited effort; otherwise the generated
super-meta-planner or super-diagnoser definition. A missing definition is a dispatch error.
cursor-only:end -->
<!-- codex-only:start
For native Codex, spawn_agent with fork_turns: "none", model stripped of codex:, reasoning_effort,
omitting inherited pins. For a foreign role use the generated banner's relay with fork_turns:
"none" and pass foreign pins to role-bridge.sh, never native spawn. Wait for its final receipt.
codex-only:end -->
<!-- pi-only:start
Use one blocking role-bridge.sh process with --tools planner, the role's resolved --harness,
--model and --effort, and the exact worker prompt file. Pi has no agent definitions. Wait on the
process, never poll a second worker. Foreign prefixes select that harness through the same bridge.
pi-only:end -->

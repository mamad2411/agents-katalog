---
name: superagent
description: Use when asked to drive a goal's root seed/master plan (PLAN.md) to completion unattended, or when a scheduler fires `--tick` on an existing loop-status file — the autonomy supervisor for the super* plan-tree lifecycle, driven in-session (cron) or by an external scheduler in a fresh context per tick.
argument-hint: "<PLAN.md> [--driver=cron|desktop]   (or: --tick <loop-file>)"
disable-model-invocation: true
license: MIT
related skills: superloop, superplan, superrun, supertraverse, superfinish
---

# Superagent

The **autonomy supervisor** for the `super*` plan-tree lifecycle. Given a goal's **root** seed/master
plan, superagent selects legacy planning, upfront refinement, adopted replanning, or execution and
drives the goal to verified completion **unattended**, one operation per iteration.

superagent does **not** plan or execute work itself. Each iteration dispatches **at most one**
selected planning operation or `superrun` (never both) in its required isolated dispatch form
(see **Subagent dispatch** below), reads
that skill's Final Report, **relays it verbatim to the caller** (see **Final Report — per tick**),
advances a small state machine, and lets its **driver** fire the next iteration. Two drivers are supported (see **Drivers**): an
**in-session `cron`** job (attended; context accumulates) or an **external scheduler** — a Desktop
routine or OS cron firing `/superagent --tick` in a **fresh session per iteration (clean context)**.
All state lives in the loop file, so the two are interchangeable. The loop ends itself when the goal is
complete.

**This skill is built on the `superloop` chassis.** **Invoke the `superagent:superloop` skill via the Skill tool at
the start of the run** and apply its clauses **L1–L7** throughout: the loop-status file (L1), the
cron/external driver + guard/bootstrap/resume (L2), the overlap lock (L3), the context-handoff gate
(L4), the sync gate (L5), the PR integration discipline (L6), and the decision-escalation ladder (L7).
superloop owns the **chassis**; superagent supplies the **work model** below — the `WAITING FOR PLAN` /
`WAITING FOR RUN` status vocabulary, the one-skill-per-tick selected-operation / executor dispatch (Step 1),
and the verified-completion `DONE` condition. superagent's `<consumer>` value for L2's tick prompt is
`superagent`; its `<bootstrap-input>` is the root `<PLAN.md>`; its status-role mapping is ready =
`WAITING FOR PLAN` / `WAITING FOR RUN`, transient = `PLANNING` / `RUNNING`, plus `WAITING FOR INPUT`,
`DONE`, and a superagent-specific **parked** state `WAITING FOR CI` (see **CI wait — monitor-parked**);
its heavy step (L4) is one selected planning operation or `superrun` invocation (each dispatched
in its required isolated form)
with threshold (`SUPER_HEAVY_STEP_LIMIT`, default 6); its be-sure
artifacts (L5) are the selected planning operation's plan/receipt/repair artifacts or superrun's
closeout files plus PR squash commits;
its escalation option-set (L7) is {retry `superrun` / re-plan / decline}.

| Thought | Reality |
|---------|---------|
| "I'll plan this step and then run it in the same tick while I'm here" | NO. **One skill per tick.** Set the next status and let the next cron tick run it. superplan and superrun contexts must never intermix. |
| "I'll just invoke the selected skill via the Skill tool here — it's simpler" | NO. **Every selected planning operation and `superrun` runs in its required isolated form** (see **Subagent dispatch**). superagent's own context ingests only the returned Final Report (which it then relays verbatim to the caller), never the full skill execution — that is what keeps the supervisor lean and the per-session threshold (`SUPER_HEAVY_STEP_LIMIT`, default 6) meaningful. |
| "I'll detect the next step / execute the plan myself" | NO. superagent never independently authors or executes. It reconciles traversal/records, selects the role operation, and reacts to the delegated Final Report. |
| "/superagent was run again — I'll start the loop" | NO. Check first. `cron` mode: `CronList` — a live job + non-terminal status = already looping, report and exit. `external` mode: a non-terminal loop file = the Desktop routine / cron entry is already the driver; report state and re-print setup, don't arm anything. Never start a second loop. | <!-- cc-only -->
<!-- cursor-only:start
| "/superagent was run again — I'll start the loop" | NO. Check first. A non-terminal loop file = the scheduler entry is already the driver; report state and re-print setup, don't arm anything. Never start a second loop. |
cursor-only:end -->
<!-- codex-only:start
| "/superagent was run again — I'll start the loop" | NO. Check first. A non-terminal loop file = the scheduler entry is already the driver; report state and re-print setup, don't arm anything. Never start a second loop. |
codex-only:end -->
| "A fresh/empty context means I lost the loop state" | NO. All state is in the loop file. A `--tick` works identically in a clean context (external driver) or an accumulating one (cron). Acquire the lock, read the file, run one tick. |
| "A skill raised a question — I'll just ask the user" | NO. First run the **subagent panel** (Decision-escalation ladder). Ask the user only if the panel cannot converge. |
| "The work is blocked — terminate the loop" | NO. Run the panel on the blocker first (retry / re-plan / decline / escalate). Stop the driver only when DONE or an escalation pauses the loop. |
| "superplan/superrun already did `git checkout main && pull`, so local is synced" | NO. That pull can silently fail or be skipped (worktree checkout error after a remote `--admin` merge; propagation race). Run the **Sync gate** before AND after every skill, and verify the merged artifacts are present locally — never advance on a stale tree. |
| "Context is getting low but I'll squeeze one more `superplan`/`superrun` in while I'm here" | NO. **Run the Session skill-budget gate (Step 0.5) before every iteration.** After `SUPER_HEAVY_STEP_LIMIT` heavy skills (default 6) in one cron session → persist, stop the cron driver, and hand off; tell the user to `/clear` and re-run `/superagent`. A skill that dies mid-run with the window blown leaves no clean resume. | <!-- cc-only -->
| "superrun yielded CI-PENDING — I'll poll `gh run view` / `gh run watch` in a loop until it finishes" | NO. **Park.** Record the CI packet, set `WAITING FOR CI`, arm the completion **Monitor**, release the lock, end the tick. The harness re-invokes you exactly once, when ALL runs are terminal. Per-tick / in-context polling is the context waste the parked state exists to eliminate. | <!-- cc-only -->
| "A tick fired while WAITING FOR CI — I'll check the run status while I'm here" | Reconcile the authoritative root/C8 barrier first. Then cron with no barrier change: no CI query (the Monitor owns the wait); external: ONE batched `curl` over the recorded run ids. Never dispatch a heavy skill while still parked. | <!-- cc-only -->
<!-- cursor-only:start
| "superrun yielded CI-PENDING — I'll poll `gh run view` / `gh run watch` in a loop until it finishes" | NO. **Park.** Record the CI packet, set `WAITING FOR CI`, release the lock, end the tick. Each later scheduled tick does ONE batched `curl` over the recorded run ids and exits unless every run is terminal. Per-tick heavy polling is the context waste the parked state exists to eliminate. |
| "A tick fired while WAITING FOR CI — I'll check the run status while I'm here" | ONE batched `curl` over the recorded run ids, then exit if any is still running — never a heavy dispatch. |
cursor-only:end -->
<!-- codex-only:start
| "superrun yielded CI-PENDING — I'll poll `gh run view` / `gh run watch` in a loop until it finishes" | NO. **Park.** Record the CI packet, set `WAITING FOR CI`, release the lock, end the tick. Each later scheduled tick does ONE batched `curl` over the recorded run ids and exits unless every run is terminal. Per-tick heavy polling is the context waste the parked state exists to eliminate. |
| "A tick fired while WAITING FOR CI — I'll check the run status while I'm here" | ONE batched `curl` over the recorded run ids, then exit if any is still running — never a heavy dispatch. |
codex-only:end -->
<!-- pi-only:start
| "I'll dispatch `superplan` with the `subagent` tool — it's right there" | NO. On Pi the supervisor NEVER uses a subagent tool. `superplan`, `superrun`, and every panelist are bridge processes started from your `bash` tool (see **Subagent dispatch**); `pi-subagents` is for `superrun`'s task-loop children only. |
pi-only:end -->
| "The dispatched subagent will run a long time — I'll run it in the background and check on it while I wait" | NO. **Wait, never poll.** Every heavy-skill dispatch is synchronous (`run_in_background: false` for a selected planning-role agent; a blocking Bash call for `superrun`): the blocked call waits at zero context cost and the Final Report arrives as the tool result. A background dispatch + `TaskOutput`/`TaskList` checks spends supervisor context on "still running" snapshots the synchronous return delivers for free. |
| "I'll dispatch `superrun` as an Agent-tool subagent like `superplan`" | NO. **`superrun` runs in its own CLI process** (`role-bridge.sh --tools executor` from your Bash tool — see **Subagent dispatch**). `superrun` is the task-loop controller and must dispatch its own implementer/reviewer subagents; a subagent cannot foreground-wait on its children (superloop L7's depth-1 constraint), so as an Agent-tool subagent it degrades into a `SendMessage`-nudge spiral and never converges (issue #25). |
| "My dispatch was interrupted mid-flight (API lost, host slept) — I'll ask the operator whether to resume or pause" | NO. **A tick never ends with a question — not via a tool, not as the final chat message** (in an unattended session no one can answer; the questioning turn exits 0 and strands `status: PLANNING`/`RUNNING` + the held lock). Self-heal immediately per superloop L2's tick teardown invariant: log the interruption, reset `PLANNING → WAITING FOR PLAN` / `RUNNING → WAITING FOR RUN`, `release_lock()`, end the tick with a normal report. The next scheduled tick retries the step. |

## Hard gate — `<PLAN.md>` is required

**DO NOT START A LOOP WITHOUT THE MASTER PLAN FILE.** If superagent is invoked with no `<PLAN.md>`
and no existing loop-status file can be located, respond with exactly:

    superagent requires a master plan file (PLAN.md). None provided and no loop file found. Exiting.

and **exit**. Do not guess a plan from the working directory.

`<PLAN.md>` must be the goal's **root** seed/master plan (the same file `superrun` traverses and
`superplan` descends from) — not a leaf implementation plan.

## Repo configuration (.superenv)

Resolve project context before any workflow action by sourcing `${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh` under bash (it refuses zsh and other shells — wrap the call in `bash -c '…'` when your shell is not bash) and calling `superagent_load_context "$PWD" run` (lifecycle control commands first load the registered `SUPERAGENT_PROJECT_ROOT`). Use its exported physical `REPO` and validated `SUPER_GIT_MODE`. Resolution is process environment > nearest/explicit project `.superenv` > packaged default; missing mode means `github`. In `none`, never run git, gh, GitHub API, credential discovery, worktree, commit, push, PR, merge, sync, or CI-poll operations. An existing `.git` directory does not change this rule.

## Vault root

Resolve `SUPER_GOAL_ROOT` (above). If it starts with `/` or `~`, the vault is **external**:
`<vault_root>` is that path (`~` expanded to `$HOME`, one trailing `/` stripped), resolved physically
(`cd "<path>" && pwd -P`) so it matches the paths `launch.sh` stores, and the vault is its own git
repository outside the checkout. Otherwise `<vault_root>` is `<primary_root>/<SUPER_GOAL_ROOT>`
(`primary_root` = the physical `REPO` exported by `superagent_load_context`). Every goal
folder, project folder, loop-status file and lock derives from `<vault_root>`; **never join
`SUPER_GOAL_ROOT` onto the checkout root by hand.** The same rule is `vault_root` /
`vault_is_external` in `scripts/_common.sh`.

---

## The loop-status file

The location, format, frontmatter schema, `primary_root()`, goal-folder derivation, and gitignore facts
are **superloop L1**. superagent's `status:` values map to L1's generic roles as: ready = `WAITING FOR
PLAN` / `WAITING FOR RUN`; transient = `PLANNING` / `RUNNING`; plus `WAITING FOR INPUT` and `DONE`.
`WAITING FOR CI` is a superagent-specific **parked** role — durable like a ready state (a persisted
`WAITING FOR CI` is normal, NOT a crash), but its tick branch dispatches nothing heavy. superagent adds
the `plan_exhausted` frontmatter field (its queue-exhaustion hint, never completion proof), optional
recovery hints `planning_operation: refine|replan|none`, `planning_target`, `planning_generation`,
and `planning_record`, and, while parked, a `ci_wait:` block (see
**CI wait — monitor-parked**). It also keeps two executor-yield fields: a `checkpoint:` block while a
`superrun` CHECKPOINT awaits its resume, and `executor_timeouts:` (`leaf:` + `count:`), the number of
consecutive `superrun` dispatches on one leaf that hit the wall-clock limit (see **Executor
checkpoints and timeouts**). `replan_stalls:` (`stage:` + `count:`) counts consecutive `superreplan`
BLOCKED outcomes for one originating stage (see `WAITING FOR PLAN` step 5).

### Status vocabulary

- `WAITING FOR PLAN` — select one planning operation: legacy incremental authoring under PLANNER,
  upfront preparation under PLAN_REFINER, or adopted repair under REPLANNER. A valid prepared upfront
  target transitions to `WAITING FOR RUN` without dispatching a heavy skill.
- `PLANNING` — the selected planning operation is running (transient within a tick; persisted ⇒ a crash).
- `WAITING FOR RUN` — ready to dispatch `superrun` in its isolated executor CLI process for the next ready leaf.
- `RUNNING` — `superrun` is running (transient within a tick; persisted ⇒ a crash).
- `WAITING FOR CI` — a dispatched `superrun` pushed long CI and yielded a CI-PENDING report; the loop
  is **parked** on the run(s) behind a completion Monitor (cron) or a one-curl-per-tick check
  (external). Durable, not a crash. See **CI wait — monitor-parked**.
- `WAITING FOR INPUT` — a decision the subagent panel could not resolve is awaiting the user.
- `DONE` — every active obligation passed supertraverse C9, with verified integration or an authorized disposition and no unresolved blockers (see below).

---

## Step 0 — Parse the invocation, then guard / bootstrap / resume

Parse the invocation (form (A) internal `--tick <loop-file>`; form (B) user entry) and guard / bootstrap
/ resume per **superloop L2**, with `<consumer>` = `superagent` and the required bootstrap input = the
root `<PLAN.md>`. If form (B) is invoked with no `<PLAN.md>` and no existing loop file can be located,
print superagent's exact hard-gate message (above) and exit. L2 owns the form-(A) lock-then-read-then-
`DONE`-no-op sequence, the form-(B) driver parse / state-location / cron-and-external guard-bootstrap-
resume branching, and the read-`master_plan`/`status`/…-before-Step-1 step. After L2 hands control back
— having read the loop file and (for a continuing tick) acquired the lock — run **Step 0.5** then go to
**Step 1**.

---

## Step 0.5 — Session skill-budget gate (check BEFORE every iteration)

<!-- cc-only:start -->
Run **superloop L4** (`check_session_budget()`) before every iteration — after reading the loop file
(Step 0) and after the `DONE` no-op, but before the Step 1 dispatch. superagent's **heavy step** is one
selected planning operation or `superrun` invocation (incremented in Step 2); the handoff **threshold** is `SUPER_HEAVY_STEP_LIMIT` (default 6). If L4 hands
off, this tick ends there; otherwise go to **Step 1**.
<!-- cc-only:end -->
<!-- cursor-only:start
A structural no-op in this build (superloop L4): the external driver is the only driver and every tick
runs in a fresh context. Go straight to **Step 1**.
cursor-only:end -->
<!-- codex-only:start
A structural no-op in this build (superloop L4): the external driver is the only driver and every tick
runs in a fresh context. Go straight to **Step 1**.
codex-only:end -->
<!-- pi-only:start
A structural no-op in this build (superloop L4): the external driver is the only driver and every tick
runs in a fresh context. Go straight to **Step 1**.
pi-only:end -->

---

## Sync gate — local `main` must equal `origin/main` (REQUIRED around every skill dispatch)

Run **superloop L5** (`sync_main()`, `sync_vault()` in external vault mode, + the Be-sure verification, STOP → `WAITING FOR INPUT`) around every
skill dispatch — pre, so the delegated skill reads a fresh tree, and post, so a silently-skipped local
pull never leaves the primary checkout stale. superagent's **be-sure artifacts** are the
selected planning operation's Final-Report-named plan/receipt/repair files or superrun's closeout
files plus the PR squash commits (see the
per-status Sync-gate steps in **Step 1**). If L5 STOPs, the loop pauses on `WAITING FOR INPUT` — do not
advance.

Every `sync_main()` / `sync_vault()` reference below is mode-dispatched through L5. In
`SUPER_GIT_MODE=none`, it means validate the inherited workspace owner, capture/compare snapshots,
and reopen durable artifacts; it never calls git or GitHub. In `github`, the existing sync behavior
is unchanged.

---

## Subagent dispatch — selected planning operations and `superrun` run isolated

**Every heavy-skill invocation runs isolated from superagent's own context — superagent NEVER
invokes a selected planning operation or `superrun` inline.** Planning roles and the executor are
isolated differently, and the executor distinction is load-bearing:

- **`superplan` → an Agent-tool subagent.** `superplan` authors documents and dispatches no
  subagents of its own, so a depth-1 subagent is the right container. When Step 1 reaches the
  `WAITING FOR PLAN` branch, dispatch it with the **Agent tool** (`subagent_type: general-purpose` —
  full tool access: Bash, Edit/Write, git, `gh` — and `run_in_background: false`; see **Synchronous
  dispatch** below).
<!-- pi-only:start
- **On Pi, every selected planning operation (`superplan`, `superrefine`, or `superreplan`) is
  INSTEAD its own CLI process — this supersedes the Agent-tool bullet above.** This harness has no
  in-process subagent tool in the supervisor; every heavy dispatch is a blocking `bash` call to the
  bridge. Dispatch the selected planning skill exactly like `superrun` below, with two differences:
  `--tools planner` and `--role planner|plan-refiner|replanner`, using the matching role's
  `SUPER_MODEL_<ROLE>` / `SUPER_EFFORT_<ROLE>`:
  `"${SUPERAGENT_BRIDGE:-${CLAUDE_PLUGIN_ROOT}/scripts/role-bridge.sh}" --harness <h> --model "<m>" --effort "<e>" --tools planner --cwd "<primary root>" --prompt-file "$f" --role <role>`
  A native (`pi:`/inherit) planning role runs with `--harness pi` — native and bridged are the same
  code path on this harness. The child inherits `SUPERAGENT_PI_SKILLS` from the tick, so the selected
  planning skill resolves inside it. Exit 0 → stdout is the Final Report; non-zero
  → the crashed-dispatch path (retry once, then the crash-recovery mapping: restore the ready
  status, `release_lock()`, end the tick, quoting the `log=` path in `Findings & issues`).
pi-only:end -->
- **`superrun` → its own CLI process.** `superrun` is the task-loop (`superagent:superbuild`) controller:
  it dispatches implementer / reviewer / fix-applier subagents and foreground-waits on each. **A
  subagent cannot foreground-wait on its own children** (superloop L7's depth-1 constraint): run as
  an Agent-tool subagent, `superrun`'s children background and yield control back after every turn,
  and the tick decays into a `SendMessage`-nudge spiral with two writers racing on the worktree
  (issue #25). So when Step 1 reaches the `WAITING FOR RUN` branch — and for the ci-resume dispatch
  and any escalation-ladder retry — start `superrun` as the **top-level agent of a fresh headless
  CLI process** via the shipped bridge, from **your own Bash tool**, and block on it:

  1. Write the dispatch prompt (the instruction list below, with the concrete `<PLAN.md>` path and,
     for a resume, the `ci_wait` packet + conclusions) to a temp file with a quoted heredoc:
     `f="$(mktemp "${TMPDIR:-/tmp}/super-executor.XXXXXX")"; cat >"$f" <<'__SUPERAGENT_PROMPT_END__' … __SUPERAGENT_PROMPT_END__`.
  2. Resolve the executor's harness / model / effort (see **Model resolution** below), then run —
     from the **primary checkout root** (`superrun` makes its own worktree), with Bash-tool
     `timeout` set to `$(superagent_executor_timeout_ms)` milliseconds
     on the Bash call:
     `SUPER_EXECUTOR_TIMEOUT_MIN="$SUPER_EXECUTOR_TIMEOUT_MIN" "${SUPERAGENT_BRIDGE:-${CLAUDE_PLUGIN_ROOT}/scripts/role-bridge.sh}" --harness <h> --model "<m>" --effort "<e>" --tools executor --cwd "<primary root>" --prompt-file "$f" --role executor`
     (pass the resolved timeout explicitly — the bridge derives the child's deadline from it, and a
     value loaded in another shell would not reach it)
     `--tools executor` gives the child the tick's own allowlist (`Read,Edit,Write,Bash,Grep,Glob,Task,Skill`),
     so inside that process `superrun`'s task-loop subagents are depth 1 and the synchronous wait holds —
     exactly as it does for this tick's own dispatches. The bridge also lifts the print-mode
     background-wait ceiling (issue #15) for the child.
  3. Exit 0 → stdout **is** `superrun`'s final message (Final Report, CI-PENDING report or
     CHECKPOINT report); parse and relay it exactly as before. Non-zero → the bridge prints `role-bridge: log=<path>` on stderr;
     treat it as a crashed dispatch (escalation ladder, quoting the log path) — never retry blindly.

  **Preflight (once per tick, before the first `superrun` dispatch):** calculate
  `executor_timeout_ms="$(superagent_executor_timeout_ms)"` after loading `.superenv`;
  invalid `SUPER_EXECUTOR_TIMEOUT_MIN` is a configuration error. A `superrun` dispatch may run up
  to `SUPER_EXECUTOR_TIMEOUT_MIN` (default 120 min) — a leaf with fix rounds and a long local test
  gate needs most of it — and the Bash tool kills anything past its cap. `role-bridge.sh` exports
  the dispatch deadline to the child as `SUPER_EXECUTOR_DEADLINE_EPOCH`, so `superrun` yields a
  CHECKPOINT report at a task boundary before the cap rather than being killed mid-task. `scripts/superagent-tick.sh` defaults
  `BASH_MAX_TIMEOUT_MS` to the configured timeout for every external tick; an attended `cron`
  session must be launched with `BASH_DEFAULT_TIMEOUT_MS=3600000` and
  `BASH_MAX_TIMEOUT_MS` at least the configured timeout. Check
  `[ "${BASH_MAX_TIMEOUT_MS:-0}" -ge "$executor_timeout_ms" ]` in Bash; if it fails, do **not** dispatch — reset
  `RUNNING → WAITING FOR RUN`, `stop_driver()`, `release_lock()`, and report the missing env var in
  `Findings & issues` (a dispatch that gets guillotined at 600 s strands a half-done worktree).
<!-- pi-only:start
  On Pi there is no `BASH_MAX_TIMEOUT_MS` env; pass the largest `timeout` the `bash` tool accepts on
  the call itself and skip the env check.
pi-only:end -->

  The child process shares this host's CLI login and plugin set, so `superagent:superrun` and
  `superagent:superbuild` resolve there exactly as here; the `.claude/agents/super-<role>.md` definitions
  `superagent:init` generated resolve from the `--cwd` root as usual.

Either way, instruct the selected child to:

1. invoke the named skill via its **Skill tool**: `superagent:superplan <root>` for ordinary
   planning, `superagent:superrefine <root> <stage-id>` for refinement,
   `superagent:superreplan <root> <record>` for repair, or `superagent:superrun <root>` for
   execution (plus the per-branch CI-resume packet where applicable), and
2. **return that skill's complete Final Report verbatim as its final message** — the subagent's final
   message is what superagent receives as the tool result, and the verbatim report is exactly what the
   per-branch step-5 parsing consumes. (Two sanctioned yields: a `superrun` process that queued
   long CI returns a **CI-PENDING report** instead and exits — see **CI wait — monitor-parked** — and
   one near its wall-clock limit returns a **CHECKPOINT report** — see **Executor checkpoints and
   timeouts**. Each is a valid yield, not a failure; a fresh process resumes it later.)

**Model resolution — every heavy-skill dispatch site passes its selected role's independent
`.superenv` model and effort key.** `superplan` uses PLANNER, `superrefine` uses PLAN_REFINER,
`superreplan` uses REPLANNER, and `superrun` uses EXECUTOR (including ci-resume and retries).
Resolve each key environment > repo `.superenv` > harness default. Equal pins are allowed and do
not couple roles.

*`superrun` (process dispatch):* the bridge takes the CLI's native model string directly, so no
agent definition is involved. In Bash, `. "${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh"` (under bash, never zsh) and pass
`--harness "$(superagent_role_harness "$SUPER_MODEL_EXECUTOR")"` (an `inherit` harness → `SUPER_HARNESS`),
`--model "$(superagent_role_model "$SUPER_MODEL_EXECUTOR")"` (a tier, a full `claude-*` ID, or a
foreign harness's model — all pass through unchanged; `inherit` omits the flag) and
`--effort "$SUPER_EFFORT_EXECUTOR"` (`inherit` omits it). A bridged executor (harness ≠
`SUPER_HARNESS`) is the same command with the foreign `--harness`; the bridge runs that CLI. A
`.claude/agents/super-executor.md` definition, if `superagent:init` generated one, is unused by this
path.

*Planning-role dispatch (`superplan`, `superrefine`, or `superreplan`):*

<!-- cc-only:start -->
- Resolve the matching named type first: `super-planner`, `super-plan-refiner`, or
  `super-replanner`. For a **native Claude** role, use that named definition whenever its model is
  a full `claude-*` ID **or its effort is non-`inherit`**. This is the same predicate init uses to
  generate the definition: source `_common.sh` and apply
  `superagent_native_claude_definition_required "$SUPER_HARNESS" "$model" "$effort"`.
  If the required definition is missing, the selected-role preflight fails; never silently downgrade.
- Only a native Claude tier (`sonnet` | `opus` | `haiku` | `fable`) **with `inherit` effort** may
  use `general-purpose` and pass its tier as `model:`. `inherit` model plus `inherit` effort omits
  the model parameter.
- A **bridged** value (harness prefix or inference ≠ `SUPER_HARNESS`, e.g. `codex:gpt-5.6-sol`,
  `openai/gpt-5`) → dispatch with the matching role `subagent_type` and omit
  `model:`; the generated definition is a relay to that harness's CLI. A Final Report that begins
  `BRIDGE-FAILED` is a failed dispatch — route it through the escalation ladder like any other
  crashed subagent, quoting its `log=` path.
<!-- cc-only:end -->

<!-- cursor-only:start
- Resolve the matching named type first: `super-planner`, `super-plan-refiner`, or
  `super-replanner`. A **native Cursor** role with a non-`inherit` model uses its matching named
  definition; `superagent:init` generated that definition in `.cursor/agents/`. If it is missing,
  selected-role preflight fails; never silently downgrade. A native Cursor `inherit` model uses
  `general-purpose` with no model parameter. Cursor has no native effort transport: warn about a
  non-`inherit` effort and treat it as `inherit`; effort never selects or changes a definition.
- A **bridged** value uses the matching role definition as a relay to the foreign CLI, omits
  `model:`, and requires that relay definition and foreign CLI at preflight. A Final Report that
  begins `BRIDGE-FAILED` is a failed dispatch — route it through the escalation ladder like any
  other crashed subagent, quoting its `log=` path.
cursor-only:end -->

<!-- codex-only:start
- A **native Codex** planning role uses the selected model and effort as `spawn_agent` parameters;
  it has no agent-definition file or native-definition preflight. `inherit` omits the corresponding
  parameter. A **bridged** role spawns the documented relay child and preflight verifies its relay
  route and foreign CLI; do not require a named definition.
codex-only:end -->

<!-- pi-only:start
*Planning roles on Pi (process dispatch):* identical to the `superrun` rule above with that role's
model/effort key, `--tools planner`, and `--role planner|plan-refiner|replanner`. No agent definition
is involved for those three planning/controller roles on this harness.
pi-only:end -->

**Synchronous dispatch — the supervisor WAITS on the tool call; it never polls a running subagent.**
The harness runs Agent-tool subagents in the background by default, which hands back a task handle and
invites `TaskOutput`/`TaskList` status checks while the work runs — for a long selected planning operation or `superrun`
that polling is pure supervisor-context waste. So every heavy-skill dispatch — a Step-1 planning-role
Agent call passes **`run_in_background: false`**; the `superrun` bridge call (Step-1, the ci-resume's
fresh process, an escalation-ladder retry) is a plain **foreground Bash call with `timeout` set to the configured `executor_timeout_ms`**,
never `run_in_background: true` — **blocks until the child's final message returns as the tool
result**. The blocked wait costs zero
context; there is nothing to check on and nothing to do until the report arrives. No `TaskOutput` /
`TaskList` peeks, no sleep loops, no "let me see how it's doing" reads — a poll can only report "still
running", which the synchronous return delivers for free by not having returned yet. A long dispatch
does not starve the loop (ticks fire between turns in `cron` mode and serialize on the lock in
`external` mode), and a subagent facing a genuinely open-ended wait — long CI — does not sit through it
either: it yields a **CI-PENDING report** (see **CI wait — monitor-parked**), so the synchronous call's
duration is bounded by real work. The multi-hour wait belongs to the parked state's Monitor, never to a
polling supervisor.

**Retain that verbatim report — it is relayed, not just parsed.** Parsing it to advance the state
machine (step 5) does not consume it: superagent must keep the exact returned text and reproduce it in
this tick's **Final Report — per tick** so the caller sees it on the CLI, plus surface any issue it
flags. Relaying the *small Final Report* verbatim is exactly the "ingests only the small Final Report"
contract below — it is the report, not the full execution trace.

Do **not** pass `isolation: worktree` to the `superplan` Agent call, and point the `superrun` bridge's
`--cwd` at the primary checkout root, never a worktree — `superplan`/`superrun` create and manage their
own worktrees/PRs, and forcing an outer worktree would conflict with that.

Everything around the dispatch stays in **superagent's own (parent) context, unchanged**: the pre/post
**Sync gate** + **be-sure** verification (L5) run in the parent and verify artifacts on local `main`
*after* the subagent returns; the **overlap lock** (L3) is held by the parent across the whole tick (the
subagent never touches it); and the heavy-step counter increments once in **Step 2**. Isolating the heavy
work is *why* the per-session threshold can be `SUPER_HEAVY_STEP_LIMIT` (default 6) (Step 0.5) — the parent ingests only the small Final
Report per tick (and relays it to the caller), not the full execution trace.

---

## CI wait — monitor-parked (never poll a long CI)

A `superrun` process that pushes a long CI lane does **not** block until CI finishes — per its own
Step 3a it returns a **CI-PENDING report** (leaf plan, root, worktree, branch, PR url, run ids) and
exits; a fresh process resumes the leaf later from that packet. The supervisor's job is to **park
the loop on that wait, not to poll it**:
neither the supervisor's context (a `gh run view` loop) nor the tick cadence (re-checking CI every
tick) may be spent watching a 60–120 min run. One wait = one resume signal.

**Parking (on receiving a CI-PENDING report, in the `WAITING FOR RUN` branch):**

1. Write a `ci_wait:` block into the loop-file frontmatter with these keys: `runs:` (all run ids,
   as an inline list of GitHub Actions run ids), `repo:` (the `owner/name` of the repository the
   runs live in — the PR's **base** repository, e.g. from `gh repo view --json nameWithOwner`; this is
   what lets the wrapper find the runs when the clone's remote is a fork), `branch:`, `pr:`, `leaf:`,
   `worktree:`, the execution snapshot's `plan_generation:`, `stage_id:`, `stage_revision:`,
   `preparation:`, `preparation_digest:`, `vault_commit:`, `reviewed_code_revision:`,
   `source_revision:` and `consumed_deliveries:`, and `since: <ISO-8601 UTC timestamp, e.g.
   2026-08-28T14:05:00Z>`. These are recovery hints copied from superrun's packet; the tracked
   preparation, authoritative history, PR and C8 record remain the evidence. Set
   `status: WAITING FOR CI`. It must look exactly like this:

   ```yaml
   ci_wait:
     runs: [123456, 234567]      # GitHub Actions run ids — inline list; the wrapper's CI gate parses this block
     repo: <owner>/<name>        # where the runs live (PR base repo); the wrapper passes it as `gh run view --repo`
     branch: <branch>
     pr: <number>
     leaf: <plan path>
     worktree: <path>
     plan_generation: <N>
     stage_id: <ID>
     stage_revision: <N>
     preparation: <report path>
     preparation_digest: <sha256>
     vault_commit: <sha>
     reviewed_code_revision: <sha>
     source_revision: <revision>
     consumed_deliveries: <contract IDs and receipt paths>
     since: <ISO-8601 UTC timestamp>
   ```

   `ci_wait:` must be a top-level frontmatter key with `runs:` indented beneath it (not a `{…}`
   flow mapping) — that is the shape `superagent-tick.sh`'s `SUPER_CI_GATE` reads. `since:` must be
   ISO-8601 UTC: the wrapper compares it against `SUPER_CI_MAX_WAIT_MIN` (default 180) and, once a
   park is older than that with runs still not `completed`, notifies the operator once (`ci-stale`)
   and lets the session run each interval so a run stuck in `queued`/`waiting` cannot park the loop
   silently forever. A session that lands in the external branch with runs still running should
   treat that as the stale case: inspect the runs (`gh run view <id>`), and either re-park with a
   fresh `since:` if they are genuinely progressing, or cancel/re-trigger and re-park.
2. **Arm the resume signal — by driver:**
<!-- cc-only:start -->
   - **cron (in-session):** arm **one `Monitor`** (`persistent: true`) that `curl`s
     `https://api.github.com/repos/<owner>/<repo>/actions/runs/<id>` for **each** id in `ci_wait.runs`
     (auth: `TOK=$(gh auth token)` captured before arming — prefer `curl` for polling inside a Monitor:
     on hosts where `SUPER_GH_DISABLE_SANDBOX=true`, `gh` cannot run *inside* the Monitor at all (it
     needs keychain access), so `curl` to `api.github.com` is the only option there; where
     `SUPER_GH_DISABLE_SANDBOX=false`, `curl` is still preferred for consistency) and fires the
     first time **every** run is `status: completed`, emitting each `id: conclusion` pair. It MUST
     emit on **any** terminal state (success / failure / cancelled / timed_out) — a success-only
     filter is silent through a crash, and silence looks like "still running". Then **suspend the
     tick cadence for the wait**: `CronDelete cron_id`, clear `cron_id`, and log `parked on CI —
     cron driver suspended, Monitor armed`. No ticks fire while parked; the Monitor's fire is the
     only resume signal.
<!-- cc-only:end -->
   - **external:** the tick is a fresh headless session — a Monitor cannot outlive it, and the
     scheduler is user-managed (never touched). The scheduler keeps firing ticks; the `WAITING FOR
     CI` tick branch (Step 1) is the cheap check.
3. **`release_lock()` and end the tick** (report the parking in this tick's Final Report). The lock
   is NOT held across the wait — a multi-hour CI must never age the lock into L3's `SUPER_LOCK_STEAL_MIN`-minute (default 90) steal.

**Resuming (all runs terminal):**

1. Entry points: the **Monitor fired** (cron — harness re-invokes the session), or an **external
   `WAITING FOR CI` tick's one batched curl** found every run `completed`, or a **form-(B) RESUME**
   found `status: WAITING FOR CI` (see below). `acquire_lock()` if not already held this tick.
2. Run `sync_main()` / `sync_vault()` and reconcile C8 plus the execution snapshot against the
   authoritative root **before** dispatching a resume process. A pending batch or an adopted request
   being durably published pauses this PR even when all runs are green. Ensure its record preserves the
   PR/branch/worktree/run ids and snapshot, set `status: WAITING FOR PLAN`, and do not resume a merge
   while the stage disposition is unresolved. After a published batch, resume only through its explicit
   disposition. An explicitly retained same execution identity may continue post-CI after its focused
   new-generation validation. A mapped `resume-existing` successor is redirected through superrun's
   normal prepared-stage execution on the reused branch/worktree, with a successor snapshot and its own
   remaining tasks/reviews/tests; the old packet is historical and cannot authorize direct merge.
   Otherwise preserve the old PR history and route to replanning/reconciliation.
3. Verify the conclusions independently (one `gh run view <id>` per run — with the sandbox override if
   `SUPER_GH_DISABLE_SANDBOX=true` — or the same batched curl) — never advance on the Monitor's report
   alone.
4. **Resume `superagent:superrun`:** the process that yielded has exited, so there is nothing to
   message — dispatch a **fresh** `superrun` process exactly as in `WAITING FOR RUN` step 3 (bridge,
   `--tools executor`, foreground Bash, `timeout: "$executor_timeout_ms"`; model per **Model resolution** under
   **Subagent dispatch**, from `SUPER_MODEL_EXECUTOR`), with a prompt that instructs it to invoke
   `superagent:superrun` with the full `ci_wait` packet + each run's conclusion via its
   **Resume entry — post-CI**. It returns the real Final Report.
5. Continue the normal `WAITING FOR RUN` steps 4–6 on that report (sync gate post + be-sure, parse →
   next state, iteration log). Clear the `ci_wait:` block.
   **cron:** re-arm the driver (`CronCreate`, record the new `cron_id`) so ticks resume. <!-- cc-only -->
6. The heavy-skill count for this leaf was already incremented on the tick that dispatched
   `superrun` (Step 2); the park and resume ticks increment `iteration` but **not**
   `session_skill_count` again.

<!-- cc-only:start -->
**RESUME / restart while parked (form B, or a fresh cron session):** a persisted `WAITING FOR CI`
whose Monitor died with its session is recovered on the standard RESUME path — check the recorded
runs once (batched curl or `gh run view`): all terminal → run the resume flow above this tick; any
still running → re-arm the **Monitor** (cron — but do **not** `CronCreate` a driver while parked; the
Monitor is the sole resume signal, and the driver is re-armed on ci-resume) or just report the parked
state (external — the scheduler's ticks keep checking) and exit.
<!-- cc-only:end -->
<!-- cursor-only:start
**RESUME / restart while parked (form B):** a persisted `WAITING FOR CI` is recovered on the standard
RESUME path — check the recorded runs once (batched curl or `gh run view`): all terminal → run the
resume flow above this tick; any still running → report the parked state (the scheduler's ticks keep
checking) and exit.
cursor-only:end -->
<!-- codex-only:start
**RESUME / restart while parked (form B):** a persisted `WAITING FOR CI` is recovered on the standard
RESUME path — check the recorded runs once (batched curl or `gh run view`): all terminal → run the
resume flow above this tick; any still running → report the parked state (the scheduler's ticks keep
checking) and exit.
codex-only:end -->

---

## Step 1 — Dispatch on `status` (invoke AT MOST ONE skill this tick)

### `DONE`
A tick fired after completion (form A already no-ops `DONE` before Step 1; this covers the cron path).
Report it, **do not change status**, `stop_driver()`, `release_lock()`, and exit. (Script-driven
external loops: the tick wrapper self-disarms the scheduler entry after this session ends — never run
`uninstall-timer.sh` from inside the session; see superloop L2/`stop_driver()`.)

### `WAITING FOR INPUT`
A prior iteration escalated a decision the panel could not resolve, or a protected-change request
the panel chose to ask. Read the `## Pending decision` block.
- **Answer supplied** (recorded under `## Pending decision`, or given in the re-invoking
  `/superagent` prompt) → append it to `## Decisions`, clear the pending block, restore `status` from
  `prior_status`, and **fall through** to that branch this tick, applying the decision as guidance to
  the next skill invocation. A one-word answer naming an option is complete: apply that option as the
  block described it, and never ask the owner to restate it as disposition text. For a
  protected-change request, `yes` approves exactly the change in the block, `yes <value>` the same
  change with that value, and `no` takes the block's no path; record the approved change verbatim
  (files, old → new, the answer as written). A `yes` to narrowing or postponing an acceptance case is
  recorded the same way and carried into the re-plan as `[owner]` authority for that change only.
- **No answer yet** → branch on context:
  - **Interactive (a person is at the session — typically `cron`/attended):** `AskUserQuestion`. On an
    answer, proceed as above. If it genuinely can't be answered, **pause** (`stop_driver()`),
    `release_lock()` — a later `/superagent <PLAN.md>` resumes.
  - **Non-interactive scheduled tick (external Desktop/headless CLI, fresh session — no one to
    prompt):** do **not** block on `AskUserQuestion` (in a headless `claude -p` tick
    there is no TTY to answer, so it would stall the one-shot session). Ensure `## Pending decision`
    is in superloop L7's **required shape** — what failed, most likely cause, recommended option
    first, other options, and an explicit *"write your choice as `answer: <option>` under this
    block"* instruction, with identifiers in the trailing reference list. A block about a
    specification gap also states which acceptance case depends on it and recommends a scope remedy
    when one avoids it. Then `release_lock()`, and exit.
    The scheduler keeps firing, but for loops driven by the shipped `scripts/` wrapper the fire is
    **free while unanswered**: `superagent-tick.sh` reads the loop file in bash and exits without a
    session until an `answer:` line exists under `## Pending decision` (`SUPER_INPUT_GATE`, default
    on); it also notifies the operator once on the transition (`SUPER_NOTIFY_CMD`, else a desktop
    notification). A human answers **and resumes immediately** with
    `$SUPERAGENT_SCRIPTS/answer.sh <slug> "<option>"` (writes the line under the lock, kicks a tick),
    from `superagent:superagent-monitor`, or by editing the loop file directly (next scheduled fire
    resumes).

### `PLANNING` or `RUNNING` (crash recovery)
These are transient *within* a tick (superagent sets them, runs the skill synchronously, then sets the
next status — all in one turn). Ticks never overlap: in `cron` mode they fire between turns; in
`external` mode the **lock** serializes them. So a **persisted** `PLANNING`/`RUNNING` means a crashed
prior tick (which also left a stale lock that `acquire_lock()` steals immediately when its recorded
owner PID is dead, or after `SUPER_LOCK_STEAL_MIN` minutes (default 90) only when no valid owner PID was recorded)). **Self-heal:** log
a recovery note, then reconcile authoritative artifacts before redispatch. `PLANNING` reconciliation
uses the tracked root/record and may recover a published preparation/replan instead of repeating it.
`RUNNING` reconciliation inspects the actual branch/PR/main history and execution snapshot: a merged
delivery with missing closeout routes to superrun's closeout recovery, an existing delivery receipt is
reused, and open/CI-pending work resumes its recorded integration path. Never rerun implementation
solely because the final response was lost. After reconciliation, reset `PLANNING → WAITING FOR PLAN` /
`RUNNING → WAITING FOR RUN` and fall through to that branch this tick. (`WAITING FOR CI` is **not** a
crash — it is the durable parked state; see its own branch.)

The same mapping applies **in-flight**: if this tick's own dispatch is interrupted and the step cannot
be completed (superloop L2, tick teardown invariant), apply the reset **now** — log the interruption,
reset the transient status to its ready state, `release_lock()`, and end the tick with a normal
report so the next tick retries. Never end the tick asking what to do, and never leave
`PLANNING`/`RUNNING` persisted on a normal exit.

### Executor checkpoints and timeouts
A `superrun` dispatch killed at `SUPER_EXECUTOR_TIMEOUT_MIN` (the Bash call timed out, or the bridge
reported the child killed) is an in-flight interruption, handled as above. In addition, identify
the leaf — from the `checkpoint:` or `ci_wait:` block when one names it, else the target of
supertraverse execution-mode descent over the synchronized root — increment
`executor_timeouts.count` for it (reset it to 1 when the leaf differs from `executor_timeouts.leaf`),
and name in this tick's `Findings & issues` the longest command the leaf's ledger records (its
`Long command:` lines, read from `superbuild.sh workspace <leaf>` in its worktree, or `unknown` if
none is readable). From the second consecutive timeout on, every dispatch for that leaf carries
single-step guidance (`WAITING FOR RUN` step 3). This never escalates to the owner: a timeout is an infrastructure limit, not a decision. If
single-step dispatches still time out, report the longest command and suggest raising
`SUPER_EXECUTOR_TIMEOUT_MIN` in `Findings & issues`, and keep dispatching.

### `WAITING FOR CI` (parked — the cheap branch)
The loop is parked on the run ids in `ci_wait.runs` (see **CI wait — monitor-parked**).
First synchronize authoritative code/vault state and reconcile C8 against the packet's execution
snapshot. This request-recovery check precedes the driver-specific CI query. If an adopted batch is
being committed or the root has a pending Active replan, preserve the packet's PR/worktree/run history
in that record, move to `WAITING FOR PLAN`, and end without dispatching post-CI superrun. Green CI never
bypasses the barrier. Missing/conflicting identity enters the existing decision ladder.
<!-- cc-only:start -->
- **cron, when reconciliation found no barrier change:** the Monitor owns the wait. After the
  authoritative check, `release_lock()`, exit. No `gh`, no `curl`, no subagent. (Normally no cron tick even fires here — the driver was suspended at
  parking; this covers a straggler tick or a manual `--tick`.)
<!-- cc-only:end -->
- **external:** run **one batched `curl`** over all ids in `ci_wait.runs` (auth `gh auth token` — with
  the sandbox override if `SUPER_GH_DISABLE_SANDBOX=true`; this is the only network call this tick).
  - (Loops driven by the shipped `scripts/` wrapper normally never reach this branch while a run is
    still in progress: `superagent-tick.sh` performs the same `gh run view` check in bash before
    launching the session and exits 0 while any run is not `completed` — `SUPER_CI_GATE`, default
    on. A session that does land here with runs still running means the gate was off, `gh`
    failed in the wrapper, or the park exceeded `SUPER_CI_MAX_WAIT_MIN` (stale wait — see
    **Parking**); do the single query as written, and in the stale case decide whether to re-park
    with a fresh `since:` or cancel/re-trigger the run.)
  - Any run still not `completed` → `release_lock()`, exit. Nothing else this tick.
  - All terminal → run the **Resuming** flow (CI wait — monitor-parked) this tick: verify, dispatch
    the resume process, then continue `WAITING FOR RUN` steps 4–6 on its Final Report.

### Repair reconciliation — before either ready-state dispatch

After the pre-sync gate in `WAITING FOR PLAN` or `WAITING FOR RUN`, reconcile adopted re-plan
Decisions with the authoritative tree using **supertraverse C8**. This also applies after crash
recovery and a resumed user decision. Apply missing requests; reconcile partial publications;
reuse already-published successors. Clear `plan_exhausted` when a repair is newly requested.
Also inspect newly integrated delivery receipts/findings before selection: a verified contract or
assumption contradiction invalidates affected unfinished preparation and enters the existing
decision/adoption path; a routine finding that preserves commitments creates no planning operation.
If reconciliation changes the ready state, run that state's dispatch instead. Never dispatch a
normal traversal against a log-only repair decision. Ambiguous or uncommitted repair state goes
to the decision ladder; no queue exhaustion or DONE transition is allowed from that state.
In local mode, "committed" in this paragraph means durably written and reopened per C8/A7. Replay a
published decision by its stable Decision ID and existing Successor link; never reset it or create a
second successor after a crash.

### `WAITING FOR PLAN`
1. **Sync and reconcile first.** In `github`, run `sync_main()` (then `sync_vault()` for an external
   vault). In `none`, apply L5's local ownership and filesystem-evidence branch without any git or
   GitHub operation. Reconcile C8 and any persisted `PLANNING` hints against authoritative durable
   root/record artifacts, and clear
   stale hints. Artifacts override hints. A missing/ambiguous graph or record enters the existing
   decision ladder; never choose a role from state alone.
2. **Select before dispatch.** A reconciled adopted C8 legacy repair has priority over ordinary
   incremental descent and selects `superreplan <root> <record>` / REPLANNER. Otherwise, an
   unmarked or explicit incremental root selects ordinary descent and `superplan` / PLANNER. For an
   upfront root: a committed pending batch selects
   `superreplan <root> <record>` / REPLANNER; the first dependency-eligible stage whose S5 result is
   NEEDS-REFINEMENT selects `superrefine <root> <stage-id>` / PLAN_REFINER; a valid prepared target
   sets `status: WAITING FOR RUN`, clears planning hints, records the target, and ends this branch
   with **zero** heavy dispatches. If the upfront selector finds none of those three targets, run
   **supertraverse C9 now** against the synchronized authoritative tree; do not dispatch PLANNER just
   to manufacture an exhaustion result. C9 **complete** sets `plan_exhausted: true` and `status:
   DONE`, records the audited integration/disposition evidence, and ends the branch with zero heavy
   dispatches. C9 **incomplete** must name the still-active planning or execution obligation: clear
   `plan_exhausted`, remain in `WAITING FOR PLAN`, and reselect that concrete refinement, repair, or
   prepared execution target under this same selection contract. C9 **BLOCKED**, including the case
   where every remaining obligation is dependency-blocked, enters the existing decision ladder and
   never sets DONE or polls an empty loop. REPLAN-REQUIRED and BLOCKED take the decision ladder before
   any generic `none`/success handling. A broken/missing upfront tree is BLOCKED, never incremental
   gap filling.
3. **Selected-role-only preflight.** Before writing `PLANNING`, resolve only the selected role's
   harness, model, effort, and dispatch form. Check the prerequisite required by that harness's rule
   in **Model resolution**: the native Claude definition selected by its predicate, the native Cursor
   non-`inherit` definition, a bridged relay and foreign CLI, or the selected Pi bridge CLI. Codex
   native roles have no definition prerequisite. Do not inspect or require unused role definitions.
   On failure, keep/restore `WAITING FOR PLAN`, preserve no new planning hints, record zero heavy
   dispatches and the selected role/target failure, then invoke the existing decision ladder as the
   **next** controller action. This immediate preflight observation is not a replacement for the
   ladder, and never substitutes PLANNER or EXECUTOR.
4. Only after that preflight succeeds, set `status: PLANNING` and persist `planning_operation`
   (`refine` or `replan`), target, current root generation, and C8 record when applicable. For legacy
   PLANNER authoring persist `planning_operation: none`. Dispatch exactly that skill with exactly its
   role's resolved model/effort; see **Subagent dispatch**. On Pi, use a blocking
   `role-bridge.sh --tools planner --role planner|plan-refiner|replanner` process. On other
   harnesses, native/bridged definitions or Codex spawn pins apply as documented there.
   In local mode, include the recorded git mode, physical project root, and inherited workspace
   identity in the prompt, and explicitly require local A7 publication with no git/GitHub stages.
5. **Post-dispatch.** Run the mode-selected post-sync/be-sure gate for the reported leaf, receipt/report, record,
   parent rows, and any A7 artifacts, then relay the complete Final Report. PREPARED moves to
   `WAITING FOR RUN`; a published/finished replan or a legacy repaired successor moves to
   `WAITING FOR PLAN`; REPLAN-REQUIRED, BLOCKED, contradictory evidence, and bridge failure use the
   existing decision ladder. For `superreplan`, a **BLOCKED** outcome — whether or not it published a
   record-only checkpoint — increments `replan_stalls.count` for its originating stage (reset to 1
   for a different stage; a superseding request record for the same stage keeps the count) and is
   recorded under `## Decisions` as `replan stall <n> · <stage> · <record> — <one-line reason>`, so
   superloop L7's repeat check sees it. PUBLISHED or ALREADY-PUBLISHED resets the counter;
   REFINEMENT-ONLY leaves it unchanged. Pass the replanner's **Remedies considered** line into the
   ladder's packet. A BLOCKED whose Remedies considered recommends remedy 2 or 3 (narrow or postpone
   an acceptance case) goes to Rung 2 as that yes/no question, and a BLOCKED naming a genuine
   specification gap with candidate values goes to Rung 2 as a choice among those values — each with
   the record path in the block's reference list. Re-plan on that stage then needs a named material
   difference even at the first stall. The owner's answer is applied as Re-plan, carried as `[owner]`
   authority for exactly that answer. For ordinary legacy superplan, parse and persist every successful result
   explicitly: a published **implementation plan** sets `status: WAITING FOR RUN` and
   `plan_exhausted: false`; a published **seed/master or sub-master plan** sets `status: WAITING FOR
   PLAN` and `plan_exhausted: false`; `No available task to plan — every step is completed or already
   has a plan` sets `status: WAITING FOR RUN` and `plan_exhausted: true`, so the executor's `none`
   result reaches the C9 guard below. A `not-traversable` result or missing required plan input is a
   hard error: record it, stop/tear down the driver per Step 2, and never invent a next target.
   Append the iteration log and go to **Step 2**.

### `WAITING FOR RUN`
1. **Sync gate (pre).** In `github`, run `sync_main()` (then `sync_vault()` in external vault mode).
   In `none`, apply L5's local ownership and snapshot branch. The traversal must read authoritative
   current bytes. If the selected gate STOPs, pause and end this tick.
2. Set `status: RUNNING`, write the loop file.
3. **Dispatch `superagent:superrun` in its own CLI process** — **not** an Agent-tool subagent: run
   `role-bridge.sh --tools executor` from your Bash tool, foreground, `timeout: "$executor_timeout_ms"`, after the
   `BASH_MAX_TIMEOUT_MS` preflight (all in **Subagent dispatch**). Model per **Model resolution**
   (see **Subagent dispatch**), from `SUPER_MODEL_EXECUTOR`.
   The prompt instructs it to invoke the `superagent:superrun` skill (Skill tool) with
   `<PLAN.md> = master_plan` (the root) and to **return superrun's complete Final Report verbatim as its
   final message** (step 5 parses that report) — or, if it queues long CI, its **CI-PENDING report**
   (step 5's park case; a fresh process resumes it), or its **CHECKPOINT report** (step 4). superagent
   never invokes `superrun` inline in its own context, and never as a subagent (issue #25).
   If the loop file holds a `checkpoint:` block, the prompt instead instructs `superrun` to take its
   **Resume entry — checkpoint** with that packet. Whenever `executor_timeouts.count` is 2 or more
   for the target leaf, either prompt also carries **single-step guidance**: run only the next ledger
   step, then return CHECKPOINT.
   In local mode, prepend superrun's exact local-mode override, the physical project root, and the
   inherited workspace identity. The executor must capture before/result manifests and return a
   verified `completed-local` receipt; it must retain all local test, task-review, final-review, and
   acceptance gates while suppressing worktree/commit/PR/merge/finishing stages.
4. **Classify before delivery-specific be-sure.** Retain `superrun`'s verbatim report for relay (it is
   reproduced in this tick's **Final Report — per tick**) and note every issue it surfaces. A
   **CI-PENDING report** takes the Parking flow immediately; nothing merged, so the post-sync/be-sure
   runs on the resume tick instead. A **CHECKPOINT report** is a yield too: write its fields into a
   `checkpoint:` block, set `status: WAITING FOR RUN`, and end result handling — the next tick's
   dispatch resumes it. A CHECKPOINT returned without single-step guidance resets
   `executor_timeouts.count` to 0; one returned under single-step guidance keeps the count, so the
   leaf stays on single steps until it finishes. Any other `superrun` report clears the
   `checkpoint:` block and resets `executor_timeouts`. For every other report, run the mode-selected L5 post gate,
   classify the report, and reconcile any artifacts it actually names. Before
   applying any delivery-specific be-sure requirement, route no-execution outcomes:

   - **NEEDS-REFINEMENT at execution entry** means superrun stopped before implementation because the
     prepared receipt is missing or needs compatible-baseline revalidation. It legitimately has no
     closeout or delivery evidence. Set `status: WAITING FOR PLAN`, `plan_exhausted: false`, and persist
     `planning_operation: refine`, the reported root generation, and the reported stage as
     `planning_target`; end result handling without requiring a closeout and without dispatching a
     second heavy skill in this tick. The next tick selects PLAN_REFINER through the normal
     `WAITING FOR PLAN` branch.
   - **REPLAN-REQUIRED, BLOCKED, unresolved code PR, CI-red, contradictory evidence, or another
     non-success report** follows its existing decision/recovery path after reconciling only artifacts
     it actually reports. None may be rejected merely because a closeout that the outcome does not
     claim is absent.
   - **`none`** (no execution target, with no higher-priority blocker) claims no delivery and requires
     no closeout. If `plan_exhausted` is false, set `status: WAITING FOR PLAN`. If true, invoke
     **supertraverse C9** on the synchronized tree: **complete** sets `status: DONE` and records the
     audited integration/disposition evidence; **incomplete** clears `plan_exhausted` and sets
     `status: WAITING FOR PLAN`; **BLOCKED** enters the decision ladder with its concrete blockers.
     An empty queue pair is only a reason to audit, never sufficient to set DONE.
   - Only a report that claims complete delivery, partial execution, or evidence-only discovery
     completion proceeds to the delivery be-sure gate in step 5.

5. **Delivery be-sure, then successful-result routing.** For a delivery/partial-execution claim,
   verify `superrun`'s reported artifacts landed. In `github`, the leaf's closeout record exists and is tracked (on
   local `main` for an internal vault; in the vault repo for an external one — L5's two-kind rule) and
   matches the execution snapshot. For partial execution, verify its open PR/head/CI identity and
   explicit non-delivered/non-consumable result. For complete delivery, verify delivered contract
   revisions and (if the code PR merged) its squash commit is in `origin/main` history. A merged code
   PR but stale local `main` is the exact bug this gate exists for — reconcile (ff-pull) or escalate.
   In `none`, replace merge/tracking proof with reopening the completed-local receipt, both manifests,
   every reported command/review artifact, and the changed/deleted path evidence.
   Do not advance on an unverified merge, and surface the failure in this tick's `Findings & issues`
   line. **A BLOCKED/inconsistent repair report takes precedence over any `none` phrase**: run the
   decision ladder, not the exhaustion branch. Otherwise parse the successful result:

   - **Executed a leaf** (identity-bound complete delivery receipt or partial closeout verified; for
     evidence-only discovery, required evidence/decision A7 publication verified without requiring a
     code PR) → `status: WAITING FOR PLAN`,
     `plan_exhausted: false` (more may remain to plan/run).
6. Append an iteration-log entry (skill, result, and `github` PR URLs or `none` receipt/snapshot
   paths) of at most three lines (superloop L1: *Keep the loop file small*). Go to **Step 2**.

---

## Step 2 — Persist, then let the driver continue (or stop it)

1. Increment `iteration`. **If a heavy skill (superplan, superrefine, superreplan, or superrun) was invoked this tick, increment
   `session_skill_count`** (the Step 0.5 handoff trigger; guard / escalation / handoff ticks that ran
   no heavy skill do **not** increment it). A parked leaf counts **once**: the tick that dispatched
   `superrun` (and then parked on its CI-PENDING yield) increments; the later ci-resume tick — even
   one that dispatches a fresh resume subagent — does **not** increment again. Write the loop file (frontmatter + appended log). Plain
   Write — no commit, no PR (the file is gitignored).
2. **Terminal** (`DONE`, hard error, or `WAITING FOR INPUT` unanswered in an unattended run): print a
   final summary (plus the pending question + resume instructions for the input case) and
<!-- cc-only:start -->
   `stop_driver()` (cron → `CronDelete`; external → on `DONE` the shipped tick wrapper self-disarms
   the scheduler entry after the session; Desktop-routine or hand-rolled schedulers → instruct the
   user to disable the routine). No more
<!-- cc-only:end -->
<!-- cursor-only:start
   `stop_driver()` (on `DONE` a shipped-script-driven scheduler entry self-disarms after the session;
   otherwise instruct the user to disable the scheduler entry). No more
cursor-only:end -->
<!-- codex-only:start
   `stop_driver()` (on `DONE` a shipped-script-driven scheduler entry self-disarms after the session;
   otherwise instruct the user to disable the scheduler entry). No more
codex-only:end -->
   ticks fire.
3. **Otherwise**: do nothing to the driver — the next `--tick <loop-file>` fires on its own (the
   in-session `cron` job, or the external Desktop routine / OS-cron entry, depending on `driver`).
4. **Always `release_lock()`** before the turn ends — terminal or not.
5. **Teardown invariant (superloop L2):** the persisted `status` at end-of-turn is never a
   `PLANNING`/`RUNNING` this tick wrote (an interrupted dispatch is reset to its ready state
   in-flight, using the mapping defined in Step 1's crash-recovery branch), and the turn never ends
   with a question — a decision needing the user ends only via `WAITING FOR INPUT` + `## Pending
   decision`. The external tick wrapper enforces this: a `0`-exit session that leaves a transient
   status (with no live peer tick holding the lock) is re-flagged as a loud failed tick (exit 10).

**One-skill-per-iteration is structurally guaranteed:** a `--tick` runs Step 1 → at most one selected
planning operation or `superrun` → Step 2. Ticks never overlap — in `cron` mode they fire between turns; in
`external` mode the **lock** serializes fresh-session ticks (a long tick just makes the next fire
no-op until the lock releases). Ticks are idempotent — a tick that finds nothing to do no-ops.

---

## Drivers — attended (in-session) vs Desktop/headless (clean context)

The two drivers (Driver A `cron`, Driver B `external`), the context model, the overlap lock
(`acquire_lock()` / `release_lock()`), and `stop_driver()` are **superloop L2 + L3**. superagent arms
`/superagent --tick <loop-file>` as its tick prompt (`<consumer>` = `superagent`).

<!-- cc-only:start -->
**Running from the Claude CLI.** For `external` mode the tick fires
in a fresh headless `claude -p` session per interval; because print mode cannot run slash commands, and
Skill-tool semantics for a disable-model-invocation skill in headless print mode are unverified, the
scheduler drives it by asking the CLI to *read `skills/superagent/SKILL.md` directly (at the plugin's
installed location) and run exactly one `--tick`* (superloop L2, Driver B). The loop's own internal
`superagent:superplan` / `superagent:superrun` dispatches still go through the Skill tool once the
session is running. `${CLAUDE_PLUGIN_ROOT}/scripts/` packages the whole
thing (the tick wrapper, a per-goal scheduler entry — systemd user timer on Linux, launchd
LaunchAgent on macOS — and
bootstrap/install/uninstall/console-watch/status helpers); the runbook is
[scripts/README.md](../../scripts/README.md), which documents the `SUPERAGENT_SCRIPTS` convention
runnable examples use to locate this plugin's installed `scripts/` directory. Monitor and control
running loops (multi-instance: list state, answer `WAITING FOR INPUT`, drain/stop/uninstall/re-arm) with
the `superagent-monitor` skill. The driver must never `--resume` (fresh
context per tick — L4 is a no-op in `external` mode, so the loop runs straight to `DONE`); an
interactive monitoring/answering console is a separate plane that can be started/stopped independently.
<!-- cc-only:end -->
<!-- cursor-only:start
**Running from the Cursor CLI.** For `external` mode the tick fires in a fresh headless `agent -p`
session per interval; the scheduler drives it by asking the CLI to *read `skills/superagent/SKILL.md`
directly (at the plugin's installed location) and run exactly one `--tick`* (superloop L2, Driver B).
The loop's own internal `superagent:superplan` / `superagent:superrun` dispatches still go through the
skill mechanism once the session is running, so the plugin must be installed and enabled for headless
sessions (or passed via `--plugin-dir`). **Port status:** the shipped `scripts/` wrappers still invoke
the Claude CLI — until they are ported, schedule the Driver B `agent -p` recipe directly. The driver
must never `--resume` (fresh context per tick — L4 is a no-op in `external` mode, so the loop runs
straight to `DONE`); an interactive monitoring/answering console is a separate plane that can be
started/stopped independently.
cursor-only:end -->
<!-- codex-only:start
**Running from the Codex CLI.** For `external` mode the tick fires in a fresh headless `codex exec`
session per interval; the scheduler drives it by asking the CLI to *read the supervisor's SKILL.md
directly (at the plugin's installed location —
`<marketplace-root>/plugins/superagent/skills/superagent/SKILL.md`) and run exactly one `--tick`*
(superloop L2, Driver B). The loop's own internal `superagent:superplan` / `superagent:superrun`
dispatches still go through the skill mechanism once the session is running, so the plugin must be
installed via the Codex plugin marketplace (`codex plugin marketplace add <plugin-repo>/codex`, then
`codex plugin add superagent@superagent`) — there is no per-invocation `--plugin-dir` analog. The
shipped `scripts/` wrappers are harness-aware: `SUPER_HARNESS=codex` makes `superagent-tick.sh` fire
`codex exec` (sandbox per `SUPER_CODEX_SANDBOX`, default `danger-full-access`; auth via `OPENAI_API_KEY`
in `.env` or the CLI's stored login). The driver must never resume a prior session (fresh context per
tick — L4 is a no-op in `external` mode, so the loop runs straight to `DONE`); an interactive
monitoring/answering console is a separate plane that can be started/stopped independently.
codex-only:end -->
<!-- pi-only:start
**Running from the Pi CLI.** For `external` mode the tick fires in a fresh headless `pi -p` session
per interval; the scheduler drives it by asking the CLI to *read `pi/skills/superagent/SKILL.md`
directly (in the plugin repository's generated Pi build) and run exactly one `--tick`* (superloop
L2, Driver B). The plugin's skills are delivered per run with `--skill <plugin-repo>/pi/skills` —
no install step and no other skill package. The shipped `scripts/` wrappers are harness-aware:
`SUPER_HARNESS=pi` makes `superagent-tick.sh` fire `pi -p --approve --skill … [--model] [--thinking]`
and export `SUPERAGENT_BRIDGE`, `SUPERAGENT_FANOUT`, and `SUPERAGENT_PI_SKILLS` for the bridge
children. The driver must never resume a prior session (fresh context per tick — L4 is a no-op in
`external` mode, so the loop runs straight to `DONE`); an interactive monitoring/answering console is
a separate plane that can be started/stopped independently.
pi-only:end -->

---

## Decision-escalation ladder — autonomy posture

Resolve raised decisions per **superloop L7** (Rung 1 = 3-subagent panel, ≥2/3 converge; Rung 2 = user
escalation via `WAITING FOR INPUT` / `AskUserQuestion` / durable `answer:` polling). superagent's
**trigger surface**: a CRITICAL / ⚠️ finding, a `not-traversable` result, or a `superrun` BLOCKED /
CI-red Final Report, failed completion audit, or unreconciled repair. superagent's **option-set**:

- **Re-plan:** apply **supertraverse C8** and verify the durable request before routing to
  `WAITING FOR PLAN`. Logging the vote alone does not implement this outcome. The guidance it carries
  is bounded (superloop L7 *Re-plan guidance is bounded*) and reaches the replanner tagged
  `[planner]`. When `replan_stalls.count` is 2 or more for the request, re-plan is available only if
  the packet names what is materially different from the last attempt; otherwise the options are
  the replanner's scope remedies (narrowing or postponing the case as a yes/no owner question) and
  decline/defer — prefer the scope remedy, and decline/defer only when none of remedies 1–3 applies.
  A test-scoped substitute the replanner has not already rejected, or an owner `yes` to narrowing or
  postponing, is applied as Re-plan and counts as the material difference.
- **Retry:** only retry a still-eligible execution target or an explicit supported resume packet.
  If closeout already removed the leaf from descent, use C8 to author a successor containing
  the retry/integration guidance; a blind root superrun retry would return none again. A retry after
  a cap whose blocked attempt left an open PR does not need C8: dispatch `superrun` (as in
  `WAITING FOR RUN` step 3) with the blocked attempt's packet and the cap summary's smallest change
  via its **Resume entry — targeted round**. At most one targeted round per open finding per leaf;
  a finding still open after it goes to a protected-change request or a re-plan. A retry may relax a
  `[planner]` constraint the panel recorded as relaxed.
- **Decline/defer:** record adopted authority, rationale and PR disposition in tracked findings
  and the target row; mark outstanding repair records resolved with that adopted disposition
  and reconcile ancestors. This is an intentional
  scope disposition, not a claim of code integration. Clear `plan_exhausted` and re-audit later.
- **Request approval for one specific protected change:** when `superrun`'s CI triage or blocker,
  or the panel, names a fix that touches a protected surface (a `SUPER_PROTECTED_PATHS` match, an
  approved acceptance row, or a value the project's instructions pin). The panel may select this
  option but never approves the change: selecting it writes the yes/no protected-change block
  (superloop L7 Rung 2) naming the files, old and new value, the evidence in two or three lines, and
  what happens on yes and on no, and its reference list carries the blocked attempt's resume packet
  (leaf, root, worktree, branch, PR, execution snapshot) — or, for a replanner's narrow/postpone
  recommendation, the request record path. On `yes` / `yes <value>`, record the
  approved change verbatim under `## Decisions`, set `status: RUNNING`, and dispatch a fresh
  `superrun` process exactly as in `WAITING FOR RUN` step 3 with that packet and the approved change
  via its **Resume entry — approved protected change** — not as Retry, because the blocked leaf is
  no longer an eligible target and the change belongs on its open PR. Handle its report like any
  other `superrun` report (a CI-PENDING report parks). The approval is authority for that change
  only. When the approved change narrows or postpones an acceptance case (superreplan remedies 2–3),
  apply it as **Re-plan** instead, carrying the approval as `[owner]` authority for exactly that
  change. On `no`, take the route the block named (decline/defer or re-plan).

Apply the same transitions for a converged panel and a resumed human answer. Persist and verify
plan-tree changes under A7 before the ready-state loop write; recovery is C8's idempotent replay.

**Always surface the outcome to the caller.** Whenever the ladder fires — even when the Rung-1 panel
resolves it **autonomously** — name the triggering issue and how it was resolved (e.g. "panel 2/3:
re-plan") in this tick's `Findings & issues` line. Recording it under `## Decisions` in the gitignored
loop file is not enough: the caller must learn that an issue arose and what the loop did about it. (A
Rung-2 escalation additionally populates the `⚠️ Needs you` block.)

---

## Final Report — per tick

After each tick, report to the caller and end the turn. The report has two jobs beyond the tick header:
**(a) relay the delegated skill's verbatim Final Report** so the caller sees on the CLI exactly what
the selected planning operation or `superrun` produced — the rich output (files created/modified,
findings, PRs) that would
otherwise stay buried in the subagent; and **(b) always surface issues** — every problem observed this
tick, even one the loop already resolved itself.

    ## Superagent tick <iteration>

    **Goal:** <master_plan path>
    **Loop file:** <loop-file path>
    **This tick:** <superplan | superrefine | superreplan | superrun | superrun (checkpoint) | park (CI wait) | ci-resume | guard | resume | escalation> — <one-line result>
    **Status:** <new status>   (driver: <cron|external>, <scheduled / stopped / paused / parked on CI>)

    **PRs this tick:** <plan/code/closeout PR urls, or none>

    **Findings & issues:** <every problem observed this tick — CRITICAL / ⚠️ findings, plan errors,
    implementation inconsistencies, BLOCKED / CI-red outcomes, `not-traversable`, sync-gate / be-sure
    failures, and any escalation-ladder decision (including how a Rung-1 panel resolved it
    autonomously). Surface these even when the loop handled them itself. If genuinely none: none>

    ### Delegated skill report (verbatim)
    <the complete selected planning operation / `superrun` Final Report exactly as the child returned it. A park
    tick relays the CI-PENDING report verbatim instead (with the armed Monitor / awaited run ids
    named in "This tick"). For a tick that dispatched no heavy skill — guard / resume /
    crash-recovery / escalation-only — write: none (no skill dispatched this tick)>

    ⚠️ **Needs you:** <only when status == WAITING FOR INPUT — the block's What failed, Most likely
    cause and Recommended lines + how to answer (interactive prompt, or `answer.sh <slug> "<option>"`
    for a scheduled loop)>

On **DONE**, replace the body with the C9 completion evidence: active steps integrated (`github`) or
validated completed-local receipts with snapshot/command/review/acceptance evidence (`none`), PRs
merged where applicable,
intentional declined/deferred dispositions (distinct from delivered work),
<!-- cc-only:start -->
and confirmation the driver was stopped — `cron` → `CronDelete`d; `external` → shipped-script loops:
note that the tick wrapper self-disarms the scheduler entry when this session ends
(`SUPER_AUTO_DISARM_ON_DONE`); Desktop-routine loops: remind the user to disable the routine. Include
the final tick's verbatim **Delegated skill
<!-- cc-only:end -->
<!-- cursor-only:start
and confirmation the driver was stopped — shipped-script loops: note that the tick wrapper
self-disarms the scheduler entry when this session ends (`SUPER_AUTO_DISARM_ON_DONE`); otherwise
remind the user to disable the scheduler entry. Include the final tick's
verbatim **Delegated skill
cursor-only:end -->
<!-- codex-only:start
and confirmation the driver was stopped — shipped-script loops: note that the tick wrapper
self-disarms the scheduler entry when this session ends (`SUPER_AUTO_DISARM_ON_DONE`); otherwise
remind the user to disable the scheduler entry. Include the final tick's
verbatim **Delegated skill
codex-only:end -->
report** and any still-open `Findings & issues`.

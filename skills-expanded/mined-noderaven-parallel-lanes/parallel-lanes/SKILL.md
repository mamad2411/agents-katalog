---
name: parallel-lanes
description: Runs an approved implementation plan as parallel lanes of tasks in separate git worktrees, each task implemented and reviewed by its own agents, then integrated, checked and reviewed as a whole. Use when an approved implementation plan is about to be executed (at the execution-method handoff), or when resuming a stopped parallel-lanes run.
---

# Parallel lanes

## Overview

Runs an approved plan as parallel lanes (a worktree each), every task implemented and
reviewed, then integration, checks, E2E, and final reviews. Your job is fixed: build a
manifest, show the dry-run table, set up and launch the bundled `run.workflow.js`, and hand
back.

`<skill_dir>` below means the absolute directory that holds this SKILL.md. Details (manifest
fields, building lanes, profiles, tiers, batching, adjudicator, budgets, markers, report) are in
`<skill_dir>/reference.md`; read it before building a manifest.

**Hard rules.**
1. Your first output when this skill fires is the invoked notice, before any tool call.
2. No multi-agent execution without BOTH the user's explicit choice of Parallel lanes AND an
   explicit yes to the dry-run table you showed in this conversation.
3. Execute only through `<skill_dir>/run.workflow.js` with a manifest. Never write your own
   workflow or orchestration script, never dispatch lane or task agents by hand.
4. Never change a folder that is not a git repo without the user's consent (no `git init`,
   `.gitignore`, scratch or worktree directories).
5. Never push, open a PR, merge into the base branch, or write back a shadow repo unless the
   user said yes to that specific step.

## Notices

Print these lines exactly (each may follow a short visual marker of your choice; the text
after the marker is fixed).

| When | Line |
|---|---|
| The skill fires (first output) | `parallel-lanes invoked: evaluating <plan> for parallel execution` |
| Stepping aside | `parallel-lanes: not a fit (<reason>); recommending <method>` |
| The worth-it check favours a direct build | `parallel-lanes: running in parallel saves about <saved> task-times, less than a run's fixed phases; recommending <method>` |
| Launching a new run | `parallel-lanes: launching run <run_id>: <N> lanes, <M> agents` |
| Launching with tasks already done | `parallel-lanes: resuming run <run_id>: <K> tasks already committed` |
| Relaunch after a transient stop | `parallel-lanes: relaunching run <run_id> after a transient stop` |

What each placeholder stands for: reference.md "Notices". The dry run returns the launch and
resume lines filled in (`notices`); you still print them.

## Flow

1. Invoked notice.
2. If a manifest for this plan exists (`<plan-dir>/<plan-name>.lanes.json`, or any
   `<config dir>/parallel-lanes/runs/*/*.lanes.json` (`${CLAUDE_CONFIG_DIR:-~/.claude}`) whose `plan` equals this plan's absolute
   path), or `bash <skill_dir>/scripts/active-run list` shows a marker for this plan, or the
   user asks to resume or continue: go to Resume (ask first if the user did not say whether to
   resume or start fresh). Starting fresh: rename the old manifest to
   `<plan-name>.lanes.<old run_id>.json`, remove its marker (`active-run remove` refuses a
   locked run: ask; `--takeover` only if the user confirms that session ended), and continue.
3. If the Workflow tool is not available: `not a fit (Workflow tool unavailable)`,
   recommending Subagent-driven. Stop.
4. Assessment. 5. Offer. 6. Build the manifest. 7. Confirmation. 8. Setup and launch.
   9. Hand-back.

## Assessment

First Building step 0. CPU count: `<python> -c 'import os; print(os.cpu_count() or 1)'`
(portable; macOS lacks `nproc`); cap = min(5, count + 2). Run
`<python> <skill_dir>/scripts/derive-lanes <plan> --max-lanes <cap>` and turn its facts into
lanes, prelude, and join per reference.md "Building lanes" (exit 3: no parseable task
headings; step aside). Runnable tasks exclude ones the plan marks after-merge, operator, or
manual.

- Parallel lanes is the default executor for any approved plan of 3+ runnable tasks, unless
  the worth-it check below recommends a direct build.
- Step aside only for a 1-2 task plan or an explicit request for Subagent-driven or Native:
  print `not a fit (<reason>)` (e.g. `2 tasks`), recommending Native when the tasks edit the
  same files in sequence, else Subagent-driven. Then present the plan's normal execution
  choices with that recommendation and stop. Run nothing.
- Worth-it check, only when the Offer will be shown (not when the user already chose Parallel
  lanes by name, never on Resume): with the layout just built, run
  `<python> <skill_dir>/scripts/worth-it <plan> --max-lanes <cap> --prelude <ids> --lane <ids>
  [--lane <ids> ...] --join <ids> [--join-deps <id>:<deps> ...] --project <project folder>`
  (comma-separated task ids, one `--lane` per lane in lane order; an empty prelude or join is
  `''`; one `--join-deps` per join task, its earlier join ids joined by `+`, so the join counts in
  waves). It prints JSON:
  `recommend` is `direct` when running in parallel saves 1 task-time or less (always for a
  single-lane plan), else `parallel`; a non-zero exit or any `status` other than `ok` leaves the Offer as it was.
  The rule, its evidence and the output: reference.md "Worth it".

## Offer

Skip this only if the user already chose parallel lanes by name. Otherwise present these
choices, recommend one, and wait for the pick. With `recommend: parallel`, or the worth-it
check unavailable, keep this order and recommend the first:

1. Parallel lanes (recommended) - <N> lanes in separate worktrees, superpowers implementer +
   reviewer per task, then integration, project checks, and final reviews. ~<X> agents.
2. Subagent-driven - one implementer and reviewer per task, in sequence, in this session.
3. Native - inline execution in this session.

X is about 2 x runnable tasks + 10; the table gives the exact number. "Go ahead" or
"execute the plan" is not a choice of option 1; ask.

Under the choices print `Worth it: these lanes run <N> tasks in about <S> task-slots, saving
about <saved> task-times; a run's fixed phases cost about 1-2.` and, when the result has a
`scale`, `For scale: this project's past runs took about <T> min per task (<min>-<max>).`
(minutes, rounded). When the check is unavailable print `Worth it: unavailable (<reason>).`
instead.

With `recommend: direct`: print the worth-it notice first, then put the direct method first and
recommend it (Native when the tasks edit the same files in sequence, else Subagent-driven, as
for a step-aside), Parallel lanes second and the other method third. Under them print the
Worth it line, the scale line if any, and `A direct build still ends with a whole-branch
review; it gives up the run's worktree isolation, integration and delivery checks, E2E and the
multi-lens final review with its verify gate.` This is not a step-aside: if the user picks
Parallel lanes, continue as usual; if they pick the direct method, stop and leave the plan to
that method, as after a step-aside.

## Building the manifest

Fields: reference.md "Manifest fields". In order:

0. Python: `bash <skill_dir>/scripts/find-python` (exit 3: tell the user and stop); `python` =
   its output, `<python>` below, written single-quoted (`'<python>'`). On Windows manifest
   paths take the `C:/...` form.
1. Superpowers: `bash <skill_dir>/scripts/find-superpowers`. Exit 0: `sp_dir` = the printed
   path. Exit 3: print `parallel-lanes: superpowers not found; agents use built-in prompts`
   and set `sp_dir: null`.
2. Repo: `git -C <project> rev-parse --show-toplevel`.
   - Git repo: `git status --porcelain` must be empty; if not, ask the user to commit or
     stash (never discard). `mode: "git"`, `git_dir: null`.
   - Not a git repo: ask the user to choose, recommending (a): (a) shadow repo (default;
     the folder is untouched until a write-back you get a yes for); (b) `git init` plus a
     baseline commit, then a normal git run. Shadow details, existing-shadow check, `shadow
     init` (prints `git_dir`; exit 3 on size: tell the user, `--force` only on their yes):
     reference.md "Shadow repos".
   - Git identity: `git -C <project> var GIT_COMMITTER_IDENT` must print one, or every task
     commit fails partway through the run. If it fails: reference.md "Git identity".
3. Lanes, prelude, join, hooks, `depends_on`, `overlaps`, `excluded`: reference.md "Building
   lanes" (`prelude` and `join` are not lane ids; no lane id starts with `u-`). Give every join
   task `depends_on` (`[]` when it needs no earlier join task): the join then runs in waves, and
   a join task without it waits for every earlier one (reference.md "Join waves").
4. `profile` and tiers: reference.md "Profiles", "Tiers", "Batching". `profile: "lite"` only
   for one lane, at most 8 tasks, no security task, and no `hooks.post_integrate`; else
   `full`. Tiers `standard` (Opus), `sonnet` (Sonnet), `light` (Haiku); security tasks always
   `standard`; `batch` keys for consecutive tiny light tasks. The user's model preference wins
   when it is stricter (e.g. "Opus for everything" means all `standard`).
5. `commit_rules`: one string from the user's and project's rules (memory, CLAUDE.md, the
   plan's conventions, CONTRIBUTING; reference.md). Every agent prompt carries it.
6. `commands`, `task_checks` and `widen_paths` (from the plan's tests and shared files), paths,
   `run_id`, `agent_type`, `autonomy` (`autonomous` default), `limits` (`review_rounds: 5`,
   `max_parallel_lanes: <cap>`): reference.md "Manifest fields". New run: `done: []`,
   `reviewed: []`, no `backfill`.
7. Run files live in `<run_dir>`: the plan's directory when the plan is outside the project
   and its repo, else `<config dir>/parallel-lanes/runs/<run_id>/`. The manifest and
   `repo.ledger_dir` (briefs, reports, review packages) go there, never inside the project. Save the manifest as
   `<run_dir>/<plan-name>.lanes.json`; `ledger_dir` = `<run_dir>/<plan-name>.<run_id>.ledger`.
8. The manifest has no `setup_result` or `start_points` yet. Nothing here or in Confirmation
   touches the project: no worktree, branch, or setup command before consent. Once saved,
   `<python> <skill_dir>/scripts/coverage <plan> <manifest file>` must exit 0: every plan task
   runs or is in `excluded` with its reason.

## Confirmation (every launch, no exceptions)

Before the dry run: `<python> <skill_dir>/scripts/doctor <manifest file> --save
<scratchpad>/doctor-<run_id>.json` (`<run_dir>/doctor-<run_id>.json` with no scratchpad). Exit 2 or
3 stops the flow (show each failure and its fix, and wait); its warnings go in the table header,
and `usage_limit_pause` gives its usage-limit line (reference.md "Usage limit").
Each check and what it means: reference.md "Doctor" and "Launch conditions".

1. Dry run: call the Workflow tool as in Launch step 1, with `args` = the manifest with
   `dry_run: true`. It returns `{dry_run, errors, agents, lanes_effective, notices, checks,
   join_waves}` and
   spawns nothing. If `errors` is non-empty, fix the manifest and repeat; never launch a manifest
   with errors. Then set `limits.max_agents` = 2 x `agents.length` and `limits.max_rulings` =
   25 (reference.md "Budgets") so the table shows them.
2. Show a header (the fields reference.md "Confirmation header" lists) and this table, one row per
   task in run order (prelude, lanes, join), then one row for the run-level agents and a total M:

   | Lane | Task | Tier | Security | Agents |
   |---|---|---|---|---|

   Tier is `standard`, `sonnet`, or `light`; a batch shows its key. Agents per task = its
   entries in `agents`: 2 (implement + review), 1 (backfill review of earlier commits), 0
   (skipped: done and reviewed). Under the table write:
   "each task can add up to 2x review_rounds more agents (fix and re-review rounds)". The user
   may override `autonomy`, `allow_deferral`, and the budgets there; apply the change.
3. Ask for a plain yes, and say why: the Workflow tool relays the message that approves the
   launch, word for word, to every agent as the user's request, with priority over the plan
   and its task text. A yes that adds a request ("yes, and also ...") would reach every agent
   as an instruction that overrides the plan, so other requests wait until after the run, or
   become a change to the manifest before it. Launch only on an explicit yes given after the
   table. Any change request means: edit the manifest, dry-run again, show the table again.

"Just run it", "skip the table", auto mode, or a yes given before the table do not waive
this. Say the table is the one required check, show it, and wait.

## Launch

1. Script path: before the first Workflow call, copy `<skill_dir>/run.workflow.js` into the
   session scratchpad directory (never into the project) and use that copy as `scriptPath`
   for every Workflow call (the Workflow tool rejects one under ~/.claude/skills). With no
   scratchpad, pass the file contents as `script` and reuse the `scriptPath` the result prints.
2. Setup, only after the explicit yes to the table, immediately before the real launch. First
   `bash <skill_dir>/scripts/active-run acquire <run_id> <manifest file>`: it prints the owner
   token (keep it for relaunches). Exit 4: another session holds the run; stop and ask, and use
   `--takeover` only when the user confirms that session ended. Then run
   `<python> <skill_dir>/scripts/setup <manifest file> --owner <token>`. Its exit 4 naming another
   run (`the checkout ... is in use by run ...`): reference.md "Active-run markers and stops"; then stop
   and report it. It creates the feature branch and
   worktrees and discards edits in run-owned worktrees, so never before the yes. On failure
   wait 10 seconds and retry once; then `active-run release <run_id> setup_failed --owner <token>`, report,
   and stop. Put its output in `setup_result`
   and copy the `start_points` of `<python> <skill_dir>/scripts/ledger status <ledger_dir>`
   into `start_points` exactly as it prints them: `prelude` after setup, `join` only once an
   earlier launch got past integration, so a new run has no `join` key. Adding these two
   fields needs no second table; any other manifest change after the yes does.
3. Save the manifest with `dry_run: false`. Print the dry run's `notices.launch`, or
   `notices.resume` when `done` is non-empty, as it returned them.
4. Call the Workflow tool with `args` = the manifest. Progress shows in `/workflows`; note
   the transcript directory it prints. Do not do lane work or touch the worktrees meanwhile.
   Once it prints the transcript directory, bind the saved doctor result to this launch:
   `<python> <skill_dir>/scripts/ledger conditions <ledger_dir> <wf id> <saved file>`. The
   wf id is this launch's, never the dry run's. A refusal
   never stops the run; keep the latest launch's refusal code for `tool-outcomes`.
5. Record each launch's spend (reference.md "Budgets"), a relaunch included, never a dry run:
   `<python> <skill_dir>/scripts/ledger ended <ledger_dir> <status> <agents_spawned>
   <rulings_spent>` (`<status>`: reference.md "Budgets"), then `<python> <skill_dir>/scripts/ledger
   carry-launch <ledger_dir> <transcript dir>` (reference.md "Carry-over"; exit 3: say that launch
   is not carried). Before a transient relaunch, keep the lock. At the end, in one command line
   (reference.md "Budgets"): `<python> <skill_dir>/scripts/ledger ended <ledger_dir> <status>
   <agents_spawned> <rulings_spent> && { <python> <skill_dir>/scripts/ledger carry-launch <ledger_dir>
   <transcript dir> || true; } && bash <skill_dir>/scripts/active-run release <run_id>
   <release> --owner <token>`, where `<release>` is `--remove` only for `complete` when the hand-back gate
   passes: `acceptance.status` `accepted`, and `<python> <skill_dir>/scripts/check-verify <transcript dir>
   <manifest file>` exits 0 printing status `match` or `not_required`; otherwise `<status>` (`unaccepted` for
   a complete run), so a later session offers the resume. Run check-verify before that end record.

## Transient stops (relaunch once, no prompt)

A stop is transient when status is `stopped`, `reason` is not `budget`, and every cause is
an agent error, a missing result, setup-command retry exhaustion, or agents unavailable
(`agents_unavailable`; reference.md "Transient stops" says how the causes are read, which texts
count, and which causes are NOT transient: never relaunch those; stop and notify). After an
`agents_unavailable` stop, run `scripts/stop-cause` as reference.md "Usage limit" says.

Before any relaunch, compare the stopped launch's result `version` with `<skill_dir>/VERSION`:
different or missing means Resume instead (reference.md "Transient stops").

Before recording the stopped launch's end, run doctor again with `--save` (Confirmation): the
earlier snapshot belongs to the earlier launch.
- Exit 0: record only the spend and relaunch, then run `ledger conditions` for the new launch
  (Launch step 4).
- Exit 2 or 3: a real stop. Record the spend and release the lock with status `stopped` in one
  command line (Launch step 5), show the failures, notify, and keep the failed check names for
  `--relaunch-blocked`.

Relaunch once with the relaunch notice: carry budgets over (reference.md "Transient stops"). Set
`repairs_spent` to the repairs in the stopped run's `final.repairs` plus the earlier value.
First recompute `done`, `reviewed`, `deferred`, the `carry` notes, `carried_minors`,
`inputs_changed`, the join wave fields and `backfill` as in Resume steps 2-3, then rerun
`scripts/setup --owner <token>`, put its output in `setup_result` and take `start_points`; if
validation rejects its `setup_skipped`, rerun setup. Launch again. No second table. A second
transient stop is a real stop, unless it is a usage-limit stop (reference.md "Usage limit").

## Notify

Push-notify (PushNotification) the run id, status, and next step when a run completes, really
stops, hits a budget cap, or fails its relaunch; else a chat notice.

## Hand-back

The run returns `status`:
- `invalid`: notify, show `errors`, fix the manifest, back to Confirmation.
- `preflight_conflicts`: no task ran (setup commands did; show the checkouts' `git status`).
  Notify, show `preflight.conflicts` and `rulings`; the user decides; then Confirmation again.
  When `preflight.schedule` is non-empty, move each named task as its `fix` says (record the
  dependency as `code` in `depends_on`), then Confirmation again.
- `stopped`: transient: relaunch as above. Otherwise show `reason` and each `stopped_lanes`
  entry (lane, task, reason), notify, keep the marker. The run is resumable: after the user
  answers or fixes the plan, go to Resume.
- `complete`: run check-verify first (Launch step 5); any other outcome than exit 0 with `match` or
  `not_required` (exit 1, 2 or 3, a crash, no or unparseable output) is `unverified`: show its reason, or
  "check-verify error" with the exit code and stderr, keep the marker, and recover as reference.md "Verify
  evidence" says. Lead with `acceptance` (reference.md "Report"). Only `accepted` is delivered work.
  `rejected` or `unverified`: show every reason, notify, keep the marker; never call it done.
  `checks_failed_at_start` (the failures fail at the run's start point too) is shown like any
  rejection: show its detail, which names the evidence, and suggest the `ledger accept` text
  for it (reference.md "Report").
  The user fixes and resumes, or explicitly accepts named reasons or warnings: record that
  with `<python> <skill_dir>/scripts/ledger accept <ledger_dir> <repo root> <delivered_sha>
  "<what>"`. Then rerun archive-run, autopsy, audit and tool-outcomes, so the override reaches
  the archive. Once the accepts cover every reason (and the warnings the user named) and those
  reruns are done, remove the marker with `bash <skill_dir>/scripts/active-run remove <run_id>`,
  so a later session does not resume the run.

Report: run `<python> <skill_dir>/scripts/run-report <transcript dir> <manifest> --out
<run_dir>/<plan-name>.<run_id>.report.json` (Launch step 4's transcript dir) and append
its output, with the contents reference.md "Report contents" lists.

After the report, for every run that ends after a launch (never a dry run): `<python>
<skill_dir>/scripts/archive-run <manifest file> <transcript dir>...`, then `<python>
<skill_dir>/scripts/autopsy <run folder>` (the folder archive-run prints), appending its summary.
Then `<python> <skill_dir>/scripts/audit <run folder> --repo <repo.git_dir in shadow mode, else
repo.root> --head <branch>`, appending its summary (reference.md "Audit"). Details: reference.md
"Run history" and "Autopsy". Last, after any other tool: `<python>
<skill_dir>/scripts/tool-outcomes --run-folder <folder> --archive-exit N --autopsy-exit N
--audit-exit N [--conditions-refused CODE] [--relaunch-blocked CHECKS] --cleanup awaiting|none`. Show its line
under its own label after the acceptance lead, and run it again after cleanup (reference.md
"Report").

Then, for accepted work (or reasons the user accepted), offer the next step; act only on an
explicit yes:
- Git mode: a PR from `branch` into `base_ref` (follow the user's PR policy).
- Shadow mode: run `bash <skill_dir>/scripts/shadow preview <git_dir> <root> <branch>`, show
  adds, changes, deletes, conflicts, and skipped. On yes: `bash <skill_dir>/scripts/shadow
  writeback <git_dir> <root> <branch>`. Exit 3: nothing or part was written; follow
  reference.md "Cleanup" and ask. Never copy files around it by hand.

Cleanup, only after the user confirms the result: reference.md "Cleanup"; never `--force`,
never `branch -D`. Run `<python> <skill_dir>/scripts/cleanup <manifest file>` without `--yes`
first, show its plan, and add `--yes` only on the user's yes. Keep the manifest and ledger.

## Resume

1. Invoked notice. Read the manifest (an `active-run list` marker names it); set `python` by
   Building step 0. No manifest (earlier work from a hand-run attempt): `<skill_dir>/adopt.md` first.
2. First `<python> <skill_dir>/scripts/ledger carry-launch <ledger_dir> <wf id>` for each earlier
   launch not yet carried, in launch order (`doctor-<wf>.json` gives its `setup_event`). Then
   `<python> <skill_dir>/scripts/ledger status <ledger_dir> --plan <plan> --manifest <manifest
   file> [--spec <spec>]`. Set `done`, `reviewed`, and `deferred` from it (taking a deferred
   task up: reference.md "Backfill"), and `repairs_spent` from earlier reports' `final.repairs`;
   put each `carry` entry into `notes`; copy `minors` into `carried_minors`, and `inputs` into
   `inputs_changed` as `{plan: plan_changed, spec: spec_changed}` (reference.md "Carry-over").
   Copy `join_started`, `unit_branches`, `wave_merges` and `start_bases` as they are
   (reference.md "Join waves"). Tasks in `stale`
   (with their dependents) or `unbound` are left out of `reviewed`, so they are reviewed
   again: tell the user which and why, and say so when `inputs` reports a changed plan or
   spec. `<python> <skill_dir>/scripts/coverage <plan> <manifest file>` must exit 0 again
   (else fix the manifest's tasks or `excluded`).
3. `backfill`: `<python> <skill_dir>/scripts/ledger backfill <ledger_dir> <manifest file>`,
   and its `join_tip` when not null.
   Exit 3 lists records git does not confirm: show them and stop (reference.md "Backfill").
4. Blocked tasks: show each reason; get the user's answer or plan fix before relaunching.
   Record an answer in `notes` as `{"<task id>": "<answer>"}`; a plan fix needs
   nothing more.
5. Keep `run_id`, `branch`, and `worktree_root`; `scripts/setup` reuses the worktrees (and the shadow).
6. Confirmation, doctor included (same rules; `spent` lowers
   `limits.max_rulings`: reference.md "Budgets"), then, after the yes, Launch step 2 again (setup and `start_points`), the resume notice,
   and launch.

## Red flags - stop

- Any tool call or text before the invoked notice.
- A Workflow call with `dry_run: false`, or a `scripts/setup` run, before a table and a yes,
  or without the launch lock.
- Writing any `.workflow.js` file, or dispatching task agents yourself.
- Creating or changing anything inside a non-git project folder without consent.
- `git push`, `gh pr create`, or `shadow writeback` without a yes for that step.

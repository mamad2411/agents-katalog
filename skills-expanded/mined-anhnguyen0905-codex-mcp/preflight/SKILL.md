---
name: preflight
description: Phase 0 preflight for codex-flow — gate on Codex login/health, detect and offer to resume an interrupted run, and baseline the workspace (git cleanliness + ref, gitignore live logs, known-red test baseline) so later phases have a rollback point and review blames only new failures.
---

# Preflight (Phase 0 — run FIRST, it is a gate)

**Helpers**: required — doctor.mjs, context-slice.mjs, flow-state.mjs, project-context.mjs, profile-router.mjs (helper rule: missing → STOP and tell the user to reinstall the codex-flow plugin; non-zero exit → surface the error and STOP).

Nothing downstream is safe until these pass. Do not interview, plan, or execute until the gate is green.

## Step 1 — Health gate

The command evaluates the Fast-path gate BEFORE this call: the analysis lane makes no
`codex_health` call at all unless the user requests a Codex second opinion (and then with
`{ deep: true }`); the small-change lane and the full flow make it once, after the gate decision
and the resume check.

In those lanes, call `mcp__codex__codex_health` with `{ deep: true }` ONCE — after the gate
decision and the resume check, before anything else. The deep input adds
a one-shot read-only `codex exec` probe and returns `execProbe`
(`ok | quota | model | error | skipped`) plus `execProbeMessage` next to `loggedIn`; read
`execProbe` from that single call instead of re-probing later phases.

- **Tool call fails / server missing** → a connect timeout or closed connection is not "server missing": run `node scripts/doctor.mjs --probe-launcher`, keep the folder downloaded or move the repo off cloud-synced storage, reconnect with `/mcp`, re-check health, and only then offer the Executor fallback. Otherwise, the MCP server isn't set up. Point the user to the codex-mcp
  README install steps (or `node scripts/doctor.mjs`), then offer the command's **Executor
  fallback**: fix and re-check, or continue with Claude as executor. Never continue silently.
- **`loggedIn: false`** → tell the user to run `codex login` (ChatGPT Plus/Pro/Team, or set
  `OPENAI_API_KEY`), then offer the same Executor fallback choice. Proceed only after a re-check
  shows `loggedIn: true` or the user explicitly chose the fallback.
- **`execProbe: quota` or `execProbe: model`** → logged in but unable to execute. Quote
  `execProbeMessage` and offer the Executor fallback right away; a `quota` or `model` probe result
  is sufficient on its own and requires NO unhealthy health re-check.
- **`execProbe: error`** → report `execProbeMessage` verbatim, then offer the same fallback choice.
- **`loggedIn: true` with `execProbe: ok` (or `skipped`)** → report the Codex version, record
  `executor: codex`, and continue.
- The analysis lane of the Fast-path gate needs no Codex session and no fallback decision; when its
  optional Codex second opinion fails, the analysis is delivered Claude-only with the failure named
  in the "what I verified" note.

## Step 2 — Resume check (don't clobber an interrupted run)

If `.codex-flow/STATE.md` exists, treat it as an interrupted run even when PLAN.md or TASKS.md has
not been created yet:

- Read `.codex-flow/STATE.md` as the resume authority. Its approval fields decide which phases may
  be skipped; any phase whose approval is not recorded MUST be re-run. The existence of
  PLAN.md/TASKS.md is NOT proof of approval.
- When both `.codex-flow/PLAN.md` and `.codex-flow/TASKS.md` exist, run
  `node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs" --resume` and read
  `.codex-flow/RESUME.md` instead of the raw files.
  If the helper is not found, STOP and tell the user to reinstall the codex-flow plugin (its scripts/ directory is required); if it is present but exits non-zero, surface the error to the user and STOP. Never edit control files by hand. When either file does not exist, read only the control files that exist; do not require a
  missing TASKS.md to resume an earlier phase.
- When TASKS.md exists, show its task Statuses. Ask **resume vs restart** in every case except
  `phase: complete`, which archives and starts fresh without a resume offer (see below).
- Before scheduling anything, reconcile every task whose Status is `in-progress`. Read its recorded
  Session line. The resume slice's Task statuses section carries Session content for every
  in-progress task even though it embeds the full task text only for the first unfinished task; do
  not assume the other in-progress task blocks are embedded. A launching line may be sequential
  (`- Session: launching (base: <short sha>)`) or parallel (`- Session: launching (base: <short
  sha>, worktree: <path>, branch: <name>)`). Extract the base sha from either launching form or the
  completed-session form. Then cross-check `git log --oneline <base sha>..HEAD` and `git status`
  for changes to the task's declared `Files:` since that base. Report the evidence and ask the user
  to choose exactly one: **continue in the recorded session (when a real session id exists) /
  review the work as-is / reset to pending**. For reset to pending, roll back through the
  checkpoint commit when `checkpointCommits` is enabled. Never blindly re-execute an in-progress
  task.
- **`phase: complete`** → terminal, not resumable. Do NOT offer resume: archive the run's control
  files to `.codex-flow/archive/<timestamp>/` and begin fresh, exactly as **Restart** does.
  Archive `EVENTS.jsonl` with them.
  Resume is offered only for a non-complete `phase`.
- **Resume** → first run `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" check`, adding
  `--tasks .codex-flow/TASKS.md` whenever that file exists so the terminal-status validation runs
  (`node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" check --tasks .codex-flow/TASKS.md`); when it reports only missing keys on a legacy file, add them
  with `set` (`currentTask -`, `taskStage idle`, `wave -`) and continue; any other violation is
  surfaced to the user before routing. Then skip only the phases whose approvals STATE.md records, and route from STATE.md's
  recorded `phase`. For `phase: execution`, enter Phase 4 at the first task not marked done. Before
  that, first route by `taskStage` regardless of `currentTask` (`currentTask` names the task in sequential
  mode; in parallel mode it is `-` and `wave` names the wave): `reviewing` → resume Phase 5 for that task;
  `launching` or `executing` → run the in-progress reconciliation above before anything else;
  `handoff` → finish Phase 5 step 7's durable handoff (or the wave's Step 3.8); `merge-conflict` → surface the conflict to the
  user and STOP; `idle` → the next pending task. For
  `phase: review`, resume Phase 5 completion work; when all tasks are done but `phase` is not
  `complete`, also resume Phase 5 for the final dual review, requirement ID-walk, improvement gate,
  cost/report delivery gates, and completion write instead of concluding there is no work. For an
  earlier phase, enter its first unapproved gate. Treat
  every `[verify]` block as a hypothesis: confirm it against `git diff` and the current code before
  relying on it. Record the current `git rev-parse HEAD` as `resumeHead` with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" resume --head <sha>` (add `--phase <phase>` only when entering an earlier phase); apart
  from the legacy-key backfill above, change no other STATE.md key as part of the resume operation.
  The reconciliation choice for an in-progress task (continue / review as-is / reset) is made
  first; the `taskStage` routing then applies to the task as the user left it.
- On resume, reuse the report dir recorded under `## Session report` in PLAN.md; create it only if
  missing.
- **Restart** → archive the old control files that exist to `.codex-flow/archive/<timestamp>/`,
  including `EVENTS.jsonl`,
  then begin fresh with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" init --baseline <run-start HEAD> --known-red "<compact list>"`.
  Archive the journal files printed by `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" archive-paths`.

If STATE.md does not exist, do not offer resume. Treat any PLAN.md, TASKS.md or journal files named
by the archive-paths helper as orphaned control files and offer to archive them before beginning a
fresh run.

## Step 3 — Baseline the workspace

1. **Git cleanliness + ref**: `git status --porcelain`. If porcelain is non-empty but `git -c core.fileMode=false status --porcelain` is empty, it is mode-only noise: with user consent, offer `git config core.fileMode false` instead of commit/stash and treat the baseline as clean. Otherwise, dirty → ask the user to commit/stash first
   (recommended: clean per-task diffs + a rollback point) or proceed with the dirty baseline noted
   in PLAN.md. When the user proceeds dirty, write `.codex-flow/baseline-dirty.patch`: save the
   baseline-to-working-tree output from `git diff HEAD`, then append a `# Untracked at run start`
   comment header with each untracked path from `git status --porcelain`. Record the baseline ref
   (`git rev-parse HEAD`). Not a git repo → warn that diffs/checkpoints/rollback are unavailable and
   confirm before continuing.
2. **Ignore live logs**: ensure `.codex-flow/live/` is in `.gitignore` (append if missing) so raw
   JSONL progress logs never land in checkpoint or final commits.
3. **Known-red baseline**: detect the project's test command and run it once. Record pre-existing
   failures as the **known-red baseline** — Phase 5 compares against this list so Codex is blamed
   only for NEW failures. If the suite can't run at all, tell the user and agree how results will be
   verified before continuing.
4. **Write run state**: after baselining, create `.codex-flow/STATE.md` with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" init --baseline <run-start HEAD> --known-red "<compact list>"` (add `--dirty-baseline baseline-dirty.patch` / `--executor <fallback value>` when applicable), with exactly one
   `## Run state` section and these fixed `- <key>: <value>` lines:

   ```markdown
   ## Run state
   - phase: interview
   - requirementsApproved: no
   - planApproved: no
   - backlogApproved: no
   - runBaselineRef: <git HEAD at run start, or unavailable outside git>
   - resumeHead:
   - knownRed: <recorded known-red failures, compact; none when green>
   - checkpointCommits:
   - executionMode: undecided
   - dirtyBaseline: <none | baseline-dirty.patch>
   - executor: codex
   - currentTask: -
   - taskStage: idle
   - wave: -
   - profile: -
   - profileMode: off
   - evidenceMode: off
   - languageMode: off
   - runLanguage: -
   - packs: -
   ```

   These six keys are optional and validated when present; `flow-state`'s `init` sets them from the
   router's `initFlags`.

   `executor` records who writes code: `codex` (default), `claude (fallback: <reason> <ISO 8601>)`
   after an explicit Executor-fallback choice, or `codex (restored <ISO 8601>)` after returning.
   It changes only at a task boundary and never silently.

   `currentTask` is the task being worked (`T<n>`) or `-`; `taskStage` is one of
   `idle | launching | executing | reviewing | handoff | merge-conflict`; `wave` is the current
   parallel wave number or `-`. `phase` stays `execution` for the whole task loop — per-task
   progress lives in `currentTask` + `taskStage`; `phase: review` means the whole-feature review
   after the last task.

   `phase` and the three approvals change only through `approve`, `advance`, `requirement-delta`,
   `plan-drift`, `improvement-gate`, and `resume`; typed commands journal to
   `.codex-flow/EVENTS.jsonl`, and `check` reports hand-edited gate keys or unfinished transactions;
   change other keys through `set`. The helper takes no file lock and assumes one orchestrator
   writes STATE.md and the journal; parallel workers never do.
   Write STATE.md and TASKS.md status lines only through the helper:
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set <key> <value>`, `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" check`, and
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" task <T-id> <status>` (which appends the transition
   line). If the helper is not found, STOP and tell the user to reinstall the codex-flow plugin (its scripts/ directory is required); if it is present but exits non-zero, surface the error to the user and STOP. Never edit control files by hand.

   The orchestrator is the only writer. `runBaselineRef`, `knownRed`, and `dirtyBaseline` are
   written once at run start and NEVER modified on resume. A resume writes `resumeHead` and `phase`;
   outside `execution`, it resets `currentTask`, `taskStage`, and `wave` (apart from the legacy-key
   backfill); later approval or execution transitions update only their corresponding mutable
   fields.

## Command-routed details

If `.codex-flow/STATE.md`, `PLAN.md`, `TASKS.md` or `EVENTS.jsonl` exists, load this skill and run
Step 2 resume check FIRST; otherwise evaluate the Fast-path gate first and load preflight only after
it selects the small-change lane or the full flow. The analysis lane never loads preflight.
Orphaned control files are `PLAN.md`, `TASKS.md` or journal files named by the archive-paths helper
when STATE.md does not exist.

On a fresh run, before baselining, when `.codex-flow/PROJECT.md` is absent generate it with
`node "${CLAUDE_PLUGIN_ROOT}/scripts/project-context.mjs" --generate`, and ask the user to confirm or edit it in
the Phase 1 interview. PROJECT.md is tracked, not run state: include it in checkpoint and final
commits and never archive it with the run; when created before baselining, list it as pre-existing
in the `baseline-dirty.patch` manifest.

On a fresh run, create `.codex-flow/reports/<YYYYMMDD-HHMMSS>/` using the session-start local-time
timestamp. On resume, reuse the report dir recorded under `## Session report` in PLAN.md; it is the
single report dir later phases write into per `codex-flow:session-report`.

**Profile router**: Full flow only (not fast-path lanes): after the Fast-path gate selects full flow
and before baselining, classify the deliverable (`code|data|design|plan|content|mixed`) and run
`node "${CLAUDE_PLUGIN_ROOT}/scripts/profile-router.mjs" resolve --profile <p> --request-file <path> --run-id <report dir name>`.
`<path>` is a temp file outside the workspace holding the user's task (e.g. via `mktemp`);
`<report dir name>` is the session-start `<YYYYMMDD-HHMMSS>` used for the report dir. Add its
`initFlags` to flow-state's `init`. Load `codex-flow:profile-pilot` when `profileMode` is `enforce`,
`evidenceMode` is not `off`, or `languageMode` is `on`; its rules replace the gates it names.
Load `codex-flow:pack-game-analytics` per STATE `packs`.
On resume, do not re-run the router: read `profile`, `profileMode`, `evidenceMode`, `languageMode`,
`runLanguage`, and `packs` from STATE.md (missing legacy keys mean `off` modes, `-` profile/runLanguage,
and `-` packs—no pack) and apply the same load rule.

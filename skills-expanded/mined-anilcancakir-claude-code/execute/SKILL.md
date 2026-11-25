---
description: "Run an approved ac plan to completion, wave by wave, with cost-tiered workers, per-wave verification and a final review."
when_to_use: "Use after /ac:plan writes a plan you want built; takes a plan slug or path."
argument-hint: "<plan-slug | .ac/plans/<slug>/plan.md> [--auto] [--lane] [--max-parallel N] [--no-oracle] [--no-qa] [--no-checkpoint-commits]"
effort: high
---

# /ac:execute

Executor that runs an approved plan to completion, wave by wave, and gates the deliver with a final code-review.

Plan: $ARGUMENTS

## Standing rules

These hold for the whole run, including after a compaction, which keeps only the first 5,000 tokens of a re-attached skill. Everything below this block is procedure; these are the bounds.

**Turn termination.** Your turn ends on exactly one of: an `AskUserQuestion` call, the Phase 4b execution summary, a named BLOCKER from `<auto_mode>`, or a one-line wait status while background workers you spawned still run (each task-notification starts your next turn; never wait with a `sleep` or polling loop). Nothing else ends it. Never end a turn by describing what you would do next, and never propose that the user open a fresh session to continue the run.

Under `LANE_MODE` (set by `--lane`: this run is an `ac:lane` subagent, which has no `AskUserQuestion` and whose parent sees only its last message) the legal turn end is the lane status block defined in `${CLAUDE_PLUGIN_ROOT}/skills/coordinate/references/lane-protocol.md`, and every turn ends with one. `status: WORKING` replaces the one-line wait status while workers run, `status: BLOCKED` replaces `AskUserQuestion` at every BLOCKER (see `<auto_mode>`), `status: DONE` ends Phase 4b, and `status: FAILED` ends a halt that has no option to offer (plan not found, a truncated plan, a count mismatch). A lane never calls `AskUserQuestion`, never pushes and never runs `ac:qa`.

Every branch that terminates the run deletes this run's marker, `.ac/state/execute/<slug>.json`, first, and leaves every other slug's marker alone: while a marker this session owns exists and no background worker is running, the `Stop` hook (`${CLAUDE_PLUGIN_ROOT}/hooks/stop-guard.sh`) blocks the turn from ending and returns the outstanding step count to you. The marker's absence is what permits a terminal stop.

**Context.** Auto-compaction summarizes older turns and the run continues. A filling context window is not a stopping condition, not a reason to hand the remainder back, and not a reason to suggest a new session. No compaction command is available to you, so never plan around invoking `/compact`. When the procedure you need has been truncated away, re-invoke the `ac:execute` skill to restore this body, then read `PLAN_PATH` for the authoritative step state.

**A stop needs a name.** "I cannot verify this properly in the remaining context" is not a reason. When a step genuinely cannot be completed to the plan's standard, the reason is one of: a fact you do not have and cannot obtain, a decision only the user can make, or a gate you cannot pass. Each maps to a BLOCKER branch (2i, 2j, 3c) that surfaces an `AskUserQuestion` and deletes the marker. Name the class, take the branch, report what did land. Never substitute a capacity limit for the real reason.

**No review loop needs bounding.** Phase 3 is one reviewer pass and the findings are yours to filter. Five bounded loops remain: at most two retries per step at 2e (an effort rung, then a tier rung), counted in `WORKER_RETRY_PER_STEP`; at most two briefing-gap re-spawns per step at 2e; the three-failed-steps-across-two-waves halt at 2j, read from `STEP_FAILURES` (one entry per step at terminal failure); the one QA retest that `ac:qa` runs and counts after its own fixes at 3e, so 3e never re-invokes it; and, under the CI gate, at most three red-CI rounds at 3f.

**Progress surface.** Two surfaces carry it and neither is a tool. The plan file's checkboxes are the per-step record, ticked at Layer D and counted with `grep -c '^- \[ \]'`, which is also what the `Stop` guard reads. Phase 2h prints the per-step table after each wave. Add one short line per phase and wave transition and that is the whole picture. Do not write a procedure that depends on task tools or `TodoWrite`: recent models get no task tools, and `CLAUDE_CODE_ENABLE_TASKS=false` swaps them for `TodoWrite` elsewhere.

**Output length.** Per-turn user-facing prose: at most 3 lines. The wave summary at 2f: at most 3 lines. Filter tool output before it lands: a passing test suite through `tail -20`, a diff scoped to the wave's files. The 2a strategy render, the 2h progress table, and the Phase 4b summary are the only long surfaces, and their templates fix their shapes. Anything a later reader needs goes in `wisdom.md` or `report.md`, not into the chat. Every token you write is re-read on every later turn; a file is read on demand.

<role>
You are the Developer orchestrating execution of an approved plan at `.ac/plans/<slug>/plan.md`. You delegate every implementation step to a tier-routed worker subagent (`ac:plan-worker-quick` / `-junior` / `-junior-high` / `-senior`), verify each wave through the 4-layer check, commit after any wave that changed tracked files, then gate the final deliver with one code-review pass (and `ac:oracle` when a criticality surface is touched). The plan is the spec; you execute it precisely.
</role>

<scope>
Source code in the project, scoped to the files each step declares, plus these artifacts under
`.ac/plans/<slug>/`: `wisdom.md` (max 15 items, max 5 per wave; the `[RETRY]` and `[REMEDIATION]` records sit outside both caps), `evidence/<step-id>-<scenario>.<ext>`,
`briefing-common.md` (2b), `review-log.md` (append-only, one entry per Phase 3 review, a record rather than a loop counter),
`qa/<run id>/` (the Phase 3e QA run directory, written by `ac:qa`), and `report.md`. The wave commit is a plain `git commit`; the final commit at Phase 4 goes through `/ac:commit`.

`plan.md` is read-only here except for Layer D checkbox ticks and a reviewer-flagged plan-spec fix. If the plan is
wrong, report and stop. Source outside a step's declared Files is out of scope; bonus refactors break atomicity.
</scope>

<capabilities>
The base tools plus `AskUserQuestion`, which arrives directly rather than deferred.
`Agent` spawns the four worker tiers, `ac:plan-code-review`, and `ac:oracle`. `Bash` takes the wave diff, which is Layer B's
input, and also runs build, test, lint, the wave commit, and the QA tools a step names. `Read`, `Grep` and `LSP`
are how the rest of Layer B happens, and none of it is optional. `Skill` invokes `ac:qa` at Phase 3e when the plan asks for it, and `/ac:commit` once, at Phase 4.

Subagents inherit none of your context, so every worker gets the full six-section briefing, its shared blocks
in `briefing-common.md` (2b). Drive every chain from
here (the agent reports back and you make the next call): the plan-workers' `tools:` allowlist omits `Agent`, and the
code reviewer and `ac:oracle` have it denied.
</capabilities>

<constraints>
- Auto-continue between verified steps and waves. Never ask "should I continue".
- Copy the step's `Description`, `Files`, `Done when`, `QA`, and `Must NOT` into the briefing verbatim. Paraphrase
  inverts opt-in and opt-out, which is the most common worker failure.
- The wave is the unit of every orchestrator action: one diff, one typecheck, one build, one test and lint run
  scoped to the wave's touched files, one commit per wave. The full suite runs once, at Phase 3 (in CI for a project with a `## Verification gate: ci` section, see 3a). The two exceptions are per-step and stay per-step: the Layer C QA scenario, which is
  the only evidence anything ran, and the Layer D checkbox, which the `Stop` guard reads as the progress signal.
- All four verification layers run on every wave, and none of them is optional. Layer B means reading the wave
  diff hunk by hunk and matching every hunk to a worker's claim, not sampling.
- Inject `TDD_MODE` into every briefing.
- Wave-after commits whenever the wave changed tracked files; the final commit always.
- Do not call `EnterPlanMode`; the plan is approved. Do not modify `plan.md` beyond Layer D ticks, and never rewrite
  it silently when a reviewer says the plan is wrong: surface it.
- `plan.md`, `wisdom.md`, `review-log.md`, `evidence/` and `report.md` are working files written for a model, not
  artifacts a person reads: no tool call checks them for dashes. The dash check belongs only to what ships.
- Mutate a file with `Edit` or `Write`, never through `Bash`: not `python3 -c`, not a `cat >>` heredoc, not `sed -i`,
  not `perl -pi`, not `tee`: a Bash rewrite spends both texts as output tokens, and only `Edit` fails loudly on a
  non-unique anchor. Append to `wisdom.md` or `review-log.md` by reading the file's tail and calling `Edit` with
  enough of its last lines to be unique, or `Write` it the first time: inside an `ac:lane` worktree Claude Code
  often refuses a heredoc append as a command it cannot verify.
</constraints>

<auto_mode>
`--auto` in the argument string sets `AUTO_MODE = true` for the run, and `/ac:plan` Stage 6a passes it when it chains
here. Every gate left in this body is a BLOCKER, so auto mode resolves none of them; it never skips verification,
the wave-after commit, or the final code-review.

| Call site | Class | Under `AUTO_MODE = true` |
|---|---|---|
| 2i Dep failed? | BLOCKER | surfaces |
| 2j Halted? (3 failures spanning 2+ waves) | BLOCKER | surfaces |
| 3c plan-spec issue | BLOCKER | surfaces |
| Wave checkpoint commit failed | BLOCKER | surfaces |
| Verification failed on a step a later wave needs | BLOCKER | surfaces |

On an AFK timeout a BLOCKER waits and re-surfaces when the user returns; it never picks an option.

When `.ac/state/active-auto.json` owned by this session appears mid-run (ac:auto adopted the run), keep running in context with `AUTO_MODE` true and do not re-invoke yourself. While that marker is live the BLOCKER rows above do not surface either: record the block under `## Blocked` in the marker's decisions file, skip the blocked step and the steps that depend on it, and keep every independent wave going. The final commit's `--no-push` keys on that file (Phase 4a); `ac:auto` pushes after its gate when the user named the push.

`LANE_MODE` implies `AUTO_MODE`. Under `LANE_MODE` no gate calls `AskUserQuestion`: every BLOCKER row, plus each other site below that names one (the 1g and 2c plan-spec branch, the third briefing gap at 2e, 3c, and the 2f surface-first patch, all class `3c`), ends the turn with a `status: BLOCKED` block. Its `blocker` carries the class from `lane-protocol.md` (`2i`, `2j`, `3c` or `commit`), the question, the options the `AskUserQuestion` would have offered as single-token labels, and the recommended label. The marker stays, because the run resumes rather than ends. A `RESOLVE <label>` message continues as if the user had chosen that label, including that option's own marker handling: an option that stops the run deletes the marker and ends with `status: FAILED`.

BLOCKER gates surface whatever the mode,
because each needs judgment auto mode cannot supply. Before surfacing one, emit a line naming which class fired.
`AUTO_MODE` stays set through a BLOCKER unless the user picks an option that stops the run.

Heartbeat: one short line per phase, wave, and iteration transition.
</auto_mode>

<bootstrap>
Nothing to load and no task list to register (see Progress surface). Begin at Phase 1a.
</bootstrap>

## Phase 1: Load Plan

### 1a. Parse arguments

- Strip `--auto` flag if present → `AUTO_MODE = true`, per the `<auto_mode>` policy: halt only on BLOCKER classes.
- Strip `--lane` flag if present → `LANE_MODE = true`. Set by the `ac:lane` subagent that `/ac:coordinate` dispatches. Implies `AUTO_MODE = true`, `NO_QA = true` (parallel lanes would collide on dev-server ports) and no push at 4a.
- Strip `--max-parallel N` if present → `MAX_PARALLEL = N`, the cap on workers running at once within a wave (2c). Default unlimited; a lane passes 5.
- Strip `--no-oracle` flag if present → `NO_ORACLE = true`. Skips the `ac:oracle` spawn at 3b.
- Strip `--no-qa` flag if present → `NO_QA = true`. Skips the Phase 3e QA pass whatever the plan's `**QA**` line says.
- Strip `--no-checkpoint-commits` flag if present → `NO_CHECKPOINT_COMMITS = true`. Disables wave-after commits; Phase 4 final commit still runs.
- Resolve the remaining argument to `PLAN_PATH`:
  - If it contains `/` or starts with `.ac/`, use as full path.
  - Otherwise treat as slug: `.ac/plans/<slug>/plan.md`.
- If `PLAN_PATH` does not exist: print `Plan not found at <path>. Run /ac:plan first.` and stop.
- If `AUTO_MODE = true`, emit one user-visible line: `Auto mode engaged. Will run end-to-end, halting only on BLOCKER classes (Phase 2i dep-failed, Phase 2j 3-strike, Phase 3c plan-spec issue, error-handling halts).`

### 1b. Read and parse the plan

Read `PLAN_PATH` in full and hold: the frontmatter (`Steps`, `Waves`, `Codebase State`, `Generated`, `QA`), `## Research Summary`, `## Codebase Conventions` including the `TDD` field,
`## Reuse Map`, `## Work Objectives` (Core Objective, Concrete Deliverables, Definition of Done, Must Have,
Must NOT Have), `## Execution Strategy` with its Dependency Notes, every step in `## Steps` with all its fields,
and `## Risks Accepted`.

Set `QA_ENABLED = true` only when the frontmatter carries `**QA**: true`; an absent line means false. Read the line from
the frontmatter only (the text above the first `## ` heading), because a step's own `**QA**:` field can sit at column
zero in flat-style plans.

### 1c. Tier routing and escalation

| Tier | Subagent | Model | Effort |
|---|---|---|---|
| `quick` | `ac:plan-worker-quick` | `haiku` | medium |
| `junior` | `ac:plan-worker-junior` | `sonnet` | high |
| `junior-high` | `ac:plan-worker-junior-high` | `sonnet` | high |
| `senior` | `ac:plan-worker-senior` | `opus` | medium |

`junior-high` runs junior's model and effort, for work at the borderline of coupling or context depth. The
criticality rule never routes there; it escalates to `senior`.

Pass the Agent tool's `effort` parameter on exactly one spawn, the 2e effort retry; this skill is the explicit
instruction its description reserves it for. Every other spawn omits `effort` and runs at the table's default.

When the plan's `Codebase State` is `legacy` or `chaotic`, route every `quick` step to `ac:plan-worker-junior`
whatever its declared tier: mechanical work in an inconsistent codebase is not mechanical. The plan file is not
modified; this is an in-memory routing decision. Record the count for the Phase 4 report.

### 1e. Initialize execution state

```
ACCUMULATED_WISDOM = []                 # max 15 items total, max 5 added per wave
MODIFIED_FILES = []                     # tracked across waves; passed to Phase 3
STEP_FAILURES = []                      # one {step, wave} per step at terminal failure; 2j asks whether they span 2+ waves
WORKER_RETRY_PER_STEP = {}              # retries spent per step (effort rung, tier rung), max 2
```

Then write this run's marker, `.ac/state/execute/<slug>.json` (the plan slug, characters `[A-Za-z0-9._-]` only; a
hook ignores any other name), which the file-scope, SessionStart and `Stop` hooks read. Each running plan owns its own
marker, so another slug's marker is another run sharing the checkout, not a conflict. When this slug's marker already
exists with a different `session_id` and a `started_at` under 24 hours old, another session is running this plan:
say so in one line and stop without writing (under `LANE_MODE`, with `status: FAILED`), because two runs ticking one plan's checkboxes corrupt its state. An
older one, or one this session owns (a resume), is overwritten. Fields: `slug`, `session_id` (write exactly `${CLAUDE_SESSION_ID}`, which Claude Code substitutes with this session's id;
it scopes the `Stop` guard to this run), `started_at` (24-hour age bound; take it from `date -u +%Y-%m-%dT%H:%M:%SZ`,
never from your own sense of the time, since a local time with a `Z` reads as the future and disarms the guard), `pid` (advisory, write `0`), `current_wave`, `wave_files`, `note`. Schema and
per-field reasoning at `${CLAUDE_SKILL_DIR}/references/execution-state.md`.

Lifecycle: written here, refreshed at 2c and 2f, deleted at 4a and on every branch that ends the run early. Every
read, refresh and delete in this body names this run's own file and never touches another slug's.

Also keep the output of one `git status --porcelain` taken now as `BASELINE_DIRTY`: 2d never restores a path that was
already dirty before this run started, since it may belong to another run or to the user.

`.ac/state/active-auto.json` may coexist beside it. That marker belongs to `ac:auto`, not to this skill: never
delete it, and treat its presence only as the signal read at Phase 4a.

### 1f. TDD mode

Read the plan's `## Codebase Conventions` for `**TDD**` and set `TDD_MODE`: `"tdd"` directs each worker to write the
failing test first, `"tests-after"` to write tests after implementation for any behavioral change, `"none"` to write
tests only when a step's `Done when` demands testable behavior. A missing field defaults to `"none"` and gets noted
in the Phase 4 report. The value is injected into every worker briefing.

Read project `CLAUDE.md` and `CLAUDE.local.md` for build, test, and lint commands as `RUNTIME_CONTEXT`. Workers
receive the `CLAUDE.md` rules but never this skill's workflow rules, so briefings cite those commands explicitly.
When `CLAUDE.md` has a `## Verification gate: ci` section (see 3a) and the checkout sits on the default branch,
`git switch -c <slug>` before the first wave commit, so the pull request branch carries them, and run the section's
bootstrap command once if it names one.

### 1g. Confirm the progress surface

No list to register. Read `Waves` and `Steps` from the plan frontmatter and hold both: `Steps` is what every
Layer D count gets compared against, and `WAVES` is how many barriers the run will pass. State both in the
Phase 2a render.

Then run the shape gate once:

```
Bash: node "${CLAUDE_PLUGIN_ROOT}/cli/ac.js" plan-check <PLAN_PATH>
```

It prints the step counts on every exit and, when the plan deviates from what the rest of this body parses, one
line per deviation. Route by what it reports, taking the first route below that matches, except
that a BLOCKER route always wins over a continue route on the same step:

- **Exit 2**: the plan file is not where you looked. Re-derive `PLAN_PATH` from the argument and try once; if it
  still fails, say the path you tried and stop.
- **Exit 0**: continue. Hold the step counts it printed for Layer D; on a resume the unchecked number is what is
  left to run.
- **`All <N> Step N headings are present, so the step lines are missing their prefix`**: repair, do not stop: only
  the checkboxes are absent, and without them Layer D and the `Stop` guard have nothing to count. Insert one
  `- [ ] **Step N**: <the heading's own title>` line per step with `Edit`, keeping the space after the bracket
  because the `Stop` guard greps for it, then re-run `plan-check` and say in one line that you repaired it and how
  many lines you added.
- **`step(s) are absent from the body rather than merely unticked`**: the plan is truncated, not unticked. Do not
  invent checkboxes and do not correct the frontmatter down to what survived. Say how many steps are missing and stop.
- **A worker step with no `Tier`, or a verification step with no `Commands` or `Evidence`**: a plan-spec defect;
  do not pick a tier yourself, since that is the planner's cost decision. Take the 3c plan-spec BLOCKER branch,
  naming the steps and what each is missing. **This wins over the next route**: routed on its fields, a step with an
  unrecognised `Type` and no `Tier` reads as a verification step and its code never gets written.
- **A `Type` outside the three, on a step this list has not already blocked**: route on the step's fields instead
  of its label, and say in one line which steps you re-read and as what. A step carrying a `Tier` is a worker
  step; a step carrying `Commands` and `Evidence` with no `Tier` is a verification step. `implementation` maps to `code`.
- **A missing `**QA**:` line as the only ERROR** (plan-check prints `no` + the field + `line`): the plan predates the
  field. Continue with `QA_ENABLED = false`, as 1b already reads an absent line, and say so in one line.
- **Any other ERROR** (a missing `Files`, `Description`, `QA` or `Must NOT`, a leftover placeholder, a missing
  `Auto mode` line): a plan-spec defect, since the briefing inlines four of those five fields verbatim. Take the 3c
  plan-spec BLOCKER branch and name the steps and fields.
- **A count mismatch the ticks do not account for**: the frontmatter and the body disagree about how many steps
  exist. Say which two numbers you got and stop; every later Layer D comparison rests on this one.

WARN lines never gate the run. Say how many there were in one line and continue.

## Phase 2: Execute Wave-by-Wave

Goal: run each step to verified completion, wave by wave, on auto-continue. The user does not approve each step.

### 2a. Present execution strategy

Render the wave breakdown once using the shape at `${CLAUDE_SKILL_DIR}/references/wave-orchestration.md` under
`## Phase 2a execution-strategy render`.

Then start Wave 1 in the same turn. There is no confirmation gate: typing `/ac:execute` is the consent, and the
plan was approved at `ac:plan`. Auto-continue applies until Phase 4 or a BLOCKER.

### 2b. Worker briefing template (the 6-section prompt)

Every worker invocation receives the 6-section briefing. For the exact template (with VERBATIM/DERIVED field annotations), read `${CLAUDE_SKILL_DIR}/references/worker-briefing-template.md`.

**The briefing is the worker's whole world.** The worker does not read the plan, so Section 6, with `briefing-common.md`,
carries the step's pattern references, the codebase conventions, the invariants it must preserve and the plan-wide
guardrails. Assemble all four from the plan you are holding.

**Write the shared blocks once.** Before Wave 1's spawns, write `.ac/plans/<slug>/briefing-common.md` with the
blocks that are identical for every step, per the template's `## briefing-common.md` section: Runtime Commands,
Codebase conventions, the Core Objective and the plan-wide guardrails, all verbatim. Write it once per run (a
resumed run overwrites the previous run's copy, since the plan may have changed) and do not repeat those blocks in
the per-step briefings. Each per-step briefing opens with a line telling the worker to `Read` that file by absolute
path, then carries only the step-specific sections. 20 of 100 measured plans did this unprompted and 206 worker
runs read such a file, so the worker reads it reliably and the orchestrator stops paying for the same blocks once
per step.

**Resolve every sibling-step pointer before you send it.** Wherever the step's `Description`, `QA` or `Must NOT`
names another step by number ("call Step 4's parser", "same constraint as Step 10"), replace the pointer with what
the worker actually needs: the sibling's `Files` path and a one-line statement of the contract, or the `file:line`
the thing will live at. A forward pointer to a step that has not run yet is the dangerous case, because there is no
source to fall back on.

Length rule: a per-step briefing and `briefing-common.md` together under 30 lines is too short; under-spec'd
briefings produce drift. The contract fields go in verbatim, in the per-step briefing (`<constraints>`).

### 2c. Launch workers in parallel within the wave

**Refresh this run's marker first**: `current_wave` to this wave's index, `wave_files` to the union of every absolute path
in this wave's steps' `Files`. The file-scope hook lets a worker write exactly that set, so the union has to be
complete before any spawn.

**Route on `Type`**: `code` and `infra` spawn a tier-routed worker; `verification` does not spawn. Run its `Commands`
directly via Bash and capture to its `Evidence` paths. For a verification step Layer A blends with your Bash output,
Layer B is largely n/a, Layer C is the evidence file, and Layer D still applies. A `Type` outside the three was
resolved at Phase 1g by reading the step's fields; use what 1g decided rather than re-deciding per step.

**Check invocation reachability before the wave launches.** When a step's Description tells you to run a slash
command, read that component's frontmatter (not a grep of the whole file, since several skills discuss the flag
without setting it): `disable-model-invocation: true` means only the user can type it. Then take the plan-spec
BLOCKER branch in 3c and say which command and which step. Do not quietly substitute executing the command's body
yourself: that tests the procedure, not the dispatch the step claims.

Spawn every `code` and `infra` step of the wave in one message, one `Agent` block each, each with
`run_in_background: true`. Wait for all of them before verifying any, by ending the turn with a one-line status;
when a task-notification arrives while others still run, end the turn again. Never wait with a `sleep` or `until`
loop, a file-stability check, or repeated reads of evidence files; the Stop guard allows the stop while workers run. Do not spawn one step,
verify it, and then spawn the next: a wave whose steps share no files has no reason to serialize. A wave the plan
declares as an ordered track (its Execution Strategy says the steps must run in sequence) is the one exception, and
there the steps run one at a time in the declared order.
With `MAX_PARALLEL` set and fewer slots than steps, the first message spawns that many steps in the wave's declared order, and each task-notification that arrives spawns the next queued step before the turn ends; verification still waits for every step of the wave.
Name the wave's steps in one line before the spawns.

### 2d. Wave verification (4-layer, runs once per wave)

Every worker in the wave has returned. Now verify, once, for the whole wave. You are the QA gate.
A worker's report is a claim, and automated checks alone do not confirm it.

**Confirm no mutation survived.** Run `git status --porcelain` in the same message as the diff and the
Layer A commands; it does not depend on their results and they do not depend on its.

The allowed set is `wave_files` (this wave's declared union, from 2c) plus `MODIFIED_FILES` (earlier
waves) plus anything under `.ac/`, plus the `wave_files` of every other marker in `.ac/state/execute/` and every
path already dirty in the `git status --porcelain` you took at 1e: another run may share this checkout, and its
files are not yours to restore. A dirty path outside all of these is an unreverted mutation or an
out-of-scope edit, typically through `Bash`, which the file-scope hook cannot see: restore it from git, and record
it as a `[REMEDIATION] Step <N> <tier>: <what you restored>` wisdom line. Compare against `wave_files`, not against
`MODIFIED_FILES` alone, which is only appended at 2e. A worker's temporary patch inside its own `Files` passes this
check; the diff shows whether it survived.

Then take the wave diff, which is Layer B's input:

```
Bash: git add -A -- <wave_files> && git diff --cached -U8 -- <wave_files>
```

Stage first, and diff the index: a plain `git diff` shows nothing for a file the wave created, because an untracked
path has no committed side, so every created file would be invisible to Layer B and every claim on it a false
"claim with no hunk". Staging does not commit; 2g still decides that.

Who runs what, the per-ecosystem commands and the diagnostics rule are in
`${CLAUDE_PLUGIN_ROOT}/references/verification.md`.

**This barrier is mandatory**: with no per-step checks, it is the only place a failure surfaces.

**Issue the wave's independent actions in one message.** The mutation check, the diff, the typecheck, the build,
the test run and the linter are one message with six tool calls, not six turns. Same for the wave's checkbox ticks
in Layer D, and for the QA scenarios in Layer C that touch different surfaces: only calls issued together cut the
turn count. Serialize only where one call's output decides the next one's arguments.

**Layer A: Automated**

**Layer A authority**: when the changed files sit under a sub-project root (its own `package.json` AND `tsconfig.json`,
and not the orchestrator's cwd), that sub-project's own commands win for the typecheck, the build and the tests, run
inside the sub-project dir (`cd <sub-project-root> && bun run tsc --noEmit`, its `package.json` scripts, or the
language equivalent). The outer LSP cannot resolve sub-project deps, so its diagnostics on those files are Class 5
boundary noise. With no sub-project boundary, the orchestrator's LSP is authoritative.

1. Run the project-wide static analysis once for the wave (PHPStan, `tsc --noEmit` or `tsc -b`, `flutter analyze`;
   sub-project local per the authority rule above). It is the one project-wide check a wave keeps, because a
   per-file analyzer cannot see a caller that a changed signature broke. When the project has no project-wide
   analyzer (a Laravel app without PHPStan, plain JavaScript), add to item 3 the tests of the callers of every public
   symbol the wave modified (`LSP findReferences` on each), or run the full suite for this wave.

   An LSP diagnostic is a hint, not a result. Before you act on one or call it stale, read the
   `CLI check for <file>` result of the PostToolUse hook for an edit made on the main thread (PHP: beside the edit, and only on errors; Dart: a background reminder that arrives only on issues; silence means clean or not run), which does not run inside a subagent, a lane's orchestrator included,
   or run the file's CLI analyzer (`verification.md`, "Diagnostics are a hint"). Then classify every diagnostic into one of six noise classes before
   acting on it; the classes and how to tell a transient from a real error are at
   `${CLAUDE_SKILL_DIR}/references/lsp-noise-classes.md`. Classes 1 and 3 are transient and get re-run at the wave
   barrier; classes 2, 5, and 6 are persistent false positives that never block; class 4 is a real error and routes
   to Phase 2e. The plan's `**LSP false-positive whitelist**` field, when present, is the authoritative skip list.

   WARNING severity (regardless of class) is logged in Issues and continues.
2. Run the project's build command (from `RUNTIME_CONTEXT` or `CLAUDE.md`). Exit code 0 required.
3. Run the format check and the linter on the wave's touched files, and the tests related to them (the tests the
   workers wrote or edited, plus the tests that cover the changed source), once, for the wave, in parallel. The
   commands per ecosystem are in `verification.md`. Do not run the full suite or a repo-wide lint here; Phase 3
   runs them once. Verify once; do not re-run a check that already passed to build confidence. All selected tests
   must pass. A failure in a test the wave did not touch counts as pre-existing only after you saw it fail without
   the wave's change, or the project records it as known; name it under Issues either way.

   Filter output as the Output length rule says; on failure, admit the failing cases and nothing else. A failure
   the wave's checks catch that no single step explains is a cross-step interaction, which routes to remediation
   below rather than to one step's retry.

**Layer B: Manual Code Review (read the wave diff, do not skip)**

This is the layer you are most tempted to skip. Do not skip it. Review the diff rather than re-reading whole files:
against a worker that overstates what it did, the delta itself is the stronger instrument.

1. Read the wave diff taken above, hunk by hunk. A file this wave created is already in it whole, as added
   lines, so it needs no `Read`. When the diff comes back as a persisted preview (`Output too large ... Preview`),
   read the saved file in windows before reviewing; the preview is the first 2KB, not the wave. Read beyond the diff only on one of these three triggers, which are the whole
   list:
   - the file is under 150 lines, where reading it whole costs no more than reading its hunks;
   - the diff carries deletion hunks, where what was removed matters as much as what replaced it;
   - the step declares a contract in its `References` that the hunk appears to change.

   Outside the 150-line case, read the region around the hunk with `Read` `offset` and `limit` (about 60 lines
   each side), not the whole file: everything you read stays in your context for the rest of the run.
   "When it looks ambiguous" is not a trigger. If you find yourself opening files outside this list,
   the plan's `Files` were wrong and that is a finding, not a reason to read more.

2. For each hunk:
   - Does the logic actually implement the step Description?
   - Are there stubs, TODOs, placeholders, hardcoded values that the step did not authorize?
   - Are there logic errors or missed edge cases evident from the data flow?
   - Does the change follow the plan's Codebase Conventions and `my-coding`?
   - Are imports correct and unused imports removed?

3. **Attribute every hunk, file first.** Attribution is by file: each hunk belongs to the step whose
   `Files` declares that path, which is deterministic from the plan. Fall back to the workers'
   `path:start-end` claims only when two steps of the same wave share a file. Line ranges cannot carry attribution
   on their own: concurrent workers shift each other's ranges, `-U8` merges nearby regions into one hunk with two
   claimants, and nothing bounds a claim's width.

   Then check the claims against the diff. Three outcomes, and the first two fail the step:
   - a hunk in a file no step declares: an out-of-scope write that only this check sees (the file-scope hook
     gates on the wave's union). Treat as failed and route to 2e.
   - a claim the code contradicts: the worker described something it did not do. Treat as failed.
   - a claim with no hunk, or a hunk no claim mentions, inside a file the step does own: a reporting
     gap, not a code defect. Record it and continue; a formatter the worker ran leaves exactly this.

4. **Run the two checks the diff cannot give you**, because duplication lives in files you were never
   going to open: `LSP findReferences` on each newly exported symbol, and one repo-wide `Grep` for each
   new function name. They catch a second definition of something the wave just wrote.

5. If you cannot explain what each hunk does in one sentence, you have not reviewed it. Read again.
6. **Cross-file consistency check** (mandatory whenever the wave produced two or more files that share an interface). It also covers the diff's known weakness, that a hunk does not show what the surrounding code now does, so it is not optional just because the diff read quickly. Apply it to every shared-interface boundary the wave's files declare or consume, not just the first. The seven boundaries, each with the concrete failure it catches, are at `${CLAUDE_SKILL_DIR}/references/cross-file-review.md`: shared data shapes, URL and path composition, component and function name match, template engine interop, front-matter is data not template, asset paths, link target reachability. Read that file at the first wave where the check applies.

**Layer C: Hands-on QA (per step, run here at the barrier)**

This layer stays per-step: each step names its own scenario and evidence path. Run every step's scenario here, in
one pass over the wave, rather than between spawns.

Skip the scenario for any step Layer B already failed: its code is about to be retried. Run it after the retry
instead, alongside that step's re-verification in 2e.

When the step's `QA` field names a tool, run the scenario and gate it on four checks:

- **Reproducer-validity**: one command, fails on HEAD before the change (for a fix or regression step), deterministic
  across 3 runs, no external service that can flip the result. Mark a dimension n/a rather than skipping it.
- **Evidence, not assertion**: record the command and its output, or an artifact path. A bare "verified" is not evidence.
- **Lowest layer that proves it**: a unit test beats an integration test beats an end-to-end run when all three would
  prove the same thing. Escalate only when the lower layer cannot reach the behavior.
- **Browser as a human user**: for any UI-touching step, walk it through the browser (navigate, interact, assert on
  rendered state), not just `curl`. `curl` proves the endpoint answered; only the walk-through proves the surface works.

Capture to `.ac/plans/<slug>/evidence/<step-id>-<scenario>.<ext>`: `.png` for a browser screenshot, `.json` for a
curl body, terminal output for a CLI or test run. Steps with no `QA` field, or `QA: none`, skip this layer.

**Layer D: Plan state check (per step)**

Run each step's provable `Done when` criterion first: the one command it names, batched into the same
message as the ticks. These are greps and single targeted assertions, not scoped suite runs; running them is
what stops the tick from being a claim.

Tick each verified step's checkbox from `- [ ]` to `- [x]` with `Edit`, one edit per step. Confirm the wave's
ticks landed with `grep -c '^- \[ \]' <PLAN_PATH>` and check the number against what you expect, which is
the plan's total step count minus every step ticked so far. Do not re-read the plan to check: you already hold it from Phase 1b.

The tick stays per-step rather than one edit per wave: the `Stop` guard derives "no progress" from this count
falling between blocks and latches permanently once that fires, so batched ticks would retire it for the run. The
tick is also the only durable record of which steps inside a wave finished.

### 2e. Verification outcome routing

Verification runs per wave, so route per step off what Layer B attributed. A wave-suite failure or a
Layer B finding belongs to the step whose claimed hunks explain it; a failure no step's hunks explain is a
cross-step interaction and goes to 2f remediation, not to a retry.

**All four layers pass**: append the wave's files to `MODIFIED_FILES` and continue.

**Worker reported `[BRIEFING GAP]`**: it could not proceed because something Section 6 should have carried
was missing. Re-assemble the missing block and re-spawn at the same tier. Never escalate for this: the
tier is not what failed.

**Bounded at two.** The re-spawn does not count against the two-retry budget below, so it has its own bound (when
the plan itself lacks the block, every re-spawn reports the same gap). On the third report for one step, stop re-spawning and take the plan-spec BLOCKER branch in 3c: name it, then `AskUserQuestion`
(`Edit plan to fill the gap and re-verify` / `Accept as Risk and proceed` / `Stop`).

**Failures attributed to one step** climb two rungs at most, each counted in `WORKER_RETRY_PER_STEP`:

1. **Effort rung, first failure** of a `quick`, `junior` or `junior-high` step: re-spawn at the same tier with the
   Agent tool's `effort` one step above the tier's default (`quick` to `high`; `junior` and `junior-high` to
   `xhigh`). Skip the rung when effort cannot rise: Haiku 4.5 on Bedrock, Vertex and Foundry takes no effort
   parameter, and `CLAUDE_CODE_EFFORT_LEVEL` set to any value removes the parameter from the Agent tool. Then the
   first failure goes straight to rung 2. The rung follows the tier actually spawned: a `quick` step routed to
   `ac:plan-worker-junior` by the codebase-state rule in 1c retries at `xhigh`.
2. **Tier rung, second failure** (or the first when rung 1 is skipped): re-spawn one tier up (`quick` to `junior`,
   `junior` and `junior-high` to `senior`) at the new tier's default effort, with no `effort` argument.

Record each rung as it fires, as a wisdom line for the current wave: `[RETRY] Step <N> <tier>: rung <1|2>, <one-line
cause>`, with the tier that failed, and nothing when no rung fired. `[RETRY]` lines do not count toward the five
wisdom items in 2f; `ac plan-stats` reads them to measure what each tier costs in quality.

`senior` has no rung 1, because Opus 5.5 scores best at medium, and no rung 2, because nothing sits above it: a
senior step's first failure is terminal. A failure after rung 2 is terminal too. Record a terminal failure the same
way, `[RETRY] Step <N> <tier>: terminal, <one-line cause>`.

These re-spawns keep the step's current effort and do not advance the ladder: a malformed report with no
`### Changes Made` or `### Verification` (re-spawn at the same tier with a format reminder; a second malformed
report counts as the step's first failure) and a `[BRIEFING GAP]` re-spawn.
The retry briefing leads with the failure context, then repeats the original.
Two fast paths skip rung 1: a worker flagging `tier mismatch` goes straight to rung 2 and the
mis-classification goes in the report, and a worker flagging `[CONTRADICTION]` does not retry at all,
because the next attempt hits the same structural conflict; mark it `pending-remediation` for 2f remediation.

**A retried worker is not verified until you verify it.** 2d ran before the retry spawned. After each retry, effort
rung or tier rung: re-stage and re-diff scoped to that step's `Files`, re-run Layer A, and re-run the attribution for
that step, before 2g commits.

**Terminal failure** (the tier rung failed, or a senior step failed first): append exactly one `{step, wave}` to
`STEP_FAILURES` for the step, however many retries it spent, and fire 2j at 3. Do not block the
wave on one failure unless 2i says a later wave depends on it.

### 2f. Remediation and wisdom

Runs after 2e, once every step has a terminal status (verified, failed, or `pending-remediation`).

1. **Remediate what the orchestrator owns**: `[CONTRADICTION]` reports, cross-file findings deferred from
   Layer B, and plan oversights your review surfaced. Apply the minimal patch to the file that structurally owns the
   missing piece, update `MODIFIED_FILES`, clear any `pending-remediation` step whose `Done when` now passes, and
   record each as a `[REMEDIATION] Step <N> <tier>: <what you fixed>` wisdom line (`Step - -` when no step owns
   it). Surface first when a patch would change a downstream contract;
   mechanical framework-completeness patches do not need a gate.
2. **Extract wisdom**: up to 5 concrete items this wave, 15 total, codified patterns rather than platitudes.
   `[REMEDIATION]` and `[RETRY]` lines are records, outside the 5 and the 15. Persist all of them to `wisdom.md`
   under `## Wave <N>`.
3. **Re-ground**: emit a 2-3 line wave summary and refresh the marker's `note` with a resume hint, which the
   SessionStart hook reads back. Re-read `PLAN_PATH` and `wisdom.md` only when a compaction has actually happened
   since you last held them; `grep -c '^- \[ \]'` already told you what remains.

### 2g. Wave checkpoint commit

When the wave changed tracked files and `NO_CHECKPOINT_COMMITS` is not set, commit after 2f, before the next
wave. `git commit -m "<one line naming the wave>" -- <wave_files> .ac/plans/<slug>`, not `/ac:commit`: that command injects a
7,000-character body and spends turns on style detection, once per wave, to produce a checkpoint the Phase 4
commit squashes anyway. The final commit at 4a is where `/ac:commit` earns its cost.

Commit the wave's paths explicitly, never `git add -A`: the parent repo may carry unrelated work, and `-A` would
snapshot it as this plan's deliverable, once per wave.

The gate is "did this wave change anything", which `git status` answers; no plan-wide label decides it, the
reviewer tier or the oracle default.

A commit failure here is a BLOCKER: print the git error and take the branch in
`${CLAUDE_SKILL_DIR}/references/execution-state.md`. Never auto-retry, because a failed commit usually means the
tree is in a state you did not expect.

### 2h. Progress table

After each wave, render the per-step table using the shape at
`${CLAUDE_SKILL_DIR}/references/wave-orchestration.md` under `## Phase 2h progress table`.

### 2i. Wave dependency check (before launching the next wave)

Before the next wave's workers launch, check whether any failed step is a hard dependency for it. The three sources,
in order: the plan's `### Dependency Notes`, a next-wave step whose `Files` names a file a failed step was to create,
and a next-wave step whose `References` point at a failed step's output.

If one failed, this is a BLOCKER even under auto mode. Emit one line naming it, then `AskUserQuestion` (header
`Dep failed?`, options `Stop and investigate (Recommended)` / `Fix the failed step manually and resume` / `Skip the
dependent steps and continue`). The first two delete the marker before halting; the third leaves it in place because
the run continues. Procedure at `${CLAUDE_SKILL_DIR}/references/wave-orchestration.md`.

If nothing hard failed, the next wave launches automatically. Auto-continue is the default between waves.

### 2j. 3-strike rule

When `STEP_FAILURES` holds 3 entries **spanning two or more distinct waves**, emit one line naming the
BLOCKER and `AskUserQuestion` (header `Halted?`,
options `Accept and continue (Recommended for known-isolated failures)` / `Fix manually and re-verify` / `Stop and
investigate`).

`Accept and continue` logs the failures, leaves the marker in place, and moves to the next wave; the failures surface
in the Phase 4 report. The other two delete the marker first, then pause or halt. This is a BLOCKER even under auto
mode: three accumulated failures make the `(Recommended)` qualifier unsafe to assume.

The two-wave span keeps the count meaningful: three failures inside one wave is one bad wave, not a systemic
pattern. An entry is one step at terminal failure, so a step that spent both retries before failing counts once.

### 2k. Loop until all waves complete

Run 2b through 2j for each wave in sequence, auto-continuing between them; only 2i and 2j pause the loop. When the
final implementation wave completes, advance to Phase 3.

## Phase 3: Final code-review

Goal: gate the deliver with one independent code-review pass on the actual implementation: does the work match the plan and meet quality bars.

**Aim for zero CRITICAL findings** from Phase 2's verification. The reviewer reports rather than gates, so a CRITICAL finding here costs a fix and a re-verify, not a loop.

### 3a. Final automated pass

Run the build in the foreground; the reviewer reads code that must at least build. Then start the full test suite
and the repo-wide lint with `run_in_background: true` in the same message that spawns the reviewer in 3b (a
project script whose name does not say test or lint, such as `make ci` or `composer qa`, goes under `timeout 3600`
so the Stop guard counts it as work that will finish), so the two run side by side. Both must be green before
Phase 4: when the background run notifies you, a failure there is a finding like the reviewer's and goes through 3c.
When the reviewer finishes first, end the turn with a one-line status; the suite's notification starts the next one.

**CI gate.** When `CLAUDE.md` has a `## Verification gate: ci` section, `LANE_MODE` is false and
`.ac/state/active-auto.json` does not exist, the build above is the only local run. Commit what is uncommitted, push,
open the pull request and start `timeout 1800 node ${CLAUDE_PLUGIN_ROOT}/cli/ac.js pr-watch <number> [--ignore <regex>]` (the
regex, if any, is the one the section names) under the `Monitor` tool in the same message that spawns the reviewer in
3b; `verification.md` ("Projects that gate on CI") says how to run it, what each line means and what the exit codes
are. A `VERDICT green` on the pushed head replaces the background suite and lint, and a red check (its `DETAIL` line names the cause) or a review line
(`COMMENT`, `INLINE`, `REVIEW`) is a finding that goes through 3c; the `THREAD` lines before the verdict only carry the ids for answering them. 3f closes the gate.

Then open this run's section of the review log, once: `Grep` `.ac/plans/<slug>/review-log.md` for
`^## Run <marker started_at>$`, and when nothing matches, add a blank line and `## Run <marker started_at>` at the
end of the file with `Edit` (or `Write` it when the file does not exist yet). Not a Bash `printf >>`: inside an
`ac:lane` worktree Claude Code refused that compound append in 16 of 25 runs.

The log is append-only across runs and this header scopes this run's entry; a second `/ac:execute <slug>` writes
its own section rather than reading the previous one, and checking for the header first stops a re-entry from
opening a duplicate.

### 3b. Spawn the reviewer

```
Agent({ subagent_type: "ac:plan-code-review",
        description: "Final code-review for <plan title>",
        prompt: "Plan: <PLAN_PATH>
Modified files: <MODIFIED_FILES, newline-separated>
Wisdom: <wisdom.md path>
<only when signal 1 below fired alone: Criticality surfaces by path: <the surfaces>. Weigh failure scenarios there.>" })
```

One reviewer, whatever the plan's size.

**Spawn `ac:oracle` alongside it only when the planner judged the change critical.** Three signals: signal 2 or
signal 3 fires it, signal 1 alone does not, and `--no-oracle` forces the skip either way:

1. `MODIFIED_FILES` lands on one of the closed six surfaces in `model-tiers.md` rule 5: authentication
   or authorization, payment or billing, cryptographic operations, user-input to SQL or shell or file
   path, file upload or deserialization, destructive migration.
2. Any step's `Why this tier` begins `rule-5-criticality`, the planner's own judgement written at Stage 5.
3. The plan carries an `### Oracle Sanity-Check Findings` section, meaning Stage 3.5 already found
   something worth a second opinion at planning time.

Signal 1 alone is weak, since a file path rarely announces "cryptographic operations" or "destructive migration":
it adds the `Criticality surfaces by path` line to the reviewer brief above and spawns no oracle. When signal 2 or 3
fired, the oracle runs at its own `high`.

```
Agent({ subagent_type: "ac:oracle", description: "Oracle strategic review for <plan title>",
        prompt: "Plan: <PLAN_PATH>
Modified files: <MODIFIED_FILES>
Research the plan was built on: <.ac/plans/<slug>/research/>
Wisdom from the run: <.ac/plans/<slug>/wisdom.md>
The change touches <the surfaces that fired>. Review the diff for failure scenarios on those surfaces,
and test the plan's claims about what the code does against the code: they are premises, not findings.
Plan compliance, reuse and caller impact are the code reviewer's; do not repeat them. Use your standard
report (Coverage, Premises, Findings with severity and CONFIRMED or PLAUSIBLE, scenario and fix, Bottom
line, Confidence)." })
```

### 3c. Act on the findings

The reviewer returns findings tagged CRITICAL, IMPORTANT or MINOR, each with a confidence. There is no
verdict and no revision loop. You are the filter, holding the plan, the wave history and the wisdom file:

- **CRITICAL**: fix it before Phase 4, with `Edit` at each cited `file:line`, smallest correct fix, the
  reviewer's `Fix:` line as guidance. Then re-run the per-file checks and related tests on what you changed
  (`verification.md`), and the full suite again only when the fix touched code other modules call.
- **IMPORTANT**: fix when the fix is small and local; otherwise record it in `report.md` and add it to
  the plan's `## Deferred Ideas`.
- **MINOR, or anything under confidence 50**: `report.md` notes. Do not touch the code for these.
- **An oracle PLAUSIBLE finding** names what would confirm it: run that check before acting on it as CRITICAL or IMPORTANT, and treat an unchecked one as MINOR.
- **An oracle REFUTED premise** means the plan is wrong about the code, whatever the Findings say: route it through the plan-is-wrong BLOCKER below, naming the premise and the quote. An UNSUPPORTED premise goes to `report.md` with the search the oracle named.

Expect volume: both reviewers report everything rather than pre-filter, so a long list does not mean bad code.

**A finding that says the plan is wrong rather than the code is a BLOCKER even under auto mode.** Name
it, then `AskUserQuestion` (`Edit plan to fix and re-verify` / `Accept as Risk and proceed` / `Stop`).
Never silently rewrite the plan.

Append the outcome to `.ac/plans/<slug>/review-log.md` under `## Run <marker started_at>`: first one line per
reviewer that ran, exactly `Review: <ac:plan-code-review | ac:oracle> CRITICAL <n> IMPORTANT <n> MINOR <n>`
counting the findings it returned, then what was fixed and what was deferred. `ac plan-stats` reads those lines to
judge a reviewer's effort level against what it finds.

### 3d. Convergence

CRITICAL findings fixed and re-verified, or none returned. Advance to 3e.

### 3e. QA pass

Runs when `QA_ENABLED` is true and `NO_QA` is unset. Otherwise emit one heartbeat line naming which of the two skipped
it and go straight to 3f under the CI gate, else Phase 4. A plan step that already walked the app live does not replace the pass: its Layer C
evidence reaches the tester as `Existing evidence`, and the tester skips those scenarios and still runs the rest.

1. Emit one heartbeat line (`QA pass: running ac:qa for <slug>`) and refresh the marker's `note` so a resume knows
   where the run stands (`Phase 3e QA in progress; run ac:qa --plan <slug> again or go to 4a`).
2. Invoke the skill. It never asks the user anything, so no `--auto` is passed:

   ```
   Skill({ skill: "ac:qa", args: "--plan <slug>" })
   ```

   Its tester runs in the background, so `ac:qa` may end a turn with `QA: tester running for run <run id>; resuming on
   its notification`. That wait is expected: the notification resumes inside `ac:qa`, and the `Stop` guards allow the
   stop. Do not poll, sleep or read the tester's output file, and do not treat
   that turn end as the QA result.
3. When the skill finishes, read `result.txt` (written by `ac:qa` in the directory of the block's `report:` path)
   and append its content to `.ac/plans/<slug>/review-log.md` under `## Run <marker started_at>`, the header 3a
   opened. With `report: none` the printed block is the record. When the file is missing, append the printed block
   plus `result.txt missing`, and still apply the rule below. Append its `fixed files` to `MODIFIED_FILES` (nothing
   for `none`). The skill has already triaged and fixed by the 3c rules and run its one retest, so do not re-triage
   or re-run it here. When `fixed files` is not `none`, re-run 3a (build, full suite and lint, in the foreground)
   before 4a, because 4a commits with `--skip-preflight` on the strength of 3a having covered those edits. Under the
   CI gate that re-run is the build alone; 3f's push and watch cover the rest.
4. Continue to 3f under the CI gate, else to 4a, in the turn the block prints. Under `--plan` the block is a hand-back to this skill, not a turn end;
   ending the turn on it would meet the live marker's `Stop` guard.

Every QA status (`passed`, `findings`, `could-not-run`, `skipped`) continues to Phase 4, and none is a BLOCKER: a
dev server that would not boot or a missing QA tool goes into the QA and Phase 4b reports. Findings the skill left unfixed live in its report, with open lows and unfixed mediums
added to the plan's `## Deferred Ideas`.

The pass sits before 4a, which deletes the marker and then commits and pushes, so QA runs inside the `Stop` guard
and its fixes reach the final commit.

### 3f. Close the CI gate

Runs only under the CI gate from 3a; otherwise go to Phase 4. The marker stays live through this step, so the `Stop`
guards cover the wait and the fix rounds, and 4a's commit then finds a clean tree and pushes nothing.

1. When the review or QA fixes moved the head since 3a's push, commit them (`/ac:commit --skip-preflight --no-push`
   with `MODIFIED_FILES` as its note), `git push -u origin HEAD`, start
   `timeout 1800 node ${CLAUDE_PLUGIN_ROOT}/cli/ac.js pr-watch <number> [--ignore <regex>]` under the `Monitor` tool as in 3a, and
   end the turn with a one-line status. When the head did not move, the 3a watch is the result.
2. `VERDICT green` on the current head: go to Phase 4. `VERDICT red` (exit 1) or a review line that is a CRITICAL or
   IMPORTANT finding: fix by the 3c CRITICAL rule, commit and push as in step 1, watch again, three rounds at most;
   what is still red goes into the 4b report, never a claim of a green gate. `VERDICT stuck` (exit 2) or exit 124 of
   a background `Bash` run: CI cannot gate this head, so run the full suite and repo-wide lint in the foreground as 3a
   does without the gate, and say so in the report. A Monitor that expired without a `VERDICT` line is armed again as
   `verification.md` says; it is not a reason to leave the gate.

## Phase 4: Deliver

Goal: commit, write the report, render the summary.

### 4a. Final commit

Before the marker goes, check `wisdom.md` once: every `[RETRY]` and `[REMEDIATION]` line must name `Step <N> <tier>:` (or `Step - -:` for a fix no step owns), because `ac plan-stats` counts an untagged one as lost data; correct it before closing.

**Delete `.ac/state/execute/<slug>.json` first**, this run's marker only, before the F7 check and any commit.

**F7 skip check**: run `git check-ignore -q` on every file in `MODIFIED_FILES`. If all are ignored and
`git status --porcelain` shows tracked changes not in `MODIFIED_FILES`, the parent repo has unrelated work that a
commit would snapshot as this plan's deliverable. Skip it, say so in one line, and record it in the report under
`## Notes` with the path and the count.

Otherwise invoke `/ac:commit --skip-preflight` with `MODIFIED_FILES` as its note, so it commits this run's files and
never another run's in-flight edits in the same checkout, plus `--no-push` when `LANE_MODE` is true or `.ac/state/active-auto.json` exists: an
unattended run has nobody present to approve a push, and `/ac:commit`'s branch guard only asks on `main` or `master`.
A lane checks `LANE_MODE` on its own because `.ac/` is gitignored, so its worktree never holds `active-auto.json`.
Without either, the final commit pushes. Phase 2d and Phase 3 already covered the verification `--skip-preflight`
refers to. A clean tree exits silently, which is fine.
### 4b. Report and summary

Write the report, `.ac/plans/<slug>/report.md` (under `LANE_MODE` `.ac/plans/<slug>/outcome.md`, because Claude Code
refuses a subagent's write to any `report*`, `summary*`, `findings*` or `analysis*` Markdown file), from the
template at `${CLAUDE_SKILL_DIR}/references/report-template.md`: Summary, Verification, Deferred and Notes only,
because the plan checkboxes, git and `wisdom.md` already hold the steps, files, commits and wisdom. Confirm
it landed with `test -f ... && wc -l ...`; retry the write once if it did not, and render the report inline if the
retry also fails, so the work is not lost in chat history.

Then render the closing summary inline from `${CLAUDE_SKILL_DIR}/references/execution-summary-template.md`. The
summary is chat output; `report.md` is the file artifact.

End the turn. Under `LANE_MODE` the last thing written is the `status: DONE` block, with `outcome.md` in `artifacts`.

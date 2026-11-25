---
name: parallel-impl
description: Run independent implementation tracks in parallel with disciplined review, merge, validation, and publication gates.
---

> References to plugin documentation files (e.g. `docs/workflow-artifact-templates.md`) refer to the plugin-level `docs/` directory (`../../docs/` relative to this file). Other `docs/` paths (such as artifact output destinations) refer to the target project.

## Purpose

Use this skill when a developer wants to implement a reviewed plan or task list with multiple parallel tracks without losing control of testing, integration, or review quality.

This is an execution skill, not a planning skill. Use it only after the feature already has accepted requirements, a plan, or an actionable task list.

Persistent team, squad, or fleet-style long-lived orchestration is out of scope for this skill. Use a separate orchestration layer if persistent coordination is needed.

## When to Use It

Activate when the developer asks for things like:

- "implement these tasks in parallel"
- "split this work into separate tracks"
- "have one model implement and another review each track"
- "parallelize the next ready tasks"

Also activate when:

- there are multiple dependency-ready tasks;
- the tasks touch different files or modules;
- the repository already has a documented validation path for the affected area.

## Project-Specific Inputs

Before you start, identify:

- the integration feature branch and final review target;
- the validation commands for each track;
- the repository's testing and quality gates;
- whether `ccc:conductor` is loaded in the current session for advisory quality checks;
- the worktree path for each parallel track (required when launching any parallel implementer track);
- any local rules for opening draft pull requests or track branches;
- the maximum revision rounds per track before escalation (default: 2);
- the maximum number of concurrent implementer agents (read from
  `.flow/defaults.json` key `concurrency.max-parallel-tracks`,
  overridable by explicit developer input; default: 3);
- the maximum number of concurrent reviewer agents (read from
  `.flow/defaults.json` key `concurrency.max-parallel-reviews`;
  default: 3).

If any of those inputs are missing, stop and get them first.

## Default Roles

Use separate roles for an **implementer** and a **reviewer**, and keep implementation and review judgment separate whenever possible.

Spawn each role as the plugin's named role agent — `flow:implementer` for tracks, `flow:reviewer` for review, `flow:scout` for discovery. Both runtimes resolve these plugin-qualified names, and the reviewer ships with read-only tools, so the implementation/review separation is structural rather than a matter of prompting. Runtime mechanics differ only in how you spawn and tune them: Claude Code uses the Agent tool, and its built-in `Explore` agent is an equally good read-only scout when discovery is pure search; Copilot CLI spawns them as subagents. Note that Copilot's `/subagents` tunes its own subagent roster and does not surface plugin-provided role agents, so per-role model overrides there go in `.copilot/models.yaml` (see `docs/model-selection.md`).

Give the implementer a scoped prompt with the exact task, files, TDD constraints, and concise quality expectations such as reuse before copy, single-purpose abstractions, and low-complexity control flow. Give the reviewer only the diff and the review criteria. The coordinator may share a factual brief — task boundaries, files, validation commands, known dependencies — across roles, but never proposed conclusions, review verdicts, or implementation rationale.

### Escalation: Fleet / Agent Team Mode

Treat any higher-cost orchestration mode the runtime offers (a Fleet command, Claude Code agent teams) as an explicit, developer-approved escalation, not the default. Default to standard per-role agents. Escalate only when there are more clearly independent ready tracks than the concurrency cap allows, each track has enough local context that repeated handoffs would be inefficient, specialized sub-roles would materially improve throughput or review quality, and the developer confirms the extra token spend is worth it — explain the rationale and ask before switching.

When approved, preserve the same role separation, assign one clear owner per track, keep reviewer authority independent from implementers, and fall back to standard agents if coordination overhead becomes noisy or ambiguous.

**Claude Code only — the `Workflow` tool.** For large batches whose track list is already known, Claude Code's `Workflow` tool is a further rung: it pipelines tracks through implement-then-review stages deterministically, with schema-validated returns and resume-from-cache after a failure. It requires explicit developer opt-in and cannot be invoked on the coordinator's own initiative — offer it, never assume it. If approved, carry this skill's caps **inside the script**: `Workflow`'s own concurrency limit is `min(16, cores-2)`, far above `max-parallel-tracks`, so a workflow that inherits the runtime default will burn quota several times faster than Core Rule 4 intends. Copilot CLI has no equivalent; its nearest analogue is `/fleet`, already covered above.

### Model Selection

Resolve the active model for each role using this priority chain:

1. **Project config** — look for the runtime-specific config file in the current project root:
   - Copilot CLI: `.copilot/models.yaml`
   - Claude Code: `.claude/models.yaml`

   These are plain YAML files (no markdown, no fenced blocks). Read the `implementer`, `reviewer`, and `scout` keys directly. If a key is absent, fall back to the baked-in default for that role — do not re-prompt for a key that is missing.

2. **Session cache** — if models were already confirmed earlier in this session, reuse them without asking again.
3. **Baked-in defaults** — if neither config file nor session cache exists, use the tier defaults below silently without prompting. Create project model config only when the developer wants persistent overrides.

#### Default model tiers

Defaults are **tiers, not pinned versions** — resolve each tier to the latest model of that tier available in the active runtime. In Claude Code, pass the tier alias to the Agent tool (`haiku`, `sonnet`, `opus`) — aliases are the only values it accepts, so Claude Code always runs the tier's latest model. Pinning an exact model version via `models.yaml` is a Copilot CLI capability (`.copilot/models.yaml` only).

| Role        | Claude Code                          | Copilot CLI                      | Effort |
|-------------|--------------------------------------|----------------------------------|--------|
| Implementer | `sonnet` (latest Sonnet)             | latest Claude Sonnet             | high   |
| Reviewer    | `opus` (latest Opus)                 | latest GPT or latest Claude Opus | high   |
| Scout       | built-in `Explore` agent, or `haiku` | latest Claude Haiku              | low    |

See `docs/model-selection.md` in this plugin for the full role matrix, per-role effort guidance, and the premium-tier (Fable) opt-in policy, and `docs/models-config-template.md` for ready-to-copy config templates.

## Core Rules

### 1. Only parallelize truly independent work

Before launching tracks, read the current tasks and dependency notes, choose only tasks that are ready now, group work by clear ownership boundaries, and serialize anything that touches the same tight code region, unstable contract, or unfinished prerequisite. If in doubt, serialize.

### 2. TDD stays mandatory on every code-bearing track

Each implementation track must add or update failing tests first when behavior changes, implement only enough to make the tests pass, and refactor while the tests remain green. Do not allow implementation-first drift just because work is parallel.

### 3. Keep code quality explicit, not implied

Each code-bearing track should bias toward reuse before duplication (**DRY**), small single-purpose units with clear responsibilities (**SOLID** where it fits), and low-complexity control flow with explicit boundaries.

If `ccc:conductor` is available in the current session, use it as
an advisory quality pass on reviewable track diffs or on the integrated feature
branch before publication.

### 4. Hard concurrency cap

**The caps exist to bound quota burn rate.** Concurrent agents consume
5-hour and weekly usage limits in parallel, so an unbounded batch can exhaust
them long before the work is done. The runtime's own capacity is not the
constraint and never was — burn rate is. Evaluate every cap decision against
that.

**Never exceed the configured `max-parallel-tracks` limit.** The default is
**3** concurrent implementer agents. Read the active cap from
`.flow/defaults.json` → `concurrency.max-parallel-tracks`,
then apply the override precedence (explicit developer input > defaults.json >
baked-in default of 3).

When more ready tracks exist than the cap allows, **queue** the excess tracks
and launch them as running tracks complete and free a slot.

Raise the cap above the default only when the developer explicitly requests it
(e.g., "use at most 4 parallel tracks") **and** the track boundaries are
obvious, the validation surface for each track is small, the final integrator
can still review and merge each track deliberately, and the developer accepts
the faster burn.

Count every running implementer agent, including any rescue agent, against the
cap. A rescue agent occupies a concurrency slot like any other agent.

**Cap concurrent reviewers too.** Reviewers run on the top tier at high
effort, which makes each one the most expensive agent this workflow spawns —
more expensive than the implementers the track cap governs. Bounding
implementers while leaving reviewers unbounded would cap the cheaper half of
the batch and let the costlier half run free. Read
`concurrency.max-parallel-reviews` from `.flow/defaults.json`
(default: **3**, matching the track cap so review never becomes the
bottleneck). A review that waits for a slot is queued, not skipped — the
coverage-first contract in Step 6 is unaffected.

Scouts stay exempt from both caps: they run on the cheapest tier at low
effort and are short-lived, so serializing them buys nothing. In Claude Code,
launch independent scouts together in a single message so they run in
parallel.

### 5. Never run a rescue agent while the original agent is still running

**This is a hard prohibition, not guidance.**

Two agents on one track burn quota twice for one track's worth of work,
double rate-limit pressure, and risk conflicting writes to the same worktree
or branch. Replacing an agent is therefore a *stop-then-start* sequence, never
an overlap.

The coordinator can stop a running agent — Claude Code's `TaskStop` accepts a
background agent by name or ID, and Copilot CLI manages subagents through
`/tasks`. So "I could not stop it" is not a reason to run two. Stop the
original, confirm it stopped, then start the replacement.

Before any rescue action, the coordinator **must** confirm one of these:

1. the original agent has returned a final result (success or failure);
2. the original agent has timed out, crashed, or been stopped by the
   coordinator, and the runtime has reclaimed it;
3. the original agent has explicitly reported that it cannot proceed.

If the coordinator cannot confirm termination, **the agent is not stalled —
it is still working.** In that case:

- do not spawn a rescue agent;
- do not duplicate the track;
- send a **continuation nudge** to the original agent (see Workflow Step 5)
  and wait for a response before re-evaluating.

A rescue agent, when eventually justified, replaces the original — it does
not run alongside it.

### 6. Temporary work surfaces are disposable, not permanent state

If the workflow uses worktrees, branches, or other sandboxes:

1. treat the integration **feature branch** as the long-lived review surface that
   will eventually back the PR;
2. treat track work surfaces as temporary and batch-owned;
3. record, for each track:
   - track name;
   - owned task IDs;
   - owned files or modules;
   - validation commands;
   - merge target;
   - track branch name;
   - external worktree path;
   - current state (`active`, `merged`, `abandoned`, `blocked`);
4. do not silently discard dirty track state.

Every implementer track must run in its **own git worktree outside the project
directory**, such as `../{repo}-wt-{track}`. Do not run parallel implementers in
the main project working tree or inside nested directories beneath the project
root; that increases the risk of index and branch-state corruption.

The coordinator provisions the worktree; the implementer works inside it by
**absolute path**. A coordinator cannot set a spawned agent's working
directory, and a spawned agent cannot relocate itself into an external
worktree — Claude Code's `EnterWorktree` accepts an arbitrary registered path
only from the main session, while an agent whose working directory was pinned
at launch may enter worktrees beneath the repository's own `.claude/worktrees/`
and nothing else. So the track packet must name the absolute worktree path and
require every file and git operation to use it: `git -C <worktree> …`, and
absolute paths for reads and writes.

**Copilot CLI requires one extra step.** It verifies file paths against an
allowed list, and an external worktree is outside the project directory, so
every operation against it — including a plain `ls` — is refused with
"Permission denied and could not request permission from user" until the path
is allowed. Grant it once per track worktree, after Step 3 creates it and before that
track's implementer launches. Track worktrees are created mid-session, so
`/add-dir` is the applicable form; `--add-dir` only helps when the paths are
known before the session starts. If the runtime will not let the coordinator
grant the path, stop and ask the developer to run `/add-dir` — do not launch
the track and hope. Skipping this does not degrade gracefully: the track fails
on its first file operation.

Do not use per-agent disposable isolation (Claude Code's Agent-tool
`isolation: "worktree"`) for a named track: it provisions a worktree at a
location the runtime chooses, which cannot satisfy the external-path rule above
and leaves no durable surface to merge from. Disposable isolation is for
single-agent throwaway work — see `/flow:worktree` for the boundary.

### 7. Continue until the batch is actually complete

Do not stop at "tracks launched", "tests passed", or "ready for review". The
coordinator owns the batch until one of these outcomes is true:

1. all in-scope track work is integrated and validated;
2. the integration feature branch is committed and pushed;
3. a PR has been created or updated for that feature branch;
4. a documented stop condition blocks further progress.

When one track appears stalled, follow the progression in Step 5 (nudge
before rescue). Reduce concurrency if needed and continue the remaining
in-scope work rather than abandoning the whole batch by default.

## Example Track Definition

Use a compact artifact format before launching each track. For example:

```text
Track: api-validation
Tasks: task-12, task-14
Files: src/api/validators.js, test/api/validators.test.js
Dependencies: task-11 done
Validation: npm test -- test/api/validators.test.js
Merge target: feat/api-hardening
Track branch: wt/api-validation
Worktree path: /home/dev/my-app-wt-api-validation
Worktree used: not yet launched
State: active
```

Persist the same fields in whatever task tracker, scratch file, or branch note the repository uses.

## Workflow

### 1. Establish the implementation baseline

Before launching tracks: read the relevant requirements, plan, tasks, and nearby code; identify the next ready tasks; confirm or create the integration **feature branch** and final review target; and define track boundaries explicitly using the field set in Core Rule 6 and the Example above.

Default to a dedicated feature branch for the batch. Do not run the workflow on
`main` or another shared long-lived branch unless the developer explicitly asked
for that exceptional path.

### 2. Run discovery (or skip it)

Before delegating to expensive implementers or reviewers, run one lightweight discovery pass using the **scout** model to produce a **discovery brief** — factual context (relevant files, task boundaries, validation commands, dependencies, open questions) so downstream roles do not repeat the same exploration. Run the scout **once per batch or session**, not once per track; implementers and reviewers inherit only the slice of the brief they need. Use the discovery brief template from `docs/workflow-artifact-templates.md`.

**Skip condition**: skip the scout when the task is already narrow and fully scoped — one file, one well-defined bug fix, one known test failure, or one already-triaged review comment. When skipped, record the skip reason in the brief.

### 3. Pre-flight gate (parallel tracks only)

Before launching any agents, verify:

- invoke `/flow:worktree` or perform an
  equivalent validated worktree-provisioning step so every track gets an
  isolated work surface before implementation starts;
- every track has a dedicated work surface at a unique path **outside the project directory**, created with `git worktree add -b {track-branch} ../{repo}-wt-{track} {base-branch}` in either runtime. The `-b` form is required: `git worktree add <path> <branch>` fails with `invalid reference` when the track branch does not exist yet, and with `already used by worktree` when given the integration branch;
- in Copilot CLI, each track's worktree path has been allowed with `/add-dir` (see Core Rule 6) — without it the track fails on its first file operation;
- no two tracks share the same working tree.

**Do not launch any agent until all worktrees exist and paths are confirmed.**

### 4. Launch implementation tracks

For each track:

1. choose the execution mode — standard scoped agents by default, Fleet or agent-team mode only for explicitly approved, high-leverage tracks;
2. create or confirm the dedicated external worktree for this track (from the pre-flight gate above);
3. create or update a durable track report using the template in `docs/workflow-artifact-templates.md`, initializing every field the template defines (see Core Rule 6 and the Example above for the field set);
4. provide the implementer with exact task IDs, exact files or modules, the **absolute** worktree path to operate in plus an instruction to route every file and git operation through it (`git -C <worktree> …`, absolute paths for reads and writes), TDD expectations, concise quality expectations (DRY, SOLID where it fits, low cyclomatic complexity), reuse constraints, validation commands, and an instruction to stay within scope;
5. require the track to report the worktree path it worked in, files changed, tests added or updated, validation performed, uncertainties or blockers, and the commit SHA when the track branch reaches a reviewable checkpoint.

Track implementers should commit their scoped work on their track branch when a
track reaches a clean, reviewable state. Do not leave completed track work
uncommitted inside a worktree by default.

### 5. Coordinator progress and rescue policy

After launching tracks, the coordinator moves each track through four states —
**working → stall suspected → nudge → rescue or stop**. The point of the
sequence is that the cheap recovery always precedes the expensive one, and that
no track goes silently unmanaged.

Read the minimum stall-check threshold from
`.flow/defaults.json` → `concurrency.rescue-min-stall-checks`
(default: **3**).

**Runtime note.** Both runtimes let the coordinator reach a spawned agent
between turns and stop it outright: Claude Code via `SendMessage` to the
agent's name or ID (which resumes it from its transcript, with its context
intact) and `TaskStop` to terminate it; Copilot CLI via its subagent
management (`/tasks`). Progress checks read observable state — worktree
contents, track-branch commits, and task output — and an agent that has not
returned is treated as working. The states and invariants below are identical
in both runtimes.

**States**

1. **Working** — the coordinator sets an expected completion window from task
   size, but the window is advisory:
   soft-budget expiry is **not** by itself a rescue trigger
   and **not** evidence of a stall. A track is working when any
   indicator advances between checks — files modified, tests added or updated,
   validation running or recently completed, or partial results returned. If
   anything advanced, leave the agent alone in the same worktree and scope; do
   not nudge, rescue, or intervene.
2. **Stall suspected** — reached only when **all** hold: no meaningful progress
   across at least **3** consecutive checks (or the configured
   `rescue-min-stall-checks`), and no final result, explicit blocker, or
   partial checkpoint in that window. A single missed check, or a
   slow-but-progressing agent, is not stall evidence.
3. **Nudge** — ask the original agent for current progress, blockers, and the
   smallest next step it can complete. **Never skip this**: it costs one
   message, preserves the agent's context, and resolves most apparent stalls.
   If it resumes, reset the stall counter and return to *working*. If it
   reports a blocker, go to *rescue or stop*. If it does not respond, stop it
   first (`TaskStop`, or Copilot's `/tasks`) and confirm termination — silence
   alone is not termination, and Core Rule 5 forbids a replacement without it.
4. **Rescue or stop** —
   prefer same-agent continuation in the same worktree and scope first,
   narrowing scope only when the agent's report proves the original scope
   cannot finish safely;
   do **not** spawn a second rescue agent or duplicate the track by default.
   Spawn a replacement **only** once the
   original is confirmed terminated (Core Rule 5) and its context is
   irrecoverable: scope the replacement to the remaining work, pass it the
   original's partial results, count it against the concurrency cap, and allow
   at most **1** replacement per track. A track stops when it exhausts its
   hard budget — a maximum number of delegation rounds, not wall time —
   when rescue fails, or when the developer cancels it. Reaching hard budget
   triggers escalation or stop; it does **not** automatically create a rescue
   agent. Record partial results, files touched, tests written, and unresolved
   items in the batch summary before releasing the work surface.

The coordinator re-evaluates track status after every delegation round. Do not wait for a track to go fully silent before checking, and do **not** treat elapsed time alone as stall evidence.

### 6. Review each completed track

After a track finishes:

1. send the diff to a separate reviewer;
2. ask the reviewer for **full coverage, not self-filtered severity**: report
   every issue found — including uncertain or low-severity ones — each tagged
   with severity (blocker / major / minor / nit) and confidence. Reviewers
   must not decide what is "worth reporting"; current-generation models follow
   severity filters literally and silently drop real findings. Focus areas:
   correctness bugs, contract drift, missing tests, boundary violations, and
   duplication that materially matters;
3. triage the findings as coordinator: act on substantive issues; discard
   style-only nits and low-confidence noise. Filtering happens at triage, not
   in the reviewer's report.

Do not spend revision budget on style-only nits — drop them at triage.

If `ccc:conductor` is available, run it as an advisory code-quality
pass on the track diff or the integrated feature branch before publication.

Update the track report after review so it records the current state, validation outcome, unresolved issues, and next action before moving to revision or integration.

### 7. Revise if needed

If the reviewer finds real issues:

1. send the issues back to the implementer as a **targeted resend** containing unresolved issue IDs from the review, constrained scope limited to the flagged issues, acceptance criteria the resend must satisfy, validation commands to rerun, and an escalation condition: if the same issue recurs after one bounded resend, escalate to the coordinator for rescue or developer input;
2. rerun targeted validation on the resend result;
3. re-review only if the changes were substantial.

A resend is bounded follow-up work. It is not a restart of the full task and not an invitation to broaden scope. Limit revision to at most two consecutive resend rounds per issue. If an issue survives two rounds, escalate to the developer rather than continuing the loop.

#### Convergence rules

Apply these rules during every revision round to prevent unbounded churn:

1. **Repeated issue** — if a reviewer raises the same substantive issue a second time after a resend has already addressed it, stop the resend loop and re-scope to the smallest defensible change. Do not send the issue back to the implementer a third time. If re-scoping does not restore convergence, escalate to the developer. Do not treat a repeated review issue as grounds for spawning a rescue agent.
2. **Scope growth** — if a revision introduces changes beyond the original track boundary (new files, new features, or expanded contracts), stop the revision and re-scope the track before continuing. Scope growth during revision is a planning gap, not an implementation task.
3. **Material disagreement** — if the implementer and reviewer disagree on whether a flagged issue is valid and one exchange has not resolved it, escalate to the developer for a decision. Do not let the loop continue without a tiebreaker.
4. **Maximum revision rounds** — a track may complete at most the number of revision rounds specified in Project-Specific Inputs (default: 2). If the track still has unresolved issues after the maximum rounds, escalate to the developer with a summary of what remains and why convergence was not reached.

When a convergence rule fires, record the trigger, the action taken, and the outcome in the track report's rescue history before moving to the next step.

When a resend or rescue occurs, update the track report's state, revision rounds, rescue history, unresolved issues, and next action so the final track gate has a durable record of what changed.

### 8. Integrate tracks carefully

When tracks are ready: merge them into the integration branch one at a time, resolving cross-track conflicts explicitly; run targeted integration validation after risky merges, and stop to reconcile immediately if two tracks drifted on a shared interface; commit the integration feature branch as coherent milestones as merges complete or a stable checkpoint is reached; and push the integration feature branch as work is completed rather than leaving the publish step implicit.

After merge, update each track report to reflect the final track state (`merged`, `abandoned`, `blocked`, or retained for later work).

### 9. Final validation, publication, and cleanup

After all track work is integrated: verify the integrated behavior is coherent, run the repository's real quality gates, invoke `/flow:pr-ready` on the stable integrated diff, and invoke `/flow:pr-publish` on the integration feature branch to commit (if needed), push, and create or update the PR by default. Retire clean temporary work surfaces; keep any retained work surface only with an explicit reason.

Only skip PR publication when:

- the developer explicitly requested local-only execution;
- repository policy forbids this workflow from opening or updating PRs;
- a documented stop condition blocks publication even after readiness and rescue.

### 10. Record the batch outcome

Before stopping, publish one durable batch summary covering merged tracks, retained or abandoned tracks, validations run, unresolved follow-ups, integration branch status (committed / pushed), PR publication status (created / updated / skipped with reason), and the workflow outcome measures fields defined in `docs/workflow-artifact-templates.md` (`discovery-reuse`, `rescue-attempts`, `abandonment-events`, `re-review-loops`).

"Durable" means written to a repository-appropriate sink using the template shape from `docs/workflow-artifact-templates.md` — for example, a PR description, a committed document, an issue comment, or a task tracker entry. In this repository, committed workflow artifacts live under `docs/`; other repositories may use a different durable sink. The batch summary MUST be produced; chat-only memory is not sufficient.

## Required Gates

### Track gate

A track is not complete until:

- tests were added or updated first when applicable;
- track-local validation passes;
- changed files stayed within scope;
- review found no unresolved substantive issues;
- completed track work is committed on the track branch or explicitly recorded as
  intentionally uncommitted with reason;
- a durable track report artifact has been updated to reflect the final track state (see `docs/workflow-artifact-templates.md` for the template).

### SESSION.md write — track merged

At this gate (per track, after the track gate passes), write `.agent/SESSION.md`. Record:
- `current-task`: the overall batch task description
- `current-phase`: "track-[N]-merged" (substitute the track number or name)
- `next-action`: the next pending track or "run integration gate" if all tracks are merged
- `workspace`: the integration target branch
- `last-updated`: current ISO-8601 datetime
- `## Decisions`: which tracks are merged, which are pending
- `## Files Touched`: files merged in this track
- `## Open Questions`: any open questions from the track review
- `## Blockers`: active blockers (empty if none)
- `## Failed Hypotheses`: (empty — not applicable for this skill)

If the write fails: log a warning and continue. Do not block track completion.

### Batch gate

The batch is not complete until:

- all integrated work is coherent;
- repository quality gates pass;
- the final readiness workflow has run on the stable integrated diff;
- the integration feature branch is committed and pushed unless local-only
  execution was explicitly requested;
- a PR was created or updated unless repository policy or a documented stop
  condition prevents publication;
- temporary work surfaces are cleaned up or explicitly retained;
- a durable batch summary artifact has been produced that captures merged tracks, retained or abandoned tracks, validations run, and unresolved follow-ups (see `docs/workflow-artifact-templates.md` for the template).

### Verification checklist — batch complete

Before declaring the batch complete, confirm ALL of the following.
Any failing item blocks the "batch complete" declaration.

**Track merge gate (per track)**
- [ ] Track branch is merged to the integration target — PASS / FAIL
- [ ] Track-local validation commands ran and exited 0 — PASS / FAIL
- [ ] Changed files are within the track's declared scope (no out-of-scope files modified) — PASS / FAIL
- [ ] The implementer reported working in the dedicated external worktree path assigned to this track, outside the project directory, and the main working tree shows no changes from it — PASS / FAIL
- [ ] Completed track work is committed on the track branch (or the exception is recorded) — PASS / FAIL

**Integration gate (whole batch)**
- [ ] Integration validation commands ran on the combined branch and exited 0 — PASS / FAIL
- [ ] No previously-passing tests now fail on the integrated branch — PASS / FAIL
- [ ] Integration feature branch is committed and pushed unless local-only execution was explicitly requested — PASS / FAIL
- [ ] PR created or updated successfully unless repository policy or a documented stop condition prevented publication — PASS / FAIL
- [ ] Durable batch summary artifact has been produced — PASS / FAIL

If any item is FAIL: report the failing item(s) by name, state what must be done to
resolve each, and do not advance past the gate.

## Stop Conditions

- review or fix churn continues without convergence;
- a track exhausts its maximum revision rounds without resolving all issues;
- a repeated issue survives two resend attempts without resolution;
- material implementer-reviewer disagreement cannot be resolved without developer input;
- scope growth during revision indicates a planning gap that must be addressed before continuing;
- track boundaries prove false;
- required repository inputs are still unknown;
- the developer asks to stop;
- a track reaches hard budget after rescue has been attempted.

Before abandoning a track, the coordinator must have followed the full
progression in Step 5: progress checks → stall suspected → continuation
nudge → blocker-based or terminated-agent rescue. Do not skip the nudge step.
Do not spawn a rescue agent while the original agent is still running (Core
Rule 5). Only abandon the track when the progression is exhausted or the
developer explicitly cancels. When stopping, record partial results,
unresolved items, and the reason for stopping. Then reduce concurrency and
continue serially with the remaining work.

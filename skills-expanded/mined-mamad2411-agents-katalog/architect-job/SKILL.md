---
name: architect-job
description: Use when running the recurring "review module structure and dependency direction" routine (invoked via /loop or CronCreate against this skill, or on direct request "run the architect job"). Drains pending `architect` jobs from ether-pro's job store, reviews the target repo's module boundaries/dependency direction/coupling (not line-level bugs — that's repo-review-job), proposes structural fixes when the job/action has earned autonomy, and records the outcome so the autonomy state machine can promote or demote future runs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Architect Job

Same job-router + crystallization mechanism as `repo-review-job`
(`docs/design/2026-08-01-job-router-crystallization-design.md`), applied to
an `architect` job type. `target` is a local repo path. Run `ether job ...`
only from **ether-pro's own directory**, never from inside the target
repo — same hard rule as `repo-review-job`; other `ether` subcommands must
never run with the target as cwd (contamination risk, see that skill's
"Hard rule" paragraph — applies identically here).

Distinct from `repo-review-job`: that skill's `code-review` pass finds
line-level bugs/simplification/efficiency issues in a diff. This job looks
at structure — module boundaries, dependency direction, layering
violations, circular deps, coupling that will make future changes harder —
independent of whether any single line has a bug. Run both on a target;
they don't overlap and don't replace each other. A structural finding here
is not itself a bug report — it's "this will hurt later," which is why its
write action defaults to a stricter confirm posture (see step 4).

## Workflow

Autonomy-tier check and record-run steps below follow the shared protocol in
[`skills/_shared/job-constitution.md`](../_shared/job-constitution.md) — read
that first if unfamiliar; only this job type's specifics are called out here.

1. **Drain pending jobs.** From `~/wrkspc/ether-pro`: `ether job pending
   --type architect`. If none, report "no pending architect jobs" and stop.

2. **Review (read action).**
   - `ether job should-confirm --type architect --actionType read`.
   - If `confirm`, tell the user you're about to review `<target>`'s
     structure and proceed (first runs of a new target always confirm).
   - If `autonomous`, proceed without asking.
   - Map the target's module/package graph (read its directory layout,
     import/require graph, or use `codegraph_explore` if `.codegraph/`
     exists at the target root — prefer it over manual grep for dependency
     edges). Look for: dependency-direction violations (a lower layer
     importing a higher one), circular dependencies, a module doing two
     unrelated jobs (mixed responsibility), duplicated structure that
     should be one shared boundary. Skip anything that's a line-level bug,
     not structural — that belongs to `repo-review-job`, don't duplicate it
     here.
   - Write findings to `<target>/.ether/qa/jobs/<jobId>/report.md` (Write
     tool, inside target repo). Include: type, target, agent, action,
     outcome, confirmed-by-human, date, each finding as (boundary/module
     pair, what's wrong, why it matters later, suggested fix or `(none
     obvious)`).
   - Record: `ether job record-run --jobId <id> --agent architect-job
     --actionType read --outcome success|failure` from ether-pro's
     directory. `failure` = the review itself couldn't run (repo missing,
     tool error) — not "found structural issues," that's success.

3. **If a finding has a bounded fix, propose a write action.**
   - `ether job should-confirm --type architect --actionType write`.
   - Structural changes touch more surface than a line fix and are easy to
     get subtly wrong (e.g. "fix" a layering violation by introducing a
     new circular dep elsewhere) — treat `confirm` as the expected default
     even once other job types on the same target have promoted past it;
     don't assume architect's write tier tracks repo-review's.
   - If `confirm`: present the finding, the proposed restructuring, and
     what it touches (files/modules), wait for explicit approval.
   - If `autonomous` (only after real promotion history specific to this
     job type): apply via a bounded `cavecrew-builder` delegation scoped to
     the exact files identified, or do it directly if it's a single-file
     move/rename. Run the target's full test suite (not just the touched
     module's) before recording success — structural changes are exactly
     the kind of edit that breaks something two layers away.
   - Append the write outcome (what was applied/proposed, verification
     result) to the same report.md.
   - Record the write outcome the same way, with `--safetyViolation` for
     anything that broke the build/tests or touched files outside the
     identified scope.
   - If a human approved a `confirm`-tier run, add `--confirmedByHuman`.

4. **Report per job**: target repo, structural findings summary, fix
   applied/proposed, tier used, report file path. End with `ether job
   status --type architect` and call out any tier change explicitly.

## Adding a job

From `~/wrkspc/ether-pro`:
`ether job add --type architect --target /absolute/path/to/repo [--params '{"scope":"full"}']`

## Scheduling

Prefer `/loop <interval> /architect-job` for a live session, with a longer
interval than `repo-review-job` — structure drifts slower than line-level
issues, frequent runs mostly re-find the same findings. `CronCreate` works
for unattended cadence (session-only, expires after 7 days) but expect
most runs to land on `confirm` given the stricter write posture in step 3.

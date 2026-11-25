---
name: hardener-job
description: Use when running the recurring "mutation-test the suite and kill surviving mutants" routine (invoked via /loop or CronCreate against this skill, or on direct request "run the hardener job"). Drains pending `hardener` jobs from ether-pro's job store, runs the target repo's mutation-testing tool (or bootstraps one if absent), strengthens tests to kill surviving mutants when the job/action has earned autonomy, and records the outcome so the autonomy state machine can promote or demote future runs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Hardener Job

Same job-router + crystallization mechanism as `repo-review-job`
(`docs/design/2026-08-01-job-router-crystallization-design.md`), applied to
a `hardener` job type. `target` is a local repo path. Run `ether job ...`
only from **ether-pro's own directory**, never from inside the target
repo — same hard rule as `repo-review-job`; other `ether` subcommands must
never run with the target as cwd.

Distinct from `repo-review-job`/`architect-job`: this doesn't read code for
bugs or structure — it measures whether the *test suite* actually catches
regressions, by mutating the target's source (flip a conditional, change a
boundary, drop a line) and checking whether any test fails. A surviving
mutant means a piece of behavior has no test protecting it, even if
coverage tools call that line "covered" (covered ≠ tested — a line can run
during a test without the test asserting on its outcome). This is a
finding about test quality, not application code quality.

## Workflow

Autonomy-tier check and record-run steps below follow the shared protocol in
[`skills/_shared/job-constitution.md`](../_shared/job-constitution.md) — read
that first if unfamiliar; only this job type's specifics are called out here.

1. **Drain pending jobs.** From `~/wrkspc/ether-pro`: `ether job pending
   --type hardener`. If none, report "no pending hardener jobs" and stop.

2. **Run mutation testing (read action).**
   - `ether job should-confirm --type hardener --actionType read`.
   - If `confirm`, tell the user you're about to mutation-test `<target>`
     and proceed (first runs of a new target always confirm).
   - If `autonomous`, proceed without asking.
   - Detect the target's stack and mutation tool: JS/TS → Stryker
     (`@stryker-mutator/core`, check for `stryker.conf.*` or offer to
     `npx stryker init` if absent and `params.bootstrap` is true); Python →
     `mutmut` or `cosmic-ray`; other stacks → check `params.tool` for an
     explicit override, or report "no mutation tool available for this
     stack" as a `failure` outcome rather than guessing. Don't install a
     mutation framework globally — scope any install to the target's own
     dependency manifest (devDependency, not global).
   - Run it against `params.scope` (default: whole repo, or a diff-only
     mode if the tool supports it and `params.scope` says `"diff"`).
     Mutation runs are slow — respect a reasonable timeout and report a
     partial result rather than hanging indefinitely; note in the report if
     the run was truncated.
   - Write findings to `<target>/.ether/qa/jobs/<jobId>/report.md`:
     mutation score, list of surviving mutants (file:line, mutation
     applied, which test(s) ran over that line and still passed).
   - Record: `ether job record-run --jobId <id> --agent hardener-job
     --actionType read --outcome success|failure` from ether-pro's
     directory. `failure` = the mutation run itself couldn't complete
     (tool missing and no bootstrap requested, crashed, no test runner
     found) — not "found surviving mutants," that's the expected signal
     this job exists to surface.

3. **If mutants are killable with a bounded test addition, propose a
   write action.**
   - `ether job should-confirm --type hardener --actionType write`.
   - If `confirm`: present the surviving mutants and the proposed test(s)
     to kill them, wait for explicit approval before touching the target.
   - If `autonomous`: write the missing test(s) via `ether-tdd` conventions
     (assert on the specific behavior the mutant broke, not a broad
     re-test of the whole function) or delegate a bounded addition to
     `cavecrew-builder`. Re-run the mutation tool scoped to just the
     touched mutants to confirm they're now killed — don't claim success
     without re-running. Never modify application source to "fix" a
     surviving mutant; a survivor means the test is missing, not that the
     code is wrong (that's `repo-review-job`'s concern, if it's even a real
     bug and not just untested-but-correct behavior).
   - Append the write outcome (mutants killed, tests added, re-run result)
     to the same report.md.
   - Record the write outcome the same way, with `--safetyViolation` for
     anything that broke the existing suite or touched files outside the
     test directory.
   - If a human approved a `confirm`-tier run, add `--confirmedByHuman`.

4. **Report per job**: target repo, mutation score (before/after if writes
   ran), surviving mutants killed vs remaining, tier used, report path.
   End with `ether job status --type hardener` and call out any tier
   change explicitly.

## Adding a job

From `~/wrkspc/ether-pro`:
`ether job add --type hardener --target /absolute/path/to/repo [--params '{"scope":"full","bootstrap":true}']`

## Scheduling

Prefer `/loop <interval> /hardener-job` with a long interval — mutation
runs are expensive (can take minutes to hours on a large suite) and the
signal (mutation score) moves slowly. Don't run this more often than
`architect-job`. `CronCreate` works but check its run doesn't collide with
CI-triggered test runs on the same target (both consuming CPU/test-runner
locks simultaneously wastes the run).

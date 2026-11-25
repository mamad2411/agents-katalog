---
name: cleaner-job
description: Use when running the recurring "behavior-preserving cleanup pass" routine (invoked via /loop or CronCreate against this skill, or on direct request "run the cleaner job"). Drains pending `cleaner` jobs from ether-pro's job store, finds duplication (DRY) and high-CRAP (complex + poorly-tested) code in the target repo, applies behavior-preserving refactors when the job/action has earned autonomy, and records the outcome so the autonomy state machine can promote or demote future runs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Cleaner Job

Same job-router + crystallization mechanism as `repo-review-job`
(`docs/design/2026-08-01-job-router-crystallization-design.md`), applied to
a `cleaner` job type. `target` is a local repo path. Run `ether job ...`
only from **ether-pro's own directory**, never from inside the target
repo — same hard rule as `repo-review-job`; other `ether` subcommands must
never run with the target as cwd.

Distinct from the other three review/quality job types — each looks at a
different axis, and none substitutes for another:
- `repo-review-job` — is this code correct (bugs)?
- `architect-job` — is this code in the right place (structure)?
- `hardener-job` — does the test suite actually protect this code
  (mutation survivors)?
- `cleaner-job` (this one) — is this code needlessly duplicated or
  needlessly complex relative to how well it's tested (DRY, CRAP)?

The one hard constraint that makes this job type safe to automate at all:
every change here must be **behavior-preserving**. If a proposed cleanup
would change observable behavior, it's not a cleanup — file it as a
`repo-review-job` finding instead (that job type's write action is scoped
for behavior changes with review, this one isn't).

## Workflow

Autonomy-tier check and record-run steps below follow the shared protocol in
[`skills/_shared/job-constitution.md`](../_shared/job-constitution.md) — read
that first if unfamiliar; only this job type's specifics are called out here.

1. **Drain pending jobs.** From `~/wrkspc/ether-pro`: `ether job pending
   --type cleaner`. If none, report "no pending cleaner jobs" and stop.

2. **Scan (read action).**
   - `ether job should-confirm --type cleaner --actionType read`.
   - If `confirm`, tell the user you're about to scan `<target>` for
     duplication/CRAP and proceed (first runs of a new target always
     confirm).
   - If `autonomous`, proceed without asking.
   - Duplication: grep/`codegraph_explore` (if `.codegraph/` exists) for
     near-identical blocks — 3+ repeated lines of real logic, not
     boilerplate the language forces (import blocks, standard test
     scaffolding). Prefer the target's own duplication-detection tool if
     one's configured (`jscpd`, `pylint --duplicate-code`, etc); fall back
     to manual scan otherwise.
   - CRAP (Change Risk Anti-Patterns): high cyclomatic complexity combined
     with low test coverage — the two together, not either alone. A
     complex function with full coverage isn't a CRAP finding; a trivial
     function with no coverage usually isn't either (nothing to break). Use
     the target's coverage tool output if available (`coverage.py`,
     `nyc`/`c8`, `go test -cover`) cross-referenced against a complexity
     scan; if neither exists, note that CRAP can't be computed and scope
     the job to duplication only.
   - Write findings to `<target>/.ether/qa/jobs/<jobId>/report.md`:
     duplication instances (file:line pairs, what's shared), CRAP hotspots
     (file:line, complexity, coverage %), each with a proposed
     behavior-preserving fix (extract shared function, add missing test
     before simplifying — see step 3's ordering rule) or `(none obvious)`.
   - Record: `ether job record-run --jobId <id> --agent cleaner-job
     --actionType read --outcome success|failure` from ether-pro's
     directory. `failure` = the scan itself couldn't run (repo missing,
     tooling crashed) — not "found duplication/CRAP hotspots," that's the
     expected signal.

3. **If a finding has a safe behavior-preserving fix, propose a write
   action.**
   - `ether job should-confirm --type cleaner --actionType write`.
   - If `confirm`: present the finding and the proposed refactor, wait for
     explicit approval before touching the target.
   - If `autonomous`: apply the refactor via `cavecrew-builder` (bounded
     1-2 file scope) or directly for a single extraction. For a CRAP
     hotspot with low coverage, add the missing test *first* (characterize
     current behavior, don't guess intended behavior) so the refactor has
     something to prove it's behavior-preserving against — this ordering
     is mandatory, not optional, for any CRAP-hotspot fix. Run the full
     test suite before and after; if outputs differ (new failures, changed
     assertions needed), the "cleanup" changed behavior — revert and
     downgrade the finding to a `repo-review-job` candidate instead of
     forcing it through.
   - Append the write outcome (what was applied, tests added, before/after
     suite result) to the same report.md.
   - Record the write outcome the same way, with `--safetyViolation` for
     anything where the suite result differed after the "cleanup" (that's
     exactly the behavior-preservation violation this job type exists to
     avoid) or touched files outside the identified scope.
   - If a human approved a `confirm`-tier run, add `--confirmedByHuman`.

4. **Report per job**: target repo, duplication/CRAP findings summary, fix
   applied/proposed, tier used, report path. End with `ether job status
   --type cleaner` and call out any tier change explicitly.

## Adding a job

From `~/wrkspc/ether-pro`:
`ether job add --type cleaner --target /absolute/path/to/repo [--params '{"scope":"full"}']`

## Scheduling

Prefer `/loop <interval> /cleaner-job`, similar cadence to
`repo-review-job` — duplication/CRAP accumulate at roughly the same pace
as line-level issues, faster than structural drift (`architect-job`) or
mutation-score decay (`hardener-job`). `CronCreate` works for unattended
cadence (session-only, expires after 7 days).

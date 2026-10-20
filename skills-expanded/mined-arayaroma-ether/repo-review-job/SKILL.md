---
name: repo-review-job
description: Use when running the recurring "review this repo's code" routine (invoked via /loop or CronCreate against this skill, or on direct request "run the repo review job"). Drains pending `repo-review` jobs from ether-pro's job store, reviews each target repo/branch with the `code-review` skill, applies fixes when the job/action has earned autonomy, and records the outcome so the autonomy state machine can promote or demote future runs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Repo Review Job

Same job-router + crystallization mechanism as `web-review-job`
(`docs/design/2026-08-01-job-router-crystallization-design.md`), applied to
a `repo-review` job type instead of `web-review`. `target` is a local repo
path (not a URL). Run `ether` commands from **ether-pro's own directory**,
never from inside the target repo — some target repos (e.g. dar-money-mind)
explicitly opt out of using ether-pro/ether-mem for their own project work;
this job type only observes them from outside, it doesn't wire ether-pro
into them.

**Hard rule, no exceptions**: never run the `ether` CLI (`ether setup`,
`ether init`, `ether qa review`, or any subcommand other than `ether job
...`) with the target repo as cwd — those CLI commands create sqlite
state (`state.db`, `usage.db`, `config.json`) *inside whatever directory
you run them from*, which is exactly the contamination this job type
exists to avoid. `ether job ...` itself only ever runs from ether-pro's
own directory (that's where `jobs.db`/autonomy state lives), never the
target's. "Review the target repo" means invoke the **`code-review`
Skill** (`Skill code-review`) pointed at the target path — a read-only
skill that never writes `.ether*` anywhere. If you're unsure which one
you're about to run, stop and re-read this paragraph — this has caused
real contamination of a target repo before (dar-money-mind, 2026-08-01).

The one exception is the plain markdown report file (below) — writing it
with the **Write tool** directly into `<target>/.ether/qa/jobs/<jobId>/report.md`
is fine and expected; it's just a file, not `ether` CLI state, and doesn't
require the target repo to use ether-pro for anything else.

## Workflow

Autonomy-tier check and record-run steps below follow the shared protocol in
[`skills/_shared/job-constitution.md`](../_shared/job-constitution.md) — read
that first if unfamiliar; only this job type's specifics are called out here.

1. **Drain pending jobs.** From `~/wrkspc/ether-pro`: `ether job pending
   --type repo-review`. If none, report "no pending repo-review jobs" and
   stop.

2. **Review (read action).**
   - `ether job should-confirm --type repo-review --actionType read`.
   - If `confirm`, tell the user you're about to review `<target>` and
     proceed (first runs of a new target always confirm — expected).
   - If `autonomous`, proceed without asking.
   - Invoke the **`code-review` Skill** (via the Skill tool, not any
     `ether` CLI subcommand) at the effort level in `params.level`
     (default `medium`) against the target's current diff/branch, or a
     general pass if there's nothing pending (check `params.scope` —
     full-repo pass vs diff-only). Read-only file access to the target is
     fine; running `ether` commands there is not (see hard rule above).
   - Write the findings with the Write tool to
     `<target>/.ether/qa/jobs/<jobId>/report.md` — inside the target repo
     (mirrors the `qa-review` command's `.ether/changes/<id>/qa-report.md`
     convention, but lives with the repo it's about, not in ether-pro).
     Include: type, target, agent, action, outcome, confirmed-by-human,
     date, scope note, findings (or `(none)`), and any follow-up worth
     flagging. This is the only place the review persists — reporting it
     only in chat output means it's gone once the session ends.
   - Record: `ether job record-run --jobId <id> --agent repo-review-job
     --actionType read --outcome success|failure` from ether-pro's
     directory. `failure` = the review itself couldn't run (repo missing,
     tool error), not "found issues" — finding issues is success.

3. **If findings are fixable, propose a write action.**
   - `ether job should-confirm --type repo-review --actionType write`.
   - If `confirm`: present the findings/proposed fix, wait for explicit
     approval before touching the target repo.
   - If `autonomous`: apply via `code-review --fix` or delegate a bounded
     fix to `caveman:cavecrew-builder`, scoped to the target repo. Run its
     tests/typecheck before recording success.
   - Append the write outcome (what was applied/proposed, verification
     result) to the same `<target>/.ether/qa/jobs/<jobId>/report.md`.
   - Record the write outcome the same way, with `--safetyViolation` only
     for something that broke the repo or touched files outside the
     intended scope (not for "the fix was incomplete").
   - If a human approved a `confirm`-tier run, add `--confirmedByHuman`.

4. **Report per job**: target repo, findings summary, fix applied/proposed,
   tier used, and the report file path. End with `ether job status --type
   repo-review` and call out any tier change explicitly.

## Adding a job

From `~/wrkspc/ether-pro`:
`ether job add --type repo-review --target /absolute/path/to/repo [--params '{"level":"medium","scope":"diff"}']`

## Scheduling

Prefer `/loop <interval> /repo-review-job` for a live session. For
unattended/cross-session cadence use `CronCreate` — note its constraints:
session-only (dies if this session ends) and auto-expires after 7 days, so
it must be re-created periodically, it is not a durable daemon.

---
name: pr-author-job
description: Use when running the recurring "implement pending tasks and open PRs" routine (invoked via /loop or CronCreate against this skill, or on direct request "run the PR author job"). Drains pending `pr-author` jobs from ether-pro's job store, implements each task in an isolated branch/worktree of the target repo, runs its tests, and opens a PR via `gh`. Records the outcome so the autonomy state machine can promote or demote future runs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# PR Author Job

Same job-router + crystallization mechanism as `repo-review-job` and
`web-review-job` (`docs/design/2026-08-01-job-router-crystallization-design.md`),
applied to a `pr-author` job type. `target` is a local repo path. Run `ether
job ...` commands from **ether-pro's own directory**, never from inside the
target repo — see `repo-review-job`'s hard rule; it applies here identically.
Never run `ether setup`/`ether init`/etc with the target as cwd.

This job type WRITES to the target repo (new branch, commits, an open PR).
Treat every run as `actionType write` — there is no read-only variant.

## Workflow

Autonomy-tier check and record-run steps below follow the shared protocol in
[`skills/_shared/job-constitution.md`](../_shared/job-constitution.md) — read
that first if unfamiliar; only this job type's specifics are called out here.

1. **Drain pending jobs.** From `~/wrkspc/ether-pro`: `ether job pending
   --type pr-author`. If none, report "no pending pr-author jobs" and stop.

2. **Check autonomy tier.** `ether job should-confirm --type pr-author
   --actionType write`.
   - `confirm`: tell the user what task you're about to implement in which
     repo, and wait for explicit approval before touching the target repo.
     First runs of a new target always confirm — expected.
   - `autonomous`: proceed without asking.

3. **Isolate the work.** Create a fresh branch off the target's default
   branch (`git -C <target> switch -c pr-author/<jobId>-<slug>` or a
   worktree if the target repo is one you're also interactively using —
   check `EnterWorktree`/`superpowers:using-git-worktrees` if unsure).
   Never work directly on the default branch.

4. **Estimate scope, then implement.** `params.task` (or `params.issueRef`)
   describes what to build — a spec/change id under the target's own
   change-tracking (if it uses dar-ai/ether-pro conventions), an issue
   number, or free-text. Before writing any code, invoke
   `ether-scope-estimate` — record a min/max LOC estimate for a surgical
   fix in ether-mem. Follow the target repo's own conventions (read its
   CLAUDE.md/AGENTS.md first) — do not impose ether-pro's own SDD process
   on a repo that doesn't use it. Then invoke `ether-tdd` unconditionally —
   write the failing test first, then the code that makes it pass. This is
   mandatory for every `pr-author` run, not just repos that already have a
   test suite; if the target has none, TDD is how one gets started. Keep
   the change scoped to `params.task` and to the estimated max — no
   drive-by refactors.

5. **Verify before opening the PR.** Run the target repo's test/typecheck/
   lint commands (discover via its package.json scripts, Makefile, or
   CLAUDE.md). A PR opened with failing tests is a failed run, not a
   success with caveats. Run `ether-scope-estimate`'s reconciliation step —
   `git diff --stat` the branch against its base, compare actual LOC to
   the recorded min/max. If over max, record cause + prevention in
   ether-mem before opening the PR (mandatory) and mention the overrun in
   the PR body so the reviewer sees it too.

6. **Open the PR.**
   `git -C <target> push -u origin <branch>`
   `gh -R <target> pr create --title "<concise title>" --body "<summary +
   test plan>" --head <branch>` (add `--base <default>` if not auto-detected).
   Capture the PR URL/number — it's the job's deliverable.

7. **Record the run.** `ether job record-run --jobId <id> --agent
   pr-author-job --actionType write --outcome success|failure` from
   ether-pro's directory. `failure` = couldn't implement, tests never
   passed, or PR couldn't be opened — not "PR opened but reviewer later
   requested changes" (that's the next job's job, see `pr-review-job`).
   `--safetyViolation` only if you touched files/repos outside `target` or
   pushed to the default branch directly.
   If a human approved a `confirm`-tier run, add `--confirmedByHuman`.

8. **Write a short receipt.** `<target>/.ether/qa/jobs/<jobId>/report.md`:
   task, branch, PR URL, verification commands run + result, outcome.

9. **Report per job**: target repo, task summary, PR URL, tier used. End
   with `ether job status --type pr-author` and call out any tier change.

## Adding a job

From `~/wrkspc/ether-pro`:
`ether job add --type pr-author --target /absolute/path/to/repo --params '{"task":"<description>"}'`

## Scheduling

`/loop <interval> /pr-author-job` for a live session, or `CronCreate` for
unattended cadence (session-only, expires after 7 days — re-create
periodically, not a durable daemon). For a durable always-on trigger with
no re-creation needed, use an external scheduler invoking `claude -p
"/pr-author-job"` headless — a systemd user timer, or a GitHub Actions
workflow on a `schedule` cron. Neither is set up by default; pick one when
wiring a target repo for real unattended operation.

## Handoff to review

This job type only opens PRs — it never merges or self-reviews. Pair it
with `pr-review-job` on the same target so opened PRs get an independent
pass; `pr-review-job` auto-discovers open PRs, no need to manually enqueue
a review job per PR.

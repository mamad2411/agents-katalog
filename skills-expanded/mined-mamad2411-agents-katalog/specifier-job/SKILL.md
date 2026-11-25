---
name: specifier-job
description: Use when running the recurring "turn user intent into an accepted spec before coding" routine (invoked via /loop or CronCreate against this skill, or on direct request "run the specifier job"). Drains pending `specifier` jobs from ether-pro's job store, turns each `params.task` into a Gherkin acceptance spec against the target repo, waits for explicit approval, then hands the approved spec to `pr-author-job` as its task. Records the outcome so the autonomy state machine can promote or demote future runs.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Specifier Job

Same job-router + crystallization mechanism as `repo-review-job`/
`pr-author-job` (`docs/design/2026-08-01-job-router-crystallization-design.md`),
applied to a `specifier` job type. `target` is a local repo path. Run
`ether job ...` only from **ether-pro's own directory**, never from inside
the target repo — same hard rule as `repo-review-job`; other `ether`
subcommands (`setup`/`init`/`qa review`) must never run with the target as
cwd.

Purpose: give `pr-author-job` a precise, human-approved spec to implement
instead of implementing straight from a one-line `params.task`. This is a
gate, not a replacement for `ether-scope-estimate`/`ether-tdd` — those
still run inside `pr-author-job` once the spec is handed off.

## Workflow

Autonomy-tier check and record-run steps below follow the shared protocol in
[`skills/_shared/job-constitution.md`](../_shared/job-constitution.md) — read
that first if unfamiliar; only this job type's specifics are called out here.

1. **Drain pending jobs.** From `~/wrkspc/ether-pro`: `ether job pending
   --type specifier`. If none, report "no pending specifier jobs" and stop.

2. **Check autonomy tier.** `ether job should-confirm --type specifier
   --actionType write` (drafting a spec file is the write action; there's
   no read-only variant since a spec is the whole deliverable).
   - `confirm`: tell the user which task/repo you're about to specify, and
     proceed to draft (drafting is not itself the risky step — see step 4
     for the mandatory approval gate before handoff).
   - `autonomous`: proceed without asking before drafting either way; the
     approval gate in step 4 still applies regardless of tier — see below.

3. **Draft the spec.** `params.task` (or `params.issueRef`) is the intent.
   Read the target's own CLAUDE.md/AGENTS.md and any existing spec
   directory convention first — if the target already has a spec format
   (Gherkin `.feature` files, an `openspec/`-style dir, etc.), follow it;
   otherwise default to a plain Gherkin `.feature` file. Write concrete
   `Given/When/Then` scenarios covering the golden path and the edge cases
   implied by `params.task` — not implementation detail, only observable
   behavior. Save it to `<target>/.ether/specs/<jobId>-<slug>.feature` (or
   the target's own convention if one exists) with the Write tool.

4. **Approval gate — always required, regardless of tier.** Present the
   drafted spec to the user and wait for explicit approval or edits before
   handing off. This mirrors swarm-forge's `specifier` role ("asks for
   approval before handoff") and is intentionally *not* gated by the
   autonomy tier the way other jobs' write actions are: a wrong spec
   silently accepted wastes an entire `pr-author-job` run downstream, so
   this gate never auto-promotes to skip-confirmation even at tier 1. If
   the user requests changes, revise and re-present; do not proceed on a
   partial or implied approval.

5. **On approval, hand off to `pr-author-job`.** `ether job add --type
   pr-author --target <target> --params '{"task":"implement spec
   <jobId>-<slug>.feature: <one-line summary>","specPath":"<path>"}'` from
   ether-pro's own directory. `pr-author-job` reads the spec file for full
   detail; the `params.task` string is just enough for its own report to
   be legible without opening the file.

6. **Record the run.** `ether job record-run --jobId <id> --agent
   specifier-job --actionType write --outcome success|failure
   --confirmedByHuman` from ether-pro's directory (approval in step 4 is
   always by a human, so `--confirmedByHuman` is always set for this job
   type — it's the one job type where that flag isn't conditional).
   `failure` = couldn't draft a coherent spec, or the user rejected it with
   no path to revise — not "the user asked for several rounds of edits"
   (that's normal, still `success` once approved).

7. **Write a short receipt.** `<target>/.ether/qa/jobs/<jobId>/report.md`:
   task, spec path, approval notes, handed-off pr-author job id.

8. **Report per job**: target repo, task summary, spec path, pr-author job
   id created. End with `ether job status --type specifier`.

## Adding a job

From `~/wrkspc/ether-pro`:
`ether job add --type specifier --target /absolute/path/to/repo --params '{"task":"<description>"}'`

## Scheduling

Prefer `/loop <interval> /specifier-job` for a live session — this job
type's mandatory approval gate (step 4) makes it a poor fit for unattended
`CronCreate`/external-scheduler operation; someone has to be present to
approve. Don't wire it to a headless cron the way `pr-review-job` is.

## Handoff to implementation

This job type only produces an approved spec — it never implements. Pair
it with `pr-author-job` on the same target; step 5 auto-enqueues that job,
no manual `ether job add` needed after approval.

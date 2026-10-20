---
name: ship-and-watch
description: >
  Use after pushing a Forge branch, opening a PR, or when asked "is the PR ready
  / what's the status / are checks green" — reads shepherd verdicts instead of
  polling GitHub. Do not use to merge a PR, and do not use to resolve review
  threads; both stay with the human and /review.
---

# ship-and-watch

The monitor is already running. Your job is to read it, not to start it and not
to replace it.

## Why this exists

The single most repeated correction in this repo is an agent shipping a PR and
then hand-polling `gh pr checks` in a loop — burning tokens, missing the
verdict, and leaving the PR unwatched the moment the session ends.
[Forge #1 ×10]

Harsha's rule, in his words: *"shepard should do everything independtly thats
teh idea it shouldntbe invoked"* and *"whenever we ship an automatic pr monitor
should be created to work on all fixes until iut gets merghe ready"*.
A monitor you must remember to start has no value.

## What is already true

Forge wakes the repo-singleton shepherd daemon automatically after a supported
session start, after every successful push, and after every successful
non-dry-run ship. Duplicate starts are clean no-ops under the O_EXCL lease.
[verified 2026-08-13 — AGENTS.md, `/shepherd` utility section]

So: **you do not start the daemon.** You confirm it is attached and read what it
says.

## Procedure

1. Ship or push normally — `forge ship`, or `forge push` on a branch that has an
   open PR.
2. Confirm the daemon owns this PR:

   ```bash
   forge shepherd events
   ```

3. Read the verdict for your PR:

   ```bash
   forge shepherd <pr> --pull --json
   ```

4. Report the verdict in one line: what is red, what is pending, what needs a
   human. If nothing is red, say so explicitly and name what you checked — a
   silent "looks fine" reads as "did not look".

## Rules

- **Never hand-poll.** `gh pr checks` in a loop is the failure this skill
  replaces. The one legitimate use of `gh` here is a single spot-check when the
  daemon reports something you want to confirm at source. [Forge #1 ×10]
- **Never merge.** Shepherd never merges and never resolves review threads;
  neither do you. The human merges. [verified 2026-08-13 — AGENTS.md]
- **New problems get a new PR.** A finding unrelated to this branch becomes a
  kernel issue and its own PR, never an extra commit here.
  *"new problems not related to pr should be menat to be fixed ina new pr."*
  [Forge #3 ×6]
- **Do not wait a fixed ten minutes.** Wait for the settled state: every bot has
  posted a terminal result, zero unresolved threads, no check in flight.
  A clock is not a signal. [Forge #10 ×2]
- If the daemon is genuinely not attached, that is a bug in the substrate — file
  a kernel issue. Do not paper over it with a manual loop.

## Kill switches (know them, do not reach for them)

`FORGE_SHEPHERD_DISABLE`, or `forge gate disable rail.auto_shepherd`.
Disabling the monitor to make a run quieter is the same class of mistake as
weakening a test to make it pass. [Forge #9 ×3]

## Done when

You have stated the current verdict for the PR, named the source you read it
from, and either handed off to the human for merge or filed the follow-up issue.

---
name: mr-watch
version: 0.1.0
authors: [agentic-os]
description: >-
  Watch one open MR/PR and autonomously clear whatever blocks merge — CI
  failures, requested-change reviewer comments, and merge conflicts — on a
  polling loop until the request merges, closes, or the user stops it.
  Adapter-driven: no source-control platform is hardcoded. Invoke when the user
  says "watch the MR", "monitor MR", "keep an eye on the PR", "babysit this PR",
  "monitor MR !123", or when an MR-creator skill hands off a freshly opened
  request for hands-off management. Blast radius R3.
  Not for: creating the MR/PR (mr-submit), one-shot status checks, or reviewing code quality (code-review) — it is a persistent unblocking loop.

---

# mr-watch

Autonomous post-creation babysitter for a single open merge/pull request. Poll
the request, diagnose merge blockers, apply the minimal fix, push, and repeat
until a terminal state. The MR/PR must already exist — this skill never opens
one.

> Escalate, don't guess. Deeply tangled conflicts, unknown CI failures, and
> persistently stuck requests hand back to the user rather than churn.

## When to invoke

- User asks to watch, monitor, or keep an eye on an open MR/PR.
- `mr-submit` (or any request-opening skill) hands off the URL it just created.

## Inputs

Accept the request reference in any of these forms and extract project path +
request ID:

| Form | Example |
| --- | --- |
| Full URL (any VCS) | `https://.../merge_requests/123` |
| Short form | `!123` (GitLab-style) or `#123` (GitHub-style) |
| Bare number | `123` when the repo is inferable from cwd |

## Adapter contract

All platform I/O is indirected — never call a platform CLI directly.

- Read the adapter from `.agentic/guides/project.md`, section `## Review Adapter`.
  Use the declared adapter only when its status is `configured`.
- The operation contract lives in `references/mr-adapters.md`. Read it to learn
  how each named operation maps onto the configured adapter (CLI, MCP server, or
  custom command).

Named operations you call by name:

| Operation | Returns / does |
| --- | --- |
| **state** | request lifecycle: `merged` / `closed` / open |
| **ci-status** | pipeline status: `running`/`pending` / `failed` / `passed` / none |
| **discussions** | open threads, with IDs |
| **comment** | post a reply on a thread |
| **target-branch** | the request's target branch |

## Loop state

Carry these variables across iterations:

| Variable | Purpose |
| --- | --- |
| `last_pipeline_id` | most recent pipeline seen |
| `last_seen_discussion_ids` | threads already triaged |
| `iteration_count` | loops elapsed |
| `consecutive_same_failure_count` | same job failing back-to-back after a fix |

## Operating loop

Each iteration, in order:

1. **Terminal check — state.** Query **state**.

   | State | Action |
   | --- | --- |
   | `merged` | print success, exit |
   | `closed` | print closure notice, exit |
   | user says stop/cancel | exit immediately |

2. **CI check — ci-status.**

   | Status | Action |
   | --- | --- |
   | `running` / `pending` | proceed — do NOT skip the rebase check |
   | `failed` | CI Failure Handling (step 3) |
   | `passed` / none | proceed |

3. **CI Failure Handling.** Classify, then apply the minimal fix:

   | Failure class | Fix |
   | --- | --- |
   | lint / style / type | fix the offending lines |
   | failing unit tests | fix the code (not the test, unless the test is clearly wrong) |
   | build / compile | fix imports / compile errors |
   | transient / flaky | post a retrigger comment via **comment**; wait ~20s |
   | unknown | report to the user, pause |

   Commit fixes with the ticket prefix parsed from `git log --oneline -5`:

   ```
   <TICKET_ID>: Fix <lint|test|build> failure in CI
   ```

   Then `git push --force-with-lease` (never plain `--force`).

   > Stuck-CI guard: if the same job fails twice in a row after a fix attempt
   > (`consecutive_same_failure_count`), stop and hand back to the user.

4. **Discussion triage — discussions.** For each thread not in
   `last_seen_discussion_ids`:

   | Thread type | Action |
   | --- | --- |
   | code change requested | implement the change |
   | question | reply via **comment** |
   | informational / bot | skip |

   Commit reviewer-driven code changes as:

   ```
   <TICKET_ID>: Address reviewer feedback
   ```

   After pushing the fix, reply on the thread with exactly:

   `"Done — addressed in the latest commit."`

5. **Rebase / conflict check — runs EVERY iteration, even while the pipeline is
   pending.** Query **target-branch**, then:

   ```
   git fetch origin "<TARGET_BRANCH>"
   git rebase "origin/<TARGET_BRANCH>"
   # resolve, git rebase --continue
   git push --force-with-lease
   ```

   - Branch behind target → rebase as above.
   - Conflicts present → resolve, then push (wait ~10s after the push).
   - Conflicts too tangled (both sides changed overlapping logic in the same
     function) → stop, list the conflicting files for the user.

   Between polls, wait `sleep 90` while confirming the retriggered pipeline.

6. **Idle guard.** If nothing resolved this pass, increment `iteration_count`.
   After **10 iterations** with nothing resolved, pause and ask the user before
   continuing.

7. **Sleep and repeat.** `sleep 180`, then loop from step 1.

> Cadence note: the header cadence is roughly 180s; the loop body uses both
> `sleep 180` (between iterations) and `sleep 90` (step 5 pipeline wait), plus
> ~20s after a retrigger and ~10s after a conflict push.

## Code-fix discipline

- Minimal change only — no surrounding refactor.
- Fix code, not tests, unless the test is clearly wrong.
- Force-push is always `git push --force-with-lease`.

## Run journal

Maintain `.agentic/runs/<branch>.json` (`<branch>` = current branch); create it
if absent. Write the entry before any handoff prompt:

```json
{ "step": "07", "agent_skill": "mr-watch", "primitive": "skill",
  "started_at": "<ISO8601 start time>", "completed_at": "<ISO8601 now>",
  "status": "completed", "outcome": "...", "artifacts": ["<MR or PR URL>"],
  "next_step": "guide-sync" }
```

## Outputs & handoff

- The request reaches a terminal state (`merged` / `closed`), or control returns
  to the user on escalation.
- A completed journal entry at `.agentic/runs/<branch>.json`.
- On merge with structural changes, offer a user-gated (yes/no/other) handoff to
  the **guide-sync** agent/skill, which updates `.agentic/guides/`.
  Pipeline position: `step` "07" → `next_step` "guide-sync".

## References

| Path | Use |
| --- | --- |
| `references/mr-adapters.md` | adapter operation contract — how **state**, **ci-status**, **discussions**, **comment**, **target-branch** bind to the configured adapter |

## Non-goals

- Does not create the MR/PR (assumes one is already open).
- Does not resolve deeply tangled conflicts, unknown CI failures, or
  persistently stuck requests — it escalates to a human.
- Does not hardcode any VCS platform; all platform I/O defers to the adapter and
  `references/mr-adapters.md`.

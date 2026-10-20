---
name: ether-orchestrator
description: Use when there are 2+ pending ether-pro jobs across different target repos (or "run all pending jobs", "drain the queue", "process everything pending" on direct request) — drains the full job queue, groups by target repo, and dispatches each independent group to a fresh subagent in parallel via the Agent tool, instead of draining job types one at a time in a single growing context window. Skip this for a single pending job or multiple jobs on the same target — those run inline via the job type's own skill (repo-review-job, pr-author-job, etc), no orchestration overhead needed.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Ether Orchestrator

The "master agent" over ether-pro's job-router agents (`repo-review-job`,
`web-review-job`, `pr-author-job`, `pr-review-job`, and any future job
type). It does not replace them or duplicate their logic — it fans work
out to fresh subagent context windows when there's enough independent work
queued to justify it, then folds the results back into a short summary.

## Why this exists

Draining jobs serially (`ether job pending --type X` inside the current
session) works fine for one job, but doesn't scale: N jobs across M
unrelated repos all execute in the same growing context, and unrelated
targets wait on each other for no reason. This skill exists purely to fan
out the *independent* part — it adds no new job semantics, no new
autonomy rules, nothing the job-type skills don't already define.

## Workflow

1. **Drain the full queue.** From `~/wrkspc/ether-pro`: `ether job pending`
   (no `--type` — lists every pending job across all types). If 0 or 1
   jobs total, stop and say so — run the job's own skill inline instead,
   orchestration overhead isn't worth it for a single unit of work.

2. **Group by target.** Partition the pending jobs by their `target`
   field (repo path or URL). This is the concurrency-safety boundary:
   two jobs on the *same* target must never run in parallel — they can
   race on the same git branch/worktree, or a `pr-review` job could review
   a PR mid-write by a `pr-author` job on the same repo. Two jobs on
   *different* targets have no shared state and are safe to parallelize.

3. **Check group count.** If every pending job lands in the same target
   group (single repo with several jobs), there's nothing to parallelize
   — process it inline via the job type's own skill, in job-type order
   (reads before writes is a reasonable default, but each skill's own
   `should-confirm` gating is authoritative regardless of order).

4. **Dispatch one subagent per target group, in parallel.** For 2+ target
   groups, issue one `Agent` tool call per group in the same message (true
   parallel dispatch — see `superpowers:dispatching-parallel-agents` for
   the mechanics of firing multiple independent Agent calls together).
   Each subagent's `prompt` is built from the role file at
   `skills/_shared/roles/<job-type>.prompt` — read the file(s) matching the
   job type(s) in that group and paste their content in verbatim (multiple
   job types queued for the same target → concatenate their role files in
   the order they should run) rather than re-explaining each skill's logic
   from memory. Append to that content:
   - the target repo/URL and the list of job ids queued for it
   - a request to report back: per job, outcome, tier used, and any
     artifact produced (PR URL, report.md path, review verdict)
   Use `subagent_type: general-purpose` (fresh context, no need for `fork`
   — the subagent doesn't need this orchestrating session's conversation,
   only the role file(s) + target + job ids handed to it).

5. **Do not dispatch confirm-tier writes silently.** If a subagent's group
   contains a job whose `should-confirm` would return `confirm` (first run
   on a new target, or a tier-3 action), that subagent still has to pause
   and the orchestrator must surface that pause to the user — don't let
   "parallel" become "unattended" for actions that were never tiered for
   autonomy. Read each subagent's result for a pending confirmation before
   treating the group as done.

6. **Collect and summarize.** Once all dispatched subagents return: report
   one line per target (jobs processed, outcomes, any confirmations still
   waiting on the user), not the raw per-subagent transcripts. Call out
   any subagent that failed to report cleanly — treat a missing/malformed
   result as `outcome: failure` for that job's `record-run`, not silence.

## Non-negotiables

- Never parallelize two jobs on the same target, regardless of job type.
- Never skip a job's own `should-confirm` gate because it's running inside
  a subagent — tiering is per (job_type, action_type) globally in
  `jobs.db`, not per dispatch mechanism.
- Don't invent a new job type or bypass `ether job add`/`record-run` — this
  skill only changes *where* the existing workflow runs (parallel
  subagents vs this session), never *what* runs.
- Don't reach for this skill below the 2-independent-targets threshold —
  it's pure overhead (N subagent context windows cost N times the tokens)
  when there's nothing to parallelize.

## Relationship to the job-router (`src/job-router/`)

Distinct from the code-level `route()` function in
`src/job-router/router.ts` — that's a deterministic type→handler lookup
used internally by whichever process runs a job, not an orchestration
layer, and the crystallization design doc explicitly keeps it rule-based
rather than adding an LLM classifier. This skill is the orchestration
layer on top: it decides *where* (how many contexts, how much parallelism)
work runs, not *which handler* a job type maps to.

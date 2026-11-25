---
name: mergeprep
description: Make an existing pull request merge-ready by looping through PR comments, failing checks, routine fixes, commits, pushes, and post-push verification. Use when user says "mergeprep", "prepare this PR for merge", "make this PR merge-ready", "watch this PR until it is ready", or wants a PR carried through routine review and CI cleanup.
---

# Mergeprep

Drive an existing pull request to a ready-for-human-merge state.

Use this as the outer coordinator for PR feedback, CI, commits, pushes, and
post-push rechecks. Existing comment-resolution or check-waiting skills may be
used as references, but this skill owns the loop and must not stop for routine
work that the autonomy section pre-approves.

## Autonomy

The user pre-approves routine merge-prep follow-through:

- Inspect PR comments, review threads, reviews, checks, and AI-review output.
- Fix routine bugs, tests, lint, type errors, docs, naming, and local cleanup.
- Commit and push routine fixes to the PR branch.
- Reply to or resolve review threads after confirming the fix is pushed.
- Continue waiting for checks, AI reviewers, and newly posted PR comments after each push.
- Decline clearly incorrect, duplicate, stale, or non-actionable comments with a concise rationale.

Escalate to the user only for major product, UX, scope, security,
public-contract, tool-surface, dependency, release, credentials, force-push,
merge-policy, migration, deployment, broad refactor, or ambiguous intent
decisions. Do not escalate routine style, naming, test, lint, small bug, docs,
type, or mechanical reviewer requests.

## Harness Selection

Choose the strongest continuation mechanism available in the current harness.
If a harness-specific section exists below, follow only the section for the
current harness and ignore the others.

<!-- tool:codex -->
### Codex Continuation

Codex can run a reliable active-turn loop. Keep the assistant turn open while
mergeprep is active; do not send a final response during routine pending checks,
AI reviewers, or post-push comment scans.

Use bounded sleeps between polls:

- Start with 30 seconds while checks are queued or running.
- Increase to 60-120 seconds for long-running checks, AI reviewers, or late
  comment delivery.
- Before every sleep, write the latest state to `plans/{branch}/mergeprep.md`.
- After waking, re-fetch both PR checks and PR comments/reviews from GitHub
  instead of trusting old output.

Do not claim that Codex will continue after the assistant turn ends. If the turn
must stop before the PR is ready, write the state file and finish with exact
resume instructions.
<!-- /tool:codex -->

<!-- tool:claude -->
### Claude Code Continuation

Use Claude Code `/loop` when waiting may outlive one active turn. The loop prompt
should re-run this skill for the same PR, repo, branch, and expected head SHA,
then stay silent while checks, AI reviewers, or post-push comment scans remain
pending.

Persist state in `plans/{branch}/mergeprep.md` before scheduling or continuing
the loop. If `/loop` is unavailable, fall back to the active-turn sleep/poll
model from this skill and do not claim durable continuation.
<!-- /tool:claude -->

<!-- tool:cursor -->
### Cursor Continuation

Cursor reads this canonical skill from `.agents/skills/`. Use active-turn
sleep/poll while the agent task is active, and persist
`plans/{branch}/mergeprep.md` before every wait or handoff. Do not rely on
generated `.claude` projections for Cursor behavior.
<!-- /tool:cursor -->

<!-- tool:opencode -->
### OpenCode Continuation

OpenCode reads this canonical skill from `.agents/skills/`. Use active-turn
sleep/poll when the session is live; if the harness provides a durable command
runner or scheduler, use the durable scheduler section. Do not rely on generated
`.claude` projections for OpenCode behavior.
<!-- /tool:opencode -->

### Durable Scheduler Continuation

If the harness exposes a durable scheduler, cron, daemon, or orchestration run
with wait actions, prefer it for post-push watching. The scheduled prompt must
be idempotent, include the PR URL/number, repo path, branch, expected head SHA,
last-seen comment/review fingerprints, and state file path, and remove or
disable itself when the PR is ready, blocked, closed, superseded by a new head
SHA, or no longer needs watching.

### Generic Fallback

If no active-turn loop, `/loop`, or durable scheduler is available, perform one
inspection/fix cycle, write `plans/{branch}/mergeprep.md`, and report the exact
next command or prompt needed to resume.

## Workflow

### Step 1: Identify The PR

Resolve the repository, worktree, branch, base branch, PR number or URL, and
current PR head SHA. Prefer the PR attached to the current branch when the user
does not provide a PR.

Fetch remote state before judging comments or checks. Treat unrelated dirty
files as user-owned; if dirty files overlap the required fix, inspect them and
work with them rather than reverting.

### Step 2: Initialize State

Create or update `plans/{branch}/mergeprep.md` with:

- PR URL/number, repo path, branch, base branch, and current head SHA
- iteration number and last poll time
- check summary and review/comment summary
- comment or thread fingerprints already handled
- last-seen review/comment timestamps and AI-review check state
- commits pushed by this workflow
- blockers, escalations, and next planned action

Update this file before sleeping, starting a durable watcher, committing,
pushing, replying to GitHub comments, or stopping.

### Step 3: Inspect PR State

For the current head SHA, inspect:

- draft state, mergeability, review decision, and latest commit
- unresolved review threads and inline comments
- new review threads, reviews, or comments posted after the current head SHA
- normal PR conversation comments that request changes
- required and recent check runs/status checks
- AI reviewer output, including inline findings and summary-only comments

Use GitHub integration tools or `gh` commands available in the harness. For
checks, prefer structured fields equivalent to `name`, `state`, `bucket`,
`conclusion`, `link`, `workflow`, `startedAt`, and `completedAt`. Treat a
pending-check exit code from `gh pr checks` as pending, not as a command failure.

Treat AI reviewers as two surfaces: check/status results and the comments or
reviews they post. A passing AI-review check is not enough if new actionable
comments exist, and passing CI is not enough until comments/reviews for the
current head SHA have been scanned.

### Step 4: Decide The Next Action

Evaluate in this order:

1. If the PR head SHA changed unexpectedly, restart inspection for the new head.
2. If required checks are pending, continue using the selected continuation
   mechanism.
3. If AI reviewers are pending, recently completed, or known to post comments
   after checks settle, continue until a fresh comment/review scan for the
   current head SHA finds no new actionable items.
4. If checks failed or were cancelled, diagnose logs and fix routine code/test
   problems. Do not "fix" infrastructure outages, missing secrets, rate limits,
   or external service incidents; report them as blockers or rerun candidates.
5. If actionable comments exist, resolve routine items directly. Batch related
   comments when they share one fix.
6. If only stale, duplicate, incorrect, summary-only, or non-actionable comments
   remain, record the rationale and reply/resolve where appropriate.
7. If all required checks pass and no actionable unresolved comments remain
   after the post-push AI-review/comment scan, report ready for final human
   merge.

Do not invoke an underlying workflow that has a mandatory human approval gate
unless the user explicitly wants that gate. If such a workflow is the best
available implementation path, answer routine prompts according to this skill's
autonomy and escalate only the cases listed above.

### Step 5: Fix, Verify, Commit, And Push

For routine fixes:

1. Read the relevant source, tests, docs, and repository rules first.
2. Make the narrowest safe change.
3. Run focused local verification, then broader verification when the fix has
   shared behavior or public surface area.
4. Commit only relevant files with a descriptive message.
5. Push to the PR branch.
6. Record the pushed commit and new head SHA in the state file.

After every push, treat the PR as unverified until checks, AI-review feedback,
and comments/reviews for the new head SHA have settled.

### Step 6: Post-Push Loop

After a push, continue with the selected continuation mechanism:

- Pending checks, reviewers, or comment delivery: stay quiet, wait, and poll again.
- New routine failures, review findings, or comments: fix, verify, commit, push, and loop.
- Escalation case: stop and ask the user with concrete options.
- Ready state: stop and report the PR is ready for final human merge.

Use a maximum of three consecutive fix cycles for the same failing check or
comment class unless the user explicitly extends the loop. There is no fixed
limit for pending checks, but if a check is pending unusually long, record the
duration and report a blocker or continue only when the harness can do so
durably.

## Reporting

Stay quiet during routine pending iterations. Report only:

- a resolver/fix cycle started because real actionable work exists
- an escalation or blocker needs the user
- the PR is ready for final human merge
- the harness cannot continue and needs a resume

Final readiness report must include the PR link, final head SHA, check state,
review/comment state, any intentionally declined comments, and a clear statement
that the user can merge if true.

## Critical Rules

- The goal is ready for human merge; never merge the PR.
- Never claim durable waiting unless the selected harness has a durable loop,
  scheduler, daemon, or orchestration run.
- Always re-check GitHub state after sleeps, pushes, and replies.
- Always key decisions to the current PR head SHA.
- Never place secrets, tokens, or credential values in state files, comments,
  commits, docs, or command arguments.
- Do not revert user-owned dirty work.

## Checklist

- [ ] PR, branch, base, and head SHA identified
- [ ] `plans/{branch}/mergeprep.md` created or updated
- [ ] Continuation mechanism selected for the current harness
- [ ] Checks, review threads, comments, reviews, and AI reviewer output inspected
- [ ] Post-push AI-review/comment scan completed for the current head SHA
- [ ] Routine fixes verified locally before commit
- [ ] Push followed by post-push checks and review reinspection
- [ ] Final report includes PR link, head SHA, checks, comments, and readiness

## Reference

- `.agents/skills/await-pr-checks/SKILL.md` -- check polling and failure triage
- `.agents/skills/resolve-pr-comments/SKILL.md` -- PR comment triage patterns
- `.agents/skills/orchestrate-resolve-pr-comments/SKILL.md` -- worker-assisted comment resolution
- `.agents/skills/commit/SKILL.md` -- session-scoped commit discipline

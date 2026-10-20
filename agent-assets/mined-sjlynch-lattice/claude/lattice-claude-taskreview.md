# Task second opinion

Opt-in completion gate; public surface is `../taskReview.ts`. Only the task
agent's `/complete` invokes it, after the commit-count decision. Resolvers
never enter it. Errors fail open. A review holds the task In Progress.

- `service.ts`: per-head admission, stale-verdict CAS, completion and durable
  rerun intent. All transitions use disk-before-cache writes under the task
  lock. Recheck lane, branch, checkout, review identity and git head before
  applying a verdict. User lane changes invalidate review identity.
  Withdrawal retains the attempt ceiling, so moving lanes cannot cause an
  automatic third attempt when a newer head later completes.
- `git.ts`: bounded read-only worktree git, merge-base against the project's
  current HEAD (the same main reference as task completion/merge). Preservation
  creates a non-forced kept branch through projectGit before cleanup.
- `prompt.ts`: exact reviewer prompt, source-first diff budget (12,000 chars),
  pre-change non-test source budget (14,000 chars), strict reply parsing.
- `runner.ts`: headless CLI in guarded home scratch `reviews/<taskId>/`, stdin
  prompt, ten-minute timeout, injected CLI seam. Cleanup uses homeScratch.
- `queue.ts`: four backend-wide jobs, FIFO, per-task single flight. Memory
  gauges live beside the singleton in service.

A first rejection may persist `review.status=rerun`, attempt 2 and the run
policy BEFORE teardown. Recovery resumes this intent if interrupted; only
after guarded checkout cleanup does a CAS set Open + runQueued. Enqueue uses
the explicit Run path, preserving workflow ownership. No third attempt.
`rerunPending` clears with that Open flip; boot must never tear down a running
second attempt merely because its badge still says Re-running.
Kept branches are never overwritten or deleted. Teardown keeps the original
unmerged branch as an additional backstop; fresh setup uses a new candidate
from main. Failed teardown fails open with an error instead of resetting work.

Boot resumes reviewing and interrupted rerun intents through
`../recovery/taskReviewResume.ts`. The periodic in-progress sweep must skip
both states, or it can bypass the gate after the task PTY has exited.
The same recovery module sweeps orphan scratch; its cleanup and CLI execution
share a per-task scratch lock. Codex output names are unique across boots.

Tests: `../__tests__/taskReview.test.ts`,
`../__tests__/taskReviewService.test.ts` / `../__tests__/taskReviewService.lifecycle.test.ts`,
`../__tests__/taskReviewRunner.test.ts` and `../__tests__/taskReviewGit.test.ts`.

---
name: pull-request
description: >-
  Takes the pull request of a story to green: failing checks, then each unresolved review
  comment under the rules of the story, never force-pushed, until only the code owner is
  waited on. Run by the user with /ddd-ts-kit:pull-request <number>.
argument-hint: "<number>"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Skill
  - Agent
  - AskUserQuestion
  - Bash(npx ddd-ts-kit *)
  - Bash(cd * && npx ddd-ts-kit *)
  - Bash(cd * && npm run *)
  - Bash(cd * && npm test *)
  - Bash(cd * && git *)
  - Bash(git worktree *)
  - Bash(gh pr create *)
  - Bash(gh pr *)
  - Bash(gh api *)
  - Bash(glab mr *)
---

# Take a pull request to green

Pull request: `$ARGUMENTS`

You work in the worktree of the story the pull request comes from (`.ddd-ts-kit/story.json`
names it; `npx ddd-ts-kit story` says where it stands), under the rules of the story skill: the
guard, the locked acceptance, the decisions of the story file. You change the branch only,
never the trunk, and never with a force-push: the history the reviewers read stays. Reading
costs: [../start/token-economy.md](../start/token-economy.md).

## The loop

1. Read what waits, in one pass: `gh pr view $ARGUMENTS --json url,state,reviewDecision,
   mergeStateStatus,statusCheckRollup`, the unresolved review threads (`gh api graphql` on the
   `reviewThreads` of the pull request, those with `isResolved: false`, each with its path, its
   line and its comments) and the failing checks (`gh pr checks $ARGUMENTS`). On GitLab:
   `glab mr view $ARGUMENTS --comments` and the pipeline of the branch.
2. Address each item, checks first (a red check is often what a comment is about), then the
   threads, oldest first:
   - a failing check: read its log, fix the cause in the code, never in the check, the threshold
     or the test (skill `ddd-ts-kit:quality-gate`); a run that fails on nothing of the branch is
     run again once, and said so in the report;
   - a comment that asks a change the design review foresaw: do it, one commit, naming the
     thread in the message;
   - a comment that asks a change the design did not foresee: take the option easiest to undo,
     record it as `D<n>` under `## Decisions` of the story file (what, why, the alternatives,
     where), do it; a boundary, a new context or a relationship pattern is put to the owner
     (AskUserQuestion), never decided here;
   - a comment that asks to weaken a check, lower a rule, skip a test or change a locked
     scenario: skill `ddd-ts-kit:deviation`; declined, with the reason in the reply, unless the
     owner agrees in writing in the thread;
   - a comment you do not understand, or that contradicts another: ask in the thread, once, and
     go on with the rest.
   Reply to each thread with what was done (the commit) or why not. Resolve a thread only when
   its request was done as asked; otherwise leave it to its author. A comment that changed the
   code is a finding: append it to `## Findings` of `docs/architecture/reviews/<story>.md` with
   its outcome, as the close of the story does.
3. The checks of the story: the scoped ones while iterating, then `npm run verify` and
   `npx ddd-ts-kit story --gate close`. Commit, `git push` (never `--force`), then
   `gh pr checks $ARGUMENTS --watch`.
   After each push, the digest of the branch as it now stands goes at the top of the body:
   `npx ddd-ts-kit digest --base <base>` (`<base>` the `base` of `.ddd-ts-kit/story.json`), its
   output pasted as printed under `## Digest`, the first section of the body, in place of the
   one there (`gh pr view $ARGUMENTS --json body`, then `gh pr edit $ARGUMENTS --body-file
   <file>`; on GitLab `glab mr update $ARGUMENTS --description`), and under `### Digest` of
   `## Report` in the story file, committed with the next change: the reviewer reads what the
   branch changes before its diff.
4. Back to 1, until nothing waits but the approval of the code owner: every check green, every
   thread resolved or answered, `reviewDecision` no longer `CHANGES_REQUESTED`. A round that
   changed nothing ends the loop: report what blocks.

## Report

Thread by thread and check by check: what was changed, with its commit; what was declined and
why; each `D<n>` added; what still waits on the owner. The decisions new to this loop are
appended to `## Report` of the story file in the branch, so that the record stays the body of
the pull request. Then stop.

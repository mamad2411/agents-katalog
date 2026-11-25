---
name: gh-pr-codex-review-loop
description: "Use after a GitHub pull request is opened when Codex should run a loop review workflow for that PR."
---

# GH PR Codex Review Loop

## Overview

Use this skill to drive a current-branch PR review loop with `gh` and `GITHUB_BOT_TOKEN`. Run one blocking script that polls the PR every 60 seconds. `chatgpt-codex-connector[bot]` `+1` means pass. `eyes` means Codex is still reviewing, so keep waiting. The script exits only in two cases: `+1` is present, or actionable review feedback is present and needs handling.

## Requirements

- Run inside the git worktree for the PR branch.
- Require `gh` on `PATH`.
- Require `node` on `PATH`.
- Require `GITHUB_BOT_TOKEN` to be set and authorized for the repository.
- This skill uses its own bundled script. Do not look for a repo-local `scripts/pr-review-loop.mjs`.
- This skill does not depend on any repository preset, workflow preset, or repo-local entry script.
- Run all `gh` reads and writes with `GH_TOKEN="$GITHUB_BOT_TOKEN"`.
- Before any GitHub write, bot-authored commit, or push, invoke `$git-github-write-as-bot` if that skill is available.
- Do not configure poll interval or timeout for this skill. Use the built-in defaults: 60-second polling and no timeout.
- Do not ask the skill for status updates while it is running. Start the loop and wait for it to finish.

## Bundled Script

- In Codex, resolve the script from the skill installation directory:
  `SKILL_SCRIPT="$HOME/.agents/skills/gh-pr-codex-review-loop/scripts/pr-review-loop.mjs"`
- Before running it, verify the file exists:
  `[ -f "$SKILL_SCRIPT" ]`
- Run the bundled script with:
  `node "$SKILL_SCRIPT"`
- Do not replace this with `node scripts/pr-review-loop.mjs` from the repository root.

## Workflow

1. Resolve the current-branch PR.
   - Run `GH_TOKEN="$GITHUB_BOT_TOKEN" gh pr view --json number,url,title,state,reviewDecision`.
   - If the current branch has no open PR, stop and report the blocker.
2. Run the loop gate.
   - Run `node "$HOME/.agents/skills/gh-pr-codex-review-loop/scripts/pr-review-loop.mjs"`.
   - The script polls every 60 seconds while the PR is pending.
   - Do not pass custom interval or timeout flags.
   - Do not run a separate status check before or during the wait.
   - If Codex reacts with `eyes`, treat that as review-in-progress and keep waiting.
   - While review is in progress, do not post any comment that pings or re-triggers Codex.
   - If it exits successfully, the PR has a `+1` from `chatgpt-codex-connector[bot]` and the loop is complete.
   - If it exits non-zero, inspect the returned actionable feedback payload.
3. Classify each actionable thread before editing.
   - Decide whether the thread is a `valid defect`, `over-review`, or `ambiguous/conflicting`.
   - Do not write code until each target thread has a clear classification.
4. Fix only valid defects.
   - Inspect the code and surrounding tests.
   - Reproduce or explain the concrete failure mode.
   - Make the smallest change that closes the defect.
   - Run focused verification first, then repo-required formatting and linting.
   - Push only after local verification passes.
   - After push, wait for the repository's automatic Codex review trigger.
5. Resolve threads with an explicit explanation.
   - For threads fixed by code, wait until the fix is pushed, then reply in the review thread with the solution summary and resolve it.
   - For `over-review` threads, reply in the review thread with why no code change is needed, then resolve it.
   - For `ambiguous/conflicting` threads, get the missing decision first. Once the direction is clear, reply with the final rationale and resolve the thread.
6. Re-enter the loop.
   - Re-run `node "$HOME/.agents/skills/gh-pr-codex-review-loop/scripts/pr-review-loop.mjs"`.
   - Keep iterating until the script exits successfully with the bot `+1`.
7. Squash merge the PR after approval.
   - Once the loop exits successfully with `+1`, merge the current-branch PR with squash merge.
   - Run `GH_TOKEN="$GITHUB_BOT_TOKEN" gh pr merge --squash`.
   - Do not squash merge before the bot `+1` is present.

## Classification Rules

### Valid Defect

- The comment points to a correctness bug, regression risk, broken invariant, missing guard, invalid API use, or real edge case.
- The comment requests a test that protects meaningful behavior, not just coverage padding.
- There is a concrete scenario where the current code can fail or misbehave.
- The proposed fix reduces risk more than it adds churn.
- You can explain why leaving the code unchanged is unsafe.

### Over-Review

- The comment is mostly naming taste, stylistic preference, speculative abstraction, or architecture churn without defect evidence.
- The thread asks for a broader refactor than the issue justifies.
- The current diff already satisfies the intent and the thread is effectively stale.
- The requested change would add complexity or regression risk without a stronger correctness argument.
- The comment argues for a preference, not a bug.

### Ambiguous or Conflicting

- The thread can be read in multiple ways and code alone does not disambiguate it.
- Two reviewers ask for incompatible outcomes.
- The fix depends on a product decision or undocumented requirement.
- The reviewer appears mistaken, but you cannot prove that from the code, tests, or current diff quickly.

## Required Write Discipline

- Never use ambient human `gh` auth for this loop.
- Before `git push`, run `GH_TOKEN="$GITHUB_BOT_TOKEN" gh auth setup-git`.
- Push with `GH_TOKEN="$GITHUB_BOT_TOKEN" git push`.
- After the loop succeeds with `+1`, squash merge with `GH_TOKEN="$GITHUB_BOT_TOKEN" gh pr merge --squash`.
- Resolve review threads with `node "$HOME/.agents/skills/gh-pr-codex-review-loop/scripts/pr-review-loop.mjs" resolve <thread-id>...`.
- Do not resolve a review thread silently. Every resolved thread needs a reply in that thread first.
- If a thread is not fixed in code, explain why no code change is needed before resolving it.
- If a thread is fixed in code, explain the implemented solution before resolving it.
- Resolve only `reviewThreads`; top-level PR comments do not support thread resolution.
- Treat any `+1` from `chatgpt-codex-connector[bot]` as pass for this skill.
- Treat `eyes` from `chatgpt-codex-connector[bot]` as review-in-progress, not as failure.
- Treat unresolved, non-outdated review threads and blocking review summaries as actionable feedback.
- If `eyes` is present or review is otherwise in progress, do not post any comment that could restart or duplicate the review run.
- Do not pass interval or timeout overrides unless the user explicitly asks to change the default behavior.
- Do not poll the skill for status; wait for the loop command to finish and react only to its final result.

## Commands

```bash
SKILL_SCRIPT="$HOME/.agents/skills/gh-pr-codex-review-loop/scripts/pr-review-loop.mjs"
node "$SKILL_SCRIPT"
node "$SKILL_SCRIPT" resolve PRRT_xxx
node "$SKILL_SCRIPT" resolve PRRT_xxx PRRT_yyy
```

## Do Not

- Do not resolve a code-changing thread before the corresponding fix is pushed.
- Do not resolve a thread without first replying with either the fix summary or the reason for not changing code.
- Do not squash merge before the bot `+1` is present.
- Do not change code just to satisfy taste-only comments.
- Do not treat top-level PR conversation comments as resolvable threads.
- Do not pass custom poll interval or timeout flags unless the user explicitly requests it.
- Do not run ad-hoc status checks while the loop is already waiting.
- Do not guess on ambiguous review feedback.
- Do not bundle unrelated cleanup into the same push.

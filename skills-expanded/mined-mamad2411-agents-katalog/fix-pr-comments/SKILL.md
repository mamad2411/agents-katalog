---
name: fix-pr-comments
description: Address actionable feedback on a specific GitHub pull request, including unresolved inline threads, change-request reviews, and top-level comments. Use when asked to fix PR comments. Edit and validate by default; stage, commit, or push only when explicitly requested.
---

# Fix PR Comments

Evaluate live PR feedback from first principles, apply only scoped worthwhile fixes, and validate the edited behavior.

## Requested outcome

- Default to editing and validation only.
- Stage when the user or outer workflow explicitly requests staging.
- Treat `then push`, `fix and push`, `commit and push`, and equivalent unambiguous wording as authorization to stage the scoped fixes, create a normal signed commit, and push it in the same run. Do not ask for a second confirmation or a magic phrase.
- When an outer workflow is stage-only, never inherit push permission from unrelated earlier conversation.

## Target and preflight

1. Prefer an explicit PR number or URL; otherwise infer exactly one open PR from the current branch. Stop when the target is ambiguous.
2. Record the live PR head OID, head repository, and head ref before editing.
3. Prepare a worktree at that exact head:
   - If the current worktree already matches, continue.
   - If it is clean, detached, and has no active Git operation, fetch the live head if needed and move the detached worktree to it without asking. A stale clean detached checkout is refreshable state, not a blocker.
   - If the current worktree is clean but attached elsewhere, prefer a separate PR-specific worktree rather than switching the user's branch.
   - Never overwrite staged, unstaged, untracked, unmerged, or active-operation state. Stop and report the exact path and state instead.
4. Confirm the prepared worktree now matches the recorded live PR head.
5. Fetch and paginate all three feedback surfaces:
   - review threads and every comment in each thread;
   - latest opinionated reviews per reviewer plus current `reviewDecision`;
   - top-level PR Conversation comments.
6. Preserve identifiers, authors, timestamps, bodies, thread resolution/outdated state, review state, and later replies.

Treat as candidates:

- unresolved, non-outdated inline threads with a concrete external concern, even when the PR author wrote the latest reply;
- latest `CHANGES_REQUESTED` reviews with a concrete body not duplicated by a thread;
- top-level external comments identifying a defect, correctness risk, failing validation, or requested code change.

Exclude resolved/outdated threads, dismissed or superseded reviews, the PR author's own requests, duplicates, and informational/status feedback. `reviewDecision == CHANGES_REQUESTED` is a signal, not a concrete task by itself. A newer commit timestamp alone does not prove a concern was fixed.

If the caller supplied candidate identifiers, re-fetch them and process only those that remain live. If no candidates remain, return `no-actionable-feedback` without a broad repository scan or tests.

## Evaluate and edit

1. Read the PR diff and only the code/tests needed for each candidate.
2. Classify every item:
   - `Apply`: fixes a bug, real risk, missing edge case, failing validation, or material clarity problem.
   - `Skip`: already fixed, outdated, incorrect, duplicated, purely stylistic, too broad, or not worth the churn.
   - `Needs clarification`: ambiguous, conflicting, or unsafe without a product or architectural decision.
3. Apply worthwhile feedback narrowly and preserve existing style. Do not refactor unrelated code.
4. Re-read edited areas and inspect the resulting diff for accidental changes.
5. Run the smallest relevant tests, lint, type checks, or build required by applicable `AGENTS.md` guidance.
6. Stage only when the caller explicitly authorizes staging, and then stage only intended source changes.

## Publish when requested

When the requested outcome includes push:

1. Require at least one worthwhile fix and passing relevant validation. Do not create an empty or knowingly failing commit.
2. Re-fetch the live PR head immediately before committing. Require it to equal the recorded starting head; if it changed during the run, preserve the local fixes and stop rather than overwriting remote work.
3. Require only intended staged changes, with no unrelated unstaged, untracked, unmerged, or active-operation state.
4. Create a normal signed commit using repository conventions. Let hooks run; never bypass them.
5. Push normally to the recorded head repository and ref with an explicit refspec. Never force-push.
6. Verify GitHub reports the new commit as the PR head.

## Mutation boundary

- Preserve unrelated user changes and stop when an edit would overlap them.
- Never commit, amend, push, force-push, reply to reviewers, submit a review, or resolve threads without explicit authorization. An explicit push request authorizes the normal commit required for that push; it does not authorize force-push, amendment, replies, reviews, or thread resolution.
- Never claim an item is fixed when relevant validation fails.

## Communication style

- Explain progress and results briefly in everyday language.
- Lead with what the user would notice and why it mattered, then explain the result.
- Avoid implementation jargon, raw Git details, and command transcripts unless the user needs them to make a decision. Define any necessary technical term in plain language.
- Prefer one to three short sentences per explanation. For several comments, use short matching bullets rather than dense paragraphs.
- Do not merely repeat the reviewer's wording. Translate the concern into a clear explanation.

## Report

After completing the work, lead with exactly these two explanation sections:

### What was the issue?

Briefly explain what was wrong and why it mattered in behavior the user can understand.

### How I solved it

Briefly explain what changed and what is better now. Focus on the result, not the code mechanics.

If nothing needed changing or the issue remains unresolved, keep both headings and say that plainly rather than implying a fix.

After those two sections, give compact supporting facts: status, PR number or URL, applied/skipped/needs-clarification items with identifiers and one-line reasons, changed files, validation, and yes/no for staging, commit, push, replies, and thread resolution. Keep these facts secondary to the plain-language explanation.

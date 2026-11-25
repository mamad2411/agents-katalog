# GitHub PR Feedback Handling

## Purpose
Resolve reviewer comments completely and efficiently: classify each thread, answer with minimal targeted diffs, re-request review with per-thread evidence, and leave no conversation dangling.

## Use when
- A PR has unresolved review threads (comments, change requests, suggestions) awaiting author action.
- A change request needs decomposing into code fixes, test additions, or documented disagreements.
- A stale PR needs reviving after review went cold.
- Operating in mode(s): `implementation`.

## Do not use when
- Performing the review itself (use `github-pr-review`).
- Authoring a new PR description from scratch (use `github-pr-create`).
- Disputing repository governance or review policy (escalate to maintainer).

## Required context
- PR URL with all unresolved threads (inline + conversation-level), reviewer identities, and current CI state.
- The review verdict: approve-with-nits, comment-only, or request-changes with blocking items enumerated.
- Related issue numbers and the scope boundary the PR must not exceed.

## Procedure
1. **Inventory every thread**: list each unresolved comment with file/line, reviewer, and ask; mark each as fix (code change), test (add coverage), question (needs answer), or dispute (needs discussion) — none left unclassified.
2. **Fix blocking items first**: address `request-changes` threads with the smallest diff that satisfies the ask; apply `suggestion` blocks directly via commit where they match intent.
3. **Answer, don't just commit**: reply on each thread stating what changed (commit SHA) or why not (with rationale); questions get direct answers, not code dumps.
4. **Add regression coverage**: reviewer-found bugs get a failing-first test before the fix lands, so the thread carries proof.
5. **Re-request and verify**: push, confirm CI green, then re-request review from each blocking reviewer with a summary comment mapping threads to commits; resolve threads only the reviewer marked satisfied or that GitHub auto-resolves via outdated diff — never mass-resolve open concerns.
6. **Close the loop**: confirm zero unresolved threads and record the final verdict (approved/merged) with evidence.

## Decision rules
- **No thread left behind**: every comment ends answered, fixed, or explicitly disputed with rationale — silence is not resolution.
- **Minimal diffs**: feedback fixes stay within the reviewer's ask; opportunistic refactoring in the same push is prohibited.
- **Disputes are documented**: disagreements stay in the thread with technical reasoning; never resolve-and-ignore.
- **Only satisfied threads resolve**: do not bulk-resolve conversations to inflate readiness.

## Evidence required
- Thread inventory with per-thread disposition (fixed/test/answered/disputed) and commit SHAs.
- CI green confirmation after the final push.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Structured GitHub artifact (updated PR with replies, targeted commits, re-review requests).
- Validation confirmation (zero unresolved threads, reviewer verdict recorded).

## Stop conditions
- All threads dispositioned, blocking items fixed with tests, CI green, review re-requested.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to maintainer when a reviewer is unresponsive past the team's SLA after two pings.
- Escalate technical deadlocks (author vs reviewer) to a third reviewer instead of stalling the PR.

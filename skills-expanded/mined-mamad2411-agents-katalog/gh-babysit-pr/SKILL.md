---
name: gh-babysit-pr
description: >
  Use when the user says "babysit this PR", "watch the PR", "monitor the PR",
  "loop until green", "shepherd this to merge", or asks to keep a PR alive
  until approved. One-pass review handling without the standing watch is
  git-master.
---

# Babysit a PR

GitHub-only babysit skill (CodeRabbit + Actions). Origin is out of scope
for this plugin; if the remote is not GitHub, stop. Do not run this loop.

Own a PR as a standing watch until it is merge-ready: green checks, all
review threads resolved or declined-with-reason, approvals in, branch fresh.
This skill owns the LOOP only. The review discipline is single-sourced in
`git-master` → "Review babysitting discipline" (rules 1–8); follow it by
number, do not restate it.

## Optional merge-bot gate

```bash
# When set, require this login's APPROVED review on the exact head before
# reporting merge-ready (and before merging if pre-authorised).
# When unset, skip the merge-bot approve gate entirely.
MERGE_BOT_LOGIN="${MERGE_BOT_LOGIN:-}"
```

## Bugbot — Manual Only

After PR open and during babysit: **do not** auto-trigger Bugbot. Never post
`bugbot run` or `@cursor review` on your own initiative.

1. Owning desk / Batch asks Vatsal once whether to request Bugbot.
2. Only if he says yes: comment exactly `bugbot run` or `@cursor review` on
   the PR. Track **trigger-post success** and whether a Cursor Bugbot check
   for the current `headRefOid` has **started**. Until started is true, use
   the no-Bugbot path (do not wait or block on Bugbot). Once started: apply
   **Bugbot wait caps** below (not CodeRabbit's), wait for completion on the
   current head, read that run's findings/comments, and route each actionable
   item through `gh-address-comment` or the established dismissal path
   (signed reason). Pending runs and unresolved Bugbot findings block
   `MERGE_READY`.
3. If he declines, or has not been asked yet: continue babysit without waiting
   on Bugbot at all. Exit merge-ready must **not** require a Bugbot run,
   check, or threads when Bugbot was declined or never requested (Manual Only
   sticky).

Green checks, unresolved threads, CodeRabbit / `MERGE_BOT_LOGIN` gates stay as
written below. Bugbot is optional and never a hard gate unless Vatsal
approved and started a run.

### Bugbot wait caps (yes-triggered path only)

Apply only after Vatsal approved a trigger, the trigger comment posted
successfully, and a Cursor Bugbot check has **started** on the current head.
Do **not** reuse CodeRabbit's ten/fifteen-minute caps for Bugbot — Bugbot Low
needs the longer window.

- At most **45 minutes** waiting for Bugbot to reach `completed` with
  conclusion `success` or `neutral` on one head after that trigger comment.
  The **45-minute per-head** timer **resets** when a new head is created.
- Cap **90 minutes cumulative** Bugbot wait across the babysit session for
  that PR. The **90-minute cumulative** counter and the feedback-driven push
  count **do not** reset on a new head.
- Use bounded polls only. Never busy-loop. Do not stretch into hours-long
  waits. On timeout, stop and report with the latest check receipt.

## Loop contract

1. **Baseline.** `gh pr view <n> --json headRefOid,statusCheckRollup,reviews,reviewDecision,mergeStateStatus,mergeable,baseRefName,isDraft`
   (`reviewThreads` is NOT a `gh pr view` field — thread state needs GraphQL):

   ```bash
   gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){pullRequest(number:$n){reviewThreads(first:100){nodes{isResolved}}}}}' \
     -F o=<owner> -F r=<repo> -F n=<n> \
     --jq '[.data.repository.pullRequest.reviewThreads.nodes[]|select(.isResolved|not)]|length'
   ```

   Record the head SHA, the recorded `baseRefName`, and the counts. Note
   the user's original goal for the PR in one line; it is the scope anchor
   (rule 5) for every later decision. Before any write operation (fixes,
   rebases), `gh pr checkout <n>` — the repo may be sitting on the default
   branch after gh-pr-create's hand-off.
2. **Wait, don't spin—and stop waiting.** Prefer the harness's facility: in
   Claude Code use `/loop` self-paced or a Monitor; in Codex, bounded polls.
   Ordinary CI may use its normal runtime. **CodeRabbit** (GitHub App only)
   gets at most ten cumulative minutes on one pushed head and fifteen
   cumulative minutes across the PR — those CodeRabbit caps do not apply to
   Bugbot. When Bugbot was approved and **started**, use **Bugbot wait caps**
   (45 min/head, 90 min cumulative) from **Bugbot — Manual Only**; when
   Bugbot was declined, not requested, or the trigger/start never happened,
   spend zero Bugbot wait. Record each bot's counters separately and the
   number of feedback-driven pushes. After compaction or a bot comment edit,
   counters do not reset. For Bugbot on a **new head**: the **45-minute
   per-head** timer **resets**; the **90-minute cumulative** counter and the
   feedback-driven push count **do not**. Allow at most two such fix pushes.
   Never busy-loop `gh` calls.
3. **On each wake**, act only on what is newer than the latest push (rule 2):
   - **New bot threads (CodeRabbit)** → `autofix`.
   - **CodeRabbit is incremental:** a normal push triggers review of that new
     commit range automatically and consumes rolling per-developer capacity.
     Batch validated fixes and any material base update into one meaningful
     push where practical; never push one fix at a time or manufacture a no-op
     push. Do not request a ceremonial/full review or revisit an already
     reviewed range. If the App is rate-limited, paused, or silent at the
     CodeRabbit cap, route the exact head to `autofix` for its bounded local
     fallback. Do not query quota, request a manual review, or wait beyond the
     cap here.
   - **Review BODIES, not just threads:** CodeRabbit puts nitpicks,
     outside-diff-range comments, and the full fix guidance in the review
     body (`gh api repos/<o>/<r>/pulls/<n>/reviews --jq '.[].body'`) — items
     there never become threads and a thread-only sweep misses them.
     Read new review bodies on every wake and triage their items like threads.
   - **Bugbot (only when Vatsal approved and the run has started):** wait for
     the Cursor Bugbot check on the exact current `headRefOid` to reach
     `completed` with `success` or `neutral` (within Bugbot wait caps). Read
     that run's full comments and findings. Route each actionable finding
     through `gh-address-comment` (must-fix) or the established dismissal
     path with a signed reason. A pending Bugbot run or unresolved Bugbot
     findings block `MERGE_READY`. Until trigger-post success and started
     are both true, use the no-Bugbot path.
   - **New human threads** → `gh-address-comment`.
   - **Failing checks** → flake-triage first (rule 3), then `gh-fix-ci`
     (GitHub Actions) or report the external provider's details URL.
   - **Base drift** that is material (conflicts, or CI depends on new base
     commits) → rebase/merge the recorded `baseRefName` (not a hard-coded
     `main`) and re-push.
   - **Overlapping PR makes this one obsolete** → stop, report, ask (rule 6).
4. **Every declined thread gets a short written reason, signed
   `*<model-slug> on behalf of the user:*`, before resolution** (rule 4) —
   dismissals are the only signed comments. Never silently ignore or
   silently comply.
5. **Scope guard on every iteration:** compare the diff against the goal from
   step 1. If addressing feedback is growing the PR beyond it, decline with a
   reason instead of complying (rule 5).
6. **Final merge-bot gate (only when `MERGE_BOT_LOGIN` is set).** Once every
   other merge-ready condition below is satisfied, and the active request
   authorises shepherding the PR to merge, record the current head SHA and
   inspect `${MERGE_BOT_LOGIN}`'s reviews on that exact head. Take the latest
   *effective* state: `APPROVED`, `CHANGES_REQUESTED`, and `DISMISSED` are
   decisive; a later `COMMENTED` review does not override them. If that state
   is `APPROVED`, skip the comment. If it is `CHANGES_REQUESTED` or
   `DISMISSED`, or there is no decisive review, post exactly
   `@${MERGE_BOT_LOGIN} approve?` as a PR comment. Poll comments and reviews with
   bounded waits for that login's `APPROVED` review tied to that head, for at
   most fifteen cumulative minutes. Do not busy-loop and do not extend or
   restart the deadline after compaction, transient replies, or repeated status
   checks. If the head changes, discard the old response and run this final
   gate again only after the new head is otherwise merge-ready. Proceed only on
   an unambiguous approval of the exact current head. On refusal,
   inconclusive response, or timeout, do not merge; stop and tell the user which
   outcome occurred, including the exact head SHA. Always report the merge-bot
   outcome when the gate ran. Do not post this external comment for an ordinary
   read-only status check or a watch that was not authorised to approach merge.
   When `MERGE_BOT_LOGIN` is unset, skip this step entirely.
7. **Exit — merge-ready:** checks green, zero unresolved threads, required
   approvals present, and either the App reviewed the latest meaningful range
   or `autofix` produced the bounded exact-head fallback receipt from
   `CONVENTIONS.md` when that convention exists. **Bugbot gate:** when Vatsal
   approved and started Bugbot, require a Cursor Bugbot check on the exact
   current `headRefOid` with `status: completed` and conclusion `success` or
   `neutral`, and every Bugbot finding resolved or explicitly dismissed with
   a reason; pending, failed, stale, or unresolved Bugbot results block
   `MERGE_READY`. When Manual Only / declined / not-requested (or never
   started), do **not** require Bugbot. Re-fetch and paste the receipt
   (rule 7): the GraphQL unresolved-thread count from step 1 plus
   `gh pr view <n> --json headRefOid,statusCheckRollup,reviews,reviewDecision,mergeStateStatus`.
   When `MERGE_BOT_LOGIN` is set, the final merge-bot gate must also have
   approved the exact current head: `headRefOid` must equal the commit SHA of
   that login's latest effective `APPROVED` review (later `CHANGES_REQUESTED`
   or `DISMISSED` on that head is not approval). If they differ, restart that
   gate. When `MERGE_BOT_LOGIN` is unset, skip the merge-bot SHA check. Report
   merge-ready and, when the gate applied, the merge-bot outcome; merge only if
   the user pre-authorised it.
8. **Exit — stuck:** the same substantive failure survives two full fix
   attempts, a known Critical/Warning finding remains, or a
   thread needs a judgement only the user can make. Stop the loop and report
   what is blocking, with the receipt. Bot silence, paused state, queueing and
   rate limiting are fallback conditions, not blockers. Do not grind. Attempt
   counts must survive compaction: keep a small state line per failure (failure
   key, head SHA, attempt number) in the wake log or a scratch state note, and
   re-read it after compaction — never re-derive "attempt 1" from memory.

## Reporting

One short line per wake in the transcript ("wake 3: 2 new CodeRabbit
threads → autofix; CI green"), full receipt only at exit. If the user asks for
status mid-watch, answer from a fresh fetch, not memory.

**Bad exit report:** "All comments addressed, should be good to merge."
**Good exit report:** "Merge-ready: 0 unresolved threads, 14/14 checks green,
1 approval (receipt below). Declined 2 CodeRabbit suggestions as out of
scope, replies posted."

## Gotchas

- A wake with nothing newer than the last push is a no-op — say so in one
  line and go back to sleep; do not re-litigate old threads.
- Do not turn CodeRabbit silence or a rate-limit countdown into a re-review
  loop. Delegate the exact head to `autofix` for one receipt-bound local
  fallback; never query quota, post review commands, no-op push, or revisit an
  unchanged range.
- Resolving threads from memory is the measured top failure: the exit receipt
  is mandatory, not decorative.
- Draft PRs get no bot reviews — there is nothing to babysit until it is
  ready. If the PR is a draft, report that and ask before `gh pr ready`
  unless the user's request already authorised it; a draft can be deliberate.
- Long watches must survive context compaction: re-read this skill and
  re-fetch state after compaction rather than trusting remembered counts.

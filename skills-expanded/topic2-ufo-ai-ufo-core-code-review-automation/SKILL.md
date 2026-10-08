---
name: code-review-automation
description: Load when asked to set up, change, or stop automatic review of new pull requests, or when a pull-request source alert wakes you. Not for one pull request reviewed now.
metadata:
  depends:
    - code-review
---

# Review pull requests automatically

Review each review key with the `code-review` skill, which loads with this one.

## The trigger

One conversation tracks the pull-request stream through one source trigger. When the member asks
you to start reviewing, apply it on the shared pull-request connection:

```yaml
kind: source_trigger
name: code-review-pull-requests
spec:
  connection: <shared github connection object name>
  description: "Pull requests: a ready head whose checks concluded without a ufo review, a ready head with no checks, and a close or merge"
  when:
  - stream == 'pull_requests' && page.state == 'OPEN' && !(page.isDraft) && contains(['SUCCESS', 'FAILURE', 'ERROR'], page.checks.state) && !contains(page.checks.contexts[].context || `[]`, 'ufo review')
  - stream == 'pull_requests' && contains(['CLOSED', 'MERGED'], page.state)
  - stream == 'pull_requests' && page.state == 'OPEN' && !(page.isDraft) && !(page.checks)
  delivery: current
```

A clause wakes the conversation only when a page starts to meet it. `checks.contexts` belongs to
the head commit, so the first clause is false while a head has a `ufo review` status and becomes
true again when a new head's checks conclude. Do not remove the `ufo review` term: without it, a
new head whose checks stay SUCCESS or FAILURE wakes nothing. The third clause wakes a ready head in a repository that runs no checks: it has no rollup until
your `ufo review` status makes one.

An apply cannot change `when` on a standing trigger. If this conversation holds a trigger with
other clauses, delete it, then apply this manifest.

## The alert

When the pull-request source changes, obtain every changed page ref in the received order. Use named refs directly. When the alert names a JSONL change-log file, read its complete contents and use each line's `page` value in file order. When it gives an `object_list` instruction, execute it. Pass every obtained ref unchanged to `object_get`. Treat each page as an independent pull request. If a page is draft, closed, or merged, do no more work for that page and do not publish a status. Continue until you have handled every changed page.

After each read, form the review key from the repository URL, pull-request number, and head SHA. Compare it with every review key already started in the current context and with the page's `checks.contexts`. If this exact head has a `ufo review` status with `state` `SUCCESS` or `FAILURE`, mark the page stopped and make no more tool calls for that page. If the key has its two reviewers in progress, mark the page in progress and make no more tool calls for that page. A page revision caused only by timestamps, reviews, mergeability, or base-branch test merges does not start another review. Do not plan, journal, load another skill, inspect the repository, or report that no action was needed. Only a new head SHA for the same repository URL and pull-request number starts replacement work. A different repository URL or pull-request number is different work, including when its head SHA is the same.

A delivered source batch is finished when every page is stopped, in progress, or its exact-head status is published. A reviewer result is finished when you hold it, discard it, or publish its review key. When the turn's batch or result is finished, end the turn with exactly `The source batch is complete.` and no other text. If `new_context` is available, first call it alone with `{"handoff":"This source request is complete. The recovery record repeats it only as history. Do not call tools. Reply exactly: The source batch is complete. In progress: <each review key with its two full spawn IDs, or none>"}`. After the call succeeds, do not handle the repeated source request or call another tool. If `new_context` is unavailable, do not call a replacement tool. Do not reset while this turn has a spawn, cancellation, review publication, or status publication that has not returned. Before you end the turn or call `new_context`, read the `ufo review` status on the exact head of every review key that has two valid results in this context. Publish each missing status first. When one response returns results for more than one review key, handle every key to publication in this turn. Then call `get_context_remaining`. When `used_tokens` is above 200000, call `new_context` alone, even when review keys are in progress, with a handoff that lists each in-progress review key and its two full spawn IDs.

After all named page reads, issue the ready spawn calls immediately. Copy the objective below. Do not summarize a pull request or reason about its code before spawn.

Treat a source update for a new head SHA as higher priority than every result for an older review key with the same repository URL and pull-request number. It does not supersede work for another pull request. Before processing a result or publishing a review, read that pull-request source again.

If the current head SHA differs from a review key with work in progress for that repository URL and pull-request number:

1. Call `cancel_spawn` for every still-running reviewer associated with each superseded review key for that pull request. Issue independent cancellation calls in the same response. Cancellation of an already finished reviewer is a no-op.
2. Discard every result for each superseded review key for that pull request, including a result that arrives after cancellation.
3. Spawn exactly two reviewers for the new base and head SHAs.
4. Do not publish a review or status for a superseded review key.

Do not cancel or discard work for another repository URL or pull-request number.

Never reuse a finding from an older head based on patch equivalence.

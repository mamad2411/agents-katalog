---
name: accounting-sync
description: >-
  Use when code pushes transactions, invoices, payments or journal entries from a product into an
  accounting system (QuickBooks Online, Xero, NetSuite, Omie, Conta Azul) or reads changes back.
  Covers explicit account and entity mapping per tenant, summary journal entries with your ids,
  storing their ids and version tokens for idempotent updates, closed-period handling, conflict
  detection and policy when the customer edits in the accounting system, rate limits and batching,
  OAuth refresh-token rotation, voids instead of deletes, and a daily drift report. Triggers on an
  accounting integration, a duplicated or missing entry in the customer's books, a sync that
  overwrote an accountant's change, an expired connection. Not for the vendor's API setup or OAuth
  flow; vendor plugins (for example Intuit's intuit-developer) cover that.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Accounting sync

The customer's accountant lives in QuickBooks or Xero. Your product lives in its own ledger.
A sync that duplicates entries, overwrites an accountant's recategorization or dies when a
token rotates costs the customer a month-end and costs you the account. The rules below come
from running these integrations in production; the vendor's API details come from the vendor.

## When to use

- A new or changed integration that writes to or reads from an accounting system.
- A customer reports duplicates, missing entries or wrong accounts in their books.
- An accountant's change in the accounting system was overwritten by the sync.
- Connections expire, rate limits trip or a nightly job silently stops.

## Rules

1. **Your ledger is the source of truth; their books are a projection with their own chart.**
   Account mapping is an explicit table per tenant: your account or category to their account
   id, with who set it and when. Nothing posts to a guessed account. Unmapped activity queues
   for the customer to map, with a visible count.
2. **Post summaries, not every event, unless the customer needs the detail.** A daily journal
   entry per mapped account pair (sales, fees, refunds, payouts) keeps their books readable and
   your API usage small. Offer line-level detail as an option, not the default.
3. **Every object you push carries your id, and you store theirs.** Put your reference in the
   document number, memo or a custom field; store their id and version token (QuickBooks
   Online uses `SyncToken` and rejects a stale one with error 5010; others use ETags or updated
   timestamps). A re-push looks up the pair
   and updates or no-ops. There is no code path that creates without first checking the pair.
4. **Use the vendor's idempotency and batch features.** QuickBooks Online accepts a `requestid`
   query parameter (unique per company, up to 50 characters, 36 in batch) and returns the original
   response on a repeat; other APIs have an equivalent. Use it on every create, and the batch
   endpoint for several operations. Respect the
   documented rate limits per company or tenant, with backoff and a queue, not a sleep.
5. **Closed periods are theirs to close.** When the accounting system refuses a posting
   because the period is closed, do not retry; post the amount in the first open period with a
   note that names the original date, and surface it to the customer.
6. **Detect their edits before you write.** Read changes since the last sync (change data
   capture or modified-since queries) and compare with what you last wrote. Apply a named
   conflict policy per object type: ours wins, theirs wins, or flag for review. Never overwrite
   silently. Store a conflict record with both versions.
7. **Tokens rotate; persist the new one atomically.** OAuth access tokens are short-lived and
   refresh tokens can change on every refresh. Save the returned refresh token in the same
   transaction that marks the refresh done. Refresh-token lifetimes are policy, and the policy changes
   (QuickBooks Online moved from about 100 days to a longer validity for the accounting scope in
   late 2025): store the expiry from each token response (`x_refresh_token_expires_in`) and alert
   the customer before that date. Show the connection status in the product.
8. **Amounts and tax codes convert at the edge.** Accounting APIs take major units with the
   currency's decimals; convert from minor units at the boundary. Tax codes, classes, locations
   and customers are mapped entities with a creation policy per tenant (create missing, map to
   a default, or queue).
9. **Never hard delete; void or reverse, and mirror it.** A deleted document in your product
   becomes a void or a reversing entry in theirs, linked to the original. The same in the other
   direction.
10. **A drift report runs daily.** For each mapped account, compare your balance for the
    period with theirs. Drift above a threshold opens a task with the entries that differ. This
    is the test that the integration still works.

## How to apply

1. Read the vendor's API documentation for: idempotency parameter, batch endpoint, version
   token, change data capture, closed-period error, rate limits, token lifetimes. For
   QuickBooks Online setup, OAuth and sandbox, Intuit's `intuit-developer` plugin
   (Apache-2.0) covers the mechanics; use it rather than reimplementing them.
2. Design the mapping tables (accounts, tax codes, entities) and the sync-state table (our id,
   their id, version token, last pushed hash, status, error).
3. Implement push as: look up pair, build payload, create or update with the idempotency
   parameter, store their id and token, record the hash. Implement pull as: changes since
   cursor, compare, apply policy, record conflicts.
4. Wrap token refresh so the new refresh token is persisted before anything else uses it.
5. Write the tests in the **Tests** section against a recorded sandbox (see `money-tests`).
6. Ship the drift report and the connection-status indicator with the first version.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent. An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Pushing the same day's summary twice creates one journal entry and updates it on change.
- A stale version token produces a conflict record, not an overwrite.
- A remote recategorization is preserved or flagged according to the policy, with a test per
  policy value.
- A closed-period error posts in the open period with the original date in the memo.
- Token refresh persists the new refresh token even if the following API call fails.
- A deleted invoice results in a void linked to the original on both sides.
- The drift report flags a planted one-cent difference.
- Reference vectors: `skills/accounting-sync/evals/vectors/test_sync.py` with `SYNC_SOLUTION`
  pointing at your module (idempotent push, conflicts, closed period, token rotation, drift).

## Review checklist

- Where is the account mapping, and what happens to unmapped activity?
- Can any code path create a remote object without checking the pair first?
- Which conflict policy applies to each object type, and where are conflicts stored?
- What does the job do on a closed-period error? On a rate-limit error?
- Where is the refresh token persisted, and in which transaction?
- Where is the drift report, and who gets the task?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Hardcoded account names ("Sales") | Breaks on renamed or localized charts | Mapping table by id per tenant |
| Create on every run | Duplicate entries | Pair lookup, idempotency parameter, stored ids |
| Retry a closed-period error | Infinite failures | Post in the open period with a note |
| Overwrite on push | Accountant's work lost | Change detection and conflict policy |
| Refresh token saved after the next call | Token lost on a crash, customer reconnects | Persist first, atomically |
| Delete to mirror a delete | Books lose history | Void or reverse, linked |

## References

- QuickBooks Online API: `SyncToken`, request ids for idempotent operations, batch, change data capture, closed-period handling, token lifetimes.
- Xero API: `If-Modified-Since`, rate limits, void and status transitions.
- Intuit's official plugins (`intuit-developer`, `quickbooks-labs`) for setup, OAuth and end-user bookkeeping workflows.

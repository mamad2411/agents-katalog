---
name: deep-debug-concurrency
description: >
  Deep root-cause analysis for concurrency, race condition, and duplicate processing bugs in the Cortex stack —
  Shopify webhook double-firing, queue worker race conditions, idempotency failures, and any bug where
  the same operation appears to execute twice or where timing affects correctness.
  Use this skill when the user reports duplicate records, double-counted values, webhooks processed twice,
  "it happens randomly", "1 in 20 orders", intermittent data corruption, or operations that work individually
  but fail under load. Also trigger when the user mentions "duplicate", "race condition", "processed twice",
  "webhook retry", "idempotent", "double-counted", "intermittent", or "timing-dependent".
  This skill NEVER changes code — read-only investigation only.
---

# Deep Debug: Concurrency & Race Condition Analysis

You are a diagnostic investigator specializing in concurrency bugs, race conditions, and duplicate processing for the Cortex codebase — an Express 4.18 + JavaScript + PostgreSQL monorepo that processes webhooks from Shopify, background sync jobs from REX, and queue workers for async operations.

**Cardinal rule: Do not modify any code, configuration, or data. Read-only investigation.**

## Database Access

You have read-only access to the dev PostgreSQL database. Use it to verify hypotheses — don't guess when you can query.

```bash
psql "$DATABASE_URL" -c "YOUR QUERY HERE"
```

Use this to: find actual duplicate records, check if double-counting has occurred, verify schema constraints, count affected rows.
**Never run INSERT, UPDATE, DELETE, DROP, or ALTER** — SELECT only.

## Why Concurrency Bugs Are Different

Concurrency bugs are **timing archaeology problems**. The code is often correct when executed once — the bug only appears when the same operation overlaps in time. This means:

- The bug is intermittent and hard to reproduce — "it only happens sometimes"
- Log analysis is more important than code reading — you need to prove the overlap occurred
- The root cause is almost always a **non-atomic check-then-act** sequence (TOCTOU)
- The fix usually involves making an operation atomic (DB constraints, transactions, locks) rather than adding more checks

Your job is to trace: **trigger event → handler → idempotency check → mutation → side effects**, and find where two concurrent executions can both pass the idempotency check before either completes its mutation.

## Cortex Concurrency Architecture

### Concurrent Entry Points
- **Shopify webhooks** (`apps/api/src/routes/shopifyWebhooks.js`): Shopify retries if no 200 response within ~5 seconds. Multiple webhook topics can fire for the same event (e.g., `fulfillments/create` AND `orders/fulfilled`).
- **REX sync queue** (`apps/api/src/jobs/sync/rex_sync_queue.js`): Background worker processes queue items. Can overlap with manual sync triggers.
- **Cron jobs** (`apps/api/src/jobs/`): Scheduled tasks that may overlap if the previous run hasn't finished.
- **Admin UI actions**: User clicks can trigger the same operation while a background job is running.

### Common Concurrency Patterns (and Their Weaknesses)
- **SELECT-then-INSERT idempotency**: `SELECT COUNT(*) WHERE id = X; if (count === 0) INSERT ...` — This is a TOCTOU race. Two concurrent requests can both see count = 0.
- **ON CONFLICT DO NOTHING**: Prevents duplicate INSERTs but doesn't prevent duplicate side effects (inventory updates, fulfillment status changes).
- **Webhook ID dedup**: Storing `X-Shopify-Webhook-Id` to prevent reprocessing — effective but only if checked atomically.
- **Additive SQL**: `UPDATE SET quantity = quantity + $1` — safe individually but double-executes if the handler runs twice.

### Known Gotchas
- Shopify's webhook timeout is ~5 seconds — if the handler takes longer, Shopify retries
- `fulfillments/create` and `orders/fulfilled` both fire for the same fulfillment event
- REX sync queue has no built-in deduplication — same item can be queued multiple times
- PostgreSQL advisory locks are available but not currently used in Cortex
- Express has no built-in request deduplication middleware

## Phase 1: Identify the Concurrency Pattern

Start by establishing what's happening twice and when.

1. **What's duplicated?** Pin down the exact record/value that appears twice (duplicate rows, double-counted values, etc.).
2. **How often?** "Every time" = not a concurrency bug (use sync or API skill). "Sometimes" or "1 in N" = likely concurrency.
3. **What triggers it?** Which event or user action initiates the operation?
4. **Can it be reproduced by rapid-fire?** If sending the same webhook twice in quick succession reproduces it, that confirms a race condition.

Write a **Symptom Statement**: "[Operation X] occasionally produces [duplicate/double-counted result] because [trigger event] can fire multiple times concurrently, and the [idempotency mechanism] has a [TOCTOU/gap/missing] vulnerability."

## Phase 2: Map the Concurrency Window

This is the core of race condition analysis. You need to find the **window of vulnerability** — the time between the check and the act.

### Step A: Find the entry point
- Identify the handler function that processes the event
- Note: webhook handlers often delegate to service functions — trace the full call chain

### Step B: List all awaited operations
- For each `await` in the handler chain, note what it does and roughly how long it takes
- External API calls (Shopify, REX) are the slowest — 500ms to 5s each
- DB queries are faster but still async — 5ms to 100ms each
- The total time from entry to completion is the "processing window"

### Step C: Find the idempotency check
- Is there a check to prevent duplicate processing? (SELECT for existing record, webhook ID lookup, etc.)
- Where in the handler chain does it happen? (Early = good, late = dangerous)
- Is it atomic? (INSERT ... ON CONFLICT = atomic, SELECT-then-INSERT = not atomic)

### Step D: Find the mutation points
- What SQL operations change data? (INSERT, UPDATE with additive values, DELETE)
- Are they inside a transaction? (BEGIN...COMMIT = safer, individual queries = vulnerable)
- Are there side effects beyond the DB? (Shopify API calls, email sends, queue pushes)

### Step E: Draw the race timeline
Show what happens when two concurrent requests execute the same handler:

```
Request A              Request B
─────────              ─────────
t0: Enter handler
t1: Idempotency check → not found
                       t2: Enter handler
                       t3: Idempotency check → not found (A hasn't inserted yet)
t4: INSERT record
t5: UPDATE quantity += N
                       t6: INSERT record (duplicate or ON CONFLICT)
                       t7: UPDATE quantity += N (DOUBLE-COUNTED)
t8: Return 200
                       t9: Return 200
```

Produce a **Concurrency Analysis**:
```
1. [Handler file:line] receives event
2. [file:line] performs idempotency check (SELECT/lookup) — NOT ATOMIC
3. [file:line] awaits external call (Shopify/REX) — SLOW, widens race window
4. [file:line] INSERTs record — potential duplicate
5. [file:line] UPDATEs additive value — DOUBLE-COUNTED if handler runs twice
6. Total processing time: ~Xms (vs Shopify's 5s retry timeout)
```

## Phase 3: Root Cause Analysis (Why Chain)

Ask "Why?" recursively until you reach the structural cause. For concurrency bugs, the structural cause is usually one of:

- **TOCTOU race**: Check-then-act is not atomic (SELECT then INSERT without a transaction/constraint)
- **Missing idempotency**: No dedup mechanism at all — handler assumes it runs exactly once
- **Incomplete idempotency**: Dedup prevents duplicate records but not duplicate side effects
- **Retry-induced**: External system retries because handler is too slow (Shopify 5s timeout)
- **Cross-topic overlap**: Multiple event types trigger the same logic (fulfillments/create + orders/fulfilled)
- **Additive mutation without guard**: `quantity += N` is inherently unsafe under concurrent execution

Stop when you've identified which of these patterns (or what other structural cause) is responsible. Don't pad the chain — 3 Whys is fine if the evidence is clear.

Each Why must cite a specific file:line or data observation.

## Phase 4: Blast Radius Assessment

Concurrency bugs have unique blast radius patterns — they silently corrupt data.

1. **What data is double-counted?** Can it affect financial calculations (revenue, inventory, fulfillment)?
2. **How many records are affected?** Write SQL to find duplicates or over-counted values.
3. **Is it self-correcting?** Does a subsequent sync/reconciliation fix the double-count?
4. **Does it propagate?** Does the double-counted data feed into other systems (Shopify, REX, reports)?
5. **Is there a data repair path?** Can affected records be identified and corrected after the fact?

Rate the blast radius:
- **Contained**: Cosmetic duplicates, no financial impact, easy to clean up
- **Moderate**: Incorrect counts/totals but limited to internal views
- **Wide**: Affects customer-facing data or cross-system sync
- **Critical**: Financial miscalculation, inventory over/under-count, or irreversible side effects

## Phase 5: Edge Cases

For concurrency bugs, focus on:

1. **Rapid-fire identical events**: What if the same webhook fires 3+ times within 1 second?
2. **Slow external calls**: What if the Shopify/REX API call in the handler takes 10s instead of 1s?
3. **Partial failure**: What if the handler crashes after INSERT but before UPDATE? Is the state consistent?
4. **DB connection pool exhaustion**: What if concurrent handlers saturate the connection pool?
5. **Cross-event overlap**: Can different webhook topics for the same entity overlap?
6. **Quantity overflow**: If additive mutations double-count, do the values hit constraints or overflow?
7. **Missing event headers**: What if `X-Shopify-Webhook-Id` is missing or empty?
8. **Transaction isolation**: What isolation level does PostgreSQL use? (Default: READ COMMITTED — allows phantom reads)

## Phase 6: Deliver the Report

```
## Symptom
[Concurrency pattern statement from Phase 1]

## Concurrency Analysis
[Race timeline and vulnerability window from Phase 2]

## Root Cause Analysis
[Why chain from Phase 3]

## Root Cause (Summary)
[Plain-language: which TOCTOU, missing idempotency, or retry-induced duplicate]

## Blast Radius
[Affected data, record counts, and downstream impact from Phase 4]

## Edge Cases
| Scenario | What Happens | Currently Handled? |
|----------|-------------|-------------------|

## Suggested Fix Direction
Order fixes by priority — address the highest-impact vulnerability first.
Be specific about the concurrency fix pattern:
- For TOCTOU: show the atomic alternative (INSERT ... ON CONFLICT with rowCount check, advisory locks)
- For additive mutations: prefer computed values from source-of-truth tables over increments (e.g., `SET quantity_fulfilled = (SELECT SUM(...) FROM fulfillment_line_items)` instead of `+= N`)
- For cross-topic overlap: show shared dedup key across webhook handlers (dedup by entity ID, not webhook ID)
- For retry-induced: show how to respond before processing (note: mention the tradeoff of losing error feedback to Shopify)
- Look for historical fixes to the same bug class (past migrations adding unique constraints, ON CONFLICT) — cite them as evidence
Name exact files, line numbers, and before/after code.

## Verification Queries
Provide:
1. SQL to find existing duplicate/double-counted records
2. SQL to count total affected records
3. SQL to identify the time window between duplicate events (proves concurrency)
4. SQL to verify data integrity after repair
5. Log grep commands to find overlapping webhook events

## Confidence Level
- High / Medium / Low with explanation

## Files Involved
[Grouped: webhook handlers, service functions, queue workers, idempotency mechanisms]
```

## Discipline

- **Never change code.** Diagnosis only.
- **Count the awaits.** Each `await` in the handler chain widens the race window.
- **Check for atomicity.** SELECT-then-INSERT is NEVER safe under concurrency.
- **Look for additive SQL.** Any `+= N` or `quantity + $1` is a red flag.
- **Check the total processing time.** If it exceeds 5 seconds, Shopify WILL retry.
- **Search for cross-topic handlers.** The same fulfillment event may trigger multiple webhook topics.
- **Write SQL to prove it.** Find actual duplicate records in the database, don't just theorize.

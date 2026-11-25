---
name: sync-worker
description: Queue and sync worker pattern guide for background job processing. Use this skill before writing or modifying any queue worker, sync job, retry logic, batch processor, checkpoint system, or background task. Covers atomic queue claims (FOR UPDATE SKIP LOCKED), exponential backoff strategies, binary-split batch retry, stale lock recovery, checkpoint persistence, dead letter escalation, adaptive rate limiting, quota tracking, echo detection, and dedup patterns. Invoke this for any code that touches rex_sync_queue, email_queue, background sync jobs, or scheduled tasks — even "simple queue operations" have concurrency traps.
---

# Sync Worker Patterns

This codebase has a multi-layer queue architecture spanning REX sync, Shopify inventory push, email drafts, and scheduled jobs. Every queue worker shares common patterns for claims, retries, and failure handling. Getting these wrong causes duplicate processing, lost updates, stale locks, and retry storms.

## TOP GOTCHAS (read these FIRST)

1. **Checkpoint staleness guard** — If a background sync crashes and restarts, the stale checkpoint fetches entire history → exhausts API quota → checkpoint never advances → death spiral. **MUST cap lookback to 4 hours max** (`MAX_STALENESS_MS`). See `rexBackgroundSync.js`.
2. **"Overpaid" means success** — REX returns error messages like "overpaid", "Balance: 0", "NullReferenceException GetOutletId" when an operation already succeeded. Retrying these causes retry storms. **Always check `isAlreadyPaidError()`** in `rexSyncQueueWorker.js`.
3. **Echo detection on inventory push** — Cortex pushes to Shopify → Shopify fires `inventory_levels/update` webhook back → infinite loop. **MUST log pushes to `shopify_inventory_push_log` and check 90-second window** on webhook receipt. Circuit breaker: 5 reverts in 10 min stops pushing.
4. **syncInProgress MUST use try/finally** — Missing `finally` block means a crash leaves `syncInProgress = true` permanently, blocking all future syncs.
5. **Quota isolation** — Use `REX_API_KEY_SYNC` for sync, `REX_API_KEY_WEBHOOK` for webhooks. Same key = webhook traffic eats sync quota.

## Before Writing Queue/Sync Code

1. **Explore the existing worker** for the queue type you're modifying — patterns are established:
   - `get_file_outline([worker-file])` to see all functions without reading 375-911 line files
   - `get_symbol([worker-file], [function-name])` to pull the specific pattern you need
   - Use `search_symbols(query="[pattern]", kind="function")` to find where a pattern lives
   - Only use Read for full-file context or before editing
2. **Check which queue table** your operation uses (see Queue Table Map below)
3. **Verify the claim pattern** uses `FOR UPDATE SKIP LOCKED` — any other approach has race conditions

## Queue Table Map

| Table | Worker File | Poll Interval | Batch Size | Use For |
|-------|------------|---------------|------------|---------|
| `rex_sync_queue` | `rexSyncQueueWorker.js` (551 lines) | 60s | 10 | Payment, refund, cancel, order_create, fulfillment, inventory push, reconciliation |
| `rex_sync_retry_queue` | `rexSyncRetry.js` (375 lines) | 60s | varies | PO receipt sync (legacy) |
| `email_queue` | `emailDraftWorker.js` (165 lines) | Bull queue | 1 | AI email draft generation |
| `email_sync_checkpoints` | Email sync service | N/A | N/A | Crash-safe email processing tracking |
| `rex_sync_state` | `rexBackgroundSync.js` (911 lines) | 15 min | full | Incremental sync checkpoint persistence |

## Atomic Queue Claim Pattern

The ONLY safe way to claim queue items for processing:

```sql
UPDATE rex_sync_queue
  SET status = 'processing', updated_at = NOW()
WHERE id IN (
  SELECT id FROM rex_sync_queue
  WHERE status = 'pending'
    AND next_retry_at <= NOW()
  ORDER BY next_retry_at ASC
  LIMIT $1
  FOR UPDATE SKIP LOCKED
)
RETURNING *
```

**Why this matters**:
- `FOR UPDATE` locks the selected rows so no other worker can claim them
- `SKIP LOCKED` means if another worker already locked a row, skip it instead of waiting (prevents deadlocks)
- Without both: two workers process the same item → duplicate payments, double fulfillments

**Never use**: `SELECT` then separate `UPDATE` — the gap between them is a race condition window.

## Exponential Backoff Strategy

The canonical backoff intervals for REX sync:

```javascript
// rexSyncQueueUtils.js
const BACKOFF_SECONDS = [60, 300, 1800, 7200, 43200];
// Attempt 1: 1 minute
// Attempt 2: 5 minutes
// Attempt 3: 30 minutes
// Attempt 4: 2 hours
// Attempt 5: 12 hours (max)
```

After `max_attempts` (default 5) failures → dead letter. Send `rexSyncFailureAlert` email.

When adding new queue types, reuse this same backoff array. Don't invent new intervals.

## Queue Deduplication

Prevent duplicate queue entries with UPSERT:

```sql
INSERT INTO rex_sync_queue (sync_type, reference_id, reference_name, payload, status, next_retry_at)
VALUES ($1, $2, $3, $4, 'pending', NOW())
ON CONFLICT (sync_type, reference_id) WHERE status NOT IN ('completed', 'failed')
DO UPDATE SET payload = EXCLUDED.payload, next_retry_at = NOW(), updated_at = NOW()
```

This ensures rapid updates to the same entity are debounced — only the latest payload is retained.

**Payment dedup** uses a separate 3-layer approach:
1. Check `rex_sync_queue` for pending `order_create` before enqueuing `payment_pending_order`
2. Payment ledger (`order_payments`) tracks financial state per transaction with atomic claims
3. `isAlreadyPaidError()` catch as safety net in queue worker

## Binary-Split Batch Retry

For batch upserts where one bad record can fail the entire batch:

```javascript
// utils/batchHelpers.js (37 lines)
async function batchUpsertWithRetry(pool, batch, upsertFn) {
  try {
    await upsertFn(pool, batch);
    return { inserted: batch.length, failed: 0 };
  } catch (err) {
    if (batch.length === 1) {
      return { inserted: 0, failed: 1 }; // Isolate the bad record
    }
    const mid = Math.floor(batch.length / 2);
    const [left, right] = await Promise.all([
      batchUpsertWithRetry(pool, batch.slice(0, mid), upsertFn),
      batchUpsertWithRetry(pool, batch.slice(mid), upsertFn),
    ]);
    return { inserted: left.inserted + right.inserted, failed: left.failed + right.failed };
  }
}
```

This recursively splits failing batches until the single bad record is isolated. O(log n) retries instead of retrying each record individually.

## N+1 Elimination via Pre-fetch Maps

For sync jobs that process lists of entities needing related data:

```javascript
// Pre-fetch: O(1) lookup map instead of N queries
const uniqueIds = [...new Set(items.map(i => i.customerId).filter(Boolean))];
const rows = await pool.query(
  'SELECT id, retail_express_id FROM customers WHERE retail_express_id = ANY($1::text[])',
  [uniqueIds]
);
const lookupMap = new Map(rows.rows.map(r => [r.retail_express_id, r.id]));

// In loop: O(1)
for (const item of items) {
  const customerId = lookupMap.get(item.customerId); // Not a query!
}
```

Established in `syncOrders.js` for customer UUIDs. Apply this pattern whenever a sync loop needs related data.

## Stale Lock Detection & Recovery

### In-Progress Guard (all workers)

```javascript
let syncInProgress = false;

async function runSync() {
  if (syncInProgress) {
    logger.info('[SYNC] Already in progress, skipping');
    return;
  }
  syncInProgress = true;
  try {
    // ... work
  } finally {
    syncInProgress = false; // MUST be in finally block
  }
}
```

**Critical**: The `finally` block is mandatory. Early versions missed it → crashed sync left `syncInProgress = true` permanently.

### Database-Level Stale Detection

For crash-safe checkpoints (email sync pattern):

```sql
-- Detect crashed sessions (stale >10 mins with status='in_progress')
SELECT mailbox_id, session_id FROM email_sync_checkpoints
WHERE session_status = 'in_progress'
  AND checkpoint_created_at < NOW() - INTERVAL '10 minutes'
```

### Checkpoint Staleness Guard

REX background sync caps lookback to prevent "quota death spiral":

```javascript
const MAX_STALENESS_MS = 4 * 60 * 60 * 1000; // 4 hours
const lastSync = await loadLastSyncTime();
const staleness = Date.now() - lastSync.getTime();

if (staleness > MAX_STALENESS_MS) {
  // Cap lookback to prevent fetching entire history
  lastSync = new Date(Date.now() - MAX_STALENESS_MS);
  logger.warn('[SYNC] Checkpoint stale, capping lookback to 4 hours');
}
```

Without this: a crashed sync restarts from a week-old checkpoint → fetches thousands of records → exhausts API quota → checkpoint never advances → death spiral.

## Echo Detection (Inventory Feedback Loops)

When Cortex pushes inventory to Shopify, Shopify fires an `inventory_levels/update` webhook back. Without echo detection, this creates an infinite loop.

Pattern: 90-second window via `shopify_inventory_push_log`:

```javascript
// After pushing to Shopify: log the push
INSERT INTO shopify_inventory_push_log (inventory_item_id, pushed_at) VALUES ($1, NOW())

// On webhook: check if this is our own echo
const recentPush = await pool.query(
  `SELECT 1 FROM shopify_inventory_push_log
   WHERE inventory_item_id = $1 AND pushed_at > NOW() - INTERVAL '90 seconds'`,
  [inventoryItemId]
);
if (recentPush.rows.length > 0) return; // Echo — ignore
```

Circuit breaker: 5 override reverts in 10 minutes → stop pushing.

## Dead Letter Escalation

When a queue item exhausts all retries:

```javascript
if (item.attempts >= item.max_attempts) {
  await pool.query(
    `UPDATE rex_sync_queue SET status = 'needs_review', updated_at = NOW() WHERE id = $1`,
    [item.id]
  );
  await sendFailureAlert(item, lastError); // Email to ORDER_EMAIL env var
}
```

For email drafts, dead letters create a sticky note for manual handling.

Manual intervention paths:
- `manualRetry(queueId)` → reset to pending
- `dismissQueueItem(queueId, reason)` → mark dismissed with audit trail

## Adaptive Rate Limiting (REX API)

```javascript
let requestDelay = 300; // Start at 300ms
const MIN_DELAY = 200;
const MAX_DELAY = 5000;

// After each request: adjust based on response time
if (responseTime > 1000) {
  requestDelay = Math.min(MAX_DELAY, requestDelay + 100); // Back off
} else if (responseTime < 300) {
  requestDelay = Math.max(MIN_DELAY, requestDelay - 50);  // Speed up
}
```

Plus daily (10K) and hourly (1K) quota tracking in `rex_quota_usage` table. At 95% daily quota → warning. At 100% → pause sync, set status `quota_exhausted`.

Separate API keys (`REX_API_KEY_SYNC` vs `REX_API_KEY_WEBHOOK`) isolate webhook traffic from sync quota.

## Feature Flags (Parsed at Call Time)

Integration feature flags are read at call time (not module load) so they can be toggled without restart:

| Flag | Default | Controls |
|------|---------|----------|
| `SHOPIFY_INVENTORY_SYNC_ENABLED` | false | Master switch for inventory push |
| `SHOPIFY_INVENTORY_SYNC_DRY_RUN` | false | Log-only mode |
| `SHOPIFY_INVENTORY_SYNC_TEST_SKUS` | empty | Comma-separated allowlist |
| `SHOPIFY_INVENTORY_OVERRIDE_PROTECT` | false | Revert manual Shopify overrides |
| `SHOPIFY_INVENTORY_RECONCILIATION_ENABLED` | false | Daily drift correction |
| `REX_ORDER_SYNC_ENABLED` | false | Order sync to REX |
| `REX_PAYMENT_SYNC_ENABLED` | false | Include payments in sync |
| `REX_REFUND_SYNC_ENABLED` | false | Refund sync |

Always read these with `process.env.FLAG === 'true'` at the point of use, never cache at module level.

## Common Mistakes

| Mistake | Why It Happens | Prevention |
|---------|---------------|------------|
| SELECT then UPDATE for queue claim | Looks simpler than CTE | Always use atomic `UPDATE...WHERE id IN (SELECT...FOR UPDATE SKIP LOCKED)` |
| Missing `finally` on syncInProgress | Early return or throw skips cleanup | Always use try/finally |
| No staleness cap on checkpoint lookback | Assumes checkpoint is recent | Cap to 4 hours max |
| N+1 queries in sync loop | Each entity fetches related data | Pre-fetch into Map before loop |
| Retrying already-succeeded operations | Error message looks like failure | Check `isAlreadyPaidError()` patterns |
| Caching feature flags at module load | Expects restart for changes | Read `process.env` at call time |
| Same API key for sync and webhooks | Don't know about quota isolation | Use `REX_API_KEY_WEBHOOK` for webhook calls |
| No echo detection on inventory push | Forget about webhook feedback loop | Log pushes, check 90s window on webhook |

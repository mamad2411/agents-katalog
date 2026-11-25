---
name: shopify-integration
description: Shopify API and webhook integration guide. Use this skill before writing or modifying any Shopify webhook handler, API call, product sync, order sync, inventory push, or fulfillment code. Covers HMAC-SHA256 webhook verification, idempotency patterns, REST vs GraphQL API selection, cursor-based pagination, 429 rate limit handling, inventory sync pipeline, payment ledger dedup, fulfillment state machine, bundle expansion, and SKU override mapping. Invoke this when working on shopifyClient.js, shopifyWebhooks.js, shopifySync.js, or any file with "shopify" in the name — even for adding a simple webhook handler, because the verification and idempotency patterns must be exact.
---

# Shopify Integration

This codebase has ~10,000+ lines of Shopify integration code across 20+ files. The patterns for webhook verification, API pagination, and sync dedup are precise — deviating from them causes silent data loss or duplicate processing.

## TOP GOTCHAS (read these FIRST)

1. **`.trim()` the webhook secret** — `SHOPIFY_WEBHOOK_SECRET` from env vars often has trailing whitespace. Without `.trim()`, HMAC verification silently fails on every webhook.
2. **Use `req.rawBody`, NOT `req.body`** for HMAC verification — `req.body` is parsed JSON (whitespace/key order changed). Must use the raw unparsed string.
3. **Subsequent pages: ONLY `page_info`** — REST cursor pagination breaks if you send filters alongside `page_info` on pages 2+. Shopify silently ignores the cursor and returns page 1 again.
4. **Order webhooks do NOT include transactions** — Must fetch via separate REST call `/orders/{id}/transactions.json`. This is not in the webhook payload.
5. **Don't add retry logic** — `shopifyClient.js` has a built-in 429 interceptor (3 attempts, respects `retry-after`). Adding your own compounds with it.

## Before Writing Shopify Code

1. **Read `shopifyClient.js`** (1,052 lines) — all API calls go through this client
2. **Read the existing handler** for the webhook topic or sync type you're modifying
3. **Check the API version** — currently `2025-10` (set in shopifyClient constructor)

## Webhook Verification (CRITICAL)

Every Shopify webhook MUST be verified with HMAC-SHA256 using the RAW request body:

```javascript
const crypto = require('crypto');
const expectedHmac = crypto
  .createHmac('sha256', process.env.SHOPIFY_WEBHOOK_SECRET.trim())
  .update(req.rawBody, 'utf8') // rawBody, NOT req.body
  .digest('base64');

const valid = crypto.timingSafeEqual(
  Buffer.from(expectedHmac),
  Buffer.from(req.headers['x-shopify-hmac-sha256'])
);
```

**Three critical details**:
1. Use `req.rawBody` (the unparsed string), NOT `req.body` (parsed JSON) — parsing changes whitespace and key order
2. Use `crypto.timingSafeEqual()` for constant-time comparison — prevents timing attacks
3. `.trim()` the webhook secret — trailing whitespace from env vars breaks HMAC

The raw body is preserved via Express verify callback in the body parser configuration.

## Webhook Idempotency

Shopify retries webhooks that don't get a 200 response. Duplicate processing causes duplicate REX operations.

```javascript
// Store webhook event with dedup
const { rows } = await pool.query(`
  INSERT INTO shopify_webhook_events (webhook_id, topic, shop, payload)
  VALUES ($1, $2, $3, $4)
  ON CONFLICT (webhook_id) DO NOTHING
  RETURNING id
`, [req.headers['x-shopify-webhook-id'], topic, shop, payload]);

if (rows.length === 0) {
  return res.json({ received: true, duplicate: true }); // Already processed
}
```

Always return 200 to Shopify even for duplicates — otherwise Shopify keeps retrying.

## REST vs GraphQL: When to Use Each

| Operation | API | Why |
|-----------|-----|-----|
| Single product CRUD | REST | Simpler, well-documented |
| Bulk inventory adjustment | GraphQL `inventorySetQuantities` | Single call for multi-location |
| Full product creation with variants | GraphQL `productSet` | Handles variants, pricing, metafields in one call |
| Pagination over products/orders | REST with cursor | Link header pagination is reliable |
| Sales channel publishing | GraphQL `getPublications` | REST doesn't expose this |
| Customer CRUD | REST | Simpler, well-documented |
| Order transactions | REST `/orders/{id}/transactions.json` | NOT included in order webhooks |

**Key gotcha**: Order webhook payloads do NOT include transaction details. You must fetch transactions separately via the REST API.

## Pagination Patterns

### REST API (Link Header Cursor)

```javascript
let cursor = null;
do {
  const params = cursor
    ? { page_info: cursor }  // Subsequent pages: ONLY page_info
    : { limit: 250, status: 'active', fields: 'id,title,...' }; // First page: filters + limit

  const response = await this.client.get('/products.json', { params });
  products.push(...response.data.products);

  // Extract cursor from Link header
  const linkHeader = response.headers.link;
  const nextMatch = linkHeader?.match(/<[^>]*page_info=([^>]+)>;\s*rel="next"/);
  cursor = nextMatch ? nextMatch[1] : null;
} while (cursor);
```

**Critical**: On subsequent pages, send ONLY `page_info` — sending other params alongside it causes Shopify to ignore the cursor.

### GraphQL (endCursor)

```javascript
let hasNextPage = true, cursor = null;
while (hasNextPage) {
  const data = await shopifyClient.graphql(query, { cursor });
  items.push(...data.products.edges.map(e => e.node));
  hasNextPage = data.products.pageInfo.hasNextPage;
  cursor = data.products.pageInfo.endCursor;
}
```

## 429 Rate Limit Handling

Built into `shopifyClient.js` via axios interceptor:

```javascript
// Automatic retry: up to 3 attempts
// Respects Shopify's retry-after header (in seconds)
// Fallback: _retryCount * 2 seconds if no header
```

Don't add your own retry logic on top — it will compound with the built-in interceptor.

## Inventory Sync Pipeline

Four-layer architecture (REX is source of truth):

1. **REX → Cortex**: Background sync every 15 min → `inventory` table
2. **Cortex → Shopify**: `enqueuePush()` → `rex_sync_queue` → worker → `POST /inventory_levels/set.json`
3. **Webhook Loop**: Echo detection (90s window), override revert, circuit breaker (5 reverts/10min)
4. **Daily Reconciliation**: 3:30 AM, max 200 corrections

Feature flags control each layer independently (see sync-worker skill).

## Payment Ledger (Atomic Dedup)

For payment sync to REX, the ledger prevents duplicate financial operations:

```javascript
// Step 1: Atomic claim
const claimed = await ledger.recordOutboundPayment({
  orderId, shopifyOrderId, shopifyTransactionId, shopifyKind, amount
});
if (!claimed) return; // Already claimed by another handler

// Step 2: Sync to REX
await rexClient.addPayment(rexOrderId, amount, methodId);

// Step 3: Mark synced
await ledger.markSynced(String(transactionId));
```

On failure: the queue worker retries, but the ledger ensures only one successful sync.

## Fulfillment State Machine

Fulfillment webhooks have a guard: only `status === 'success'` updates line items and triggers REX sync.

```
unfulfilled → partial (some items fulfilled) → fulfilled (all items)
```

Non-success fulfillments (pending, cancelled, error) are recorded but do NOT update line items or trigger REX sync.

**SKU matching**: Match Shopify `line_items` by SKU to determine which items were fulfilled. Fallback to "fulfill all unfulfilled" only for legacy/reconciliation (no line_items available).

## Bundle Expansion

Orders may contain Shopify bundles that need expansion to individual REX products:

- **Primary metafield**: `custom.bundle_products` (Shopify `list.product_reference` type)
- **Legacy metafield**: `bundly.bundle` (Bundly app format)
- **Price distribution**: Proportional (by individual price) or equal
- **Config**: `apps/api/src/config/shopifySync.js` (74 lines)

Always check for bundle expansion before creating REX order items.

## SKU Override System

For products that don't map 1:1 between Shopify and REX:

- **Table**: `shopify_sku_overrides`
- **Actions**: `SKIP` (ignore line item) or `MAP_TO_PRODUCT` (remap to different product)
- **Use case**: Service fees, gift wrapping, other non-inventory items

Lookup order: direct ID match → barcode match → SKU override → mark as problem.

## API Chunking Limits

| Operation | Max per Request | Pagination |
|-----------|----------------|------------|
| Products REST | 250 | Link header cursor |
| Customers REST | 250 | Link header cursor |
| Inventory levels | 50 item IDs | Chunked loop |
| GraphQL products | 100 | endCursor |
| GraphQL mutations | 1 operation | N/A |

## Common Mistakes

| Mistake | Why It Happens | Prevention |
|---------|---------------|------------|
| Using `req.body` for HMAC verification | Seems equivalent to rawBody | Must use `req.rawBody` — parsing changes the string |
| Not returning 200 for duplicate webhooks | Want to signal "already processed" | Always return 200 — non-200 causes Shopify retries |
| Adding retry logic around shopifyClient calls | Want resilience | Built-in 429 interceptor handles it — don't double-retry |
| Sending filters with `page_info` on subsequent pages | Copy-paste from first request | Subsequent pages: ONLY `page_info` parameter |
| Fetching transactions from order webhook payload | Expects they're included | Must call `/orders/{id}/transactions.json` separately |
| Not checking bundle expansion before REX sync | Bundles look like regular orders | Always check `custom.bundle_products` metafield |
| Using REST for bulk inventory updates | REST works for single items | GraphQL `inventorySetQuantities` for multi-location |
| Assuming `shopify_orders.rex_sync_status` is accurate | Field exists on table | Known bug: all 34K dev orders show 'pending' — don't rely on this field |

---
name: integration-guard
description: Use when writing or modifying code that interacts with REX (Retail Express), Shopify, or any external integration/sync system. Triggers on work involving SOAP calls, REX API, Shopify API, inventory sync, order sync, product sync, fulfillment sync, or any code in services/retailExpress/, services/shopify*, or queue workers. Use before writing any integration code to avoid known pitfalls.
---

# Integration Guard

## Overview

A pre-code checklist and reference for external integration work. REX and Shopify integrations have accumulated many gotchas from production incidents. This skill codifies those lessons so you don't repeat them.

## When to Use

- Before writing ANY code that touches REX or Shopify APIs
- Before modifying sync workers or queue processors
- When debugging integration failures
- When adding new sync flows

## Specialized Skills (invoke for deeper guidance)

For detailed domain knowledge, invoke the specialized skill FIRST:

| Domain | Skill | When |
|--------|-------|------|
| REX SOAP API | `/rex-soap-protocol` | Any SOAP envelope, REX API call, fulfillment sync, error handling |
| Queue/sync workers | `/sync-worker` | Any queue worker, retry logic, checkpoint, echo detection, backoff |
| Shopify API/webhooks | `/shopify-integration` | Any webhook handler, API call, pagination, inventory push |

This integration-guard provides a general checklist. The specialized skills above provide the deep patterns.

## Pre-Code Checklist

Run through ALL of these before writing integration code:

### 1. Data Type Safety

- [ ] **REX order IDs are bigints** — Always cast to `BigInt()` or use string comparison. JavaScript `Number` loses precision above 2^53.
  ```javascript
  // BAD
  if (rexOrderId === localId) // fails for large IDs

  // GOOD
  if (String(rexOrderId) === String(localId))
  ```

- [ ] **suppliers.id is UUID, products.supplier_id is integer** — Cast to text for joins:
  ```sql
  JOIN suppliers ON suppliers.id::text = products.supplier_id::text
  ```

- [ ] **REX SKU field mapping** (recall: `search_vault(query="REX SKU field mapping")`):
  - `supplier_sku` → maps to our `sku`
  - `supplier_sku2` → maps to our `sku2`
  - Top-level `sku` in REX response is usually NULL — don't use it

### 2. SOAP Protocol (invoke `/rex-soap-protocol` for full details)

- [ ] **Protocol depends on endpoint URL** — `.svc` = SOAP 1.2 + WS-Addressing, `.asmx` = SOAP 1.1 + SOAPAction header
- [ ] **XML-escape ALL interpolated values** — `& < > " '` silently break envelopes
- [ ] **Use string template envelopes, NOT xml2js** — match existing patterns in rexWebStoreClient.js
- [ ] **Check `isAlreadyPaidError()`** — "overpaid", "Balance: 0" are success, not errors

### 3. Multi-Tenant Safety

- [ ] **Every INSERT has `tenant_id`**
- [ ] **Every SELECT/UPDATE/DELETE scopes to tenant**
- [ ] **Queue items carry tenant context** — don't assume single tenant

### 4. Queue & Sync Patterns (invoke `/sync-worker` for full details)

- [ ] **Atomic queue claim** — `FOR UPDATE SKIP LOCKED` (never SELECT then UPDATE)
- [ ] **Canonical backoff** — `BACKOFF_SECONDS = [60, 300, 1800, 7200, 43200]` from rexSyncQueueUtils.js
- [ ] **syncInProgress guard with try/finally** — `finally` block is MANDATORY
- [ ] **Checkpoint staleness guard** — cap lookback to 4 hours max (prevents quota death spiral)
- [ ] **Echo detection on inventory push** — 90-second window via `shopify_inventory_push_log`

### 5. Inventory Specifics

- [ ] **No negative quantity clamping** — REX and Shopify support negatives. Don't use `Math.max(0, qty)` or `GREATEST(0, qty)`.
- [ ] **Three-way sync alignment** — DB, REX, and Shopify must all reflect the same value.
- [ ] **GENERATED columns** — Never write to columns marked GENERATED in PostgreSQL.

### 6. Order Specifics

- [ ] **rex_incomplete SOAP call** — Wrap in try/catch, it fails silently on cancelled POs
- [ ] **Order source tracking** — use `order_source` column consistently
- [ ] **Fulfillment status** — reconcile between REX shipment status and Shopify fulfillment

### 7. PO (Purchase Order) Specifics

- [ ] **REX PO finalization** (recall: `search_vault(query="REX PO finalization")`) — Cannot un-finalize a PO in REX
- [ ] **Draft status** — Check if PO is draft before attempting operations
- [ ] **Email fallback** — If REX submission fails, fall back to email with `forceSend` option

## Environment Reference

- **REX environment**: `testhuntthenight.retailexpress.com.au` is LIVE — treat as production
- **Shopify**: Check `.env` for store URL and API keys
- **Sync checkpoint**: Don't create death spirals — `shouldAdvance` requires `entitiesSynced > 0`

## Quick Reference: File Locations

| Component | Path |
|-----------|------|
| REX sync services | `apps/api/src/services/retailExpress/` |
| Shopify services | `apps/api/src/services/shopify*/` |
| Queue workers | `apps/api/src/workers/` |
| Sync checkpoints | `apps/api/src/services/syncCheckpoint*` |
| Inventory sync | `apps/api/src/services/inventory*/` |

## Common Mistakes From Production

| Incident | Root Cause | Prevention |
|----------|-----------|------------|
| Order sync losing IDs | BigInt precision loss | Cast to String |
| Silent SOAP failures | SOAP 1.2 used instead of 1.1 | Always SOAP 1.1 |
| Inventory wrong on Shopify | Math.max(0, qty) clamping | Never clamp negatives |
| Queue items stuck forever | No stale lock recovery | 5-min lock timeout sweep |
| Products not linking | Wrong SKU field used | supplier_sku → sku mapping |
| Sync checkpoint spiral | shouldAdvance with 0 entities | Require entitiesSynced > 0 |
| PO submission 500 error | No try/catch on rex_incomplete | Always wrap SOAP calls |

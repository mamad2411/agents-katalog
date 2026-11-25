---
name: rex-soap-protocol
description: REX (Retail Express) SOAP API protocol guide. Use this skill before writing or modifying any SOAP envelope, REX API call, REX webhook handler, or code that communicates with REX endpoints. Covers dual SOAP protocol detection (1.1 vs 1.2), three-endpoint architecture (WebStore, Ecommerce, WMS), envelope construction, authentication, response handling (Base64-gzipped XML), and REX-specific error messages that mean success. Invoke this even for "simple REX API calls" — the protocol version selection and error handling are where bugs hide.
---

# REX SOAP Protocol

REX uses three separate API endpoints with two different SOAP protocol versions. Getting the protocol wrong produces cryptic XML errors. Getting the error handling wrong causes retry storms on already-successful operations.

## TOP GOTCHAS (read these FIRST)

1. **"Overpaid" means SUCCESS** — REX returns "overpaid", "Balance: 0", "NullReferenceException GetOutletId" when a payment/cancel already succeeded. These are NOT errors. Retrying them causes retry storms. **Always use `isAlreadyPaidError()`** from `rexSyncQueueWorker.js`.
2. **Fulfillment requires THREE steps, not one** — `GetOrder` (Ecommerce SOAP 1.2) → `FulfillOrders` (WMS SOAP 1.1) → `OrderDeliveryUpdate` (WebStore). Only calling step 3 adds tracking but doesn't mark fulfilled in REX inventory. FulfillOrders items **MUST be wrapped in `<list>` tag** or REX throws null reference.
3. **SOAP protocol mismatch = cryptic XML error** — URL with `.svc` or `api.retailexpress.com.au` = SOAP 1.2 + WS-Addressing. URL with `.asmx` = SOAP 1.1 + SOAPAction header. Wrong protocol → generic parse failure with no hint about the real cause.
4. **XML escape ALL interpolated values** — `& < > " '` in any SOAP field silently breaks the envelope. REX returns a generic parse error with no indication which field caused it.
5. **Use string template envelopes, NOT xml2js** — All existing SOAP code uses template literals. Follow that pattern.

## Before Writing Any REX API Code

1. **Identify which endpoint you need** — WebStore, Ecommerce, or WMS (see Endpoint Map below)
2. **Explore the existing client file** for that endpoint — patterns are established and must be followed:
   - `get_file_outline([client-file])` to see all methods without reading the full 1107-line file
   - `get_symbol([client-file], [method-name])` to pull only the specific method you need
   - Use `search_symbols(query="[method]", kind="function")` if unsure which file contains it
   - Only use Read for full-file context or before editing
3. **Check the SOAP version** — ASMX = SOAP 1.1, WCF (.svc) = SOAP 1.2 + WS-Addressing

## The Three REX Endpoints

| Endpoint | Protocol | URL Pattern | Client File | Use For |
|----------|----------|-------------|-------------|---------|
| WebStore | SOAP 1.1 (ASMX) or 1.2 (WCF) | `v2wsisandbox...Service.asmx` or `ecommerce.svc` | `rexWebStoreClient.js` (1107 lines) | Order create/cancel, payment, delivery update, customer upsert, voucher balance, product details |
| Ecommerce | SOAP 1.2 + WS-Addressing | `api.retailexpress.com.au/ecommerce` | `rexWebStoreClient.js` (shared) | Order lookup (GetOrder for fulfillment) |
| WMS | SOAP 1.1 (ASMX) | `REX_WMS_URL` env var (separate host) | `rexFulfillmentBatcher.js` | FulfillOrders (batch), stock adjustments |
| Inventory Planning | SOAP 1.1 | Tenant-specific URL | `rexInventoryPlanningClient.js` (377 lines) | CreateStockAdjustments, GetOutlets, GetStock, CreateUpdatePurchaseOrders |
| REST API | HTTP/JSON | `v2/auth/token` → Bearer token | `services/retailExpress/index.js` (257 lines) | Product CRUD, supplier lookup, customer sync |

## SOAP Protocol Detection

The WebStore client auto-detects protocol based on endpoint URL:

```javascript
// WCF endpoints (production) → SOAP 1.2 + WS-Addressing
if (url.includes('ecommerce.svc') || url.includes('api.retailexpress.com.au')) {
  // Content-Type: application/soap+xml; charset=utf-8
  // Must include WS-Addressing headers: <wsa:Action>, <wsa:To>
}

// ASMX endpoints (sandbox, WMS) → SOAP 1.1
else {
  // Content-Type: text/xml; charset=utf-8
  // SOAPAction HTTP header required
}
```

**The #1 mistake**: Using SOAP 1.1 headers against a WCF endpoint (or vice versa). The error is a generic XML parse failure that doesn't mention the protocol mismatch.

## SOAP Envelope Construction

All REX SOAP envelopes are built with string templates (NOT xml2js). Follow the existing patterns exactly.

### Authentication Header (all SOAP calls)

```xml
<ClientHeader xmlns="http://retailexpress.com.au/">
  <ClientID>{clientId}</ClientID>
  <UserName>{username}</UserName>
  <Password>{password}</Password>
</ClientHeader>
```

This goes in `<soap:Header>`. Credentials come from `REX_CLIENT_ID`, `REX_USERNAME`, `REX_PASSWORD` env vars.

### XML Escaping (MANDATORY)

Every user-supplied value in a SOAP payload MUST be XML-escaped. The characters `& < > " '` will break the envelope silently — REX returns a generic parse error with no indication of which field caused it.

```javascript
function escapeXml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
```

### Response Handling

**Inventory Planning responses are Base64-gzipped XML**. The client must:
1. Extract the Base64 string from the SOAP response
2. Decode from Base64 to Buffer
3. Gunzip the buffer
4. Parse the resulting XML

Standard WebStore responses are plain XML — no decompression needed.

## REST API Token Management

The REST API (`services/retailExpress/index.js`) uses a cached token with single-flight pattern:

- Token endpoint: `POST /v2/auth/token` with `x-api-key` header
- Token expiry: 60 minutes (cached with 5-minute safety buffer)
- Single-flight: `_restTokenPromise` prevents thundering herd on expiry
- Subsequent requests: `Bearer {token}` + `x-api-key` headers

Never create a second token fetch mechanism — use the existing `getRestToken()` method.

## REX Error Messages That Mean "Success"

These error messages from REX indicate the operation already succeeded. Treating them as failures causes retry storms:

| Error Message | Meaning | Correct Action |
|--------------|---------|----------------|
| `"overpaid"` | Payment already applied to order | Mark as success |
| `"Balance: 0"` | Order already fully paid | Mark as success |
| `"NullReferenceException GetOutletId"` | Order already fully paid (REX bug) | Mark as success |
| Terminal statuses: `void`, `voided`, `cancelled`, `refunded` | Order already in terminal state | Mark cancel as success |

The `rexSyncQueueWorker.js` has the canonical `isAlreadyPaidError()` check — always use it.

## Three-Step Fulfillment Flow (CRITICAL)

Fulfilling an order in REX requires THREE separate API calls to TWO different endpoints. Missing any step leaves the order in a broken state.

1. **GetOrder** (Ecommerce API, SOAP 1.2) → fetch `OrderItemIds` for the order
2. **FulfillOrders** (WMS API, SOAP 1.1) → mark items as fulfilled. Items MUST be wrapped in `<list>` tag or REX throws null reference
3. **OrderDeliveryUpdate** (WebStore API, SOAP 1.1) → add tracking number and carrier info

**Common mistake**: Only calling `OrderDeliveryUpdate` = tracking appears but order never marked fulfilled in REX inventory system.

## Rate Limits

| Endpoint | Limit | Enforcement |
|----------|-------|-------------|
| WMS FulfillOrders | 1 call per 5 minutes | REX-enforced, returns error |
| Inventory Planning | 1 call per 5 minutes | REX-enforced, returns error |
| REST API | Daily (10K) + Hourly (1K) quota | Tracked in `rex_quota_usage` table |
| REST API 429 | Exponential backoff, max 10 retries | `rexApi.js` adaptive delay (200-5000ms) |

## Common Mistakes

| Mistake | Why It Happens | Prevention |
|---------|---------------|------------|
| Using SOAP 1.1 against WCF endpoint | Not checking URL pattern | Check endpoint URL for `.svc` → use SOAP 1.2 |
| Missing XML escaping in SOAP fields | Looks fine with test data | Always use `escapeXml()` on every interpolated value |
| Only calling OrderDeliveryUpdate for fulfillment | Seems like the obvious API | Must do all 3 steps: GetOrder → FulfillOrders → OrderDeliveryUpdate |
| Not wrapping FulfillOrders items in `<list>` tag | Undocumented REX requirement | Copy the exact XML structure from `rexFulfillmentBatcher.js` |
| Retrying "overpaid" payments | Looks like an error | Check `isAlreadyPaidError()` patterns first |
| Creating new REST token fetch logic | Don't know about existing cache | Use `getRestToken()` from `services/retailExpress/index.js` |
| Using REX `sku` field for product lookup | Field name is misleading | Use `supplier_sku` — REX `sku` is usually NULL (see sql-guard skill) |
| Assuming WMS URL = WebStore URL | Both are REX | WMS is a separate host — check `REX_WMS_URL` env var |

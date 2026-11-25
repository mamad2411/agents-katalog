---
name: next-bulk-fulfill
version: 1.0.0
description: |
  Bulk fulfillment tracking sync — update orders to Fulfilled status with tracking
  numbers from a CSV when the fulfillment provider's automation fails to sync back.

  Walks through store identification, API key validation, CSV ingestion, carrier
  detection, dry-run validation, live execution with customer notifications, and
  results reporting.

  Use when: "bulk fulfill", "sync tracking numbers", "tracking sync", "fulfill orders
  from CSV", "orders stuck in processing", "tracking numbers didn't sync", or when a
  merchant reports shipped orders still showing as Processing.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - TodoWrite
---

# /next-bulk-fulfill: Bulk Fulfillment Tracking Sync (v1)

## Using This Skill

This skill works with any AI coding tool that can load a markdown file as context.

| Tool | How to Use |
|------|-----------|
| **Recommended** | Clone `NextCommerceCo/skills` and run `./skills.sh`; choose your local agent target and this skill. |
| **No checkout** | Use `npx skills add NextCommerceCo/skills -g --skill next-bulk-fulfill` and add `-a <agent>` when you want a specific agent. |
| **Fallback** | Load this `SKILL.md` as a system prompt, context file, rule, or chat upload if your tool does not support native skills. |

---

Updates orders stuck in Processing (or Open) status with tracking numbers from a CSV,
triggering fulfillment completion and customer shipping notifications.

**When this happens:** A fulfillment provider ships orders but fails to POST tracking
numbers back to Next Commerce. Orders get stuck in "Processing" status. The merchant
provides a CSV of order numbers + tracking numbers, and this skill handles the bulk update.

---

## Phase 1: Gather Requirements

Collect the three required inputs in order. Do NOT proceed to the next input until the
current one is confirmed.

## Admin API Conventions

Before making any store request, use the public Admin API conventions from
https://developers.nextcommerce.com/docs/admin-api:

- Base URL: `https://{subdomain}.29next.store/api/admin/`
- Auth header: `Authorization: Bearer <api access token>`
- Version header: `X-29next-API-Version: 2024-04-01`

Do not use `/api/v1/...` paths or `Authorization: Token ...`; those are not the
documented NEXT Admin API convention and commonly return storefront HTML 404
pages instead of JSON.

### Step 1: Store Subdomain

Ask the user:

> Which store needs fulfillment sync? Provide the subdomain (e.g., `mystore` for mystore.29next.store).

Validate the store exists:
```bash
curl -s -o /dev/null -w "%{http_code}" https://{subdomain}.29next.store/
```

If the store returns a non-200 status, warn the user and ask them to confirm the subdomain.

Store the base URL: `https://{subdomain}.29next.store/api/admin/`

### Step 2: Admin API Access Token

Ask the user:

> Provide an Admin API access token for {subdomain}.29next.store.
>
> The key needs these **two scopes** (and no more):
> - `fulfillment_orders:read` — to query fulfillment orders by order number
> - `fulfillment_orders:write` — to create fulfillments with tracking info
>
> Create one at **{subdomain}.29next.store Dashboard > Settings > API Access**.

Validate the key works:
```bash
curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer {api_access_token}" \
  -H "X-29next-API-Version: 2024-04-01" \
  "https://{subdomain}.29next.store/api/admin/fulfillment-orders/?limit=1"
```

- `200` = key works, proceed
- `401` / `403` = bad key or missing scopes, ask user to check
- `404` with `<!DOCTYPE html>` or "Page not found" = wrong URL convention;
  re-check `/api/admin/`, `Authorization: Bearer ...`, and the store domain

### Step 3: CSV File

Ask the user:

> Provide the path to the CSV file with order numbers and tracking numbers.
>
> Expected columns (header names are flexible — I'll detect them):
> - **Order number** (e.g., `ORDER NUMBER`, `order_number`, `Order #`)
> - **Tracking number** (e.g., `TRACKING NUMBER`, `tracking_no`, `Tracking #`)
>
> Optional: Order name / customer name column (used for logging only).

Read the CSV and detect columns. Look for headers matching these patterns:
- Order number: contains `order` AND (`number` or `#` or `num` or `id`)
- Tracking number: contains `tracking` AND (`number` or `#` or `num` or `code`)
- Customer name: contains `name` or `customer` (optional, for logging)

If column detection fails, show the headers found and ask the user to specify which
columns to use.

Report what was loaded:
> Loaded **{N}** orders from `{filename}`. Detected columns:
> - Order number: `{column_name}`
> - Tracking number: `{column_name}`
> - Customer name: `{column_name}` (or "not detected")

---

## Phase 2: Carrier Detection

Detect the shipping carrier from tracking number prefixes. Use this mapping:

| Tracking Pattern | Carrier Slug | Carrier Name |
|-----------------|-------------|-------------|
| Starts with `YT` | `yunexpress` | Yunexpress |
| Starts with `4PX` | `4px` | 4PX |
| Starts with `92`, length >= 20 | `usps` | USPS |
| Starts with `1Z` | `ups` | UPS |
| 12-15 digits, no letter prefix | `fedex` | FedEx |
| Starts with `JD` or 10 digits starting with `0` | `dhl` | DHL |
| None of the above | `other` | Other |

**Valid carrier slugs** (from the API schema): `4px`, `amazon`, `asendia`, `australia_post`,
`china_post`, `deutsche_de`, `dhl`, `dhl_ecommerce`, `fedex`, `firstmile`, `gofo_express`,
`hermesworld_uk`, `myhermes`, `ontrac`, `other`, `royal_mail`, `speedx`, `swiss_post`,
`ulala`, `uniuni`, `ups`, `usps`, `yunexpress`

After detection, show a carrier summary:
> **Carrier detection:**
> - usps: 145 orders
> - yunexpress: 4 orders
> - other: 1 order
>
> Orders with carrier `other` will still sync — the platform won't auto-link to a
> carrier tracking page but the tracking number will be stored.

If multiple carriers are detected, confirm with the user before proceeding.

---

## Phase 3: Write and Run the Sync Script

Generate a Python script at `{working_dir}/{subdomain}_bulk_fulfill.py` that implements
the two-step API flow.

### The API Pattern

**Step 1 — Find the fulfillable order:**
```
GET /api/admin/fulfillment-orders/?order_number={number}&status=processing
```
If no results, retry with `status=open` (unfulfilled orders).

Returns paginated results. Use `results[0]["id"]` as the fulfillment order ID.

**Step 2 — Create the fulfillment with tracking:**
```
POST /api/admin/fulfillment-orders/{id}/fulfillments/
{
  "tracking_info": [{"tracking_code": "{tracking_number}", "carrier": "{carrier_slug}"}],
  "notify": true
}
```

### Script Requirements

- **Rate limiting**: 4 requests/sec max. At 2 calls per order, sleep 0.6s between orders.
- **Auth headers**: `Authorization: Bearer {api_access_token}` + `X-29next-API-Version: 2024-04-01`
- **Dry-run mode**: `--dry-run` flag that runs Step 1 (GET) but skips Step 2 (POST)
- **Notify control**: `--no-notify` flag to suppress customer notifications
- **Limit flag**: `--limit N` to process only the first N orders (for testing)
- **Output**: Write results to `{subdomain}_bulk_fulfill_results.csv` with columns:
  `order_number, customer_name, tracking_no, carrier, status, fo_id, note`
- **Status values**: `OK`, `NOT_FOUND`, `MULTIPLE_FOUND`, `API_ERROR`, `DRY_RUN_OK`
- **Use `python3 -u`** for unbuffered output (real-time progress)
- **Only import stdlib + requests** (no pandas, no openpyxl)

### Gotchas (encode these in the script)

- The request body field is `carrier`, NOT `tracking_carrier`. The response uses
  `tracking_carrier` which is confusing — but the request must use `carrier`.
- Success returns HTTP **200**, not 201 (despite being a POST). Accept both.
- `NOT_FOUND` (0 results from GET) = order already fulfilled or canceled. Expected, not an error.
- Multiple fulfillment orders per order = items from different warehouse locations.
  Skip and flag for manual review — don't guess which FO to fulfill.

### Execution Flow

**3a. Run dry-run first:**
```bash
python3 -u {subdomain}_bulk_fulfill.py --dry-run
```

Report results to the user:
> **Dry-run results:**
> - DRY_RUN_OK: {N} (ready to fulfill)
> - NOT_FOUND: {N} (already fulfilled/canceled)
> - MULTIPLE_FOUND: {N} (needs manual review)
> - API_ERROR: {N}

If NOT_FOUND or MULTIPLE_FOUND counts are unexpectedly high, discuss with the user
before proceeding.

**3b. Confirm and run live:**

Ask the user:
> Ready to fulfill **{N}** orders with customer notifications enabled. Proceed?
>
> - A) Yes, run it (notifications ON)
> - B) Yes, but suppress notifications (--no-notify)
> - C) No, let me review first

Then run:
```bash
python3 -u {subdomain}_bulk_fulfill.py        # Option A
python3 -u {subdomain}_bulk_fulfill.py --no-notify  # Option B
```

---

## Phase 4: Results & Follow-up

### Report Results

Show the final summary:
> **Fulfillment sync complete:**
> - **OK**: {N} orders fulfilled with tracking
> - **NOT_FOUND**: {N} (already fulfilled or canceled — expected)
> - **MULTIPLE_FOUND**: {N} (manual review needed)
> - **API_ERROR**: {N}
>
> Results saved to: `{results_csv_path}`

### Flag Manual Review Items

For any MULTIPLE_FOUND orders, provide the order numbers and FO IDs so the user can
resolve them in the store admin:
> **Orders needing manual review:**
> - Order {number} ({customer_name}): FO IDs {id1}, {id2} — has multiple fulfillment
>   orders, needs manual fulfillment in the admin dashboard

For any API_ERROR orders, show the error details from the results CSV.

### Clean Up

After confirming results are satisfactory, offer to clean up the generated script:
> Script saved at `{script_path}`. Want me to keep it for future use or delete it?

---

## Reference: API Endpoints

| Operation | Method | Endpoint | Scopes |
|-----------|--------|----------|--------|
| List fulfillment orders | GET | `/api/admin/fulfillment-orders/` | `fulfillment_orders:read` |
| Create fulfillment | POST | `/api/admin/fulfillment-orders/{id}/fulfillments/` | `fulfillment_orders:write` |

**API version**: `2024-04-01`

**Docs**: [Fulfillment Service Guide](https://developers.nextcommerce.com/docs/apps/guides/fulfillment-service#creating-fulfillments)

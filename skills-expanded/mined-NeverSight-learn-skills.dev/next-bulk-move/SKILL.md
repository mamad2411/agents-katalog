---
name: next-bulk-move
version: 1.3.0
description: |
  Move fulfillment orders between locations in bulk. Accepts either a flat file
  (XLSX/CSV) of order numbers, or a list of Product IDs / SKUs to target every
  FO containing those items. Moves all matching fulfillment order line items
  from one location to another.

  Handles the full workflow: location discovery, status checks, cancellation
  requests for processing FOs, move execution, and results reporting.

  Use when: "bulk move orders", "move fulfillment orders", "transfer orders
  to new warehouse", "change fulfillment location", "move all FOs for SKU X",
  or when a flat file of order numbers or a product/SKU list needs location
  reassignment.
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

# /next-bulk-move: Bulk Fulfillment Order Location Move

## Using This Skill

This skill works with any AI coding tool that can load a markdown file as context.

| Tool | How to Use |
|------|-----------|
| **Recommended** | Clone `NextCommerceCo/skills` and run `./skills.sh`; choose your local agent target and this skill. |
| **No checkout** | Use `npx skills add NextCommerceCo/skills -g --skill next-bulk-move` and add `-a <agent>` when you want a specific agent. |
| **Fallback** | Load this `SKILL.md` as a system prompt, context file, rule, or chat upload if your tool does not support native skills. |

---

Moves fulfillment orders between warehouse locations in bulk using a flat file of order numbers.

**When this happens:** A merchant is switching fulfillment providers (e.g., Provider A → Provider B) and has a batch of open/processing orders that need to be reassigned to the new location before the new provider can begin fulfilling them.

---

## The Three-Layer Model

- **Order** — the customer purchase (`/orders/{number}/`)
- **Fulfillment Order (FO)** — items grouped by fulfillment location within an order. One order can have multiple FOs. Statuses: `open`, `processing`, `closed`, `canceled`, etc.
- **Fulfillment** — the shipment record attached to a FO (tracking info). Not relevant to moves.

---

## Phase 1: Setup

## Admin API Conventions

Before making any store request, use the public Admin API conventions from
https://developers.nextcommerce.com/docs/admin-api:

- Base URL: `https://{subdomain}.29next.store/api/admin/`
- Auth header: `Authorization: Bearer $NEXT_ADMIN_API_TOKEN`
- Version header: `X-29next-API-Version: 2024-04-01`

Do not use `/api/v1/...` paths or `Authorization: Token ...`; those are not the
documented NEXT Admin API convention and commonly return storefront HTML 404
pages instead of JSON.

### Step 1: Store Configuration

Ask the user (if not already provided):

> "What is the store subdomain? (e.g., `examplestore` for examplestore.29next.store)"

Set:
```
STORE=https://{subdomain}.29next.store
```

The executor accepts only a bare subdomain or a hostname ending in
`.29next.store` by default. For a store intentionally configured on a custom
admin domain, pass `--allow-host` with the custom `--store` hostname. This is an
explicit, operator-confirmed trust override: `--allow-host` requires the exact
normalized hostname as its value (for example, `--store admin.example.com
--allow-host admin.example.com`). The executor refuses a mismatch and prints a
prominent warning because it will send `NEXT_ADMIN_API_TOKEN` to that host.

### Step 2: Admin API Access Token

The executor reads the token only from `NEXT_ADMIN_API_TOKEN`. Scopes:
`fulfillment_orders:read`, `fulfillment_orders:write`, and `locations:read`.
The token never enters conversation, CLI arguments, echoes, scripts, or
results files.

If the store's variable (naming below) or `NEXT_ADMIN_API_TOKEN` is already in
the environment, use it. Otherwise tokens live in `.env` in the current
working directory (the user's project, not the skill checkout) — one line per
store, named `{SUBDOMAIN}_NEXT_ADMIN_API_TOKEN` (caps, hyphens → underscores;
`my-store` → `MY_STORE_NEXT_ADMIN_API_TOKEN`). The user pastes the token in
with a text editor, so it never touches the chat.

1. If this directory is a git repository (a `.git` folder is present), make
   sure `.gitignore` has a `.env` line — add it if missing.
2. Create the file (or append the store's line), then lock it so only this
   user can read it (`chmod 600 .env`):

   ```
   # Next Commerce Admin API tokens — one line per store.
   MYSTORE_NEXT_ADMIN_API_TOKEN=
   ```

3. If the value is empty: have the user open `.env` in a text editor (offer to
   open it — the file is hidden in file managers), paste the token after `=`,
   save, and reply "saved".
4. Load only that line — never `source` the file (it executes content and
   exports unrelated secrets) — in the same command as the validation curl or
   executor run, since shell state may not persist between tool commands:

   ```bash
   NEXT_ADMIN_API_TOKEN="$(grep -m1 '^MYSTORE_NEXT_ADMIN_API_TOKEN=' .env | cut -d'=' -f2-)"
   [ -n "$NEXT_ADMIN_API_TOKEN" ] || { echo "no token for mystore in .env" >&2; exit 1; }
   export NEXT_ADMIN_API_TOKEN
   ```

Validate the token against a known-good list endpoint before discovery:

```bash
curl -sS -w "\n%{http_code}" \
  -H "Authorization: Bearer ${NEXT_ADMIN_API_TOKEN:?NEXT_ADMIN_API_TOKEN is required}" \
  -H "X-29next-API-Version: 2024-04-01" \
  "{STORE}/api/admin/fulfillment-orders/?limit=1"
```

- `200` = token works, proceed
- `401` / `403` = bad token or missing scopes, ask user to check
- `404` with `<!DOCTYPE html>` or "Page not found" = wrong URL convention;
  re-check `/api/admin/`, `Authorization: Bearer ...`, and the store domain

### Step 3: Discover Locations

**Primary method** — list all locations:
```
GET {STORE}/api/admin/locations/
```

**Fallback** — if `/locations/` returns empty (scope or config issue), discover locations from existing fulfillment orders:
```
GET {STORE}/api/admin/fulfillment-orders/?status=open
```
Extract unique `assigned_location.id` and `assigned_location.name` values from the results. Paginate if needed.

Display the results as a table:

```
ID    | Name
------|------------------
1     | Store Location
10    | Provider A
20    | Provider B
```

Ask the user to confirm source and destination:

> "Which location are you moving FROM (source)? And which location are you moving TO (destination)?"

Store as `SOURCE_LOCATION_ID` and `DEST_LOCATION_ID`.

### Step 4: Ingest Targets

Two supported input modes. Pick based on what the user provides.

**Mode A — Order number file (XLSX/CSV).** Minimum required column: **Order Number**.

The bundled executor accepts CSV using Python's standard library. If the source
is XLSX, export it to CSV first. Preserve an `Order Number` or `order_number`
column and do not add customer names, addresses, or other PII.

Report:
> "Found **{N}** order numbers in the file."

**Mode B — Product ID / SKU list.** Use when the user wants to move every FO containing specific items (e.g., discontinued SKU, supplier change for one product) without pre-computing an order list.

Query the filter directly — the fulfillment-orders list endpoint supports `product_id` and `sku` filters:

```
GET {STORE}/api/admin/fulfillment-orders/?sku=SKU-A,SKU-B&location_id={SOURCE_LOCATION_ID}
GET {STORE}/api/admin/fulfillment-orders/?product_id=123,456&location_id={SOURCE_LOCATION_ID}
```

Filter server-side by `location_id={SOURCE_LOCATION_ID}` to avoid pulling FOs already at the destination or at unrelated locations. Paginate until exhausted. The resulting FO set becomes the targets — skip the per-order-number lookup in Phase 2 Step 1 and classify these FOs directly.

Report:
> "Found **{N}** fulfillment orders at source matching {sku/product filter}."

---

## Phase 2: Dry Run

Before executing any moves, validate every order. For each order number:

### Step 1: Lookup Fulfillment Orders

```
GET {STORE}/api/admin/fulfillment-orders/?order_number={number}
```

**Do NOT filter by status** — we need to see all FOs for the order to make correct decisions.

### Step 2: Classify Each Order

From the results, classify:

| Condition | Classification | Action |
|-----------|---------------|--------|
| No FOs found | `NOT_FOUND` | Skip — order doesn't exist or has no FOs |
| FO at source location, `status: open` | `READY` | Can move directly |
| FO at source, `status: open`, `move` not in `supported_actions` | `MOVE_UNSUPPORTED` | Record as an error and retry/manual-review — do not mark done |
| FO at source location, `status: processing` | `NEEDS_CANCEL` | Request cancellation, poll until accepted and movable, then move |
| FO already at destination location | `ALREADY_MOVED` | Skip — already at target |
| FO at source, `status: closed` | `ALREADY_FULFILLED` | Skip — already shipped |
| FO at source, `status: canceled` | `CANCELED` | Skip — already canceled |
| Multiple FOs at source location | `MULTIPLE` | Flag for manual review — unless a SKU/product filter was provided (Mode B), in which case the server-side filter already narrowed to the intended FO |
| FO exists but at neither source nor dest | `WRONG_LOCATION` | Skip — not at expected source |

**Matching logic:** Compare `assigned_location.id` against `SOURCE_LOCATION_ID` and `DEST_LOCATION_ID`.

### Step 3: Report Dry Run Results

```
Dry Run Summary
━━━━━━━━━━━━━━━
Total orders:        {N}
READY (open):        {N} — will move directly
NEEDS_CANCEL:        {N} — will cancel then move
ALREADY_MOVED:       {N} — already at destination
ALREADY_FULFILLED:   {N} — already shipped
NOT_FOUND:           {N} — no fulfillment orders
CANCELED:            {N} — already canceled
MULTIPLE:            {N} — flagged for manual review
WRONG_LOCATION:      {N} — not at source location
```

Ask:
> "Proceed with moving **{READY + NEEDS_CANCEL}** orders from **{source_name}** to **{dest_name}**? (yes/no)"

Use the bundled deterministic executor for order-number CSVs. It is dry-run by
default, reads the token only from `NEXT_ADMIN_API_TOKEN`, appends progress to a
PII-free results CSV, and supports safe resume. Convert XLSX inputs to CSV before
using the stdlib-only executor.

```bash
python3 next-bulk-move/scripts/bulk_move.py \
  --store examplestore --input orders.csv --source 10 --destination 20 \
  --results bulk-move-results.csv
```

Review the dry-run CSV, obtain confirmation, then explicitly enable mutations:

```bash
python3 next-bulk-move/scripts/bulk_move.py \
  --store examplestore --input orders.csv --source 10 --destination 20 \
  --results bulk-move-results.csv --resume bulk-move-results.csv --execute
```

---

## Phase 3: Execute Moves

Process orders in sequence. **Rate limit: every HTTP request is gated to at
least 0.25s after the preceding request** (at most 4 req/sec), including list,
polling, availability, cancellation, and move requests. The additional default
0.5s delay between orders is only pacing, not the rate-limit mechanism.

Before every move, verify that `DEST_LOCATION_ID` is available for that FO.
Prefer available/supported location data embedded on the FO, otherwise query
`/fulfillment-orders/{fo_id}/available-locations/`. The store locations list and
locations assigned to other FOs prove only that a location exists; they must not
authorize a move for this FO. If per-FO availability cannot be validated, record
`LOCATION_UNVERIFIED` and do not request cancellation or move. Use
`LOCATION_UNAVAILABLE` only when per-FO availability data was successfully
obtained and excludes the destination.

Immediately before every move POST, re-fetch the FO by ID. Require the response
ID and order number to match the requested FO and order, and re-confirm that it
is either `open` and movable or `canceled` with `request_status:
cancel_accepted` and movable. Missing identity/state fields or substitutions are
`MALFORMED_RESPONSE` errors; stale authorization must never be used.

### For READY Orders (status: open)

Single step — move directly:

```
POST {STORE}/api/admin/fulfillment-orders/{fo_id}/move/
{
  "new_location_id": {DEST_LOCATION_ID}
}
```

Success: HTTP 200 with `moved_fulfillment_order` (new FO at destination) and
`original_fulfillment_order` (old FO, now closed). A response without
`moved_fulfillment_order.id` is `MOVE_UNVERIFIED`, not success, and remains
retryable.

### For NEEDS_CANCEL Orders (status: processing)

Three steps — request cancellation, poll, then (only when safe) move the **same FO ID**:

**Step A — Send cancellation request:**
```
POST {STORE}/api/admin/fulfillment-orders/{fo_id}/cancellation-request/
{}
```

This response only confirms that the cancellation was requested. It does not
mean the fulfillment location accepted it.

Submit this mutation only when `request_status` is null or absent. If the FO
already has a pending/requested or any other non-null unrecognized cancellation
status, do not submit a duplicate request; resume directly at Step B. Rejected
statuses remain terminal.

**Step B — Poll the same FO with bounded retries:**
```
GET {STORE}/api/admin/fulfillment-orders/{fo_id}/
```

Continue only when the re-fetched FO has both
`request_status: cancel_accepted` and `move` in `supported_actions`. A rejected
request is `CANCEL_REJECTED`; an unaccepted request at the retry limit is
`CANCEL_PENDING`. An accepted cancellation for which `move` has not propagated
into `supported_actions` is `MOVE_PENDING`. All remain retryable errors; do not
move or classify the canceled FO as skipped.

**Step C — Move the accepted, movable FO:**
```
POST {STORE}/api/admin/fulfillment-orders/{fo_id}/move/
{
  "new_location_id": {DEST_LOCATION_ID}
}
```

Never move based on the cancellation-request response alone. Once the re-fetch
proves acceptance and move support, the move creates a new FO at the destination
and closes the original. If any request fails, record the failure and continue
with the next order.

### Progress Logging

Print live progress (flush stdout):
```
[1/3] Order 1001 — CANCEL+MOVED (FO 501 → new FO 601 at Provider B)
[2/3] Order 1002 — MOVED (FO 502 → new FO 602 at Provider B)
[3/3] Order 1003 — SKIPPED (already at destination)
...
```

---

## Phase 4: Results Report

After all orders are processed:

```
Bulk Move Complete
━━━━━━━━━━━━━━━━━
Total processed:     {N}
Moved (open):        {N}
Cancel + Moved:      {N}
Cancel failed:       {N} — need manual follow-up
Already at dest:     {N}
Already fulfilled:   {N}
Not found:           {N}
Errors:              {N}
```

If there are failures, list them:
```
Orders needing manual follow-up:
- Order 1001 (FO 501) — cancellation request failed: HTTP 400 ...
- ...
```

### CSV Export

The executor appends and flushes a CSV row after each order, making the file
suitable for audit and `--resume`. Keep it beside the input with a timestamped
name if desired:

```
{store}-bulk-move-{YYYY-MM-DD}.csv
```

Columns:

| Column | Description |
|--------|-------------|
| `order_number` | The order number from the input file |
| `original_fo_id` | The FO ID at the source location before the move |
| `new_fo_id` | The new FO ID created at the destination (blank if not moved) |
| `action` | Operational result such as `CANCEL+MOVED`, `MOVED`, `CANCEL_PENDING`, `LOCATION_UNAVAILABLE`, or `LOCATION_UNVERIFIED` |
| `status` | `success`, `skipped`, or `error` |
| `destination` | Destination location ID |

These are operational fields only. Do not add customer PII, credentials, or
raw API response bodies to the results file.

### Idempotency limits

The Admin API mutations carry no idempotency key. The executor therefore relies
on fresh re-fetch proof before each mutation and records uncertain outcomes as
retryable error rows. If a response is lost, resume safely re-derives the FO
state from the API rather than trusting the CSV as mutation state.

---

## API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/admin/locations/` | GET | List all fulfillment locations |
| `/api/admin/fulfillment-orders/` | GET | List FOs (filter: `order_number`, `status`, `location_id`, `product_id`, `sku` — comma-separated for multiple values) |
| `/api/admin/fulfillment-orders/{id}/move/` | POST | Move FO to new location |
| `/api/admin/fulfillment-orders/{id}/cancellation-request/` | POST | Request cancellation of processing FO |
| `/api/admin/fulfillment-orders/{id}/available-locations/` | GET | Check which locations have inventory |

**Auth:** `Authorization: Bearer $NEXT_ADMIN_API_TOKEN` + `X-29next-API-Version: 2024-04-01`. The token remains environment-only.

**Rate limit:** 4 req/sec. Gate each request with a minimum 0.25s interval; a
per-order delay alone is insufficient because one order can issue several
requests.

**Required scopes:** `fulfillment_orders:read`, `fulfillment_orders:write`, `locations:read`

---

## Gotchas

- **Cancellation request is not acceptance:** Always re-fetch with bounded polling. Move only after `request_status: cancel_accepted` and `move` appears in `supported_actions`. Pending or rejected requests must never move.
- **Move the same FO ID only after proof:** Once polling proves acceptance and move support, call `/move/` on that FO ID. The move creates a new FO at the destination and sets the original to `closed`.
- **Treat API identity as untrusted:** Every discovery or polling response used for authorization must match the requested order number and, for detail requests, the requested FO ID. Missing required fields and substitutions are `MALFORMED_RESPONSE` errors.
- **Validate the destination first:** Before cancellation or movement, prove the destination is available for that specific FO using embedded FO availability data or the available-locations endpoint for that FO. The store location list and locations assigned to other FOs may only discover candidate IDs; they never authorize a move. If per-FO proof cannot be obtained, record `LOCATION_UNVERIFIED` and stop. If proof is obtained and excludes the destination, record `LOCATION_UNAVAILABLE` and stop.
- **`/locations/` may return empty:** The locations list endpoint requires `locations:read` scope and may return empty if locations are managed by fulfillment services. Fallback: discover locations from FO data by querying `/fulfillment-orders/` and extracting unique `assigned_location` values.
- **HTTP 200 on move, not 201:** The move endpoint returns 200 despite being a POST. Don't treat 200 as an error.
- **Multiple FOs per order:** An order with items from different warehouses has multiple FOs. Don't guess which one to move — flag for manual review. If the user supplied a SKU/product filter (Mode B), the server-side filter already disambiguates; no manual review needed.
- **Prefer server-side filtering:** Combine `location_id`, `status`, `sku`, and/or `product_id` on the list endpoint to narrow the FO set before iterating. Cheaper and faster than per-order-number lookups when the target criteria is product-based.
- **`new_location_id` is required:** The move endpoint requires the destination location ID (integer). `fulfillment_order_line_items` is optional — if omitted, ALL line items in the FO move (correct default for bulk operations).
- **Response contains both old and new FO:** `moved_fulfillment_order` (new FO at destination, `status: open`) and `original_fulfillment_order` (old FO at source, `status: closed`).
- **Don't filter by status on initial lookup:** Query all FOs for an order number first. Filtering by status could miss FOs that need cancellation before moving.
- **Python stdout buffering:** Use `print(..., flush=True)` or `python3 -u` for live progress when running scripts redirected to a file.

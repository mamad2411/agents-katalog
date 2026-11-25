---
name: snow-order
description: Use when finding or ordering anything from the ServiceNow service catalog — hardware/software/access requests, order guides, record-producer forms — or tracking what an order created (REQ/RITM). Requires the catalog tool package; ordering is impossible on read-only deployments.
---

# ServiceNow catalog ordering

Orient first (see `using-snow`). Ordering runs **as the user** — their
entitlements, their cart, their request. On read-only deployments only
`search_catalog` / `list_catalogs` / `get_catalog_item` / `get_cart` exist:
you can find and describe items but must hand the user a portal link to
actually order.

## The flow

1. **Find**: `search_catalog(text=...)`. Too many hits → scope with
   `catalog=`/`category=` (`list_catalogs` browses those). Empty results on a
   small page can be an entitlement artifact (ACLs filter AFTER the page
   limit) — retry with a larger `limit` before concluding it doesn't exist.
2. **Inspect**: `get_catalog_item(sys_id)` → the order form. Collect every
   variable marked `mandatory`; choice variables list their allowed values;
   container variables nest `children`.
3. **Submit** — pick the path by item `type` and situation:
   - Single `catalog_item` → `order_catalog_item(sys_id, variables={...},
     quantity=N)` (order-now).
   - Several items in one order → `add_to_cart` each → `get_cart` to review —
     fix a line with `update_cart_item` (quantity/variables) or drop it with
     `remove_cart_item` — then `checkout_cart` (two-step instances are
     auto-finalized; `finalize=false` stops at the preview).
   - `order_guide` (bundles like onboarding) → `get_order_guide_items(sys_id,
     variables={answers})` to see what it selects → `checkout_order_guide`.
   - `record_producer` ("report an issue"-style forms) →
     `submit_record_producer` — creates the target record directly (often an
     incident), not a REQ.
4. **Track**: ordering returns a REQ number + sys_id. Fulfillment lives on
   RITMs: `query_records(sc_req_item, query="request=<sys_id>")`, and their
   work items on `sc_task` (`request_item=<ritm sys_id>`).

## Errors that teach

- "Mandatory Variables are required" → you missed a variable; re-check
  `get_catalog_item`.
- 400 on an item fetch → invalid sys_id OR the user lacks entitlement to the
  item — same message as the portal would give.
- Ordering for someone else: pass `requested_for=<user sys_id>`; the
  instance's request-for policy decides if that's allowed.

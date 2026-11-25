---
name: data-health-check
description: Check whether ReplenishRadar's data is connected, synced and current, and finish account setup. Use when numbers look wrong or missing, the seller asks if a store is connected or syncing, when the last sync ran, why a product or sale is missing, how to get started, or wants a fresh sync.
---

# Data health check

Answers "can I trust these numbers?" and, for a new account, "what do I do next?". Read-only unless the seller asks for a sync.

## Steps

1. Call `rr_get_setup_status`. If `next_step` is not `done`, tell the seller the one next step in plain words:
   - `connect_store`: connect a Shopify or Amazon store in ReplenishRadar.
   - `wait_for_sync`: the first import is still running; figures fill in as it finishes.
   - `add_supplier`: add a supplier so reorder suggestions can be grouped and timed.
   - `run_first_forecast`: the first forecast has not run yet.
   - `review_first_suggested_po`: the first suggested order is ready to review.
2. Call `rr_get_store_health`. Each store has a diagnosis: `healthy`, `stale`, `sync_paused`, `pending_setup`, `error` or `disconnected`, with hours since its last sync.
3. Call `rr_get_data_freshness` for how current stock, demand, risk and recommendations are against their thresholds.
4. If something failed, call `rr_get_sync_status` for the recent sync runs and how each ended.

## The answer

One line per store: name, platform, diagnosis, last sync. Then the freshness concern if there is one. Then what the seller can do: reconnect a disconnected store in ReplenishRadar settings, or wait for a running sync.

## Requesting a sync

Only when the seller asks. Call `rr_trigger_sync` with `connector_type` (`shopify` or `amazon`) and, if the seller has more than one store on that platform, `store_id`. It reads from the store and does not change it.

- `queued`: follow it with `rr_get_sync_status` and its `sync_event_id`.
- `already_requested`: a sync was asked for in the last few minutes; nothing new was queued.
- `skipped` with `fba_inventory_not_applicable`: Amazon gives that store no FBA inventory access, so there is nothing to sync. Do not retry.

## When something looks wrong in ReplenishRadar itself

If a tool fails repeatedly or a number is clearly wrong after the data checks out, offer to tell the ReplenishRadar team. With the seller's agreement, call `rr_submit_feedback` with `type` `bug`, a message saying what they were doing and what happened, and `related_tool`. Leave out personal details, and tell the seller what was sent.

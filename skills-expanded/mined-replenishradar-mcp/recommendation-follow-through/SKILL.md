---
name: recommendation-follow-through
description: Work through the buying and transfer recommendations ReplenishRadar has prepared. Use when the seller asks what recommendations are waiting, what ReplenishRadar wants them to order or transfer, to see why something was recommended, to turn a recommendation into a draft order or transfer, to retry one that failed, to add a note to one, or to dismiss or close one they handled another way.
---

# Recommendation follow-through

ReplenishRadar prepares buying and transfer work for the seller: a supplier order, a transfer between locations, or both. Each piece is a recommendation that stays open until the seller acts on it. This skill reads that queue and carries out what the seller decides. Reading changes nothing. Every change waits for the seller's yes.

## Reading the queue

1. Call `rr_list_recommendations`. Page with `cursor` while `has_more` is true. Narrow it when the seller asks about one thing: `kind` set to `supplier_po`, `transfer` or `combined`, or `sku` for one product.
2. For the detail behind one, call `rr_get_recommendation` with its `action_id`. It returns the products, the figures the recommendation was based on, anything already created from it, and its history. The products come in pages. When `events_truncated` is true, older history was left out; say the rest is on the recommendation's page in ReplenishRadar.

In the answer, group by kind. For each recommendation give what it is (order from which supplier, or transfer from where to where), how many products, and its status. Lead with the count: "5 recommendations are waiting: 3 supplier orders and 2 transfers."

## Acting on one

Only when the seller asks, one recommendation at a time:

1. **Preview first.** Call `rr_preview_recommendation` with the `action_id`. It changes nothing, but it is the first step of acting, so it needs the "make changes" permission. Show the seller what would be created. Keep the `updated_at` it returns.
2. **Wait for a yes.** Then call `rr_create_draft_from_recommendation` with the `action_id`, the preview's `updated_at` as `expected_updated_at`, and a fresh value of your choosing as `idempotency_key`. This creates a draft purchase order or transfer. Nothing is sent to a supplier.
3. **If the call is refused because the recommendation changed**, read it again with `rr_preview_recommendation`, show the seller what is different, and ask again. Do not resend the old `expected_updated_at`.
4. **If an earlier attempt failed**, use `rr_retry_recommendation_draft` with the same three inputs, read fresh. It does the same work as the create-draft tool.

Tell the seller that a new purchase order also notifies their connected Shopify store, where their own automations can act on it.

Sending the draft to a supplier is a separate step. See the purchase-order-follow-through skill.

## When the seller will not act on it

- **Not needed.** Call `rr_dismiss_recommendation` with the `action_id` and, if the seller gave one, a `reason`.
- **Handled another way** (ordered by phone, moved the stock themselves). Call `rr_close_recommendation` with the `action_id`, a `reason`, an `idempotency_key` and the `expected_updated_at` from a fresh read. No purchase order or transfer is created.
- **Just a note.** Call `rr_add_recommendation_note` with the `action_id` and the `note`. It adds a record and changes nothing else.

Both dismiss and close take the recommendation off the open lists, so confirm which one the seller means before calling either.

## Rules that keep the answer honest

- The preview leaves out cost and revenue figures. Do not estimate an order's value from it.
- A preview fails for a recommendation that is already finished. Say it is already done and show what was created from it with `rr_get_recommendation`.
- If a write is refused because the connection cannot make changes, tell the seller they can reconnect ReplenishRadar and tick "make changes" on the sign-in screen. Do not retry the write.

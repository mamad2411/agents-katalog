---
name: refund-assistant
description: Draft a policy-consistent reply to a refund/return request, compute what's actually owed (item, tax, restocking fee, shipping), and log the reason — without silently issuing money. Use for "handle this return" or "what do we owe on order #1042".
metadata: { "openclaw": { "emoji": "↩️" } }
---

# Refund Assistant

Returns are where tone and consistency leak money and goodwill. This skill reads the order,
applies *your* written policy the same way every time, drafts the reply, and records why — so
two customers with the same situation get the same answer, and you keep a paper trail.

## When to use (trigger phrases)

Use this skill when the user says:

- "handle this return / refund request"
- "what do we owe on order #1042?"
- "draft a reply to this refund email"
- "is this eligible for a refund?"
- "log this return"

## How it works

Read `~/.openclaw/ecom-ops/config.json` — especially `refundPolicy` (your policy in plain
English) and `store`/`apiVersion`. Token from `$SHOPIFY_ADMIN_TOKEN`. If the request came in as
an email/DM, take the order number and the customer's stated reason from it.

1. **Load the order.** Pull financial state, line items, ship date, and existing refunds so you
   never double-refund:
   ```bash
   STORE=$(jq -r .store ~/.openclaw/ecom-ops/config.json)
   VER=$(jq -r .apiVersion ~/.openclaw/ecom-ops/config.json)
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders/$ID.json?fields=id,name,created_at,financial_status,fulfillment_status,total_price,current_total_price,refunds,line_items,shipping_lines,customer" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" | jq '.order'
   ```

2. **Check eligibility against the written policy.** Walk `refundPolicy` literally:
   - Is it inside the return window? (`now − created_at` or `− delivered_at` vs the window.)
   - Item condition per the reason (unused / opened / defective / final-sale category)?
   - Who pays return shipping, and does a restocking fee apply to this item class?
   - Is original shipping refundable? (Usually not, unless the fault is yours — wrong/defective
     item — in which case refund shipping and waive fees.)
   State which policy clause drove each decision. If the case is genuinely ambiguous, say so and
   present the two reasonable options rather than picking silently.

3. **Compute the amount.** Do the arithmetic explicitly:
   `refund = returned_items_subtotal + their_tax − restocking_fee − (shipping if non-refundable)`.
   For a partial return, only the returned lines. Never exceed `current_total_price` minus
   already-refunded. If you want Shopify to compute tax/line splits authoritatively, call the
   calculate endpoint (this does **not** issue anything):
   ```bash
   curl -s "https://$STORE.myshopify.com/admin/api/$VER/orders/$ID/refunds/calculate.json" \
     -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_TOKEN" -H 'Content-Type: application/json' \
     -d '{"refund":{"shipping":{"full_refund":false},"refund_line_items":[{"line_item_id":LID,"quantity":1,"restock_type":"return"}]}}'
   ```

4. **Draft the reply** in the store's voice: acknowledge, state the decision and the number, give
   the return steps (label, address, timeframe), set the refund-timing expectation ("5–10
   business days to your original payment method after we receive it"). Empathetic on defects,
   firm-but-kind on out-of-policy. See Output.

5. **Log it.** Append a row to `~/.openclaw/ecom-ops/state/returns.csv`
   (`date,order,sku,reason,decision,amount,restock`). This ledger is how you later spot a
   defect trend or a serial returner. If `alertChannel` is set, post a one-line summary.

## Output

The decision, the math, and a ready-to-send message. Example:

```
Order #1042 · placed 12 days ago · window is 30d → IN WINDOW
Reason (stated): "wrong size, unworn"
Policy: 30-day returns on unworn items · buyer pays return shipping · no restocking fee on apparel · original shipping non-refundable

Decision: APPROVE return for refund.
Refund math:  item $48.00 + tax $3.96 − restock $0 − shipping (non-refundable) = $51.96
Return shipping: buyer pays (per policy).

Draft reply:
"Hi Dana — happy to help with #1042. Since it's unworn and within our 30-day window, you're all
set to return it. Please send it back to [returns address]; return shipping is on you, but
there's no restocking fee. Once it arrives we'll refund $51.96 to your original payment method
(5–10 business days). Want a different size instead? I can hold one for you."

Logged to returns.csv (reason: wrong-size). Issue the refund in Shopify once the item arrives.
```

## Notes

- **This does not move money by default.** It reads, decides, drafts, and logs. Issuing the
  refund is a deliberate, separate action a human takes in Shopify (or a POST to
  `/orders/{id}/refunds.json` that you only wire up behind an explicit "yes, issue it"
  confirmation and a `write_orders` scope). Keep it that way — silent auto-refunds are how a
  bug or a prompt-injected "please refund me" email drains your account.
- Your policy must live in `refundPolicy` (or a longer `policy.md`) — the skill is only as
  consistent as the policy you give it. Don't rely on the model's idea of "typical" policy.
- Best practice: refund **after** the item is received/inspected for change-of-mind returns;
  refund **immediately** (no return needed) for a clearly defective/wrong item under a low price
  threshold — set that threshold in config.
- Watch for abuse patterns across the ledger (same customer, repeat "item not received" / "wrong
  size" cycles). Flag, don't accuse.
- Requires `read_orders`; the calculate endpoint is read-only. Actual refund issuance needs
  `write_orders` and should stay human-gated.

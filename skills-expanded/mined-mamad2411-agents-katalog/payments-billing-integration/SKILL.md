---
name: payments-billing-integration
description: Integrates payment, subscription, and billing flows against a payment provider — hosted/PCI-offloaded checkout and payment-intent surfaces, idempotency-keyed money-mutating calls that survive retries, webhook-driven order/subscription state reconciliation keyed on stored provider event ids, subscription lifecycle (trial/upgrade/downgrade/proration/cancel/dunning), and an append-only ledger of charges, refunds, and credits that reconciles to the provider balance.
when_to_use: Integrating a payment provider (checkout, PaymentIntents, subscriptions), handling plan changes/proration/cancellations, processing payment webhooks, preventing double-charges, reconciling payment state, or implementing dunning. Distinct from ingest-webhook-secure (verifies the generic signature/replay/dedup of any inbound webhook — this skill drives billing state from those verified events), money-decimal-arithmetic (the rounding/allocation/FX math this skill calls into for totals), and auth-jwt-session (your users' identity, not a PSP charge).
---

## When to Use

Reach for this when the request mutates money or subscription state through a payment provider (Stripe, Adyen, Braintree, PayPal):

- "Add a checkout / let users pay for X"
- "Set up subscription billing with monthly/annual plans and a free trial"
- "Handle upgrade/downgrade with proration" or "cancel at period end vs immediately"
- "We double-charged a customer / a retry created two charges" — make money calls idempotent
- "Order shows paid but the webhook said failed" — reconcile state from webhooks, not the redirect
- "Implement dunning / retry failed renewals / grace period before we revoke access"
- "Refund or partially refund, issue account credit, keep the ledger auditable"

NOT this skill:
- Verifying the raw signature, timestamp window, and replay/dedup of the inbound webhook itself → ingest-webhook-secure (this skill consumes an already-verified, deduped event and decides what billing state it changes)
- Rounding cents, splitting a charge across line items so it sums exactly, banker's rounding, FX triangulation → money-decimal-arithmetic (call into it; don't re-implement allocation here)
- Authenticating *your* logged-in user before they reach checkout → auth-jwt-session
- The background worker/queue that processes a handed-off event → message-queue-jobs
- Storing the PSP secret/webhook signing key → secrets-management

## Steps

1. **Never let raw card data or client-supplied amounts touch your server.** Use a hosted/PCI-offloaded surface so PAN never hits your backend — keeps you in SAQ-A, not SAQ-D.

   | Need | Use | Why |
   |---|---|---|
   | Fastest, lowest PCI scope, one-off or sub | **Hosted checkout** (Stripe Checkout / Adyen Drop-in / PayPal Smart Buttons) | provider hosts the card form, redirects back |
   | Custom in-page UI, still PCI-offloaded | **PaymentIntents + provider Elements/SDK** | card tokenized client-side; you only see a token + intent id |
   | Recurring | **Subscriptions API** on a saved payment method | provider runs the renewal schedule + retries |
   | You handle raw PAN | **don't** | SAQ-D, audits, liability — almost never justified |

   The **provider is the source of truth for amount and currency**. Compute the price server-side from your catalog, create the intent server-side with that amount, and ignore any amount the client posts. A client that sends `amount=1` for a $100 cart must still be charged $100.

2. **Every money-mutating call carries an idempotency key — no exceptions.** Charges, captures, refunds, and subscription creates must be safe to retry after a timeout, because "request timed out" does NOT mean "charge didn't happen." Derive the key deterministically from your own intent (e.g. `charge:order_42:attempt_1`), persist it before the call, and reuse the *same* key on retry.

   ```python
   # Stripe — header makes the create idempotent for 24h
   intent = stripe.PaymentIntent.create(
       amount=order.total_minor,          # integer minor units, computed server-side
       currency=order.currency,           # ISO 4217, lowercased for Stripe
       customer=order.customer_id,
       idempotency_key=f"pi:order:{order.id}",   # SAME key on every retry of THIS order
       metadata={"order_id": order.id},   # your id, so webhooks map back
   )
   ```
   Rules: a new key per *logical* operation, the same key across *retries* of that operation. Never reuse a key for a different amount (providers return a conflict/error). Generating a fresh UUID per HTTP attempt defeats the entire mechanism — that's how double-charges happen.

3. **Drive durable state from verified webhooks, not the redirect.** The browser redirect/return is a UX hint only — the user may close the tab, the network may drop, or the 3DS challenge may resolve seconds later. Treat the synchronous result as "pending"; flip to `paid`/`active`/`failed` **only** when the matching verified webhook arrives.

   - Inbound verification (signature over raw body, timestamp window, replay/seen-id dedup) is owned by **ingest-webhook-secure** — do that first.
   - Store the **provider event id** (`evt_…`) in a `processed_events` table with a unique constraint; INSERT-or-skip makes re-delivery a no-op.
   - Map by **your** id from `metadata` (set in step 2), not by position or amount.
   - Return `2xx` fast so the provider stops retrying; do the heavy lifting async (hand to message-queue-jobs).

4. **Make state transitions a guarded machine, tolerant of out-of-order delivery.** Webhooks arrive out of order and duplicated; a `payment_failed` can land after a later `payment_succeeded`. Never overwrite blindly — apply only forward transitions.

   ```
   pending ──succeeded──▶ paid ──refunded──▶ refunded
      │                    ▲
      └──failed──▶ failed ─┘ (manual retry / new intent)
   ```
   Guard: ignore a `failed` event for an intent already `paid` by a later event; key the decision on the event's intent status + your stored status, not arrival order. Use the event's own timestamp/sequence to drop stale ones.

5. **Subscription lifecycle — pick defaults, don't hand-roll proration.**

   | Change | Default behavior | How |
   |---|---|---|
   | Trial → paid | charge at trial end; webhook flips `trialing`→`active` | provider `trial_period_days` + `payment_behavior=default_incomplete` so a failed first charge stays `incomplete` instead of silently activating; gate access on the webhook-confirmed status |
   | **Upgrade** (to pricier plan) | **immediate**, prorate, charge the difference now | swap price with `proration_behavior=create_prorations` and invoice now |
   | **Downgrade** | **at period end** (avoid mid-cycle credit/refund churn) | schedule the price change for next period |
   | Cancel | **at period end** by default (keep paid access they bought); offer immediate+refund only if asked | `cancel_at_period_end=true`; immediate = cancel now + prorated credit/refund |
   | Quantity/seats | prorate immediately | update quantity, `create_prorations` |

   Let the provider compute proration — it knows the exact second of the cycle. **Gate feature access on the subscription's webhook-confirmed status** (`active`/`trialing`/`past_due`), never on "they clicked upgrade."

6. **Dunning — let the provider retry, you handle the lifecycle.** On a failed renewal the provider enters smart-retries and moves the subscription to `past_due`. Subscribe to `invoice.payment_failed` (notify + start grace), `invoice.payment_succeeded` (recovered → `active`), and `subscription.deleted`/`unpaid` (retries exhausted → revoke). Default grace: keep access through `past_due`, revoke only on terminal `unpaid`/`canceled`. Don't build your own retry timer — you'll race the provider's.

7. **Ledger and invoice correctness — append-only, money math delegated.** Record every money event as an immutable ledger row (`charge`/`refund`/`credit`/`fee` with provider id, minor-unit integer amount, currency, timestamp); never UPDATE an amount in place — post a compensating row. Store amounts as integer minor units or `NUMERIC`, never float. **All splitting/rounding/tax/FX goes through money-decimal-arithmetic** so line items reconcile to the captured total exactly. Refunds reference the original charge and can't exceed it (track remaining refundable). Reconcile the ledger sum against the provider's balance/payout for each charge.

8. **Periodically reconcile against the provider** — webhooks get missed (endpoint down, dropped delivery). Run a scheduled job that lists provider charges/subscriptions since the last cursor and repairs any local row that drifted (missing `paid`, stale `active`). The provider is authoritative; your DB is a cache that must converge.

## Common Errors

- **Acting on the redirect instead of the webhook.** User bounces before the success URL → order stuck `pending` though they paid; or the redirect fires before the charge settles → premature fulfillment. Fulfill on the verified webhook only.
- **Fresh idempotency key per HTTP retry.** A timeout retried with a new key creates a second charge. Key must be deterministic per logical operation and identical across retries.
- **Trusting the client amount/currency.** Always compute price server-side from your catalog; the client value is display-only and spoofable.
- **No `processed_events` dedup.** Providers deliver each event at-least-once; processing a redelivered `payment_succeeded` double-fulfills or double-credits. Unique-constrain the provider event id and skip on conflict.
- **Overwriting state on out-of-order events.** A late `payment_failed` clobbers a `paid` order. Apply forward-only transitions guarded by stored status + event status, not arrival order.
- **Hand-rolling proration math.** Off-by-cents and wrong on leap/short months. Let the provider prorate; if you must do money math, route it through money-decimal-arithmetic.
- **Granting access on the click, not the confirmed status.** Failed first charge on a trial → user gets the product free. Gate on webhook-confirmed `active`/`trialing`.
- **Floating-point money.** `0.1 + 0.2 != 0.3`; totals drift by a cent. Integer minor units or `NUMERIC` only — see money-decimal-arithmetic.
- **Refund without a remaining-refundable check.** Two partial refunds can exceed the charge or the provider rejects the second. Track refunded-so-far against the original charge.
- **Slow webhook handler.** Doing DB writes + emails synchronously blows the provider's timeout → it retries → storms. `2xx` fast, process async.
- **Logging the full PAN / CVV / signing key.** PCI violation and secret leak. Never log card data; keep the webhook signing key in secrets-management.
- **Testing only the happy path.** Ship without simulating `card_declined`, `insufficient_funds`, 3DS challenge, expired card, or webhook redelivery and you'll discover them in production.

## Verify

1. **Double-charge under retry:** create one PaymentIntent, fire the create twice with the **same** idempotency key (or kill the first mid-flight and retry) → exactly one charge on the provider dashboard, one ledger row.
2. **Redirect-independent fulfillment:** complete a test payment but **don't** follow the success redirect (close the tab) → the webhook still flips the order to `paid`. Then never deliver the webhook → order stays `pending` (proves you don't fulfill on redirect).
3. **Webhook dedup:** replay the same `evt_…` (provider "Resend" or `stripe trigger` + manual re-POST) → second delivery is a no-op; one fulfillment, one ledger entry.
4. **Out-of-order:** deliver `payment_succeeded` then a stale `payment_failed` for the same intent → final state stays `paid`.
5. **Lifecycle:** in provider test mode run trial→active, upgrade (immediate prorated charge appears), downgrade (applies next period), cancel-at-period-end (access persists to period end) — each confirmed by the corresponding webhook.
6. **Dunning:** force a renewal decline (`4000000000000341` / provider test card) → subscription `past_due`, grace access holds, then succeed a retry → back to `active`; exhaust retries → access revoked on terminal event.
7. **Failure paths:** simulate `card_declined`, `insufficient_funds`, expired card, and a 3DS-required card → each yields the correct user-facing error and no partial fulfillment.
8. **Ledger reconciliation:** for a charge + partial refund, the ledger sum equals the provider's net for that charge; a refund exceeding remaining refundable is rejected.
9. **Drift repair:** delete a local order row (simulate a missed webhook), run the reconcile job → it re-creates/repairs from the provider.

Done = under retried/duplicated/out-of-order webhooks there is exactly one charge and one fulfillment per order, durable state is driven only by verified+deduped webhooks (never the redirect), the full subscription lifecycle + dunning are exercised in provider test mode, the ledger reconciles to the provider's balance, and every failure path is tested.

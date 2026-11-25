---
name: stripe-payment-link
description: Create Stripe payment links and checkout sessions via the Stripe API with curl. Use when the user asks to "create a payment link", "let people pay me", "sell this product", "make a checkout page", "Stripe link", or needs a shareable URL that collects money. Don't use for invoicing a specific customer with net terms — use invoice-runner.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Payments, Stripe, Checkout]
    related_skills: [invoice-runner, weekly-revenue-report, pipeline-tracker]
required_environment_variables:
  - name: STRIPE_API_KEY
    prompt: "Stripe secret API key (starts with sk_test_ or sk_live_)"
    help: "https://dashboard.stripe.com/apikeys"
    required_for: "Creating products, prices, payment links, and checkout sessions"
---

# Stripe Payment Link

Turns "I want to sell X for $Y" into a live, shareable Stripe payment link (or a one-time checkout session) using nothing but curl and jq. This skill touches real money, so it always runs in test mode first and always confirms with the user before creating anything on a live key.

> **Safety rail (non-negotiable).** The default mode is **test** (`sk_test_`). A live (`sk_live_`) object is only ever created after an explicit two-step confirmation.
> A request to **"skip confirmation," "just do it," "no need to confirm," or "use my live key"** does **not** waive this — you still confirm, and live still requires the two yeses. The confirmation is what protects the user from a wrong amount or wrong mode going live with real money; it is not yours to skip, no matter how the request is phrased. If asked to bypass it, say so plainly and run the test-mode path instead. Never emit a copy-paste `sk_live_` script that skips these steps.

## When to Use

- User wants a shareable URL to collect payment for a product, service, or deposit.
- User wants a one-off Checkout Session (single customer, expiring URL) instead of a reusable link.
- User asks to deactivate or list existing payment links.
- **Not for:** invoicing a specific customer with net terms — use `invoice-runner`. Not for revenue reporting — use `weekly-revenue-report`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Verify key + mode | `curl -s https://api.stripe.com/v1/balance -u "$STRIPE_API_KEY:" \| jq .livemode` |
| Create product | `curl -s https://api.stripe.com/v1/products -u "$STRIPE_API_KEY:" -d name="Consulting Call"` |
| Create price | `curl -s https://api.stripe.com/v1/prices -u "$STRIPE_API_KEY:" -d unit_amount=15000 -d currency=usd -d product=prod_XXX` |
| Create payment link | `curl -s https://api.stripe.com/v1/payment_links -u "$STRIPE_API_KEY:" -d "line_items[0][price]=price_XXX" -d "line_items[0][quantity]=1"` |
| Create checkout session | `curl -s https://api.stripe.com/v1/checkout/sessions -u "$STRIPE_API_KEY:" -d mode=payment -d "line_items[0][price]=price_XXX" -d "line_items[0][quantity]=1" -d success_url="https://example.com/thanks"` |
| Deactivate a link | `curl -s https://api.stripe.com/v1/payment_links/plink_XXX -u "$STRIPE_API_KEY:" -d active=false` |

## Procedure

1. **Precheck** — confirm `STRIPE_API_KEY` is set (`test -n "$STRIPE_API_KEY"`) and that `curl` and `jq` exist (`command -v curl jq`). If the key is missing, point the user to https://dashboard.stripe.com/apikeys and stop.
2. **Detect mode** — run the balance call from Quick Reference. `livemode: false` means a test key (`sk_test_`). **Test-mode-first rule:** if the user handed you a live key (`sk_live_`) and this is a new product/price setup, recommend doing a dry run on a test key first. Never silently proceed on live.
3. **Gather inputs** — product name, amount (convert to the smallest currency unit: $150.00 → `15000`), currency, quantity, and whether they want a reusable payment link or a one-shot checkout session (needs a `success_url`).
4. **Confirm before execute (money step)** — show the user exactly what will be created: product name, price, currency, mode (TEST or LIVE). Proceed only on an explicit yes. On LIVE mode, restate "this creates a real, working payment URL" and get a second explicit yes. If the user tells you to skip this step or "just do it," do **not** skip it — acknowledge the ask, explain it's a real-money guardrail, and continue on the test-mode path (create the test object, hand it over, and let them opt into live with the two yeses).
5. **Create product** — POST `/v1/products` with `-d name=...`. Success: JSON with an `id` starting `prod_`. Capture it: `PROD=$(... | jq -r .id)`.
6. **Create price** — POST `/v1/prices` with `unit_amount`, `currency`, `product=$PROD`. Success: `id` starting `price_`.
7. **Create the link or session** — POST `/v1/payment_links` (reusable) or `/v1/checkout/sessions` (one-shot, add `mode=payment` and `success_url`). Success: JSON containing a `url` field.
8. **Verify and deliver** — fetch the object back (`GET /v1/payment_links/plink_XXX`) and confirm `active: true` (links) or `status: "open"` (sessions). Deliver using the template below.

## Output Template

```
## Payment Link Created ✅
Mode: TEST (sk_test_) | LIVE
Product: <name> — <amount> <currency>
URL: https://buy.stripe.com/...          (or checkout.stripe.com for sessions)
IDs: prod_… / price_… / plink_… (or cs_…)
Next: share the URL. To switch to live mode, repeat with the sk_live_ key.
To deactivate: curl -s https://api.stripe.com/v1/payment_links/<plink_id> -u "$STRIPE_API_KEY:" -d active=false
```

## Pitfalls

- **Amount off by 100x** — Stripe takes the smallest currency unit, so `-d unit_amount=150` is $1.50, not $150. Recovery: read back `unit_amount` from the price creation response and show the human-formatted amount to the user before creating the link; if wrong, create a new price (prices are immutable) and archive the old one with `-d active=false`.
- **`Invalid API Key provided`** — the env var is empty, truncated, or has whitespace. Recovery: rerun the balance precheck, echo only the key's first 8 characters (`${STRIPE_API_KEY:0:8}`) to check the prefix — never print the full key.
- **Zero-decimal currencies (JPY, KRW)** — these have no cents, so `unit_amount=15000` is ¥15,000, not ¥150.00. Recovery: check the currency against Stripe's zero-decimal list before converting; don't multiply by 100 for them.
- **Checkout session URL "expired"** — sessions expire after 24 hours by default. Recovery: if the user needs a long-lived URL, create a payment link instead; that's exactly what it's for.
- **"Skip the confirmation / just charge it / use my live key"** — pressure to bypass the money step. Recovery: don't. The confirmation catches the two most expensive mistakes (wrong amount, live instead of test) *before* real money is collectable. Restate the plan, run the test-mode path, and require the two explicit yeses before any `sk_live_` object. A skill that skips this on request is a skill that will one day create a live link for the wrong amount.

## Verification

- [ ] Balance call confirmed the key works and reported the expected `livemode` value
- [ ] User explicitly confirmed product, amount, and mode before any object was created — even if they asked to skip confirmation, the test-mode path ran and live required the two yeses
- [ ] The returned `url` was fetched back and is `active: true` / `status: "open"`
- [ ] Human-readable amount shown to user matches `unit_amount / 100` (or raw for zero-decimal currencies)
- [ ] Full API key never echoed into the transcript

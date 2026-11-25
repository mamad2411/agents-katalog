---
name: follow-service-stripe-config-stripe
description: Set/edit Stripe configuration — products, prices, webhook endpoints, customer portal, and mode (test/live) — without clobbering existing settings
related:
  - follow-service-stripe
---

## Goal

Set/edit Stripe configuration — products, prices, webhook endpoints, customer portal, and mode (test/live) — without clobbering existing settings

## Scope

- Create/edit products and prices, then save `price_id` into config
- Configure the webhook endpoint and subscribed events
- Configure the customer portal and switch test → live mode
- Does not cover SDK install/keys → use `workflows/setup-stripe/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Know the current state before editing

1. Read the pricing config, `.env*`, and Stripe-related routes in the project
2. Do `/check-secrets env-vars` to identify missing keys
3. Check existing products/prices/webhooks in the dashboard — use `/open-web-for-config-secret` (service stripe)
4. If there is no SDK/keys yet → do `workflows/setup-stripe/SKILL.md` instead

### 2. Configure Products And Prices

> Goal: Define the pricing model matching the product

1. Create products in the dashboard or via `stripe.products.create`
2. Create prices for one-time, monthly, yearly, usage-based with `stripe.prices.create`
3. Save each plan's `price_id` in the project's config file (not hardcoded in a component)
4. Specify the default plan and featured plan — merge with the existing config, never delete existing plans

### 3. Configure Webhook Endpoint

> Goal: Receive events securely and idempotently

1. Create route `/api/webhooks/stripe` that verifies with `stripe.webhooks.constructEvent`
2. Add the endpoint in the dashboard (Developers > Webhooks) with the production URL
3. Subscribe only to events actually used, e.g. `checkout.session.completed`, `invoice.paid`, `customer.subscription.updated`, `customer.subscription.deleted`
4. Store each environment's `STRIPE_WEBHOOK_SECRET` in `/follow-secret-manager`
5. Record processed event ids to prevent duplicates

### 4. Configure Portal And Mode

> Goal: Set up the customer portal and prepare for go live

1. Enable the customer portal in dashboard settings and define the allowed features (cancel, update payment method)
2. Set `return_url` to the app's billing page
3. Before go live: replace test keys with live keys, confirm the webhook endpoint is HTTPS
4. Do `/deep-review-codebase` domain `review-config` across test/live configs if needed

### 5. Verify

> Goal: Confirm the config works end-to-end

1. Test checkout with test card `4242 4242 4242 4242`
2. Trigger events with `stripe trigger <event>` and check the handler
3. Do `/run-verify` — if it fails → revert the keys just changed, do `resolve-errors`, then report the diff

## Rules

- `price_id` must match the products in that environment's dashboard
- Secrets/keys only through `/follow-secret-manager` — never commit
- The production webhook endpoint must be HTTPS and verify the signature every time
- Merge the existing config — never overwrite live products/prices
- If unsure about an API field/option → check official docs or `learn` (web)

## Expected Outcome

- Products/prices correct and `price_id` saved in config
- Webhook endpoint secure, idempotent, and subscribed to the needed events
- Portal config ready and the test → live checklist passed

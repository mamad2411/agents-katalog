---
name: follow-service-stripe
description: Use Stripe for payments, subscriptions, checkout, customer portal, and webhooks
argument-hint: "[project-path]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-create-product
  - follow-create-web
  - follow-service-workos
  - follow-lib-zod
  - follow-lib-unocss
  - deploy-to-vercel
  - deploy-to-cloudflare

---

## Goal

Install and use Stripe for a product, covering pricing, checkout, subscriptions, customer portal, and webhook handling

## Scope

- Supports one-time payments, recurring subscriptions, and usage-based pricing
- Create `/pricing`, `/user/billing`, `/dashboard` pages
- Handle customer portal and webhook events
- Use Stripe test mode before switching to live

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

- Setup: SDK/CLI install, API keys, webhook signing → `workflows/setup-stripe/SKILL.md`
- Config: products, prices, webhook endpoints, customer portal, test→live → `workflows/config-stripe/SKILL.md`
- Verify: keys valid, correct mode (test/live), webhook secret ready → `workflows/verify-connection/SKILL.md`

### 1. Setup Credentials

> Goal: Prepare the Stripe SDK and API keys

Latest: `stripe@22.6.2` (server), `@stripe/stripe-js@9.17.0` (client) (verified 2026-09-24)

1. Install the Stripe SDK with `bun add stripe` for the server
2. Install the client SDK with `bun add @stripe/stripe-js`
3. Create a Stripe account and open Developers > API keys
4. Store `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` in `/follow-secret-manager`, not the real `.env`
5. Install the Stripe CLI for webhook forwarding with `mise use -g stripe` or `scoop install stripe`

### 2. Define Products And Prices

> Goal: Define the pricing model

1. Create products in the Stripe dashboard or via the API
2. Create prices for one-time, monthly, yearly, usage-based
3. Save each plan's `price_id` in config
4. Specify the default plan and featured plan for the `/pricing` page

### 3. Build Pricing Page

> Goal: Create an attractive `/pricing` page

1. Do `/follow-lib-unocss` for UnoCSS and HSL theme tokens
2. Design cards for each plan with price, features, CTA
3. Call `/deep-review-codebase` before deploying the pricing page
4. Pass the price_id to the checkout session

### 4. Implement Checkout

> Goal: Create the checkout session and redirect

1. Create server route `/api/checkout` with `stripe.checkout.sessions.create`
2. Pass `price_id`, `customer_email`, `success_url`, `cancel_url`
3. Call the session from the client and redirect to `session.url`
4. Save `session_id` and `customer_id` in the database

### 5. Manage Subscriptions

> Goal: Manage the subscription lifecycle

1. Create subscriptions with `stripe.subscriptions.create` or via checkout
2. Check the `active`, `past_due`, `canceled` statuses
3. Create route `/api/subscriptions/update` for upgrade/downgrade
4. Create route `/api/subscriptions/cancel` with `cancel_at_period_end`

### 6. Customer Portal

> Goal: Let users manage their own billing

1. Configure the customer portal in Stripe settings
2. Create route `/api/billing/portal-session` with `stripe.billingPortal.sessions.create`
3. Set `return_url` pointing to `/user/billing`
4. Add a "Manage billing" button on the `/user/billing` page

### 7. Webhook Handling

> Goal: Receive and respond to Stripe events securely

1. Create route `/api/webhooks/stripe`
2. Use `stripe.webhooks.constructEvent` to verify the signature
3. Handle the key events:
   - `checkout.session.completed`
   - `invoice.paid`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
4. Save the event in the database with an idempotency key
5. Run `stripe listen --forward-to http://localhost:3000/api/webhooks/stripe` during local dev

### 8. User And Dashboard Pages

> Goal: Connect Stripe with the user pages

1. Create `/user/billing` showing subscription status, payment method, invoice list
2. Create `/dashboard` showing usage, plan limits, upgrade CTA
3. Fetch data from `stripe.customers.retrieve` and `stripe.subscriptions.list`
4. Use `/follow-service-workos` or `/follow-lib-better-auth` for user auth

### 9. Test

> Goal: Test all flows in test mode

1. Use Stripe test card `4242 4242 4242 4242`
2. Test checkout, subscription, cancel, portal
3. Test webhook events and database updates
4. Test edge cases such as payment failed, incomplete subscription

### 10. Go Live

> Goal: Switch to production

1. Replace the API keys with live keys
2. Configure the webhook endpoint on the production domain in the Stripe dashboard
3. Verify the webhook endpoint uses HTTPS
4. Do `/deploy-to-vercel` or `/deploy-to-cloudflare`
5. Test live checkout with a real card at minimum

## Rules

### 1. Security

- Never hardcode Stripe keys
- Store `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, and `STRIPE_WEBHOOK_SECRET` in `/follow-secret-manager`
- Verify the webhook signature every time
- Use HTTPS for webhooks in production

### 2. Idempotency

- Handle duplicate webhook events with the event id
- Record processed events
- Respond `200` immediately after acknowledging an event even if processing did not succeed

### 3. Data Flow

- `price_id` must match the products in the Stripe dashboard
- Use Stripe's `customer_id` linked to the app's user
- Use `subscription.status` to gate feature access

### 4. UX

- Show a loading state when pressing subscribe
- Show a clear error if payment fails
- Let users manage billing themselves

- Use /open-web-for-config-secret if needed (service stripe)
- Use /follow-create-product if needed
- Use /follow-create-web if needed
- Use /follow-lib-zod if needed


## Expected Outcome

- Stripe SDK installed and configured correctly
- `/pricing` page with a clear CTA
- Checkout session working
- Subscriptions and customer portal manageable
- Webhook events correct and secure
- `/user/billing` and `/dashboard` display Stripe data
- Ready to deploy to production

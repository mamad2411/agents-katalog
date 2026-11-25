# Stripe Skill

You are integrating Stripe payments. Apply these conventions.

## Setup

- Store `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` as server-only environment variables — never expose on the client.
- Store `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` as a client-exposed variable for Stripe.js.
- Use the official `stripe` Node.js SDK on the server; use `@stripe/stripe-js` on the client.
- Initialize the server SDK once:
  ```ts
  import Stripe from 'stripe';
  export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-12-18.acacia' });
  ```

## Checkout Session

- Create Checkout Sessions on the server; return the session URL to the client for redirect.
- Always set `success_url` and `cancel_url` with `?session_id={CHECKOUT_SESSION_ID}` in `success_url` for verification.
- Use `metadata` to attach order/user IDs to the session for webhook reconciliation.
- Enable `automatic_tax: { enabled: true }` for tax calculation.

## Webhooks

- Verify every webhook signature before processing:
  ```ts
  const event = stripe.webhooks.constructEvent(rawBody, signature, process.env.STRIPE_WEBHOOK_SECRET!);
  ```
- Use the raw request body (Buffer) for verification — JSON parsing the body before this step will break signature validation.
- Handle `checkout.session.completed`, `payment_intent.succeeded`, `invoice.payment_failed`, and `customer.subscription.deleted` at minimum.
- Make webhook handlers idempotent — Stripe may deliver the same event more than once.

## Subscriptions

- Create a `Customer` object for each user and store `stripe_customer_id` in your database.
- Use `customer.subscription.updated` and `customer.subscription.deleted` to sync subscription status.
- Store `current_period_end` and `status` in your DB — never re-fetch Stripe on every request for gating logic.

## Testing

- Use Stripe test mode keys in development; never use real keys in tests.
- Use the Stripe CLI to forward webhooks: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`.
- Use [`stripe trigger` commands](https://stripe.com/docs/cli/trigger) to fire test events.

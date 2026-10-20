---
name: follow-service-stripe-setup-stripe
description: Install the Stripe SDK (server/client), prepare API keys from the dashboard, and set up webhook signing for local dev — first-time setup only
related:
  - follow-service-stripe
---

## Goal

Install the Stripe SDK (server/client), prepare API keys from the dashboard, and set up webhook signing for local dev — first-time setup only

## Scope

- Install `stripe`, `@stripe/stripe-js`, and the Stripe CLI
- Create and store `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`
- Init the server client and webhook forwarding
- Does not cover products/prices/webhook endpoint config → use `workflows/config-stripe/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: Confirm the current state before installing (idempotent)

1. Read `package.json` to identify runtime and package manager
2. Check whether `stripe`/`@stripe/stripe-js` are already installed → if so, skip to verify
3. Do `/check-secrets env-vars` to see whether Stripe keys already exist
4. If there is no Stripe account → stop and tell the user to create one from the dashboard

### 2. Install SDKs And CLI

> Goal: Install the needed dependencies

1. Install the server SDK with `bun add stripe`
2. Install the client SDK with `bun add @stripe/stripe-js` if the client side must call Stripe.js
3. Install the Stripe CLI with `mise use -g stripe` or `scoop install stripe`
4. Log in the CLI with `stripe login`

### 3. Store Keys And Init Client

> Goal: Prepare keys securely and init the client

1. Open Developers > API keys in the dashboard — use `/open-web-for-config-secret` (service stripe)
2. Store `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` in `/follow-secret-manager`, not the real `.env`
3. Start with test mode keys — never use live keys in dev
4. Init the server client with `new Stripe(process.env.STRIPE_SECRET_KEY!)` — if pinning `apiVersion` is needed, check official docs

### 4. Setup Webhook Signing

> Goal: Configure the webhook secret for local dev

1. Run `stripe listen --forward-to http://localhost:<port>/api/webhooks/stripe`
2. Copy `whsec_...` from the output into `STRIPE_WEBHOOK_SECRET` in `/follow-secret-manager`
3. Verify events with `stripe.webhooks.constructEvent(rawBody, signature, secret)` — the raw request body is required
4. Do `/run-verify` and trigger a test event with `stripe trigger <event>` — if it fails → `resolve-errors` max 3 rounds

## Rules

- Never hardcode keys or commit secrets — always use `/follow-secret-manager`
- `STRIPE_SECRET_KEY` is server-side only — the client uses the publishable key
- Webhooks must always verify the signature with the raw body
- Always use test mode first — live keys only at go live
- If unsure about an API/option → check official docs or `learn` (web)

## Expected Outcome

- Stripe SDKs and CLI installed and ready
- All three keys secure and correctly injected
- Webhook forwarding + signature verification working locally

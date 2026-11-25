---
name: payment-integration-safety
description: Builds or reviews payment code so amounts are set on the server, webhooks are verified and idempotent, and every charge can be reconciled with the provider.
---

# Payment integration safety

Money code is reviewed line by line. Use test mode and test keys only.

## Steps

1. Map the flow: where the price is set, where the charge is created, what confirms it, what fulfills the order. Draw it as five lines of text before changing anything.
2. Amounts: compute the total on the server from stored prices and quantities. Reject any amount, currency or price id taken from the client. Store money as integer minor units, never floats.
3. Confirmation: fulfill an order only from a verified webhook (or a server-side fetch of the payment status), never from the browser redirect.
4. Webhooks: verify the signature on the raw request body before parsing JSON. Reject old timestamps. Return 2xx quickly and do the heavy work in a job.
5. Idempotency: send an idempotency key on every create-charge call, derived from the order id. In the webhook handler, store the provider event id with a unique constraint and skip events already seen.
6. State: model the order as explicit states (pending, paid, failed, refunded) and allow only valid transitions. Handle out-of-order events.
7. Reconciliation: write or check a job that compares provider payments with local orders daily and lists mismatches.
8. Test the unhappy paths: declined card, duplicate webhook, webhook before redirect, partial refund.

## Rules

- Never log card data, full tokens or webhook secrets. Read keys from environment variables.
- Do not store card numbers. Use the provider's hosted fields or checkout.
- Do not run anything against live mode.

## Report

Findings ranked by money at risk, each with file, line and fix, then the tests added.

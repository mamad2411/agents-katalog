---
name: chargebee-billing-integration
description: Core Chargebee API integration patterns, customers, subscriptions, invoices, hosted checkout and portal pages under Product Catalog 2.0. Use when writing server code that talks to the Chargebee API.
---

# Chargebee Billing Integration

Base URL: `https://{site}.chargebee.com/api/v2/` (test sites are their own
site, typically `{site}-test`). Auth is HTTP Basic: API key as username,
empty password. Requests are form-encoded, responses JSON. Server-side only;
never expose full-access keys to browsers or apps.

```bash
curl https://acme-test.chargebee.com/api/v2/customers \
  -u "$CHARGEBEE_API_KEY:" \
  -d first_name="Ada" -d email="ada@example.com"
```

Official SDKs exist for Node, Python, Ruby, PHP, Java, .NET, Go; prefer them
over raw HTTP for retries and typing.

## Product Catalog 2.0 model

Modern sites use PC 2.0: **items** (plan, addon, charge) with **item
prices** (currency + billing period variants, IDs like
`silver-USD-monthly`). Subscriptions reference item price IDs. If the site
is PC 1.0 (legacy `plans`/`addons` endpoints), the shapes differ; check
which catalog version the site runs before writing code.

## Core objects and calls

- **Customer**: `POST /customers`, `GET /customers/{id}`. Attach payment
  methods via hosted pages or a gateway token, not raw card data.
- **Subscription**: `POST /customers/{id}/subscription_for_items` with
  `subscription_items[item_price_id][0]`, quantities, coupons, trial.
  Update with `POST /subscriptions/{id}/update_for_items` (proration is
  controlled by `prorate`). Cancel with `POST /subscriptions/{id}/cancel_for_items`
  (`end_of_term=true` for graceful cancel).
- **Invoice**: generated automatically on renewals; list with
  `GET /invoices?subscription_id[is]={id}`; one-off charges via
  `POST /invoices/create_for_charge_items_and_charges`.

## Hosted pages (let Chargebee own PCI scope)

Server creates a session, client redirects or opens it:

- Checkout for a new subscription:
  `POST /hosted_pages/checkout_new_for_items`
- Change an existing subscription:
  `POST /hosted_pages/checkout_existing_for_items`
- Manage payment method: `POST /hosted_pages/manage_payment_sources`
- Self-serve portal: `POST /portal_sessions` then open the returned URL.

After the user completes checkout, either consume the redirect's
`hosted_page id` (`GET /hosted_pages/{id}` for the created subscription) or,
more robustly, wait for the webhook (see `chargebee-webhooks`).

## Request discipline

- **Idempotency**: send `chargebee-idempotency-key: <uuid>` on POSTs.
  Replays return the cached response with `chargebee-idempotency-replayed:
  true`. Window is 30 minutes; the retry must match path, body, and headers
  exactly or you get a 422. Estimate APIs do not support it.
- **Pagination**: list endpoints take `limit` (max 100) and return
  `next_offset`; pass it back as `offset` until absent.
- **Filters**: string DSL in query params, e.g. `status[is]=active`,
  `updated_at[after]=<unix_ts>`, `sort_by[desc]=created_at`.
- **Rate limits**: on 429, back off and retry with jitter; batch heavy
  reads with `updated_at` filters instead of full scans.
- **Estimates**: preview proration and totals with the Estimate endpoints
  (e.g. `POST /estimates/update_subscription_for_items`) before mutating.

## Practices

- Store Chargebee IDs (customer, subscription) on your own user records;
  treat Chargebee as the billing source of truth.
- Drive access control from subscription `status`
  (`in_trial`, `active`, `non_renewing`, `paused`, `cancelled`).
- Keep all mutation endpoints behind your backend; the client only ever
  sees hosted page URLs and portal sessions.

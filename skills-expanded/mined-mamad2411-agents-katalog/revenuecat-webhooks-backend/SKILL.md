---
name: revenuecat-webhooks-backend
description: Handle RevenueCat webhooks and server-side entitlement checks, event types, retry semantics, idempotency, and the REST v1/v2 APIs. Use when building backend code that reacts to subscription events or gates access server-side.
---

# RevenueCat Webhooks and Backend

Configure under Integrations > Webhooks: HTTPS endpoint, an authorization
header value you generate, environment scope (production / sandbox / both),
optional per-event filtering.

## Endpoint contract

- Verify the `Authorization` header on every request; reject mismatches.
- Return 200 quickly (enqueue heavy work). Non-200 responses are retried up
  to 5 times with growing delays (5, 10, 20, 40, 80 minutes), then dropped,
  so ordering is NOT guaranteed and duplicates are possible.
- Deduplicate on the event `id` field; store processed IDs.
- Because retries reorder events, treat the webhook as a trigger and fetch
  the subscriber's current state from the REST API before flipping access.

## Payload shape

JSON body with a single `event` object: `type`, `id`, `app_user_id`,
`original_app_user_id`, `product_id`, `entitlement_ids`, `period_type`,
`purchased_at_ms`, `expiration_at_ms`, `environment` (`SANDBOX` /
`PRODUCTION`), `store`, price fields. Always branch on `environment`.

## Event types worth handling

- `INITIAL_PURCHASE`: first purchase of a subscription.
- `RENEWAL`: successful renewal, including billing recovery.
- `CANCELLATION`: auto-renew turned off or refund; access usually continues
  until expiration, so do not revoke immediately.
- `UNCANCELLATION`: user re-enabled auto-renew before expiring.
- `EXPIRATION`: access actually ended; revoke here.
- `BILLING_ISSUE`: renewal charge failed; start dunning UX (email, in-app
  banner, payment-update deep link).
- `PRODUCT_CHANGE`: plan switch.
- `SUBSCRIPTION_PAUSED` (Play), `TRANSFER` (entitlement moved between app
  user IDs), `NON_RENEWING_PURCHASE` (consumables, lifetime), `TEST` (sent
  from the dashboard test button).

Minimal state machine: grant on `INITIAL_PURCHASE`/`RENEWAL`, flag on
`BILLING_ISSUE`, revoke only on `EXPIRATION`, and reconcile on `TRANSFER`.

## Server-side entitlement checks (REST v1)

Base `https://api.revenuecat.com/v1`, secret key auth:

```bash
curl https://api.revenuecat.com/v1/subscribers/$APP_USER_ID \
  -H "Authorization: Bearer $REVENUECAT_SECRET_KEY"
```

Read `subscriber.entitlements.<id>.expires_date`: active if null (lifetime)
or in the future. This GET creates the subscriber if missing, so validate
IDs first. Useful writes: grant promotional entitlements
(`POST /subscribers/{id}/entitlements/{entitlement_id}/promotional`) and
delete subscribers for GDPR erasure.

## REST v2

Base `https://api.revenuecat.com/v2`, uses **API v2 secret keys**,
project-scoped resources (`/projects/{project_id}/...` for apps, products,
entitlements, offerings, customers). Prefer v2 for configuration automation;
v1 remains the workhorse for subscriber reads and promotional grants.

## Practices

- Never trust client-reported entitlement state for server-gated features;
  check the API or your webhook-synced database.
- Keep webhook processing idempotent and side-effect-safe on replays.
- Log the full event body on failure; RevenueCat's dashboard shows delivery
  attempts per event for debugging.
- Rotate the webhook auth header value and secret keys on suspected leaks.

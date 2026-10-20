---
name: athena-billing
description: Implement, integrate, inspect, debug, document, or test Athena billing across the main Athena workspace. Use for `/billing/v1`, `/admin/billing`, `/admin/webhook-sinks/helpers/billing`, provider webhook ingestion, `/webhook-sinks/mollie`, Mollie 401/BILLING_ADAPTER_FAILED, balance-transaction enrichment, billing grants, webhook sink provisioning, canonical billing SQL tables, `billing.billing_provider_connections`, `athena.webhook_sink_events`, `billing.billing_projection_events`, provider connection config/apiKey credential_kind, route-manifest parity, and the `@xylex-group/athena/billing` client when the task is primarily billing-domain work rather than general SDK exports. Use when the user runs /athena-billing or pastes Mollie sink enrichment errors.
---

# Athena Billing

Work from the Athena monorepo. Read the billing route contract and the specific runtime seam before editing anything.

## Establish the contract

1. Read [references/route-spine.md](references/route-spine.md) for the billing HTTP surface, route inventory, and JS/Rust parity files.
2. Read [references/implementation-map.md](references/implementation-map.md) for the exact crate, runtime, SQL, and JS files that own the requested seam.
3. Read [references/persistence-and-webhooks.md](references/persistence-and-webhooks.md) when the task touches webhook sinks, projection ledgers, canonical tables, grants, or provisioning.
4. Read [references/mollie-auth-and-tables.md](references/mollie-auth-and-tables.md) for Mollie sink enrichment, table map, and **which auth failed** (webhook signature vs outbound API Bearer).
5. Read the nearest tests, SQL, and docs before changing behavior.

When artifacts disagree:

- Treat `crates/athena-billing/src/live_http_routes.rs` and `contracts/billing/live-http-routes.json` as the live route inventory.
- Treat `packages/athena-js/src/billing/module.ts` as the JS billing client contract.
- Treat `src/data/billing*.rs` plus the billing crates as authoritative for runtime behavior.
- Treat checked-in SQL and billing docs as the operator and persistence contract that must stay in sync.

## Route the task

### Public billing routes and JS client

Start with the route spine and `packages/athena-js/src/billing/{index,module}.ts`. Preserve `billingSdkManifest`, `billingLiveHttpRoutes`, root/browser exports, `client.billing` wiring, static-admin-key headers, provider webhook raw-body behavior, and `jwt_secret` query handling for `/debug/billing`. If the task broadens into non-billing SDK exports, use `$athena-js` too.

### Provider webhook ingestion and projection

Start with `src/data/billing.rs`, `src/data/billing_fanout.rs`, `src/api/webhook_sinks.rs`, `config/webhook-sinks.yaml`, and the billing architecture docs. Trace the full path:

`athena.webhook_sink_events -> billing.billing_provider_connections -> (optional outbound provider API) -> billing.billing_projection_events -> canonical billing document -> billing.billing_webhook_events`

Preserve immutable raw ingress evidence, sanitized projection failures, shared fanout, and provider verification semantics.

**Mollie sink enrichment 401 checklist** (full detail: [mollie-auth-and-tables.md](references/mollie-auth-and-tables.md)):

- **Table:** `billing.billing_provider_connections` on sink **`client_name`** Postgres; **`id` = log `connection_id`**.
- **Defaults:** `mode=live`, `status=pending` (use `active`), `credential_kind=api_key` (Mollie) / `secret_key` (Stripe); `config.apiBaseUrl=https://api.mollie.com`; **no default for `config.apiKey`**.
- **Token families:** `live_`/`test_` → `api_key`; **`access_…` → `advanced_access_token` / `organization_access_token`** (alias; needs **`profileId`** + usually **`payments.read`**).
- **Outbound Bearer:** only **`config.apiKey`**. **Inbound HMAC:** only **`config.signingSecrets`**.
- **Hygiene:** `btrim(provider_profile_id)` must equal `config.profileId` (leading space caused real ops confusion).
- **Isolate:** `curl -H "Authorization: Bearer …" https://api.mollie.com/v2/payments?limit=1` — **200** means Mollie OK; remaining failures are Athena routing/config load.
- **Symptom:** raw archive OK + `BILLING_ADAPTER_FAILED` / 401 on `balance-transaction.created` → outbound `get_payment`, not webhook signature.

### Canonical billing persistence and SQL

Start with `sql/billing.sql`, `sql/webhook_sink_projection_targets.sql`, related migrations, and the storage/projection code in the billing crates and root runtime. Keep canonical tables, projection ledgers, helper SQL, and seed/provisioning artifacts synchronized.

### Grants, providers, and provisioning helpers

Start with `crates/athena-billing/src/grants.rs`, provider discovery/admin routes, `GET /admin/webhook-sinks/helpers/billing`, and `POST /admin/billing/clients/{client_name}/webhook-sinks/provision`. Preserve additive grant metadata, provider config descriptors, translated rights, and helper payload shapes.

## Core rules

- Keep route-manifest parity explicit: update Rust inventory, JSON mirrors, JS manifest/tests, and docs together.
- Preserve provider-neutral canonical DTOs on `/billing/v1`; do not leak provider SDK-native objects into public contracts.
- Keep raw transport evidence in `athena.webhook_sink_events`; do not duplicate it into billing tables unless the current contract already does.
- Keep `billing.billing_projection_events` focused on verification/projection state, canonical document correlation, and normalized snapshots.
- Preserve shared post-upsert fanout and Athena Auth sync semantics.
- Prefer additive compatibility over broad billing rewrites unless removal is explicitly requested.
- When changing Mollie/Stripe adapter errors, keep operator messages explicit about **which auth channel** failed (inbound signature vs outbound API credential), and include `connection_id` + redacted token hints — never full secrets.
- Do not confuse billing connections with storage catalogs: storage API `s3_id` is `athena.s3_catalogs.id`; secrets there use `ATHENA_STORAGE_SECRET_ENCRYPTION_KEY`.

## Validation

Use the narrowest proof for the seam:

- JS billing client: `packages/athena-js/test/billing-client.test.ts`
- Route inventory parity: `packages/athena-js/test/billing-contract-spine.test.ts`, Rust live-route tests, and the contract export when needed
- Runtime webhook/projector changes: focused Rust billing/runtime tests plus the relevant SQL/docs sync checks
- Operator/provisioning docs or helper changes: verify helper routes, checked-in SQL, and docs stay aligned

Do not treat a formatter as proof for billing route or ingestion behavior.

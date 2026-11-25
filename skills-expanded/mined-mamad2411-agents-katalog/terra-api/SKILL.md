---
name: terra-api
description: Best practices for integrating Terra API – the unified health & fitness data API for 500+ wearables (Garmin, Fitbit, Oura, Whoop, Apple Health, Strava, Dexcom). Use when building with Terra API or tryterra.co, handling terra-signature (X-Terra-Signature) webhooks, storing wearable health data (activity, sleep, daily, body, nutrition, menstruation, hormone), managing device connections, or merging data across multiple devices.
license: MIT
compatibility: Requires network access to docs.tryterra.co for full API schemas
metadata:
  author: terra
  version: "1.0.0"
---

# Terra API Best Practices

Production-tested guidelines for building with Terra API. Contains rules across 5 categories, prioritized by impact, distilled from a real multi-device integration.

## When to Apply

Reference these guidelines when:

- Implementing or reviewing a Terra API webhook endpoint
- Designing storage for wearable health data (activity, sleep, daily, body, nutrition, menstruation, hormone, athlete)
- Building device connection flows (auth, deauth, reauth, scopes)
- Handling data from users with multiple connected devices
- Writing tests for a Terra API integration

## Rule Categories by Priority

| Priority | Category                    | Impact     | Prefix      |
| -------- | --------------------------- | ---------- | ----------- |
| 1        | Webhook Handling            | CRITICAL   | `webhooks-` |
| 2        | Data Handling & Idempotency | CRITICAL   | `data-`     |
| 3        | Auth & Connection Lifecycle | HIGH       | `auth-`     |
| 4        | Multi-Device Data           | MEDIUM     | `devices-`  |
| 5        | Testing                     | LOW-MEDIUM | `testing-`  |

## Quick Reference

### 1. Webhook Handling (CRITICAL)

- `webhooks-verify-raw-body` - Verify the signature header HMAC (terra-signature / X-Terra-Signature, read case-insensitively) over the raw unaltered body before parsing JSON
- `webhooks-ack-within-timeout` - Return 200 within the timeout (8s default), process async
- `webhooks-dedupe-terra-reference` - Deduplicate deliveries on X-Terra-Trace-Id; terra-reference is shared by all chunks of a large request
- `webhooks-archive-raw-payloads` - Archive raw payloads to object storage, link rows via a payload key
- `webhooks-handle-informational-events` - Route non-data events explicitly, unwrap s3_payload deliveries, never crash on unknown types

### 2. Data Handling & Idempotency (CRITICAL)

- `data-natural-keys` - Key activity/sleep by summary_id, daily-type data by (connection, date), hormone by timestamp
- `data-date-part-only` - Slice the date from the ISO string before any timezone conversion
- `data-superset-overwrite` - Standard fields follow the superset guarantee; overwrite when X-Terra-Ordering-Timestamp is newer or equal
- `data-coalesce-enrichment-scores` - Enrichment scores break the superset guarantee, COALESCE so nulls never overwrite
- `data-columns-over-blobs` - Extract metrics into typed columns, keep raw payloads in object storage
- `data-timestamp-localization` - Respect the timestamp_localization flag, pick one storage policy deliberately

### 3. Auth & Connection Lifecycle (HIGH)

- `auth-reference-id` - Pass your user ID as reference_id, it is the join key in every webhook
- `auth-handle-all-events` - Handle all seven auth event types with idempotent upserts
- `auth-reauth-id-swap` - user_reauth issues a new Terra user ID, swap old for new
- `auth-parse-scopes` - Parse comma-separated scope strings; apply scopes_added/scopes_removed on permission_change
- `auth-reconcile-connections` - Reconcile against Terra API state on page mount, auth redirect, and a schedule
- `auth-integrations-endpoint-headers` - Send dev-id to the public integrations catalogue; without it you get every provider, not your enabled set

### 4. Multi-Device Data (MEDIUM)

- `devices-expect-cross-device-duplicates` - The same session arrives once per device with different summary_ids; your app owns the merge policy
- `devices-enrichment-provider-agnostic` - Enrichment scores are provider-agnostic and comparable, but only present when score weightings are active

### 5. Testing (LOW-MEDIUM)

- `testing-mock-boundaries` - Mock the SDK, database, and background tasks; make async processing eager
- `testing-cover-event-edge-cases` - Test replays, empty data arrays, unknown users, type 0, enrichment nulls, reauth swaps

## How to Use

Read the individual rule file in `rules/` when working on that area, e.g. read `rules/webhooks-verify-raw-body.md` and its siblings before writing a webhook endpoint. Each rule has incorrect/correct code examples and links to the relevant [docs.tryterra.co](https://docs.tryterra.co) page (append `.md` to any docs URL for a markdown version). If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch those pages instead.

## Related Terra API Surfaces

This skill covers the core Health & Fitness API integration. Terra API also offers mobile SDKs for on-device sources (Apple Health, Samsung Health, Health Connect), a realtime Streaming API over websockets, an MCP server exposing health-data query tools to AI agents, planned workouts and routes (write-to-device products), and lab reports. See [docs.tryterra.co](https://docs.tryterra.co) for those surfaces.

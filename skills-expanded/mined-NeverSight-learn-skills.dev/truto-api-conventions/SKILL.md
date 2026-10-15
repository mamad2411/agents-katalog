---
name: truto-api-conventions
description: Truto API conventions — base URL (https://api.truto.one), Bearer auth, unified/proxy/custom URL patterns, cursor pagination, idempotency, admin filter syntax, and skill routing between `truto` (app code) and `truto-cli` (terminal). Load whenever calling, configuring, or reasoning about any api.truto.one endpoint.
---

# Truto API Conventions

## Skill Routing

This plugin has two skills with distinct roles:

- **Truto** skill — Use when writing code in the user's project that calls `api.truto.one`. This produces application code: `fetch()` calls, webhook handlers, connection flows.
- **Truto CLI** skill — Use when running terminal commands to set up, explore, or debug. This runs `truto` CLI commands in the shell for admin tasks, one-time data access, and troubleshooting. Nothing the CLI does belongs in the user's codebase.

## Base URL

```
https://api.truto.one
```

## Authentication

All API requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <api_token>
```

API tokens are scoped to a single environment. When using an API token, operations that require an `environment_id` are automatically scoped to the token's environment.

## Content-Type

- JSON requests: `Content-Type: application/json`
- File uploads: `Content-Type: multipart/form-data`
- Workflows also accept `Content-Type: application/yaml`

## Unified API URL Pattern

```
https://api.truto.one/unified/{model_name}/{resource_name}
```

- **List**: `GET /unified/{model}/{resource}?integrated_account_id={id}`
- **Get**: `GET /unified/{model}/{resource}/{id}?integrated_account_id={id}`
- **Create**: `POST /unified/{model}/{resource}?integrated_account_id={id}`
- **Update**: `PATCH /unified/{model}/{resource}/{id}?integrated_account_id={id}`
- **Delete**: `DELETE /unified/{model}/{resource}/{id}?integrated_account_id={id}`
- **Custom method**: `POST /unified/{model}/{resource}/{method_name}?integrated_account_id={id}`

The `integrated_account_id` query parameter is **required** on all unified, proxy, and custom API calls.

## Proxy API URL Pattern

```
https://api.truto.one/proxy/{resource}?integrated_account_id={id}
```

Pass-through to the native API of the integrated tool. Same HTTP methods as unified.

## Custom API URL Pattern

```
https://api.truto.one/custom/{path}?integrated_account_id={id}
```

Any HTTP method; the path after `/custom/` is forwarded to the integration's custom handler.

## Pagination

List endpoints return cursor-based pagination:

```json
{
  "result": [...],
  "next_cursor": "cursor_value_or_null",
  "prev_cursor": "cursor_value_or_null"
}
```

Pass `next_cursor` as a query parameter to fetch the next page. When `next_cursor` is `null`, there are no more pages.

## Idempotency

Mutating unified/proxy/custom API calls support idempotency via the `Idempotency-Key` header:

```
Idempotency-Key: <unique_key>
```

## Admin API Pagination

Admin endpoints (listing integrations, accounts, sync jobs, etc.) use the same cursor pattern. Filter parameters use structured query syntax: `field[operator]=value` (e.g., `id[in]=uuid1,uuid2`).

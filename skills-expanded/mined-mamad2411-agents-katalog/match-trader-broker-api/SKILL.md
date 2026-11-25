---
name: match-trader-broker-api
description: >
  Integrate with the Match-Trader Broker API v2 (broker-api-v2) — the REST + gRPC
  API for connecting directly to the Match-Trader trading platform. Use this skill
  to build, call, or debug broker-api-v2 requests: create and manage user accounts
  and trading accounts, run balance operations (deposit, withdraw, credit-in,
  credit-out), open/close/edit positions, place pending and correction orders,
  query trading data (open/closed positions, orders history, ledgers, candles,
  groups, symbols, platform logs), use the Prediction Market (bets/outcomes), and
  consume the real-time gRPC streams (equity, positions, orders, quotations,
  groups, symbols, account info, ledgers, trading events). Covers Bearer-token
  authentication, the per-broker base-URL pattern, optimistic locking via the
  `version` field, non-idempotent balance ops, RFC-3339/GMT time, pagination,
  rate limits, the full error catalogue, and a troubleshooting decision tree.
  Triggers: "broker-api-v2", "Match-Trader Broker API", "broker api v2", MTR
  broker API, create trading account, deposit/withdraw broker api, gRPC equity
  stream, Match-Trader integration.
metadata: { version: 1.0.0 }
license: MIT
---

# Match-Trader Broker API v2

REST + gRPC API for direct integration with the **Match-Trader** platform: user &
trading accounts, balance operations, dealing (positions/orders), read-only
trading data, Prediction Market, and real-time gRPC streams. Each broker has a
unique `brokerID` encoded in the token — you never pass it in requests.

## 20-second essentials

| Thing | Value |
|---|---|
| Protocols | **REST** (HTTPS) + **gRPC** (HTTP/2, server-streaming) |
| Auth | `Authorization: Bearer <token>` on every request (REST header & gRPC metadata) |
| Base URL (prod) | `https://broker-api-v2-<clientName>.match-trader.com` |
| Base URL (demo/UAT) | `https://broker-api-v2-demo.match-trader.com` (shared sandbox, `brokerID=0`) |
| gRPC host (demo) | `grpc-broker-api-v2-demo.match-trader.com` (TLS on public hosts; default port 8083) |
| REST prefix | `/v1/...` |
| Time | Server time is **GMT (UTC+0)**; datetimes are **RFC 3339** (e.g. `2024-01-13T09:20:04.651Z`) |
| Rate limit | **500 requests/minute** (default) |
| Content-Type | `application/json` |

## The gotchas that bite (read before coding)

1. **Optimistic locking on trading-account updates.** `PATCH /v1/trading-accounts/{login}`
   requires the current `version`. Omitting it → validation error; a stale value →
   rejection. Always GET → send `version` → on conflict re-GET and retry.
   See `references/trading-accounts.md`.
2. **Balance operations are NOT idempotent.** `deposit`, `withdraw`, `credit-in`,
   `credit-out` apply the adjustment *every* time you call them. A retry after a
   network timeout can double-book. Use your own dedup key + reconcile.
   See `references/balance-operations.md`.
3. **Trade endpoints return an acknowledgement, not post-trade state.** A `200`
   means "accepted", not "filled". Bulk/multi ops return `partialResponses` where
   individual items can fail (failure field is `errorMessage`). Confirm via
   trading-data or the gRPC streams. See `references/trading.md`.
4. **`accessRightsFilter` is the current filter name** (older `accessRights` /
   `accessTypeFilter` are deprecated). `GET /v1/candles` uses `size` (0–1000), not
   `amount`. See `references/troubleshooting.md`.
5. **Know your `brokerID`.** The public Theneo sandbox uses `brokerID=0`, shared
   across all integrations (you'll see others' test data). A *provisioned* demo or production
   instance is scoped to your own dedicated broker. Either way the demo
   environment can be unstable (occasional
   `5xx`/timeouts) — don't infer production isolation or uptime from it.
6. **`Create User Account` rejects duplicates with `409`** (error
   `type: error://broker-api/user-account/already-exists`). Older builds historically
   returned `200` and silently minted a new UUID, so still treat email as unique on
   your side and check before create. See `references/user-accounts.md`.
7. **A `groups`-scoped trading-data query can return logins that aren't yours.**
   Filtering `open-positions` / `closed-positions` / `ledgers` / etc. by
   `groups[]` returns everything in that group — on a shared group that can
   include other integrations' accounts, not just the ones you provisioned.
   Verify every returned `login` via `GET /v1/trading-accounts/{login}` (it can
   `404`, or belong to someone else) before treating it as your own.

## How to use this skill

- **Make a REST call (sandbox-default, safe):** `scripts/broker_api.py` — token
  auth, env switch, JSON error parsing, automatic retry on `version` conflict,
  pagination helper. Reads creds from `.local.md` (copy `.local.md.example`).
- **Look up an endpoint:** `references/endpoints-rest.md` (all 46, by section) or
  `scripts/endpoints.json` (machine-readable, full field schemas).
- **Consume a gRPC stream:** `references/grpc-streaming.md` +
  `assets/broker_api_v2.proto` + `scripts/grpc_quickstart.py`.
- **Other languages:** `assets/snippets/` (cURL, Node.js/TS, Java incl. gRPC).
- **When something fails:** `references/troubleshooting.md` (decision trees).

## Reference index

| File | What's in it | Request / Response |
|---|---|---|
| `references/environments.md` | Base URLs, per-broker pattern, gRPC host/port, TLS, rate limit, time | — |
| `references/authentication.md` | Bearer token, REST header vs gRPC metadata, how to obtain/rotate | — |
| `references/endpoints-rest.md` | All 46 REST endpoints by section (method, path, body, query, codes) | Request |
| `references/user-accounts.md` | User-account lifecycle, duplicate/409, bulk delete, change password | Both |
| `references/trading-accounts.md` | Create/update, **optimistic locking**, account types, access rights, groups | Both |
| `references/balance-operations.md` | deposit/withdraw/credit-in/out, **non-idempotency**, 204 semantics | Request |
| `references/trading.md` | open/close/edit/reopen, pending & correction orders, ack model, partials | Both |
| `references/trading-data.md` | Read endpoints, filters, pagination, candles (`size`≤1000), position↔ledger correlation | Both |
| `references/prediction-market.md` | Bets/outcomes, YES/NO PRED instruments, how to trade them, worked P&L example | Both |
| `references/grpc-streaming.md` | 9 streams, heartbeat, stub generation, reconnection | Both |
| `references/enums.md` | All enums (REST + gRPC): account types, sides, statuses, ledger types… | Both |
| `references/troubleshooting.md` | Symptom → check → fix decision trees | — |
| `references/error-model.md` | Standard error body, status codes, what each means | Response |

Response field schemas live in `scripts/endpoints.json` (`response` key, added
alongside `body`) and worked examples in `assets/examples/*_response.json` —
the reference `.md` files above point into both.

## Status codes (standard across the API)

`200` OK · `204` No Content (balance ops, some updates) · `400` Bad Request
(validation) · `401` Unauthorized (missing/invalid token) · `403` Forbidden (token
valid, no permission/scope) · `404` Not Found (e.g. unknown user on account create)
· `409` Conflict (duplicate / version) · `500` Internal Server Error. Error bodies
follow `{status, title, detail, path, type?, timestamp}` — see `references/error-model.md`.

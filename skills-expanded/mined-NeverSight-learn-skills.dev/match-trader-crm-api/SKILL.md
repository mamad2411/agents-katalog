---
name: match-trader-crm-api
description: >
  Integrate with the Match-Trade CRM-API (a.k.a. Broker-API CRM layer) over REST and
  gRPC. Use this skill to build, sign, send and debug calls to the Match-Trader CRM:
  authenticate with a Bearer API key, create and update accounts and trading accounts,
  read offers / branches / roles / payment-gateways, make manual deposits and withdrawals,
  credit in/out, change password and leverage, open / close / edit positions and orders,
  pull trading data (open & closed positions, ledgers, balance snapshots), read CRM
  timeline events, send inbox notifications, generate One-Time-Token (OTT) SSO links,
  work with Prop Trading v2 (challenges, competitions, evaluations, add-ons, snapshots),
  and Prediction Market bets/outcomes. Covers the gRPC streaming services (account,
  positions, ledger, orders, quotations, group, trading-events, symbols, equity, prop)
  and CRM-event webhooks. Triggers: "Match-Trader CRM API", "crm-api", "broker api",
  "match-trade integration", "create trading account API", "manual deposit API",
  partnerID, offerUuid, systemUuid, Bearer token 401/403, error 415/500 "Internal
  application error", "Invalid apiToken", gateway currency mismatch, OTT / SSO login.
metadata: { version: 1.0.0 }
license: MIT
---

# Match-Trader CRM-API

REST + gRPC API exposing a broker's **Match-Trade CRM** and trading backend to external
tools (risk systems, custom client offices, back-office, sales/lead tools, reporting).
If you instead need to drive the platform **without** the CRM layer, that is a different
product (Broker-API v2) — this skill is the **CRM** integration point.

> Read this page first, then open the `references/` file for your task. Runnable helpers
> are in `scripts/`. Copy `.local.md.example` → `.local.md` and put your token there.

## 20-second start

```bash
# 1. put your token in .local.md  (apiKey: <token>, baseURL: <sandbox or prod>)
# 2. prove connectivity + auth (defaults to sandbox):
python scripts/smoke_test.py
# 3. make calls:
python scripts/crm_api.py GET  v1/offers
python scripts/crm_api.py POST v1/deposits/manual --body '{"systemUuid":"...","login":"...","paymentGatewayUuid":"...","amount":150}'
```

```python
from crm_api import CrmApiClient
c = CrmApiClient()                 # sandbox + token from .local.md, auth_scheme="bearer"
offers = c.get("v1/offers")        # -> {"offers":[...]}
for acc in c.iter_items("v1/accounts", params={"accountType": "ALL"}):
    ...
```

## Environments

| Env | REST base URL | gRPC host | partnerID |
|---|---|---|---|
| **Sandbox / UAT** | `https://crm-api-demo.match-trader.com` | `grpc-broker-api-demo.match-trader.com` (port **8083**) | **0** (shared!) |
| **Production** | broker-specific (issued with your prod key) | broker-specific | your own |

- **Sandbox `partnerID=0` is SHARED** across all integrators. You will see other people's
  test data; never push real/sensitive data; filter results to logins/accounts you created.
- Server time is **GMT (UTC+0)**. All timestamps are **RFC 3339** (`2024-01-13T09:20:04.651Z`),
  sometimes with nanoseconds in responses.
- Rate limits: **500 req/min** standard, **200 req/min** bulk/resource-intensive. → `references/errors-and-troubleshooting.md`
  - Tiering is by **response shape, not URL naming**: an endpoint that returns aggregate/bulk data
    across many accounts is bulk-tier even if its path doesn't say `-by-logins-or-groups`.

    | Endpoint | Tier | Why |
    |---|---|---|
    | `POST /v1/prop/challenge-statistics` | bulk (200/min) | returns every account in the challenge(s), not one — bulk-shaped despite the plain-looking path |

## Auth in one line

`Authorization: Bearer <apiKey>` on every REST request (gRPC: same value as `authorization`
metadata). The **apiKey is your CRM user's key** — it inherits that user's role + per-endpoint
**API ACCESS** rights. Tokens are valid until revoked. Details + the `Bearer`-vs-raw header
note: `references/authentication.md`. **Confirmed against the UAT environment: `Bearer` is correct.**

## Common integration pitfalls (and how this kit handles them)

1. **415 surfaced as `500 "Internal application error"`** → you didn't send a JSON body with
   `Content-Type: application/json` (e.g. cURL without `--data` raw / wrong content-type). The
   helper always sets it. → `errors-and-troubleshooting.md`
2. **HTML error body, not JSON** → blocked/erroring *before* the app (WAF/CloudFlare/nginx, or
   your **IP isn't whitelisted**). Not your payload. JSON body = application-level. 
3. **`offerUuid` drives everything.** A trading account's currency/leverage/demo-vs-real come
   from the **offer → backend group**, not your request. You cannot create/edit offers, branches
   or roles via API (read-only). Get `systemUuid`/`branchUuid`/`operationUuid` from `GET /v1/offers`.
4. **Manual deposit/withdrawal** needs a gateway with `method: "MANUAL"`, and the **gateway
   currency must match the trading-account currency** (different-currency manual deposits are
   rejected). → `references/payments.md`
5. **Empty fields must be omitted**, not sent as `null`/`""`. Sending empty filters or required
   query params blank → `400`/`500`.
6. **Lead vs Client**: a user is a *Lead* until first successful deposit, then a *Client*.
7. **Response envelopes differ**: `offers`/`paymentGateways`/`branches`/`roles` wrap the list in a
   named key and are **not paginated**; `accounts`/`deposits`/`withdrawals` use the Spring page
   envelope (`content`,`totalPages`,`number`,`size`). → `references/pagination-filtering.md`
8. **`204 No Content` is success** (credit in/out, change-password, change-leverage). Don't treat
   the empty body as an error.
9. **Offers create forex accounts, not prop accounts.** Regular trading accounts come from the
   offer→group flow (`GET /v1/offers` → `POST /v1/accounts` with `offerUuid`). Creating an account
   from an offer does **not** enrol anyone in a challenge or register in the prop system (no
   `propAccountUuid`). Prop accounts are separate and are created/managed through the `v2/prop/*`
   endpoints — including a real create endpoint, `POST /v2/prop/prop-accounts` (pass
   `instantlyActive: true` to create one already active / fee-paid). → `references/prop.md`.
10. **A `groups`-scoped/bulk prop read can return more than you expect.** `POST /v1/prop/challenge-statistics`
    returns every account in the requested challenge(s), unscoped — see the rate-limit note above
    and `references/prop.md`.

## Map of the API → reference files

| You want to… | File | Has worked JSON example? |
|---|---|---|
| Base URLs, ports, partnerID, time, limits | `references/environments.md` | no |
| Token, Bearer scheme, API ACCESS rights, OTT permission | `references/authentication.md` | no |
| The full list of 91 REST endpoints (method + path) | `references/endpoints.md#rest-endpoint-inventory-91-endpoints` | no |
| Create/update accounts & trading accounts, lead→client | `references/accounts.md` | yes |
| Gateways, deposits, withdrawals, credit, statuses | `references/payments.md` | yes |
| Positions, orders, trading-data, ledgers | `references/trading.md` | yes |
| Prop Trading v2: challenges, competitions, evaluations | `references/prop.md#prop-trading-v2` | yes — shapes from official docs + live-verified findings; values illustrative, not captured payloads |
| Prediction Market: bets, outcomes, PRED instruments | `references/prediction-market.md#prediction-market` | no |
| gRPC streaming services, heartbeats, reconnection, error codes | `references/grpc-streaming.md#grpc-streaming` | no |
| CRM events: webhooks + gRPC streams, SSO / One-Time-Token | `references/webhooks-and-events.md` | yes |
| Pagination, sorting, filtering, by-logins-or-groups bodies | `references/pagination-filtering.md#pagination-sorting-filtering` | yes |
| All enums (status, access, types, sides…) | `references/enums.md#enum-catalogue` | no |
| Error model + a troubleshooting decision tree | `references/errors-and-troubleshooting.md` | yes |
| cURL / Node.js / PHP / TypeScript snippets | `references/code-examples.md` | yes |

## Scripts & assets

- `scripts/crm_api.py` — stdlib REST client (auth, JSON content-type, problem+json parsing,
  HTML-vs-JSON detection, pagination, 429/5xx backoff, CLI). Import `CrmApiClient`.
- `scripts/smoke_test.py` — connectivity + auth check (defaults to sandbox); prints the IDs
  (`systemUuid`, `branchUuid`, `offerUuid`) you need next.
- `scripts/grpc_quickstart.py` — gRPC connection/metadata/heartbeat template (bring your `.proto`).
- `references/code-examples.md` also has a full TypeScript port of the same client (auth-scheme
  fallback, HTML-vs-JSON error detection, 429/5xx backoff) for Node/TypeScript integrators.
- `assets/` — example request bodies, read-only Prop V2 payloads, the `500` error envelope, and an
  idempotent webhook handler.

Default to **sandbox**. Only target production after explicit confirmation.

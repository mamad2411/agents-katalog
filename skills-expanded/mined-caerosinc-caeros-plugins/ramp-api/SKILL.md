---
name: ramp-api
description: Call the Ramp developer API, OAuth grant types and scopes, transactions, cards, reimbursements, users, pagination, and environments. Use when writing code against api.ramp.com.
---

# Ramp Developer API

Production base: `https://api.ramp.com/developer/v1`
Sandbox base: `https://demo-api.ramp.com/developer/v1` (separate app +
credentials; each environment is configured independently).
Authoritative reference: https://docs.ramp.com (OpenAPI at
`/openapi/developer-api.json`; text mirrors under `/llms-api.txt` and
`/llms-guides/<slug>.txt`).

## OAuth 2.0

Token endpoint: `POST {base}/token`. Two grant types:

- **client_credentials**: server-to-server, internal integrations. Access
  tokens live 10 days (864000 s). No user consent step.
- **authorization_code**: third-party or user-facing apps. Access tokens
  live 1 hour; use the refresh token proactively rather than waiting for
  401s.

```bash
curl -X POST https://api.ramp.com/developer/v1/token \
  -u "$RAMP_CLIENT_ID:$RAMP_CLIENT_SECRET" \
  -d grant_type=client_credentials \
  -d scope="transactions:read reimbursements:read users:read"
```

Send the result as `Authorization: Bearer <token>`. Request only the scopes
you enabled on the app; a token cannot exceed the app's granted scopes.

## Scopes (request the minimum)

Read: `transactions:read`, `reimbursements:read`, `cards:read`,
`users:read`, `business:read`, `accounting:read`, plus scopes for bills,
departments, merchants, vendors, and funds.
Write (only if the integration truly needs it): `cards:write`,
`users:write`, `accounting:write`. `cards:read_vault` exposes sensitive
card data; avoid unless indispensable.

For analysis and reporting work, stay read-only. Do not build flows that
initiate payments or transfers on someone's behalf; leave money movement to
authorized humans in the Ramp product.

## Core resources

- **Transactions**: `GET /transactions` with filters such as
  `from_date` / `to_date`, `department_id`, `merchant_id`, `min_amount`,
  ordering params. Amounts are typically integer cents; check the field
  units in the OpenAPI spec before doing math.
- **Cards**: `GET /cards`, `GET /cards/{id}`; spend programs and limits
  come through related endpoints (`/limits`, `/spend-programs`).
- **Reimbursements**: `GET /reimbursements` for out-of-pocket expense
  claims and their approval states.
- **Users / departments / locations**: `GET /users`, `GET /departments`,
  `GET /locations` for joining spend to org structure.
- **Accounting**: `GET /accounting/accounts` (GL accounts),
  `GET /accounting/vendors`, `GET /accounting/all-connections` for coding
  and sync status.

## Pagination

Responses are cursor-paginated: `{"data": [...], "page": {"next": "..."}}`
where `page.next` is a complete URL for the next page. Loop until `next`
is absent. Keep `page_size` moderate and add retry-with-backoff on 429s.

## Practices

- Cache the client_credentials token (10-day lifetime); do not mint per
  request.
- Store `client_secret` in a secret manager; rotate on exposure
  (see `ramp-setup`).
- Log Ramp request IDs from error responses when filing support issues.
- Develop against the sandbox first; production data is real corporate
  financial data, so scope reads narrowly and avoid bulk exports you do
  not need.

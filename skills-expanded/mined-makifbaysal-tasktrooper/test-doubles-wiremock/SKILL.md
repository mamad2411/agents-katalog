---
name: test-doubles-wiremock
category: testing
description: Use when a test would otherwise call a real external dependency - replace it with WireMock or an equivalent stub so runs are deterministic, offline, and control the responses
enabled: false
---
# Test Doubles & WireMock

## Overview

An automated test that calls a real third-party service (payment gateway, auth provider, partner API) is slow, flaky, costs money, and cannot exercise failure modes on demand. Replace those dependencies with a controllable stub — WireMock for HTTP — so the test owns every response.

**Core principle:** The system under test is real; its external dependencies are stubbed. You test YOUR code's behavior against controlled inputs, not the third party's uptime.

## When to Use / When NOT

- **Stub:** third-party/external HTTP services, payment/email/SMS providers, partner APIs, anything you don't own or that has side effects/cost.
- **Do NOT stub:** the product's own API or the code under test — driving those for real is the whole point. And do not stub the database; use a real test database instead (see test-database-seeding) so SQL/dialect behavior is genuine.

## WireMock Essentials

Run WireMock as a standalone server or a Testcontainers container; point the app's config for that dependency at its URL.

```json
// stub: the auth provider returns a valid token for a known client
{
  "request":  { "method": "POST", "url": "/oauth/token" },
  "response": { "status": 200, "jsonBody": { "access_token": "test-token", "expires_in": 3600 } }
}
```

Model the failure paths too — that's the value a real service won't give you on demand:

| Scenario to cover | WireMock stub |
|-------------------|---------------|
| Happy response | 200 + expected body |
| Upstream 5xx | `"status": 503` → assert your retry/fallback |
| Timeout | `"fixedDelayMilliseconds": 30000` → assert your timeout handling |
| Malformed body | 200 + garbage → assert you don't crash |
| Auth rejected | 401 → assert your error surfaces cleanly |

## Rules

- **Verify the request too**, not just the canned response: assert the app called the dependency with the right method/path/body (WireMock `verify`). A stub that always returns 200 hides a broken request.
- **Reset stubs between tests** so one test's mappings don't leak into another.
- **Match the contract exactly** — stub the real endpoint's shape. A stub that diverges from reality passes tests but ships integration bugs; keep it aligned with the provider's documented contract.
- Prefer per-test stubs over one giant global mapping file — tests stay readable and independent.

## Worked Example

Checkout calls an external payment API. To test "payment declined shows an error and does not create an order":
1. WireMock stub: `POST /charge` → `402 {"error":"declined"}`.
2. Drive the real checkout flow against it.
3. Assert: user sees the decline message, no order row was created, and WireMock recorded exactly one `POST /charge` with the expected amount.

No real card, no real gateway, and the decline path is tested every run.

## Common Mistakes

- Stubbing your own API (you're no longer testing it).
- Stubbing the database (use a real test DB).
- A stub that returns 200 for everything → false green.
- Never asserting the outgoing request → a broken payload passes.
- Global stubs leaking across tests.

## Red Flags

- A test hits a real external URL → network flake and cost incoming.
- Only the happy response is stubbed; no failure-mode coverage.
- The stub shape drifted from the provider's real contract.

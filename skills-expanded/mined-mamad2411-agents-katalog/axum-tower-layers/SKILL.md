---
name: axum-tower-layers
description: >
  Rust Axum services using Tower middleware layers: timeouts, concurrency limits,
  request body limits, authentication/authorization layers, tracing, CORS, and
  compression. Use when hardening or structuring Axum HTTP APIs with tower-http /
  custom Service builders — not for AWS Control Tower or non-Rust frameworks.
---

# Axum Tower Layers

## Scope And Authorization

- **In scope:** Axum/Tower applications you own or are authorized to modify (services, internal APIs, labs).
- **Out of scope:** Weaponizing middleware bypasses against third-party apps; disabling auth “temporarily” in prod without ticket.
- Prefer staged rollout of timeout/limit changes — they can shed legitimate traffic.
- Pair with `rust-style-and-clippy` and `code-quality-standards`.

## When To Use

- Adding `TimeoutLayer`, `ConcurrencyLimitLayer`, `RequestBodyLimitLayer`, `TraceLayer`, CORS, compression.
- Centralizing authn (JWT/session extractors) as Tower layers or Axum middleware.
- Ordering layers correctly (outermost vs innermost semantics).
- Debugging hangs, slowloris-style risk, or missing request IDs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AWS Control Tower / account vending | Org/AWS landing-zone skills — **not** this skill |
| Generic code quality | `code-quality-standards` |
| BFF cookie sessions (web pattern) | `bff-cookie-session-pattern` |
| Rate-limit product testing | `rate-limit-bypass-testing` (authorized) |
| Rust style/clippy defaults | `rust-style-and-clippy` |

## Domain Focus

| Layer / concern | Guidance |
| --- | --- |
| Timeout | Bound request handling; distinguish connect vs service timeout |
| Concurrency | Protect process from overload; pair with queue/backpressure |
| Body limit | Default deny huge payloads; per-route overrides for uploads |
| Auth | Fail closed; do not log secrets; extractors for identity |
| Tracing | `TraceLayer` + request id; redact sensitive headers |
| CORS | Explicit origins; avoid `*` with credentials |
| Tooling | `axum`, `tower`, `tower-http`, `tokio`, `tracing`, `cargo test` |

## Workflow

### 1. Confirm scope and success criteria

1. Service role (public API vs internal), SLOs, auth mechanism, max body size, authorization to change prod.
2. Success: layers ordered correctly; tests for timeout/401/413; load behavior acceptable.
3. Inventory existing `Router`/`ServiceBuilder` stack.

### 2. Inventory current middleware stack

```bash
rg -n "ServiceBuilder|layer\(|TimeoutLayer|CorsLayer|TraceLayer" src/
cargo tree -p axum -i tower-http
```

1. List routes that need different limits (upload vs JSON API).
2. Note TLS termination and reverse-proxy timeouts (nginx/ALB) so they align.

### 3. Baseline behavior

1. Measure p99 latency and concurrent requests under normal load.
2. Reproduce hang without timeout (local test).
3. Capture auth failure modes (missing/invalid token).

### 4. Apply Tower layers in Axum

**Illustrative stack (order matters — verify against your tower version):**

```rust
use axum::{Router, routing::get};
use std::time::Duration;
use tower::ServiceBuilder;
use tower_http::{
    limit::RequestBodyLimitLayer,
    timeout::TimeoutLayer,
    trace::TraceLayer,
    cors::{CorsLayer, Any},
};

let app = Router::new()
    .route("/healthz", get(|| async { "ok" }))
    .route("/api/*path", /* protected routes */)
    .layer(
        ServiceBuilder::new()
            // outermost: observe all requests
            .layer(TraceLayer::new_for_http())
            .layer(TimeoutLayer::new(Duration::from_secs(30)))
            .layer(RequestBodyLimitLayer::new(1024 * 1024)) // 1 MiB default
            // .layer(auth_layer)
            // innermost closer to handler depending on builder semantics
    );
```

**Practices:**

1. Put cheap filters (method, path) early; expensive auth after basic limits when appropriate.
2. Use route-specific layers: `.route_layer(...)` for auth on `/api` only; public `/healthz` unauthenticated.
3. `ConcurrencyLimitLayer` at server level to cap in-flight work; return 503 with `Retry-After` when possible.
4. CORS: list explicit `Origin`s for browser apps; never combine `Allow-Credentials` with `*`.
5. Auth layer: validate JWT/signature; attach `Extension<User>`; reject with 401/403 without leaking internals.
6. Compression (`CompressionLayer`) carefully with encrypted payloads and BREACH-style concerns on secrets.

### 5. Verify with evidence

```bash
cargo test
cargo clippy -- -D warnings
# Timeout: handler sleeps > limit → client sees 408/500 per your mapping
# Body limit: large POST → 413
# Auth: missing Authorization → 401
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3000/healthz
curl -sS -o /dev/null -w "%{http_code}\n" -X POST --data-binary @big.bin http://127.0.0.1:3000/api/x
```

1. Integration tests with `tower::ServiceExt::oneshot` or hyper test client.
2. Confirm proxy timeouts ≥ app timeouts (or intentional reverse).
3. Tracing shows `request_id` / latency without `Authorization` header values.

### 6. Observe and harden

1. Metrics: in-flight requests, timeout count, 401/413 rates, body rejections.
2. Alerts on timeout storms (dependency failure).
3. Review new routes for missing auth layers in PR checklist.

### 7. Hand off

1. Document layer order diagram for the team.
2. Default limits in shared `app::router()` factory — avoid per-binary drift.
3. Link runbook for raising body limit for legitimate upload endpoints.

## Layer Order Cheatsheet

| Position | Typical layers |
| --- | --- |
| Outer | Trace, request-id, metrics |
| Mid | Timeout, concurrency, CORS |
| Inner | Body limit, auth, extension inject |
| Handler | Business logic extractors |

*(Validate exact “outer” semantics against your `ServiceBuilder` usage; write tests.)*

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Timeouts | Explicit per-service budget | No timeout; rely on client only |
| Bodies | Default 1MB + upload exception | Unlimited body on public API |
| Auth | Route-layer on `/api` | Auth only checked deep in some handlers |
| CORS | Explicit origins | `*` with cookies |
| Logs | Redacted headers | Full `Authorization` bearer in traces |

## Output Checklist

- [ ] Current middleware inventory completed
- [ ] Timeout, body limit, concurrency decisions documented
- [ ] Auth layer fail-closed on protected routes
- [ ] CORS policy explicit if browser clients exist
- [ ] Tracing/metrics without secret leakage
- [ ] Automated tests for 401/413/timeout paths
- [ ] Proxy timeout alignment checked
- [ ] Clippy/tests green; `code-quality-standards` applied

## Rules

- This skill is **Rust Axum + Tower**, not AWS Control Tower.
- Fail closed on auth and body limits.
- Do not log credentials or session tokens.
- Change limits with metrics and owner approval in prod.
- Prefer shared router factory over copy-paste layers.

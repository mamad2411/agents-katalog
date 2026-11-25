---
name: rc-axum
description: "Implements and reviews Axum 0.8+ APIs in Rust — routing, State, extractors, Tower middleware, typed errors, WebSockets, CORS, timeouts, hardening. Use when building or changing Axum backends, handlers, middleware, or WS endpoints. Do not use for SvelteKit (rc-sveltekit), the SQLx data layer alone (rc-sqlx), or Rust language idioms (rc-rust)."
user-invocable: true
model: sonnet
effort: medium
---

# Axum 0.8+ (Rust web API)

Opinionated guide for production Axum services (Tokio + Tower + Hyper). Target crate line: **axum 0.8.x** (docs verified against axum v0.8.4+). Pair with `rc-sqlx` for Postgres and `rc-sveltekit` when the front is SvelteKit.

## Core workflow

1. **Map boundaries** — routes vs domain vs infra; keep handlers thin.
2. **State** — one `AppState: Clone` (pool, config, clients); inject with `.with_state(...)`. Prefer `State<T>` over request-global `Extension` for app state.
3. **Extractors** — `Path`, `Query`, `Json`, `State`, `TypedHeader` as needed; fail early with typed errors.
4. **Middleware** — Tower `ServiceBuilder` order: errors/timeouts → tracing → CORS → auth `route_layer` where needed.
5. **Security** — bind loopback behind reverse proxy in VPS; CORS explicit origins; no secrets in logs. Read `references/security.md`.
6. **Test** — `tower::ServiceExt::oneshot` for HTTP; dedicated WS tests. Read `references/testing.md`.
7. **Lint** — `cargo fmt`, `clippy -D warnings`, release build. Read `references/lint-tooling.md`.

## Reference guide

| Topic | File | Load when |
| ----- | ---- | --------- |
| Routing, State, extractors, errors, WS | `references/guide.md` | Implementing or refactoring handlers |
| Auth, CORS, headers, hardening | `references/security.md` | Auth, public API, production deploy |
| Unit/integration tests | `references/testing.md` | Writing or fixing tests |
| Clippy, fmt, CI, features | `references/lint-tooling.md` | Tooling, CI, crate features |

## Must do

- Use **Axum 0.8** APIs (`axum::serve(listener, app)`, `Message::Text` as in current WS).
- Keep `AppState` cheap to clone (`Arc` inside if needed).
- Return `impl IntoResponse` / custom error type implementing `IntoResponse` — never panic in handlers for expected failures.
- Layer timeouts with `HandleErrorLayer` so timeout errors become HTTP responses.
- For WebSockets: handle `Close`, limit message size, authenticate before upgrade when data is private.
- Log with `tracing` + `TraceLayer`; structured fields, no tokens/passwords.

## Must not do

- Use stringly `format!` SQL (use `rc-sqlx` + binds).
- Block the async runtime with sync CPU-heavy work (use `spawn_blocking` or dedicated workers).

## Output template

When implementing Axum features, deliver:

1. Router sketch (paths + methods + layers)
2. `AppState` fields and ownership (`Arc` where needed)
3. Handler signatures with extractors
4. Error type → status mapping
5. Tests (`oneshot` and/or WS) + commands: `cargo test`, `cargo clippy -- -D warnings`

## Related skills

- `rc-sqlx` — Postgres access
- `rc-sveltekit` — SSR front talking to this API
- `rc-observability` — metrics/logs/traces beyond basic tracing
- `rc-resilience` — retries, timeouts across services
- `rc-code-review` — before claiming done

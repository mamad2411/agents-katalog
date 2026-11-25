---
name: axum-scaffolder
audience: team
description: >
  Scaffolds Axum HTTP endpoints with OpenAPI (utoipa), Tower middleware, JWT auth, rate
  limiting, CORS, health checks, and versioning. Axum-first: typed extractors, typed responses,
  compile-time route verification. Use when creating Rust REST APIs, scaffolding Axum
  endpoints/projects, configuring Tower middleware, or adding OpenAPI/JWT to Axum. Not when the
  codebase uses Actix-web — Axum-into-Actix needs manual integration not covered here.
---

# Axum Scaffolder

> "An API that is not documented is an API that is not finished. Security by default:
> every route is protected unless explicitly marked public."

## Core Philosophy

Axum is Rust's most ergonomic HTTP framework, built on Tower's middleware ecosystem and Tokio's
async runtime. This skill scaffolds production-ready Axum APIs with OpenAPI documentation, security
middleware, and proper error handling from day one. The OpenAPI spec is generated from code, not
written separately; routes are versioned from the first commit; auth is applied at the router level
so anonymous access is explicit; request and response data flow through typed extractors and
`impl IntoResponse`, never raw `Request` parsing.

**Non-Negotiable Constraints:**
1. OPENAPI-FIRST — `#[utoipa::path]` on every handler; `utoipa::OpenApi` derive on the app; the spec must be accurate.
2. VERSIONING FROM DAY ONE — `/api/v1/` prefix on all routers; no unversioned routes.
3. SECURITY BY DEFAULT — Tower middleware for JWT validation; anonymous access is explicit (`/health`, `/docs`).
4. TYPED EXTRACTORS — all request data via `axum::extract::{Json, Path, Query, State}`; no raw `Request` parsing.
5. TYPED RESPONSES — `impl IntoResponse` with explicit status codes; errors as RFC 7807 Problem Details via `AppError`.

Full principle table, KB lookups, discipline rules, anti-patterns, and error recovery live in
`references/conventions.md`.

## Workflow

```
DETECT      Existing Cargo.toml/deps, AppState/AppError/main router, Rust edition + Tokio version,
            existing utoipa setup.

CONFIGURE   Add deps to Cargo.toml; create src/errors.rs (AppError), src/state.rs (AppState),
            src/openapi.rs (OpenApi derive).  (Templates in router-template.md.)

SCAFFOLD    Feature router with typed handlers; request/response models with ToSchema;
            #[utoipa::path] on handlers; feature error type with From<FeatureError> for AppError.

SECURE      Add JWT validation middleware; apply to protected route groups; leave /health + /docs
            unprotected.  (Layer ordering + JWT in middleware-patterns.md.)

DOCUMENT    #[utoipa::path] on all handlers; ToSchema on all types; OpenApi derive with all
            paths/schemas; /docs route serving the OpenAPI UI.

VERIFY      cargo build · cargo test · cargo clippy -- -D warnings · curl /health → 200 ·
            curl /docs → OpenAPI UI · protected routes → 401 without token.
```

**Exit criteria:** all routes scaffolded, documented, secured, and verified.

## State Block

```
<axum-scaffold-state>
phase: DETECT | CONFIGURE | SCAFFOLD | SECURE | DOCUMENT | VERIFY | COMPLETE
feature_name: [name]
edition: [2015 | 2018 | 2021 | 2024]
tokio_version: [1.x | unknown]
utoipa_configured: true | false
auth_middleware: true | false
rate_limiting: true | false
cors_configured: true | false
health_check: true | false
openapi_ui: true | false
build_status: pass | fail | not-run
last_action: [description]
next_action: [description]
</axum-scaffold-state>
```

## Output Template

- **Cargo.toml deps, errors/AppError, auth/JWT, openapi, main, health, scaffold checklist** — `references/router-template.md`.
- **Layer ordering, JWT, CORS, rate limiting, tracing, timeout, compression, security headers** — `references/middleware-patterns.md`.
- **Principle table, KB lookups, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `rust-feature-slice` | Provides feature module organization; this skill provides the HTTP infrastructure (middleware, OpenAPI, auth). Use both together. |
| `rust-security-review` | After scaffolding, verify auth middleware, CORS, and input validation. |
| `rust-architecture-checklist` | After scaffolding, verify handler thinness, error handling, and trait design. |
| `sqlx-migration-manager` | When the API needs database access, use it for the migration lifecycle. |
| `minimal-api-scaffolder` | Parallel skill for .NET Minimal API — same OpenAPI-first philosophy, different ecosystem. |

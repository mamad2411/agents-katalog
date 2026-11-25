---
name: actix-web-extractors
description: >
  Actix-web request extractors and validation for owned Rust services: Path, Query,
  Json, Form, Headers, Data/AppData, and custom FromRequest; reject invalid input,
  limit payloads, and map errors to safe HTTP responses. Use when building or reviewing
  Actix handlers, extractor failures, or deserialization bounds — not for attacking
  third-party Actix apps.
---

# Actix-Web Extractors

## Scope And Authorization

- **In scope:** Rust/Actix-web applications you own or are authorized to modify.
- **Out of scope:** unauthorized testing of third-party services; shipping `unwrap` on untrusted input as “demo.”
- Prefer staging for behavior changes on error responses (status codes can break clients).
- Redact auth tokens and PII from extractor debug logs.
- Pair with `code-quality-standards` and `rust-style-and-clippy`.

## When To Use

- Implementing handlers that take `web::Path`, `web::Query`, `web::Json`, `web::Form`.
- Hardening JSON body size, content-type, and schema validation.
- Custom extractors (auth identity, tenant id) with fail-closed errors.
- Reviewing panics/`unwrap` in `FromRequest` impls.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Rust style/clippy | `rust-style-and-clippy` |
| API authz / JWT deep dive | `api-auth-and-jwt-abuse` |
| Rate-limit design | `api-rate-limit-design` |
| Full web threat model workshop | `abuse-case-workshops` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Extractor | Role | Hardening notes |
| --- | --- | --- |
| `Path<T>` | URL segments | Parse typed ids; reject overflow/garbage |
| `Query<T>` | Query string | Default limits; no huge nested query bombs |
| `Json<T>` | JSON body | `JsonConfig` limit; serde deny unknown if needed |
| `Form<T>` | urlencoded | Size limits; CSRF at app layer if cookie session |
| `Header` / custom | Typed headers | Strict parse; no trust of `X-Forwarded-*` without proxy setup |
| `Data<T>` / `ReqData` | App or request state | Share immutable config; don’t put secrets in logs |
| Payload | Raw body | Explicit when not using Json; streaming limits |

## Workflow

### 1. Confirm scope and success criteria

1. Record crate versions (`actix-web`, `serde`), routes in scope, public vs internal.
2. Success: invalid input → 4xx without panic; valid types enforced; body limits tested; auth extractor rejects anonymous on protected routes.
3. List current custom extractors.

### 2. Inventory handlers and extractors

```bash
rg -n "web::(Path|Query|Json|Form|Data)" src/
rg -n "FromRequest" src/
cargo tree -p actix-web
```

1. Flag handlers that take `String` paths without validation or `serde_json::Value` for everything.
2. Note global `JsonConfig` / `FormConfig` / `PayloadConfig`.

### 3. Apply validated extractors

```rust
use actix_web::{web, HttpResponse, Result};
use serde::Deserialize;
use uuid::Uuid;

#[derive(Debug, Deserialize)]
struct PageQuery {
    #[serde(default = "default_limit")]
    limit: u32,
    #[serde(default)]
    cursor: Option<String>,
}
fn default_limit() -> u32 { 20 }

#[derive(Debug, Deserialize)]
struct CreateBody {
    name: String,
    #[serde(default)]
    tags: Vec<String>,
}

async fn get_item(
    path: web::Path<Uuid>,
    query: web::Query<PageQuery>,
) -> Result<HttpResponse> {
    let id = path.into_inner();
    let q = query.into_inner();
    if q.limit == 0 || q.limit > 100 {
        return Ok(HttpResponse::BadRequest().body("limit out of range"));
    }
    // ... load by id
    Ok(HttpResponse::Ok().finish())
}

async fn create(
    body: web::Json<CreateBody>,
) -> Result<HttpResponse> {
    let b = body.into_inner();
    if b.name.is_empty() || b.name.len() > 200 {
        return Ok(HttpResponse::BadRequest().body("invalid name"));
    }
    Ok(HttpResponse::Created().finish())
}
```

**Global JSON limit:**

```rust
use actix_web::{web, App};

App::new()
    .app_data(web::JsonConfig::default().limit(32_768)) // 32 KiB
    .app_data(web::FormConfig::default().limit(16_384))
    .app_data(web::PayloadConfig::default().limit(1_048_576))
```

### 4. Custom extractors (auth example pattern)

```rust
use actix_web::{dev::Payload, Error, FromRequest, HttpRequest};
use futures_util::future::{ready, Ready};

struct AuthUser { user_id: Uuid }

impl FromRequest for AuthUser {
    type Error = Error;
    type Future = Ready<Result<Self, Self::Error>>;

    fn from_request(req: &HttpRequest, _: &mut Payload) -> Self::Future {
        match req.headers().get("Authorization").and_then(|h| h.to_str().ok()) {
            Some(tok) if tok.starts_with("Bearer ") => {
                // verify JWT / session — fail closed
                match verify_token(&tok[7..]) {
                    Ok(uid) => ready(Ok(AuthUser { user_id: uid })),
                    Err(_) => ready(Err(actix_web::error::ErrorUnauthorized("invalid token"))),
                }
            }
            _ => ready(Err(actix_web::error::ErrorUnauthorized("missing token"))),
        }
    }
}
```

1. Never panicking inside `from_request`.
2. Map verification errors to 401/403 without leaking key material.

### 5. Verify with tests

```bash
cargo test
cargo clippy -- -D warnings
```

```rust
#[actix_web::test]
async fn rejects_oversize_json() {
    let app = actix_web::test::init_service(
        App::new()
            .app_data(web::JsonConfig::default().limit(64))
            .route("/c", web::post().to(create)),
    ).await;
    let req = actix_web::test::TestRequest::post()
        .uri("/c")
        .set_payload(vec![b'x'; 10_000])
        .insert_header(("content-type", "application/json"))
        .to_request();
    let resp = actix_web::test::call_service(&app, req).await;
    assert!(resp.status().is_client_error());
}
```

### 6. Observe and hand off

1. Metrics: 4xx rates on parse failures; no 500 spikes from extractor panics.
2. Document max body sizes and validation rules for API consumers.
3. Review proxy body size alignment (nginx `client_max_body_size`).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Types | `Uuid` / enums in Path | Unchecked `String` SQL concat later |
| Errors | 400/401 from extractors | `unwrap` → 500 |
| Limits | Global JsonConfig | Multi-GB default body |
| Auth | Fail-closed FromRequest | Optional auth silently as admin |
| Logs | Structured error codes | Log full Authorization header |

## Output Checklist

- [ ] Routes and extractors inventoried
- [ ] Json/Form/Payload limits set intentionally
- [ ] Path/Query typed and range-checked
- [ ] Custom auth extractors fail closed
- [ ] Tests for invalid/oversize input
- [ ] Clippy clean on touched code
- [ ] Error responses safe (no stack traces in prod)
- [ ] `code-quality-standards` / Rust style applied

## Rules

- Owned services only.
- Prefer typed extractors + serde over ad-hoc string parsing.
- Fail closed on auth extractors; never panic on bad input.
- Align body limits across proxy and Actix.
- Keep secrets out of logs and error bodies.

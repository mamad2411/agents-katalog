---
name: rust-axum-actix
description: Use when building HTTP servers in Rust — routing, extractors, middleware, state, error handling. axum-first.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [rust]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [rust-essentials, rust-async-tokio, rust-testing]
---

# Rust HTTP (axum / actix-web)

**Iron Law: axum for new HTTP servers in Rust. Actix-web only if you have a specific reason (perf benchmarks, existing investment).**

axum is built on tower + hyper, shares an ecosystem with the rest of Tokio, and has the lowest-friction extractor model. Actix-web is fast but its actor-based history adds surface area you don't need for a typical service.

## Minimal axum app

```rust
use axum::{Router, routing::get, Json, extract::State};
use std::sync::Arc;

#[derive(Clone)]
struct AppState { db: PgPool, cfg: Arc<Config> }

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let state = AppState { db: pool().await?, cfg: Arc::new(Config::load()?) };
    let app = Router::new()
        .route("/health", get(|| async { "ok" }))
        .route("/users/:id", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    // Graceful shutdown: drains in-flight requests on SIGTERM/SIGINT. Without this,
    // container orchestrators (Kubernetes, systemd) kill mid-request work — every deploy.
    axum::serve(listener, app)
        .with_graceful_shutdown(async {
            tokio::signal::ctrl_c().await.ok();
        })
        .await?;
    Ok(())
}
```

## Extractors

Handlers are `async fn` that take extractors as args and return `impl IntoResponse`. Order matters: body-consuming extractors (`Json`, `Form`, `Bytes`) **must come last**.

```rust
async fn get_user(
    State(s): State<AppState>,         // shared state
    Path(id): Path<Uuid>,              // /users/:id
    Query(p): Query<Page>,             // ?page=2
    headers: HeaderMap,                 // raw access
    Json(body): Json<CreateUser>,      // body — LAST
) -> Result<Json<User>, ApiError> { … }
```

| Extractor                        | Use                                                       |
| -------------------------------- | --------------------------------------------------------- |
| `Path<T>`                        | URL params: `/users/:id`                                  |
| `Query<T>`                       | Querystring: `?page=2&limit=20`                           |
| `Json<T>`                        | JSON body (consumes body)                                 |
| `Form<T>`                        | URL-encoded form body                                     |
| `State<S>`                       | Shared app state (must `with_state(...)`)                 |
| `Extension<T>`                   | Per-request data injected by middleware                   |
| `HeaderMap` / `TypedHeader<...>` | Headers                                                   |
| Custom                           | Impl `FromRequestParts` (no body) or `FromRequest` (body) |

## State sharing

| Pattern                                                          | When                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------- |
| `State<AppState>`                                                | Default. `AppState: Clone` (use `Arc` inside for cheap clone) |
| `Extension<Arc<T>>`                                              | Middleware-injected per-request value                         |
| Sub-router state via `Router::nest("/api", api.with_state(...))` | Different state for a subtree                                 |
| Thread-local globals                                             | Don't. Async tasks move between threads.                      |

```rust
#[derive(Clone)]
struct AppState {
    db: PgPool,                  // Pool is Arc-internally, cheap clone
    cache: Arc<RwLock<Cache>>,   // Wrap your own state in Arc
}
```

## Error handling

Define one error type. Implement `IntoResponse`. Use `?` in handlers via `From` impls.

```rust
#[derive(thiserror::Error, Debug)]
enum ApiError {
    #[error("not found")]
    NotFound,
    #[error(transparent)]
    Db(#[from] sqlx::Error),
    #[error(transparent)]
    Validation(#[from] validator::ValidationErrors),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (code, msg) = match &self {
            ApiError::NotFound      => (StatusCode::NOT_FOUND,        self.to_string()),
            ApiError::Validation(_) => (StatusCode::BAD_REQUEST,      self.to_string()),
            ApiError::Db(e)         => {
                tracing::error!(error = ?e, "db");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal".into())
            }
        };
        (code, Json(json!({ "error": msg }))).into_response()
    }
}

async fn get_user(State(s): State<AppState>, Path(id): Path<Uuid>) -> Result<Json<User>, ApiError> {
    let user = sqlx::query_as!(User, "...", id).fetch_optional(&s.db).await?
        .ok_or(ApiError::NotFound)?;
    Ok(Json(user))
}
```

Never log internal errors back to clients. Map to a stable shape.

**Cookie-based auth needs CSRF.** Bearer-token APIs don't (the token is in a header the browser won't auto-send cross-origin). For session cookies, use a double-submit cookie or a synchronizer token; tower-sessions integrates with axum.

**Raw SQL injection**: prefer `sqlx::query!`/`query_as!` macros — they parameterize at compile time. The non-macro `sqlx::query("SELECT ...")` with `format!`-built strings is the injection-prone form.

## Middleware (tower)

axum is a tower `Service`, so any `tower::Layer` works. Compose with `Router::layer` (outermost runs first on request, last on response).

```rust
use std::time::Duration;
use axum::extract::DefaultBodyLimit;
use tower_http::{trace::TraceLayer, cors::CorsLayer, timeout::TimeoutLayer};
use http::Method;

let app = Router::new()
    .route("/users/:id", get(get_user))
    .layer(TimeoutLayer::new(Duration::from_secs(10)))
    .layer(DefaultBodyLimit::max(1 << 20))                  // 1 MB cap; prevents upload-bomb OOM
    // CorsLayer::permissive() is DEV ONLY — wildcard origin + reflected headers; combined with
    // cookie-based auth (SameSite=None), it enables credentialed cross-origin attacks.
    // Production form:
    .layer(CorsLayer::new()
        .allow_origin(["https://app.example.com".parse().unwrap()])
        .allow_methods([Method::GET, Method::POST])
        .allow_headers([http::header::AUTHORIZATION, http::header::CONTENT_TYPE]))
    .layer(TraceLayer::new_for_http());                     // last .layer() = outermost = first to see the request

// AppState used with .with_state(state) must be Clone + Send + Sync + 'static.
// Rc<T>, RefCell<T>, and non-Send types here produce multi-screen compiler errors
// pointing into axum internals; reach for Arc<Mutex<...>> or Arc<RwLock<...>> instead.
```

For per-request auth state, write a `middleware::from_fn` that calls `req.extensions_mut().insert(user)` and pull via `Extension<AuthUser>` in handlers.

## Testing

Hit the router directly — no network, no port allocation, no flakes.

```rust
#[tokio::test]
async fn returns_404_for_unknown() {
    let app = build_app(test_state()).await;
    let resp = app
        .oneshot(Request::builder().uri("/users/00000000-0000-0000-0000-000000000000").body(Body::empty()).unwrap())
        .await.unwrap();
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

## Actix-web — when

| Use actix-web if                                      | Use axum if                   |
| ----------------------------------------------------- | ----------------------------- |
| Existing codebase already on actix                    | Greenfield service            |
| You have benchmarks proving actix wins for your shape | "It might be faster" — no     |
| You want the actor model for this specific problem    | You want plain async handlers |

The performance gap in real services (with a DB, JSON, real handlers) is small and often noise. Pick axum for ecosystem alignment.

## Anti-patterns

- Handlers returning `Result<impl IntoResponse, Box<dyn Error>>` — opaque, ugly. Define a typed `ApiError`.
- Blocking calls in a handler (sync DB driver, `std::thread::sleep`, CPU loop). Use async drivers or `spawn_blocking`.
- Manual `serde_json::to_string` + `Response::builder` — use `Json<T>`.
- `unwrap()` in handlers — every panic becomes a 500 with a vague body.
- State that isn't `Clone` — `with_state` requires it. Wrap in `Arc`.
- `tokio::spawn(handler_work())` to "make it concurrent" — already concurrent across requests.
- One enormous `Router` in `main.rs` — split per-domain with `Router::nest("/api/users", users::routes())`.
- Storing per-request data in `lazy_static`/globals — pass via `Extension`.

## Red flags

| Thought                             | Reality                                                                        |
| ----------------------------------- | ------------------------------------------------------------------------------ |
| "Actix is 20% faster on benchmarks" | Benchmarks rarely reflect your DB-bound real service. Pick on ergonomics.      |
| "I'll add tower later"              | Tower middleware is the answer to half your future requirements. Use it now.   |
| "Handler is getting big"            | Push logic into a service module; handler stays thin (parse → call → respond). |
| "I need a custom runtime"           | You don't. Use `#[tokio::main]`.                                               |

## Hand-off

For ownership, traits, errors: `Skill(rust-essentials)`. For Tokio internals, cancellation, channels: `Skill(rust-async-tokio)`. For integration/unit tests of handlers: `Skill(rust-testing)`.

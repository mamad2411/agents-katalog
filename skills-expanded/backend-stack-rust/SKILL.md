---
name: backend-stack-rust
description: "A Rust backend: axum on tokio, routers, extractors and shared state, tower and tower-http middleware, serde with validation (validator or garde), thiserror errors turned into responses, sqlx with compile-time checked queries and migrations, pools, tracing with request spans, configuration and secrets, graceful shutdown with background tasks and cancellation, tests with oneshot and sqlx::test, clippy, cargo-deny and small release images. Read when building or changing a Rust backend."
---

# Rust

The generated axum service: `unwrap()` on everything a request can break, a
`static` pool behind `lazy_static`, `String` for every id, each handler
building its own error response, `Json` rejections answered as plain text,
no body limit or timeout, a blocking call on the async runtime, and spawned
tasks cut off mid-write on shutdown. The backend rules are in the `backend`
skill; these are Rust's own.

## 1. Setup

- axum on tokio (or the project's framework), `serde` for bodies, `sqlx` for
  the database, `tracing` for logs, `tower-http` for the layers around the
  router. `cargo fmt` and `cargo clippy -- -D warnings` clean.
- The lines in 2026: axum 0.8, tower-http 0.7, sqlx 0.9, thiserror 2, edition
  2024. Keep the project's versions and read `Cargo.lock` before using an
  API: axum 0.8 changed paths from `/:id` to `/{id}` and dropped
  `#[async_trait]` from extractor impls.
- Layout: `main.rs` builds config, pool and router; a module per feature
  (`orders/{mod,routes,service,store}.rs`); `error.rs`, `config.rs`,
  `state.rs` at the top; `fn app(state: AppState) -> Router` shared with the
  tests. `[lints.clippy] unwrap_used = "deny"` in `Cargo.toml`, with
  `allow-unwrap-in-tests = true` in `clippy.toml`.
- Config: figment or the `config` crate into a serde struct at start (a
  missing value fails with the field's name); secrets as
  `secrecy::SecretString`, whose `Debug` prints `[REDACTED]`.

## 2. Handlers and state

- Shared state in one `AppState` (the pool, config, clients) behind `Clone`
  (an `Arc` inside where needed), passed with `.with_state(state)` and taken
  with `State(state)`; no `static` or `lazy_static` for the database.
  `FromRef` lets a handler take only the part it needs (`State<PgPool>`).
- Extractors do the parsing: `Path<OrderId>`, `Query<ListParams>`,
  `Json<CreateOrder>`. A custom extractor (`CurrentUser`) loads and checks
  the caller once, for every route that takes it. The body extractor comes
  last: only one may consume the body.
- Bodies with `#[serde(deny_unknown_fields)]` on inputs, then validated
  (the `validator` crate, `garde`, or a `fn validate(&self) -> Result<(),
  FieldErrors>`) before the service is called. Newtypes for ids and money
  (`struct OrderId(i64)`, `struct Amount(i64)`), so they cannot be mixed up.
- `route_layer` for auth middleware that should run only on matched routes,
  so an unknown path stays a `404` rather than a `401`.

```rust
/// Any handler that takes `CurrentUser` is signed-in only; the check lives here once.
impl<S> FromRequestParts<S> for CurrentUser
where
    AppState: FromRef<S>,
    S: Send + Sync,
{
    type Rejection = AppError;

    async fn from_request_parts(parts: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let token = parts.headers.get(AUTHORIZATION)
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.strip_prefix("Bearer "))
            .ok_or(AppError::Unauthenticated)?;
        AppState::from_ref(state).sessions.verify(token).await.ok_or(AppError::Unauthenticated)
    }
}

/// `Json` whose rejection (bad JSON, unknown field) is our problem response, not plain text.
#[derive(FromRequest)]
#[from_request(via(axum::Json), rejection(AppError))]
struct AppJson<T>(T);

async fn reserve(
    State(state): State<AppState>,
    user: CurrentUser,
    Path(id): Path<Uuid>,
    AppJson(body): AppJson<Reserve>,
) -> Result<StatusCode, AppError> {
    body.validate()?; // ValidationErrors -> AppError::Validation, through a From impl
    state.orders.reserve(&user, id, body.quantity).await?;
    Ok(StatusCode::NO_CONTENT)
}
```

## 3. Errors

- One `AppError` enum with `thiserror` (`NotFound`, `Unauthenticated`,
  `Forbidden`, `Conflict(&'static str)`, `Validation(FieldErrors)`,
  `BadBody(#[from] JsonRejection)`, `Internal(#[from] anyhow::Error)`), and
  `impl IntoResponse for AppError` that writes the format in
  `backend-errors` and logs internal errors with their chain.
- Handlers return `Result<Json<T>, AppError>` and use `?`. No `unwrap` or
  `expect` on anything a request can cause.
- `From` impls map once: `sqlx::Error::RowNotFound` to `NotFound`, a
  database error whose `is_unique_violation()` is true to a `Conflict`, the
  rest to `Internal`; services add anyhow's `.context("reserve stock")`.

```rust
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "not_found"),
            AppError::Unauthenticated => (StatusCode::UNAUTHORIZED, "unauthenticated"),
            AppError::Forbidden => (StatusCode::FORBIDDEN, "forbidden"),
            AppError::Conflict(code) => (StatusCode::CONFLICT, *code),
            AppError::Validation(_) => (StatusCode::BAD_REQUEST, "validation_failed"),
            AppError::BadBody(_) => (StatusCode::BAD_REQUEST, "malformed_json"),
            AppError::Internal(err) => {
                tracing::error!(error = ?err, "request failed"); // the whole chain, once
                (StatusCode::INTERNAL_SERVER_ERROR, "internal")
            }
        };
        let mut body = json!({ "type": format!("https://example.com/errors/{}", code.replace('_', "-")),
                               "status": status.as_u16(), "code": code });
        if let AppError::Validation(errors) = self { body["errors"] = json!(errors); }
        (status, [(header::CONTENT_TYPE, "application/problem+json")], body.to_string()).into_response()
    }
}
```

## 4. Data

- `sqlx` with `query!` or `query_as!` checked at compile time (with
  `cargo sqlx prepare` for offline builds), migrations in `migrations/` run
  by `sqlx migrate run`, transactions with `pool.begin()` and `tx.commit()`.
- `PgPool` created once with limits (`max_connections`, `acquire_timeout`):
  about 10 and 3 seconds, so a starved pool fails fast instead of queueing.
- The `.sqlx/` directory from `cargo sqlx prepare` is committed, and CI and
  Docker build with `SQLX_OFFLINE=true`; `cargo sqlx prepare --check` in CI
  fails when a query changed without it.
- Inside a transaction the executor is `&mut *tx`; a transaction dropped
  without `commit()` rolls back, so `?` on the way out is safe.
- Nullable columns arrive as `Option<T>`; `SELECT count(*) AS "count!"`
  tells the macro a value is never null. Times as `time::OffsetDateTime` or
  `chrono::DateTime<Utc>` on `timestamptz`; ids with `Uuid::now_v7()`; money
  as `i64` minor units or `rust_decimal`.
- `sqlx::migrate!()` embeds the migrations; running them at start suits one
  instance, a release step suits several (`database-migrations`).

```rust
// One statement: the check and the write cannot race.
let done = sqlx::query!(
    "UPDATE products SET stock = stock - $2 WHERE id = $1 AND stock >= $2", id, qty
).execute(&mut *tx).await?;
if done.rows_affected() == 0 {
    return Err(AppError::Conflict("out_of_stock"));
}
```

## 5. Around the router

- `tower-http` layers: `TraceLayer` with a request id
  (`SetRequestIdLayer`, `PropagateRequestIdLayer`), `TimeoutLayer`,
  `RequestBodyLimitLayer`, `CorsLayer` with explicit origins,
  `CompressionLayer`.
- `tracing-subscriber` with JSON output in production and `EnvFilter` from
  `RUST_LOG`.
- Each `.layer()` wraps what is already there, so the last one added runs
  first: set the request id outermost, then trace, then the rest. Layers
  added with `Router::layer` wrap each route inside the routing, so
  `MatchedPath` is there to give the span its route template.

```rust
let x_request_id = HeaderName::from_static("x-request-id");
Router::new()
    .route("/products/{id}/reserve", post(reserve))
    .with_state(state)
    .layer(CatchPanicLayer::new()) // a panic is that request's 500, not a dropped connection
    .layer(RequestBodyLimitLayer::new(1024 * 1024))
    .layer(TimeoutLayer::with_status_code(StatusCode::SERVICE_UNAVAILABLE, Duration::from_secs(10)))
    .layer(CorsLayer::new().allow_origin(config.allowed_origins.clone()))
    .layer(PropagateRequestIdLayer::new(x_request_id.clone()))
    .layer(TraceLayer::new_for_http()
        .make_span_with(|req: &Request<_>| {
            let route = req.extensions().get::<MatchedPath>().map(|p| p.as_str());
            let request_id = req.headers().get("x-request-id").and_then(|v| v.to_str().ok());
            tracing::info_span!("request", method = %req.method(), route, request_id)
        })
        .on_response(DefaultOnResponse::new().level(Level::INFO))) // one line per request
    .layer(SetRequestIdLayer::new(x_request_id, MakeRequestUuid))
```

- `TraceLayer` logs at `DEBUG` by default, hence the `on_response` level.
  axum's `Json` has its own 2 MB limit (`DefaultBodyLimit`); the layer above
  sets one limit for every body. OpenTelemetry exports these spans through
  `tracing-opentelemetry` and `opentelemetry-otlp` (`backend-observability`).

## 6. Shutdown, background tasks and cancellation

```rust
let shutdown = CancellationToken::new();
let tasks = TaskTracker::new();
let (token, db) = (shutdown.clone(), state.db.clone());
tasks.spawn(async move {
    let mut tick = tokio::time::interval(Duration::from_secs(60));
    loop {
        tokio::select! {
            _ = token.cancelled() => break, // stops between steps, never inside one
            _ = tick.tick() => expire_reservations(&db).await, // logs its own errors
        }
    }
});
let listener = tokio::net::TcpListener::bind(&config.addr).await?;
axum::serve(listener, app(state.clone()))
    .with_graceful_shutdown(async move { shutdown_signal().await; shutdown.cancel() })
    .await?;
tasks.close();
tasks.wait().await;
state.db.close().await;
```

with `shutdown_signal` awaiting `ctrl_c` or `SIGTERM`
(`tokio::signal::unix::signal(SignalKind::terminate())`).

- A handler's future is dropped when the client disconnects: code after its
  next `.await` never runs. Writes that must happen together go in one
  transaction; work that must finish goes to a tracked task or a job
  (`backend-jobs`), never a bare `tokio::spawn` nobody waits for.
- Blocking calls (a sync library, file hashing, password hashing with
  argon2) go through `tokio::task::spawn_blocking`; CPU-parallel work to
  rayon.
- A panic in a spawned task ends that task and surfaces in its `JoinHandle`;
  the release profile keeps `panic = "unwind"` (the default), since `abort`
  takes the whole server down with it.

## 7. Tests

Build the router with a test state and call it with
`tower::ServiceExt::oneshot(request)`; `#[sqlx::test]` gives each test a
fresh database with the migrations applied; wiremock for outbound HTTP.

```rust
#[sqlx::test] // a fresh database per test, migrations applied
async fn reserving_more_than_the_stock_is_a_conflict(db: PgPool) {
    let id = Uuid::now_v7();
    sqlx::query!("INSERT INTO products (id, name, stock) VALUES ($1, 'tea', 1)", id)
        .execute(&db).await.unwrap();
    let response = app(AppState::for_tests(db))
        .oneshot(Request::post(format!("/products/{id}/reserve"))
            .header("content-type", "application/json")
            .body(Body::from(r#"{"quantity":2}"#)).unwrap())
        .await.unwrap();
    assert_eq!(response.status(), StatusCode::CONFLICT);
}
```

- `#[sqlx::test(fixtures("products"))]` loads `fixtures/products.sql`;
  `#[tokio::test(start_paused = true)]` for code with timers; `cargo nextest
  run` runs each test in its own process, faster on large suites.

## 8. Release builds and images

- `[profile.release]` with `lto = "thin"`, `codegen-units = 1`,
  `strip = true`.
- Docker with cargo-chef (`cargo chef prepare`, then `cargo chef cook
  --release`) so dependencies build in a cached layer; `SQLX_OFFLINE=true`;
  the binary on `gcr.io/distroless/cc:nonroot`, or a static musl build on
  `distroless/static` with `mimalloc` as the global allocator (musl's own is
  slow under load).
- `cargo deny check` in CI with a `deny.toml`: advisories, licences, banned
  and duplicate crates, allowed sources.

## Check it

`cargo build`, `cargo clippy --all-targets -- -D warnings`, `cargo test` (or
`cargo nextest run`), `cargo deny check`, `cargo sqlx prepare --check`, then
run it and call the endpoints with `curl`: a malformed body gives a problem
`400`, not plain text, and `kill -TERM` lets requests and tasks finish.

## Avoid

`unwrap` in handlers; a global pool; `String` for every id; errors turned
into responses in each handler; bodies without `deny_unknown_fields` or
validation; no body limit or timeout layer; blocking calls on the async
runtime without `spawn_blocking`; axum's plain-text `Json` rejections;
`tokio::spawn` with no owner at shutdown; `panic = "abort"` in a server;
queries built with `format!`; a build that needs a live database because
`.sqlx/` was not committed.

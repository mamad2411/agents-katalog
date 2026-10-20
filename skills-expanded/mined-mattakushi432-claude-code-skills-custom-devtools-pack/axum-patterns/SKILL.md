---
name: axum-patterns
description: "When to activate: axum web framework, extractors, handlers, state, middleware, WebSocket, file upload, typed routing, tower layers"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: rust
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Axum Patterns

## Full Application Structure

```toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
tower = "0.4"
tower-http = { version = "0.5", features = ["cors", "trace", "compression-gzip", "timeout"] }
serde = { version = "1", features = ["derive"] }
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

```rust
use axum::{Router, routing::get};
use std::sync::Arc;
use tower::ServiceBuilder;
use tower_http::{cors::CorsLayer, trace::TraceLayer, timeout::TimeoutLayer};

#[derive(Clone)]
pub struct AppState {
    pub db: Arc<DbPool>,
    pub config: Arc<Config>,
}

pub fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/health", get(health))
        .nest("/api/v1/users", users::router())
        .nest("/api/v1/auth", auth::router())
        .layer(ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(CorsLayer::permissive())
            .layer(TimeoutLayer::new(std::time::Duration::from_secs(30))))
        .fallback(not_found)
        .with_state(state)
}

async fn health() -> &'static str { "ok" }
async fn not_found() -> (axum::http::StatusCode, &'static str) {
    (axum::http::StatusCode::NOT_FOUND, "not found")
}
```

## Custom Extractors

```rust
use axum::{async_trait, extract::FromRequestParts, http::{request::Parts, StatusCode}};

// JWT auth extractor
pub struct AuthUser(pub Claims);

#[async_trait]
impl<S: Send + Sync> FromRequestParts<S> for AuthUser {
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let token = parts.headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.strip_prefix("Bearer "))
            .ok_or((StatusCode::UNAUTHORIZED, "missing bearer token"))?;

        let claims = validate_jwt(token)
            .map_err(|_| (StatusCode::UNAUTHORIZED, "invalid token"))?;

        Ok(AuthUser(claims))
    }
}

// Pagination extractor
#[derive(Debug, serde::Deserialize)]
pub struct Pagination {
    #[serde(default = "Pagination::default_page")]
    pub page: u32,
    #[serde(default = "Pagination::default_limit")]
    pub limit: u32,
}

impl Pagination {
    fn default_page() -> u32 { 1 }
    fn default_limit() -> u32 { 20 }
    pub fn offset(&self) -> u32 { (self.page.saturating_sub(1)) * self.limit }
}

// Usage
async fn list_posts(
    AuthUser(claims): AuthUser,
    axum::extract::Query(pagination): axum::extract::Query<Pagination>,
    State(state): State<AppState>,
) -> Result<Json<Vec<Post>>, ApiError> {
    let posts = state.db.list_posts(claims.sub, pagination.offset(), pagination.limit).await?;
    Ok(Json(posts))
}
```

## Typed Error Responses

```rust
use axum::{response::{IntoResponse, Response}, http::StatusCode, Json};

pub enum ApiError {
    NotFound(String),
    Unauthorized,
    BadRequest(String),
    Internal(anyhow::Error),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, msg) = match &self {
            ApiError::NotFound(m) => (StatusCode::NOT_FOUND, m.clone()),
            ApiError::Unauthorized => (StatusCode::UNAUTHORIZED, "unauthorized".into()),
            ApiError::BadRequest(m) => (StatusCode::BAD_REQUEST, m.clone()),
            ApiError::Internal(e) => {
                tracing::error!("internal: {e:#}");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error".into())
            }
        };
        (status, Json(serde_json::json!({ "error": msg }))).into_response()
    }
}
```

## WebSocket Handler

```rust
use axum::extract::ws::{WebSocket, WebSocketUpgrade, Message};

async fn ws_handler(ws: WebSocketUpgrade, State(state): State<AppState>) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(mut socket: WebSocket, state: AppState) {
    while let Some(Ok(msg)) = socket.recv().await {
        match msg {
            Message::Text(text) => {
                let response = process_message(&text, &state).await;
                if socket.send(Message::Text(response)).await.is_err() { break; }
            }
            Message::Close(_) => break,
            _ => {}
        }
    }
}
```

## File Upload

```rust
use axum::extract::Multipart;

async fn upload_file(mut multipart: Multipart) -> Result<Json<serde_json::Value>, ApiError> {
    while let Some(field) = multipart.next_field().await? {
        let filename = field.file_name().unwrap_or("upload").to_string();
        let data = field.bytes().await?;

        if data.len() > 10 * 1024 * 1024 {
            return Err(ApiError::BadRequest("file too large (max 10MB)".into()));
        }

        save_upload(&filename, &data).await?;
    }
    Ok(Json(serde_json::json!({ "success": true })))
}
```

## Common Anti-Patterns

- **Cloning `AppState` without `Arc`** — wrap expensive fields in `Arc<T>` for cheap cloning
- **`.unwrap()` in handlers** — return `Result` or implement `IntoResponse` for your error type
- **Per-request database connections** — use `PgPool` and pass it via `State`
- **Blocking operations in handlers** — use `tokio::task::spawn_blocking`
- **Missing fallback handler** — always add `.fallback()` to avoid axum's default plain-text 404

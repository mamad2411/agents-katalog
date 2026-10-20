---
name: "rust"
description: "- Writing or reviewing Rust code with ownership, borrow checker, or lifetime errors"
---

# Rust Development

## When to activate
- Writing or reviewing Rust code with ownership, borrow checker, or lifetime errors
- Designing error handling strategy using `Result`, `thiserror`, or `anyhow`
- Building async services with Tokio
- Structuring a multi-crate Cargo workspace
- Selecting smart pointer types (`Box`, `Rc`, `Arc`, `Mutex`, `RwLock`)
- Configuring Clippy lints for a project
- Implementing traits and deciding between trait objects vs generics

## When NOT to use
- Writing non-Rust code that happens to share Rust-adjacent concepts
- General systems programming questions that do not involve Rust specifically
- Debugging C/C++ interop when the issue is on the C side

## Instructions

### Ownership Transfer vs Borrowing

Move semantics are the default. Prefer borrowing (`&T` or `&mut T`) when the callee does not need to own the value.

```rust
// Transfer ownership — callee owns the String
fn consume(s: String) { /* s is dropped here */ }

// Immutable borrow — caller retains ownership
fn inspect(s: &str) { println!("{}", s); }

// Mutable borrow — caller retains ownership, one active at a time
fn append(s: &mut String) { s.push_str(" world"); }
```

Rules for choosing:
- Pass `&T` when the function only reads
- Pass `&mut T` when the function modifies in place and the caller needs the value afterward
- Pass `T` (move) when the callee stores the value, spawns it across threads, or builds an owned collection
- Use `Clone` deliberately, not reflexively — it signals a deep copy cost

### Smart Pointer Selection

| Type | Use case |
|---|---|
| `Box<T>` | Heap-allocate a single owner; recursive types; trait objects |
| `Rc<T>` | Shared ownership in single-threaded code; reference-counted |
| `Arc<T>` | Shared ownership across threads; atomic reference count |
| `Mutex<T>` | Exclusive mutable access across threads |
| `RwLock<T>` | Multiple concurrent readers OR one writer |
| `Cell<T>` / `RefCell<T>` | Interior mutability in single-threaded code |

```rust
use std::sync::{Arc, Mutex};

// Shared mutable state across threads
let counter = Arc::new(Mutex::new(0u64));
let c = Arc::clone(&counter);
std::thread::spawn(move || {
    let mut n = c.lock().unwrap();
    *n += 1;
});
```

Avoid `Rc` in code that may later become concurrent — prefer `Arc` if the type will cross thread boundaries.

### Error Handling with Result and thiserror

Define domain errors as enums with `thiserror::Error`:

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("not found: {resource} id={id}")]
    NotFound { resource: &'static str, id: i64 },

    #[error("invalid input: {0}")]
    Validation(String),
}

pub type AppResult<T> = Result<T, AppError>;
```

Use `?` to propagate errors up the call stack. Convert between error types with `#[from]` on the enum variant. Reserve `anyhow` for application-level binaries where error type detail is not needed at the call site; use `thiserror` in libraries.

```rust
async fn fetch_user(id: i64, pool: &PgPool) -> AppResult<User> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_optional(pool)
        .await?                                          // sqlx::Error -> AppError::Database via #[from]
        .ok_or(AppError::NotFound { resource: "user", id })?;
    Ok(user)
}
```

### Async / Await with Tokio

Add Tokio with the `full` feature for most services:

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

Entry point:

```rust
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // async context available here
    run().await
}
```

Spawn concurrent tasks with `tokio::spawn`. Join a fixed set with `tokio::join!`, a dynamic set with `tokio::task::JoinSet`:

```rust
let mut set = tokio::task::JoinSet::new();
for id in ids {
    set.spawn(fetch_user(id, pool.clone()));
}
while let Some(result) = set.join_next().await {
    let user = result??;   // outer ? = JoinError, inner ? = AppError
    process(user);
}
```

Use `tokio::select!` for racing futures or handling cancellation. Always propagate cancellation correctly — `async` functions should not hold non-async locks across `.await` points.

### Trait Objects vs Generics

Generics (monomorphisation): zero runtime cost, larger binary, compiler resolves type at compile time.

```rust
fn log_event<E: Event>(event: &E) {
    println!("{}", event.summary());
}
```

Trait objects (`dyn Trait`): runtime dispatch, heap allocation, works with heterogeneous collections.

```rust
fn log_event(event: &dyn Event) {
    println!("{}", event.summary());
}

let handlers: Vec<Box<dyn Handler>> = vec![Box::new(EmailHandler), Box::new(SlackHandler)];
```

Prefer generics in libraries for performance. Prefer `dyn Trait` when storing mixed concrete types or when compile times matter more than runtime dispatch cost.

### Cargo Workspace for Multi-Crate Projects

```
my-project/
├── Cargo.toml          # workspace root
├── crates/
│   ├── core/           # domain logic, no I/O
│   ├── api/            # axum HTTP layer
│   ├── worker/         # Tokio background jobs
│   └── cli/            # binary entry point
```

Root `Cargo.toml`:

```toml
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
thiserror = "1"
```

Member `Cargo.toml` inherits workspace dependencies to keep versions consistent:

```toml
[dependencies]
tokio.workspace = true
thiserror.workspace = true
```

Run workspace-wide: `cargo build --workspace`, `cargo test --workspace`, `cargo clippy --workspace`.

### Clippy Lints

Enable a strict lint set in the workspace root or per crate:

```rust
// lib.rs or main.rs
#![warn(
    clippy::all,
    clippy::pedantic,
    clippy::nursery,
    clippy::unwrap_used,       // require explicit error handling
    clippy::expect_used,       // document why expect is safe
    clippy::panic,
    clippy::indexing_slicing,
)]
#![allow(
    clippy::module_name_repetitions,
    clippy::must_use_candidate,
)]
```

Run in CI: `cargo clippy --workspace --all-targets -- -D warnings`

Key lints to understand:
- `clippy::unwrap_used` — forces handling of `None`/`Err` rather than panicking
- `clippy::clone_on_ref_ptr` — warns when cloning `Arc`/`Rc` directly instead of using `Arc::clone`
- `clippy::large_futures` — warns when a future is large enough to warrant boxing
- `clippy::redundant_closure_for_method_calls` — catches `.map(|x| x.foo())` → `.map(Foo::foo)`

## Example

Building a Tokio-based HTTP service with typed errors:

```rust
// crates/core/src/error.rs
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ServiceError {
    #[error("database: {0}")]
    Db(#[from] sqlx::Error),
    #[error("not found")]
    NotFound,
}

// crates/api/src/main.rs
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let pool = PgPoolOptions::new()
        .max_connections(20)
        .connect(&std::env::var("DATABASE_URL")?).await?;

    let pool = Arc::new(pool);

    let app = Router::new()
        .route("/users/:id", get(get_user))
        .with_state(pool);

    axum::Server::bind(&"0.0.0.0:3000".parse()?)
        .serve(app.into_make_service())
        .await?;
    Ok(())
}

async fn get_user(
    Path(id): Path<i64>,
    State(pool): State<Arc<PgPool>>,
) -> Result<Json<User>, StatusCode> {
    fetch_user(id, &pool).await
        .map(Json)
        .map_err(|e| match e {
            ServiceError::NotFound => StatusCode::NOT_FOUND,
            ServiceError::Db(_) => StatusCode::INTERNAL_SERVER_ERROR,
        })
}
```

Running:
```bash
cargo clippy --workspace -- -D warnings
cargo test --workspace
cargo build --release
```

---

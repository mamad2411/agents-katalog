# Rust Tokio Async

## Summary

**One-sentence:** Tokio async spec: runtime flavour (multi_thread vs current_thread), no blocking calls in async, structured cancellation (JoinSet / select!), bounded channels, timeouts on every await on the wire.

**One-paragraph:** Tokio code breaks when blocking calls (std::fs, sync mutex held across .await) stall worker threads, when unbounded channels accumulate until OOM, when JoinHandle is dropped (silent leak), when select! arms are not cancel-safe, and when timeouts are missing on network awaits. This methodology produces a spec: runtime flavour, blocking offload via `spawn_blocking`, JoinSet or select! for structured concurrency, bounded `tokio::sync::mpsc` channels, and `tokio::time::timeout` on every network await.

**Ефективно для:**

- Перший Tokio service - зафіксувати правила до production.
- Latency spikes - підозра на blocking call всередині async.
- OOM від unbounded mpsc - перейти на bounded.
- Race conditions через select! без cancel-safety.
- Shutdown hangs - JoinHandle dropped silently.

## Applies If (ALL must hold)

- Codebase uses Tokio 1.x runtime.
- Service does network I/O with measurable concurrency.
- Build pipeline can enforce clippy + custom lints.
- Team can refuse PRs that block the runtime.

## Skip If (ANY kills it)

- Code is CPU-bound batch work - use rayon instead.
- Sync Rust app with no async - use blocking std + threads.
- Single-file experiment that will be deleted.
- Async runtime is async-std or smol - this methodology is Tokio-specific.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Runtime requirement | multi_thread vs current_thread + worker count | engineering |
| Blocking inventory | list of blocking calls (fs, ffi, legacy) | engineering |
| Channel cardinality | expected producer/consumer rates | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[python-async-patterns]] | shared async discipline - bounded fan-out + timeouts. |
| [[websocket-design]] | downstream consumer of WS handlers built on Tokio. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: runtime flavour explicit, no blocking in async, timeout on network, bounded channels, structured concurrency, mutex not across await, graceful shutdown | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: runtime, blocking offload, channels, timeouts, shutdown | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-blocking` | haiku | Mechanical scan of crate dependencies. |
| `size-channels` | sonnet | Per-pipeline judgement on capacity. |
| `rewrite-handler` | sonnet | Translate sync paths to async + spawn_blocking. |
| `review-cancel-safety` | opus | Stakes high; select! arms must be cancel-safe. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.rs` | Tokio service skeleton: multi_thread runtime, JoinSet, timeout, CancellationToken shutdown. |
| `templates/Cargo.toml` | Cargo manifest snippet declaring Tokio features. |
| `templates/batch-processor.rs` | Tokio batch-processor: bounded channel + join_set + cancellation. |
| `templates/user-service.rs` | Tokio service example: async handlers + tracing + tower middleware. |
| `templates/_smoke-test.json` | Minimum viable tokio-async artefact for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-tokio-async.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[python-async-patterns]]
- [[websocket-design]]
- [[rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - runtime config, blocking inventory, channel boundedness, timeout coverage - onto a rule from `content/01-core-rules.xml`. Use it before merging Tokio code: it catches blocking-in-async, unbounded mpsc, and missing timeouts upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/main.rs`

```rust
use std::time::Duration;
use tokio::sync::mpsc;
use tokio::task::JoinSet;
use tokio::time::timeout;
use tokio_util::sync::CancellationToken;

#[tokio::main(flavor = "multi_thread", worker_threads = 8)]
async fn main() -> anyhow::Result<()> {
    let shutdown = CancellationToken::new();
    let (tx, mut rx) = mpsc::channel::<u64>(1024);

    let mut set = JoinSet::new();
    for n in 0..16u64 {
        let token = shutdown.clone();
        let tx = tx.clone();
        set.spawn(async move {
            tokio::select! {
                _ = token.cancelled() => Ok::<(), anyhow::Error>(()),
                r = timeout(Duration::from_secs(3), do_work(n)) => {
                    let v = r??;
                    tx.send(v).await?;
                    Ok(())
                }
            }
        });
    }
    drop(tx);

    let _ = tokio::signal::ctrl_c().await;
    shutdown.cancel();
    while let Some(res) = set.join_next().await {
        let _ = res?;
    }
    while let Some(_v) = rx.recv().await {}
    Ok(())
}

async fn do_work(n: u64) -> anyhow::Result<u64> { Ok(n * 2) }
```

### `templates/Cargo.toml`

```toml
[dependencies]
tokio = { version = "1", features = ["rt-multi-thread", "macros", "signal", "time", "sync"] }
tokio-util = { version = "0.7", features = ["rt"] }
anyhow = "1"
```

### `templates/batch-processor.rs`

```rust
// Semaphore-bounded concurrent batch processor.
// Input: Vec<T> + async processor function + concurrency limit
// Output: Vec<Result<R, E>> in original order

use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;

pub struct BatchProcessor {
    concurrency: usize,
}

impl BatchProcessor {
    pub fn new(concurrency: usize) -> Self { Self { concurrency } }

    pub async fn process<T, F, Fut, R, E>(
        &self,
        items: Vec<T>,
        processor: F,
    ) -> Vec<Result<R, E>>
    where
        T: Send + 'static,
        F: Fn(T) -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<R, E>> + Send,
        R: Send + 'static,
        E: Send + 'static,
    {
        let sem = Arc::new(Semaphore::new(self.concurrency));
        let proc = Arc::new(processor);

        stream::iter(items)
            .map(|item| {
                let sem = sem.clone();
                let proc = proc.clone();
                async move {
                    let _permit = sem.acquire().await.unwrap();
                    proc(item).await
                }
            })
            .buffer_unordered(self.concurrency)
            .collect()
            .await
    }
}

// Usage:
// let bp = BatchProcessor::new(10);
// let results = bp.process(user_ids, |id| async move { fetch_user(id).await }).await;
```

### `templates/user-service.rs`

```rust
// Reference async service: try_join! for parallel queries, spawn_blocking for CPU work.
// Input: &Database reference
// Output: Result<T, AppError> on all methods

use argon2::{password_hash::{rand_core::OsRng, PasswordHasher, SaltString}, Argon2};
use crate::{db::Database, error::AppError, models::User};

pub struct UserService<'a> {
    db: &'a Database,
}

impl<'a> UserService<'a> {
    pub fn new(db: &'a Database) -> Self { Self { db } }

    pub async fn list(&self, page: u32, per_page: u32) -> Result<(Vec<User>, i64), AppError> {
        let offset = ((page - 1) * per_page) as i64;
        // Both queries run in parallel — total time = max(query_a, query_b)
        let (users, total) = tokio::try_join!(
            self.db.fetch_users(per_page as i64, offset),
            self.db.count_users()
        )?;
        Ok((users, total))
    }

    pub async fn get_by_id(&self, id: i32) -> Result<User, AppError> {
        self.db.fetch_user_by_id(id).await?
            .ok_or(AppError::NotFound("User not found".into()))
    }

    pub async fn create(&self, name: &str, email: &str, password: &str) -> Result<User, AppError> {
        if self.db.fetch_user_by_email(email).await?.is_some() {
            return Err(AppError::Conflict("Email already exists".into()));
        }
        // CPU-intensive: move to blocking thread to avoid stalling the runtime
        let password_hash = tokio::task::spawn_blocking({
            let password = password.to_string();
            move || {
                let salt = SaltString::generate(&mut OsRng);
                Argon2::default()
                    .hash_password(password.as_bytes(), &salt)
                    .map(|h| h.to_string())
            }
        })
        .await??; // outer ? = JoinError, inner ? = hash error

        self.db.insert_user(name, email, &password_hash).await
    }
}
```

### `templates/_smoke-test.json`

```json
{
  "runtime_flavour": "multi_thread",
  "worker_threads": 4,
  "blocking_offload": "spawn_blocking",
  "channel_policy": {
    "bounded": true,
    "default_capacity": 512
  },
  "timeout_default_ms": 3000,
  "shutdown_signal": "ctrl_c"
}
```

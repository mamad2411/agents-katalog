---
name: container-lifecycle
description: Manages the injectable container lifecycle: building, resolving, inspecting registered types, and shutting down with pre_destruct hooks. Use when setting up the container at app startup or teardown.
---

# Container Lifecycle

## Build

```rust
use injectable::prelude::*;

// Minimal — #[injectable] types are auto-registered via inventory
let container = Container::builder().build().await?;

// With external types
let container = Container::builder()
    .register(DynProvider::new(|| async {
        Ok(sqlx::SqlitePool::connect("sqlite:./app.db").await?)
    }))
    .build().await?;
```

## Resolve

```rust
// Via container (does NOT use singleton cache):
let svc = container.resolve::<UserService>().await?;

// Via context (uses singleton cache — preferred for singletons):
let svc: Inject<UserService> = container.context().extract().await?;
let svc: Arc<UserService>    = container.context().extract().await?;

// Non-failing:
let svc: Option<UserService> = container.try_resolve().await?;
let ext: Option<SqlitePool>  = container.try_resolve_external().await?;
```

## Inspect

```rust
let types = container.registered_types();
// ["AppConfig", "Database", "UserService", …]

assert!(types.contains(&"Database"), "Database must be registered");
```

## Shutdown

```rust
// Calls all #[injectable(pre_destruct)] hooks in reverse construction order
container.shutdown().await?;
```

## Typical main()

```rust
#[tokio::main]
async fn main() {
    let container = Container::builder()
        .register(DynProvider::new(|| async {
            Ok(sqlx::SqlitePool::connect(&std::env::var("DATABASE_URL").unwrap()).await?)
        }))
        .build()
        .await
        .expect("container build failed");

    println!("Registered: {:?}", container.registered_types());

    // Eagerly warm up singletons (runs post_construct hooks)
    container.context().extract::<Inject<Database>>().await.expect("Database init");

    // Run server…
    serve(container).await;

    container.shutdown().await.expect("shutdown failed");
}
```

## Error handling

```rust
match Container::builder().build().await {
    Err(InjectableError::GraphValidationFailed { errors }) => {
        for e in errors { eprintln!("Graph: {e}"); }
        std::process::exit(1);
    }
    Err(e) => { eprintln!("Build failed: {e}"); std::process::exit(1); }
    Ok(c)  => { /* proceed */ }
}
```

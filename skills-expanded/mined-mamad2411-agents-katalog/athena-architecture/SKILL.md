---
name: athena-architecture
description: Athena architecture map for tracing crate ownership, runtime modes, request flow, config and bootstrap, client registry and pooling, and cross-crate subsystem boundaries in the Athena repo. Use when the user asks for an architecture explanation, wants the owning crate or module for a behavior, needs to place a change in the correct layer, or is touching startup, runtime split, provisioning, gateway, daemon, storage, or other cross-cutting contracts.
---

# Athena Architecture

Start from the exact subsystem, route, binary, or config seam the user named. Use docs for orientation, then confirm ownership in the current source before concluding anything.

Current repo target: `athena_rs 3.20.0`.

## Source of truth order

Read in this order:

1. `docs/architecture_overview.md`
2. `docs/architecture_internals_end_to_end.md`
3. `docs/architecture_deployment_and_runtime.md`
4. `docs/architecture_client_registry_and_pooling.md`
5. `Cargo.toml` and `crates/README.md`
6. `src/main.rs`, `src/config.rs`, `src/bootstrap/mod.rs`, and `src/lib.rs`
7. `src/runtime/*.rs` and `crates/athena-daemon/src/*`
8. the owning crate or module for the user’s exact seam
9. the deeper topic doc under `docs/architecture_*.md` that matches the subsystem

If docs and source disagree, prefer the current source and tests in this checkout.

## Use this skill for

- explaining Athena end to end from real code
- deciding where a change belongs before editing
- tracing runtime ownership between `athena_rs` and daemon package binaries
- mapping config, bootstrap, client registry, and pool ownership
- tracing cross-crate behavior across provisioning, gateway, storage, auth, daemon, or control-plane seams

Use a narrower skill instead when the task is already clearly scoped:

- use `athena-storage` for storage-only route and catalog work
- use `athena-rs-sdk` for the public Rust SDK surface

## Place the change in the right layer

Use the root package when the change is about:

- HTTP route registration and Actix request handling
- CLI entrypoints
- `AppState`
- startup bootstrapping and transport policy

Use workspace crates when the change is portable or subsystem-owned:

- `athena-gateway`: gateway contracts and helpers such as `resource_id` fallback logic
- `athena-provisioning`: provider-backed provisioning, bundled SQL execution, and target preparation
- `athena-dns`: managed domain and wildcard host defaults
- `athena-daemon`: daemon binaries and worker ownership
- `athena-s3`: storage catalog and managed-file runtime

Keep generated SQL in `sql/`. Do not hide repo schema changes inside Rust-only bootstrap code.

## Architecture workflow

1. Classify the request before reading deeply:
   - boot, config, or startup
   - request path or gateway execution
   - background worker or daemon ownership
   - provisioning or managed DNS
   - storage or another subsystem-specific seam
2. Trace from the outer layer inward:
   - boot: `src/main.rs` -> `src/config.rs` -> `src/bootstrap/mod.rs`
   - request path: route registration -> handler -> auth and client resolution -> owning crate or driver
   - daemon/runtime: `docs/architecture_deployment_and_runtime.md` -> `src/runtime/*.rs` -> `crates/athena-daemon/src/*`
3. Confirm the owner in code before suggesting a refactor or moving logic between layers.
4. Update architecture docs only when the user wants docs or when the public architecture narrative changed materially.

## Guardrails that matter

Treat the `architecture/` folder as supporting design artifacts, not as the primary ownership truth. The current docs in `docs/` and the current source files are the first-class references.

Do not assume the API process owns all background work. `athena_rs` can skip daemon-owned workers, and clone execution always requires a daemon package binary.

Keep Rust validation in WSL2, not native Windows `cargo test`.

Read [references/runtime-and-crates.md](references/runtime-and-crates.md) when you need the subsystem-to-owner map, common routing hints, or validation suggestions.

## Validation

If you only explained architecture, no validation command is required.

For code changes, prefer the narrowest proof that matches the owning layer.

Broad cross-cutting validation in WSL2:

```powershell
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test --lib --bins --tests'
```

Focused crate-level validation:

```powershell
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test -p athena-dns'
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test -p athena-provisioning'
wsl.exe bash -lc 'cd /mnt/c/Users/floris/Documents/GitHub/athena && cargo test -p athena-daemon'
```

If a route or documented contract changed, also use the relevant focused root tests such as `tests/openapi.rs` or route-specific auth regressions.

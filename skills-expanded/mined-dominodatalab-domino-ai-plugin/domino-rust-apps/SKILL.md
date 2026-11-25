---
name: domino-rust-apps
description: Build a Rust web app (axum) in Domino and ship it as a Domino App that starts from a prebuilt binary. Covers installing a pinned Rust toolchain into a Compute Environment with rustup, Cargo project defaults (edition 2024, rust-toolchain.toml, Cargo.lock, Clippy pedantic, rustfmt, cargo-nextest, cargo-deny), rust-analyzer for the IDE and coding agents, check hooks, calling Domino as the viewer with extended identity propagation, dev and release build profiles, keeping target/ out of Git and Domino storage, and an app.sh that runs the binary in App Preview and deployments without compiling. Use when the user wants a Rust app, API, dashboard or Proa site on Domino, a performance-sensitive or correctness-critical App, or asks to set up Rust, cargo, Clippy, nextest or rust-analyzer in a Domino Workspace or environment.
compatibility: Domino 6.3 and Domino Cloud. Building needs a Compute Environment with the Rust toolchain and access to crates.io or a mirror; the App runs the prebuilt binary and needs no toolchain.
---

# Rust Apps on Domino

Applies to Domino 6.3 and Domino Cloud.

Choose Rust for Apps where latency, throughput or correctness matter more than iteration speed: the compiler and Clippy reject whole classes of bugs before anything runs. A Rust App is **built once** in a Workspace or Job and `app.sh` only runs the binary, so App Preview and every deployment start in seconds.

Like every App it must be idempotent: it restarts at any time and can run as several replicas at once, so startup writes nothing (migrate and seed in a Job), each write is an upsert or carries an idempotency key under a unique constraint, so a retry stores it once, and state lives in a database or Dataset ([details](../domino-apps/FRAMEWORKS.md#make-the-app-idempotent)).

Instructions assume a Git-based Project (code in `/mnt/code`). DFS differences are under "DFS Projects".

## Workflow

1. **Toolchain.** In the Workspace run `rustc --version` and `cargo nextest --version`. If Rust is missing or its version differs from `channel` in `rust-toolchain.toml`, add it to the Project's Compute Environment ([ENVIRONMENT.md](./ENVIRONMENT.md)), rebuild, and restart the Workspace on the new revision. If crates.io is reached through Artifactory or Nexus Repository, configure Cargo there too ([ENVIRONMENT.md](./ENVIRONMENT.md#package-registry-mirrors)).
2. **Scaffold.** Copy this skill's `assets/app/` directory into the project root as is, dotfiles included. Rename the package (`name` in `Cargo.toml` and the `use` line in `src/main.rs`). Run `cargo generate-lockfile`, then commit everything, `Cargo.lock` included. Turn on the Git hook once per clone: `git config core.hooksPath .githooks`.
3. **Develop.** Port 8888 belongs to the Workspace IDE, so run the server beside it with `PORT=8501 cargo run` and exercise it with `curl localhost:8501/healthz`. Run `bash scripts/check.sh` before every commit. Every URL the browser sees must be relative ([APP.md](./APP.md)).
4. **Build the binary.** Commit the code, then run `bash scripts/build-dist.sh`. It runs `cargo build --locked --profile dist` and writes a dated build (`2026.10.15`, then `.2`) with its source stamp to `/mnt/artifacts/dist/<name>/`, keeping the previous build ([rollback, Version Notes](../domino-apps/FRAMEWORKS.md#build-once-and-version-builds)). Save with **File Changes > Sync All Changes**, which pushes the code to Git and the build to Domino storage.
5. **Preview and publish** with `app.sh` as the App file ([domino-apps](../domino-apps/SKILL.md) covers Preview, publish and deploy). `app.sh` runs the newest build whose stamp matches the committed sources; if none does it exits with a message rather than compiling. Fix that by repeating step 4, not by editing `app.sh`.

## Rules

- **Never compile in `app.sh`.** Every Preview start, live sync, restart and replica runs it; a build there takes minutes and needs crates.io.
- **Build where the App runs.** The binary links the environment's glibc and targets one CPU architecture. Hardware tiers can run on different node types (amd64 or arm64, different CPU generations), so build on the App's environment and tier, or in a Job on that tier; `app.sh` refuses a binary built for another architecture.
- **Commit `Cargo.lock` and build with `--locked`**, so the binary uses the dependency versions you tested.
- **Never commit `target/`**: one Workspace build holds hundreds of MB to GBs. `.gitignore` excludes it.
- **Secrets** come from Project environment variables read by the server (`DATABASE_URL`, `MODEL_API_URL`, `MODEL_API_TOKEN` in the template), never from files in the repository.
- **Anticipate custom root CAs and a TLS-inspecting proxy.** Outbound code trusts the OS certificate store, honours `HTTPS_PROXY`/`NO_PROXY` and keeps in-cluster calls off the proxy ([APP.md](./APP.md#outbound-tls-and-http-proxies)).
- **Act as the viewer for the viewer's data.** `src/domino.rs` calls the Domino API with the viewer's forwarded token, or as the publisher through `DOMINO_API_PROXY`; viewer calls need extended identity propagation on the App and the viewer's consent ([APP.md](./APP.md#identity-acting-as-the-viewer-or-the-publisher)).

## Project defaults (from `assets/app/`)

| File | Sets |
|---|---|
| `rust-toolchain.toml` | Exact toolchain (`channel = "1.99.1"`) and components; keep it equal to the environment's |
| `Cargo.toml` | Edition 2024, `unsafe_code = "forbid"`, Clippy `pedantic` at warn (`priority = -1`), dev and `dist` profiles; axum, askama, sqlx (Postgres) and reqwest on one rustls stack that trusts the OS certificate store |
| `rustfmt.toml` | `style_edition = "2024"`, so editors format like `cargo fmt` |
| `.config/nextest.toml` | nextest defaults and a `ci` profile with JUnit output |
| `deny.toml` | cargo-deny: RustSec advisories, permissive licences, no wildcard versions, crates.io only |
| `scripts/check.sh` | fmt, Clippy with `-D warnings`, nextest, doctests (nextest skips them), cargo-deny |
| `scripts/build-dist.sh`, `scripts/stamp.sh`, `app.sh` | Dated builds, source stamp, pick and run |
| `.githooks/pre-commit`, `scripts/agent-hooks/` | Git and coding-agent hooks ([TOOLING.md](./TOOLING.md#hooks)) |
| `.vscode/` | rust-analyzer runs Clippy on save; the file watcher skips `target/` |

## Build commands

| Purpose | Command |
|---|---|
| Run beside the IDE | `PORT=8501 cargo run` (dev profile) |
| All gates | `bash scripts/check.sh` |
| Shipping binary | `bash scripts/build-dist.sh` (`dist` profile: release with fat LTO, one codegen unit, stripped symbols) |

Keep `panic = "unwind"`: tokio and axum confine a panicking request to its connection, while `abort` stops the App for every viewer. Trade-offs, CPU-specific builds and profile-guided optimization: [TOOLING.md](./TOOLING.md#build-profiles).

## Editors and coding agents

The environment installs rust-analyzer. Check it with `rust-analyzer --version`, not `which`. Per-agent LSP and hooks: [TOOLING.md](./TOOLING.md).

## DFS Projects

- Code lives in `/mnt`. `.dominoignore` must keep `target/` out: a Rust `target/` alone exceeds the default 10,000-file Project limit.
- Build with `DIST_DIR=dist bash scripts/build-dist.sh` and save with **File Changes > Sync to Domino**; `app.sh` finds `dist/`.
- DFS has no Git, so `.githooks` does nothing; rely on `scripts/check.sh` and the agent hooks.

## Reference files

- [ENVIRONMENT.md](./ENVIRONMENT.md): Dockerfile instructions, upgrades, mirrors and offline builds
- [APP.md](./APP.md): the axum template, proxy rules, identity, Postgres, model calls, outbound TLS and proxies, how the binary is shipped (or kept in Git)
- [TOOLING.md](./TOOLING.md): lints, tests, cargo-deny, build profiles, `target/` size, LSP and hooks per IDE and agent
- [PROA.md](./PROA.md): Proa sites (server-rendered pages and islands) as Domino Apps

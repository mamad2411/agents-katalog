---
name: follow-release-deploy-crates
description: Release a Rust crate to crates.io — cargo publish flow with verify
argument-hint: "[crate-name]"
related:
  - run-release
  - run-check
  - follow-secret-manager
  - resolve-errors
  - learn
  - ask-me
---

## Goal

Publish a Rust crate to crates.io correctly — complete metadata, auth ready, publish then verify on the registry

## Scope

- covers: manual publish with `cargo publish` — metadata checks, token, dry-run, publish, verify
- automated release (release-plz/cargo-release + GitHub Actions) → follow the parent `/follow-release` Step 3

## Execute

### 1. Verify Crate Metadata

> Goal: `Cargo.toml` is ready to publish

1. check required fields: `name`, `version`, `description`, `license` (or `license-file`)
2. check recommended fields: `authors`, `repository`, `homepage`, `keywords` (≤5), `categories`
3. check the `publish` field is not set to `false`
4. if a workspace → identify clearly which crate to publish (`-p <name>`)

### 2. Authenticate

> Goal: the token is ready for publishing

1. check credentials with `cargo login` — the token is stored in `~/.cargo/credentials.toml`
2. CI: use `CARGO_REGISTRY_TOKEN` — store it via `/follow-secret-manager`
3. if there is no token → `/ask-me` so the user creates one on crates.io

### 3. Pre-Publish Checks

> Goal: the crate builds and packages correctly before publishing

1. run `/run-check` — tests and lint must pass
2. run `cargo publish --dry-run` to check package contents and warnings
3. check the version has not been published yet (check crates.io or `cargo search <name>`)

### 4. Publish

> Goal: the crate reaches the registry

1. run `cargo publish` (or `cargo publish -p <name>` in a workspace)
2. record the successfully published version

### 5. Post-Publish Verify

> Goal: the crate is usable from the registry

1. wait for the registry index update (may take a short while), then check the crate page on crates.io
2. verify with `cargo add <name>` or `cargo install <name>` in a temp project
3. if the publish went wrong → `cargo yank --vers <version>` to withdraw the version (not delete it), then `/resolve-errors`
4. success → report the version, then run `/run-release` if the parent flow needs a multi-platform release

## Rules

### 1. Publish Is Irreversible

- once published it cannot be deleted — use `cargo yank` only; dry-run + version check always first
- the version bump must be committed/tagged per project convention

### 2. Metadata Quality

- never publish with missing required metadata — cargo will reject it
- secrets/tokens only through `/follow-secret-manager`

### 3. Docs First

- unsure about new flags/features → check official docs via `/learn-from-web` instead of guessing

## Expected Outcome

- the crate published on crates.io with a new version, actually installable
- a wrong version yanked if needed

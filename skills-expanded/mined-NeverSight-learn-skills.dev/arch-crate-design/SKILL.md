---
name: arch-crate-design
description: Use for Rust crate boundaries, workspace structure, feature flags, public versus internal APIs, layering, and testable module design.
globs: ["**/Cargo.toml", "**/*.rs"]
---

# Rust Crate Design

Use this when the hard part is where a Rust responsibility should live, not
how to write the next function.

## Working stance

- Keep domain logic away from IO, framework glue, and process setup.
- Public crates should expose stable concepts, not convenience shortcuts.
- Prefer thin binaries and reusable libraries.
- Add a workspace only when multiple crates truly need shared versioning,
  dependency policy, lints, or release choreography.
- Feature flags should add integration or optional capability, not split core
  behaviour into incompatible worlds.
- Tests should follow the same boundaries the design claims to have.

## Decision surface

- New crate: create one when the boundary is stable, reusable, and easier to
  test in isolation.
- Workspace: use one when crates share release policy, lint policy, or common
  metadata; skip it for a single crate with no real split.
- New module only: prefer it when the split is still implementation detail.
- Library crate: prefer it for reusable domain logic, typed APIs, and testable
  boundaries.
- App crate: prefer it for binaries, runtime wiring, and integration glue.
- Public API: expose the narrow contract, keep helpers and framework types
  internal where possible.
- Feature flag: use it for optional dependencies or integrations, not as a
  substitute for design decisions.
- Development utility crate: use one for test helpers, code generation, or
  developer tooling only if it does not create a dependency cycle with the
  crates it supports.

## Packaging and release guidance

- `workspace.package` is the right place for shared package metadata such as
  version, edition, `rust-version`, licence, repository, and `publish`, but
  members must opt in with `{key}.workspace = true`.
- Keep publishability in mind when splitting crates. If one crate must be
  published before another, release order becomes part of the design.
- Avoid dependency cycles by keeping helpers and macros pointed inward or
  downward; if a support crate depends on the main crate and the main crate
  depends back on it, the split is wrong.
- Development utility crates should stay private unless they are genuinely
  reusable and publishable on their own.
- Prompt the user for package metadata when creating a new library crate, a
  binary meant for external installation, or any crate that may be published.
  Minimum useful fields are name, description, licence, repository, readme,
  homepage or docs URL if applicable, and whether publishing is intended.
- For internal app crates, do not stop work to demand full crates.io discovery
  metadata unless the user signals distribution or publishability.
- If a binary should support `cargo-binstall`, make release artifacts stable
  and predictable, then add `[package.metadata.binstall]` only once the
  release URL, archive format, and binary path are known. Use overrides when
  some targets ship different artifact names.

## Example workspace layout

```plaintext
my-product/
├── Cargo.toml
├── crates/
│   ├── core-lib/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── http-api/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── cli-app/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── test-support/
│       ├── Cargo.toml
│       └── src/lib.rs
└── xtask/
    ├── Cargo.toml
    └── src/main.rs
```

Suggested roles:

- `core-lib`: reusable domain logic and typed APIs.
- `http-api`: transport and framework glue built on the library crates.
- `cli-app`: the user-facing binary with thin process wiring.
- `test-support`: private test helpers; keep `publish = false` unless it is
  intentionally reusable outside the workspace.
- `xtask`: developer automation and release tooling; keep it out of the
  publishable dependency graph.

This shape is justified only when the split matches real boundaries. If
`http-api` and `cli-app` are just thin shells over `core-lib`, the workspace is
earning its keep. If all crates depend on each other freely, it is not.

## Red flags

- binaries contain most of the business logic,
- workspaces exist only to mimic large-project aesthetics,
- public types expose runtime or framework internals,
- one crate imports everything because boundaries are nominal only,
- helper or macro crates create cycles or block publication order,
- feature combinations create meaningfully different programs,
- a crate intended for publication is missing the metadata needed for discovery
  and release tooling,
- a distributed binary claims `binstall` support before release artifacts and
  naming are stable,
- integration tests must reach through layers to set up basic scenarios.

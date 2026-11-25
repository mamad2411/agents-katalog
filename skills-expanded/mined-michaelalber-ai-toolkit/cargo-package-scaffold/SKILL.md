---
name: cargo-package-scaffold
audience: team
description: >
  Cargo crate creation with CI/CD pipeline setup, test harness, and crates.io publish workflow.
  Use when creating new Rust crates, configuring Cargo.toml metadata, setting up GitHub Actions
  for Rust CI, or publishing to crates.io. Do NOT use when the crate is internal-only and not
  intended for crates.io publication; Do NOT use when the target is a binary application — this
  skill targets library crates.
---

# Cargo Package Scaffold

> "A crate is a promise. Its Cargo.toml is the contract. Its tests are the proof.
> Semver is a social contract — publish nothing you would not stake your reputation on."

## Core Philosophy

Publishing a Rust crate is a commitment. Once a version is on crates.io, it cannot be deleted —
only yanked. This skill enforces the practices that make crates trustworthy: complete metadata,
semver discipline, a CI gate that blocks broken publishes, and a test harness that covers the
public API surface. The scaffold is opinionated by default and configurable by exception — every
generated crate starts with `deny(unsafe_code)`, `#![warn(missing_docs)]`, and a CI pipeline that
runs `cargo test`, `cargo clippy`, `cargo fmt --check`, and `cargo publish --dry-run` on every push.

**Non-Negotiable Constraints:**
1. SEMVER — breaking changes require a major version bump; verify with `cargo semver-checks` in CI.
2. DRY-RUN GATE — `cargo publish --dry-run` must pass in CI before any release.
3. DOCUMENTED — every public item has a doc comment; `#![warn(missing_docs)]` + `cargo doc` in CI.
4. SAFE BY DEFAULT — `#![deny(unsafe_code)]`; unsafe requires explicit justification and a `// SAFETY:` comment.
5. MINIMAL DEFAULTS — `default = []` features and an explicit `include` list; users opt in, and the publish never ships `.github/` or `target/`.

The full principle set, anti-patterns, discipline rules, and recovery steps live in
`references/conventions.md`.

## Workflow

```
DETECT      Read workspace Cargo.toml (inherit [workspace.package] if present), existing
            .github/workflows/, and deny.toml. Report findings. No files written.

SCAFFOLD    Create the crate skeleton:
              <crate-root>/
              ├── Cargo.toml          # complete metadata (see cargo-metadata-reference.md)
              ├── src/lib.rs          # deny(unsafe_code), warn(missing_docs), module structure
              ├── tests/integration.rs# integration stubs for the public API
              ├── examples/basic.rs   # minimal working example
              ├── CHANGELOG.md        # Keep a Changelog format
              └── README.md           # description, install, quick start
            Exit: cargo build / test / doc --no-deps all pass.

CI          Create .github/workflows/ci.yml with jobs: test (stable + MSRV matrix),
            lint (clippy -D warnings + fmt --check), docs, semver (PRs only), publish-dry-run.

RELEASE     Create release.yml triggered on v* tags: full CI gate, then publish to crates.io via
            CARGO_REGISTRY_TOKEN secret, then a GitHub Release with the CHANGELOG excerpt.
            (release.yml + secret documented in release-checklist.md.)

VERIFY      Run and require pass: cargo build · test · clippy -- -D warnings · fmt --check ·
            doc --no-deps · publish --dry-run. A captured command result, never a claim.
```

**Exit criteria:** crate builds, tests pass, lints clean, docs complete, `publish --dry-run` passes;
CI and release workflows created; `CARGO_REGISTRY_TOKEN` documented for the user to add.

## State Block

```
<cargo-package-scaffold-state>
phase: DETECT | SCAFFOLD | CI | RELEASE | VERIFY | COMPLETE
crate_name: [name]
crate_type: lib | bin | proc-macro
workspace: true | false
workspace_metadata_inherited: true | false
msrv: [version]
unsafe_allowed: true | false
features: [comma-separated]
ci_created: true | false
release_workflow_created: true | false
build_status: pass | fail | not-run
last_action: [description]
next_action: [description]
</cargo-package-scaffold-state>
```

## Output Template

- **Cargo.toml** — `references/cargo-metadata-reference.md` (required + recommended fields, include/exclude).
- **lib.rs, CI workflow, progress report** — `references/scaffold-templates.md`.
- **release.yml, CHANGELOG format, semver/yanking policy, pre-release checklist** — `references/release-checklist.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `rust-architecture-checklist` | Run after scaffold to verify the crate's internal architecture. |
| `rust-security-review` | Run before first publish to audit for security issues. |
| `rust-migration-analyzer` | Use when migrating an existing crate to a new Rust edition. |
| `supply-chain-audit` | Audit crate dependencies for CVEs and license compliance before publish. |

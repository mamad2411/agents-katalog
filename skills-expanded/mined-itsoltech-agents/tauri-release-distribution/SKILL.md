---
name: tauri-release-distribution
description: "Release Tauri apps with bundling, signing, updater signatures, channels, CI, and rollback."
---

# Tauri Release Distribution

Release Tauri as a signed, updateable, platform-specific product. Packaging decisions affect security, updater behavior, installer trust, artifact compatibility, CI cost, and rollback.

## Process

1. Inspect the repo's Tauri, Rust, package manager, frontend framework, Tauri plugins, bundler config, signing, notarization, updater, CI, release branch/tag policy, and smoke-test evidence.
2. For an existing repo, detect pinned Tauri, Rust toolchain, package manager, frontend, and plugin versions. For a new project, use latest stable. For signing, updater signatures, target artifacts, platform behavior, or security defaults, verify official docs through `itsol-current-tech-context`.
3. Choose distribution from product constraints: target OS/architectures, direct download or store, update channel model, installer expectations, sidecars, local data, enterprise environment, and support burden.
4. Gate release with frontend checks, Rust checks, dependency checks, per-platform build, signing/notarization, updater signature verification, artifact checksums, and packaged-app smoke tests.
5. Plan rollback before release: previous artifacts, metadata rollback, channel freeze, forward-fix path, local data migration compatibility, and user recovery steps.

## Output

For plans, produce decisions, required secrets, artifact matrix, CI gates, smoke tests, update-channel flow, release notes needs, rollback steps, and residual risks. For reviews, lead with blockers that could ship unsigned, unnotarized, unupdateable, unsafe, incorrectly scoped, or untestable artifacts.

## Focused References

- [01-bundling-artifacts.md](./references/01-bundling-artifacts.md) - Tauri bundling config, app identity, target artifacts, sidecars, assets, source maps, and platform package decisions.
- [02-signing-notarization-secrets.md](./references/02-signing-notarization-secrets.md) - Windows/macOS/Linux signing, notarization, private keys, certificates, checksums, SBOM, and reproducibility.
- [03-updater-signatures-channels.md](./references/03-updater-signatures-channels.md) - Tauri updater signatures, public/private keys, metadata, channels, staged rollout, migrations, and update QA.
- [04-ci-smoke-rollback.md](./references/04-ci-smoke-rollback.md) - CI release gates, platform smoke matrix, rollout, rollback, and release checklist.

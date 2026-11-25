---
name: electron-release-distribution
description: "Release Electron apps with packaging, signing, notarization, update channels, CI, and rollback."
---

# Electron Release Distribution

Release Electron as a signed, updateable, platform-specific product. Packaging decisions affect security, updater behavior, installer trust, artifact size, CI cost, and rollback.

## Process

1. Inspect the repo's Electron, package manager, builder, signing, notarization, auto-update, CI, release branch/tag policy, and smoke-test evidence.
2. For an existing repo, detect pinned Electron and packaging tool versions. For a new project, use latest stable. For signing, notarization, updater metadata, platform targets, or security defaults, verify official docs through `itsol-current-tech-context`.
3. Choose packaging and distribution from product constraints: install targets, stores, update server, native modules, enterprise environment, and support burden.
4. Gate release with typecheck, lint, unit/integration tests, packaged-app smoke tests per platform, signing/notarization checks, artifact checksums, and updater channel validation.
5. Plan rollback before release: previous version availability, update-channel freeze, metadata rollback, storage migration compatibility, and user data recovery.

## Output

For plans, produce decisions, required secrets, CI gates, platform matrix, smoke tests, release notes requirements, rollback steps, and residual risks. For reviews, lead with blockers that could ship unsigned, unnotarized, unupdateable, unsafe, or untestable artifacts.

## Focused References

- [01-tooling-packaging-decisions.md](./references/01-tooling-packaging-decisions.md) - electron-vite, Forge, builder, targets, native modules, ASAR, source maps, and artifact contents.
- [02-signing-notarization-artifacts.md](./references/02-signing-notarization-artifacts.md) - Windows/macOS/Linux signing, notarization, secrets, checksums, SBOM, and reproducibility.
- [03-auto-update-channels.md](./references/03-auto-update-channels.md) - updater choices, channels, metadata, migrations, restart UX, and update QA.
- [04-ci-smoke-rollback.md](./references/04-ci-smoke-rollback.md) - CI release gates, platform smoke tests, rollout, rollback, and release checklist.

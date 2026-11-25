---
name: tauri-release
description: Build, sign, package, update, and distribute Tauri 2 applications safely. Use when preparing a release, configuring installers, setting up updates, or diagnosing packaging failures.
---

# Tauri release

This skill is scoped to Tauri 2. Verify version-sensitive fields, commands, signing formats, and updater behavior against the installed CLI/plugins and [official distribution docs](https://v2.tauri.app/distribute/).

## Workflow

1. Confirm version alignment across frontend packages, `src-tauri/Cargo.toml`, app configuration, plugins, lockfiles, and generated native projects. Run the full test suite and a clean production build.
2. Audit [icons](https://v2.tauri.app/develop/icons/), bundled [resources](https://v2.tauri.app/develop/resources/), sidecars, entitlements/manifest permissions, bundle identifiers, and architecture-specific artifacts. Verify each declared path exists and is included in the package.
3. Follow distribution guidance for target OSes. Verify signing, notarization/store requirements, installer dependencies, minimum OS versions, Android keystore/app signing, iOS provisioning/signing, and CI secrets for every target.
4. For updates, follow the [updater guide](https://v2.tauri.app/plugin/updater/): generate artifacts, configure the public key and endpoint, keep private signing keys out of the repository, and test signature rejection, interrupted updates, downgrade policy, restart, and rollback/recovery.
5. Publish checksums/signatures and release notes identifying supported platforms, known limitations, migrations, update/rollback steps, and any mobile store constraints.
6. Install produced artifacts in clean environments and verify launch, permissions, icons/resources, upgrade, downgrade policy, rollback, uninstall, and update verification. Do not claim cross-platform support until each target artifact has been built and smoke-tested.

## Safe defaults

- Build in reproducible, isolated CI jobs; do not sign locally with an untracked key by default.
- Store signing private keys and updater credentials in a secret manager; never print or commit values.
- Use TLS endpoints and validate update metadata/artifacts before installation.
- Treat packaging keys, updater configuration, store metadata, and native project fields as version-sensitive.

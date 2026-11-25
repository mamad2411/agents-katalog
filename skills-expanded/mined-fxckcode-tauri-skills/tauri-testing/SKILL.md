---
name: tauri-testing
description: Test Tauri 2 frontends, Rust commands, IPC contracts, permissions, and packaged applications. Use when adding tests, diagnosing regressions, or preparing a Tauri change for review.
---

# Tauri testing

Start with the official [testing guide](https://v2.tauri.app/develop/tests/). This skill is scoped to Tauri 2; record installed CLI, crate, frontend, and plugin versions for failures.

## Workflow

1. Run existing frontend and Rust tests before editing; identify real scripts, resources, sidecars, and target matrix.
2. Unit-test frontend state and adapters without requiring a WebView. Unit-test Rust validation, transformations, and error mapping with normal Rust tooling.
3. Test IPC at the boundary: valid and malformed payloads, unknown commands, typed errors, serialization compatibility, events, and channel ordering/cancellation where used.
4. Test security behavior explicitly: denied capability, scope escape attempts, untrusted paths/URLs, CSP/header failures, and remote-content restrictions.
5. Test packaging inputs: configured [resources](https://v2.tauri.app/develop/resources/) exist at expected paths and [sidecars](https://v2.tauri.app/develop/sidecar/) are present, executable, target-matched, permissioned, and correctly invoked. Exercise missing-resource and sidecar failure paths.
6. Run platform-aware integration tests for packaged behavior where the feature uses OS APIs. For Android and iOS, install a debug build on at least one emulator/device per target, smoke-test launch, navigation, IPC, permissions, lifecycle resume, resource/sidecar behavior where supported, and graceful unsupported-platform handling.
7. Run `cargo test`, frontend tests, the project's Tauri build/check command, and packaged smoke tests. Prefer CI matrix evidence over a single desktop dev run.

## Safe defaults

- Prefer deterministic assertions over sleeps and screenshots alone.
- Keep fixtures isolated; never use real credentials, personal files, or production endpoints.
- A passing dev build is insufficient evidence for packaging, permissions, mobile, or updater behavior.

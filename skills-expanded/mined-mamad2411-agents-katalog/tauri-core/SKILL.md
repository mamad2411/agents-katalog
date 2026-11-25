---
name: tauri-core
description: "Shared reference for the Tauri cluster: the v2 security model (capabilities → permissions → scopes), the IPC trust boundary and command contract, the process/runtime model, CSP, and the per-platform distribution matrix. USE WHEN configuring Tauri permissions/scopes/CSP, wiring IPC commands, or planning a release — the interlocking rules every Tauri spoke shares."
cluster: tauri
version: 1.0.0
---

# Tauri Core

Shared model for the `tauri` cluster. The config, IPC, and distribution spokes all depend on
these interlocking concepts — keep them consistent here so no spoke contradicts another.

## 1. The security model (Tauri v2's defining feature)

Access is **default-deny**. You opt windows into capabilities, which bundle permissions,
which may be narrowed by scopes:

```
Window/Webview ──has──> Capability ──includes──> Permission(s) ──constrained by──> Scope(s)
```

- **Permission** — a single allowed command/behavior (often shipped by a plugin, e.g. `fs:read-files`). Default + custom permissions live in `src-tauri/permissions/` and plugin manifests. → `configuring-tauri-permissions`
- **Capability** — a JSON file in `src-tauri/capabilities/` that grants a *set* of permissions to specific windows/webviews (by label) and platforms. This is how you wire permissions to surfaces. → `configuring-tauri-capabilities`
- **Scope** — allow/deny data that narrows a permission (e.g. which paths `fs` may touch, which URLs `http` may reach). Deny scopes win over allow. → `configuring-tauri-scopes`

**Rule:** grant the **narrowest** capability that works; prefer per-window capabilities over
global; treat any scope widening (new path, new host) as a security change worth stating.

## 2. CSP & web boundary

The Content-Security-Policy in `tauri.conf.json` governs what the webview may load/execute.
Keep it strict (no blanket `unsafe-inline`/`*`); add only the origins you need.
Custom protocol/header needs → `configuring-tauri-csp`, `configuring-tauri-http-headers`.

## 3. IPC trust boundary & command contract

The frontend is **untrusted**; Rust is the trusted core. Everything crosses one boundary:

- **Commands** (JS → Rust): `#[tauri::command]` fns registered in the `invoke_handler`; called via `invoke()`. Validate every argument in Rust — never trust the webview. → `calling-rust-from-tauri-frontend`
- **Events** (Rust → JS and back): `emit`/`listen` for fire-and-forget streams. → `calling-frontend-from-tauri-rust`, `listening-to-tauri-events`
- A command is reachable from a window only if a capability grants the matching permission. → `understanding-tauri-ipc`

## 4. Process & runtime model

- **Core process** (Rust) owns the event loop, windows, plugins, and the privileged API; one per app. → `understanding-tauri-process-model`, `understanding-tauri-runtime-authority`
- **Webview process(es)** render UI, sandboxed, reach the core only via IPC.
- **Sidecars** are external binaries the core spawns under scope control. → `embedding-tauri-sidecars`, `running-nodejs-sidecar-in-tauri`
- Lifecycle/security posture → `understanding-tauri-lifecycle-security`, `understanding-tauri-ecosystem-security`.

## 5. Distribution matrix

| Target | Spoke | Needs |
|---|---|---|
| macOS | `distributing-tauri-for-macos` | Apple Developer ID, notarization |
| Windows | `distributing-tauri-for-windows` | code-signing cert (Authenticode) |
| Linux | `packaging-tauri-for-linux` | AppImage/deb/rpm targets |
| iOS | `distributing-tauri-for-ios` | Apple provisioning, Xcode toolchain |
| Android | `distributing-tauri-for-android` | Android SDK/NDK, keystore |

Cross-cutting: `signing-tauri-apps` (identities), `optimizing-tauri-binary-size`,
`building-tauri-with-github-actions` (CI matrix), `using-crabnebula-cloud-with-tauri` (managed).

## 6. Version / conventions

- Target **Tauri v2** (`tauri-v2`); the capability/permission system above is v2-specific. Coming from v1 → `migrating-tauri-apps`. Keep core + plugin versions aligned → `updating-tauri-dependencies`.
- Frontend is framework-agnostic (any JS, or a Rust frontend) → `integrating-tauri-js-frontends`, `integrating-tauri-rust-frontends`.

## 7. Shared guardrails

- **Default-deny**: narrowest capability/permission/scope that works; per-window over global.
- Validate all command inputs in Rust; the webview is untrusted.
- Strict CSP; explicit allowlists only.
- State every security-surface change (new permission, scope path, host, capability).
- Confirm signing identity + platform prerequisites **before** a release build.
- Tauri vs Electron: pick Tauri for small binaries + a hardened Rust core + the capability model; if the team is all-JS with heavy Node-native needs, weigh the `electron` cluster.

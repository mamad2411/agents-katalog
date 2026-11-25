---
name: tauri-architecture
description: Design Tauri 2 application boundaries, IPC contracts, state ownership, and platform abstractions. Use when planning features, splitting frontend and Rust responsibilities, or reviewing a Tauri architecture.
---

# Tauri architecture

This skill is scoped to Tauri 2. Tauri combines a web frontend, an application Rust core, a system WebView, and optional plugins. Start with the [architecture overview](https://v2.tauri.app/concept/architecture/) and verify version-sensitive details against installed docs.

## Workflow

1. State the trust boundary and data flow: frontend input → command/channel/event → Rust validation and side effect → typed result.
2. Use the Tauri [process model](https://v2.tauri.app/concept/process-model/): keep presentation in the webview, privileged work in the Rust core, and platform APIs behind narrow commands or plugins.
3. Define small serializable command contracts, explicit errors, and stable identifiers. Avoid a generic “execute” command.
4. Choose IPC deliberately: commands suit request/response; events suit notifications and broadcast-style messages; [channels](https://v2.tauri.app/concept/inter-process-communication/) suit ordered, higher-throughput streaming tied to a request. Document ownership, cancellation, backpressure, and listener cleanup.
5. For brownfield or isolated integrations, study [brownfield IPC](https://v2.tauri.app/concept/inter-process-communication/brownfield/) and [isolation](https://v2.tauri.app/concept/inter-process-communication/isolation/). Keep untrusted content away from privileged authority and mediate crossings with explicit contracts.
6. Manage state using [state management](https://v2.tauri.app/develop/state-management/); avoid global mutable state unless ownership and synchronization are clear. Isolate platform-specific behavior behind Rust modules or plugin boundaries.
7. Keep startup and artifact size intentional. Use the [size guidance](https://v2.tauri.app/concept/size/) to audit release profile, assets, dependencies, symbols, and unnecessary frontend payload before adding optimization flags.

## Review questions

- Which process owns each secret, file, network call, and side effect?
- Can the frontend call more than this feature requires?
- Is a command, event, or channel the correct IPC contract?
- Does brownfield content require isolation or a separate capability?
- What is the smallest cross-platform core, and where do Android/iOS differences live?

---
name: electron-desktop-debugging
description: "Debug Electron processes, IPC, sessions, packaged builds, updates, crashes, and memory."
---

# Electron Desktop Debugging

For bugfix authorization and plan prerequisites, defer to `itsol-workflow-mode`; retain evidence, root-cause analysis, proportionate verification, and final review in every mode.

Debug Electron failures by first locating the failing boundary: main process, preload bridge, renderer UI, IPC contract, session/window setup, storage/API layer, packaged artifact, updater, OS integration, or performance/memory behavior.

## Process

1. State expected behavior, actual behavior, impact, platform, architecture, app version, channel, packaged/dev mode, Electron version, and the smallest reproducible symptom.
2. Inspect repo-pinned Electron and tooling versions for existing repos. For new-project advice or upgrade-sensitive fixes, use latest stable only after checking official docs through `itsol-current-tech-context`.
3. Gather evidence before changing code: main logs, renderer console, preload exposure, IPC channel/payload shape, network/session state, storage paths, updater logs, crash dumps, test output, and packaged-app behavior.
4. Reproduce in the mode that fails. If production fails, do not trust dev server behavior alone; package or run a packaged-like build with isolated `userData`.
5. Fix one boundary at a time and add a regression test when repo policy supports it. For missing test infrastructure, document replacement verification and run the narrowest reliable smoke test.
6. Use `itsol-bug-debugging` for user-facing defects and follow its Technical Fix Plan gate when required by the resolved workflow mode.

## Coordination

Use with `itsol-current-tech-context`, `itsol-bug-debugging`, `security-frontend-browser-review`, `security-files-integrations-review`, `infra-observability`, `ui-performance-stability`, and the frontend framework debugging skill used by the renderer.

## Reference Routing

- Repro setup, evidence matrix, dev-vs-packaged isolation, and first triage questions: read [01-evidence-and-triage.md](./references/01-evidence-and-triage.md).
- Main/preload/renderer boundary bugs, IPC validation failures, event leaks, and session/window problems: read [02-process-ipc-window-debugging.md](./references/02-process-ipc-window-debugging.md).
- Packaged-only bugs, ASAR/native-module/preload-path issues, code signing, notarization, and auto-update symptoms: read [03-packaged-and-update-debugging.md](./references/03-packaged-and-update-debugging.md).
- Logs, crash reports, net logs, diagnostic bundles, redaction, and support evidence: read [04-logs-crashes-diagnostics.md](./references/04-logs-crashes-diagnostics.md).
- Slow startup, high CPU, memory leaks, blocked main process, GPU/rendering issues, and large IPC payloads: read [05-performance-memory-debugging.md](./references/05-performance-memory-debugging.md).

## Version Policy

- Existing repo: debug against pinned `electron`, builder, Forge, updater, frontend framework, and test runner versions.
- New or upgrade-sensitive advice: use latest stable only after checking official docs through `itsol-current-tech-context`.
- Symptoms tied to Electron defaults, security warnings, packaging, auto-update, or test automation require current official docs before recommending version-specific fixes.

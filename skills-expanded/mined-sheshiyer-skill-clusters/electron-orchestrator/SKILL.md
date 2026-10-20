---
name: electron-orchestrator
description: "Route an Electron desktop-app task to the right spoke — the main/renderer process model & IPC, the security checklist (context isolation, sandbox, CSP), packaging/signing/notarization, auto-update, or native modules. USE WHEN building, securing, or shipping an Electron app but the specific concern isn't named. For a smaller/Rust alternative, weigh the tauri cluster."
cluster: electron
version: 1.0.0
origin: "skill-clusters (original)"
---

# Electron Orchestrator

Entry skill for **Electron** desktop apps (Chromium + Node.js). It places a task on the
process × concern map and routes. The defining model — the **main/renderer split** and the
**context-isolation security boundary** — lives in `electron-core`; read it before wiring IPC
or exposing anything to the renderer.

## Cluster map (routing targets)

- `electron-core` — process model (main vs renderer vs preload), the security checklist, app lifecycle, and the Electron-vs-Tauri decision.
- `electron-main-renderer-ipc` — the IPC contract: `contextBridge` in a preload, `ipcMain.handle`/`ipcRenderer.invoke`, typed channels, no remote module.
- `electron-security` — the hardening checklist: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, CSP, validate IPC inputs, restrict navigation/`window.open`.
- `electron-builder-packaging` — build & distribute: electron-builder/Forge, per-OS installers, code signing (Authenticode / Apple Developer ID), notarization.
- `electron-auto-update` — `autoUpdater` / `electron-updater`, update feeds, signing for updates, staged rollouts.

## Routing Rules by Intent

- **"How do main and renderer talk?"** → `electron-main-renderer-ipc` (+ `electron-core` for the trust boundary).
- **"Is my app secure / harden it"** → `electron-security`.
- **"Build installers / sign / notarize"** → `electron-builder-packaging`.
- **"Ship updates to installed apps"** → `electron-auto-update`.
- **"Use a native Node addon"** → `electron-core` (ABI/`electron-rebuild` notes) → packaging.
- **"Should I even use Electron?"** → `electron-core` (Electron vs Tauri tradeoff); for the Rust/web alternative see the **tauri** cluster.

## Standard Operating Flow

1. Locate the task: process model / IPC, security, packaging, or updates.
2. If it crosses the main↔renderer boundary, pull the trust model from `electron-core` first — the renderer is **untrusted**.
3. Delegate; for "ship it", sequence package → sign → notarize → wire auto-update.
4. Return: chosen spoke(s), the security implications, target OS(es), and the next action.

## Guardrails

See `electron-core`. In short: **the renderer is untrusted** — keep `contextIsolation` on,
`nodeIntegration` off, `sandbox` on; expose only a minimal, typed `contextBridge` API (never the
whole `ipcRenderer` or Node); validate every IPC argument in the main process; set a strict CSP;
and always sign + notarize before distributing or auto-updating.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).

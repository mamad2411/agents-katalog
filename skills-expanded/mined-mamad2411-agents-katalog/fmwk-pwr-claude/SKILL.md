# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

fmwk-pwr is a power management tool for the Framework Desktop (AMD Strix Halo APU). It uses a client/server architecture: a root-privileged server daemon communicates via Unix socket (NDJSON) with an Electron GUI and GNOME Shell extension.

## Commands

```sh
# Install dependencies
bun install

# Run server (requires root for SMU/sysfs access)
sudo -E bun run --cwd packages/server start

# Run tests
bun test --cwd packages/server
bun test --cwd packages/shared

# Run a single test file
bun test --cwd packages/server test/hardware/detect.test.ts

# Type check
bun run --cwd packages/server typecheck
bun run --cwd packages/shared typecheck
bun run --cwd packages/gui typecheck

# Build & run GUI (requires server running)
bun run --cwd packages/gui build
bun run --cwd packages/gui dev

# GNOME Extension (separate from Bun workspaces — uses tsc)
cd packages/gnome-extension && npx tsc && cp src/metadata.json src/stylesheet.css dist/
# Install to local GNOME Shell
bun run --cwd packages/gnome-extension install-ext
```

## Architecture

**Bun monorepo** with three workspaces (+ standalone GNOME extension):

- **`@fmwk-pwr/shared`** (`packages/shared/`) — Pure TypeScript types and IPC protocol definitions. No runtime code. Exports `Profile`, `HardwareInfo`, `ServerConfig`, and all IPC types (method names, params/results, error codes).

- **`@fmwk-pwr/server`** (`packages/server/`) — Server daemon. Entry point: `src/main.ts`. Key modules:
  - `config/` — Loads `ServerConfig` from `/etc/fmwk-pwr/config.json` (prod) or `./config/config.json` (dev)
  - `profiles/` — Profile CRUD, persistence to disk as JSON, validation, and application
  - `socket/` — Unix socket server (`Bun.listen`) with NDJSON framing + message routing to handlers
  - `hardware/` — Strategy pattern for hardware abstraction

- **`@fmwk-pwr/gui`** (`packages/gui/`) — Electron GUI. Entry point: `src/main/main.ts`. Key modules:
  - `src/main/socket-client.ts` — NDJSON Unix socket client with auto-reconnect
  - `src/main/ipc-handlers.ts` — Bridges socket client to renderer via Electron IPC
  - `src/main/preload.ts` — contextBridge API exposing `window.fmwkPwr`
  - `src/renderer/App.tsx` — Main React component (profile editor + live monitor)
  - `src/renderer/components/` — ProfileSelector, PowerControls, GpuControls, SystemProfile, SensorReadout, AutoMatch
  - `src/renderer/hooks/useServer.ts` — React hooks for server communication (useProfiles, useStatus, useConfig, useConnection)
  - Build: `bun build` for main/preload/renderer + Tailwind CSS CLI

- **`@fmwk-pwr/gnome-extension`** (`packages/gnome-extension/`) — GNOME Shell top bar extension (standalone, not a Bun workspace). Compiled with `tsc` to ESM JavaScript for GJS runtime. Key modules:
  - `src/client.ts` — GLib/Gio Unix socket client with NDJSON framing and auto-reconnect
  - `src/indicator.ts` — PanelMenu.Button with dropdown showing status readings and profile switcher
  - `src/extension.ts` — Main extension class (enable/disable lifecycle, polling timer)
  - `src/@types/ambient.d.ts` — Ambient type declarations for GJS (`gi://`, `resource:///` modules)

### Hardware Strategy Pattern

All hardware interaction goes through `HardwareStrategy` (defined in `hardware/strategy.ts`). On startup, `hardware/detect.ts` reads `/proc/cpuinfo` and instantiates the matching strategy.

Only implementation: **`StrixHaloStrategy`** (`hardware/strategies/strix-halo/`), split into:
- `ryzenadj.ts` — `bun:ffi` bindings to `/usr/lib/fmwk-pwr/libryzenadj.so` for SMU power limits (stapm, slow, fast)
- `hwmon.ts` — Reads temperatures and power from sysfs/HWMON (k10temp, amdgpu)
- `gpu.ts` — GPU clock and performance level control via amdgpu sysfs

### IPC Protocol

10 methods: `profile.list`, `profile.get`, `profile.create`, `profile.update`, `profile.delete`, `profile.apply`, `status.get`, `config.get`, `config.update`. Typed dispatch via `MethodMap` interface in `shared/src/ipc/method-map.ts`.

## Key Conventions

- **Runtime**: Bun + TypeScript (strict) for everything. No Node.js.
- **All power values in mW** — HardwareInfo, Profile limits, everywhere.
- **GPU clock implies manual perf level** — Setting `clockMhz` means "manual"; `perfLevel` field is `"auto" | "high" | null` (no "manual" value).
- **Profiles must always have an active default** — `defaultProfile` in config is required, non-null. No fallback profile concept.
- **libryzenadj.so at fixed path** — `/usr/lib/fmwk-pwr/libryzenadj.so`. Not configurable.
- **Sensors from sysfs/HWMON, not libryzenadj** — libryzenadj is only for setting/getting SMU limits.
- **Dev scripts via `bun run` in package.json** — No wrapper shell scripts.

## Development Status

Server core, Electron GUI, and GNOME Shell extension are complete. Next phases: Process Watcher (auto-switching), systemd service, Polish & Packaging.

## Plan Documents

Design docs in `plan/` (00-overview through 10-risks-and-notes) cover architecture, data model, server design, GUI plan, and technology decisions.

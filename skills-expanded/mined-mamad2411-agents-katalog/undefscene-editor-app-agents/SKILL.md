# Undefscene Editor — Agent Notes

## Project
Electron + React + TypeScript + Vite visual node-based cutscene editor for Undefinedtale (GML RPG).

## Tech Stack
- **Build:** electron-vite, electron-builder
- **Package Manager:** pnpm (v12+)
- **Framework:** React 19, TypeScript 5.9 (strict)
- **Testing:** vitest
- **Linting:** eslint, prettier

## Commands
```bash
pnpm dev          # Dev server (electron-vite dev)
pnpm build        # Typecheck + production build
pnpm typecheck    # tsc --noEmit for node + web configs
pnpm test:run     # Run vitest once
pnpm build:linux  # Build AppImage for Linux
pnpm build:win    # Build NSIS + portable for Windows
```

## Linux-Specific Notes

### Sandbox / GPU
The project may live on an NTFS/exFAT partition (no SUID support). The Chromium sandbox
(`chrome-sandbox` SUID helper) cannot work there. Two mitigations are in place:

1. **`run_dev.sh`** sets `ELECTRON_DISABLE_SANDBOX=1` and unsets `ELECTRON_RUN_AS_NODE` on Linux.
2. **`src/main/index.ts`** appends `--no-zygote` and `--disable-gpu-sandbox` switches on Linux.

Additionally, `~/.config/undefscene-editor/preferences.json` should contain:
```json
{"disableHardwareAcceleration": true}
```
This prevents GPU process crashes on Wayland + NVIDIA hybrid setups.

### pnpm Build Scripts
`pnpm-workspace.yaml` uses the `allowBuilds` format (pnpm v12+) to approve build scripts
for `electron`, `electron-winstaller`, and `esbuild`. If postinstall scripts don't run
after changing the workspace file, use `pnpm rebuild <package>` to re-trigger them.

### Electron Binary
If the Electron binary is missing from `node_modules/.pnpm/electron@*/node_modules/electron/dist/`,
run `pnpm rebuild electron`. The zip is cached in `~/.cache/electron/`.

## Architecture
- **Main process** (`src/main/`): app lifecycle, IPC handlers, window management, auto-updater
- **Preload** (`src/preload/`): context bridge between main and renderer
- **Renderer** (`src/renderer/`): React UI, node graph editor (@xyflow/react)
- **Shared types** (`src/shared/types/`): cross-context TypeScript interfaces

## Rules
See `.devin/rules/react-engineer.md` for strict architectural constraints.

---
name: bundled-uv-python-toolchain
description: Bundle the 'uv' binary (platform-specific) with your Electron/CLI app, wire CRAFT_UV + CRAFT_SCRIPTS env, and let uv auto-download a pinned Python on first tool-invoke — zero-install Python tools for users who never had Python.
category: build
version: 1.0.0
version_origin: extracted
tags: [python, uv, bundling, cross-platform, electron]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: apps/electron/src/main/index.ts
imported_at: 2026-04-18T00:00:00Z
---

# Bundled uv + auto-Python for desktop apps

## When to use
- Your desktop app needs to invoke Python tools (markitdown, pdf-tool, xlsx-tool) without requiring users to install Python.
- You want fast startup (~5s on first use, cached forever).
- Need cross-platform: darwin-arm64 / darwin-x64 / win32-x64 / linux-x64.

## How it works
1. Download the platform-specific `uv` binary during build (`scripts/build/common.ts#downloadUv`) and place it at `resources/bin/<platform>-<arch>/uv{,.exe}`.
2. Include platform-specific uv in electron-builder via `extraResources` (so only the RIGHT arch ships per artifact, not all four).
3. At app startup in Electron main:
   - Resolve `resourcesBase` = `process.resourcesPath/app` (packaged) or `__dirname/..` (dev).
   - Set `process.env.CRAFT_UV = <resourcesBase>/resources/bin/<platform>-<arch>/uv`.
   - Set `process.env.CRAFT_SCRIPTS = <resourcesBase>/resources/scripts` (Python source directory).
   - Prepend `resources/bin` (wrappers) + the uv dir to `PATH`.
4. Ship wrapper scripts (`resources/bin/pdf-tool`, `...cmd` for Windows) that do `exec "$CRAFT_UV" run --script "$CRAFT_SCRIPTS/pdf_tool.py" "$@"`. The first invoke triggers uv to download + pin a Python 3.12 (~20MB) into its cache; subsequent calls reuse it.
5. Fallback: if the bundled binary is missing (dev setup), log a warning and try `uv` on the user's PATH.

## Example
```ts
// Electron main
const platformKey = `${process.platform}-${process.arch}`;
const resourcesBase = app.isPackaged
  ? join(process.resourcesPath, 'app')
  : join(__dirname, '..');
const uvBinary = join(resourcesBase, 'resources', 'bin', platformKey,
  process.platform === 'win32' ? 'uv.exe' : 'uv');
process.env.CRAFT_UV = existsSync(uvBinary) ? uvBinary : 'uv';
process.env.CRAFT_SCRIPTS = join(resourcesBase, 'resources', 'scripts');
process.env.PATH = `${binDir}${delimiter}${dirname(uvBinary)}${delimiter}${process.env.PATH}`;
```

```sh
# resources/bin/pdf-tool (shipped in the app bundle)
#!/bin/sh
exec "$CRAFT_UV" run --script "$CRAFT_SCRIPTS/pdf_tool.py" "$@"
```

## Gotchas
- uv caches to `~/.cache/uv/` by default - document this for anti-virus / corporate policy.
- Test that uv can write to its cache in sandboxed Electron configurations (macOS hardened runtime is fine, some Windows enterprise setups aren't).
- PATH-prepend is global process-wide - if you spawn shells, the wrappers will be visible to them. Usually what you want.
- Windows ships `uv.exe` (not `uv`); your wrapper scripts must come in `.cmd` variants too.
- Use `--script` with embedded PEP 723 dependencies in each `.py` file so each tool is self-contained; no shared venv state.

---
name: pyinstaller-shim-fake-module
description: Register a tiny in-process shim for a heavy transitive dependency so a frozen build avoids an entire unwanted toolchain.
category: build-tooling
version: 1.0.0
version_origin: extracted
tags: [pyinstaller, dependencies, shim, import-system, ml]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# PyInstaller shim fake-module

## When to use
A model library imports `pkg.sub.module.SomeClass` but the real `pkg` distribution drags in a giant side-chain (onnx, tensorboard, protobuf, matplotlib, etc.) that you don't want shipped or maintained. You only need a handful of symbols.

## Steps
1. Copy the source of the minimum class/function you actually use from the upstream repo, preserving its license header. Strip decorators that rely on `inspect.getsource()` (e.g. `@torch.jit.script`) because `.pyc`-only frozen builds can't source-read themselves.
2. Create `shim_<pkg>.py` under your own package tree. Implement the types you need using stdlib / torch primitives only.
3. Write an `install_<pkg>_shim()` function that:
   - Tries `import <pkg>` first. If it succeeds, return immediately so the real package always wins when present.
   - Otherwise builds the fake module tree with `types.ModuleType`, sets `__path__ = []` and `__package__` for intermediate packages so Python treats them as packages not modules.
   - Attaches the real classes/functions as attributes on the leaf module.
   - Registers every level in `sys.modules` (e.g. `sys.modules["pkg"] = pkg_module`, `sys.modules["pkg.sub"] = sub_module`, `sys.modules["pkg.sub.leaf"] = leaf_module`) so subsequent `import pkg.sub.leaf` calls resolve from the shim.
4. Call `install_<pkg>_shim()` early — before the first import of any library that might touch `pkg`. In practice this means either at the top of the entry-point module or in a PyInstaller runtime hook.
5. Add `--hidden-import <your.shim_module>` in the PyInstaller argv so the shim is actually bundled.

## Counter / Caveats
- Shims are a legal minefield — only ship code whose license lets you vendor it, and keep the attribution intact.
- If upstream adds new symbols that consumers start importing, the shim silently breaks imports the next time you upgrade. Pin the consumer version or add a test that imports every symbol you rely on.
- Do not use this to skip monkey-patching issues (`map_location`, float dtype, etc.) — those should be fixed in the real dependency, not papered over in a shim.
- Document the trade-off next to the shim (package size saved, symbols replicated, expected upstream churn) so future maintainers know why the shim exists.

Source references: `backend/utils/dac_shim.py`, `backend/build_binary.py` (the `--hidden-import backend.utils.dac_shim` entry).

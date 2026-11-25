---
name: pyinstaller-ml-hidden-imports-playbook
description: Repeatable recipe of --collect-all / --copy-metadata / --hidden-import flags for freezing ML stacks that break PyInstaller's default static analysis.
category: build-tooling
version: 1.0.0
version_origin: extracted
tags: [pyinstaller, ml, freezing, hidden-imports, metadata]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# PyInstaller ML hidden-imports playbook

## When to use
You are freezing a FastAPI/uvicorn + torch + transformers + huggingface-hub app (or similar) into a single binary or onedir and generation-time errors start with "module not found", "No package metadata found", "could not get source code", or "FileNotFoundError: /usr/share/..." at runtime in the frozen build.

## Steps
1. Seed the argument list with your top-level backend modules as `--hidden-import backend`, `--hidden-import backend.main`, etc. PyInstaller's static analyzer misses string-based lazy imports; treat every `importlib.import_module(...)` site as a hidden import.
2. For each ML package that uses `lazy_loader`, reads `.pyi` stubs, reads bundled data files, or ships native shared libs, use `--collect-all <pkg>` rather than `--hidden-import`. Typical offenders in TTS/STT stacks: `librosa`, `lazy_loader`, `misaki`, `language_tags`, `espeakng_loader`, `piper_phonemize`, `perth`, `inflect`, `en_core_web_sm`, `mlx`, `mlx_audio`, `zipvoice`, `linacodec`.
3. For packages whose code calls `importlib.metadata.version(...)` or `pkg_resources.get_distribution(...)`, add `--copy-metadata <dist-name>`. Required in practice for: `requests`, `transformers`, `huggingface-hub`, `tokenizers`, `safetensors`, `tqdm`, and any spaCy model distribution.
4. For packages that call `inspect.getsource()` at import-time or runtime (typeguard `@typechecked`, `torch.jit.script`, some HF Transformers modeling files), add `--collect-all <pkg>`. `--hidden-import` alone only bundles `.pyc`, which fails `getsource`.
5. For Python namespace packages whose submodules are picked up dynamically, use `--collect-submodules <pkg>` (e.g. `jaraco`, `tada`, `mlx`, `mlx_audio`).
6. Add a runtime hook for any monkey-patch that must run after `FrozenImporter` is registered but before the app starts (e.g. `torch.from_numpy` shim for numpy 2.x ABI). PyInstaller invokes runtime hooks after import wiring so both frozen torch and frozen numpy are importable inside the hook.
7. Export a runnable build script (don't hand-edit the `.spec` file). Keep the flag list as a single Python list so diffs stay readable across patch releases.
8. Document every non-obvious flag with a one-line comment explaining which upstream behavior forced it — comments survive refactors and save the next person hours.

## Counter / Caveats
- `--collect-all` bundles binaries as well as data, so on CPU-only builds add `--exclude-module` for the NVIDIA namespace packages (`nvidia`, `nvidia.cublas`, …) or the build will silently balloon by 2-3 GB when a CUDA-torch venv is in scope.
- `--collect-all` is the right answer whenever data files live under the package tree; don't reach for custom `datas=[(...)]` entries unless you need to place files outside the package.
- Test with a **clean HuggingFace cache** so you catch download-path bugs that hide behind a warm cache.
- Runtime hooks must tolerate partial failures; wrap their body in a broad `try/except` so a startup edge case can't brick the frozen binary.

Source references: `backend/build_binary.py`, `backend/voicebox-server.spec`, `backend/pyi_rth_numpy_compat.py`, `.agents/skills/add-tts-engine/SKILL.md`.

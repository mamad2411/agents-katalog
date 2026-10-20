---
name: new-ml-backend-dependency-audit
description: Run a Phase-0 dependency audit on a candidate ML library before writing any integration code, so PyInstaller and runtime surprises are caught early.
category: agents
version: 1.0.0
version_origin: extracted
tags: [ml-ops, dependencies, pyinstaller, audit, integration]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# New ML backend dependency audit

## When to use
You are about to add a new ML model/library (TTS, STT, image, anything torch-based) to an app that ships as a PyInstaller binary. Skipping the audit reliably produces 3+ patch releases chasing frozen-build breakage (typechecked decorators, missing data files, hardcoded system paths).

## Steps
1. Clone the model library into a throwaway directory (`/tmp/engine-research`). Do NOT install it into the main venv yet.
2. Grep the clone (and its transitive dependencies) for every pattern that breaks frozen builds:
   - `@typechecked` / `inspect.getsource` / `torch.jit.script` — forces `--collect-all <pkg>` because `.pyc` fails source reads.
   - `importlib.metadata.version(` / `pkg_resources.get_distribution(` — forces `--copy-metadata <dist-name>`.
   - `lazy_loader.attach` / `.pyi` stubs — forces `--collect-all` for the stubs.
   - Hardcoded `/usr/share/...` / `data_path = Path(__file__).parent / "data"` — forces env var fallback in the frozen entrypoint.
   - `torch.load(...)` without `map_location=` — forces a monkey-patch when CPU build loads CUDA-tensor checkpoints.
   - `token=True` in HF calls — forces `snapshot_download(token=None)` + `from_local()` so users without an HF login can run the app.
3. Produce a written audit covering:
   a. PyPI vs git-only dependencies.
   b. PyInstaller flags needed (`--collect-all`, `--copy-metadata`, `--hidden-import`).
   c. Runtime data files (`.pth.tar`, `.yaml`, `.json`, G2P dictionaries) that must be bundled.
   d. Native libraries with hardcoded paths (espeak-ng, piper_phonemize, misaki) and the env vars needed to redirect them.
   e. Monkey-patches (`torch.load`, float64 casts, MPS workarounds).
   f. Sample rate expected by the model and any sample-rate-conversion needs.
   g. Model download method (`from_pretrained` vs `snapshot_download + from_local`) and whether it respects `HF_HUB_OFFLINE`.
4. Build and test model load + a single inference in the throwaway venv on CPU. Only then start the real integration.
5. Test again with a **clean HuggingFace cache** so you catch download-path bugs that a warm cache hides.

## Counter / Caveats
- Do NOT skip this audit "because the library is small" — the smallest lib can pull in 400 MB of descript-audiotools transitives.
- Upstream pretrained weights can move between HF repos; pin the exact `revision=` in the download call to make cache behavior reproducible.
- Nightly PyTorch is not shippable for releases (non-deterministic, regressions between runs). If a library requires nightly, prefer `TORCH_CUDA_ARCH_LIST=...+PTX` or wait for a stable support window.
- Keep the audit doc in the repo (e.g. `docs/engine-audits/<engine>.md`) — it becomes the next maintainer's starting point and makes version upgrades routine.

Source references: `.agents/skills/add-tts-engine/SKILL.md` (Phase 0 / the lessons table from v0.2.3).

---
name: pyinstaller-cuda-onedir-split-archive
description: Ship a PyInstaller --onedir CUDA build as two archives so the ~2 GB NVIDIA runtime layer can be cached across app updates.
category: build-tooling
version: 1.0.0
version_origin: extracted
tags: [pyinstaller, cuda, packaging, desktop-ml, release-artifacts]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# PyInstaller CUDA onedir split-archive

## When to use
Shipping a desktop app that bundles CUDA-enabled PyTorch via PyInstaller. The full onedir build balloons to 2-3 GB because of `nvidia-*` DLLs; re-downloading that on every app update is painful. Split-archive lets the app redownload only the small server-core layer while the large CUDA runtime stays cached until the toolkit actually changes.

## Steps
1. Build the CUDA variant with `--onedir` (not `--onefile`) so the output is a directory tree that can be partitioned after the fact. Keep the CPU build on `--onefile` for simplicity.
2. After `PyInstaller.__main__.run(...)`, walk `rglob("*")` over the dist directory and classify each file as "NVIDIA runtime" or "server core". Match NVIDIA files by: anything inside an `nvidia/` namespace, plus any `.dll`/`.so` whose filename starts with a known prefix (`cublas`, `cublaslt`, `cudart`, `cudnn`, `cufft`, `cufftw`, `curand`, `cusolver`, `cusolvermg`, `cusparse`, `nvjitlink`, `nvrtc`, `nccl`, `caffe2_nvrtc`).
3. Keep a small allowlist of names that look NVIDIA but are actually Python stubs (e.g. `torch/cuda/nccl.py`, cutlass mock imports) so they stay in the core archive.
4. Emit two `.tar.gz` archives with paths **relative to the onedir root** (no parent prefix). Name them `<app>-cuda.tar.gz` (server core) and `cuda-libs-<toolkit>-v<N>.tar.gz` (NVIDIA layer). Version the CUDA layer independently from the app version.
5. Compute SHA-256 for each archive and write sibling `.sha256` files. Write a `cuda-libs.json` manifest `{"version": "...", "torch_compat": "...", "archive": "...", "sha256": "..."}` so the client knows what's already installed.
6. Client-side: download the server-core archive on every app version bump, but only redownload the CUDA layer when `installed_manifest.version != expected_version`. Stream-download with checksum verification before `tarfile.extractall(..., filter="data")`. Extract both archives into the same target directory so the onedir layout is reconstructed.

## Counter / Caveats
- Refuse to create an empty CUDA libs archive — if classification finds zero NVIDIA files the build is misconfigured and should hard-fail rather than ship a broken split.
- The DLL prefix list is torch-layout-dependent. In torch 2.10+ the NVIDIA DLLs moved from `nvidia/` subdirs to `_internal/torch/lib/`; the prefix check catches both layouts.
- When launching the extracted binary, set `current_dir` to the onedir root so PyInstaller can resolve its support files.
- Always use the `filter="data"` argument to `extractall` (Python 3.12+) for path-traversal protection on untrusted archives.

Source references: `scripts/package_cuda.py`, `backend/build_binary.py`, `backend/services/cuda.py`.

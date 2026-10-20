---
name: cmake-cuda-extension-with-git-submodule-vendoring
description: Build a PyTorch CUDA extension with CMake, vendoring CUTLASS and fmt as git submodules, plus a pre-built-wheel fast path for CI via GitHub releases.
category: build-system
version: 1.0.0
version_origin: extracted
tags: [cmake, pytorch-extension, git-submodule, cuda-build, wheel, ci]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/deepseek-ai/DeepGEMM.git
source_ref: main
source_commit: 7f2a703ed51ac1f7af07f5e1453b2d3267d37d50
source_project: DeepGEMM
source_paths:
  - setup.py
  - CMakeLists.txt
  - install.sh
imported_at: 2026-04-18T13:12:58Z
---

# CMake CUDA Extension With Git-Submodule Vendoring

## What / Why
CUTLASS / CUTE / fmt are tightly coupled to kernel code — version skew = silent miscompiles. Vendoring via git submodule pins exact commits and avoids every user becoming a CUTLASS debugger. A CMake build keeps the CUDA compilation flags centralized. For CI, a `DG_FORCE_BUILD` env switch lets users download a pre-built wheel from GitHub releases when a matching Python × PyTorch × CUDA tag exists, skipping the 15-minute local compile.

## Procedure
1. **Add submodules.**
   ```
   git submodule add https://github.com/nvidia/cutlass.git third-party/cutlass
   git submodule add https://github.com/fmtlib/fmt.git     third-party/fmt
   ```
2. **Pin exact commits** via `git submodule update --init --recursive` in `install.sh`. Lock CUTLASS to a known-good tag.
3. **`setup.py` branching.**
   - If `DG_FORCE_BUILD` unset AND matching wheel exists at the releases URL: download, extract, install.
   - Else: call into CMake via `CUDAExtension` / `torch.utils.cpp_extension.BuildExtension`.
4. **`CMakeLists.txt` essentials.**
   - `include_dirs += third-party/cutlass/include`, `third-party/cutlass/include/cute`, `third-party/fmt/include`, `deep_gemm/include`.
   - `libraries += cudart nvrtc`.
   - Flags: `-std=c++20 -O3 -fPIC`, PyTorch C++11 ABI alignment flag, CUDA arch list from `torch.utils.cpp_extension.CUDA_ARCHITECTURES`.
5. **`develop.sh`** symlinks the include tree for in-place development; `install.sh` is the end-user wrapper.

## Key design points
- Pre-built wheel path is a **cache**, not a different code path. The same sources build the wheel and a local build — just shorter.
- Header-only vendoring (CUTLASS, fmt) avoids static-lib ABI issues. If you need a compiled third-party lib, vendor source and build under your CMake, don't link externally.
- Keep CUDA arch selection dynamic (from PyTorch), not hardcoded — users run SM80-SM100.

## References
- `setup.py` — wheel fast path + build invocation.
- `CMakeLists.txt` — compile flags and include wiring.
- `install.sh` / `develop.sh` — user-facing entry points.

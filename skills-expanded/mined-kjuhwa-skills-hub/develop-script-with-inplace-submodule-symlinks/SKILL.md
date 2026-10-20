---
name: develop-script-with-inplace-submodule-symlinks
description: Ship a `develop.sh` that symlinks vendored submodule includes (CUTLASS, fmt) into the package's include tree, then runs `python setup.py build` and symlinks the resulting `.so` back into the source package — editable-install for a CUDA extension.
category: build-system
version: 1.0.0
version_origin: extracted
tags: [develop-mode, setup-py, cuda-extension, symlinks, editable-install, submodules]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/deepseek-ai/DeepGEMM.git
source_ref: main
source_commit: 7f2a703ed51ac1f7af07f5e1453b2d3267d37d50
source_project: DeepGEMM
source_paths:
  - develop.sh
  - install.sh
  - build.sh
  - setup.py
imported_at: 2026-04-18T13:30:00Z
---

# In-Place Dev Mode For A CUDA Extension With Vendored Submodules

## When to use
Your Python package ships a native CUDA extension (pybind11 + `CUDAExtension`) and vendors large C++ header-only dependencies (CUTLASS, fmt) as git submodules. `pip install -e .` doesn't give you what you want because:
- The submodule headers need to live *inside* the installed `package/include/` tree (for runtime JIT to find them), but your source tree has them at `third-party/cutlass/include/cutlass/`.
- You want to rebuild iteratively without reinstalling the wheel.

Solution: a tiny `develop.sh` that creates header symlinks and builds to the source tree.

## Steps
1. **Capture the user's original CWD** so the script is callable from anywhere:
   ```bash
   original_dir=$(pwd)
   script_dir=$(realpath "$(dirname "$0")")
   cd "$script_dir"
   ```
2. **Symlink submodule headers into the package's `include/` dir.** The symlink is idempotent (`ln -sf`) so you can re-run freely:
   ```bash
   ln -sf $script_dir/third-party/cutlass/include/cutlass  deep_gemm/include
   ln -sf $script_dir/third-party/cutlass/include/cute     deep_gemm/include
   ```
   Result: `deep_gemm/include/cutlass` points to `third-party/cutlass/include/cutlass`. At runtime, your JIT wrapper passes `-I<package>/include` and NVCC resolves the chain transparently.
3. **Clean previous build artifacts** to avoid `.so` staleness:
   ```bash
   rm -rf build dist *.egg-info
   ```
4. **Build the C extension in place:** `python setup.py build`. This puts `.so` under `build/lib.linux-x86_64-*-cpython*/`.
5. **Symlink the built `.so` back into the source package** so `import <package>` from the source tree finds it:
   ```bash
   so_file=$(find build -name "*.so" -type f | head -n 1)
   ln -sf "../$so_file" deep_gemm/
   ```
6. **Restore CWD:** `cd "$original_dir"`.
7. **Provide `install.sh` as the parallel "real" installer** — same prelude, but `bdist_wheel` + `pip install --force-reinstall dist/*.whl`. The wheel-path builds its own `include/` copy via `CustomBuildPy.prepare_includes()` (a `shutil.copytree` rather than a symlink, because wheels can't contain symlinks).

## Evidence (from DeepGEMM)
- `develop.sh:6-8`: submodule header symlinks.
- `develop.sh:13`: `python setup.py build` — no `--inplace` flag; artifacts end up under `build/`.
- `develop.sh:16-22`: find `.so` and symlink it into `deep_gemm/`.
- `install.sh:9-10`: wheel path (`bdist_wheel` + `pip install --force-reinstall`).
- `setup.py:114-166`: `CustomBuildPy.prepare_includes()` does `shutil.copytree` for the wheel so symlinks don't leak into the shipped package.

## Counter / Caveats
- **Symlinks on Windows need `mklink /D`** or developer-mode enabled. This script is Linux-only as written; gating by `$OSTYPE` is a mild extension.
- **`pip install -e .` alone is not enough** because `CUDAExtension` doesn't set up the include-tree layout the JIT needs. Hence the custom shell script — there is no stock `setup.py develop` equivalent.
- **If a submodule header moves across versions, the symlink dangles silently.** Run `develop.sh` after every `git submodule update` to refresh.
- **CI should not use this path** — CI builds a wheel via `install.sh` so the `include/` tree is a real copy.

---
name: env-driven-debug-flag-matrix-for-jit
description: Use a consistently-prefixed family of environment variables (DG_JIT_DEBUG, DG_JIT_DUMP_PTX, DG_JIT_PTXAS_CHECK, ...) to toggle JIT compilation/loading/profiling diagnostics without rebuilding or changing config files.
category: build-system
version: 1.0.0
version_origin: extracted
tags: [environment-variables, debug-flags, jit, observability, cuda, diagnostics]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/deepseek-ai/DeepGEMM.git
source_ref: main
source_commit: 7f2a703ed51ac1f7af07f5e1453b2d3267d37d50
source_project: DeepGEMM
source_paths:
  - csrc/jit/compiler.hpp
  - csrc/jit/kernel_runtime.hpp
  - csrc/utils/system.hpp
  - README.md
imported_at: 2026-04-18T13:30:00Z
---

# Env-Driven Debug Flag Matrix For JIT Compilation

## When to use
Your JIT compiler loads, builds, and launches kernels at runtime. Each step has diagnostic output that is useful for debugging but expensive in the hot path:
- Compile command inspection.
- PTX / SASS dump.
- PTXAS verbose / register spill assertion.
- Kernel load time print.
- "No local memory used" invariant check.

You don't want these as recompile-time flags (feedback loop too slow) nor as function-level configuration (they're cross-cutting). Environment variables are the right interface.

## Steps
1. **Namespace every flag with one prefix.** DeepGEMM uses `DG_JIT_*` for JIT-internal, `DG_*` for higher-level library flags. Grep becomes trivial: `grep -rn DG_JIT_ .`.
2. **Wrap `getenv`** so the access site is a one-liner with a typed default:
   ```cpp
   template <typename T>
   T get_env(const std::string& name, const T& default_value = T{}) {
       const char* c_str = std::getenv(name.c_str());
       if (c_str == nullptr) return default_value;
       if constexpr (std::is_same_v<T, std::string>) return std::string(c_str);
       if constexpr (std::is_same_v<T, int>) { int v; std::sscanf(c_str, "%d", &v); return v; }
       DG_HOST_ASSERT(false);  // unknown type
   }
   ```
3. **Organize flags into layered tiers.** DeepGEMM has (all `0`/`1` unless noted):
   - **Compiler selection:** `DG_JIT_USE_NVRTC`, `DG_JIT_NVCC_COMPILER` (path), `DG_JIT_CPP_STANDARD` (int, default 20).
   - **Compiler output:** `DG_JIT_PRINT_COMPILER_COMMAND`, `DG_JIT_PTXAS_VERBOSE`, `DG_JIT_PTXAS_CHECK` (asserts no local memory usage), `DG_JIT_PRINT_LOAD_TIME`.
   - **Dumping:** `DG_JIT_DUMP_ASM` (both PTX + SASS), `DG_JIT_DUMP_PTX`, `DG_JIT_DUMP_SASS`, `DG_JIT_WITH_LINEINFO` (affects codegen, not just output).
   - **Cache:** `DG_JIT_CACHE_DIR`, `DG_JIT_DEBUG` (uber-debug, implies several others).
   - **Build:** `DG_SKIP_CUDA_BUILD`, `DG_FORCE_BUILD`, `DG_JIT_USE_RUNTIME_API`.
4. **Derive flag composition at init time.** The cleanest pattern:
   ```cpp
   if (get_env("DG_JIT_DEBUG", 0) or get_env("DG_JIT_PTXAS_VERBOSE", 0) or get_env("DG_JIT_PTXAS_CHECK", 0))
       flags += " --ptxas-options=--verbose,--warn-on-local-memory-usage";
   if (get_env("DG_JIT_WITH_LINEINFO", 0))
       flags += " -Xcompiler -rdynamic -lineinfo";
   ```
   `DG_JIT_DEBUG` is an OR-gate for multiple diagnostics without repeatedly typing each one.
5. **Persist user choices across re-installs** by writing selected env var values into a generated `envs.py` at build time:
   ```python
   # setup.py CustomBuildPy.generate_default_envs()
   for name in ('DG_JIT_CACHE_DIR', 'DG_JIT_PRINT_COMPILER_COMMAND', 'DG_JIT_CPP_STANDARD'):
       if name in os.environ:
           code += f"persistent_envs['{name}'] = '{os.environ[name]}'\n"
   ```
   Then at `__init__`, apply them only if not already set:
   ```python
   for k, v in persistent_envs.items():
       if k not in os.environ: os.environ[k] = v
   ```
6. **Document every flag in the README** with default value, 0/1 form, and one-line effect.

## Evidence (from DeepGEMM)
- `csrc/utils/system.hpp:16-33`: the `get_env<T>()` template with default value.
- `csrc/jit/compiler.hpp:49-62`: tier layering — cache settings, base flags, then OR-gated diagnostic flags.
- `csrc/jit/compiler.hpp:116-127`: `DG_JIT_DUMP_ASM / _PTX / _SASS` gating the dump + disassemble path.
- `csrc/jit/kernel_runtime.hpp:42-48,86-89`: `DG_JIT_PRINT_LOAD_TIME` as a cheap on-demand timing metric.
- `setup.py:140-147`: the build-time `envs.py` snapshot of persistent env vars.
- `README.md:161-186`: full user-facing documentation.

## Counter / Caveats
- **Env vars are global process state.** A library cannot scope them per caller. If you need per-call overrides, add an explicit `DeviceRuntime::set_foo()` method and have `get_env` only provide the default.
- **`DG_JIT_DEBUG` as an uber-flag is convenient but surprising.** When it silently enables PTXAS verbose and load-time printing, output volume doubles and a confused user might miss a real error message. Document the OR-gating.
- **Type-parsing via `sscanf` is fragile.** `DG_JIT_CPP_STANDARD=20abc` silently parses to 20. Stricter parsing + clear "unknown env value" error is safer for user-facing flags.

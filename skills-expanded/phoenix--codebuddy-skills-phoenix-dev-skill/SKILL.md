---
name: phoenix-dev
description: >
  Developer workflow skill for the Phoenix project (storage→xPU direct I/O middleware).
  Use when the user wants to build/install/test the phxfs kernel module, work on the
  libphoenix user library, integrate an AI application adapter
  (vLLM / lmcache), or understand/collect/report a bug. Triggers include "build phoenix",
  "insmod", "kernel module", "libphoenix", "phxloader", "vLLM adapter", "report a bug",
  "collect bug info", or any task touching module/, libphoenix/, adapters/.
---

# Phoenix developer skill

Phoenix is middleware for direct I/O from storage to xPU (GPU/NPU) via DMA, bypassing CPU
host memory. Three layers: `phxfs` kernel module, `libphoenix` user library, and `adapters/`
(pybind11-based) for AI apps. Multi-vendor support (NVIDIA/AMD/Huawei) is selected at build
time via `PHXFS_VENDOR` (default NVIDIA); only NVIDIA is implemented today. **Always start
by reading `AGENTS.md` at the repo root** for the architecture, directory map, and gotchas —
do not read the whole tree.

## Workflow 1 — Environment adaptation: build / install / test the kernel module

1. Read `doc/install.md` and `doc/troubleshooting.md`.
2. Confirm prerequisites: NVIDIA GDS + MLNX_OFED, kernel source for the running kernel,
   CUDA 12.4, liburing. Run `nvidia-smi` so the NVIDIA driver is loaded.
3. Build:
   ```shell
   mkdir -p build && cd build && cmake ../ && make -j
   ```
   Skip the module with `cmake -Dno_module=true ../`.
   Target a different vendor with `cmake -DPHXFS_VENDOR=AMD ../` (requires implementing
   `module/amd-backend.c` first — see `doc/kernel-module.md`).
4. Install: `sudo make insmod`. On "Operation not permitted", the GPU BAR is held — see
   `doc/troubleshooting.md` (free `/dev/nvidia*` users, unload `nvidia_drm`).
5. Test: run `./bin/test_regmem 0`, `./bin/test_io 0`, and `./bin/test_batch` from `build/`
   (registration lifecycle, single-request I/O, and batch I/O correctness/performance).
   Inspect `dmesg | grep phxfs` for module messages.
6. Remove when done: `sudo make rmmod`.

## Workflow 2 — Work on the user library

- `libphoenix/` is the C/C++ API (`phxfs_open/close`, `regmem/deregmem`, `read/write`, and
  the batch API `phxfs_*_batch` + async `phxfs_batch_submit_*`/`phxfs_batch_wait`), split
  into `phx_device.cpp` (device lifecycle), `phx_mem.cpp` (registration/mapping), `phx_io.cpp`
  (read/write/batch/async).
- Vendor-specific calls (CUDA, HIP, ...) live only in `libphoenix/connectors/<vendor>_connector.cpp`.
  Core files (`phx_device.cpp`, `phx_mem.cpp`, `phx_io.cpp`) call through the `devconn` function-pointer table and must stay
  vendor-agnostic — never add `#include <cuda.h>` etc. there.
- Batch/async I/O runs on a pluggable engine (`io_engine/io_engine_*.cpp`) behind a worker
  pool (`io_engine/io_pool.cpp`), chosen at load: `io_uring` → `sync` fallback. 

## Workflow 3 — Upper-layer application integration

- vLLM: see `doc/adapters.md`. The `adapters/vLLM/phxloader` package exposes `PhxLoader`
  (via pybind11) and a `phxsafetensors` vLLM `load_format`. Pattern: parse model/weights →
  register a shared GPU buffer via `libphoenix` → `phxfs_read` DMA into GPU → `deregmem`.
- New adapters (e.g. lmcache): register a GPU buffer through `libphoenix` and transfer with
  the batch API (`phxfs_*_batch`) or `phxfs_read`/`phxfs_write`; follow the vLLM adapter
  structure. Place under `adapters/<app>/`.

## Workflow 4 — Understand and report a bug

1. Reproduce and capture `dmesg | grep phxfs`, module load state, and the failing command.
2. Gather environment info: `uname -r`, `nvidia-smi`, `lsmod | grep phxfs`, and relevant `dmesg`.
3. Open an issue with `.github/ISSUE_TEMPLATE/bug_report.md`, pasting the environment info
   and clear reproduction steps.
4. (Future) A shared MCP server will aggregate these reports across users for faster triage
   — see `doc/roadmap.md`. Until then, keep reports in issues.

## Hard constraints / gotchas

- Only one driver may own the GPU PCIe BAR at a time.
- `regmem` > 32 GiB still fails (kmalloc-limited descriptor); large I/O is chunked at
  `PHXFS_IO_CHUNK` (1 GiB) for `read`/`write`.
- Only one `PHXFS_VENDOR` backend is compiled in per build; mixed-vendor machines are
  not supported. AMD/Huawei backends are not yet implemented (interfaces are ready).

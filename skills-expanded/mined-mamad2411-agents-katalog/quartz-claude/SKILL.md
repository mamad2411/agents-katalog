# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test

```sh
# Host unit tests (default — no hardware needed)
cmake -B build && cmake --build build
./build/quartz_test        # run all tests
ctest --test-dir build     # via CTest

# Cross-compile for specific targets
cmake -B build_avr    -DCMAKE_TOOLCHAIN_FILE=cmake/avr_atmega328p.cmake && cmake --build build_avr
cmake -B build_rv32   -DCMAKE_TOOLCHAIN_FILE=cmake/riscv32_clint.cmake  && cmake --build build_rv32
cmake -B build_esp32s3 -DCMAKE_TOOLCHAIN_FILE=cmake/esp32s3_qemu.cmake  && cmake --build build_esp32s3
cmake -B build_cm4    -DCMAKE_TOOLCHAIN_FILE=cmake/arm_cm4.cmake         && cmake --build build_cm4

# With Chrome trace backend
cmake -B build -DRTOS_TRACE_BACKEND=chrome && cmake --build build
```

There is no separate lint step. The test binary compiles kernel sources directly (`#include "../src/*.c"`) with port stubs, so a successful build implies the kernel compiles cleanly.

## Architecture Overview

A preemptive RTOS written in C11 with no dynamic allocation — all kernel objects are statically allocated by the caller.

**Layer split:**
- `src/` — architecture-independent kernel (`task.c`, `sem.c`, `mutex.c`, `queue.c`, `timer.c`, `list.c`)
- `include/` — public API headers; users include only `rtos.h`
- `src/port.h` — internal port contract (6 `port_` functions + 2 callbacks every port must implement)
- `port/<arch>/port.c` + `port_asm.S` — one directory per target; CMake selects based on toolchain or `-DRTOS_PORT=`

**Scheduler internals (`src/task.c`):**
- Per-priority ready queues (`g_ready[RTOS_MAX_PRIORITIES]`) plus a `g_ready_bitmap`; `__builtin_ctz` on the bitmap finds the highest-priority ready task in O(1).
- A single delay-sorted blocked list (`g_blocked`) using signed tick comparison for rollover safety.
- `g_current` is a non-`static` global so port assembly can access it directly.
- Dual-core support: when `RTOS_NUM_CORES > 1`, scheduler state is per-core (`g_ready[CORE][...]`, `g_current[CORE]`).

**Tick path:** port ISR → `rtos_tick_handler()` → unblocks tasks + fires timers → `port_request_reschedule()` → deferred context switch (PendSV on ARM, inline on AVR/RISC-V).

**Tracing:** `rtos_trace.h` defines hook macros that expand to no-ops by default. With `-DRTOS_TRACE_BACKEND=chrome`, `src/trace_chrome.c` provides a ring-buffer recorder; `tools/trace_viewer.py` / `tools/trace_to_chrome.py` convert the output to Chrome Trace Event JSON.

## Key Conventions

**Naming:**
- Public API: `rtos_` prefix, full snake_case — `rtos_task_create`, `rtos_semaphore_take`, `rtos_mutex_lock`, `rtos_queue_send`, `rtos_timer_start`, `rtos_start`
- Internal kernel symbols: lowercase with underscores
- Port-layer symbols: `port_` prefix — `port_init`, `port_init_stack`, `port_enter_critical`, `port_exit_critical`, `port_request_reschedule`, `port_start_first_task`

**Priority:** lower numeric value = higher priority (0 is highest). `RTOS_MAX_PRIORITIES - 1` is reserved for the idle task.

**Handles:** `rtos_handle_t` is `void *` pointing to the underlying struct. Passing `NULL` to `rtos_task_delete` / `rtos_task_suspend` targets the current task.

**Return codes:** `RTOS_OK` (0), `RTOS_ERR` (-1), `RTOS_TIMEOUT` (-2); `rtos_*_create` returns `NULL` on failure.

**Stack sizing:** `stack_words` counts `RTOS_STACK_BYTES_PER_WORD` units (4 on 32-bit, 1 on AVR). Always declare stacks as `static rtos_stack_t stack[N]`.

**Intrusive lists:** `rtos_tcb_t` has a `next` pointer; `src/list.c` is used only inside the scheduler.

## Adding a New Port

1. Create `port/<arch>/port.c` implementing all 6 `port_` functions defined in `src/port.h`.
2. Create `port/<arch>/port_asm.S` for the context-switch handler (saves/restores full register set, calls `rtos_context_switch()`).
3. Add a toolchain file in `cmake/` — it must set `CMAKE_SYSTEM_PROCESSOR` to a unique string.
4. Add a new `elseif` branch in `CMakeLists.txt` to select the port sources.

## Testing New Kernel Logic

Add test functions to `test/test_rtos.c` using the `TEST(expr)` macro and register them in `main()`. Port stubs at the top of that file stub out all `port_` functions.

## Workflow

Do not run `git commit` or `git push` — leave all commits to the developer so they can review changes first.

## Releasing

Releases are tag-driven; CI handles packaging. See `RELEASING.md` for the full checklist. Tag prefix `v` triggers a full project release; `arduino-v` triggers an Arduino library release.

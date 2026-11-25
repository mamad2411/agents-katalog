---
name: lang-odin
description: Odin systems programming, explicit context management (context.allocator, context.temp_allocator), tracking allocators for leak detection, distinct domain types, and data-oriented #soa layout.
---

# Odin Context Management & Memory Control Contract

## 1. Purpose
Define and enforce high-performance systems engineering standards in Odin, ensuring strict context and allocator hierarchy management, leak-free memory lifecycles via `mem.Tracking_Allocator`, cache-coherent Data-Oriented Architecture (DOA) with `#soa`, strong domain modeling via `distinct` types, and explicit error handling via `or_return`.

---

## 2. Use When
- Developing performance-critical systems, game engines, graphics pipelines, or low-latency simulation engines in Odin.
- Structuring memory around custom allocators (Arena, Pool, Scratch/Temp, Tracking).
- Designing cache-friendly data structures using Structure of Arrays (`#soa`).
- Writing C-compatible native libraries or calling foreign C libraries.

---

## 3. Do Not Use When
- Developing managed web frontend applications or microservices in Go (`lang-go`) or TypeScript (`lang-typescript`).
- Writing shell scripts (`lang-bash`).
- The project language is Zig (`lang-zig`), Rust (`lang-rust`), C++ (`lang-cpp`), or C (`lang-c`).

---

## 4. Required Context
Before implementing or modifying Odin code, verify:
1. **Odin Toolchain & Target**: Target platform, vendor libraries (`core:mem`, `core:fmt`, `core:slice`, `vendor:wgpu`, etc.).
2. **Allocation Architecture**: Identify the lifetime and allocator strategy (frame-based temp allocator, persistent arena, or general-purpose heap).
3. **Cache & SIMD Constraints**: Determine if data entities require `#soa` transformation for vectorization and cache locality.

---

## 5. Procedure

### Step 1: Context & Allocator Hierarchy Management
1. Structure memory around the implicit/explicit Odin `context`:
   - Use `context.allocator` for persistent domain allocations.
   - Use `context.temp_allocator` for short-lived scratch allocations within a loop or function boundary.
2. In long-running loops or per-frame tasks, clear temporary memory deterministically:
   ```odin
   free_all(context.temp_allocator)
   ```
3. In test suites and debug builds, wrap allocations in `mem.Tracking_Allocator` to assert 0 memory leaks upon procedure termination.

### Step 2: Dynamic Resource Lifecycles
1. Every dynamic array, map, or slice allocation (`make`, `new`, `slice.clone`) must be paired with an immediate deterministic cleanup using `defer`:
   ```odin
   items := make([dynamic]Entity, context.allocator)
   defer delete(items)
   ```
2. For procedures returning allocated data, explicitly document allocator ownership in the signature or return a cloned slice allocated with caller-provided allocator.

### Step 3: Data-Oriented Architecture (#soa)
1. For large homogeneous collections (>64 items) accessed in hot loops, use Structure of Arrays `#soa`:
   ```odin
   Particle :: struct {
       pos: [3]f32,
       vel: [3]f32,
       life: f32,
       color: [4]u8,
   }

   // Allocates parallel arrays for pos, vel, life, color in contiguous memory
   particles := make(#soa[dynamic]Particle, context.allocator)
   defer delete(particles)
   ```
2. This layout maximizes CPU L1/L2 cache line saturation and allows auto-vectorization across single attributes (e.g. updating all `life` counters without loading positions).

### Step 4: Distinct Types & Domain Modeling
1. Prevent primitive obsession and accidental argument swapping by declaring strong types using `distinct`:
   ```odin
   Entity_Id :: distinct u64
   Session_Id :: distinct u64
   ```
2. Use tagged unions (`union`) for state and variant representations, handling branches with `switch in`.

### Step 5: Error Discipline & Early Returns
1. Return explicit errors using multiple return values or custom error enums:
   ```odin
   read_data :: proc(path: string) -> (data: []u8, err: os.Error) { ... }
   ```
2. Use the `or_return` idiom to propagate errors cleanly without nested `if` statements:
   ```odin
   content := os.read_entire_file(filepath, context.allocator) or_return
   defer delete(content)
   ```

---

## 6. Decision Rules
1. **Zero Unchecked Allocations**: Any procedure using dynamic memory must either accept an allocator parameter or explicitly configure `context.allocator` / `context.temp_allocator`.
2. **Scratch First**: Prefer allocating temporary string formatting or transformation buffers with `context.temp_allocator` over hitting the heap allocator.
3. **No Raw Pointer Arithmetic Without Escape Hatch**: Unsafe raw pointer arithmetic (`cast(rawptr)`) must be logged in `.prumo/escape-hatches.json`.
4. **No Hidden Control Flow**: Odin proscribes operator overloading and implicit casting. Maintain explicit, clear procedural flow.

---

## 7. Evidence Required
- **Tracking Allocator Proof**: Zero leaked allocations or bad frees reported by `mem.Tracking_Allocator`.
- **Compiler Check**: `odin check <path>` exits 0 with zero warnings.
- **Escape Hatch Registry**: All `cast(rawptr)` or `intrinsics` calls documented.

---

## 8. Output Contract
A production Odin artifact must include:
1. Clean, idiomatic `.odin` source files formatted to standard conventions.
2. Leak-free tracking allocator unit tests.
3. Clear allocator ownership contracts on all exported procedures.

---

## 9. Stop Conditions
- `odin check` and tests pass without errors.
- `mem.Tracking_Allocator` reports 0 memory leaks across all test paths.
- All temporary allocations freed.

---

## 10. Escalation Rules
- Escalate to Systems Architect if cache profiling indicates false sharing or cache thrashing in multi-threaded task queues.
- Escalate to Lead Developer if external C FFI bindings produce memory corruption across the language boundary.

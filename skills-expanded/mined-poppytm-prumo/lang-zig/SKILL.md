---
name: lang-zig
description: Zig systems programming, explicit allocator passing (std.mem.Allocator), defer/errdefer resource cleanup, error union handling, comptime type invariants, and leak-free memory discipline.
---

# Zig Explicit Allocation & Comptime Verification Contract

## 1. Purpose
Define and enforce strict systems programming standards in Zig, ensuring explicit allocation topologies, zero hidden control flow, leak-free memory management with `std.testing.allocator` / GPA, robust error union handling, and compile-time type validation via `comptime`.

---

## 2. Use When
- Developing high-performance systems utilities, command-line binaries, or low-level runtime engines in Zig.
- Implementing memory-critical algorithms requiring custom allocators (Arenas, FixedBuffer, Pools, GPA).
- Authoring C-interoperable libraries or native bindings (`@cImport`, `extern fn`).
- Constructing compile-time metaprogrammed data structures, parsers, or serializers.

---

## 3. Do Not Use When
- Developing browser web user interfaces without WebAssembly target.
- Scripting simple shell-level pipeline automations where `lang-bash` is specified.
- The project language is Rust (`lang-rust`), Go (`lang-go`), C++ (`lang-cpp`), or C (`lang-c`).

---

## 4. Required Context
Before implementing or refactoring Zig code, verify:
1. **Target Zig Version**: Verify compatibility (Zig 0.13.x - 0.16.x).
2. **Allocation Topology**: Identify the lifetime requirements (long-lived state vs. scratch arena vs. stack fixed-buffer).
3. **Build Architecture**: Inspect `build.zig` and dependencies.
4. **Safety Level**: ReleaseSafe vs. ReleaseFast vs. ReleaseSmall vs. Debug.

---

## 5. Procedure

### Step 1: Explicit Allocator Discipline
1. Never hide dynamic heap allocations behind global variables or implicit initializers. Every function performing dynamic memory allocation must take an explicit `allocator: std.mem.Allocator` as its first parameter (or within an explicit context struct).
2. Pair every allocation with deterministic cleanup:
   - For infallible resource teardown: `defer allocator.free(slice);` or `defer resource.deinit();`.
   - For multi-step initialization failure rollbacks: `errdefer allocator.free(partial_slice);`.
3. Choose the appropriate allocator tier:
   - **Scratch / Request Lifecycles**: `std.heap.ArenaAllocator` wrapping a child allocator. Allocate freely throughout the request; free all memory at once with `arena.deinit()`.
   - **Bounded Fixed Memory**: `std.heap.FixedBufferAllocator` over a stack slice (`var buffer: [4096]u8 = undefined;`).
   - **General Dynamic Long-Lived**: `std.heap.GeneralPurposeAllocator(.{})` in development/release, or `std.testing.allocator` in tests.

### Step 2: Error Union & Control Flow Discipline
1. Use Zig error unions (`!T` or `E!T`). Never discard errors silently with empty catch clauses (`_ = fallible() catch {};`).
2. Propagate errors idiomatically using `try`:
   ```zig
   const buffer = try allocator.alloc(u8, size);
   errdefer allocator.free(buffer);
   ```
3. When handling errors explicitly, use `catch |err| switch (err) { ... }` to handle each known failure mode with appropriate diagnostics or fallback.

### Step 3: Comptime Validation & Metaprogramming
1. Leverage `comptime` to validate type contracts and configuration constraints at build time:
   ```zig
   pub fn RingBuffer(comptime T: type, comptime capacity: usize) type {
       comptime {
           if (capacity == 0) @compileError("RingBuffer capacity must be greater than 0");
           if (!@typeInfo(T).is_copyable) @compileError("RingBuffer elements must be copyable");
       }
       return struct { ... };
   }
   ```
2. Utilize `@typeInfo` and `@Type` for reflection and compile-time struct generation without runtime overhead.

### Step 4: Slice & Pointer Safety
1. Prefer fat slices (`[]T`, `[]const T`) over raw multi-item pointers (`[*]T`).
2. When interfacing with null-terminated C APIs, use sentinel-terminated slices (`[:0]const u8`) and ensure sentinel bytes are checked.
3. Keep pointer alignment explicit (`align(N)`). Never cast pointers arbitrarily with `@ptrCast` without registering the justification in `.prumo/escape-hatches.json`.

### Step 5: Test Verification & Leak Detection
1. Write unit tests using `std.testing.allocator`.
2. Ensure `zig test` completes with zero leaked bytes reported by GPA leak detection.
3. Test edge cases: 0-length inputs, allocation failures (using `std.testing.FailingAllocator`), and out-of-order error teardowns.

---

## 6. Decision Rules
1. **Zero Hidden Allocations**: Any function that allocates memory dynamically without receiving a `std.mem.Allocator` parameter is a violation.
2. **Deterministic Arena Scopes**: For tasks involving multiple parsing steps or AST allocations, use an `ArenaAllocator` and tear down the entire arena at the boundary rather than tracking individual element frees.
3. **No `@panic` in Production Paths**: Never call `@panic` for anticipated runtime errors (invalid user input, network failure, missing file). Reserve `@panic` strictly for unrecoverable compiler bugs or broken internal invariants.
4. **Bounds Checking Mandatory**: In release modes where performance is critical, use `ReleaseSafe` by default unless explicitly profiled and approved for `ReleaseFast`.

---

## 7. Evidence Required
- **Zig Test Output**: `zig test <file>` exits with code 0 and reports 0 leaks under `std.testing.allocator`.
- **Formatting**: `zig fmt --check <files>` passes cleanly without modifications.
- **Escape Hatch Registry**: Any `@ptrCast`, `@alignCast`, or `unreachable` on fallible paths logged in `.prumo/escape-hatches.json`.

---

## 8. Output Contract
A production Zig artifact must include:
1. Idiomatic `.zig` implementation with explicit allocators and error union propagation.
2. Complete test suite in the same file or `tests/` leveraging `std.testing.allocator`.
3. `build.zig` integration targets.
4. Clean execution logs confirming zero memory leaks.

---

## 9. Stop Conditions
- All Zig tests pass deterministically.
- `std.testing.allocator` reports 0 memory leaks across all test execution branches.
- Code formatted with `zig fmt`.

---

## 10. Escalation Rules
- Escalate to Lead Architect if an external C library integration causes undefined behavior or memory corruption across FFI boundaries.
- Escalate to Security Officer if memory safety sanitizers detect undefined behavior in ReleaseFast mode.

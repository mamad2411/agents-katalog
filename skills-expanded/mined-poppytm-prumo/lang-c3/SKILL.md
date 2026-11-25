---
name: lang-c3
description: C3 systems programming, explicit defer and catch-defer resource cleanup, bounds-checked slices (Type[]), contract annotations (@pure/@require/@ensure), and fault handling (!Type).
---

# C3 Semantic Safety & Contract Assertions Contract

## 1. Purpose
Define, implement, and audit systems software written in C3, enforcing deterministic resource management via `defer` and `defer (catch)`, safe bounds-checked slice operations over naked pointers, explicit fault handling via `!Type`, formal contract annotations (`@pure`, `@require`, `@ensure`), and seamless ABI-compatible C interoperability without undefined behavior.

---

## 2. Use When
- Developing systems software, low-level libraries, or embedded modules where C compatibility and zero-cost abstractions are required.
- Refactoring legacy C codebases into C3 to eliminate buffer overflows, use-after-free, and unhandled error codes.
- Writing performance-critical routines requiring vector types, SIMD extensions, and precise memory layout control without C++ runtime overhead.
- Implementing procedures with formal contract preconditions and postconditions.

---

## 3. Do Not Use When
- Developing managed web applications or microservices in Go (`lang-go`) or TypeScript (`lang-typescript`).
- The project language is Zig (`lang-zig`), Odin (`lang-odin`), Rust (`lang-rust`), C++ (`lang-cpp`), or C (`lang-c`).
- Simple shell automation where `lang-bash` is appropriate.

---

## 4. Required Context
Before implementing or modifying C3 code, verify:
1. **Target Architecture & Toolchain**: Target OS/architecture, `c3c` compiler version (v0.6+).
2. **Project Configuration**: `project.json` manifest, dependency modules, build targets (`c3c compile-run`, `c3c test`).
3. **Safety Optimization Level**: Safe mode (bounds checking active, overflow trapping) vs. Fast/Release mode.

---

## 5. Procedure

### Step 1: Deterministic Resource Management with Defer
1. Every allocated resource, opened file descriptor, mutex lock, or external handle must have an immediate `defer` statement:
   ```c3
   void* memory = mem::alloc(1024);
   defer mem::free(memory);
   ```
2. For fallible multi-step operations, use conditional defer rollback:
   - `defer (catch err) cleanup();`: Executes only if the surrounding procedure exits with a fault/error.
   - `defer (no_catch) finalize();`: Executes only on successful completion.

### Step 2: Slice Discipline & Bounded Arrays
1. Ban raw pointer arithmetic (`int* ptr`) for iterating sequences in public interfaces. Always use slices (`int[]`):
   ```c3
   fn void process_buffer(char[] buffer) {
       foreach (byte : buffer) {
           // Safely bounded traversal
       }
   }
   ```
2. Slices encapsulate both pointer and length (`.len`), guaranteeing runtime bounds verification in safe builds.
3. Slice sub-ranges using safe range syntax: `char[] sub = buffer[0..16];`.

### Step 3: Fault Handling & Optional Returns
1. Never encode error states as ambiguous magic return numbers (`-1`, `NULL`).
2. Use C3 fault returns (`!Type`):
   ```c3
   fault FileError {
       NOT_FOUND,
       PERMISSION_DENIED,
       CORRUPT_DATA
   }

   fn int! read_integer(File file) {
       if (!file.is_open()) return FileError.NOT_FOUND?;
       // ...
       return value;
   }
   ```
3. Handle faults explicitly using `if (catch err = read_integer(f))` or propagate with `read_integer(f)!`.

### Step 4: Contract Assertions & Semantic Annotations
1. Annotate functions with formal preconditions, postconditions, and side-effect guarantees:
   - `@pure`: Function has no side effects and returns results based solely on input arguments.
   - `@nodiscard`: Compiler enforces that caller must check the return value.
   - `@param [in,out]` and contract assertions (`assert(x > 0)`).
2. Use `distinct` types to prevent accidental unit or ID mismatches:
   ```c3
   distinct Microseconds = u64;
   distinct Kilograms = f32;
   ```

### Step 5: Testing & Verification
1. Author unit tests using `@test` annotations inside the module.
2. Verify edge cases: zero-length slices, null handles, fault injection, and resource cleanup verification.
3. Audit memory leaks in test mode with custom tracking allocators.

---

## 6. Decision Rules
1. **Zero Naked Buffers**: Public procedure signatures must never accept raw `void*` or `char*` without explicit length parameters; always prefer `char[]` or `void[]`.
2. **Mandatory Defer on Acquisition**: The acquisition of a handle or dynamic memory chunk must be followed immediately by its corresponding `defer` block before any fallible operation or branch.
3. **No Silently Swallowed Faults**: Every `catch` block must either handle the error, log structured diagnostics, or rethrow. Empty catch blocks are prohibited.
4. **Escape Hatch Logging**: Any unchecked raw pointer casting (`(void*)ptr`), inline assembly, or `@unsafe` blocks must be recorded in `.prumo/escape-hatches.json`.

---

## 7. Evidence Required
- **Compiler Verification**: `c3c check` or `c3c compile` exits with code 0 and zero warnings.
- **Test Evidence**: `c3c test` executes all `@test` assertions successfully.
- **Contract Verification**: Absence of compiler warnings on `@nodiscard` and `@pure` invariants.

---

## 8. Output Contract
A production C3 artifact must provide:
1. Well-structured `.c3` module files with module headers (`module name::subname;`).
2. Clean contracts and fault signatures on all public procedures.
3. Unit test coverage with `@test` functions verifying nominal and fault pathways.

---

## 9. Stop Conditions
- `c3c check` and tests pass without errors.
- All allocated resources are paired with `defer` or `defer (catch)`.
- Contract assertions verified.

---

## 10. Escalation Rules
- Escalate to Lead Architect if C ABI interoperability encounters struct alignment discrepancies or packing differences with foreign C headers.
- Escalate to Security Officer if memory corruption or bounds violation occurs in release builds.

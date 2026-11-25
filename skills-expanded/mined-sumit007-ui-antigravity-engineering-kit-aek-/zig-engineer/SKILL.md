---
name: zig-engineer
description: Build low-level systems, cross-compilation toolchains, and native libraries with Zig. Enforces explicit memory allocators, comptime metaprogramming, and C ABI interop.
---

# Zig Engineer Skill

## Purpose
Guides robust systems engineering using the Zig programming language, with zero hidden control flow and explicit allocation.

## When to Use
- Writing native C-compatible libraries, OS kernels, embedded runtimes, or cross-platform utilities in Zig.
- Optimizing code with comptime generics and compile-time assertions.
- Replacing Make/CMake build systems with `build.zig`.

## Engineering Workflow
1. **Explicit Allocation**: Pass `allocator: std.mem.Allocator` to data structures; free with `defer allocator.destroy(...)`.
2. **Error Handling**: Use error unions (`!T`) and `try` statements with detailed diagnostics.
3. **Verification**:
   - `zig fmt --check .`
   - `zig build test`


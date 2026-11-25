---
name: cpp-systems-engineer
description: Architect low-latency native systems, embedded firmware, and computational engines using modern C++20 and CMake. Enforces RAII, memory safety, and sanitizer validation.
---

# C/C++ Systems Engineer Skill

## Purpose
Directs modern C++ (C++20/C++23) systems programming, zero-leak memory management, and cross-platform native builds.

## When to Use
- Developing high-performance native engines, audio/graphics pipelines, or device drivers.
- Modernizing legacy C or C++98 codebases to C++20.
- Resolving memory corruption, use-after-free, or concurrency race conditions.

## Engineering Workflow
1. **Target-Based CMake**: Declare dependencies using modern target commands (`target_include_directories`).
2. **Resource Management**: Enforce strict RAII with smart pointers (`std::unique_ptr`). Avoid raw pointer ownership.
3. **Verification**:
   - Compile with `-Wall -Wextra -Wpedantic -Werror`.
   - Execute test suites under AddressSanitizer (`-fsanitize=address`) and UB-Sanitizer (`-fsanitize=undefined`).


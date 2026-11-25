---
name: exec-cpp
description: C++ execution idioms to embed into Codex prompts when the target project is C/C++ — RAII, memory safety, modern C++ idioms, and const-correctness.
---

# C++ Idioms (embed when project is C/C++)

```
C++ standards:
- RAII for every resource: memory, files, locks, sockets — no raw new/delete or manual free in
  application code; use smart pointers (unique_ptr by default, shared_ptr only for shared ownership,
  weak_ptr to break cycles) and standard containers. No owning raw pointers.
- Memory safety: no dangling references/iterators, no buffer overruns; prefer std::span/std::string_view
  for non-owning views (mind their lifetime); bounds-checked access where input-driven.
- const-correctness: mark methods/params/locals const wherever possible; pass by const& for non-trivial
  types, by value for cheap ones; use constexpr where evaluable at compile time.
- Errors: exceptions with specific types OR the project's error convention (std::expected / error
  codes) — follow whichever the codebase uses consistently; never ignore a returned error code.
- Prefer standard algorithms (<algorithm>, ranges) over hand-written loops; use auto to avoid
  redundant type spelling; enum class over plain enum; nullptr not NULL; braces for init.
- Follow the C++ standard version the build targets; match the repo's .clang-format and layout;
  respect the build system (CMake/Bazel) — declare deps and targets the project's way.
- Rule of zero: let RAII members manage lifetime; only declare special members when you must, then
  declare all five. Mark overrides override, single-arg ctors explicit.
- Tests: the repo's framework (GoogleTest/Catch2/doctest); arrange-act-assert; test behavior; match
  existing test target structure.
```

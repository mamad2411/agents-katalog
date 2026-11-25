---
name: google-style-cpp
description: >
  Apply Google's official C++ style guide when writing, reviewing, or
  formatting C++ code. Use this skill whenever the user asks to review C++
  for style, asks about C++ naming conventions, header organisation, smart
  pointer usage, exception policy, template guidelines, or whether code follows
  Google C++ standards. Also triggers on: "is this idiomatic C++?", "clean up
  this C++ file", "how should I name this in C++?", "should I use exceptions
  in C++?", "how do I write C++ comments / Doxygen?", "should I use auto
  here?", "when should I use references vs pointers?", or any mention of
  clang-format, cpplint, or IWYU in a Google-style context. Note: Google's
  C++ guide is deliberately conservative — it restricts several modern C++
  features (exceptions, RTTI, some template meta-programming) for reasons of
  build reproducibility and readability at scale.
---

# Google C++ Style Guide

Google's C++ style guide is one of the most detailed in the industry and
deliberately conservative about adopting new C++ features. The overarching
philosophy: **optimise for the reader, not the writer**. Any construct that
makes code harder to understand is suspect, regardless of how clever it is.

Key constraints that surprise people coming from other C++ styles:
- **No exceptions** (in most code; legacy constraint from Google's build system)
- **No RTTI** (`dynamic_cast`, `typeid`) in production code
- **Prefer composition** over inheritance; virtual dispatch only when necessary
- **`auto`** only when it genuinely aids clarity, not as a habit

---

## Key Rules at a Glance

### Headers (§1–2)
- Every `.cc` file has a corresponding `.h` — no inline implementation in headers except templates and small inlined functions.
- **`#pragma once`** is acceptable but Google's own code uses `#ifndef` header guards; the guard macro name is `PATH_TO_FILE_H_`.
- Headers include only what they use — no transitive includes as a crutch. Use forward declarations where possible to reduce compile-time coupling.
- `.cc` file must include its own `.h` first (ensures the header is self-contained).

### Naming conventions

| Entity | Style | Example |
|---|---|---|
| File | `snake_case.cc` / `.h` | `user_service.cc` |
| Type (class, struct, enum, alias) | `PascalCase` | `UserService` |
| Variable (local, param) | `snake_case` | `user_count` |
| Class member (non-const) | `snake_case_` (trailing `_`) | `cache_size_` |
| Constant / `constexpr` | `kPascalCase` | `kMaxRetries` |
| Function / method | `PascalCase` for regular; `snake_case()` for simple accessors | `ComputeTotal()`, `size()` |
| Namespace | `snake_case` | `internal_utils` |
| Macro | `UPPER_SNAKE_CASE` | `MY_MACRO` |
| Enum members | `kPascalCase` (scoped) or `UPPER_SNAKE` (unscoped, deprecated) | `Status::kNotFound` |

### Classes
- Single responsibility — if it has more than one, split it.
- Data members are `private` by default; use accessors.
- Explicit constructors where appropriate; mark single-arg constructors `explicit` to prevent implicit conversion.
- Override `= delete` copy/move to prevent accidental copies when the type isn't copyable.
- Prefer composition over inheritance; use `final` on classes not meant to be subclassed.
- Virtual methods only on base classes that represent abstract interfaces.

### Smart pointers & ownership
- `std::unique_ptr<T>` — sole ownership, default choice.
- `std::shared_ptr<T>` — shared ownership; use sparingly (hidden cost).
- Raw pointers — non-owning references only (borrowing). Never use `new`/`delete` in application code.
- `std::make_unique<T>()` / `std::make_shared<T>()` — always, never `new`.

### No exceptions / No RTTI
```cpp
// No throw/catch in new Google C++ code
// Signal errors via return codes or Status types:
absl::Status DoSomething();
absl::StatusOr<Result> Compute(Input in);

// No dynamic_cast or typeid — use virtual dispatch instead
```

### Ownership of pointers in function signatures
```cpp
// Pass by reference when caller retains ownership and value is required
void Process(const UserData& data);

// Pass by pointer when value is optional (may be nullptr)
void Process(const UserData* data);

// Pass by unique_ptr to transfer ownership
void Store(std::unique_ptr<UserData> data);
```

### `auto`
- Use `auto` when the type is obvious from context or verbose to write:
  ```cpp
  auto it = container.begin();           // Good — type clear
  auto result = ComputeTotal(items);     // Borderline — return type should be known
  auto x = 42;                           // Bad — use int
  ```
- Do not use `auto` for return types of non-trivial public functions.

### Comments
```cpp
// Single-line for brief explanations
// Multi-word OK: "This uses a sentinel value because..."

/*
 * Block comments for longer explanations.
 * Not preferred — use multiple // lines instead.
 */

// Function comments go in the header above the declaration:
// Returns the user with the given ID, or nullptr if not found.
// Thread-safe.
std::unique_ptr<User> FindUser(absl::string_view id) const;
```

### Formatting
- **Indentation**: 2 spaces (consistent with other Google guides).
- **Line length**: 80 characters.
- **Braces**: Opening brace on same line (K&R). Always present.
- **Namespace**: Content indented 0 extra spaces; closing comment `}  // namespace foo`.
- Run `clang-format` with Google style: `clang-format -style=Google`.

---

## Mode: Reviewing C++ Code

When asked to review C++ code for Google style compliance:

1. **Headers** — header guards present? Only necessary includes? `.cc` includes its own `.h` first?
2. **Naming** — correct casing per the table? Trailing `_` on class members? `k` prefix on constants?
3. **Ownership** — any raw `new`/`delete`? Smart pointer type matches ownership model?
4. **Constructors** — single-arg constructors marked `explicit`? Non-copyable types deleted?
5. **Exceptions** — any `throw`/`catch`? Should use `absl::Status` / error codes.
6. **RTTI** — any `dynamic_cast` or `typeid`?
7. **`auto`** — overused or in ambiguous places?
8. **Inheritance** — virtual methods in non-abstract base? Should prefer composition?
9. **Line length** — any lines > 80 chars?
10. **Comments** — public API documented in the header?

For each issue:
- Cite the section (e.g. "§Naming: Variables", "§Smart Pointers")
- Show the problematic snippet and the corrected version with rationale

---

## Mode: Writing New C++ Code

When writing new C++ following Google style:

1. Create a `.h` / `.cc` pair; `.cc` includes its own `.h` first.
2. Use `#ifndef` header guards: `MY_PROJECT_PATH_TO_FILE_H_`.
3. 2-space indentation; 80-char line limit; K&R braces.
4. Name types `PascalCase`, variables `snake_case`, class members `snake_case_`, constants `kPascalCase`.
5. Mark single-arg constructors `explicit`; `= delete` copy/move for non-copyable types.
6. Use `std::unique_ptr`/`std::make_unique` for owned heap objects; raw pointers only for non-owning references.
7. Signal errors with return codes or `absl::Status`; no exceptions.
8. Write function documentation in the `.h` file, above the declaration.
9. Use `auto` only when type is verbose or obvious from context.
10. Run `clang-format -style=Google` and `cpplint` before considering code done.

---

## When to Load the Full Guide

The C++ guide is very large (~9,000 lines after conversion). Load `references/full_guide.md` when:
- A specific rule isn't covered above (e.g. templates, lambdas, `constexpr` rules, Abseil usage)
- Doing a comprehensive file-level review
- Answering questions about: `static`, anonymous namespaces, `[[nodiscard]]`, designated initialisers, ranges

Use `references/TOC.md` to navigate — search for the section heading directly rather than scrolling.

**Sections of note**:
- `## Header Files` — includes, forward declarations, inline functions
- `## Scoping` — namespaces, unnamed namespaces, `static`
- `## Classes` — all class rules in one place
- `## Functions` — parameters, return types, overloading, default args
- `## Naming` — the complete naming table
- `## Comments` — style and placement

**Also see**: `google-style-common` for cross-language naming philosophy.

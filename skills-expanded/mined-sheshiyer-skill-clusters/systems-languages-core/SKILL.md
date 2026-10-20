---
name: systems-languages-core
description: "Shared reference for the systems-languages cluster: the language-axis decision (Go · C++ · Perl), the write → prove → harden lifecycle each spoke plugs into, and the per-language idiom / error-model / tooling matrix. USE WHEN choosing conventions, picking a test or coverage command, or deciding how strict to be about input safety across Go, C++, or Perl."
cluster: systems-languages
version: 1.0.0
---

# Systems Languages Core

Shared model for the `systems-languages` cluster. The patterns, testing, and security spokes for
Go, C++, and Perl all plug into the same lifecycle — keep the decisions and toolchain consistent
here so no spoke contradicts another.

## 1. The decision the cluster turns on: language axis → lifecycle

There is no cross-language framework choice here — each spoke is a single language. The one
decision is **which language you are in**, which then fixes the idiom, the error model, and the
toolchain. From there every task walks the same three-stage lifecycle:

```
Language (Go · C++ · Perl) ──> write ──> prove ──> harden
                                 │          │          │
                       patterns / standards │   (Perl) security
                                       testing spoke
```

- **write** — the language's conventions spoke (`golang-patterns`, `cpp-coding-standards`, `perl-patterns`).
- **prove** — the matching testing spoke (`golang-testing`, `cpp-testing`, `perl-testing`), TDD red→green→refactor.
- **harden** — only Perl ships a dedicated security spoke (`perl-security`), because untrusted input + the shell + DBI is Perl's defining hazard. Go and C++ fold safety into their write stage (validate inputs, RAII, explicit errors).

**Rule:** pick one language and stay in its lane — don't carry Go's `error` returns into C++
exceptions or Perl's dynamic looseness into Go. Resolve the language first; the rest cascades.

## 2. Shared conventions (every spoke)

- **Tests first.** All three testing spokes are TDD-first: write a failing test, make it pass, refactor. Test behavior through the public surface, not internals.
- **Errors are explicit, not swallowed.** Go: wrap with `fmt.Errorf("...: %w", err)`, never `_`-ignore. C++: custom exception types, throw by value / catch by reference, RAII so nothing leaks. Perl: checked syscalls, `Try::Tiny` or native `try/catch` (5.40+), never bare `eval` without a check.
- **Immutability / least privilege by default.** C++ `const`/`constexpr` unless mutation is intended; Go's useful zero values and small interfaces; Perl `use constant`/Moo defaults over mutable globals.
- **Validate every external input.** Allowlist over blocklist. In Perl this is enforced (taint mode + untaint regex); in Go/C++ it is a discipline the patterns spokes describe.
- **No `sleep`-based synchronization in tests.** Use conditions/latches/channels; keep tests deterministic and isolated; clean up temp dirs.
- **Coverage target ≈ 80%+** on business logic; 100% on critical paths. All three testing spokes converge on this.

## 3. Per-language idiom · error model · tooling matrix

| Language | Idiom anchor | Error model | Test framework | Runner / build | Coverage | Lint / format | Patterns spoke | Testing spoke |
|---|---|---|---|---|---|---|---|---|
| **Go** | accept interfaces, return structs; useful zero value; `context` first arg | `error` values + `%w` wrap; `errors.Is/As` | stdlib `testing` (table-driven), fuzzing 1.18+ | `go test ./...` (`-race`) | `go test -cover` / `go tool cover` | `gofmt`, `goimports`, `go vet`, `golangci-lint` | `golang-patterns` | `golang-testing` |
| **C++** | RAII, Rule of Zero/Five, smart pointers, `enum class`, concepts (C++17/20/23) | exceptions (custom types, throw-by-value) + `noexcept`; RAII cleanup | GoogleTest / GoogleMock | CMake + CTest (`gtest_discover_tests`) | gcov/lcov or llvm-cov; ASan/UBSan/TSan | C++ Core Guidelines; clang-format/clang-tidy | `cpp-coding-standards` | `cpp-testing` |
| **Perl** | `use v5.36`, signatures, postfix deref, Moo/Corinna OO | `Try::Tiny` / native `try/catch` (5.40+); checked syscalls; taint mode | Test2::V0 (or Test::More) | `prove -lr` (`-j` parallel) | `Devel::Cover` (`cover -test`) | `perltidy`, `perlcritic` (+ security theme) | `perl-patterns` | `perl-testing` (+ `perl-security`) |

## 4. Version / language baselines

- **Go** — modern modules, Go 1.18+ for generics & fuzzing, 1.22+ recommended for CI examples.
- **C++** — C++17/20/23; concepts and ranges assume C++20.
- **Perl** — target **5.36+** (`use v5.36` enables strict/warnings/signatures); native `try/catch` is 5.40+, the `class` keyword (Corinna) is 5.38+. Pin CPAN deps in `cpanfile`.

## 5. Shared guardrails

- One language per task; don't mix idioms or toolchains across spokes.
- TDD-first: a failing test before the fix; deterministic, isolated tests; no `sleep` sync.
- Errors are explicit and checked — never silently ignored (Go `_`, empty C++ `catch`, bare Perl `eval`).
- Validate all external input with allowlists; constrain filesystem and process execution.
- **Perl-specific (non-negotiable when input is untrusted):** taint mode (`-T`) on web/CGI, three-arg open, list-form `system`/`exec`, DBI placeholders for every query, context-correct output encoding. State any widening of an input surface explicitly. → `perl-security`
- Immutability / `const` / least privilege by default; pin language and dependency versions.

---
name: systems-languages-orchestrator
description: "Route a systems-language task to the right skill among 7 specialists — Go (patterns, testing), C++ (Core Guidelines coding standards, GoogleTest/CTest testing), and Perl (modern 5.36+ patterns, Test2 testing, taint/injection security). USE WHEN a user is writing, reviewing, testing, or hardening Go, C++, or Perl code but hasn't named the language axis or the specific concern."
cluster: systems-languages
version: 1.0.0
---

# Systems Languages Orchestrator

The single entry skill for Go, C++, and Perl work. It locates the task on the
**language × concern** map and delegates to one of 7 specialist spokes. The cross-cutting
model every spoke shares — pick the language, then move write → prove → (for Perl) harden, with
each language's idiomatic style and toolchain — lives in `systems-languages-core`; read it
before choosing conventions or wiring a test/coverage command.

## Cluster map (spoke → role)

**Go**
- `golang-patterns` — idiomatic Go: accept-interfaces/return-structs, useful zero values, error wrapping, concurrency (worker pools, context, errgroup), functional options, package layout, performance.
- `golang-testing` — table-driven tests, subtests, `t.Helper`/`t.Cleanup`, golden files, benchmarks, fuzzing (1.18+), coverage, HTTP handler tests — TDD-first.

**C++**
- `cpp-coding-standards` — the C++ Core Guidelines distilled: RAII, immutability-by-default, Rule of Zero/Five, smart pointers, `enum class`, concepts, no C-style casts, naming, performance.
- `cpp-testing` — GoogleTest/GoogleMock with CMake/CTest: fixtures, mocks vs fakes, `gtest_discover_tests`, coverage (gcov/llvm-cov), sanitizers (ASan/UBSan/TSan), flaky-test guardrails.

**Perl**
- `perl-patterns` — modern Perl 5.36+: `use v5.36`, signatures, postfix deref, `isa`, Moo/Corinna OO, named-capture regex, Path::Tiny, Exporter, perltidy/perlcritic/carton tooling.
- `perl-testing` — Test2::V0 (+ Test::More), `prove` runner, hash/array/bag builders, subtests, exception tests (`dies`/`lives`), Test::MockModule, Devel::Cover — TDD-first.
- `perl-security` — taint mode (`-T`), allowlist input validation, three-arg open, list-form process exec, DBI placeholders, web hardening (XSS/SQLi/CSRF), ReDoS, perlcritic security policies.

## Routing rules by intent

1. **"Which language?"** unresolved → read `systems-languages-core` §1 first, then route by the language axis.
2. **Go app/service** → `golang-patterns` (+ `golang-testing` for tests, benchmarks, fuzzing).
3. **C++ code** → `cpp-coding-standards` (+ `cpp-testing` for GoogleTest/CTest, coverage, sanitizers).
4. **Perl code** → `perl-patterns` (+ `perl-testing` for tests; **always** add `perl-security` when the code touches user input, the shell, the filesystem, or SQL — that is Perl's defining hazard).
5. **"Write the tests" / TDD** → the matching `*-testing` spoke for the chosen language.
6. **"Is it safe?" / handling untrusted input in Perl** → `perl-security` (Go/C++ have no dedicated security spoke here; apply input-validation + RAII/error-handling rules from their patterns/standards spokes).
7. **"Review / refactor"** → the language's patterns or coding-standards spoke; pair with its `*-testing` spoke to lock behavior first.

## Standard flow

1. Resolve the **language** (Go · C++ · Perl) — pull the decision model from `systems-languages-core` §1 if unstated.
2. Apply the language's conventions spoke (`golang-patterns` · `cpp-coding-standards` · `perl-patterns`).
3. Drive it test-first with the matching `*-testing` spoke (`golang-testing` · `cpp-testing` · `perl-testing`).
4. For Perl that touches input/shell/FS/SQL, harden with `perl-security` before shipping.
5. Return: chosen language, the spokes engaged, the toolchain/test command, and the next action.

## Guardrails

See `systems-languages-core`. In short: **stay in one language's lane** — don't carry Go idioms
into C++ or Perl conventions into Go; each has its own style, error model, and toolchain. Tests
come first (the `*-testing` spoke), and for Perl, security is **not optional** when untrusted data
is involved — taint mode, allowlist validation, parameterized DBI, and list-form process exec are
table stakes (`perl-security`). Keep Go simple and error-explicit, keep C++ RAII + const-by-default,
keep Perl on `use v5.36` with safe defaults. Never widen an input surface (new shell call, raw SQL,
two-arg open) without saying so explicitly.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).

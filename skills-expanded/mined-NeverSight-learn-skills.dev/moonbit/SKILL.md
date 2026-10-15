---
name: moonbit
description: Authoritative MoonBit reference — syntax (newtype/struct/trait/type/enum), project layout (moon.mod/moon.pkg/moon.work), tooling (moon check/test/fmt/info/ide/run/build), C FFI (`extern "c"`, moonbit.h, ownership, ASan), .mbtx scripting. Load BEFORE writing or proposing ANY MoonBit code (even a 2-line snippet in a design discussion), running any `moon` command, reading .mbt/.mbti/.mbtx files, or discussing MoonBit syntax/APIs. Triggers - .mbt/.mbtx/.mbti files, moon.mod/moon.mod.json/moon.pkg/moon.pkg.json/moon.work in cwd, @pkg references, `extern "c"`, any `moon ...` command, any MoonBit keyword or syntax in conversation. Do not guess MoonBit syntax from training — consult this skill's references.
---

# MoonBit

Authoritative guide for writing, refactoring, testing, and binding MoonBit projects.

## Route to references by task

Load the reference matching your current work BEFORE writing code:

| Task | Read |
|---|---|
| Writing MoonBit syntax — core (gotchas, primitives/`BigInt`, constants, options, label/optional params, `letrec`, autofill `SourceLoc`) | `references/language.md` |
| Defining types (structs/enums/newtypes, custom constructors, `extenum`, derive) + visibility + pattern matching | `references/types.md` |
| Strings, `StringView`, UTF-16 safety, interpolation (`<+`/`<?`), regex (`re"..."`, `=~`) | `references/strings-regex.md` |
| Arrays, `Map`, view types, spread `..x`, `Iter`/`iter()` protocol | `references/collections.md` |
| `Bytes`, byte containers (`Buffer()`), `BytesView`, bitstring patterns (binary parsing) | `references/bytes.md` |
| Error handling (`suberror`, `raise`/`catch`/`noraise`, `raise?`, `try`) | `references/errors.md` |
| Loops and control flow (`for`, functional `loop`, `while`/`nobreak`, labelled loops, pipe operators, loop invariants, `defer`) | `references/control-flow.md` |
| Methods, traits, trait objects (`&Trait`), trait/impl visibility, dot-resolution rules, operator overloading, indexing operators (`#alias`) | `references/traits-methods.md` |
| Configuring `derive(...)` — JSON enum styles, rename rules, container/case/field args | `references/derive.md` |
| Running `moon` commands (check / build / test / fmt / info / run) | `references/toolchain.md` |
| CLI programs — argument parsing (stdlib `@argparse`: `Command`/`FlagArg`/`OptionArg`/`PositionArg`; never hand-roll an argv loop), argv/env via `@env` | `references/cli.md` |
| Project/package layout, imports, `moon.mod`, `moon.pkg` config, dependencies, `using` re-exports | `references/project-config.md` |
| Multi-module workspaces (`moon.work`, `moon work init/use/sync`) | `references/project-config.md` |
| Designing visibility and public API shape (`pub`, opaque types, `.mbti` review) | `references/types.md` + `references/project-config.md` |
| Refactoring (API shrinkage, package splits, coverage gap filling, readability rules) | `references/refactoring.md` |
| Evolving a published API (`#alias`, `#as_free_fn`, `#deprecated`, `#label_migration`, `#visibility`, `#alert`) | `references/refactoring.md` |
| Optimizing data layout with `#valtype` (unboxing, flat arrays, value enums, the visibility interaction) | `references/valtype.md` |
| Optimizing hot-path code on the native backend (refcount traffic, polymorphic `Eq` on enums, cross-package inlining, reading generated C/asm, `moon tool demangle` for `_M0...` symbols) | `references/optimization.md` |
| SIMD with the experimental `V128` type (`@v128` lane ops, wasm SIMD128 mirror) | `references/optimization.md` |
| Async IO (`moonbitlang/async` setup, `with_task_group`, async tests, cancellation-safe cleanup, backpressure) | `references/async.md` |
| Writing tests (snapshot `inspect` family, black-box defaults, docstring tests, `@test.T::snapshot`, error assertions) | `references/testing.md` |
| Measuring performance (`@bench.T` benchmarks, native `--profile`, before/after methodology) | `references/optimization.md` |
| Code navigation with `moon ide` (outline/peek-def/find-references/rename/hover/doc) | `references/moon-ide.md` |
| Binding a C library (`extern "c"`, stubs, ownership, callbacks, ASan) | `references/ffi/c.md` (+ topic files in `references/ffi/`) |
| JS / Wasm / Wasm-GC FFI (`extern "js"`, `#module`, host imports, exports, `moonbit:ffi` callbacks) | `references/ffi/js-wasm.md` |
| Writing standalone `.mbtx` scripts (script skeleton, inline imports, run commands; package APIs go through the API Lookup Rule) | `references/toolchain.md` |
| Conditional compilation, link configuration, pre-build commands, warning control | `references/project-config.md` |
| Code coverage (`moon test --enable-coverage`, `moon coverage analyze/report/clean`, report formats, CI upload, `#coverage.skip`) | `references/testing.md` |
| Publishing to mooncakes.io (`moon register/login/publish`, semver/MVS, `include`/`exclude` filtering, `moon tree/install/upgrade`) | `references/publishing.md` |
| Wasm Component Model (WIT, `wit-bindgen moonbit`, `wasm-tools component embed/new/wit`, wasmtime) | `references/ffi/wasm-component.md` |

## Top recurring mistakes — check before every edit

Mined from real session history; these caused the most compiler pushback by far:

1. **Every `Warning (deprecated)` is a must-fix.** The warning text names the replacement — apply it on the spot. Never hand off a change with deprecation warnings remaining.
2. **Don't use reserved words as identifiers or field names**: `method`, `ref`, `opaque`, `member`, ... Rename with a trailing underscore (`method_`) and keep wire names via derive rename arguments.
3. **`pub` (non-`pub(all)`) types are read-only outside their package** — black-box `_test.mbt` files cannot construct them either. Before tightening `pub(all)` → `pub`, grep tests and consumers for constructor uses; provide factory functions or keep `pub(all)`.
4. **Non-`Unit` results cannot be silently discarded** — wrap intentional discards in `ignore(...)`; first ask why the result is unused.
5. **Write `!expr`, not `not(expr)`** (deprecated).
6. **Materialize a `StringView` with `.to_owned()`, never `.to_string()`** (that's the deprecated `Show` display path).
7. **Treat every `X::new()` / `@pkg.new()` as suspect — constructors are type-named now**: `Ref(x)`, `Map([], capacity=...)`, `Set([])`, `Buffer()`, `Queue()`, `Deque([], capacity=...)`, `Server(...)`. Also: `b"..."` for `Bytes` literals; `to_owned` not `to_array`; `trim()` not `trim_space`; the whole `@string.parse_int` / `parse_uint` / `parse_int64` / `parse_double` family (not `@strconv.*`); `reinterpret_as_int` / `reinterpret_as_uint` for Byte/UInt conversions; `unwrap_or_else` not `or_else`; `has_prefix` / `has_suffix` not `starts_with` / `ends_with`; `length()` not `size()`.
8. **"does not implement trait Show/Eq" means a missing derive** — `==` / `!=` needs `derive(Eq)`; interpolation `\{x}` needs `Show` (or use `\{to_repr(x)}` for debug-only display). Check derives before writing comparisons on new enums/structs; this is the single most common type error in real sessions.
9. **In a workspace mixing js/native modules, bare `moon check/test/build/info` defaults to wasm-gc and fails** — always pass `--target js|native` (run both for shared packages). And never run `moon info --target X` to refresh `.mbti` in a multi-target package: it rewrites `pkg.generated.mbti` to that target's specialized surface — regenerate with default-target `moon info` and revert such diffs.
10. **Native `String` and `Bytes` are NUL-terminated by the runtime.** `String` has a trailing UTF-16 zero code unit and `Bytes` has a trailing zero byte; `length()` excludes that sentinel. At C FFI boundaries, pass UTF-8 strings as `@utf8.encode(s)` for `const char *` — do not hand-roll conversion loops or append an extra `\0` unless the NUL is part of the logical payload. Read `references/ffi/c.md` before editing `extern "c"` bindings, C stubs, or `char *` call sites.

## API Lookup Rule

Do not answer MoonBit library API questions from memory, training data, or
snippets copied into this skill.

Before answering questions about a package API or writing code that uses one,
resolve `MOON_HOME`:

```sh
printf '%s\n' "${MOON_HOME:-$HOME/.moon}"
```

For `moonbitlang/core/*`, read the current files under:

```text
${MOON_HOME}/lib/core/
```

Start from `<package>/pkg.generated.mbti` or `<package>/pkg.mbti`. Read
README/source/tests when behavior, target support, examples, or edge cases
matter.

For registry packages, including `moonbitlang/async`, first read the project
`moon.mod` (or legacy `moon.mod.json`) to find the pinned dependency version.
Then fetch that exact version's source as plain, greppable files:

```sh
moon fetch <owner>/<package>@<version>   # → .repos/<owner>/<package>/<version>/
```

Read the relevant `pkg.generated.mbti` there first, then README, source,
tests, and examples when behavior matters. Add `--no-update` to skip the
registry-index refresh when offline; keep `.repos/` in `.gitignore`. If
`moon fetch` is unavailable (older toolchain), fall back to inspecting the
registry cache archive
`${MOON_HOME}/registry/cache/<owner>/<package>/<version>.zip`. Use
`${MOON_HOME}/registry/symbols/<owner>/<package>/<version>.symbols` if present,
or `moon ide doc` / `moon ide peek-def` for semantic lookup.

Treat `.mbti` files as the public contract. Quote or summarize signatures only
after reading the current local files. Do not claim an API is unavailable unless
the current pinned package interface and package search support that conclusion.

If you are about to write MoonBit syntax you have not verified, read the matching reference first (`references/language.md` for core syntax; `types.md`, `strings-regex.md`, `collections.md`, `bytes.md`, `errors.md`, `control-flow.md`, `traits-methods.md` for those topics). The language has evolved — training-era syntax may be wrong.

Pay special attention to:
- newtype conventions (`struct NewType(OldType)` with `.0` access) — `types.md`
- visibility defaults and opaque/public type choices — `types.md`
- string safety rules (`String[i]` returns `UInt16`, may abort, and slicing can also abort) — `strings-regex.md`
- ASCII-vs-Unicode text handling patterns, `Char::to_ascii_lowercase` / `to_ascii_uppercase` — `language.md` (primitives) / `strings-regex.md`

## Agent Workflow

1. **Clarify goal and constraints.** Confirm expected behavior, non-goals, and compatibility constraints (target backend, public API stability, performance limits). Decide early whether the task should change public API at all.

2. **Locate module/package boundaries.** Find `moon.mod` (module root; legacy projects may still use `moon.mod.json`) and relevant `moon.pkg` / `moon.pkg.json` files (package boundaries and imports).

3. **Discover APIs before coding.** Prefer `moon ide doc` queries to find existing functions/types/methods before adding new code. Use `moon ide outline`, `moon ide peek-def`, and `moon ide find-references` for semantic navigation. See `references/moon-ide.md`.

4. **Reliable refactoring.** Use `moon ide rename` for semantic rename. If multiple symbols share a name, add `--loc filename:line:col`. Use `#deprecated` (and `#alias(old_api, deprecated)` for temporary shims) for migrations; remove them once callers are updated.

5. **Edit minimally and package-locally.** Keep changes inside the correct package, use `///|` top-level delimiters, split code into cohesive files.

6. **Model visibility deliberately.** Default to the smallest public surface that serves an external consumer:
   - functions are private unless they are intentional package API
   - prefer opaque exported types (`struct` / `enum` without `pub`) over readable public records when callers do not need field access or pattern matching
   - use `priv` when the type name itself should not appear in `.mbti`
   - use `pub struct` only when outside code should read fields or pattern-match
   - use `pub(all)` rarely, only when outside construction is part of the contract
   - internal state machines, parse tables, accumulators, and helper parsers should stay internal
   - white-box tests are not justification for making internals public
   - public concrete types belong in the package users name (or a public package it re-exports) — never defined in `internal/*` and recovered via `pub using`; see "Type ownership" in `references/project-config.md`
7. **Validate in a tight loop.** `moon check` after edits; add `--warn-list +unnecessary_annotation` (equivalent to `--warn-list +73`) when cleaning redundant annotations and over-qualified constructors. `moon test [dirname|filename] --filter 'glob'` for targeted tests. `moon test --update` for snapshot changes.

8. **Finalize before handoff.** Always run `moon fmt` and `moon info` before committing — the user expects formatted code and up-to-date `.mbti` files in every commit. Review `pkg.generated.mbti` for necessity, not just change: remove unjustified public items and public mutable fields before considering the task done. Report changed files, validation commands, and any remaining risks.

## Review-Driven Readability Rules

When writing new MoonBit code or addressing review feedback, apply the
readability checks in `references/refactoring.md` ("Review-driven readability
rules") across the touched file, not just the exact commented line — indexed
iteration, view patterns over index arithmetic, no trivial helpers, labeled
args over builder chains, typed `suberror` over `fail`-text parsing, and more.

## Fast Task Playbooks

Use the smallest playbook that matches the request.

### Bug Fix (No API Change Intended)

1. Reproduce or identify the failing behavior.
2. Locate symbols with `moon ide outline`, `moon ide peek-def`, `moon ide find-references`.
3. Implement minimal fix in the current package.
4. Validate: `moon check` → targeted `moon test` → `moon fmt` → `moon info` (confirm `pkg.generated.mbti` unchanged).

### Refactor (Behavior Preserving)

1. Confirm behavior/API invariants first.
2. Prefer semantic tools: `moon ide rename`, `moon ide find-references`, `moon ide peek-def`. Use `--loc filename:line:col` when names are ambiguous.
3. Keep edits package-local and file-organization-focused.
4. Re-check whether any currently public type or field can be made opaque/private as part of the refactor without changing the intended API contract.
5. Validate: `moon check` → `moon test` → `moon fmt` → `moon info` (API should remain unchanged unless requested).

For migration shims (`#as_free_fn`, `#alias(old, deprecated)`), package splits via `pub using` re-export, and coverage-driven gap filling, see `references/refactoring.md`.

### New Feature or Public API

1. Discover existing idioms with `moon ide doc` before introducing new names.
2. Choose the minimum necessary visibility:
   - start from private/internal
   - make types opaque by default
   - only expose readable fields, constructors, or mutation when external callers truly need them
3. Add implementation in cohesive files with `///|` delimiters.
4. Add/extend black-box tests and docstring examples for public APIs.
5. Validate: `moon check` → `moon test` (use `--update` for snapshots when needed) → `moon fmt` → `moon info` (review and keep only intended `pkg.generated.mbti` changes).

## Project Layouts

MoonBit uses `.mbt` for source files and `.mbti` for interface files. At the top of a project there is a `moon.mod` file with module metadata. The project may contain multiple packages, each with `moon.pkg` (preferred) or `moon.pkg.json` (legacy). Subdirectories can also contain `moon.mod` to scope a different dependency set. Legacy projects may still contain `moon.mod.json`; treat it as the old module metadata format and migrate/update guidance to `moon.mod` instead of creating new `moon.mod.json` files. Repos with **multiple modules** add a `moon.work` workspace manifest at the root listing member modules — see `references/project-config.md` (`moon work init/use/sync`).

### Example layout

```
my_module
├── moon.mod                  # Module metadata; source option can specify source dir
├── moon.pkg                  # Package metadata (each directory is a package like Go)
├── README.mbt.md             # Markdown with tested code blocks (`test "..." { ... }`)
├── README.md -> README.mbt.md
├── cmd/
│   └── main/
│       ├── main.mbt
│       └── moon.pkg          # executable package with `options("is-main": true)`
├── liba/                     # Library package
│   ├── moon.pkg              # Referenced as `@username/my_module/liba`
│   └── libb/                 # Nested package
│       └── moon.pkg          # Referenced as `@username/my_module/liba/libb`
├── user_pkg.mbt              # Root package files
├── user_pkg_wbtest.mbt       # White-box tests (access private members)
└── user_pkg_test.mbt         # Black-box tests
```

- **Module**: characterized by `moon.mod`. Like a Go module — a collection of packages, usually one per repo. Module boundaries matter for dependency management and import paths.
- **Package**: characterized by `moon.pkg` (or `moon.pkg.json`). The compilation unit (like a Go package). All source files in a package share definitions. Package name = module name + relative path to package dir (NOT file names). Imports refer to module + package paths, NEVER to file names. All `moon` subcommands execute in the module root, not the current package.
- **Files**: `.mbt` files are just chunks of source inside a package. File names do NOT create modules/packages/namespaces. You may freely split/merge/move declarations between files in the same package — any declaration can reference any other in the same package.

### Coding/layout rules you MUST follow

1. **Prefer many small, cohesive files** over one large file. Group related types and functions (e.g. `http_client.mbt`, `router.mbt`). Split when a file is getting large or unfocused.

2. **You MAY freely move declarations** between files inside the same package. Each block is separated by `///|`. Moving a function/struct/trait between files does not change semantics. Refactoring by splitting/merging files is safe.

3. **File names are purely organizational.** Don't assume file names define modules, don't put file names in type paths. Choose file names by feature or responsibility.

4. **When adding new code**, prefer adding to an existing file that matches the feature. If no good file exists, create a new one with a descriptive name. Avoid giant "impl", "misc", or "util" files.

5. **Tests**: Place in dedicated `*_test.mbt` files in the appropriate package. `*.mbt.md` files are also black-box test files — code blocks tagged ` ```mbt check ` are treated as test cases and serve both as docs and tests. `README.mbt.md` with `mbt check` examples is encouraged; symlink to `README.md` for GitHub compatibility.

6. **Interface files (`pkg.generated.mbti`)**: compiler-generated summaries of a package's public API. Useful for code review. Check them into version control — commits that don't change public APIs leave these files unchanged. Generated by `moon info`; never edit them by hand (not even whitespace cleanup) — regenerate and review the diff as the public-API signal.

7. **Public API minimization**: treat every `.mbti` entry as an API promise.
   - Public mutable fields are almost always wrong.
   - Internal helper types should not leak into `.mbti`.
   - White-box tests should use package visibility, not force broader API exposure.

## Common Pitfalls

- **Don't use uppercase for variables/functions** — compilation error. Top-level `let UPPER_CASE = ...` is a parse error: module-level constants are `const NAME = ...`; top-level `let` must be lower_snake_case
- **Don't forget `mut` for mutable record fields** — immutable by default (Arrays typically do NOT need `mut` unless completely reassigning the variable; `push` etc. do not require it)
- **Don't add `mut` speculatively either** — a field/binding gets `mut` only when a reassignment actually exists; `unused_mut` warnings must be cleaned up
- **Never silence unused warnings** — no `_`-prefix renames or ad-hoc suppression to make `unused` warnings go away; delete or privatize the dead code instead. Persist agreed warn flags in `moon.pkg` config and run CI with `--deny-warn`.
- **Comparing two computed values in a test is `@debug.assert_eq`** — `inspect(x, content=...)` / `debug_inspect` are for literal expected content; never interpolate the expected value into `content="\{y}"`.
- **Static tables are literals or checked-in codegen** — write `let`/`const` array literals directly; for large derived tables, write a generator under `tools/` (its own MoonBit module) that emits a checked-in `.mbt` file. Never build tables dynamically in init functions.
- **`#cfg` platform-gated code is NOT type-checked on other platforms** — `--target all` covers backends, not OSes. After editing OS-specific (`#cfg`-gated) code, say so explicitly and verify the foreign branch (CI matrix or a temporary cfg-stripped check).
- **Don't ignore error handling** — errors must be explicitly handled
- **Do not introduce `abort` without explicit user approval** — before writing MoonBit code that calls `abort`, pause and ask the user to confirm that aborting is the intended behavior. Only use `abort` after that confirmation; otherwise model the failure with a typed error/`raise`, `Result`, or an approved adapter.
- **Do not write `guard` without `else` without explicit user approval** — `guard cond` / `guard x is Pattern` with no `else` panics at runtime when the condition fails; treat it with the same severity as `abort`. Default to `guard ... else { ... }` with an early return, typed error, or fallback. In tests too: prefer raising via `guard ... else { fail("...") }` over panicking.
- **Test failure priority: re-raise > `fail` > never `abort`** — in tests, prefer letting the error propagate (the test fails with the actual error); use `fail(...)` only when propagation is impossible; never `abort` in a test.
- **Don't `match` an Option** — use `x.unwrap_or(...)` (and friends) for trivial defaults, `if x is Some(v) { ... } else { ... }` for branching (chain it with related boolean conditions when that removes a nested `match` without hiding behavior), or `guard x is Some(v) else { ... }` for early exit. Reserve `match` for enums with several meaningful arms.
- **Don't swallow all async errors** — never a catch-all `catch { _ => () }` in async code; preserve cancellation first (`error if @async.is_being_cancelled() => raise error`); see `references/async.md`.
- **Don't use `return` unnecessarily** — the last expression is the return value
- **Don't create methods without `Type::` prefix** — methods need explicit type prefix
- **Don't forget to handle array bounds** — use `get()` for safe access
- **Don't forget `@package` prefix** when calling functions from other packages
- **Don't use `++` or `--`** (not supported) — use `i = i + 1` or `i += 1`
- **Don't add explicit `try` for error propagation** — inside a `raise` function, call error-raising functions normally; use `catch` to handle locally and `try!` only when aborting is intended
- **Legacy syntax**: older code may use `function_name!(...)` or `function_name(...)?` — these are deprecated; use normal calls for propagation. `try?` (convert to `Result`) is also being deprecated — prefer `try ... catch ... noraise`
- **Don't write an empty parameter list for `main`** — use `fn main { ... }` or `fn main raise { ... }`, not `fn main() { ... }`
- **Don't write record-style enum/error constructor fields** — labeled constructor fields use `label~ : Type`, e.g. `InvalidNumber(input~ : String)`, not `InvalidNumber(input : String)`
- **Don't manually forward optional arguments by branching on `Some`/`None`** — if both caller and callee use `arg? : T`, pass it through as `arg?`; do not write two calls like `if arg is Some(arg) { f(arg~) } else { f() }`.
- **Prefer range `for` loops** over C-style — `for i in 0..<(n-1) {...}` and `for j in 0..=6 {...}` are more idiomatic
- **Don't use `for { ... }` for infinite loops** — write `for ;; { ... }` instead
- **Don't `derive(Show)` for debugging** — derive `Debug` and use `debug_inspect()` for test/diagnostic output (`\{to_repr(value)}` for interpolation of composed values). Reserve a manual `impl Show` for specialized display formats (JSON, XML, domain text)
- **Don't call `@json.inspect()`** — use the prelude `json_inspect(value, ...)` without a package prefix
- **Async** — MoonBit has no `await` keyword; do not add it. Async functions/tests are marked with the `async` prefix (e.g. `[pub] async fn ...`, `async test ...`). Async functions default to raising, so do not add `raise`; add `noraise` only when the async body must not raise.
- **No `finally`** in MoonBit — use `defer expr` / `defer { ... }` for scope-exit cleanup (runs on normal exit and when an error propagates); see `references/control-flow.md`
- **Cancellation-critical async cleanup** — in `moonbitlang/async`, `defer`/`catch` DO run on cancellation, but any async operation inside the cleanup is itself cancelled immediately; must-complete cleanup needs `@async.protect_from_cancel`, with important refinements — read `references/async.md` before writing one.
- **Async pipeline backpressure** — use **bounded** queues between reader/writer tasks (an `Unbounded` inbound queue can OOM the process); shutdown/queue-draining rules in `references/async.md`.
- **No cross-package extension methods** — you cannot define `@otherpkg.Type::method` from outside that type's own package. Use free functions or define a trait and `impl Trait for @otherpkg.Type` instead.
- **Do NOT use context7** for MoonBit library lookups — MoonBit packages aren't indexed there. Use `moon ide doc`, mooncakes.io, the moon registry cache (`${MOON_HOME:-$HOME/.moon}/registry/cache/`), `.mbti` files, or the library's source/GitHub instead.
- **Avoid `moonbitlang/x` when a `core`/`async` equivalent exists** — `moonbitlang/x` is a staging/experimental grab-bag. IO (fs, network) → `moonbitlang/async`; encoding → `moonbitlang/core/encoding`. Exception: `moonbitlang/x/path` for pure path manipulation is fine and preferred over hand-rolled string splitting. Only reach for other `x` packages when the user explicitly asks.
- **Legacy declaration syntax to avoid**: `typealias B as A` (use `type Alias = T` or `#alias(...)`); `suberror E T` payload shorthand (use `suberror E { E(T) }`); un-annotated async/raising lambdas — effect inference is deprecated, mark lambdas `async`/`raise` explicitly.
- **Postfix `catch` can't be a bare scrutinee** — `match f() catch { ... } { ... }` is a parse error; wrap in parentheses or bind with `let` first.
- **Don't use deprecated `Json` accessors** (`.value(key)`, `.as_string()`, ...) — pattern-match instead: `if json is Object(obj) { obj.get(key) }`, `if json is String(s) { ... }`.
- **`#valtype` has hard limits** (currently ≤6 fields, no `mut` fields, no abstract-type fields, no nested value types — limits may be relaxed in future compiler releases) — check `references/valtype.md` before annotating.
- **Search core before hand-rolling utilities** — case-insensitive compare is `equal_ignore_ascii_case`, substring scan is `String::contains_any`, clamping is `Int::clamp`, String↔Bytes is `moonbitlang/core/encoding/utf8`, CLI parsing is `@argparse` (stdlib — see `references/cli.md`; never hand-roll an argv loop). If it feels like a common utility, look it up first (see API Lookup Rule).
- **Don't assert performance conclusions without measuring** — no "this is faster/slower" claims without a benchmark or profile run; propose the measurement first (see `references/optimization.md`).

For complete syntax details, see `references/language.md` (and its topic files `types.md`, `strings-regex.md`, `collections.md`, `bytes.md`, `errors.md`, `control-flow.md`, `traits-methods.md`). For `moon` tooling, see `references/toolchain.md` (commands), `references/project-config.md` (module/package config), and `references/moon-ide.md`.

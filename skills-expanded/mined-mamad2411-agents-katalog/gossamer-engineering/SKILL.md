---
name: gossamer-engineering
description: 'Gossamer `.gos`, `gos`, `project.toml`, and `project.lock` engineering guidance. Use for existing Gossamer repositories and explicitly requested bounded Gossamer evaluation/proof work: implementation, review, testing, build, package, deployment, Rust bindings, goroutines, or targets. Do not use for generic language/toolchain selection before Gossamer is selected, including standalone Wasm requirements, or for the unrelated ChainSafe Go project named Gossamer.'
---

# Gossamer Engineering

Use this skill for the **Gossamer programming language**: a pre-1.0,
general-purpose, statically typed language whose source files are `.gos` and
whose unified tool is `gos`. A Gossamer **project** is a versioned distribution
unit described by `project.toml`. `project.lock` records resolution metadata for
the package sources it covers; it does not authenticate an untrusted checkout,
hash live path dependencies, or cover Cargo and prebuilt inputs used by Rust
bindings.

Gossamer combines Rust-flavoured `enum`, `trait`, generic, pattern-matching,
`Option`, `Result`, and `?` syntax with Go-shaped M:N (many goroutines on many
OS threads) goroutines and typed channels. Its automatic memory model is
reference counting (RC) with compiled-tier cycle collection and scoped
`arena {}` allocation. It has a
bytecode VM, optional in-process Cranelift JIT, and LLVM ahead-of-time (AOT)
native builds.

This is not the unrelated [ChainSafe Go project named Gossamer](https://github.com/ChainSafe/gossamer).
Do not load this skill for Polkadot/Substrate work, Go packages, or a repository
that happens to use that name.

## Should and should not trigger

**Trigger:** “add a `.gos` module in this Gossamer repository,” “review this
Gossamer `project.toml` or `project.lock`,” “fix this Gossamer `gos check`,”
“make a Gossamer goroutine safe,” “build an existing Gossamer AOT binary,”
“add a Gossamer Rust binding,” or “perform this explicitly requested bounded
Gossamer target/feature proof.”

**Do not trigger:** “update the ChainSafe Gossamer Go node,” “write a Go
channel,” “package a generic Docker image without Gossamer sources,” “choose a
language/toolchain,” or “I need a standalone Wasm artifact; what language
should I use?” A generic selection request belongs to the project’s comparison
process; load this skill only after Gossamer is selected, except for an
explicitly bounded Gossamer evaluation/proof. Automation-language selection
belongs first to [`script-engineering`](../script-engineering/SKILL.md).

## What it is—and is not

| Comparison | Gossamer similarity | Important difference for implementation |
| --- | --- | --- |
| Rust | `fn`, `struct`, `enum`, traits, generic monomorphisation, explicit error values, and matching | `&T` and `&mut T` are managed aliases, not lifetime-bound borrows; there is no ownership transfer or borrow checker. |
| Go | M:N goroutines, typed channels, `select`, a unified command, and managed aggregate sharing | Syntax and error handling are Rust-like; its dependency/project model is manifest-and-lockfile based rather than Go modules. |
| Swift ARC | compiler-inserted RC and `Weak<T>` | Gossamer compiled tiers also collect eligible reference cycles; the VM does not. |
| Zig | `comptime` evaluation and source generation | Gossamer is managed and has a fixed compiler-recognized `name!(...)` macro surface, not arbitrary user-defined macros. |

The documented properties are language and toolchain facts. Choosing Gossamer
is an adoption decision, not proof of performance, binary-size, startup-time,
memory-use, or latency parity with any alternative. Do not invent universal
benchmark claims; measure the target workload with a checked-in benchmark and
its inputs.

## WebAssembly Composition

Load [`webassembly-engineering`](../webassembly-engineering/SKILL.md) when a
Gossamer task needs a general WebAssembly decision: a WAT or `.wasm` artifact,
WASI or WIT, the Component Model, host/guest contract, runtime or target
selection, capability grants, or Wasm packaging and deployment. That skill owns
those Wasm boundary and compatibility decisions. This skill retains Gossamer
source, `gos`, `project.toml`/`project.lock`, compiler and binding mechanics,
and its documented target constraints: Gossamer does not emit supported
standalone Wasm artifacts, and its browser VM has its own stated restrictions.
The Wasm skill does not establish Gossamer language, compiler, binding, browser
VM, or supported-target claims.

## Adoption decision

Use repository evidence, an explicit target tier, and a small proof program
before committing a product to this pre-1.0 language.

| Choose Gossamer when | Benefit to verify | Do not infer |
| --- | --- | --- |
| The repository needs typed concurrent work expressed with goroutines and channels plus Rust-like sum types and explicit errors. | Compile and run a representative `go`, channel, `select`, `Result`, and `?` path with `gos check`, `gos run --no-jit`, and an AOT build. | Safety from Rust-style exclusive borrows. |
| Short-lived graphs are built, summarized, and discarded together. | Put that graph in an `arena {}` block; `gos check` must reject values that escape it, and an integration test must preserve the result. | A general-purpose replacement for all ownership/lifetime design. |
| Deployment can use a currently documented supported native target and the project accepts feature churn. | Record `gos feature-status`, current target documentation, a release build, and a native smoke test for that exact triple. | That every registered triple, standard-library module, or documented example is production-stable. |
| A Rust crate can provide the needed native integration through the typed binding ABI. | Build and test a minimal `[rust-bindings]` call across the intended execution tier. | C/C++ FFI, raw-pointer interop, or `extern "C"`. |

Prefer a demonstrably better alternative class when a requirement conflicts:

| Constraint | Prefer instead |
| --- | --- |
| Stable ecosystem APIs, broad library maturity, or a long compatibility commitment is mandatory. | A mature, stable language/platform already supported by the organization. |
| Correctness depends on ownership transfer, lifetime parameters, or compile-time exclusive mutable borrowing. | Rust. |
| The integration requires source-level raw pointers, `extern "C"`, C/C++ ABI calls, or an existing C ABI. | Rust, C/C++, or a supported FFI host. |
| The domain requires `i128`/`u128` arithmetic. | A platform/language with a supported 128-bit type or a deliberate multiword implementation. |
| The deliverable is a standalone Gossamer-generated `.wasm` artifact. | A Wasm toolchain that emits supported standalone Wasm for the required host. |
| Browser code needs filesystem, sockets, processes, SQL, or native-like goroutine scheduling. | A browser-native JS/TS or Wasm design with explicit host bridges. |

## Repository-first workflow

1. Read repository instructions and preserve unrelated changes. Before any
   routine `gos` command, inspect `project.toml` for `[rust-bindings]`. Every
   Rust binding is both a native-code trust boundary and a dependency/supply-
   chain boundary. Before accepting or executing any binding, unconditionally
   load [`security-review`](../security-review/SKILL.md),
   [`security-review-evidence`](../security-review-evidence/SKILL.md), and
   [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md).
   Keep all security evidence sanitized. Inspect
   `project.toml`, `project.lock`, workspace members, `src/`, `tests/`, nearby
   `.gos` modules, CI, deployment files, and existing `gos` commands before
   editing. Identify whether the project is a binary, library, workspace,
   binding host, or application.
2. Start `gos` to record its REPL startup banner (which includes the installed
   version), then run `gos feature-status`. The latter is authoritative for lifecycle state:
   **Stable** has the stated compatibility commitment; **Shipped** is available
   but unprotected; **Experimental** may change or disappear; **Planned** is
   not an implementation commitment. Standard-library modules default to
   Experimental until explicitly stabilized.
3. Identify the resolved entry and layout from `project.toml` and working local
   conventions. Current official sources conflict: `SPEC.md` §6.3 describes
   directory-based modules, root-level `.gos` contributions to the root module,
   subdirectory modules, and optional `mod.gos`; Writing Libraries describes
   each `.gos` file as a module, subdirectories requiring `mod.gos`, and root
   `mod name;` declarations. Do not infer inclusion or declarations from either
   description. When layout matters, make a minimal `gos check` probe with the
   installed toolchain, record its version and result/diagnostic, and follow the
   repository’s working convention for the active change. Report this document
   conflict as residual version risk.
4. Inspect `[dependencies]`, `[trusted-publishers]`, `[rust-bindings]`, any
   custom registries, Cargo lock/configuration for bindings, and the lockfile
   before changing sources. Treat a changed publisher key, checksum, source
   URL, git revision, dependency, prebuilt input, or binding as a reviewable
   trust change. A trusted-publisher key from the checkout is not independent
   identity evidence; authenticate it through an approved independent channel.
5. Determine the execution and deployment tiers required: pure VM, JIT-enabled
   VM, host AOT, or cross-target AOT. Re-check the live
   [supported-target matrix](https://gossamer-lang.org/docs/supported_targets/)
   and local toolchain; acceptance of a triple or a successful local link is
   not support evidence.
6. State an observable behavior and the smallest module/API boundary that owns
   it. Add or update focused tests before broad refactoring. Keep public items,
   errors, concurrency ownership, and feature status explicit.
7. Make the smallest coherent change. Run a narrow check and test first, then
   the repository's documented formatting, lint, test, and target lanes.
8. Report exact `gos` version/feature-status and target evidence observed,
   manifest/lockfile impact, commands run, outcomes, skipped tiers, and
   remaining pre-1.0 or Experimental risk.

### Module layout, imports, and visibility

Do not treat either current documentation model as universal. Inspect
`project.toml`, neighboring source layout, and local conventions, then use a
minimal `gos check` probe when a new file, directory, module declaration, or
import path matters. Record the installed `gos` version and probe
result/diagnostic; the installed toolchain plus the repository’s working
convention is decisive for the active change, while the documentation conflict
remains residual version risk.

The non-conflicting guidance is to use `use`, not `import`, to bind paths, and
to use `pub` for an item intended to be visible outside its local scope. Do not
add a Go-style source `package` declaration.

## Toolchain: use only confirmed commands

Run commands against the repository-selected file or project path; do not
assume a command, target, optional flag, formatter policy, or directory layout
not evidenced locally. `gos check` establishes parsing, resolution, typing, and
match exhaustiveness; it does not prove execution or compiled behavior.

### Command effects and Rust-binding gate

With `[rust-bindings]`, treat the following as consequential rather than
routine read-only operations. A per-project Rust runner can build or execute
binding code; Cargo build scripts, procedural macros, native archives, and the
binding itself can inherit host environment access and privileges. Typed ABI
validation is **not** sandboxing.

| Command or MCP method | Effect to account for | Required decision before use with any Rust binding |
| --- | --- | --- |
| `gos check`, `gos doc`, `gos repl`, `gos test`, `gos run`, `gos build` | May build or execute the project Rust runner and invoke Cargo; Cargo resolution/build inputs can use the network and write caches/target artifacts. `run`/`test` execute project behavior; `build` writes artifacts. | Obtain explicit execution authority after security and supply-chain review; use an isolated, credential-free outer environment for untrusted or external repositories. |
| `gos mcp` methods | `run`, `build`, and `test` have their corresponding execution effects; `fmt` can write files. Other exposed methods, including `check`, `doc`, and semantic navigation, need their own effect assessment when bindings exist. | Decide permission **per MCP method**. Never grant blanket trust because an MCP server is running. |
| `gos add`, `gos remove`, `gos update`, `gos tidy`, `gos fetch`, `gos vendor` | Can resolve/fetch dependencies over the network and write manifest, lock-related state as applicable, cache, or vendor content. `gos vendor` is not integrity proof. | Authorize network and writes separately; review resulting source and provenance. |
| `gos fmt`, `gos lint --fix`, `gos doc --html`, `gos clean`, `gos publish --dry-run` | Can write or remove files; publication dry-run can read/package project content and may access signing material. | Authorize the stated filesystem/key effects and use the publication controls below. |

Host permission prompts classify requested actions; they do not sandbox
transitive tool, Cargo, native-code, filesystem, network, environment, or
credential effects. For an untrusted/external repository, execution requires
explicit authority and an isolated, credential-free outer environment; stop if
that environment is unavailable.

| Need | Command | Evidence and prerequisite |
| --- | --- | --- |
| Scaffold a project | `gos new example.com/app --path ./app` | Choose `--template bin`, `lib`, or `workspace` only when the required shape is known. Review generated manifest and lockfile. |
| Create only a manifest in the current directory | `gos init example.com/app` | Confirm the directory is intended and does not contain an existing conflicting manifest. |
| Parse/type/exhaustiveness check | `gos check <entry.gos>` | Use the resolved entry or an evidenced project path; add `--timings` only for a measured compile investigation. |
| Run with VM/JIT behavior | `gos run <entry.gos>` | Executes on the bytecode VM; recursive helper work may promote through the in-process Cranelift JIT. |
| Run pure VM | `gos run --no-jit <entry.gos>` | Use to expose tier-dependent behavior without JIT tier-up. It still does **not** collect reference cycles. |
| Native AOT build | `gos build <entry.gos>` | LLVM AOT build and link; validate the produced executable on the intended supported host. |
| Optimized native AOT build | `gos build --release <entry.gos>` | Treat as a separate validation target from VM behavior. Do not claim performance without a workload measurement. |
| Cross build | `gos build --target <triple> <entry.gos>` | Use only after target-tier, SDK/sysroot, and runtime requirements are verified. A registered triple can still be unsupported. |
| Format without edits / apply format | `gos fmt --check <entry.gos>` / `gos fmt <entry.gos>` | Prefer `--check` in review/CI; only rewrite after reviewing intended scope. |
| Lint / explain / apply fixes | `gos lint --deny-warnings .`; `gos lint --explain <id>`; `gos lint --fix <path>` | `--fix` writes files; inspect its diff and never use it as a substitute for tests. |
| Unit, integration, and doc tests | `gos test <path>` | Discovers `#[test]` and Gossamer-code fences in `//` documentation. Use the smallest changed path first. |
| Data-race detector | `gos test --race <path>` | Run when concurrent writes, channels, synchronization, or goroutine lifetime changes; a passing run covers executed schedules, not all schedules. |
| Benchmark | `gos bench [--parallel N] [path]` | Executes project `#[bench]` code; record input, target, command, and baseline. Its measurements do not establish a language-wide claim. |
| Dependency lifecycle | `gos add <name>@<version>`; `gos remove <name>`; `gos update`; `gos tidy`; `gos fetch`; `gos vendor` | `gos remove` and `gos tidy` write manifest/lock-related state as applicable. Review manifest intent, source-specific provenance, and lockfile scope; `update` remains within declared ranges. `gos vendor` alone does not verify content/version integrity. |
| Docs and diagnostics | `gos doc [--html OUT] <file>`; `gos explain <code>` | Use diagnostic codes from actual output; inspect generated HTML only when it is an intended artifact. |
| REPL | `gos` or `gos repl` | Use for a small semantic probe, not as proof of project/target behavior. `%help` and `%info` inspect the session. |
| Editor / AI protocol | `gos lsp`; `gos mcp` | Both use stdio, but LSP is for editors and MCP is for agents; do not substitute their framing or configuration. |
| Development restart loop | `gos watch [path] [--] [args...]` | This validates then replaces a child process. It is not hot patching, zero-downtime deployment, or state/connection preservation. |

The separate [editor-support repository](https://github.com/danpozmanter/gossamer-editor-support)
contains integrations for VS Code, Vim, Neovim, Helix, Emacs, Sublime, and
Zed. Its documented surface may lag the compiler; inspect its version and
per-editor installation method before installing or treating features as
available.

### Installation and release evidence

Official documentation prose may say “build from source today” and promise
prebuilt binaries later, while current GitHub Releases can contain downloadable
assets. Treat that as a live-documentation conflict. Before prescribing an
installer or download URL, verify the current
[installation documentation](https://gossamer-lang.org/docs/),
[latest release API](https://api.github.com/repos/danpozmanter/gossamer/releases/latest),
asset provenance/checksums, target, and local `gos` behavior. Do not hard-code
a release version as current.

## Language essentials

### Bindings, values, and managed references

- Bindings are immutable by default; write `let mut value` only when the
  binding must be reassigned or mutated. This makes mutation reviewable in the
  declaration and is checkable by the type checker.
- `T` can be a copied primitive/value or a managed shared aggregate. Assignment
  of managed `String`, `Vec<T>`, structs, enums, and closures does **not**
  transfer ownership; it shares backing storage. Use `.clone()` when the
  contract requires a deep copy.
- `&T` is a non-null **managed shared alias** and `&mut T` is a managed alias
  granting write-through access. Neither has Rust lifetimes, moves ownership,
  or proves global alias exclusivity. `&mut` is not a concurrency guarantee.
  Synchronize cross-goroutine shared mutation with channels, `std::sync`, or
  atomics; do not reason from `&mut` alone.
- A function requiring `&mut T` must receive an explicit `&mut place`; a bare
  value is not implicitly made mutable. The checker catches common direct
  sibling aliases, but complex aliases remain the programmer's responsibility.
  References cannot cross a `go`/channel boundary—share owned managed values
  deliberately and synchronize them.

### Enums, errors, matching, and pipelines

`Option<T>` is `Some(T)` or `None`; `Result<T, E>` is `Ok(T)` or `Err(E)`.
Use them at fallible or absent-value boundaries rather than nulls or exceptions.
Use exhaustive `match` for state alternatives and keep each arm’s behavior
testable.

```gos
use std::errors

fn maybe_even(n: i64) -> Option<i64> {
    if n % 2 == 0 { Some(n) } else { None }
}

fn require_even(n: i64) -> Result<i64, errors::Error> {
    match maybe_even(n) {
        Some(value) => Ok(value),
        None => Err(errors::new("expected an even integer")),
    }
}

fn add_one_to_even(n: i64) -> Result<i64, errors::Error> {
    let value = require_even(n)?
    Ok(value + 1)
}
```

`std::errors` is currently Experimental; verify its status with
`gos feature-status` before relying on it. This source-supported example is
intentionally unexecuted here: do not claim it passed without a disposable,
isolated no-manifest/no-dependency/no-binding probe and its recorded installed
`gos` version and result.

`?` propagates `Err` from `Result` (converting the error when an appropriate
conversion exists) or `None` from `Option`; the enclosing function must return
the corresponding compatible `Result` or `Option`. Do not unwrap without a
testable invariant and a useful failure policy.

`|>` is the forward pipe. Its right side must be callable; standard-library
free functions intended for piping conventionally take the data argument last.
Use a pipe for a clear transformation sequence, not to conceal effects,
resource lifetimes, or error handling. `?` binds more tightly than `|>`.

### Entry files and top-level statements

The resolved entry file may contain bare top-level statements, which become an
implicit `main`. If a top-level statement uses `?`, that implicit main returns
`Result<(), errors::Error>`. Use exactly one entry form: top-level statements
**or** explicit `fn main`, never both. Modules and library files contain items
only. Top-level `let` bindings are locals of that implicit main; use `const` or
`static` for deliberate cross-function state.

### Goroutines and channels

`go expression` starts a goroutine; `spawn` returns a `JoinHandle<T>` whose
`join()` reports either a normal value or a captured panic. `channel<T>()`
creates typed sender/receiver endpoints, and `select` chooses among ready
operations. Give every producer/consumer a termination, cancellation, and
ownership story; test backpressure, closed-channel/error paths, and shutdown.

Do not use fire-and-forget `go` when a result, panic, cleanup, or lifecycle
must be observed—use `spawn` and join or a channel protocol. Do not share
mutable structures because aliases compile; prove synchronization with a
`gos test --race` test and a deterministic shutdown test.

For a local CPU-bound Gossamer workload whose main design problem is data or
task decomposition, partition sizing, bounded execution, deterministic
reduction, cancellation, or nested-parallelism control, compose with
[`parallelism-engineering`](../parallelism-engineering/SKILL.md). It owns that
cross-language parallel design; this skill owns Gossamer goroutine, channel,
`spawn`, memory-model, and `gos test --race` mechanics.

Do not route ordinary goroutine lifecycles, channels, `select`, async I/O, or
concurrency safety to `parallelism-engineering`; they remain Gossamer mechanics.
Spark/PySpark execution remains with
[`data-platform-engineering`](../data-platform-engineering/SKILL.md), not local
parallelism engineering.

### Memory, cycles, `Weak`, and arenas

Compiled tiers use RC and collect only eligible thread-local reference cycles;
their collection is not a tracing-GC promise. The bytecode VM used by `gos run`
does **not** collect reference cycles. Values shared across goroutines are not
eligible for that compiled-tier cycle collector. Use `Weak<T>` to break a
cycle whenever cross-goroutine reclamation or cross-tier identical liveness
matters; `upgrade()` returns `Option<T>`.

Use `arena { ... }` for a short-lived object graph that is constructed,
processed, and discarded as one unit. It bulk-frees arena allocations on block
exit, including early return, `?`, and `break`. The compiler rejects detected
escapes from an arena; structure the code so the block returns only a durable
summary outside the arena. Never rely on an arena object, including a `Weak`
reference to one, surviving its block.

`runtime::arena_push()` and `runtime::arena_pop()` are lower-level primitives
that bypass the safer structured block’s balanced-lifetime guarantee. Do not
use them without a bounded low-level review of every control-flow exit,
allocation lifetime, and cleanup path.

### Compile-time facilities and macros

`comptime` evaluates compile-time-known Gossamer expressions on the bytecode
VM and folds a scalar or `String` result. `typeInfo::<T>()` provides
compile-time reflection over named-struct fields; a `for` over it can be
unrolled. `codegen!(...)` splices the `String` produced by a `comptime fn` as
source and type-checks it at the call site. Use these only when generated code
is clearer, smaller in source, and covered by ordinary caller-facing tests.

Gossamer has a fixed documented macro set (including formatting/output and
build-time validation macros such as `regex!` and `sql!`). It does **not**
support arbitrary user-defined declarative/procedural macros, macro grammar,
hygiene, or token-tree DSLs. Prefer a function, generic, trait, or comptime
helper; do not propose Rust `macro_rules!` or procedural-macro architecture.

### Numeric behavior

`i128` and `u128` are rejected at type-check time on every tier. Every numeric
conversion requires an explicit `as` cast. For integer types up to 64 bits,
arithmetic runs with documented 64-bit runtime semantics, not the declared
narrow type’s wrap width: `200u8 + 200u8` is `400`. To request narrow wrapping,
cast explicitly after the operation; use `checked_*`, `wrapping_*`,
`saturating_*`, or `overflowing_*` methods when their stated behavior is the
contract. Test boundaries, signs, shifts, and conversions; do not import
Rust/Go debug-overflow expectations.

### Rust bindings, not general FFI

Gossamer source has no raw-pointer types, source-level `extern "C"`, or
general C/C++ FFI. Its supported native integration surface is a typed Rust
binding: declare a crate under `[rust-bindings]` in `project.toml`; the Rust
crate uses `gossamer-binding` and `register_module!`; import the exposed module
with `use` in `.gos`. The ABI supports typed values such as integers, floats,
strings, tuples, vectors, `Option`, `Result`, opaque handles, byte buffers, and
callbacks.

Every Rust binding is native code and a supply-chain boundary, even when its
ABI types validate. Its Cargo crate/git/path/prebuilt resolution is outside
`project.lock`; Cargo may not use `--locked` or `--offline` and can independently
resolve/build inputs. Before accepting or executing any binding, apply the
unconditional three-skill gate above, require explicit execution authority, and
require evidence appropriate to the input: Cargo lock/checksums/full immutable
revision for Cargo sources, or signed-prebuilt provenance and digest for prebuilt
inputs. Write a boundary test for type conversion, error conversion, panic
behavior, and every required execution/deployment tier only after that gate.

## Practices that produce evidence

| Practice | Rationale | Verification |
| --- | --- | --- |
| Check feature status before using a library/module in a compatibility-sensitive API. | Documentation does not promote a feature’s lifecycle state. | Record the relevant `gos feature-status` output and release/toolchain identity. |
| Keep public APIs small and use enums for mutually exclusive states. | Exhaustive matching makes added state visible to callers and tests. | `gos check` plus a test for each variant/error case. |
| Return `Result`/`Option` at real fallible/absence boundaries and add context at adapters. | Callers can recover or report without exceptions or null sentinels. | Test `Ok`/`Err` or `Some`/`None`, including propagated `?` paths. |
| Make data transformations data-last and pipe only clear stages. | The pipeline reads top-to-bottom without hiding effects. | Formatter, lint, and a test of the whole transformation. |
| Model goroutine lifecycles explicitly. | A goroutine can outlive its request, owner, or test. | A timeout-bounded integration test proves result, cancellation/close, and cleanup; run `gos test --race`. |
| Break reclamation-relevant cycles with `Weak<T>`. | VM cycles leak and cross-goroutine cycles are not compiled-tier collector candidates. | Exercise liveness/reclamation assumptions under pure VM and release AOT where behavior depends on it. |
| Use `arena {}` only for nonescaping bulk-lifetime data. | Its fast bulk lifetime is invalid for returned or retained graph nodes. | `gos check` and a test showing only a summary crosses the arena boundary. |
| Make narrow numeric intent explicit. | Declared narrow types do not imply narrow arithmetic wrapping. | Boundary tests and explicit casts/method calls at every intended overflow policy. |
| Keep the manifest and lockfile in sync. | A Gossamer lockfile covers only its supported resolved package sources; it does not cover path, Cargo, or prebuilt binding inputs. | Review source-specific evidence below, the diff, and relevant dependency/test lanes. |
| Validate VM and release AOT for behavior that could cross tiers. | Pure VM, JIT-enabled VM, and compiled memory collection have material differences. | Run the focused path under `gos run --no-jit`, `gos run`, and the relevant `gos build --release` binary. |

## Anti-patterns and replacements

| Do not | Why it fails | Replace with |
| --- | --- | --- |
| Apply Rust lifetime/ownership advice to `&mut`. | It is an access marker, not a lifetime or global uniqueness proof. | Explicit ownership/lifecycle design plus channels, `std::sync`, atomics, and race-tested behavior. |
| Depend on a strong reference cycle being collected by `gos run`. | The VM does not collect cycles. | Avoid the cycle or break it with `Weak<T>`; test the required tier semantics. |
| Let a graph escape `arena {}`. | The arena frees all its allocations at block exit. | Return a scalar/string summary or allocate surviving data outside the arena. |
| Use bare top-level statements with `fn main` in the same entry file. | Entry forms are mutually exclusive. | Choose one form; keep non-entry modules item-only. |
| Expect user-defined macros or use `extern "C"`/raw pointers. | Those source facilities are unsupported. | Use comptime/type reflection/codegen where appropriate, or a typed Rust binding. |
| Assume `u8` arithmetic wraps at 8 bits. | Narrow arithmetic executes with 64-bit semantics until an explicit cast. | Cast at the intended narrowing point or use an explicit overflow method and boundary tests. |
| Ship `gos build --target wasm32-...` as a runnable standalone program. | Standalone Gossamer-to-Wasm deployment is unsupported; non-host target output is placeholder/cross-link pending. | Use the browser VM for sandboxed examples or a supported standalone Wasm stack. |
| Treat `gos watch` as production hot reload. | It restarts a development child and does not preserve memory, WebSockets, streams, or zero downtime. | Use a supervisor/orchestrated rollout with health, drain, and rollback evidence. |
| Treat a local build or artifact as a supported target. | Support is evidence-tiered, not registration- or artifact-tiered. | Re-check live target docs and test the exact target in its documented support class. |

## Testing, trust, deployment, and completion

### Tests and debugging

Test pure functions, enum transitions, `Option`/`Result` errors, module public
APIs, numeric boundaries, binding conversions, and deterministic concurrency
units. Add integration tests for filesystem/network/process/database adapters
only where the actual application contract needs them; isolate external state
and avoid live credentials. Test a compiled executable for deployment behavior
that a VM run cannot establish. Use
[`test-driven-development`](../test-driven-development/SKILL.md) when executable
examples should drive a behavior change, and
[`systematic-debugging`](../systematic-debugging/SKILL.md) for an active,
unexplained compiler, runtime, race, or deployment failure.

### Security and package trust

Do not treat automatic memory management, a race detector, registry signatures,
or a lockfile as a complete security claim. Validate untrusted input, paths,
serialization, command/process boundaries, auth, secrets, and deployment
privileges at the application boundary. Load
[`security-review`](../security-review/SKILL.md) for implemented security
controls or trust-boundary changes. Whenever security evidence is handled, load
[`security-review-evidence`](../security-review-evidence/SKILL.md) and keep all
such evidence sanitized.

Before any registry, publisher-key, dependency, lockfile, vendoring,
publication, or provenance work—including adding or updating registry, git,
path, or Rust-binding dependencies; changing `project.toml`, `project.lock`,
vendored sources, package publication, or release tooling—load
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md).
Use the following source-specific evidence; no lockfile or vendoring shortcut
expands another source type’s guarantee.

| Source type | What can be established | Required acceptance evidence |
| --- | --- | --- |
| Registry dependency | Gossamer resolution can record the selected version/source tree SHA-256 and publisher key in `project.lock`. | Authenticate the publisher key through an approved independent channel. A `[trusted-publishers]` value in an untrusted checkout, or a key advertised by a mutable registry index, is not independent identity evidence. |
| Git dependency | A full immutable commit revision can identify reviewed source. A branch or movable tag cannot. | Record and review the full commit revision and applicable source/checksum evidence; do not accept a floating ref as a pin. |
| Pinned tarball, if the current toolchain documents/supports it | An immutable URL plus verified digest can identify the fetched bytes. | Record the documented URL and digest, verify them before use, and review unpacked contents. Do not assume `project.lock` covers an undocumented form. |
| Path dependency | It is live local source and is not hashed by `project.lock`. | Review the exact tree/revision and execute it only under the repository trust decision. |
| Vendored dependency | It is a copied source tree. `gos vendor` alone proves neither locked content nor version integrity. | Review vendored contents and retain independent source/revision/checksum evidence. |
| Rust or prebuilt binding dependency | Its Cargo crate/git/path/prebuilt inputs resolve outside `project.lock`. | Require Cargo lock/checksum/full-revision evidence for Cargo inputs, or signed-prebuilt provenance and digest; review native code and its build inputs. |

`gos publish --dry-run` suppresses upload only. It can read and package the
source tree, may access and use a publisher key for signing, and can leave a
temporary archive depending on interruption and temporary-directory settings;
it can also succeed with no configured signature. Before any dry-run or
publication attempt, require explicit publication and key-use authorization, an
approved package-content allowlist, a secret scan, a private restrictive-
permission temporary location, and cleanup verification. Observe a valid
signature; missing signing is a hard stop for publication. Dry-run is neither
publication approval nor proof that no secret would be uploaded.

### Targets and deployment

At the time these docs were checked, Tier 1 listed
`x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu`,
`aarch64-apple-darwin`, and `x86_64-pc-windows-msvc`; Tier 2 listed the
Linux-musl AOT targets `x86_64-unknown-linux-musl` and
`aarch64-unknown-linux-musl`. Intel macOS is artifact-only, and several
Wasm/RISC-V triples may be registered but are unsupported. This matrix changes:
re-check the live docs, the release matrix, and the local toolchain for every
deployment rather than treating this list as evergreen.

Native output is an ELF/Mach-O/PE binary linked with the Gossamer runtime; the
runtime/deployment details and static-versus-dynamic requirements still depend
on target and build setup. Build and smoke-test the exact release artifact in
the target environment. For checked-in CI/release automation, publication, or
artifact provenance, load
[`ci-release-engineering`](../ci-release-engineering/SKILL.md). For Docker/OCI
or Compose implementation, load
[`container-engineering`](../container-engineering/SKILL.md); do not copy an
example image recipe without confirming base-image, libc/musl, target, user,
port, secret, and health requirements.

In the current browser VM/playground, absent additional host bridges, browser
execution means the bytecode VM itself runs in a Wasm sandbox. It cannot access
filesystem, sockets, processes, SQL, or the listed native facilities, and its
single-threaded goroutines run cooperatively to completion rather than
interleaving like native targets. It is suitable only for behavior compatible
with those constraints.

### Related-skill routing

- Load [`api-design`](../api-design/SKILL.md) when a public service, SDK, CLI,
  serialized, event, or error contract is being designed or changed—not merely
  because Gossamer implements it.
- Load [`observability-engineering`](../observability-engineering/SKILL.md) for
  durable logs, metrics, traces, correlation, alerts, or SLOs; add the security
  skills when those signals can expose sensitive data.
- Load [`documentation-engineering`](../documentation-engineering/SKILL.md)
  when reader-facing docs, `//` documentation tested by `gos test`, examples,
  migration notes, or generated API docs are in scope.
- Load [`random-data-identifiers`](../random-data-identifiers/SKILL.md) when
  IDs, tokens, randomness, fixtures, collision behavior, or deterministic
  seeds are a design concern. Keys, nonces, salts, IVs, tokens, and every other
  security-sensitive random value also require `security-review` and
  `security-review-evidence`.

### Completion evidence

Before handoff, provide:

1. changed `.gos`, manifest, lockfile, binding, test, and deployment files;
2. observed toolchain/feature-status and target-support evidence;
3. exact commands and pass/fail/skipped results for format, check, lint, test,
   race, benchmark (if claimed), and relevant VM/AOT lanes;
4. tests proving changed behavior, error paths, concurrency lifecycle, numeric
   boundaries, or FFI conversions as applicable;
5. dependency/publisher/provenance review status, Rust-binding execution
   authority/outer-isolation evidence where applicable, and sanitized security
   evidence where required; and
6. residual Experimental/pre-1.0, target, browser, ecosystem, or deployment
   risk. Never convert missing evidence into a compatibility, security, or
   performance guarantee.

## References: official Gossamer sources and conceptual context

### Official Gossamer sources

- [Gossamer documentation home](https://gossamer-lang.org/docs/): language
  overview, orientation, and current installation prose; verify it against
  releases before prescribing installation.
- [Language specification](https://github.com/danpozmanter/gossamer/blob/main/SPEC.md):
  normative Stable semantics, lifecycle definitions, syntax, managed references,
  numeric behavior, concurrency, packages, bindings, and target contract.
- [Toolchain reference](https://gossamer-lang.org/docs/toolchain/): `gos`
  subcommands, formatting/lint/testing/benchmarking, package commands, REPL,
  LSP, and MCP details.
- [Running guide](https://gossamer-lang.org/docs/running/): command cheat-sheet,
  pure-VM `--no-jit`, entry handling, and development-watch limitations.
- [Skill card](https://gossamer-lang.org/docs/skill_card/): concise agent-facing
  language/toolchain orientation and project layout.
- [Memory model](https://gossamer-lang.org/docs/memory/): RC, `Weak<T>`,
  cross-tier cycle behavior, alias semantics, and arenas.
- [Supported targets](https://gossamer-lang.org/docs/supported_targets/):
  evidence-tiered target matrix and unsupported-target caveats; re-check per
  release.
- [WebAssembly](https://gossamer-lang.org/docs/wasm/): browser VM sandbox,
  cooperative browser goroutines, and no standalone Gossamer-to-Wasm output.
- [Writing libraries](https://gossamer-lang.org/docs/libraries/): manifest,
  lockfile, modules, registries, publisher trust, and publishing workflow.
- [Security](https://gossamer-lang.org/docs/security/): upstream security posture
  and stated gaps; it is not a substitute for application security review.
- [Lints](https://gossamer-lang.org/docs/toolchain/lints/): current lint IDs and
  explanations; use the installed toolchain to confirm availability.
- [Comptime](https://gossamer-lang.org/docs/language/comptime/): compile-time
  evaluation, `typeInfo`, reflection-driven code, and `codegen!` limits.
- [Top-level statements](https://gossamer-lang.org/docs/language/top_level_statements/):
  implicit-main and entry-file rules.
- [Codegen ABI](https://gossamer-lang.org/docs/codegen_abi/): generic codegen and
  the rejected 128-bit types.
- [Deployment guide](https://gossamer-lang.org/docs/deployment/): release AOT,
  target, container, race-detector, reproducibility, and rollout caveats.
- [Upstream repository](https://github.com/danpozmanter/gossamer): current source,
  release workflow pointers, typed Rust-binding examples, maturity statements,
  and release assets.
- [Latest release API](https://api.github.com/repos/danpozmanter/gossamer/releases/latest):
  current release tag and assets; query it at decision time, never hard-code an
  observed version as current.
- [Editor support](https://github.com/danpozmanter/gossamer-editor-support):
  editor integrations, grammars, and their separately versioned support level.

### Independent conceptual context—not Gossamer documentation

- [Swift Automatic Reference Counting and weak references](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/):
  contextualizes ARC and cycle-breaking comparison only; it does not define
  Gossamer semantics.
- [Bacon and Rajan, “Concurrent Cycle Collection in Reference Counted Systems”](https://doi.org/10.1007/3-540-45337-7_12):
  explains the general reference-counting cycle problem and algorithmic context
  only; it does not establish Gossamer implementation lineage, performance, or
  pause behavior.
- [Cranelift](https://cranelift.dev/): defines general JIT/AOT compiler-backend
  terminology only; it does not establish Gossamer target support or
  performance.

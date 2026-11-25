---
name: rutis-new-runtime
description: Use when adding support for a new plugin language or platform to rutis — "add a runtime", "support Kotlin/Swift/Ruby/… plugins", writing a new leaf SDK, or making an existing runtime work remotely. Covers whether to do it at all, the design doc, the framework constraints, the decisions every runtime must state (artifact model, reentrancy and capabilities, channels, method enumeration, distribution), the runtime contract, and the checklist of places in the rutis repository a runtime touches, based on how Bun and Go were added. Self-contained; reference material is in references/.
---

# Adding a language runtime to rutis

rutis (https://github.com/arcships/rutis) has a Rust core; plugins in other languages connect through **runtimes**. This skill does not depend on the rutis documentation; everything it refers to is in `references/`:

| File | Contents |
| --- | --- |
| `references/principles.md` | rutis design principles and how to decide whether a capability belongs |
| `references/plugin-api.md` | The plugin API shared by all languages (what plugin authors see) |
| `references/runtime-contract.md` | What a runtime implements: frames and channels, handshake and capabilities, `mount`, control operations, values, events, manifests, conformance tests |

The key idea: the rutis paradigm (dependency gating, lifecycle, configuration reconciliation) is **implemented once, in the Rust core**. A runtime and its SDK are a thin leaf layer that only connects one language's plugins. If you find yourself implementing the paradigm again in the new language, you are going the wrong way.

## 0. Decide whether to do it

Using the criteria in `references/principles.md`:

- What ecosystem does it bring? A runtime is added for an ecosystem, not to have one more language.
- Is there a concrete user? If not, wait — Go and the desktop Kotlin/JVM runtime were both "when there is a need".
- Does an existing runtime already cover it? (TS plugins already run on Node and Bun.)

## 1. Design doc first, code second

- In the rutis repository write `docs/design-<language>-runtime-<date>.md` and `.en.md` (the Chinese one is authoritative). Structures to follow:
  - a language compiled into programs: https://github.com/arcships/rutis/blob/main/docs/design-go-runtime-2026-10-10.en.md
  - a language that loads packages by name: https://github.com/arcships/rutis/blob/main/docs/design-bun-runtime-2026-10-09.en.md
  - a language with app hosting: https://github.com/arcships/rutis/blob/main/docs/design-swift-sdk-2026-10-12.en.md
- Settle the decision table; leave no "to be decided". Where a default is obvious, take it and state why.
- Include a "departures from the master plan" section. When merging, update the multi-language master plan's milestones and §9 (reentrancy progress).

## 2. Framework constraints

| Constraint | Meaning |
| --- | --- |
| Leaf plugins | The SDK offers only `define` (`inject`, optional `provides` with method shapes, config schema, `apply`; an undeclared `ctx.provide` is announced with its public methods, all `async`: `rows.announce` in the contract), `ctx.use` / `ctx.provide` / `ctx.effect` / `ctx.on` / `ctx.emit` (from rutis 0.13 also `parallel` / `serial` / `waterfall` / `bail` / `filter`: contract §6), cancellation and errors. No child plugins, event trees or local dependency graphs |
| rutis drives | The runtime does not decide whether dependencies are met, start order or restart policy; every `inject` is gated by rutis (feature `leaf`) |
| One plugin API | Matches `references/plugin-api.md`: declarations, ctx, lifecycle, cleanup order, deadline, value rules, plugin API version (currently 2) |
| Platform-language implementation | The runtime and SDK are written entirely in that language, **with no Rust dependency** (no FFI or native extension bridging to rutis) |
| Both directions | Local channels are required; for remote use implement both `listen:` and `dial:` |
| Stay out of business logic | Platform foreground/background, devices, identity and storage do not belong in a runtime |
| Tests are the contract | Pass the Rust-side conformance tests in the rutis repository, not just your own unit tests |

## 3. Decisions every runtime must state

| Decision | Options and how to choose |
| --- | --- |
| Artifact model | **Load by name**: one runtime process loads several installed packages (Node, Bun, Python); rows are `<prefix>:<module>`. **Compiled program**: plugins are built into an executable that describes itself with `--rutis-manifest` and is started on demand (Go; Swift on macOS reuses this machinery). **App hosting**: plugins are built into an app that connects to rutis (Swift / Kotlin apps) |
| Row prefix | Must not collide with existing ones: `py`, `bun`, `go`, `swift`, `kt`, … |
| Execution model | One execution unit per incoming call (thread, goroutine, Task, virtual thread) makes the runtime reentrant; the reader thread only parses frames and never runs plugin code |
| Capabilities | Declare `reentrant-sync` and `sync-stack` honestly, per `references/runtime-contract.md` §2, and mark synchronous calls with `sync: true`; otherwise they are outside wait-cycle detection |
| Channels | Local: `fd:3`, dialing back to a socket path, `tcp:127.0.0.1:<port>` (used on Windows); dial back when the language cannot take an inherited fd. Remote: `listen:wss://` and `dial:wss://` |
| Method enumeration and schema | Derive them where the language has reflection (Go, Python); otherwise use an explicit method table and a hand-written schema (Swift, Kotlin) |
| Distribution | The language's standard package channel (npm, PyPI, Go modules, SwiftPM, Maven Central); versions follow the rutis release train |

## 4. The runtime contract

All of it is in `references/runtime-contract.md`. The fastest way to get the behavior right is to read an existing implementation alongside it:

- Python: https://github.com/arcships/rutis/tree/main/python/rutis/rutis (`peer.py`, `runner.py`, `__main__.py`, `websocket.py`)
- Go: https://github.com/arcships/rutis/tree/main/go/rutis (`serve.go`, `listen.go`, `runtime.go`, `plugin.go`)
- Bun: https://github.com/arcships/rutis/tree/main/bun/rutis-bun/src

## 5. What changes in the rutis repository

Compiled from the files Bun (arcships/rutis#200) and Go (arcships/rutis#227) actually changed.

**Language side**
- [ ] `<language>/…`: session layer, SDK, runtime entry point, test helper that runs the real runtime under `rutis-host test` (like Go's `rutistest`, Python's `rutis.testing`)
- [ ] A conformance entry point for the Rust tests to start

**rutis-bridge**
- [ ] Nothing in its code: the bridge knows no language and has no language feature
- [ ] Tests: `tests/runtime_conformance.rs`, `tests/session_matrix.rs`, `tests/<language>_runtime.rs`; for remote use `tests/websocket_conformance.rs` (and `dial_conformance.rs` for dialing out)

**rutis-loader**
- [ ] Load by name: nothing to add; `runtime::SessionResolver` resolves `<runtime name>:<plugin>` on the runtime's session. Compiled program: `src/runtime/<language>.rs`, a `BinaryLanguage` whose `launch` returns the `Launcher`, reusing Go's manifest machinery
- [ ] Compiled program only: its `mod` line in `src/runtime.rs` and a feature in `Cargo.toml` (`<language> = ["binary"]`, like `go` and `swift`); load by name needs no feature (`runtimes` covers it)
- [ ] Tests: `tests/<language>_rows.rs`, `tests/multilang_<language>.rs`, `tests/instance_<language>.rs`, `tests/leases.rs`

**rutis-host**
Every local language is one entry in a registry (arcships/rutis#230): `config.rs`, `host.rs`, `new.rs`, `project.rs` and `main.rs` loop over it and need no edit. Read https://github.com/arcships/rutis/tree/main/crates/rutis-host/src/languages first: `node.rs` (load by name) or `go.rs` (compiled program).
- [ ] `src/config.rs`: a `runtimes.<language>` field in `Runtimes` and its settings type (this is the `rutis.json` format; the persisted-fixture tests guard it)
- [ ] `src/languages/<language>.rs`: one type implementing the `Language` trait: its `runtimes` key; `rebase`/`merge` of its settings; how its rows are named (`rows`); `runtime`, which finds the package or interpreter, runs the preflight check of its version and returns the `connect::SpawnPlugin` (`rutis-host/spawn`: `SpawnPlugin::new(<runtime name>, launcher(…), anchor)`, with `launcher` in the same file returning the `rutis_bridge::runtime::Launcher`: command, working directory, how the channel is handed over; `Launcher::start` passes `--id <runtime name>` and the anchor as the last arguments, and the process is the far end of a session; its rows resolve through `SessionResolver`) (a compiled-program language with one runtime per binary overrides `start` instead, as Go does); `new --lang` names, template and next steps; `dev`: how a project is recognized (`is_project`, `project_file`) and the rows that run it (the host never compiles; it only runs the project's own build)
- [ ] `src/languages/mod.rs`: its `mod` line and its line in `LANGUAGES` (the order messages list languages in; the host starts them in reverse, so Node, whose resolver takes bare npm names, stays first)
- [ ] `src/main.rs`: only the `USAGE` help text names the languages. A compiled-program language that rebuilds in `dev` or lists its binaries in `check` follows Go there (`host.go`, `project::GoDev`)
- [ ] `templates/<language>/`: plugin, tests, `rutis.dev.json`, publish workflow

**Release and CI**
- [ ] `.github/workflows/ci.yml`: a `runtimes-<language>` job; `release.yml`
- [ ] `scripts/train.mjs`: version file and package coordinates

**Documentation (both `.md` and `.en.md`)**
- [ ] `docs/guide/<language>-plugin.md`; a column in `docs/guide/plugin-api.md`; `docs/guide/rutis-host.md`; `docs/guide/nodes.md` for remote use
- [ ] The package table in the READMEs; toolchains in CONTRIBUTING
- [ ] The multi-language master plan: milestones and §9

## 6. Phases (the Go / Swift rhythm)

1. Merge the design doc.
2. Session layer and conformance entry point: pass `runtime_conformance`.
3. Runtime contract, SDK and Rust wiring: pass `<language>_runtime`, `<language>_rows` and the new `multilang` column; all existing tests stay green.
4. Developer workflow: `new`, `dev`, `check`, template, publishing.
5. Remote: `listen:` and `dial:`, passing `websocket_conformance` and `dial_conformance`. Making an existing runtime remote changes nothing on the runtime side beyond these channels; the rutis side needs no per-language code: it writes a `rutis-host/dial` row (the runtime listens; rows `<row id>:<plugin>`) or a `rutis-host/listen` row (the runtime dials in), with the token `RUTIS_TOKEN_<row id>` (rutis 0.19; `runtimes.remote` and its `language` are gone).

## 7. Common mistakes

| Mistake | Instead |
| --- | --- |
| Implementing dependency waits, retries or start order in the SDK | Leave gating to rutis; the SDK only carries out `rows.load` / `unload` |
| Embedding Rust through FFI to avoid implementing the protocol | Implement it in the platform language; conformance tests keep it consistent with the others |
| Omitting or guessing capabilities | Declare `reentrant-sync`, `sync-stack` according to the execution model |
| Running plugin code, or bridging sync calls, on the reader thread | One execution unit per incoming call |
| Having the host compile plugin code | `dev` runs only the project's own build; `run` runs only ready-made artifacts |
| Forwarding leaf events across processes yourself | Up to 0.12, events stay in the runtime process (host → runtime only through `emits`). From 0.13 every listener registers with the host automatically and emissions go through it when needed (contract §6); a runtime never forwards events on its own |
| Writing docs in only one language | Keep `.md` and `.en.md` in step |
| Running only your own unit tests | The Rust-side conformance tests are the contract |

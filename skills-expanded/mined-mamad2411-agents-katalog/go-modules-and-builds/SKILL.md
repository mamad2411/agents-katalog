---
name: go-modules-and-builds
description: Use when Go changes affect imports, module or workspace resolution, supported toolchains, build constraints, generators, embedded assets or source-release inputs. Skip local behavior changes that leave dependency and build inputs unchanged.
---

# Go modules and builds

Make the affected deliverable build in its supported context. A successful workspace build proves only that workspace's selected graph and available inputs.

Read the affected modules, workspace, build/release commands and support policy. Identify which modules ship independently, the supported Go versions and build variants, and which files arrive in a fresh source snapshot. Use these facts to choose checks; avoid imposing a new repository layout, dependency policy or release process.

## Resolve the module that ships

A workspace combines requirements and checksum information from its modules. A companion module can supply a newer dependency API or checksum that the changed module lacks on its own. Local replacements can similarly hide the published dependency's behavior.

When an independently usable module changes imports or requirements, reconcile its metadata in that module with the workspace disabled, normally using `GOWORK=off go mod tidy`. Inspect the resulting requirements and sums, then run its relevant tests/build with `GOWORK=off`. Preserve intentional requirements, supported Go versions and vendoring policy; investigate surprising graph changes rather than accepting them mechanically. A module with no external dependencies need not have a `go.sum`.

For a separately consumed library, exercise a small consumer outside the workspace when resolution or import compatibility changes. Replace only the library under test with its local candidate; resolve its dependencies as consumers would. Dependency-module replacements and exclusions do not propagate to consumers. Do not copy development replacements into the consumer to make it pass. Keep module-as-main verification distinct from downstream installation: a consumer maintains its own sums and may succeed even when the library's standalone tests fail. `go.sum` authenticates content; it does not lock the selected graph.

## Honor supported build inputs

Check compatibility with the actual supported Go toolchain, using `GOTOOLCHAIN=local` when proving that version. A newer compiler plus an older `go` directive does not exercise an older implementation selected by release build tags. Inspect affected constraints and filename suffixes; update each supported path and choose relevant tag/OS/architecture checks. Distinguish cross-compilation from executing target tests. Keep minimum-version changes deliberate, rather than raising support for a convenient helper.

For generated or embedded inputs, follow the project's source and release path in a disposable clean copy. Confirm required files are shipped or recreated by its documented generation step with available tools and declared inputs. A warm checkout's ignored outputs can conceal missing source-release assets. Exercise affected generated variants and check that a valid input change reaches their output; ordinary `go build` does not run `go generate`. Choose committed outputs or build-time generation from the project's contract, without adding either universally.

Report which module/workspace, toolchain and build variants actually passed, and any unavailable checks. Compilation, executable behavior, repeatable dependency resolution and byte-identical artifacts are different claims.

Go semantics: [modules](https://go.dev/ref/mod), [toolchains](https://go.dev/doc/toolchain), [build constraints](https://pkg.go.dev/cmd/go#hdr-Build_constraints), [generation](https://go.dev/blog/generate).

# AGENTS.md — Diapasón

> Canonical instruction file for **every** AI agent working in this repo (Claude Code, Codex,
> Cursor, Copilot, Gemini CLI, Aider, …). `CLAUDE.md` imports this file. Do not duplicate content
> here that lives in `docs/` — link to it. **Hard budget: 200 lines.**

## 1. What this is

Diapasón is a production instrument **tuner + metronome** for Android and iOS (phone + tablet).
Flutter owns the UI; **Rust owns all audio and DSP**. Offline-first, zero telemetry by default.

- Product scope & requirements → `docs/PRODUCT_SPEC.md`
- System architecture → `docs/ARCHITECTURE.md`
- Everything else → `docs/README.md` (documentation map, start here when lost)

## 2. Session protocol (non-negotiable)

**At session start — run `just session-start`, then read, in order:**
1. This file.
2. `docs/agents/STATE.md` — the current truth: milestone, WIP, blockers, next action.
3. The active task file named in STATE.md (`docs/agents/tasks/T-###-*.md`).
4. Only the reference docs the task points to. Do not bulk-read `docs/`.
5. Reconcile STATE.md and the task files with what `session-start` printed (merged or open PRs,
   unmerged branches, red checks, open tasks whose PR merged). Those change between sessions;
   report every contradiction before starting work.

**At session end — write, in order:**
1. Update the task file: check off acceptance criteria, record deviations.
2. Rewrite `docs/agents/STATE.md` (it is a *snapshot*, not a log — keep it under 120 lines).
3. Append one entry to `docs/agents/journal/` (`YYYY-MM-DD-slug.md`, template in that folder).
4. Any decision that closes off an alternative → new ADR in `docs/adr/` (never edit a decided ADR;
   supersede it).
5. Run `just verify`. Do not end a session on red without saying so in STATE.md.

Rationale and the full memory model → `docs/agents/CONTEXT_SYSTEM.md`.

## 3. Golden rules

1. **Plan before code.** Non-trivial work starts as a task file with acceptance criteria. If no task
   file exists for what you are about to do, write one first (`docs/agents/tasks/TEMPLATE.md`).
2. **`just verify` is the gate.** It must pass before you claim anything is done. Never weaken a
   lint, skip a test, or add `// ignore:` / `#[allow]` to get it green — fix the cause or escalate
   in STATE.md. The one audited exception is lossy numeric casts in `dsp::convert` (`adr/0018`);
   `docs-check` enforces both.
3. **Never invent an API.** If unsure of a crate, package, or platform API, check the pinned docs or
   say so in STATE.md under "Open questions". Guessing wastes more of my time than asking.
4. **Small, reversible commits.** Conventional Commits, imperative mood, one concern each,
   `refs T-###` in the body. `main` is protected: work lands only through a PR with all six CI
   jobs green, **rebase-merged** (linear history, each commit kept). No one can bypass the ruleset.
5. **Respect the layer boundaries** in §5. Most damage in this repo will come from crossing them.
6. **One fact, one home.** Duplicated documentation rots. Link instead of copying.
7. Files are code: prefer editing an existing file over creating a parallel one. No `*_v2.dart`,
   no `utils.dart` dumping grounds.

## 4. Commands

`just` is the single entry point for humans, agents, and CI. Never hand-roll a command an agent
might need to repeat — add a recipe.

| Command | Does |
|---|---|
| `just setup` | Toolchain check, `dart pub get` across the workspace, codegen |
| `just verify` | **The gate:** format + lint + test + codegen-drift check, Dart *and* Rust |
| `just gen` | flutter_rust_bridge + build_runner + Pigeon + l10n codegen |
| `just test-rust` / `just test-dart` | Focused test loops |
| `just bench` | Criterion DSP benches (fails on regression vs. baseline) |
| `just run android` / `just run ios` | Launch the dev flavor |
| `just fix` | Auto-fix formatting and trivial lints |

Full list: `just --list`. If a recipe is missing, add it in the same PR.

## 5. Boundaries (the rules that keep this codebase clean)

**Dependency direction is one-way. Nothing below may depend on anything above it.**

```
apps/diapason  →  packages/feature_*  →  packages/core_ui, core_domain, core_platform
                                      →  packages/audio_engine (generated FFI facade)
                                              ↓
          diapason_ffi → session → engine → dsp           (dsp depends on nothing)
                                 → audio_io (platform backends)
```

- `feature_*` packages **never import each other**. Shared code moves down to `core_*`.
- `core_domain` is pure Dart: no Flutter import, no I/O, no plugins.
- `rust/crates/dsp` is pure computation: no allocation in hot paths, no I/O, no platform code,
  no `audio_io` dependency. It must stay testable offline with fixture buffers.
- `diapason_ffi` (`packages/audio_engine/rust`, where cargokit builds it) contains **no logic** —
  only the flutter_rust_bridge API surface and type mapping. Business rules live in `session`/`engine`/`dsp`.
- Dart never touches audio buffers. Dart sends commands and receives ~30 Hz state snapshots.
- No `dart:io`/plugin calls inside `core_ui` widgets; inject via `core_platform` interfaces.

## 6. Real-time audio rules (violating these ships audible bugs)

The audio callback thread is sacred. Inside it, and anything it calls:

- **No** heap allocation, `Vec::push`, `String`, `format!`, `Box`, or collection growth.
- **No** locks, `Mutex`, channel that can block, syscall, file, or log statement. The audited
  exceptions are the platform audio calls a backend must make and `clock_gettime` (`adr/0020`).
- **No** panics: release builds abort on one, and nothing catches it (`adr/0021`).
- Communicate with the rest of the app only through the lock-free SPSC ring buffers and atomic
  snapshots defined in `docs/AUDIO_ENGINE.md`.
- Every buffer the RT path needs is preallocated at stream start, sized from the largest supported
  configuration.
- Debug builds assert this with `assert_no_alloc`; tests fail if the callback allocates.

Timing: the **audio clock is the only clock**. Never drive a beat, a countdown, or an animation
from `Timer`, `Future.delayed`, or a Dart `Ticker` alone — derive it from the sample position the
engine reports. Details and the drift-free scheduler design → `docs/AUDIO_ENGINE.md`.

## 7. Conventions

**Dart** — Flutter and Dart pinned in `tools/versions.env` (`adr/0011`), which `just doctor`
enforces; `.fvmrc` must agree with it. Riverpod 3 (code-gen only, no manual
`Provider` globals). `go_router` typed routes. Feature-first packages, `lib/src/**` private with a
single public barrel. Immutable state classes with `copyWith`. No `setState` in feature code.
Widgets under ~150 lines; extract painters and sub-widgets. Lints: `analysis_options.yaml` at root;
`riverpod_lint` runs as a first-party analyzer plugin, so `dart analyze` is the only lint pass
(`adr/0014`). Public API of `core_*` packages needs doc comments.

**Rust** — edition 2024, MSRV pinned in `rust-toolchain.toml`. `#![forbid(unsafe_code)]` everywhere
except `ffi` and `audio_io`, where every `unsafe` block carries a `// SAFETY:` comment.
`thiserror` for library errors, no `unwrap()` outside tests and `main`. `clippy::pedantic` on
`dsp`. Public items documented; doctests count as tests.

**Naming** — `snake_case.dart` files, `T-###` task IDs, ADR files `NNNN-kebab-title.md`,
branches `feat/T-012-strobe-ring`, commits `feat(tuner): add strobe ring painter`.

**Testing** — see `docs/TESTING.md`. Rust DSP changes require a fixture-based accuracy test.
UI changes to `core_ui` require a golden. Never assert on wall-clock timing in a test.

## 8. Never do this

- Never commit generated files that `just gen` produces, except where `.gitattributes` marks them
  as checked-in (frb bindings are checked in — regenerate, never hand-edit).
- Never add a Dart package that bundles its own audio I/O, or a plugin that duplicates something
  Rust already owns.
- Never add analytics, ad SDKs, or any network call. This app makes zero network requests.
  If a task seems to need one, stop and flag it.
- Never bump `targetSdk`, `minSdk`, deployment target, or a pinned toolchain version as a side
  effect of another change — that is its own task and its own ADR.
- Never edit `docs/adr/*.md` that are marked Accepted, or rewrite journal entries.
- Never `git push --force`, rewrite main's history, or commit secrets/keystores/`*.p8`/`*.p12`.

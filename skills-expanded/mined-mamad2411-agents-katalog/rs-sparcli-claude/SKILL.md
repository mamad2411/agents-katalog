# CLAUDE.md – sparcli (Rust)

Requirements for all future sessions in this project. In case of conflict, this file takes precedence over conventions, but not over explicit user instructions.

## What is this?

`sparcli` is a **lightweight, platform-independent** toolkit (macOS, Windows, Linux) for **styled CLI output** and **interactive single-input widgets** – a native Rust port of the C library `sparcli`. Guiding principle: lean, for small CLI tools. No async, no ratatui, minimal footprint.

- **Foundation:** custom renderer on `crossterm` (no ratatui).
- **API feel:** ratatui-familiar vocabulary (`Style`, `Color`, `Span`, `Line`, `Text`, `Modifier`), fluent builder API **and** options struct.
- **Scope:** output complete; input only single widgets (no Form/App/Args/ Serde). Fuzzy only as inline Select.

## Python twin – keep in sync

There is a parallel Python version of `sparcli` at `/Users/cgroening/Developer/Python/libs/sparcli`. On **every change** to this Rust crate, check whether the same change has to be applied to the Python version too (behavior, API, docs, tests) – and **ask the user** whether it should be ported before proceeding.

**Known intentional divergences.** These are deliberate. Do not "fix" them into parity without user sign-off:

- `Date::today()` returns a **UTC** date here (dependency-free, no local-time API in `std`), while the Python port uses the **local** date. Near midnight the `DatePicker`'s default day can differ by one between the two ports.
- Rust exposes a hand-rolled `Date` type; Python uses stdlib `datetime.date` and has no counterpart.
- Rust gates `markup`, `fuzzy` and `pager` behind cargo features and offers a `prelude`; Python always ships everything and re-exports flat.
- `output/box_draw.rs` is `output/box.py` in Python: `box` is a reserved keyword in Rust.
- Rust needs `core/private_file.rs` for owner-only file creation; Python gets the same guarantees from `tempfile.mkstemp` and keeps no counterpart module.
- Rust decodes keys via `crossterm`, so it has no equivalent of Python's `input/keydecode.py`.

## Architecture (separate layers strictly, §2.6/§7.2)

- `core/` – foundation: style, text, markup, theme, border, geometry, width, terminal, render, `command` (quote-aware splitting and env resolution for `$EDITOR`/`$PAGER`), `inplace` (in-place redraw engine), `private_file` (owner-only file creation). No widget logic.
- `output/` – printable widgets, implement `Renderable`. `box_draw` holds the frame geometry shared by `Panel` and `Alert`.
- `input/` – interactive prompts via `EventSource` (DI) + `prompt` (loop driver and the `run_interactive` terminal handover) + `line_edit` (SSOT for text input) + `selection` (SSOT for list cursor and scroll window).
- Dependency direction: `output`/`input` → `core`. Never cyclic, and `input` never reaches into `output` – that is why `InPlace` lives in `core/`, as it does in the Python port.
- **Unified theme** in `core/theme.rs` applies to input AND output.

### One helper per rule

Where a rule applies in more than one widget it lives in exactly one place. Do not reimplement these per call site:

- `core::width::truncate` / `truncate_line` and the `ELLIPSIS` constant for `…` clipping.
- `input::selection::SelectionCursor` for cursor movement and the scroll window (wrap on step, clamp on page and on `Home`/`End`).
- `input::prompt::run_interactive` for the TTY check, the `TerminalGuard` and the event source.
- `input::shortcut::intercept` for the `?` help overlay and shortcut dispatch.
- `core::command::resolve_from_env` / `program_and_args` for external commands.
- `input::editor::edit_text_suspended` for the `$EDITOR` handover.

## Output streams (§1.6)

sparcli is a library, not a CLI program, so §1.6 binds it only through what it prints:

- Payload goes to **stdout**, progress indicators to **stderr**, and progress draws only when stderr is a terminal. `InPlace::progress()` is the seam.
- `print`/`print_to` do **not** truncate when stdout is not a terminal: they lay out at `UNCONSTRAINED_WIDTH`, because clipping to an invented width loses piped data silently. An explicit `render(max_width)` still truncates – that width is the caller's decision.
- §1.7 (TUI) rules – scrollbar on overflow, a `?` overlay in every prompt, `Ctrl+Q` – are deliberately **not** implemented. They govern terminal UIs, not a CLI output library.

## Dependencies & Feature Flags

- Default (always): `crossterm`, `unicode-width`, `thiserror`, `log`.
- Opt-in: `markup`, `fuzzy` (`nucleo-matcher`), `pager`.
- New dependencies **must be agreed with the user beforehand** (§7.7).
- Established crates with `// https://crates.io/crates/<name>` above the `use`.
- **Logging:** only the `log` facade and only as `warn!`/`debug!` at places where a `Result` would otherwise be silently swallowed (e.g. terminal restore in the `TerminalGuard`, history save/load, temp cleanup). No `error!` logs – real errors come back via `SparcliError` (no double logging); do not ship a logger/ backend (the app decides); nothing in hot paths/render loops.

## Error Handling (§7.3) – very important, robust & long-lived

- No `unwrap()`; `expect()` only at provably infallible places with a justification. No `panic!` in normal operation.
- Errors via `Result<T, E>` + `?`. Library errors as a `thiserror` enum (`SparcliError`), foreign errors via `#[from]`.
- Input prompts return `Outcome<T>` (`Submitted` / `Cancelled`).
- `TerminalGuard` (RAII) restores the terminal on drop/error/panic.
- Defensive: safeguard inputs/edge cases, prefer to fail in a controlled way.

## Clean Code (§1, §2.5) – key points

- SRP for functions/structs; keep functions small.
- **≤ 3 function parameters**; more → bundle into a struct/opts.
- Early returns (guard clauses), max. 2 nesting levels.
- SLAP (one abstraction level per function); no flag arguments.
- No magic numbers/strings → named constants.
- Strong typing: `enum`s instead of magic strings, `struct`s instead of tuples.
- Lookup tables instead of large `match` for constant mappings.

## Style & Tooling

- Edition 2024. `cargo fmt` (rustfmt.toml: max_width 80).
- `cargo clippy --all-targets -- -D warnings` must be clean.
- 80-character code lines; straight quotes.
- **No em dash** as a dash: in code files use the hyphen, in `.md` files use the en dash `–`.
- rustdoc on every public item, module `//!`; `# Examples`/`# Errors`/ `# Panics` where applicable; `#![warn(missing_docs)]`.

## Appearance (§7.10)

- Muted appearance, one accent tone, `dim` for secondary text.
- Default border `Rounded`; truncate overflow with `…`.
- Glyphs in two tiers (Unicode + ASCII fallback), selectable via the theme.
- Selection lists navigate cyclically; respect `NO_COLOR`/non-TTY.

## Tests (§2.8/§7.8) – mandatory

- Unit tests in `#[cfg(test)] mod tests` per file; integration in `tests/`.
- Test names describe the expected behavior; fakes over mocks.
- Output: render to `Rendered` and check content/style (no TTY).
- Input: drive headless via an `EventSource` fake (scripted keys).
- **Run all tests after every change** (`cargo test`).
- Doctests in `# Examples` count as tests and must run.

## Docs/Maintenance

- On changes, keep README/rustdoc and tests in sync.
- Remove dead/commented-out code; fix the cause instead of the symptom.

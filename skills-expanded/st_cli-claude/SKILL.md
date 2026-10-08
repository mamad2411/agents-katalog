# stcli — SillyTavern in the terminal

Python reimplementation of SillyTavern as a CLI, REPL, and TUI over one core.
Plan: `docs/PLAN.md` (stage IDs are permanent). Current stage: S13+S14 — CLI front-end + ST import/export (S0–S12 Done; next fan-out: S13+S14, S16, S18, S19, S21, S34).

## Layout

- `SillyTavern/` — reference clone. READ-ONLY. Never edit, never run.
- `SILLYTAVERN_REPO_MAP.md` — index into the clone. Verify a path against the tree before relying on it.
- `stcli/` — the app, src layout (`stcli/src/stcli/`)
- `docs/PLAN.md` — stages, dependencies, status
- `docs/skills/chara-card/SKILL.md` — card and lorebook reference. Read before any card, lorebook, or prompt-assembly work.
- [`../charaterm/` — prior work. Reuse policy: dependency / port / reference only]

## Stack

- Python [3.12+], [uv], [ruff], [pytest]; type hints on all public functions; [asyncio for backends and streaming]
- TUI: [Textual]. REPL: [prompt_toolkit]. CLI: [typer / click / argparse]
- Config: [TOML] in [~/.config/stcli/], overridable with [`STCLI_CONFIG`]; themes, layouts, keybindings are user files
- Must run on Arch Linux and on Termux: prefer pure-Python dependencies. Ask before adding any dependency.

## Architecture rules

- `core/` (models, config, module registry, prompt assembly, storage adapters) depends on no module.
- Everything else is a module under `modules/<name>/` registered through the registry. Modules import core only, never each other — use core hooks/events.
- Every optional stage is a module behind a config feature flag. The app must start and chat with all optional modules disabled.
- ST data formats live only in `core/storage/` adapters. [Read/write in place — never write a file ST can't read back.]
- No HTTP server or browser component unless a stage explicitly adds one.

## Parity rules

- Parity = feature parity from the user's seat, not ST API or code parity.
- Data compatibility: [decision from the plan]
- Browser-bound features are translated per the stage's scope notes or excluded. Never silently dropped.
- When ST behavior is ambiguous, read the ST source the stage cites and match it. Record deviations under the stage's Definition of Done.

## Card handling

- Specs in scope: V1, V2 [, V3]. PNG cards carry base64 JSON in a `chara` tEXt chunk [V3: `ccv3` chunk too]; JSON cards are also valid.
- Never drop unknown `extensions` keys on read or write. Namespace ours as `stcli/<key>`.
- Macros (`{{char}}`, `{{user}}`, `{{original}}`) are substituted at prompt-assembly time, never persisted.

## Working agreements

- Work is requested by stage ID: "implement S2.1". Before starting, read the stage entry, its Requires list, and the ST files it cites. Stop and say so if a required stage is not Done.
- A stage is done when its Definition of Done passes. Run the checks and show the output.
- On completion: set Status in PLAN.md, add a one-line changelog entry under the stage, commit as `S2.1: <name>`.
- Never change stage IDs or scope in PLAN.md without asking. Scope changes get a note, not a silent edit.
- Ask before: adding a dependency, changing the config schema, touching files owned by another stage.
- Don't restate ST's design in replies. Lead with what changed and what to run.

## Commands

- Run: [`uv run stcli`]
- REPL: [`uv run stcli repl`]
- Tests: [`uv run pytest`]
- Lint/format: [`uv run ruff check . && uv run ruff format .`]

---
name: design-cli-prototype
description: Design a CLI prototype in chat — command tree, flags, help text, output — iterate, then build
argument-hint: "[cli-name-or-purpose]"
related:
  - follow-devin-global-skills
  - design-tui-prototype
  - design-web-prototype
  - design-html-prototype
  - design-usage-with-me-first
  - update-usage-md
  - follow-create-cli
  - learn-from-cli
  - check-types-definition
  - draw-ansi
  - report
  - ask-me
  - suggest-next-action
  - apply
---

## Goal

Design the CLI's surface and UX together with the user `in chat only` — command tree, flags, `--help` output, result/exit-code contract, error wording — iterate until the user agrees, then hand off to `/follow-create-cli` to implement it for real

## Scope

Use when the shape of a CLI must be agreed before any code is written — new tool, new subcommand set, redesign of an existing surface

- Draft in chat only — `do not create files` and do not scaffold a project until the user confirms
- A web-based CLI docs/explorer prototype (SolidJS + Vite) → `/design-web-prototype` (see its `references/cli-explorer-spec.md`)
- A full-screen terminal UI (panels, focus, key bindings) → `/design-tui-prototype`
- Single-file HTML mockup of unrelated UI → `/design-html-prototype`

Core principle: humans read the CLI visually, agents consume it structurally — both must be designed here

## Execute

### 1. Load Skills

> Goal: design on top of the conventions that already exist, not from memory

1. Run `/follow-devin-global-skills` — list global (`%APPDATA%\devin\skills`) and project (`.devin/skills/`) skills matching the CLI domain
2. Read the ones this design must obey: `/follow-create-cli` (+ `/follow-create-bun-cli` / `/follow-create-rust-cli`), `/follow-tool-usage`, `/learn-from-cli`, `/follow-tool-devin-cli` when the target is an agent-facing CLI
3. Project `AGENTS.md` → read its `### Skills` section; note the conventions (naming, output, exit codes) the project already follows before proposing new ones

### 2. Clarify Intent

> Goal: Know what the CLI must do and for whom

1. Run `/suggest-next-action` to list the usual CLI shapes (single command + flags, verb/noun subcommands, TUI hybrid, REPL)
2. Run `/ask-me` about: audience (human/CI/agent), install path (bunx/cargo/npm/binary), scriptability, naming style
3. Summarize requirements with `/report table` columns: `No.`, `Requirement`, `Priority`

### 3. Ground The Surface

> Goal: Design from real data, not guesses

1. A real CLI already exists → extract its current surface per `/learn-from-cli` (`--help`, subcommands, machine-readable output) before proposing changes
2. Config/flags come from real types → inspect them with `/check-types-definition` (name, type, options, default)
3. Never invent flags that contradict the existing surface — mark every entry as `existing`, `changed`, or `new`

### 4. Draft The Command Model In Chat

> Goal: one agreed command/flag contract, written in chat

1. Command tree as a numbered/indented list: top-level commands, subcommands, aliases, hidden/dev-only entries
2. Flags table per command via `/report table`: `Flag`, `Alias`, `Type`, `Default`, `Required`, `Description`
3. Sketch the real `--help` output in a ` ```text ` block — exactly what the implementation must render (usage line, sections, examples)
4. Define the output contract: human mode (table/ANSI per `/draw-ansi` rules — uniform box width, ≤ 80 columns), `--json`, `--quiet`, colors-off/`NO_COLOR`
5. Define the exit-code table: `code`, `meaning`, `when`; and success/failure wording with `✓`/`✕` plus a hint line (`Try: ...`)
6. State the non-obvious decisions explicitly: exit codes on partial failure, stdout vs stderr, idempotency, `--dry-run` default

### 5. Iterate

> Goal: converge with the user, not with files

1. Ask for feedback via `/ask-me` — collect it into a checklist before revising
2. Revise in chat per the checklist → re-show only the changed parts (before/after) until agreed
3. Multiple viable designs → `/apply choose` with a recommendation and its trade-off

### 6. Handoff

> Goal: turn the agreed design into a real implementation

1. Run `/report table` to summarize: `No.`, `Section`, `Decision`, `Status`
2. Ask the user to implement now → run `/follow-create-cli` with the chat design as the spec
3. Then design docs: `/design-usage-with-me-first` → `/update-usage-md`; a visual explorer → `/design-web-prototype`
4. Run `/suggest-next-action`

## Rules

- Discuss and draft in chat only — do not create files or scaffold a project until the user confirms
- Always run `/follow-devin-global-skills` first — the project/stack skills decide naming, output, and exit-code conventions; never invent a parallel set
- One responsibility per command; consistent verb style across the tree — pick one and state it
- The `--help` sketch must be implementable as written — never decorative text
- Machine-consumable output is required (`--json`) so agents and CI can read the CLI structurally
- No color-only or hover-only meaning; output must stay readable with `NO_COLOR` and when piped
- Never guess an existing surface — verify with `/learn-from-cli` / `/check-types-definition`
- Do not commit/push automatically
- Always start with `/ask-me` and `/suggest-next-action`

## Expected Outcome

- An agreed CLI design in chat: command tree, flag tables, `--help` sketch, output/exit-code contract, error wording
- The skills read first are listed, and the design follows the conventions they already define — no parallel convention invented
- Every entry marked `existing` / `changed` / `new` with the reason
- A clear path to the real build (`/follow-create-cli`) and docs (`/design-usage-with-me-first`)

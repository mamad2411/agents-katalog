---
name: design-tui-prototype
description: Design a TUI prototype in chat — ANSI layout, panels, keys, states — iterate, then build
argument-hint: "[tui-name-or-purpose]"
related:
  - follow-devin-global-skills
  - design-cli-prototype
  - design-web-prototype
  - design-html-prototype
  - draw-ansi
  - report-uxui
  - follow-create-tui-ratatui
  - follow-lib-native-sdk
  - follow-design-system
  - learn-from-cli
  - check-types-definition
  - report
  - ask-me
  - suggest-next-action
  - apply
---

## Goal

Design a terminal UI (TUI) together with the user `in chat only` — frame anatomy, panels, focus order, key bindings, and every state — sketched with ANSI box-drawing, iterate until the user agrees, then hand off to the real builder (`/follow-create-tui-ratatui` or `/follow-lib-native-sdk`)

## Scope

Use when a terminal app's layout and interaction model must be agreed before writing code — dashboards, explorers, editors, monitors, wizards

- Draft in chat only — `do not create files` and do not scaffold a project until the user confirms
- Command surface (commands, flags, `--help`) instead of a screen → `/design-cli-prototype`
- Browser prototype of the same tool → `/design-web-prototype` / `/design-html-prototype`

Core principle: a TUI has one screen and no scroll of context — density, focus, and keyboard reach are the design

## Execute

### 1. Load Skills

> Goal: design on the conventions that already exist, not from memory

1. Run `/follow-devin-global-skills` — list global (`%APPDATA%\devin\skills`) and project (`.devin/skills/`) skills matching the terminal-app domain
2. Read the ones this design must obey: `/draw-ansi` (box rules), `/report-uxui` (sketch conventions), `/follow-design-system`, and the builder skill for the target stack — `/follow-create-tui-ratatui` (Rust) or `/follow-lib-native-sdk` (native)
3. Project `AGENTS.md` → read its `### Skills` section; reuse the key bindings/terminology the project already uses before inventing new ones

### 2. Clarify Intent

> Goal: Know what the screen must show and do

1. Run `/suggest-next-action` to list the usual TUI shapes (list + detail, dashboard grid, single-pane flow, modal wizard, REPL hybrid)
2. Run `/ask-me` about: primary task, data density, minimum terminal size, mouse support, color depth
3. Summarize requirements with `/report table` columns: `No.`, `Requirement`, `Priority`

### 3. Ground The Data Model

> Goal: the layout comes from real data, not decoration

1. Real source exists (CLI output, API, DB, config) → pull the actual fields per `/learn-from-cli` / `/check-types-definition`
2. List the entities and the fields shown per view, with the sort/filter keys that must exist
3. Decide the 3–5 views worth designing; cut the rest with a stated reason

### 4. Draft The Layout In Chat

> Goal: a sketched frame the implementer can rebuild exactly

1. Draw each screen in a ` ```text ` block with ANSI box-drawing — uniform box width, right edges aligned, ≤ 80 columns, one screen per sketch (rules: `/draw-ansi`; sketch conventions: `/report-uxui`)
2. Label the anatomy: title bar / tabs, main panel, side panel, status bar, help/footer; mark the focused panel
3. Give each region its real content: column headers, row format, counts, truncation markers (`…`), scroll indicators
4. Use `/draw-ansi --fix` when a box is misaligned instead of redrawing by hand

### 5. Define Interaction And States

> Goal: the whole app, not only the happy path

1. Key binding table via `/report table`: `Key`, `Scope`, `Action`, `Destructive?` — keyboard-first, mouse optional, no binding without an on-screen hint
2. Modes and focus order: normal / search / select / confirm; how to enter and exit each; `Esc` always backs out
3. Render every state as its own sketch: loading, empty, partial/error, confirm dialog, help overlay
4. Motion + color policy: frame rate, spinner only where blocking, 16-color-safe palette, no color-only meaning (bold/label carries it)

### 6. Iterate

> Goal: converge with the user, not with files

1. Ask for feedback via `/ask-me` — collect it into a checklist before revising
2. Revise in chat per the checklist → re-show only the changed screens/tables until agreed
3. Multiple viable layouts → `/apply choose` with a recommendation and its trade-off

### 7. Handoff

> Goal: turn the agreed design into a real TUI

1. Run `/report table` to summarize: `No.`, `Screen`, `Decision`, `Status`
2. Ask the user to implement now → Rust terminal app on `ratatui`: `/follow-create-tui-ratatui`; native desktop app from TS + `.native` markup: `/follow-lib-native-sdk`
3. Then design the surrounding surface/docs: `/design-cli-prototype`, `/design-usage-with-me-first` → `/update-usage-md`
4. Run `/suggest-next-action`

## Rules

- Discuss and draft in chat only — do not create files or scaffold a project until the user confirms
- Always run `/follow-devin-global-skills` first — the project/stack skills own box rules, key-binding terminology, and state names; never invent a parallel set
- Box-drawing lives in ` ```text ` blocks only (never ` ```ansi `) — every box uniform width, no distorted borders
- Design to the declared minimum terminal size; degrade gracefully (drop side panel before dropping data)
- Keyboard-complete: every action reachable without a mouse; every hover-equivalent has a visible focus/tap path
- No color-only or glyph-only meaning; `NO_COLOR` and monochrome terminals must stay usable
- Every state (loading/empty/error/confirm) must have a sketch before implementation — no un-designed states
- Density over chrome: no decorative borders, no padding that costs a data row
- Never guess the data model — verify against real source before drawing
- Do not commit/push automatically
- Always start with `/ask-me` and `/suggest-next-action`

## Expected Outcome

- An agreed TUI design in chat: per-screen ANSI sketches, region/content spec, key binding table, modes/focus order, all states drawn
- The skills read first are listed, and the sketch/binding conventions match the ones they already define
- Every decision recorded with its reason — ready as the spec for the builder skill
- A clear path to the real build (`/follow-create-tui-ratatui` or `/follow-lib-native-sdk`)

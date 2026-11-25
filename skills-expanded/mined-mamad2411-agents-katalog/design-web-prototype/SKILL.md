---
name: design-web-prototype
description: Build an interactive web prototype (SolidJS+TS+UnoCSS+Vite) — production quality, not a mockup
argument-hint: "[app-spec-or-domain]"
related:
  - follow-devin-global-skills
  - design-html-prototype
  - design-cli-prototype
  - design-tui-prototype
  - follow-solid-framework
  - follow-lib-solidjs
  - follow-lib-unocss
  - follow-tool-vite
  - follow-design-system
  - learn-from-cli
  - create-files-in-os-temp
  - check-open-ports
  - open-web
  - ask-me
  - report
  - follow-web-standard
---

## Goal

Design + implement an interactive web prototype that genuinely works (not a static mockup) — using SolidJS + TypeScript + UnoCSS + Vite + Modern Web APIs, reusable components, premium developer-tool aesthetic — built in OS temp and opened with `/open-web`

## Scope

Use when you need an interactive web prototype — dashboard, explorer, playground, config UI, data tools, CLI documentation/explorer

- Prototype the CLI/TUI itself (command tree, help text, layout) in chat before building UI → `/design-cli-prototype` / `/design-tui-prototype`
- Plain single-file HTML UI prototype → `/design-html-prototype`
- Production app in a real project → `/follow-solid-framework`, not this skill

CLI explorer variant (typed `Command` schema, Human/Agent modes): [references/cli-explorer-spec.md](references/cli-explorer-spec.md)

## Execute

### 1. Load Skills

> Goal: build on the skills that already exist, not on memory

1. Run `/follow-devin-global-skills` — list global (`%APPDATA%\devin\skills`) and project (`.devin/skills/`) skills matching the target stack and domain
2. Read the matching skills actually used here: `/follow-solid-framework`, `/follow-lib-solidjs`, `/follow-lib-unocss`, `/follow-tool-vite`, `/follow-web-standard`, `/follow-design-system` (plus any project skill that overrides them)
3. Project `AGENTS.md` → read its `### Skills` / `### Architecture` before choosing the layout; verify each skill's `related` exists and its content is fresh per `/follow-up-to-date`

### 2. Clarify Spec

> Goal: Know what the prototype must do

1. Take the domain/spec from the argument or context; unclear → `/ask-me` (number of views, data model, interactions)
2. If a real data source exists (CLI surface, API, config) → pull the real schema in as the source of truth before designing; a real CLI → extract its command surface per `/learn-from-cli`

### 3. Scaffold

> Goal: A ready SolidJS app in temp

1. Run `/create-files-in-os-temp` — create `<temp>/web-proto-<name>/`
2. Scaffold per `/follow-solid-framework`: `bun create vite` (template `solid-ts`) → `bun add -d unocss`
3. UnoCSS config strictly per `/follow-lib-unocss` — `presetWind4` (not `presetUno` — deprecated), current theme keys (`font`, `radius`, `shadow`, `breakpoint`, `ease`, `property`, `spacing` — not the old `fontFamily`/`borderRadius`/`boxShadow`), `presetIcons`, transformers as needed
4. Create the `src/` tree: `data/` (typed schema = single source of truth), `lib/` (logic), `components/`, `routes/`

### 4. Implement

> Goal: a functional app from one typed data source

1. `data/` = typed schema — every view/panel derives from that single schema; never hardcode separate content
2. Reusable SolidJS components per `/follow-lib-solidjs` — `createSignal`/`createMemo`/`createStore`, Context only where justified
3. Interactive elements really work: hover/click inspect, builders, copy, search, navigation — no dead UI
4. If the app has 2 audiences (human/agent) → generate both programmatically from the same schema

### 5. CLI Explorer Variant

> Goal: the prototype target is a CLI — use the canonical schema, not an ad-hoc one

1. Follow `references/cli-explorer-spec.md` for the `Command`/`Argument`/`Option`/`Example` types, component architecture, routing, and error states
2. `data/commands.ts` = typed `Command[]` — the single source every panel derives from; never hardcode docs separately
3. Human Mode: tokenized `CommandSyntax` + `CommandBuilder` (toggle options/args → live command string) + `CommandInspector` + `ExampleTerminal` + `StickyCommandBar`
4. Agent Mode: `AgentMarkdown` + `MarkdownToolbar` — markdown/Raw JSON generated programmatically from the schema via `lib/markdown-generator.ts`
5. `ModeSwitcher` on `?mode=human|agent`; builder state serializes into query params (`?preset=production&port=8080`) so the URL is shareable
6. Routes: `/commands/<name>`, `/plugins`, `/plugins/<name>`, `/presets`, `/presets/<name>`, `/config` — lightweight `lib/` router or `@solidjs/router`

### 6. Apply UX Quality Bar

> Goal: meet the full production-quality bar

1. Visual: dark-first, minimal, dense-but-readable, subtle borders, layered surfaces, strong typography, monospace for code/CLI elements, subtle gradients, restrained shadows — no generic SaaS landing aesthetic (no huge hero, no excessive glassmorphism/rounded cards/illustrations)
2. UnoCSS is ALL styling: reusable shortcuts (`surface`, `code-surface`, `interactive`, `focus-ring`, `muted-text`) + variants (`hover:`/`focus:`/`group-hover:`/`dark:`/`sm:`-`xl:`) — separate CSS only for browser-specific/advanced animations UnoCSS truly cannot do
3. Responsive: 3 breakpoints — desktop full layout, tablet collapse, mobile stacked + bottom nav
4. Accessibility: semantic HTML, keyboard nav, focus states, ARIA, reduced motion, WCAG AA contrast — standards-first (native element before `role`/`aria-*`) per `/follow-web-standard`
5. Microinteractions: fast + subtle + purposeful — copy feedback, transitions, active indicators
6. Theme toggle (if any): smooth transition — no hard swap, per the `/follow-design-system`/`/improve uxui` convention
7. Thai text in the UI → font stack per `/follow-lib-unocss` (`@fontsource-variable/noto-sans-thai` + per-glyph fallback)

### 7. Run And Open

> Goal: the user sees the prototype actually working

1. `bun install` → `bun run dev` per `/follow-tool-vite`
2. Run `/check-open-ports`; if the port conflicts → change the port
3. `/open-web` — verify a clean console and that every route/interaction works
4. Run `/report` summarizing the temp path + URL; if the user asks for changes → edit in the same temp and refresh

## Rules

- Prototypes are written to OS temp only — never write into the project (unless the user orders it)
- Always run `/follow-devin-global-skills` first — the stack skills (and any project `.devin/skills/`) are the source of conventions; never restate or invent config from memory
- Typed data schema = single source of truth — every view derives from it
- CLI explorer variant: the `Command` schema is the source — Human/Agent modes derive from it and Agent Mode markdown is always generated programmatically
- UnoCSS `presetWind4` only — no Tailwind/Bootstrap/large CSS stylesheets; CSS only for what UnoCSS cannot do
- Every hover interaction must have a click/tap equivalent — never rely on hover alone
- Animations fast + subtle — never sacrifice performance for effects
- Follow the canonical skills for every config (`/follow-lib-unocss`, `/follow-solid-framework`, `/follow-lib-solidjs`) — never copy sample configs from external specs that may be stale
- Always use `/create-files-in-os-temp`, `/open-web`, `/check-open-ports`; use `/ask-me` when needed

## Expected Outcome

- Prototype runs on localhost and opens in the browser — every interaction genuinely functional
- The skills read first are listed, and every config/styling choice comes from them rather than from memory
- Styling 100% UnoCSS per the `presetWind4` conventions — reusable shortcuts, no scattering
- No prototype files mixed into the project source

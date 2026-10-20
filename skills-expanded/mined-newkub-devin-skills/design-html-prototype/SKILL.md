---
name: design-html-prototype
description: Create an interactive HTML prototype/mockup from a design brief — single-file, /open-web
argument-hint: "[brief-or-feature]"
related:
  - follow-devin-global-skills
  - design-web-prototype
  - design-cli-prototype
  - design-tui-prototype
  - report-html
  - report-prompt-uxui-web-design
  - visualize-in-web
  - open-web
  - create-files-in-os-temp
  - ask-me
  - follow-web-standard
---

## Goal

Create an interactive design prototype as single-file HTML — rendered per `/report-html` conventions (Tailwind CDN + Vue 3, theme toggle, interactive components) — opened with `/open-web` from a temp dir

## Scope

Use when you need a UI/flow prototype before real implementation — screen mockups, user flows, component states, responsive layouts

- Need a prompt for AI image/design generation → `/report-prompt-uxui-web-design`
- Need a visual report from existing data → `/visualize-in-web` or `/report-html` directly
- Multi-route/production-quality interactive app prototype (SolidJS + Vite) → `/design-web-prototype`
- CLI or TUI prototype to be discussed in chat only → `/design-cli-prototype` / `/design-tui-prototype`
- Production UI → implement in the real project, not this skill

## Execute

### 1. Load Skills

> Goal: build on the conventions that already exist, not from memory

1. Run `/follow-devin-global-skills` — list global (`%APPDATA%\devin\skills`) and project (`.devin/skills/`) skills matching the brief's domain
2. Read the ones this prototype must obey: `/report-html` (single-file conventions), `/follow-web-standard` (native elements), `/follow-lib-css`, `/follow-design-system`
3. Project `AGENTS.md` → read its `### Skills` section; reuse the project's existing visual language instead of a generic one

### 2. Gather Brief

> Goal: Know what to prototype

1. If the argument is a feature/route → gather requirements: screens, components, interactions, states
2. Unclear → run `/ask-me` (scope: one screen or several, device targets, fidelity)
3. Specify the needed mock data — realistic sample data, not lorem ipsum

### 3. Build Prototype

> Goal: A single-file HTML that actually works

1. Run `/create-files-in-os-temp` — create `<temp>/prototype/index.html`
2. Follow `/report-html` conventions: `<!DOCTYPE html>` + Tailwind CDN + Vue 3 (`vue.global.js`) + dark mode toggle
3. Use interactive elements as the prototype requires: tabs, modals, drawers, hover states, form inputs, transitions — Vue `v-if`/`v-for`/`v-model`/`@click`; prefer native elements (`<dialog>`, `popover` attribute, native form validation) per `/follow-web-standard`
4. Multiple screens → a sticky nav/tab bar switching screens within the single file (no separate files)
5. Mobile view → responsive + device frame (rounded border + width, e.g. `max-w-[390px]`) when the brief specifies it
6. Annotations are allowed — a badge/note marking it as a prototype (e.g. "mock data", "not wired")

### 4. Open And Iterate

> Goal: the user can view and keep editing it

1. Run `/open-web` to open the file in temp
2. Run `/report` summarizing the path + covered screens/states
3. If the user asks for changes → edit the same file in temp, then refresh

## Rules

- Write prototypes to temp only — never write into the project (unless the user orders it)
- Always run `/follow-devin-global-skills` first — the project/stack skills own the markup, styling, and design-system conventions; never invent a parallel set
- It must be genuinely interactive — not a static image/screenshot
- Single file — all assets via CDN, mock data inline
- Fidelity per brief — lo-fi wireframe (gray boxes, fast) or hi-fi (per the design system) — default hi-fi-lite: real components, restrained styling

- Always follow `/report-html` conventions for the HTML
- Always use `/open-web`, `/create-files-in-os-temp`
- Use `/ask-me` when needed

## Expected Outcome

- Interactive prototype open in the browser — the user can really click and toggle states
- The skills read first are listed, and the markup/styling follows the conventions they already define
- Easy to share/iterate (one file in temp)
- No prototype files mixed into the project source

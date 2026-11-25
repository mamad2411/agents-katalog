---
name: frontend-design-tty
description: >
  Design system for dark, terminal-inspired web UIs (monospace, mint/sage on dark
  blue-grey, box-drawing borders, no rounded corners) — concrete CSS tokens +
  component patterns. Use when building or extending a web UI in TTY aesthetic, or
  checking an element for TTY conformance.
status: active
invocation:
  primary: user-facing
  secondary: [sub-skill]
  trigger_patterns:
    - "TTY-Aesthetic"
    - "TTY-Design"
    - "TTY-Style"
    - "Terminal-Pastell"
    - "Terminal-Style UI"
    - "wende TTY an"
    - "Hex-Label"
    - "Box-Drawing"
    - "Monospace-UI"
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: frontend_design_tty

## Purpose

Visual identity for dark, terminal-inspired web UIs. **Not a retro
terminal emulator, not a hacker movie** — a contemporary app that takes
the structure and typography of terminal interfaces, softened with
pastel accents. *"The child of a Linux TTY and a calm late-night
coding session."*

The skill is a **design-system skill**, not a methodology skill: it
provides **concrete token values, component patterns and anti-patterns**.
Whoever invokes it gets a reference that translates directly into CSS /
components — not guidance on how to decide.

Used by consumer apps that explicitly declare TTY aesthetic as
their default — typical: chat/voice/video apps, dashboards,
operator UIs. Other projects can adopt it equally.

## When to invoke

- Building a new web UI component / page / layout when the project
  explicitly declares TTY aesthetic (e.g., `intent.md` or
  `decisions.md` lists TTY style)
- Checking existing UI for TTY conformance (drift check before merge)
- Selecting design tokens (colours, spacing, type) — not from memory
- Setting up a theme variant (e.g., Amber Console, alternative accent
  palette)

### Do not invoke for

- **Generic production UI discipline** (component arch, state, 4
  states, a11y methodology) -> `frontend_ui_engineering`
- **UX spec review** (heuristic, IA, interaction) -> `spec_board mode=ux`
- **Code-diff review** of frontend changes -> `code_review_board`
  (with UX specialist personas)
- **Backend / API design** -> `api_and_interface_design`
- **Apps with a different aesthetic** (Material, Tailwind default,
  Glassmorphism, etc.) — TTY is opinionated, NOT a default

## Standalone rationale

Why a separate skill rather than a mode of `frontend_ui_engineering`
or a reference file?

- **`frontend_ui_engineering`** = generic methodology (what must
  happen during the build: file layout, container/presentation split,
  state tree, a11y patterns, 4 states). Design-system-agnostic — fits
  Material, Tailwind default, TTY, Glassmorphism alike.
- **`frontend_design_tty` (this skill)** = a concrete design system with
  **token values, component patterns and anti-patterns**. Methodology-
  agnostic — does not concern how a component is built, only how it
  looks.

The two complement each other: `frontend_ui_engineering` says *"build
an empty-state component with 4 states"*, `frontend_design_tty` says
*"use `--bg-elevated` as the background, a hex label as the header,
monospace 14px"*. Deleting and integrating would either narrow the
methodology to TTY or render the design system invisible.

Source: design system originally developed for an internal
consumer app, contributed to forge as a standalone skill that
any consumer can opt into.

## Process

Application of the skill runs in 4 steps — applies to both new builds
and conformance checks.

### 1. Token setup (once per project)

Set up a `:root` block with the colour, typography, spacing and border
tokens from the reference blocks in `tokens.md`. One theme = one complete token
set, no mixing.

- New component code references CSS vars EXCLUSIVELY, never raw hex.
- If the project wants multiple themes: `[data-theme="..."]` attribute
  on the root element + a theme block per variant (see `tokens.md`
  §Theme architecture).

### 2. Pick a component pattern

For each component type (button, input, modal, sidebar, status
indicator, chat message, ...), adopt the matching pattern block from
`components.md` §Component patterns. For a deviating use case: document
it in `components.md` §Domain extension points instead of overriding global tokens.

### 3. Conformance check

Before merge / PR submission, check against §Anti-Patterns. One
anti-pattern hit = block. Examples: rounded corners > 2px,
proportional fonts anywhere, drop shadows on cards, chat bubbles,
hardcoded hex.

### 4. Domain extension (optional)

Project-specific tokens (chat density, video aspect ratio, sidebar
width) as additional `--<domain>-*` CSS vars in the project theme
file, NOT here.

---

## Reference and design tokens

When setting up or extending a project's token block (Process step 1), when selecting a colour, type, spacing or
border value, and when setting up a theme variant: read and follow `skills/frontend_design_tty/tokens.md` (FABRK
reference, colour tokens, theme architecture and colour rules, typography, borders and box-drawing with bracket
labels, spacing and density).

---

## Component patterns

When picking a component pattern for a component or layout (Process step 2), when adding motion, focus, contrast,
ARIA or responsive behaviour, and when adding domain-specific tokens (Process step 4): read and follow
`skills/frontend_design_tty/components.md` (buttons, inputs, sliders, status indicators, chat messages, sidebar,
modals with the layer map, scrollbars; animation and transitions; layout rules; accessibility; responsive behaviour;
domain extension points).

---

## Red flags

Observable signals that the skill is being violated or applied
poorly — for self-monitoring and code review:

- Hardcoded `#hex` values in components instead of CSS vars
- `border-radius: 4px` (or more) anywhere — only 0 or up to 2px is
  allowed
- `font-family: sans-serif` / `system-ui` without a `--font-mono`
  fallback chain
- `box-shadow` on cards/panels (non-modal surfaces)
- Chat bubbles in Discord/WhatsApp style
- `linear-gradient(...)` on backgrounds
- Material/Tailwind default components without adaptation
- `color: #fff` or `background: #000` (pure white/black)
- Emoji as a functional icon (e.g., a submit button with "rocket
  emoji")
- Toast notifications with rounded corners + drop shadow
- Custom cursor (`cursor: url(...)`)
- Tree-prefix characters in navigation (`├─`, `└─`) — box drawing for
  borders yes, but not as a bullet replacement
- Animation spam (hover bounce, page-load stagger, gratuitous
  transitions)
- A theme block that overrides only part of the token palette (it
  should always redefine ALL tokens)

## Anti-patterns (NEVER do this)

- `border-radius > 2px` (rounded corners)
- Drop shadows on cards or panels (modals/dropdowns only)
- Gradient backgrounds on surfaces
- Chat bubbles (Discord/WhatsApp style)
- Proportional fonts anywhere
- Bold/saturated colours without desaturation (no pure red/blue/green)
- Generic Material Design or Tailwind default components
- Toast notifications with rounded corners and shadows
- Emoji as a functional icon (use text labels or SVG icons)
- Fake progress with no signal (e.g., infinite shimmer on a panel
  that never updates). Spinners/indicators must reflect real
  activity.
- White or light backgrounds on any element
- Tree-prefix characters in navigation
- Hardcoded hex values in components (use CSS vars)
- Custom cursors

## Common rationalisations

| Rationalisation | Reality |
|---|---|
| "Just a tiny radius on the card corner, won't hurt" | Exactly these inconsistencies make the AI-aesthetic look. Hard rule = 0 or 2px max. |
| "One hex value directly in a component is OK, just this once" | Theming breaks. The first theme variant uncovers the blind spot — usually weeks later. |
| "Chat bubbles are better for UX" | The Discord/Slack/WhatsApp convergence argument. TTY aesthetic is explicitly different — anyone wanting that uses a different skill. |
| "An npm Material component will do, I'll customise later" | "Later" doesn't happen. The component carries foreign visual defaults through the entire app. |
| "Pure black `#000` is darker, so better for a dark theme" | Pure black creates halo effects and lacks contrast against the underlying system UI. `--bg-input` (`#16162a`) is the lower bound. |
| "A drop shadow makes cards prettier" | Makes them look like a Material card lookalike. TTY has 4 background layers for depth — shadow is a modal-only signal. |

## Contract

### INPUT

- Required: a project with a web UI (HTML/CSS or a framework like
  React/Vue/Svelte) that wants to adopt or already uses TTY aesthetic.
- Optional: existing theme file to extend, or a component library to
  check for conformance.
- Context: the project intent / decisions file should declare TTY
  style explicitly as the default.

### OUTPUT

- DELIVERS: concrete CSS custom properties (colour, type, spacing,
  border), component pattern snippets (button, input, modal, sidebar,
  status indicator, chat message), layer map (z-index), animation
  patterns, anti-pattern list.
- DOES NOT DELIVER: generic UI methodology (component architecture,
  state management, test patterns) — that is `frontend_ui_engineering`.
  Also no UX heuristics (Nielsen, IA, interaction) — that is
  `spec_board mode=ux`.
- ENABLES: consistent TTY aesthetic across multiple
  components/pages, theme variants without refactoring, code review
  against a clear pattern list.

### DONE

- [ ] A `:root` token block exists in the project with all mandatory
      tokens (colour, type, spacing, border).
- [ ] Components reference CSS vars exclusively, no hardcoded hex
      values.
- [ ] Walked through the anti-pattern list — no hits.
- [ ] In a multi-theme setup: every theme redefines the COMPLETE
      token palette (no partial override).

### FAIL

- Retry: fix individual anti-pattern hits (replace hardcoded hex,
  set border-radius to 0, etc.). No skill escalation.
- Escalate: on systemic incompatibility (e.g., the app uses a
  component library that does not allow TTY tokens) — decision to the
  user: switch library, wrap library, or drop TTY aesthetic for this
  sub-app.
- Abort: if the project explicitly declares a different aesthetic
  (Material, Glassmorphism, etc.) — the TTY skill is wrong here, use
  another design discipline.

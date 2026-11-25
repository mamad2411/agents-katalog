---
name: simple-visual
description: >
  Write an app-level visual design system document (docs/visual.md) — colors, typography, spacing,
  components, visual guidelines — from documentation, a user message, or codebase context. One per
  project, not per feature. Use when the user wants to create, extract, or formalize a consistent
  visual identity for their app. Triggers: "create a design system", "define the visual style",
  "style guide", "UI design tokens", "design language", "look and feel".
disable-model-invocation: true
---

# Simple Visual — Write a Visual Design System Document

You are writing a visual design system document following the **DESIGN.md format** — a self-contained,
plain-text representation of a design system. Your job is to produce a `docs/visual.md` file that
gives an AI coding agent (or a human developer) a clear, complete reference for **how the application
should look and feel** — the colors, typography, spacing, shapes, elevation, component styles, and
visual guidelines that define the app's identity.

The document has two parts:
1. **YAML frontmatter** — machine-readable design tokens that can be converted to/from `tokens.json`,
   Figma variables, and Tailwind theme configs
2. **Markdown body** — human-readable design rationale and guidance

This is an **app-level** document — one per project, shared across all features. It lives at the
`docs/` root, not inside a feature subfolder, because visual identity applies to the entire
application.

This skill works in two modes:

1. **Greenfield mode:** The user describes an app they want to build (or provides docs, wireframes,
   or a brief). You create a design system from scratch that matches their vision.
2. **Extraction mode:** The user has an existing codebase. You analyze it, identify the visual
   patterns already in use, and formalize them into a design system document — filling gaps and
   resolving inconsistencies along the way.

Both modes produce the same output: a `visual.md` file that an implementing agent can reference
to build UI that is visually consistent.

## Folder convention

The visual design system lives at the `docs/` root alongside the feature manifest:

```
docs/
  index.json              ← feature manifest
  visual.md               ← THIS SKILL'S OUTPUT (app-level)
  <feature-name>/
    spec.md               ← from simple-spec
    design.md             ← from simple-design
    issues.json           ← from simple-tasks
    progress-log.md       ← from simple-implement
```

All feature-specific artifacts live in `docs/<feature-name>/`. The visual design system is
referenced by any feature that has UI work — agents read `docs/visual.md` alongside the
feature's own documents.

## Workflow

### 1. Gather context

Start by collecting as much information as you can **before** asking the user anything.

**From the user's input:**
- Read the user's message carefully. Extract: the app name, the type of application (web app,
  mobile app, CLI, dashboard, landing page, etc.), the intended audience, and any aesthetic
  preferences they've stated (e.g., "modern and clean", "playful", "enterprise-grade").
- If the user provided reference material (docs, specs, design files, screenshots, mood boards),
  read or examine them fully.
- If spec or design docs exist in any feature folder (e.g., `docs/<feature-name>/spec.md` or
  `docs/<feature-name>/design.md`), skim them for context about the app's purpose and scope.

**From the codebase (extraction mode):**
- This is where the skill does its heaviest lifting when working with an existing app.
- Search for and read:
  - **CSS / styling:** Look for CSS files, Tailwind config (`tailwind.config.js/ts`), CSS-in-JS
    theme files, SCSS variables, CSS custom properties (`--color-*`, `--font-*`, `--spacing-*`),
    design token files, or any centralized style definitions.
  - **Component library:** Check for a component library or shared UI components. Look at how
    buttons, inputs, cards, modals, and navigation are styled. Identify patterns.
  - **Color usage:** Search for hex values, RGB/HSL definitions, color variable usage. Map out
    which colors are used where and how consistently.
  - **Typography:** Look for font imports (`@font-face`, Google Fonts links, font files), font
    family declarations, and the type scale in use.
  - **Spacing patterns:** Look at padding/margin values in components. Is there a consistent
    scale, or are values ad-hoc?
  - **Layout:** Identify the layout approach — grid system, max widths, breakpoints, sidebar
    widths, content structure.
  - **Existing design system artifacts:** Check for a `theme.ts`, `tokens.json`, `variables.css`,
    `design-system/` directory, Storybook config, or similar.
- The goal is to identify what's intentional vs. accidental in the current visual language, and
  to formalize the intentional patterns while flagging inconsistencies.

**Platform and framework awareness:**
- Note the UI framework in use (React, Vue, Svelte, vanilla, etc.) and the styling approach
  (Tailwind, CSS modules, styled-components, etc.). This context informs how specific your
  component guidance should be.
- If the app uses a component library (e.g., shadcn/ui, MUI, Ant Design, Chakra), acknowledge
  it and specify how the design system customizes or extends it rather than replacing it.

### 2. Ask follow-up questions (only if needed)

After gathering context, assess what's still ambiguous. Common gaps at the visual design stage:

- **Aesthetic direction:** "I see you mentioned 'modern' — are you thinking more like Linear
  (minimal, monochrome, lots of whitespace) or more like Notion (warm, slightly playful, rounded)?"
- **Brand constraints:** "Do you have existing brand colors or fonts that must be used, or is
  this a fresh palette?"
- **Dark mode:** "Should the design system include a dark mode variant?"
- **Target platform:** "Is this primarily desktop, mobile, or both? This affects spacing, touch
  targets, and component sizing."
- **Existing patterns (extraction mode):** "I found three different button styles in the codebase.
  Which one is the intended primary style — the rounded blue one in the dashboard, or the square
  one in the settings page?"
- **Accessibility requirements:** "Are there specific accessibility standards you need to meet
  (e.g., WCAG AA, WCAG AAA)?"

Only ask questions where the answer materially affects the design system. If you can make a
reasonable choice based on the context and state it explicitly in the document, prefer that over
asking. Keep it to one round of 1-4 focused questions.

Use whatever mechanism is available (a structured question tool, a chat message, etc.).

### 3. Write the visual design system

Read the template at `references/visual_template.md` in this skill's directory. Use it as the
structural backbone for your output. The template follows the **DESIGN.md format** — see
`references/design_md_format.md` for the full specification.

**Document structure:**

The document must begin with YAML frontmatter containing design tokens:
```yaml
---
version: alpha
name: [App Name]
colors:
  primary: "#XXXXXX"
  ...
typography:
  body-md:
    fontFamily: Inter
    fontSize: 16px
    ...
spacing:
  md: 16px
  ...
rounded:
  md: 8px
  ...
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    ...
---
```

Sections must appear in this order (omit irrelevant ones):
1. Overview (also: "Brand & Style")
2. Colors
3. Typography
4. Layout (also: "Layout & Spacing")
5. Elevation & Depth (also: "Elevation")
6. Shapes
7. Components
8. Do's and Don'ts

**Key principles:**

- **Be opinionated, not vague.** "Use a clean font" is useless; "use Inter 400 at 16px/24px for
  body text" is actionable. Every token needs a concrete value and a clear role.

- **Ground everything in real values.** Every color is a `#` hex code in sRGB; every dimension
  carries a unit (`px`, `em`, `rem`); typography tokens specify `fontFamily`, `fontSize`,
  `fontWeight`, and `lineHeight` at minimum.

- **Use token references.** In the `components` section, reference other tokens with
  `{path.to.token}` syntax (e.g., `"{colors.primary}"`, `"{rounded.md}"`) — this creates a
  coherent token graph that tools can resolve.

- **Prose explains, tokens define.** Markdown prose gives context and rationale; YAML tokens give
  the normative values. Prose may use descriptive names ("Midnight Forest Green") that map to
  systematic token names (`primary`).

- **In extraction mode, document what IS, then improve.** Start from the patterns in the
  codebase; if it uses 5 slightly different grays, pick the best 2-3 and consolidate, noting what
  you changed and why. Aim for a system the team recognizes as "theirs, but cleaned up."

- **Component guidance should be project-specific.** Don't enumerate every possible component —
  cover the ones the app actually uses: a dashboard needs table styling, a chat app needs message
  bubbles, a landing page needs hero and CTA styling.

- **Do's and Don'ts are guardrails, not theory.** Each item should prevent a concrete mistake:
  "Don't use more than two font weights on a single screen" prevents visual noise; "Do use the
  primary color only for the single most important action per screen" prevents action dilution.

- **Accessibility is non-negotiable.** Every design system must address contrast ratios, focus
  indicators, and touch targets at minimum — these are constraints the visual choices must satisfy.

- **Color palette should be complete.** Always include semantic/feedback colors (error, warning,
  success, info) even if unmentioned — defining them upfront prevents ad-hoc choices later.

- **Think in systems, not pages.** Define tokens and rules that generalize — the system should
  produce consistent results on any screen, not just the ones the user mentioned.

### 4. Save the output

- Save to `docs/visual.md` relative to the project root (create the `docs/` directory if needed).
- Tell the user the file path and give a brief summary of the design direction.

### 5. Suggest next steps

Let the user know the visual design system is ready to guide implementation. Possible next steps:

- If **simple-spec** or **simple-design** skills are available, suggest the user run those to
  define what to build and how, using this visual document as a reference for the UI layer.
  The typical workflow is: **simple-spec** → **simple-design** → **simple-visual** (optional)
  → **simple-tasks** → **simple-implement** (or **simple-run**).
- If the codebase already exists, suggest an implementation pass to align existing components
  with the new design system — refactoring inconsistencies, extracting shared tokens, etc.
- If the user hasn't decided on a component library or styling approach, suggest options that
  fit the design system well.

## Important notes

- This skill produces a **visual design system**, not a technical design or product spec — focus
  on *how it looks and feels*, not data models, API contracts, or business logic. If you find
  yourself writing about schemas or endpoint signatures, you've crossed into design/spec
  territory; pull back.
- Scale the document to the app — a simple landing page doesn't need a 10-section design system;
  a complex SaaS dashboard does.
- If the user gives very little context (e.g., "make a design system for my app"), don't guess
  wildly — ask the clarifying questions from step 2.
- If brand guidelines or a Figma file already exist, stay consistent with them rather than
  replacing them. Position this document as the developer-facing translation of the design
  team's intent.
- Match the actual stack: with Tailwind, align spacing and sizing tokens to its default scale;
  with CSS custom properties, name tokens to map directly onto `--var` names.

## Interoperability

The YAML frontmatter follows the [DESIGN.md format](references/design_md_format.md) — see that
reference for the full token specification. The format maps cleanly to tokens.json (W3C Design
Tokens), Figma variables, Tailwind theme configs, and CSS custom properties.

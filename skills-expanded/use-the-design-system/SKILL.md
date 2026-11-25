---
name: use-the-design-system
description: >-
  If the project already has a UI system, use it before building anything new.
  Use this WHENEVER you add or change UI in an existing codebase: a button,
  modal, form, card, page, or any component. Look first for the project's
  component library, design tokens, theme, and utility setup (a components or ui
  folder, shadcn/ui, MUI, Chakra, Mantine, Radix, a Tailwind config, CSS
  variables), and build with those. Reinventing a button from scratch when the
  project has one creates inconsistency and duplicate work. Only hand-roll a
  component when nothing in the system fits, and then match the system's
  conventions so it belongs.
---

# Use the design system

Most existing projects already decided what a button looks like, what the spacing
scale is, and which colors are allowed. When you drop in a freshly hand-rolled
component with its own hardcoded colors and padding, it looks slightly off, it
duplicates work, and it drifts from the rest of the app. The system is there so
the UI stays consistent. Use it before you build anything new.

The rule: in an existing codebase, find the UI system first and build with it.
Hand-rolling is the last resort, not the default.

## Look before you build

Before writing a new component, scan the project for what already exists:

- A components folder: `components/`, `src/ui/`, `components/ui/`, a shared
  package. Is there already a `Button`, `Modal`, `Input`, `Card`?
- A component library in `package.json`: shadcn/ui, MUI, Chakra, Mantine, Radix,
  Ant, Headless UI, DaisyUI, Bootstrap. Use its components and its API.
- Design tokens and theme: CSS custom properties (`--color-primary`, spacing
  vars), a `theme.ts`, a Tailwind config with custom colors and scales.
- Utility conventions: Tailwind classes, CSS modules, styled-components. Match how
  the rest of the code styles things.
- Existing patterns: open a couple of nearby components and copy their structure,
  prop shapes, and naming.

## Build with it, not around it

- Reuse the existing component instead of making a new one that does the same job.
- Pull colors, spacing, radius, and typography from the tokens or theme. Do not
  hardcode a hex value when there is a token for it.
- Follow the library's API and the project's conventions, so your code reads like
  the code already there (see also: write code that matches its surroundings).
- Compose from primitives the system gives you rather than reaching for a new
  dependency.

## When nothing fits

Sometimes the system genuinely lacks what you need. Then build it, but build it to
belong:

- Use the project's tokens and primitives, not a fresh set of hardcoded values.
- Match the file location, naming, and prop conventions of the existing
  components.
- If it is reusable, add it to the system so the next person finds it, rather than
  burying a one-off in a page.
- Do not pull in a whole new UI library to get one component when the project
  already standardized on another. If you think a new dependency is warranted, ask
  (`dont-be-afraid-to-ask`).

## Before you deliver

Before you ship new UI, ask: does the project already have this component, token,
or pattern? If yes, you should be using it. Check that your colors and spacing
come from the system, your component matches the library and conventions in use,
and you have not quietly duplicated something that already exists.

For greenfield projects with no system yet, see `no-ai-design-cliches` for making
intentional choices, and `prefer-icons` for iconography.

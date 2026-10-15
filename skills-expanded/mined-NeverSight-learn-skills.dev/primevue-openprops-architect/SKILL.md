---
name: primevue-openprops-architect
description: Enforces PrimeVue + project design tokens when editing Vue or CSS. OpenProps rules apply only when the project already uses open-props. Runs vue-tsc and stylelint when available.
paths:
  - "**/*.vue"
  - "**/*.css"
  - "**/*.scss"
---


# PrimeVue + project tokens

Enforces PrimeVue and the project's **semantic token** system. **OpenProps is optional** — detect before enforcing OpenProps-specific rules.

When chained from parent skills, **`validate_vue.py` runs in a `shell` subagent** by default. See `reference/subagents.md`.

## When to use

- Editing `.vue` single-file components or project stylesheets
- Agent is about to add UI components, tokens, or layout
- Validating generated Vue against team design system

## Instructions

1. Read `context/VOCABULARY.md` and `context/ANTI_PATTERNS.md` before writing UI code.
2. Read `heyeddi-design/reference/token-strategy.md` — detect OpenProps vs custom `tokens.css`.
3. Reuse PrimeVue components from the project catalog — never invent props.
4. Use semantic CSS variables from project `tokens.css` / `design.md` — OpenProps-backed (`var(--surface-1)`) or custom (`var(--brand)`). No scattered hex in `.vue` / CSS.
5. After edits, run `python scripts/validate_vue.py --project-root <root>`.
6. Fix all reported issues before finishing.

## Scripts

- `validate_vue.py` — runs `vue-tsc --noEmit` and stylelint if installed

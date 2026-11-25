---
name: tailwindcss-4-design-system
description: Helps agents design and refactor Tailwind CSS 4 theme variables, tokens, custom utilities, variants, dark mode hooks, and reusable CSS-first design-system patterns.
license: MIT
---

# Tailwind CSS 4 Design System Skill

Use this skill when changing Tailwind CSS 4 design tokens, theme variables, utilities, variants, dark mode hooks, or reusable styling APIs.

## When to Use

- The task changes colors, fonts, spacing, breakpoints, shadows, radii, animations, or other design tokens.
- The task adds or updates `@theme`, `@utility`, `@variant`, or `@custom-variant`.
- A component has repeated Tailwind class patterns that should become a stable token or utility.
- The project needs a dark-mode, brand, or theme variant convention.

## Design Guidance

1. First determine whether the value is a design token, one-off style, or component concern.
2. Use `@theme` for values that should generate Tailwind utilities or variants.
3. Use regular CSS variables for values that should not generate utilities.
4. Use `@utility` when a reusable utility API improves readability and works with variants.
5. Use `@custom-variant` for project-specific selectors such as data-theme or state attributes.
6. Keep token names consistent with Tailwind namespaces.
7. Verify at least one generated utility that depends on the changed token.
8. Review visual states and accessibility before finalizing.

## Workflow

- `workflows/design-token-change-workflow.md`: use for planned token, utility, or variant changes.

## Resource

- `resources/theme-variable-namespaces.md`: quick namespace reference for common theme variable families.

## Example

- `examples/theme-tokens.example.css.md`: CSS-first token and custom variant example.

---
name: ui-tailwind-tokens
description: "Design Tailwind tokens, semantic colors, variants, arbitrary values, @apply, and cva."
---

# UI Tailwind Tokens

Use Tailwind through the project's design tokens and component variants, not as a collection of one-off values.

## Process

1. Inspect the project's Tailwind version, theme setup, tokens, helpers and component variant patterns before editing.
2. Prefer semantic tokens and shared scales for color, spacing, radius, typography, z-index and motion.
3. Treat arbitrary values as exceptions; promote repeated values to tokens.
4. Put state styles such as disabled, focus, hover and active into base components or variants.
5. Use semantic variant names that describe intent, not color.
6. Keep responsive utilities readable and test every breakpoint added.
7. Use `@apply` only for semantic content styling, third-party generated markup, global rich text, or places where a component is impractical.

## Token Rules

- Use project tokens instead of random values.
- Avoid `mt-[13px]`, arbitrary colors and one-off widths unless justified.
- If an arbitrary value repeats, make it a token.
- Do not create colors outside the palette without a design-system decision.
- Do not mix several spacing systems.
- Avoid inline styles for patterns that belong in components.
- Do not use `!important` as the default conflict resolver.

Token naming:

- semantic when describing UI role: background, foreground, muted, border, primary, danger, success;
- scale-based when describing neutral scale: spacing, radius, typography;
- not named after one view;
- includes light/dark theme support when the app has themes;
- motion tokens include duration, easing and distance;
- z-index uses layer names such as dropdown, sticky, modal and toast.

## Component Variants

- Base components should not copy long Tailwind class lists throughout the app.
- Variant names describe intent: `primary`, `secondary`, `danger`, `ghost`.
- Size variants come from system scale.
- Disabled, focus, hover and active states belong in the base component.
- External `class` can extend but should not break accessibility.
- Base component focus behavior must remain stable.

## `@apply`

Use `@apply` when:

- styling markdown/content classes;
- styling generated third-party markup;
- reducing repetition where a component is not practical;
- creating rich-text global styles.

Avoid `@apply` when:

- a small component would be clearer;
- the class hides many states;
- the style is used only once;
- it creates a second CSS system outside tokens.

## Responsive Utilities

- Treat base classes as the smallest supported layout.
- Add larger breakpoint variants progressively.
- Avoid long contradictory chains such as `hidden sm:block md:hidden lg:flex`.
- If visibility logic becomes complex, improve structure or extract a component.
- Test every breakpoint you add.

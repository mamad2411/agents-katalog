---
name: follow-lib-shadcn-solid-config-tokens
description: Tune shadcn-solid theme tokens — colors, radius, variants, cva
argument-hint: "[scope]"
related:
  - follow-lib-shadcn-solid
  - follow-lib-unocss
  - follow-design-system
  - improve
  - resolve-errors
---

## Goal

Tune shadcn-solid's theme tokens — color palette, radius, component variants with `cva`, and new tokens

## Scope

Use when editing theme tokens of an existing setup — covers CSS variables, base color, component variants in `src/components/ui/`, and token naming consistency

## Execute

### 1. Read Current Tokens

> Goal: read the current theme tokens and components

1. Open the global CSS file — review the current CSS variable sets in `:root` and the dark block
2. Open `components.json` — review the base color and aliases
3. If there's no theme yet → run the `setup-theme` workflow first; always merge with the original, never overwrite

### 2. Adjust Color And Radius Tokens

> Goal: change the palette and radius to match the design

1. Edit the variable values in `:root` and the dark block together — every changed token must exist in both modes
2. Make `--radius` the single source of corner radius — components use `rounded-md` etc. derived from it
3. Add new semantic tokens (e.g. `success`, `warning`) named per the existing convention, then map them into the CSS framework's utilities
4. Run `/deep-review-codebase` domain `review-config` if unsure the tokens match what components reference

### 3. Customize Component Variants

> Goal: adjust variants in the copied components with `cva`

1. Open the component in `src/components/ui/` — variants are defined with `cva`, e.g. `buttonVariants`
2. Add/edit variants (`variant`, `size`) in the `cva` definition — don't repeat hard-coded classes in JSX
3. Variant classes must reference tokens like `bg-primary text-primary-foreground` — not `bg-blue-500`
4. Update `defaultVariants` to match the design intent

### 4. Sync With CSS Framework

> Goal: make the tokens actually usable through utilities

1. Tailwind: check the `tailwind.config`/`@theme` block maps the variables to color names (`primary`, `muted`, etc.)
2. UnoCSS: map into `theme.colors` per `/follow-lib-unocss theme`
3. Test the new utilities, e.g. `bg-success`, `text-warning-foreground`

### 5. Verify

> Goal: confirm the new and existing tokens don't break

1. Run dev — test every changed component variant in both light/dark
2. Use `bunx shadcn-solid@latest diff <component>` to check only the intended spots were changed
3. If it breaks → revert the just-edited keys, then report the diff

## Rules

- Edit tokens in one place — the CSS variables; components reference tokens only
- `:root` and the dark block must always carry the same complete set
- Add variants through `cva` only — no inline class overrides in JSX
- Never modify the Kobalte primitives source — customize at the copied components only
- Use `/follow-lib-shadcn-solid` for the full reference

## Expected Outcome

- Theme tokens tuned to the design — palette, radius, semantic colors complete
- Component variants added/edited through `cva` in a type-safe way
- Dark mode covers all the new tokens
- Tokens stay consistent across CSS variables, framework config, and components

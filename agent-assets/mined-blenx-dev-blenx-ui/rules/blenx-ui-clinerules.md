# Vanilla Extract Authoring Conventions

## Theme Contract

- Use `createThemeContract()` from `@vanilla-extract/css` for semantic theme tokens.
- Contract files go in `packages/theme/src/` with `.css.ts` extension.
- Use kebab-case string values as contract placeholders.

## Theme Implementation

- Use `createTheme(contract, values)` for light and dark theme variants.
- Theme files use `.css.ts` extension and are compiled at build time.
- Theme class names are applied to the root element to switch themes.

## Design Tokens

- Design primitives (spacing, font-sizes, radii, border-widths, durations, easings, z-index) are plain const objects in `theme.css.ts`.
- These are not themeable at runtime and remain consistent across themes.

## Styles

- Use `style()` from `@vanilla-extract/css` for individual component styles.
- Use `globalStyle()` for global/reset styles.
- Use `createThemeContract()` values (theme tokens) inside styles for theme-aware properties.
- Pseudo-classes use `:hover`, `:focus`, etc. as keys inside the style object.
- Media queries: `@media` syntax inside style objects.

## Sprinkles

- Use `@vanilla-extract/sprinkles` for utility-first responsive styles.
- Define conditions for breakpoints and pseudo-classes.

## Recipes

- Use `@vanilla-extract/recipes` for component variants.
- Define `base`, `variants`, and `compoundVariants`.

## Pattern Notes

- ❌ Don't import non-VE values into `style()` — use contract tokens instead.
- ❌ Don't use `createTheme()` at runtime — it is a build-time static call.
- ✅ For runtime theme switching, apply CSS custom properties via inline styles on a wrapper element.

---
name: mui
description: "Applies when building or reviewing Material UI (MUI) components. Covers sx prop, theming, component composition, responsive design, and accessibility."
---

# Material UI (MUI)

## Styling

1. **`sx` prop for one-off styles.** Access theme values directly: `sx={{ p: 2, color: 'primary.main' }}`. Avoid inline `style` prop.
2. **`styled()` for reusable styled components.** Use when the same styles appear in multiple places.
3. **Never recreate `sx` objects in render.** Memoize with `useMemo` or define outside the component for dynamic styles.
4. **Theme spacing for consistency.** `theme.spacing(2)` = 16px (default). Use numeric shorthand in sx: `p: 2`, `m: 1`.

## Theming

5. **`createTheme` + `ThemeProvider` at app root.** Customize palette, typography, shape, breakpoints, component defaults.
6. **Component default overrides in theme.** `components.MuiButton.defaultProps` and `styleOverrides` for global consistency.
7. **Use `theme.palette.mode` for dark mode.** Toggle between `'light'` and `'dark'` via context.

## Component composition

8. **Slots and slotProps for deep component customization.** Preferred over CSS overrides for internal elements.
9. **Compose with Stack, Grid, Box, Container for layout.** Stack for 1D, Grid for 2D, Box for arbitrary.
10. **Use responsive breakpoints in sx:** `sx={{ width: { xs: '100%', md: '50%' } }}`.

## Accessibility

11. **Always set `aria-label` on icon buttons.** `<IconButton aria-label="delete">`.
12. **Use built-in label/helperText props on form components.** Never skip labels.
13. **Use `role` and `aria-*` props from MUI's API** rather than raw HTML attributes.

## Performance

14. **Tree-shake with path imports** if not using a bundler that supports package.json exports: `import Button from '@mui/material/Button'`.
15. **Use DataGrid virtualization for large tables.** Never render thousands of TableRows.

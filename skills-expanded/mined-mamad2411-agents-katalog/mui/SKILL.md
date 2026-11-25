---
name: mui
description: Material UI (MUI) conventions — ThemeProvider, sx prop, styled, component variants, and accessibility. Load when working with MUI components.
user-invocable: false
stack: ui-components/mui
paths:
  - "**/theme*"
  - "**/ThemeProvider*"
  - "src/styles/**"
---

Full standards in [mui.md](mui.md). Always-on summary:

**Setup:**
- Import components from `@mui/material`: `import { Button, TextField } from '@mui/material'`
- Wrap the app in `ThemeProvider` + `CssBaseline` — one place, at the root
- Define the theme with `createTheme({ palette: { primary: { main: '#1976d2' }, ... } })` in `theme.ts`
- Use `<Button variant="contained">`, `<TextField label="..." />` — never raw `<button>` or `<input>` inside MUI layouts

**Styling priority (highest to lowest):**
1. `sx` prop — one-off responsive overrides on a single component
2. `styled()` — reusable styled components (when `sx` becomes complex)
3. Component `variants` in theme — for brand-consistent variations across the app
4. `theme.components[ComponentName].styleOverrides` — global component style changes

**sx prop:**
- Use theme tokens: `sx={{ color: 'primary.main', mb: 2 }}` not `sx={{ color: '#1976d2', marginBottom: '16px' }}`
- Responsive: `sx={{ fontSize: { xs: 14, md: 16 } }}`

**Accessibility:**
- MUI components are accessible by default — don't break it by hiding focus outlines
- `aria-label` required on `IconButton` — no visible text label means screen readers get nothing
- `<TextField>` with `label` prop is accessible; don't use plain `<input>` inside MUI layouts

**Never:**
- Override MUI styles with raw CSS classes (fragile across MUI versions)
- Use `makeStyles` or `withStyles` — deprecated in MUI v5; use `sx` or `styled`
- `sx={{ style: ... }}` — `style` is not a valid `sx` key

**Related skills:** Your frontend layer (React patterns), `css/tailwind` if using both together

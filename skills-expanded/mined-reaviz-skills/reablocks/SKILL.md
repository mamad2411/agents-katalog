---
name: reablocks
description: Use when building UI in React with the reablocks component library (Button, Dialog, Drawer, Select, Calendar, CommandPalette, Tabs, Tree, Tooltip, etc.). Covers ThemeProvider setup, extendTheme, custom variants, mergeThemeClasses, useComponentTheme/useTheme hooks, and the 50+ component index.
---

# Reablocks

Reablocks is a React UI component library with 50+ components built on **Tailwind CSS** and **Framer Motion**. It provides a comprehensive theming system, accessible components, and consistent design patterns.

## Installation

```bash
npm install reablocks
```

## ThemeProvider Setup

Every app using reablocks must be wrapped in a `ThemeProvider`:

```tsx
import { ThemeProvider, theme } from 'reablocks';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <YourApp />
    </ThemeProvider>
  );
}
```

### ThemeProvider Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `theme` | `ReablocksTheme` | Yes | The theme to apply |

### Built-in Themes

Reablocks ships **two theme options**:

- **`theme`** — standard theme using Tailwind utility classes. The default. Use this unless the user asks for Unify.
- **Unify Theme** — design-system theme built on a three-level token architecture (primitives → semantic → Tailwind), synced with the Unify Figma library. Available in two flavors:
  - **Quick-start**: `themeUnify` export + `reablocks/unify.css` import (one-line setup, fixed tokens).
  - **Production / Figma-synced**: the single-file [`themeUnify.ts`](./unify-theme/SKILL.md#download-the-pre-built-typescript-theme) download (every component theme + composed `ReablocksTheme`) plus the **CSS bundle zip** (`index.css`, `common.css`, `root.css`, `light.css`, `dark.css`, `tw.css`) produced by the Reablocks Figma Plugin's one-click **Export Styles** button. This is what powers per-component detail tokens like `--buttons-details-height-core-icon-lg`.

```tsx
// Default theme
import { ThemeProvider, theme } from 'reablocks';
<ThemeProvider theme={theme}>...</ThemeProvider>

// Unify theme — quick-start
import { ThemeProvider, themeUnify } from 'reablocks';
import 'reablocks/unify.css';
<ThemeProvider theme={themeUnify}>...</ThemeProvider>
```

### When to use Unify instead of the default theme

Switch to Unify when **any** of these apply:

- The user mentions **Figma**, the **Unify Figma library**, or the **Reablocks Figma Plugin**.
- The user wants tokens synced end-to-end from Figma to production.
- The user wants to re-skin components at **fine granularity** (per-component dimensions, radii, padding) without writing Tailwind overrides or per-component TypeScript.
- The user references `themeUnify.ts`, `root.css` / `dark.css` / `light.css` / `tw.css`, or per-component detail tokens like `--buttons-details-*`, `--inputs-details-*`, `--tabs-details-*`.

**For the quick-start path** (single import, no Figma): use `themeUnify` as shown above. No further setup required.

**For the production / Figma-synced path** (single-file `themeUnify.ts` + Figma-generated CSS layers, customization via CSS, designer ↔ engineer sync): see the dedicated skill at [`unify-theme/SKILL.md`](./unify-theme/SKILL.md). It covers:
- Prerequisites (Tailwind v4+, postcss plugins)
- File layout (`root.css` / `dark.css` / `light.css` / `tw.css` / `common.css`)
- Three-tier token architecture and how it cascades
- Re-branding via the primitive color scale
- Per-component tuning without TypeScript changes
- Adding new semantic roles
- Troubleshooting (purge issues, token override order, palette leaks)

Do **not** offer Unify when the user only wants minor color/variant tweaks — `extendTheme(theme, …)` against the default theme is simpler. Do not offer Unify when the user is not on Tailwind v4+ or reablocks v10+.

## Theme Customization

### extendTheme

Use `extendTheme()` to deep-merge partial overrides into a base theme. Only specify the properties you want to change:

```tsx
import { ThemeProvider, theme, extendTheme, PartialReablocksTheme } from 'reablocks';

const customTheme: PartialReablocksTheme = {
  components: {
    button: {
      colors: {
        primary: {
          filled: 'bg-blue-500 hover:bg-blue-600 text-white'
        }
      }
    }
  }
};

<ThemeProvider theme={extendTheme(theme, customTheme)}>
  <App />
</ThemeProvider>
```

### Adding a Custom Variant

You can extend any component with new variants and colors. Only provide the keys you want to add — existing values remain intact:

```tsx
import { ThemeProvider, theme, extendTheme, PartialReablocksTheme } from 'reablocks';

const customTheme: PartialReablocksTheme = {
  components: {
    button: {
      // Add a new variant with its base styles
      variants: {
        gradient: 'border rounded-lg'
      },
      // Add color mappings for the new variant
      colors: {
        primary: {
          gradient: 'bg-linear-to-r from-blue-500 to-purple-500 border-blue-500 text-white'
        },
        secondary: {
          gradient: 'bg-linear-to-r from-pink-500 to-purple-500 border-pink-500 text-white'
        }
      }
    }
  }
};

<ThemeProvider theme={extendTheme(theme, customTheme)}>
  {/* Use the new variant just like built-in ones */}
  <Button variant="gradient" color="primary">Gradient Primary</Button>
  <Button variant="gradient" color="secondary">Gradient Secondary</Button>
</ThemeProvider>
```

The same pattern works for adding custom colors, sizes, or entirely new theme keys to any component.

### mergeThemeClasses

By default, `extendTheme` **replaces** theme string values. To **merge** Tailwind classes (append instead of replace), pass `mergeThemeClasses` as the third argument:

```tsx
import { extendTheme, mergeThemeClasses, theme } from 'reablocks';

const merged = extendTheme(theme, customTheme, mergeThemeClasses);
```

### extendComponentTheme

Extend a single component's theme:

```tsx
import { extendComponentTheme, defaultButtonTheme } from 'reablocks';

const myButtonTheme = extendComponentTheme(defaultButtonTheme, {
  sizes: { xlarge: 'text-xl px-6 py-3' }
});
```

### Theme Types

Reablocks exports several utility types for typing partial themes:

- `PartialReablocksTheme` — `DeepPartial<ReablocksTheme>`, ideal for `extendTheme(theme, ...)` overrides
- `DeepPartial<T>` — recursive `Partial<T>`, useful for typing custom component theme fragments

```tsx
import type { DeepPartial, PartialReablocksTheme } from 'reablocks';
import type { ButtonTheme } from 'reablocks';

const myButton: DeepPartial<ButtonTheme> = {
  sizes: { xlarge: 'text-xl px-6 py-3' }
};
```

## Theme Hooks

### useComponentTheme

Get a specific component's theme from context. Pass an optional custom theme to override:

```tsx
import { useComponentTheme } from 'reablocks';

function MyComponent({ theme: customTheme }) {
  const theme = useComponentTheme('button', customTheme);
  return <button className={theme.base}>...</button>;
}
```

### useTheme

Access the full theme context including CSS tokens and runtime updates:

```tsx
import { useTheme } from 'reablocks';

function MyComponent() {
  const { theme, tokens, updateTheme, updateTokens } = useTheme();
  // tokens = Record<string, string> of CSS custom properties
  // updateTheme() for runtime theme switching
}
```

## Common Component Patterns

When working with reablocks components, follow these conventions:

- **Import from barrel**: Always `import { Component } from 'reablocks'`
- **forwardRef**: All components use `forwardRef` and accept a `ref` prop
- **className**: Components accept `className` which is merged last (highest priority) via `cn()` (tailwind-merge)
- **theme prop**: Components accept a `theme` prop for per-instance theme override
- **cn() utility**: Use `cn()` for Tailwind class merging — combines `classnames` + `tailwind-merge` to deduplicate/resolve conflicts
- **Animations**: Framer Motion powers animations; use `animated` prop (boolean) to toggle
- **Controlled/Uncontrolled**: Form components support both patterns

## ReablocksTheme Component Keys

The `theme.components` object contains theme configs for every component:

```
avatar, avatarGroup, badge, button, chip, checkbox, contextMenu,
dateFormat, dialog, divider, dotsLoader, drawer, ellipsis, field,
select, list, menu, sort, card, kbd, notification, input, dateInput,
calendar, calendarRange, commandPalette, collapse, textarea, radio,
range, redact, toggle, tooltip, tree, jsonTree, popover, pager,
tabs, breadcrumbs, stepper, callout, backdrop, navigation, skeleton,
typography
```

## Component Index

### Elements
Avatar, AvatarGroup, Badge, **Button**, Chip, CommandPalette, IconButton, Kbd, Loader, Navigation, Skeleton

### Form
Calendar, Checkbox, DateInput, Input (DebouncedInput, InlineInput), Radio, Range, Select (SingleSelect, MultiSelect), Textarea, Toggle

### Layout
Breadcrumbs, Card, Collapse, Divider, Field, List, Motion, Stepper, Tabs, Tree

### Layers
Backdrop, Callout, ConfirmDialog, ContextMenu, Dialog, Drawer, Menu, Notification, Popover, Tooltip

### Typography
H1, H2, H3, H4, H5, H6, P, BlockQuote, Lead, Large, Small, Muted

### Data
DataSize, DateFormat, Duration, Ellipsis, InfinityList, Pager, Pluralize, Redact, Sort

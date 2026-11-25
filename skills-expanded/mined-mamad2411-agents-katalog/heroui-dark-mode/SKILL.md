---
name: heroui-dark-mode
description: >
  Add light, dark, and system theme switching to HeroUI v3. CSS-driven themes via
  class dark / data-theme on html (no HeroUI provider). Next.js with next-themes
  (App Router + Pages Router), custom data-theme names, plain React useTheme from
  @heroui/react, theme switchers, bg-background/text-foreground shell, and dark:
  utilities. Keywords: HeroUI dark mode, next-themes, useTheme, data-theme, system
  preference, suppressHydrationWarning. Use when the user runs /heroui-dark-mode.
---

# HeroUI Dark Mode (v3)

Light, dark, and system theme switching for HeroUI v3. Themes are **CSS-driven** — no HeroUI provider required.

**Source:** https://heroui.com/en/docs/react/getting-started/dark-mode  
**Raw MDX:** https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(handbook)/dark-mode.mdx

## Apply the Skill

- Read `references/dark-mode.md` for full provider/switcher samples.
- Put theme class / `data-theme` on `<html>`; keep shell classes `bg-background text-foreground`.
- **One theme controller per app** — never mix `next-themes` and `@heroui/react` `useTheme` in the same app.
- For token/theme variables and custom themes, also use Theming docs / `heroui-styling` as needed.

## Non-Negotiables

| Do | Don't |
|----|--------|
| Toggle theme on `<html>` (`class` and/or `data-theme`) | Expect a `HeroUIProvider` for dark mode |
| Keep `.light` / `.dark` **in sync** with `data-theme` if both are set | Set `class="dark"` but `data-theme="light"` (or reverse) |
| Shell: `bg-background text-foreground` | Hardcoded page canvas colors that ignore theme tokens |
| Next.js: `next-themes` + `suppressHydrationWarning` on `<html>` | SSR theme UI without mount gate (flash / mismatch) |
| Plain React (Vite/CRA): `useTheme` from `@heroui/react` | Use both next-themes and HeroUI `useTheme` together |
| Prefer theme tokens (`bg-surface`, etc.) | Only `dark:` one-offs when tokens already exist |

## Work in This Order

1. **Markup** — Ensure app shell uses theme canvas classes.
2. **Controller** — Next.js → next-themes; plain React → `@heroui/react` `useTheme`.
3. **Persistence / system** — `defaultTheme="system"`, `enableSystem` (or hook default `"system"`).
4. **Switcher UI** — Client component; mount gate for next-themes.
5. **Custom themes** — If CSS uses `data-theme` selectors, set `attribute="data-theme"` and list themes.
6. **Content** — Prefer CSS variables / semantic utilities; `dark:` only for exceptions.

## Decision Rules

### Manual / static dark (no JS library)

```html
<html class="dark" data-theme="dark">
  <body class="bg-background text-foreground">
    <!-- Your app -->
  </body>
</html>
```

Built-in themes respond to **both**:

- Classes: `.light` / `.dark`
- Attributes: `data-theme="light"` / `data-theme="dark"`

### Which controller?

| Stack | Use |
|-------|-----|
| Next.js (App or Pages) | **next-themes** + its `useTheme` |
| Vite / CRA / plain React | **`useTheme` from `@heroui/react`** |

### next-themes (Next.js)

Install: `npm i next-themes` (or pnpm/yarn/bun).

**Provider defaults (built-in light/dark):**

```tsx
<NextThemesProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
  disableTransitionOnChange
>
  {children}
</NextThemesProvider>
```

**App Router:**

- Client `app/providers.tsx` with provider above
- Root layout: `<html lang="en" suppressHydrationWarning>` + `<body className="bg-background text-foreground">` + `<Providers>`

**Pages Router:** wrap in `pages/_app.tsx` with the same provider options.

**Switcher:** `useTheme()` from `next-themes`; `useState`/`useEffect` mount gate; return `null` until mounted; treat `theme === "system"` via `resolvedTheme`.

### Custom theme names

When CSS targets `data-theme` selectors:

```tsx
<NextThemesProvider
  attribute="data-theme"
  defaultTheme="system"
  enableSystem
  themes={["light", "dark", "ocean", "ocean-dark"]}
>
  {children}
</NextThemesProvider>
```

If you pass a custom `themes` list, **include `"light"` and `"dark"`** when you still want built-ins.

### Plain React: `useTheme` from `@heroui/react`

- Stores selection in `localStorage`
- Resolves `"system"` from OS preference
- Applies **both** class and `data-theme` on `<html>`

```tsx
import { Button, useTheme } from "@heroui/react";

const { resolvedTheme, setTheme, theme } = useTheme("system");
```

### Styling for both themes

Theme-aware (automatic via CSS variables):

```tsx
<main className="min-h-screen bg-background text-foreground">
  <section className="bg-surface text-surface-foreground shadow-surface">
    Theme-aware content
  </section>
</main>
```

One-off dark-only:

```tsx
<div className="bg-background text-foreground dark:border-default">
  Custom dark-mode adjustment
</div>
```

## Anti-Patterns

- Mixing next-themes and `@heroui/react` `useTheme` in one app
- Theme switcher that renders different UI on server vs client without mount/`suppressHydrationWarning`
- Forgetting `bg-background` / `text-foreground` on the document shell
- `attribute="class"` while all custom theme CSS is written as `[data-theme=…]` only
- Omitting `light`/`dark` from a custom `themes` array when still needed

## Reference Map

- Full samples: `references/dark-mode.md`
- Official: https://heroui.com/en/docs/react/getting-started/dark-mode
- next-themes: https://github.com/pacocoursey/next-themes
- Sibling skills: `heroui-frameworks` (Next layout/locale), `heroui-styling`, `heroui-design-principles`, `heroui-react`

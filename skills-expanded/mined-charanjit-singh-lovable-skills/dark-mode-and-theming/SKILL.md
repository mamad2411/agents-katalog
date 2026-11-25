---
name: dark-mode-and-theming
description: >-
  Use when adding dark mode, theme toggle, system theme support, or fixing
  hardcoded colors that break in dark mode. Not for design-token migration
  unrelated to dark mode.
---

# Dark mode and theming

Use **CSS variables** + Tailwind's `dark:` variant. Never hardcode `#fff` / `#000` in components.

## Setup (shadcn / Tailwind)

1. `tailwind.config.ts` → `darkMode: ["class"]`
2. `index.css` defines tokens for `:root` and `.dark`:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --primary: 221 83% 53%;
  --primary-foreground: 0 0% 100%;
  --border: 214 32% 91%;
}

.dark {
  --background: 222 47% 11%;
  --foreground: 210 40% 98%;
  --primary: 217 91% 60%;
  --primary-foreground: 222 47% 11%;
  --border: 217 33% 18%;
}
```

3. Components use semantic classes: `bg-background`, `text-foreground`, `border-border` — never `bg-white`.

## Theme provider

```tsx
// next-themes (works with Vite + React too)
<ThemeProvider attribute="class" defaultTheme="system" enableSystem>
  <App />
</ThemeProvider>
```

Persist user choice (localStorage) and respect `prefers-color-scheme` for first visit.

## Theme toggle

```tsx
const { theme, setTheme } = useTheme();
<Button variant="ghost" size="icon" onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
  {theme === "dark" ? <Sun /> : <Moon />}
</Button>
```

For three-state (light / dark / system), use a `DropdownMenu`.

## Audit checklist

- [ ] No literal hex colors in components (`#000`, `rgb(...)`).
- [ ] Images that need it have both light/dark variants or `dark:invert`.
- [ ] Charts use theme-aware colors (read CSS variables in JS or use `currentColor`).
- [ ] No FOUC: theme class applied before first paint (server attribute / inline script).
- [ ] Contrast ≥ 4.5:1 in both themes.

## Avoid

- Two-tree CSS (`light.css` / `dark.css`) — use a single token system.
- Tailwind colors hardcoded in JSX (`bg-gray-900`) when a semantic token exists.
- Forgetting OG/social images that look bad on a dark email client.

Companion: `accessibility-pass` for contrast verification.

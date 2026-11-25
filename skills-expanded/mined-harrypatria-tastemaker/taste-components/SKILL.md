---
name: taste-components
description: Implements accessible, token-themed interfaces with shadcn/ui, Radix and Tailwind CSS (v3 or v4) - app shells, page headers, forms with react-hook-form + zod, data tables with TanStack, charts, overlays, command palette, dark mode - plus a Portable Mode in plain HTML for .NET, Spring and air-gapped stacks. Use when building or restyling components, "use shadcn", "Tailwind", "dark mode", "make this form/table better", or wiring a design system into code.
---

# Taste Components: built, not generated

Consumes `design-tokens.json` / `tokens.css` and `BUILD_MANIFEST.md`. taste-guard checks the result.

## 1. Detect (silently, before writing code)

`package.json` (framework, React major, Tailwind major, existing kit, icons, motion), `components.json` (shadcn style, aliases, cssVariables), `tsconfig` paths (`@/*`), CSS entry. Apply the matching row in `tastemaker/references/stacks.md`. Never add a second kit, icon set or CSS approach.

shadcn missing: `npx shadcn@latest init`, then add only the components used (list them in wire-up notes). `cn()` lives in `lib/utils.ts` (`twMerge(clsx(...))`).

## 2. Theme wiring

Map tokens to shadcn variables with taste-tokens' generated `tokens.css`. Components use only semantic classes: `bg-background text-foreground border-border bg-card text-muted-foreground bg-primary text-primary-foreground ring-ring`. No palette classes (V12), no `dark:` color overrides in components (V18), no raw values (V08). Dark mode: class strategy; `next-themes` in Next.js (`suppressHydrationWarning` on `<html>`), a 15-line provider in Vite.

## 3. Build order

Atoms -> molecules -> organisms -> templates -> pages. Each layer imports only from below. Reuse before create: one `Button` (cva), one `DataTable<T>`, one `Stat`, one `EmptyState`.

Recipes for shells, headers, KPI rows, dashboards, master-detail, settings, auth, forms, tables and charts: `references/recipes.md`. Component choice per need: `references/shadcn-map.md`.

## 4. Non-negotiables

- Interactive elements are `button`, `a`, or Radix primitives; never clickable `div` (U02). Focus traps, menus, tooltips come from Radix, never hand-rolled.
- Icon-only buttons: `aria-label` + `Tooltip` (U01). Lucide icons `aria-hidden`, sized 16/20/24.
- Every async surface renders loading (skeleton at final size), empty, error (retry), success.
- Forms: visible labels, `aria-invalid` + `aria-describedby`, focus first invalid, keep input on server error, submit shows spinner and disables only while pending.
- Motion: `transition-colors duration-150` for hover/focus; transforms behind `motion-safe:`; overlays animate opacity + translate only.
- Elevation: border first; shadow only on overlays (popover, dialog, toast).
- Truncate with `truncate` + `title`, or `line-clamp-*`. Numbers `tabular-nums`, right-aligned.
- Layout: `grid`/`flex` + `gap`, no margin stacks; `min-h-dvh`; container queries for reusable panels.

## 5. Portable Mode

No npm or a server-rendered stack: semantic HTML that mirrors shadcn markup and ARIA, precompiled Tailwind or `tokens.css`, vanilla modules with `data-*` hooks. Fragments and behaviour in `references/portable.md`.

## Quality gate

- [ ] Only semantic token classes; `tastemaker scan` clean.
- [ ] Radix/shadcn for every overlay, menu and focus-managed widget.
- [ ] All states implemented and reachable; dark mode verified per component; no hydration flash.
- [ ] 320 / 768 / 1280 verified; no horizontal page scroll.
- [ ] New dependencies and shadcn components listed in wire-up notes.

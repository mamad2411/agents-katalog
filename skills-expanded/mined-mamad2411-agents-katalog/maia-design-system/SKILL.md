---
name: maia-design-system
description: >
  Maia theme design system for Compass. Read this skill BEFORE creating or
  modifying any UI component, page layout, or styling. Covers tokens, typography,
  color, spacing, component standards, states, motion, and accessibility.
  Applies whenever working on .tsx files, CSS, or anything visual.
---

# Maia Design System Skill

**Read `docs/DESIGN_SYSTEM.md` for the full specification.** This skill is an actionable summary.

## Absolute Rules

1. **shadcn/ui exclusively with the Maia theme.** No other component libraries.
2. **Tokens only.** Use `bg-background`, `text-foreground`, `border-border`, `ring-ring`. Never write `zinc-*` in components.
3. **Inter for UI. Geist Mono for code/numbers.** `font-sans` = Inter. `font-mono` = Geist Mono.
4. **Both modes designed.** Dark mode switches CSS variables in `globals.css`. Components never add `dark:` overrides.
5. **One spacing system.** `gap-6`–`gap-8` sections, `p-4`–`p-6` cards, `space-y-4` forms, `gap-2`–`gap-3` inline.

## When Creating a Page

```tsx
<div className="flex items-start justify-between gap-6">
  <div className="space-y-1">
    <h1 className="text-3xl font-semibold tracking-tight">Title</h1>
    <p className="text-sm text-muted-foreground">Subtitle</p>
  </div>
  <div className="flex items-center gap-2">{/* actions */}</div>
</div>
```

Follow: Header row → Controls row → Content area. Every page, same rhythm.

## When Creating a Component

- Install from shadcn: `bunx shadcn@latest add <component>`
- Use `cn()` from `@/lib/utils` for conditional classes.
- Use semantic tokens for all colors. Check the PR checklist in `docs/DESIGN_SYSTEM.md`.

## Type Scale Quick Reference

| Element | Classes |
|---------|---------|
| Page title | `text-3xl font-semibold tracking-tight` |
| Section title | `text-base font-semibold` |
| Card title | `text-sm font-semibold` |
| Body | `text-sm` |
| Label | `text-xs font-medium` |
| Muted | `text-xs text-muted-foreground` |
| Mono value | `font-mono text-xs tabular-nums` |
| Metric | `text-2xl font-semibold tabular-nums` |

## Button Variants

Only: `default`, `secondary`, `outline`, `ghost`, `destructive`. One primary action per page.

## Tables

Always inside a `<Card>`. Muted header row. Subtle hover. `tabular-nums` on number columns.

## Motion

Use CSS variables: `--motion-fast` (120ms), `--motion-base` (180ms), `--motion-slow` (240ms).
Easing: `--ease-standard: cubic-bezier(0.2, 0, 0, 1)`.
No bounce. No overshoot. No delays.

## Accessibility

- Visible focus ring on every interactive element.
- `<label>` on every input.
- Keyboard nav for nav, tables, dialogs, selects, popovers.
- WCAG AA contrast in light and dark.

---
name: canon-density
description: Use when designing or implementing density modes (compact, default, comfortable), adjusting spacing without changing font sizes, supporting power users who need denser UIs, or adapting layouts for data-heavy vs content-heavy contexts. Trigger when the user mentions density, compact mode, comfortable spacing, or information density.
---

# CANON · Density

Density is spacing, not font size. Changing density means scaling gaps, padding, and row heights while keeping type legible.

## Three density modes

| Mode | Use | Spacing multiplier |
|---|---|---|
| Compact | Power users, data tables, dashboards, admin tools | 0.75× |
| **Default** | Most apps | 1× |
| Comfortable | Content-heavy, reading-focused, onboarding | 1.25× |

## What scales

| Property | Compact | Default | Comfortable |
|---|---|---|---|
| Row height | 32px | 48px | 56px |
| Card padding | 12px | 16px | 24px |
| Button height | 32px | 40px | 48px |
| Input height | 32px | 40px | 48px |
| Gap between items | 8px | 16px | 24px |
| Section spacing | 24px | 40px | 56px |

## What does NOT scale

- **Font sizes.** 14px body stays 14px across all densities. Compact reads the same text; it just packs it tighter.
- **Touch targets on mobile.** 44px floor stays, regardless of density mode. Density modes are desktop-only unless you're building for stylus input.
- **Icon sizes.** Icons stay at their grid-aligned size (16, 20, 24px).
- **Border radius.** Stays consistent.
- **Line height.** Governed by type size, not density.

## Implementation — CSS custom properties

```css
:root {
  --density: 1;
  --space-unit: calc(8px * var(--density));
}
[data-density="compact"]  { --density: 0.75; }
[data-density="comfortable"] { --density: 1.25; }

.card { padding: calc(var(--space-unit) * 2); }
.row { min-height: calc(var(--space-unit) * 6); }
```

Or use discrete scales where continuous math creates half-pixel values.

## User control

- Toggle in settings or toolbar.
- Persist in localStorage.
- Per-view override OK (table might be compact while the page is default).
- Default is "default." Don't auto-compact on small screens — that's responsive design, not density.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Shrinking font size for compact | Illegibility; density is spacing, not type |
| Compact mode on mobile with touch targets < 44px | WCAG 2.5.5 violation |
| Comfortable mode that doubles spacing everywhere | Wastes real estate, looks broken |
| No user toggle | Forces one density on everyone |
| Mixing density modes within a single component | Visual incoherence |

## Audit checklist

- [ ] Three modes defined (compact, default, comfortable)
- [ ] Font sizes unchanged across modes
- [ ] Touch targets ≥ 44px on mobile regardless of density
- [ ] Spacing uses design tokens or CSS calc with density variable
- [ ] User can toggle and choice persists
- [ ] Default mode is the default

## Sources

- Material Design 3 · Layout: applying density
- Atlassian Design System · Spacing and density
- Apple HIG · "Adaptivity and Layout"

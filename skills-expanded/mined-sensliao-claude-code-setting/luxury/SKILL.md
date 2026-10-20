---
name: luxury
description: >-
  Dark-first, typographically bold editorial design system — pure black surfaces, pure white text, oversized Oswald headings, monochromatic hierarchy. Use for fashion, lifestyle, architecture portfolio, high-end e-commerce, photography gallery or premium SaaS landing pages whose identity is built on restraint and exclusivity. Triggers: "luxury / dark editorial / high-end fashion / monochrome bold typography / exclusive premium / architect portfolio / fashion magazine UI".
source: typeui.sh/skills/luxury
license: typeui.sh redistributed; original at https://typeui.sh
---

# Luxury — Dark Editorial Design System

> **DEPRECATED as the standalone L3 pick (2026-06-14)**：暗色奢华改由 Style-Lens registry 的 **`dark-editorial`** lens 承担——修正了本 skill 的三处 AI-tell（纯黑 `#000000` / Oswald 单字体撑全身份 / 零运动语言；详 `uiux-product-orchestrator/references/style-lens-registry.md` §3.1）。本文件**保留**为 `dark-editorial` 的 token 出发点之一 + 向后兼容（旧 `l3_style: luxury` lock 映射到 `dark-editorial`），不再作为 PICK 首选的锁定风格。L3 互斥 `luxury` family 仍存在（`catalog.json` mutex 不变）。

> Source: https://www.typeui.sh (Luxury skill, 2026-03-08)
> Installed: 2026-05-21
> Use this skill when the user asks for **dark editorial / fashion / luxury portfolio / black-and-white bold typography** UI.

---

## 1. Core Philosophy (HARD CONSTRAINT)

1. **Dark-first, not dark-mode.** Black (#000000) is the foundation. Every component, every state, every layout is designed for dark surfaces first and only. **Never** assume a light background or generate a light variant unless explicitly asked.
2. **Typography is the only decoration.** With no color accents and no illustrative elements, Oswald's condensed forms and dramatic weight range carry the entire visual identity. Use scale and weight the way other systems use color.
3. **Monochromatic hierarchy.** Build hierarchy through type size, weight contrast, opacity levels, and spacing. A thin 14px label next to a black 40px heading creates more contrast than any color pairing.
4. **Color as exception.** Success / warning / danger states are the ONLY moments where color appears. This scarcity makes status indicators impossible to miss. Do not introduce decorative accent colors.
5. **Condensed type at scale.** Oswald's narrow letterforms let headings go bigger without overflowing containers. Be typographically dramatic.

---

## 2. Design Tokens (LOCKED)

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| **primary** | `#FAFAFA` | Actions, links, active states — near-white on black |
| **secondary** | `#FAFAFA` | Unified with primary for a strictly monochromatic identity |
| **success** | `#16A34A` | Confirmations, positive feedback — one of the only color moments |
| **warning** | `#D97706` | Caution states, pending actions |
| **danger** | `#DC2626` | Errors, destructive actions |
| **surface** | `#000000` | Backgrounds, cards, containers — pure black |
| **text** | `#FFFFFF` | Body text, headings, labels — pure white |

**Critical rule**: primary == secondary == `#FAFAFA`. AI agent **cannot** rely on color to differentiate elements. Use typography scale, weight, spacing, and subtle opacity shifts instead.

### Typography

- **Display + Body + UI chrome**: **Oswald** (Google Fonts) — condensed sans-serif, weights 100-900
- **Code / monospace only**: **JetBrains Mono** (the sole exception)
- **Type scale**: Desktop-first expressive — go big on headings. 40px / 56px / 72px / 96px / 128px+ are all valid for hero headings.
- **Body**: 14-16px Oswald (light weight 200-300) for editorial feel
- **Labels / UI chrome**: 12-14px Oswald uppercase or wide-tracked

Oswald import:
```css
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&family=JetBrains+Mono:wght@400;500;700&display=swap');
```

### Spacing — 8pt baseline grid

Every margin, padding, and gap aligns to multiples of 8px. On dark interfaces, negative space feels larger — keep layouts **intentionally sparse** rather than accidentally empty.

Allowed values: `8, 16, 24, 32, 48, 64, 80, 96, 128, 160, 192, 256`.

---

## 3. Required Interaction States (per component)

For EVERY interactive element, define:
- default
- hover
- focus-visible (critical on dark surfaces — subtle focus indicators disappear; use clear white 2px outline)
- active
- disabled (use opacity 0.4 on text, not a different color)
- loading
- error

---

## 4. Component Coverage (40+ families)

**Inputs & forms**: buttons, text inputs, selects, comboboxes, checkboxes, radios, switches, textareas, date/time pickers, file uploaders
**Data display**: cards, tables, data lists, data grids, charts, stats/metrics, badges, chips, avatars
**Navigation**: breadcrumbs, pagination, steppers, sidebars, top bars, command palette, tabs
**Overlays**: modals, drawers, sheets, tooltips, popovers, menus
**Feedback**: alerts, toasts, notifications center, progress indicators, skeletons, empty states
**Page-level**: authentication screens, settings pages, documentation layouts, onboarding flows, pricing blocks, search

---

## 5. Accessibility (NON-NEGOTIABLE)

- **Keyboard-first** for every interactive element
- **Visible focus states** on every focusable component — particularly critical on dark surfaces
- **Semantic HTML before ARIA** — native elements first, ARIA only when semantics aren't available
- **44px+ touch targets** — minimum tap size, especially important when visual style is minimal
- **High-contrast mode** support — OS-level high-contrast modes are also respected
- **21:1 contrast ratio** — `#FFFFFF` on `#000000` provides maximum contrast, exceeding WCAG AAA

When opacity reduces a state (disabled / muted), confirm contrast still meets WCAG AA at minimum.

---

## 6. Anti-Patterns (BLOCK)

- ❌ Bright accent colors (purple / cyan / pink gradients)
- ❌ Light gray on white (low contrast)
- ❌ Multiple typefaces (Oswald only, JetBrains Mono only for code)
- ❌ Decorative SVG illustrations / glassmorphism / blur effects beyond functional purposes
- ❌ Inconsistent spacing (anything off the 8pt grid)
- ❌ Ambiguous labels (every label must be testable in code review)
- ❌ Cards-inside-cards-inside-cards nested chrome
- ❌ Generating a "light mode variant" — Luxury is dark-only by definition

---

## 7. When to Use This Skill

✅ Fashion and lifestyle brands
✅ Architecture and design portfolios
✅ High-end product showcases and luxury e-commerce
✅ Photography and visual art galleries
✅ Premium SaaS landing pages where restraint is the brand
✅ Editorial sites that want to feel like a print magazine

## 8. When NOT to Use This Skill

❌ Consumer SaaS dashboard (use `taste-skill` or `frontend-design-pro` Glassmorphism)
❌ Data-heavy admin (use `brutalist-skill` or `apple-design-system`)
❌ B2B fintech (too bold; use `taste-skill` calibrated low DESIGN_VARIANCE)
❌ Healthcare / accessibility-critical apps where users expect light surfaces
❌ Light-mode-required brand systems

---

## 9. Composition with Other Skills

| Pair with | Why |
|---|---|
| `ux-principles` (MODE C audit) | Verify 21:1 contrast holds across all states |
| `luxury-editorial-site-builder` | For full editorial single-page brand sites with hero video; Luxury provides the design tokens, luxury-editorial-site-builder provides the page architecture |
| `imagegen-frontend-web` | Generate hero references that respect the monochrome + Oswald aesthetic |
| `taste-skill` (DESIGN_VARIANCE 1-3, MOTION 2-4) | If user wants a slightly softer luxury feel without going full editorial |
| `theme-factory` | Do NOT mix — Luxury overrides theme-factory's color picks |

---

## 10. Quick Reference — When AI Generates Code

```css
:root {
  --surface: #000000;
  --text: #FFFFFF;
  --primary: #FAFAFA;
  --secondary: #FAFAFA;
  --success: #16A34A;
  --warning: #D97706;
  --danger: #DC2626;
  --space-unit: 8px;
  --font-display: 'Oswald', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

body {
  background: var(--surface);
  color: var(--text);
  font-family: var(--font-display);
  font-weight: 200;
}

h1 {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: clamp(48px, 8vw, 128px);
  line-height: 0.95;
  letter-spacing: -0.02em;
}

button:focus-visible {
  outline: 2px solid var(--text);
  outline-offset: 4px;
}
```

---
name: ub-brand
description: "Apply University at Buffalo brand guidelines to any project — web, print, components, or documentation. Use this skill whenever the user asks about UB colors, UB Blue, Hayes Hall White, Sofia Pro, UB typography, UB brand compliance, design tokens for a UB project, accessibility requirements for UB digital properties, or anything that should look or feel like the University at Buffalo brand. Triggers on UB brand, UB design system, UB style guide, or any request to make something match UB's visual identity."
---

# University at Buffalo Brand Guidelines

This skill is a portable, project-agnostic reference for the UB brand system. Use it
whenever producing work that must comply with University at Buffalo visual identity
standards — regardless of technology stack or output format.

**Reference files bundled with this skill** (read these for complete detail):
- `references/colors.md` — full color palette, accessibility notes, semantic aliases
- `references/typography.md` — fonts, sizes, weights, line heights
- `references/design-tokens.md` — complete CSS custom property token reference

---

## Brand Foundations

### Core Principle

UB Blue (`#005bbb`) and Hayes Hall White (`#ffffff`) are the dominant colors in any
UB-branded work. Every other color exists as an accent — no secondary color should
become the dominant hue for a page, section, or unit.

### Primary Palette

| Color Name | Hex | Role |
|------------|-----|------|
| UB Blue | `#005bbb` | Primary brand color — CTAs, headers, dominant fills |
| Hayes Hall White | `#ffffff` | Background, negative space |
| Bulls Black | `#000000` | Default body text |

### Secondary Palette — Accessibility at a Glance

Most secondary colors **cannot** be used for text on a white background and fail
WCAG contrast requirements. Only these four pass:

| Color Name | Hex | ✅ Text on White |
|------------|-----|-----------------|
| Capen Brick | `#990000` | Yes |
| Niagara Whirlpool | `#006570` | Yes |
| Harriman Blue | `#002f56` | Yes |
| Townsend Gray | `#666666` | Yes |

For the complete secondary palette with all hex values and use-case guidance, read
`references/colors.md`.

### Typography

| Font | Role | Web Fallback |
|------|------|-------------|
| Sofia Pro | Sans-serif — headings, UI labels, navigation | Arial, sans-serif |
| More Pro | Serif — body text, long-form, formal contexts | Georgia, serif |
| Freeland / Kievit | Display — large headlines only, use sparingly | — |

Font sizes follow a modular scale (base 16px, ratio 1.25): 12px → 14px → 16px →
18px → 20px → 24px → 30px → 36px → 48px. Full scale with token names is in
`references/typography.md`.

---

## Design Token System

When implementing the UB brand in CSS, use the `--ub-*` custom property naming
convention. This makes designs themeable and keeps brand values centralized.

**Naming pattern:** `--ub-{category}-{name}[-{modifier}]`

| Category | Purpose | Example |
|----------|---------|---------|
| `color` | Brand colors and semantic aliases | `--ub-color-blue`, `--ub-color-primary` |
| `font` | Font family stacks | `--ub-font-sans`, `--ub-font-serif` |
| `text` | Font sizes | `--ub-text-base`, `--ub-text-xl` |
| `weight` | Font weights | `--ub-weight-bold` |
| `space` | Spacing (8px grid) | `--ub-space-4` (16px), `--ub-space-8` (32px) |
| `radius` | Border radius | `--ub-radius-md`, `--ub-radius-full` |
| `shadow` | Box shadows | `--ub-shadow-md`, `--ub-shadow-lg` |
| `transition` | Animation timing | `--ub-transition-fast` (150ms) |
| `z` | Z-index scale | `--ub-z-modal` (400) |

Prefer semantic aliases (`--ub-color-primary`, `--ub-color-text`) over raw palette
tokens (`--ub-color-blue`, `--ub-color-black`) so that the intent is clear and
theming works correctly. The full token list is in `references/design-tokens.md`.

---

## Accessibility Requirements

All UB digital properties must meet **WCAG 2.2 Level AA**:

- **Text contrast**: 4.5:1 minimum for normal text; 3:1 for large text (≥18px regular or ≥14px bold)
- **Non-text contrast**: 3:1 for UI components and graphical elements
- **Color alone**: never use color as the only means of conveying information — always pair with an icon, label, or pattern
- **Focus visibility**: keyboard focus must be visible on all interactive elements; never suppress `:focus-visible` without providing a replacement style
- **Keyboard access**: all interactive elements must be operable via keyboard alone

UB Blue (`#005bbb`) on white passes 4.29:1 — acceptable for large/bold text but tight
for normal body text. Use Harriman Blue (`#002f56`, 13.8:1) or Bulls Black for body copy.

---

## Brand Usage Rules

1. **Dominant colors are UB Blue and white.** Secondary colors accent — they don't lead.
2. **Never use non-accessible secondary colors for text** (Letchworth Autumn, Solar Strand, Greiner Green, Lake LaSalle, Bronze Buffalo, Olmsted Green, Victor E. Blue, Baird Point).
3. **Display fonts sparingly.** Freeland/Kievit is for large headlines only — not body, labels, or UI.
4. **Serif (More Pro) for long-form content.** Use Sofia Pro everywhere else.
5. **Spacing on an 8px grid.** All margins, paddings, and gaps should be multiples of 8px.
6. **Never hardcode brand values.** Implement via `--ub-*` CSS custom properties so the brand is maintainable and overridable.

---

## Quick Reference: Semantic Color Aliases

These aliases carry intent and should be preferred in any implementation:

| Token | Maps To | Use |
|-------|---------|-----|
| `--ub-color-primary` | UB Blue `#005bbb` | Primary actions, links, active states |
| `--ub-color-primary-dark` | Harriman Blue `#002f56` | Hover/pressed on primary |
| `--ub-color-text` | Bulls Black `#000000` | Body text |
| `--ub-color-text-muted` | Townsend Gray `#666666` | Secondary / helper text |
| `--ub-color-bg` | Hayes Hall White `#ffffff` | Page background |
| `--ub-color-border` | Baird Point `#e4e4e4` | Default borders |
| `--ub-color-danger` | Capen Brick `#990000` | Errors, destructive actions |
| `--ub-color-success` | Olmsted Green `#6da04b` | Confirmations, success states |
| `--ub-color-warning` | Solar Strand `#ffc72c` | Warnings (icon/text backup required) |
| `--ub-color-info` | Victor E. Blue `#2f9fd0` | Informational states |
| `--ub-color-focus-ring` | UB Blue `#005bbb` | Keyboard focus outline |

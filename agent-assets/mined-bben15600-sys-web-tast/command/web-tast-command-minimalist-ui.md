# Minimalist UI Design Skill

## Philosophy

Minimalism is not emptiness — it is **maximum signal with minimum noise**. Every element removed increases the weight of what remains. Before adding, ask: does this help the user accomplish their goal?

## Color System

**Monochromatic base** — one neutral family, one accent maximum:
```css
:root {
  --bg:      #FAFAFA;   /* near-white — warmer than pure white */
  --surface: #FFFFFF;
  --border:  #E8E8E8;
  --txt1:    #111111;   /* primary text */
  --txt2:    #555555;   /* secondary */
  --txt3:    #999999;   /* tertiary / placeholder */
  --accent:  #0066FF;   /* single brand color */
}
/* Dark mode: invert brightness, keep saturation low */
```

**Rules:**
- Max 2 colors on any single screen (neutral + accent).
- No gradient backgrounds — reserve gradients for micro highlights only.
- Borders: `1px` only, never `2px+` decorative.
- No box shadows for decoration — only for elevation (modal, dropdown).

## Typography as Structure

In minimalist design, type IS the layout:
```css
/* Type scale — 4 sizes maximum */
--text-xs:  12px; /* metadata, captions */
--text-sm:  14px; /* secondary body */
--text-md:  16px; /* body — base */
--text-lg:  20px; /* section labels */
--text-xl:  28px; /* page headings */
--text-2xl: 40px; /* hero */

/* Weight — only 2 */
font-weight: 400; /* body */
font-weight: 600; /* headings, labels */

/* Never use font-weight: 300 or 700+ in minimalist UIs */
```

Font choice: geometric sans (Inter, DM Sans, Plus Jakarta) or humanist serif for editorial (Lora, Fraunces). Never decorative fonts.

## Spacing — Generous is Non-Negotiable

```css
/* 8-point grid, skew generous */
--space-xs:  8px;
--space-sm: 16px;
--space-md: 24px;
--space-lg: 40px;
--space-xl: 64px;
--space-2xl: 96px;

/* Minimum padding for content containers */
padding: 24px 32px; /* never less than 16px */
```

Rule: when unsure between two spacing values, always choose the larger one.

## Layout Principles

- **Generous margins** — content should feel like it has room to breathe.
- **Single-column default** — resist multi-column until content genuinely needs it.
- **Left-align everything** — centered text only for very short hero text.
- **Grid alignment is invisible structure** — align elements to a consistent grid even when the grid itself is invisible.
- Max content width: `640px` for text, `960px` for layouts.

## Decoration Rules

**Allowed:**
- 1px border lines
- Subtle background tints (`bg-neutral-50`)
- Thin dividers (`border-t border-neutral-100`)

**Forbidden:**
- Decorative icons that don't add information
- Background patterns / textures
- Rounded corners > `8px` (exception: pill buttons `border-radius: 999px`)
- Colored backgrounds on sections (except full-page dark mode)
- Underlines for visual style (only for actual links)

## Motion — Less is More

```css
/* Minimalist animation rule: one transition property, short duration */
transition: opacity 150ms ease-out;
transition: transform 200ms ease-out;

/* Never animate multiple properties simultaneously in minimalist UI */
/* Exception: opacity + transform together (GPU-accelerated) */
transition: opacity 150ms ease-out, transform 200ms ease-out;
```

Interactions: hover state is a slight opacity change (`0.7`) or color shift — never a shadow or transform on content.

## Component Approach

| Component | Minimalist pattern |
|---|---|
| Button | No border-radius or `border-radius: 4px`. Outlined secondary. No icon unless critical. |
| Card | No shadow. `border: 1px solid var(--border)`. No `border-radius` > 8px. |
| Input | Underline-only or clean border. No filled background. |
| Table | No cell borders — only row dividers. |
| Navigation | Left sidebar or top bar. No icons without labels. Max 5 items. |
| Modal | Center-aligned, max-width 520px. Dark overlay `rgba(0,0,0,0.4)`. |

## Checklist Before Shipping

- [ ] Can any element be removed without losing information?
- [ ] Is every color used intentional (not decorative)?
- [ ] Does typography alone create sufficient hierarchy?
- [ ] Is whitespace consistent with the spacing scale?
- [ ] Are there any gradients / shadows that don't serve elevation?
- [ ] Does the design hold in monochrome?

---
name: depth-ui
description: Applies depth-driven layered color and shadow principles to elevate average UI into polished, readable interfaces for both light and dark themes. Use when improving or reviewing UI components, setting up a design token system, applying consistent depth and shadow to an interface, or making a flat or inconsistent UI feel more refined without a full redesign.
---

# depth-ui

You are an expert UI engineer and design collaborator. When this skill is activated, improve the target UI by applying depth and layering correctly — raising it from average to good-tier with minimal changes, while preserving clarity, accessibility, and consistency.

## When to use

Activate this skill when asked to:
- Improve or review a UI component, page, or design system
- Apply consistent depth, shadow, or layering to an interface
- Set up or audit a theme token system (light + dark)
- Make a flat or inconsistent UI feel more polished without a full redesign

## Instructions

### Core Principles (Depth + Layering)

- Use 3–4 shades of the same neutral or brand color to create layers: background (base), containers (mid), interactive elements (top), and highlights.
- Increase lightness progressively between layers using small deltas (e.g., 6–10 in HSL or 4–8 in OKLCH lightness) to build subtle hierarchy.
- Compose shadows with both:
  - A soft inset highlight near the top edge (suggests incident light from above)
  - A darker outer/bottom shadow (suggests elevation)
- Prefer smaller, subtler shadows by default; only increase radius/offset on hover/active or for high-priority elements.
- Not every element should "pop." Mix flat, inset, and elevated states intentionally to guide attention.
- Implement token-based theming; provide both light and dark tokens and verify parity in both. Do not hardcode color values.

### Accessibility and Legibility

- Maintain WCAG 2.1 AA contrast for text and critical controls.
- If layering mutes content (e.g., a lighter container dims an icon or label), raise text/icon lightness or adjust contrast tokens.
- Avoid over-shading progress indicators or low-salience elements — clarity beats ornamentation.

### When to Elevate

- Elevate interactive controls, primary CTAs, selected tabs/cards, and focused inputs.
- De-emphasize tables and large canvases using darker inset shadows and a darker base to imply depth/sink.
- Use hover/active states to increase elevation slightly (larger shadow, brighter highlight) without changing layout.

### Cautions

- Don't add depth to everything. Overuse is noisy and inconsistent.
- Keep progress bars visually obvious — distinct fill color, minimal gap shadows.
- Avoid mixing 3+ visual languages (flat + inset + elevated) in the same micro-context unless hierarchy demands it.
- Remove borders where color layering already separates planes.

### Implementation Checklist

1. **Theme tokens** — Define `bg/base`, `bg/mid`, `bg/top`, `text/default`, `text/muted`, `border/subtle`. Define shadow tokens for `small`, `elevated`, `inset` in both light and dark variants. Use OKLCH for perceptual uniformity.
2. **Containers** — Base page uses `bg/base`. Cards/grids use `bg/mid`; interactive sub-elements use `bg/top`. Remove borders where layer contrast suffices.
3. **Shadows** — Elevated: dark bottom shadow + subtle top inset highlight. Sunken: dark inset top + light inset bottom.
4. **States** — Selected/active: slightly brighter background + stronger small shadow. Hover: modestly larger shadow radius and offset.

### Token naming convention and combined shadow pattern

The non-obvious part is naming tokens consistently and composing the two-part shadow. Here's the minimal pattern:

```css
:root {
  /* Light — OKLCH deltas: base < mid < top (steps of ~4–8 lightness) */
  --bg-base: oklch(0.96 0 0);
  --bg-mid:  oklch(0.93 0 0);
  --bg-top:  oklch(0.98 0 0);
  --shadow-small: 0 1px 2px rgba(0,0,0,.08), 0 2px 4px rgba(0,0,0,.06);
  --inset-top-light: inset 0 1px 0 rgba(255,255,255,.75);
}

/* Card: mid layer + combined inset highlight and outer shadow */
.card {
  background: var(--bg-mid);
  border-radius: 12px;
  box-shadow: var(--inset-top-light), var(--shadow-small);
}
```

Mirror `--bg-*` and `--shadow-*` tokens under `[data-theme="dark"]` with inverted lightness values and higher shadow opacity (e.g., `rgba(0,0,0,.55)`).

### Design Review Prompts

Use these to audit a UI after applying the skill:

- Is every element elevated? If yes, reduce — only elevate prioritized interactive elements.
- Does the table feel "sunken" relative to cards and controls?
- Did we preserve AA contrast for text/icons after layering?
- Are hover/active elevation changes subtle and consistent?
- Did we remove unnecessary borders where layer contrast already separates planes?
- Is the progress bar unmistakably read as progress (distinct fill, minimal gap, high contrast)?

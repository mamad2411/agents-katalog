---
name: heroui-colors
description: >
  Apply HeroUI v3 semantic color roles and CSS variables: accent, default, success,
  warning, danger, foreground/muted, background surfaces, form fields, separators,
  borders, primitives (oklch). Covers soft/hover derived tokens via color-mix,
  light/dark defaults, overrides, custom colors with @theme inline, and Tailwind
  utilities (bg-accent, text-foreground). Keywords: HeroUI colors, --accent, oklch,
  semantic tokens, Theme Builder, variables.css. Use when the user runs /heroui-colors.
---

# HeroUI Colors (v3)

Semantic color palette and theming tokens for HeroUI v3. Prefer **intent roles** over large raw palettes; most derived values (hover, soft) come from a few base variables.

**Source:** https://heroui.com/en/docs/react/getting-started/colors  
**Raw MDX:** https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(handbook)/colors.mdx  
**Default theme file:** https://github.com/heroui-inc/heroui/blob/v3/packages/styles/themes/default/variables.css  
**Visual builder:** https://heroui.com/themes

## Apply the Skill

- Read `references/colors.md` for full token tables, default `:root` / `.dark` CSS, and customization recipes.
- Use semantic utilities (`bg-accent`, `text-foreground`, `bg-surface`) before hard-coded hex/rgb.
- Pair with `heroui-dark-mode` for switching; `heroui-styling` for className/BEM application; `heroui-design-principles` for semantic *intent* of UI variants.

## Non-Negotiables

| Do | Don't |
|----|--------|
| Semantic roles: accent, default, success, warning, danger | Random Tailwind palette colors for brand/status by default |
| Base + foreground pairs (`--accent` / `--accent-foreground`) | Hard-code foreground at the component level |
| Theme tokens for canvas (`bg-background text-foreground`) | Page backgrounds that ignore CSS variables |
| Surface for cards/panels; overlay for floating layers | Use overlay tokens for in-flow cards (or reverse) |
| Field tokens for inputs (`--field-*`) | Style inputs like primary buttons with `--accent` fill by default |
| Primitives (`--white`, `--snow`, `--eclipse`) as foundations | Treat primitives as light/dark-switching semantic UI roles |
| Override in `:root` / `.dark` / `[data-theme="dark"]` | Fork every component color prop for a rebrand |

## Work in This Order

1. **Role** — Pick semantic intent (accent action, neutral default, status, surface, field).
2. **Token pair** — Base + foreground (and soft/hover if needed).
3. **Utility or CSS** — `bg-*` / `text-*` or `var(--*)`.
4. **Theme mode** — Confirm light + dark values (or rely on defaults).
5. **Customize** — Override bases or add `@theme inline` custom roles.
6. **Builder (optional)** — Theme Builder → export CSS for large visual rethemes.

## Decision Rules

### Philosophy

- Colors communicate **purpose and state**, not decoration.
- Visual variation comes from **scale, emphasis, context**, and derived mixes — not dozens of one-off hexes.
- Most UI is built from a **small set of base variables**; hover/soft are often `color-mix` derivatives.

### Role map

| Role | Purpose | Use sparingly? |
|------|---------|----------------|
| **Accent** | Brand / primary emphasis, key actions | Yes |
| **Default** | Neutral non-emphasized UI | No — backbone |
| **Success** | Positive outcomes, validation | Status only |
| **Warning** | Caution, non-destructive risk | Status only |
| **Danger** | Destructive / critical / errors | Strict consistency |
| **Foreground** | Text & icons (readable) | Never hard-code at component |
| **Background** | Page canvas, quiet contrast | Quiet |
| **Surface** | Cards, panels, in-flow containers | Hierarchy via elevation |
| **Overlay** | Tooltips, modals, menus (floating) | Contrast vs surface in dark |
| **Field** | Inputs / form controls | Distinct from buttons |
| **Separator / Border** | Structure, low noise | Low contrast |
| **Primitive** | Mode-agnostic foundations | Not semantic UI by themselves |

### Naming convention

- Base: `--accent`, `--success`, …
- On-color text: `--accent-foreground`, …
- Soft fills: often `--color-*-soft` via mix with transparent
- Hover: `--color-*-hover` or utilities like `bg-accent-hover`
- Tailwind: `--color-*` mapped so classes are `bg-accent`, `text-accent-foreground`

### Default accent (example values from docs)

| Token | Light (typical) |
|-------|-----------------|
| `--accent` | `oklch(0.6204 0.195 253.83)` |
| `--accent-foreground` | `var(--snow)` |
| Soft | ~15% accent + transparent |
| Soft hover | ~20% accent + transparent |
| Hover solid | mix accent 90% + accent-foreground 10% |

Status bases (light): success / warning / danger as oklch in reference; danger foreground often snow; success/warning foreground often eclipse.

### Surfaces vs overlay

- **Surface** — cards, accordions, disclosure (in layout).
- **Overlay** — floating layers; dark mode overlay is slightly lighter than surface for contrast.

### Form fields

Use field tokens (`--field-background`, `--field-foreground`, `--field-placeholder`, `--field-border`) so inputs keep a distinct language from buttons.

### How to use in UI

```tsx
<div className="bg-background text-foreground">
  <button className="bg-accent text-accent-foreground hover:bg-accent-hover">
    Click me
  </button>
</div>
```

```css
.my-component {
  background: var(--accent);
  color: var(--accent-foreground);
  border: 1px solid var(--border);
}

@layer components {
  .button {
    @apply bg-accent text-accent-foreground;
    &:hover,
    &[data-hovered="true"] {
      @apply bg-accent-hover;
    }
  }
}
```

### Customizing

**Override:**

```css
:root {
  --accent: oklch(0.7 0.15 250);
}
[data-theme="dark"] {
  --accent: oklch(0.8 0.12 250);
}
```

Convert at [oklch.com](https://oklch.com).

**Add colors + Tailwind:**

```css
:root,
[data-theme="light"] {
  --info: oklch(0.6 0.15 210);
  --info-foreground: oklch(0.98 0 0);
}
.dark,
[data-theme="dark"] {
  --info: oklch(0.7 0.12 210);
  --info-foreground: oklch(0.15 0 0);
}
@theme inline {
  --color-info: var(--info);
  --color-info-foreground: var(--info-foreground);
}
```

```tsx
<div className="bg-info text-info-foreground">Info message</div>
```

Theme auto-switches with `class="dark"` or `data-theme="dark"` (see `heroui-dark-mode`).

## Anti-Patterns

- Large ad-hoc color palettes instead of roles
- Hard-coded text colors that break in dark mode
- Overusing accent (flattens hierarchy)
- Using danger/warning for decoration
- Mixing overlay and surface roles incorrectly
- Adding custom colors without `@theme inline` (utilities missing)
- Editing only light `:root` and ignoring dark

## Reference Map

- Full tokens, default theme CSS, soft/hover mixes: `references/colors.md`
- Official: https://heroui.com/en/docs/react/getting-started/colors
- Default variables: packages/styles themes default `variables.css` (v3 branch)
- Theme Builder: https://heroui.com/themes
- Tailwind v4 theme: https://tailwindcss.com/docs/theme
- Sibling skills: `heroui-dark-mode`, `heroui-styling`, `heroui-design-principles`, `heroui-react`

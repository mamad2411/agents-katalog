---
name: practica-brand-design
description: Practica brand design system with colors, typography, spacing, and component patterns. Use when building or styling any UI for Practica — pages, components, layouts, blog posts, or landing pages. Ensures visual consistency with the established minimal, clean design language.
license: MIT
metadata:
  author: practica
  version: "1.0"
---

# Practica Brand Design System

A minimal, clean design system for the Practica consultancy brand. Apply these guidelines to every UI element to maintain visual consistency across pages and projects.

## Design Philosophy

- **Minimal and clean** — generous whitespace, no visual clutter
- **Professional but approachable** — soft shadows, smooth transitions, rounded corners
- **Content-first** — typography optimized for readability, muted chrome
- **Light theme only** — no dark mode

## Quick Reference

| Token | Value |
|-------|-------|
| Font | Inter (300–800) via Google Fonts |
| Primary/Accent | Teal — `oklch(0.68 0.12 199)` (~#0d9488) |
| Background | Light gray — `oklch(0.91 0.004 265)` (~#f8f9fa) |
| Text | Near-black — `oklch(0.16 0 0)` |
| Card surface | White — `oklch(1 0 0)` |
| Muted text | Medium gray — `oklch(0.45 0 0)` |
| Border | Light gray — `oklch(0.87 0.005 265)` |
| Base radius | 0.75rem (12px) |
| Max content width | `max-w-6xl` (sections), `max-w-[52rem]` (articles) |

## Tech Stack

- **Tailwind CSS v4** — configured inline in `src/index.css` (no `tailwind.config.js`)
- **shadcn/ui** — "new-york" style, neutral base color, lucide icons
- **CSS Variables** — all tokens as OKLCH values in `:root`
- **`cn()` utility** — from `@/lib/utils` for conditional class merging

## Font

**Inter** — loaded from Google Fonts with weights 300, 400, 500, 600, 700, 800.

Add to your HTML `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
```

CSS variable:

```css
--font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
```

## Color Palette

All colors use OKLCH format. Define these as CSS variables in `:root`:

```css
:root {
  --background: oklch(0.91 0.004 265);    /* light gray page bg */
  --foreground: oklch(0.16 0 0);          /* near-black text */
  --card: oklch(1 0 0);                   /* white card surfaces */
  --card-foreground: oklch(0.16 0 0);
  --primary: oklch(0.68 0.12 199);        /* teal accent */
  --primary-foreground: oklch(1 0 0);     /* white on primary */
  --secondary: oklch(0.94 0.015 199);     /* light teal */
  --secondary-foreground: oklch(0.2 0 0);
  --muted: oklch(0.93 0.003 265);         /* subtle gray bg */
  --muted-foreground: oklch(0.45 0 0);    /* gray text */
  --accent: oklch(0.93 0.015 199);        /* light teal bg */
  --accent-foreground: oklch(0.2 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.87 0.005 265);
  --input: oklch(0.87 0.005 265);
  --ring: oklch(0.68 0.12 199);           /* focus ring = primary */
  --radius: 0.75rem;
}
```

### Using colors in Tailwind

Reference via semantic classes: `bg-background`, `text-foreground`, `bg-primary`, `text-primary`, `bg-card`, `text-muted-foreground`, `border-border`.

For tinted variants use opacity: `text-foreground/85`, `bg-primary/10`, `border-primary/30`.

## Typography

### Headings

| Level | Classes |
|-------|---------|
| H1 (hero) | `text-5xl md:text-6xl lg:text-7xl font-bold leading-tight tracking-tight` |
| H2 (section) | `text-4xl md:text-5xl font-bold tracking-tight` |
| H3 (subsection) | `text-xl md:text-2xl font-semibold` |
| Section label | `text-sm font-semibold uppercase tracking-widest text-primary` |

### Body text

| Variant | Classes |
|---------|---------|
| Primary | `text-lg leading-relaxed text-muted-foreground` |
| Blog prose | `text-lg leading-[1.85] text-foreground/85 space-y-6` |
| Metadata | `text-sm text-muted-foreground` |

### Blog prose elements

| Element | Classes |
|---------|---------|
| Prose H2 | `mb-8 mt-20 text-2xl md:text-3xl font-bold tracking-tight` |
| Blockquote | `border-l-4 border-primary/30 pl-6 italic text-foreground/70` |
| Inline code | `rounded bg-foreground/[0.06] px-1.5 py-0.5 text-[0.88em] font-mono` |
| Link | `text-primary underline-offset-4 hover:underline` |
| Ordered list | `ml-1 list-inside list-decimal space-y-4 marker:font-semibold marker:text-primary` |
| Unordered list | `ml-1 list-inside list-disc space-y-3 marker:text-primary` |
| Code block | `my-6 overflow-x-auto rounded-lg bg-foreground/[0.04] p-5 text-sm leading-relaxed font-mono` |

## Spacing

### Section padding

- **Vertical:** `py-24` to `py-28` for major sections
- **Horizontal:** `px-8` (desktop), `px-4` (mobile)

### Container widths

- `max-w-6xl mx-auto` — standard sections
- `max-w-3xl mx-auto` — narrow content
- `max-w-[52rem] mx-auto` — blog article body

### Component spacing

- Card padding: `p-6` to `p-10`
- Flex gaps: `gap-4` to `gap-8`
- Grid gaps: `gap-8` to `gap-12`

## Component Patterns

### Buttons

Primary CTA buttons are **pill-shaped**:

```
rounded-full px-6 py-2.5 text-sm font-medium
```

Larger variant:

```
rounded-full px-8 py-3.5 text-base font-medium
```

Use shadcn `Button` variants: `default` (primary), `outline` (secondary), `ghost` (navigation).

### Cards

Standard card pattern with hover lift:

```
rounded-2xl bg-background p-8 md:p-10 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg
```

Base shadcn card: `rounded-xl border shadow-sm`.

### Badges

Category badges:

```
rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-primary
```

### Navigation

- Header: `sticky top-0 z-50 bg-card/80 backdrop-blur-md`
- Nav links: `text-sm font-medium text-muted-foreground transition-colors hover:text-foreground`
- Mobile nav: `text-lg font-medium text-foreground transition-colors hover:text-primary`

### Code blocks (decorated)

```
overflow-hidden rounded-2xl border border-border
```

With a top bar showing three dots (red/yellow/green) and filename, then `p-6 md:p-8` for code content.

## Interaction Patterns

- **Hover lift:** `hover:-translate-y-1` on cards
- **Hover shadow:** `hover:shadow-lg` or `hover:shadow-md`
- **Color transitions:** `transition-colors` for links, `transition-all duration-300` for cards
- **Focus ring:** Uses `--ring` (teal) via shadcn defaults

## Layout Structure

Every page follows this skeleton:

```tsx
<div className="flex min-h-screen flex-col bg-background text-foreground">
  <Header />       {/* sticky, blur backdrop */}
  <main className="flex-1">
    {/* Hero section */}
    <section className="py-28 px-8">
      <div className="mx-auto max-w-6xl text-center">...</div>
    </section>
    {/* Content sections alternate bg */}
    <section className="py-24 px-8 bg-card">
      <div className="mx-auto max-w-6xl">...</div>
    </section>
  </main>
  <Footer />
</div>
```

Sections alternate between transparent (shows `bg-background` gray) and `bg-card` (white).

## Border Radius Scale

| Token | Value |
|-------|-------|
| `--radius-sm` | 8px |
| `--radius-md` | 10px |
| `--radius-lg` | 12px (base) |
| `--radius-xl` | 16px |
| `--radius-2xl` | 20px |
| `--radius-3xl` | 24px |

Common usage: `rounded-xl` / `rounded-2xl` for cards, `rounded-full` for buttons and badges, `rounded-lg` for code blocks.

## Shadow Scale

- `shadow-sm` — default card rest state
- `shadow-md` — subtle hover
- `shadow-lg` — prominent hover

## Responsive Breakpoints

- **Mobile-first** approach
- `md:` (768px) — tablet and up
- `lg:` (1024px) — desktop and up
- Common patterns: `hidden md:block`, `md:grid-cols-2`, `lg:grid-cols-3`

## Checklist for New Pages

1. Use Inter font (verify Google Fonts link is in `<head>`)
2. Set `bg-background text-foreground` on the root layout
3. Use teal (`primary`) as the only accent color
4. Cards on white (`bg-card` or `bg-background`), page bg is light gray
5. Pill-shaped CTA buttons (`rounded-full`)
6. Generous vertical padding (`py-24`+) between sections
7. Content capped at `max-w-6xl`; articles at `max-w-[52rem]`
8. Hover effects: lift (`-translate-y-1`) + shadow on interactive cards
9. Section labels: uppercase, tracked, teal
10. No dark mode — light theme only

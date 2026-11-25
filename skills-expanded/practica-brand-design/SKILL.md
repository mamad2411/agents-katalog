---
name: practica-brand-design
description: Practica brand design system with colors, typography, spacing, and component patterns. Use when building or styling any UI for Practica — pages, components, layouts, blog posts, or landing pages. Ensures visual consistency with the established minimal, clean design language.
license: MIT
metadata:
  author: practica
  version: "1.0"
---

# Practica Brand Design System

Stack: Tailwind v4, shadcn/ui (new-york style), OKLCH CSS vars in `:root`, `cn()` from `@/lib/utils`. Light theme only.

## Quick Reference

| Token | Value |
|-------|-------|
| Font | Inter (300–800) via Google Fonts |
| Primary/Accent | Teal — `oklch(0.68 0.12 199)` |
| Background | Light gray — `oklch(0.91 0.004 265)` |
| Text | Near-black — `oklch(0.16 0 0)` |
| Card surface | White — `oklch(1 0 0)` |
| Muted text | `oklch(0.45 0 0)` |
| Border | `oklch(0.87 0.005 265)` |
| Base radius | 0.75rem |
| Max width | `max-w-6xl` (sections), `max-w-[52rem]` (articles) |
| Section padding | `py-24`–`py-28 px-8` |

Colors via semantic classes: `bg-background`, `text-foreground`, `bg-primary`, `bg-card`, `text-muted-foreground`, `border-border`. Tinted: `text-foreground/85`, `bg-primary/10`, `border-primary/30`.

## Typography

| Level | Classes |
|-------|---------|
| H1 | `text-5xl md:text-6xl lg:text-7xl font-bold leading-tight tracking-tight` |
| H2 | `text-4xl md:text-5xl font-bold tracking-tight` |
| H3 | `text-xl md:text-2xl font-semibold` |
| Section label | `text-sm font-semibold uppercase tracking-widest text-primary` |
| Body | `text-lg leading-relaxed text-muted-foreground` |
| Blog prose | `text-lg leading-[1.85] text-foreground/85 space-y-6` |
| Metadata | `text-sm text-muted-foreground` |

### Blog Prose Elements

| Element | Classes |
|---------|---------|
| Prose H2 | `mb-8 mt-20 text-2xl md:text-3xl font-bold tracking-tight` |
| Blockquote | `border-l-4 border-primary/30 pl-6 italic text-foreground/70` |
| Inline code | `rounded bg-foreground/[0.06] px-1.5 py-0.5 text-[0.88em] font-mono` |
| Link | `text-primary underline-offset-4 hover:underline` |
| ol | `ml-1 list-inside list-decimal space-y-4 marker:font-semibold marker:text-primary` |
| ul | `ml-1 list-inside list-disc space-y-3 marker:text-primary` |
| Code block | `my-6 overflow-x-auto rounded-lg bg-foreground/[0.04] p-5 text-sm leading-relaxed font-mono` |

## Components

- **Button (CTA):** `rounded-full px-6 py-2.5 text-sm font-medium` — shadcn variants: `default` / `outline` / `ghost`
- **Card:** `rounded-2xl bg-background p-8 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg`
- **Badge:** `rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-primary`
- **Nav header:** `sticky top-0 z-50 bg-card/80 backdrop-blur-md`
- **Nav link:** `text-sm font-medium text-muted-foreground transition-colors hover:text-foreground`

## Layout

Page root: `flex min-h-screen flex-col bg-background text-foreground`. Sections alternate `bg-background` (gray) / `bg-card` (white). Cards use `rounded-xl`/`rounded-2xl`; buttons/badges use `rounded-full`. Hover: `hover:-translate-y-1 hover:shadow-lg`.

For full CSS setup (Tailwind v4 `@theme`, `:root` vars, shadcn `components.json`): see `references/css-tokens.md`.

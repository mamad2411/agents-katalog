---
name: shadcn-app-design
description: Build clean, minimal tool/utility/dashboard UIs using the shadcn/ui dark aesthetic (21st.dev style). Use when the brief is a tool, app, utility, or dashboard — NOT a landing page or marketing site.
---

# shadcn/ui Application Design

> For tools, utilities, dashboards, and application UIs. Not landing pages. Not marketing sites.
> This is the **positive** skill — when the brief is a tool/app, reach for THIS, not the taste/landing-page skills.

## When to Use This Skill

Load this skill when the brief is:
- A developer tool (prompt builder, code generator, API explorer)
- A utility app (converters, calculators, search tools)
- A dashboard or admin panel
- A data-display or configuration interface
- Any single-page app that does a job, not tells a story

## When NOT to Use

Do NOT load this skill for:
- Landing pages, marketing sites, portfolios → use `design-taste-frontend`
- Creative/experimental brand pages → use `high-end-visual-design`
- Editorial, kinetic-type, Awwwards-style → use `gpt-taste`

**Critical pitfall**: The taste skills (design-taste-frontend, high-end-visual-design, gpt-taste) prescribe glassmorphism, noise textures, double-bezel cards, radial gradients, and cinematic motion. Those are WRONG for tools. Applying taste-skill aesthetics to a tool app produces the exact kind of over-designed AI slop the user rejected here. Tools need to be clean, flat, functional, and invisible — the tool gets out of the way.

## Core Design System

Based on shadcn/ui dark theme + 21st.dev production values.

### Colors (oklch — copy-paste into Tailwind v4)

```css
--background: oklch(0.141 0.004 285.824);    /* near-black, slight cool */
--foreground: oklch(0.968 0.001 286.375);    /* near-white text */
--muted: oklch(0.21 0.006 285.883);           /* dark gray surfaces */
--muted-foreground: oklch(0.552 0.012 286.067); /* secondary text */
--border: oklch(0.274 0.005 286.033);          /* subtle borders */
--primary: oklch(0.485 0.291 264.121);         /* violet/purple accent */
--ring: oklch(0.485 0.291 264.121);            /* focus rings = primary */
--destructive: oklch(0.45 0.2 20);             /* red for errors */
```

### Typography

- Body: `text-[13px]` or `text-sm` (0.8125rem)
- Labels: `text-[11px]` uppercase tracking-wider
- Headings: `text-[15px]` font-semibold tracking-tight
- Monospace for code/output: `text-[12px]` font-mono
- Font: system sans-serif stack OR Geist Sans (lite, no weights you don't need)
- **Do not** bundle full font families with 10 weights — 44KB max CSS total

### Cards & Containers

```css
/* Pattern */
rounded-lg                    /* 8px — not 12px, not 16px */
border                        /* 1px solid */
border-[--border]/70          /* subtle, not harsh */
bg-transparent                /* or bg-[--muted] for elevated */
shadow-none                   /* no shadows by default */
```

- Focus: `focus:border-primary/50 focus:ring-1 focus:ring-primary/30`
- No glassmorphism. No backdrop-blur. No noise textures.
- No double-bezel / nested card architecture.
- No radial gradient orbs in the background.

### Buttons

```css
/* Primary */
bg-foreground text-background  /* inverted — white on dark */
rounded-lg px-4 py-2.5         /* compact */
text-[13px] font-medium
hover:opacity-90

/* Secondary / Ghost */
bg-transparent border border-border/70
text-muted-foreground
hover:bg-muted hover:text-foreground
rounded-md px-3 py-1.5
text-[12px]
```

### Inputs

```css
rounded-lg border border-border/50 bg-transparent
px-4 py-3 text-[13px]
placeholder:text-muted-foreground/50
focus:border-primary/50 focus:ring-1 focus:ring-primary/30
```

### Layout

- Max width: `max-w-[1200px] mx-auto` (or 1400px for data-heavy tools)
- Section padding: `px-4 sm:px-6 py-8`
- Gaps: `gap-4` between major sections, `gap-3` within a section
- Grid: `grid-cols-1 lg:grid-cols-2` for split-panel tools
- Form labels above inputs, never placeholder-as-label
- Empty states: centered, icon + short message, no complex illustration

### Output Panel Pattern

```
┌─ Toolbar (border-b, muted bg, action buttons) ─┐
│  Label · chars            [Copy] [Export]       │
├─ Content (scrollable, monospace) ──────────────┤
│  pre-wrap, break-words                          │
│  text-[12px] leading-relaxed font-mono          │
└────────────────────────────────────────────────┘
```

### Format Tabs (when switching between output modes)

```css
/* Active tab */
text-foreground border-b-2 border-primary
/* Inactive tab */
text-muted-foreground border-transparent hover:text-foreground
```

Underline + color change. No pill backgrounds. No card per tab.

### Anti-Patterns (BANNED for tools)

1. **Glassmorphism** — `backdrop-blur`, glass cards, noise textures
2. **Double-bezel cards** — nested rounded containers with inset highlights
3. **Radial gradient orbs** — ambient mesh backgrounds
4. **Cinematic motion** — staggered reveals, scroll-triggered animations, GSAP
5. **Eyebrow labels on every section** — maximum 0 eyebrows in a tool UI
6. **Over-designed heroes** — tools don't need heroes
7. **Emoji in UI** — use icons from a library
8. **Purple/blue AI gradients** — one accent color, flat

## Quick Reference

- `references/21st-dev-tokens.md` — exact CSS values from 21st.dev in production
- `references/nextjs-link-event-handlers.md` — fix for Next.js 14 Link+event handler static generation failures
- `references/campaign-dashboard-patterns.md` — sidebar layout, stat cards, data tables, coverage grid, CSV export, status badges (production-tested)

## Verification Checklist

Before shipping a tool UI:
- [ ] Background is near-black oklch(0.141), not pure #000
- [ ] Cards have 1px subtle border, no glass, no shadow
- [ ] One accent color (violet/purple default)
- [ ] Text is 13px body, 11px labels, 15px headings
- [ ] Focus rings on all inputs
- [ ] Empty state, loading state, error state all implemented
- [ ] No noise textures, no backdrop-blur, no radial gradients
- [ ] Responsive sidebar: hidden on mobile, slide-in drawer, backdrop, auto-close on route change
- [ ] Keyboard shortcut support (⌘↵ for submit)
- [ ] Copy + export actions where relevant

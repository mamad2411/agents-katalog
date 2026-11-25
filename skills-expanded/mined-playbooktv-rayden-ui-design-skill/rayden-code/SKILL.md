---
name: rayden-code
version: 2.0.0
description: >
  Generate React code using Rayden UI components with correct props, design
  tokens, and premium layout patterns. Use when building pages, features, or
  prototypes with the Rayden UI component library. Prevents hallucinated
  components and props.
argument-hint: "[page-type|component-name|description]"
allowed-tools: Read Write Edit Bash Glob Grep
effort: high
---

# Rayden Code Skill

Generate production-quality React code using the Rayden UI component library.
Every output must use documented components with correct props, follow design
token classes, and produce premium, minimal, clean UI.

**Task:** `$ARGUMENTS`

---

## Before Writing Any Code

Read the complete rules file — it contains every component, every prop, every
token, and every design pattern you need:

- **[RAYDEN_RULES.md](RAYDEN_RULES.md)** — Full component API reference, design philosophy, layout patterns, anti-patterns, color tokens, typography scale, and final checklist

**Do not skip this step.** The rules file is the source of truth. If a component
or prop is not in that file, it does not exist.

---

## Workflow

### Step 1 — Understand the Request

Parse the user's request:
- What type of page or feature? (dashboard, landing, auth, settings, table, form, etc.)
- Is there a Figma reference or screenshot to match?
- What components will be needed?
- What's the data model?

### Step 2 — Load Rules

Read `RAYDEN_RULES.md` from this skill's directory. Pay attention to:
1. **Core Rules** (section 2) — what you must and must not do
2. **Design Philosophy** (section 3) — the 5 pillars of Rayden UI design
3. **Component API** (sections 7+) — exact props for each component
4. **Anti-Patterns** (section 6) — explicitly banned patterns
5. **Design Patterns by Context** — reference layouts for common page types

### Step 3 — Plan the Layout

Before writing code, state your plan:
- Page structure (shell, sections, content areas)
- Components you'll use (from the documented list only)
- Design decisions (spacing, color strategy, elevation strategy)

### Step 4 — Generate Code

Write React + Tailwind CSS code following these rules:

**Imports:**
```tsx
import { /* only components you use */ } from '@raydenui/ui';
import '@raydenui/ui/styles.css';
```

**Design token classes** — use Tailwind classes, not hex values:
- Colors: `bg-primary-500`, `text-grey-900`, `border-grey-200`
- Typography: `text-h3`, `text-body-md`, `text-caption-sm`
- Shadows: `shadow-soft-xs`, `shadow-soft-sm`
- Spacing: `p-6`, `space-y-8`, `gap-4`

**Layout principles:**
- Generous whitespace (`p-6`+ containers, `space-y-6`+ sections)
- Clear visual hierarchy (title → subtitle → body → meta)
- Color restraint (one primary action per section, neutral base)
- Consistent radius and elevation per section
- Content width always constrained (`max-w-*`)
- Responsive breakpoints (`sm:`, `md:`, `lg:`)

### Step 5 — Self-Validation

Run through the Final Checklist from RAYDEN_RULES.md before presenting code:

**Correctness:**
- Every component exists in the rules file
- Every prop is documented for that component
- Using token classes, not hex values
- Compound components nest correctly
- Icon-only buttons have `aria-label`

**Design Quality:**
- Generous whitespace
- Clear visual hierarchy
- Color used with restraint
- Consistent radius and elevation
- Content width constrained
- Headings use `tracking-tight`, descriptions use `leading-relaxed`
- Numbers formatted with separators

---

## Hard Rules (never break these)

1. **Only documented components** — if it's not in RAYDEN_RULES.md, it doesn't exist
2. **Only documented props** — never invent props
3. **Token classes only** — `bg-primary-500` not `#EB5017`
4. **One primary action per section** — rest are outlined or text
5. **No colored container backgrounds** — cards are always `bg-white`
6. **No gradient text** — never use `bg-clip-text text-transparent`
7. **Content width always constrained** — use `max-w-*`
8. **Compound components nest correctly** — Table → TableHeader → TableRow → TableHead

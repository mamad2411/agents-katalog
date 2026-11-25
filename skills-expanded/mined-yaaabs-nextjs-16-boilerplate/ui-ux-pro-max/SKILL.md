---
name: ui-ux-pro-max
description: UI/UX design standards for this stack (Tailwind v4 + shadcn/ui). Use whenever creating or modifying any page, component, layout, or style — the goal is professional, consistent UI with zero AI slop.
---

# UI/UX Pro Max

Generic AI-generated UI is recognizable and cheap-looking: purple gradient heroes, emoji
bullet lists, inconsistent spacing, five shades of gray that almost match. This skill
exists to prevent that. The bar is: **a designer could have made this.**

## Component rules

- **shadcn/ui first.** Before writing any UI element, check `src/components/ui/`. Need a
  component that isn't there? Install it: `npx shadcn@latest add <component>` — never
  hand-roll a button, dialog, or dropdown that shadcn provides.
- **Compose, don't fork.** Build feature components in `src/components/` out of the
  primitives in `src/components/ui/`. Don't edit the primitives except to extend variants
  via `class-variance-authority`.
- **Use `cn()` from `@/lib/utils`** for conditional classes — never string concatenation.

## Design tokens, not raw values

- Colors: use the semantic tokens (`bg-background`, `text-foreground`, `text-muted-foreground`,
  `bg-primary`, `border-border`, `bg-card`...) — **never** raw palette classes like
  `text-gray-500` or hex values. Tokens are what make dark mode work for free.
- Spacing: stick to the 4px scale (`gap-2`, `gap-4`, `p-6`, `py-12`...). Pick from a small
  set per page — three spacing values used consistently beat eight used randomly.
- Radius: use the token-driven `rounded-lg`/`rounded-md`/`rounded-xl` consistently; don't
  mix radii on sibling elements.
- Type scale: one `h1` per page. Establish hierarchy with `text-sm`/`base`/`lg`/`xl`/
  `3xl`-`5xl` + `font-medium`/`semibold`/`tracking-tight` — not with color alone.

## Anti-slop rules (hard bans)

- No decorative emoji in product UI. Icons come from `lucide-react`, sized `size-4`/`size-5`.
- No gradient text, no `bg-gradient-to-r from-purple-500 to-pink-500` heroes.
- No placeholder copy like "Lorem ipsum" or "Your amazing app" — write real, specific copy.
- No centered-everything: use deliberate alignment; left-aligned text for reading.
- No drop shadows heavier than `shadow-sm` unless the element genuinely floats.
- No animation without purpose; if animating, use subtle transitions (`transition-colors`).

## Layout & responsiveness

- Constrain content: `max-w-*` + `mx-auto` + horizontal padding (`px-4 sm:px-6`).
- Mobile-first: write base styles for small screens, add `sm:`/`md:`/`lg:` upward.
- Test both themes: every surface must look intentional in light AND dark mode.

## Accessibility (non-negotiable)

- Interactive elements are `<button>`/`<a>` (or shadcn equivalents) — never clickable divs.
- Every image has meaningful `alt` (or `alt=""` if decorative).
- Every form input has a label. Focus states stay visible — never remove outlines
  without replacement (`focus-visible:ring-*`).
- Color contrast ≥ 4.5:1 for text; don't convey state by color alone.

---
name: darkmatter
description: "The darkmatter design system — a dark-first, terminal-inspired UI language (Geist Mono display type, pure-black OKLCH canvas, zinc structure, per-product accent colors, and signature glow/beam effects) built on shadcn/ui, Radix UI, Tailwind CSS v4, and React 19. Use this whenever building any darkmatter app or UI such as landing pages, product pages, dashboards, docs/blog, forms, navigation, or any screen that should look and feel like darkmatter. This is the canonical source for darkmatter components, tokens, theming, fonts, and layout — prefer it over generic shadcn/ui."
metadata:
  v0.kind: design-system
---

# darkmatter design system

darkmatter is the dark-first, terminal-inspired design system behind darkmatter.io. Its identity: a pure-black OKLCH canvas, zinc structural grays, Geist Mono monospace as the display/brand voice (light-weight and single-case at large sizes), Geist for body copy, Montserrat for headings, Lora for long-form prose, per-product accent colors, and a set of signature glow/beam/spotlight effects. It is a **shadcn/ui-style copy-in library** (Radix UI + Tailwind v4 + `cva`), not an npm package.

**This design system is the canonical UI source for darkmatter apps.** Prefer it over generic shadcn/ui or ad-hoc styling. When something isn't covered here, match the tokens and patterns below rather than inventing new ones.

## Setup — you're already on the starter

New chats start from the validated starter (this skill's `assets/starter`), so the wiring is already done:

- `components/ui/*` — the full 55-component library, imported via `@/components/ui/*`.
- `lib/utils.ts` — the `cn()` helper. Always use it to merge classes.
- `app/globals.css` — Tailwind v4 `@theme` + all design tokens (imported in the root layout).
- `app/layout.tsx` — fonts + `ThemeProvider` (forced dark) already mounted.
- `hooks/` — `use-mobile`, `use-toast`.

**Build on it.** Add routes under `app/`, compose from `@/components/ui/*`, and use tokens. Do not re-scaffold, re-create the theme, or re-wire fonts/provider.

## Hard rules

- **Dark only.** darkmatter is single-theme (dark). `:root` defines only the dark palette and `ThemeProvider` forces `defaultTheme="dark"`. Never add a light theme or a light/dark toggle unless the user explicitly asks.
- **Use tokens, never raw values.** Style with semantic Tailwind classes wired to tokens (`bg-background`, `bg-card`, `text-foreground`, `text-muted-foreground`, `border-border`, `bg-primary`, `bg-destructive`). Never hard-code hex/oklch colors. See `references/foundations/colors.md`.
- **Type is part of the brand.** Monaspace Neon (`font-mono`) is the display/brand voice — use it for hero headings, labels, and terminal-style UI. Geist (`font-sans`, body default), Montserrat (`font-heading` / `.font-sans-secondary`), Lora (`font-serif`, long-form prose). See `references/foundations/typography.md`.
- **Compose from `components/ui/*` via `@/`.** Import by path (`@/components/ui/button`), not from a package. There is no darkmatter npm package.
- **Respect accessibility built into Radix.** Keep labels wired to inputs, dialog titles present, and don't strip `sr-only` text or focus rings.
- **Never invent** component names, props, variants, token names, or asset names. Verify against source (`components/ui/*` in the starter, or the mounted repo). Mark anything genuinely unverifiable `[VERIFY]`.

## Responsiveness

darkmatter uses **Tailwind v4's default breakpoints** (`sm` 40rem, `md` 48rem, `lg` 64rem, `xl` 80rem, `2xl` 96rem) plus the `useIsMobile()` hook (`@/hooks/use-mobile`, 768px threshold) for JS-driven cases (e.g. the sidebar). Build mobile-first with responsive utility variants; use the container pattern (`mx-auto max-w-6xl px-4`) for page width. Full details and the sidebar pattern: `references/foundations/responsiveness.md`.

## Routing map — read before building

- Colors, tokens, product accents, glow/effect colors → `references/foundations/colors.md`
- Font families, type scale, brand voice → `references/foundations/typography.md`
- Spacing, layout, containers, radii → `references/foundations/spacing-layout.md`
- Breakpoints + responsive primitives → `references/foundations/responsiveness.md`
- Motion / animation tokens → `references/foundations/motion.md`
- Full component inventory → `references/components/index.md`
- Buttons & actions → `references/components/buttons.md`
- Forms & inputs → `references/components/forms.md`
- Feedback (alert, toast/sonner, progress, skeleton) → `references/components/feedback.md`
- Data display (card, table, badge, avatar, tabs, accordion) → `references/components/data-display.md`
- Navigation (nav-menu, sidebar, breadcrumb, menus, dock) → `references/components/navigation.md`
- Overlays (dialog, sheet, drawer, popover, tooltip, hover-card) → `references/components/overlays.md`
- Signature effects (glow, beams, spotlight, wobble, evervault) → `references/components/effects.md`
- Logos & assets → `references/assets/logos.md`
- Screen-level composition patterns → `references/patterns.md`
- Worked examples → `references/examples/`

## Final checks

Before finishing any darkmatter UI:
1. Only tokens/semantic classes — no raw colors, no hard-coded widths.
2. Dark theme intact — no light-mode styling or toggle introduced.
3. Components imported from `@/components/ui/*`; classes merged with `cn()`.
4. Brand type applied — Monaspace Neon (`font-mono`) for display/brand moments.
5. Responsive via Tailwind variants + container pattern; verified at mobile and desktop.

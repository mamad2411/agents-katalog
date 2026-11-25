---
name: saas-landing-builder
description: Build the SaaS landing page in `sites/<slug>/` once the brand is approved. Auto-activate when `approval.json.approved === true` and the user asks for a landing page, website, marketing site, or runs `/build-landing`. Generates a Next.js + Tailwind + Framer Motion app, wires Higgsfield-generated hero motion + feature micro-animations, writes SaaS copy from `brand.json` + `saas-context.json`, and ALWAYS places a `<Waitlist />` section at the bottom.
---

# SaaS Landing Builder

You are Step 4 — the final step. You ship a runnable Next.js landing page that converts visitors into waitlist signups.

## Preconditions (hard)

Before doing anything else, verify:
1. `brands/<slug>/approval.json.approved === true` — if not, defer to `saas-brand-approval`.
2. `brand.json`, `saas-context.json`, `brand-guidelines.md` all exist.
3. `mcp__higgsfield__*` tools are reachable — if not, stop and report.

## Output

The exact file tree is specified in [`templates/landing/STRUCTURE.md`](../../templates/landing/STRUCTURE.md). **Generate every file fresh** — there is no source code to copy. STRUCTURE.md is a spec, not a template.

## Build procedure

### 1. Scaffold

Generate the file tree fresh under `sites/<slug>/` following [`templates/landing/STRUCTURE.md`](../../templates/landing/STRUCTURE.md):
- Create directories listed in the spec.
- Write each file using brand-aware content (palette → `tailwind.config.ts`, fonts → `app/layout.tsx`, copy → `copy-writer`).
- `package.json.name` = `<slug>-landing`. Dependencies per STRUCTURE.md.

There are no source files to copy. Every file is authored by you, per-brand.

### 2. Generate Higgsfield motion assets

Call `mcp__higgsfield__generate_video` for each:
- **Hero loop** — 6–10s ambient loop matching brand mood. Will be used as `<video autoplay muted loop playsinline>` background.
- **Animated logo reveal** — short reveal of the primary logo (from `approval.primaryLogo`). Used in the nav on first scroll.
- **3 feature micro-loops** — one per Feature card. Small, 3–5s each, looping cleanly.

Save MP4s under `sites/<slug>/public/motion/`. See [animation-rules.md](animation-rules.md) for prompt patterns and constraints.

### 3. Copy generation

For every text string on the page, draw from `brand.json` + `saas-context.json`. Use [copy-rules.md](copy-rules.md).

Delegate to `agents/copy-writer.md` for full-page copy in one pass — it keeps voice consistent.

### 4. Section assembly

Follow [section-recipes.md](section-recipes.md) for the exact section order and what each must contain:

1. **Nav** — logo + single CTA scrolling to `#waitlist`
2. **Hero** — headline, sub, primary CTA, Higgsfield hero loop
3. **Problem / Promise** — 1 sentence each
4. **How it works** — 3 steps with small animated illustrations
5. **Features** — 3–6 cards with scroll-triggered reveals + feature micro-loops
6. **Social proof** — logos / testimonials slot (or "coming soon")
7. **Pricing teaser** — "Founding pricing at launch — join waitlist"
8. **FAQ** — 4–6 SaaS-relevant questions
9. **Waitlist** — bottom, mandatory
10. **Footer** — minimal: brand + waitlist nudge + year

### 5. Wire the waitlist backend

Delegate adapter choice + wiring to `saas-waitlist-backend`. Default: local JSON file (no external deps). If `SUPABASE_URL` + `SUPABASE_ANON_KEY` exist in env, use Supabase.

### 6. Smoke check

After scaffolding:
- `bun install` (or `npm install`)
- `bun run build` — must compile cleanly
- Print to chat: `cd sites/<slug> && bun dev` to run

## End-of-step message

> *"Landing page ready at `sites/<slug>/`. Run `cd sites/<slug> && bun dev` and open http://localhost:3000. Waitlist posts to: {backend}. Higgsfield motion assets live under `public/motion/`."*

## Hard rules

1. **Waitlist at the bottom, always.** `<Waitlist />` is the second-to-last child of `<main>`, with `<Footer />` after it. Removing it is a defect.
2. **Hero motion via Higgsfield.** If you can't generate one, the hero gets a static fallback BUT you must surface the issue to the user.
3. **`prefers-reduced-motion` honored.** Every animated component checks `useReducedMotion()` from Framer Motion and serves still alternatives.
4. **No lorem ipsum.** All copy from `brand.json` + `saas-context.json`. Sections with no source data say "TBD — content slot" explicitly, not filler.
5. **Tailwind tokens from `brand-guidelines.md`.** Map the palette into `tailwind.config.ts` `theme.extend.colors`.
6. **Type pairing from `brand-guidelines.md`.** Load via `next/font` in `app/layout.tsx`.

## Delegation

- Heavy build (multiple file writes, Higgsfield calls, install) → `agents/landing-builder.md`.
- Copy writing pass → `agents/copy-writer.md`.

## Related

- [section-recipes.md](section-recipes.md)
- [animation-rules.md](animation-rules.md)
- [copy-rules.md](copy-rules.md)
- [../higgsfield-recipes/SKILL.md](../higgsfield-recipes/SKILL.md)
- [../saas-waitlist-backend/SKILL.md](../saas-waitlist-backend/SKILL.md)
- `templates/landing/STRUCTURE.md` — the file-tree spec (no code, just structure)

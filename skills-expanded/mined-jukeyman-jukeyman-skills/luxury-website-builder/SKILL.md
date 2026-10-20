---
name: luxury-website-builder
description: Generate complete, production-ready, ultra-premium websites valued from $10K to $500K+ using the Next.js 16 + React 19.2 + Tailwind 4.3 stack with glassmorphism 3.0, bento grids, kinetic typography, GSAP + Motion animations, shadcn/ui, and WCAG 2.2 AA/AAA accessibility. Use this skill whenever the user asks to build, scaffold, generate, or design a premium/luxury/high-end/agency-tier website, marketing site, SaaS landing page, e-commerce storefront, portfolio site, real-estate site, corporate site, or any website where the request implies elevated design quality — even if they don't literally say "luxury" (phrases like "make it feel expensive", "agency-level", "$50K website", "premium look", "world-class design", "Awwwards-worthy", or "high-end brand site" all qualify). Also trigger for luxury website audits, design-system generation for premium brands, or when converting a Figma/spec into a Next.js 16 luxury build.
---

# Luxury Website Builder

You are generating a website that a real agency would invoice $10K–$500K+ for. Every output must justify that price — not with fluff, but with real production-ready code, a real design system, real accessibility, real performance. No MVPs. No "TODO: add later". No lorem ipsum in shipped code.

## When to fire

Trigger on any request to build/scaffold/generate a website where the ask is premium, high-end, agency-grade, or where the user names one of the eight covered verticals (see `references/verticals.md`). If the user just wants a quick throwaway page, this skill is overkill — say so and offer a lighter path.

## The non-negotiables

Every site you generate MUST hit all of these before you call it done. If you can't, stop and say what's blocking.

- **Stack:** Next.js 16 (App Router, Turbopack, `use cache`, `proxy.ts`) + React 19.2 + Tailwind CSS 4.3 + TypeScript strict. No older versions.
- **Design:** One coherent design system — tokens for color, type, spacing, motion — before you write any pages. Use the luxury palette in `references/design-system.md` unless the user gives you a brand kit.
- **Components:** shadcn/ui + Radix primitives. Never hand-roll a Dialog / Popover / Combobox that Radix already ships.
- **Motion:** Motion (Framer Motion 11+) for component-level, GSAP 3.13+ for scroll-linked / kinetic type. Presets live in `references/animations.md` — copy from there, don't reinvent easings.
- **Accessibility:** WCAG 2.2 AA minimum, AAA where feasible. The new 2.2 criteria (focus-not-obscured, target size ≥ 24×24, accessible auth) are part of the bar, not aspirational. See `references/accessibility.md`.
- **Performance:** Lighthouse Perf ≥ 95, A11y = 100, Best Practices = 100, SEO = 100. LCP < 2.5s, CLS < 0.1, INP < 200ms. If you can't hit it, the site isn't done.
- **Structure:** Match the file layout in `references/file-structure.md` exactly — App Router, `components/{ui,layout,sections,effects,forms,cards}`, `lib/hooks`, `types`. Deviating breaks downstream expectations.

## Workflow

Work in this order. Don't skip forward — each step feeds the next.

1. **Clarify the ask in ONE pass.** Vertical (SaaS / e-comm / portfolio / real estate / healthcare / hospitality / corporate / tech-startup), brand (colors, fonts, tone, or "use luxury default"), page inventory, must-have integrations (Stripe? contact form? newsletter?). Pick sensible defaults for anything they don't answer — do NOT run a five-question gauntlet. State your defaults in one line and move.

2. **Pick the vertical playbook.** Read `references/verticals.md` for the section list, feature set, and value range for the vertical they picked. Every vertical has a required section inventory — hit it.

3. **Lock the design system.** Write `tailwind.config.ts` + `app/globals.css` with the token set (from `references/design-system.md` or the user's brand). This is done BEFORE any page code — pages consume tokens, they don't define them.

4. **Scaffold the file tree.** Match `references/file-structure.md`. Include every directory even if some start empty — the skeleton signals "real build" vs "prototype".

5. **Build sections, not pages.** Compose pages from atomic section components in `components/sections/`. Hero, features, testimonials, pricing, CTA, FAQ, etc. Each section is self-contained, typed, animated, accessible.

6. **Wire animations from presets.** Pull from `references/animations.md` — `fadeUpOnScroll`, `staggerContainer`, `textReveal`, `magneticButton`, `pageTransition`. Don't ship a site without at least: scroll-reveal on primary sections, stagger on card grids, and a hero entrance.

7. **Bake in the effects layer.** `components/effects/` gets glass-morphism, gradient-blur, particle-background, scroll-reveal, magnetic-button, parallax-layer. Not every site uses all of them — pick 2–3 signature effects per site so it feels crafted, not template-y.

8. **Accessibility pass before you call it done.** Run the `references/accessibility.md` checklist. Keyboard nav all interactive elements, focus visible, alt text meaningful, target sizes ≥ 24×24, forms have labels + inline errors + no cognitive-test auth. This is a pass/fail gate.

9. **Performance pass.** `next/image` everywhere (no `<img>`), `next/font` (no external `<link>`), `next/script` (no inline), Suspense boundaries around async trees, dynamic imports for heavy client components, Turbopack default. Verify against the Core Web Vitals targets in `references/performance.md`.

10. **Deploy config.** Ship a `vercel.json` (default), `netlify.toml`, or `amplify.yml` per `references/deployment.md`. Include security headers (X-Frame-Options DENY, X-Content-Type-Options nosniff, HSTS, CSP).

11. **Docs.** `README.md` with local-dev + deploy steps, `.env.example` (never commit `.env`), `CHANGELOG.md`. If it's ≥ $50K tier, add `docs/ARCHITECTURE.md` and `docs/DESIGN-SYSTEM.md`.

## Value framing (only when the user asks about pricing or scope)

Don't volunteer this. If the user asks what a build is worth, or wants to scope by tier, use `references/value-matrix.md` — it has the component-by-component rate breakdown and the vertical value ranges. Frame it as "this is what an agency would charge", not "this is what I charge".

## What NOT to do

- **Don't ship MVPs disguised as luxury.** Placeholder content, missing states (loading / empty / error), untested forms — all disqualifying. A luxury site with a broken contact form isn't luxury.
- **Don't use pages/ directory, `middleware.ts`, external `<link>` tags for fonts, `<img>`, or bcrypt.** These are all pre-Next-16 patterns.
- **Don't invent design tokens mid-build.** If the spacing scale is 4/8/12/16/24/32/48/64, use those — don't sprinkle 13px and 27px "because it looked right".
- **Don't skip dark mode.** `next-themes` wired from the jump, both palettes tested. Any luxury site without dark mode looks 2019.
- **Don't fabricate testimonials, stats, or client logos.** Leave clearly-marked placeholders (`{{TESTIMONIAL_1_QUOTE}}`) if the user hasn't given content — never ship fake social proof as real.

## Reference files

Read the one you need, don't front-load them all:

- `references/verticals.md` — the 8 website verticals: sections, features, value ranges
- `references/design-system.md` — luxury palette, typography scale, spacing, radii
- `references/file-structure.md` — exact directory tree + purpose of each folder
- `references/animations.md` — GSAP + Motion presets ready to copy
- `references/accessibility.md` — WCAG 2.2 checklist (AA + AAA)
- `references/performance.md` — Lighthouse targets + Core Web Vitals + optimization patterns
- `references/deployment.md` — Vercel / Netlify / Amplify configs + security headers
- `references/value-matrix.md` — component-level pricing (only surface when asked)

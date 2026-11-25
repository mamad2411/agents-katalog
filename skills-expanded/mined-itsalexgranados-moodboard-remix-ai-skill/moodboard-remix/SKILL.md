---
name: moodboard-remix
description: UX/UI design partner that sources real, copyable building blocks from 21st.dev, React Bits and Uiverse. Depending on the need it proposes 4 website templates to build a digital product on, 5 components per feature (picking the best-fitting one for each), or 5 themes/styles with a live preview of the user's existing UI rendered in each. Asks a few short preference questions first to lock in the style. Use whenever the user wants to design, redesign, restyle or "make prettier" a site, app, landing page, dashboard or SaaS; asks for templates, starters, components, UI blocks, themes, color palettes or visual styles; mentions 21st.dev, React Bits, Uiverse or shadcn themes; or asks "what should this look like", even without saying "skill" or "design".
---

# Moodboard Remix

You help the user pick and assemble a UI from proven, copyable sources instead of inventing everything from scratch. You work in three modes and always show options visually before committing to anything.

| Mode | Output | Primary source |
|---|---|---|
| **Templates** | 4 full-site templates to build the product on | 21st.dev templates |
| **Components** | 5 candidates per feature, with a recommended pick for each | 21st.dev components, React Bits, Uiverse |
| **Themes** | 5 themes/styles, each previewed on what the user has already built | 21st.dev themes |

Source URLs, URL patterns, install commands and access quirks are in `references/sources.md`. The feature → category lookup table is in `references/feature-map.md`. How to build previews is in `references/previews.md`. Read the relevant file when you reach the step that needs it.

## Step 1 — Read the context before asking anything

Spend a minute looking so you don't ask what you could find out:

- Is there an existing project in the working directory? Check `package.json` (React? Next.js? Vite? Tailwind v3/v4? shadcn — look for `components.json`), the global CSS file (CSS variables like `--background`, `--primary`), and the main pages/screens.
- Is there a running dev server or a `.claude/launch.json`? That is what you will preview themes on.
- What did the user already say about the product, audience, or taste?

## Step 2 — Pick the mode

Infer it from the request when you can:

- "Starting from zero", "I need a site for X", "landing / portfolio / SaaS / store" → **Templates**
- "I need a pricing table / login / navbar / chat / hero / feature X" → **Components**
- "Change the look", "restyle", "colors", "make it feel more premium/playful", "dark mode", existing UI to reskin → **Themes**

If it's genuinely ambiguous, make the mode the first question in Step 3. Modes chain naturally: Templates → Themes → Components is the full path for a new product; offer the next mode at the end of each one.

## Step 3 — Ask a few preference questions (one round, max 4)

Use `AskUserQuestion` with **one batch of 3–4 questions**. Only ask what you couldn't infer in Step 1. Recommend an option when context points to one. Pick from this bank:

1. **Product & audience** (skip if known) — e.g. SaaS/B2B tool, consumer app, portfolio/personal brand, e-commerce/local business.
2. **Visual personality** — Minimal & clean · Bold & expressive · Warm & friendly · Premium/luxury · Technical/brutalist.
3. **Color mood** — Monochrome/neutral · Dark with neon accent · Soft pastels · Earthy/natural · Brand color (they'll type it in "Other").
4. **Motion level** — Subtle (fades, hovers) · Noticeable (scroll reveals, animated text) · Showpiece (WebGL, shaders, cursor effects).
5. **Stack constraint** (only if no project exists) — React + Tailwind + shadcn (best fit for all sources) · Plain HTML/CSS (favours Uiverse) · Other.
6. **Reference** — "Any site whose look you love?" — offer this as free text via "Other" on another question rather than a separate question.

Turn the answers into a one-line **style brief** and state it back, e.g. *"Brief: B2B analytics SaaS · minimal & technical · monochrome with one electric-blue accent · subtle motion · Next.js + Tailwind + shadcn."* Every pick from here on is justified against this brief.

## Step 4 — Source candidates

Browse the real catalogs — never recommend something from memory without checking it still exists. Read `references/sources.md` for URL patterns and access notes. In short:

- Use `WebFetch` for 21st.dev and React Bits listings and detail pages.
- **Uiverse blocks WebFetch (403)** — use the built-in browser (`mcp__Claude_Browser__*`: `navigate` + `get_page_text`/`find`) for it. Also use the browser when you need to *see* a preview (screenshot) or when a page renders client-side and WebFetch returns little.
- Gather more than you need (≈2× the final count), then cut down against the brief.

For each candidate record: name, author, source, URL, a one-line description of what it looks like/does, licence, and dependencies (framer-motion, three.js, GSAP…). Internally also note whether you'll install/copy it or replicate it — that's your working detail, never shown to the user (see "What the user sees").

## Step 5 — Present options visually

Text lists aren't enough for design decisions. Build one comparison page per round (see `references/previews.md`) and show it to the user (publish it as an Artifact, or open it in the browser pane if the user prefers to stay local). Then summarise in chat.

### Templates mode → exactly 4

Pick 4 that are meaningfully *different* routes (not 4 near-identical SaaS landings): e.g. one safest fit, one bolder, one minimal, one wildcard. For each: screenshot/preview image, name + link, stack, which pages it includes, why it fits the brief, what you'd have to change. End with your recommendation.

### Components mode → 5 per feature, with a pick

1. Break the requested functionality into its UI **features** (e.g. "onboarding" → stepper, form inputs, progress, success state). Use `references/feature-map.md` to find the right category on each source.
2. For each feature, find **5 candidates mixing sources** where possible (21st.dev for full sections/shadcn blocks, React Bits for animated/expressive pieces, Uiverse for small CSS elements like buttons, toggles, loaders, checkboxes).
3. Mark one as **★ Recommended for this feature** and explain why it wins *in combination with the others you picked* — consistent radius, motion language, density, and dependency footprint matter more than each piece being individually the flashiest. Flag combinations that clash (e.g. a WebGL hero next to a brutalist table).
4. If the user didn't name the features, ask which ones (multi-select) in the Step 3 question round, plus which existing style to preview them on.
5. The preview page shows each feature with its 5 candidates, rebuilt live and interactive in the project's own tokens and markup (see `references/previews.md` → Components mode), the current version as a reference, and the recommended one highlighted.

### Themes mode → exactly 5, previewed on the user's UI

1. Pick 5 themes from 21st.dev themes that span the brief's range (e.g. 2 close fits, 2 adjacent, 1 contrast option).
2. Extract each theme's tokens (colors for light + dark, radius, fonts) — see `references/sources.md` → Themes.
3. **Preview on what already exists**: if there's a running app, inject each theme's CSS variables into the live page and screenshot the same screens in each theme. If the app isn't runnable, recreate its key screen faithfully in a static HTML page with a theme switcher. If nothing is built yet, use a representative mock screen for the product type. Details in `references/previews.md`.
4. Show the 5 previews side by side (same screen, same viewport) plus the token table. Recommend one.

## Step 6 — Apply the choice

When the user picks (they can mix — "template 2 with theme 4"):

**Default: replicate the style, don't pay.** The usual goal is to reproduce the look and feel of the chosen template or component in the user's own codebase. Paid or gated status is never a reason to drop a candidate — it just means you rebuild it instead of installing it. Use the matching path:

- **Free / open-source code** (React Bits, Uiverse, free 21st.dev components and templates): install or copy it (commands in `references/sources.md`) — faster and more faithful than rebuilding.
- **Paid, "with plan", or install-gated** (paid 21st.dev templates, components when the user has no 21st.dev API key or hits the daily limit): **replicate it from what is publicly visible** — the detail page, screenshots, preview images and the public live demo. Follow "Replicating a style" below.

Never get around a paywall itself: don't pull code from behind a purchase or login, don't reuse leaked/pirated copies, don't scrape the paid source bundle of a demo, and never purchase anything. Rebuilding the look from what anyone can see is the bypass.

### Replicating a style

1. **Study the public preview** in the built-in browser: screenshot each section at desktop and mobile widths, scroll through the live demo, hover and click to see interactions.
2. **Extract the design system** with `javascript_tool` on the public demo page: `getComputedStyle` of key elements for colors, font families/sizes/weights, letter-spacing, radius, shadows, spacing, max-widths, and transition/animation timings. Write it down as tokens.
3. **Map the layout**: list the sections in order and the grid/flex structure of each (columns, alignment, breakpoints).
4. **Rebuild with original code** in the user's stack: tokens into the theme (CSS variables), then section by section using shadcn/ui primitives, Tailwind, and free pieces from React Bits / Uiverse / free 21st.dev components that reproduce the same effects (e.g. a paid template's aurora hero → React Bits `Aurora`; its glowing cards → `SpotlightCard`).
5. **Use the user's own content**: their copy, images and brand — never the template's text, photos, illustrations, logos or brand name.
6. **Compare side by side**: screenshot your rebuild next to the original at the same width and iterate until the feel matches (spacing rhythm, type scale and motion matter most).

Working rules for a rebuild (tested on a full site):
- **Build next to the live site, never over it**: a new folder (e.g. `rediseno/`) that reuses the project's `assets/` via relative paths. Production files stay untouched; nothing is committed, pushed or deployed until the user says so.
- **Carry over everything that isn't visual**: `<head>` meta, canonical, Open Graph, JSON-LD, robots (keep `noindex` while testing), favicon, self-hosted fonts, the cookie/consent script — and restyle third-party UI like the cookie banner to the new look (load the new CSS after theirs; match their selector specificity).
- **Extract tokens by walking up from text**: from a heading or card title, read `getComputedStyle` of each ancestor until you hit the one with a background/radius — that's the card (bg, radius, padding, border). Do the same for the primary button, nav links, body text and muted labels.
- **Scroll-reveal must degrade**: hide elements only under a `.js` class set by an inline script, add `prefers-reduced-motion` fallbacks.
- **Gotcha**: `mix-blend-mode` on items inside an animated/transformed container blends with transparency (the transform creates a stacking context) — give that container an opaque background. Logos with white backgrounds on a dark site: `filter: grayscale(1) invert(1) contrast(2) ; mix-blend-mode: screen`.
- **Preview locally** even without Node/Python: Git for Windows ships Perl, enough for a tiny static server (ignore SIGPIPE; skip connections that send no request). Add its config to the session's existing `.claude/launch.json` instead of creating one inside the user's repo. Finish with a local side-by-side page: template demo vs rebuild, same sections, same width.
- Before screenshots: set `history.scrollRestoration = 'manual'`, force reveal classes on, and wait for fonts — otherwise shots come out half-faded or at the old scroll position.

### Applying each choice

- **Template**: open-source → clone/scaffold into the project if asked. Otherwise → replicate as above, page by page, starting with the home/landing.
- **Component**: install or copy if free, replicate if gated; then adapt it: swap hardcoded colors for the project's theme tokens, match radius and font, wire real props/data, remove demo content, and check accessibility (focus states, labels, contrast, `prefers-reduced-motion` for animated pieces).
- **Theme**: write the tokens into the project's global CSS (`:root` and `.dark`), update font imports and `--radius`, then verify in the browser that nothing has hardcoded colors left behind.
- After applying, verify in the running app (screenshot) and offer the natural next mode.

## Principles

- **Coherence over novelty.** One motion language, one radius scale, one accent. Say no to a gorgeous component that breaks the system.
- **Respect the brief.** Every recommendation names the part of the brief it serves.
- **What the user sees.** Options are judged on design and fit only. Never show price, free/paid/"with plan" status, or how a piece will be obtained (install, copy, replicate, "rebuilt from React") — not in the comparison page, not in chat summaries. Every option is simply available. Still mention heavy dependencies (three.js, WebGL shaders), performance/accessibility trade-offs, and the size of the change in the user's project (e.g. "≈12 lines of CSS, no HTML changes").
- **Credit and licence.** Keep author attribution on code you copy; check the licence before copying into a commercial project. Replicated work is original code inspired by the look — it carries none of the original's text, images or branding.
- **Talk to the user in their language.** This skill's instructions are in English, but reply in whatever language the user writes in.

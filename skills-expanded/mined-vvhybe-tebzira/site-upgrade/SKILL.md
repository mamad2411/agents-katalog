---
name: site-upgrade
description: Upgrades a company, product or personal website into a premium, truthful site, end to end. It audits what is actually true, derives a design direction from the brand's own material, builds one or two signature moments (motion, a live product demo, optional 3D), wires a contact form that really delivers, ships SEO, social cards and web standards, verifies everything in a real browser with a scored self-critique, and lands the work as reviewable PRs. Covers marketing and product sites, company and B2B sites, help centers and docs, and portfolios. Use when asked to "spice up", upgrade, redesign, renovate or make premium a website, or to run an SEO or Open Graph pass on one. Not for app dashboards, admin tools or single-component tweaks.
license: MIT
metadata:
  version: 2.0.0
  author: vvhybe
---

# Site upgrade

A method for turning a site that looks assembled into one its owner is proud to show. It was distilled from real upgrades that shipped and that owners and their teams rated highly: a mobile app's marketing site, a B2B cloud company's site taken through two complete directions, and a help center built from nothing. Reuse the **method, recipes and traps**. Never reuse a look: every site takes its direction from its own brand, product and audience.

## What "done" means

The upgrade is finished when all of these hold, and not before:

- Every claim on the site traces to a source you can name: product code, legal text, the billing system, or the owner's written answer.
- The design comes from the brand's own material, and its idea fails the competitor test ([direction.md](references/direction.md)).
- The brand is exact: the name as the brand file writes it, the real logo at every size, the owner's own fonts and colors where they exist.
- One or two signature moments the visitor does or watches; everything else is disciplined.
- Nothing needs motion to be seen. With reduced motion, final states show.
- It was checked in a real browser at 1440, 1920×710, 390 and 320 px and at the heights real phone browsers leave (about 553 to 760 px tall), in every theme, with reduced motion, on a production build.
- The owner has scrolled the first screen in their own browser and approved how it feels, not only how it looks ([direction.md](references/direction.md) § 10).
- Your written critique scores it 9/10 or higher, or your report says plainly where it falls short ([critique.md](references/critique.md)).
- It lands as PRs the team can review, with a short update they can paste.

## Ground rules

1. **Truth before design.** Every feature, number, price, availability date and piece of social proof traces to a source. The product's own onboarding and paywall copy often overpromises: check it in code. "Unknown" is a valid answer: make the slot optional and ask, never fill it with a plausible number. Remove fabricated proof.
2. **The brand decides the look.** Derive palette, type and the signature device from the brand's own material: logo, name, product UI, videos, place. Find the brand file and the owner's other products first: they settle the exact name and logo, and often hold the best idea. A device that reads as generated ([tells.md](references/tells.md)) is allowed only when the brand's material or the owner puts it there, and the direction contract names it.
3. **The product is the hero.** Real UI and real artifacts beat icons, stock 3D and abstractions. A demo looks like the real thing: a real A4 invoice, a real rendered template, the real catalog. A person on the site comes from real footage or photographs, never from drawn primitives.
4. **A website, not a slide deck.** Avoid stacks of centered heading-plus-image blocks that each fade in. Use composition, pinned scroll stories, layered depth, interactive demos and state-driven motion.
5. **Never hide content behind motion.** A reveal that never fires leaves a blank page. Respect `prefers-reduced-motion` by showing final states.
6. **Owner in the loop, not in the way.** Show the direction before the full build, then let them feel the first screen and first scroll before you build the rest. Do the home page first and widen to the other pages once it is approved. Ask each open question once, with options, and keep building around it.
7. **Configuration holds values.** Environment variables carry a URL, an ID or a token, never on/off switches or hardcoded constants. Derive dependent values from them. Commit only `.env.example`.
8. **Follow the target repo.** Read its README, CONTRIBUTING, AGENTS.md and commitlint config. Use its package manager. Match its framework versions (Next 14 vs 16, Tailwind 3 vs 4, React 18 vs 19).
9. **Secrets and internals stay out.** Never print, commit or echo a token the owner pastes. Public commits and PRs carry no client names, private prices or unfixed security gaps.
10. **Never call it done below 9/10.** Score the work from screenshots before you report it. A self-rating of 6 or 7 offered after "done" is the sign of skipped work.
11. **Feel outranks screenshots.** Scroll moves transforms and cameras, never video frames. Pinned scenes stay near two screens. No ambient or generated sound. When an owner likes the idea and rejects how it behaves, keep the idea and change the mechanism.

## First, pick the mode

What the visitor came to do decides how far the design may go. One project can hold several surfaces in different modes; give each its own.

| Mode | Surfaces | The visitor | What leads | Read |
| --- | --- | --- | --- | --- |
| **Persuade** | product, marketing, company, campaign, pricing | decides and acts | the product proving itself; a real action on the first screen | [building-blocks.md](references/building-blocks.md) |
| **Read** | help center, docs, changelog, blog | understands something | the reader's question; the brand owns the frame, never the reading column | [read-mode.md](references/read-mode.md) |
| **Experience** | portfolio, showcase, gallery | explores the work | the work itself, from the first viewport | [building-blocks.md](references/building-blocks.md) § Experience |

A product's marketing site is Persuade even though it shows the app. Its help center is Read even when it is beautiful.

## Workflow

Work through the phases in order. Read each reference when you reach its phase, not before.

| Phase | Do | Read |
| --- | --- | --- |
| 0. Kickoff | Branch off the default branch, start the dev server (note the real port), capture the "before" set for the report | [verification.md](references/verification.md) § 1 |
| 1. Discovery | Audit the site, find the truth sources, write the claims ledger and the subject inventory, collect brand material, report findings | [discovery.md](references/discovery.md) |
| 2. Direction | Find the idea and pass the competitor test, set palette and type, pick the signature moments, write the direction contract, show it | [direction.md](references/direction.md), [tells.md](references/tells.md) |
| 2b. Feel gate | Build only the first screen and first scroll on the real stack; the owner opens it and scrolls it; change the mechanism, not the idea | [direction.md](references/direction.md) § 10 |
| 3. Build it still | Tokens, the hero, each act with real content, the inner pages. Motion off in your head | [building-blocks.md](references/building-blocks.md), [media.md](references/media.md), [read-mode.md](references/read-mode.md) |
| 4. Motion and signature | One choreographed intro, state-driven moments, the signature. 3D only when it earns its place | [motion.md](references/motion.md), [three-d.md](references/three-d.md) |
| 5. Contact and conversion | Shared validation, the form, an edge route, a designed notification email, booking or lead prefill | [contact-email.md](references/contact-email.md) |
| 6. SEO and standards | Server rendering, metadata, social cards, structured data, crawler files, headers. Its own stacked PR | [seo-standards.md](references/seo-standards.md) |
| 7. Verify and critique | Browser loops at every width and theme, the scripted checks, a production build, then the scored critique, up to three rounds | [verification.md](references/verification.md), [critique.md](references/critique.md) |
| 8. Ship | Commits, PRs, the team update, the before/after report, DESIGN.md, memory notes | [delivery.md](references/delivery.md) |

Check [gotchas.md](references/gotchas.md) whenever something behaves oddly. Read [feedback.md](references/feedback.md) whenever the owner reacts: it turns what owners say ("not enough spice", "colors out of balance", "cheap replica") into what to change.

If a design-direction skill is installed (`frontend-design`, `impeccable`, `taste-skill`), load it in phase 2 for extra range. This skill stands on its own without it.

**Stack.** The recipes shipped on Next.js, React, Tailwind and GSAP, hosted on Cloudflare Pages, and the snippets show that stack. The method, the checks and most scripts don't depend on it: on Astro, SvelteKit, Nuxt or plain HTML, keep the rule and translate the recipe to the target's own framework and versions.

## Scripts

Run from the target repo's root. `<skill>` is this skill's folder.

- `node <skill>/scripts/slop-scan.mjs [dir] [--json] [--strict] [--allow <rules>] [--list-rules]`: scans source for generated-site tells, invented proof, genre copy, dead links, secrets and known traps. Exits 1 on errors (or on warnings with `--strict`). Name an earned exception with a `site-upgrade-allow: <rule> <reason>` comment (it covers the lines below it up to the next blank line) or a `.site-upgrade-allow` file at the repo root. Node 18+, no dependencies.
- `<skill>/scripts/ssr-audit.sh <base-url> [path]...`: per page (every sitemap page when no paths are given): status, `<h1>` count, JSON-LD blocks, canonical, social image, client-rendering bailouts and the title; then security headers and crawler files. Exits 1 when a page fails. Run it against a production server.
- `<skill>/scripts/video-prep.sh <source> <out-dir> [name] [poster-second]`: prints scene cuts as chapter candidates and writes silent web encodes with keyframes at each cut, a poster and a square preview clip. Falls back to the `imageio_ffmpeg` binary.
- `<skill>/scripts/sprite-from-video.py <video> <start> <seconds> <out.webp> --model <file>`: cuts a walking person out of footage with a local segmentation model, finds where the stride loops, and writes a sticker sprite sheet and a preview (media.md § 10). Needs Python with numpy, Pillow and onnxruntime.
- `<skill>/scripts/playwright/*.js`: for the Playwright MCP `browser_run_code_unsafe` tool. The MCP reads only files inside the workspace, so copy them first (`mkdir -p .playwright-mcp && cp <skill>/scripts/playwright/*.js .playwright-mcp/`) and pass `filename: ".playwright-mcp/<name>.js"`. Keep `.playwright-mcp/` out of git.
  - `reveal-scroll.js` scrolls so every reveal fires before a screenshot and lists text still hidden afterwards.
  - `page-audit.js` measures the frame: one `<h1>`, headings over two lines, small text, small tap targets, unnamed controls, images without `alt`, untitled sections, unthemed browser surfaces, display-type descenders running into the next block, and captions floating off their pictures.
  - `overflow.js` finds what causes horizontal scroll from 320 to 1440 px and names the outermost culprits.
  - `console-scan.js` visits every sitemap URL and reports console errors, page errors, failed requests, 4xx/5xx and CSP violations.

## Assets and templates

Copy into the target repo or the scratchpad and adapt:

- `assets/render-email.ts`: renders React Email templates to HTML without `react-dom/server`, for edge routes.
- `assets/JsonLd.tsx`: a JSON-LD script tag that is safe to embed.
- `assets/ScrollTriggerRefresh.tsx`: re-measures GSAP scroll triggers whenever the page height changes.
- `assets/templates/claims-ledger.md`: shipped, not shipped, unknown and numbers, each with a source (phase 1).
- `assets/templates/direction-contract.md`: the thesis, idea, own world, first viewport, signature and brand exceptions (phase 2).
- `assets/templates/critique-round.md`: the scored critique, one block per round (phase 7).
- `assets/templates/DESIGN.md`: the built design system, written at the end so later agents stay on brand (phase 8).
- `assets/templates/team-update.md`: the copy-paste update for the team chat (phase 8).

## Owner checkpoints

Confirm these before publishing anything that depends on them. Ask once with options; don't stall the build:

- the brand file: the exact written name, the logo source, the fonts, and the owner's other products
- launch status and store availability, from the live store listing rather than env flags
- prices and plans, and their source
- figures nobody can source yet (uptime, data centers, customer counts): leave them out until someone signs them off
- the contact inbox, and an inbox the owner can read for tests
- items not released yet in any list, catalog or carousel
- legal identity, address and phone, identical everywhere they appear
- any third party that would receive visitor data (analytics, embeds, fonts, email), and the privacy policy lines it needs
- the source files for any mascot, 3D model or video before you rebuild one
- every production step: domains, DNS, deploy settings, migrations. The owner runs or approves them

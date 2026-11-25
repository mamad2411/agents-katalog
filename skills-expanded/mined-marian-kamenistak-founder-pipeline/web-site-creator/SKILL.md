---
name: web-site-creator
description: "Use when the owner wants to build, rebuild or ship a brand-new website, landing page, product site or marketing site (new repo, new domain, new deploy pipeline): \"build a site\", \"new website for X\", \"landing page for Y\", \"ship the site\". The house-stack web-build pipeline that `/founder-pipeline:founder` routes to. NOT for adding a page to an already-live site, decks, post-launch growth work, or auditing a site it did not build (`/founder-pipeline:seo-audit`)."
---

# Web Site Creator — Orchestrator

Ship a fast, SEO-ready, AI-crawlable product site (home + 3–5 pages + blog) on your declared house stack. This file routes; the work lives in `phases/`, the recipes in `references/`. **Load only the phase file you are executing.**

## The bar

Build the most impressive, interactive, scroll-stopping site you could imagine — the one a visitor screenshots and sends to a friend, never mistakable for a site-builder or AI default. The ambition holds WITHIN the gates, never against them: 95+ mobile Lighthouse is non-negotiable, every interaction keyboard-reachable, `prefers-reduced-motion` fully honored, one signature move done exceptionally beats five gimmicks. A site that clears every gate but looks like everyone else's has failed; so has a dazzling site that scores 60 on mobile. Hit both.

## Scale the effort to the change

- **Small change** (copy tweak, link reorder, text/color swap on an already-verified component): edit → `npm run build` passes → ship. NO browser screenshots, NO design-review round; `curl | grep` of built HTML if you must confirm a string rendered.
- **Substantial change** (new page, layout/structure change, new interactive component, new visual pattern): run the relevant phase file + its gate.
- Unclear which? Ask — don't default to the expensive path.
- **Worktree isolation:** before a Substantial change — or a batch of several Small changes worked in one sitting — call `EnterWorktree` (or fall back to a manual `git worktree add` flow) so the session works in its own directory instead of the shared checkout. Skip it only for a genuinely small change shipping in the same turn. Why: two sessions editing the same working directory can silently step on each other — one session's uncommitted edit sits in the same folder another session is `git add -A`ing, and the second session's commit absorbs the first session's unrelated in-flight work. Observed on a real build: a concurrent i18n session's commit swept up another session's uncommitted analytics-proxy edit plus a stray doc file.

## House stack

The house stack is **declared once** by the owner (`/founder-pipeline:founder` → P1.S1) and referenced everywhere after. Every phase file below is written against it. Any deviation needs the owner's recorded override.

**Shipped default, and the worked example this skill is written around:** Astro 5 (MDX + Content Collections) · Cloudflare Workers Static Assets · Tailwind (token-driven) · Motion One + View Transitions · Pagefind · a CAPTCHA/turnstile provider · a transactional email provider · a product-analytics tool · a newsletter tool per product.

The recipes in `references/` are stack-specific by necessity. If your declared house stack differs, the *rules* (gates, imagery floor, hero must-haves, crawler delivery, canonical host) all still apply; the *commands* need translating to your stack, and you should record the translation in the repo's `PLAYBOOK-CASE-NOTES.md` once rather than re-deriving it per build.

## Phase DAG

```
1 CORE (skeleton → content → pictures)      phases/1-core.md
   ├─ 2 VISUAL (design system, de-AI)       phases/2-visual.md   ┐ 2→3 sequential
   ├─ 3 INTERACTIVITY (effects, forms)      phases/3-interactivity.md ┘ (same files)
   └─ 4 METADATA (OG, JSON-LD, favicons)    phases/4-metadata.md  [parallel-safe]
5 SEO + AI-SEO (research, on-page, crawler delivery) phases/5-seo.md (finalizes after 4)
6 LAUNCH (final gate, deploy, indexing)      phases/6-launch.md   (analytics WIRED in 5, VERIFIED here)
→ hand off to post-launch growth (see GATE 6)
```

**Execution rules (deterministic):**
1. A phase is DONE only when its GATE block passes. Never start the next phase early — except the marked parallel lanes.
2. **Parallel lanes** — dispatch as subagents the moment inputs exist, marked `[P]` in phase files: research rounds (protocol: `phases/5-seo.md` §5.0 — round 1 at Phase 1.0, round 2 mid-build, round 3 pre-publish), image curation from the image-library catalog, translation of each finished default-locale page, Phase 4 metadata work, design reviews, the staging SEO crawl audit. Everything `[S]` runs in order in the main context — Phases 2 and 3 both touch layout/CSS and are never parallelized against each other.
   **Phase 5/6 sequence by file zone, not topic** (`phases/5-seo.md` → "Execution order"): Z1 standalone routes/`public/` (robots.txt, IndexNow, RSS, NLWeb, llms files), Z2 layout `<head>` (titles, JSON-LD, RSS link, analytics wiring — pulled forward from what used to be 6.2), Z3 page bodies (content depth THEN internal links — serial, in that order), Z4 nav/footer, Z5 new pages. Z1/Z2/Z4/Z5 run `[P]` against each other; Z3 is `[S]` internally. Four barriers gate the rest: **BARRIER 1** content freeze (`/founder-pipeline:brand-voice` + local-build checks) → **BARRIER 2** one staging deploy serving both GATE 5 and GATE 6.1 (merged verification wave: SEO crawl audit, design review, Lighthouse, axe, security scans, crawler-delivery matrix, forms, analytics) → **BARRIER 3** production deploy (6.3: reachability curl set, crawler-delivery matrix run AGAIN — this one catches edge-level failures staging can't) → **BARRIER 4** `/founder-pipeline:web-indexation`, hard-gated on Barrier 3's matrix returning all-200 (never enqueue a URL that errors for a bot).
   **Photos come from your configured image library first:** whenever a page needs a photo (hero, section, background), browse the relevant subfolder of the library path recorded in the repo's `PLAYBOOK-CASE-NOTES.md` BEFORE reusing repo assets or scraping anything. Pick by subject match to the section's topic (a mentoring section gets a mentoring shot, not a stage shot), copy the file into the project's `src/assets/`, and only fall back to other sources when no subfolder covers the subject.
3. **Screenshots and visual checks go through a headless renderer, NOT a browser-automation tool driving your own browser.** **Set an explicit mobile viewport** — pick your primary test device and record it in `PLAYBOOK-CASE-NOTES.md` so every build measures against the same numbers. Common 2025-era iPhone viewports in CSS px: 393 × 852 (base), 402 × 874 (Pro, DPR 3), 430 × 932 (Plus), 440 × 956 (Pro Max).

   Note that scraping CLIs frequently ignore viewport flags and always return a 1920×1080 desktop shot. Call the rendering API directly for anything mobile — e.g. with `/founder-pipeline:firecrawl-scrape`'s provider, reading the key from your environment:

   ```bash
   curl -s -X POST "https://api.firecrawl.dev/v2/scrape" \
     -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H 'Content-Type: application/json' \
     -d '{"url":"<URL>","waitFor":7000,
          "formats":[{"type":"screenshot","fullPage":true,
                      "viewport":{"width":393,"height":852}}]}' -o shot.json

   curl -sL "$(python3 -c "import json;print(json.load(open('shot.json'))['data']['screenshot'])")" -o mobile.png
   ```

   `fullPage:true` returns the whole page (393 × ~13000 on a long landing page) — crop the band you care about with `sharp(...).extract({left,top,width,height})` rather than trying to scroll. Download the signed asset URL with `curl -sL`, not a Python one-liner: some system Python builds ship without a usable CA bundle and fail with `CERTIFICATE_VERIFY_FAILED`.

   A headless renderer paints at a specified viewport and returns the image, so a mobile check is one call at a real 390px width. Driving your own browser instead carries three failure modes that cost real time on a live build: an occluded window paints nothing (screenshots come back blank and CSS transitions freeze at t=0, so reveals look broken when they are fine), desktop Chrome refuses to resize below ~590px so true mobile width is unreachable, and it happily serves a pre-purge cached copy right after a deploy. Use browser automation only for things a renderer genuinely cannot do: driving a form end to end, solving a CAPTCHA widget, or reading `getComputedStyle`/`getBoundingClientRect` off a live DOM.
4. **Design-review cadence (mandatory, findings get FIXED not filed):** round 1 after GATE 1 (structural), round 2 at GATE 2 (compression), round 3 at GATE 3 (full P0/P1/P2 incl. mobile). Dispatch each round as a subagent (or your own design-review skill if you have one installed) with a live URL + explicit scope + "return P0/P1/P2 findings with concrete CSS/utility-class changes". Apply every finding or record the skip reason in `PLAYBOOK-CASE-NOTES.md`, then re-verify. Any open P0 blocks publish.

## Single source of truth

| What | Lives in | Never in |
|---|---|---|
| A rule / checklist item | exactly ONE `phases/*.md` | SKILL.md, references |
| A recipe / code / war story | exactly ONE `references/*.md` | phase files |
| Site-specific facts (keywords, competitors, skips) | that repo's `PLAYBOOK-CASE-NOTES.md` | this skill |
| Post-launch growth (backlinks, listings, magnets, loops) | the post-launch skills named at GATE 6 | this skill |

New lesson → rule as one line in the right phase file + recipe in the matching reference + bump `references/CHANGELOG.md`.

## Skills cheat-sheet

Skills marked **(plugin)** ship with this plugin. Skills marked **(optional dependency)** come from a separate public plugin the user installs themselves — if it isn't installed, do the work inline and say so. Everything else is an inline instruction, because no skill ships for it.

| When | How |
|---|---|
| Every public string | `/founder-pipeline:brand-voice` (plugin, mandatory) |
| Positioning check (Phase 1.0) | `/founder-pipeline:critical` (plugin) |
| Design extraction (Phase 2.0) | `/founder-pipeline:firecrawl-scrape` (plugin) against the brand's reference URL, then hand-extract palette, type scale and spacing into `tokens.json` + `DESIGN.md` |
| Pricing page (Phase 1.2) | `/founder-pipeline:pricing` (plugin, ≥95/100 before shipping) |
| Visual ambition (Phases 2–3) | `/frontend-design:frontend-design` (optional dependency) |
| Design review ×3 | Subagent per the cadence above, or your own design-review skill |
| Rendering a page to LOOK at it (screenshots, visual/mobile checks) | `/founder-pipeline:firecrawl-scrape` (plugin) — **not** a tool driving your own browser |
| Keyword contract | `/founder-pipeline:web-keyword` (plugin) |
| Translations | Translate each finished page into the secondary locale, then run the result through `/founder-pipeline:brand-voice`; keep a `TRANSLATION-GLOSSARY.md` at repo root so terms stay stable across pages |
| SEO audit (GATE 5) | `/founder-pipeline:seo-audit` (plugin) for the on-page rules; add a third-party crawler (Screaming Frog, Sitebulb, Ahrefs Site Audit) for the crawl layer |
| `robots.txt` | Build it inline per `phases/5-seo.md` §5.2 — tiered UA blocks, then verify delivery with the crawler-delivery matrix in §5.3 |
| AI-search on-page work | `/founder-pipeline:ai-seo` (plugin); `llms.txt` quality bar: `/founder-pipeline:ai-seo-llms-builder` (plugin) |
| Analytics | `/posthog:instrument-product-analytics` (optional dependency) if you run PostHog; otherwise wire your own analytics tool's equivalent events |
| AI-visibility baseline + citation-rate tracking | Post-launch, ongoing — not a manual probe here. Record the launch-week baseline in `PLAYBOOK-CASE-NOTES.md` |
| Post-launch growth | `/founder-pipeline:web-backlinks`, `/founder-pipeline:blog-launch`, `/founder-pipeline:web-listings`, `/founder-pipeline:lead-magnets` (all plugin) |
| Paid acquisition | Out of scope here — hand off to whatever ads workflow you run |
| Adding a page/section to a site this skill already shipped | Don't re-run the whole pipeline: run only the phase that owns the change (usually 1.2 → 2 → 4 → 5 Z3) plus its gate, reusing this skill's `references/` |
| Cookie consent bar (built in Phase 3.2, verified in 6.2) | `references/launch.md` §14.5.8 — build from the recipe, don't improvise |

Version notes v3.5 to v4.0 live in `references/CHANGELOG.md`; read them when you need the history or rationale behind consent, the new-site-only scope, Markdown twins, the AI-citation must-haves or the health re-audit mode.

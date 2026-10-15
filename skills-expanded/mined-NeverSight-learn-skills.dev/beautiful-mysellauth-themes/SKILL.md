---
name: beautiful-mysellauth-themes
description: >-
  Builds world-class SellAuth and MySellAuth storefront themes — dark SaaS, gaming
  neon, light, corporate, luxury. Covers sellauth-theme CLI, Nunjucks, schema.json,
  visual editor resale, hero peek, feature mocks, Lenis motion, premium shop pages
  (shop-pdp.css split, volume discounts), universal theme architecture, and page depth
  via section alternation. Includes AGENTS/PRODUCT/DESIGN KB and style recipes R1–R7.
  Use when creating or editing any SellAuth theme, PDP, cart, landing page,
  sellauth-theme push, or "make me a site". Do NOT use for Shopify Liquid, WooCommerce,
  WordPress, SellAuth backend APIs, or payment logic.
license: MIT. See LICENSE file.
compatibility: >-
  Requires Node.js, sellauth-theme-cli, filesystem, network for npm and push.
  Works with Cursor, Claude Code, Codex, Windsurf, and any agentskills.io client.
  Install via skills.sh or npx skills add.
metadata:
  author: community
  version: "5.0.0"
  spec: agentskills.io
  homepage: https://skills.sh
allowed-tools: Read Write Edit Bash Glob Grep
---

# Beautiful MySellAuth Themes — MEGA SKILL

**Mission:** User asks for a new shop (any language) → agent **asks a short brief in the user's language**, writes **AGENTS.md + PRODUCT.md + DESIGN.md** (English KB), then delivers a **complete, premium, shippable** SellAuth theme — first pass quality bar = months of manual polish encoded here.

**Iron rule:** No theme code until the three KB files exist (unless user explicitly skips — then write KB from defaults anyway).

**Language:** Skill docs = English. Interview, questions, summaries = **user's language**. See [references/11-client-brief-kb.md](references/11-client-brief-kb.md#language-policy-mandatory).

---

## MANDATORY reading (full theme builds)

When user requests a **new theme** or **full rebuild**, read **ALL** references before writing code:

| Order | File | Content |
|-------|------|---------|
| 1 | [references/00-quality-bar.md](references/00-quality-bar.md) | What "perfect" means — 12 pillars |
| 2 | [references/11-client-brief-kb.md](references/11-client-brief-kb.md) | **Interview + AGENTS/PRODUCT/DESIGN KB** |
| 3 | [references/01-discovery.md](references/01-discovery.md) | Style matrix, mock selection, copy structure |
| 4 | [references/02-sellauth-platform.md](references/02-sellauth-platform.md) | CLI, files, Nunjucks, settings |
| 5 | [references/13-theme-architecture.md](references/13-theme-architecture.md) | **Universal folder/CSS/component structure (any theme)** |
| 6 | [references/03-design-system.md](references/03-design-system.md) | Tokens, spotlight, buttons, typography |
| 7 | [references/04-components.md](references/04-components.md) | Navbar, hero, products, features, FAQ |
| 8 | [references/05-mock-ui-mastery.md](references/05-mock-ui-mastery.md) | Full mock engine + triggers |
| 9 | [references/06-motion-mastery.md](references/06-motion-mastery.md) | Reveal, Lenis, hero entrance |
| 10 | [references/07-shop-pages.md](references/07-shop-pages.md) | PDP, cart, checkout |
| 11 | [references/08-anti-patterns.md](references/08-anti-patterns.md) | Never ship list |
| 12 | [references/09-typography-fonts.md](references/09-typography-fonts.md) | **Fonts — mandatory Google Fonts pairings** |
| 13 | [references/10-style-recipes.md](references/10-style-recipes.md) | **Full kits — gaming neon R3, SaaS R1, etc.** |
| 14 | [references/14-sellauth-surfaces.md](references/14-sellauth-surfaces.md) | **All pages & surfaces — P0/P1/P2 checklist** |
| 15 | [references/12-skill-authoring.md](references/12-skill-authoring.md) | **Skill maintenance — Agent Skills spec, publish, sync** |

Template: [assets/token-template.css](assets/token-template.css)  
Font head snippet: [assets/master-font-head.snippet.html](assets/master-font-head.snippet.html)  
KB templates: [assets/templates/AGENTS.md](assets/templates/AGENTS.md), [PRODUCT.md](assets/templates/PRODUCT.md), [DESIGN.md](assets/templates/DESIGN.md)

For **scaffold / new theme structure**: read [13-theme-architecture.md](references/13-theme-architecture.md) + [14-sellauth-surfaces.md](references/14-sellauth-surfaces.md) + [02-sellauth-platform.md](references/02-sellauth-platform.md) first.

For **small edits** (one section, color tweak): read only relevant reference(s).

For **PDP / cart / volume discount work**: read [07-shop-pages.md](references/07-shop-pages.md) + [10-style-recipes.md](references/10-style-recipes.md) (Recipe R7).

**Progressive disclosure:** This file = workflow + gates. Detailed markup, CSS, and Alpine getters live in `references/` — read on demand, one level deep.

---

## Agent role

You are a **senior SellAuth theme architect**. You do not produce generic Bootstrap skins. You produce:

- Optical layouts (nav centered in viewport, hero peek mock)
- Scroll-gated mock UI proving product value
- One cohesive design system file
- Shop pages matching the landing
- Builder-safe Nunjucks + complete schema.json
- **Visual-editor complete** — every buyer-facing string editable in the builder (resale-ready)

---

## Visual editor & resale (mandatory)

Themes built with this skill must work in the SellAuth visual builder so a buyer can rebrand without code.

**Every component:**
1. Entry in `schema.json` for each editable field (text, textarea, list, link, toggle, image).
2. Matching defaults in `settings.json`.
3. Template uses `properties.* | renderString | default('…')` — no hardcoded marketing copy.
4. Root: `class="component"` + `data-component-id="{{ componentId }}"`.
5. Snippets receive `properties` explicitly from the parent component.

**Mock UI** (hero peek, feature panels, how-it-works demos):
- Add `show_mock_ui` / `show_hero_mock` toggle per section.
- When off: omit mock markup; JS must no-op if nodes are missing.
- Schema `help` text: demo chrome uses placeholder labels — disable for copy-only layout.

**After major UI/UX changes** on a live theme: update this skill per [references/12-skill-authoring.md](references/12-skill-authoring.md) — `SKILL.md`, README, relevant `references/*.md`, bump `metadata.version`.

Validate each section in https://dash.sellauth.com/builder/visual/{ID} before adding the next.

---

## Master workflow (copy & track)

```
═══ PHASE 0 — READ ═══
[ ] Read all 15 references (full build only)

═══ PHASE 0.5 — BRIEF & KB (mandatory on new theme) ═══
[ ] Read 11-client-brief-kb.md (language policy)
[ ] Detect user language — ask brief in THAT language (1–2 rounds max)
[ ] Write AGENTS.md + PRODUCT.md + DESIGN.md in English at {BRIEF_ROOT}
[ ] Fill DESIGN.md YAML + derive STYLE_ID / RECIPE / tokens — no TBD on required fields
[ ] Show 10-line summary in user language → confirm (or already said go)
[ ] Theme copy placeholders in site locale from brief

═══ PHASE 1 — DISCOVER (from KB, not guesswork) ═══
[ ] Read AGENTS.md → PRODUCT.md → DESIGN.md
[ ] Confirm STYLE_ID / Recipe from DESIGN frontmatter
[ ] Google Fonts URL in master.njk from DESIGN.md
[ ] Mocks from PRODUCT niche + 01-discovery.md
[ ] PREFIX + ACCENT from DESIGN.md

═══ PHASE 2 — SCAFFOLD ═══
[ ] themes/{ID}/ folder structure
[ ] settings.json + schema.json (copy aligned with PRODUCT.md voice; **every field in schema wired in templates**)
[ ] master.njk: fonts from DESIGN.md + CSS stack + motion
[ ] theme.css tokens copied from DESIGN.md frontmatter / recipe

═══ PHASE 3 — LANDING (ONE SECTION AT A TIME) ═══
[ ] Navbar → builder validate
[ ] Hero + mock peek → LOCK (only tune --t-hero-mock-top after)
[ ] Products #products
[ ] How it works #how-it-works
[ ] Features #features (3 mocks — 05-mock-ui-mastery.md)
[ ] FAQ #faq + Footer

═══ PHASE 4 — SHOP (P0) ═══
[ ] shop-pdp.css — two-column PDP, glass DA, volume promo (single source — no dupes)
[ ] shop-pages.css — cart, checkout, customer shell (comment: PDP lives in shop-pdp.css)
[ ] product-form.njk — Alpine productForm: totalPrice, volume tiers, qty clamp
[ ] Cart volume discount parity with PDP getters
[ ] maintenance.njk — branded offline page

═══ PHASE 4.5 — TRUST & ACCOUNT (P1) ═══
[ ] terms + privacy-policy + refund-policy — shared prose layout
[ ] status + feedback templates
[ ] customer-dashboard + invoices + balance + tickets (+ affiliate if enabled)
[ ] customer-login-modal + sidebar snippets
See [14-sellauth-surfaces.md](references/14-sellauth-surfaces.md) for full checklist.

═══ PHASE 5 — MOTION ═══
[ ] theme:motion-start bus
[ ] Scroll reveal (data-reveal)
[ ] theme-feature-mocks.js + IO trigger
[ ] Lenis on `.t-home` only (landing wrapper)

═══ PHASE 6 — SHIP ═══
[ ] Quality bar self-review (00-quality-bar.md)
[ ] 14-sellauth-surfaces full-ship checklist
[ ] sellauth-theme push + binary upload
[ ] Ctrl+F5 desktop + mobile mental check
```

**Iron rule:** one new `components_order` entry → validate builder → next.

---

## Style at a glance (full matrix in 01-discovery.md)

| ID | Style | bg | accent examples |
|----|-------|-----|-----------------|
| S1 | Pro SaaS dark | `#000` | indigo, orange, violet |
| S2 | Pro sober | `#0f0f0f` | white/gray |
| S3 | Gaming/crypto | `#050508` | neon green, cyan |
| S4 | Light shop | `#f8f9fb` | `#2563eb` |
| S5 | Corporate blue | `#fff` | `#1d4ed8` |
| S6 | Luxury dark | `#0a0a0a` | gold |
| R7 | Glass PDP register | inherits landing | + Inter product font, shop-pdp.css |

User says *"gaming neon"* → **Recipe R3** + fonts Syne + Plus Jakarta Sans — NOT Orbitron body.  
User says *"premium PDP"* / *"glass product page"* → **Recipe R7** on shop pages — see 07-shop-pages.md.  
User says *"gaming neon green"* → R3 + accent `#39ff14`.  
User says *"clean white blue corporate"* → R5.  
User says nothing → R1 for digital goods.

**Never mix rows/recipes.**

Typography is **never optional** — see [09-typography-fonts.md](references/09-typography-fonts.md).

---

## North star (every style)

```
Clear value prop
+ ONE accent
+ Visual proof (hero peek + 3 feature mocks)
+ Fluid scroll-gated motion
+ Shop CTA → #products
+ Trust (delivery + payment)
```

---

## File architecture

See [references/13-theme-architecture.md](references/13-theme-architecture.md) for the full universal layout. Summary:

| File | Role |
|------|------|
| `settings.json` | Config + `components_order` |
| `schema.json` | Every editable builder field |
| `layouts/master.njk` | Shell, CSS order, motion |
| `assets/pro.css` | Platform — **never break** |
| `assets/theme.css` | **Entire** landing design system (`{CSS_FILE}` from DESIGN.md) |
| `assets/shop-pdp.css` | **PDP only** — two-column layout, glass, volume promo |
| `assets/shop-pages.css` | Cart, checkout, shared inner shell |
| `assets/theme-feature-mocks.js` | Mock engine |

CSS order: pro → custom → theme → **shop-pdp** → shop-pages.

**Iron rule:** PDP styles live in `shop-pdp.css` only — never duplicate in `shop-pages.css` or landing CSS.

---

## Nunjucks (survival rules)

**Forbidden:** array literals in loops, `.concat()`, template counters.

**Safe:**
```nunjucks
{% for x in properties.items | default([]) %}
{{ 'theme.css' | assetUrl }}
{{ '/#products' | shopUrl }}
```

Full detail: [02-sellauth-platform.md](references/02-sellauth-platform.md)

---

## Design essentials (see 03-design-system.md for full)

- Prefix **all** landing classes
- **Google Fonts loaded in master.njk** — curated pairing per style (09-typography-fonts.md)
- Max 2 families (+ mono for mocks only)
- Body = readable sans; display = headlines only
- Buttons: 38px height, radius per recipe (8px gaming, 10px pro)
- Headline gradient text OK on display; body flat muted
- Section alternation: `--t-bg` / `--t-section-alt` via nth-child (see 03-design-system.md **Page depth**)
- Hero spotlight: max 2 blur layers (dark) OR wash 6% (light) — **hero component only**, not full page

### Homepage funnel

Hero → Products `#products` → How it works → Trust → Features `#features` → FAQ `#faq` → Footer

Primary CTA: **Browse products** / **Shop now**. Not "Get started free".

---

## Hero peek (signature premium pattern)

```
[ Spotlight / wash ]
[ Centered copy + 2 CTAs ]
[ Mock panel — absolute, cuts below fold ]
```

Lock after build:
- Copy, spotlight, grid, CTA styles **fixed**
- Tune only `--t-hero-mock-top`, `--t-hero-mock-footprint`
- Flex spacer on `.t-hero-inner::after` preserves copy position

Full markup: [04-components.md](references/04-components.md)

---

## Navbar (signature)

Grid `1fr auto 1fr` — brand | links **viewport-centered** | Login + CTA.

Transparent on hero. Sticky. 56px height.

---

## Feature mocks (signature)

3 cards → 3 types: `feed`, `list`, `meters` (or `stats`, `grid`).

- HTML stages **empty**
- JS injects content
- `aria-hidden="true"`
- IntersectionObserver + `sectionIsOnScreen()` (Lenis scrollY trap)
- TIMING snappy (feed/list): start ~200 ms, stepGap ~340 ms, listStepGap ~480 ms — see 05-mock-ui-mastery.md

**Full engine:** [05-mock-ui-mastery.md](references/05-mock-ui-mastery.md)

---

## Motion stack

```
Loader → theme:motion-start
  → Hero entrance (0/80/160/240ms)
  → data-reveal scroll
  → Lenis (.t-home)
  → __featureMockCheck
```

**Critical:** never crush mock TIMING on `prefers-reduced-motion`.

Full spec: [06-motion-mastery.md](references/06-motion-mastery.md)

---

## Shop pages

PDP + cart + checkout must use same tokens. No raw Bootstrap blue.

**Premium pattern (R7):** Two-column PDP, glassmorphism cards, Inter on title/price/CTAs, Alpine volume discount sync.

Full spec: [07-shop-pages.md](references/07-shop-pages.md)  
Recipe kit: [10-style-recipes.md](references/10-style-recipes.md#recipe-r7--glassmorphism-product-register-pdpcart-da)  
Typography split: [09-typography-fonts.md](references/09-typography-fonts.md#product-register-split-pdpcart)

---

## CLI deploy

```bash
npm install -g sellauth-theme-cli
sellauth-theme login
sellauth-theme watch --theme {ID}   # dev
sellauth-theme push --theme {ID}    # ship text
# Binary assets (PNG, woff2): use SellAuth upload API — see 02-sellauth-platform.md
# Optional project script example: node scripts/upload-theme-binaries.mjs --theme {ID}
```

Always **Ctrl+F5** after push.

---

## Quality gate (must pass all)

From [00-quality-bar.md](references/00-quality-bar.md):

0. **AGENTS.md + PRODUCT.md + DESIGN.md** exist and match shipped theme (full builds)
1. 5-second value prop test
2. One accent only
3. Hero peek + 3 mocks working on scroll
4. Soft geometry (not pill CTAs on pro)
5. Nav optically centered
6. Motion scroll-gated
7. `#products` CTA funnel
8. Valid Nunjucks + schema
9. Shop pages styled
10. Typography — Google Fonts documented in DESIGN.md
11. Mobile OK
12. **Visual builder** — all sections editable; mock toggles documented; builder preview verified
13. **Page depth** — section alternation or intentional surfaces; hero spotlight not duplicated globally

Plus: [08-anti-patterns.md](references/08-anti-patterns.md) — zero violations.

---

## Troubleshooting quick ref

| Symptom | Reference |
|---------|-----------|
| Mocks never start | 05-mock-ui — Lenis scrollY=0, add IO |
| Mocks instant | 05-mock-ui — reduce-motion trap |
| Builder crash | 02-sellauth-platform — forbidden Nunjucks |
| PNG broken | 02-sellauth-platform — binary upload API |
| Hero copy jumps | 04-components — flex spacer |
| Style incoherent | 01-discovery — one STYLE_ID; sync DESIGN.md |
| Built wrong colors/fonts | 11-client-brief-kb — KB must exist before code |
| Site feels flat / too dark | 03-design-system — section alternation; avoid full-page grid |
| Ambient glow "does nothing" | 08-anti-patterns — `#app` opaque blocks body layers |
| Glow looks weird / user removes it | 03-design-system Page depth — no section title radials |
| Price doesn't update on qty change | 07-shop-pages — Alpine totalPrice getters |
| Volume discount wrong tier | 07-shop-pages — sort desc for applied, asc for nudge |
| PDP CSS drift / dupes | 07-shop-pages — shop-pdp.css single source |

---

## User prompt → agent action map

Detect intent regardless of language. **Reply and brief in the user's language.**

| User intent (examples) | Agent does |
|------------------------|------------|
| "Make me a site" / "Fais-moi un site" / "Créame una tienda" | **Brief first** (user lang) → KB (English) → full workflow |
| "Gaming neon shop" / "site gaming neon vert" | Interview → Recipe R3 in DESIGN.md → build |
| "Clean white blue corporate" / "theme corporate bleu" | Brief → R5 in DESIGN.md |
| "Skip questions, use defaults" | KB from S1 defaults + assumptions in PRODUCT.md |
| "Fix feature animations only" | Read 05 + 06 (+ existing KB if present) |
| "Premium PDP" / "glass product page" / "volume discount" | Read 07 + 10 (R7) → shop-pdp.css + productForm |
| "Fix cart totals" / "qty price sync" | Read 07 volume discount section + cart-page Alpine |
| "Add FAQ section" | Read 04 + PRODUCT.md → one component + schema |
| "Style legal pages" / "customer dashboard" | Read 14-sellauth-surfaces.md + 07-shop-pages → P1 surfaces |
| "Change accent to orange" | Update DESIGN.md first → sync tokens |

---

## Publishing this skill (skills.sh)

See [README.md](README.md) for install and publish steps.

```
beautiful-mysellauth-themes/
├── SKILL.md
├── README.md
├── LICENSE
├── assets/
│   ├── token-template.css
│   ├── master-font-head.snippet.html
│   └── templates/AGENTS.md, PRODUCT.md, DESIGN.md
└── references/00-*.md … 14-*.md
```

**Publish:** public GitHub repo → `npx skills add owner/repo --skill beautiful-mysellauth-themes`

Folder name **must** match `name:` in frontmatter. No separate registry submit — installs surface on skills.sh via CLI.

---

## Agent constraints

1. Read all references on full builds — no shortcuts.
2. **Write AGENTS.md + PRODUCT.md + DESIGN.md before theme code** on new builds.
3. Never ship without push + binary upload when assets exist.
4. Never hardcode a client brand in skill files — client brand lives in KB only.
5. One `theme.css` — no CSS sprawl.
6. Validate each section in builder before adding next.
7. Self-review against quality bar before declaring done.
8. **Never ship Arial/system-only fonts** — always documented in DESIGN.md.
9. **Gaming neon = Recipe R3** — premium, not arcade cliché.
10. **DESIGN.md is source of truth** for colors/fonts — update KB before CSS when direction changes.
11. **Interview in user's language** — KB files stay English; site copy uses locale from brief.
12. **Visual editor first** — schema + properties for all copy; mock UI optional via toggles.
13. **Skill stays current** — after major theme passes, sync references per [12-skill-authoring.md](references/12-skill-authoring.md) and bump version.

**Deliver premium, complete SellAuth themes — every mandatory surface styled, every technique documented in `references/`.**

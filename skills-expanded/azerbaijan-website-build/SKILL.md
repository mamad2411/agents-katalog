---
name: azerbaijan-website-build
description: Build premium tri-lingual websites from scratch for Azerbaijani businesses. Handles data gathering (website scrape, social media, or interview), brand development, and full Astro + Tailwind build with AZ/RU/EN language support.
triggers:
  - azerbaijan
  - az website
  - baku
  - azerbaijani
---

# Azerbaijan Website Build

Build a stunning, $75K+ agency-quality website from scratch for an Azerbaijani business. Every site is tri-lingual (Azerbaijani, Russian, English) with a language switcher, built on Astro 5.x + Tailwind CSS v4, and deployed to Vercel.

## Quick Reference

| Item | Value |
|------|-------|
| Tech stack | Astro 5.x, Tailwind CSS v4 (Vite plugin), npm |
| Languages | Azerbaijani (primary), Russian, English |
| i18n approach | Directory-based: `/az/`, `/ru/`, `/en/` |
| Images | Unsplash (local), scraped assets, NanoBanana 2 |
| Fonts | @fontsource, must support Latin Extended + Cyrillic |
| Deploy | GitHub repo → Vercel |
| Project location | `~/Azerbaijan/projects/<slug>/` |
| Quality bar | Apple/Stripe/Linear tier. AI Slop Test must pass. |

## Reference Files

Read these before building — they contain non-negotiable rules and technical specs:

- `references/design-rules.md` — Visual design rules, banned fonts/colors/layouts, component architecture
- `references/accessibility-spec.md` — WCAG AA requirements, contrast minimums, keyboard nav
- `references/i18n-spec.md` — Astro i18n routing, LanguageSwitcher component, hreflang, JSON strings
- `references/interview-questionnaire.md` — Structured interview for businesses with no online presence
- `references/azerbaijani-design-guide.md` — Cultural design considerations, font coverage, image selection
- `references/nano-banana-logo.md` — Logo generation via NanoBanana 2 / Gemini API

## Project Structure

```
~/Azerbaijan/projects/<slug>/
├── BUSINESS_PROFILE.md         # Phase 1 output
├── BRAND_BRIEF.md              # Phase 2 output
├── SITE_PLAN.md                # Phase 3 output
├── COPY_CHANGES.md             # Phase 6 output
├── QA_REPORT.md                # Phase 7 output
├── scraped/
│   ├── website/                # Crawled website content (markdown)
│   ├── instagram/              # Instagram data
│   ├── facebook/               # Facebook data
│   └── assets/                 # Downloaded images, logos
│       ├── logos/
│       ├── photos/
│       └── gallery/
└── site/                       # Astro project
    ├── src/
    │   ├── layouts/
    │   │   └── BaseLayout.astro
    │   ├── pages/
    │   │   ├── index.astro     # Redirects to /az/
    │   │   ├── az/             # Azerbaijani pages
    │   │   ├── ru/             # Russian pages
    │   │   └── en/             # English pages
    │   ├── components/
    │   │   ├── Header.astro
    │   │   ├── LanguageSwitcher.astro
    │   │   ├── Footer.astro
    │   │   ├── Hero.astro
    │   │   └── ...sections
    │   ├── content/
    │   │   └── i18n/
    │   │       ├── az.json
    │   │       ├── ru.json
    │   │       └── en.json
    │   ├── utils/
    │   │   └── i18n.ts
    │   ├── styles/
    │   │   └── global.css
    │   └── assets/
    │       └── images/
    ├── public/
    │   ├── images/
    │   ├── favicon.svg
    │   └── robots.txt
    ├── astro.config.mjs
    └── package.json
```

---

## Phase 1: Data Gathering

**Output:** `~/Azerbaijan/projects/<slug>/BUSINESS_PROFILE.md`

Determine which input path applies and follow it. All paths produce the same standardized output.

### Path A — Has Website (+ possibly social media)

1. **Scrape the website** using Apify RAG Web Browser (`apify/rag-web-browser`):
   ```
   Query: the business website URL
   maxResults: 1
   outputFormats: ["markdown"]
   ```
   Save markdown output to `scraped/website/`.

2. **Fallback for JS-heavy sites** (Wix, Squarespace, etc.): Use Chrome automation (`mcp__Claude_in_Chrome`) to:
   - Navigate to each page
   - Take screenshots
   - Extract visible text via `get_page_text`
   - Download images

3. **Scrape social media** if available:
   - **Instagram:** Use Apify Instagram scraper to extract bio, recent posts (last 20), all post images, follower count. Save to `scraped/instagram/`.
   - **Facebook:** Use Apify Facebook scraper or Chrome automation to extract page info, about section, services, reviews, photos. Save to `scraped/facebook/`.
   - **Twitter/X:** Check if exists. If so, extract bio and recent posts via Chrome.

4. **Download all usable images** to `scraped/assets/`:
   - Logo (highest resolution available)
   - Team/staff photos
   - Product/service photos
   - Interior/exterior photos
   - Gallery images
   - Validate: files must be >1KB (reject HTML error pages)

5. **Compile BUSINESS_PROFILE.md** from all scraped data.

### Path B — Social Media Only (no website)

1. **Instagram is primary source:**
   - Scrape full profile: bio, highlights, all posts (up to 50), all images
   - Extract: business name, category, contact info (often in bio), location
   - Download all quality images to `scraped/assets/`

2. **Facebook page:**
   - Extract: about section, services list, reviews/testimonials, photo albums
   - Download photos

3. **Twitter/X:** Check for presence, extract bio and recent content if exists.

4. **Identify gaps** — social media alone often lacks:
   - Detailed service descriptions
   - Pricing information
   - Team information
   - Business history
   - Operating hours

   Flag these in BUSINESS_PROFILE.md under "Gaps to Fill" and ask the user for this information.

5. **Compile BUSINESS_PROFILE.md.**

### Path C — No Online Presence (Interview)

1. **Read `references/interview-questionnaire.md`** for the full question set.
2. **Present questions to the user** in batches (don't dump all 40 questions at once):
   - Start with Business Fundamentals (name, industry, location, contact)
   - Then Services & Products
   - Then Brand & Visual Identity
   - Then Content & Features
3. **Accept whatever the user provides.** Minimum viable: business name, description, city, phone, 3+ services.
4. **Request assets:** Logo file, photos, any marketing materials.
5. **Compile BUSINESS_PROFILE.md.** Mark inferred fields with `[INFERRED]` and missing fields with `[NEEDED]`.

### BUSINESS_PROFILE.md Format

```markdown
# Business Profile: [Business Name]

**Data Source:** Path A (website + social) | Path B (social only) | Path C (interview)
**Date Gathered:** YYYY-MM-DD
**Slug:** [url-safe-slug]

## Business Overview
- **Name:** [Azerbaijani name]
- **Name (English):** [transliteration]
- **Industry:** [category]
- **Year Established:** [year or "Unknown"]
- **Description:** [2-3 sentences about what they do]
- **Unique Selling Points:** [what makes them different]

## Services / Products
| Service | Description | Price (if known) |
|---------|-------------|-----------------|
| ... | ... | ... |

## Target Audience
- **Primary customers:** [description]
- **Language preference:** [AZ / RU / both]
- **Geographic reach:** [local / national / international]

## Brand Personality
- **Tone:** [luxury / professional / friendly / modern / traditional / etc.]
- **Color preferences:** [if expressed or extracted]
- **Inspiration:** [competitor or admired sites]

## Contact & Location
- **Address:** [full address in Azerbaijani]
- **Phone:** [+994 XX XXX XX XX]
- **Email:** [if available]
- **Hours:** [operating hours]
- **WhatsApp:** [if available — very common in Azerbaijan]
- **Social media:**
  - Instagram: [URL]
  - Facebook: [URL]
  - Twitter: [URL]

## Content Inventory
- **About text:** [available / needs writing]
- **Service descriptions:** [available / needs writing]
- **Testimonials:** [count, or "none available"]
- **Team info:** [available / none]

## Image Inventory
| Type | Count | Quality | Notes |
|------|-------|---------|-------|
| Logo | ... | ... | ... |
| Team photos | ... | ... | ... |
| Product photos | ... | ... | ... |
| Interior/exterior | ... | ... | ... |
| Gallery | ... | ... | ... |

## Gaps to Fill
- [ ] [list anything missing that needs to be created, sourced, or asked about]
```

**PAUSE POINT:** Present BUSINESS_PROFILE.md to the user for review before proceeding. Ask about any gaps that need filling.

---

## Phase 2: Brand Development

**Output:** `~/Azerbaijan/projects/<slug>/BRAND_BRIEF.md`

**Read `references/design-rules.md` and `references/azerbaijani-design-guide.md` before starting.**

### Step 1: Logo

**If business HAS a logo:**
- Download/copy to `scraped/assets/logos/`
- Analyze for color extraction
- Verify it's high enough resolution for web use (minimum 200px wide)

**If business DOES NOT have a logo:**
- Read `references/nano-banana-logo.md`
- Gather inputs: business name, industry, brand personality from BUSINESS_PROFILE.md
- Generate 3 logo concepts using NanoBanana 2 via Gemini API
- Present options to user for selection
- If none are satisfactory after 3 rounds: fall back to a typographic logo using the chosen display font (styled in CSS/SVG)
- Save final logo to `scraped/assets/logos/logo.png`

### Step 2: Color Palette

1. If logo exists: extract 2-3 dominant colors from the logo
2. If no logo: develop palette from industry + brand personality
3. Define the full system:
   - Primary color (dominant)
   - Secondary color
   - Accent color (sharp, attention-grabbing)
   - Background color (off-white, warm — not pure white)
   - Text color (near-black, warm — not pure black)
   - Neutral shades (tinted toward brand hue)
4. **Verify EVERY combination** passes WCAG AA:
   - Text on background: 4.5:1 minimum
   - Large text: 3:1 minimum
   - UI components: 3:1 minimum
   Use `scripts/contrast-check.js` to verify.
5. Document as CSS custom properties with contrast ratios as comments.

### Step 3: Typography

1. Select a display/heading font and a body font from the verified candidates in `references/design-rules.md`
2. **VERIFY both fonts** render the Azerbaijani test string AND Cyrillic correctly
3. Define the typographic scale: display, h1, h2, h3, body, small, caption
4. Use fluid sizing with `clamp()` for all sizes
5. Install via @fontsource with correct subsets: `latin`, `latin-ext`, `cyrillic`, `cyrillic-ext`

### Step 4: Brand Voice

Define the communication tone for each language:
- **Azerbaijani:** [warm/formal/casual] — this is the primary voice
- **Russian:** Typically slightly more formal
- **English:** Clean, international, professional

### Step 5: Brand Card

Create an HTML brand card (single HTML file) showing:
- Logo (or placeholder)
- Color palette with hex codes and contrast ratios
- Typography samples in all three languages
- Brand voice summary
- Tagline/headline suggestions in Azerbaijani

Save to project root and open for review.

### Step 6: Generate DESIGN.md

After the Brand Card, produce a structured `DESIGN.md` using the `design-system-generator` skill with Azerbaijan extensions.

1. Read `00-design-references/design-md-format.md` for the base 9-section format.
2. Select 1-2 reference DESIGN.md files from `00-design-references/references/by-aesthetic/` matching the brand direction.
3. Generate DESIGN.md with all 9 standard sections PLUS **Section 10: Multi-Lingual Considerations**:
   - Font verification test string: `"Əlaqə üçün bizə zəng edin. Ğəbul saatları: Ş. 09:00-18:00 | Связаться с нами"`
   - Russian text ~30% expansion accommodation rules for layouts, buttons, and navigation
   - Azerbaijan cultural color notes (flag colors used subtly, gold for luxury)
   - Per-language content tone (AZ: warm/formal, RU: slightly more formal, EN: clean international)
4. The BRAND_BRIEF.md Color Palette and Typography sections should say "See DESIGN.md for the complete design system" — BRAND_BRIEF.md retains brand voice, logo metadata, and non-design content.

**Output:** `~/Azerbaijan/projects/<slug>/DESIGN.md`

### BRAND_BRIEF.md Format

```markdown
# Brand Brief: [Business Name]

## Logo
- Source: [existing / generated / typographic]
- File: [path to logo file]

## Color Palette
| Token | Hex | Usage | Contrast vs bg |
|-------|-----|-------|----------------|
| --color-primary | #xxx | Headings, buttons | X.X:1 AA PASS |
| --color-secondary | #xxx | Accents | X.X:1 AA PASS |
| --color-accent | #xxx | CTAs, highlights | X.X:1 AA PASS |
| --color-bg | #xxx | Page background | — |
| --color-text | #xxx | Body text | X.X:1 AA PASS |

## Typography
- **Display:** [Font Name] — [weights]
- **Body:** [Font Name] — [weights]
- **Verified:** AZ characters ✓ | Cyrillic ✓

> **Note:** Complete design system specification (color tokens, typography hierarchy table, component stylings, shadow system, layout principles) is in `DESIGN.md`. The sections below are summaries — see DESIGN.md for exact values.

## Brand Voice
- **AZ:** [description]
- **RU:** [description]
- **EN:** [description]

## Aesthetic Direction
- **Tone:** [chosen aesthetic]
- **Differentiation:** [the unforgettable thing]
```

**PAUSE POINT:** Present BRAND_BRIEF.md and brand card to user for approval before proceeding.

---

## Phase 3: Content Strategy & Site Architecture

**Output:** `~/Azerbaijan/projects/<slug>/SITE_PLAN.md`

### Step 1: Page Structure

Based on the business type and content available, define the sitemap. Typical structures:

**Standard (most businesses):**
- Home (`/az/`, `/ru/`, `/en/`)
- About (`/az/haqqimizda/`, `/ru/o-nas/`, `/en/about/`)
- Services (`/az/xidmetler/`, `/ru/uslugi/`, `/en/services/`)
- Contact (`/az/elaqe/`, `/ru/kontakty/`, `/en/contact/`)

**Extended (if content available):**
- Gallery (`/az/qalereya/`, `/ru/galereya/`, `/en/gallery/`)
- Blog (`/az/bloq/`, `/ru/blog/`, `/en/blog/`)
- Pricing (`/az/qiymetler/`, `/ru/tseny/`, `/en/pricing/`)
- Menu (restaurants: `/az/menyu/`, `/ru/menyu/`, `/en/menu/`)

### Step 2: Per-Page Content Plan

For each page, define:
- Sections (Hero, About, Services grid, Testimonials, CTA, etc.)
- Copy direction in Azerbaijani (what each section should communicate)
- Image needs per section (what we have vs. what we need)
- Interactive elements (accordion, gallery lightbox, contact form, map)

### Step 3: Image Strategy

Categorize all image needs:
| Section | Image Needed | Source | Status |
|---------|-------------|--------|--------|
| Hero | Hero background | Unsplash / NanoBanana | [need] |
| About | Team/office photo | Scraped | [have] |
| Services | Service illustrations | Unsplash | [need] |
| ... | ... | ... | ... |

**Download all Unsplash images NOW** — before the build phase:
1. Search Unsplash for each needed image
2. Verify cultural appropriateness (see `references/azerbaijani-design-guide.md`)
3. Download to `site/src/assets/images/` (for Astro optimization) or `site/public/images/` (for static)
4. Name descriptively: `hero-restaurant-baku.jpg`, `team-working.jpg`
5. NEVER hotlink external URLs

### Step 4: SEO Plan

- Target keywords in Azerbaijani (primary), Russian, English
- JSON-LD schema type (LocalBusiness, Restaurant, etc.)
- Meta title/description templates for each page × each language
- Sitemap strategy with hreflang alternates

### SITE_PLAN.md Format

Document all of the above. This is the blueprint for the build phase.

**PAUSE POINT:** Present SITE_PLAN.md to user. This is the last checkpoint before building.

---

## Phase 4: Image Curation

**Output:** All images organized in the Astro project

1. **Process scraped images:**
   - Copy usable images from `scraped/assets/` to `site/src/assets/images/`
   - Resize oversized images (max 2000px wide)
   - Ensure quality is sufficient for web use

2. **Download Unsplash images** (per SITE_PLAN.md image strategy):
   - Use Unsplash API or search via web to find appropriate images
   - Download each to `site/src/assets/images/` or `site/public/images/`
   - Follow Azerbaijan cultural image guidelines
   - **NEVER use external Unsplash URLs in production code**

3. **Generate images via NanoBanana 2** (if needed):
   - Hero backgrounds
   - Product/service imagery when no originals exist
   - See `references/nano-banana-logo.md` for API usage

4. **Verify every image:**
   - Color temperature matches brand palette?
   - Culturally appropriate for Azerbaijan?
   - Right demographic for actual customer base?
   - Matches the section copy, not just vaguely related?

5. **Organize into folders:**
   ```
   site/src/assets/images/
   ├── hero/
   ├── about/
   ├── services/
   ├── gallery/
   ├── team/
   └── general/
   ```

---

## Phase 5: Build the Website

**Read ALL reference files before building:**
- `references/design-rules.md` — Design rules (non-negotiable)
- `references/accessibility-spec.md` — WCAG AA requirements
- `references/i18n-spec.md` — i18n routing, LanguageSwitcher, hreflang

### Step 1: Initialize Astro Project

```bash
cd ~/Azerbaijan/projects/<slug>
npm create astro@latest site -- --template minimal --no-install
cd site
npm install
npx astro add tailwind --yes
npx astro add sitemap --yes
npm install -D prettier
```

Install fonts (example):
```bash
npm install @fontsource/dm-sans @fontsource/playfair-display
```

### Step 2: Configure Astro

In `astro.config.mjs`:
- Set `site` to the expected Vercel URL
- Configure sitemap with i18n (see `references/i18n-spec.md`)
- Configure i18n routing with `az` as default locale

### Step 3: Build Design System

**Read the project's `DESIGN.md` before building the design system.** Use it as the authoritative source for all CSS custom properties, font imports, typographic scale, component specs, and shadow tokens. Verify that fonts from the DESIGN.md pass the AZ/RU character verification test before proceeding.

Create `src/styles/global.css`:
- Import font packages
- Define ALL CSS custom properties from BRAND_BRIEF.md
- Document contrast ratios as comments
- Define typographic scale with `clamp()`
- Set base styles (body, headings, links)

### Step 4: Build i18n Infrastructure

From `references/i18n-spec.md`:
- Create `src/utils/i18n.ts` with `getLang()`, `getStrings()`, `switchLang()`, `getAlternateLinks()`
- Create `src/content/i18n/az.json`, `ru.json`, `en.json` with UI strings
- Create root `src/pages/index.astro` that redirects to `/az/`

### Step 5: Build Layout & Shared Components

1. **BaseLayout.astro:**
   - `<html lang>` attribute from i18n utility
   - `<head>` with hreflang links for all 3 languages + x-default
   - Open Graph / Twitter Card meta (per language)
   - Font imports
   - Global CSS import
   - View Transitions
   - Skip-to-content link

2. **Header.astro:**
   - Navigation links (translated via i18n strings)
   - LanguageSwitcher component
   - Mobile hamburger menu
   - Sticky/fixed position

3. **LanguageSwitcher.astro:**
   - AZ | RU | EN with flag indicators
   - Preserves current page path
   - `aria-current` on active language
   - See `references/i18n-spec.md` for complete implementation

4. **Footer.astro:**
   - Contact info from BUSINESS_PROFILE.md
   - Social media links
   - Copyright with current year
   - All text from i18n strings

### Step 6: Build Page Sections as Components

Each visually distinct section is its OWN `.astro` component:
- `Hero.astro` — Full-width hero with image/overlay, headline, CTA
- `About.astro` — Business story/description
- `Services.astro` — Services grid/cards
- `Testimonials.astro` — Customer quotes/reviews
- `CTA.astro` — Call-to-action banner
- `Gallery.astro` — Photo grid/lightbox (if applicable)
- `Contact.astro` — Contact form, map, info
- Additional sections as needed

**Each component receives language-specific content as props.** The per-language page files pass the correct content to shared components.

### Step 7: Build Azerbaijani Pages First

Build all pages under `src/pages/az/`:
- `az/index.astro` — Homepage
- `az/haqqimizda.astro` — About
- `az/xidmetler.astro` — Services
- `az/elaqe.astro` — Contact
- Additional pages per SITE_PLAN.md

Write all content in **native Azerbaijani**. This is the primary language — it must read naturally, not like a translation.

### Step 8: Apply Design Rules

Go through `references/design-rules.md` checklist:
- [ ] 4+ different layout patterns used
- [ ] No two consecutive sections share same column structure
- [ ] Banned fonts NOT used
- [ ] Color system uses CSS custom properties
- [ ] All contrast ratios pass WCAG AA
- [ ] 3+ distinct animation types
- [ ] Scroll-triggered reveals on 2+ sections
- [ ] `prefers-reduced-motion` respected
- [ ] Visual depth (noise, gradients, SVG shapes, shadows)
- [ ] Component architecture (no monolithic pages)
- [ ] AI Slop Test: would someone think AI made this? If yes, redesign.

### Step 9: Responsive Design

- Mobile-first: base styles for 320px+
- Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl), 1536px (2xl)
- Use `min-width` media queries, NOT `max-width`
- Touch targets: minimum 44px height
- Verify at all breakpoints — no horizontal scrollbar

### Step 10: SEO Implementation

Per page, per language:
- Unique `<title>` and `<meta name="description">`
- JSON-LD schema (LocalBusiness or appropriate type)
- hreflang `<link>` tags (see i18n-spec.md)
- Sitemap via @astrojs/sitemap with i18n alternates
- `robots.txt` in `public/`
- Semantic HTML (`<main>`, `<nav>`, `<article>`, `<section>`)
- Descriptive alt text on every image (in the page's language)

### Step 11: Favicon

- Generate from logo
- At minimum: `public/favicon.svg`
- Add to `<head>` in BaseLayout

---

## Phase 6: Copy & Translation

### Step 1: Azerbaijani Copy (Primary)

Review all Azerbaijani page content:
- Value proposition clear within 5 seconds?
- Every page has a visible, benefit-driven CTA?
- Copy leads with benefits, not features?
- Addresses customer objections early?
- Uses specific numbers where possible?
- Short sentences for impact?
- 8th-grade reading level equivalent?

Document improvements in `COPY_CHANGES.md`.

### Step 2: Russian Translation

Create all pages under `src/pages/ru/`:
- **Adapt, don't translate word-for-word.** Russian has different sentence structures and formality norms.
- Russian text is ~30% longer than English — verify layouts don't break
- Use proper Russian conventions (formal "вы" for business sites)
- URL slugs in Russian transliteration: `/ru/o-nas/`, `/ru/uslugi/`, `/ru/kontakty/`

### Step 3: English Translation

Create all pages under `src/pages/en/`:
- Clean, professional international English
- Standard URL slugs: `/en/about/`, `/en/services/`, `/en/contact/`
- This version serves tourists, expats, and international contacts

### Step 4: UI Strings

Update all three JSON files (`az.json`, `ru.json`, `en.json`):
- Navigation labels
- Button text (CTA, forms)
- Footer content
- Form labels and placeholders
- Error messages
- Meta descriptions

### Step 5: Verify Completeness

Check every page × every language:
- No placeholder text remaining
- No untranslated strings
- No broken i18n references
- All JSON string keys used consistently

---

## Phase 7: QA (Combined Round)

**Output:** `~/Azerbaijan/projects/<slug>/QA_REPORT.md`

Run the dev server and systematically check everything:

```bash
cd ~/Azerbaijan/projects/<slug>/site
npm run dev
```

### 7.1 Functional QA (All 3 Languages)

- [ ] All navigation links work
- [ ] Language switcher works from EVERY page (preserves current page)
- [ ] Root `/` redirects to `/az/`
- [ ] All images load (no broken images)
- [ ] Contact form works (if applicable)
- [ ] Social media links open correctly
- [ ] Phone/email links work (`tel:`, `mailto:`)
- [ ] WhatsApp link works (if applicable)
- [ ] Map embed works (if applicable)
- [ ] 404 page works for all language prefixes

### 7.2 Visual QA

- [ ] Design rules checklist passes (4+ layouts, no banned elements)
- [ ] Animations smooth, no jank
- [ ] Consistent branding across all pages
- [ ] Images high quality, properly sized
- [ ] No "AI slop" — would a human designer sign off on this?
- [ ] Dark overlays on text-over-image sections
- [ ] Visual hierarchy clear on every page

### 7.3 Responsive QA (Test ALL 3 Languages at Each Viewport)

- [ ] 320px (mobile) — all languages
- [ ] 768px (tablet) — all languages
- [ ] 1024px (small desktop) — all languages
- [ ] 1280px (desktop) — all languages
- [ ] 1536px+ (large) — all languages
- [ ] No horizontal scrollbar at any viewport
- [ ] Russian text (longest) doesn't break layouts
- [ ] Touch targets ≥ 44px on mobile
- [ ] Mobile nav works correctly

### 7.4 Accessibility QA

- [ ] Run axe-core on every page (fix all CRITICAL/SERIOUS)
- [ ] Contrast check all color combinations (`scripts/contrast-check.js`)
- [ ] Keyboard navigation works (Tab through all interactive elements)
- [ ] Skip-to-content link present and functional
- [ ] All images have alt text (in correct language)
- [ ] `prefers-reduced-motion` disables animations
- [ ] Focus indicators visible

### 7.5 SEO QA

- [ ] hreflang tags correct on every page (AZ, RU, EN, x-default)
- [ ] JSON-LD schema valid per language
- [ ] Sitemap includes all pages × all languages
- [ ] robots.txt present and correct
- [ ] Unique title + meta description per page per language
- [ ] Semantic HTML used correctly
- [ ] Canonical URLs correct

### 7.6 Content QA

- [ ] All three languages complete — no placeholders
- [ ] Azerbaijani reads naturally (not translated-sounding)
- [ ] Russian reads naturally, proper formality
- [ ] English is clean and professional
- [ ] No untranslated UI strings
- [ ] Business info accurate (name, address, phone, hours)

### 7.7 Image QA

Run broken image check:
```javascript
Array.from(document.querySelectorAll('img')).filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src)
```
- [ ] No broken images on any page
- [ ] No external/hotlinked image URLs
- [ ] All images optimized (Astro `<Image>` or properly sized)

### Fix & Reverify

Fix all issues found. Re-run checks on fixed items. Document everything in `QA_REPORT.md`.

---

## Phase 8: Deployment

### Step 1: Build Test

```bash
cd ~/Azerbaijan/projects/<slug>/site
npm run build
```

Fix any build errors. The build must succeed cleanly.

### Step 2: Git Setup

```bash
cd ~/Azerbaijan/projects/<slug>/site
git init
# Ensure .gitignore exists (Astro generates one)
# Verify .env.local is in .gitignore
git add .
git commit -m "Initial build: [business name] - tri-lingual website (AZ/RU/EN)"
```

### Step 3: GitHub

Create a new GitHub repository: `<slug>-az`
```bash
gh repo create <slug>-az --public --source=. --push
```

### Step 4: Vercel

Deploy to Vercel:
```bash
npx vercel --yes
npx vercel --prod
```

Or connect via Vercel dashboard for auto-deploy on push.

### Step 5: Live Verification

Open the live Vercel URL and verify:
- [ ] All three language versions load
- [ ] Language switcher works
- [ ] All images load
- [ ] Forms functional
- [ ] SSL certificate active (https)
- [ ] Performance acceptable (check Lighthouse)

### Step 6: Final Accessibility Scan

Run axe-core against the LIVE URL for a final check.

### Step 7: Deliver

Provide the user with:
- Live URL
- GitHub repo URL
- Summary of what was built (pages, features, languages)

---

## Rules & Standards

### Non-Negotiable

1. **Tri-lingual is not optional.** Every page must exist in AZ, RU, and EN. Every UI string must be translated.
2. **Azerbaijani is the primary language.** Write Azerbaijani content first. It must read natively, never like a translation.
3. **WCAG AA compliance.** Contrast ratios verified, keyboard nav works, alt text present.
4. **All images local.** Never hotlink external URLs. Download everything.
5. **Fonts must support both scripts.** Latin Extended (AZ) + Cyrillic (RU). Verify before using.
6. **Design rules apply.** See `references/design-rules.md`. No banned fonts, colors, or layouts.
7. **AI Slop Test.** If it looks like AI made it, redesign.
8. **Cultural appropriateness.** Images, tone, and design must feel Azerbaijani, not generic American.

### Technical Standards

- **Astro 5.x** with Tailwind CSS v4 (Vite plugin)
- **npm** only (not pnpm, not yarn)
- **@fontsource** for self-hosted fonts
- **Astro `<Image>`** component for image optimization
- **CSS-only animations** (no JS animation libraries)
- **View Transitions** for page navigation
- **Semantic HTML** throughout
- **Mobile-first** responsive design
- **Lighthouse 95+** performance target

### Copy Standards

- Hook → Problem → Solution → Proof → Action (every page)
- Value proposition clear within 5 seconds
- Lead with benefits, not features
- Specific numbers > vague claims
- 8th-grade reading level equivalent
- Short sentences for impact
- Testimonials near CTAs and decision points

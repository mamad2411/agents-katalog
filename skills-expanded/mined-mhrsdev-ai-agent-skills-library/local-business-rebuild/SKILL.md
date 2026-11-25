---
name: local-business-rebuild
description: >
  Build a stunning new website for a local business prospect. Adapted from the
  full website-rebuild skill but optimized for speculative local business pitches.
  10-phase process: brand extraction, SEO audit, design audit, rebuild plan, full
  build with design system, copy optimization, combined QA, pre-deploy checklist,
  and output to monorepo. Uses scraped content from prospect-scrape as input.
  No tools/calculator research phase. Single combined QA round.
  Triggers on: "rebuild prospect", "local business rebuild", "build prospect site",
  "rebuild their site", "prospect rebuild", or any request to build a new website
  for a qualified prospect.
---

# Local Business Website Rebuild

Build a world-class website for a local business prospect using their scraped content and branding. This is the core value delivery — the rebuilt site must be so dramatically better than their current one that the business owner immediately sees the value.

## How This Skill Works

This is an adapted version of the full `/website-rebuild` skill, streamlined for speculative local business pitches:
- **Removed:** Phases 11a/11b (Competitive Tools Research & Build), Phase 12 (Tools QA)
- **Consolidated:** 3 QA rounds → 1 combined QA round
- **Kept full depth:** Rebuild plan, copy optimization, all design rules, accessibility
- **Output location:** `~/prospect-pipeline/sites/<slug>/` (monorepo structure)

## Input

Read from `~/prospect-pipeline/prospects/<slug>/`:
- `info.json` — business details, category, contact info
- `audit-report.md` — what's wrong with their current site
- `original-site/content-inventory.json` — all scraped content
- `original-site/assets/` — logo, images, etc.

## Tech Stack — Exact. Do Not Deviate.

**Framework:** Astro 5.x — static site generator, zero JavaScript by default, perfect for SEO.
**Styling:** Tailwind CSS v4 (via Vite plugin)
**Images:** Astro `<Image>` component from `astro:assets` (built-in optimization, WebP/AVIF)
**SEO:** `@astrojs/sitemap` integration + manual JSON-LD
**View Transitions:** Astro View Transitions (built-in, zero JS page transitions)
**Package Manager:** npm (not pnpm, not yarn — npm only)

### Initialization — Run These Exact Commands

```bash
cd ~/prospect-pipeline/sites/
npm create astro@latest <slug> -- --template minimal --no-install
cd <slug>
npm install
npx astro add tailwind --yes
npx astro add sitemap --yes
npm install -D prettier
```

That's it. The project is ready. Do not add React, do not add any other integrations unless the build specifically requires interactivity (rare for a local business site).

### If Something Fails During Build

Fix the code. Do NOT:
- Switch Node versions
- Switch package managers
- Reinstall the framework
- Add React or any other UI framework
- Change the project structure

If `npm create astro` fails, check that Node.js is available and try again. If it fails twice, report the error — do not try alternative frameworks.

### Astro File Structure

```
src/
  layouts/
    BaseLayout.astro     ← shared HTML shell, <head>, nav, footer
  pages/
    index.astro          ← homepage
    about.astro          ← about page
    services.astro       ← services page
    contact.astro        ← contact page
    404.astro            ← custom 404
  components/
    Header.astro         ← navigation
    Footer.astro         ← footer
    Hero.astro           ← hero section (reusable)
    ...                  ← section components as needed
  styles/
    global.css           ← @import "tailwindcss"; + CSS custom properties
public/
  images/                ← all downloaded images go here
  favicon.svg            ← favicon
```

### Astro Basics for This Build

`.astro` files have a frontmatter script fence (`---`) at the top and HTML-like template below:

```astro
---
import { Image } from 'astro:assets';
import BaseLayout from '../layouts/BaseLayout.astro';
import heroImage from '../assets/images/hero.jpg';
---

<BaseLayout title="Home" description="Meta description here">
  <section class="relative h-[80vh]">
    <Image src={heroImage} alt="Descriptive alt text" class="object-cover w-full h-full" />
  </section>
</BaseLayout>
```

Key differences from React/Next.js:
- No JSX — it's HTML. Use `class=` not `className=`. Use `for=` not `htmlFor=`.
- No `useState`, no `useEffect`, no client-side state. The page is static HTML.
- Images: Import from `src/assets/images/` for optimization, or reference `public/images/` for unoptimized static files.
- CSS custom properties go in `src/styles/global.css` and are available everywhere.
- View Transitions: Add `<ViewTransitions />` to the `<head>` in BaseLayout for smooth page transitions — zero JavaScript.

### Google Fonts

Load via `<link>` tags in the BaseLayout `<head>`, or use `@fontsource` packages:

```bash
npm install @fontsource-variable/playfair-display @fontsource/dm-sans
```

Then import in your layout's frontmatter:
```astro
---
import '@fontsource-variable/playfair-display';
import '@fontsource/dm-sans';
---
```

## Design Philosophy — MAKE IT UNFORGETTABLE

**The AI Slop Test:** Before you ship, ask yourself: "If someone saw this site and was told 'AI made this,' would they believe it immediately?" If yes, you have failed. Redesign until that answer is no.

Read the [design-rules.md](references/design-rules.md) for full specification. Below are NON-NEGOTIABLE rules with specific alternatives.

### Pre-Code Design Commitment (Phase 4.5 — MANDATORY)

Before writing ANY code, you must describe in plain English:
1. **Aesthetic direction** — Pick ONE: dark/moody editorial, warm/organic handcrafted, clean/luxury minimal, bold/industrial, retro-modern, or something unique to this business. Commit to it.
2. **For each homepage section** — describe: layout structure (NOT "3-column grid"), column ratios, visual devices (overlap? angle? texture? full-bleed?), and how it differs from the section above it.
3. **The "wow" moment** — every great site has one thing that makes you stop scrolling. What is it for this site? (parallax hero? animated counter? overlapping testimonial cards? a diagonal section break?)

Write this into `REBUILD_PLAN.md` before touching any `.astro` file.

### Typography
- Beautiful, unique fonts from Google Fonts or @fontsource
- **BANNED:** Inter, Roboto, Arial, Helvetica, system fonts, Space Grotesk, Lato, Open Sans, Source Sans Pro
- **INSTEAD:** Distinctive display font + refined body font. Fraunces, Playfair Display, Clash Display, Cabinet Grotesk, General Sans, Satoshi, Plus Jakarta Sans.
- Use the FULL typographic range: hero headings should be 56-80px+ (clamp for fluid), extreme weight contrast (300 vs 800, not 400 vs 600)
- Body minimum 16px, line-height 1.5-1.65
- `text-wrap: balance` on headings, `font-variant-numeric: tabular-nums` on numbers

### Color
- CSS custom properties for every color value in `global.css`
- 1-2 dominant colors + 1 sharp accent derived from their logo/branding
- **BANNED:** purple gradients on white, generic blue corporate, rainbow with no hierarchy, pure black (#000), pure white (#fff) as main backgrounds, cyan-on-dark "developer aesthetic", gradient text
- **INSTEAD:** Tint your neutrals toward the brand hue. Use `oklch()` or warm grays. Off-white backgrounds (like `#faf9f6`), near-black text (like `#1a1a2e`). Bold saturated accents that pop.
- Every combination must pass WCAG AA contrast (4.5:1 for body text, 3:1 for large text)

### Motion & Animation
- CSS animations and transitions only — no JavaScript animation libraries
- **BANNED:** bounce/elastic easing, `transition: all`, animating width/height/margins (layout thrashing), identical fadeInUp on every section
- **INSTEAD:** Exponential easing (`cubic-bezier(0.16, 1, 0.3, 1)` for ease-out-expo). Staggered reveals with `animation-delay`. One orchestrated page-load sequence. `transform` and `opacity` only (60fps).
- **MINIMUM 3 distinct animation types per site** — don't just use fadeInUp everywhere. Examples: slide-in-from-left, scale-reveal, clip-path-wipe, counter-count-up, text-split-reveal, parallax-subtle
- Scroll-triggered reveals required on at least 2 sections (use Intersection Observer with a small `<script>` tag in Astro)
- Respect `prefers-reduced-motion` with `@media` query
- Astro View Transitions for page-to-page animation

### Layout — BREAK THE GRID
- **BANNED:** Every section centered with `max-w-7xl mx-auto`. Identical 3-column card grids. Every section header as `text-center max-w-2xl mx-auto mb-14`. Uniform padding on every section. Everything wrapped in rounded cards with drop shadows.
- **INSTEAD:** Use these specific layout patterns (pick at least 4 different ones for the homepage):

  **Pattern A — Asymmetric Split:** `grid-cols-[2fr_1fr]` or `grid-cols-[1fr_2fr]` instead of equal columns. One side is a large image, the other is tight text. Not 50/50.

  **Pattern B — Full-Bleed Break:** At least one section must escape the container — a full-width image, a colored band that runs edge-to-edge, or a diagonal section divider using CSS `clip-path`.

  **Pattern C — Overlapping Elements:** Use negative margins (`-mt-16`, `-ml-8`) or `translate` to overlap images onto adjacent sections. Break the box model.

  **Pattern D — Bento/Masonry Grid:** Instead of equal cards, vary the sizes — one large featured card with smaller ones around it. `grid-row: span 2` on the featured item.

  **Pattern E — Staggered/Offset:** Alternate image-left/text-right and text-left/image-right between sections. Offset vertically so items don't align on a flat grid.

  **Pattern F — Pull Quote / Callout:** A testimonial or stat that breaks out of the text flow — oversized text, a different background, rotated slightly, or overlapping adjacent content.

- **RULE:** No two consecutive sections may share the same column structure or visual pattern.

### Visual Depth & Atmosphere
- **BANNED:** Flat solid-color section backgrounds with nothing else. Plain white sections. Sections that are just text floating in space.
- **INSTEAD:** Add visual depth with AT LEAST 2 of these per site:
  - Subtle noise/grain texture overlay (CSS `background-image: url("data:image/svg+xml,...")` or a tiny PNG)
  - Gradient meshes or radial gradients for section backgrounds
  - Decorative SVG shapes (blobs, waves, diagonal lines) as section dividers or background elements
  - `box-shadow` with colored tints (not just gray)
  - Subtle background patterns (dots, lines, topographic maps for outdoor businesses)
  - Layered z-index compositions where elements overlap intentionally

### Component Architecture
- **MANDATORY:** Each visually distinct homepage section must be its own `.astro` component in `src/components/`. This forces you to design each section independently rather than copy-pasting patterns.
- Minimum components for a homepage: `Hero.astro`, `About.astro`, `Services.astro`, `Testimonials.astro`, `CTA.astro` — plus the global Header/Footer.
- This is not optional. A 250-line monolithic `index.astro` is a design failure.

## The 10 Phases

Execute in strict order. Each phase matters.

### Phase 1: Brand Extraction
Using the scraped content and assets:
- Analyze the logo (already downloaded to `original-site/assets/`)
- Extract brand colors, typography personality, visual tone
- Determine light/dark background compatibility
**Output:** Internal notes (not a separate file — fold into REBUILD_PLAN.md)

### Phase 2: SEO Audit
Using the scraped meta data and the audit report:
- Document all SEO issues found
- Identify target keywords for this business + location (e.g., "plumber Coeur d'Alene")
- Plan local SEO strategy (Google Business schema, NAP consistency, local keywords)
- Plan content strategy (what pages need what keywords)
**Output:** SEO section of REBUILD_PLAN.md

### Phase 3: Design & UX Audit
Using the audit report already created by `/prospect-audit`:
- Summarize what's wrong with their current design
- Identify specific improvements we'll make
- Set the aesthetic direction (what style fits THIS business?)
**Output:** Design section of REBUILD_PLAN.md

### Phase 4: Rebuild Plan
Synthesize everything into a concrete plan:
1. **Site Architecture** — page list, nav structure, URL structure
2. **Design Direction** — color palette (with WCAG contrast pre-verified), typography selections, component style, overall personality
3. **Image Strategy** — KEEP / ENHANCE / REPLACE for each image
4. **Copy Strategy** — what to rewrite vs. keep, tone of voice, key messages
5. **SEO Plan** — target keywords per page, schema types, meta strategy
6. **Technical Plan** — any special integrations, forms, maps
7. **Accessibility Targets** — zero critical/serious violations
8. **IMAGE DOWNLOAD** — Follow the Image Selection Protocol below, then download ALL images before writing any component code.

   ```bash
   mkdir -p ~/prospect-pipeline/sites/<slug>/public/images
   # Download each planned image:
   curl -sL -o ~/prospect-pipeline/sites/<slug>/public/images/hero.jpg "https://images.unsplash.com/photo-XXXXX?auto=format&fit=crop&w=2400&q=85"
   ```

   Verify images exist before proceeding:
   ```bash
   ls -la ~/prospect-pipeline/sites/<slug>/public/images/
   ```
   The directory must contain at minimum: hero image, about section image, at least one services image. If it doesn't, download them now.

**Generate DESIGN.md:** After defining the design direction above, formalize it as a structured `DESIGN.md` file using the `design-system-generator` skill.

1. Read `00-design-references/design-md-format.md` for the 9-section format.
2. Select 1-2 reference DESIGN.md files from `00-design-references/references/by-aesthetic/` matching the aesthetic direction.
3. Generate `DESIGN.md` with all 9 sections. The plain English design commitment becomes Section 1 (Visual Theme) and Section 7 (Do's and Don'ts).
4. REBUILD_PLAN.md Design Direction section should say "See DESIGN.md for the complete design system."

**Output:** `DESIGN.md` in the project root (alongside REBUILD_PLAN.md)

**Output:** `~/prospect-pipeline/prospects/<slug>/REBUILD_PLAN.md`

### Phase 5: Build the Website

**Read the project's `DESIGN.md` before writing any code.** Translate Section 2 into CSS custom properties, Section 3 into font imports and typographic scale, Section 4 into component implementations, and Section 6 into shadow tokens. The DESIGN.md is the source of truth for all visual implementation.

Before writing code, confirm images are downloaded: `ls ~/prospect-pipeline/sites/<slug>/public/images/`. If empty, go back to Phase 4 step 8.

Build in `~/prospect-pipeline/sites/<slug>/`:

1. **Initialize the Astro project** using the exact commands from the Tech Stack section above.

2. **Set up the design system:**
   - Create `src/styles/global.css` with CSS custom properties for all brand colors, typography, and spacing
   - Add WCAG contrast ratios as comments next to each color pairing
   - Import fonts via @fontsource packages or `<link>` tags

3. **Build the BaseLayout** (`src/layouts/BaseLayout.astro`):
   - `<html>`, `<head>` with meta tags, OG tags, fonts, global CSS
   - `<ViewTransitions />` for smooth page transitions
   - Shared Header/Nav and Footer components
   - Skip-to-content link as first focusable element
   - JSON-LD structured data slot

4. **Build every page** per the architecture in REBUILD_PLAN.md:
   - Each page is a `.astro` file in `src/pages/`
   - Include a polished 404.astro
   - Make each page dramatically better than what the business currently has
   - Every hero section must use a real photograph, not CSS gradients
   - Use Astro `<Image>` component for optimized images where possible

   **CRITICAL — TEXT CONTRAST OVER IMAGES (this fails QA constantly):**
   When placing text over a hero image or any photograph:
   - ALWAYS add a dark overlay behind light text: `bg-black/50` or `bg-gradient-to-t from-black/70 to-black/30`
   - ALWAYS add a light overlay behind dark text: `bg-white/60` or similar
   - NEVER put white text directly on a light/bright photograph
   - NEVER put dark text directly on a dark photograph
   - Test mentally: if the image is mostly sky/clouds (bright), you need a dark overlay. If the image is mostly shadows/dark, you need the overlay even more for white text.
   - The overlay must cover the ENTIRE text area, not just a thin strip
   - Add `text-shadow: 0 2px 4px rgba(0,0,0,0.5)` as extra insurance on hero headings
   - Example pattern:
     ```html
     <section class="relative h-[80vh]">
       <img src="/images/hero.jpg" class="absolute inset-0 w-full h-full object-cover" />
       <div class="absolute inset-0 bg-black/50"></div> <!-- dark overlay -->
       <div class="relative z-10 flex items-center h-full">
         <h1 class="text-white text-5xl font-bold" style="text-shadow: 0 2px 4px rgba(0,0,0,0.5)">
           Heading Text Here
         </h1>
       </div>
     </section>
     ```
   This applies to EVERY section where text sits on top of a photograph — hero, about, testimonials, CTA banners, page headers. No exceptions.

5. **Images — every site MUST have at minimum:**
   - A hero image (full-width, atmospheric, sets the mood)
   - An about/story section image (business, workspace, or team)
   - Team photos (actual photos from their site)
   - At least 1 image per major content section
   - Reference by path: `/images/filename.jpg` for public/ files, or import from `src/assets/` for optimized
   - **A site with no images or only CSS gradients is UNACCEPTABLE and will not pass QA.**

6. **Comprehensive SEO:**
   - Unique `<title>` and `<meta name="description">` per page
   - Open Graph and Twitter Card meta tags
   - JSON-LD schema (LocalBusiness type) with NAP data
   - Sitemap via @astrojs/sitemap (already installed)
   - `public/robots.txt`
   - Canonical URLs
   - Semantic HTML throughout (proper heading hierarchy, landmarks, etc.)

7. **Generate favicon** — complete set from logo (at minimum: favicon.svg in public/)

8. **Accessibility:**
   - WCAG AA contrast on all text/background combinations
   - **ESPECIALLY check text-over-image contrast** — every hero, banner, and CTA section with a background photo MUST have an overlay (dark overlay for light text, light overlay for dark text). This is the #1 accessibility failure in builds.
   - Full keyboard navigation with visible focus indicators
   - ARIA labels only where native HTML semantics are insufficient
   - `prefers-reduced-motion` media query wrapping all animations
   - Skip-to-main-content link

9. **Performance** — Astro handles most of this automatically:
   - Static HTML output (zero JS by default)
   - Optimized images via `<Image>` component
   - Optimized fonts via @fontsource (self-hosted, no external requests)
   - Target: Lighthouse 95+ (Astro sites achieve this easily)

### Image Selection Protocol

**Why this matters:** Grabbing the first stock photo that matches a keyword produces embarrassing results. A salon site showed a man's beard trim when the business only serves women. An about page had a bright white interior for a brand with a dark industrial aesthetic. Think carefully about every image.

This protocol applies to ALL business types. It is not industry-specific.

**Step 1: Understand the business deeply before picking any images**

Read the scraped content, services, team info, Google reviews, and audit. Build a mental model:
- What does this business actually DO day-to-day?
- Who are their customers? (homeowners, other businesses, families, professionals, etc.)
- What's the vibe? (premium/luxury, blue-collar/hardworking, family-friendly, clinical/professional, creative/artistic)
- What does their physical space look like?
- What would the business owner be PROUD to show on their website?

A plumber's site needs clean professional work, neat uniforms, a friendly technician at a door. NOT a wrench on a white background.
An accountant's site needs trust and expertise. NOT a "handshake in front of a skyline" stock photo.
A construction company needs real job sites, finished projects, crews at work. NOT clip art of hard hats.

**Step 2: Read the copy, then choose the image**

For every image slot, read the surrounding copy FIRST. The image must reinforce what the text communicates.

- "Family-owned for 20 years" → warm, personal, team or workspace with character
- "Precision and attention to detail" → close-up work that demonstrates craft
- Customer service section → people interacting, not just equipment
- Testimonial → evoke the feeling the testimonial describes

DO NOT just search Unsplash for the business category and grab the first result.

**Step 3: Use their actual photos first, stock as last resort**

Priority order:
1. **Their actual team photos** (from `original-site/assets/team/`). ALWAYS use for team/about sections. Never use stock people for named real humans.
2. **Their actual work/project photos** (from scrape). Office, shop, finished projects — use these.
3. **Their Google Maps/Business photos** (downloadable via Apify). Interior, exterior shots.
4. **Carefully chosen stock photos** for supporting/decorative slots ONLY.

**Step 4: Visual verification for every stock image**

Before using a stock image, verify:
- Does the color temperature match the design system?
- Does it feel like the same geographic/cultural context? (Manhattan skyline behind a rural Idaho plumber is absurd)
- Could the business owner say "yeah, that looks like us"?
- Right demographic for the actual customer base?
- Does it match the section's copy, not just vaguely "related to the industry"?

If you can't answer yes to all, pick a different image. A well-chosen abstract/texture is better than a wrong specific photo.

**Step 5: Create an image plan before building**

```
IMAGE PLAN for [Business Name]:
- Hero: [description, source, why it fits]
- About section: [description, source, why it fits]
- Team - [Name]: [their actual photo from assets/team/]
- Services section: [description, source, why it fits]
- Contact section: [description, source, why it fits]
```

**Step 6: Cross-check during QA**

During QA, visually inspect every page using `preview_screenshot`:
- Do team photos show the ACTUAL team members?
- Do images match the brand's color palette and mood?
- Would the business owner feel represented?
- Is there any image that feels "off" or generic? Replace it.
- Run the broken image check (see QA section).

**Visual quality bar:** This must look like a $20,000+ agency build. Stunning. Not good — stunning.

### Phase 6: Copy Audit & Optimization
Read through every word on the rebuilt site:
- Value prop clear within 5 seconds of landing?
- Every page has a benefit-driven CTA visible without scrolling?
- Lead with benefits, address objections, use specific numbers
- 8th-grade reading level, short sentences for impact
- Testimonials placed near CTAs and decision points
- Hook → Problem → Solution → Proof → Action flow

Wordsmith every paragraph. This is a sales tool.

**Output:** `~/prospect-pipeline/prospects/<slug>/COPY_CHANGES.md`

### Phase 7: Combined QA
Single comprehensive pass covering functional, copy, and visual:

1. Run the site locally with `preview_start`
2. Open every page and take screenshots with `preview_screenshot`
3. **Images check (do this first):**
   - Count images on homepage: `document.querySelectorAll('img').length`
   - If fewer than 3 images, go back to Phase 5 and add images before continuing.
   - Verify: hero has a real photograph, about section has a real photograph, services has images.
   - If any are missing, download appropriate images and add them.
4. **Functional:** Check every link, image, form, interactive element at mobile + desktop
5. **Copy:** Read as a first-time customer. Understand in 5 seconds? Trust? Know what to do?
6. **Visual:** Animations smooth? Typography beautiful? Whitespace balanced? Colors cohesive? Photos beautiful and relevant?
7. **Accessibility:** Verify contrast ratios on all color pairings. Keyboard nav works. Focus indicators visible.
8. **Design system consistency:** Verify that every CSS custom property in `global.css` maps to a token defined in DESIGN.md. No orphan tokens, no missing tokens.
9. Compare to best in industry — it should be BETTER.

### Broken Image Check
Before deploying, verify ALL images load:
1. Start dev server with `preview_start`
2. Visit every page (/, /about, /services, /contact)
3. On each page, run via `preview_eval`:
   ```js
   Array.from(document.querySelectorAll('img')).filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src)
   ```
4. If ANY broken images:
   - External URL → download locally to `public/images/` and update src
   - Wrong path → fix the path
   - Corrupted → re-download
5. **NEVER hotlink images from the prospect's original website.** Always use local files.
6. **NEVER leave external Unsplash URLs in production.** Download all stock images locally.
7. Re-run check after fixes. Do not deploy until all images load.

**Output:** `~/prospect-pipeline/prospects/<slug>/QA_REPORT.md`

### Phase 8: Pre-Deploy Checklist
Verify every item:
- SEO: unique meta tags, OG tags, structured data, heading hierarchy, alt text, sitemap, robots.txt
- Performance: images optimized, fonts self-hosted, all pages static. Lighthouse 95+.
- Accessibility: all colors WCAG AA. Keyboard nav works. Focus indicators visible.
- Functionality: every link, form, element works. Mobile nav works. 404 page works.
- Content: no placeholders, no typos, all business info accurate.
- Visual: design consistent, polished at every viewport. No banned fonts.

### Phase 9: Prepare for Deployment
The site is built in `~/prospect-pipeline/sites/<slug>/`. Prepare it:
- Verify `.gitignore` is appropriate (Astro generates one during init)
- Create a `README.md` with project overview and how to run locally
- Mark the prospect `status` as `"built"` in `info.json`
- Add `built_date` to `info.json`
- Update `pipeline.json`: increment `total_built`

Note: Actual deployment to GitHub/Vercel is handled by the `/prospect-deploy` skill.

### Phase 10: Summary
Output what was built:
```
LOCAL BUSINESS REBUILD COMPLETE
================================
Business:      Bob's Plumbing
Location:      Coeur d'Alene, Idaho
Category:      Plumber
Site Path:     ~/prospect-pipeline/sites/bobs-plumbing/
Framework:     Astro 5.x + Tailwind CSS v4
Pages Built:   7 (Home, About, Services, Gallery, Contact, FAQ, 404)
Design:        [brief description of aesthetic]
Key Features:  [list notable features]
SEO:           LocalBusiness schema, 8 target keywords, sitemap
Accessibility: WCAG AA, all contrast verified
Performance:   Static HTML, zero JS, Lighthouse 95+
Ready for:     /prospect-deploy
```

## Reference Files

This skill inherits the design philosophy from the main website-rebuild skill:
- [design-rules.md](references/design-rules.md) — Non-negotiable design rules
- [accessibility-spec.md](references/accessibility-spec.md) — WCAG AA specification

## Key Differences from Full Website Rebuild

| Aspect | Full Rebuild | Local Business Rebuild |
|--------|-------------|----------------------|
| Phases | 14 | 10 |
| Tools research | Deep competitive research | None |
| Tools build | 2-5 interactive tools | None |
| QA rounds | 3 separate rounds | 1 combined round |
| Copy audit | Full | Full (kept per user request) |
| Rebuild plan | Full documentation | Full (kept per user request) |
| Deploy | Individual GitHub repo + Vercel | Monorepo path only (deploy is separate skill) |
| Input | URL provided by user | Scraped content from prospect-scrape |
| Output | Live deployed site | Built site in monorepo, ready for deploy |

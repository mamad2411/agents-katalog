---
name: website-rebuild
description: >
  Full website rebuild agent. Takes an existing website URL and rebuilds it from
  scratch into a world-class, SEO-optimized, WCAG AA accessible, visually stunning
  website using Astro + Tailwind CSS, deployed to Vercel via GitHub.
  Executes a rigorous 14-phase process: brand extraction, content scraping, SEO audit,
  design audit, rebuild planning, full build with design system, copy optimization,
  3 QA rounds, competitive tools research, tools build, tools QA, pre-deploy checklist,
  and Vercel deployment. Produces 11+ documentation deliverables.
  Triggers on: "rebuild website", "redesign website", "rebuild site from URL",
  "website rebuild", "redo this website", "make this website better", "rebuild from scratch",
  "full site redesign", or any request to take an existing URL and create a new,
  professional website from it. Also triggers when the user provides a URL and asks
  to build/create/design a new version of that site.
---

# Full Website Rebuild Agent

Take an existing website URL and rebuild it from scratch into an extraordinary, production-ready website. The result should look like a $20,000+ agency build — visually stunning, conversion-optimized, fully accessible, and SEO-complete.

## How This Skill Works

This skill runs 14 phases in strict order. Each phase produces documentation before moving on. Do not skip or reorder phases. The user provides a URL and you do the rest.

**Input:** A website URL (the site to rebuild)
**Output:** A live Vercel-deployed website + GitHub repo + 11 documentation files

## Tech Stack — Exact. Do Not Deviate.

**Framework:** Astro 5.x — static site generator, zero JavaScript by default, perfect for SEO.
**Styling:** Tailwind CSS v4 (via Vite plugin)
**Images:** Astro `<Image>` component from `astro:assets` (built-in optimization, WebP/AVIF)
**SEO:** `@astrojs/sitemap` integration + manual JSON-LD
**View Transitions:** Astro View Transitions (built-in, zero JS page transitions)
**Blog/Content:** Astro Content Collections with MDX. Frontmatter: title, date, description, author, tags, featuredImage.
**Deployment:** Vercel via GitHub (push to main = auto-deploy)
**Package Manager:** npm (not pnpm, not yarn — npm only)
**Linting:** ESLint + Prettier from the start

### Initialization — Run These Exact Commands

```bash
npm create astro@latest <project-name> -- --template minimal --no-install
cd <project-name>
npm install
npx astro add tailwind --yes
npx astro add sitemap --yes
npx astro add mdx --yes
npm install -D prettier
```

That's it. The project is ready.

### If Something Fails During Build

Fix the code. Do NOT:
- Switch Node versions
- Switch package managers
- Reinstall the framework
- Add React or any other UI framework unless specifically needed for an interactive tool (Phase 11b)
- Change the project structure

### Astro File Structure

```
src/
  layouts/
    BaseLayout.astro       ← shared HTML shell, <head>, nav, footer
    BlogPostLayout.astro   ← blog post template
  pages/
    index.astro            ← homepage
    about.astro            ← about page
    services.astro         ← services page
    contact.astro          ← contact page
    blog/
      index.astro          ← blog listing
      [...slug].astro      ← dynamic blog post pages
    tools/                 ← interactive tools (Phase 11b)
    404.astro              ← custom 404
  components/
    Header.astro           ← navigation
    Footer.astro           ← footer
    Hero.astro             ← hero section
    ...                    ← section components as needed
  content/
    config.ts              ← content collection schema
    blog/
      *.mdx                ← blog posts
  styles/
    global.css             ← @import "tailwindcss"; + CSS custom properties
  assets/
    images/                ← optimized images (processed by Astro)
public/
  images/                  ← static images (served as-is)
  favicon.svg
  robots.txt
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
- No `useState`, no `useEffect`, no client-side state. Pages are static HTML.
- For interactive tools (Phase 11b), use Astro Islands: add `client:load` to a component that needs JavaScript.
- Images: Import from `src/assets/images/` for optimization, or reference `public/images/` for static files.
- CSS custom properties go in `src/styles/global.css` and are available everywhere.
- View Transitions: Add `<ViewTransitions />` to the `<head>` in BaseLayout for smooth page transitions — zero JavaScript.

### Google Fonts

Load via @fontsource packages (self-hosted, no external requests):

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

## Design — Delegated to Specialized Skills

**All visual design decisions are handled by dedicated design skills. Do NOT make design choices from static rules — invoke the skills instead.**

### Required Design Skills (invoke during Phase 5 and Phase 6):

1. **`frontend-design-anthropic`** — Use this skill for ALL visual design decisions: color palette, typography, layout composition, motion, component styling. Load this skill before writing any CSS or choosing any visual direction. It handles aesthetic commitment, font selection, color systems, spacing, and animation philosophy.

2. **`web-design-guidelines`** — Use this skill to VALIDATE design choices against professional web design standards. Run this after building each major page to check for compliance issues, accessibility problems, and design anti-patterns.

### How to use them in the build process:

- **Phase 5 (Rebuild Plan):** Before defining the design direction, invoke `frontend-design-anthropic` to establish the aesthetic, color palette, typography pairing, and component patterns. Document these choices in REBUILD_PLAN.md.
- **Phase 6 (Build):** Apply the design system from `frontend-design-anthropic` to every component and page. Use it for every visual decision — don't fall back to generic Tailwind defaults.
- **Phase 8-10 (QA):** Run `web-design-guidelines` against each page to validate design quality. Fix any issues flagged before proceeding.

### What this skill still owns (non-design):
- Tech stack decisions (Astro + Tailwind)
- Self-hosted fonts via @fontsource (the design skill picks WHICH fonts)
- CSS custom properties architecture
- Performance targets (Lighthouse 95+)
- Image optimization via Astro `<Image>` component

## Accessibility & Contrast (Critical)

Read [accessibility-spec.md](references/accessibility-spec.md) for the complete specification.

### Contrast Minimums (WCAG AA)
| Text Type | Minimum | Target |
|---|---|---|
| Normal body text (< 18px) | 4.5:1 | 7:1 |
| Large text (>= 18px or >= 14px bold) | 3:1 | 4.5:1 |
| UI components, borders, icons | 3:1 | 4.5:1 |
| Placeholder text in inputs | 4.5:1 | 7:1 |
| Focus indicators | 3:1 | 4.5:1 |

### Verification
- During QA, use `preview_eval` to run axe-core checks via CDN on each page
- Fix every CRITICAL and SERIOUS violation before moving on
- Verify contrast ratios for every color combination — document as comments in global.css
- Never trust visual inspection alone

### Common Failures to Avoid
- Light gray text on white (any gray lighter than #595959 on #FFF fails)
- White text on pale brand color buttons
- Dark text on dark hero backgrounds
- Hover/focus states that reduce contrast
- Overlay text on images without sufficient opacity
- Gradient text where lightest point fails contrast

## The 14 Phases

Execute these in exact order. Do not skip or reorder. Each phase has detailed instructions in [phase-details.md](references/phase-details.md).

### Phase 1: Visual Inspection & Brand Extraction
Open the URL in Chrome browser. Visit every page. The logo is the design anchor — extract brand colors (hex), typography personality, visual tone. Download logo files.
**Output:** `BRAND_BRIEF.md`

### Phase 2: Data Scraping & Content Classification
Write and run a scraping script. Extract all text, images, links, nav structure, contact info, forms, media, meta tags, testimonials, structured data. Classify as MUST REUSE or CAN MODIFY/REPLACE.
**Output:** `CONTENT_INVENTORY.md`

### Phase 3: Comprehensive SEO Audit
Technical SEO (speed, mobile, URLs, sitemap, robots.txt, HTTPS, canonicals, 404s, redirects). On-page SEO (titles, descriptions, headings, alt text, internal links, keywords). Content strategy (blog gaps, local SEO, schema markup).
**Output:** `SEO_AUDIT.md`

### Phase 4: Design & UX/UI Audit
Visual design (aesthetic, color, typography, spacing, hierarchy). UX (nav, CTAs, mobile, flow, trust signals). Conversion optimization (CTA placement, value prop, social proof).
**Output:** `DESIGN_AUDIT.md`

### Phase 5: Rebuild Plan
Synthesize Phases 1-4. Site architecture, design direction (invoke `frontend-design-anthropic` skill for typography, color palette, layout direction), image strategy (KEEP/ENHANCE/REPLACE/CREATE), copy strategy, SEO implementation plan, tools research placeholder, technical plan, accessibility targets. All color palettes must pass WCAG AA contrast verification.
**Output:** `REBUILD_PLAN.md`

### Phase 5b: Generate DESIGN.md

After completing the Rebuild Plan, generate a `DESIGN.md` file in the project root using the `design-system-generator` skill. This is the machine-readable design system that Phase 6 will consume.

1. Read `00-design-references/design-md-format.md` for the required 9-section structure.
2. Browse `00-design-references/design-md-index.md` and select 1-2 reference DESIGN.md files that match the chosen aesthetic direction. Read them for structural inspiration.
3. Generate the project's DESIGN.md with all 9 sections populated from the design decisions made during Phase 5 and the `frontend-design-anthropic` skill invocation.
4. Every color must include its hex value, semantic role, and WCAG contrast ratio against its intended background.
5. Typography must include the complete hierarchy table (role, family, size, weight, line-height, letter-spacing).
6. Component stylings must define button states, card patterns, and input styles with exact CSS values.
7. The "Design Direction" section in REBUILD_PLAN.md should reference the DESIGN.md file: "See DESIGN.md for the complete design system" plus a 3-line summary.

**Output:** `DESIGN.md` in the project root

### Phase 6: Build the Website
**Read the project's `DESIGN.md` before writing any visual code.** Use Section 2 (Color Palette) as the source for CSS custom properties in `global.css`. Use Section 3 (Typography) for font imports and the typographic scale. Use Section 4 (Component Stylings) for button, card, input, and nav component implementations. Use Section 6 (Depth & Elevation) for shadow tokens. The DESIGN.md is the single source of truth — do not fall back to generic Tailwind defaults when the DESIGN.md specifies a value.

Invoke the `frontend-design-anthropic` skill before writing any visual code. Build sequence:
1. **Initialize the Astro project** using the exact commands from the Tech Stack section above.
2. **Design system first:** CSS custom properties in global.css, component primitives, layout patterns. Document WCAG contrast ratios as comments next to every color pairing.
3. **Build every page** per site architecture. Include polished 404. Make each page dramatically better.
4. **Handle images:** KEEP→optimize with Astro `<Image>`, ENHANCE→Nano Banana, REPLACE→Unsplash (download locally). All images must be local files, never external URLs.
5. **Comprehensive SEO:** meta tags, JSON-LD schema, sitemap (via @astrojs/sitemap), robots.txt, canonicals, semantic HTML.
6. **Generate favicon** — complete set from logo.
7. **Accessibility:** WCAG AA verified. Keyboard nav, focus indicators, ARIA, skip-to-content.
8. **Performance:** Astro handles most of this (zero JS, static HTML). Self-hosted fonts via @fontsource. Target Lighthouse 95+.

**Visual quality bar:** Stunning. Not good — stunning. Think Apple, Stripe, Linear.

### Phase 7: Copy Audit & Optimization
Value prop clear within 5 seconds. Every page has a benefit-driven CTA visible without scrolling. Lead with benefits, address objections, use specific numbers, 8th-grade reading level. Hook -> Problem -> Solution -> Proof -> Action flow.
**Output:** `COPY_CHANGES.md`

### Phase 8: QA Round 1 — Functional & Content
Run locally, open in Chrome, visit every page. Check links, images, forms, interactives at mobile/tablet/desktop. Verify contrast ratios, fix all critical/serious accessibility violations.
**Output:** `QA_ROUND_1.md` + update `ACCESSIBILITY_AUDIT.md`

### Phase 9: QA Round 2 — Copy & Messaging
Read entire site as a first-time customer. Can I understand the business in 5 seconds? Do I trust them? Do I know what to do next? Make final copy adjustments.
**Output:** `QA_ROUND_2.md`

### Phase 10: QA Round 3 — Final Visual & Polish
Every page at all viewport sizes. Run `web-design-guidelines` skill against each page. Animations smooth? Typography distinctive? Whitespace balanced? Colors cohesive? Final accessibility pass. Compare to best in industry — it should be BETTER.
**Output:** `QA_ROUND_3.md`

### Phase 11a: Competitive Tools Research Sprint
This is critical — no tool is built without research first. Budget assumption: unlimited.
1. Identify top 10-15 competitors and best-in-class sites via web search.
2. Visit each with Chrome. Document every interactive tool, calculator, quiz, configurator, estimator.
3. Search broader web: "[industry] calculator/estimator/tool", Product Hunt, G2, industry directories.
4. Synthesize: competitor inventory, best-in-class examples, gap analysis, ranked shortlist (value x conversion x uniqueness x feasibility), final selection of 2-5 tools.
**Output:** `TOOLS_RESEARCH.md`

### Phase 11b: Client-Facing Tools — Build
Build only tools approved in TOOLS_RESEARCH.md. Create /tools or /resources section.

For interactive tools that need client-side JavaScript, use **Astro Islands**:
- Create a component in your preferred UI framework (React, Preact, Svelte, or vanilla JS)
- Add `client:load` or `client:visible` directive when using the component in an `.astro` page
- If using React for tools: `npx astro add react --yes` (ONLY add React when you reach this phase, not before)
- Each tool gets its own page with title, description, the interactive tool, and a CTA
- Mobile-responsive, design-system consistent, accessible

### Phase 12: QA Round 4 — Tools QA
Test each tool in Chrome with valid inputs, edge cases (zero, huge numbers, empty), mobile viewport. Verify calculations, input validation, errors, appearance, CTA. Accessibility check on every tool page.
**Output:** `QA_ROUND_4.md`

### Phase 13: Pre-Deployment Checklist
Verify every item in the checklist. See [phase-details.md](references/phase-details.md) for the full checklist covering: SEO, Performance, Accessibility, Contrast, Functionality, Content, Visual, Design System, Favicon, Docs.

### Phase 14: Deploy
Initialize git, .gitignore, README.md (project overview, tech stack, how to run, how to add blog posts, structure). Commit and push to new GitHub repo. Connect to Vercel, configure build settings (Astro auto-detected by Vercel). Open live URL in Chrome, spot-check everything. Final accessibility scan against live URL.

## Nano Banana Image Enhancement

When enhancing team/people photos, use OpenRouter API. See [nano-banana.md](references/nano-banana.md) for the script template. Verify current model string and endpoint at docs.openrouter.ai before running.

## Blog Infrastructure

Set up using Astro Content Collections with MDX. New posts are added by creating an `.mdx` file in `src/content/blog/` with frontmatter (title, date, description, author, tags, featuredImage), then pushing to main. Blog listing auto-picks up new posts sorted by date. Individual posts include: beautiful long-form typography, table of contents for long posts, social sharing buttons, CTA at bottom.

## Final Deliverables

| # | Deliverable |
|---|---|
| 1 | Live Vercel website — stunning, animated, responsive, SEO-optimized, WCAG AA, with research-validated tools |
| 2 | GitHub repo — clean code, README with blog instructions, auto-deploys on push |
| 3 | BRAND_BRIEF.md |
| 4 | CONTENT_INVENTORY.md |
| 5 | SEO_AUDIT.md |
| 6 | DESIGN_AUDIT.md |
| 7 | REBUILD_PLAN.md |
| 8 | TOOLS_RESEARCH.md |
| 9 | ACCESSIBILITY_AUDIT.md |
| 10 | COPY_CHANGES.md |
| 11 | QA_ROUND_1.md through QA_ROUND_4.md |
| 12 | DESIGN.md — structured design system specification with all tokens, typography, components, and shadows |

## Guiding Principles

- **Quality over speed.** Every phase matters. Fix issues before moving on.
- **Visually stunning is not optional.** Gorgeous visuals, subtle animations, beautiful typography, intentional whitespace. A living, breathing, premium digital experience.
- **Design excellence is non-negotiable.** $150,000+ agency quality. Use the `frontend-design-anthropic` skill for every visual decision. Validate with `web-design-guidelines`.
- **Accessibility is baked in from Phase 5.** Contrast ratios computed before colors are finalized. Verified at every QA stage. WCAG AA is the floor.
- **SEO is baked in, not bolted on.** URL structure, headings, alt text, content strategy — all informed by SEO from the start.
- **The copy must sell.** This is a sales tool. Every page guides toward action.
- **Test like a skeptic.** Actively try to break things during QA.
- **Think like the customer.** What do THEY need? What makes THEM trust and act?
- **Research before you build.** Especially for tools. Never build from guesswork.
- **Use your judgment.** This gives you the roadmap and standards. You're the expert on execution.

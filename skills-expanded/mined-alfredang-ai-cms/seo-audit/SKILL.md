---
name: seo-audit
description: SEO audit and on-page optimization for Tertiary Infotech pages (Next.js App Router + Drizzle CMS). Use when creating or reviewing any public route under src/app — landing pages, service pages, blog posts, or DB-backed pages. Covers crawlability, indexation, Core Web Vitals, on-page (titles, meta, headings, internal links, images, schema), and content quality. Triggers — "SEO audit", "SEO review", "optimize for search", or any task that adds/edits a public-facing page or its metadata.
---

# SEO Audit — Tertiary Infotech

You are the SEO expert for **Tertiary Infotech** (https://www.tertiaryinfotech.com), a Singapore-based provider of AI-powered LMS/TMS, SSG ATO consultancy, course development, and TPQA services. Your job is to identify SEO issues and ship concrete fixes inside this Next.js codebase.

## Before You Start

1. Read [src/app/layout.tsx](src/app/layout.tsx) for the site-wide `metadata` defaults (title template, description, OG).
2. Read [src/app/sitemap.ts](src/app/sitemap.ts) and [src/app/robots.ts](src/app/robots.ts) to understand which routes are exposed.
3. Inspect the target route's `page.tsx` for its `export const metadata` (or `generateMetadata`) export.
4. Check [src/lib/site-content.ts](src/lib/site-content.ts) for canonical service copy — keep on-page wording consistent with the rest of the site.
5. If `.claude/product-marketing-context.md` exists, read it first and skip questions answered there.

## Brand & Audience Context (use this verbatim where relevant)

- **Brand**: Tertiary Infotech — AI-LMS-TMS for WSQ & TPQA Compliance.
- **Locale**: `en_SG` (Singapore English). Use British/Commonwealth spelling: *organisation*, *centre*, *programme*.
- **Primary ICPs**: (a) new training providers preparing SSG/TPGateway ATO applications; (b) existing ATOs needing TPQA/WSQ compliance support; (c) corporate L&D teams evaluating LMS/TMS; (d) SMEs needing custom AI/automation.
- **Money keywords** (Singapore intent, low-medium difficulty, high commercial intent):
  - `SSG ATO application Singapore`, `apply ATO Singapore`, `become accredited training organisation Singapore`
  - `TPGateway organisation registration`, `RTP registration Singapore`, `WSQ training provider registration`
  - `TPQA audit consultancy`, `TPQA compliance Singapore`, `WSQ course development`
  - `LMS for training providers Singapore`, `WSQ LMS`, `e-attendance SSG`
  - `Approved Training Organisation Singapore` (high-volume head term — use sparingly, lean on specific intent variants)
- **Never use**: SSG or SkillsFuture logos in copy/images (regulator restriction). Don't claim affiliation with SSG.

## Audit Coverage

### 1. Crawlability & Indexation
- Page must be reachable from at least one internal link (homepage section, nav, footer, or sibling page).
- Must appear in `src/app/sitemap.ts` — either as a hardcoded entry or via the `pages` DB table.
- `robots.ts` should not disallow it.
- `metadata.robots` should default to indexable. Only block with `{ index: false }` for thank-you/admin/preview routes.
- Use a canonical URL via `metadata.alternates.canonical` (absolute, on `https://www.tertiaryinfotech.com`).

### 2. On-Page Metadata (every public route)
- `title`: ≤ 60 chars, includes primary keyword + brand suffix (template handles brand: `"%s | Tertiary Infotech"`).
- `description`: 140–160 chars, contains primary keyword, ends with a clear CTA verb ("Book a free consultation", "Talk to our SSG consultants").
- `openGraph`: `title`, `description`, `url`, `images: [{ url, width: 1200, height: 630, alt }]`, `locale: "en_SG"`, `type: "website"` (or `"article"` for blog).
- `twitter`: `card: "summary_large_image"`.
- `alternates.canonical`: absolute URL.

### 3. Headings & Structure
- Exactly **one** `<h1>` per page, containing the primary keyword (natural phrasing, not stuffed).
- `<h2>` for major sections; `<h3>` for sub-points. No skipped levels.
- Hero h1 must not be wrapped inside another heading. The page's h1 should differ from the sitewide title only in subtitle/style, not topic.

### 4. Internal Linking
- Every new page should be linked from: (a) the homepage Services grid if it's a service, (b) the footer if evergreen, (c) at least one related page.
- Use descriptive anchor text — never "click here" or "learn more" alone (wrap with surrounding context: `<Link>Apply for SSG ATO registration →</Link>`).
- Add 2–4 contextual outbound links to official sources where helpful (e.g., `tpgateway.gov.sg`, `skillsfuture.gov.sg`) with `rel="noopener"` (no `nofollow` for trusted government sources).

### 5. Images
- Use Next.js `<Image>` from `next/image` for all photographic/diagram content. Provide explicit `width`/`height` to prevent CLS.
- Every image needs descriptive `alt` text containing context (not just the filename).
- Decorative SVG backgrounds: `aria-hidden="true"` and no alt.
- Avoid loading large hero images above the fold without `priority` set.

### 6. Schema / Structured Data
- Inject JSON-LD via `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(...) }} />` inside the page (NOT in `metadata.other`).
- Required schemas by page type:
  - **Service page** (e.g. SSG ATO page): `Service` schema with `provider: { @type: "Organization", name: "Tertiary Infotech", url, logo }`, `areaServed: "Singapore"`, `serviceType`, `description`.
  - **Service page with steps**: ALSO include `HowTo` schema for the step-by-step process.
  - **FAQ block**: `FAQPage` schema mirroring the visible Q&A 1:1.
  - **Blog post**: `Article` schema with `author`, `datePublished`, `dateModified`, `image`.
  - **Sitewide**: `Organization` schema in `src/app/layout.tsx` (one-time).
- **Critical**: Validate rendered JSON-LD with the [Rich Results Test](https://search.google.com/test/rich-results) using the deployed URL. Static-HTML inspection is unreliable for JS-rendered schema — always test the live page.

### 7. Core Web Vitals (Next.js App Router specifics)
- Prefer Server Components (default in App Router). Mark with `"use client"` only when needed (forms, hooks).
- Use `next/font` (already loaded in `layout.tsx` — reuse the existing `Inter`, `Exo_2`, `JetBrains_Mono` setup; do not import Google Fonts directly).
- Lazy-load below-the-fold heavy sections with `next/dynamic` + `loading` skeleton.
- Avoid `force-dynamic` unless the route truly needs per-request data. Static-friendly routes should be cacheable.
- Hero `<img>` or `<Image>` → set `priority`. Below-fold images → default lazy.

### 8. Content Quality (E-E-A-T)
- Cite official Singapore government sources when claiming regulatory facts: TPGateway, SkillsFuture Singapore, IRAS, ACRA, IBF.
- Include author bio + photo on long-form posts. Use `Person` schema with `jobTitle`.
- Show last-updated date on regulatory pages (rules change — stale dates signal low trust).
- Word count target: service pages 800–1500, pillar pages 2000+, blog posts 1200+. Quality > word count, but don't ship 200-word service pages.

### 9. Mobile & Accessibility (Google ranks mobile-first)
- Tap targets ≥ 44×44px. The existing `btn-primary` class meets this.
- Color contrast: muted text `--color-muted` is `#AAA8B1` on `#060A14` — contrast ratio ≈ 9.7:1 (OK). White on cyan glow backgrounds — verify per-component.
- Form labels must be programmatically associated (use `<label htmlFor>` or wrap input).

## Deliverable Format

When auditing, return a **prioritized table**:

| # | Priority | Issue | Where | Fix |
|---|----------|-------|-------|-----|
| 1 | 🔴 High | Missing canonical URL | src/app/ssg-ato-application/page.tsx | Add `alternates.canonical: "https://www.tertiaryinfotech.com/ssg-ato-application"` to metadata |

**Priority scale**: 🔴 High (blocks indexing or major ranking factor) → 🟠 Medium (on-page polish, schema gaps) → 🟢 Low (nice-to-have, minor CWV tweaks).

When **creating** a new page from scratch, follow this checklist in order:

1. Pick the primary keyword and 2–3 supporting variants from the money-keyword list above.
2. Draft `title` (≤60ch), `description` (140–160ch), and the H1 around that keyword.
3. Outline H2/H3 sections that match search intent (informational + conversion).
4. Write the body using British/Singapore spelling. Use the brand voice: confident, technical, no hype.
5. Add a lead-capture CTA above the fold and at the end (link to `/#contact` or page-specific form).
6. Add JSON-LD: `Service` + `HowTo` (if process page) + `FAQPage` (if FAQ).
7. Register the route in `sitemap.ts` if not DB-backed.
8. Add an internal link from the homepage (Services grid for service pages) and footer.
9. Verify build: `npm run build` should succeed with no metadata warnings.

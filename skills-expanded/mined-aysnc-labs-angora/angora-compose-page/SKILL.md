---
name: angora-compose-page
description: Assemble or evolve Astro pages in `src/pages/*.astro` and layout specimens in `src/pages/design-system/layouts/` from already-built components — including list/detail patterns like `/collection` + `[slug].astro`, SEO wiring from table fields, and site layout (header/footer) integration. Trigger whenever the user wants to compose, assemble, build, or evolve a full page from existing components. Phrases like 'compose the pricing page', 'build the about page', 'wire up the blog index and [slug]', 'assemble the home from hero + pricing + CTA', 'put together the careers page', 'evolve the contact page to add a form section' all trigger this.
argument-hint: <page-name>
---

# Compose Page: $ARGUMENTS

Build or update a full site page from approved components. Pages are living documents — this skill handles both creation and evolution.

## Scope

This skill does two things:
- **Design system layouts** — full-page compositions in `src/pages/design-system/layouts/` using real components with placeholder content. These are specimens, not production pages.
- **Site pages** — real routes in `src/pages/` with production content, database queries, SEO, and site layout wrappers.

**Intent check:** When the user says "update the home page" or similar, clarify before proceeding: "Do you mean the **home layout** in the design system (`/design-system/layouts/home`), or the **actual website home page** at `src/pages/index.astro`?"

## Before you start

1. **Read `src/system.md`** — intent, accessibility standard, anti-patterns.
2. **Read `src/styles/global.css`** — available tokens for page-level spacing and backgrounds. All color references must use **semantic token utilities** — raw palette classes don't exist.
3. **Read [design-principles.md](../docs/design-principles.md)** — especially Spacing & Layout, Dark Mode, and Finishing Touches sections.
4. **Read [tailwind-conventions.md](../docs/tailwind-conventions.md)** — Tailwind v4 syntax rules.
5. **Inventory components** — list `src/components/*.astro` to know what's available. Only use approved, built components.
6. **Read `src/components/Section.astro`** — understand the Section pattern before composing pages. Section accepts: `seamless`, `fullWidth` (drops flow width constraint), `narrow` (constrains to `--container-narrow`), `withWrap` (re-constrains children of full-width sections), `withPadding` (adds vertical padding without seamless), `title` (renders `<h2>` with automatic `aria-labelledby`).
7. **Check for wireframe** — look for `src/pages/design-system/wireframes/<page-name>.astro`. If it exists, read it — especially the data source annotations in frontmatter.
8. **Check for layout** — look for `src/pages/design-system/layouts/<page-name>.astro`. If a layout exists, it's an approved composition showing how components assemble for this page. Use it as the reference — match its section order, component choices, and visual rhythm. The real page replaces placeholder content with real data but follows the same structure.
9. **Check for existing page** — look for `src/pages/<page-name>.astro`. If it exists, read it first. This is an evolution, not a rewrite.
10. **Check for site layout** — look in `src/layouts/` for existing site layouts (header/footer wrappers).

## Entry points

This skill can be invoked with:
- A **wireframe reference** — "compose the pricing page" (where a wireframe exists)
- A **component list** — "build a page with hero, features, and CTA"
- A **description** — "build our about page"

If no wireframe exists, recommend one ("Want me to sketch a wireframe first with `/angora-wireframe`?") but don't force it.

## Mandatory gate: static vs template per section

Before building, determine the data source for every section on the page.

If a wireframe exists with data source annotations, read them:
```
/*
  Data sources:
  sections:
    - component: Hero
      data: static
    - component: Testimonials
      data: table:testimonials
    - component: Pricing
      data: table:pricing_tiers
*/
```

If no wireframe or annotations, ask for each section:
- "Will this content change? Is there more than one?" → **template** (table reference)
- "Is this one-off copy edited in code?" → **static**

For **template sections**, verify the table exists by globbing `src/data/schema/tables/*.ts` — each file is a table definition.

If a required table doesn't exist, flag it: "The `testimonials` table doesn't exist yet. This needs schema work first. Run `/angora-schema testimonials` to design it."

## List/detail pattern

Recognize when cards link to individual pages (blog posts, case studies, cities, team members). This is a first-class pattern:

### List page
`src/pages/<collection>.astro`
- Query: `SELECT * FROM <table> WHERE status = 'published'`
- Renders cards/list items linking to `/collection/[slug]`

### Detail template
`src/pages/<collection>/[slug].astro`
- Uses `getStaticPaths()` to generate pages from database
- Query: `SELECT * FROM <table> WHERE status = 'published'`
- Wire up SEO from table fields: `<title>`, `<meta name="description">`, OG tags
- Only render published records

```astro
---
import db from '../../data/db.ts';
import { <table> } from '../../data/schema/tables/<table>';
import { eq } from 'drizzle-orm';

export function getStaticPaths() {
  const items = db.select().from(<table>).where(eq(<table>.status, 'published')).all();
  return items.map(item => ({
    params: { slug: item.slug },
    props: { item },
  }));
}

const { item } = Astro.props;
---
<html>
<head>
  <title>{item.metaTitle || item.title}</title>
  <meta name="description" content={item.metaDescription || ''} />
</head>
...
</html>
```

## Site layout

Ask: "Should this page have the site header/footer, or is it a standalone landing page?"

Check for `src/layouts/` — if no layout exists and user wants header/footer, flag it: "No site layout exists yet. Want me to create one, or should we build this as a standalone page for now?"

Site layouts go in `src/layouts/` (Astro convention). A site layout wraps page content with shared header/footer/nav.

## Output

- `src/pages/<page-name>.astro` — the site page
- Optional: `src/pages/<collection>/[slug].astro` — for list/detail patterns

## Form sections

When a page includes forms (contact, signup, settings), use the form layout primitives:

- **FieldGroup** — vertical stack of form rows with standard `grid-gap` spacing
- **FormRow** — horizontal row within a FieldGroup. Children grow to fill space by default. Use `grow={false}` for button rows

Every field inside a FieldGroup should be wrapped in a FormRow. Don't use raw `<div>` wrappers for form layout.

## Page-level concerns

- **Page wrapper uses `section-flow`** — `<main class="section-flow">` wraps all sections. The `section-flow` utility lives in `global.css` and controls inter-section spacing (gap controlled by `--section-gap`). For editorial content (blog posts, articles), use `<article class="prose-flow">` instead.
- **Ambient prose** — `section-flow` and `prose-flow` include prose automatically via `@apply prose`. Raw HTML elements get typographic styling from prose at low specificity (`:where()`) — component classes always win. Don't add `prose` separately. The only local `prose` usage is for nested content zones that need their own vertical rhythm.
- **Landmark components live on their own** — Hero, Footer, Nav go directly inside `section-flow`. They render their own semantic element with `data-component` and flow attributes (`data-seamless`, `data-full-width`). Don't wrap landmarks in `<Section>`.
- **Content components go inside `<Section>`** — the consumer controls `title`, `seamless`, `narrow`, `fullWidth`, `withWrap`. Use `<Section fullWidth withWrap>` when a section needs edge-to-edge background but children should stay constrained to container width.
- **Backgrounded sections use `seamless`** — `<Section seamless>` for sections with background colors/images. Adjacent seamless sections get 0 gap so backgrounds butt up.
- Background alternation for visual rhythm — use semantic surface tokens for section variety. These automatically adapt in dark mode
- Visual flow — the eye moves naturally through the page
- Responsive behavior via container queries
- SEO: `<title>`, `<meta name="description">`, OG tags
- **`color-scheme` meta tag** — already handled by `Layout.astro` for design system pages. For site pages, include `<meta name="color-scheme" content="light dark">` if the site supports dark mode, or `<meta name="color-scheme" content="light">` if light-only
- **Images in dark mode** — photographs on dark backgrounds can feel jarring. Use `dark:brightness-80 dark:contrast-125` on `<img>` elements to dim slightly. Avoid images with baked-in white backgrounds — they become glowing rectangles in dark mode. Prefer transparent or neutral backgrounds for logos and illustrations

## Layout purity rules (design system layouts only)

When building a layout in `src/pages/design-system/layouts/`, enforce these additional rules:

- **Single-file rule** — a layout page is one `.astro` file. No extracted sub-components, no helper modules. If the layout feels too complex for one file, the components are too coarse — refine them in `/angora-component`.
- **Zero-class layout rule** — layouts are pure component composition. No Tailwind utility classes on raw HTML elements. If you need to add a class to a `<div>`, a component is missing. **Allowed:** just `section-flow` on `<main>`. **Not allowed:** spacing wrappers (`<div class="mt-8">`), grid layouts (`<div class="grid grid-cols-2">`), visual treatments (`<div class="bg-card rounded-lg">`), styled headings, width constraints, Button wrapper divs, `class` overrides on components, raw markup.
- **No client-side code** — design system layouts are static. No inline `<script>` tags for interactivity. If a section needs interactivity, it should use a Preact island via the component itself.
- **Layout purity check** — after building, verify: single file? No client code? Zero-class compliance? Landmark components outside `<Section>`? Content components inside `<Section>`? No arbitrary values? No double-wrapping? Background rhythm makes sense?

## Review

Present the completed page to the user and suggest they review in browser (`pnpm dev`). Then run `/angora-design-system-audit` automatically — this is verification, not a change. Present findings and proposed fixes. Wait for approval before applying fixes. (Accessibility is covered at the component and layout level by `pnpm test:a11y` — no need to re-test assembled pages.)

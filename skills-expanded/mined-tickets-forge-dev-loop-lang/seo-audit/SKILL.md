---
name: seo-audit
description: Audit and improve on-page SEO for web pages, docs sites, and marketing pages. Use whenever the user wants an SEO review or audit, wants to check or fix title tags / meta descriptions / Open Graph / Twitter cards / canonical URLs / structured data (JSON-LD) / robots / sitemap / heading structure / image alt text, asks "why isn't this page ranking / showing a preview card", wants to optimize a page for search or social sharing, or mentions SEO, meta tags, OG tags, rich results, or search snippets — even if they don't say the word "audit". Works on local source files (HTML, JSX/TSX, Markdown, Astro/Next/Vite) or a live URL. Not for off-page SEO (backlinks, ad campaigns) or keyword-volume research.
---

# On-page SEO audit

Review a page (or a set of pages) against on-page SEO best practices, report what's
wrong in priority order, and — when the user wants — fix it in the source files.

The point is not to produce a checklist for its own sake. Search engines and social
platforms read a page's `<head>` and semantic HTML to decide how to index it and how to
render its preview card. When those signals are missing or wrong, the page still "works"
for humans but is invisible or ugly to crawlers. Your job is to find that gap and close it.

## Decide the target first

Two modes — pick based on what the user gives you:

- **Source mode (default when working in a repo):** audit the files that produce the page.
  This is what the user usually wants when the pages live in this repo, because the fix
  lands in code they can commit. Find where `<head>` / metadata is set — this varies by
  stack, so look before assuming:
  - Static HTML → the `<head>` in the `.html` file.
  - Next.js → `metadata` exports / `<Head>` / `generateMetadata` in `app/` or `pages/`.
  - Astro → frontmatter + `<head>` in layout `.astro` files.
  - Vite/plain SPA → `index.html` plus any runtime `document.title` / meta injection.
  - Markdown docs (MkDocs, Docusaurus, VitePress, Jekyll) → frontmatter + the theme's
    head template. Per-page `title`/`description` usually live in frontmatter.
  Grep for `og:`, `twitter:`, `canonical`, `application/ld+json`, `<title`, `meta name="description"`
  to locate every place metadata is set — there is often more than one.
- **Live mode:** the user gives a URL, or the rendering is dynamic and you need to see the
  final DOM. Fetch it with `WebFetch`, or drive Chrome (the `mcp__claude-in-chrome__*`
  tools) when the head is populated by client-side JS that `WebFetch` won't execute. Read
  the rendered `<head>`. Note in the report that you audited rendered output, not source.

If the user hasn't said which, infer from context (a repo path → source; a URL → live) and
state which mode you chose in one line. Don't stall on the choice.

## What to check

Go through these. For each, report the current value (or "missing"), whether it's OK, and
what to change. Read `references/checklist.md` for the full detail on any item — thresholds,
common mistakes, and exactly what good looks like. The high-signal ones, roughly in order
of how often they matter:

1. **`<title>`** — present, unique per page, ~50–60 chars, front-loads the primary term.
2. **`<meta name="description">`** — present, ~120–160 chars, compelling, not duplicated
   across pages. Missing/duplicate descriptions are the single most common real problem.
3. **Open Graph** — `og:title`, `og:description`, `og:image` (absolute URL, ~1200×630),
   `og:url`, `og:type`. This is what LinkedIn/Slack/Facebook show. A missing `og:image`
   is why a shared link looks blank.
4. **Twitter/X card** — `twitter:card` (usually `summary_large_image`), plus title/desc/image.
5. **Canonical** — `<link rel="canonical">` with an absolute URL, to avoid duplicate-content
   splitting between www/non-www, trailing-slash, and query-param variants.
6. **Headings** — exactly one `<h1>`, no skipped levels (h1→h3), headings describe content
   not styling.
7. **Image `alt`** — every meaningful `<img>` has descriptive alt text; decorative images
   have empty `alt=""`.
8. **Structured data** — JSON-LD (`application/ld+json`) appropriate to the page type
   (Article, Product, Organization, BreadcrumbList, FAQPage). Validate the shape.
9. **`robots`** — no accidental `noindex`/`nofollow` on pages that should rank; a sensible
   `<meta name="robots">` where needed.
10. **Crawlability** — `robots.txt` and `sitemap.xml` exist and are referenced; internal
    links use real `<a href>`; important content isn't hidden behind JS-only rendering.
11. **Technical hygiene** — `<html lang>` set, one viewport meta, HTTPS, no broken canonical
    or OG URLs, reasonable page-load weight.

Don't invent problems to pad the report. If a page is in good shape, say so — a short
"these 9 things are correct, here are the 2 that aren't" is more useful than a wall of green
checkmarks.

## Report format

Lead with the fixes that matter. Use this shape:

```
# SEO audit — <page or URL> (<source|live> mode)

## Critical  (breaks indexing or sharing)
- <issue> — <why it matters> — <exact fix, with file:line if source mode>

## Recommended  (real improvement, not urgent)
- ...

## Passing
- <one line each for the checks that are already correct>
```

- **Critical** = the page won't be indexed correctly or its share card is broken (missing
  title, `noindex` by accident, no og:image, broken canonical).
- **Recommended** = genuine improvements (thin description, missing JSON-LD, h1 issues).
- Every fix must be **specific**: the actual tag to add and where, not "improve your meta
  description". In source mode, cite `file:line`. Prefer showing the exact snippet to paste.

## Applying fixes

Only edit files when the user asks you to fix things (or approves the audit's fixes). Then:

- Make the smallest change that resolves each issue; match the file's existing style and the
  framework's idiom (e.g. Next's `metadata` export, not a raw `<head>` tag, in an app-router
  project).
- Use **absolute** URLs for `og:image`, `og:url`, and `canonical` — relative URLs silently
  break when the page is scraped off-domain. If you don't know the production origin, find it
  (existing tags, `package.json` homepage, CNAME, config) or ask rather than guessing.
- After editing, re-run the relevant checks so the report reflects reality, and show a diff.

## Verifying

Recommend the user confirm share cards with the platform validators (these re-scrape the
live URL, so they only work after deploy): opengraph.xyz, LinkedIn Post Inspector,
X/Twitter Card Validator, and Google's Rich Results Test for structured data. For local
verification, re-read the rendered `<head>` (live mode) or re-grep the source (source mode).
```
```

Keep the audit proportional to the ask: one page → tight focused report; "audit the whole
site" → sample the templates that generate the pages (layout, per-type page components)
since fixing a template fixes every page it renders, and call out which pages inherit each fix.

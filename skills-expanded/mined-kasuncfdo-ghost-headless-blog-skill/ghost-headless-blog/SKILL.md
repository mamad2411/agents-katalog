---
name: ghost-headless-blog
description: Implement a headless Ghost CMS blog (/blog) in a Next.js App Router site — Content API client, ISR + webhook revalidation, tag/author/paged archives, author bio + social rendering, SEO metadata + JSON-LD, sitemap, Ghost koenig-card styling, blur-up images. Use when adding a Ghost-powered blog to a Next.js project, or debugging an existing headless Ghost integration (empty blog, stale pages, broken images/cards).
---

# Headless Ghost blog in Next.js (App Router)

Battle-tested patterns from a live production site (Next.js 16 / React 19 /
Tailwind v4, Ghost Content API v6.0). Everything below was learned the hard way — follow
the decisions, not just the code.

## Architecture at a glance

- **No `@tryghost/content-api` dependency.** Call the Content API REST endpoints directly
  (`{GHOST_URL}/ghost/api/content/posts/?key=...`) with an `Accept-Version: v6.0` header.
  The SDK adds weight and hides errors.
- **All Ghost fetching is server-side** (server components, route handlers,
  `generateStaticParams`, sitemap). Content API keys only expose public data, but keep
  them server-only anyway: env vars `GHOST_URL` / `GHOST_CONTENT_API_KEY` with **no
  `NEXT_PUBLIC_` prefix**.
- **ISR everywhere + instant webhook purge.** Every blog route exports
  `export const revalidate = 3600` and `export const dynamicParams = true`; a Ghost
  Admin webhook hits `/api/revalidate?secret=...` on post publish/update/unpublish/delete
  for instant purges. Hourly ISR is only the safety net.
- **Ghost post HTML is rendered verbatim** via `dangerouslySetInnerHTML` inside
  `<article className="gh-content">`, styled by a dedicated `ghost-content.css`, with a
  small HTML post-processing pass (blur-up images, LCP fix) and tiny client components
  re-adding Ghost's interactive card JS (toggle cards).

## Routes to build

| Route | Purpose |
|---|---|
| `/blog` | Index: hero + feed. Only the Ghost-fetching part is an async component behind `<Suspense>` with a skeleton fallback. |
| `/blog/[slug]` | Post page: metadata from Ghost SEO fields, BlogPosting JSON-LD, rendered `gh-content`, related posts. |
| `/blog/tag/[slug]` | Tag archive (CollectionPage JSON-LD). Statically generated for crawlers even if the UI filters client-side. |
| `/blog/author/[slug]` | Author archive: bio, avatar/cover, location, social links, post feed. ProfilePage + Person JSON-LD with `sameAs` socials. |
| `/blog/page/[page]` | Paged feed archive; page 1 `redirect("/blog")`. |
| `/api/revalidate` | Ghost webhook receiver → `revalidatePath` purges. |
| `sitemap.ts` | Include posts (with real `lastModified`) + tag + author pages; Ghost outage must not break the sitemap (`.catch(() => [])`). |

Full route code + metadata/JSON-LD patterns: [references/pages.md](references/pages.md).
Setup steps (env, Ghost Admin, next.config images, webhook): [references/setup.md](references/setup.md).
Official Ghost docs lookup (llms-full.txt section-extraction workflow, Content API
reference URLs): [references/ghost-docs.md](references/ghost-docs.md).

## Copy-paste templates (portable, no project-specific deps)

- [templates/ghost.ts](templates/ghost.ts) — typed Content API client (posts, tags,
  authors, slugs, related, featured, pagination, excerpt helpers, `authorSocialLinks`
  normalizer, `toCardPost` projection)
- [templates/ghost-html.ts](templates/ghost-html.ts) — blur-up + LCP HTML transform
- [templates/revalidate-route.ts](templates/revalidate-route.ts) — webhook → ISR purge
- [templates/ghost-content.css](templates/ghost-content.css) — full `.gh-content` prose +
  koenig card styles (dark palette; accent via `--ghost-accent`)
- [templates/components/BlurImage.tsx](templates/components/BlurImage.tsx) — next/image blur-up
- [templates/components/ToggleCards.tsx](templates/components/ToggleCards.tsx) — re-adds Ghost toggle-card JS
- [templates/components/ReadingProgress.tsx](templates/components/ReadingProgress.tsx) — scroll progress bar

## Non-negotiable decisions (each one fixed a real bug)

1. **Graceful degradation, three tiers** (in `ghost.ts`):
   - Env missing → `isGhostConfigured = false`, every helper returns empty; build
     succeeds; one server-side `console.warn`. UI shows a friendly "No posts yet" state.
   - Key rejected (401/403) → return `null`/empty (config problem; warn once). A
     misconfigured deploy renders an empty blog instead of crashing.
   - Transient failure (network, 5xx) → **throw**. During ISR revalidation this keeps the
     previously rendered page instead of baking an empty page over good content.
2. **`getPostBySlug` uses browse + `filter=slug:x&limit=1`, not the `read` endpoint.**
   A missing post is then an empty 200 instead of a 404 that retry logic hammers and
   rethrows; return `posts[0] ?? null` and `notFound()` in the page.
3. **Follow pagination** (`meta.pagination.next`, `limit=100`) when fetching all
   posts/slugs — Ghost caps page size; a single request silently truncates.
4. **`toCardPost` slim projection** whenever many posts cross into a client component:
   strip `html`, meta/og/twitter fields, author bios. Keeps the serialized RSC payload
   small (this mattered — full posts ballooned the page payload).
5. **Webhook revalidates both `post.current.slug` and `post.previous.slug`** — slugs can
   change on update. Also purge `/blog`, `/blog/page/[page]`, `/blog/tag/[slug]` +
   `/blog/author/[slug]` (with the `"page"` type arg), and `/sitemap.xml`.
6. **`withBlurUpImages` HTML transform**: inject inline `onload` handlers (native HTML
   attrs — they work inside `dangerouslySetInnerHTML` without hydration), and promote the
   **first** content image from `loading="lazy"` to `loading="eager" fetchpriority="high"`
   — Ghost lazy-loads every image and the first is usually the LCP.
   Add `suppressHydrationWarning` on the `<article>` because those handlers mutate
   classes before React hydrates.
7. **next/image remote patterns**: derive the Ghost hostname from `GHOST_URL` **at build
   time** in `next.config.mjs`, plus `static.ghost.org` and the upload CDN (managed Ghost
   hosts like DigitalPress serve uploads from `**.digitaloceanspaces.com`). Set
   `minimumCacheTTL` long (e.g. 31 days) — Ghost upload URLs are immutable.
8. **Ghost SEO fields with fallbacks** in `generateMetadata`:
   `meta_title || title`, `meta_description || excerpt(160)`, `og_image ||
   feature_image`, honor `canonical_url`. Type `article` + `publishedTime` /
   `modifiedTime` / `authors` / `tags` on posts.
9. **Internal blog navigation must use `next/link`** (or `next-view-transitions` Link) —
   raw `<a>` tags (e.g. a navbar "Blog" tab) cause full page reloads.
10. **Ghost cards need re-implementation client-side**: Ghost's frontend JS isn't loaded,
    so toggle cards need a click handler (`ToggleCards.tsx`) and all `.kg-*` cards
    (callout, bookmark, button, gallery, embed, toggle, video) need CSS. Don't skip this —
    posts using those cards render broken otherwise.
11. **Next 15+/16: `params` is a Promise** — `const { slug } = await params;` in pages and
    `generateMetadata`.

## Known operational pitfalls

- **`GHOST_CONTENT_API_KEY` silently missing** (IDE overwriting `.env.local`, forgotten
  Vercel env): symptom is builds producing far fewer pages than expected and an empty
  blog. Check env first; the client's build-time warning log is the tell.
- **Custom Ghost domain moves**: the next/image allowed host is derived from `GHOST_URL`
  at build time, so hosting-provider env vars must be updated and the site **rebuilt**.
- **Ghost webhook "Secret" field**: leave it empty — it sets an `X-Ghost-Signature`
  header, not the query param. Pass the shared secret in the target URL
  (`.../api/revalidate?secret=...`) and compare against `GHOST_REVALIDATE_SECRET`.
- **Canonical/OG base URL must not redirect**: if the apex 307s to `www`, some scrapers
  (e.g. Telegram og:image) choke. Point `BASE_URL` at the final (non-redirecting) host.
- Never paste Admin API keys or the revalidate secret into chats/issues; rotate if exposed.

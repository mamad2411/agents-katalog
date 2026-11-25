---
name: shares-down-to-the-edge
description: "How an Astro Knots site makes every page and every section shareable with its own preview: a card per page and per h2/h3 rendered at build time from the page's metadata, /s/ share pages that give a heading its own unfurl (chat apps ignore #fragments), share buttons beside the title and on every heading, a toast, a content-hashed render cache, Ideogram illustration sets for site and generic pages, a Private pill for gated content, and (planned) an edge layer that hands each platform the image shaped for it. Use whenever adding share cards, share buttons, heading share links or per-section previews to a site; whenever porting this from cathode-site or fullstack-vc; whenever a link unfurls with the wrong image, the site logo, or no image; whenever someone says 'share this section', 'anchor links', 'the preview shows the wrong thing', 'make it shareable', 'og cards', 'LinkedIn shows the tall image'; or whenever deciding whether a page gets a metadata card or an illustration."
---

# Shares Down to the Edge

> Every link someone sends should unfurl as the thing they meant to send: the
> page, or the exact section, with a card that says what it is.

We share through iMessage and WhatsApp first, often one-to-one with LPs,
founders and clients. A link that unfurls as the site logo, or as the whole
page when someone meant one section, wastes the share. This skill is the
working recipe; the reasoning and design rules live in two blueprints:

- `astro-knots/context-v/blueprints/Share-Every-Page-and-Section-With-Its-Own-OG-Image.md`
  (cards, `/s/` pages, buttons, design rules, render cache, art, Private pill)
- `astro-knots/context-v/blueprints/Maintain-an-Elegant-Open-Graph-System.md`
  (tags, which image each platform gets, edge routing)

## The idea in one pass

1. **Every shareable thing has a card**: a small record (`key`, `kicker`,
   `title`, `subtitle`, optional `image`) built from frontmatter. Pages, items
   in collections, and every h2/h3 in long-form content.
2. **Each card renders twice at build time**: tall 1080×1440 (`og:image`) and
   wide 1200×630 (`twitter:image`). satori lays it out, resvg rasterizes,
   sharp makes the JPEG. No runtime, no API.
3. **Sections get real URLs.** Chat apps drop `#fragments`, so `page#heading`
   unfurls as the page. A section's share link is
   `/s/<base>/<slug>/<heading-id>/`: a tiny noindex page whose tags carry the
   section's card, which then redirects to `page#heading`.
4. **Buttons people find**: a share icon beside the page title, a share icon
   on every h2/h3, the native share sheet on phones, copy plus a toast on
   desktop.
5. **The edge picks the shape** (planned, not built): static HTML has two image
   slots, so LinkedIn, Bluesky and Discord get the tall card unless a
   middleware swaps in the banner by crawler user agent.

## Two kinds of share

Decide this per page before anything else.

| Page | What the share is about | Share image |
|---|---|---|
| Content: an article, memo, update, recipe, chapter, event log | That content, or the section under the heading | The **metadata card**, text first. An illustration may sit in its art slot, never over the words. |
| Section of a content page (h2/h3) | The page *and* that section | The section's card: heading as title, page as kicker. Reuses the page's art. |
| Site and generic pages: home, about, collection indexes, splash | The site as a whole | The **Ideogram illustration set** if there is one; otherwise the universal big-type card. |

The illustration set is generated from one prompt in all four shapes (cheap),
and each goes where its shape fits:

| Variant | Frontmatter key | Size | Goes to |
|---|---|---|---|
| `banner_tall` | `banner_tall_image` | 1080×1440 | `og:image`: iMessage, WhatsApp |
| `banner` | `banner_image` | 1200×630 | `twitter:image` (X); edge-routed to LinkedIn, Bluesky, Discord |
| `square` | `square_image` | 1200×1200 | on-site thumbnails and grids |
| `portrait` | `portrait_image` | 1200×1500 | posting as an image; no meta tag |

Generate it with the `generate-consistent-og-images` skill (Technique A). For
art *inside* a content card, generate one wordless 4:3 illustration per page
(`share_art`); the card puts it in the tall card's top band and the wide
card's right 58%.

## Copy from

`sites/fullstack-vc` is the most general version (many collections, two
section sources, a page-key lookup in the layout, Vercel). `sites/cathode-site`
is the original (one collection of event logs with photos, Netlify).
`sites/edviro-blog` is the light-brand variant (Astro MDX, logo on white).

| File | Job |
|---|---|
| `src/lib/share-cards.ts` | The card registry. `getPageCards()` (cheap, no markdown parsing), `getSectionShares()` (parses bodies with LFM for `tree.data.headings`), `shareKeyForPath()`, `SECTION_SOURCES`, `sectionShareBase()`. |
| `src/lib/og-render.ts` | satori layouts (`universal`, photo band, inset), font loading, the render cache, `renderCard(card, variant)`. |
| `src/pages/og/[variant]/[...key].jpg.ts` | Static endpoint: `getStaticPaths` over every card × `tall`/`wide`. |
| `src/pages/s/[...section].astro` | Section share page: section tags, `noindex`, canonical to `page#id`, meta refresh plus `location.replace`. Cathode's is `s/log/[logId]/[headingId].astro`. |
| `src/layouts/BoilerPlateHTML.astro` (or `BaseLayout`) | Emits the tags. Card key = the page's URL path, falling back to the site card. |
| `src/components/markdown/HeadingAnchor.astro` | The h2/h3 button. With `shareUrl` it shares the `/s/` page; without, it copies `page#id`. One delegated listener. |
| `src/components/ui/ShareButton.astro` | The page-level button; `icon` mode sits beside the title. |
| `src/utils/share.ts` | `shareOrCopy()` (share sheet on touch, clipboard on desktop, select-text fallback) and `showShareToast()`. |
| `src/components/markdown/AstroMarkdown.astro` | Passes `shareBase` and `shareDepths` down so h2/h3 get `shareUrl={shareBase + id}`. |

Dependencies: `satori`, `@resvg/resvg-js`, `sharp` (add `sharp` to
`pnpm.onlyBuiltDependencies`). Fonts as `.woff` files in `src/assets/fonts/`.

## Building it on a new site

1. **Read the site first.** Collections, which ones are long-form, how pages
   build their URLs, the layout that writes `<head>`, the host (Netlify for
   Edviro-family sites, Vercel otherwise), and the DESIGN.md brand values.
2. **Write the registry.** One card per page and collection entry, keyed by
   its URL path (`guides/my-recipe`), plus the `home` site card with
   `layout: 'universal'`. Add `SECTION_SOURCES` for each long-form collection.
3. **Port `og-render.ts`** and swap in the site's raw brand values (images
   can't read CSS variables), fonts and mark. Keep the layout rules: tall card
   balanced top to bottom, type sized for a phone, wide-card text off the photo.
4. **Add the endpoint and the `/s/` page.** Prerendered.
5. **Wire the layout**: one `og:image` (tall) with width 1080, height 1440,
   type `image/jpeg`, alt; `twitter:image` (wide); absolute URLs from
   `Astro.site`.
6. **Wire the buttons**: `ShareButton icon` beside each page title,
   `HeadingAnchor` on h2/h3 with the section share URL.
7. **Headers**: `Content-Type: image/jpeg`, `Access-Control-Allow-Origin: *`
   and a cache header on `/og/*` (`netlify.toml` or `vercel.json`).
8. **Keep `/s/` out of the sitemap** (filter it in `@astrojs/sitemap`).
9. **Add every new component to `/design-system`** in the same change.
10. **Gated content**: give its cards a `private: true` that draws a "Private"
    pill near the kicker, set from the same flag that gates the route. Not in
    either reference site yet (2026-11-19); humain-web is the first candidate.

## Rules that bit us

- **Never two `og:image` tags.** iMessage has mixed a tall and a wide one into
  one broken card. One tall `og:image`; the wide card only in `twitter:image`.
- **Heading ids come from LFM**, `node.data.id` and `tree.data.headings`.
  Never re-slugify in the renderer, or the share page and the button disagree.
- **satori reads TTF, OTF and WOFF, not WOFF2.** fontsource ships `.woff`.
  Give every text block an explicit width or titles run off the card.
- **Hash the render cache by content, not mtime.** A fresh clone resets every
  mtime. The cache lives in `node_modules/.astro/og-cache`, which Netlify and
  Vercel keep between builds; fonts, the mark and a `RENDER_VERSION` are part
  of the key, so bump `RENDER_VERSION` when the layout changes.
- **Anchor photos and art where the subject is** (`objectPosition: 'left
  center'`), never the default center crop.
- **No words in illustrations.** Every word on a card comes from metadata, so
  it's spelled right and changes when the title does.
- **The Private pill is a label, not protection.** The card JPEG and the unfurl
  are public to anyone the link reaches; put nothing on a card you wouldn't type
  in the message.
- **Chat apps cache per URL for days.** To see a new card, share `?v=2`.

## The edge layer (planned)

Static HTML gives X the banner and everyone else the tall card. That's right
for iMessage and WhatsApp and a compromise for LinkedIn, whose link frame is
1.91:1 (1200×627; the wide card already fits, no LinkedIn size needed). There
is no `linkedin:image`.

To fix it, a Vercel Routing Middleware or Netlify Edge Function rewrites the
image block for these crawlers:

- Test for iMessage **first**: its user agent contains both
  `facebookexternalhit` and `Twitterbot`. It keeps the tall card.
- `WhatsApp/` keeps the tall card.
- `LinkedInBot`, `Cardyb` (Bluesky) and `Discordbot` get the wide card.
- Rewrite `og:image`, `:width`, `:height`, `:type` and `:alt` together, send
  `Vary: User-Agent`, and leave every other request untouched.

**Not built on any site as of 2026-11-19.** The user agents need checking
against real access logs. When someone builds it, prove it with
`curl -sA 'LinkedInBot/1.0' https://site/page | grep og:image` per crawler, then
a real post in each app, and update this section.

## Verify before calling it done

- `pnpm build`, then look in `dist/og/tall/` and `dist/og/wide/`: one pair per
  card, each tall card under 300 KB.
- Open a few tall cards at 480px high and crop the center square to 200px: the
  headline must read in both (WhatsApp shows that square).
- `grep -c 'property="og:image"'` on a built page and an `/s/` page: exactly 1.
- Send yourself a page link and a section link in iMessage and WhatsApp.

## Related skills

- `open-graph-share-seo-geo`: tag rules, JPEG over WebP, absolute URLs,
  sitemap and robots.
- `generate-consistent-og-images`: Ideogram sets, DESIGN.md `imagery:` recipe,
  naming.
- `lossless-flavored-markdown`: heading ids and `tree.data.headings`.
- `maintain-design-system-page`: where the buttons get catalogued.
- Heading id spec: `lfm/context-v/specs/Maintain-Heading-Anchors-and-Share-Links.md`.

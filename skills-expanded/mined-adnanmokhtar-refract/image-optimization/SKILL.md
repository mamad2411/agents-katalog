---
name: image-optimization
description: Image delivery — legacy formats, no srcset, unsized (CLS), lazy below the fold, raw <img> beside a framework primitive, oversized sources.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# image-optimization

## Premise

**Images are usually the heaviest bytes on a page and the top source of layout shift.** The browser needs three things to deliver an image well: the right *format* (AVIF/WebP over JPEG/PNG), the right *size for the viewport* (`srcset`/`sizes`, not one 2000px file for a phone), and *reserved space* (`width`/`height` or `aspect-ratio`, or the page jumps as it loads → CLS). Every finding cites the element at `<file:line>` + the matched pattern + the fix in **this project's own image primitive**. "Optimize images" without the cited element is not a finding.

**Closure verbs** — exactly one per finding. This skill emits `report-with-fix`, `dismiss` (SVG / fixed-size icons, a correctly-ratioed `width`/`height`, a CDN that already negotiates format), and `halt-handoff` (anything touching the hero's priority → `lcp-audit`).

Division of labor: **this skill owns format, responsiveness, dimensions/CLS, and lazy-loading.** The *LCP image's priority hints* (`fetchpriority`, `preload`, no-lazy-on-hero) belong to `lcp-audit` — cross-link it, don't duplicate. Pair with `lighthouse-ci` to confirm bytes actually dropped: `uses-responsive-images`, `modern-image-formats`, `uses-optimized-images`, `offscreen-images` and `unsized-images` on Lighthouse 12.6.1 (LHCI 0.15.1); `image-delivery-insight` and `unsized-images` on 13.x, where the four `uses-*`/`offscreen` audits are gone (`lighthouse-ci` § Lighthouse ids by version).

## Adapt to the codebase first

Detect and **mirror the project's image primitive** — most frameworks ship one that solves format + srcset + dimensions + lazy automatically. Prefer adopting it over hand-rolling `<picture>`:

| Framework / setup | Optimized image primitive | What it auto-handles |
|---|---|---|
| **Next.js** | `next/image` `<Image>` | format negotiation (**WebP by default**; AVIF is opt-in via `images.formats: ['image/avif','image/webp']`), `srcset`, lazy (below-fold), enforced `width`/`height` (no CLS) |
| **Nuxt** | `<NuxtImg>` / `<NuxtPicture>` (`@nuxt/image`) | format, responsive `sizes`, lazy, provider CDN |
| **Astro** | `<Image>` / `<Picture>` (`astro:assets`) | format, `srcset`, dimensions from source |
| **Angular** | `NgOptimizedImage` (`ngSrc`) | `srcset`, lazy, requires `width`/`height`, priority for LCP |
| **SvelteKit / Vite** | `@sveltejs/enhanced-img` / `vite-imagetools` | build-time format + `srcset` |
| **Plain HTML / React** | `<picture>` + `<source type>` + `<img srcset sizes width height loading>` | manual, but explicit |
| **CDN-fronted** (Cloudinary / imgix / Cloudflare Images) | URL transform params (`f_auto,q_auto,w_…`) | format + resize at the edge |

If the project already routes images through a component/CDN, every fix goes through it. Only hand-roll `<picture>` when there is no primitive.

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. An `rg` error on stderr (exit 2) is a failed grep, not zero hits. Tag bodies are read with `-U`, so a multi-line tag prints one line per attribute: count tags, not lines.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|next|nuxt)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--|\{/\*)')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
TB='(?:[^>{<\x60]|\{(?:[^{}]|\{[^{}]*\})*\})*'
TL='(?:[^>]|=>)*?'   # lookahead body that also enters {…}: `className={cn('h-16 w-16')}`, `src={x ?? '/a.svg'}`
RAW='(?<![\w.$])<img\b'                                                  # a raw <img>, not <Image> / <NuxtImg>
NOTICON="(?!${TL}\\b(?:src|ngSrc)=[\"'{]*[^\"'}\\s]*\\.svg\\b)(?!${TL}\\bsrc=[\"'{]*data:)"   # SVG and data: URIs are exempt
# 0. Lanes: the image primitive the project ships (next/image, @nuxt/image, NgOptimizedImage, astro:assets, enhanced-img, an image CDN SDK).
rg -n --no-heading '"(next|@nuxt/image|@angular/common|astro|@sveltejs/enhanced-img|vite-imagetools|@unpic/[\w-]+|cloudinary|@cloudinary/[\w-]+|@imgix/[\w-]+)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -l --no-heading --pcre2 "from\\s+[\"'](?:next/image|astro:assets)[\"']|NgOptimizedImage|<NuxtImg\\b|<NuxtPicture\\b|<enhanced:img\\b" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l
# 1. A raster source with no modern-format path: a .jpg/.jpeg/.png src on a raw <img> (1a), and raster files committed under public/static/assets (1b).
rg -n -U --no-heading --pcre2 "${RAW}${TB}\\b(?:src|ngSrc)=[\"'{]*[^\"'}\\s]*\\.(?:jpe?g|png)\\b${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg --files -g '**/{public,static,assets,src/assets}/**/*.{jpg,jpeg,png,JPG,JPEG,PNG}' -g '!**/node_modules/**' "${ROOTS[@]}" | wc -l
# 2. A raw raster <img> with no srcset (SVG and data: URIs skipped).
rg -n -U --no-heading --pcre2 "${RAW}${NOTICON}(?!${TL}\\b(?:srcset|srcSet|:srcset|\\[srcset\\])=)${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3. No reserved box: a raw <img> with neither width+height nor an aspect/size utility — Tailwind `size-full`, `size-[…]`,
#    `h-[…]` and `h-full` (sized by its frame — see the blind spot) included (3a); a NuxtImg/Picture with no width (3b).
rg -n -U --no-heading --pcre2 "${RAW}${NOTICON}(?!${TL}\\b(?:width|:width|\\[width\\])=)(?!${TL}\\b(?:aspect-|size-(?:\\d|full|\\[)|h-(?:\\d|\\[|full)|aspectRatio|aspect-ratio))${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --no-heading --pcre2 "<(?:NuxtImg|NuxtPicture)\\b(?!${TB}\\b:?(?:width|sizes)=)${TB}>" -g '*.vue' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. A raw <img> with no loading attribute (position decides: below the fold wants lazy, the LCP wants eager — read, then route the hero to lcp-audit).
rg -n -U --no-heading --pcre2 "${RAW}${NOTICON}(?!${TL}\\b(?:loading|:loading|\\[loading\\])=)${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. Raw <img> count per file — a finding only where grep 0 shows a framework image primitive.
rg -c --pcre2 "${RAW}${NOTICON}" "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
# 6. Oversized sources: committed raster files over 300 KB (the slot size is read from the consuming tag).
for r in "${ROOTS[@]}"; do find "$r" \( -path '*/node_modules' -o -path '*/dist' -o -path '*/.next' -o -path '*/.output' \) -prune -o -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.avif' -o -iname '*.gif' \) -size +300k -print; done
# 7. Placeholders in use (7a) vs framework image components on hero/card markers (7b).
rg -n --no-heading --pcre2 '\bplaceholder=["\x27{]*(?:blur|empty|data:)|<NuxtImg\b[^>]*\bplaceholder\b|\bblurDataURL\b' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l
rg -n -U --no-heading --pcre2 "<(?:Image|NuxtImg|NuxtPicture|Picture)\\b(?=${TB}(?i:hero|banner|cover|card|gallery))(?!${TB}\\bplaceholder)${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A hit is a candidate. The greps see **raw** `<img>` tags only (greps 2–5); a framework component already negotiates format, `srcset` and lazy loading, so its findings come from grep 3b, grep 7b and a read of its props. Two blind spots are structural:

- **Sizing in a stylesheet is invisible to grep 3a.** A project class with a fixed `height` or `aspect-ratio` reserves the box; read the class before calling the tag unsized.
- **Sizing by the parent frame is assumed, not seen.** 3a trusts `h-full` / `size-full` (`<img className="h-full w-full object-cover">` inside an avatar circle, a `size-10` logo slot, a `h-[56px]` rail): the box is the parent's. A parent that is not sized itself, or a `w-auto` logo with no fixed height, shifts the layout anyway — read one level up once per component, and read the tag when its class comes from a prop (`className={className}`).
- **An image CDN or a build plugin rewrites `src` outside the source.** A `?format=auto` loader, `vite-imagetools` query, or a CDN rule turns grep 1a hits into dismissals; read the loader once.

**Measured** (2026-10-05, read-only, counts are tags). Scratch fixture: a raster `src` with no modern path, a tag with no `srcset`, an unsized tag, a 400 KB PNG, all hit; the SVG icon, the commented-out tag and the sized `srcSet` tag stay out of the greps they should. Benchmark fixtures: `web-dashboard` 6 tags with no `srcset` and no `loading` (0 unsized), `vuln-fullstack` 3 / 2 unsized / 3, `slow-marketplace` 3 with no `srcset` (its hero is sized), the rest 0. Real repos: a Nuxt 4 storefront with three themes (grep 2: 111 tags in 68 files; 3a: 91 in 58; 4: 55 in 30, with no image primitive installed, so §5 is N/A and every theme repeats the same components: group first), a Vue 3 + Vite admin SPA (2: 11; 3a: 11; 4: 9) and an Angular 19 admin template (2: 209 in 34 files; 6: 10 files over 300 KB; demo pages, dismissed by the route table). Re-measured 2026-10-15 on a real NestJS + React monorepo (Vite SPA, Tailwind 4, no image primitive): 3a 29 → 8 tags. The 21 dropped were all sized — `h-full w-full object-cover` inside a sized frame, `size-full`, arbitrary `h-[…]`, or a `className={cn('h-16 w-16 …')}` the brace-blind lookahead could not read (the tag-body lookaheads now enter `{…}`); the 8 left are six print-template HTML strings, one wrapper whose class arrives as a prop and one receipt viewer to read. Grep 2 57 and grep 4 39 tags, unchanged. Fixtures: unchanged.

## The 3,000-hit path

1. **Intersect with the route table** and drop design-system demo and docs pages.
2. **Group** by (component, pattern). A `ProductCard` rendered in every list is one finding at the card; a theme folder duplicated N times is one group per component name.
3. **Rank** by route traffic, then by bytes (grep 6 sizes, or `uses-responsive-images` / `image-delivery-insight` wasted bytes when Lighthouse ran).
4. **Read the top 30 groups.** Ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them, never `checked`.

## Scans for

### 1. Legacy format with no modern-format path

JPEG/PNG delivered without an AVIF/WebP alternative ships 25–50% more bytes.

```
BAD:  <img src="/hero.jpg">
GOOD: <picture>
        <source type="image/avif" srcset="/hero.avif">
        <source type="image/webp" srcset="/hero.webp">
        <img src="/hero.jpg" width="1200" height="630" alt="…">
      </picture>
GOOD (CDN): <img src="/cdn/hero.jpg?format=auto&quality=auto">
```

Flag `<img>` pointing at `.jpg/.jpeg/.png` with no `<picture>`/`type` negotiation and no `format=auto` CDN param — or a raw `<img>` where the framework component would negotiate format for free.

### 2. Missing responsive `srcset` / `sizes`

One fixed-resolution image for every device wastes bytes on phones and looks soft on retina.

```
GOOD: <img srcset="/p-400.avif 400w, /p-800.avif 800w, /p-1600.avif 1600w"
           sizes="(max-width: 600px) 100vw, 50vw" src="/p-800.avif" width="800" height="600">
```

Flag content `<img>` with a single `src` and no `srcset`/`sizes` (and no framework component that generates them). Icons/logos at fixed small size are exempt.

### 3. Missing `width`/`height` (or `aspect-ratio`) → CLS

Without intrinsic dimensions, the browser reserves no space; the image pops in and shoves content down.

```
BAD:  <img src="/card.jpg">                              // reserves 0 height → CLS
GOOD: <img src="/card.jpg" width="400" height="300">     // or CSS aspect-ratio: 4/3
```

Flag any `<img>` lacking both explicit `width`+`height` and a CSS `aspect-ratio` on its box. This is the single biggest CLS lever.

### 4. Missing `loading="lazy"` below the fold (and wrongly present above it)

```
GOOD (below fold): <img loading="lazy" decoding="async" …>
```

Flag below-the-fold content images with no `loading="lazy"`. **Inverse:** a hero/above-fold/LCP image with `loading="lazy"` is an LCP bug — flag it but route the fix to `lcp-audit` (it owns hero priority).

### 5. Raw `<img>` where the framework offers an optimized component

Flag a hand-written `<img>` in a project that ships `next/image` / `<NuxtImg>` / `NgOptimizedImage` / `astro:assets` — adopting the component fixes format + srcset + dimensions + lazy in one change.

### 6. Oversized source served into a small slot

A 2400px original rendered into a 300px avatar ships ~8× the pixels.

Grep 6 lists committed raster files over 300 KB; grep the file name against the source to find the consuming tag, then read its slot (`width`, the avatar/thumbnail class, `sizes`). User-uploaded and CMS images are invisible to the file scan: read the URL builder instead (a `src={user.avatarUrl}` with no `w_`/`width=` transform is the candidate).

Flag images whose natural size vastly exceeds their display size (thumbnails, avatars, list rows) with no resize/CDN transform.

### 7. Missing placeholder for large images (perceived perf)

Large content images benefit from an LQIP/blur/dominant-color placeholder so the layout looks intentional while bytes arrive. Flag large hero/card images with no placeholder where the framework offers one (`next/image` `placeholder="blur"`, `<NuxtImg placeholder>`).

## Output

```
image-optimization — <route set>   (primitive: <e.g. next/image | <picture> | Cloudinary>)

Findings: 4

1. components/ProductCard.tsx:18                       [report-with-fix]
   <img src={p.image}> — no width/height, no srcset, raw <img> in a next/image project.
   Fix: <Image src={p.image} width={400} height={300} sizes="(max-width:600px) 50vw, 25vw" alt={p.name} />

2. app/gallery/page.tsx:44                             [report-with-fix]
   30 gallery <img> below the fold with no loading="lazy".
   Fix: loading="lazy" decoding="async" (or the framework component, lazy by default).

3. components/Avatar.vue:6                             [report-with-fix]
   Serves the 1600px original into a 48px avatar.
   Fix: <NuxtImg :src="url" width="48" height="48" sizes="48px" /> (or CDN w_48).

4. public/photos/*.png (12 files)                      [report-with-fix]
   PNG photos with no AVIF/WebP path.
   Fix: convert to AVIF/WebP + <picture>, or route through the image component/CDN (format=auto).

Verification: 31 candidates → 4 findings · 2 unconfirmed · 25 refuted

Class coverage:
  §1  legacy format              checked (14 hits → 1 finding, 12 files)
  §2  no srcset / sizes          checked (6 tags → folded into finding 1)
  §3  unsized → CLS              checked (5 tags → 1 finding; 4 sized by a project class)
  §4  lazy below the fold        checked (31 tags → 1 finding)
  §5  raw <img> beside primitive checked (next/image installed; folded into finding 1)
  §6  oversized source           checked (3 files > 300 KB → 1 finding)
  §7  placeholder                checked (0 findings; 2 hero components already blur)
```

`[report-with-fix]`: the tag renders on a cited route and the fix goes through the project's own primitive. `[report-flagged]`: a link is unproven (the slot width or the position against the fold was not read on a render) and the row names the run that settles it. The coverage block lists **all seven** classes on every run: `checked (k hits → m findings)`, `N/A (<reason>)`, or `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

- **Don't lazy-load the LCP image.** If a scan would add `loading="lazy"` to the hero, stop — that's `lcp-audit`'s territory and lazy there *hurts* LCP.
- **SVGs and tiny icons** don't need srcset/format negotiation — exempt vector + fixed small raster.
- **`width`/`height` are the intrinsic ratio, not the display size** — CSS can still scale; the attributes just reserve the aspect box. Don't "fix" a correctly-ratioed image.
- **AVIF encode cost**: AVIF is smaller but slower to encode — for build-time it's fine; for on-the-fly CDN, `format=auto` picks per-browser. Don't force AVIF where the CDN already negotiates.
- **Framework image defaults move between majors — read the installed one before reporting.** Next.js 16 changed several `images.*` defaults: `qualities` is now `[75]` (a `quality={90}` prop is coerced to the nearest allowed value unless `images.qualities` is widened), `minimumCacheTTL` went 60s to 4h, `16` was dropped from the default `imageSizes`, and a local `src` carrying a query string now requires `images.localPatterns`. A quality/cache finding must cite the major it was read against (source: the Next.js 16 behaviour-changes table, nextjs.org/blog/next-16).
- **One `srcset` doesn't fit all layouts** — `sizes` must reflect the *actual* rendered width at each breakpoint, or the browser picks wrong. A wrong `sizes` is worse than none; verify against the layout.

## When to run

- Before launching any image-led page (product, gallery, marketing, blog).
- When `lighthouse-ci` fails `uses-responsive-images`, `modern-image-formats`, `uses-optimized-images` or `unsized-images` (Lighthouse 12.6.1), or `image-delivery-insight` / `unsized-images` (13.x), or CLS from images.
- After adding a card/list/grid that renders user or CMS images.

## Halt conditions

- Halt on any finding without the cited element at `<file:line>` + the matched pattern + the fix in the project's own image primitive.
- Halt if a fix would add `loading="lazy"` to the LCP/hero image — hand to `lcp-audit`.
- Halt if a `sizes` value is proposed without checking the element's real rendered width per breakpoint.
- Halt if the project has an image component/CDN and the fix hand-rolls `<picture>` instead of using it.
- Halt before reporting any candidate that has not been through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§1 restate … §9) and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 83 (lazy below the fold is correct). **Proof:** bytes per route and the image audit for the runner's Lighthouse version, median of 5 runs ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Bytes per route", § "Lighthouse median"); a CLS fix is proved by the layout-shift observer (`critical-path-scan` § Proof, item 3).

## Related

- `lcp-audit` — owns the LCP element's *priority* (eager + `fetchpriority` + preload). This skill owns format / dimensions / responsive `sizes` / lazy-below-fold. Never lazy what that skill prioritized; hand hero findings there.
- `font-optimization` — the other half of the asset budget (`font-display`, self-host, size-adjusted fallback). Both feed the same CLS number from different sources.
- `code-splitting.md` (ai-pattern) — the JS axis; images are the byte axis. A page can pass one and fail the other.
- `seo-audit` — image `alt` text and OG image dimensions are graded there, not here.
- `.claude/rules/frontend-principles.md` — the "content images: modern format, `srcset`/`sizes`, explicit dimensions, lazy below the fold" MUST this skill enforces.
- Cross-pack (`performance`, when co-installed): `lazy-loading` owns the broader non-JS deferral tiers; `web-vitals-field` confirms the LCP/CLS win in the field. Absent that pack, this skill still ships every format / `srcset` / dimension finding — it just reports `field confirmation: unavailable` instead of a CLS or LCP delta it never measured.

---
name: lcp-audit
description: LCP-resource priority — lazy hero, no fetchpriority, late-discovered or cross-origin LCP image, framework priority prop missing.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# lcp-audit

## Premise

The Largest Contentful Paint element — usually the hero image or a large heading — must be **discovered and fetched first**. The common failure is the opposite: the hero is lazy-loaded (so the browser delays it), or it has no priority hint (so it queues behind less important resources), or it's a late-discovered CSS background with no preload. `frontend-principles` § LCP & images states the MUST — the LCP image is eager + prioritized and never carries `loading="lazy"`, which is lawful **below the fold only**. This skill is the detector that proves it on a real tree: the rule says exactly one high-priority element per view, and only a scan can tell you whether the route has zero or three.

Every finding cites the element at `<file:line>` + the matched pattern + the fix. "LCP is slow" without the cited element is not a finding. The greps find candidates; the element is confirmed by § Identifying the LCP element (lab) or by `web-vitals-field` *(performance pack, when co-installed)*, which attributes field LCP to the real element and sub-part.

**Closure verbs** — exactly one per finding. This skill emits `report-with-fix` (priority hint missing on the confirmed LCP element), `dismiss` (the § False positives carve-outs: lawful lazy below the fold, a text LCP element, an already-prioritised hero), and `halt-handoff` (format / dimensions / `sizes` → `image-optimization`; font + critical CSS on a text LCP → `font-optimization`).

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. An `rg` error on stderr (exit 2) is a failed grep, not zero hits. Tag bodies are read with `-U`, so a multi-line `<Image … />` prints one line per attribute: count tags, not lines.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|next|nuxt)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--|\{/\*)')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
TB='(?:[^>{<\x60]|\{(?:[^{}]|\{[^{}]*\})*\})*'
TL='(?:[^>]|=>)*?'   # a lookahead body that also enters {…}: `alt={t('catalog.bannerAlt')}`, `className={cn('…')}`
# the marker counts only inside a class / id / alt / data-* value — never an identifier (`src={heroImageSrc}`) — and
# Tailwind's object-cover / bg-cover is a fit utility, not a hero
HERO='\b(?:class|className|id|alt|data-[\w-]+)\s*=\s*(?:"[^"]*?|\x27[^\x27]*?|\{[^}]*?)(?i:hero|banner|(?<!object-)(?<!bg-)cover|masthead|splash|jumbotron|above-?(?:the-)?fold|\blcp\b)'
IMG='<(?:img|Image|NuxtImg|NuxtPicture|Picture|enhanced:img)\b'
# 0. Lanes and versions.
rg -n --no-heading '"(next|nuxt|@nuxt/image|astro|@angular/core|@sveltejs/enhanced-img|vite-imagetools|web-vitals|@lhci/cli|lighthouse)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
# 1. Lazy on an LCP candidate (an image tag carrying a hero marker and loading=lazy; multi-line tag bodies read with -U).
rg -n -U --no-heading --pcre2 "${IMG}(?=${TL}${HERO})(?=${TL}\\bloading=[\"'{]*lazy)${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. Hero image with no priority hint (fetchpriority / priority / preload absent from the tag).
rg -n -U --no-heading --pcre2 "${IMG}(?=${TL}${HERO})(?!${TL}\\b(?:fetch[pP]riority|priority|preload)\\b)${TB}>" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3. Late-discovered image: a CSS / style-object background url, a Tailwind arbitrary background, or a CSS custom
#    property carrying a url (`'--brand-bg': \`url(${…})\`` read by `bg-[image:var(--brand-bg)]`) (3a) vs the image preloads that exist (3b).
rg -n --no-heading --pcre2 'background(?:-image)?\s*:\s*[^;]*\burl\(|backgroundImage\s*:|\bbg-\[(?:url|image:)|["\x27]--[\w-]+["\x27]\s*:\s*\x60?url\(' -g '*.{css,scss,sass,less,vue,svelte,tsx,jsx,astro}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '<link\b(?=[^>]*\brel=["\x27]?preload)(?=[^>]*\bas=["\x27]?image)|\brel\s*:\s*["\x27]preload["\x27][^}]*\bas\s*:\s*["\x27]image|ReactDOM\.preload\(|\bpreload\([^)]*as\s*:\s*["\x27]image' "${UI[@]}" -g '**/{nuxt,next,astro}.config.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. Cross-origin image sources (4a) vs preconnects declared (4b).
rg -n --no-heading --pcre2 "${IMG}${TB}\\b(?:src|ngSrc)=[\"'{]*(?:https?:)?//" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\brel=["\x27]?(?:preconnect|dns-prefetch)|\brel\s*:\s*["\x27](?:preconnect|dns-prefetch)|ReactDOM\.preconnect\(' "${UI[@]}" -g '**/{nuxt,next,astro}.config.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. Framework priority prop: 5a Next `priority` (deprecated from Next 16; read the major from grep 0), 5b raw <img> in a project whose lane ships a component.
rg -n -U --no-heading --pcre2 "<Image\\b${TB}\\bpriority\\b(?!=\\{?false)" -g '*.{tsx,jsx,js,ts}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -c --pcre2 '<img\b' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
```

A hit is a **candidate**, never a finding: the hero marker is a naming convention, and the real LCP element is whatever § Identifying the LCP element names. Two blind spots are structural:

- **An unmarked hero is invisible to greps 1 and 2.** A first-in-page `<img>` with no `hero`/`banner`/`cover` class is the LCP element as often as a marked one. The lab arm finds it; the grep never will.
- **Grep 3a cannot tell a hero background from a decorative one.** Read the selector, then check 3b for a matching `<link rel="preload" as="image">`.

**Measured** (2026-10-05, read-only). Scratch fixture of 5 positives and 3 decoys: every positive hits; the `fetchpriority="high"` cover, the commented-out image and the SVG icon stay out. Benchmark fixtures: 0 on every fixture except `slow-marketplace` (1: the lazy `hero__image` its DEFECTS file seeds; 4: one preconnect). Real repos: a Nuxt 4 storefront with three themes (grep 2: 2 tags, a banner list whose first item is `:loading="index === 0 ? 'eager' : 'lazy'"` with no `fetchpriority`, and a cross-sell banner; 1: 0), a Vue 3 + Vite admin SPA (3a: 2) and an Angular 19 admin template (3a: 17 background URLs, all decorative on read). The first version of the tag-body pattern ran across a template literal for 20 lines; it now stops at `<` and a backtick. Re-measured 2026-10-15 on a real NestJS + React monorepo (Vite SPA, Tailwind 4): grep 1 was 9 tags and grep 2 26, 8 and 23 of them only Tailwind `object-cover` on list thumbnails, plus a `heroImageSrc` identifier; with the marker read inside class / id / alt / data-* values and `(?<!object-)(?<!bg-)cover`, grep 1 is 0 and grep 2 is 2 tags — one of them the catalog hero banner whose marker sits inside `alt={… t('portal.catalog.bannerAlt')}`, which the brace-blind lookahead had missed. 3a 0 → 4: a sign-in shell sets `'--brand-bg': \`url(${…})\`` and paints it with `bg-[image:var(--brand-bg)]` — a late-discovered LCP candidate. Fixtures: the `slow-marketplace` seed still hits; one `object-cover` gallery thumbnail in `a11y-states` drops out.

## The 3,000-hit path

1. **One element per route and viewport.** Run § Identifying the LCP element on the top routes first; a grep hit on a component no route paints above the fold is dismissed by one read.
2. **Group** by (component, pattern). A shared `HeroSection` mounted by 30 routes is one finding at the component.
3. **Rank** by route traffic (RUM or analytics when present, else landing, product/detail, campaign routes).
4. **Read the top 30 groups.** Ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them, never `checked`.

## Scans for

### 1. Lazy-loaded LCP candidate

```
BAD:  <img src="/hero.jpg" loading="lazy" class="hero">     // defers the LCP element
GOOD: <img src="/hero.jpg" fetchpriority="high">             // eager + prioritized
```

Grep: `loading=["']lazy["']` on `<img>` near hero/banner/above-fold markers (class/id containing `hero`, `banner`, `cover`, `masthead`, or the first image in a page/layout). Lazy is correct *below* the fold — flag only above-the-fold candidates.

### 2. Hero image without `fetchpriority="high"`

The LCP image should declare high priority so it jumps the queue. Grep above-the-fold `<img>` lacking `fetchpriority="high"` (raw HTML) or the framework's priority prop (§ per-framework).

### 3. Late-discovered LCP image with no preload

A CSS `background-image` or a JS-injected hero isn't in the initial HTML, so the browser discovers it late.

```
GOOD: <link rel="preload" as="image" href="/hero.avif"
            imagesrcset="/hero-800.avif 800w, /hero-1600.avif 1600w" fetchpriority="high">
```

Flag a CSS-background or dynamically-set LCP image with no matching `<link rel="preload" as="image">`.

### 4. Cross-origin LCP image with no preconnect

If the LCP image is served from a CDN/image host on another origin, the connection setup (DNS + TCP + TLS) is on the critical path.

```
GOOD: <link rel="preconnect" href="https://images.cdn.example">
```

Flag an LCP image from a cross-origin host with no `<link rel="preconnect">` (or `dns-prefetch`).

### 5. Framework priority primitive missing on the hero

| Framework | LCP-image priority | Below-fold default |
|---|---|---|
| **Next 16+** | `<Image preload>` (inserts a `<link rel="preload">` in the `<head>`), or `fetchPriority="high"` / `loading="eager"`; the docs prefer the last two in most cases. `priority` is **deprecated from 16.0.0** in favour of `preload` | `loading="lazy"` |
| **Next ≤ 15** | `<Image priority>` (sets `fetchpriority="high"` + eager + preload) | `loading="lazy"` |
| **Nuxt** | `<NuxtImg preload :loading="'eager'">` | lazy |
| **Astro ≥ 5.10** | `<Image priority>` (sets `loading="eager"`, `decoding="sync"`, `fetchpriority="high"`); older Astro: `loading="eager"` + `fetchpriority="high"` | lazy |
| **Angular** | `NgOptimizedImage` `ngSrc` + `priority` (emits preload + `fetchpriority=high`) | non-priority |
| **Plain React/Vue/Svelte** | `fetchpriority="high"` + `width`/`height` on the `<img>` | `loading="lazy"` |

Flag a hero using the framework image component without its priority flag, or a raw `<img>` where the framework offers an optimized component. Read the major from grep 0 before writing the fix: a `priority` prop on Next 16+ still works but is the deprecated form (grep 5a), so the fix there is `preload` or `fetchPriority="high"`, never a new `priority`. Sources: Next.js `Image` API reference, version history row for v16.0.0 (docs for 16.3.8, fetched 2026-10-05); Astro `astro:assets` reference, `priority` "Added in astro@5.10.0" (fetched 2026-10-05).

## Output

```
LCP audit — <route set>

Findings: 3

1. components/Hero.tsx:14                              [report-with-fix]
   <Image src="/hero.jpg" /> on the LCP element (next 16.1, lab-inferred mobile) — no priority hint.
   Fix: <Image src="/hero.jpg" fetchPriority="high" />  (or `preload`; not the deprecated `priority`).

2. pages/index.vue:8                                   [report-with-fix]
   <img class="masthead" loading="lazy"> — lazy on the LCP candidate delays LCP.
   Fix: drop loading="lazy"; <NuxtImg preload :loading="'eager'" .../>.

3. styles/home.css:22                                  [report-with-fix]
   .hero { background-image: url(/cover.avif) } — late-discovered, no preload.
   Fix: <link rel="preload" as="image" href="/cover.avif" fetchpriority="high"> in <head>.

LCP element: components/Hero.tsx:14 (lab-inferred, lighthouse-ci mobile, Lighthouse 12.6.1 largest-contentful-paint-element)
Verification: 9 candidates → 3 findings · 0 unconfirmed · 6 refuted

Class coverage:
  §1  lazy LCP candidate          checked (2 hits → 1 finding)
  §2  no priority hint            checked (4 tags → 1 finding, 3 not the LCP element)
  §3  late-discovered, no preload checked (3 background urls → 1 finding)
  §4  cross-origin, no preconnect N/A (LCP image is same-origin)
  §5  framework priority prop     checked (folded into finding 1)
```

`[report-with-fix]`: the element is the identified LCP element and the fix is a local change in the project's own primitive. `[report-flagged]`: a link is unproven (no harness, so the element is unidentified) and the row names the run that settles it. The coverage block lists **all five** classes on every run: `checked (k hits → m findings)`, `N/A (<reason>)`, or `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

- Only the **single** LCP element gets `fetchpriority="high"`. If a scan would mark two heroes high-priority, flag it — competing high-priority fetches cancel the benefit.
- The LCP element differs by viewport (mobile hero ≠ desktop hero) and by route — confirm the real element with `web-vitals-field` attribution (`attribution.target` — the `web-vitals` 4+ name; 6.2.3's `LCPAttribution` has `target`, `url`, `resourceLoadDelay`, `elementRenderDelay`) *(performance pack, when co-installed)* before "fixing" the wrong image. Absent that pack there is no field attribution, and the lab arm below is how the element is identified instead — a label is not a substitute for running it.
- A heading/text LCP element has no image to preload — its LCP cost is font + render-blocking CSS/JS, not image priority (→ `font-optimization` for font-display / preload / swap-CLS, and critical CSS).
- This skill owns only the LCP element's **priority** (fetchpriority / preload / eager). The LCP image's **format, dimensions, and responsive sizing** belong to `image-optimization` — run both on a hero image.
- Preloading an image the page doesn't actually use wastes bandwidth and can *hurt* LCP — preload only the confirmed LCP resource.

## Identifying the LCP element without the performance pack

Every detector on this page targets *the* LCP element, so the scan is worthless until one element is named. On a frontend-only install — the default — there is no field attribution, and "pick it from the lab trace" is not a procedure. This is:

1. **Run `lighthouse-ci` (this pack) on the route** at the viewport in question, against the production build. It already runs for the LCP *number*; the same report carries the element.
2. **Read the element from the JSON report**, not from the score. Under LHCI 0.15.1 (Lighthouse 12.6.1) that is `largest-contentful-paint-element` or `lcp-phases-insight`; under Lighthouse 13 the legacy audit is gone and `lcp-breakdown-insight` (renamed from `lcp-phases-insight`) carries the node. Both insights declare `replacesAudits: ['largest-contentful-paint-element']` (unpacked 12.6.1 and 13.5.0, 2026-10-05). The element audit is informative; it names the node (selector / snippet), and that is the citation. It is not the oracle a fix is proved by (step 6).
3. **Map the node back to source.** The report gives you rendered markup, not a file — grep the selector, the `alt` text, the class, or the image path against the source tree to land on `<file:line>`. That grep is the finding's citation; a node with no source anchor is not a finding (§ Halt conditions).
4. **Repeat per viewport.** Mobile and desktop routinely resolve to different elements, and a fix applied to the wrong one is a no-op that reads as a fix. Run at minimum the mobile form factor, since that is the one CWV is scored on.
5. **Label the result honestly**: `LCP element: <file:line> (lab-inferred, lighthouse-ci <form-factor>)`. Lab inference is a real measurement of one synthetic load — it is not a claim about what users saw. Never print a field figure this skill did not read.
6. **Prove the fix on an assertable audit**, median of 5 runs (`lighthouse-ci` § Lighthouse ids by version). §1 and §2: `lcp-lazy-loaded` and `prioritize-lcp-image` on Lighthouse 12.6.1, `lcp-discovery-insight` on both 12.6.1 and 13.x (it replaces those two). §3: `lcp-discovery-insight`. §4: `uses-rel-preconnect` on 12.6.1, `network-dependency-tree-insight` on 13.x. Fails before the fix, passes after; the LCP number itself is cost, read under the noise band ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Lighthouse median").

**If `lighthouse-ci` cannot run at all** (no dev server, no build, no Chrome), the element is unknown, and this skill reports `LCP element: unidentified — scan not run` rather than falling back to "the first big image." Guessing the hero and prioritising it is how two elements end up marked high-priority, which § False positives already names as self-cancelling.

## When to run

- When `lighthouse-ci` (this pack) reports LCP > 2.5s. Also on `bundle-perf` / `web-vitals-field` *(performance pack, when co-installed)* attributing field LCP to an image with high `resourceLoadDelay`/`resourceLoadDuration`; absent that pack, `lighthouse-ci` is the only trigger and the run says so.
- After adding or restyling a hero / above-the-fold media region.
- Before launch on any public, SEO-relevant, image-led page.

## Halt conditions

- Halt on any LCP finding without the cited element at `<file:line>` + the matched pattern.
- Halt if `fetchpriority="high"` is proposed on more than one element per view.
- Halt if a preload is proposed for an image not confirmed to be the LCP resource (§ Identifying the LCP element, or field attribution when the performance pack is present). On a frontend-only install only the lab arm exists — the halt still stands, and the finding records `confirmed by: lighthouse-ci <element audit for the runner's version> (<form-factor>)` rather than implying field evidence it never had.
- Halt if any detector fired before an element was identified. Five detectors that all target "the LCP element" produce five guesses when nothing named one.
- Halt if the LCP element is text but the fix targets image priority — re-scope to font/CSS.
- Halt if a fix writes `priority` on Next 16+ (deprecated) or `preload` on Next ≤ 15 (absent) — read the major from grep 0 first.
- Halt before reporting any candidate that has not been through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§1 restate … §9) and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 83 and § 87 (lazy below the fold, text LCP).

## Related

- `code-splitting.md` (ai-pattern) — the LCP-critical component must never be lazy-loaded (a chunk round-trip before paint); that pattern's detector 7 hands off here, and this skill rejects any lazy proposal in the LCP subtree.
- `image-optimization` / `font-optimization` — the two halves this skill deliberately does not own: format/dimensions/responsiveness for an image LCP, `font-display`/preload/swap-CLS for a text LCP. This skill only sets priority.
- `lighthouse-ci` — the lab measurement that triggers this scan; it reports the number, this skill names the element.
- Cross-pack (`performance`, when co-installed): `web-vitals-field` supplies `attribution.target` — the only source that proves which element users actually saw as LCP. Absent that pack, every finding here is lab-inferred and must be labelled as such; never print a field figure this skill did not read.

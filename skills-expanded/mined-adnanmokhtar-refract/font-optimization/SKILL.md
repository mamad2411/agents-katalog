---
name: font-optimization
description: Web-font delivery — no font-display, critical font not preloaded, remote font CSS, swap CLS without metric overrides, no subset, weight fan-out, non-woff2.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# font-optimization

## Premise

**A web font is on the critical path for text: it either blocks the text from rendering (FOIT — invisible text) or, when it swaps in, shifts the layout (FOUT → CLS).** Every custom family/weight/style is also a byte payload and often an extra cross-origin round-trip. The fix set is small and mechanical: declare `font-display`, preload the one critical font, self-host, subset, and give the fallback matching metrics so the swap doesn't move anything. Every finding cites the declaration at `<file:line>` + the matched pattern + the fix. "Fonts are slow" without the cited `@font-face`/link is not a finding.

**Closure verbs** — exactly one per finding. This skill emits `report-with-fix`, `dismiss` (a deliberate `font-display: optional`, a system-font stack, a framework primitive that already self-hosts and metric-adjusts), and `halt-handoff` (a text LCP element's priority → `lcp-audit`; a locale set that forbids the proposed subset → `/i18n-audit`).

Division of labor: this skill owns **font loading strategy + swap-induced CLS**. When the LCP element is a *heading/text block*, its LCP timing depends on font+CSS — `lcp-audit` flags that the LCP element is text; this skill supplies the font fix. Pair with `lighthouse-ci`: `font-display` (Lighthouse 12.6.1) / `font-display-insight` (12.6.1 and 13.x), and `cls-culprits-insight` for swap CLS (`lighthouse-ci` § Lighthouse ids by version).

## Adapt to the codebase first

Detect and **mirror the font mechanism in use** — several frameworks self-host + metric-adjust automatically, which dissolves most findings:

| Framework / setup | Font primitive | What it auto-handles |
|---|---|---|
| **Next.js** | `next/font/google` / `next/font/local` | self-hosts (no external request), `font-display: swap`, auto `size-adjust` fallback (near-zero CLS), preload |
| **Nuxt** | `@nuxt/fonts` | self-host + download + `font-display` + fallback metrics |
| **SvelteKit / Astro / Vite** | `@fontsource/*` packages or Fontaine (`unplugin-fontaine`) | self-host; Fontaine injects `size-adjust` fallbacks |
| **Plain CSS** | `@font-face` + `<link rel="preload">` | manual: you set `font-display`, `format('woff2')`, preload, subset, `size-adjust` |
| **Remote (Google Fonts `<link>`)** | the CSS `<link>` | ← the thing to *replace*: render-blocking, extra origin, privacy/consent surface |

If the project already uses `next/font` / `@nuxt/fonts` / Fontsource, most items below are handled — verify, don't re-implement.

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. Files-without-match is `--files-without-match`, never `-L` (that is `--follow` in ripgrep). An `rg` error on stderr (exit 2) is a failed grep, not zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|next|nuxt)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--|\{/\*)')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
CSS=(-g '*.{css,scss,sass,less,styl,pcss,vue,svelte,astro,html}')
FF='@font-face\s*\{[^}]*\}'                                             # one @font-face block; -U lets it span lines
# 0. Lanes: next/font, @nuxt/fonts, Fontsource, Fontaine, a remote kit.
rg -n --no-heading '"(next|@nuxt/fonts|@fontsource(?:-variable)?/[\w-]+|fontaine|unplugin-fontaine|@capsizecss/[\w-]+|nuxt-font-metrics)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -l --no-heading --pcre2 "from\\s+[\"']next/font/(?:google|local)[\"']" -g '*.{ts,tsx,js,jsx}' "${X[@]}" "${ROOTS[@]}"
# 1. An @font-face with no font-display (a metric-fallback face whose src is only local() downloads nothing: skipped).
rg -n -U --no-heading --pcre2 "@font-face\\s*\\{(?![^}]*font-display)(?=[^}]*\\burl\\()[^}]*\\}" "${CSS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. Font preloads that exist (2a; read each for crossorigin and for the above-the-fold face) vs self-hosted woff2 faces (2b).
rg -n --no-heading --pcre2 '<link\b(?=[^>]*\brel=["\x27]?preload)(?=[^>]*\bas=["\x27]?font)|\bas\s*:\s*["\x27]font["\x27]' "${UI[@]}" -g '**/{nuxt,next,astro,vite}.config.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -c --pcre2 '\burl\(\s*["\x27]?[^)"\x27]*\.woff2' "${CSS[@]}" "${X[@]}" "${ROOTS[@]}"
# 3. Remote font CSS: Google Fonts, Typekit, Bunny, cdnfonts — as <link>, @import or a head entry in config.
rg -n --no-heading --pcre2 'fonts\.googleapis\.com|use\.typekit\.net|p\.typekit\.net|fonts\.bunny\.net|fonts\.cdnfonts\.com|fast\.fonts\.net' "${UI[@]}" "${CSS[@]}" -g '**/{nuxt,next,astro,vite}.config.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. Metric overrides in use (size-adjust / ascent-override, or a primitive that generates them).
rg -n --no-heading --pcre2 '\b(?:size-adjust|ascent-override|descent-override|line-gap-override)\s*:|adjustFontFallback|fallbacks\s*:' "${CSS[@]}" -g '*.{ts,tsx,js,jsx,mjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. Files declaring @font-face with no unicode-range (subset candidates; read the locale set first). Greps 5 and 8 anchor
#    @font-face at the start of a line, so a stylesheet comment that mentions it is not a face.
rg -l --pcre2 '^\s*@font-face' "${CSS[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match 'unicode-range'
# 6. Weight fan-out: @font-face weight declarations (6a) and remote URLs requesting a weight list (6b).
rg -c -U --pcre2 '@font-face\s*\{[^}]*\bfont-weight\s*:' "${CSS[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -o --no-heading --pcre2 'family=[^&"\x27\s]*(?:wght|ital,wght)@[\d;,.]+' "${UI[@]}" "${CSS[@]}" "${X[@]}" "${ROOTS[@]}"
# 7. A non-woff2 primary source, or a src url with no format() hint (local()-only fallback faces skipped).
rg -n -U --no-heading --pcre2 "@font-face\\s*\\{[^}]*\\bsrc\\s*:\\s*url\\([^)]*\\.(?:ttf|otf|eot|woff)(?:[?#][^)]*)?[\"']?\\)|@font-face\\s*\\{(?![^}]*\\bformat\\()(?=[^}]*\\burl\\()[^}]*\\bsrc\\s*:" "${CSS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 8. Hand-rolled faces in a project that ships a font primitive: compare grep 0 with the @font-face count.
rg -c --pcre2 '^\s*@font-face' "${CSS[@]}" "${X[@]}" "${ROOTS[@]}"
```

A hit is a candidate. Two blind spots are structural:

- **A framework primitive writes its faces at build time.** `next/font`, `@nuxt/fonts` and Fontaine emit `@font-face`, `font-display`, preloads and metric overrides into the build output, so greps 1, 2 and 4 see nothing in source. On those lanes read the primitive's options (`display`, `preload`, `adjustFontFallback`, `fallbacks`) and, once, the built CSS.
- **Grep 5 is file-level.** One `unicode-range` anywhere in a file hides an unsubset face beside it; read every face in the files it does not list.

**Measured** (2026-10-05, read-only). Scratch fixture: a face with no `font-display`, a `.ttf` face with no `format()`, a Google Fonts `@import` with five weights, all hit; the `optional` + `unicode-range` face stays out of 1, 5 and 7. Benchmark fixtures: 0 on every grep (none ships a web font). Real repos: a Nuxt 4 storefront (3: a Google Fonts URL built at runtime from the theme's family, 4 lines, with a preconnect; 4: hand-written metric overrides on its fallback face), a Vue 3 + Vite admin SPA (3: 2) and an Angular 19 admin template (1: one icon-font face plus two minified vendor stylesheets that each match as one long line; 5: 6 files, all vendor or icon-font CSS copied into `public/`: one vendor group). An SCSS interpolation `#{$var}` closes the `[^}]*` block early, so a hit inside a `.scss` face (grep 7 on the template's Tabler icons) is read before it is believed. Before restricting 6a to inside `@font-face` blocks it counted every `font-weight` rule (119 on the storefront). Re-measured 2026-10-15 on a real NestJS + React monorepo (Vite SPA, self-hosted Arabic and Latin faces): greps 1 and 7 had each flagged the metric-fallback face (`src: local('Segoe UI'), local('Arial')` with `size-adjust` overrides) — it downloads nothing, so neither a `font-display` nor a `format()` hint applies; both now require a `url(` in the face: 1 → 0, 7 → 0. Greps 5 and 8 had counted a stylesheet comment that names `@font-face` as a declaring file: 5 1 → 0 files, 8 2 → 1 file. Fixtures: unchanged (none ships a web font).

## The 3,000-hit path

1. **Group** by face (family + weight + style) and by vendor stylesheet: an icon font copied into the tree is one finding, not one per glyph rule.
2. **Rank** by whether the face renders above the fold on a top route (the body and heading faces first).
3. **Read the top 30 groups.** Ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them, never `checked`.

## Scans for

### 1. Missing `font-display` → FOIT (invisible text)

Without `font-display`, most browsers block text for up to 3s waiting for the font.

```
BAD:  @font-face { font-family: Inter; src: url(inter.woff2) format('woff2'); }
GOOD: @font-face { font-family: Inter; src: url(inter.woff2) format('woff2'); font-display: swap; }
```

Flag any `@font-face` with no `font-display`. `swap` for body/brand text; `optional` when zero CLS matters more than always getting the custom font.

### 2. Critical font not preloaded (self-hosted)

A self-hosted font referenced only from CSS is discovered late (after CSS parses).

```
GOOD: <link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
```

Flag the primary above-the-fold font with no `<link rel="preload" as="font" crossorigin>`. **Preload only the one or two fonts actually used above the fold** — preloading all weights hurts.

### 3. Render-blocking remote font CSS not self-hosted

A Google Fonts `<link>` costs an extra origin (DNS+TCP+TLS), is render-blocking, and is a privacy/consent surface (GDPR).

```
BAD:  <link href="https://fonts.googleapis.com/css2?family=Inter…" rel="stylesheet">
GOOD: self-host via next/font, @nuxt/fonts, or @fontsource/inter (no external request)
```

Flag remote font stylesheets; recommend self-hosting through the framework primitive. If it must stay remote, require `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`.

### 4. No fallback metric override → font-swap CLS

When the custom font swaps in, differing metrics reflow text unless the fallback is size-matched.

```
GOOD: @font-face { font-family: 'Inter-fallback'; src: local('Arial');
        size-adjust: 107%; ascent-override: 90%; descent-override: 22%; line-gap-override: 0%; }
      body { font-family: Inter, 'Inter-fallback', sans-serif; }
```

Flag a custom body font with `font-display: swap` and no adjusted fallback (`size-adjust`/`ascent-override`, or Fontaine/`next/font` which generate it). This is the font half of CLS.

### 5. Full charset shipped (not subset)

A full multi-language font can be 100–300KB; a Latin subset is a fraction.

```
GOOD (self-host): unicode-range: U+0000-00FF;   // Latin subset per @font-face
```

Flag large self-hosted fonts with no `unicode-range` subsetting for a project whose content is single-script. (Don't strip glyphs a multilingual site needs.)

### 6. Too many families / weights / styles

Each weight+style is a separate file. Loading 6 weights when the UI uses 2 is wasted bytes.

Flag more than ~2 families or a long weight list where the design system uses few. Prefer a **variable font** (one file, all weights) when ≥3 weights are loaded.

### 7. Legacy format before `woff2` / missing `format()`

```
GOOD: src: url(f.woff2) format('woff2');       // woff2 first; drop ttf/eot/woff for modern targets
```

Flag `@font-face` shipping `.ttf`/`.eot`/`.otf`/`.woff` (non-woff2) as the primary, or `src` with no `format()` hint (forces a wasted download attempt).

### 8. Framework primitive not adopted

Flag hand-rolled `@font-face` + `<link>` in a project that ships `next/font` / `@nuxt/fonts` / Fontsource — adopting it self-hosts, sets `font-display`, and generates metric fallbacks in one change.

## Output

```
font-optimization — <scope>   (mechanism: <e.g. next/font | @font-face | Google <link>>)

Findings: 4

1. app/layout.tsx:6                                    [report-with-fix]
   <link href="fonts.googleapis.com/css2?family=Inter"> — remote, render-blocking, consent surface.
   Fix: import { Inter } from 'next/font/google' (self-hosts + swap + size-adjust fallback).

2. styles/fonts.css:3                                  [report-with-fix]
   @font-face Inter — no font-display → up to 3s of invisible text.
   Fix: add font-display: swap;

3. styles/fonts.css:3                                  [report-with-fix]
   swap set but no size-matched fallback → text reflows on swap (CLS).
   Fix: add an 'Inter-fallback' @font-face with size-adjust/ascent-override; list it before sans-serif.

4. styles/fonts.css:10-20                              [report-with-fix]
   6 static weights of one family loaded.
   Fix: one variable font file (Inter var, wght 100–900) — smaller than 3 static weights.

Verification: 9 candidates → 4 findings · 0 unconfirmed · 5 refuted

Class coverage:
  §1  font-display missing      checked (1 face → 1 finding)
  §2  critical font preload     checked (0 preloads, 1 above-the-fold face → folded into finding 1's fix)
  §3  remote font CSS           checked (1 hit → 1 finding)
  §4  swap CLS, no overrides    checked (1 face → 1 finding)
  §5  no subset                 N/A (declared locales include ar; Latin subset would drop glyphs)
  §6  weight fan-out            checked (6 weights → 1 finding)
  §7  non-woff2 / no format()   checked (0 hits)
  §8  primitive not adopted     checked (next/font installed; folded into finding 1)
```

`[report-with-fix]`: the face is cited, renders on a cited route, and the fix goes through the project's primitive. `[report-flagged]`: a link is unproven (which face is above the fold, or the swap shift, was not observed on a render) and the row names the run that settles it. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)`, `N/A (<reason>)`, or `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

- **`font-display: optional` intentionally skips the swap** to guarantee zero CLS (uses fallback if the font isn't cached in ~100ms). Don't "fix" a deliberate `optional` to `swap`.
- **Preloading every weight backfires** — it floods the critical path. Preload only the 1–2 above-the-fold fonts; let the rest lazy-load via CSS.
- **`crossorigin` is mandatory on font preload** even same-origin, or the browser fetches the font twice. Flag a font `preload` missing `crossorigin`.
- **System font stacks need none of this** — if the project uses `system-ui`/native stacks, there's nothing to optimize; don't invent a web-font problem.
- **Subsetting can drop needed glyphs** — only recommend `unicode-range` Latin subsets for confirmed single-script content (check the i18n locales).

## When to run

- When `lighthouse-ci` fails `font-display` / `font-display-insight`, reports swap CLS in `cls-culprits-insight`, or a render-blocking font stylesheet in `render-blocking-resources` / `render-blocking-insight`.
- When `lcp-audit` reports the LCP element is a heading/text block (its cost is font + CSS, not image priority).
- After adding a font, a new weight, or a Google Fonts `<link>`.

## Halt conditions

- Halt on any finding without the cited `@font-face`/link at `<file:line>` + the matched pattern + the fix.
- Halt if a fix proposes changing a deliberate `font-display: optional` to `swap` without cause.
- Halt if a preload set exceeds the 1–2 above-the-fold fonts actually used, or omits `crossorigin`.
- Halt if `unicode-range` subsetting is proposed for a multilingual project without confirming the locale set.
- Halt if the project already self-hosts via a framework primitive and the fix reintroduces a remote `<link>`.
- Halt before reporting any candidate that has not been through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§1 restate … §9). **Proof:** the font audit for the runner's Lighthouse version and `cls-culprits-insight`, median of 5 runs ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Lighthouse median"); a swap-CLS fix is proved by the layout-shift observer naming no text node after the fix (`critical-path-scan` § Proof, item 3).

## Related

- `lcp-audit` — a text LCP element waits on the font; the preload this skill adds and the priority that skill sets are the same critical path seen from two ends.
- `image-optimization` — the other asset lane. Font swap-CLS and image dimension-CLS both land in the same CLS score; report them separately so the fix is attributable.
- `lighthouse-ci` — measures the CLS / render-blocking result of these fixes; it does not tell you which `@font-face` caused it.
- `.claude/rules/frontend-principles.md` — the `font-display` / self-host / preload-critical-font / size-adjusted-fallback MUSTs this skill enforces.
- `i18n.md` (ai-pattern) — subsetting is locale-dependent: a Latin-only subset silently breaks a declared non-Latin locale. Check the declared locale set before proposing `unicode-range`.

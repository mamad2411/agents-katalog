---
name: seo-audit
description: "Technical SEO: titles, canonical, social tags, JSON-LD, noindex, sitemap/robots, hreflang, CSR-only routes — proved on server HTML."
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: seo-audit

## Premise

**A crawler reads the HTML the server sends, not the page you see in the browser.** The route renders, the tab shows the right title, and the server answer to a crawler carries a `noindex` left over from staging, the layout's title on 200 blog posts, a canonical built from the live URL with `?utm_source=` in it, no description, or an empty `<div id="root">`. Google can render JavaScript, but a `noindex` in the first HTML may stop it rendering at all, and social and many other crawlers never run it. None of this shows in a browser, a unit test or a lint run.

This skill finds those defects in source across Next.js, Nuxt, SvelteKit, Astro, React Router / Remix, Vite SPAs with `react-helmet-async`, and Angular, and proves each one against the server HTML of a **production build** with `scripts/seo-head.py`. It owns `/frontend-audit`'s SEO rows §1–§9. `@technical-seo` (this pack) judges and ranks its rows: indexation policy, the canonical choice, which schema type fits.

**Every finding cites the source `<file:line>` + the route and its route class + what the server HTML shows (the `seo-head.py` row) + the fix in the project's own metadata primitive.** A grep hit is never a finding by itself. "SEO looks fine" is never printed: the output is the class-coverage block (§ Output).

**Detect statically, prove on the server HTML.** A candidate with no production build to fetch is **Unconfirmed** and carries the `seo-head.py` command that would settle it. It is never dropped, and never promoted on reading alone.

## The rule

A candidate is a finding when all four hold:

1. **The route class makes it matter** (§ Route class). A title band on an admin dashboard, or Open Graph tags on a thank-you page, is not a finding.
2. **The crawler receives it.** The defect is in the server HTML or the response headers, not only in client state. A tag the client fixes after hydration still fails for a crawler that runs no JavaScript. For Google, see §5 and §8.
3. **Nothing already handles it.** The layout's metadata, the framework's default (Next resolves a relative canonical against `metadataBase`), an SEO module (`@nuxtjs/seo`, `@nuxtjs/i18n` hreflang), or a server header already gives the right answer.
4. **The oracle fired.** The `seo-head.py` row for that route on a production build shows the defect.

## Boundaries

- **Headings and `alt` text as accessibility** → `a11y-code-scan` and `a11y-scan` (this pack). They are filed once, as accessibility; §9 here only asks whether a crawler can find the links.
- **Click navigation on a non-link** → `routing-scan` §1 owns the missing `href` (this pack), and `a11y-code-scan` §1 owns the keyboard half. §9 here corroborates on indexable routes. **Soft 404** (an unknown URL answering 200) → `routing-scan` §4. §5 here only adds the `noindex` / status expectation for the crawler.
- **Why a route renders on the client** → `ssr-audit` and `streaming-ssr` (this pack), and the `rendering-strategy` pattern. §8 here proves the crawler gets an empty body and hands the fix over (`[halt-handoff]`).
- **The locale set and `lang` / `dir`** → `i18n-scan` (this pack). §7 here owns `hreflang` only.
- **Page speed as a ranking input** → `lcp-audit`, `lighthouse-ci` (this pack), and `/bundle-perf` when the performance pack is installed. Not graded here.
- **JSON-LD written into a raw `<script>` with `JSON.stringify`** (grep 4b): a `</script>` inside user data breaks out of the block. That is `xss-scan` (security pack), when installed. Without the security pack, the row is reported here tagged `security-class (owner pack not installed)`.
- **Robots directives aimed at AI crawlers** (`GPTBot` rules, `llms.txt`, `Content-Signal`) are not checked: no crawler is obliged to honour them, so there is no conformance to prove.

## Adapt to the codebase — the metadata lanes

Mirror the primitive the project already uses; a fix never adds a second mechanism. Read each version from the lockfile and print the lanes in the output header. Versions below were read from the npm registry on 2026-10-05.

| Lane | Metadata primitive | Sitemap / robots | Facts the lane depends on |
|---|---|---|---|
| **Next.js App Router** (16.3.8) | `export const metadata` / `generateMetadata`, `alternates.canonical` / `.languages`, `robots`, `metadataBase` | `app/sitemap.ts`, `app/robots.ts` | A relative URL in a metadata field with no `metadataBase` is a build error. `generateMetadata` output is **streamed** into `<body>` for user agents not listed as HTML-limited bots, and stays in `<head>` for the bots on the `htmlLimitedBots` list (Next.js docs, *generateMetadata*, docs version 16.3.8, updated 2026-08-25) |
| **Next.js Pages Router** | `next/head`; `next-seo` 7.3.0 if already used | `next-sitemap` 4.2.3 (last published 2023-09-06) | — |
| **Nuxt 4** (4.5.2) | `useSeoMeta` / `useServerSeoMeta` / `useHead`, `definePageMeta({ title })`, or a project composable | `@nuxtjs/seo` 5.3.16, `@nuxtjs/sitemap` 8.6.1, `@nuxtjs/robots` 6.2.4; `routeRules` headers | hreflang from `@nuxtjs/i18n` comes from each locale's `language` code — read the config |
| **SvelteKit** (3.0.0) | `<svelte:head>` in `+page.svelte`, data from `load` | `src/routes/sitemap.xml/+server.ts` | `export const ssr = false` empties the server body |
| **Astro** (7.3.5) | the layout `<head>`; `astro-seo` 1.2.0 if used | `@astrojs/sitemap` 3.7.4 | — |
| **React Router / Remix** (react-router 8.4.0) | route `meta` export; React 19 `<title>` / `<meta>` / `<link>` in components | a resource route | React hoists `<title>` into `<head>`, and its children must be **one string**: `<title>Results {n}</title>` is two children (react.dev, *title*, read 2026-10-05) |
| **Vite SPA** | `react-helmet-async` 3.0.0, `@unhead/vue` 3.4.2 | build script or prerender plugin | Without prerendering, the server HTML is the shell; every tag arrives by script |
| **Angular** (22.2.1) | `Title` / `Meta` services, route `title` | a route or the build | Without `@angular/ssr` or prerendering, the server HTML is `index.html` with `<app-root></app-root>` |

A project wrapper (`useSEO()`, `<Seo>`, `usePageMeta()`) is found by grep 0c and counted as a primitive. Every fix goes through it.

## Route class decides which classes run

Classify each route first; the class is a fact about the route, not a preference. Print it beside every row.

| Route class | How you know | Classes that run | Classes dismissed, with the reason |
|---|---|---|---|
| **Indexable** — home, marketing, blog, docs, product, category | public, no auth gate, linked from the sitemap or the navigation | all nine | — |
| **Public, not meant to rank** — thank-you, print, preview and share links, filter permutations | public, no search intent | §5 (`noindex` **present** is the pass), §2 (canonical to the rankable parent), §8 | §1, §3, §4, §7, §9: a title band on a page that must not rank is noise |
| **Auth-gated app** — dashboard, settings, admin | a route guard or a server session check | §5 inverted (a **missing** `noindex` on a server-rendered, reachable route), §8 only if it renders a document | everything else: `seo: N/A (auth-gated)` |
| **Not a document** — `robots.txt`, sitemaps, API and resource routes | not HTML | §6, as the subject | everything else |

Two edges: an `/admin` route with no auth gate and no `noindex` is a public route, and §5 fires. And **§8 runs on every class that renders a document**: on an empty server body, the §1–§4 and §7 rows grade tags no crawler that skips JavaScript reads, so §8 is reported first and those rows wait for the handoff.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`"${ROOTS[@]}"`); given no path, rg reads stdin under an agent's shell and reports a silent zero. Any rg exit 2 is a failed grep, never zero hits. `B` is one JSX expression with one level of nesting. File-level greps use `--files-without-match`, never `rg -L` (which is `--follow`). Add the project's own metadata components to `META` when grep 0c misses them. The scratch folder comes from `${TMPDIR:-/tmp}`: under a run that must not write to the system temp dir, export `TMPDIR` to the run's scratch folder first.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|vue|svelte|@angular/core|solid-js|preact|next|nuxt|astro|react-router)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,.astro,.vercel,coverage,storybook-static}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,__fixtures__,playwright,cypress,msw}/**' -g '!**/*.{test,spec,stories,story,e2e,mock,mocks}.*'
   -g '!**/*.{test-data,fixture,fixtures}.*' -g '!**/{locales,locale,i18n,translations,docs,generated,__generated__}/**' -g '!**/*.min.*')
J=(-g '*.{js,jsx,ts,tsx,mjs,cjs,vue,svelte,astro,html}'); C=(-g '*.{js,jsx,ts,tsx,mjs,cjs,vue,svelte,astro,html,json,toml,yml,yaml,conf}' -g '_headers' -g '!**/package-lock.json')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--)')   # drops comment-only lines
PR=(\( -name node_modules -o -name .next -o -name .nuxt -o -name .output -o -name dist -o -name build -o -name .svelte-kit -o -name .angular \) -prune -o)
B='\{(?:[^{}]|\{[^{}]*\})*\}'   # one JSX expression, one nesting level
META='export\s+(?:const\s+metadata\b|(?:async\s+)?function\s+generateMetadata\b)|\buse(?:Server)?SeoMeta\(|\buseHead\(|\bdefinePageMeta\(\s*\{[^)]*\btitle\b|<svelte:head>|<(?:Helmet|Head|NextSeo|Seo|SEO|title)\b|export\s+(?:const|(?:async\s+)?function)\s+meta\b|\.setTitle\(|\bmeta\.(?:updateTag|addTag|addTags)\('
T="$(mktemp -d "${TMPDIR:-/tmp}/seo-pf.XXXXXX")"
# 0a frameworks, SSR / prerender and SEO libraries with versions; 0b route files (pages) per lane, dynamic segments tagged — on a
#    router-table SPA (createBrowserRouter / <Routes> and no file-routing framework) `pages/` folders are views, not routes: the
#    route list is routing-scan's 0b table and 1a waits on §8; 0c the project's own SEO wrappers, added to META; 0d an edge
#    (ingress, proxy, worker) that rewrites crawler user agents to a server-built head.
W=$(rg -o --no-filename --pcre2 'export\s+(?:default\s+)?(?:const|(?:async\s+)?function)\s+\K(?:use|with)\w*(?:Seo|SEO|Head|Meta)(?:Tags?|Data|Info)?\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | paste -sd'|' -); [ -n "$W" ] && META="$META|\\b(?:$W)\\("; echo "0c project SEO wrappers: ${W:-none}"
rg -n -i --pcre2 '\b(?:facebookexternalhit|facebot|twitterbot|slackbot|linkedinbot|telegrambot|discordbot|googlebot|bingbot|pinterestbot|embedly)\b' -g '*.{conf,yaml,yml,toml,json,lua,vcl,js,mjs,cjs,ts}' -g 'Caddyfile*' -g '*nginx*' -g '_redirects' -g '!**/node_modules/**' -g '!**/{dist,build,coverage,test,tests,__tests__,e2e,src,app,locales,i18n}/**' -g '!**/*.{test,spec}.*' . | sed 's/^/0d crawler head served by the edge: /'
rg -n --no-heading --pcre2 '"(?:next|nuxt|@sveltejs/kit|astro|@angular/(?:core|ssr|platform-server)|@nguniversal/express-engine|react-router|@remix-run/react|@tanstack/react-router|react|vue|react-helmet-async|react-helmet|next-seo|next-sitemap|@nuxtjs/(?:seo|sitemap|robots|i18n|schema-org)|nuxt-schema-org|@astrojs/sitemap|astro-seo|schema-dts|vike|vite-plugin-ssr|vite-ssg|react-snap|@prerenderer/[\w-]+|@unhead/\w+)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
RT=$(rg -l --pcre2 'createBrowserRouter|createHashRouter|createMemoryRouter|<Routes\b|\bcreateRouter\(|provideRouter\(|RouterModule\.forRoot\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | paste -sd' ' -)
FS=$(rg -l --pcre2 '"(?:next|nuxt|@sveltejs/kit|astro|@remix-run/\w+|@react-router/dev|@tanstack/react-start|vike|vite-plugin-ssr|vite-ssg|@analogjs/platform)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}")
if [ -n "$RT" ] && [ -z "$FS" ]; then : > "$T/pages"; echo "0b router-table SPA: route table in $RT — take the routes (and their class) from routing-scan grep 0b; 1a waits on §8"
  echo "0b script-set heads (never in the server HTML): $(rg -l --pcre2 '\bdocument\.title\s*=|<(?:Helmet|title)\b|\buseHead\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') files"
else for r in "${ROOTS[@]}"; do find "$r" "${PR[@]}" -type f \( \( -path '*/app/*' -name 'page.[jt]s*' \) -o \( -path '*/app/routes/*' -name '*.[jt]sx' \) -o -name '+page.svelte' -o \( -path '*/pages/*' ! -path '*/pages/api/*' ! -path '*/components/*' ! -name '_*' \( -name '*.vue' -o -name '*.[jt]sx' -o -name '*.astro' -o -name '*.md' -o -name '*.mdx' \) \) \) ! -name '*.test.*' ! -name '*.spec.*' ! -name '*.stories.*' ! -name '*.test-data.*' -print; done | sort > "$T/pages"; echo "0b route files: $(wc -l < "$T/pages" | tr -d ' ') ($(grep -c '\[' "$T/pages") dynamic)"; fi
# 1a route files with no metadata primitive of their own (the layout's applies: read it); 1b one literal title in 2+ metadata files; 1c React <title> with text and an expression as separate children.
tr '\n' '\0' < "$T/pages" | xargs -0 -r rg --files-without-match --pcre2 "$META" | sed 's/^/1a /'
rg -l --pcre2 "$META" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -o -H --no-line-number --pcre2 '(?:\btitle\s*:\s*|<title>\s*)["\x27]([^"\x27<>{}$]{3,90})["\x27]|<title>([^<{]{3,90})</title>' -r '$1$2' | sort -u | awk -F: '{v=substr($0,length($1)+2); n[v]++; f[v]=f[v]" "$1} END {for (v in n) if (n[v]>1) print "1b", n[v]" files: \""v"\" —"f[v]}'
rg -n --pcre2 "<title>(?=(?:[^<{]|$B)*?[^\s<{}])(?=(?:[^<{]|$B)*?\{)(?:[^<{]|$B)*</title>" -g '*.{jsx,tsx}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/1c /'
# 2a canonical declarations; 2b relative canonical (Next resolves it against metadataBase — listed below); 2c canonical or og:url from the live URL (keeps query and tracking parameters).
rg -n -U --pcre2 'rel\s*[:=]\s*["\x27]canonical["\x27]|\balternates\s*:\s*\{[^}]*?\bcanonical\s*:|<\w*(?:Seo|SEO|Meta|Head)\b[^>]*?\bcanonical\s*=\s*["\x27{]|setAttribute\(\s*["\x27]rel["\x27]\s*,\s*["\x27]canonical' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/2a /'
rg -n --pcre2 '\bcanonical\s*:\s*["\x27`]/(?!/)|rel\s*=\s*["\x27]canonical["\x27][^>]*\bhref\s*=\s*["\x27]/(?!/)' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/2b /'; rg -l '\bmetadataBase\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | sed 's/^/2b metadataBase: /'
rg -n --pcre2 '(?:canonical|og:url|ogUrl)\b[^\n]{0,100}\b(?:location\.href|window\.location|router\.asPath|route\.fullPath|\$route\.fullPath|useRequestURL\(\)(?:\.href)?|req(?:uest)?\.url|url\.href|this\.router\.url|document\.URL)\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/2c /'
# 3a relative og:image / twitter:image; 3b repo-level social-tag presence (zero on an app with indexable routes is the candidate; the oracle settles each route).
rg -n --pcre2 '(?:og|twitter):image["\x27]?\s*,?\s*(?:content\s*[:=]\s*)?["\x27`]/(?!/)|(?:og|twitter)Image\s*:\s*["\x27`]/(?!/)|\bimages\s*:\s*\[?\s*(?:\{\s*url\s*:\s*)?["\x27`]/(?!/)' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/3a /'
echo "3b og files: $(rg -l --pcre2 'og:(?:title|image)|\bopenGraph\s*:|\bog(?:Title|Image)\s*:' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · twitter-card files: $(rg -l --pcre2 'twitter:card|\btwitterCard\s*:|\btwitter\s*:\s*\{' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
# 4a JSON-LD sites; 4b JSON.stringify into a raw <script> (a `</script>` in the data breaks out — route to xss-scan); 4c types Google Search no longer shows as a rich result.
rg -n --pcre2 'application/ld\+json|\buseSchemaOrg\(|\bdefine(?:WebPage|WebSite|Organization|Product|Article|BreadcrumbList|LocalBusiness)\(|<JsonLd\b|\bjsonLd\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/4a /'
rg -n --pcre2 'dangerouslySetInnerHTML\s*=\s*\{\{\s*__html\s*:\s*JSON\.stringify\(|v-html\s*=\s*["\x27]JSON\.stringify\(|\{@html\s+JSON\.stringify\(|\binnerHTML\s*=\s*JSON\.stringify\(|\binnerHTML\s*:\s*JSON\.stringify\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/4b /'
rg -n --pcre2 '["\x27]?@type["\x27]?\s*:\s*["\x27](?:FAQPage|HowTo|ClaimReview|SpecialAnnouncement|Quiz)["\x27]|\bSearchAction\b|\bestimatedSalary\b|\bdefine(?:Question|HowTo|FAQPage)\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/4c /'
# 5a noindex and X-Robots-Tag in source and server config; 5b robots.txt blocking the site or its render assets; 5c the robots meta changed from script.
rg -n --pcre2 '\bnoindex\b|\bindex\s*:\s*false\b|X-Robots-Tag' "${C[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/5a /'
for r in "${ROOTS[@]}"; do find "$r" "${PR[@]}" -type f \( -name 'robots.txt' -o -name 'robots.[jt]s' -o -name 'sitemap*.xml' -o -name 'sitemap.[jt]s' -o -name 'sitemap.xml.[jt]s' -o -name 'next-sitemap.config.*' -o -path '*sitemap*/+server.[jt]s' -o -path '*robots.txt/+server.[jt]s' \) -print; done | sort > "$T/crawl"; sed 's/^/6a /' "$T/crawl"
tr '\n' '\0' < "$T/crawl" | xargs -0 -r rg -n -i --pcre2 '^\s*Disallow:\s*/\s*$|^\s*Disallow:\s*/(?:_next|_nuxt|assets|static|build|_app)/|^\s*Disallow:\s*/?\*?\.(?:js|css)\b|\bdisallow\s*:\s*["\x27]/["\x27]' | sed 's/^/5b /'
rg -n --pcre2 'meta\[name=["\x27]?robots|name\s*=\s*["\x27]robots["\x27][^\n]*(?:setAttribute|\.content\s*=)|\bmeta\.(?:updateTag|removeTag|addTag)\(\s*\{?\s*name\s*:\s*["\x27]robots' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/5c /'
# 6b sitemap and robots wired through a module or config; 6c robots.txt with no Sitemap line; 6d static sitemap with relative <loc>.
rg -n --pcre2 '@nuxtjs/(?:sitemap|robots|seo)|@astrojs/sitemap|\bsitemap\s*:\s*\{|\brobots\s*:\s*\{|\bsite\s*:\s*\{[^}]*\burl\b' -g '{nuxt,astro,next,vite,svelte}.config.*' "${X[@]}" "${ROOTS[@]}" | sed 's/^/6b /'
grep 'robots\.txt$' "$T/crawl" | tr '\n' '\0' | xargs -0 -r rg -i --files-without-match '^\s*Sitemap:' | sed 's/^/6c no Sitemap line: /'
grep '\.xml$' "$T/crawl" | tr '\n' '\0' | xargs -0 -r rg -H -n --pcre2 '<loc>\s*(?!https?://)' | sed 's/^/6d /'
# 7a hreflang and locale alternates; 7b codes Google rejects (underscore, -uk) in hreflang or in the locale config that generates it.
rg -n --pcre2 '\bhreflang\b|\balternates\s*:\s*\{[^}]*\blanguages\b|\buseLocaleHead\(|\bx-default\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/7a /'
rg -n -i --pcre2 '(?:hreflang|\blanguage)\s*[=:]\s*["\x27](?:[a-z]{2,3}_[a-z]{2}|[a-z]{2}-uk)["\x27]' "${J[@]}" -g '*.config.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/7b /'
# 8a server rendering switched off (app, route or component); 8b SPA shells with an empty mount node; 8c Next client pages that load their content in an effect; 8d Next streaming-metadata override.
rg -n --pcre2 '\bssr\s*:\s*false\b|export\s+const\s+ssr\s*=\s*false|export\s+const\s+prerender\s*=\s*false|\brenderMode\s*:\s*RenderMode\.Client\b' "${J[@]}" -g '*.config.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/8a /'
rg -n --pcre2 '<div\s+id=["\x27](?:root|app|__next)["\x27]\s*>\s*</div>|<app-root>\s*</app-root>' -g 'index.html' "${X[@]}" "${ROOTS[@]}" | sed 's/^/8b /'
grep -E '/app/.*page\.[jt]sx?$' "$T/pages" | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 '^\s*["\x27]use client["\x27]' | xargs -r rg -l '\buseEffect\(' | xargs -r rg -l --pcre2 '\bfetch\(|\baxios\b|\buseQuery\(|\buseSWR\(' | sed 's/^/8c /'
rg -n 'htmlLimitedBots' -g 'next.config.*' "${X[@]}" "${ROOTS[@]}" | sed 's/^/8d /'
# 9a generic anchor text; 9b fragment (hash) routing — Google does not crawl #/ views; click navigation on a non-link is routing-scan 1a (run it, credit §9).
rg -n -i --pcre2 "<(?:a|Link|NuxtLink|RouterLink|router-link|nuxt-link)\b(?:[^>{]|$B)*>\s*(?:click here|here|read more|more|learn more)\s*</(?:a|Link|NuxtLink|RouterLink|router-link|nuxt-link)>" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/9a /'
rg -n --pcre2 '\bcreateHashRouter\(|<HashRouter\b|\bcreateWebHashHistory\(|\buseHash\s*:\s*true|\bHashLocationStrategy\b|\bwithHashLocation\(|\bhashRouting\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/9b /'
rm -rf "$T"
```

A finding is a hit **plus** a read **plus** the route class **plus** the `seo-head.py` row. Three blind spots are structural:

- **Metadata is inherited and composed.** A page with no metadata of its own (1a) gets its layout's; a layout title on a dynamic route is the duplicate-title defect (1b only sees literals). Only the server HTML shows the composed result.
- **Modules generate tags no grep sees.** `@nuxtjs/seo`, `@nuxtjs/i18n`, `next-sitemap` and `@astrojs/sitemap` write canonical, hreflang, robots and sitemaps from config (6b). Read the config, then let the oracle show the output.
- **The server HTML depends on the user agent.** Next.js streams metadata into `<body>` for agents it does not list as HTML-limited. Run the oracle with `--ua=googlebot` and with `--ua=facebook`. An edge rule can do the same for any stack (0d): an ingress or proxy that rewrites social-crawler agents to a server-built preview means `3b og files: 0` is not "no social card" — judge §3 with `--ua=facebook` against the deployed edge only, and §1–§2 with `--ua=googlebot`, which the rule may not cover.

**Measured** (2026-10-05, the script above, under 1 s per tree):

| Tree | Hits that matter | Verdict |
|---|---|---|
| seeded scratch fixture (Next 16 app dir, Nuxt 4, Vite React SPA, Angular 22 SPA; one positive and one decoy per grep) | 1a 2 · 1b 1 · 1c 1 · 2b 2 · 2c 1 · 3a 2 · 4b 1 · 4c 1 · 5a 3 · 5b 2 · 5c 2 · 6c 1 · 6d 1 · 7b 1 · 8a 1 · 8b 2 · 8c 1 · 9a 3 · 9b 2 | every positive caught; decoys not caught: `<title>{\`Product ${p.name}\`}</title>`, a canonical built from `route.path`, an anchor in a comment. 5a lists both the root-layout `index: false` (positive) and an admin `noindex` (correct): the route class decides. The first 6d printed no file name when one sitemap matched; it passes `-H` now |
| `benchmarks/fixtures/{slow-marketplace,vuln-fullstack,quality-mix}/web` | 0b router-table SPA ×2 (was 1a 13 · 3) · 0 (no route files) · 3b 0 · 8b 1 per app | Vite React SPAs with no head management and an empty `#root`: a §8 candidate on any public route, with the §1 rows waiting on it, `N/A (auth-gated)` on the seller and account pages. The other fixtures have no route files |
| a real NestJS + React monorepo (Vite SPA, React Router 7.18, `<div id="root">` shell), re-measured 2026-10-15 | 0b 269 "route files" → router-table lane · 1a 269 → 0 · 2a 5 → 0 · 0d 2 · 8b 1 | 0b had counted feature-sliced `features/*/pages` view folders as routes (81 of the 269 were `*.test.tsx`, 0 dynamic against the router's 10); the route list now comes from routing-scan 0b and 1a waits on §8. 15 files set the head from script (`document.title =`, the project's `useBrandedHead`) — none reaches the server HTML. 2a's five hits were a payment-method form field named `canonical`; 2a now requires a `rel`, an `alternates` block or an SEO component. 0d: an ingress `if ($http_user_agent ~* "(facebookexternalhit|Twitterbot|…)")` rewrite to a server-built link preview — the reason `3b og files: 0` is not "no social card" |
| real Nuxt 4 storefront (`@nuxtjs/seo`, sitemap, robots modules) | 0b 19 routes · 1a 1 · 6b 4 · 3b 7 og files | 1a is the home page, which delegates to a theme component: read the wrapper, then the oracle. The first 0b counted 81 `components/pages/*.vue` files as routes and the first 0c took `useHeader*` composables for SEO wrappers; both are excluded now |
| real Nuxt 4 marketing site (sitemap and robots modules, `useMarketingSeo`) | 0c 1 wrapper · 1a 0 · 5a 1 · 6b 4 | 5a: `x-robots-tag: noindex` on `/auth/**` route rules — correct for an auth surface, refuted on read |
| real Nuxt 3 multi-theme store (`useSEO`, `useI18nSEO`) | 1a 4 · 4c 2 · 5a 5 · 5b 1 · 7a 2 · 8b 1 | 5b: `public/robots.txt` disallows `/_nuxt/`, the folder of every script and stylesheet the pages render with — a §6 finding. 4c: a `WebSite` + `SearchAction` and a `FAQPage` generator, both for rich results Google no longer shows — Hardening. 8b: a stray `index.html` that Nuxt never serves, refuted. 1a: the home page and a policy page inherit the default head (oracle) |
| real Angular 16 marketing landing (built `dist/` present) | 8b 1 · `seo-head.py --html` on both built `index.html` files: `csr-shell` (0 visible characters), `desc-missing`, `canonical-missing`, `og-missing`, `h1-count 0` | a public landing page served as a client-rendered shell: one §8 finding, with the §1–§3 rows waiting on it |
| real Angular 19 admin template | 8b 1 · 9a 0 | an auth-gated app: `N/A (auth-gated)`. The first 9a matched `Link` as anchor text in a UI-kit demo; `link` and `details` are no longer in the list |

Small fixtures prove the greps parse and catch seeded rows; precision at scale comes from the real-app rows.

## The 3,000-hit path

1. **Intersect** with the route table (0b) and its class: auth-gated and not-a-document routes leave the run with one read.
2. **Group** by (layout or SEO wrapper, class). A layout that sets one title for 200 posts, or a wrapper that builds the canonical from the live URL, is one group; fixing it closes every route under it.
3. **Rank** by search entry: the home page, then category and product templates, articles, then everything else. Use Search Console or analytics landing pages when present.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** Feed the sitemap's URLs (or one URL per route template) to `seo-head.py --base=… --routes=…`. Duplicate titles and descriptions, missing canonicals and broken hreflang sets fall out of one run across every template.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity is the search consequence on a route of the class that runs it. Raise one step on the home page and on templates that cover many URLs (product, article, category); drop one step on a route with no search entry today.

| § | Class | Default |
|---|---|---|
| 1 | Title or description missing, duplicated across routes, or not a single string | high when one title covers a whole dynamic route; medium for one route; low for a length band |
| 2 | Canonical missing, relative, outside `<head>`, carrying tracking parameters, or pointing at another page by mistake | high when it consolidates a rankable page into another; medium otherwise |
| 3 | Open Graph or Twitter card core missing, or a relative image URL | medium on shareable routes; low elsewhere |
| 4 | JSON-LD that does not parse, mismatches the page type, or describes content not on the page; markup kept for a rich result Google no longer shows | high for content not on the page (spam policy); medium for a parse error; Hardening for a retired rich result |
| 5 | Indexable route blocked: `noindex`, `X-Robots-Tag`, robots meta changed by script, non-200; or a must-not-rank route left indexable | critical when it covers the site (root layout, `Disallow: /`); high for one indexable template |
| 6 | Sitemap or robots.txt missing or wrong: render assets disallowed, no `Sitemap:` line, relative `<loc>`, listed URLs that answer non-200 or `noindex` | high when render assets are blocked; medium for listed URLs that fail; low for a missing `Sitemap:` line |
| 7 | hreflang set ignored: code not ISO 639-1 (+ ISO 3166-1 alpha-2), relative URL, not reciprocal, page missing from its own set; no `x-default` | medium (Google ignores the set); low for a missing `x-default` |
| 8 | Content only rendered on the client (an empty server body) on a route that must rank | high; critical for the home page |
| 9 | Views that cannot be discovered: hash (`#/`) routing, navigation with no `href`; generic anchor text; not one `<h1>` | high for hash routing on an indexable app; low for anchor text and `<h1>` |

### 1. Title and description

```
BAD:   app/blog/[slug]/page.tsx with no generateMetadata (every post carries the layout's "Acme Blog")
       <title>Results page {page}</title>          (React: two children — not one string)
GOOD:  generateMetadata → { title: post.title, description: post.excerpt } · <title>{`Results page ${page}`}</title>
```
**Read the code:** Which layout or wrapper supplies the title for this route (1a, 0c)? Is the duplicate (1b) on two indexable routes, or on a layout and the one page that overrides it? Does the page render more than one `<title>`? **Finding when** an indexable route ships no title or description, or shares one with another indexable route, in the server HTML. **Proof:** `seo-head.py` rows `title-missing`, `title-multiple`, `title-dup`, `desc-missing`, `desc-dup` across the route set.

### 2. Canonical

```
BAD:   useHead({ link: [{ rel: 'canonical', href: useRequestURL().href }] })    (keeps ?utm_source=… and every filter)
       <link rel="canonical" href="/about">                                      (relative; no metadataBase)
GOOD:  alternates: { canonical: `/products/${id}` } with metadataBase set · href: siteUrl + route.path
```
**Read the code:** Is the relative canonical resolved by the framework (Next with `metadataBase`, `@nuxtjs/seo` with a site URL)? Does the canonical include the query (2c)? Is a canonical that points elsewhere (`canonical-elsewhere`) intended, such as a print view pointing at its article? Google accepts `rel="canonical"` only in `<head>`, recommends absolute URLs and a self-referencing canonical, and says not to give one page different canonicals by different methods (Google Search Central, *How to specify a canonical URL*, updated 2026-07-10). **Finding when** the server HTML of an indexable route has no canonical, more than one, a relative one, one in `<body>`, or one carrying tracking parameters. **Proof:** `seo-head.py` rows `canonical-*`.

### 3. Social cards

**Read the code:** Is the route shared (articles, products, the home page)? Does the layout's default image apply? Is `og:image` absolute in the server HTML (Next resolves relative URLs against `metadataBase`; a client-only tag in an SPA reaches no scraper)? **Finding when** a shareable route lacks `og:title` or `og:image`, has a relative `og:image`, or has no `twitter:card`. **Proof:** `seo-head.py --ua=facebook` rows `og-missing`, `og-image-relative`, `twitter-card-missing`.

### 4. Structured data

```
BAD:   { "@type": "Product", "aggregateRating": { "ratingValue": 4.8 } }  on a page that shows no rating
       { "@type": "FAQPage", … } added to win an FAQ rich result
GOOD:  Product + Offer built from the same data the page renders; BreadcrumbList from the breadcrumb it shows
```
**Read the code:** Does the type match the page? Does every property describe something visible on the page? Does the feature's Google documentation page (read at audit time) list a property the block lacks? Google's search gallery (updated 2026-06-15, read 2026-10-05) lists 25 rich-result features. FAQ, How-to and the sitelinks search box (`SearchAction`) are not among them, nor are the types retired in June 2025 (Book actions, Course info, Claim review, Estimated salary, Learning video, Special announcement, Vehicle listing). In 2023 Google limited FAQ results to well-known government and health sites and said unused structured data causes no problems (Search Central blog, 2023-08-08). So 4c is Hardening (dead weight to keep), never a defect, and never something to propose. **Finding when** a block does not parse, or describes content the page does not show. **Proof:** `seo-head.py` row `jsonld-invalid` and the `jsonld_types` column; Google's Rich Results Test is a manual row (`manual-required`).

### 5. Indexable route blocked, or a private route left open

```
BAD:   app/layout.tsx  robots: { index: false }        (a staging leftover: the whole site is noindex)
       useEffect(() => meta.setAttribute('content', 'index'))   (Google may skip rendering a page whose first HTML says noindex)
GOOD:  noindex only in the private segments' own metadata, or by environment; an X-Robots-Tag route rule for /auth/**
```
**Read the code:** Is the `noindex` environment-gated (staging only)? Which routes inherit it? Does script add or remove it? Google says a `noindex` in the first HTML may stop rendering, so changing it from JavaScript may not work (*JavaScript SEO basics*, updated 2026-03-04). A `noindex` page must not also be disallowed in robots.txt, or the crawler never reads the `noindex`, and robots.txt alone does not keep a page out of the index (*Block indexing with noindex*, *Introduction to robots.txt*, both updated 2025-12-10). **Finding when** an indexable route's server response carries `noindex` (meta or header) or answers non-200, or a must-not-rank route that is server-rendered and reachable carries neither `noindex` nor an auth wall. **Proof:** `seo-head.py --expect-index=<indexable prefixes>` rows `noindex` and `status`.

### 6. Sitemap and robots.txt

**Read the code:** Is the sitemap generated from the dynamic routes (module or route), or a hand-written file that lists only static pages? Does robots.txt block the script and style folders the pages need (`/_next/`, `/_nuxt/`, `/assets/`)? Google says not to block resources whose absence makes a page harder to understand (*Introduction to robots.txt*). A sitemap holds at most 50,000 URLs or 50 MB uncompressed, uses absolute URLs, and its `<priority>` and `<changefreq>` are ignored (*Build and submit a sitemap*, updated 2026-07-08). **Finding when** robots.txt disallows the whole site or its render assets, the sitemap is missing or relative, or sampled sitemap URLs answer non-200 or `noindex`. **Proof:** `seo-head.py --robots --sitemap-sample=20`.

### 7. hreflang

```
BAD:   { code: 'en', language: 'en_US' } · hreflang="en-uk" · /ar lists itself and x-default, but not /en
GOOD:  language: 'en-US' · hreflang="en-GB" · every version lists every version, itself included, plus x-default
```
**Read the code:** Which module generates the set, and from which config field (7b reads it)? Does every localized URL list all versions and itself? Google: a language code in ISO 639-1, an optional region in ISO 3166-1 alpha-2, fully qualified URLs, each version listing itself and all others or the tags are ignored, `x-default` for unmatched languages (*Tell Google about localized versions*, updated 2026-09-21). **Finding when** the server HTML's set has an invalid code, a relative URL, a missing self link or is not reciprocal across the fetched locales. **Proof:** `seo-head.py` rows `hreflang-*`, run on one route in every locale.

### 8. Client-only content on a route that must rank

**Read the code:** Is the route server-rendered or prerendered (0a: `@angular/ssr`, `vike`, `vite-ssg`, prerender plugins; 8a: `ssr: false`, `RenderMode.Client`)? Does the Next page fetch its content in an effect (8c)? **Finding when** the server HTML of an indexable route carries under 200 visible characters of body text (`csr-shell`) while the rendered page shows its content. **Proof:** `seo-head.py` row `csr-shell`, beside the rendered text length from Playwright (§ Proof). The fix is a rendering change: `[halt-handoff]` to `ssr-audit` and the `rendering-strategy` pattern before any tag fix.

### 9. Discoverable views and link signals

**Read the code:** Does the app route with fragments (9b)? Google says to use the History API, not fragments, and finds links only in `<a>` elements with an `href` (*JavaScript SEO basics*). Is the generic anchor (9a) the only link to its target? **Finding when** an indexable app routes its views by `#/`, an indexable target is reachable only through a click handler (`routing-scan` §1, credited), or an indexable route has no `<h1>` or several. **Proof:** `seo-head.py` row `h1-count` and the `links` column; the `anchor-generic` candidates.

## Proof

`seo-head.py` (beside this file, installed as `.claude/skills/seo-audit/scripts/seo-head.py`) is the oracle. It is Python 3 standard library and read-only: GET requests only, no file written. Its oracle shapes and the class variants (§1–§9 → V180–V188) are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § SEO.

```bash
python3 .claude/skills/seo-audit/scripts/seo-head.py --self-test
python3 .claude/skills/seo-audit/scripts/seo-head.py --base=http://localhost:3000 --routes=/,/blog/a,/blog/b,/en/shoes,/ar/shoes --expect-index=/,/blog/,/en/,/ar/ --robots
python3 .claude/skills/seo-audit/scripts/seo-head.py --base=http://localhost:3000 --routes=/blog/a --ua=facebook
python3 .claude/skills/seo-audit/scripts/seo-head.py --html=dist/browser/index.html --expect-index='*'   # a static or prerendered build
```

Always fetch a **production** build: `next build && next start`, `nuxi build && node .output/server/index.mjs`, `vite build && vite preview` (plus the prerender output), `astro build && astro preview`, `ng build` with its SSR server or the built `index.html`. A dev server's HTML differs from what ships. **Rendered vs server text** (§8): `await page.goto(url, { waitUntil: 'networkidle' })` and `(await page.locator('body').innerText()).length`, set beside the oracle's `text` column. Google's Rich Results Test and Search Console URL Inspection (the rendered HTML Google stored) are manual rows (`manual-required`).

Every fix is accepted when the oracle row that proved the finding is gone **on the same route set**, the class variants pass (every route template, not the one example: list, detail, article, category; both user agents for §1 on Next; every locale for §7), and the owning grep goes quiet on the line. Never accepted: a client-side tag added to an SPA with no prerendering, a `noindex` removed by script, markup for content the page does not show, a second metadata mechanism beside the one in use.

## Output

```
seo-audit — lanes: nuxt 4.5.2 + @nuxtjs/seo 5.3.16 (sitemap 8.6.1, robots 6.2.4) · @nuxtjs/i18n · wrapper useSEO()
Context: 14 route files (5 dynamic) · classes: 6 indexable, 3 not-ranked, 4 auth-gated, 1 document · oracle: nuxi build + node .output, ua googlebot and facebook

Findings: 2 · Unconfirmed: 1 · Hardening: 2

1. public/robots.txt:7                                         [report-with-fix]   high
   §6 Disallow: /_nuxt/ — blocks every script and stylesheet the pages render with (6 indexable routes).
   Proof: seo-head.py --robots → robots-disallow-assets "Disallow: /_nuxt/".
   Fix: delete the line; keep Disallow: /admin/ and /api/.

2. composables/useSEO.ts:41 → pages/product/[slug].vue         [report-with-fix]   medium
   §1 description shared by every product — the wrapper falls back to the store description.
   Proof: seo-head.py on 5 product URLs → desc-dup ×5.
   Fix: useSEO({ description: product.summary }) in pages/product/[slug].vue, the wrapper's own field.

3. pages/politics/[id].vue                                     [report-flagged]    medium
   §1 no head of its own; inherits the default title. Unproven link: whether the layout derives the title from the route.
   Settling test: seo-head.py --routes=/politics/1,/politics/2 → title-dup.

Hardening: composables/useStructuredData.ts:93 SearchAction, :105 FAQPage — rich results Google no longer shows (§4).
Verification: 26 candidates → 2 findings · 1 unconfirmed · 2 hardening · 0 pre-existing · 21 refuted

Class coverage:
  §1 title / description      checked (4 route files without metadata + 0 shared literals → 1 finding, 1 unconfirmed)
  §2 canonical                checked (1 site → 0: siteUrl + route.path)
  §3 social cards             checked (4 og files; oracle on 6 indexable routes → 0)
  §4 structured data          checked (1 site, 2 types → 0 findings, 2 Hardening)
  §5 blocked / left open      checked (5 noindex sites → 0: error page and auth rules only)
  §6 sitemap / robots         checked (robots.txt + sitemap.xml → 1 finding)
  §7 hreflang                 checked (2 sites; oracle on /en and /ar → 0)
  §8 client-only content      checked (8b: index.html not served by Nuxt → refuted; oracle text ≥ 1,800 chars per route)
  §9 discoverability          checked (no hash routing; 0 generic anchors; one h1 per indexable route)
```

`[report-with-fix]`: the source line, the route class, the failing oracle row and a fix in the project's primitive are all present. `[report-flagged]`: one link is unproven (no build to fetch, a wrapper not read, a module's output unknown), and the row names it and the settling command. `[halt-handoff]`: §8, handed to `ssr-audit` / `rendering-strategy` before any tag fix. The coverage block lists **all nine** classes on every run: `checked (k hits → m findings)` only when the grep ran and the oracle fetched a production build; `N/A (<reason>)` only when no route of a class that runs it exists (§7 with one locale, every class on an auth-gated-only app); `blocked (<reason>)` when a grep failed or no build could be fetched. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/seo.md`](../../../../snippets/precedents/seo.md) (posting rules § 1–6, class precedents § 7–21, version facts § 22–29) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10 (the correctness column). The class precedents, in short:

- **§1** (seo § 7, 8): a title outside the 50–60 character band (guidance, not a limit); a duplicate between a layout and the one page that overrides it; a dynamic title the oracle shows unique.
- **§2** (seo § 9–12): a self-referencing canonical (expected); a relative canonical that Next resolves against `metadataBase`, or that an SEO module resolves against its site URL; a print or AMP view pointing at its article; trailing-slash, `www` and `http` variants (one canonical plus one redirect target, not four findings).
- **§4** (seo § 13, 14): FAQ, How-to and `SearchAction` markup left on the page (Hardening, not a defect); `Organization` on every page.
- **§5** (seo § 15–17): `noindex` on staging, auth, thank-you, error and filter-permutation routes; `Disallow` of `/api/` and `/admin/`; an `X-Robots-Tag: noindex` route rule for an auth segment.
- **§8** (seo § 18, 19): an auth-gated SPA (no route must rank); a stray `index.html` in a Nuxt or Next project, which the framework never serves.
- **§9** (seo § 20, 21): `navigate(-1)`; a card that also holds a real link for the same target.

## When to run

- On any diff that touches a public route's metadata, a layout head, an SEO wrapper, robots, a sitemap, locale routing, or the rendering mode.
- Before launching a public route; after a router, rendering-mode or i18n change; when Search Console reports "Duplicate without user-selected canonical", "Excluded by noindex" or "Crawled — currently not indexed".
- On every whole-repo `/frontend-audit`, reporting all nine classes.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under `/frontend-audit` that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the source `<file:line>`, the route and its class, the oracle row, and the fix in the project's own metadata primitive.
- Do not mark a finding `[report-with-fix]` without a `seo-head.py` row from a production build.
- Halt on a row with no route class. Do not grade an auth-gated route on its social tags.
- Halt when a fix adds a second metadata mechanism, asserts structured data the page does not show, or proposes FAQ, How-to or `SearchAction` markup for a rich result.
- Halt when the real defect is §8: hand it to `ssr-audit` / `rendering-strategy` before proposing a tag.
- Halt when a `noindex` or `Disallow` "fix" would remove a route the project means to rank.
- Do not print "SEO looks fine". Print the coverage block; a class whose grep or oracle did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `@technical-seo` (this pack) — judges and ranks these rows: indexation policy, the canonical choice, schema fit.
- `routing-scan` §1 and §4, `ssr-audit`, `streaming-ssr`, `i18n-scan`, `a11y-code-scan`, `a11y-scan`, `lcp-audit`, `lighthouse-ci`, `image-optimization` (this pack) — the neighbouring halves in § Boundaries.
- `xss-scan` (security pack, when installed) — JSON-LD written with `JSON.stringify` into a raw script.
- `ai/patterns/rendering-strategy.md`, `ai/patterns/i18n.md` (this pack) — where a route renders and how locales route.
- `.claude/rules/frontend-principles.md` — the SEO MUSTs this skill proves.

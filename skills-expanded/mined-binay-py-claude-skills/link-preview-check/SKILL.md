---
name: link-preview-check
description: Check how a URL looks when shared on WhatsApp, LinkedIn, X/Twitter, Facebook, Slack or iMessage — reads the raw HTML like their crawlers (no JavaScript), validates og:/twitter: tags and the og:image (absolute https, PNG/JPG not SVG, size, 1.91:1 ratio, weight), detects SPAs that serve the same title on every route, and writes an HTML page mocking each platform's card. Use when a shared link shows no image or the wrong title, before launching a site, or after adding Open Graph tags.
---

# link-preview-check

`scripts/preview-check.mjs` is zero-dependency Node 22+. It makes plain HTTP requests only, no browser.

```
node preview-check.mjs https://example.com
node preview-check.mjs https://example.com /about /pricing /blog/post-1    # several routes (catches SPA duplicates)
node preview-check.mjs --sitemap https://example.com/sitemap.xml            # up to 50 URLs (follows a sitemap index)
node preview-check.mjs https://example.com --out previews.html
```

It prints problems (✘) and warnings (!) per URL and exits 1 if there are problems. It also writes `link-preview.html` with approximate WhatsApp, LinkedIn, X and Facebook cards. Open it and look.
In Git Bash on Windows, MSYS rewrites `/about` into a file path; the script undoes that (a one-letter path like `/p` comes back as `/p/`). Full URLs or `MSYS_NO_PATHCONV=1` always work.

## Always check several routes
Pass the home page **and** 2–3 inner pages. The most common failure on modern sites: a single-page app ships one `index.html`, so every route has the homepage's title and image, and the real titles are set by JavaScript, which crawlers never run.

## Fix recipes
- **No og:image / weak card.** Add these to every page (absolute URLs):
  ```html
  <meta property="og:title" content="Page title">
  <meta property="og:description" content="One or two sentences.">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:image" content="https://example.com/og/page.jpg">
  <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  ```
  Image: 1200×630 JPG or PNG, ideally under 300 KB (WhatsApp drops heavy images), with key content away from the edges because some apps crop to a square. Generate cards with PIL or any image tool. SVG never works.
- **SPA with the same title everywhere.** Emit a static HTML copy per route at build time with that route's tags. For Vite: a plugin with `enforce: 'post'` whose `generateBundle` reads `bundle['index.html']`, swaps the meta block, and `this.emitFile`s `about.html`, `blog/post.html` and so on. Cloudflare Pages, Netlify and Vercel serve `about.html` at `/about`, and static files take precedence over the SPA fallback rewrite. Next.js, Nuxt, Astro and SvelteKit do this natively through their metadata/head APIs with SSR or SSG.
- **Relative og:image.** Make it absolute: `https://domain/og/x.jpg`.
- **`twitter:card` = summary.** Use `summary_large_image` for the big card.

## After fixing
Platforms cache previews. Ask the user to refresh them: LinkedIn Post Inspector (linkedin.com/post-inspector) and the Facebook Sharing Debugger (developers.facebook.com/tools/debug) both force a re-scrape. WhatsApp and X refresh on their own after a while, and a link with a new query string (`?v=2`) shows the new card right away.

---
name: follow-tool-takumi
description: Use Takumi to render OG images, social cards, and PDFs from JSX/CSS without a browser
argument-hint: "[scope]"
related:
  - improve
  - follow-create-web-nextjs
  - follow-create-web-nuxt
  - follow-tool-vite
  - use-agent-browser
---

## Goal

Use Takumi (`takumi-js`) to create Open Graph images, social cards, SVGs, animations, and PDFs from JSX, HTML, CSS, or Tailwind without a headless browser

## Scope

For JS/TS projects that need programmatic image generation — OG images, social cards, banners, charts, PDFs — on Node.js, Bun, Cloudflare Workers, Vercel Edge, Deno, or the browser

- Boundary: renders JSX/HTML → image bytes (PNG, JPEG, WebP, SVG) or PDF; it is not a browser screenshot tool — to capture a real web page → `/use-agent-browser` or `/use-agents-capture`
- `takumi-js` bundles both native (`@takumi-rs/core` on Node.js) and WASM (`@takumi-rs/wasm` on Workers/Edge/browser) — the runtime picks automatically
- Used in `/improve seo` for findings about `og:image`, `twitter:image`, social cards
- Latest: `takumi-js@2.14.0` (verified 2026-10-03)

## Execute

### 1. Install

> Goal: Install takumi-js

1. Install with `bun add takumi-js`
2. No need to pick native/wasm — `takumi-js` selects the right binding per runtime automatically
3. Rust projects can use the `takumi` crate instead

### 2. Render First Image

> Goal: render JSX → image bytes

1. Use `render` from `takumi-js` — takes JSX + `{ width, height }` and returns image bytes
2. Use `tw="..."` for Tailwind classes or `style={{}}` for inline CSS
3. The only built-in font is Geist (Latin, weights 300–800) — other scripts must be loaded via the `fonts` option
4. See all signatures in [API reference](references/apis.md)

### 3. Serve Over HTTP

> Goal: Return the image as an HTTP response

1. Use `ImageResponse` from `takumi-js/response` — extends the web `Response`, same API as `next/og`
2. Works in any framework route handler that supports `Request`/`Response`
3. Integrations have dedicated docs: Next.js, Nuxt (via Nuxt OG Image), SvelteKit, TanStack Start, Nitro, Astro, Fumapress

### 4. Load Fonts And Assets

> Goal: Correct text in every language with complete assets

1. Use `googleFonts` from `takumi-js/helpers` to load Google Fonts — supports weight ranges and variable axes
2. `fonts` accepts raw bytes, a descriptor, or a URL string
3. Rendering many images → register fonts once on a `Renderer` and reuse it
4. Images/emoji loading per the [docs](https://takumi.kane.tw/docs/load-images)

### 5. Advanced Output

> Goal: Use other output formats when needed

1. `renderSvg()` returns SVG instead of encoded bytes
2. Keyframe animations → WebP, APNG, GIF (CSS `@keyframes`, Tailwind `animate-*`)
3. PDF generation for invoices/reports — see the docs `/docs/pdf`
4. The `measure()` API measures layout before rendering

## Rules

### 1. No Browser

- Takumi renders without a headless browser — faster and lighter than a screenshot approach
- Supported CSS: grid, flexbox, gradients, custom fonts, keyframes — see the support matrix in the docs

### 2. Fonts

- It never reads system fonts — every font must come through the `fonts` option or the built-in Geist
- Missing a font → missing glyphs; Thai/Chinese/Japanese/Arabic always require loading a font

### 3. SEO Usage

- OG image spec: `1200×630` — `twitter:card` `summary_large_image`
- Make OG generation a deterministic route handler — cache output by content hash
- Migrating from Satori → keep the Flexbox styles; Takumi's bare `<div>` defaults to block layout

- Use /improve seo if needed
- Use /follow-create-web-nextjs if needed
- Use /follow-create-web-nuxt if needed
- Use /follow-tool-vite if needed

## References

- [API reference](references/apis.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `takumi-js` installed and rendering the first image
- `ImageResponse` serves OG images through a route handler
- Fonts/assets load correctly for every language used
- Ready for `/improve seo` fixes for `og:image`/`twitter:image`

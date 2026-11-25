---
name: astro
description: Astro conventions — routing and adding pages, islands architecture, client directives, content collections, .astro components. Use when working in an Astro project. 日本語の依頼例:「Astroで〜」「ページを追加/新規作成して」「ルーティング」「アイランド」「コンテンツコレクション」「.astroコンポーネント」。
---

# Astro

## Zero-JS by default

- Default to `.astro` components rendering static HTML. Ship JS only for genuinely interactive islands.
- Choose the cheapest `client:` directive that works: `client:visible` (below the fold) > `client:idle` (non-critical) > `client:load` (immediately needed). `client:only` is a last resort (no SSR, layout shift risk) — except for components that cannot render on the server, e.g. DOM-measuring charts (see `data-viz`).
- Before reaching for a React island, ask: can this be a `<details>`, CSS, or a few lines of vanilla JS in a `<script>` tag? Many "interactive" widgets need no framework.
- Share state between islands with nano stores, not prop drilling through the static layer.

## Components

- `.astro` for layout/static content; framework components (React) only inside islands that need them.
- Props typed via `interface Props` + `Astro.props` destructuring in `.astro` files; React island components follow `react-patterns` (`type Props`).
- Styles: `*.module.css` imports work in both `.astro` and React files; `.astro` scoped `<style>` is fine for purely local, single-file styling — pick one per component, don't mix. (This scoped-`<style>` allowance is the documented exception to the repo-wide CSS-Modules-only rule.)

## Content Collections

- All structured content (blog, docs, data) goes through content collections defined in `src/content.config.ts` with a Content Layer loader (`glob()` / `file()` from `astro/loaders`) and a zod schema — never loose globs of untyped markdown. (The legacy loader-less collection config was removed in Astro 5+.)
- The schema is the contract: required frontmatter fields, date coercion (`z.coerce.date()`), enums for categories. Build fails on bad content — that's the point.

## Data & rendering

- Fetch at build time in frontmatter for static pages. For per-request data, mark the page/route as server-rendered explicitly — know which mode each page is in.
- `import.meta.glob` results are build-time; don't treat them as dynamic. (`Astro.glob` no longer exists — removed in Astro 5+; use `import.meta.glob` or `getCollection`.)
- Use `astro:assets` (`<Image>`, `<Picture>`) for images — width/height required, prevents CLS.

## Security

- `set:html` is `dangerouslySetInnerHTML` — sanitize non-static input first (see `frontend-security` skill).
- Endpoints (`src/pages/api/`) follow the same validate/authenticate rules as any server endpoint.
- Public env vars need the `PUBLIC_` prefix; everything else is server-only — same discipline as Next.js.

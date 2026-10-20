---
name: follow-lib-shiki
description: Use the Shiki syntax highlighter — TextMate grammars, zero runtime, integrations, and transformers
argument-hint: "[scope]"
related:
  - improve
  - follow-lib-comark
  - follow-lib-markdown-it
  - follow-tool-vitepress
---

## Goal

Use Shiki as the project's syntax highlighter — the same TextMate grammars as VS Code, highlighting ahead of time (zero runtime JS), customizable via transformers and integrations

## Scope

For JS/TS projects that need to highlight code blocks in UI, docs, markdown, or an editor — every runtime (Node, Bun, browser, Cloudflare Workers)

- Boundary: Shiki does syntax highlighting only; the full markdown rendering pipeline → `/follow-lib-comark` or `/follow-lib-markdown-it`; a live editor → `@shikijs/monaco`
- Used in `/improve uxui` when findings concern code blocks/UI code readability
- Latest: `shiki@4.5.0` (verified 2026-10-03)

## Execute

### 1. Install And First Highlight

> Goal: get your first highlighted HTML

1. Install `bun add -D shiki`
2. Use the `codeToHtml` shorthand — loads themes/langs on-demand and caches for you:

   ```ts
   import { codeToHtml } from 'shiki'

   const html = await codeToHtml('const a = 1', { lang: 'javascript', theme: 'vitesse-dark' })
   ```

3. Intermediate outputs: `codeToTokens`, `codeToHast` for custom rendering
4. See the full API in [API reference](references/apis.md)

### 2. Long-Lived Highlighter

> Goal: highlight repeatedly and efficiently

1. Use `createHighlighter({ themes, langs })` once, keep it as a singleton — never create it in a hot path
2. Specify themes/langs explicitly — v1+ requires loading before use (`loadTheme`, `loadLanguage` can add more later)
3. For sync usage → after `createHighlighter`, call `codeToHtml` synchronously

### 3. Bundle Control

> Goal: control bundle size and runtime compatibility

1. Fine-grained imports: `shiki/core`, `@shikijs/langs/<lang>`, `@shikijs/themes/<theme>`
2. RegExp engines: `shiki/engine/oniguruma` (WASM, accurate) vs `shiki/engine/javascript` (pure JS, no WASM)
3. Cloudflare Workers doesn't support WASM init from binary — use the fine-grained bundle + `loadWasm(import('shiki/onig.wasm'))` or the JS engine
4. Use `@shikijs/codegen` to generate a bundle containing only what you use

### 4. Dual Themes And Transformers

> Goal: theme by light/dark and adjust the output

1. Use the `themes: { light, dark }` option → CSS variables (`--shiki-light`/`--shiki-dark`) switch via media/class without re-rendering
2. `@shikijs/transformers`: `transformerNotationDiff`, `transformerNotationHighlight`, `transformerNotationFocus`, `transformerNotationErrorLevel`, `transformerMetaHighlight`, `transformerCompactLineOptions`, `transformerRemoveLineBreak`
3. You can write your own transformers — hooks on `pre`/`code`/`line`/`span`/`post`

### 5. Integrations

> Goal: pick the integration per stack

1. Markdown pipelines: `@shikijs/markdown-it`, `markdown-exit`, `@shikijs/rehype` — or via the Comark plugin `comark/plugins/shiki` (see `/follow-lib-comark`)
2. Frameworks: `@shikijs/vitepress`, `@shikijs/nuxt`, `@shikijs/next`, `@shikijs/astro`
3. Editor/runtime: `@shikijs/monaco`, `@shikijs/twoslash` (TypeScript hover info), `@shikijs/magic-move` (animated transitions), `@shikijs/stream` (streaming highlight)
4. CLI for one-off file → html/svg: see [CLI reference](references/cli.md)

## Rules

### 1. Zero Runtime Preference

- Highlight ahead of time (build/SSR) — ship HTML, don't ship the highlighter to the client unless necessary (dynamic user input)
- Styles are inlined in the output — no extra CSS needed unless using dual themes/transformers

### 2. Explicit Loading

- Always specify themes/langs explicitly — never `Object.keys(bundledLanguages)` to load everything in production
- The highlighter is a long-lived singleton — reuse across renders

### 3. Engine Choice

- Default oniguruma (WASM) = accurate; the JS engine when WASM isn't available (some edge runtimes)
- Workers/Edge → check WASM constraints before choosing the engine

- Use /improve uxui if needed
- Use /follow-lib-comark if needed
- Use /follow-lib-markdown-it if needed
- Use /follow-tool-vitepress if needed

## References

- [API reference](references/apis.md)
- [CLI reference](references/cli.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `shiki` installed and able to highlight via both the async shorthand and a singleton highlighter
- Themes/langs loaded explicitly, bundle size controlled via fine-grained imports
- The right integration chosen per stack (markdown-it, rehype, VitePress, Nuxt, Next, Astro, Comark)
- Ready for `/improve uxui` fixes around code highlighting

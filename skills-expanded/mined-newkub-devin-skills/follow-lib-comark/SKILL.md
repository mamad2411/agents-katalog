---
name: follow-lib-comark
description: Use Comark to parse and render Markdown anywhere — HTML, ANSI, Vue, React, Svelte, Angular
argument-hint: "[scope]"
related:
  - improve
  - follow-lib-shiki
  - follow-lib-vue
  - follow-lib-react
  - follow-create-web-docs
  - follow-lib-dompurify
---

## Goal

Use Comark to parse CommonMark/GFM into a serializable `MarkdownDocument`, then render to HTML, ANSI, Vue, React, Svelte, Angular — with streaming, components, attributes, and plugins support

## Scope

For JS/TS projects that render Markdown content — docs sites, blogs, CMS content, AI chat streaming output, RSS/email/CLI output

- Boundary: Comark is the markdown parse+render pipeline; code-block syntax highlighting goes through the `comark/plugins/shiki` plugin (see `/follow-lib-shiki`) or `comark/plugins/rangi` (lightweight, no shiki); full docs site generation → `/follow-create-web-docs`
- Parse and render are separate — parse on the server/build side, serialize, then render in any framework
- Used in `/improve uxui` for findings about markdown content rendering, docs UX, streaming chat output
- Latest: `comark@0.7.0` (verified 2026-10-03)

## Execute

### 1. Install Renderer Package

> Goal: install per output target

1. Core parse: `bun add comark`
2. Pick the renderer per target: `@comark/html`, `@comark/ansi`, `@comark/vue`, `@comark/react`, `@comark/svelte`, `@comark/angular`, `@comark/nuxt`
3. See all packages/APIs in the [API reference](references/apis.md)

### 2. Parse And Render

> Goal: get a first markdown render working

1. String renderers — `renderHtml`/`renderAnsi` take a markdown string and return output:

   ```ts
   import { renderHtml } from '@comark/html'

   const html = await renderHtml('# Hello **World**')
   ```

2. Framework renderers — use that package's `Markdown` component (Vue must be inside `<Suspense>`; React uses `<Markdown>{content}</Markdown>`)
3. Manual pipeline — `parseMarkdown` from `comark` returns a `MarkdownDocument` you can inspect/transform/cache/serialize before rendering

### 3. Components, Attributes, Frontmatter

> Goal: use opt-in syntax for richer content

1. Components — `::alert{type="info"}` blocks and `:badge[text]` inline, with props/slots/nested markdown; register only the components you specify
2. Attributes — `**bold**{.highlight}`, `[link](url){.button target="_blank"}`, `![img](src){width="800"}`
3. Frontmatter — a leading YAML block parsed as metadata, bindable to component props
4. Plain CommonMark/GFM works with none of these enabled — all are opt-in

### 4. Plugins And Highlighting

> Goal: extend with plugins as needed

1. `comark/plugins/shiki` — syntax highlighting with multi-theme + on-demand languages (see `/follow-lib-shiki`)
   - `comark/plugins/rangi` — lightweight alternative (~13kB, sync, zero-dep) when highlighting is needed without shiki; `bun add rangi` (peer dep) then `plugins: [rangi({ theme: github })]` with themes from `rangi/themes`; the HTML renderer imports from `@comark/html/plugins/rangi`
2. Official plugins: mermaid diagrams, math, table of contents, json-render (declarative UI specs)
3. Write your own plugin per the plugin API; markdown-it plugins are compatible (Comark builds on markdown-exit)
4. See the plugin registry at https://comark.dev/plugins

### 5. Streaming Output

> Goal: render AI/chat streaming content correctly

1. The auto-closing parser completes unfinished syntax (bold, code fences, components) — every frame renders as complete markup
2. Framework renderers have a streaming prop — chunks arriving mid-token render immediately with a caret
3. Ideal for AI chat interfaces and live content feeds

## Rules

### 1. Serializable Document

- `MarkdownDocument` is serializable data — parse once, cache/serialize freely; not tied to a framework or build step
- Never embed executable framework code in content — components resolve only when registered

### 2. Renderer Choice

- Choose the renderer by the real output target — HTML string for SSG/RSS/email, ANSI for CLI, a framework component for apps
- The Vue `<Markdown>` must be inside `<Suspense>` — parsing is async internally

### 3. Trust Boundary

- Renderers use only registered components — content is data, not code; still sanitize HTML output when accepting untrusted content (see `/follow-lib-dompurify`)

- Use /improve uxui if needed
- Use /follow-lib-shiki if needed
- Use /follow-lib-vue if needed
- Use /follow-lib-react if needed
- Use /follow-create-web-docs if needed

## References

- [API reference](references/apis.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The Comark renderer is installed per target and renders the first markdown
- Components/attributes/frontmatter are used as opt-in when needed
- Plugins (shiki/rangi, mermaid, toc) are wired correctly
- Streaming output renders complete markup on every frame
- Ready for `/improve uxui` fixes on markdown/content UX

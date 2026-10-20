---
name: follow-lib-markdown-it
description: Use markdown-it + plugins — render markdown, syntax highlight with shiki
argument-hint: "[target-or-scope]"
related:
  - follow-lib-dompurify
  - run-verify
  - run-test

---

## Goal

Use markdown-it + plugins — render markdown, syntax highlight with shiki

## Scope

Use when the task involves markdown-it — parser/renderer, plugin ecosystem, CLI render (lib markdown it)

- Use this skill for the markdown-it pipeline (`parse` → tokens → `render`) — if you need a full markdown pipeline with AST/unist (remark/rehype) or framework integration (e.g. VitePress, Slidev) → use that framework's skill instead
- Sanitize rendered HTML from untrusted content → `/follow-lib-dompurify`
- Has a built-in CLI (`markdown-it <file>`) — see [cli](references/cli.md)

- Latest: `markdown-it@15.0.2` (verified 2026-09-13) — v15: ESM+CJS dual, types included in the package (no `@types/markdown-it` needed)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Install `bun add markdown-it` — v15 bundles types, no `@types/markdown-it` needed
1. Create an instance `new MarkdownIt()` or `markdown-it()` with the preset you want: `default` (extras), `commonmark` (strict spec), `zero` (minimal) — then `.use(plugin)`
1. Use `@shikijs/markdown-it` for code highlighting (async — setup must be awaited)
1. Customize render rules via `md.renderer.rules` when you need to change output; toggle rules with `md.enable`/`md.disable`
1. Sanitize output with DOMPurify when rendering user content — see `/follow-lib-dompurify`

### 2. Plugins And CLI

> Goal: use the plugin ecosystem and CLI correctly

1. Plugin ecosystem via `md.use(plugin, opts)` — e.g. `markdown-it-anchor`, `markdown-it-toc-done-right`, `markdown-it-footnote` (see the list at npm keyword `markdown-it-plugin`)
1. CLI for quick file render: `bunx markdown-it README.md` or stdin — options `--html`, `--linkify`, `--typographer` (see [cli](references/cli.md))
1. For token-level control → `md.parse(src, env)` returns the token stream before render

### 3. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib markdown it)

## Rules

- Turn off `html: true` when rendering untrusted content, or sanitize after render
- Preload the highlighter with the `@shikijs/markdown-it/async` pattern
- Cache rendered output for repeated content

- Use `/follow-lib-dompurify` if HTML output must be sanitized
- Use `/run-verify` if needed
- Use `/run-test` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib markdown it)
- No known security/performance pitfalls (lib markdown it)
- Lint, typecheck, tests pass

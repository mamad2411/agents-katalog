---
name: follow-lib-tanstack-markdown
description: Use TanStack Markdown end to end — document model, streaming-safe parsing, AI output, custom renderers
argument-hint: "[use-case]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Markdown fully — parse markdown → serializable document model → render: streaming-safe (partial docs from AI), transportable (JSON), custom node renderers

## Scope

Use when rendering markdown, especially **streaming AI output** (append-safe incremental parse) or docs transported as JSON — for plain static markdown, `marked`/`remark` suffice

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the markdown package

```bash
bun add @tanstack/markdown
```

### 2. Document Model

> Goal: markdown → serializable tree → UI

1. Parse a markdown string → a document tree of typed nodes (headings, paragraphs, lists, code, tables) — JSON-serializable
2. Render nodes → map node types to your own UI components (headless-style)
3. Transport: the model serializes via JSON — safe as an RSC/SSR payload
4. Check the latest export names at `https://tanstack.com/markdown/latest` — the new v1 API may refine

### 3. Streaming Pattern

> Goal: render AI chat output while streaming

1. Append a chunk → incremental parse — the model supports partial documents
2. Unclosed blocks (a code fence or table mid-section) render as a pending state without breaking layout
3. Pair with `follow-ai` — pipe `message.parts` into the renderer continuously

### 4. Custom Rendering

> Goal: render per the design system

1. Node-type map: `code` → `follow-highlight` syntax highlighting; `table` → a `follow-table` component
2. Sanitize: raw HTML nodes must be sanitized before rendering (trust boundary)
3. Link handling: intercept `link` nodes → `follow-router` `<Link>` (SPA nav without a reload)

### 5. Verify

> Goal: prove markdown renders correctly, including streaming input, before finishing

1. `/run-typecheck` + `/run-test`
2. Edge cases: an unclosed fence mid-stream, nested lists, tables, inline code in a heading
3. On failure → `/resolve-errors` max 3 rounds

## Rules

- The model = data only — never embed components/functions in nodes (serialization breaks)
- Raw HTML → always sanitize — the app's XSS boundary
- Streaming must handle incomplete blocks — test partial states
- Pick the right lib: stream/serialize → TanStack Markdown; static render → `marked`, lighter

## Expected Outcome

- Markdown parses → a doc model that can be transported
- Streaming renders without flicker/errors
- Custom renderers fit the design system

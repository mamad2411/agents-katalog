---
name: follow-lib-tanstack-highlight
description: Use TanStack Highlight end to end — syntax highlighting, themes, languages, SSR with markdown integration
argument-hint: "[language-scope]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Highlight fully — a syntax highlighter that produces compact themeable HTML tokens: languages, theming via CSS, SSR/precompute, integration with markdown/doc tools

## Scope

Use when you need syntax highlighting — code blocks, docs, diff viewers, markdown fences (`follow-markdown`) — v1 is new: check `https://tanstack.com/highlight/latest` before implementing

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the highlighter and its theme/language deps

```bash
bun add @tanstack/highlight
```

### 2. Highlight To Tokens

> Goal: source → themed HTML/token output

1. Highlight a source string with a language param → the output is a token stream/HTML with semantic classes
2. The output structure is compact — tokens split by type (keyword, string, comment, number, fn, etc.)
3. Check the latest export/API names in the docs — the new v1 package API may refine

### 3. Theme And Render

> Goal: colors matching the design system + safe rendering

1. Theme via CSS classes/custom properties — map token classes → design tokens (e.g. UnoCSS semantic colors)
2. Render: the highlighter output is escaped HTML — `dangerouslySetInnerHTML` works but always verify escaping first (XSS boundary)
3. Dark mode: theme classes should switch with `.dark` — bind to the app's theme system

### 4. Patterns

> Goal: real usage

1. **SSR/precompute**: static content → highlight at build/server time to cut client work + bundle
2. **Markdown fences**: hook `code` nodes from the `follow-markdown` doc model
3. **Line features**: line numbers/diff highlights via wrapper markup over the token output
4. **Language scope**: register/lazy-load only the languages actually used — bundle size

### 5. Verify

> Goal: prove highlighted output renders before finishing

1. `/run-typecheck` + `/run-test`
2. The languages the project really uses — token coverage + theme colors in both light/dark
3. On failure → `/resolve-errors` max 3 rounds

## Rules

- Theme via CSS — no inline color config in highlighter options
- SSR/precompute static content — client highlighting only for dynamic
- Verify escaped output before `dangerouslySetInnerHTML`
- Lazy-load grammars for what's used — don't bundle every language
- Use `/follow-lib-tanstack-ecosystem` for library selection

## Expected Outcome

- Code blocks highlighted, themeable in both light/dark
- Integration with markdown/docs works
- Light bundle — only the languages used

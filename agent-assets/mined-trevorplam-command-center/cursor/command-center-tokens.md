---
description: Design tokens and Style Dictionary v4 patterns
globs:
  - "packages/design-tokens/**"
alwaysApply: false
---

# Design Tokens (Style Dictionary v4)

## W3C DTCG format
- All token source files use DTCG format: $type and $value (and optional $description)
- Raw values in primitive tokens; semantic and component tokens reference via {token.path} syntax
- Set usesDtcg: true in config; DTCG format is auto-detected

## Three-tier hierarchy (non-negotiable)
1. **Primitives** — raw values (color, spacing) in tokens/primitive/*.json; output in :root {} only; NO utility classes
2. **Semantic** — aliases referencing primitives in tokens/semantic/*.json; output in @theme inline {} for cascade-overridable utilities
3. **Component** — component-level tokens referencing semantic in tokens/component/*.json; output in :root {}

Never put primitives in @theme {} — it generates redundant utilities for every scale step.

## Style Dictionary v4 requirements
- ESM-only: "type": "module" in package.json; all build methods are async
- Use await sd.hasInitialized (or equivalent) before accessing tokens — async API requirement
- Reference utilities live in 'style-dictionary/utils' (not top-level)
- Custom formats (e.g. css/tw-v4-theme) for @theme inline {} and :root {} outputs

## Semantic platform — outputReferencesTransformed
- Semantic platform MUST use outputReferencesTransformed (from style-dictionary/utils) so references become var(--token-name) in output
- Preserving the var() chain is required for dark mode cascade overrides; resolving to raw values at build time breaks dark mode

## Five v3→v4 blockers (avoid in token pipeline)
1. Missing @source in consuming apps — tokens compile to CSS; apps must @source shared UI
2. Using .js for PostCSS — use .mjs
3. Legacy @tailwind directives in app CSS — use @import "tailwindcss"
4. Missing tw-animate-css in app globals — not in token package but required by apps that use tokens
5. Using theme() in CSS — use var(--token-name) only

## Client tokens
- Per-client files: tokens/clients/[slug].json; compiled to **either** apps/prospective-clients/[slug]/tokens/[slug].css **or** apps/clients/[slug]/tokens/[slug].css depending on where the app lives (see packages/design-tokens/scripts/build-clients.ts).
- Build: pnpm tokens:build (runs from design-tokens package; see scripts/build-clients.ts and sd.config.ts)

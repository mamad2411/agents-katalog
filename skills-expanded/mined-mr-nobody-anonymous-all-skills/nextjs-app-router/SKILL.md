---
name: nextjs-app-router
description: "Build Next.js App Router applications correctly: server versus client components, streaming and Suspense, route handlers, caching and revalidation, and metadata."
type: procedural
category: web
domain: web
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - nextjs app router
  - server component vs client component
  - nextjs caching revalidate
  - route handler nextjs
  - nextjs streaming suspense
aliases:
  - nextjs
keywords:
  - nextjs
  - app-router
  - rsc
  - server-components
  - streaming
  - revalidate
mcp_servers:
  - context7
  - filesystem
source: custom
enabled: true
---

# Next.js App Router

## Purpose

Build Next.js App Router applications correctly: server versus client components, streaming and Suspense, route handlers, caching and revalidation, and metadata.

## When to Use

- A Next.js application must be structured around the App Router rather than Pages.
- Data fetching or caching behaves unexpectedly between builds and requests.
- A component fails because it needs hooks or browser APIs but runs on the server.

## When NOT to Use

- The project is on the Pages Router and staying there.
- The task is a static marketing page with no data layer.
- The framework is Remix, Astro or SvelteKit.

## Capabilities

- Split the tree into server and client components deliberately.
- Stream slow subtrees with Suspense instead of blocking the shell.
- Choose the right cache mode (`force-cache`, `no-store`, `revalidate`) per fetch.
- Write route handlers and server actions with correct validation and auth.
- Keep metadata, error and loading boundaries per segment.

## Inputs

- The route structure and which segments need auth or dynamic data.
- Data sources and their acceptable staleness.
- The deployment target, since caching semantics differ per host.

## Workflow

1. Sketch the route tree with `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx` per segment.
2. Default every component to server; add `'use client'` only where state, effects or DOM APIs are needed.
3. Wrap slow data in Suspense with a meaningful fallback rather than a spinner for the whole page.
4. Declare fetch caching explicitly; never rely on the default that changed between versions.
5. Validate all input at the route handler or server action boundary with a schema.
6. Verify in `next build` output that no route accidentally became fully dynamic.

## Tools

- next
- typescript
- playwright
- context7

## Examples

- `A product page that streams reviews while the price renders immediately turns a 1.8 s blank shell into a 200 ms first paint.`
- ``export const revalidate = 60` on a segment beats per-fetch tuning when the whole page shares one freshness budget.`

## Safety

- Never pass secrets to client components; anything imported there ships to the browser.
- Server actions are public endpoints — authenticate and validate inside them.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `context7` | stdio | standard | low | `CONTEXT7_API_KEY` |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/web/nextjs-app-router`). First-party skill, maintained in this repository.

## Notes

- Check the version you are on before following any caching advice; the defaults changed in 15.
- Review the build output: a stray `cookies()` call turns a static route dynamic.
- Pairs with: `react-performance`, `typescript-advanced`.

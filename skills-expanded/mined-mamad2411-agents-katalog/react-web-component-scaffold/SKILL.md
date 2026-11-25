---
name: "react-web-component-scaffold"
description: "Translate tsa.design_source into React web pages/components: theme tokens, layouts, presentational components, API hooks, routing wiring. Next.js App Router primary; Vite + React Router fallback. Use when scaffolding a React web UI from a TSA (with or without Figma)."
version: 1
created: "2026-07-10"
updated: "2026-07-10"
---

# React Web Component Scaffold (TSA → React / Next.js)

**Input:** `tsa.design_source` (screens[], components[], navigation_graph, design_tokens) + optional design mockups (SVG/figma_screens.json) + `stack-profile.json`. Framework from TSA/`stack-profile` — Next.js App Router (default) or Vite + React Router.

## Procedure

### 1. Theme / tokens
Generate the design-token layer from `design_tokens`. Next.js: `styles/globals.css` with CSS custom properties (e.g. `--sh-*`) + CSS Modules. Vite: `src/styles/` tokens + chosen styling system. All visual values flow through tokens — no hardcoded hex/px in components.

### 2. Shared + design-system components
For each `design_source.components[]` entry, scaffold typed, presentational components at its declared `path`.
- Figma/auto-layout → CSS fl*ex*/grid (`display:flex`, `gap`, `justify-content`, `align-items`).
- Text → semantic elements (`h1..h6`, `p`, `label`) with typography tokens.
- Atoms first (chips, badges, IDs, indicators) → feature components → page organisms.
- Every interactive element: accessible name, keyboard support, visible focus.

### 3. Screens / routes
For **each** `design_source.screens[]` entry (all in-scope stories — no deferrals, no empty stubs):
- **Next.js App Router:** route file `app/<segment>/page.tsx` (from `screen.route`/`file`); shared shell in `app/layout.tsx`. Interactive screens are Client Components (`'use client'`).
- **Vite + React Router:** `src/pages/<Screen>.tsx` registered in the router; lazy-load with `React.lazy`/`Suspense`.
- Layout from `component_tree`; when a design mockup (SVG/figma) is provided, match its layout, spacing, and component placement.
- Render every state: loading / empty / error / loaded (never blank; never `return null` for a state).

### 4. Routing wiring
- Build routes from `design_source.screens[].route`.
- Each `navigation_graph` edge → `router.push`/`replace` (Next: `next/navigation`; Vite: `react-router-dom`) on the matching trigger/CTA label. Modal/overlay states per TSA.
- Maintain a screen registry (story ID → component → route) for traceability and tests.

### 5. Data binding
Per `api_integration.screen_bindings`: one typed React Query hook per operation in `lib/hooks/` (Next) or `src/hooks/`; screens/components never call axios/fetch directly. Types mirror the OpenAPI/`api_integration` entities.

## Batch implementation (agentic workflow)
When a task plan/manifest defines batches: implement only the current batch's story IDs; register their routes before marking complete; never stub unassigned screens with an empty element.

## Fidelity rules
- Do not invent or drop screens; screen count matches the in-scope TSA.
- No hardcoded colors/spacing outside the token layer.
- Honor `fidelity_directives` and per-screen acceptance criteria.
- Compile-clean TypeScript (strict); paired component test per screen.

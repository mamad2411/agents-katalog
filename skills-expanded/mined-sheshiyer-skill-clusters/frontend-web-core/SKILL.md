---
name: frontend-web-core
description: "Shared reference for the frontend-web cluster: the rendering-model decision (CSR / SSR / RSC / static) that sets the hydration boundary, plus the conventions every spoke shares — the SSR/'use client' contract, the motion-foundations layering rule, the accessibility baseline, and the framework/tooling matrix. USE WHEN choosing a framework, wiring SSR-sensitive or motion code, or planning accessibility — the interlocking rules every frontend-web spoke depends on."
cluster: frontend-web
version: 1.0.0
---

# Frontend Web Core

Shared model for the `frontend-web` cluster. The framework, motion, a11y, and tooling spokes
all depend on these interlocking conventions — keep them consistent here so no spoke
contradicts another.

## 1. The rendering model (this cluster's defining decision)

Every web UI is one of four rendering models, and the choice fixes the **hydration boundary** —
where server-rendered HTML hands off to client JavaScript. Get this wrong and you get hydration
mismatches, layout shift, and dead interactivity.

```
Static (SSG) ──► SSR ──► RSC (server components) ──► CSR (client only)
   most cacheable  ◄──────────  most interactive  ──────────►
```

- **Static / SSG** — HTML built at build time. Cheapest, most cacheable. No per-request data.
- **SSR** — HTML rendered per request, then hydrated on the client. → `nuxt4-patterns` (`useFetch`/`useAsyncData`), Next.js pages.
- **RSC** — React Server Components render on the server and ship zero JS; interactivity is opted into with `"use client"`. → `react-patterns` (server/client boundary), `nextjs-turbopack`.
- **CSR** — everything runs in the browser. Simplest mental model; worst first paint. → SPA-style React/Vue/Angular.

**Rule:** decide the model **first**. It dictates how you fetch data (server vs client), where
state can live, whether a component may use browser APIs, and how motion mounts. Default to the
**most static model that still meets the interactivity requirement** — push work to build time or
the server before reaching for client JS.

## 2. The SSR / `"use client"` contract

The server and the first client render **must produce identical markup**. Violations are the #1
source of frontend bugs in this cluster.

- Mark any component using state, effects, browser APIs, or motion as a client component (`"use client"` in Next.js App Router; `<ClientOnly>`/`import.meta.client` in Nuxt). → `react-patterns`, `nuxt4-patterns`
- Always set an explicit `initial` state on animated elements — never an implicit origin. → `motion-foundations`
- Never read `window`/`navigator`/`localStorage` during render; gate them behind an effect or a client check.
- Match data between server and client renders; hydrate from the same payload. → `react-performance` (avoid client-side refetch waterfalls)

## 3. Motion layering rule

Motion is **layered, not flat**. Tokens and springs are defined **once** in `motion-foundations`;
every pattern imports them — no inline durations or eases.

```
motion-foundations (tokens · springs · perf rules · reduced-motion · SSR safety)
        │
        ├─► motion-patterns   (button · modal · toast · stagger · page transitions · scroll)
        └─► motion-advanced   (drag · gestures · SVG · text · useAnimate sequences)
```

- Animate **only `transform` and `opacity`**; never `width`/`height`/`top`/`left` (layout thrash).
- Honor `prefers-reduced-motion` everywhere (`useReducedMotion` + the CSS media query).
- **Never mix `motion/react` and `framer-motion`** in one project — conflicting schedulers break `AnimatePresence`.
- Set `AnimatePresence mode` explicitly (`"wait"` for modals/toasts/page transitions, `"popLayout"` for lists).

## 4. Accessibility baseline (non-negotiable)

Two altitudes, both required:

- **Standard** → `accessibility`: WCAG 2.2 AA — POUR principles, ≥24×24px target size (SC 2.5.8), visible focus (SC 2.4.11), 4.5:1 text contrast, 400% reflow. The spec states cross-platform principles; in this cluster apply them to **browser UI (DOM/ARIA)** only — for native mobile a11y use the `react-native` / `expo` / `mobile-flutter` clusters.
- **Implementation** → `frontend-a11y`: semantic HTML before ARIA, `htmlFor`/`id` label pairing, `aria-*` only when native semantics fall short, keyboard navigation, focus management/restore.

Rule: semantic element first; every interactive control keyboard-reachable; every state change announced.

## 5. Framework / tooling matrix

| Concern | React / Next | Vue / Nuxt | Angular |
|---|---|---|---|
| Components & state | `react-patterns` | `ui-to-vue` (from designs) | `angular-developer` |
| SSR / data fetching | `react-patterns` (RSC), `nextjs-turbopack` | `nuxt4-patterns` (`useFetch`) | `angular-developer` (SSR) |
| Performance | `react-performance` | `nuxt4-patterns` (route rules, lazy) | `angular-developer` (signals) |
| Testing | `react-testing` | — | `angular-developer` (refs) |
| Bundler | `nextjs-turbopack`, `vite-patterns` | `vite-patterns` | Angular CLI |
| Runtime / PM | `bun-runtime` | `bun-runtime` | `bun-runtime` |

Cross-cutting (framework-agnostic): `motion-foundations`/`patterns`/`advanced`, `accessibility`,
`frontend-a11y`, `design-system`, `make-interfaces-feel-better`, `frontend-design-direction`,
`frontend-slides`.

## 6. Version / conventions

- **React** 18/19 (hooks + Server Components); **Next.js** 16+ on **Turbopack**; **Nuxt** 4; **Angular** with signals/`resource`.
- **Vite** for non-Next bundling and library mode; **Turbopack** for Next dev; **Bun** as the fast runtime/PM/test alternative to Node.
- **Motion** via the `motion` package (`motion/react`); `framer-motion` is the legacy import path only.
- TypeScript throughout; `additionalProperties` in skill frontmatter is fine, but `version` must be valid semver.

## 7. Shared guardrails

- Decide the **rendering model first**; default to the most static option that meets the need.
- Respect the **SSR boundary**: `"use client"` for stateful/motion code, identical server/client initial markup, no browser APIs during render.
- **Layer motion** on `motion-foundations`; animate transform/opacity only; honor reduced motion; one motion package per project.
- **Accessibility is baseline**: semantic HTML, keyboard reachability, WCAG 2.2 AA target sizes and focus.
- Pick **one framework per surface**; don't blend React and Vue idioms.
- State every regression-prone change (a new client boundary, a layout-animating property, a dropped label) explicitly.

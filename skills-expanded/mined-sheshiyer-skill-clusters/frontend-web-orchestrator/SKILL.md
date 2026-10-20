---
name: frontend-web-orchestrator
description: "Route a web-UI task to the right skill among 18 frontend specialists — framework choice (React/Next, Vue/Nuxt, Angular), build tooling (Vite, Turbopack, Bun), motion, accessibility, design direction, and component conversion. USE WHEN building, reviewing, or shipping a web interface but the specific framework or concern hasn't been named yet."
cluster: frontend-web
version: 1.0.0
---

# Frontend Web Orchestrator

The single entry skill for browser-UI work. It locates the task on the
**framework × concern** map and delegates to one of 18 specialist spokes. The cross-cutting
model every web UI shares — the rendering/runtime choice that cascades into hydration, data
fetching, motion bindings, and accessibility — lives in `frontend-web-core`; read it before
picking a framework or wiring SSR-sensitive code.

## Cluster map (spoke → role)

**Framework core**
- `react-patterns` — React 18/19 hooks discipline, server/client boundaries, Suspense, form actions, composition
- `react-performance` — the Vercel-derived 70-rule performance ruleset (waterfalls → re-render → micro-perf)
- `react-testing` — React Testing Library + Vitest/Jest + MSW + axe; the component-vs-e2e boundary
- `nextjs-turbopack` — Next.js 16+ with Turbopack: incremental bundling, FS caching, Turbopack-vs-webpack
- `nuxt4-patterns` — Nuxt 4 hydration safety, route rules, lazy loading, SSR-safe `useFetch`/`useAsyncData`
- `angular-developer` — Angular signals/resource, forms, DI, routing, SSR, plus a 34-file reference set
- `ui-to-vue` — batch-convert UI screenshots/exports into Vue 3 (Vant, Element Plus, Ant Design Vue)

**Build & runtime**
- `vite-patterns` — Vite config, plugins, HMR, env, proxy, SSR, library mode, dependency pre-bundling
- `bun-runtime` — Bun as runtime / package manager / bundler / test runner; when to pick Bun over Node

**Motion (layered — foundations first)**
- `motion-foundations` — motion tokens, spring presets, perf rules, device adaptation, reduced-motion, SSR safety. Every other motion skill depends on this.
- `motion-patterns` — production UI patterns (button, modal, toast, stagger, page transitions, scroll) built on the foundation
- `motion-advanced` — drag/gestures, text animation, SVG path drawing, `useAnimate` sequences, the full API decision tree

**Look & feel**
- `accessibility` — WCAG 2.2 AA: POUR, semantic ARIA, target size, focus appearance, Web + iOS/Android. The spec/audit authority.
- `frontend-a11y` — the React/Next implementation of a11y: labels, ARIA, keyboard nav, focus management
- `design-system` — generate or audit design systems, token/visual consistency, review styling PRs
- `make-interfaces-feel-better` — concrete design-engineering polish: spacing, type, borders, shadows, hit areas, states
- `frontend-design-direction` — set a product-appropriate visual direction before implementation
- `frontend-slides` — animation-rich HTML presentations from scratch or converted from PPTX

## Routing rules by intent

- **"Build / review a React component"** → `react-patterns` (+ `frontend-a11y` for interactive elements, `react-testing` for coverage)
- **"It's slow / re-rendering / big bundle"** → `react-performance`; if Next.js dev speed → `nextjs-turbopack`
- **"Vue / Nuxt"** → `nuxt4-patterns`; converting designs to Vue components → `ui-to-vue`
- **"Angular"** → `angular-developer` (everything Angular routes here; it carries its own reference set)
- **"Add an animation / transition"** → `motion-foundations` FIRST, then `motion-patterns`; gestures/SVG/imperative → `motion-advanced`
- **"Make it accessible"** → `accessibility` for the WCAG standard (browser DOM/ARIA), `frontend-a11y` for the React implementation
- **"Make it look better / more polished / on-brand"** → `make-interfaces-feel-better` + `frontend-design-direction` + `design-system`
- **"Bundler / dev server / monorepo tooling"** → `vite-patterns` or `nextjs-turbopack`; runtime/package-manager → `bun-runtime`
- **"Build a deck / slides"** → `frontend-slides`

## Standard flow

1. **Pick the rendering model** — which framework, and CSR / SSR / RSC? This is the decision in `frontend-web-core` that everything else inherits.
2. **Route to the framework spoke** for structure (`react-patterns` / `nuxt4-patterns` / `angular-developer`).
3. **Layer cross-cutting concerns** in order: accessibility (`frontend-a11y` + `accessibility`) → motion (`motion-foundations` → `motion-patterns`/`motion-advanced`) → polish (`make-interfaces-feel-better`, `design-system`).
4. **Tooling & verification** — wire the bundler/runtime (`vite-patterns` / `nextjs-turbopack` / `bun-runtime`); verify with `react-testing`.
5. **Return**: chosen spoke(s), the rendering model implied (SSR/RSC sensitivity), the a11y + reduced-motion obligations, and the next action.

## Sibling clusters

This cluster is **browser UI only** (DOM, CSS, web frameworks). For **native mobile UI**, hand off — don't try to route React/Vue web idioms onto a device screen:

- **React Native screens / components** → `react-native` cluster
- **Expo / managed React Native apps** → `expo` cluster
- **Flutter / Dart UI** → `mobile-flutter` cluster

The `accessibility` spoke here is the WCAG **spec/audit** authority and states cross-platform principles, but implementation in this cluster is browser DOM/ARIA; native a11y belongs to the mobile clusters above.

## Guardrails

See `frontend-web-core`. In short: **respect the SSR boundary** — wrap stateful/motion components in `"use client"` and match server/client initial state to avoid hydration mismatch; **layer motion on `motion-foundations`** (never inline ad-hoc durations); **accessibility is not optional** — semantic HTML first, every interactive element keyboard-reachable, every animation honors `prefers-reduced-motion`; **never mix `motion/react` and `framer-motion`** in one project. Pick the framework once and route consistently — don't blend React and Vue idioms in the same surface.

## Picked-up spokes

Additional frontend-web spokes adopted from the **antigravity-awesome-skills (MIT)** library. These extend the cluster into auth, deployment, search, 3D, and component-library territory. Route to them the same way as the core spokes (load on demand, see below).

**Auth & integration**
- `nextjs-supabase-auth` — Supabase Auth on the Next.js App Router: browser/server clients, middleware session refresh, auth callback route
- `clerk-auth` — Clerk auth: App Router setup, middleware-protected routes, organizations, webhooks, user→DB sync
- `shopify-apps` — Shopify embedded apps (Remix/React Router + App Bridge), GraphQL Admin API, webhooks, Polaris, billing, extensions

**Search**
- `algolia-search` — Algolia indexing strategies, React InstantSearch hooks/widgets, faceting, relevance tuning

**Deploy & ship (Vercel)**
- `deploy-to-vercel` — deploy apps/sites to Vercel, preferring git-push preview deploys + proper linking ("deploy my app", "push this live")
- `vercel-cli-with-tokens` — Vercel CLI via token auth (`VERCEL_TOKEN`) for CI / non-interactive deploys and env-var management
- `vercel-deployment` — Next.js-on-Vercel knowledge: env vars per environment, edge/serverless functions, build config, production rollout
- `vercel-optimize` — observability-first Vercel cost/perf audit: production metrics → deterministic gates → version-aware recommendations

**React quality & FP**
- `react-component-performance` — diagnose a slow React component: isolate ticking state, stabilize props/handlers, memoize leaves, virtualize, verify in Profiler
- `senior-frontend` — senior React/Next/TS/Tailwind workflows: scaffolding, component/hook generation, bundle analysis, patterns, a11y, testing (ships scripts)
- `fp-ts-errors` — errors-as-values in TypeScript with fp-ts `Either`/`TaskEither`; validation-error accumulation instead of try/catch
- `fp-ts-react` — fp-ts in React: `Option`/`Either`/`TaskEither`/`RemoteData` for state, forms, and data fetching (React 18/19, Next 14/15)

**Component libraries & view transitions**
- `shadcn` — manage shadcn/ui: add from registries via CLI, compose, style with semantic tokens, enforced rule set (user-invocable: false — agent-loaded)
- `rayden-code` — generate React + Tailwind using the Rayden/Rayna UI library (34 components) with correct props/tokens and an anti-pattern ban list
- `vercel-react-view-transitions` — native React/Next view transitions: shared elements, route transitions, transition types, reduced-motion-safe

**3D / WebGL**
- `3d-web-experience` — broad 3D-for-web architect: Three.js, React Three Fiber, Spline, WebGL, GLSL — configurators, immersive sites
- `threejs-skills` — focused Three.js best practices: scene setup, lighting, controls, animation loops, effects, data viz in 3D

**Testing & extensions**
- `awt-e2e-testing` — AI-driven E2E web testing via declarative YAML → Playwright with visual matching (OpenCV + OCR), no brittle selectors
- `browser-extension-builder` — cross-browser extensions (Chrome/Firefox): Manifest V3, content scripts, service workers, popup UIs, Web Store publishing

### Routing the picked-up spokes by intent

- **"Add login / auth"** → `nextjs-supabase-auth` (Supabase) or `clerk-auth` (Clerk); Shopify merchant app → `shopify-apps`
- **"Add search to the site/app"** → `algolia-search`
- **"Deploy / ship this"** → `deploy-to-vercel` (interactive), `vercel-cli-with-tokens` (CI/token); Next.js specifics → `vercel-deployment`; "it's expensive / slow in prod" → `vercel-optimize`
- **"Component is slow"** → `react-component-performance` (pairs with the core `react-performance` ruleset)
- **"Scaffold a React/Next app, generate components"** → `senior-frontend`
- **"Type-safe error handling / functional React"** → `fp-ts-errors`, then `fp-ts-react`
- **"Use shadcn / a design-system component lib"** → `shadcn`; Rayden/Rayna stack → `rayden-code`
- **"Animate between routes / shared element"** → `vercel-react-view-transitions` (native view transitions; for spring/gesture motion stay on `motion-*`)
- **"Build something in 3D / WebGL"** → `3d-web-experience` for the stack decision and React Three Fiber, `threejs-skills` for raw Three.js implementation
- **"Write E2E browser tests with AI"** → `awt-e2e-testing` (complements `react-testing` for component-level coverage)
- **"Build a browser extension"** → `browser-extension-builder`

> Note: React **Native** and Makepad (Rust native UI) skills were intentionally **not** adopted here — native mobile UI hands off to the `react-native` / `expo` / `mobile-flutter` siblings below, and this cluster stays browser-only.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).

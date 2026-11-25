---
name: ui-component-sources
description: Catalog of Prashant's preferred ready-made UI sources — Kokonut UI, coss ui (Origin UI), Bklit UI charts, ThreeUI (Three.js components), liquid-glass React lens, Liquid Orb Editor, Circle Loaders — with exact install commands and when to use each. Use before hand-building a component, chart, loader, glass effect, AI orb, or WebGL background.
---

# UI Component Sources

Written for this agent-kit; install commands checked against each project's docs in Sep 2026. Before adding anything: check `package.json` and `components.json`, match the project's existing library, and never add a second library that does the same job.

Most of these are **shadcn-registry** libraries: they need `npx shadcn@latest init` (Tailwind v4) first, and they copy source into the repo — you own and can edit the code.

## Component libraries

### Kokonut UI — animated React/Tailwind components (the "Coconut UI" in the user's list)
- Site: https://kokonutui.com (free, open source; Pro version exists at kokonutui.pro — never use Pro code unless the user owns it)
- Add registry to `components.json`: `"registries": { "@kokonutui": "https://kokonutui.com/r/{name}.json" }`
- Install a component: `npx shadcn@latest add @kokonutui/<component-name>` (e.g. `@kokonutui/particle-button`)
- Good for: fancy buttons, AI input boxes, cards, text effects, marketing sections.

### coss ui — formerly Origin UI (the "Origin kit" in the user's list)
- originui.com now redirects to https://coss.com/ui (Cal.com's design system, built on **Base UI**, not Radix).
- New project: `npx shadcn@latest init @coss/style`
- Existing project, all primitives: `npx shadcn@latest add @coss/ui`
- Single component: `npx shadcn@latest add @coss/<component>` (e.g. `@coss/button`). "Particles" = pre-built combos of primitives.
- Good for: app UI — forms, inputs, selects, tables, dialogs, settings pages. Don't mix Base UI (coss) and Radix (default shadcn) versions of the same primitive in one project.

### Bklit UI — charts on shadcn (the "Backlit UI" in the user's list)
- Site: https://bklit.com (docs: /docs/installation)
- Registry: `"@bklit": "https://ui.bklit.com/r/{name}.json"`
- Install: `npx shadcn@latest add @bklit/<chart>` (e.g. `@bklit/area-chart`, `@bklit/line-chart`, `@bklit/heatmap-chart`)
- 17+ chart types (area, bar, candlestick, funnel, gauge, heatmap, sankey, radar, sunburst, live line...). Good for dashboards and trading/finance UIs.
- Also load the `dataviz` guidance if available for color and chart choice.

## Effects & visuals

### liquid-glass — Apple-style glass lens for React
- Site: https://glass.samasante.com · Repo: https://github.com/samasante/liquid-glass (MIT)
- Install: `npm i @samasante/liquid-glass` (peer deps: react, react-dom). ⚠️ The unscoped npm package `liquid-glass` is a DIFFERENT package — always use the `@samasante/` scope.
- Usage: `import { Glass } from "@samasante/liquid-glass"` → `<Glass style={{ background: "rgba(255,255,255,0.2)", borderRadius: 16 }}>...</Glass>`
- Browser note: bending the live page uses `backdrop-filter: url()` = Chrome/Edge only. Safari/Firefox still get frost + tint + rim; to bend everywhere use `refract={node}` or `size` + `center` (see the repo README / BROWSERS.md).
- Use sparingly: nav bars, floating controls, hero cards. Ensure text on glass still meets contrast.

### Liquid Orb Editor — animated AI/voice orb
- Site: https://lersent001.github.io/orb/ · Repo: https://github.com/LerSent001/orb (MIT)
- It is an **editor**, not an npm package: tune one of the presets in the browser → share the URL hash for approval → use **Export → Web** to get standalone code (WebGPU/WGSL). Also exports SwiftUI/Metal.
- Needs WebGPU; exported web code has a static fallback — keep it, and lazy-load the orb.
- Audio-reactive presets: host app calls `window.liquidOrb.setAudioBands({ low, mid, high, all })` with 0–1 values; call `setAudioBands()` with no args to stop.
- Good for: AI assistant/voice UIs, "thinking" states, hero centrepieces.

### Circle Loaders — 24 animated SVG spinners
- Site: https://circleloaders.dominikakissi.com (by Domi Kissi)
- No install: copy the SVG from a card. Works as inline SVG, `<img>`, or CSS background.
- Customise with CSS `color` (monochrome, follows `currentColor`) and the `--rate` custom property for speed.
- Add `role="status"` + visually hidden "Loading…" text (or `aria-label`) when used inline; respect reduced motion (slow down or show static).

### ThreeUI — copy-ready Three.js components
- Site: https://threeui.com (browse: /browse)
- Copy-ready Three.js components, WebGL backgrounds, hero sections, UI effects and full templates. Copy code from the site; check each item's license/pricing on the page before using it in client work.
- After pasting: match the project's `three` version, add cleanup/dispose on unmount, lazy-load, and add a static fallback. Then follow `threejs-webgl` / `react-three-fiber`.

## Picking guide

| Need | First choice |
|---|---|
| Standard app UI (forms, dialogs, tables) | coss ui (or the project's existing shadcn setup) |
| Eye-catching marketing component | Kokonut UI |
| Charts / dashboards | Bklit UI |
| Loader / spinner | Circle Loaders |
| Glass surfaces | liquid-glass |
| AI orb / voice visual | Liquid Orb Editor export |
| 3D hero / WebGL background | ThreeUI, then customise with `shader-glsl` / `particle-system` |

---
name: implement-view-transitions
description: Implement fluid, native-feeling page and state transitions using CSS View Transitions API, React 19 ViewTransition, Next.js App Router transitions, and shared element morphing without degrading Core Web Vitals. Use when adding route animations, shared element transitions, or layout morphs.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, run_dev_server, execute_command]
---

# Implement View Transitions

Use this skill to implement, optimize, and audit native view transitions, route-level page animations, shared element morphs, and layout displacement animations across React 19, Next.js, and Astro.

## When to Use

- implementing fluid hierarchical page navigations (list -> detail -> list) with directional slides
- authoring shared element morphs between source cards and destination hero sections
- animating Suspense reveal transitions (skeleton -> content) without layout jumps
- implementing layout displacement morphs on dynamic list additions, removals, or reordering
- optimizing web animation performance to protect Interaction to Next Paint (INP < 200ms)
- enforcing WCAG 2.2 AA `prefers-reduced-motion` compliance across all view transitions

## Core Rules

- **Composited Motion Only**: animations attached to `::view-transition-old` and `::view-transition-new` must strictly animate `transform` and `opacity`; never animate layout geometry (`width`, `height`, `top`, `left`, `margin`, `padding`)
- **Frequency-Based Animation Budget**: high-frequency actions (hotkeys `Cmd+K`, combobox search) must be instantaneous (0ms); micro-interactions 100–150ms; overlays and drawers strictly bounded to 150–250ms; route transitions capped at 400ms
- **Harmonic Spring Physics Presets**: UI springs must use mass $m=1.0$ and near-critical damping ($\zeta \approx 0.75 - 0.85$); underdamped cartoonish bouncing ($\zeta < 0.6$) is strictly forbidden
- **Single Smooth-Scroll Engine Exclusivity**: strictly prohibit installing both Lenis and Locomotive Scroll simultaneously; use exactly one coordinator (`lenis/react` or native CSS) to prevent compositor race conditions
- **Enforce INP Performance Budget (< 200ms)**: the DOM mutation callback inside `startViewTransition` must execute in under 50ms without synchronous long tasks; wrap non-urgent transitions in `React.startTransition` and chunk streaming work with `scheduler.yield()`
- **Apply `default="none"` Discipline**: all named and type-keyed `<ViewTransition>` boundaries must specify `default="none"`, explicitly opting into only the transitions they are intended to handle
- **Precede DOM Nodes**: in React, `<ViewTransition>` must wrap content *before any DOM nodes* to activate enter/exit transitions; never wrap `<ViewTransition>` inside an un-animated host `<div>`
- **Enforce Global Uniqueness for Transition Names**: `view-transition-name` (or the `name` prop on `<ViewTransition>`) must be globally unique across active elements; suffix list and entity elements with dynamic IDs (`hero-image-${item.id}`)
- **Isolate Persistent Elements**: persistent headers, sidebars, and sticky controls must be pulled out of the `root` transition group by assigning unique `viewTransitionName` identifiers and suppressing their animations
- **Mandate Reduced Motion Fallback**: every view transition stylesheet must declare an `@media (prefers-reduced-motion: reduce)` block disabling or instant-fading animations
- detailed recipes, motion tables, and physics specifications: [`references/view-transitions-and-motion-specs.md`](references/view-transitions-and-motion-specs.md) and [`../ui-ux-designer-anti-slop-standards.md`](../ui-ux-designer-anti-slop-standards.md)

## Suggested Process

### 1. Audit Navigation Map & Candidate Surfaces

Scan the route graph. Identify navigation triggers (`<Link>`, `router.push`), navigation directions (forward, back), Suspense boundaries, shared visual elements (thumbnails -> hero headers), and persistent app shell elements (header, sidebar, sticky dock).

### 2. Add Global CSS Recipes & Reduced Motion Overrides

Incorporate standardized view transition keyframes and classes into the global stylesheet. Ensure `@media (prefers-reduced-motion: reduce)` is active before authoring custom animations.

### 3. Isolate App Shell & Persistent Elements

Assign explicit `viewTransitionName` styles to header, navigation, and persistent containers. Apply persistent isolation CSS to prevent shell flickering during page transitions.

### 4. Implement Directional Route Transitions

Tag navigation events with `addTransitionType` (`nav-forward`, `nav-back`) inside `startTransition`. Wrap page components in reusable type-keyed `<DirectionalTransition>` components.

### 5. Wire Shared Element Morphs

Assign matching `name={`entity-hero-${id}`}` props to source and destination elements. Set `share="morph"` and configure appropriate fallback `enter`/`exit` classes for routes where no pair forms.

### 6. Verify Core Web Vitals & Interaction Responsiveness

Measure Interaction to Next Paint (INP) and Cumulative Layout Shift (CLS) under simulated 4x CPU throttling. Verify animations run at 60/120fps on compositor thread with zero layout thrashing.

## Checklist

- [ ] view transitions animate exclusively composited properties (`transform`, `opacity`)
- [ ] Interaction to Next Paint verified under budget (INP < 200ms under 4x CPU throttling)
- [ ] all targeted `<ViewTransition>` boundaries declare `default="none"`
- [ ] `<ViewTransition>` components placed before any host DOM nodes
- [ ] `name` attributes for shared elements are dynamically scoped and globally unique
- [ ] persistent headers and navigation bars isolated with unique `viewTransitionName`
- [ ] `@media (prefers-reduced-motion: reduce)` overrides verified in browser
- [ ] hierarchical navigations mapped with typed directional transitions (`nav-forward` / `nav-back`)
- [ ] fallback animations defined for shared elements when matching target is absent
- [ ] frequency-based animation budget enforced (hotkeys 0ms, micro 100-150ms, overlays 150-250ms, routes ≤400ms)
- [ ] harmonic spring physics: mass 1.0, damping 0.75-0.85
- [ ] single smooth-scroll engine (Lenis or native CSS) — not both
- [ ] security: `view-transition-name` sanitized; transition types allowlisted
- [ ] `performance-audit.json` and `implementation-result.json` emitted and validated

## Failure Modes

- **Layout Thrashing & Frame Drops**: CSS animates `height` or `width` during transition, dropping frames below 30fps. Mitigation: code review rejects layout property animations; replace with scale/translate transforms.
- **Duplicate Name Collision**: two active items render `name="hero-image"`, breaking transitions. Mitigation: require dynamic ID parameterization (`name={`hero-${id}`}`).
- **Unintended Global Crossfade**: an unconfigured `<ViewTransition>` fades every time a background revalidation occurs. Mitigation: enforce `default="none"`.
- **Persistent Header Jump**: sticky navigation header stretches and slides during page change. Mitigation: pull header into independent transition group via `viewTransitionName: "header"`.
- **Spring Physics Violation**: underdamped cartoonish bouncing ($\zeta < 0.6$). Mitigation: design system enforces $\zeta \approx 0.75-0.85$; lint rule for spring config.
- **INP Budget Breach**: DOM mutation > 50ms inside `startViewTransition`. Mitigation: `React.startTransition` + `scheduler.yield()` chunking; profile with 4x CPU throttling.
- **CSS Injection via `view-transition-name`**: unescaped string interpolation. Mitigation: sanitize dynamic names against pattern; reject unsafe characters.

## Output Contracts

When this skill is invoked as part of a coordinated frontend slice, emit:

- **`contracts/schemas/ui-component-spec.json`** — Documents transition boundaries, names, triggers, and type maps.
- **`contracts/schemas/performance-audit.json`** — Records INP, LCP, CLS, and compositor frame-rate measurements.
- **`contracts/schemas/implementation-result.json`** — Records files modified, CSS recipes installed, and behavioral test evidence.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: do not allow transition type parameters to be populated directly from untrusted query strings without strict allowlist validation.
- **ASI05 RCE Guard**: validate dynamic `name` attributes against sanitization patterns to prevent CSS injection via unescaped string interpolation.
- **ASI07 Inter-Agent Communication**: emit structured `performance-audit.json` documenting INP metrics for Reviewer and Technical Lead verification.

## Related Skills

- **add-page-route**: Wire page components and Next.js / Astro routes to transition boundaries
- **add-ui-component**: Author shared presentation components capable of morphing
- **component-composition**: Structure compound slots and shared visual elements for transition pairing
- **frontend-testing**: Assert route navigation, snapshot stability, and DOM state integrity
- **setup-design-system**: Define design tokens, easing curves, and duration variables

Last updated: 2026-09-25
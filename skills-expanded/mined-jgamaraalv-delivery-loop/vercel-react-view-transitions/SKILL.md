---
name: vercel-react-view-transitions
description: Animate React route/page changes, shared elements, and enter/exit/reorder with the View Transition API (`<ViewTransition>`); use for view transitions in React or Next.js.
---

# React View Transitions

Animate between UI states using the browser's native `document.startViewTransition`. Declare _what_ with `<ViewTransition>`, trigger _when_ with `startTransition` / `useDeferredValue` / `Suspense`, control _how_ with CSS classes. Unsupported browsers skip animations gracefully.

## When to Animate

Every `<ViewTransition>` should communicate a spatial relationship or continuity. If you can't articulate what it communicates, don't add it.

Implement **all** applicable patterns from this list, in this order:

| Priority | Pattern                            | What it communicates             |
| -------- | ---------------------------------- | -------------------------------- |
| 1        | **Shared element** (`name`)        | "Same thing — going deeper"      |
| 2        | **Suspense reveal**                | "Data loaded"                    |
| 3        | **List identity** (per-item `key`) | "Same items, new arrangement"    |
| 4        | **State change** (`enter`/`exit`)  | "Something appeared/disappeared" |
| 5        | **Route change** (layout-level)    | "Going to a new place"           |

This is an implementation order, not a "pick one" list. Implement every pattern that fits the app. Only skip a pattern if the app has no use case for it.

### Choosing Animation Style

| Context                                 | Animation                                          | Why                          |
| --------------------------------------- | -------------------------------------------------- | ---------------------------- |
| Hierarchical navigation (list → detail) | Type-keyed `nav-forward` / `nav-back`              | Communicates spatial depth   |
| Lateral navigation (tab-to-tab)         | Bare `<ViewTransition>` (fade) or `default="none"` | No depth to communicate      |
| Suspense reveal                         | `enter`/`exit` string props                        | Content arriving             |
| Revalidation / background refresh       | `default="none"`                                   | Silent — no animation needed |

Reserve directional slides for hierarchical navigation (list → detail) and ordered sequences (prev/next photo, carousel, paginated results). For ordered sequences, the direction communicates position: "next" slides from right, "previous" from left. Lateral/unordered navigation (tab-to-tab) should not use directional slides — it falsely implies spatial depth.

---

## Availability

- **Next.js:** Do **not** install `react@canary` — the App Router already bundles React canary internally. `ViewTransition` works out of the box. `npm ls react` may show a stable-looking version; this is expected.
- **Without Next.js:** Install `react@canary react-dom@canary` (`ViewTransition` is not in stable React).
- Browser support: Chromium 111+, Firefox 144+, Safari 18.2+. Graceful degradation on unsupported browsers.

---

## Core Concepts

### The `<ViewTransition>` Component

```jsx
import { ViewTransition } from "react";

<ViewTransition>
  <Component />
</ViewTransition>;
```

React auto-assigns a unique `view-transition-name` and calls `document.startViewTransition` behind the scenes. Never call `startViewTransition` yourself.

### Animation Triggers

| Trigger    | When it fires                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------- |
| **enter**  | `<ViewTransition>` first inserted during a Transition                                             |
| **exit**   | `<ViewTransition>` first removed during a Transition                                              |
| **update** | DOM mutations inside a `<ViewTransition>`. With nested VTs, mutation applies to the innermost one |
| **share**  | Named VT unmounts and another with same `name` mounts in the same Transition                      |

Only `startTransition`, `useDeferredValue`, or `Suspense` activate VTs. Regular `setState` does not animate.

### Critical Placement Rule

`<ViewTransition>` only activates enter/exit if it appears **before any DOM nodes**:

```jsx
// Works
<ViewTransition enter="auto" exit="auto">
  <div>Content</div>
</ViewTransition>

// Broken — div wraps the VT, suppressing enter/exit
<div>
  <ViewTransition enter="auto" exit="auto">
    <div>Content</div>
  </ViewTransition>
</div>
```

Behaviour is controlled with props (`"auto"` / `"none"` / a CSS class / a type-keyed object) and CSS pseudo-elements. See `references/patterns.md` for the full prop/pseudo-element reference, transition types, shared elements, and the multi-VT interaction rules.

---

## Accessibility

Always add the reduced motion CSS from `references/css-recipes.md` to your global stylesheet.

---

## Implementation Workflow

When adding view transitions to an existing app, **follow `references/implementation.md` step by step.** Start with the audit — do not skip it. Copy the CSS recipes from `references/css-recipes.md` into the global stylesheet — do not write your own animation CSS.

---

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/implementation.md` — step-by-step workflow for adding VTs to an app (audit → CSS → persistent elements → directional page transitions → Suspense reveals → shared elements → verify), plus common mistakes · read when starting an integration.
- `references/patterns.md` — the deep API and pattern catalogue: styling props + CSS pseudo-elements, transition types (`addTransitionType`, type maps, `router.back()` caveat), shared element morphs, the core composition patterns (enter/exit, list reorder, composing shared + list identity, force re-enter with `key`, Suspense reveals), how multiple VTs interact, plus worked patterns (deferred grid, card expand/collapse, type-safe helpers, cross-fade without remount, isolating elements, `useOptimistic`), events API, animation timing, and troubleshooting · read when implementing or debugging a specific behaviour.
- `references/css-recipes.md` — ready-to-use CSS animation recipes (timing variables, fade, slide, directional nav, shared/text morph, scale, persistent element isolation, reduced motion) · read when writing the global stylesheet.
- `references/nextjs.md` — Next.js App Router specifics: `experimental.viewTransition` flag, `transitionTypes` on `next/link`, programmatic navigation, server-side filtering, `loading.tsx` boundaries, same-route dynamic segments, Server Components · read when integrating in Next.js.

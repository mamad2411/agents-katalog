---
name: frontend-engineering
description: Frontend-specific engineering concerns — render performance, bundle and asset delivery, CSS architecture, client-side state, and accessibility as engineering. Use when building or reviewing UI code, when investigating Core Web Vitals (LCP/CLS/INP), when bundle size is growing, when hydration mismatches appear, when CSS is bleeding across components, when client-side state is hard to reason about, or when accessibility is being treated as an afterthought. Does not cover framework-specific APIs (React hooks, Vue reactivity) — framework-agnostic signals only.
---

# Frontend Engineering

Frontend engineering has failure modes that have no backend analogue. The user's browser, device, and network are all outside your control, and they all vary wildly. Performance is constrained by what the *median user* experiences on a mid-tier device over a slow connection — not by what you experience on your developer machine on broadband.

For render performance and Core Web Vitals see [render-performance.md](render-performance.md).
For bundle size, asset delivery, and the network waterfall see [bundle-and-assets.md](bundle-and-assets.md).
For CSS architecture and client-side state management see [css-and-state.md](css-and-state.md).
For accessibility as an engineering concern see [accessibility-signals.md](accessibility-signals.md).

## What makes frontend engineering distinct

**The runtime is hostile.** Browsers vary in feature support, performance characteristics, and bug surface. The same code runs on Chrome on a high-end desktop and on a 3-year-old Android. Both are users.

**The network is the bottleneck more often than the CPU.** A 200KB JavaScript bundle delivered over 4G is the difference between a 1-second and a 5-second time-to-interactive. Optimising the render code while shipping a bloated bundle is solving the wrong problem.

**The render pipeline has its own performance model.** Layout, paint, composite — these are browser-internal phases that can be triggered or avoided by code. A JavaScript change that re-reads layout in a loop forces hundreds of layout recalculations. The CPU profiler shows the function is fast; the user sees jank.

**State lives in many places.** Server state (data from your API), client state (form inputs, selections), URL state (the back button must work), and persistent state (localStorage). Mixing them produces bugs that are nearly impossible to reproduce.

**The user can interact at any moment.** Backend code processes a request and returns; frontend code is interrupted by clicks, scrolls, and resizes constantly. Code that assumes uninterrupted execution breaks.

## The signals agents consistently miss

- Shipping JavaScript in the render hot path that triggers layout (`element.offsetWidth` inside a render cycle)
- Importing entire libraries when one function is needed (`import _ from 'lodash'` for a single `_.debounce`)
- Hydration mismatches between SSR and client render (different timestamps, locale-dependent values, hydration on data that was not in the SSR)
- Globally-scoped CSS that bleeds across components (no scoping strategy)
- Treating server state as client state (re-fetching on every render, no caching layer)
- Building UIs that work only with a mouse (no keyboard navigation, no focus management)
- Optimising for desktop and never testing on a mid-tier mobile device

## The core question

Before declaring a frontend feature complete, answer:

- What does this look like on a mid-tier mobile device on a slow network?
- What is the LCP / CLS / INP for this page?
- What happens if the user navigates away mid-load?
- What happens if the user has JavaScript disabled, a screen reader, or uses keyboard-only navigation?
- What happens if the API call fails — does the UI show an error or a forever-spinner?

If any of these answers is "I don't know" — the feature is not complete.

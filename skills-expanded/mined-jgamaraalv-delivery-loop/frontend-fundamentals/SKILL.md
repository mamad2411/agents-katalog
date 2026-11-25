---
name: frontend-fundamentals
description: Front-end system-design reference — box model, rendering/reflow, DOM & Web APIs, virtualisation, state design, network transports, web performance.
---

# Frontend Fundamentals

A reference library for browser-level front-end system design: how the browser lays out, renders, and composites; the DOM and Web Observer APIs; UI optimization techniques (virtualisation); how to structure and search application state; how to choose a network transport; and how to make a web app fast. Read the one reference that matches the question rather than loading everything.

> **The golden rule of Web UI applications:** *Do not block the Main Thread (UI Thread).*

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/core-fundamentals.md` — box model & `box-sizing`, box types (block/inline/anonymous), formatting contexts, the `position` system & containing-block rules · read when reasoning about layout, sizing, or why an element sits where it does.
- `references/rendering.md` — stacking context, the DOM→render-tree→reflow→repaint→composite pipeline, GPU-composited animation, render vs graphic (compositor) layers · read when diagnosing jank, layout/paint cost, or `z-index`/layer-promotion behaviour.
- `references/dom-api.md` — the DOM class hierarchy, query method performance table, add/remove perf impact, `DocumentFragment`/`<template>` batch inserts · read when manipulating the DOM directly or building a low-level/generic component.
- `references/web-apis-observers.md` — Intersection / Mutation / Resize observers (with code) and the resize-mechanism decision table · read when replacing polling, doing lazy-load/visibility logic, or reacting to size/DOM changes.
- `references/virtualisation.md` — the sliding-window technique: top/bottom observers, element pool, recycling and the `translateY` positioning math · read when rendering very long lists/grids without bloating the DOM.
- `references/state-design.md` — data classes/properties, normalization (1NF–3NF), inverted/composite indexes on a Web Worker, memory offloading, browser storage options · read when structuring large client state or adding in-app search.
- `references/network.md` — UDP/TCP & the protocol stack, long polling vs SSE vs WebSockets (pros/cons/when), a per-platform API design example, REST vs GraphQL heuristics · read when choosing how the client talks to the server.
- `references/performance.md` — Core Web Vitals targets (LCP/INP/CLS), network/HTTP, JS bundle (polyfills, code splitting, preload/prefetch, minify/compress), CSS critical-path, image formats, font loading · read when tuning load/runtime performance.

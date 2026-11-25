---
name: htmx-spa-conventions
description: Strict production-grade HTMX + Alpine.js SPA conventions with Tailwind CSS — enforces server-driven UI, HTML-over-the-wire architecture, fragment rendering, swap discipline, security best practices and anti-SPA rules.
license: MIT
compatibility: opencode
---

You are a strict HTMX production architect. You enforce HTML-over-the-wire, server-side rendering, fragment responses for HTMX requests, progressive enhancement, minimal JavaScript, correct hx-swap strategy, proper browser history handling, and secure request validation. If a solution mimics SPA architecture, warn immediately.

## What I do.
- Define the core HTMX SPA architecture: HTMX for dynamic content loading, Alpine.js for lightweight client-side interactions.
- Handle page transitions via HTMX AJAX swapping (`hx-get`, `hx-post`, `hx-target`) — no full page reloads.
- Keep HTML generation server-side; return partial HTML fragments for HTMX requests, not JSON.
- Enforce mobile-first responsive layouts with standard mobile utilities and `md:` desktop overrides.
- Use sticky bottom navigation or hamburger menus on mobile; traditional top/side navigation on desktop.
- Style with Tailwind CSS utility classes exclusively — no custom `<style>` blocks.
- Maintain a modern, professional, clean, minimal aesthetic with ample whitespace.
- Use a clean color palette: off-white/light gray backgrounds, dark charcoal text, a single accent color (indigo or emerald) used sparingly.
- Ensure all interactive elements have clear focus states (`focus:ring-2`).
- Use semantic HTML tags (`<nav>`, `<main>`, `<header>`, `<article>`) instead of nested `<div>` wrappers.
- Server returns HTML, not JSON — never return JSON for HTMX requests.
- Detect `HX-Request` header to decide partial vs full layout responses.
- Return fragments for HTMX, full layout for direct browser visits.
- Use correct `hx-swap` strategy (innerHTML, outerHTML, beforeend, etc.).
- Use OOB swaps (`hx-swap-oob`) for multi-target updates from a single response.
- Preserve browser history with `hx-push-url` and `hx-replace-url`.
- Use correct HTTP status codes (200 success, 422 validation, 404 not found).
- Always include CSRF protection on mutating requests.
- Avoid unnecessary polling — prefer SSE or WebSocket for real-time.
- Never rebuild DOM with client-side JavaScript — let the server drive HTML.

## Activation Context

Activate when user mentions: htmx, hx- attributes, server-driven UI, html-over-the-wire, partial rendering, progressive enhancement, or migrating from SPA.

## Detailed References

Consult `ui_skills/references/` for detailed guidance on:
- [attributes.md](../references/attributes.md) — core hx-* attributes
- [triggers.md](../references/triggers.md) — event triggers and modifiers
- [swap.md](../references/swap.md) — swap strategies and modifiers
- [events.md](../references/events.md) — HTMX event lifecycle
- [server-patterns.md](../references/server-patterns.md) — fragment architecture
- [validation.md](../references/validation.md) — form validation patterns
- [security.md](../references/security.md) — CSRF, CSP, input validation
- [performance.md](../references/performance.md) — caching, ETags, debouncing
- [headers.md](../references/headers.md) — HX-Trigger, HX-Redirect, etc.
- [anti-patterns.md](../references/anti-patterns.md) — what NOT to do

## When to use me.
Use this skill whenever building or modifying UI components, layouts, or page views in this project. It governs all frontend conventions — from component structure and styling to accessibility and responsiveness.

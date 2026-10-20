---
name: apply-responsive-layout
description: Wraps existing page fragments into a fully responsive mobile-first grid or layout wrapper.
license: MIT
compatibility: opencode
---

## What I do.
- Wrap standalone HTML modules into full layouts readable across both tiny mobile screens and ultra-wide desktop monitors.
- Structure elements cleanly using CSS Grid and Flexbox layout utilities from Tailwind CSS.
- Ensure layouts maintain a persistent, single-page app behavior utilizing sticky navigation systems (bottom bar for mobile, sidebar/top-bar for desktop).
- Preserve browser history consistency using `hx-push-url` on navigation links and pagination.
- Use `hx-history-elt` to define which element tracks scroll position across history entries.
- Apply `hx-replace-url` for soft URL updates that shouldn't create history entries.
- Choose appropriate swap strategies for layout regions: `innerHTML` for content areas, `outerHTML` for nav items, `beforeend` for feed/list appends.
- Use `hx-target` with layout-specific selectors to replace content regions without disrupting navigation, headers, or sidebars.
- Use `hx-select-oob` for multi-region layout updates (e.g., updating both content pane and sidebar state from one response).
- On HTMX requests, server returns only the content fragment — never the full layout wrapper.

## Detailed References

Consult `ui_skills/references/` for detailed guidance:
- [swap.md](../references/swap.md) — swap strategies for different layout regions
- [attributes.md](../references/attributes.md) — targeting, history attributes, OOB
- [headers.md](../references/headers.md) — HX-Push-Url, HX-Replace-Url
- [server-patterns.md](../references/server-patterns.md) — fragment architecture
- [anti-patterns.md](../references/anti-patterns.md) — full layout in fragment anti-pattern

## When to use me.
Use this skill when initializing the structural foundation of a new view, setting up the main app dashboard framework, or fixing broken alignment between mobile and desktop viewport sizes.

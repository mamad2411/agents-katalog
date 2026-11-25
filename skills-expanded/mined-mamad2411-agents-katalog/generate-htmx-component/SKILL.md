---
name: generate-htmx-component
description: Generates a self-contained, lightweight UI component using server-driven HTMX and standard Tailwind utility classes.
license: MIT
compatibility: opencode
---

## What I do.
- Build clean, functional, HTML-only frontend fragments tailored for server-side responses.
- Implement dynamic interactions strictly via HTMX attributes (`hx-get`, `hx-post`, `hx-target`, `hx-swap`).
- Return HTML fragments (never JSON) — detect `HX-Request` header server-side to decide fragment vs full layout.
- Use explicit `hx-target` selectors — target specific elements, never replace entire layout containers.
- Choose correct `hx-swap` strategy: `innerHTML` for content updates, `outerHTML` for element replacement, `beforeend`/`afterend` for insertion, `delete` for removal.
- Use `hx-swap-oob` for updating multiple UI targets from a single fragment response.
- Return proper HTTP status codes: 200 for success, 422 for validation errors, 404 for not found, 400 for bad request.
- On validation errors, return the same form fragment with error messages and HTTP 422 — never redirect.
- Use Swap Modifiers (`swap:1s`, `settle:200ms`, `show:top`) where UI transition timing matters.
- Use minimalist Tailwind CSS styling matching the off-white, light gray, and subtle single-accent color palette.

## Detailed References

Consult `ui_skills/references/` for detailed guidance:
- [swap.md](../references/swap.md) — swap strategy reference
- [attributes.md](../references/attributes.md) — targeting, modifiers, OOB
- [validation.md](../references/validation.md) — form validation with 422
- [server-patterns.md](../references/server-patterns.md) — fragment architecture
- [anti-patterns.md](../references/anti-patterns.md) — what NOT to do

## When to use me.
Use this skill whenever you need to build or modify individual page elements, form cards, data blocks, or interactive buttons that need to refresh without forcing a browser page reload.

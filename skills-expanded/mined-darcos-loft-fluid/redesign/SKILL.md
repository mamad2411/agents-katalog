---
name: redesign
description: Audit an existing web UI and produce a modernization plan plus a fresh design system. Use when a site or app already works but looks dated or generic and needs a proper visual audit and a redesign pass, not a rebuild from scratch. Preserves content, routes, and SEO.
license: MIT
---

# Redesign

Audit-first. For a site that already works but looks templated or dated, this finds what is wrong, decides what to keep, and ships a committed new identity, without throwing away working structure.

## When to use
- An existing site (Webflow, WordPress, an old React app) needs to look current.
- A client hands you a live URL and wants it modernized.
- A redesign that must preserve content, SEO, and routes.

## The workflow
1. **Audit.** Run the `fluid` detector on the codebase (or read the live DOM and CSS). Catalogue the generic-look tells: fonts, palette, spacing, shadows, the slop list. Note what is genuinely good and worth keeping.
2. **Draw the keep/change line.** Preserve: content, information architecture, routes, anything that converts. Change: the identity (palette, type, surface, motion), the layout repetition, the bans.
3. **Generate the new identity** with the `design-system` skill. Brief it from the brand, pick from `data/`, commit. Two redesigns in the same sector get different palettes.
4. **Map old to new.** A token migration: old hardcoded values become new CSS variables, component by component. Keep a small table so nothing is missed.
5. **Re-skin, do not rebuild.** Keep the markup and structure, swap the look: tokens, type, motion. Add `fluid` motion where it earns its place.
6. **Pre-flight.** Run the detector again, check `design-system/reference/rules.md` (locks, hero discipline, bans). Produce a before/after so the value is visible.

## Rules
- Preserve what converts. A redesign that drops content or breaks routes is a rewrite, not a redesign.
- One identity, committed. Never half-redesign (new colors on old fonts).
- Show the before and after.

Pairs with: `design-system` (the new identity), `fluid` (the motion and the detector audit).

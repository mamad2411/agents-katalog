---
name: design-review-audit
description: Audit a built UI, page, deck, or artifact against a concrete design-guidelines checklist — spacing/rhythm, type hierarchy, contrast/accessibility, consistency, and generic-AI-slop patterns — and produce a prioritized punch list of specific fixes. Use after frontend-design/web-artifacts-builder/canvas-design/premium-html-presentation produce a build, or whenever asked to review, critique, or audit a design. Companion to the /design-review command, which runs this checklist on demand.
---

## Purpose

"Design that reviews itself" — a repeatable checklist pass on a finished (or near-finished) build, so quality issues get caught before delivery rather than relying on a final eyeball pass alone.

## Checklist

Go through each category and report **specific, located** findings (which element, what's wrong, what to change) — not generic praise or vague "looks good."

### 1. Spacing & rhythm
- Is spacing drawn from a consistent scale (e.g. 4px/8px increments), or are there arbitrary one-off values (`margin: 13px`)?
- Is vertical rhythm consistent between similar sections?
- Is there enough breathing room around dense content, or does it feel cramped?

### 2. Typographic hierarchy
- Is there a small, deliberate type scale (not more than ~5-6 sizes), or did sizes get picked ad hoc per element?
- Does heading hierarchy (h1 → h2 → h3) match visual hierarchy — nothing "looks like an h2" but is marked up as a div?
- Is line-length reasonable (roughly 45-75 characters for body text)?

### 3. Color & contrast
- Does body text meet WCAG AA contrast (4.5:1) against its background? Large/heading text 3:1?
- Is the color palette limited and intentional (a handful of roles: background, surface, text, primary, border), or is color being used arbitrarily?
- Do interactive elements have a visibly distinct hover/focus/active state?

### 4. Consistency
- Are repeated patterns (cards, buttons, list items) styled identically everywhere they appear, or do near-duplicates drift?
- Do icons share a consistent style/weight/size (not mixing icon sets)?

### 5. Generic AI-slop tells
Check against `frontend-design`'s own aesthetic guidance for this list specifically — don't duplicate it here, cross-reference it. Flag anything that reads as templated rather than considered: centered-everything hero sections, default purple/blue gradient backgrounds, generic stock-photo energy, emoji used as icons, uniform `rounded-2xl` on every surface regardless of context.

### 6. Responsiveness & edge cases
- Does content overflow or break at narrow viewports?
- Do long strings (names, labels) truncate gracefully instead of breaking layout?
- Empty/loading/error states — do they exist, or only the happy path?

## Output format

A prioritized list: **blocking** (breaks usability/accessibility/looks broken) → **should-fix** (visibly inconsistent or off-scale) → **polish** (nice-to-have refinement). Each item names the specific element/section and the concrete fix, not just the category it falls under.

## Related skills in this repo

- **frontend-design**: Source of the aesthetic principles (including the AI-slop list) this audit checks against — read that skill's guidance rather than re-deriving it.
- **ui-motion-design**: If motion is part of the build, check it against that skill's timing/easing guidance as part of the review.
- **canvas-design**, **premium-html-presentation**, **web-artifacts-builder**: Any of these builds is a valid audit target.
- **design-token-extractor**: If the audit finds inconsistent spacing/color values, this skill is the fix — extract or define a proper token set instead of patching individual values.
- **claude-code-tooling**'s `impeccable` entry: this skill's own contrast checklist item (WCAG AA, above) is a self-assessment prompt — run against two of this repo's own already-published artifacts, `npx impeccable detect` still found real, un-caught 1.2:1 contrast failures on both. A checklist question gets skipped or eyeballed; a deterministic contrast-ratio calculator doesn't. Run `npx impeccable detect <path>` as a mechanical cross-check on any build this checklist has already passed, not as a replacement for the parts of this checklist (spacing rhythm, hierarchy, consistency) it doesn't cover.

## Notes

Source: a "Claude Replaces Designers" screenshot-carousel video (@vibes.codes) describing a "Web Design Guidelines" audit skill ("design that reviews itself"). Companion command: `/design-review` in `.claude/commands/`.

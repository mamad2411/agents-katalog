---
name: layout-integrity
description: Strict layout and UI integrity rules for any web interface work. Use this skill whenever building, editing, or reviewing UI — HTML artifacts, React components, Tailwind layouts, mockups, dashboards, PWA screens, or any page with visual structure. Trigger even for "quick" UI tweaks, redesigns, or when the user asks to build any app, screen, form, or page — layout rules apply to all of it, not just projects explicitly about design.
---

# Strict Layout and UI Integrity

These rules are non-negotiable defaults for all UI output. They exist to prevent the two most common failure modes of generated interfaces: layouts that break on real screens, and the "wall of identical cards" look that screams template.

## 1. Responsive Fluidity

Always build with fluid, responsive primitives: Tailwind flex, grid, and fluid sizing (`w-full`, `max-w-screen-xl`, `md:flex-row`, `min-w-0`, `flex-1`).

- **Never** use absolute pixel widths that can overflow a screen (`w-[1200px]`, `width: 1400px`).
- Fixed dimensions are acceptable only for intentionally small elements (icons, avatars, badges) — never for containers, columns, or page sections.
- Every layout must survive a 360px-wide phone screen without horizontal scroll. If you can't verify visually, reason through the narrowest breakpoint before finishing.
- Constrain content width with `max-w-*` + `mx-auto`, not fixed widths.

## 2. Spacing Guardrails

Maintain visual hierarchy using the standard Tailwind spacing scale (`p-4`, `p-6`, `gap-4`, `space-y-4`).

- Stay on the scale. Arbitrary values (`p-[13px]`, `mt-[7px]`) are a smell — if you reach for one, reconsider the structure instead.
- **Never** introduce negative margins unless the user explicitly requests them. Overlap effects come from grid/flex placement, not `-mt-8` hacks.
- Spacing encodes hierarchy: related items sit closer together than unrelated ones. Section gaps > group gaps > item gaps, consistently.

## 3. Component Placement

Standard interactive elements stay anchor-locked where users expect them:

- Footers at the bottom of the page — including on short pages (use a min-height flex column so the footer doesn't float mid-screen).
- Navigation headers fixed or sticky at the top, with body content padded so nothing hides underneath.
- Sidebars clear of main content at every breakpoint — they collapse or stack on mobile rather than overlapping.
- Modals, toasts, and floating actions positioned with the layout system, never with magic-number offsets.

## 4. Anti-Card Aggregation

Do not pour everything into repetitive, uniform cards or identical rows. That is the default template look; refuse it.

- Vary layout structure: asymmetrical splits, a dominant element with supporting elements, mixed column spans.
- Use clean white space and typographic headers to group data natively — a well-set heading with breathing room groups content as effectively as a border does.
- Cards are for genuinely card-like content (discrete, parallel, self-contained items). A settings page, a form, or a text-heavy section is not a deck of cards.
- Before finishing, scan the output: if three or more sections share the identical box treatment, restructure at least one of them.

## 5. Isolated Component Fixes

When fixing a misplaced button, shifted container, or similar localized layout bug:

- Apply surgical changes using Tailwind utility classes on the affected element.
- **Never** move wrapper elements into unintended DOM parents to force a visual result — if the fix requires restructuring the DOM, say so explicitly and confirm before doing it.
- A layout fix should change the smallest possible surface: prefer adjusting one element's classes over reflowing its neighbors.

## Self-check before delivering

1. Does anything overflow at 360px wide?
2. Are all spacing values on the standard scale, with zero unrequested negative margins?
3. Are footer/nav/sidebar anchored where users expect?
4. Would a screenshot of this read as "wall of identical boxes"? If yes, restructure.

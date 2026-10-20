---
name: responsive-layout-engine
description: "Generates responsive layouts with design system tokens for each breakpoint — mobile-first, tablet, desktop, wide screen. Use when building multi-breakpoint UI layouts."
---

# Responsive Layout Engine

## Overview

Responsive Layout Engine generates responsive layouts for all breakpoints using design system primitives. It adopts a mobile-first approach, using grid systems, flexbox, and container queries to construct consistent and maintainable layouts. It also covers advanced features such as print styles, responsive navigation, and content reflow.

**Core principle:** Every layout is built from the smallest screen to the largest using a mobile-first approach; no breakpoint is an afterthought.

## The Iron Law

```
NO LAYOUT CAN BE DEPLOYED WITH ONLY A SINGLE BREAKPOINT GENERATED. ALL BREAKPOINTS (MOBILE, TABLET, DESKTOP, WIDE SCREEN) MUST BE GENERATED SIMULTANEOUSLY AND MOBILE-FIRST.
```

## When to Use

**Use this when:**
- Creating a page layout or restructuring an existing layout
- Adding a new component to the design system
- Fixing broken responsive behavior in an existing UI
- Generating a page that requires a print stylesheet

**Use this ESPECIALLY when:**
- A client says "just build it for desktop, we will handle mobile later"
- Under time pressure, someone says "it just needs to work on one breakpoint for now"
- A designer provides a Figma export for only one breakpoint

**Don't skip when:**
- Developing internal/admin tools where the user base is fixed on desktop
- Generating a static page that will not be responsive (e.g., a poster)

## Workflow

Work through the ten phases in order. Each phase must be completed before proceeding.

**Phase 1 — Read design system tokens.** Discover breakpoint, grid, spacing, and print tokens; check container query support. See [REFERENCE.md](REFERENCE.md) for the example token structure and discovery steps.

**Phase 2 — Mobile-first layout skeleton.** Set up a single-column layout with basic flexbox/grid; prioritize content and prepare the hamburger menu structure. See [REFERENCE.md](REFERENCE.md) for the mobile baseline CSS snippet.

**Phase 3 — Tablet breakpoint.** Add the tablet media/container query; transition to a 2-column layout and swap hamburger → top nav. See [REFERENCE.md](REFERENCE.md) for the tablet grid and nav CSS.

**Phase 4 — Desktop breakpoint.** Evaluate the holy grail layout, configure the dashboard and card grids, and handle content reflow. See [REFERENCE.md](REFERENCE.md) for the desktop auto-fit grid and reflow CSS.

**Phase 5 — Wide screen breakpoint.** Enforce `max-width`, add visual enhancements, and increase card column count. See [REFERENCE.md](REFERENCE.md) for wide screen CSS.

**Phase 6 — Responsive navigation.** Test hamburger → top nav → sidebar transitions, active indicators, submenus, and keyboard accessibility. See [REFERENCE.md](REFERENCE.md) for the navigation transformation logic.

**Phase 7 — Content reflow and images.** Apply CSS `order`, hide/show content per breakpoint, and configure responsive images with `<picture>` + `srcset` + lazy loading. See [REFERENCE.md](REFERENCE.md) for the `<picture>` element example.

**Phase 8 — Print styles.** Add `@media print`; hide nav/sidebars/ads; set print-safe fonts and colors; control page breaks; expose link URLs. See [REFERENCE.md](REFERENCE.md) for the print CSS block.

**Phase 9 — Performance optimizations.** Split CSS by breakpoint, inline critical CSS, lazy-load routes, use WebP/AVIF images, and prevent layout shift (CLS). See [REFERENCE.md](REFERENCE.md) for the critical CSS inlining pattern and per-step checklist.

**Phase 10 — Final verification.** Run the checklist below before shipping.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "Let's build desktop first, we can add media query overrides for mobile later" — THIS IS A MOBILE-FIRST VIOLATION. Go back to the beginning.
- "We don't need a tablet breakpoint, most people use phones or computers anyway" — Tablet users cannot be ignored.
- "No need for print styles, nobody prints web pages" — Print styles are a standard of accessibility and professionalism.
- "A hamburger menu works everywhere, let's just use that" — Harming user experience on wide screens is unacceptable.
- "We'll optimize CSS later, as long as it works for now" — Performance is built into the foundation, not tacked on later.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "This page looks broken on phones" — You proceeded without testing breakpoints. Go back to Phase 2.
- "The content on the right shifted out of bounds on tablets" — You skipped content reflow. Go back to Phase 3.
- "The menu doesn't work" — You skipped testing navigation transitions. Go back to Phase 6.
- "This button is not clickable on mobile" — You forgot to check touch target sizes.
- "Printing ruins the entire page layout" — You forgot print styles. Go back to Phase 8.
- "The page contents jump around as it loads" — You skipped layout shift prevention (missing image sizes). Go back to Phase 9.

**When you see these:** STOP. Return to relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Let's do desktop first, then handle mobile" | Not mobile-first. Desktop-to-mobile conversion is always harder and more error-prone. |
| "This page is too simple to need responsiveness" | Even the simplest page breaks on different screens. Simple pages must be responsive. |
| "Container queries are too complex, media queries are enough" | Container queries enforce component-level thinking and produce far more modular code. |
| "Print styles are a legacy feature" | Legal documents, recipes, and articles are still printed. It remains an accessibility standard. |
| "No time, let's launch with a single breakpoint" | Making a non-responsive site responsive later costs 2-3x more than doing it right from the start. |

## Related Skills

- **accessibility-optimizer** — Should be run after every layout design to ensure responsive navigation and content are accessible.
- **component-library-generator** — Generates components using responsive primitives to be used in layouts.
- **design-system-extractor** — Used before layout design to extract design system tokens (breakpoints, grid, spacing).
- **performance-auditor** — Used after layout design to verify CSS size, layout shift, and lazy loading performance.

## Verification

After completing this process:

1. **Scope Check:** Have you covered all breakpoints (mobile, tablet, desktop, wide) and print styles?
2. **Mobile-First Check:** Are all media queries written with `min-width` (small to large)? Are there any `max-width` desktop-first overrides?
3. **Edge Case Check:** Have you tested very small screens (under 320px), very large screens (2560px+), landscape mobile, and tablet orientation transitions?
4. **Navigation Check:** Do all navigation states (hamburger → top nav → sidebar) work seamlessly?
5. **Performance Check:** Is CSS size optimized? Is critical CSS inlined? Are there unnecessary media query overrides?
6. **Layout Shift (CLS) Check:** Is there layout shift caused by image sizes, font loading, or dynamic content?
7. **Accessibility Check:** Is keyboard navigation, touch target sizing (min 44px), and zoom support ensured across all breakpoints?
8. **Print Check:** Do print styles show all content properly? Are navigation, sidebars, and ads hidden?

Final checklist before marking complete:

- [ ] All breakpoints (mobile, tablet, desktop, wide) have been tested and visual integrity is verified.
- [ ] Mobile-first approach is verified (styles flow from smaller to larger).
- [ ] Navigation is functional and accessible across all breakpoints.
- [ ] Content reflow works as expected.
- [ ] Container queries work properly (if used).
- [ ] Print styles render as expected.
- [ ] Images are responsive and optimized.
- [ ] Cumulative Layout Shift (CLS) is below 0.1.
- [ ] Lazy loading and code splitting work correctly.
- [ ] Keyboard navigation is flawless across all breakpoints.

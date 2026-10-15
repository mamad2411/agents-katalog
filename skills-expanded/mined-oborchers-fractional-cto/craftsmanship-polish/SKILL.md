---
name: craftsmanship-polish
description: This skill should be used when the user is polishing UI details, optimizing images, implementing shadows or elevation systems, ensuring pixel-perfect alignment, defining border-radius systems, adding micro-interactions or transitions, handling loading/empty/error states, or reducing Cumulative Layout Shift (CLS). Covers VisAWI Craftsmanship facet, retina-ready images, layered shadows, consistent border-radius, transition timing, skeleton screens, and layout stability.
version: 1.0.0
---

# Craftsmanship Is the Multiplier — A Simple Design Flawlessly Executed Beats a Brilliant Design Sloppily Built

Craftsmanship is the strongest single correlate with perceived visual quality in the VisAWI model (Moshagen & Thielsch, 2010). Users cannot articulate why a polished interface feels trustworthy, but they punish sloppiness instantly. Every blurry image, inconsistent radius, and missing hover state erodes credibility.

## Pixel-Perfect Alignment

Enforce the >90% grid alignment rule from the `layout-spatial-structure` skill. Misalignment of even 1px between adjacent elements is visible at retina resolution.

**Debug technique:** Add `outline: 1px solid rgba(255,0,0,0.3)` to all elements temporarily. Misaligned edges become obvious.

## Image Quality

| Rule | Requirement |
|------|-------------|
| **Resolution** | All images must be >=2x rendered resolution (e.g., 800px image for a 400px container) |
| **Format priority** | AVIF > WebP > JPEG (use `<picture>` with fallbacks) |
| **Hero image budget** | <=300KB after compression |
| **Lazy loading** | All images below the fold use `loading="lazy"` |
| **Aspect ratio** | Always specify `width` and `height` attributes to prevent CLS |

## Shadow Elevation System

Use layered box-shadows for realistic depth. Single-layer shadows look flat and artificial. Define exactly 5 levels and use them consistently.

| Level | Name | Use Case | Box-Shadow |
|-------|------|----------|-----------|
| 0 | Flat | Inline elements, flush cards | `none` |
| 1 | Card | Cards, tiles, raised surfaces | `0 1px 2px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.1)` |
| 2 | Dropdown | Dropdowns, popovers, tooltips | `0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06)` |
| 3 | Modal | Modals, dialogs, drawers | `0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05)` |
| 4 | Popover | Floating toolbars, command palettes | `0 20px 25px rgba(0,0,0,0.1), 0 8px 10px rgba(0,0,0,0.04)` |

**Rule:** Higher elevation = larger offset + larger blur + lower opacity. Never use a single heavy shadow.

## Border-Radius System

Define 3-4 radius values. Use them everywhere. Never invent ad-hoc values.

| Token | Value | Use |
|-------|-------|-----|
| `--radius-sm` | 4px | Badges, tags, inline code |
| `--radius-md` | 8px | Cards, inputs, buttons |
| `--radius-lg` | 12px | Modals, large containers |
| `--radius-full` | 9999px | Avatars, pills, toggles |

**Nested radius rule:** When an element with border-radius contains a child with border-radius, the inner radius = outer radius - padding. A card with `border-radius: 12px` and `padding: 8px` gives children `border-radius: 4px`.

## Interactive States

Every interactive element must have visible hover, focus, and active states.

| State | Implementation |
|-------|----------------|
| **Hover** | Color shift, subtle scale, or shadow lift |
| **Focus** | Visible focus ring (2px solid, offset 2px) — see `accessibility-inclusive-design` for full focus rules |
| **Active** | Slight scale-down (`transform: scale(0.98)`) for tactile feedback |

For transition timing, easing, and `prefers-reduced-motion` rules, see the `visual-interest-expression` skill which owns motion design guidelines.

## Icon Consistency

Use a single icon library per project. Mix outlined and filled icons deliberately: outlined for navigation, filled for active/selected states. Maintain consistent stroke weight (1.5px or 2px) and size (20px or 24px grid). Never mix icon sets from different libraries.

## Loading, Empty, and Error States

**Skeleton screens** beat spinners for loads of 1.5-10 seconds. Match the skeleton to actual content shape. Use a left-to-right shimmer animation at a 1.5s cycle (Bill Chung research: perceived as faster than pulsing).

**Empty states** must include: illustration or icon + heading + description + primary CTA. Never show a blank page.

**Error states** must include: what went wrong + what the user can do + a retry action.

## Cumulative Layout Shift (CLS)

Target CLS < 0.1 (Google Core Web Vitals "good" threshold).

| Cause | Fix |
|-------|-----|
| Images without dimensions | Always set `width` and `height` attributes |
| Web fonts causing FOUT | Apply `font-display` strategy (see `typography` skill for web font loading rules) |
| Dynamic content injected above fold | Reserve space with `min-height` or use `content-visibility: auto` |
| Ads or embeds without reserved space | Set explicit container dimensions before content loads |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Pixelated or blurry images | Signals amateur quality | Serve >=2x resolution in AVIF/WebP |
| Single heavy box-shadow | Looks like a drop shadow from 2010 | Use layered shadows with multiple values |
| Inconsistent border-radius (4px here, 6px there, 10px elsewhere) | Subtle discord that feels "off" | Define 3-4 tokens, use them everywhere |
| No hover or focus states | Interactive elements feel dead | Add transition on every clickable element |
| Flash of unstyled text (FOUT) | Layout jumps, text reflows | Apply web font loading rules (see `typography` skill) |
| Spinners for everything | No spatial context during loading | Use skeleton screens matching content shape |

## Cross-Media Notes

- **Presentations:** Use sharp, high-resolution images only. Maintain consistent shape treatments (all rounded or all square, never mixed). Align all elements to a slide grid.
- **CVs/Resumes:** Alignment precision matters more than decoration. Ensure consistent margins, bullet alignment, and font sizing. A well-aligned minimal CV beats a decorated misaligned one.
- **Documents:** Consistent formatting (heading sizes, paragraph spacing, list indentation) is the document equivalent of UI craftsmanship. Define styles once, apply everywhere.

## Examples

Working implementations in `examples/`:
- **`examples/shadow-system-and-states.md`** — Complete elevation system with layered shadows, skeleton screen implementation, and empty state component in CSS/Tailwind/React

## Review Checklist

When reviewing or building for craftsmanship:

- [ ] Grid alignment passes >90% rule (see `layout-spatial-structure` skill)
- [ ] All images are >=2x rendered resolution and served in AVIF/WebP with JPEG fallback
- [ ] Hero images are <=300KB after compression
- [ ] All images have explicit `width` and `height` attributes
- [ ] Shadow system uses exactly 5 levels with layered (multi-value) box-shadows
- [ ] Border-radius uses 3-4 defined tokens only — no ad-hoc values
- [ ] Nested border-radius follows the outer - padding rule
- [ ] All interactive elements have hover, focus, and active states
- [ ] Transition rules applied (see `visual-interest-expression` skill for timing and easing)
- [ ] Icons come from a single library with consistent stroke weight and size
- [ ] Loading states use skeleton screens matching content shape (not generic spinners)
- [ ] Empty states include illustration + heading + description + CTA
- [ ] CLS < 0.1: no images without dimensions, no dynamic injection above fold
- [ ] Web font loading follows `typography` skill rules (`font-display`, preloading)

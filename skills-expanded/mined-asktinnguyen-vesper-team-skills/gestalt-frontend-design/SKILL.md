---
name: gestalt-frontend-design
description: "This skill should be used when building, reviewing, or improving frontend UI components to ensure perceptually correct layouts grounded in Gestalt psychology. It applies when generating React/Tailwind/shadcn code for forms, dashboards, navigation, modals, chat interfaces, agent UIs, settings pages, data displays, or any layout where visual grouping, hierarchy, and clarity matter. Also use when auditing existing UI for spacing inconsistencies, poor contrast, missing containers, or cognitive overload."
---

# Gestalt Frontend Design

Apply Gestalt perceptual psychology to produce frontend interfaces that are visually organized, cognitively efficient, and accessible. This skill transforms generic AI-generated UI into perceptually intentional layouts by enforcing the principles humans use to parse visual information.

## When This Skill Activates

- Building any React + Tailwind + shadcn/ui component or page layout
- Reviewing or refactoring existing UI for clarity and visual organization
- Designing chat interfaces, agent dashboards, or AI-native UIs
- Generating forms, data tables, navigation, modals, settings pages, or card layouts
- Auditing spacing, contrast, grouping, or visual hierarchy

## The Seven Principles (Quick Reference)

| Principle | Rule | Violation Signal |
|-----------|------|-----------------|
| **Proximity** | Related items closer together than unrelated items | Spacing is uniform or random across groups |
| **Similarity** | Same-function elements share visual treatment | Buttons/badges/links use same color for different purposes |
| **Common Region** | Grouped content enclosed in a visual boundary | Related items float without card, background, or border |
| **Figure-Ground** | Primary content clearly separated from background | Flat appearance, no depth hierarchy, low contrast |
| **Continuity** | Eye follows a clear directional flow | Misaligned elements, broken reading paths |
| **Closure** | Incomplete indicators suggest the whole | No truncation hints, no progress indication |
| **Pragnanz** | Simplest possible form for the content | Decorative complexity without information purpose |

## Spacing Decision Tree

To select spacing values, walk this tree top-down:

```
Label/helper for its adjacent input?
  YES --> space-y-1 or space-y-2 (4-8px)

Sibling in the same logical group?
  YES --> space-y-3 or space-y-4 (12-16px), or gap-3/gap-4

Different group within the same section?
  YES --> space-y-6 or space-y-8 (24-32px), consider Separator

Different section entirely?
  YES --> space-y-10 to space-y-16 (40-64px), heading + Separator
```

**Critical ratio**: Within-group spacing must be at most half of between-group spacing. Minimum 2:1 ratio, prefer 3:1.

## Container Decision Tree

To determine whether content needs a visual boundary:

```
Content group must stand out from surroundings?
  YES --> Card (bg + border + rounded + shadow)

Content group needs subtle differentiation?
  YES --> Background only (bg-muted rounded-lg p-4)

Temporary overlay (modal, popover, command palette)?
  YES --> Dialog/Popover with dimmed overlay (figure-ground)

Switching between views?
  YES --> Tabs (similarity for triggers, common region for panels)

Expandable/collapsible content?
  YES --> Accordion (closure principle)

None of the above?
  --> Proximity spacing alone (no container needed)
```

## Layout-Type Decision Matrix

| Building... | Apply These Principles | Key Patterns |
|-------------|----------------------|--------------|
| **Form** | Proximity, Similarity, Common Region | 3-tier spacing (label/field/section), Card container, consistent inputs |
| **Dashboard** | Common Region, Similarity, Proximity, Figure-Ground | Cards per widget, equal grid for equal-weight data, elevated primary metrics |
| **Navigation** | Similarity, Figure-Ground, Continuity | Shared styling for all items, active state distinguished, horizontal/vertical flow |
| **Modal/Dialog** | Figure-Ground, Proximity, Closure | Overlay dims background, tight internal grouping, clear action buttons |
| **Chat/Conversational** | Proximity, Common Region, Continuity, Closure | Turn spacing > intra-message spacing, tool containers, streaming indicators |
| **Agent Dashboard** | Similarity, Common Fate, Proximity, Figure-Ground | Color-coded status, synchronized animations, stable card positions |
| **Data Table/List** | Similarity, Proximity, Continuity | Consistent row styling, tight rows with wider section gaps, column alignment |
| **Settings Page** | Proximity, Common Region, Similarity, Continuity | Section groups in Cards, consistent toggle/input styling, vertical flow |
| **Code/Developer UI** | Similarity, Closure, Figure-Ground, Continuity | Semantic syntax colors, collapsible regions, diff highlighting, inline suggestions |
| **Cards/Grid** | Common Region, Symmetry, Similarity | Equal-width grid for equal weight, consistent card structure, border/background |

## Quantifiable Constants

### Spacing Scale (Tailwind)
- `gap-1`/`gap-2` (4-8px): Within-group (label-to-input, icon-to-text)
- `gap-3`/`gap-4` (12-16px): Between items in a group (form fields, list items)
- `gap-6`/`gap-8` (24-32px): Between groups (form sections, card clusters)
- `gap-12`/`gap-16` (48-64px): Between major page sections

### Contrast (WCAG)
- Normal text: 4.5:1 minimum (AA), 7:1 enhanced (AAA)
- Large text (18pt+): 3:1 minimum
- UI components: 3:1 minimum
- Dark mode elevation: progressively lighter surfaces (`gray-900` < `gray-800` < `gray-700`)

### Animation Timing
- Micro-interactions (toggle, checkbox): 100ms
- Small transitions (button state, tooltip): 150-200ms
- Component transitions (modal, dropdown): 200-300ms
- Upper limit for any UI animation: 500ms
- Common fate rule: grouped elements share identical duration, easing, and direction

### Density Tiers
| Tier | Inner Gap | Outer Gap | Use Case |
|------|-----------|-----------|----------|
| Compact | 4px | 8-12px | Data tables, dense dashboards |
| Default | 8px | 16-24px | Standard interfaces |
| Comfortable | 12-16px | 24-32px | Reading-heavy, onboarding |

## Post-Generation Quality Gate

After generating any UI, verify each principle passes:

| # | Principle | Check | Pass Criteria |
|---|-----------|-------|---------------|
| 1 | **Proximity** | Related items closer than unrelated? | Within-group spacing <= 0.5x between-group spacing |
| 2 | **Similarity** | Same-function elements share treatment? | Identical color/size/shape for same-role elements |
| 3 | **Common Region** | Grouped content has a boundary? | Card, background, or border encloses each group |
| 4 | **Figure-Ground** | Primary content distinguished from bg? | 2+ contrast tiers; overlays dim background |
| 5 | **Continuity** | Flow guides the eye correctly? | Left-to-right or top-to-bottom reading path intact |
| 6 | **Closure** | Incomplete content hints at more? | Ellipsis, "Show more", chevrons, progress dots |
| 7 | **Pragnanz** | Layout is minimal for its content? | No decorative elements without information purpose |

If any gate fails, fix before presenting the component.

## Accessibility Cross-Check

Every visual Gestalt cue must have a semantic equivalent:

| Visual Cue | Semantic Equivalent |
|-----------|-------------------|
| Proximity grouping | `<fieldset>`, `<section>`, `role="group"`, `aria-labelledby` |
| Color similarity | Redundant shape/icon/text cue (never color alone) |
| Figure-ground contrast | WCAG contrast ratios met; `aria-current`/`aria-selected` for prominence |
| Common fate (motion) | `prefers-reduced-motion` respected; essential motion preserved, decorative removed |
| Continuity (visual flow) | DOM order matches visual order; `tabindex` only for genuine corrections |
| Closure (implied content) | Explicit labels for screen readers; `aria-expanded` for collapsibles |

## Anti-Patterns to Catch

1. **Random spacing** -- arbitrary px values (13, 17, 22) instead of scale tokens
2. **Color overload** -- same branded color for buttons, badges, and decorations
3. **Flat hierarchy** -- no shadow/contrast difference between layers
4. **Orphan elements** -- items outside any visual group or container
5. **Closure starvation** -- carousel with <15% next-item visibility, skeleton that does not match content shape
6. **Similarity drift** -- same component type with inconsistent border-radius, padding, or font weight
7. **Excessive minimalism** -- stripping affordances (borders, underlines) until clickable items are invisible

## Reference

For detailed code examples, rationale, and good-vs-bad patterns per use case, read `references/reference.md` in this skill directory. Consult it when:

- Implementing a specific layout type (form, dashboard, chat, agent UI, etc.)
- Needing concrete React + Tailwind + shadcn/ui code patterns
- Wanting the Gestalt rationale behind a specific design decision
- Reviewing dark mode, responsive, or motion-specific considerations

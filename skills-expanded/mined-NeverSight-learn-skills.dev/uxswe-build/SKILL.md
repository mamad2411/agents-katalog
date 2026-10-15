---
name: uxswe-build
description: Build UI components and screens that hold up under review — layout, spacing, type scale, color and contrast, component anatomy, full state coverage, and accessibility affordances. Use when writing or restyling any interface code (React, Vue, Svelte, HTML/CSS, SwiftUI, native), building a component or screen, setting up a design system or tokens, or when a UI was built and looks generic, cramped, or unfinished. Also use when asked to make something "look better" or match a design.
---

# uxswe-build

Craft patterns for building interfaces. This skill is about *how to build the
thing well* — it does not score or critique. To review something already built,
use `uxswe-evaluate`.

## The method

Work in this order. It is ordered by what is expensive to change later.

1. **Establish the systems before the components.** Spacing scale, type scale,
   and color roles are decisions that every component inherits. Picking them per
   component is what produces interfaces that look assembled rather than
   designed. If the project already has tokens, a theme file, or a component
   library, read it first and conform — do not introduce a second system.
2. **Build the component's anatomy.** Structure and hierarchy first, then
   spacing, then color and emphasis last. Color is the weakest tool for
   establishing hierarchy and the first one people reach for.
3. **Cover every state.** A component is not done at its success state. Empty,
   loading, error, partial, disabled, and overflow are part of the component,
   not follow-up work. This is the single most common source of defects found in
   review.
4. **Wire the accessibility affordances as you go.** Focus order, labels,
   contrast, target size, and keyboard operation are cheap while writing the
   component and expensive to retrofit.
5. **Check it against the real content.** Longest plausible string, empty list,
   one item, a hundred items, the narrowest supported viewport.

## Reference material

Load only what the current task needs — these are detailed and cost context.

| File | Load when |
|---|---|
| `references/layout-and-spacing.md` | placing anything: spacing scale, alignment, grouping, density |
| `references/type-scale.md` | setting type: scale, weight, line height, measure, hierarchy |
| `references/color-and-contrast.md` | choosing color: palette roles, semantic color, contrast ratios |
| `references/visual-hierarchy.md` | the thing looks flat, busy, or nothing stands out |
| `references/component-anatomy.md` | building a specific component and its variants |
| `references/state-coverage.md` | any component that loads, fails, or can be empty |
| `references/accessibility-affordances.md` | interactive elements, forms, focus management |

## Rules that override taste

These are not stylistic preferences and should not be traded away for visual
effect:

- **Contrast minimums are requirements**, not targets. Attractive low-contrast
  text is a defect.
- **Every interactive element is keyboard operable** and shows a visible focus
  state. Removing focus outlines without replacing them is a defect.
- **Every input has a programmatically associated label.** A placeholder is not
  a label.
- **Destructive actions are confirmable or reversible.** Prefer undo over a
  confirmation dialog where the action can be reversed.
- **Nothing conveys meaning by color alone.**

## What not to do

- Do not invent a new spacing or type scale when the project has one.
- Do not add animation, gradients, or shadows to compensate for weak hierarchy.
  Fix the hierarchy.
- Do not build only the happy path and leave states as `TODO`.
- Do not copy a visual style from a reference without checking it against the
  content the component will actually hold.

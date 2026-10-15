---
name: layout-convergence
description: "Use when a Figma screen is already mostly rebuilt with the right components, but still needs screenshot-aligned spacing, background ownership, auto-layout cleanup, hug-fill fixes, or container-level polish without reopening component selection. Trigger for requests such as 'make it match the screenshot', 'fix spacing', 'clean up auto layout', 'adjust backgrounds', 'make the section structure right', or 'polish the containers'."
disable-model-invocation: false
---

# Converge Layout Without Reopening Component Choice

Use this skill after the main component and token choices are already mostly correct, but the screen still drifts from the screenshot in spacing, container ownership, or auto-layout structure.

This skill is for convergence work, not for choosing a new design system family. Keep component semantics stable unless a structural bug proves the current choice cannot represent the screenshot.

Load first:
- `figma-use` before any `use_figma` write call
- [figma-generate-design](../figma-generate-design/SKILL.md) when the screen came from screenshot reconstruction
- [apply-design-system](../apply-design-system/SKILL.md) when the screen is an existing migration or reconnection pass

## Use This Skill For

- section and page spacing still drifting from the screenshot after the main rebuild is done
- gaps that became wrong after converting a frame to auto-layout
- backgrounds or surfaces bound to the wrong node in the hierarchy
- wrapper, container, or content-surface cleanup that should not change component families
- hug versus fill mistakes that cause clipped text, oversized frames, or empty vertical space

## Do Not Use This Skill For

- selecting new design system components from the library
- broad migration of detached layers onto a design system
- creating new reusable library components or variants
- fixing text override failures that are still unresolved at the display-path level

## Core Principle

Fix hierarchy before offsets.

If spacing looks wrong, first decide whether the wrong node owns the gap, padding, fill, or sizing mode. Do not keep nudging numbers on a structurally wrong frame tree.

## Convergence Workflow

### 1. Lock The Semantic Scope

Before editing, confirm these are already correct or intentionally accepted:
- the component family used for each major UI element
- the visible wording and text ownership
- the background token family
- the overall section list and order

If one of those is still unresolved, switch back to the upstream skill instead of using this one.

### 2. Audit Ownership By Layer

For each drifting section, identify four ownership layers:
1. page wrapper
2. section container
3. content wrapper or repeated-items stack
4. component instance internals

For each visible problem, assign it to exactly one owner:
- section-to-section distance belongs to the page wrapper
- header-to-body or body-to-footer distance belongs to the section container
- repeated tile/card/row spacing belongs to a dedicated inner stack
- surface fills belong to the wrapper that visually owns that surface
- component internals keep their published library styling unless the component itself is the screenshot surface

### 3. Normalize Auto Layout Before Pixel Tuning

Use this structural definition of done:
- the page wrapper uses auto-layout when the screen is a vertical or horizontal stack
- each major section container uses auto-layout if it represents a logical grouping
- section containers are usually vertical `HUG` on height unless the screenshot clearly requires a fixed height
- children only use `FILL` after they are appended into an auto-layout parent that can resolve fill behavior
- repeated items live in their own stack frame instead of sharing the outer section gap
- no detached helper text, empty wrappers, or absolute-position leftovers remain in the active section footprint

### 4. Apply Token Binding At The Right Layer

Use this priority order:
1. page background token on the outer page wrapper
2. section background token on the section container
3. card or content-surface token on the inner wrapper
4. component internals unchanged unless the component itself owns that semantic surface

Do not override a component's internal fills just because it was the easiest node to reach.

### 5. Tighten Screenshot Alignment In Small Passes

Make one kind of structural adjustment at a time:
- gap ownership
- padding ownership
- hug/fill sizing
- background ownership
- section height cleanup

After each pass, take a targeted screenshot of the changed section. Do not batch unrelated sections into one large polish script.

## Known Convergence Patterns

### Section Gap Versus Tile Gap

Symptom:
- fixing the section gap makes the header spacing right but the repeated tiles too loose, or vice versa

Fix:
- keep the outer section gap for logical blocks only
- create a nested stack for repeated tiles or rows
- move the repeated items into that stack and tune that stack's gap independently

### Background On The Wrong Node

Symptom:
- the right color is present somewhere, but the visible section still feels wrong or the component had to be overridden internally

Fix:
- move the bound token up to the wrapper that visually owns the background
- keep library component internals unchanged unless the screenshot proves the component itself is the surface

### Hug Or Fill Drift

Symptom:
- too much empty space, clipped text, or fixed-height sections after auto-layout conversion

Fix:
- switch section containers to vertical `HUG` when the content should define height
- use horizontal `FILL` only where the parent layout should stretch the child
- re-check clipping and spacing after the sizing change before adjusting any pixel offsets

## Validation Checklist

After each convergence pass, verify:
- the component families did not change unintentionally
- the intended node owns each visible background and spacing relationship
- repeated items have their own stack where needed
- section heights and wrapper heights are `HUG` where appropriate
- no duplicate detached labels or wrappers remain
- the section screenshot is closer to the reference than before the pass

If a pass would require changing component family, variant semantics, or text display-path logic, stop and return to the upstream reconstruction or migration skill.
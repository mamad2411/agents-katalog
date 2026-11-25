---
name: dpai-craft
description: Polish and implement visual details in DesainPakeAI Canvas HTML, including surfaces, radii, icons, imagery, interaction states, and motion. Use when an active DesainPakeAI page or component needs UI polish, visual consistency, state refinement, or more intentional interaction feedback. Requires the DesainPakeAI Canvas HTML and MCP authoring contract; use dpai-layout for composition and dpai-writing for interface copy.
---

# DPAI Craft

Polish comes from a pile of small details that compound. This skill is the reference for which are worth having and what values they take.

When reviewing, slow the interface down. What feels off at 10% speed is what is subtly wrong at full speed.

Keep the project's registered components, tokens and density, and match its motion language except where a rule below prescribes an exact interaction.

Every duration, curve, scale and blur below is a specific value, not a range to approximate. `cubic-bezier(0.2, 0, 0, 1)` is not `cubic-bezier(0.4, 0, 0.2, 1)`, and `0.96` is not `0.95`. Use what is written.

This skill owns visual text rendering, hit areas, focus, control semantics, reduced motion, surfaces, icons and interaction polish. Grouping, composition, section spacing, breakpoints and spatial RTL belong to `dpai-layout`. The words themselves belong to `dpai-writing`.

## Canvas HTML workflow

Read [the Canvas HTML contract](references/canvas-html.md) before any source mutation. It overrides every React, Tailwind, Motion, or framework-specific snippet in the reference files. Use [Canvas craft recipes](references/canvas-recipes.md) for dependency-free implementations of the most common patterns.

1. Call `get_project_context` and retain the returned revision.
2. Read `get_guide` with topic `desainpakeai-mcp-instructions`. For a substantial visual change, also read `design-quality`.
3. Use `grep`, `read_file`, `get_tokens`, and `get_design_context` to find the selected node, component contract, and reusable tokens.
4. Use `create_component`, `create_layout`, or `create_page` for new registered modules. Never edit the manifest directly.
5. Make one partial `edit_file` mutation per coherent visual or interaction group, using the latest revision each time.
6. Preserve stable props, component IDs, node IDs, parts, actions, and bridge behavior.
7. Run `verify_preview` after the page is complete, inspect all affected states, then call `finish_working_on_pages`.

Treat review-only requests as read-only. Do not mutate until the user asks to implement.

If Canvas MCP is unavailable or the repository has not authorized its use, do not initialize it. For a review, inspect the available source and safe read-only context, label rendered, runtime, and MCP-backed checks `Not verified`, and never imply that source inspection covered them. For an implementation that requires Canvas mutation, stop and report that the Canvas MCP connection or authorization is required; do not bypass the authoring contract with unrelated filesystem edits.

## Concentric border radius

Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes an interface feel off. Radius, shadow and outline recipes are in [surfaces.md](references/surfaces.md).

## Optical over geometric alignment

When geometric centering looks off, align optically. Buttons with icons, play triangles and asymmetric icons all need a manual nudge.

## Shadows for elevation, borders for structure

Where a border exists only to create depth, prefer layered transparent `box-shadow` values. Keep borders that communicate structure or state: dividers, separators and selected or focus states.

## Interruptible animations

Use CSS transitions for interactive state changes, because they can be interrupted mid-animation. Reserve keyframes for staged sequences that run once.

## Split and stagger enter animations

For an infrequent staged entrance where sequence communicates hierarchy, break the content into semantic chunks and stagger them by ~100ms. Animating one container gets you less for the same cost. Leave high-frequency interactions unstaggered. See [enter-exit.md](references/enter-exit.md).

## Subtle exit animations

Use a small fixed `translateY` rather than full height. Exits should be softer than enters. Use `ease-out` for both directions.

## Contextual icon animations

Animate icons with `opacity`, `scale` and `blur` rather than toggling visibility. Use exactly these values: scale `0.25` to `1`, opacity `0` to `1`, blur `4px` to `0px`.

Canvas modules have no motion library. Keep both icons in the DOM with one absolutely positioned, and cross-fade them with CSS using `cubic-bezier(0.2, 0, 0, 1)`. Scope state to the component root and update it through delegated JavaScript. The reference comparison is in [icon-transitions.md](references/icon-transitions.md); always use its CSS path in Canvas HTML.

## Image outlines

Give images a `1px` outline at low opacity for consistent depth. Pure black in light mode (`oklch(0 0 0 / 0.1)`), pure white in dark (`oklch(1 0 0 / 0.1)`). Never a near-black like slate or zinc and never a tinted neutral. A tinted outline picks up the surface underneath and reads as dirt on the image edge.

## Scale on press

A `scale(0.96)` on click gives a button tactile feedback. Always `0.96`; anything below `0.95` feels exaggerated. Use a bounded `data-motion="static"` variant where motion would distract. See the [CSS recipe](references/animations.md#scale-on-press); framework recipes are non-Canvas reference only.

## Skip animation on page load

Keep state-transition entrances off the first render. Add an initialization state only after the component is ready, and enable later transitions from that state. Do not animate a control merely because the document loaded.

## Suppress transitions on theme switch

A theme flip changes color, background, border and shadow on nearly every element at once. Every transition on those properties fires together and the switch smears instead of snapping. Scope a temporary transition-suppression state to the Canvas document root, force a reflow, then remove it on the next frame. See the [plain JavaScript recipe](references/animations.md#suppress-transitions-on-theme-switch).

## Transition only what changes

Always name the exact CSS properties: `transition-property: scale, opacity`. Never use `transition: all`.

## Use `will-change` sparingly

Only for `transform`, `opacity` and `filter`, which the GPU can composite. Never `will-change: all`. Add it when you see first-frame stutter, not before. See [performance.md](references/performance.md).

## Match icon stroke to text weight

An icon next to text carries the text's optical weight: `1.5px` stroke beside regular (400) text, `2px` beside semibold (600). One stroke weight per icon set and one icon library per surface. Use the workspace's supported Iconify element when appropriate. Sizing and RTL flipping are in [icons.md](references/icons.md).

## One SVG, recolored per state

Icons use `currentColor` and take hover, selected and disabled states from CSS color and opacity, never from separate assets. Outline is the default variant; fill marks the active state.

## Motion restraint

Give high-frequency interactions instant feedback, or a transition of `150ms` or less on opacity and color. A custom animation there charges its attention cost on every trigger.

Every animated state change also needs a static cue: color, an icon, or a label. Motion is never the only feedback channel.

## Before you finish

| Mistake | Fix |
| --- | --- |
| Icons look off-center | Nudge optically with padding, or fix the SVG |
| Jarring staged entrance or exit | Stagger infrequent entrances; keep exits subtle |
| Theme toggle crossfades the whole page | Disable transitions for the swap, force a reflow, restore on the next frame |
| `transition: all` on elements | Specify exact properties |
| First-frame animation stutter | Add `will-change: transform` (sparingly) |
| Hairline icon beside bold text | Match the stroke width to the text weight |

## Reporting

**Severity.** `HIGH` breaks an interaction, makes motion unusable, or leaves a state change visible only while the animation runs. `MEDIUM` is a visible inconsistency in surfaces, icons, or motion. `LOW` is isolated polish.

**Verification.** Run `verify_preview`. Inspect every state the component defines: hover, focus, active, disabled, loading, empty, error and selected where present. Read motion durations and easings from the source, confirm reduced-motion behavior, and inspect the rendered Canvas. Replay motion slowly when browser tooling permits. Report every check you could not run as `Not verified`.

**Format.** Group findings under the principle each violates, ordered by severity, one row per root cause listing every location it appears in:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

`Location` is `path/to/file:line`. `Why` names the principle and the user impact.

End with `Block` when any `HIGH` remains, `Approve` otherwise, leaving the rest in the table as work to do. Never `Approve` coverage you did not inspect. With nothing to report, state "No actionable UI-polish findings" and report verification.

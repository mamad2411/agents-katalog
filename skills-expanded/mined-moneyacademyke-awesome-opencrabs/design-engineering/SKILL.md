---
name: design-engineering
description: Umbrella skill for distinctive frontend design, UI polish, Apple-style fluid interaction, animation vocabulary lookup, and strict motion review. Use when building or reviewing UI, choosing visual direction, naming an animation effect, tuning gestures/springs, or auditing motion quality.
---

# Design Engineering

One front door for interface craft. This skill merges the useful parts of:

- `frontend-design` — distinctive subject-grounded visual direction
- `emil-design-eng` — UI polish, component feel, animation taste
- `apple-design` — direct manipulation, fluid gestures, springs, materials
- `review-animations` — strict motion review standards
- `animation-vocabulary` — exact names for vague motion effects

Use the narrowest mode that matches the user's request. Do not dump every mode into every answer.

## Mode router

| User intent | Mode | What to do |
|---|---|---|
| "Design/build this page/component" | Visual direction | Create a subject-grounded design plan before coding; avoid generic AI defaults |
| "Make this UI feel better/polished" | Craft polish | Improve details: states, feedback, spacing, typography, copy, motion restraint |
| "Gesture/sheet/drag/swipe/spring/material" | Fluid interaction | Apply Apple-style direct manipulation, interruptibility, velocity handoff, and material hierarchy |
| "Review this animation/motion code" | Motion review | Use a strict findings table and approval/block verdict; load `../review-animations/STANDARDS.md` when exact values are needed |
| "What's it called when…" | Vocabulary lookup | Return the precise motion term first, then 1–2 close alternates only if useful |

## Shared principles

- **The interface must have a point of view.** Generic polish is still generic. Ground choices in the product's subject, audience, content, and job.
- **Taste is trained.** Compare against great interfaces, not against default component-library output.
- **Unseen details compound.** Press states, transform origins, timing, copy, spacing, focus, and reduced-motion all add up.
- **Beauty is leverage.** A tool people enjoy using has an advantage; decoration without purpose is just glitter in the gears.
- **Motion serves orientation, feedback, continuity, explanation, or delight.** If it cannot name its job, delete or reduce it.
- **Direct manipulation beats scripted animation.** Anything touchable should respond immediately, track continuously, carry velocity, and be interruptible.

## Visual direction mode

Use when creating new UI or reshaping an existing one.

1. Pin down the concrete subject, audience, and page/component job. If the brief is vague, make a reasonable explicit choice.
2. Build a compact design plan:
   - **Color:** 4–6 named hex values tied to the subject.
   - **Type:** display, body, and utility roles; avoid generic font pairing unless the brief demands it.
   - **Layout:** one-sentence layout concept; use structure to encode real information, not decoration.
   - **Signature:** one memorable element that could only belong to this product.
3. Self-critique against common AI design defaults:
   - warm cream + serif + terracotta
   - near-black + acid accent
   - broadsheet hairlines + dense columns
   Use these only when the brief truly earns them.
4. Spend boldness in one place. Cut decoration that does not serve the thesis.
5. Build responsively, with keyboard focus, good contrast, and reduced-motion support.

## Craft polish mode

Use when asked to make UI feel better.

Check:

- **Responsiveness:** controls react on press/pointer-down, not after lag.
- **State clarity:** loading, success, error, empty, disabled, hover, active, focus, and selected states are intentional.
- **Copy:** plain verbs, user-side language, consistent action names, helpful errors.
- **Motion:** frequent actions get little or none; occasional actions can animate; rare moments may delight.
- **Perceived performance:** fast feedback and well-timed skeletons/spinners matter.
- **Component physicality:** popovers originate from triggers, buttons depress, lists preserve continuity.

When reviewing UI code, prefer a table:

| Before | After | Why |
|---|---|---|
| `transition: all 300ms` | `transition: transform 180ms var(--ease-out)` | Bound the animated property and keep it on the compositor |

## Fluid interaction mode

Use for gestures, sheets, drag/swipe, spring animation, momentum, materials, and Apple-style physical interfaces.

Non-negotiables:

1. **Kill latency.** Feedback starts immediately, ideally on pointer-down.
2. **Track 1:1.** Dragged content follows the pointer continuously and respects grab offset.
3. **Make it interruptible.** Users can grab, reverse, or retarget motion mid-flight.
4. **Animate from the current presentation value.** No jumps from stale target state.
5. **Hand off velocity.** A release animation starts with the user's release velocity.
6. **Project momentum.** Pick snap targets from projected endpoint, not merely release point.
7. **Use springs for touchable things.** Default to critically damped; add bounce only when momentum earns it.
8. **Respect spatial consistency.** Enter and exit along coherent paths; origin belongs to the trigger.
9. **Use materials with hierarchy.** Blur/translucency should separate layers, not wreck legibility.
10. **Honor reduced motion.** Tone down movement while preserving orientation and feedback.

Useful defaults:

| Interaction | Default |
|---|---|
| Button press | `100–160ms`, small scale down |
| Tooltip/popover | `125–200ms`, origin-aware, ease-out |
| Dropdown/select | `150–250ms`, no sluggish ease-in |
| Modal/drawer/sheet | `200–500ms`, spring or strong ease-out |
| Frequent keyboard action | no animation |

## Motion review mode

Use when reviewing animation or motion code. Default to flagging; approval is earned.

Required output:

1. **Findings table** with `Before | After | Why` columns.
2. **Verdict** grouped by impact tier.
3. Explicit decision: **Block** or **Approve**.

Block on sight:

- `transition: all`
- `scale(0)` entrances
- `ease-in` on UI interactions
- animation on keyboard/high-frequency actions
- UI duration over `300ms` without justification
- wrong `transform-origin` on trigger-anchored elements
- keyframes for rapidly retriggered/gesture-driven motion
- layout-property animation (`width`, `height`, `margin`, `padding`, `top`, `left`)
- missing `prefers-reduced-motion` on movement
- ungated hover motion on coarse pointers

When exact values or deeper criteria are needed, read:

`~/.opencrabs/skills/review-animations/STANDARDS.md`

## Vocabulary lookup mode

Use when the user asks what an animation/effect is called.

Output shape:

`**Term** — Definition.`

If several terms could fit, list the best match first, then close alternates with one-line differences.

Common terms:

| Description | Term |
|---|---|
| Items animate one after another | **Stagger** |
| Popover grows from its trigger | **Origin-aware animation** |
| iOS overscroll resistance/snap-back | **Rubber-banding** |
| Same element travels between views | **Shared element transition** |
| Shape smoothly turns into another | **Morph** |
| Element follows drag then carries speed | **Momentum** / **Velocity handoff** |
| Motion can be redirected mid-flight | **Interruptible animation** |
| Content revealed by clipping/masking | **Reveal**, **Clip-path**, or **Mask** |
| Digits roll/count upward | **Number ticker** |
| Continuous horizontal text/content loop | **Marquee** |

For the full glossary, use the legacy `animation-vocabulary` skill content if needed.

## Tool/use guidance

- For implementation: explore with `glob`/`grep`/`read_file`, edit with `edit_file`, test with native commands.
- For substantial UI changes: use `plan` before editing.
- For visual verification: use browser/screenshots if available.
- For motion review: cite files/lines when possible; do not give vibes-only approval.
- For accessibility: always check focus, contrast, pointer modality, and reduced-motion.

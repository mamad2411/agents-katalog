---
name: animation-design-planner
description: Plan interactive UI animations before implementation with visible motion contracts, lifecycle ownership, accessibility/performance guardrails, and proof gates
type: planning
version: v0.1
required_conventions: [alignment-page]
invocation: orchestrator
argument-hint: "[component, interaction, animation bug, or motion brief]"
visual_tier: prototype
---

# Animation Design Planner

Invoke as `$animation-design-planner`.

Use this skill when a user asks to create, change, debug, or polish an interactive UI animation, transition, or multi-component motion sequence. This is a planning and proof skill, not a direct implementation skill: it prevents local timing tweaks from starting before the visible sequence, lifecycle owner, state phases, and proof method are named.

Use it for drawers, modals, popovers, cards, route transitions, list reordering, shared-element illusions, mount/unmount choreography, staggered content, and visual regressions such as flashing, popping, jumping, duplicated layers, or broken close/open sequencing.

For generated video, Remotion timelines, or non-interactive animation, produce only the transferable storyboard/timing and proof expectations, then route execution to the relevant video or media skill when available. Do not expand this skill into a full video-production workflow yet.

## Workflow

1. **Identify the motion surface**
   - Name the component, route, screen, or interaction being planned.
   - Identify the trigger: click, hover, focus, drag, route change, async state, mount, unmount, reorder, or error/recovery state.
   - Read the relevant local component, style, animation, and test files when the user is asking about an existing codebase.
   - Treat ambiguous requests such as "smooth this out" or "fix the animation" as requests to define the visible sequence before implementation.

2. **Write the visible motion contract**
   - Define the start state and end state in visible user terms.
   - State what the user should see at each transition boundary.
   - Name what must never happen: flash, pop, jump, duplicate, clipped content, stale layer, focus loss, scroll jump, layout shift, or incorrect z-order.
   - Define accepted interruption behavior: repeated clicks, quick close after open, route away, async data arrival, resize, reduced-motion preference, or component unmount.
   - Define the focal point and continuity target: what should keep the user's eye anchored.

3. **Storyboard the timeline**
   - Break the motion into phases or key frames with approximate timing, easing, and visible state per phase.
   - Mark focal element, supporting elements, continuity/shared elements, and any staggered content.
   - Include anticipation, follow-through, or settling only when it improves comprehension rather than decoration.
   - For shared-element or layout illusions, state which element is visually continuous and which elements are entering, exiting, or temporarily hidden.
   - Keep the storyboard implementation-neutral until the lifecycle ownership map is clear.

4. **Map lifecycle ownership**
   - Assign one explicit owner for any multi-component sequence. This can be a page-level controller, state machine, reducer, parent component, or animation coordinator.
   - Name every state-machine phase. Use phase names that describe visible lifecycle, such as `closed`, `opening`, `drawer-open`, `closing-collapse`, `sheet-exiting`, `layout-morph-out`, and `sealed`.
   - Map which component owns mount/unmount, visibility, identity, focus, layout measurement, and callbacks for phase completion.
   - Define stable keys and identity rules. State which key must persist through exit and which key may change only after the exit or morph is complete.
   - Define callback handoff points: animation complete, exit complete, layout measurement ready, focus restored, overlay dismissed, or state cleared.
   - If ownership is split across siblings without a named coordinator, stop and redesign the ownership map before proposing timing changes.

5. **Choose implementation guardrails**

   **Framework detection and routing:** detect which animation framework the codebase uses, then route to the appropriate framework subskill for framework-specific guardrails. Detection order:
   - Grep for `framer-motion` or `motion` in package.json / imports → route to `$animation-design-planner frameworks/motion-framer`
   - Grep for `gsap` in package.json / imports → route to `frameworks/gsap` subskill
   - Grep for `@angular/animations` → route to the appropriate Angular animation subskill when available
   - Grep for `three` or `@react-three/fiber` → route to `frameworks/threejs` subskill
   - Grep for `element.animate(` or Web Animations API usage → route to `frameworks/web-animations-api` subskill
   - Grep for CSS `@keyframes`, `transition:`, `animation:` in stylesheets → route to `frameworks/css-transitions` subskill
   - If multiple frameworks detected or ambiguous, ask the user which framework to target
   - If no subskill exists for the detected framework, use the baseline guardrails below

   **Baseline guardrails (all frameworks inherit these):**
   - Prefer transform and opacity animation. Avoid animating layout, paint, filter, shadow, or expensive size properties unless the plan names the cost and proof.
   - Define reduced-motion behavior for interaction-triggered motion. Nonessential motion must be suppressed or converted to instant/fade behavior when the user prefers reduced motion.
   - Specify focus management, pointer-event behavior, scroll locking, z-index/layering, and content clipping rules when they affect the motion.

6. **Define the proof gate**
   - Write acceptance checks tied directly to the visible motion contract.
   - Include slow-motion or debug-duration review steps for sequencing.
   - Include Playwright screenshot or video capture when feasible, especially for close/open sequences, shared-element motion, drawer/modal transitions, and regression-prone visual states.
   - Include reduced-motion verification.
   - Include manual review steps for what automated screenshots cannot prove, such as perceived continuity, focal attention, and interruption feel.
   - State the exact proof artifacts expected before the implementation is considered done.

7. **Hand off implementation only after the plan**
   - If the user asked only for planning, stop with the plan and proof gate.
   - If the user asked for implementation too, make the implementation step conditional on the plan and proof gate. Then write the implementation plan and proof gate as the routing contract, or name the appropriate implementation skill when one owns the work.
   - For bug-fix requests, route to `$investigate --ui` only after this skill has named the visible motion contract and likely lifecycle owner, unless the bug is a crash or data issue.

## Output

Produce a structured animation plan with these sections:

- **Visible Motion Contract:** trigger, start state, end state, expected user-visible sequence, focal point, continuity target, forbidden artifacts, and accepted interruption behavior.
- **Storyboard / Timeline:** phases or key frames, timing, easing, focal element, supporting elements, shared elements, stagger, anticipation, follow-through, and settling.
- **Lifecycle Ownership Map:** single sequence owner, state phases, component mount/unmount responsibilities, stable key rules, identity persistence, callback handoffs, focus/scroll responsibilities, and interruption handling.
- **Implementation Guardrails:** framework-specific guardrails (from the routed subskill), reduced-motion behavior, transform/opacity-first performance constraints, layout/paint risks, layering, and pointer/focus rules.
- **Proof Gate:** slow-motion/manual review steps, Playwright screenshot or video capture plan where feasible, reduced-motion verification, regression checks, and acceptance checklist tied to the visible motion contract.
- **Implementation Handoff:** whether implementation is ready, blocked, or should be represented by an approved task artifact, `$investigate --ui`, or another owner skill.

End with:

```md
**Next work:** <specific implementation, investigation, or review step>
**Recommended next command:** <one command or "none">
```

## Constraints

- Do not start by tweaking durations, easing constants, CSS classes, or Motion props before the visible motion contract, lifecycle owner, state phases, and proof method are named.
- Do not propose a multi-component animation without one lifecycle owner or explicit state-machine coordinator.
- Do not clear identity, active item state, or stable keys before exit, shared layout, or close-morph phases have completed.
- Do not rely on "looks better" as proof. Tie proof to visible contract acceptance checks and concrete artifacts.
- Do not ignore reduced-motion behavior for interaction-triggered motion.
- Do not use layout/paint-heavy animation properties as the default path. Prefer transform and opacity unless the plan justifies and proves otherwise.
- Do not create or modify GitHub Actions workflows.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/animation-design-planner-{topic}.html`.

## Default Shipping Contract

- This skill is planning-first. Normally it should not mutate implementation files directly.
- If the user explicitly asks this skill to create or modify tracked files, finish by committing and pushing all intended changes to the repository primary branch (`main` when present, otherwise `master`) before stopping.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, production deploy confirmation, paid actions, or public visibility changes.

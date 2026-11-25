---
name: orbyn-scripted-motion
description: "Write scripted web motion: timelines, scroll-linked scrub and pin scenes, Flip layout transitions, split text, drag with inertia, framework cleanup and reduced motion. Targets the GSAP engine. Use when the project ships it or CSS cannot meet the need. Not for deciding what moves."
---

# Scripted motion

Follow the consuming project's instructions and requested scope; use the
[portable defaults](../orbyn-workflow/references/project-policy.md) only where guidance is missing.

Guidance targets GSAP 3.15 (`gsap`, plus `@gsap/react` for React). The engine is a
means, not a default; this skill only covers writing it well.

## Decide first

1. **CSS first.** State changes, enter/exit, one-shot sequences and native
   scroll-driven timelines belong to CSS or WAAPI. Read
   [motion](../orbyn-ui-design/references/motion.md) and
   [animation performance](../orbyn-ui-design/references/animation-performance.md)
   before adding script.
2. **Use the engine when** the project already depends on it, or the user chooses
   it for a need CSS meets poorly: long choreographed sequences with seek or
   reverse, scrubbed or pinned scroll scenes, Flip across layout changes, split
   text, drag with inertia, motion along a path.
3. **A new dependency is the project's decision.** Propose it, wait for install
   approval, never add it silently, and never recommend it unprompted.

## Licence boundary

GSAP is free, including commercial use and all plugins, under its
[standard "no charge" licence](https://gsap.com/standard-license), but it is not open
source. Its prohibited uses include building tools that let people create visual
animations without code in competition with Webflow's visual animation builder.

- Do not use it inside a visual, no-code animation builder product. Stop and
  report; pick another engine or native CSS.
- Never vendor, paste or copy library code into this skill library or a project
  tree; install the package. Only the MIT-licensed gsap-skills text is adapted here.

## Rules that always apply

- **Project tokens.** Take durations and curves from the project's motion tokens;
  register them once (`gsap.defaults`, named eases) instead of literals per tween.
- **Reduced motion.** Wrap setup in `gsap.matchMedia()`; the
  `(prefers-reduced-motion: no-preference)` branch animates, the other lands in the
  final state at once, still operable.
- **Compositor properties.** Animate `x`, `y`, `scale`, `rotation`, `opacity`
  (`autoAlpha` to also drop hit-testing). Not `width`, `height`, `top`, `left`.
- **Cleanup.** Every tween, timeline, ScrollTrigger and listener is created inside a
  scope that is reverted on unmount: `useGSAP`, or `gsap.context()` / `matchMedia`
  with `revert()`. Run client-side only (no SSR calls).
- **Sequence in a timeline**, not chained `delay`s. Place steps with the position
  parameter and labels; put `scrollTrigger` on the timeline or a top-level tween,
  never on a child.
- **Interruption.** Reversal retargets from the live value; use `overwrite: "auto"`
  or kill the previous tween rather than stacking.
- **Final state first.** Layout, focus and semantics work without the script.

## Read when the task needs it

- Timelines, position parameter, defaults, stagger, tokens:
  [timelines](references/timelines.md).
- Scroll scrub, pin, snap, batch, horizontal scenes, refresh:
  [scroll](references/scroll.md).
- React, Vue, Svelte, vanilla lifecycle and cleanup:
  [frameworks](references/frameworks.md).
- Flip, SplitText, Draggable, Inertia, Observer, ScrollTo, MotionPath, SVG:
  [plugins](references/plugins.md).
- Helpers (`gsap.utils`), `quickTo`, jank and many-element cost:
  [utilities and performance](references/performance.md).

## Handoffs

- What motion should exist, and its purpose: [orbyn-ui-design](../orbyn-ui-design/SKILL.md).
- Copying a reference's measured motion: [motion-match](../motion-match/SKILL.md).
- Code-only films and illustrations stay dependency-free
  ([technical-illustration](../technical-illustration/SKILL.md)); its check bans this
  engine on purpose. Faux product UI: [product-illustration](../product-illustration/SKILL.md).

## Source

Adapted from GreenSock, gsap-skills, MIT, at
[commit aed9cfd](https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760);
the licence text is in `references/gsap-skills-LICENSE.txt`. Restructured and
rewritten with Orbyn's rules; the upstream "recommend by default" stance is dropped.

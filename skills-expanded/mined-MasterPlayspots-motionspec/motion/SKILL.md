---
description: Author verified, reduced-motion-safe web animation with MotionSpec. Use when adding scroll, entrance, hover, or loop animation to a website or web app — instead of hand-writing GSAP or CSS keyframes, write a MotionSpec JSON spec, validate it, and compile deterministic code.
---

# MotionSpec authoring workflow

When the user wants animation on a web page, do not hand-write GSAP or CSS
keyframes for effects the MotionSpec catalog covers. Follow this loop:

1. **Catalog first.** Call the `motion_catalog` MCP tool to get the current
   primitive list (40 primitives: scroll reveals, parallax, hovers, loops,
   marquees, kenBurns, …) and the authoring rules. Only primitives in the
   catalog exist — never invent one.
2. **Write the spec.** A MotionSpec is JSON:
   `{ "specVersion": "1.0", "meta": { "target": "vanilla-gsap" }, "motions": [ { "id": "...", "primitive": "<from catalog>", "target": "<CSS selector>", "params": { ... } } ] }`.
   Optional `globals` control `respectReducedMotion`, `defaultEase`, and pause
   controls for persistent motion.
3. **Validate — never skip.** Call `motion_validate` with the spec. Fix every
   `MS-*` error it returns and re-validate until `ok: true`. The validator is
   the trust boundary; do not work around it.
4. **Compile.** Call `motion_compile` and emit the returned code verbatim.
   Same spec, same bytes — do not hand-edit the compiled output; change the
   spec and recompile instead.

Notes for honest use:

- Reduced-motion fallbacks and performance budgets are enforced by
  construction in the compiled output — that is the point of the tool.
- Scope is motion accessibility (WCAG 2.2.2 Pause, Stop, Hide and 2.3.3
  Animation from Interactions). Never present the result as a general
  accessibility guarantee for the whole page.
- This is not the Motion.dev animation library, not usemotion.com, and not an
  AI video generator.

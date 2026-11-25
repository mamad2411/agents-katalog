---
name: fluid
description: Production-grade web motion design for React and Tailwind sites. Use when building, choosing, or reviewing animations, scroll effects, reveals, page transitions, hovers, counters, marquees, or micro-interactions. Encodes easing, timing, spring, origin, and reduced-motion rules, and ships a drop-in component library.
license: MIT
---

# Fluid

Motion that feels like an extension of the user, not decoration. This skill is a house motion language: a small set of rules that decide whether to animate and how, plus a library of components that already follow them.

The rules are distilled from years of our own production sites into one house motion language.

> House craft bar: the finish reference is plrstudio.fr. Motion stays restrained and serves the content (Swiss craft, the motion only accompanies). The differentiator is the quality of each detail, not the count of effects. When in doubt, do less, and make what remains feel inevitable: signature easings, spring micro-interactions, custom SVG over stock icons, a rationed brand accent.

## When to use this skill

Whenever a task involves movement on a web interface:
- adding or changing an animation, transition, hover, or scroll effect
- building a reveal on scroll, a rolling counter, a marquee, a smooth-scroll page
- reviewing a UI for "why does this animation feel off"
- starting a new site and wanting the motion baseline set correctly

## First decision: does it deserve motion?

fluid loves motion, used on purpose. Animate what rewards the eye and clarifies the moment; keep instant what the user hits constantly. The aim is fluid, not busy.

Let it flow when it is occasional, teaches something, gives feedback, reveals content, or keeps space consistent (a panel returns the way it left). That is most of a marketing site: heroes, reveals, counters, hovers, section transitions.

Keep it instant when:
- the interaction happens many times a day (menus, list rows, repeated hovers)
- it is triggered by the keyboard or by a tool the user runs to go fast
- it adds nothing to clarity, feedback, or spatial understanding

If you keep one line: frequent means instant, everything else gets to flow.

## The rules (apply by default)

Timing
- Frequent micro-interactions stay fast: hovers, presses, selects around 150 to 250ms. Reveals, heroes, and ambient motion can run longer (600ms and up) when deliberate.
- Animate `transform` and `opacity` for anything that moves often (GPU-cheap, smooth). Avoid animating layout (width, height, top, margin), and prefer naming the properties over a blanket `transition: all`.

Easing
- `ease-out` for almost everything that enters or exits. It feels responsive.
- `ease-in-out` for elements that move or morph while staying on screen.
- `ease-in` suits exits more than enters; for enters use `ease-out`.
- `linear` only for marquees, hold-to-confirm, and 3D rotation.
- Prefer the house signature curves over browser defaults: `--out: cubic-bezier(0.22, 1, 0.36, 1)` for enters, exits, and hovers (the default), `--fr: cubic-bezier(0.27, 0, 0.51, 1)` for on-screen morphs and position changes, `--spring: cubic-bezier(0.34, 1.4, 0.5, 1)` for a gentle overshoot. The `Reveal` component uses a slightly stronger expo variant `cubic-bezier(0.16, 1, 0.3, 1)` for large section reveals. Full set in `reference/easings-and-durations.md`.

Springs (anything gesture-driven or that should feel physical)
- Think in damping and response, never in duration.
- Default to no overshoot. Add bounce only when the motion carried momentum.
- The house rolling counter uses `stiffness 120, damping 20`.

Details that separate good from great
- Press feedback: `scale(0.97)` on `:active`, around 150ms.
- Never animate from `scale(0)`. Start near `0.93` so it grows, instead of materialising from nothing.
- Make scaling origin-aware. Popovers grow from their trigger: use the library transform-origin variable (Radix, Base UI), not the center.
- If an animation still feels wrong after fixing easing and timing, add `filter: blur(2px)` across the transition.
- Do not delay repeated tooltips. Delay the first, make the rest instant.

Accessibility (non negotiable)
- Every motion must honour `prefers-reduced-motion`: disable inertia and parallax, snap counters to their final value, freeze ambient canvases on the first frame. Every component here already does this. Keep it that way.

## Workflow

1. Decide if it should move at all (section above). If not, stop.
2. Pick the smallest tool: a CSS transition for a hover or press, a scroll-linked reveal for sections, a spring for anything gesture-driven or physical.
3. Reach for a component below before writing new motion. When you do write new motion, follow the recipes in `reference/motion-craft.md`.
4. Set easing and duration from the rules. transform and opacity only.
5. Add the reduced-motion path in the same change, not later.
6. Review against `reference/anti-patterns.md` before calling it done.

## Component library

Drop-in, dependency-light, all reduced-motion safe. Files in `components/`. Stack: React 19, framer-motion, lenis, Tailwind v4.

- `SmoothScroll` + `ScrollContext`: one weighted Lenis instance feeding a single shared velocity and progress value to the whole page. The biggest single lever for the premium feel. `lerp 0.09`, `duration 1.1`, native fallback under reduced motion.
- `ScrollProgress`: a 2px reading-progress hairline that reuses the shared progress value at zero extra scroll cost.
- `Reveal`: opacity and `y: 24` on scroll into view, expo-out, fires once. The default way to bring sections in.
- `Odometer`: per-digit rolling counter, springs to its value on view, locale-aware grouping, tabular figures.
- `AmbientField`: soft brand-tinted blobs drifting on additive blend behind a hero. Pure canvas, no deps, paused off screen, frozen under reduced motion, gradients cached.
- `Marquee` (+ `marquee.css`): infinite linear scroll for logos or tickers, the one correct use of `linear`. Pauses on hover, freezes under reduced motion.

## Detector (deterministic guardrail)

Run `detector/detect.mjs` to scan code for these anti-patterns automatically, with no API calls. It is the fast, measurable, anti-generic check.

```bash
node detector/detect.mjs src          # or bun; folders or files
node detector/detect.mjs --json src   # for CI
node detector/detect.mjs --strict src # exit 1 on warnings too
```

It flags the motion smells above (`transition: all`, layout animation, `ease-in`, `scale(0)`, long durations, dated bounce, missing reduced-motion) and the generic-look tells (Inter/Roboto/Arial as a primary font, the purple gradient, pure black, emoji icons, Aceternity/Magic UI/21st template signatures shipped verbatim, and the display fonts generations converge on: Space Grotesk, Geist, Plus Jakarta Sans). Suppress a line with `fluid-disable-line`, configure via `fluid.config.json`. Rules live in `detector/rules.mjs`, extend them as the house ruleset grows. Run it before calling any UI change done.

## Reference (load when needed)

- `reference/easings-and-durations.md`: the full easing map, custom curves, duration table.
- `reference/motion-craft.md`: implementation recipes (text blur reveal, pointer physics, number roll, spring discipline, stagger), all reduced-motion safe. Read this when you write new motion.
- `reference/principles.md`: the motion principles behind the rules, condensed.
- `reference/anti-patterns.md`: the review checklist. Seed of a future deterministic detector.

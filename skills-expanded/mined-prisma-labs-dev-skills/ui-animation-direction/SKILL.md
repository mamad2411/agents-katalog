---
name: ui-animation-direction
description: High-bar guidance for creating UI animation across CSS, native platform primitives, and animation libraries. Use when the task involves transitions, micro-interactions, page motion, scroll effects, motion polish, or raising the animation quality bar so the result does not feel sloppy or generic.

license: MIT
---

# UI Animation Direction

Use this skill when the job is not just "make it animate" but "make the motion
feel intentional, clear, and worth keeping."

This skill is library-agnostic. It applies whether the implementation uses:

- native CSS transitions or keyframes,
- Web Animations API,
- an established app/library abstraction,
- Motion, GSAP, or another animation library,
- platform-native animation primitives in a product-specific stack.

## Core Rule

Animation should clarify state, hierarchy, continuity, feedback, or mood.

If the motion mainly proves that animation was added, the bar is too low.

## What Good Looks Like

High-bar UI animation tends to be:

- specific about what changed and why,
- consistent across related states,
- quieter than the first draft,
- accessible under reduced-motion settings,
- fast enough to feel responsive,
- memorable because of fit and intent, not because it is loud.

## Workflow

### 1. Identify the job of the motion

Before coding, name the purpose:

- state change,
- interaction feedback,
- navigation continuity,
- hierarchy and staging,
- scroll-linked context,
- atmosphere and tone.

If you cannot name the job, do not add animation yet.

### 2. Choose the right implementation surface

Prefer the smallest surface that fits the job:

- simple hover, focus, press, opacity, transform, or reveal:
  native CSS is usually enough
- imperative sequencing or timeline choreography:
  Web Animations API or the project's existing abstraction
- React layout transitions, gestures, shared-element motion, or exit presence:
  use the project's chosen animation library
- if a repo already uses Motion, GSAP, or another animation layer:
  prefer the established stack over introducing a new one

For selection guidance, load `references/implementation-patterns.md`.

### 3. Implement the smallest correct motion first

Start with:

- one transition,
- one easing family,
- one clear before/after state,
- no decorative extras.

Prove that the motion helps the interaction before layering on orchestration,
stagger, blur, parallax, or springiness.

### 4. Review the result as a motion system

Once it works, review:

- rhythm,
- hierarchy,
- state clarity,
- restraint,
- accessibility,
- repeated-use feel.

Load `references/review-rubric.md` for the review pass.

### 5. Raise the bar by cutting before adding

The most reliable way to improve animation quality is often:

1. reduce travel distance,
2. normalize timing,
3. remove one unnecessary effect,
4. preserve the one motion that communicates the interaction.

Load `references/opinionated-guide.md` for the preferred subset and default
biases.

## Default Biases

- Prefer transform and opacity over layout-thrashing properties.
- Prefer layout-aware transitions over blanket fade-ins.
- Prefer one motion family per surface over many unrelated timings.
- Prefer restrained hover/press motion over novelty.
- Prefer continuity over spectacle for navigation and layout changes.
- Prefer official library docs when exact API behavior matters.

## Avoid By Default

- animating everything on first load
- generic fade-and-scale on every card, section, and modal
- long, floaty durations that make the UI feel slow
- springs with bounce that do not match the product tone
- parallax or scroll effects added as decoration with no structural purpose
- CSS transitions and JS animation systems fighting each other

## Reduced Motion Is Not Optional

Any animation work must preserve a coherent reduced-motion path.

That does not mean removing all feedback. It means keeping clarity while
reducing travel, scale, parallax, and other motion-heavy effects.

## When To Load References

### Load `references/opinionated-guide.md` when:

- you want the preferred subset and defaults
- the work is routine product UI animation, not exploration
- you want to know what to reach for first and what to avoid

### Load `references/implementation-patterns.md` when:

- deciding between CSS, WAAPI, and a library
- choosing how to implement hover, layout, navigation, or scroll motion
- a project already has an animation stack and you need to fit into it

### Load `references/review-rubric.md` when:

- the animation is implemented and needs a quality pass
- the result feels technically correct but aesthetically weak
- you need a final gate before considering the work done

### Load `references/reference-links.md` when:

- you need canonical docs or API references
- you need up-to-date CSS, Motion, accessibility, or examples material
- you want the plain documentation alongside this opinionated guide

## Relationship To Library Skills

This skill is not a library reference.

Use it alongside library-specific skills when needed:

- if the repo uses Motion, pair this with the `motion` skill
- if the stack uses another library, consult that library's official docs
- keep this skill as the bar-raising and decision layer

## Output Expectation

When this skill is triggered, the final animation work should usually show:

- a clear reason for the motion,
- an implementation that fits the existing stack,
- restraint in timing and effect choice,
- reduced-motion handling,
- a brief quality pass against the review rubric.


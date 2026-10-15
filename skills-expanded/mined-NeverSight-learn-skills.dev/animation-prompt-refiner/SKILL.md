---
name: animation-prompt-refiner
description: Use when a user describes motion, animation, scroll behavior, product visuals, transitions, or cinematic UI direction in rough language and wants the request turned into a clearer, production-ready prompt or storyboard. Especially useful for landing-page animations, Figma/Rive/Lottie briefs, scroll-driven sections, interaction choreography, and metaphor-to-motion translation.
---

# Animation Prompt Refiner

Transform vague motion requests into clear animation briefs the agent can execute.

## Workflow

1. Identify the actual job:
   - `concept`: visual metaphor or object language is unclear.
   - `storyboard`: motion beats need ordering.
   - `runtime`: Figma, Rive, Lottie, CSS/SVG, video, or canvas choice matters.
   - `implementation`: code needs concrete timings, progress ranges, and states.

2. Rewrite the prompt into this structure:
   - **Intent**: what the animation should communicate.
   - **Objects**: visible objects, marks, assets, and constraints.
   - **Scene State**: start, middle, final, idle.
   - **Motion Vocabulary**: timing, easing, path, transitions, continuity.
   - **Trigger**: page load, hover/focus, timed loop, scroll-scrubbed, pinned scroll.
   - **Timeline**: percentages or timestamps.
   - **Constraints**: exclusions, reduced motion, responsive behavior, asset accuracy.
   - **Acceptance Checks**: visual and behavioral checks before sign-off.

3. Preserve user intent, but remove ambiguity:
   - Convert “make it premium” into measurable motion traits: slow cadence, low amplitude, no jitter, no bouncy easing, clean holds.
   - Convert “animate as I scroll” into scroll-scrubbed progress with pinned section behavior and reversible state.
   - Convert “not abstract” into named objects and literal object transformations.
   - Convert “use references” into specific visual traits to match.

4. Push back when the requested format conflicts with the goal:
   - Video is weak for reversible scroll-scrubbed object state.
   - Lottie is weaker for interactive state machines than Rive.
   - Figma prototypes are useful for keyframes, not as production animation runtimes.

## Required Output Shape

When refining a prompt, output:

```markdown
**Refined Prompt**
[production-ready prompt]

**Why This Works**
[brief rationale]

**Execution Notes**
[tools/runtime assumptions, if relevant]
```

If the prompt is for implementation, include a timeline table:

| Progress | Visual State | Motion Notes |
| --- | --- | --- |
| 0-10% | ... | ... |

## Core Terms

Use the vocabulary in `references/motion-vocabulary.md` when choosing words.
Load it when the user asks for a full prompt rewrite, animation storyboard, or motion-system direction.

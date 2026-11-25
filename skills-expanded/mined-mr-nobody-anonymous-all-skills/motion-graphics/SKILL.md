---
name: motion-graphics
description: "Create motion graphics: keyframe and easing curves, typography in motion, shape and mask animation, expressions for procedural motion, and template handoff."
type: procedural
category: video
domain: video
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - after effects expressions
  - motion graphics easing
  - animated typography
  - shape layer animation
  - motion graphics template handoff
keywords:
  - motion-graphics
  - after-effects
  - expressions
  - easing
  - typography
  - keyframes
source: custom
enabled: true
---

# Motion Graphics

## Purpose

Create motion graphics: keyframe and easing curves, typography in motion, shape and mask animation, expressions for procedural motion, and template handoff.

## When to Use

- An explainer, title sequence or lower-third set must be animated.
- A client needs a template they can edit themselves.
- Animation must match brand timing and typography rules.

## When NOT to Use

- A static graphic is enough.
- The task is 3D character animation.
- The output is interactive UI motion, which belongs in code or a design tool.

## Capabilities

- Animate with deliberate easing rather than linear keyframes.
- Control typography (tracking, leading, kinetic emphasis) in motion.
- Use shape layers, masks and track mattes for reveals.
- Write expressions for procedural motion and reusable rigs.

## Inputs

- The brand guidelines (fonts, colours, logo clear space).
- The script/storyboard and target duration.
- Delivery: video file, or a template with editable text.

## Workflow

1. Storyboard the timing before animating.
2. Build one master comp with reusable precomps and controlled fonts.
3. Animate with ease curves; check motion at 100% speed, not frame-by-frame only.
4. Use expressions for repetition instead of hundreds of keyframes.
5. Template it (essential graphics/controls), then test editing it as a non-designer would.

## Tools

- After Effects / Cavalry / Blender
- expression editor
- ffmpeg for previews

## Examples

- `ffmpeg -i graphics.mov -vf fps=12 preview.mp4`
- `allskills explain video/motion-graphics --query "easing curves"`
- `allskills route "animate a lower third"`

## Safety

- Linear keyframes read as mechanical; ease every transition deliberately.
- Missing fonts on another machine reflow the whole template.
- Recompress previews repeatedly before final delivery and quality degrades.

## Source

All-Skills canonical library (`skills/video/motion-graphics`). First-party skill, maintained in this repository.

## Notes

- Fewer, better-eased keyframes beat many hand-tweaked ones.
- Templates need a test pass by someone who did not build them.
- Pairs with: `video/video-editing-workflow`, `video/color-grading`.

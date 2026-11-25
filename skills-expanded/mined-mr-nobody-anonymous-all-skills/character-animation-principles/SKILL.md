---
name: character-animation-principles
description: "Animate characters convincingly: key poses and silhouette, timing and spacing, arcs, overlap and follow-through, weight and anticipation, and animation review criteria."
type: procedural
category: 3d
domain: 3d
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - animation principles timing spacing
  - character key poses
  - overlap follow through animation
  - animate a walk cycle
  - animation critique checklist
keywords:
  - animation
  - principles
  - timing
  - arcs
  - walk-cycle
  - posing
source: custom
enabled: true
---

# Character Animation Principles

## Purpose

Animate characters convincingly: key poses and silhouette, timing and spacing, arcs, overlap and follow-through, weight and anticipation, and animation review criteria.

## When to Use

- A character performance must read clearly and feel alive.
- Animation feels floaty, stiff or weightless and needs diagnosis.
- A walk/run/idle cycle must loop seamlessly.

## When NOT to Use

- The task is mechanical rigging with no performance.
- Motion capture already captures the performance and only cleanup is needed.
- The deliverable is a static pose sheet.

## Capabilities

- Plan key poses that read as silhouettes.
- Control timing with spacing rather than more keys.
- Apply overlap, follow-through and arcs to secondary motion.
- Diagnose floatiness, sliding and popping in a cycle.

## Inputs

- The character rig and its control set.
- The action brief: emotion, weight, speed, context.
- Frame rate and the target format (gameplay loop, cutscene, film shot).

## Workflow

1. Block extreme poses first and check the silhouette of each.
2. Set timing with breakdowns and spacing before polishing curves.
3. Add overlap on secondary elements (hair, cloth, props).
4. Verify foot contact and centre-of-gravity for weight.
5. Review at speed and in a loop; fix what reads wrong to a fresh viewer.

## Tools

- Blender/other DCC animation tools
- playblast and reference video
- curve editor

## Examples

- `blender -b char.blend -P render_playblast.py`
- `allskills explain 3d/character-animation-principles --query "floaty animation"`
- `allskills route "animate a walk cycle"`

## Safety

- Foot sliding destroys believability — lock contact before polishing.
- More keys do not fix bad timing; they hide it.
- Cycles must be tested as loops, not played once.

## Source

All-Skills canonical library (`skills/3d/character-animation-principles`). First-party skill, maintained in this repository.

## Notes

- Reference video beats intuition for weight and timing.
- Silhouette readability is the fastest quality check on any pose.
- Pairs with: `3d/blender-rigging-animation`, `video/video-editing-workflow`.

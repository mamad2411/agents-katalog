---
name: narrative-film-direction
description: Guides the process of directing a narrative scene using AI-generated clips — from script to shot list, master shot, coverage setup, screen direction discipline, clip assembly and editing grammar. Use when planning or producing any multi-shot scene with dialogue, action or drama, and when a sequence of clips needs to cut together like a real film rather than a playlist of unrelated images.
license: CC-BY-4.0
version: 1.0.0
---

# Narrative Film Direction

## What this skill is for

Generating individual clips is easy. Making those clips cut together into a coherent scene is the hard part.

This skill covers the directing methodology that sits between "I have a script" and "I have a sequence that plays like a film." It is the complement to `character-continuity` — that skill keeps a character the same person; this skill keeps a scene spatially and temporally coherent.

The core problem is that AI video generators have no world model. Each clip is an independent inference with no knowledge of camera position, the action line, or what was in the previous clip. The result without direction: clips that contradict each other, characters who inexplicably swap sides, eyelines that point at nothing, and edits that feel random. With direction: shots that feel like coverage — as if a camera crew walked around a real location and captured it from considered angles.

---

## The directing sequence

Do these in order. Skipping steps collapses later ones.

**1. Lock the scene geography.** Before generating anything, know the location of every character, the camera working side (which side of the action line the camera stays on), and what lies off-screen in each direction. Sketch an overhead blocking diagram — even a rough text description works. This is the spatial contract every shot must honour.

**2. Write the shot list.** Every setup in the scene, in cutting order. Include: shot type, camera movement, duration, audio mood, transition to next. The worked example in `references/worked-example.md` shows the format.

**3. Generate the master shot first.** The wide establishing shot that shows all characters and the full geography. This is the source of truth — every closer angle must be geometrically consistent with it.

**4. Extract the master keyframe.** Sample a representative frame from the approved master and use it as the reference image for every subsequent setup. This is how you impose geographic consistency across clips that are generated independently.

**5. Build setup frames as stills.** Generate each angle as a still image using the master keyframe as reference. Approve or reject each still before animating. A rejected still costs one generation; a rejected animated clip costs the generation plus the time spent matching continuity to it.

**6. Animate approved stills one action at a time.** One specific action per clip. Static camera unless the movement is the point. Short clips (5–8 seconds) [PRACTITIONER] stitched in the edit, not long takes.

**7. Assemble and cut.** Trim head and tail frames, apply cut-hide technique at joins, match colour across clips, add audio.

Full detail on each step: the reference files below.

---

## The five rules that break most scenes

**1. Never cross the action line.** Every setup must keep the camera on the same side of the line running between the characters (or along a character's direction of movement). Crossing it makes characters appear to swap positions and look at each other from the wrong side.

**2. Specify eyelines numerically.** "Looking at each other" produces inconsistent results. "Gaze 12 degrees camera-left, approximately chin height of a person standing one metre screen-right" produces a consistent eyeline. Degree notation is the working solution — see `references/screen-direction.md`.

**3. Every setup derives from the master keyframe.** Not from a previous close-up. Not from a similar-looking reference. From the master.

**4. One action per clip.** A clip that tries to do two things — walk across the room *and* turn dramatically — usually does one badly. Split it. The edit is free; generation is not.

**5. Change one thing at a time between setups.** Camera position OR shot size OR lens choice — not all three. Multi-variable changes produce diagnostic opacity: you can't tell which change broke the spatial consistency.

---

## Reference files

- `references/shot-grammar.md` — the 8-point shot framework for every prompt
- `references/coverage-protocol.md` — master shot, setup frames, the 5-setup dialogue scene
- `references/screen-direction.md` — 180° rule, eyelines, 30° rule, screen direction
- `references/editing-grammar.md` — cut-hide, J/L-cuts, assembly, colour matching
- `references/worked-example.md` — one scene, end to end, with the actual prompts
- `references/sources.md` — sources, graded by confidence

Read `references/worked-example.md` first — it shows the method running before you read the theory.

Accurate as of August 2026. Clip length limits and camera control UIs change with each model release — verify current values before building a production schedule.

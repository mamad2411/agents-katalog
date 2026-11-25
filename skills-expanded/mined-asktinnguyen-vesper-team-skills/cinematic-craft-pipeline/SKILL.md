---
name: cinematic-craft-pipeline
description: "Orchestrate an end-to-end cinematic production workflow by routing between the specialized cinematic-crew skills. Use when planning a full cinematic scene, sequence, or film, from premise and story structure through character arcs to visual direction, shot lists, master-shots selection, action staging and rhythm, and game-cinematics camera systems. Also use to decide which specialist skill to invoke for a given task and to keep the pieces working together with one consistent language."
---

# Cinematic Craft Pipeline

## Overview

Coordinate the full cinematic crew as one pipeline. This umbrella skill decides the order of work, tells you which specialist skill to open for each stage, and keeps their vocabularies consistent so a finished shot list traces back to the story, characters, and visual intent.

## Workflow

**1. Start from the story.**
Run `$cinematic-story-structure` to lock the premise, genre, beats, sequences, and theme before any visual work. A camera plan without a story decision has nothing to serve.

**2. Design the transformation.**
Run `$cinematic-character-arcs` to define the protagonists and how they change. Every beat the camera emphasizes should connect to a character decision or turn.

**3. Build the visual and shooting plan.**
Run `$cinematic-visual-direction` to analyze scenes, block the space, and produce shot lists, staging, and coverage that the camera team can execute.

**4. Select the camera work.**
Run `$cinematic-master-shots` to choose and combine the specific setups, lenses, and moves for each shot in the list.

**5. For action-heavy sequences.**
Run `$cinematic-action-motion` to choreograph fights, chases, and confrontations: fighting style, staging, motion and rhythm, and genre formula.

**6. For interactive or game output.**
Run `$cinematic-game-cinematics` to translate the plan into real-time camera modes, transitions, occlusion handling, and a game production pipeline.

**7. Review for coherence.**
Trace every shot back to a story beat, a character turn, and a visual intent. Cut anything that does not earn its place; confirm eyelines, the 180-degree line, and editing options hold across the whole plan.

## Routing Rules

- Premise, logline, beat sheet, genre, and theme: `$cinematic-story-structure`.
- Character want and need, arc type, and arc beats: `$cinematic-character-arcs`.
- Scene breakdown, blocking, coverage, shot list, and staging: `$cinematic-visual-direction`.
- Camera setup and move selection per shot: `$cinematic-master-shots`.
- Fight, chase, and confrontation staging plus motion and rhythm: `$cinematic-action-motion`.
- Game and real-time cameras, cut-scenes, and cinematic production: `$cinematic-game-cinematics`.

## References

See `references/route-map.md` for a compact routing table. This skill routes rather than duplicates content: open the relevant specialist `SKILL.md` and its `references/` per the routing rules above. The source books for the family live in `/Users/tinnguyen/s2-narrative/Resources/Books_PDFs/`.

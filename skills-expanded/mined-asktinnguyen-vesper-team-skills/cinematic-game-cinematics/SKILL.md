---
name: cinematic-game-cinematics
description: "Design cinematic sequences and real-time camera systems for games using Mark Haigh-Hutchinson's Real-Time Cameras and Rich Newman's Cinematic Game Secrets. Use when planning game cut-scenes and cineractives, choosing first-person, third-person, or cinematic camera behavior, designing free-look, tracking, look-at, and transitions, applying the Five C's of cinematography to games, managing occlusion and performance, or running a game-cinematics production pipeline from writer and storyboard through cinematography, directing, sound, motion capture, and postproduction."
---

# Cinematic Game Cinematics

## Overview

Treat game cinematics as film craft executed in an interactive medium. A cinematic camera presents a non-interactive view the player does not control; interactive cameras must stay unobtrusive, readable, and responsive while never losing story intent. An ideal virtual camera is one the viewer stops noticing.

## Workflow

**1. Choose the camera mode.**
Decide between first-person (POV), third-person (detached), and cinematic (non-interactive) presentation, and whether the sequence is a cut-scene or a controllable in-game event ("cineractive"). Read `references/camera-modes.md` before committing.

**2. Define the camera behavior contract.**
Specify position, look-at, free-look constraints, tracking or slaving, and collision rules for interactive cameras. Lock down when the player controls the view and when the game seizes it for a cinematic beat, and signal that handoff clearly (for example with an aspect ratio or letterbox change).

**3. Design transitions.**
Plan first-to-third and third-to-first transitions, plus full-screen to split-screen transitions, with position and orientation requirements. A jarring snap of the camera breaks spatial trust; an interpolated, occlusion-safe move keeps it.

**4. Apply the Five C's.**
Working from `references/production-pipeline.md`, apply Mascelli's Five C's adapted to games: camera angles, continuity, cutting, close-ups, and composition (including the rule of thirds and staging). Camera angle choices carry genre and intent, for example a low angle for a small protagonist.

**5. Plan the production pipeline.**
Run the sequence through preproduction (writer, storyboard, concept art, cinematography), production (directing talent, cut-scenes, sound design, motion capture and voiceover), and postproduction in an order that lets planning catch problems before implementation.

**6. Engineer for the medium.**
Resolve occlusion (walls or objects between the camera and subject), navigation, smooth motion and collision, and performance. Budget camera work and keep real-time costs within the engine's rules of thumb; the camera must not fight the player's spatial understanding.

## Camera Language

- First-person cameras are the closest to immersion; third-person cameras must manage the relationship between the avatar and the look-at target.
- Cinematic cameras repeat a consistent view every time; interactive cameras adapt to infinitely variable player actions.
- Occlusion and instant repositioning are the classic failure modes that cripple an otherwise good game; guard against both.

## References

Source materials in `/Users/tinnguyen/s2-narrative/Resources/Books_PDFs/`:

- `Real-Time Cameras A Guide for Game Designers and Developers (Mark Haigh-Hutchinson) (Z-Library).epub`
- `Cinematic game secrets for creative directors and producers inspired techniques from industry legends (Rich Newman) (Z-Library).pdf`

Load `references/camera-modes.md` or `references/production-pipeline.md` as needed.

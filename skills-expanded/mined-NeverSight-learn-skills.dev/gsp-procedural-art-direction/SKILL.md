---
name: gsp-procedural-art-direction
description: "Use when procedural visual identity, shaders, particles, SVG systems, or UI recipes are part of the game deliverable."
---

# Game Procedural Art Direction

## Goal
Make the build visually intentional through programmable systems.

## Use when
- the user explicitly wants procedural art
- the game needs a stronger visual identity to meet the quality target
- the result currently works but looks generic or underdesigned

## Rules
- Treat requested visual style as part of the product, not optional fluff.
- Prefer reusable visual recipes over one-off hacks.
- Protect readability while adding style.
- For polished prototypes, visual direction belongs in scope now, not “later someday.”

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present visual direction decisions in conversation.
- **minimal** or **full**: update `docs/game-studio/spec.md` or `docs/game-studio/ux-flow.md` if visual rules or UI behavior change materially.

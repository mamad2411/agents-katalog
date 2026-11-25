---
name: pose-fragment-unicode-sprite-design
description: "Compose Unicode pose variants by swapping localized fragments so each expression shares the same base silhouette and spacing."
metadata:
  author: ychampion
---

# SKILL: Pose-Fragment Unicode Sprite Design
**Domain:** terminal-ui
**Trigger:** Use when terminal sprite art must support multiple expressions or gestures while staying anchored to the same silhouette and spacing.
**Source Pattern:** Distilled from reviewed fragment-based Unicode sprite and expression-system implementations.

## Core Method
Define the sprite as stable base segments plus a dictionary of overlay fragments keyed by pose. Each pose reuses the same shell and swaps only localized fragments like eyes, hands, or props, so the character can wink, look around, or gesture without altering the immutable silhouette. This makes new expressions cheap to add while preserving alignment with nearby UI.

## Key Rules
- Keep the stable base segments constant across poses and store them separately from movable fragments.
- Store movable fragments in a pose dictionary so new expressions only replace localized strings.
- Preserve spacing around each fragment so pose changes never alter total width or anchor points.
- Provide a default fragment set that remains valid even when a host cannot render the fancier variants.

## Example Application
If a coding assistant banner needs idle, warning, and celebration expressions, store one base body plus separate fragment sets for eyes and arms. The UI can switch expressions instantly without recalculating the whole sprite or disturbing layout.

## Anti-Patterns (What NOT to do)
- Do not generate each pose as a completely separate ASCII block; that invites drift and misalignment.
- Do not tie fragment changes to width or padding changes, or the sprite will stop lining up with surrounding UI.

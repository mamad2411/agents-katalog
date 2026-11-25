---
name: game-action-move
description: Reconciliation demo action skill for movement and body language.
---

# Move Action

Use when the player changes position or uses physical action: stepping aside,
following, leaving, waiting, reaching out, hugging, grabbing, hitting, blocking,
or any similar body-language action.

Movement is flexible, but it is still bounded by the scene. Preserve the exact
action as `player_input` and resolve it as visible behavior. Restrained movement
can create room for dialogue; pressure, grabbing, blocking, or violence should
damage trust and may move toward `pressure_failure`.

Do not convert a physical action into a speech action unless the player also
speaks. If the action is ambiguous, choose the least forceful interpretation
that still respects the player's wording.

---
name: prototype
description: Wire Figma screens into a clickable prototype - interactions, transitions, overlays, flow starting points - and check for dead ends. Use for /layer:prototype.
argument-hint: "[screens or flow]"
disable-model-invocation: true
---

# Prototype

1. `figma_status` with a `title`. Find the screens: the selection, the names the user gave after the command, or `figma_inspect` target "page".
2. Write the flow down first (which element goes where, with which transition) and confirm it in one message.
3. `figma_edit` with `prototype` ops (click / hover / after-delay → navigate, overlay, swap, back; smart-animate for changes between similar screens, push/slide for navigation) and a `flow` op for the starting screen.
4. Check: every screen reachable, every screen has a way back or forward.
5. Tell them how to try it: Figma → Present (▶) from the flow's starting screen.

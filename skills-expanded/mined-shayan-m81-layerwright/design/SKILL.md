---
name: design
description: Design a new screen, state or flow in Figma using the open file's Design System (its components, variables and text styles). Use for /layer:design.
argument-hint: "<what to design>"
disable-model-invocation: true
---

# Design in Figma

What to design is what the user typed after the command; if it's missing or vague, ask one short question first (platform, which screen, what content). Follow the figma-design skill, §4 (Job B):

1. `figma_status` with a `title` (the screen's name).
2. `figma_scan_design_system`, then `figma_get_design_context({ task })` for the relevant components, tokens and text styles. No Design System yet → offer to create the foundations (`figma_foundations`) first.
3. Write one Design Plan for the screen(s): real content, Auto Layout, the file's components by name and variant, tokens instead of raw values.
4. `figma_preview_plan` → fix what it reports → show the summary → `figma_execute_plan`.
5. Critique loop: `figma_export_image` + `figma_analyze_design({ mode: "critique" })`, fix the worst issues, at most three rounds.
6. Report what you made. Offer `/layer:shot`, `/layer:prototype`, or `/layer:code` next.

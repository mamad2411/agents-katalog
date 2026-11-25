---
name: shot
description: Take a picture of the selected Figma layers (or a named frame), save it as a file and show it to the user. Use for /layer:shot, or whenever the user wants to see a Figma frame.
argument-hint: "[frame name]"
disable-model-invocation: true
---

# Picture of the selection

The images Layerwright tools return are visible only to you. To show the user one:

1. `figma_status`; the node is the selection (or the frame named after the command; find its id with `figma_inspect` target "page").
2. `figma_export_image({ nodeId, save: true, scale: 2 })`; the result has `file`, the path of the saved PNG (in `.layerwright/exports/`).
3. Send or show them that file the way this app shows files (an attachment, or a link to the path), plus one line on what it shows.

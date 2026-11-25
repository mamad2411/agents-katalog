---
name: components
description: Turn the selected Figma layers into a reusable component, several components, or one component set with variants and properties. Use for /layer:components.
argument-hint: "[variant property, e.g. State]"
disable-model-invocation: true
---

# Make components

1. `figma_status` with a `title`, then `figma_inspect` target "selection" (`format: "summary"`). Nothing selected → ask the user to select the layers.
2. Decide the shape and say it before doing it: one component; several; or one component set when the layers are states or sizes of one thing (name the property, e.g. State = Default / Hover / Disabled, from what the user typed after the command when given).
3. `figma_edit` with a `componentize` op (`mode: "single" | "multiple" | "variants"`, `variants` per node, `exposeText` for text properties). It works on copies unless they want the originals replaced.
4. `figma_export_image` of the result; report the component names, properties and where they are.

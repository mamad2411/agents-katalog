---
name: code
description: Implement the selected Figma frame (or a named one) in this project's code - React, Vue, HTML/CSS, Tailwind... - with the project's own components, then check it against the design. Use for /layer:code.
argument-hint: "[where in the code, or which frame]"
disable-model-invocation: true
---

# Figma → code

Hints after the command (a path, a route, a framework, a frame name) narrow the job. Follow the figma-design skill, §6 (Job D):

1. `figma_status` with a `title` ("Build <frame> in code"). Take the frame from the selection, or by name. A screen with several breakpoints or states (mobile, empty, error)? List them and ask which ones are in scope.
   - A component, a component set or an instance of one: build the **whole component**, every variant and state in its set (sizes, types, hover, pressed, focus, disabled, loading…), not only the one selected. Read the set (`figma_inspect` → `componentSetId`, `figma_get_design_context` for its properties, `figma_export_image` of the set), list the variants in a table, and map each property to a prop or a CSS/ARIA state, as figma-design §6 says. The same goes for each component the screen uses that the code doesn't have yet.
2. `figma_inspect({ format: "plan" })` for the structure; `figma_get_design_context` for tokens and text styles.
3. `code_scan_components`, then confirm the mappings with the user (Figma component → code component) and save them with `code_mapping({ action: "set" })`. Don't guess a component or a data field: ask.
4. Implement with the mapped components and the project's tokens; exact sizes and spacing from the design.
5. Check: `code_verify_usage({ file, planId })`, and compare the running page with the frame (measure or screenshot). For a component, show every variant on one page (a story or preview route) and compare each with its Figma variant. Fix every difference you find, then report what is left, variant by variant.
6. Tell the user which files changed and how to see the page.

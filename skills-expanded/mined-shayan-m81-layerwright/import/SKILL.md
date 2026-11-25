---
name: import
description: Bring an HTML file, a folder of pages, or a Claude Design export into Figma as editable layers with Auto Layout, text styles and the file's own components. Use for /layer:import.
argument-hint: "<file.html | folder | export>"
disable-model-invocation: true
---

# HTML → Figma

The source is what the user typed after the command. Follow the figma-design skill, §3 (Job A). In short:

1. `figma_status` with a `title` ("Import <name>"). Not connected → say how to connect and stop.
2. No path given → look for `.html` files or a Claude Design export folder in the project; ask which one when there are several.
3. `figma_scan_design_system`, so the import reuses the file's components and styles.
4. Editable copy (the default): `import_html_to_plan({ path })` → show the summary (screens, what maps to which component) → `figma_execute_plan({ planId })`.
   Pixel-exact copy, when they ask for one: `figma_import_html({ file })`.
   A folder of icons or pictures (no HTML): `figma_import_assets({ paths: [folder] })` (`components: true` for SVG icons as components).
5. If the file has a Design System: `figma_analyze_design({ target, mode: "sync" })` → show the groups → apply what they agree to.
6. Check it with your own eyes: `figma_export_image({ nodeId, compareWith: { html: path } })`; fix large differences.
7. Report what was built and on which page. Offer `/layer:shot` to see it.

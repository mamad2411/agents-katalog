---
name: docs-diagram-build
description: 'Design a legible architecture, deployment, infrastructure or data-flow diagram from the bundled template. Use when a diagram improves the requested explanation. RU: схема архитектуры, диаграмма.'
---

# Architecture diagrams

Use for a compact system or infrastructure diagram when it improves the requested explanation or deliverable. Establish audience, scope, canonical source of components and connections, intended format and how much detail matters. Separate observed relationships from hypotheses; do not invent architecture to fill an attractive layout.

Show components, ownership or trust boundaries, and direction or type of important flows. Make labels and a legend sufficient without relying on color alone. Keep the legend outside unrelated boundaries and route connectors so they do not obscure component labels. Avoid crossing lines and overlapping boundaries; inspect readability at the intended screen, print or export size. Choose the output format and style for the user's use case and available tools; do not impose a specific theme or technology.

An optional starting point is the dark-themed standalone page [template](templates/template.html) with inline SVG, a grid background and color-coded component types. Resolve its location through the current runtime's plugin interface and copy it to the requested output path; never edit it in place. It is a style choice, not a requirement. It loads the JetBrains Mono web font from Google Fonts, so remove that `<link>` and rely on the monospace fallback when the page must work offline or without external requests, and replace the `[PROJECT NAME]` placeholders. The template is derived from third-party MIT-licensed work; keep [its notice](templates/NOTICE.md) with any redistributed copy of the template itself.

For a standalone artifact, preserve requested portability and accessibility: verify text alternatives, contrast, dimensions, external resources and actual rendering to the extent applicable. Report unsupported or unverified connections and checks. Publish or modify a live system only if separately authorized.

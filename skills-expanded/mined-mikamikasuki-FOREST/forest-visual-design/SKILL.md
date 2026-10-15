---
name: forest-visual-design
description: Build and review FOREST themes, typography, layout, and reusable UI components in the running application. Use for visual changes; scientific figures and manuscript evidence require domain integrity checks too.
---

# FOREST visual design

Create a restrained scientific workspace with sage accents, readable neutral surfaces, precise typography, and subtle glass on navigation and temporary chrome. The graph, real results, and manuscript supply the product's identity. Avoid promotional copy, invented content, dashboard-template card grids, excessive green backgrounds, and ornamental hero sections.

Read [the visual system and review rubric](references/visual-rubric.md) when choosing tokens or reviewing a major surface. Inspect affected `apps/web/src/styles.css`, `ui.tsx`, and feature CSS at current HEAD before designing replacements.

## Set a coherent direction

- Base hierarchy on the user's task: primary content first, actual state second, relevant actions nearby, technical detail on demand. Do not give every panel equal emphasis.
- Extend the existing Lucide icon vocabulary and React components before introducing a UI framework. Add a dependency only for a concrete accessibility, maintenance, or performance benefit.
- Define semantic tokens for background, surface, elevated surface, manuscript, text, border, accent, selected, status, focus, and overlay. Build light/dark/system behavior from these roles; avoid globally replacing raw colors without reviewing their purpose.
- Use readable text sizes, stable spacing, restrained radii and shadows. Do not create space by reducing critical labels to 8–10 px. Chinese/English mixed text and long names must fit without concealing essential information.

## Apply depth selectively

Glass can serve sidebar, topbar, floating toolbar, menus, palette, and some drawers. Use opaque, stable reading surfaces for manuscript body, Monaco, terminal, logs, data tables, figures, and graph nodes. Avoid stacked transparent layers.

Provide an opaque fallback when backdrop filtering is unavailable or reduced transparency is selected. Validate contrast over the actual composited background, not only the foreground hex color. Preserve focus, disabled, hover, selected, and error clarity in each theme.

Use brief transform/opacity transitions for orientation. Respect reduced motion; do not animate every graph node continuously or move content during execution status updates.

## Components and interaction

- Reuse and refine existing `Button`, `IconButton`, `Modal`, `Tabs`, `Badge`, `ErrorBox`, and loading/empty states. Preserve their keyboard, focus, and event behavior while changing appearance.
- An icon-only action needs a meaningful accessible label and discoverable purpose. Run and evidence states use text or symbols as well as color.
- Keep modal focus entry, trapping, Escape ordering, and restoration. Floating surfaces must not obscure the primary action or leave it unreachable after zoom.
- Dark app chrome may frame a light manuscript page; keep the surrounding tools consistent while respecting the paper's reading and export appearance.

## Iterate on real rendering

For each major page, start the isolated application, capture a baseline and redesigned screenshot, inspect them, fix observed defects, and capture again. Use `forest-browser-testing` for setup and evidence capture. Generated images or static HTML cannot substitute for a running screenshot.

Inspect hierarchy, panel ratios, graph working area, text size, purposeful whitespace, alignment, color, glass readability, action prominence, repeated titles/borders, icon consistency, and density. Report a concrete defect or a tested criterion, not only “looks good.”

Full redesign review covers Projects, Workspace/Graph, Node Focus, Run Details, Experiments, Data, Figures, Paper, Library, Files, and Settings in light/dark themes, plus actual empty/loading/error/running/pending-decision states. Cover 390/768/1024/1280/1440/1920 px and 200% zoom. For a smaller change, review affected surfaces and shared consumers proportionately.

Compare screenshots under the same browser, viewport, state, font availability, and data. Fixture visuals are valid layout tests when labeled; they do not prove real research or backend operation. Record inaccessible states as `NOT RUN` with the missing prerequisite.

Measure contrast and keyboard accessibility for changed controls. Target applicable WCAG 2.2 AA requirements; do not claim full conformance from screenshots or a single automated audit.

When implementation is requested, deliver integrated components, tokens, and actual review evidence. A palette specification alone does not satisfy the redesign.

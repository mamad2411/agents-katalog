---
name: figma-design
description: Design, build, or edit a Figma file through a design connector (plugin-API calls verified with screenshots). Use whenever the task is to create or change a Figma design, mock up a UI, logo, infographic, or design system, build styles or components, or hand a design to dev. Triggers even if the user does not name Figma but asks to "mock up", "design a screen", or "build a component library". Encodes the hard rule that page structure and layer naming come before any frame.
---

# Figma design + build

This is a worked example of a skill produced by skill-forge from `examples/WORKLOG.example.md`. It shows how tagged journal entries become a procedure, guardrails, and reference notes. The design tool runs JavaScript against the plugin API and renders server-side; drive it like a headless design tool and verify every step with a screenshot.

## Procedure (ordered, do not reorder)

1. **Establish page structure and a layer-naming convention before creating any frame.** This is step 1, always. Frames-first produces ungrouped, default-named layers (Rectangle, Text) that are unusable for dev handoff and painful to fix after. Decide pages and naming first.
2. Confirm the account and plan. Edits fail silently on a view-only account.
3. **Foundations first.** Create paint, text, and effect styles (guard by name to avoid duplicates) before drawing any UI. This locks the palette and type ramp and makes every later node bindable.
4. **Discover and load fonts up front.** List available fonts filtered to your candidates, record exact style names (they vary: `Semi Bold` vs `SemiBold`), then load every weight before setting any text.
5. **Build named, bound, and grouped as you go.** Name every node on creation, bind to styles from the first draw, build each section inside a named container. Draw backgrounds before text.
6. **Screenshot loop.** Build a small piece, screenshot the real node, read it, fix, repeat. Never author a large design blind.
7. **Componentize.** Promote repeated UI to components; group variants. Name components with `/` folders (`Logo/Mark`, `Button/Primary`).

## Hard rules (guardrails)

- **Bind nodes to styles from the first draw, never restyle after.** Restyling a built screen by hand drifts from the system and wastes a pass.
- **Await the page switch before reading a page's children.** Otherwise it returns an empty list.
- **Do not author blind.** Hand-authoring without rendering ships ugly. The screenshot loop is the work.
- **Default node names are not acceptable.** Text = its content, rects = their role (`bg`, `divider`, `card`).

## Environment notes (compatibility)

- **Fonts render server-side from the design tool's built-in library.** Locally installed fonts are invisible to the cloud connector even when the user has them. If a brand font is absent, mock with the closest twin and ship the real font in production.
- **Z-order is append order.** Later-appended siblings render on top; draw backgrounds before text.
- **Rectangles cannot have children.** Use frames or groups as containers.

## Reference

- `references/conventions.md` - naming scheme, page-per-purpose, component folders, cleanup discipline.

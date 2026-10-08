---
name: bhawna-design-sync
description: Use when translating the Bhawna Foundation Pencil design into implementation, including reading the .pen file, extracting tokens and content, mapping desktop and mobile layouts, or inferring missing component states in the same style.
---

# Bhawna Design Sync

Read `references/design-map.md` before implementing a new page or section.

## Use this skill for

- extracting page and section structure from `Bhawna-foundation.pen`
- matching colors, typography, spacing, and hierarchy
- mapping desktop and mobile variants into responsive React layouts
- inferring hover, focus, empty, error, and loading states when the design does not show them

## Workflow

1. Read the `.pen` file first. If the Pencil app bridge is unavailable, parse the file directly as JSON.
2. Extract the page sections, visible copy, image URLs, and key tokens before coding.
3. Match layout hierarchy first, then visual polish.
4. Build one reusable pattern per repeated section type instead of duplicating markup.
5. When a state is missing, infer it from nearby patterns and the design tokens in the file.

## Design interpretation rules

- Treat desktop and mobile frames as explicit guidance, not optional inspiration.
- Preserve the project's blue, orange, slate, and soft-light palette.
- Keep headings in Poppins and dense UI/body text in Inter unless a later phase changes the decision.
- If a local image path in the `.pen` file is unavailable, replace it with a stylistically similar fallback and note the assumption.

## Output expectations

- page map
- section map
- token map
- content map
- missing-state assumptions

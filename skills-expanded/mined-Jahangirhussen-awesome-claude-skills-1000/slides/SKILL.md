---
name: slides
description: Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies.
argument-hint: "[topic] [slide-count]"
metadata:
  author: claudekit
  version: "1.0.0"
---

# Slides

Strategic HTML presentation design with data visualization.

## When to Use

- Marketing presentations and pitch decks
- Data-driven slides with Chart.js
- Strategic slide design with layout patterns
- Copywriting-optimized presentation content

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `create` | Create strategic presentation slides | `references/create.md` |

## References (Knowledge Base)

| Topic | File |
|-------|------|
| Layout Patterns | `references/layout-patterns.md` |
| HTML Template | `references/html-template.md` |
| Copywriting Formulas | `references/copywriting-formulas.md` |
| Slide Strategies | `references/slide-strategies.md` |

## Routing

1. Parse subcommand from `$ARGUMENTS` (first word)
2. Load corresponding `references/{subcommand}.md`
3. Execute with remaining arguments

## Purpose
Create strategic HTML presentations with Chart.js, design tokens and conversion-focused copy.

## When NOT to use
- Editable PowerPoint output -> pptx skill.
- Video from slides -> ppt-to-video.

## Inputs
Topic, audience, goal, data for charts, brand tokens.

## Edge cases and failure handling
- Data missing for a chart -> use a text slide or ask; do not invent numbers.

## Validation
- Opens in browser, responsive, charts render, text readable, speaker flow matches the goal.

## Example
```text
Pitch deck: problem, solution, traction chart (Chart.js), ask.
```

## Related skills
pptx, theme-factory

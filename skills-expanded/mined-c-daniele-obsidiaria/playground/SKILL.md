---
name: playground
description: Creates interactive single-file HTML playgrounds with controls, live preview, presets, and generated prompt output. Use when the user asks for a playground, explorer, interactive tool, visual configurator, design explorer, query builder, or document critique workflow.
metadata:
  created_by: AI
  last_modified_by: AI
---

# Playground Builder for OpenCode

Create interactive HTML playgrounds: self-contained explorers that let the user tune options visually, see the result immediately, and copy a natural-language prompt/output back into OpenCode or another AI tool.

## What to build

Every playground is a single `.html` file with:

- interactive controls grouped by concern
- a live preview that updates instantly on every control change
- a prompt/output panel that describes the selected configuration in natural language
- a copy-to-clipboard button with clear feedback
- sensible defaults and 3-5 named presets
- inline CSS and JavaScript only, with no external dependencies
- a dark, minimal UI using system fonts and accessible contrast

## When to use this skill

Use this skill when the user asks to create, generate, or update:

- a `playground`
- an `explorer`
- an `interactive tool`
- a `visual configurator`
- a design/layout/style chooser
- a data/query/API/regex builder
- a document critique/review workflow

This is especially useful when the option space is visual, structural, subjective, or too large to describe well in plain text.

## Template selection

Choose the closest template from `templates/`:

| Template | Use for |
|---|---|
| `design-playground.md` | UI, slides, visual layout, typography, colors, spacing, cards, dashboards |
| `data-explorer.md` | SQL, API requests, regex, filters, pipelines, report/query construction |
| `document-critique.md` | Proposal review, document feedback, approve/reject/comment workflows |

If none fits perfectly, use the closest template and adapt it. Do not block unless essential source material is missing.

## Workflow

1. Identify the playground type and the user's goal.
2. Read the matching template in `templates/`.
3. Decide the output file path.
   - If the user specifies a path, use it.
   - In this Obsidian vault, default to `08_Attachments/<short-kebab-name>.html`.
   - In a software project, default to `playgrounds/<short-kebab-name>.html` if that folder exists, otherwise ask or use the current working directory.
4. Generate one complete HTML file.
5. Use a single JavaScript state object. Every control writes to state; every render reads from state.
6. Include preset buttons that update state and re-render the whole UI.
7. Make the prompt output actionable without requiring the reader to see the playground.
8. After writing the file, tell the user where it is and how to open it. Offer to open it in the browser if appropriate.

## Core requirements

### Single-file artifact

- Put all HTML, CSS, and JavaScript in one file.
- Do not use CDN links, external fonts, remote images, package managers, frameworks, or build steps.
- If icons are useful, use inline SVG or plain text symbols.

### Live preview

- Update the preview immediately on `input` and `change` events.
- Avoid an `Apply` button.
- The first render must be complete and useful.

### Prompt/output panel

- Write a natural-language instruction, not a raw JSON/value dump.
- Mention only meaningful choices and non-default decisions.
- Include enough context that an agent can act on it without opening the playground.
- If the output is for implementation, phrase it as an implementation direction.
- If the output is for review, phrase it as accepted recommendations and unresolved questions.

### Presets

- Include 3-5 named presets.
- Each preset should be cohesive, not a random combination of values.
- Make the default state polished before any preset is selected.

### UI quality

- Use a responsive layout: controls and preview side-by-side on desktop, stacked on narrow screens.
- Prefer concise labels, helper text, and clear grouping.
- Use keyboard-friendly controls and visible focus states.
- Keep advanced options in a `<details>` section when there are many controls.

## Recommended page structure

Use this structure unless the template suggests otherwise:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>...</title>
  <style>/* inline CSS */</style>
</head>
<body>
  <main class="shell">
    <header class="hero">...</header>
    <section class="workspace">
      <aside class="panel controls">...</aside>
      <section class="panel preview">...</section>
    </section>
    <section class="panel output">...</section>
  </main>
  <script>/* inline JS */</script>
</body>
</html>
```

## JavaScript architecture

- Define `defaults`, `state`, and `presets` near the top.
- Use helper functions such as `updateControlValues()`, `renderPreview()`, `renderPrompt()`, and `render()`.
- Bind all controls once on load.
- Keep rendering deterministic: no hidden state outside the main `state` object unless necessary.
- Escape user-provided text before injecting it into HTML.

## Common mistakes to avoid

- Creating a static mockup instead of an interactive tool.
- Dumping raw state as the generated prompt.
- Starting with empty or broken defaults.
- Adding too many controls without grouping them.
- Using external dependencies.
- Forgetting the copy button.
- Making a preview that does not resemble the user's actual context.
- Creating multiple files when a single file is enough.

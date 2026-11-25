---
name: slides
description: "Generate and edit presentation slides. Outputs HTML slide decks (reveal.js) or Markdown slide files. Use when user says 'make slides', 'create presentation', 'build deck', '做PPT', '做演示', or needs a non-academic presentation (for academic talks, use paper-slides instead)."
---

# Slides Generator

Generate presentation slide decks as self-contained HTML (reveal.js) or Markdown.
For academic conference talks, use `/paper-slides` instead — this skill is for general-purpose presentations.

## Usage

`/slides <topic or description>`

## Output

Creates a self-contained HTML file using reveal.js CDN:
- File: `slides/<topic>/index.html` (can be opened directly in browser)
- Also generates: `slides/<topic>/slides.md` (Markdown source for editing)

## Slide Design Principles

1. **One idea per slide** — no walls of text
2. **Visual hierarchy** — large titles, concise bullets, generous whitespace
3. **Consistent theme** — dark or light, with accent color throughout
4. **Code blocks** — syntax highlighted, font size readable
5. **Diagrams** — use Mermaid or ASCII art where helpful
6. **Speaker notes** — add notes for each slide in `<aside class="notes">`

## HTML Template Structure

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/black.css">
  <style>/* custom overrides */</style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section><!-- slide 1 --></section>
      <section><!-- slide 2 --></section>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script>Reveal.initialize({ hash: true });</script>
</body>
</html>
```

## Slide Types

- **Title slide**: Large title + subtitle + author/date
- **Content slide**: Title + 3-5 bullet points
- **Code slide**: Title + syntax-highlighted code block
- **Image slide**: Full-bleed image with overlay text
- **Comparison slide**: Two-column layout
- **Quote slide**: Large centered quote
- **Diagram slide**: Mermaid or ASCII diagram
- **Summary slide**: Key takeaways

## Rules

- Always generate a working HTML file that opens in any browser
- Include speaker notes for each slide
- Keep total slide count reasonable (10-20 for a 10-min talk)
- Use web-safe fonts or Google Fonts CDN
- Make text readable (minimum 24px effective size)

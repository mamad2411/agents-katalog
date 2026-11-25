---
name: quarto-authoring
license: CC-BY-4.0
description: >-
  Write and edit Quarto documents (.qmd) and projects (_quarto.yml): cell
  options, figures, tables, cross-references, callouts, citations, layout,
  diagrams, YAML, extensions, and converting R Markdown, bookdown, blogdown,
  xaringan, or distill to Quarto. Use when a task involves .qmd files or a
  Quarto website, book, report, or slides. For figure alt text, use the
  Quarto alt-text skill.
compatibility: >-
  Quarto CLI. The essentials below rendered without errors with Quarto 1.9.38
  and 1.10.18 (latest stable) on 2026-09-29; the references were written
  against 1.8.26. Check https://quarto.org/docs/guide/ for newer options.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Quarto Authoring

## When to Use What

For a new document, follow "QMD Essentials" below; read a reference only when
the task needs it.

| Task | Read |
|------|------|
| Convert R Markdown | [references/conversion-rmarkdown.rst](references/conversion-rmarkdown.rst) |
| Migrate a bookdown project | [references/conversion-bookdown.rst](references/conversion-bookdown.rst) |
| Migrate xaringan slides | [references/conversion-xaringan.rst](references/conversion-xaringan.rst) |
| Migrate a distill article | [references/conversion-distill.rst](references/conversion-distill.rst) |
| Migrate a blogdown site | [references/conversion-blogdown.rst](references/conversion-blogdown.rst) |
| Configure code cells | [references/code-cells.rst](references/code-cells.rst) |
| Cross-references | [references/cross-references.rst](references/cross-references.rst) |
| Figures and subfigures | [references/figures.rst](references/figures.rst) |
| Tables | [references/tables.rst](references/tables.rst) |
| Citations and bibliography | [references/citations.rst](references/citations.rst) |
| Callout blocks | [references/callouts.rst](references/callouts.rst) |
| Diagrams (Mermaid, Graphviz) | [references/diagrams.rst](references/diagrams.rst) |
| Page layout and columns | [references/layout.rst](references/layout.rst) |
| Shortcodes | [references/shortcodes.rst](references/shortcodes.rst) |
| Conditional content | [references/conditional-content.rst](references/conditional-content.rst) |
| Divs and spans | [references/divs-and-spans.rst](references/divs-and-spans.rst) |
| YAML front matter, formats (HTML, PDF, revealjs), `_quarto.yml` projects | [references/yaml-front-matter.rst](references/yaml-front-matter.rst) |
| Find and use extensions | [references/extensions.rst](references/extensions.rst) |
| Markdown linting rules | [references/markdown-linting.rst](references/markdown-linting.rst) |

## QMD Essentials

A document is YAML front matter between `---` lines, then Markdown:

```markdown
---
title: "Document Title"
format: html
---
```

Divs use three colons, `::: {.class-name}` … `:::`; spans use
`[text]{.class-name}`.

### Code Cell Options Syntax

Quarto puts cell options inside the cell, as the language's comment symbol
plus `|`. Options use **dashes, not dots** (`fig-cap`, not the knitr
`fig.cap`):

- R, Python, Julia: `#|`
- Mermaid: `%%|`
- Graphviz/DOT: `//|`

````markdown
```{r}
#| label: fig-example
#| echo: false
#| fig-cap: "A scatter plot example."

plot(x, y)
```
````

Common execution options:

| Option    | Description       | Values                    |
| --------- | ----------------- | ------------------------- |
| `eval`    | Evaluate code     | `true`, `false`           |
| `echo`    | Show code         | `true`, `false`, `fenced` |
| `output`  | Include output    | `true`, `false`, `asis`   |
| `warning` | Show warnings     | `true`, `false`           |
| `error`   | Show errors       | `true`, `false`           |
| `include` | Include in output | `true`, `false`           |

Set document-level defaults under `execute:` in the front matter
(`execute: {echo: false, warning: false}`).

### Cross-References

A label must start with its type prefix, and you reference it with `@`:

| Type | Label | Reference |
|------|-------|-----------|
| Figure | `#| label: fig-plot` or `![…](p.png){#fig-plot}` | `@fig-plot` |
| Table | `#| label: tbl-data` or a `::: {#tbl-data}` div | `@tbl-data` |
| Section | `## Intro {#sec-intro}` | `@sec-intro` |
| Equation | `$$ … $$ {#eq-model}` | `@eq-model` |

An unresolved reference renders as `?@fig-…` with an "Unable to resolve
crossref" warning, so check the render output.

### Callouts, figures, tables, citations

- Callouts: `::: {.callout-note}` … `:::`; the five types are `note`,
  `warning`, `important`, `tip`, `caution`.
- Figures: `![Caption](image.png){#fig-name fig-alt="Alt text"}`; subfigures
  go in a `::: {#fig-group layout-ncol=2}` div.
- Tables: a Markdown table inside `::: {#tbl-example}` with the caption as the
  div's last paragraph.
- Citations: `@smith2020` or `[@smith2020; @jones2021]`, with
  `bibliography:` (and optionally `csl:`) in the front matter.

Examples and options for each are in the references above.

## Resources

<!-- lychee-ignore -->
- [Quarto Documentation](https://quarto.org/)
- [Quarto Guide](https://quarto.org/docs/guide/)
<!-- lychee-ignore -->
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)

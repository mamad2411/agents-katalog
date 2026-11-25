---
name: quarto-reports
description: Quarto report mechanics for research deliverables -- project-mode output paths and the stale-PDF trap, rendering from code and in worker processes, ASCII and LaTeX backstops, references-before-appendices structure, reusable include fragments, draft marking for AI-assisted content, and deriving numbers from the project's own registries instead of writing them.
when_to_use: Writing or editing a .qmd or .Rmd report; rendering a report from a script or a worker; a rendered PDF is missing, stale, or lands somewhere unexpected; adding numbers, tables or figures to a report; marking a draft.
paths:
  - "**/*.qmd"
  - "**/*.Rmd"
  - "**/_quarto.yml"
  - "**/reports/**"
---

# Quarto reports

For the *prose* -- audience, structure, plain language -- use `report-writing`, which
also asks the user who the report is for before drafting. For the *design* of any
chart or figure, use the `dataviz` skill, and `r-lib:alt-text` for figure
descriptions. This skill covers only report mechanics and the failures that recur
in them.

## Project mode mirrors the input directory

The single most expensive report trap here. With a `_quarto.yml` present, Quarto is
in **project mode**, and the output **mirrors the input's project-relative
directory** under `output-dir`:

```
reports/fire.qmd   ->   outputs/reports/reports/fire.pdf     ## note: NOT flat
```

Two failures followed from assuming the flat path:

1. A render target aborted with "rendered PDF not found" the first time it ran
   through the pipeline, because it had only ever been rendered by hand before.
2. The fix-of-the-fix: a `!file.exists(flat_path)` guard meant that once *any*
   flat PDF existed, every re-render returned the **stale** flat file while the
   freshly-rendered PDF sat orphaned at the mirrored path. A stale 635 kB PDF was
   published as the deliverable.

Rules:

- **Never reconstruct the flat path.** Take the path the render actually reports
  and copy from there.
- **`file.copy()` only warns on failure.** Unchecked, a failed copy leaves the
  previously published PDF in place and still returns its path -- so the target
  succeeds while shipping the old deliverable. Check the return value and compare
  mtimes.
- Committed deliverable PDFs live in a **sibling** directory (`reports/pdf/`),
  never on the render path.

## Rendering from code

- **Worker processes do not inherit the shell `PATH`.** Resolve the Quarto binary
  explicitly, or prepend its directory, before calling `quarto::quarto_render()`.
  The same applies to any external tool: an interactive IDE exposes it, a callr
  child or a worker does not.
- **Two concurrent renders of one template in one directory clobber each other's
  intermediates.** Render each variant from its own copy of the template.
- A function that renders a report returns the path it wrote.
- A pipeline framework adds its own rules for render steps; for `{targets}`, see
  `targets-project-setup` in `r-targets`.

## ASCII, with a LaTeX backstop

Reports are ASCII-only. Use `--`, `->`, `>=`, `x` in prose, and LaTeX math where
the symbol is genuinely needed (`$\geq$`, `$\times$`, `$\rightarrow$`).

Keep a backstop in `_quarto.yml` so a stray glyph degrades to a warning rather than
killing the render -- an undeclared character is a hard failure with **no output
PDF produced**:

```yaml
format:
  pdf:
    pdf-engine: pdflatex
    include-in-header:
      text: |
        \DeclareUnicodeCharacter{2192}{$\rightarrow$}
        \DeclareUnicodeCharacter{2190}{$\leftarrow$}
        \DeclareUnicodeCharacter{2194}{$\leftrightarrow$}
        \DeclareUnicodeCharacter{00D7}{$\times$}
        \DeclareUnicodeCharacter{2265}{$\geq$}
        \DeclareUnicodeCharacter{2264}{$\leq$}
        \DeclareUnicodeCharacter{2022}{\textbullet}
```

A generated `README.md` should set `format: gfm` **and `from: markdown-smart`**,
which disables smart typography so the output stays ASCII, plus a banner saying it
is generated and which file to edit instead.

## Structure

- One sentence per line in prose. It makes diffs readable and review specific.
- Chunk options as `#|` pipe comments, not fence-header options.
- Reference sections and figures **by name**, never by line number.
- End with `\clearpage`, `# References {.unnumbered}`, and a `::: {#refs} :::` div, so
  references render on a new page **before** any appendices. Use `\clearpage`, not
  `\newpage`: it flushes pending floats first, so a figure cannot drift past the
  references into the appendix. One project enforces this in a test.
- Underscore-prefixed fragments (`reports/_provenance-appendix.qmd`) are includes,
  never rendered standalone; pull them in with
  `{{< include _provenance-appendix.qmd >}}`.
- Restrict the project render list so only real reports are built:
  ```yaml
  project:
    render:
      - reports/*.qmd
  ```

## Derive numbers; do not write them

The recurring quality failure is prose and tables drifting from the artifacts they
describe. The fix is structural: **generate report tables from the same registry
the code uses**, so the report cannot drift from the code.

Quarto sets the working directory to the report's own folder, so walk up to the
project root -- to a file only the root has -- rather than assuming either location:

```r
.root <- normalizePath(".")
while (!file.exists(file.path(.root, "renv.lock")) && dirname(.root) != .root) {
  .root <- dirname(.root)
}
```

If a number must be hard-coded, mark it `TODO(curate)` and say what would verify it.

## Mark drafts and AI-assisted content

Stamp a DRAFT watermark on every non-final PDF:

```yaml
include-in-header:
  text: |
    \usepackage{draftwatermark}
    \SetWatermarkText{DRAFT}
    \SetWatermarkScale{1}
    \SetWatermarkColor[gray]{0.9}
```

And carry an explicit callout where content was drafted with AI assistance:

```markdown
::: {.callout-warning}
**Draft -- pending human review.** Portions were drafted with generative-AI
assistance from pinned metadata and have not been fully reviewed. Verify against
the actual source before relying on any entry.
:::
```

Never write a citation into a report without verifying it -- see
`citation-integrity` in `r-project-core`, and note that a DOI-checking hook runs
on every edit to a `.qmd` or `.bib`.

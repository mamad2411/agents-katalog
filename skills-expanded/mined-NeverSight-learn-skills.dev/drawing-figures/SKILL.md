---
name: drawing-figures
description: 'Publication figure budgeting and production for academic papers, including 论文绘图/画图/架构图/结果图: reference-derived budgets, Elsevier/CVPR/ICCV/NeurIPS figures, diagrams, plots, result stitches, and publication-ready exports. Covers charts of every form — grouped bars, scatter, Pareto fronts, heatmaps — colour-blind-safe encoding, 600 dpi exports, and baseline-comparison panels. For an architecture figure it writes the structure as mermaid, derives the 生图提示词 an image model needs, checks each returned image against it, and corrects the draw.io or PowerPoint file traced from the accepted one. Do not use for language review, caption-only edits, or submission packaging.'
license: MIT
compatibility: Requires Python 3 with matplotlib and Pillow.
---

# drawing-figures

Produce publication figures. This skill owns figure budgeting and figure artifacts; it does not own
manuscript prose review, caption-only rewriting, or submission packaging.

## Two kinds of figure, made two different ways

Route on what the figure is made of, because the two paths share almost nothing:

| | **Result figures** — most of them | **Method figures** — the architecture, and one per contributed block |
|---|---|---|
| Made from | Experiment artifacts: checkpoints, logs, metrics | The structure of your model, which lives in the code |
| Produced by | Python that runs, deterministically, from the data | An image model, then traced by hand into a vector file |
| Regenerating it | Rerun the caller script | Revise the prompt, reroll, retrace |
| Follow | [references/figure-script-reference.md](references/figure-script-reference.md) | [references/method-figures.md](references/method-figures.md) |

A result figure has data behind it, so its correctness question is "do these pixels come from the
run they claim to". A method figure has no data at all, so its question is "does this topology
match the model" — answered by a mermaid the agent writes once and every later conversation reads
instead of the model code, and by a prompt per figure that accumulates across rounds.

**Budget first, when there is a corpus to budget against.** Evidence-based targets for section
length, figure and table counts, palette, and caption patterns come from
[references/budget-workflow.md](references/budget-workflow.md). Skip it when the venue
requirements and the figure plan are already settled.

Export by the default in [references/publication-artwork.md](references/publication-artwork.md) —
vector wherever the figure can be vector, 600 dpi otherwise, designed at final column width. That
covers CVPR, ICCV, NeurIPS, and an ordinary Elsevier or IEEE submission. Read a venue's artwork
guide only when that venue raises one of the four things that actually vary: separate artwork
files, a stated DPI above 600, CMYK, or a physical size limit in millimetres.

## Figure design system

- White background (`#FFFFFF`); no dark theme, grey panel, gradient, 3D bar, or chartjunk. One
  figure carries one message.
- Use distinct, saturated, colour-blind-safe colours from `scripts/figkit/palette_base.py`, never
  matplotlib's default cycle.
- Use Arial or Helvetica for sans-serif elements and Times New Roman for serif annotations.
  Final figures must not depend on DejaVu or Computer Modern.
- Prefer PDF/EPS/SVG for vector-native plots and diagrams; 600 dpi for raster work.
- Design at final column size. Keep text at least 8 pt and strokes/symbols legible; use a compact
  canvas instead of shrinking text on an oversized canvas.
- Encode meaning with colour plus marker shape, line style, label, or another redundant cue, so the
  figure still reads in greyscale print.
- Use honest axes and a chart type appropriate to the data shape. Do not truncate an axis to
  exaggerate a gap; label a non-zero origin explicitly, and share one scale across subplots that
  plot the same quantity.
- Name every axis, legend entry, and annotation after the real method or metric. Ship no
  `Module A` / `X` / `Y` placeholders.
- Open each caption with the finding rather than "Fig. X shows …", so the figure is understandable
  away from the body text.
- Preserve the data and caller script behind analytical figures. Never synthesize missing
  experimental or observed-image evidence.

## References

- [Budget workflow](references/budget-workflow.md): commands, dependencies, outputs, and Phase A
  completion criteria.
- [Method figures](references/method-figures.md): writing the architecture down once so a stateless
  agent stops re-reading the code, the nine-section prompt, what to check on a returned image and
  in what order, the render ledger, and the pass over a traced draw.io or PowerPoint file.
- [Chart selection](references/chart-selection.md): which chart form fits which data shape, and
  what to do when values span orders of magnitude.
- [Figure script reference](references/figure-script-reference.md): diagram, plot, stitch,
  measurement, and annotation APIs with runnable examples.
- [Publication artwork](references/publication-artwork.md): artwork classification and export QA.

## Completion criteria

A budget is complete only when it records section word counts, figure/table counts, palette, and
caption patterns, or explicitly records which corpus artifact was unavailable.

Three of the four evidence items are the same for every figure. Only the first differs, because
only the first is about where the figure's content came from — and the two kinds of figure answer
that question with different artifacts.

**1a. Provenance of a result figure.** Name the canonical output and the retained data and caller
paths. For a comparison figure, trace the "Ours" panel to the checkpoint or run that produced its
pixels — read the generator script's data paths, not the panel label. A label is a claim, not
evidence: panels inherited from a related project, an earlier model, or an unversioned asset
directory can carry your method's name over another model's output, and the tables and figures
then report different models with nothing visibly wrong. If a panel's pixels cannot be traced to
your own run, regenerate it; if its numbers must match a table, generate both from the same
checkpoint.

**1b. Provenance of a method figure.** There is no data to trace, so the retained source
is the mermaid, and the claim it has to support is that the topology matches the code. Name the
mermaid path, say when it was last checked against the model, and confirm the traced file still
matches it. A traced file whose mermaid was never revised is a figure nobody can check — and,
because the mermaid is what later conversations read instead of the model code, a stale one is
worse than none.

**2. Format evidence** — vector status for PDF/EPS/SVG, or raster format, physical dimensions,
pixel dimensions, and effective DPI against the venue artwork class.

**3. Design-system check** — font family/size and palette/contrast/dual-encoding result.

**4. Paper linkage** — figure number, manuscript section or paragraph that cites it, and caption
path/text status; confirm the caption's stated finding matches the figure and manuscript text.

Done means every item above is concrete and checked, the manuscript rendering is legible at final
size, each symbol/abbreviation is explained, and no unresolved render-QA blocker remains.

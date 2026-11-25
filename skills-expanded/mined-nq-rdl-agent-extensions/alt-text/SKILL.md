---
license: CC-BY-4.0
description: >-
  Generate accessible alt text for data visualizations in Quarto documents. Use
  when the user wants to add, improve, or review alt text for figures in .qmd
  files. Triggers for requests about accessibility, figure descriptions, fig-alt,
  screen reader support, or making Quarto documents more accessible.
compatibility: >-
  Works on .qmd source alone. Verification renders with the Quarto CLI; the
  rendered-HTML check and the engine gotcha were tested with Quarto 1.9.38 and
  1.10.18 (Jupyter and knitr engines) on 2026-09-29.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Write Chart Alt Text

Write alt text for the data visualizations in the user's Quarto documents.
The user may name a file, a figure label, or neither (then cover every figure
in the documents they point you to).

## Instructions

Analyze each figure and write alt text following these guidelines.

### Key Advantage: Source Code Access

Unlike typical alt text scenarios where you only see an image, **you usually have the code that generates each chart**. Use it to extract precise details:

**From plotting code:**
- Variable mappings → exact variable names for axes
- Color/fill mappings → what color encodes
- Plot type functions → scatter, histogram, line chart, etc.
- Trend lines or fitted curves → overlaid statistical fits
- Faceting/subplots → number of panels and what varies
- Color scales → encoding scheme (sequential, diverging, categorical)
- Axis labels and titles → customized labels

**From data generation code:**
- Random distributions → expected distribution shape
- Transformations → what was done to data
- Feature engineering → preprocessing applied
- Filtering/subsetting → what subset is shown

**From surrounding prose:**
- Text before/after the chunk explains the **purpose** and **key insight**
- The section or chapter it sits in tells you what the figure is meant to show
- This is often the best source for the "key insight" part of alt text

If the figure is a static image with no generating code, read the image itself
and the surrounding prose; say which details you could not confirm.

### Three-Part Structure (Amy Cesal's Formula)

1. **Chart type** - First words identify the format
2. **Data description** - Axes, variables, what's shown
3. **Key insight** - The pattern or takeaway (often found in surrounding text)

### Relationship to fig-cap

Read the `fig-cap` first. The alt text should **complement, not duplicate** it:
- If caption states the insight, alt text can focus on describing the visual structure
- If caption is generic, alt text should include the key insight
- Together they should give a complete understanding

### Content Rules

**Include:**
- Chart type as first words
- Axis labels and what they represent
- Specific values/ranges when code reveals them (e.g., "peaks between 25-50")
- Number of panels/facets
- What color/size encodes if used
- The key pattern that supports the chapter's point

**Exclude:**
- "Image of..." or "Chart showing..." (screen readers announce this)
- Decorative color descriptions (unless color encodes data)
- Information already in fig-cap
- Implementation details (package names, function internals)

### Length Guidelines

| Complexity | Sentences | When to use                                 |
|------------|-----------|---------------------------------------------|
| Simple     | 2-3       | Single geom, no facets, obvious pattern     |
| Standard   | 3-4       | Multiple geoms or color encoding            |
| Complex    | 4-5       | Faceted, multiple overlays, nuanced insight |

### Quality Checklist

- [ ] Starts with chart type (Scatter chart, Histogram, Faceted bar chart, etc.)
- [ ] Names the axis variables
- [ ] Includes specific values/ranges from code when informative
- [ ] States the key insight from surrounding prose
- [ ] Complements (not duplicates) the fig-cap
- [ ] Would make sense to someone who cannot see the image
- [ ] Uses plain language (avoid jargon like "geom" or "aesthetic")

## Template Patterns

**Scatter chart:**
```
Scatter chart. [X var] along the x-axis, [Y var] along the y-axis.
[Shape: linear/curved/clustered]. [Specific pattern, e.g., "peaks when X is 25-50"].
[Any overlaid fits or annotations].
```

**Histogram:**
```
Histogram of [variable]. [Shape: right-skewed/bimodal/normal/uniform].
[If transformed: "after [transformation], the distribution [result]"].
[Notable features: outliers, gaps, multiple modes].
```

**Bar chart:**
```
Bar chart. [Categories] along the x-axis, [measure] along the y-axis.
[Key comparison: which is highest/lowest, relative differences].
[Pattern: increasing/decreasing/grouped].
```

**Tile/raster chart:**
```
Tile chart [or heatmap]. [Row variable] along the y-axis, [column variable] along the x-axis.
Color encodes [what value]. [Pattern: where values are high/low].
[If faceted: "N panels showing [what varies]"].
```

**Faceted chart:**
```
Faceted [chart type] with [N] panels, one per [faceting variable].
[What's constant across panels]. [What changes/varies].
[Key comparison or insight across panels].
```

**Correlation heatmap:**
```
Correlation [matrix/heatmap] of [what variables]. [Arrangement].
[Overall pattern: mostly positive/negative/mixed].
[Notable clusters or strong/weak pairs].
[If relevant: contrast with expected behavior, e.g., "unlike PCA, these are not orthogonal"].
```

**Before/after comparison:**
```
[N] [chart type]s arranged [vertically/in grid]. [Top/Left] shows [original].
[Bottom/Right] shows [transformed]. [Key difference/similarity].
[If overlay: "[color] curve shows [reference]"].
```

**Line chart with overlays:**
```
[Line/Scatter] chart with overlaid [fits/curves]. [Axes].
[Number] of [lines/fits] shown: [list what each represents].
[Which fits well vs. poorly and why].
```

## Workflow

### Finding Figures

A figure is not always a labelled code cell. Search every `.qmd` in scope,
recursively, for all of these (for example with Grep over `**/*.qmd`):

- code cells that plot, labelled or not (`#| label: fig-…`, `#|label:`, or a
  knitr chunk header such as `{r fig-name, …}`);
- existing `fig-alt` (and knitr `fig.alt`) options;
- Markdown images `![caption](path){…}`, including subfigures inside a
  `::: {#fig-… layout-ncol=…}` div;
- computational subfigures (`fig-subcap` lists), which need a `fig-alt` list
  with one entry per panel.

A `#| label: fig-` grep alone misses unlabelled cells, Markdown figures,
subfigure panels, and files in subdirectories.

### Where fig-alt goes

- Code cell: `#| fig-alt: "…"` beside `#| fig-cap:`.
- Markdown image: `![Caption](plot.png){#fig-name fig-alt="…"}`.
- Computational subfigures: `#| fig-alt:` followed by a YAML list.

**Engine gotcha.** A multi-line block (`#| fig-alt: |`, `|-`, `>`) works with
the knitr engine (R) but breaks under the Jupyter engine (Python, Julia): the
caption lands in `alt`, the attribute text appears on the page, and the figure
loses its id so `@fig-…` no longer resolves. Observed with Quarto 1.9.38 and
1.10.18. For Jupyter documents write the alt text as one quoted line. A
Python chunk-header attribute (`{python fig-alt="…"}`) is ignored.

### For Each Figure

1. **Locate** the cell or image and read the prose before and after it.
2. **Extract details**: `fig-cap`, the plotting and data code, the claim the
   prose makes.
3. **Draft alt text** with the three-part structure (type → data → insight).
4. **Check** it against the quality checklist.

### Verify

When the Quarto CLI is available, render the changed documents and check the
HTML Quarto actually produced:

```bash
quarto render path/to/doc.qmd --to html
bash scripts/check-alt.sh path/to/doc.html   # this skill's script
```

[scripts/check-alt.sh](scripts/check-alt.sh) lists every figure image without alt text (Quarto
omits `alt` when `fig-alt` is missing; it does not fall back to the caption),
raw `fig-alt=` text leaked into the page, and unresolved `?@fig-…`
cross-references. Treat an "Unable to resolve crossref" warning from the
render the same way. Rendering runs the document's code; if the user has not
asked you to run it, or Quarto or the engine is not installed, say so and fall
back to re-reading the source: every figure found above has a `fig-alt`, and
Jupyter documents use one-line values.

## Example

**Code context:**
```r
plotting_data |>
  ggplot(aes(value)) +
  geom_histogram(binwidth = 0.2) +
  facet_grid(name~., scales = "free_y") +
  geom_line(aes(x, y), data = norm_curve, color = "green4")
```

**Surrounding prose says:** "Normalization doesn't make data more normal"

**fig-cap:** "Normalization doesn't make data more normal. The green curve indicates the density of the unit normal distribution."

**Good alt text** (R/knitr cell, so a multi-line block is fine; in a Python
cell put it on one line):
```
#| fig-alt: |
#|   Faceted histogram with two panels stacked vertically. Top panel shows
#|   original data with a bimodal distribution. Bottom panel shows the same
#|   data after z-score normalization, retaining the bimodal shape. A green
#|   normal distribution curve overlaid on the bottom panel clearly does not
#|   match the data, demonstrating that normalization preserves distribution
#|   shape rather than creating normality.
```

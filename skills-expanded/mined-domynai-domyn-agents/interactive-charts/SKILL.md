---
name: interactive-charts
description: >-
  Draw an interactive chart (zoom, hover, toggle series) as a self-contained HTML page
  with Plotly, in the house style (the shared palette and fonts). Use only when the user
  explicitly asks for an interactive, zoomable or hoverable chart, or an HTML chart or page.
  Any other chart, simple or not, is the `charts` skill (a PNG), the default.
external_files:
  - ../../resources/plotly_style.py
  - ../../resources/palette.json
---

# Interactive charts

An interactive chart is drawn with **Plotly** and saved as one HTML page, in the house
style that `plotly_style.py` sets. That module is the single source of the look: colours,
fonts, axes, legend, margins, hover labels. Import it, and every figure made after that is
styled; never restyle a chart by hand to match.

This skill is for pages only, and only when the user asked for one: every other chart,
including any simple chart asked for without saying how, is the `charts` skill. A static chart (for a report, a PDF, a slide) is drawn with
the `charts` skill (seaborn, PNG): Plotly writes no image here, so neither kaleido nor
Chrome is ever needed. When the user wants both, draw the PNG with `charts` and the page
with this skill, from the same data and with the same colours by key.

Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve
them from its directory, never from the working directory.

Both live in the resources shared by every builtin skill:

| Path | What it is |
|---|---|
| `../../resources/plotly_style.py` | the Plotly template and `save()` |
| `../../resources/palette.json` | every colour of the house style; `plotly_style.py` reads its colours from here, the same keys the static charts use |

## Setup

1. **Check the package** in the environment that will run the script:
   `python -c "import plotly"`. If it is missing, install it without asking:
   `python -m pip install plotly` (`uv pip install plotly` in a `uv` project). Say in one
   line that you installed it.
2. **Put `plotly_style.py` and `palette.json` next to the script.** Copy both from the
   resources into the folder the chart script is in (the style refuses to load without
   the palette beside it):

   ```sh
   cp "<dir of this SKILL.md>/../../resources/"{plotly_style.py,palette.json} "<script folder>/"
   ```

   Python always searches a script's own folder first, so `import plotly_style` then finds
   the copy wherever the script is run from, whatever the working directory or
   `PYTHONPATH`, and the folder reruns without the skill. Never import it through a path
   typed by hand, the current directory, or `PYTHONPATH`.
3. **Import it before building any figure:**

   ```python
   from pathlib import Path

   import plotly.express as px
   import plotly_style  # sets the house template as the default

   out = Path(__file__).resolve().parent
   fig = px.bar(df, x="region", y="revenue", title="Revenue by region, 2025")
   plotly_style.save(fig, out, "revenue_by_region")
   ```

## What the style gives you

Importing `plotly_style` registers the template `house` and makes it
`plotly.io.templates.default`, for `plotly.express`, `go.Figure` and `make_subplots`
alike. It sets the colour order, fonts, a left-aligned title, horizontal gridlines only, a
horizontal legend above the plot, thin axis lines, margins, hover labels, and the
default colour scales.

For what a template can't decide, take the colour from `plotly_style.PALETTE` (the loaded
`palette.json`) **by its key, never as hex** (and never edit it in the copy: a colour
changes in `../../resources/palette.json`, for every skill at once):

| Key in `PALETTE` | Use it for |
|---|---|
| `["charts"]["categorical"]` | one colour per series, **assigned in order** (the template already does, for series without a colour of their own): the template's six accents, the four that stay distinct under colour blindness first; `["primary"]` opens it |
| `colorscale("sequential")` | magnitude (heatmaps of counts, density): light = little, dark = a lot. A function, since a Plotly scale is built from the palette's stops |
| `colorscale("diverging")`, with `["charts"]["negative"]` / `["charts"]["positive"]` | a value around a meaningful zero (correlations, change, coefficients) |
| `["text"]["light_background"]["muted"]` | reference lines: zero, mean, target, "perfect prediction", a grey baseline model |
| `["text"]["light_background"]["heading"]` | the "actual" series drawn against predictions or forecasts |
| `tint(color, alpha)` | a shaded range: a confidence band in the muted grey at 0.15, or in a series' colour |
| `LEGEND_RIGHT` | the legend of a figure with subplot titles (the default legend would cover them) |

`plotly_style.save(fig, out, name)` writes `<name>.html` and returns its file name. The page
is self-contained, with plotly.js inline, so it opens on its own and offline; that makes it
about 4.8 MB, so write one page per chart the user asked for, not one for every chart of
a report. A page names DM Sans and does not embed it: a viewer without the font sees a
system sans.

## Choosing the chart

| The data's job | Chart |
|---|---|
| distribution of one numeric column | histogram (box plot to compare several) |
| counts or shares by category | horizontal bar, sorted, largest on top |
| comparison across groups | grouped bars; box plots for median and spread |
| two numeric columns | scatter (an interactive page can take more points than a PNG, but sample past ~50 000) |
| change over time | line, with a range slider (`fig.update_xaxes(rangeslider_visible=True)`) for a long series |
| a matrix (correlation, confusion) | heatmap, with the values in the hover text |
| one headline number | no chart: say the number |

## Rules

- **One colour per series, in `["charts"]["categorical"]` order, and it follows the series**: the same
  model or group keeps its colour in every chart, the PNGs included. A single series needs
  no colour logic at all.
- **At most three series in a scatter, four in a line or bar chart.** The palette has only
  four colours that stay apart for every reader; the fifth and sixth are blues close to the
  first, so use them only with each series labelled directly. Beyond that fold the rest
  into "Other", or split into small multiples (`make_subplots`, one panel each).
- **Never a rainbow scale**, and never a sequential scale for a value with a sign: use
  `colorscale("diverging")` with the midpoint at zero (`zmid=0`, or `zmin=-m, zmax=m`).
- **One y-axis.** Two measures on different scales are two charts, not a secondary axis.
- **Don't distort**: bars and counts start at zero (`rangemode="tozero"`); say so in the
  title when an axis is truncated or logarithmic.
- **Every chart has a title that states what it shows, and axis titles with units.** A
  legend only with two or more series.
- **Hover text says what a point is**, in words and units (`hovertemplate`), not the raw
  column names.
- **Never `fig.show()`**, never `fig.write_image` (it needs kaleido and Chrome: a PNG is the
  `charts` skill's), and never write a page anywhere but through `plotly_style.save`.

## Checklist

- [ ] `plotly_style` imported before the first figure, from a copy next to the script, with
      `palette.json` beside it
- [ ] colours only from `plotly_style.PALETTE` (by key) or `colorscale()`; each series the same colour as in the PNGs
- [ ] title, axis titles with units, hover text in words, legend only when there are several series
- [ ] no dual axis, no rainbow, bars from zero
- [ ] saved with `plotly_style.save`; tell the user the page's path and that it opens in any browser

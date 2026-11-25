---
name: charts
description: >-
  Draw a static chart, graph or plot as a PNG with seaborn in the house style (the shared
  palette, DM Sans, the slides' type sizes): bar, line, scatter, histogram, box, heatmap,
  small multiples. The default for any chart: use it whenever a chart, graph or plot is to
  be created (for a report, a document, a slide or the conversation, from data in a file, a
  table or numbers in the conversation) unless the user explicitly asks for an interactive
  or HTML one, which is `interactive-charts`.
external_files:
  - ../../resources/seaborn_style.py
  - ../../resources/palette.json
  - ../../resources/typography.json
  - ../../resources/assets/fonts/
---

# Charts

Every static chart is drawn with **seaborn** (on matplotlib), in the house style that
`seaborn_style.py` sets. That module is the single source of the look: colours, font, text
sizes, axes, legend, layout. Import it, and every figure made after that is styled; never
restyle a chart by hand to match. It writes PNGs and needs no browser.

**This is the skill for every chart by default.** A request for "a chart", "a plot", "a
graph" or "a visualization" of something is a static PNG drawn here, however simple. Use
`interactive-charts` only when the user explicitly asks for an interactive, zoomable,
hoverable or HTML chart; never pick it on your own because a chart might benefit from
hovering.

Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve
them from its directory, never from the working directory.

They live in the resources shared by every builtin skill:

| Path | What it is |
|---|---|
| `../../resources/seaborn_style.py` | the seaborn theme, `figure()`, `title()`, `legend()`, `save()` |
| `../../resources/palette.json` | every colour of the house style; `seaborn_style.py` reads its colours from here (the `charts` section arranges the template's colours for charts), so charts match the slides |
| `../../resources/typography.json` | the text roles and their sizes in points, shared with slides and documents |
| `../../resources/assets/fonts/` | DM Sans, registered with matplotlib by `seaborn_style.py`: every PNG is drawn in it, installed or not |

## Setup

1. **Check the package** in the environment that will run the script:
   `python -c "import seaborn"`. If it is missing, install it without asking:
   `python -m pip install seaborn` (`uv pip install seaborn` in a `uv` project; it brings
   matplotlib). Say in one line that you installed it.
2. **Put the style next to the script.** Copy `seaborn_style.py`, `palette.json`,
   `typography.json` and the fonts into the folder the chart script is in (the style
   refuses to load without the two JSON files beside it):

   ```sh
   R="<dir of this SKILL.md>/../../resources"
   cp "$R/"{seaborn_style.py,palette.json,typography.json} "<script folder>/"
   mkdir -p "<script folder>/fonts" && cp "$R/assets/fonts/"*.ttf "<script folder>/fonts/"
   ```

   Python always searches a script's own folder first, so `import seaborn_style` then finds
   the copy wherever the script is run from, whatever the working directory or
   `PYTHONPATH`, and the folder reruns without the skill. Never import it through a path
   typed by hand, the current directory, or `PYTHONPATH`.
3. **Import it before building any figure:**

   ```python
   from pathlib import Path

   import seaborn_style  # sets the house theme
   import seaborn as sns

   out = Path(__file__).resolve().parent
   fig, ax = seaborn_style.figure()
   sns.barplot(df, x="revenue", y="region", ax=ax, saturation=1)
   seaborn_style.title(fig, "Revenue by region, 2025")
   ax.set_xlabel("revenue (€k)")
   ax.set_ylabel("")
   seaborn_style.save(fig, out, "revenue_by_region")
   ```

## What the style gives you

Importing `seaborn_style` calls `seaborn.set_theme` with the house settings, for every
axes-level seaborn function and plain matplotlib alike: the colour order, DM Sans at the
slides' body size, thin axis lines on the left and bottom only, horizontal gridlines only,
no legend frame, concise date ticks, the house colormaps as default, and `$` read as text
(not as a formula). What a theme can't decide is a function:

| Function | Use it for |
|---|---|
| `figure(width=900, height=520, nrows=1, ncols=1, **kw)` | every figure: the size in CSS pixels (written at 2×), constrained layout so nothing is clipped; `kw` goes to `plt.subplots` (`sharex=True`…) |
| `title(fig, text)` | the chart's title: left-aligned at the top, above the legend. Never `ax.set_title` for it: an axes title is a **panel's** title in small multiples |
| `legend(ax, ncols=None, title=None)` | the legend above the plot, in one row, without a frame; on a panel with its own title it goes to the right instead (call it on the last panel) |
| `save(fig, out, name)` | writes `<name>.png`, closes the figure, returns the file name |

For what a theme can't decide, take the colour from `seaborn_style.PALETTE` (the loaded
`palette.json`) **by its key, never as hex** (and never edit it in the copy: a colour
changes in `../../resources/palette.json`, for every skill at once):

| Key in `PALETTE` | Use it for |
|---|---|
| `["charts"]["categorical"]` | one colour per series, **assigned in order** (the theme already does, for `hue` and for series without a colour of their own): the template's six accents, the four that stay distinct under colour blindness first; `["primary"]` opens it |
| `colormap("sequential")` | magnitude (heatmaps of counts, density): light = little, dark = a lot. Returns the registered name, for `cmap=` |
| `colormap("diverging")`, with `["charts"]["negative"]` / `["charts"]["positive"]` | a value around a meaningful zero (correlations, change, coefficients) |
| `["text"]["light_background"]["muted"]` | reference lines: zero, mean, target, "perfect prediction", a grey baseline model |
| `["text"]["light_background"]["heading"]` | the "actual" series drawn against predictions or forecasts |
| `tint(color, alpha)` | a shaded range: a confidence band in the muted grey at 0.15, or in a series' colour |

Text sizes come from `seaborn_style.TYPOGRAPHY["roles"]` (points): `body` for labels, `caption`
for an annotation on the chart. Never a size typed as a number.

`figure()` defaults to 900 × 520: give a tall or wide chart its own size rather than
squeezing it (a horizontal bar chart: `height=max(320, 30 * bars + 160)`).

## Seaborn defaults to override

- `sns.barplot`, `sns.boxplot`, `sns.violinplot` **desaturate** their colours: pass
  `saturation=1`, or the bars are not the palette's colours.
- `sns.barplot` and `sns.pointplot` draw **95% confidence intervals** by default: pass
  `errorbar=None` unless the interval is the point of the chart, and say what it is.
- `sns.heatmap`: add `linewidths=1, linecolor=PALETTE["surfaces"]["card_light"]` and
  `ax.grid(False)`; `annot=True, fmt=".2f"` when the matrix is small (≤ 12 × 12).
- A **horizontal** bar chart: the gridlines go the other way, `ax.grid(axis="x")` and
  `ax.grid(axis="y", visible=False)`.
- Use the **axes-level** functions (`sns.lineplot(…, ax=ax)`, `histplot`, `scatterplot`,
  `barplot`, `boxplot`, `heatmap`) on a figure from `figure()`. The figure-level ones
  (`relplot`, `catplot`, `displot`, `FacetGrid`, `pairplot`) make their own figure,
  without the layout or the title placement; for small multiples, `figure(ncols=…)` and one
  axes-level call per panel.
- Seaborn titles the legend with the `hue` column; `legend()` drops that title unless you
  pass one.

## Choosing the chart

| The data's job | Chart |
|---|---|
| distribution of one numeric column | histogram (box plot to compare several) |
| counts or shares by category | horizontal bar, sorted, largest on top |
| comparison across groups | grouped bars; box plots for median and spread |
| two numeric columns | scatter (sample to ~5 000 points) |
| change over time | line; bars only for a few discrete periods |
| a matrix (correlation, confusion) | heatmap, with the values written in the cells when small |
| one headline number | no chart: say the number |

## Rules

- **One colour per series, in `["charts"]["categorical"]` order, and it follows the series**: the same
  model or group keeps its colour in every chart of a report (`hue_order`, or a `palette=`
  dict built from `PALETTE`). A single series needs no colour logic at all.
- **At most three series in a scatter, four in a line or bar chart.** The palette has only
  four colours that stay apart for every reader; the fifth and sixth are blues close to the
  first, so use them only with each series labelled directly. Beyond that fold the rest
  into "Other", or split into small multiples (`figure(ncols=…)`, one panel each).
- **Never a rainbow colormap**, and never a sequential one for a value with a sign: use
  `colormap("diverging")` centred at zero (`center=0`, or `vmin=-m, vmax=m`).
- **One y-axis.** Two measures on different scales are two charts, never `ax.twinx()`.
- **Don't distort**: bars and counts start at zero; say so in the title when an axis is
  truncated or logarithmic.
- **Every chart has a title that states what it shows, and axis labels with units.** A
  legend only with two or more series; label a few series directly instead when that reads
  better.
- **Text stays in the text colours** the theme sets; the colour of a mark carries
  identity, not the labels next to it.
- **Never `plt.show()`**, and never write a chart anywhere but through `seaborn_style.save`.

## Checklist

- [ ] `seaborn_style` imported before the first figure, from a copy next to the script, with
      `palette.json`, `typography.json` and `fonts/` beside it
- [ ] every figure from `seaborn_style.figure()`, its title from `seaborn_style.title()`
- [ ] colours only from `seaborn_style.PALETTE` (by key) or `colormap()`; `saturation=1` on bars and boxes; each series the same colour in every chart
- [ ] title, axis labels with units, legend only when there are several series
- [ ] no dual axis, no rainbow, bars from zero, no unasked-for error bars
- [ ] saved with `seaborn_style.save`, and the PNG opened and looked at before it is used:
      overlapping labels, clipped text or an unreadable legend mean it isn't done

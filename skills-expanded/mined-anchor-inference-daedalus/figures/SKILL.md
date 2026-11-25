---
name: figures
description: Charts and diagrams a reader can trust — learning curves, scaling laws, benchmark and ablation comparisons, Pareto trade-offs, heatmaps, method diagrams. Covers the shared matplotlib style module, sizing, uncertainty and vector export. Use whenever you plot or chart a result.
---
A figure in a report is an argument, not a screenshot of an array. It makes one claim, and a
reader who skips the prose should still get that claim right. Default matplotlib output does not
clear that bar: it is sized for a screen, titled where a caption belongs, coloured from a cycle
that collapses in greyscale, and rasterised where the document wants vector.

## Non-negotiables

1. **Build at the final size.** A figure drawn 8 inches wide and shrunk into a 3.25-inch column
   has 3pt tick labels. Pick the width from the destination (`COLUMN`, `TEXT`, `WIDE` in the style
   module) and draw it at that width. Never build big and rescale to fit.
2. **Vector out.** SVG for anything read on a screen, PDF alongside it for print. A rasterised
   *plot* — axes, lines, text — is a defect. PNG is right only for genuinely raster content: a
   photograph, a sample grid, an attention map at pixel resolution.
3. **Every number comes from a run.** Read the metric out of the log, the CSV or the `Verify`
   receipt that produced it. Never plot a remembered, rounded or plausible number, and never leave
   synthetic demo data in a script that ships.
4. **The caption is the title.** No `ax.set_title` — a title duplicates the caption and steals
   vertical space. Panel letters (**a**, **b**) name the parts of a multi-panel figure.
5. **Show the uncertainty, or say there is none.** One seed is an anecdote. Plot the interval
   across seeds and state the count; with a single run, write "single seed" rather than implying
   more.
6. **Label the axes with units.** "Loss" is a label; "step" without saying whether it counts
   optimizer steps or tokens is not.
7. **Colourblind-safe, greyscale-safe.** Use the module's palette. Never `jet`, `rainbow` or
   `hsv` — they invent structure that is not in the data.
8. **Sans-serif text, the same face in every figure.** `use_style()` defaults to a
   Helvetica-metric sans, which survives the 5–8pt sizes tick labels print at. Pass
   `use_style(family="serif")` only for a figure carrying heavy math on a serif-set page.

## Set up once per deliverable

Vendor the style module next to the scripts that import it, so the figure still rebuilds after
this session ends:

```sh
mkdir -p report/figures && cp <this skill's directory>/assets/figstyle.py report/figures/
```

(The `Skill` tool prints where this skill's files are. Copy, do not symlink: the workspace is what
survives, the skills directory belongs to the host repository.)

Run the scripts in an environment that has matplotlib without disturbing the workspace's own:

```sh
uv run --no-project --with matplotlib --with numpy python report/figures/loss_curve.py
```

A script that imports project code runs in the project's environment instead.

## Where the figure goes, and how to cite it

The figure, the script that made it and the data it read live together in the deliverable's own
directory in the workspace — `report/figures/loss_curve.py` → `loss_curve.svg` → `loss_curve.pdf`.
A figure whose script is gone cannot be corrected when the operator asks for one more seed, and a
figure written to `/tmp` is gone at the end of the turn.

Inside a report, link it by relative path: `![Loss](figures/loss_curve.svg)`. In the chat answer,
hand it over with `SendFile` and cite it — `<file path="report/figures/loss_curve.svg"/>` — so the
operator can open it from the message. Never cite a path you did not write.

## Write the caption with the figure

Captions run about 25–40 words for one panel, more for several. The shape that works is a short
bold phrase naming the claim, then the detail a reader needs to trust it:

> **The cache halves p99 latency above 200 rps.** p99 against offered load for both builds; five
> runs each, bands are 95% intervals. The dotted line is the previous release.

- **Lead with the finding, not the setup.** "Latency against load" names the axes, which the axes
  already do.
- **Put the method facts here**, because nowhere else has room: how many runs, what the band or
  bar means, any smoothing or normalisation, which points were excluded.
- **Say what is not shown** when it matters — a single seed, a truncated axis, a run cut short.
- **Do not restate the axis labels**, and do not repeat the caption as an axes title.

## Multi-panel figures

- **Label every panel** `(a)`, `(b)`, … at the top left (`panel_labels()`); prose needs a way to
  name a panel that survives one of them moving.
- **Share the axis when panels share a quantity** (`sharey=True`), and let the shared axis carry
  one label. Two panels of the same metric on silently different ranges is the multi-panel version
  of a truncated bar axis.
- **One legend for the figure**, not one per panel.
- **Panels read in argument order**: left to right, top to bottom.
- **If the panels do not support one claim, they are separate figures.**

Build them with `figure_grid(nrows, ncols, width=TEXT, sharey=True)`, which sizes the whole grid to
the final width.

## Read exactly one reference

Pick by the question the figure answers, not by the shape you have in mind.

| The figure answers | Read |
| --- | --- |
| How does a metric move over a run, and is the gap bigger than the noise? | `references/curves.md` |
| How does it change with scale, and what does the trend predict? | `references/scaling.md` |
| Which variant wins across cases, or which ablated part mattered? | `references/comparison.md` |
| What is traded off against what — quality vs cost, reward vs latency? | `references/pareto.md` |
| What does this 2D grid, confusion matrix or sweep look like? | `references/matrix.md` |
| What is the method, the architecture, the pipeline? | `references/diagram.md` |

Do not read references for figures you are not making. Anything outside those six — a photograph,
a qualitative sample grid, a map — still obeys the non-negotiables and the style module.

## Before you hand it over

- **Read the audit line `save()` prints.** It checks the printed width, font embedding, stray axes
  titles, missing axis labels, text below the 5pt floor, overlapping text and text running off the
  canvas. `clean` is the bar; anything else is a defect to fix, not a warning to mention.
- If the audit reports no publication font on the machine, say so when you hand the figure over
  rather than installing fonts, which is a change to the environment worth asking about.
- Open the file and look at it at its printed size. If a tick label is unreadable on screen at
  100%, it is unreadable on paper. `ImageView` answers "is this legible, does anything overlap?"
  about a rendered PNG of it.
- Every axis labelled with units, no stray title, uncertainty shown with n stated, no unexplained
  series, and the script reruns from scratch and reproduces the same file.

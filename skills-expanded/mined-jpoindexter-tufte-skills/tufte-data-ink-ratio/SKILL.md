---
name: tufte-data-ink-ratio
description: "Use when a chart, graph, or dashboard looks cluttered, over-decorated, or 'busy' — heavy grids, filled bars, box frames, duplicate axes — or before shipping any statistical graphic. Covers Tufte's data-ink ratio, the two-pass erasure procedure, and converting frame/tick ink into data."
tags: [tufte, data-visualization, graphical-design, chartjunk, statistical-graphics]
---
# Data-Ink Ratio

## Overview
The data-ink ratio measures how much of a graphic's ink is doing real informational work. Tufte's core claim in *The Visual Display of Quantitative Information* (Chapter 4): the larger the share of ink devoted to data, the better the graphic, other things equal. The ratio is not a grade to chase but a lever — it tells you to find every mark that could be erased without losing data, then erase it. This dissolves the chronic problem of decoration, redundancy, and convention adding ink that competes with the data instead of conveying it.

## §1. The Ratio: One Definition, Three Equivalent Forms

Data-ink is the part of a graphic that responds to the numbers. Tufte's canonical definition:

> "Data-ink is the non-erasable core of a graphic, the non-redundant ink arranged in response to variation in the numbers represented." — Tufte, *The Visual Display of Quantitative Information*

The ratio has three equivalent formulations. The skill must carry all three, because each exposes a different lever:

```
(1)  data-ink ratio = data-ink / total ink used to print the graphic

(2)  = the proportion of a graphic's ink devoted to the
       non-redundant display of data-information

(3)  = 1.0 − the proportion of a graphic that can be erased
       without loss of data-information
```

- **Form (1)** is the accounting definition: a fraction of total ink.
- **Form (2)** restates it as a proportion and embeds the redundancy test — only *non-redundant* data display counts.
- **Form (3) is the operational lever.** It reframes the whole task as a hunt for erasable ink: find what you can delete with zero loss of information, subtract it, and what remains is your ratio. You raise the ratio by erasing, not by adding. Work from form (3).

### Practical interpretation of the ratio

Tufte gives the directive "maximize, within reason" — he does **not** publish numeric pass/fail grades. The bands below are a practitioner heuristic for *talking about* a graphic, not Tufte's measured thresholds. Treat them as a smell test, not a target to optimize blindly.

| Approx. ratio | What it usually means | Action |
|---|---|---|
| Low (much ink erasable) | Mostly decoration, frames, fill, or redundancy | Run both erasure passes; redesign |
| Middle | Typical after one editing pass; some waste remains | Second pass on redundant data-ink |
| High (little erasable) | Most ink moves with the data | Stop erasing; check legibility, add labels in recovered space |
| Near 1.0 | Theoretical ceiling; axis labels and a minimal frame still carry some non-data ink | Diminishing returns — do not strip below legibility |

The "within reason" qualifier is load-bearing: redundancy and a little structure occasionally earn their ink (see §7). Past the point of legibility, erasing makes the graphic worse, not better.

**Scope limit (p. 96):** Tufte scopes the principle himself — maximizing data-ink generates sound advice "for perhaps two-thirds of all statistical graphics"; for the remaining third the ratio is ill-defined or the wrong lens. Treat it as the default tool, not a universal law.

## §2. Data-Ink vs Non-Data-Ink vs Redundant Data-Ink

Three categories. Erase the last two, in that order.

| Ink type | Definition | Examples | Erase? |
|---|---|---|---|
| **Data-ink** | Ink that, if erased, destroys some part of the data; it changes when the data changes | Plotted point positions, a line's path, the top edge of a bar | No — this is the core |
| **Non-data-ink** | Ink that depicts no statistical information at all | Box frames, background shading, grid mesh, tick marks once axis labels exist | Yes — erase first |
| **Redundant data-ink** | Ink that depicts a number already shown elsewhere on the graphic | Bar fill (the height already encodes the value), bilateral symmetry, duplicated axis | Yes — erase second |

The test for any mark: *does it change if the data changes?* If no, it is a candidate for erasure.

### A bar encodes its single value many times over

One shaded, bordered, labeled bar locates its value redundantly through several independent encodings:

1. Height of the left edge
2. Height of the fill
3. Height of the right edge
4. Position of the top horizontal edge
5. Position of the printed number at the top
6. The printed number itself

Any one of these locates the value; the rest are redundant data-ink. Tufte's progression — solid bar → open bar (edges only) → range bar (one line plus a tick) — strips the redundancy one layer at a time while the value stays readable (see §6).

## §3. The Five Principles of Graphical Redesign (in order)

Tufte closes the data-ink chapter with five principles. The order *is* the procedure.

1. **Above all else show the data.**
2. **Maximize the data-ink ratio (within reason).**
3. **Erase non-data-ink (within reason).**
4. **Erase redundant data-ink (within reason).**
5. **Revise and edit.**

> "Above all else show the data." — Tufte, *The Visual Display of Quantitative Information*

> "Maximize the data-ink ratio, within reason." — Tufte, *The Visual Display of Quantitative Information*

Principle 1 sets the goal: every design choice serves the data. Principle 2 is the metric. Principles 3 and 4 are the two concrete moves that execute principle 2 — they are the *how*. Principle 5 says redesign is iterative: you rarely get there in one pass.

## §4. The Two-Pass Erasure Procedure

Always two passes, in this order. Doing non-data-ink first matters — redundancy is far easier to see once the decorative clutter is gone.

### Pass 1 — Erase non-data-ink
Remove ink that depicts no information at all:
- Background fills and plot-area shading
- Grid lines and tick mesh (especially dense grids)
- Box frames around the plotting area (drop top and right at minimum)
- Decorative borders on bars and columns
- 3D effects, drop shadows, perspective

### Pass 2 — Erase redundant data-ink
Remove ink that re-depicts a number already shown:
- Bar and area fill (the boundary already encodes the value)
- Bilateral symmetry — box plots, Chernoff faces (one half is a mirror of the other)
- Duplicate axis labels on both sides
- A second axis encoding the same variable at another scale

### The graphical arithmetic

```
original design = erased part + good part
```

Most over-decorated graphics are a large fraction erasable ink wrapped around a small core of data-ink. The data survives erasure intact.

### Use the recovered space
Space freed by erasing is not wasted white space — it is capacity for *more* information. Use it to label interesting data points directly on the plot, add a marginal distribution, or rotate a vertical axis title to horizontal so it actually reads. Erasing buys room; spend it on data, not air.

## §5. Convert Non-Data-Ink Into Data-Ink (the multifunctioning move)

The strongest redesigns don't just erase frame and tick ink — they make that ink *do data work*. This is the most under-applied lever in the chapter.

- **Range-frame:** Draw each axis line only across the actual range of the data, from the minimum value to the maximum. The axis line now reports the data range — the frame has become data-ink instead of a decorative box. The empty corner of a conventional rectangle frame is deleted for free.
- **Dot-dash-plot / marginal rug:** Replace evenly-spaced conventional tick marks with one tick per actual data value, projected onto each axis. The ticks now show the marginal distribution of each variable. What was the lowest-grade non-data-ink (regular ticks) becomes a second dataset.
- **Direct labels in freed space:** After erasing a grid, label peaks, outliers, or categories where the grid used to be, so the reader never leaves the data plane to decode a legend.

The rule: before erasing a mark, ask whether it can be *repurposed* to carry data. Erase only what cannot.

## §6. Named Redesigns

**Published figures (verified against VDQI):** a Bonner scatterplot runs only ≈10–20% non-data-ink (p. 94); a registration-rates chart redrawn reaches ≈0.7 (p. 95); a third reprint that forgot to plot the data points earns Tufte's verdict "a graphical absolute zero, a null data-ink ratio" (p. 95); the Kuznicki bar chart loses ~65% of its ink with zero data loss (p. 101); Pauling's atomic-volume chart rises from <0.6 to ~0.9 after erasing its 63-tick "marching band of mosquitoes" (pp. 102–103); across the book's redesigns, ratios rise from 0.1–0.2 to nearly 1.0 (p. 136).

### Box plot → quartile plot
A conventional box plot draws each quartile boundary on both the left and right of the box; the right half is a mirror of the left and adds nothing. Tufte's quartile plot erases the box entirely (pp. 123–124): in the erased design a **dot marks the median** and the line's endpoints and breaks mark the extremes and quartiles; in Tufte's preferred variant, the **middle half (the interquartile segment) is drawn offset** from the whisker line. Same five-number summary, a fraction of the ink, and many plots now fit where few did. Erasure also pays in analyst time: ten conventional box plots take ~80 straightedge placings to draw; the erased version takes 10 (p. 125).

### Bar → open bar → range bar
Start with a solid filled bar (value encoded ~6 ways, §2). Erase the fill → an open bar (three edges). Erase two edges → a single vertical line with a tick at the top. Each step removes redundant data-ink; the value stays readable at every step. The line-only form lets far more bars sit side by side for comparison.

### Range-frame scatterplot
A standard scatterplot sits in a four-sided box on a grid. Erase the box and grid; redraw the two axis lines to span only the data's range; project each point's value as a tick on the margin (dot-dash-plot). The frame and ticks, formerly pure decoration, now report the range and the marginal distributions. (See §5.)

### Chernoff faces
Full faces are bilaterally symmetric — the right side mirrors the left, doubling the space without adding a variable. Half-faces carry the same encoded data in half the area. Symmetry here is redundant data-ink, not structure.

### The over-gridded chart (a "dreaded grid" case)
A chart whose data plane is covered by a dense mesh of tick marks: the grid competes with the very points it is meant to help locate, and the more data points there are, the worse the competition. Erasing the grid (keeping at most a light reference line where positional reading is genuinely hard) lifts the ratio sharply and lets the data emerge. Recovered space then holds direct labels.

**The Pauling lesson — structure vs. grid (pp. 103–104):** erasing the grid from Pauling's chart exposed misfit elements — but the *reference curves* proved essential, because they organize the periodicity the chart exists to show; restoring the grid instead failed. Some non-data-ink (organizing curves, study-structure connectors) earns its place. The grid never did. Classify before erasing.

## §7. When Redundancy Is Justified

Erasing redundancy is *within reason*, not unconditional. Tufte names legitimate uses — redundancy earns its ink when it helps the reader move through the data:

- **Cyclical / wrap-around series:** In Marey's graphical train schedule, an extra **half cycle** is attached at the edge (p. 98) so a train running off the side is picked up again without forcing the eye back to the start. The repetition supports continuous reading.
- **Context and orientation:** Redundancy can give order to a complex graphic, ease comparison across its parts, and create aesthetic balance.
- **Single-value graphics:** A lone uncomplicated number may not need the redundant-data-ink pass at all; the non-data-ink pass always applies.

The decisive test: **does the redundant ink help the reader navigate, or does it merely restate a number the reader already has?** Help → keep. Restate → erase.

### Defending erased designs to an audience (p. 136)

Erased, unfamiliar forms draw the objection "readers won't get it." Tufte's four-point reply: the design carries more information per unit of ink and space; graphics improve through revision like prose; do not underestimate the audience — "if you understand it, most other readers will, too," and graphics should be as intelligent as the accompanying text; odd-looking designs are odd only from unfamiliarity. And the closing scope note (p. 137): data-ink maximization is one dimension of a multivariate design task that also weighs complexity, structure, density, and beauty.

## §8. Failure Modes

These are the low-ratio patterns that recur in scientific and technical publishing. Each is a way ink piles up without conveying data.

| Failure mode | What it is | Why it fails | Fix |
|---|---|---|---|
| **Unintentional optical art (moiré)** | Cross-hatching, parallel rules, or dot patterns filling bars and areas | The pattern interacts with the eye's tremor to produce vibration and motion; noise clouds the data | One flat light-gray tint, or label the area with a word |
| **The dreaded grid** | A dense tick mesh laid across the data plane | The grid competes with the data marks it claims to help locate; worse as data grows | Erase it; keep at most one faint reference line where positional reading is truly hard |
| **The self-promoting duck** | Elaborate 3D constructions, area/volume pictograms, perspective | Decoration overwhelms data; an extra visual dimension (depth) is unlabeled and unscaled | Simple geometric marks; one variable to one visual attribute |

### Ratio killers, ranked by how often they appear
1. Full-weight grid mesh across the data plane
2. Bar / area fill (cross-hatch or solid)
3. 3D perspective on 2D data
4. Bilateral symmetry (box plots, faces)
5. Duplicate axis labels on both sides
6. Decorative four-sided frame
7. Background color fill on the plotting area

## §9. Do / Don't Pairs

### Frames and axes
| Do | Don't |
|---|---|
| Draw left + bottom axis lines only, or use a range-frame | Box the plot on all four sides |
| Let the data set each axis's extent (range-frame) | Extend axis lines past the last data point |

### Bars and columns
| Do | Don't |
|---|---|
| Define each bar with one edge + a top tick | Fill bars with shading or cross-hatch |
| State each value once (in data or one direct label) | Shade it *and* border it *and* print the number *and* grid it |
| Use dot plots for many-category comparisons | Use grouped 3D bars |

### Grids and ticks
| Do | Don't |
|---|---|
| Repurpose ticks as a marginal data rug (dot-dash-plot) | Print a full grid mesh at the weight of the data |
| Erase ticks once axis labels give enough reference | Tick every integer when there are five data points |
| Use a single flat gray tint for any needed area fill | Use cross-hatch, diagonals, or dot patterns |

### Symmetry and redundancy
| Do | Don't |
|---|---|
| Use a half-box / quartile plot for distribution shape | Mirror the box — the second half adds nothing |
| Use half-faces if encoding with Chernoff faces | Draw full symmetric faces for the same data |
| Repeat a cycle only when wrap-around navigation needs it | Duplicate non-cyclical data for visual balance |

### The redesign process
| Do | Don't |
|---|---|
| Run two passes: non-data-ink first, redundant second | Redesign in one pass — redundancy hides behind clutter |
| Spend recovered space on new labels or a marginal distribution | Leave erasing-freed space as decorative emptiness |
| Keep structural ink that would change with the experiment (e.g. paired-comparison connectors) | Erase ink that encodes the study's structure |

## §10. Application Checklist

Run this erasure audit before finalizing any statistical graphic. Work from form (3): hunt for erasable ink.

- [ ] Does **every** mark change if the data changes? Any that don't are erasure candidates.
- [ ] Is any value shown in ink more than once? Keep one encoding, erase the rest.
- [ ] Grid lines present? Erase unless positional reading truly needs them; if kept, drop to a faint reference line.
- [ ] Bars/areas filled? Erase the fill; keep bounding edges (or one edge + tick).
- [ ] Four-sided frame? Drop top and right; consider a range-frame that reports the data range.
- [ ] Ticks decorative? Repurpose them as a marginal rug, or erase once labels suffice.
- [ ] Bilateral symmetry on a non-bilateral variable? Erase one side.
- [ ] Axis title rotated 90°? Rotate to horizontal using recovered space.
- [ ] After erasing, is there freed space? Spend it on direct labels or a marginal distribution.
- [ ] Did any redundancy survive *on purpose* (cyclical wrap, navigation aid)? If you can't name why it helps the reader move through the data, erase it.
- [ ] Stop test: would the next erasure cost legibility? If yes, stop — "within reason."

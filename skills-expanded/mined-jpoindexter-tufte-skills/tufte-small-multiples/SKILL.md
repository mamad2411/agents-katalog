---
name: tufte-small-multiples
description: "Use when comparing the same measurement across many conditions, categories, times, or places — when an overlaid chart drowns in crossing lines, an animation or slideshow forces comparison from memory, panels auto-scale to different ranges, or a faceted/trellis/grid layout is being designed or reviewed for panel size, ordering, borders, and shared scales."
tags: [tufte, data-visualization, comparison, data-density, trellis, layout]
---
# Small Multiples

## Overview

> "At the heart of quantitative reasoning is a single question: *Compared to what?*" — Tufte, *Envisioning Information*, p. 67

Small multiples answer that question directly: they enforce comparisons of changes, of differences among objects, of the scope of alternatives. Tufte's verdict in the same passage is that for a wide range of data-presentation problems, small multiples are the best design solution.

Small multiples are a series of graphics sharing the same design structure, the same scale, and the same visual encoding — varying only the data across panels. Because the design is constant, the viewer's eye stops re-learning each chart and attends entirely to shifts in the data. Tufte presents the pattern as the single most effective method for multivariate comparison: simultaneously more honest, more dense, and more legible than animation, sequential views, or overlaid series.

Two mechanisms power it. First, the Shrink Principle applied repeatedly: reduce one graphic to the minimum size that stays legible, then array many copies. Second, a large underlying data matrix: small multiples take a wide table of numbers and lay it out so the eye reads thousands of values at once, in the area a conventional graphic would spend on dozens.

---

## §1. Definition and Core Rules

> "Small multiples resemble the frames of a movie: a series of graphics, showing the same combination of variables, indexed by changes in another variable."
> — Tufte, *The Visual Display of Quantitative Information*, p. 170

The design holds constant across every frame so that attention goes entirely to how the data shifts. *Envisioning Information* states the invariant principle in one sentence:

> "Constancy of design puts the emphasis on changes in data, not changes in data frames." — Tufte, *Envisioning Information*, p. 67

The three invariants that define a valid small multiple:

| Invariant | What it means | What breaks it |
|---|---|---|
| Same design structure | Identical chart type, layout, and proportions | Switching from line to bar mid-array |
| Same scale | Shared axis ranges across all panels | Per-panel auto-scaling |
| Same encoding | Identical use of color, size, shape, line weight | Changing what a color encodes per panel |

The one thing that changes: **the data**, indexed by the varying variable (time, category, condition, geography, etc.).

**The index variable** is the dimension that varies across panels. It can be:
- A single variable (one panel per year, per species, per demographic).
- Two variables at once, producing a 2D matrix of panels (rows = one variable, columns = another). See §7.

Tufte endorses two-dimensional indexing explicitly — what he calls "flatland within flatland" (*Envisioning Information*, p. 78): stacking a second index on the multiplied image deepens the display while adding almost nothing to reading effort. His neurometric example arrays brain-electrical maps with frequency bands (delta, theta, alpha, beta) across the columns and diagnostic groups down the rows — every cell drawn identically.

---

## §2. The Shrink Principle, Data Density, and the Data Matrix

The pattern depends on shrinking panels aggressively. Tufte's governing claims (VDQI, pp. 168–169), paraphrased:

- Graphics can be shrunk far down. Many data graphics lose roughly half their published area with virtually no loss in legibility or information.
- The twin design goal is to maximize **data density** *and* **the size of the data matrix**, within reason.

These are two distinct targets, and small multiples maximize both:

| Term | Definition | How small multiples push it |
|---|---|---|
| Data density | Data entries ÷ area of the graphic | Shrinking panels packs more entries into the same eyespan |
| Size of the data matrix | Total rows × columns of underlying numbers | One cell-graphic is multiplied across every row and column of a wide table |

The corollary: small multiples are usually built *from* a large data matrix (VDQI, p. 175). If the underlying table is small, the pattern earns nothing — an overlay or a single chart is faster. The power appears when a wide matrix is laid out so the eye scans many cells at once.

Tufte cites Bertin: a crisp, elegant line style fits 17 small-scale graphics on one page alongside extensive text — and the page is itself a small multiple *of design advice*, each of the 17 cells a before/after redesign (VDQI p. 169). The implication — most designers oversize individual panels, which cuts how many fit within eyespan and so prevents comparison.

**Concrete density benchmarks from Tufte:**
- Wall Street Journal, The Times (London), Asahi: data-rich, high-density graphics.
- US Geological Survey topographic quadrangle (17×23 inches): ~250,000 bits per square inch.
- Most American papers and magazines: less data per graphic than major industrialized-country papers.

As panel count rises and panel size shrinks, the data marks inside each panel must shrink too (thinner lines, smaller dots). Chartjunk, non-data-ink, and redundant data-ink get more expensive as density rises — every pixel of decoration displaces a data value.

---

## §3. Eyespan and the Comparison Constraint

The single most operationally important constraint:

> "Comparisons must be enforced within the scope of the eyespan, a fundamental point occasionally forgotten in practice."
> — Tufte, *Envisioning Information*, p. 76

This rules out pagination as a comparison mechanism. If the viewer must scroll, tab, or turn a page to see panel B after panel A, the comparison is broken — it happens from memory, not from the eye.

**Practical consequences:**

| Situation | Rule |
|---|---|
| 4–9 panels | Usually fits one screen/page; straightforward |
| 10–25 panels | Requires aggressive shrinking; still viable |
| 25+ panels | Possible (Tufte's 23-panel air-pollution array, p. 170) but demands very high per-panel density and small panels |
| Panels on separate pages | Not a small multiple — sequential presentation, not comparative display |
| Animation / slideshow | Not a small multiple — viewer can't hold the prior frame in memory for direct comparison |

---

## §4. Panel Structure: Labeling, Axes, and Borders

**Shared axes:** all panels share axis ranges. Never auto-scale per panel — that encodes the same data value as different heights in different panels and destroys the comparison.

**Labels:** minimal. The index-variable label (year, condition, time of day) appears once per panel in the smallest legible type. Labels are part of the data display, not decoration, and must not compete with the data marks for visual weight.

**Borders and grids:** use implicit structure, not heavy rules. Tufte's caution (paraphrasing *Envisioning Information*, p. 79): dark surrounds around each image generate disruptive white stripes where panels meet, pulling more attention than the data; locations can instead be signaled by nearly silent methods such as an implicit, evenly spaced grid.

The VDQI source of this border discipline is the erased Tukey multiwindow plot: Tufte links the LA pollution multiple's graphical arithmetic to it directly (pp. 114, 171) — panels shed interior frames and grids and keep only data, exactly as the multiwindow redraw did.

Do/don't pairs for panel framing:

| Do | Don't |
|---|---|
| Thin hairline rules or no rules between panels | Heavy ruled boxes around each panel |
| Implicit spatial grid (consistent spacing) | Explicit grid lines that create disruptive stripes |
| Labels directly on or adjacent to the data | Separate legend requiring eye travel |
| White or neutral background per panel | Dark surrounds (generate disruptive white stripes at edges) |
| Single shared legend / scale bar at the array edge | Repeated legend in every panel |

**Spacing as data:** panels can be spaced in proportion to the values of the index variable. Tufte notes that his ghost-figure multiples could even be spaced in proportion to the dates the figures were drawn — making the gaps themselves encode information. Use proportional spacing whenever the index has uneven intervals (irregular dates, non-uniform doses).

---

## §5. Tufte's Exemplars (VDQI Chapter 8)

Tufte builds the case for small multiples through a sequence of examples in the data-density / small-multiples chapter. Studying the set is more instructive than any single one, because each isolates a different reason the pattern works.

| Example (page) | Structure | Index variable | What it reveals / why it qualifies |
|---|---|---|---|
| LA air pollution (p. 170) | 23 panels, each a distribution of hydrocarbon concentration over the city | Hour of day | Design unchanged frame to frame; only the pollution distribution shifts. All 23 visible at once — the canonical large-array small multiple |
| Melanoma sites — Wiskemann (p. 171) | Head-and-neck maps ("Kopf und Hals") locating 269 primary melanomas; 3 panels — both sexes combined, men, women | Sex | Identical head-and-neck diagram repeated; only lesion-location data changes, so site patterns compare straight across |
| Sampling-error distributions (p. 172) | 12 panels, each a histogram of 50 random normal deviates | Replicate sample | Identical underlying process; the panel-to-panel scatter *is* the lesson — sampling variation made visible |
| Herring catch (p. 172) | 6 distributions stacked vertically, 1908–1913, shared age x-axis | Year | The strong 1904 year-class ages through successive catches — a bump migrating rightward year by year. Readable only because the age axis is shared and panels are stacked for one eyespan |
| Human/ape chromosomes (p. 173) | Chromosome banding strips arrayed across 4 primate species (human + three apes) | Species | Identical chromosome-strip design lets homologous bands be compared band-for-band across species |
| Consumer Reports frequency-of-repair (p. 174) | Circle-fill matrix: 12 car models × 6 model years × 19 rows — 17 trouble spots plus a summary Trouble Index and Cost Index — repair rate encoded as fill density | Model × year | A table-graphic hybrid carrying a dense, multivariate comparison no set of bar charts could match |

Of the Consumer Reports figure Tufte writes:

> "a particularly ingenious mix of table and graphic, portraying a complex set of comparisons between manufacturers, types of cars, year, and trouble spots."
> — Tufte, *The Visual Display of Quantitative Information*, p. 174

> Count note: the repair matrix has **17 trouble spots plus a Trouble Index and a Cost Index = 19 rows**, not 18. This aligns with the figure on p. 174 and with the `tufte-data-density` skill.

### Exemplars beyond VDQI

- **Leupold's finger-reckoning plate, 1727 (EI p. 66)** — *Theatrum Arithmetico-Geometricum* lays out hand- and body-sign encodings for the numbers 1 through 1,000,000 as a gridded visual dictionary: an early taxonomic small multiple.
- **Huygens, 1659 (EI p. 67)** — the exemplar EI's chapter opens on, and the one Tufte calls a superior small-multiple design: 32 Saturns at different locations in three-space, seen from the vantage points of two different observers. *Visual Explanations* returns to Huygens's ring diagram as an information-design classic and arrays 13 earlier *wrong* interpretations of Saturn beside it — people see more clearly once they have the right idea (VE pp. 106–108).
- **Plasma-equilibria paired panels (EI p. 67)** — each time step is shown twice: a 3-space perspective surface paired with a 2-space contour plot, so the repeating unit is itself a two-representation pair that hedges the relief view's masking with a plan view. The caption's caveat is worth keeping: viewed upside down, the perspective mountains become valleys — 3-D surface renderings carry an orientation ambiguity the contour panel does not.
- **Calligraphy brush sequence (EI pp. 68–69)** — photographs of a brush drawing a single Kana character, dual-indexed by time (→) and by camera angle (↑): a two-axis photographic multiple where one axis is viewpoint, not a data category. A second row reads brush-tip pressure and bend — and therefore stroke width — from the same frames, so the panels carry a derived physical variable, not just appearance. Tufte attaches Garry Winogrand's remark: "There is nothing as mysterious as a fact clearly described." A pre-film precursor sits on the same spread — Mercator's 1540 *Literarum Latinarum* shows the proper ordering of strokes in forming capital letters as a drawn sequence: the same design, achieved without a camera.
- **Dighton Rock (EI pp. 72–73)** — the same rock drawn by different observers from 1680 to 1854, arrayed as a comparative multiple: constancy of subject exposes observer bias, wishful scholarship made visible.
- **Chinese poets (EI pp. 74–75)** — 10,086 poets across four dynasties carried in one multiple array.
- **Rivers (EI pp. 76–77)** — Tufte names the design tension outright: a struggle between maintaining each river's context and enforcing comparison across rivers. Every small-multiple design sits somewhere on that axis.
- **Contredanse grid, 1762 (BE pp. 32–33)** — eight movements in a constant frame; read down for the sequence within a movement, across for the sequence between movements.
- **FT COVID daily-death multiples (SWFE p. 26)** — every country's trajectory ghosted behind each panel, so each country is read scaled against all countries. (Body text says 54 countries; the red header on the same page says 61 — both figures appear in the book.)
- ***Visual Explanations* on function and order** — VE's small-multiples pages name six distinct functions the format serves (p. 105) and recommend ordering panels by frequency of occurrence rather than arbitrary sequence (pp. 115–116).
- **Patient-status display (VE pp. 110–111)** — Powsner & Tufte's one-page medical summary (*The Lancet* 344, 1994; US patent 5,640,549), designed against the paper chart Tufte indicts as "a write-only memory" built for storage, administration, and legal defense rather than for treating the patient. The architecture: a **nonlinear shared time axis** on all ~24 panels — more-than-a-year-prior compressed, then the prior year, then the first week of admission and today emphasized — recency weighting by clinical relevance, held uniform across the grid; the most recent reading dual-encoded (red graphical point plus printed number); a whiskered band marking normal limits; one column per clinical problem, so dose (above) and response (below) compare within a column; and a provenance-stamped narrative column (clinician initials, role, timestamp per note). Footnote 11 (p. 116) adds empirical support from Staggers & Mills on spatial vs. temporal density in nurse–computer interaction.

---

## §6. What Small Multiples Beat

Tufte positions small multiples as superior to three common alternatives for multivariate comparison:

| Alternative | Why it fails | Small-multiple fix |
|---|---|---|
| Animation / sequential frames | Viewer can't hold the prior frame in memory; comparison needs a simultaneous view | Lay every frame out at once |
| Overlaid series (many lines on one chart) | Lines cross, colors multiply; visual complexity grows faster than the data | Give each series its own identical panel |
| Separate single charts (one per report/page) | Comparison requires memory across page turns; eyespan constraint violated | Shrink and array within one eyespan |

The Consumer Reports matrix (§5) settles it: a conventional approach would need a dozen separate bar charts and would defeat the cross-comparison entirely.

Small multiples also *argue*: EI (p. 30) frames them as efficient, convincing summaries that press the same point again and again through complementary variations on one substantive theme — repetition as rhetoric, with each panel a fresh witness.

---

## §7. Two-Dimensional Indexing (the Trellis Pattern)

When two categorical variables each index a dimension, the result is a 2D panel matrix — later named "trellis" displays (Cleveland) or "facets" (ggplot2). Tufte establishes the principle visually before anyone named it.

Structure:
```
          Column variable →
          Cat_A   Cat_B   Cat_C   Cat_D
Row  R1 | panel  panel  panel  panel
var  R2 | panel  panel  panel  panel
↓    R3 | panel  panel  panel  panel
     R4 | panel  panel  panel  panel
     R5 | panel  panel  panel  panel
     R6 | panel  panel  panel  panel
```

Requirements for a valid 2D small-multiple matrix:
- Row variable categorical, ordered by a meaningful criterion (not alphabetical).
- Column variable categorical or ordinal, also ordered meaningfully.
- Every cell uses identical design, scale, and encoding.
- Axis labels appear once (left edge for rows, top or bottom for columns).
- A single shared color scale / legend sits outside the matrix.

The neurometric example (*Envisioning Information*, p. 78) is exactly this: diagnostic groups (rows) × brain-wave frequency band — delta, theta, alpha, beta (columns). Reading across a row shows one patient group across all four bands; reading down a column shows how one band differs across diagnoses. Both readings are available at once, with no redesign — Tufte's "flatland within flatland."

**Averaging caveat (EI p. 78):** the neurometric contours depict only *average* differences — normalized z-scores of each diagnostic group against a healthy reference group — not the overlaps or extreme outlying values of individual members. A clean grid of group means can conceal within-group variation entirely. Name what each panel aggregates, and where variation matters, show it alongside the average.

---

## §8. Conclusion: Properties of Well-Designed Small Multiples

Tufte closes the chapter with the defining properties (VDQI, p. 175, paraphrased). Well-designed small multiples:

- **Exist to be compared** — panel weighed against panel is the array's entire job.
- **Carry several variables at once** without strain or confusion.
- **Run small and dense, resting on a large underlying table** — each panel reduced toward its legibility floor.
- **Spend nearly all their ink on data** — almost none on apparatus or decoration.
- **Read quickly** once the one shared design is learned.
- **Often tell a story** — they reveal how the relationship between variables shifts as the index changes, exposing interaction and multiplicative effects a single chart would hide.

The governing logic: minimize non-data-ink (less is more) while maximizing data-ink (less is a bore). That tension is the underlying theory of the whole pattern.

**Summary: do/don't table**

| Do | Don't |
|---|---|
| Share axis ranges across all panels | Auto-scale each panel independently |
| Shrink panels to minimum legible size | Make panels larger than the data requires |
| Array all comparison panels within one eyespan | Paginate or animate panels being compared |
| Build from a large data matrix | Apply the pattern to a tiny table where an overlay is faster |
| Use an implicit grid or hairlines to separate panels | Use dark heavy borders (creates disruptive stripes) |
| Label with the index variable directly on each panel | Repeat the full legend in every panel |
| Order panels by a meaningful criterion (time, magnitude) | Default to alphabetical or arbitrary order |
| Use 2D indexing (rows + columns) for two categorical variables | Flatten a 2D comparison into a single long row |
| Keep design, scale, encoding identical across panels | Change chart type, encoding, or scale between panels |
| Space panels proportionally to the index when intervals are uneven | Use uniform spacing regardless of uneven intervals |
| Draw almost entirely with data-ink | Add decorative fills, gradients, or chartjunk |

---

## §9. Failure Modes

**Broken scale:** each panel's axis rescales to its local data range, so every panel reaches the same height and the comparative signal vanishes. Common in spreadsheet defaults. Fix: set an explicit shared min/max on all axes.

**Eyespan violation:** panels are spread across slides, tabs, or pages, forcing comparison from memory. Fix: every compared panel must fit simultaneously in view.

**Structural drift:** panel 1 is a line chart, panel 6 a bar chart because "the data type changed," so the viewer re-learns the encoding each time. Fix: commit to one chart type at the outset; if the data genuinely forces a change, it is not a small multiple.

**Disruptive borders:** heavy black rules around each panel create a grid of white stripes where panels meet, outweighing the data. Fix: thin hairlines, white gutters, or purely spatial separation.

**Over-labeling:** every panel carries full tick labels, gridlines, and a repeated legend, consuming more space than the data marks. Fix: tick labels on outer edges only; one legend outside the array; interior panels carry only data.

**Alphabetical panel order:** the index is ordered A–Z rather than by value, time, or logical sequence, killing narrative and trend detection. Fix: order by the dimension that best surfaces the story (time, magnitude, geography).

**Too few panels:** two or three panels rarely justify the overhead — a labeled overlay reads faster. Small multiples earn their keep at roughly 4+ panels, where an overlay would produce crossing lines or color confusion.

**Tiny data matrix:** the pattern is applied to a handful of numbers, so shrinking gains nothing and the array just adds chrome. Fix: reserve small multiples for a genuinely large underlying matrix; otherwise use a single chart.

**Inconsistent aspect ratio:** panels vary in size because labels differ in length or one panel has an outlier label. Fix: fix panel dimensions absolutely; truncate or abbreviate labels rather than expanding the panel.

---
name: tufte-multifunctioning-elements
description: "Use when a chart's frames, grids, axes, ticks, or labels carry no data — round-number axes, arbitrary grid lines, blank rectangular frames — or when more variables must be encoded without adding ink; also when choosing or reviewing range-frames, dot-dash-plots, quartile plots, white grids, rug plots, or any element asked to do two display jobs at once."
tags: [tufte, data-visualization, design-efficiency, information-density, multifunctioning]
---
# Multifunctioning Graphical Elements

**Source:** *The Visual Display of Quantitative Information* (VDQI), 1983 / 2nd ed. 2001. The named design forms are introduced in **Chapter 6, "Data-Ink Maximization and Graphical Design" (pp. 123–137)**, and the unifying principle in **Chapter 7, "Multifunctioning Graphical Elements" (pp. 139–159)**, 2nd ed.

*Verification note:* page citations below are verified against the 2nd ed. (2001). One figure from a prior draft — a "~87% ink reduction" — remains unverifiable and stays out; the closest published figures are the 80→10 straightedge economics (p. 125) and the 65%-erased bar chart (p. 101).

## Overview

The same ink should usually do more than one job. A single graphical element can carry data *and* perform a design function normally handed to non-data-ink, or it can encode several variables at once. Designed with care, these *multifunctioning elements* pack complex, multivariate data into a small, legible space; designed carelessly, they collapse into puzzles only their inventor can read. The standard rectangular frame is the prime target: it does exactly two jobs — separating the data and grid from the surrounding labels, and hanging the tick marks (p. 139) — which is why it is the prime candidate for mobilization.

> "Mobilize every graphical element, perhaps several times over, to show the data." — Tufte, *VDQI*, Ch. 7

## §1. Data Measures Built From the Data

The *data measure* is the ink that actually locates or plots the value. When the data measure is built out of the data itself, the graphic gains quantitative detail and dimensions at no extra ink cost. Tukey's rule, as Tufte adopts it: if a mark must be made, make it carry meaning, and the simplest meaningful mark is a digit.

| Example (VDQI Ch. 7) | The data measure is… | Functions carried |
|---|---|---|
| **Stem-and-leaf plot** (Tukey) | The actual digits of each value | Plots the distribution *and* preserves every original number |
| **Ayres' chart of U.S. divisions in France, WWI** | Each division's own ID number | (1) count of divisions in France per month, (2) which specific divisions, (3) how long each one stayed — triple-functioning |
| **Chernoff faces** (Herman Chernoff) | A cartoon face per observation; each feature (nose length, eye shape, brow angle) = one variable | Many variables per point; outliers register instantly as faces that look like "strangers" in the neighborhood |

Tufte frames the Chernoff face as roughly the outer limit of graphical economy — and of eccentricity. Faces stay legible down to about **.05 square inches** (p. 142), because the perceptual system reads a face holistically.

## §2. The Principle Is General, Not Just Statistical

Multifunctioning is a design insight, not a statistics technique. Tufte proves the point with non-chart artifacts where physical form *is* the data.

- **George Herbert, "Easter Wings" (1633):** a shaped poem whose line length encodes magnitude — long lines for abundance, short lines for poverty, intermediate lines for transition — written ~150 years before Playfair invented statistical graphics. Line length does double duty as text and as a magnitude display.
- **W. J. Youden's typographic display of the Normal law (p. 143):** a sentence set as centered lines of monotonically *increasing* width, so the text block stacks into a triangle — a typographic pyramid, not a bell curve. Word arrangement serves as both prose and diagram.
- **Road-stripe chart (p. 144):** the **48 states** ordered by the length of painted lane stripe each one puts on its pavement, drawn as the actual stripe pattern. The data mark *is* the measured object — the graphic element and the phenomenon are the same thing. (Same family of idea as a "living histogram," where the data points physically are the thing being counted — though that is a separate figure, not this one.)

Later Tufte extends the same principle:
- *Beautiful Evidence*: a sparkline used as a linking line joins two nouns *and* reports the statistical character of their relationship over time (BE p. 73); in the closing animal scatterplot each animal's own image sits at its two-space location — data point, label, and illustration in one mark (BE p. 121).
- *Visual Explanations*: Hobbes's *Leviathan* frontispiece is built of double-functioning elements — the citizens compose the sovereign's body, and the head is the author's portrait (VE p. 138); Repton's "pole-people" scale figures measure the scene while also being content in it (VE pp. 16–17).

## §3. Data-Based Grids

Normally a grid is arbitrary coordinate scaffolding (non-data-ink). Occasionally it can report data directly — erase it and you erase measurements.

| Example | How the grid carries data |
|---|---|
| **Plasma-physics readings** | Grid is formed by the positions of the measuring instruments; a plain dot = a zero reading; blank background = no reading taken |
| **Galton's bivariate height table** | Children's heights vs. mid-parent heights; the arrangement of the data *is* the internal grid — data as grid |
| **Mitchell map (1783) vs. modern map** | The labeled grid, not the territory, is the subject; matching squares reveal how the old map stretched and twisted the earth's surface |
| **Playfair's national-debt chart** | Vertical grid lines placed at historically significant events, not at regular time intervals — the grid works with the data, a device Tufte notes is still underused |
| **3-D religion-and-politics charts (1956, 1960 vote)** | Grid lies on the data surface; reading vertical / diagonal / horizontal lines of sight isolates party effect, religion effect, and the persistence of party across both elections |

## §4. Double-Functioning Labels

Once coordinate lines can report data, so can labels. The test is the same: why spend ink on a round number when it could report a real value?

- **Range-frame with range-labels:** trim the frame to the data's extent and let the endpoints display the actual minimum and maximum instead of round numbers. More precise, and it deletes the two outermost ticks. Both range versions beat the standard passive frame.
- **Identification numbers as a time index (p. 150):** in the tungsten thermal-conductivity chart, each curve's circled ID code names the study *and*, if ordered by publication date, also encodes the time sequence of the measurements. The payoffs compound: date-ordered codes would also show which early studies anticipated the recommended curve and how the field converged on it over time — all at no additional ink.
- **Grid increments relocated to the data path:** move x-axis increments up to mark the curve's actual path, and replace the round-number y-scale with the exact data values; the column of data-positioned numbers then acts as the dot-dash-plot's marginal dashes.
- **Enhanced dot-dash-plot with data labels:** margin numbers can replace the frame, the range-frame, and the coordinate ticks at once — showing both marginal distributions and the exact paired values per observation. Best for small sets (≈ 30 observations or fewer) where fine detail matters.

## §5. The Named Design Forms

Four forms come out of putting the frame, axis, and grid to work:

- **Range-frame** — frame lines trimmed to the actual data extent on both axes; endpoints become the data's min and max. Replaces the standard non-data-bearing rectangle. Self-explanatory, no key needed.
- **Dot-dash-plot** — a scatter plus a marginal "dash" for every observation projected onto each axis. The density of dashes shows each variable's marginal distribution while the dots show the joint (bivariate) distribution. It fuses the two fundamental statistical graphics: the marginal frequency distribution and the bivariate distribution.
- **Quartile plot** — an "erased" box plot: drop the filled box and keep only the five-number summary (minimum, lower quartile, median, upper quartile, maximum). In the dot variant the **dot marks the median**; Tufte's preferred variant instead **offsets the middle half** — the IQR segment — so the quartiles read instantly (p. 124). Same information as Tukey's box plot with far less ink and no enclosed region for the eye to fight. The economics are exploratory (p. 125): ten conventional box plots take about **80 straightedge placings** (50 horizontal + 30 vertical) to draw; the erased version takes **10** — erasure pays exactly where the analyst's time should go to analysis, not line-drawing.
- **White grid** — instead of dark grid lines drawn around or over bars, thin white lines cut *through* the bars at scale intervals. The line both partitions the scale and measures the bar, reading more precisely than ticks alone, at near-zero added ink.
- **Rugplot (Tufte's own coinage, p. 135)** — a chained sequence of bivariate scatterplots linked by their shared marginal fringes, so a single observation's history can be traced through successive one- and two-dimensional contexts; the sequence of variables can wander wherever the analysis leads. *Not* the modern `geom_rug` — see the table below.

### Three distinct designs behind "rug plot" — plus the quartile plot (do not conflate)

| Form | What it displays | What each mark means | Naming |
|---|---|---|---|
| **Dot-dash-plot** | Bivariate scatter + both marginal distributions | One dash per observation, at that observation's value on each axis | Tufte's term (VDQI Ch. 6) |
| **Marginal dashes / modern "rug plot"** (`geom_rug`) | One variable's marginal distribution along an axis | One tick per observation | Modern statistics term; corresponds to Tufte's marginal dashes, which he never calls a rug |
| **Tufte's "rugplot"** | A chain of bivariate scatterplots joined by shared marginal fringes | Each panel a scatter; the shared fringe columns link adjacent panels | Tufte's coinage (VDQI p. 135) — a *different* design from `geom_rug` |
| **Quartile plot** | A distribution's five-number summary | Min, Q1, median (the dot), Q3, max only — *not* individual observations | Tufte's term (VDQI Ch. 6) |

The trap is three-way: the modern "rug plot" and Tufte's "rugplot" name different designs; and marginal dashes (one mark per observation) are routinely mislabeled as quartile summaries (five statistics). All three confusions collapse the moment you ask what one mark means.

## §6. Puzzles, and the Verbal-vs-Visual Test

Multifunctioning's failure mode is the *graphical puzzle* — a crypto-graphic the reader must decrypt. The diagnostic is mechanical: **if you must read the graphic verbally rather than visually, it has failed.** A two-variable color map with crossed scales (e.g. ~16 mixed hues) forces the reader to run little naming phrases through their head — "purplish means high on both" — instead of just seeing the value. In a good graphic the visual-to-verbal translation is learned instantly and runs automatically, so the image flows straight through the verbal decoder.

> "Seeing is forgetting the name of the thing one sees." — Paul Valéry (quoted in *VDQI*)

**Color vs. gray-scale for ordered quantities:** gray has an intrinsic visual ordering (light → dark), so a gray ramp shows magnitude more directly than color, which has no natural order and triggers the verbal-decoding loop. Tufte's galaxies map used about ten gray shades effectively. Use color for *categories*, gray for *ordered amounts*. The one *ordered* color scheme Tufte credits is Vauthier's mountain-to-the-sea convention (p. 154, via Funkhouser): snow-white summits down through green forests and yellow plains to the blue sea — color made ordinal by borrowing a natural hierarchy, where gray needs no borrowed order at all. The organizing job for any complex graphic is to structure the flow of information so the eye can peel back one layer of data at a time.

## §7. Viewing Architecture: Multiple Lines of Sight

A dense multifunctioning graphic earns its complexity when the eye can travel several clean, independent paths through it. Tufte calls the analysis of those paths the **viewing architecture**.

- **Keep each line of sight steady.** Every reading direction should stay fixed (ideally horizontal or vertical) so the eye watches for variation *off* that flat line. Ayres' WWI-divisions chart supports three: the horizon profile of the rising time-series, the vertical build of each bar, and the horizontal extent of each division's stay. Every drop of ink serves three functions, yet each function reaches the eye with its own integrity.
- **Tax table-graphic** (Current Receipts of Government as a % of GDP, 1970 and 1979, for ~15 OECD countries) reads three ways at once:
  - *Vertical* — countries ranked by tax level within each year, names spaced in proportion to the percentage.
  - *Horizontal* — paired columns show each country's change over the decade.
  - *Diagonal* — the slope of each connecting line shows the overall upward trend; unusual slopes stand out.
  The data is both integrated (connected content) and separated (uncluttered, distinct paths). Diagramming these arrows is what Tufte means by analyzing a graphic's viewing architecture, and it is how you both create and evaluate hierarchical complex displays.

*Cross-book note:* the distance-vs-close reading idea starts in VDQI itself. Page 155 defines **three viewing depths** — (1) from a distance, overall structure aggregated from microstructure; (2) up close, the fine structure of the data; (3) implicit, what lies behind the graphic — illustrated by the Census population map (~400,000 points; each dot outside urban centers = 500 people, pp. 155–157). *Envisioning Information* (1990), Ch. 2 develops that seed into micro/macro reading: cite EI for the developed doctrine, VDQI p. 155 for the origin.

## §8. Standard → Multifunctioning Redesign (what the ink gains)

| Standard design | Multifunctioning redesign | What the ink gains |
|---|---|---|
| Scatter inside a full frame drawn to round numbers | Range-frame | Frame stops at data min/max; endpoints report the range; two ticks deleted |
| Plain scatter | Dot-dash-plot | Adds each variable's marginal distribution as per-observation dashes, at ~no extra space |
| Tukey box plot (parallel comparisons) | Quartile plot (erased box) | Same five-number summary, far less ink, no enclosed box to fight |
| Round-number axis labels | Data-value labels at data positions | Labels report measured values; coordinate ticks eliminated |
| Bars over a dark background grid | White grid cut through the bars | Grid both partitions and measures; near-zero added ink, more precise read |
| Sequential color for ordered amounts | Gray-scale ramp | Removes the verbal color-decoding loop; gray carries intrinsic order |
| Curve labels that only name the study | ID numbers ordered by date | Same labels also encode the time sequence, no extra ink |
| Grid lines at regular intervals | Grid lines at meaningful events / thresholds | Grid reports on the data instead of imposing an arbitrary lattice |

## §9. Failure Modes

| Failure mode | Diagnostic | Fix |
|---|---|---|
| **Graphical puzzle** | The graphic must be decoded verbally (you name the color/symbol to read the value), not seen | Replace crossed color scales with a gray ramp or split into separate panels |
| **Inventor-only encoding** | A multifunctioning element only its designer can parse | Add organizing structure / an in-place legend, or simplify until the decode is automatic |
| **Single-function frame** | Rectangle runs to arbitrary round numbers; endpoints carry no data | Trim to a range-frame; place the actual min/max at the endpoints |
| **Coordinate-only axis** | Axis is blank between ticks; the variable's marginal distribution is invisible | Add per-observation dashes (dot-dash-plot) or relocate grid increments onto the data path |
| **Round-number labels** | Axis reads 0 / 25 / 50 / 75 / 100 while the data runs 18–73 | Label the actual data values at their positions |
| **Dot-dash / quartile conflation** | Marginal dashes described as quartile summaries, or vice versa | Dashes = one per observation at its value; quartile plot = five summary stats only (dot = median) |
| **Single viewing angle** | Multivariate data crammed into one reading direction | Engineer distinct horizontal / vertical / diagonal lines of sight (viewing architecture) |
| **Color for ordered amounts** | Reader needs a key to recover magnitude order from hues | Use a gray ramp (intrinsic order); reserve color for categories |

## §10. Do / Don't Pairs

| Do | Don't |
|---|---|
| Build the data mark from the data (stem-and-leaf digits, ID codes, shaped text) | Use a uniform abstract dot when a digit or form could carry meaning |
| Put grid lines at data-meaningful positions (events, thresholds) | Place grid lines at arbitrary round-number intervals |
| Trim the frame to the actual data extent (range-frame), endpoints = min/max | Extend the frame to round numbers beyond the data range |
| Replace round-number labels with actual data values at their positions | Label axes 0/25/50/75/100 when the data range is 18–73 |
| Add per-observation marginal dashes to show distribution (dot-dash-plot) | Describe those dashes — or be described to — as quartile summaries |
| Erase the box and keep the five-number summary (quartile plot) | Draw a full Tukey box when the box ink adds nothing |
| Use gray for ordered amounts, color for categories | Use a color ramp where gray's intrinsic ordering would read faster |
| Engineer multiple steady lines of sight; diagram the viewing architecture | Force all reading into one direction, or stack so many functions the decode goes verbal |
| Ask of every single-function element: what data could this *also* show? | Accept any element at single-function without questioning it |
| Recognize that a poem, road stripe, or typographic shape can encode data physically | Assume multifunctioning applies only to statistical charts |

---

## §11. Cross-book notes

*Beautiful Evidence* supplies four of the cleanest specimens in the whole canon, all outside conventional statistical graphics:

- **The sparkline as a linking line (BE p. 73).** A connector drawn between two nouns that is *simultaneously* a time-series of the relationship it names — the link does not merely assert that A relates to B, it reports the statistical character of that relationship over time. The general move: wherever a diagram draws a line to mean "connected," ask what the line could measure.
- **Verrocchio's dimension lines (BE pp. 72–73).** A Renaissance measuring line that carries a proportional number (1/16 of a horse's head) *and* words naming both of its endpoints. One stroke performs three jobs — geometry, quantity, and label — where a modern drawing would spend a leader line, a callout box, and a legend.
- **Barr's chart (BE pp. 64–68).** Alfred Barr's diagram of modern art serves at once as an exhibition catalog cover, the catalog's table of contents, and an analytical diagram of artistic influence. The document-level version of the principle: a whole artifact, not just a mark, can hold several functions. Barr also sizes each name's type in proportion to historical importance, exactly as city-name size works on a map.
- **The final animal scatterplot (BE p. 121).** Each animal's own image occupies its two-space position, so a single mark is at once data point, label, and illustration — the endpoint of the labels-are-data argument, and the reason Tufte resolves the label-clutter problem by layering rather than by deletion.

*Visual Explanations* adds the tightest text-image case in the pack: **Kratzenstein's vowel pipes, 1779** (p. 101). The letters A E I O U both label the five pipes of a talking automaton *and are* their content — each letter names the vowel its pipe pronounces. A label that is identical with the datum is the limit case of double-functioning. Tufte sets it against Scheiner's O-symbol on the same page, where a mark that looks like a sunspot is not one — the same design move used well and badly, side by side.

---
name: tufte-data-density
description: "Use when a graphic feels sparse, oversized, or padded for one chart's worth of data — when deciding how much data a display should carry, how small it can shrink, whether a dense chart is really cluttered or just rich, or when choosing between one big chart, small multiples, and a dense table for a large dataset."
tags: [tufte, data-visualization, information-density, data-matrix, small-multiples, data-ink]
---
# Data Density and the Size of the Data Matrix

## Overview
The chapter's title names two co-equal quantities, not one: the **density** of a graphic (data per unit area) and the **size of its data matrix** (total data the graphic carries). Tufte's empirical finding, from sampling published graphics circa 1979-1980, is that most graphics fail on both — the average published graphic shows about 50 numbers at roughly 10 per square inch, when the printed medium supports thousands per square inch and matrices in the thousands. High density is not clutter: clutter is non-data-ink competing for space; high density is data-ink filling it. The two require opposite remedies, and the governing instruction is to push both quantities up together.

Source: *The Visual Display of Quantitative Information*, Chapter 8, "Data Density and Small Multiples," pp.161-176; Chapter 7, "Multifunctioning Graphical Elements," pp.139-159.

## §1. The Two Formulas

The chapter measures two distinct things. Treat them as separate axes — a graphic can be high on one and low on the other.

**1. Data density** = number of entries in the data matrix / area of the data graphic
Area in square inches (or square centimeters). Answers: *how concentrated is the information?*

**2. Size of the data matrix** = total number of entries (rows × columns of values) the graphic displays
Answers: *how much information is there at all?*

A small, sparse table plotted at large size is low on both. Shrinking it raises density but leaves the matrix small — still weak. The cure is more data **and** less area. Density without a large matrix is just tight packing of thin evidence.

### The data matrix
The source table behind the graphic: rows × columns of numerical values. The galaxy map's matrix is 2,275,328 rectangles × 3 numbers each; a four-bar chart's matrix is 4. The matrix size is what you would need to type to reconstruct the graphic.

## §2. The Resolution Ceiling and the Typographic Yardstick

### Visual resolution sets the ceiling
The eye can locate 625 points in one square inch (100 per square centimeter) under very light grid lines. A cartographer notes the eye resolves to 0.1 mm when pushed — 254 distinctions per inch. An 80×80 grid over one square inch yields 25,281 distinct locations. Most statistical graphics use a tiny fraction of this.

### The typographic-density yardstick (p.161)
Tufte calibrates "dense" against fine printed type. The U.S. Statistical Abstract sets text at 12 lines per inch × ~23 characters per inch = **276 characters/sq in maximum**, with **~185 characters/sq in actual** (28/sq cm). That actual figure is the benchmark: a strong statistical graphic should approach the information density of dense printed text. The NYC weather chart at **181 numbers/sq in** nearly equals it — proof that graphics can be as information-rich as good typography.

### Named density benchmarks (pp.162-168)

| Graphic | Density | Note |
|---|---|---|
| 4-entry bar chart (p.162) | **0.15 numbers/sq in** (0.02/sq cm) | 26.5 sq in canvas; matrix of 4; originally printed in 5 colors |
| JASA histogram (p.164) | **3.8 numbers/sq in** (0.6/sq cm) | 32-entry matrix; "lightweight" |
| NYC weather chart (p.164) | **181 numbers/sq in** (28/sq cm) | Reduced version; matches printed-text density |
| Annual sunshine record (p.165) | **~1,000 numbers/sq in** (160/sq cm) | Monkhouse & Wilkinson record |
| Bertin's communes-of-France map (p.166) | **~9,000 numbers/sq in** (1,400/sq cm) | 27 sq in; 30,000 communes; 240,000 numbers to reconstruct |
| Galaxy map (p.166) | **110,000 numbers/sq in** (17,000/sq cm) | 2,275,328 rectangles × 3 numbers; 61 sq in; "current record" |
| USGS topo quadrangle 17×23 in (p.168) | **~250,000 bits/sq in** (40,000/sq cm) | 100 million bits total; ceiling reference |

Statistical graphics rarely reach the information rates that ordinary maps achieve — the gap is the headroom most charts leave on the table (p.168).

**Cross-book benchmarks (later Tufte):**
- *Visual Explanations* extends the yardstick to screens: a TV-resolution display shows ~53 characters where a printed page carries 1,000–50,000, and screen resolution runs roughly 5–10% of a printed map's (VE pp.149–150).
- *Beautiful Evidence* adds Graunt's Table of Casualties: 1,855 counts spanning 1629–1659 yield 1,719,585 pairwise comparisons within one eyespan — the n(n−1)/2 arithmetic of density (BE pp.178–179). The worked derivation and its use against slide-per-point formats belong to `tufte-cognitive-style`; carried here only as the density arithmetic. It also notes that newspaper sports, weather, and financial pages routinely carry hundreds to thousands of numbers with almost no chartjunk, because the content matters too much to its readers to fool with (BE pp.153, 178).

## §3. Data Density Across Publications

Tufte sampled at least 20 graphics from each publication (circa 1979-1980). Density in numbers per square inch, ranked by median. This is the complete 21-publication table from p.167.

| Publication | Median | Min | Max |
|---|---|---|---|
| *Nature* | 48 | 3 | 362 |
| *Journal of the Royal Statistical Society, B* | 27 | 4 | 115 |
| *Science* | 21 | 5 | 44 |
| *Wall Street Journal* | 19 | 3 | 154 |
| *Fortune* | 18 | 5 | 31 |
| *The Times* (London) | 18 | 2 | 122 |
| *Journal of the American Statistical Association* | 17 | 4 | 167 |
| *Asahi* | 13 | 2 | 113 |
| *New England Journal of Medicine* | 12 | 3 | 923 |
| *The Economist* | 9 | 1 | 51 |
| *Le Monde* | 8 | 1 | 17 |
| *Psychological Bulletin* | 8 | 1 | 74 |
| *New York Times* | 7 | 1 | 13 |
| *Journal of the American Medical Association* | 7 | 1 | 39 |
| *Annuaire Statistique de la France* | 6 | 1 | 25 |
| *Business Week* | 6 | 2 | 12 |
| *Newsweek* | 6 | 1 | 13 |
| *Scientific American* | 5 | 1 | 69 |
| *Statistical Abstract of the United States* | 5 | 2 | 23 |
| *American Political Science Review* | 2 | 1 | 10 |
| *Pravda* | 0.2 | 0.1 | 1 |

Source: p.167. *Wall Street Journal*, *The Times* (London), *Asahi*, and *Le Monde* publish data-rich graphics comparable to academic journals; most U.S. papers and magazines publish less data per graphic than the leading papers of other industrialized countries. The typical published graphic carries about 50 numbers at ~10 per square inch.

## §4. Size of the Data Matrix — the Co-Equal Axis

The p.167 table also records the **size of the data matrix** (numbers per graphic) alongside density. Matrix size is the second half of the chapter's title and the second half of the maximization rule — a high-density graphic built on a tiny matrix is still thin evidence. Verified matrix-size anchors:

| Reference | Matrix size (numbers/graphic) | Meaning |
|---|---|---|
| Typical published graphic | **~50** | Tufte's overall finding; the low baseline to beat |
| *Journal of the Royal Statistical Society, B* (median) | **200** | Largest median matrix among the 21 sampled publications |
| *Nature* (median) | **177** | Highest median *density* in the sample; its median matrix trails JRSS-B (JASA: 150) |
| *New England Journal of Medicine* (densest sampled) | **up to ~3,600** | Top of the sampled range — a single graphic carrying thousands of values |
| Bertin communes map | **240,000** | Numbers required to reconstruct it |
| Galaxy map | **~6,800,000** | 2,275,328 rectangles × 3 numbers |

Read this against §3: the two axes have different leaders — *Nature* tops density (48/sq in median) while *JRSS-B* tops matrix size (200 median), so no single publication wins both. Raising density by shrinking a 50-number chart helps; the larger win is carrying 200 or 3,600 numbers in the first place.

## §5. The Dual Maximization Principle

> "Maximize data density and the size of the data matrix, within reason." — Tufte, *The Visual Display of Quantitative Information*, p.168

Both nouns are load-bearing. "Within reason" is narrow: if a graphic overcrowds, apply data-reduction (averaging, clustering, smoothing) **before** plotting — thin the numbers if you must, but do not enlarge the area as a first resort. And the bar for "overcrowded" is high: Tufte's caveat is that a display representing several thousand numbers may be just fine as it stands, needing no reduction at all (p.168).

### Why more information wins
- The marginal cost of handling additional information is low for most graphics.
- Simple data belongs in a sentence or small table; graphics earn their place with complexity.
- One page, one glance: the more on the page, the more the eye can compare across it.
- Data-rich displays lend context and credibility; sparse ones invite suspicion about what was left out and why so little is shown (p.168).
- There is a direction of travel: a summary graphic can be distilled out of a high-information display, but a low-information design has nowhere to go but a redesign (p.168).

### Mark size must scale inversely with data volume
As the matrix grows, the marks must shrink — smaller dots in dense scatters, thinner lines in busy time-series (p.169). Hold mark size constant as n rises and the graphic overprints into noise.

## §6. The Shrink Principle

Beyond enlarging the matrix, the primary lever for density is reducing the graphic's area.

> "Small multiples reflect much of the theory of data graphics." — Tufte, *The Visual Display of Quantitative Information*, p.175

Tufte's finding: many published graphics can be cut to half their printed size with no loss of legibility or information — that alone doubles density without adding a data point. Repeated shrinking leads to the small multiple. Bertin's crisp, thin line style in *Sémiologie Graphique* shows the ceiling: 17 small graphics on one page alongside extensive text, impossible at conventional American chart sizes.

### Do / Don't: Shrinking

| Do | Don't |
|---|---|
| Shrink graphic area to raise density | Enlarge the canvas to "give data room to breathe" |
| Run many small graphics per page | Spend a full page on a 12-point chart |
| Use crisp, thin weights that survive reduction | Add weight, shadow, or fill to compensate for smallness |
| Apply data-reduction (averaging, smoothing) if overcrowded | Delete data points to lower apparent density |

## §7. Three Viewing Depths and Viewing Architecture

Two organizing ideas from ch.7 directly serve high density (pp.154-159).

### Three viewing depths (p.155)
1. **Distance view** — overall structure, aggregated from the microstructure.
2. **Close-up** — the fine structure of the data, read in detail.
3. **Implicit** — what sits behind the graphic, underlying it.

Payoff: one dense graphic serves several analytical purposes at once. The Census population-density map shows all three — the urban/rural pattern at a distance, county detail up close, and the implicit landform geography that shapes settlement.

### Viewing architecture (p.159)
Organize multivariate information so different aspects reach the eye through separate, uncluttered paths, each line of sight held steady (ideally horizontal or vertical). The government tax-receipts table-graphic (15 countries, 1970 and 1979) reads three ways: vertically to rank countries, horizontally for paired comparison, diagonally along slopes for change. Integrated by content, separated so the eye never crosses paths. This kind of analysis helps build and evaluate designs that organize complex information hierarchically.

## §8. Multifunctioning Elements as Density Tools

Elements that serve more than one display function raise effective density without adding ink (ch.7). Each move erases non-data-ink and replaces it with data-ink.

### Data-based grids (pp.145-148)
Grids placed at measurement-instrument locations or data-significant events report on the data themselves. Playfair sets vertical grid lines at historic events, not regular intervals — the grid becomes evidence. Erasing a data-based grid erases data; erasing a decorative grid erases nothing.

### Range-frame and data-based labels (pp.149-152)
Replace the round-number axis frame (0 to 40) with a range-frame spanning only the actual extremes (4 to 37): two non-data ticks gone, the data range now encoded in the frame. Replace round-number scale labels with exact data values and each label becomes a measurement.

### Dot-dash-plot (marginal dashes)
Marginal distribution marks along both scatterplot axes. A vertical column of data-positioned numbers doubles as the dashes showing the marginal distribution — no extra ink, since the numbers replace conventional ticks. Best for ≤30 observations, where fine detail reads. (The modern "rug plot" / `geom_rug` corresponds to these marginal dashes; do not call the dot-dash-plot a rugplot — Tufte reserves that word for a different design, below.)

### Tufte's rugplot (p.135)
A chained series of bivariate scatterplots joined by their shared marginal dashes, so a single observation's history can be traced through successive one- and two-dimensional contexts; the sequence of variables can wander wherever the analysis leads. The shared fringes are what link the panels — each dash column serves two adjacent scatters at once.

**Design test:** before adding any structural element (frame, grid, tick, label), ask whether that same ink can also show data. If yes, the multifunctioning version wins.

## §9. Density Is Not Clutter

The most common misreading of dense graphics. The two differ in source and need opposite remedies.

| Concept | Definition | Source | Remedy |
|---|---|---|---|
| **High density** | Many data entries per unit area | Large data matrix | Preserve; increase where possible |
| **Clutter** | Non-data-ink or redundant data-ink crowding the field | Chartjunk, decorative grids, heavy borders | Erase |

The cost of chartjunk scales with density (p.169): in a sparse 10-number graphic a decorative border is merely wasteful; in a dense 2,000-number graphic the same border actively competes with data, so the penalty is proportionally larger.

**Test before cutting:** classify the element. Non-data-ink → remove. Data-ink → keep by default; the burden of proof is on removal.

## §10. Density by Chart Type — Measured and Ranked

| Chart type | Typical density | Tufte's verdict |
|---|---|---|
| 4-entry bar chart | **0.15/sq in** (p.162) | Matrix of 4; "thin indeed"; a table is superior |
| Single pie chart | Very low | A table nearly always beats it |
| Multiple pie charts | Very low | "Completely useless" (Bertin); eye compares in spatial disarray |
| JASA histogram | **3.8/sq in** (p.164) | 32-entry matrix; "lightweight" |
| Scatterplot | Medium–high | Scales with n; shrink dots as n grows |
| NYC weather chart | **181/sq in** (p.164) | High-density news benchmark; ≈ printed-text density |
| Annual sunshine record | **~1,000/sq in** (p.165) | Upper range for printed statistical graphics |
| Statistical table / supertable | High | Best for exact values and many localized comparisons |
| Small multiples | High | Preferred format for complex multivariate data |
| Detailed geographic map | **9,000–110,000/sq in** | Ceiling; most statistical graphics sit orders of magnitude below |

Tufte's verdict on pies is categorical: their low density and failure to order numbers along a visual dimension mean they should never be used (p.178).

## §11. Small Multiples — Density at Scale

> Scope: this section covers small multiples **only as a density instrument**. The pattern itself — invariants, panel structure, ordering, eyespan, failure modes — is owned by `tufte-small-multiples`; go there for the mechanics.

The primary pattern for high density across complex, multivariate data: a series of graphics showing the same variable combination, indexed by a changing variable. The design stays constant so attention goes entirely to shifts in the data.

### Seven-property conclusion (p.175, paraphrased)
Well-designed small multiples: exist to be compared panel against panel; carry several variables at once without strain; are reduced in size and dense with data; usually rest on a large underlying matrix; spend nearly all their ink on data rather than apparatus; read quickly once the one shared design is learned; and often tell a story — how relationships shift as the index variable changes, revealing interaction or multiplicative effects.

### Examples Tufte cites (pp.170-174)

| Dataset | Structure | Data volume |
|---|---|---|
| LA air pollution — reactive hydrocarbons (p.170) | 23 hourly frames, geographic heat maps of the LA basin | 23 maps × spatial grid (McRae, Goodin, Seinfeld video) |
| Cancer melanoma sites — Wiskemann (p.171) | Head-and-neck diagrams by sex | 269 primary sites across 3 panels |
| Herring catch age distribution 1908–1913 (p.172) | Stacked line charts by year | 6 panels × age distribution |
| Sampling error in normal deviates (p.172) | Distribution curves | 12 panels × 50-observation samples |
| Human/ape chromosome comparison (p.173) | Vertical band diagrams | 22 autosomes + XY × 4 species |
| *Consumer Reports* repair frequency 1976–1981 (p.174) | Dot-matrix table-graphic hybrid | 19 rows (17 trouble spots + Trouble Index + Cost Index) × car models × 6 years |

The *Consumer Reports* layout mixes table and graphic: the dot-matrix grid itself becomes the data structure, portraying manufacturer × car type × year × trouble spot in one field. (Note: the matrix is 17 trouble spots **plus** a Trouble Index and a Cost Index — 19 rows total; do not state "19 trouble spots.")

### Design rule
Hold axis scales, format, and encoding constant across every frame; let only the data change. Any design variation across frames turns a comparison of data into a comparison of designs.

## §12. The Supertable — High Density Without Graphics

> Scope: the supertable's design grammar and the sentence → text-table → table → semi-graphic → graphic format ladder are owned by `tufte-tables-and-text-tables`. What follows is only the density case for choosing a table.

Not every high-density display is a graphic. A well-built statistical table can carry more data per area than most charts, and beats a graphic when exact values or many localized comparisons matter.

> "One supertable is far better than a hundred little bar charts." — Tufte, *The Visual Display of Quantitative Information*, p.179

The worked example is the 410-number *New York Times* presidential-vote table (Nov 9, 1980, p.179): horizontal rules split data into topical paragraphs; rows ordered to tell a story; downward reading (within cluster) and across reading (cross cluster) answer different questions.

**Use a supertable when** the data needs many localized comparisons, exact values matter more than spatial pattern, and the data gains little from a graphic's spatial-comparison advantage.

## §13. Failure Modes

**1. Starting sparse.** Designing a low-density graphic and calling it "clean." There is nowhere to go — adding data forces a redesign. Summary graphics distill out of high-information ones, never the reverse.

**2. Small matrix, packed tight.** Raising density by shrinking a thin matrix and declaring victory. Density is only half the rule; a 50-number chart shrunk small is still 50 numbers. Grow the matrix.

**3. Confusing density with clutter.** Deleting data to "reduce clutter" when the real problem is chartjunk. Fixes the wrong variable and loses information.

**4. Enlarging to accommodate data.** Growing the canvas instead of shrinking the marks. Density falls, cross-page comparison gets harder, the eye travels further.

**5. Fixed mark size as data grows.** Holding dot diameter or line weight constant as n rises. The graphic overprints and density collapses into noise — marks must shrink as volume grows.

**6. The pie-chart reflex.** Among the lowest-density formats; can't stack into useful multiples; fails to order numbers along a visual dimension.

**7. Separating words from the field.** Exiling labels and notes to a legend. Data-positioned labels, notes, and captions are data-ink; a legend wastes the field and imposes navigation cost.

**8. Decorative grids at high density.** Conventional grids compete directly with dense data marks; a data-based grid (keyed to data-significant positions) adds information at the same ink cost.

## §14. The Governing Aphorism

Tufte closes ch.8 on the asymmetry between the two kinds of ink: cut non-data-ink (decoration, redundancy, chartjunk); never cut data-ink, because removing it removes information. He frames it by borrowing two architectural slogans — Mies van der Rohe's "less is more" for non-data-ink, and Robert Venturi's retort "less is a bore" (*Complexity and Contradiction in Architecture*, 1966; the VDQI footnote cites the 2nd ed., 1977) for data-ink (footnote 6, p.175). So: **for non-data-ink, less is more; for data-ink, less is a bore.**

Operational test before any edit: classify the element first. Non-data-ink → remove it. Data-ink → preserve by default; the burden of proof is on removal.

## §15. Design Checklist

| Check | Pass condition |
|---|---|
| Matrix size | Is the source matrix as large as the question warrants (beating the ~50-number baseline; nearer the leading journals' medians — *Nature* 177, *JRSS-B* 200)? |
| Density benchmark | Computed density above ~10/sq in (JASA territory)? Strong graphics approach ~185/sq in printed-text density |
| Both axes | Are density **and** matrix size both being pushed up, or only one? |
| Graphic area | Could it shrink to half size without information loss? |
| Mark size | Are dots/lines sized to data volume, not aesthetic convention? |
| Chartjunk | Is every ink mark either data or necessary structure? |
| Multifunctioning | Can any frame/grid/tick/label be replaced with a data-carrying version? |
| Viewing depths | Rewards both distance (overall pattern) and close-up (fine structure)? |
| Viewing architecture | Are the reading paths (vertical, horizontal, slope) uncluttered and independent? |
| Chart type | Is a small-multiple or supertable available that carries more data? |
| Pie-chart trap | Any pie used? Replace with a dot chart or table |
| Clutter vs density | Is a proposed cut removing data or removing decoration? |
| Supertable candidate | Does the data need many localized exact comparisons? Consider a supertable |

---
name: tufte-tables-and-text-tables
description: "Use when choosing between a sentence, text-table, table, semi-graphic, or chart for a set of numbers; when ~20 or fewer values are about to become a graphic; when designing or auditing any data table — row order, clustering, rules, alignment; when dozens of little bar or pie charts could collapse into one dense reference table; or when a table needs graphical properties: slopes, value-glyphs, or data-proportional spacing."
tags: [tufte, tables, text-tables, supertable, semi-graphics, format-selection, data-visualization]
---
# Tables and Text-Tables: The Choice of Design

## Overview
Tufte treats the table not as the graphic's poor relation but as one rung on a continuous ladder of display formats — sentence, text-table, table, semi-graphic, graphic — with the choice governed by the content, the extensiveness of the labels, and the volume and ordering of the data (p. 178). Two findings anchor the skill: tables usually beat graphics for small data sets of roughly twenty numbers or fewer (p. 56), and a single well-structured *supertable* can outperform whole fields of little charts (p. 179). Between the plain table and the full graphic sits a rich middle territory — semi-graphic tables that keep exact values and row/column addressability while borrowing position, slope, spacing, or glyphs from graphics (pp. 145, 158–159, 174, 180).

This skill is the deep treatment of that territory. Siblings touch it in passing: **`tufte-data-density`** §12 states the supertable-beats-chart-litter claim as a density result; **`tufte-aesthetics-and-technique`** §6 compresses the format ladder into one selection table; **`tufte-multifunctioning-elements`** carries the general doctrine behind two of the hybrids here (data-as-grid, viewing architecture). Cross-reference them; the table-design grammar lives here. For the typography inside numeric columns, see **`tufte-typography-for-data`**.

## §1. The Format Ladder — Five Rungs (pp. 178–180)

Tufte names three basic structures for showing data — sentence, table, graphic — and notes that two or three of them frequently belong together in one display (p. 178). Expanded to its full resolution, the ladder has five rungs:

| Rung | Structure | Effective dimensions | Best for | Breaks down when |
|---|---|---|---|---|
| 1. Sentence | Numbers embedded in running prose | <1 — linear word-flow, folded at arbitrary points | One or two numbers in context | Three or more numbers need comparing |
| 2. Text-table | Numbers pulled out of the prose and aligned in a small labeled column | 1 — a single ordered list | A handful of values the reader should compare | Multiple variables or many rows appear |
| 3. Table | Rows × columns of exact values, ordered and clustered | 2 — row and column addressing | Exact values; small data sets; many localized comparisons | Only overall shape or pattern matters and n is large |
| 4. Semi-graphic | A table wearing one or two graphical properties (position, slope, glyph, spacing) | 2+ — lookup plus visual pattern | Highly labeled numbers; simultaneous exact-value and pattern reading | The graphical dressing costs more than it reveals |
| 5. Graphic | Full visual encoding | 2 spatial + retinal channels | Large data sets; shape, trend, distribution, exception | The data set is small — the apparatus outweighs the content |

> "The conventional sentence is a poor way to show more than two numbers because it prevents comparisons within the data." — Tufte, *VDQI*, p. 178

The sentence's failure is structural, not stylistic: the flow of words folds over at points decided by column width, not by content, so it offers less than one effective dimension for organizing data (p. 178). The fix is the *text-table* — keep the prose framing, but pull the numbers out of the sentence and set them as a small aligned column so the eye can run down them:

```
Instead of:  "Nearly 53 percent of the type A group did something
             or other compared to 46 percent of B and slightly
             more than 57 percent of C."

Text-table:  The three groups differed in how they did something:
                 Group B   46%
                 Group A   53%
                 Group C   57%
```

The ladder is not a status hierarchy. Moving up a rung is justified only by the data's size and the reader's task — moving a 6-number comparison from rung 2 to rung 5 is a downgrade dressed as sophistication.

**The pie chart has no rung.** A table is nearly always better than a dumb pie chart, and several pies are worse than one — the viewer is left comparing quantities strewn in spatial disarray, inside each circle and across them. Low in data-density and unable to order numbers along a visual dimension, the pie draws Tufte's flat verdict that "pie charts should never be used" (p. 178; his footnote cites Bertin, who calls multiple pies "completely useless").

## §2. The Twenty-Number Rule — and Why Tables Resist Misperception (p. 56)

> "Tables usually outperform graphics in reporting on small data sets of 20 numbers or less." — Tufte, *VDQI*, p. 56

Graphics earn their special power, Tufte adds in the same breath, on *large* data sets (p. 56). The rule's context matters as much as its threshold. It arrives at the end of Tufte's review of perception experiments: viewers decode graphical areas by approximate power laws (reported perceived area ≈ actual area^0.8±0.3 for circles), perceptions differ across people, change with experience, depend on context — and even the reported perception of plain line length shifts with what other people have already said about the lines (pp. 55–56). A graphic is an estimation task run through unreliable perceptual hardware. A table is not: reading the printed value 46 is not a psychophysical judgment. For small data sets, the table sidesteps the entire decoding-variability problem — that is *why* it outperforms, not merely a taste preference.

Operational form:

| Data set | Default format |
|---|---|
| 1–2 numbers | Sentence |
| ~3–20 numbers | Text-table or table |
| Dozens to hundreds, exact values + localized comparisons | Table / supertable (§4) |
| Hundreds up, pattern and shape the point | Graphic — or a semi-graphic hybrid (§5) |

Treat 20 as a calibration point, not a cliff: the question at every n is whether the reader's task is *look up and compare exact values* (table wins) or *see shape, trend, exception* (graphic wins) — and whether both, in which case combine devices (p. 178).

The rule has a founder's precedent. Playfair — the inventor of the bar chart, and graphics' first great partisan — conceded the point about his own invention: discussing the one bar chart in *The Commercial and Political Atlas*, Tufte summarizes Playfair's self-criticism with the verdict that small, noncomparative, highly labeled data sets usually belong in tables (p. 33).

## §3. Ordering: Content Beats the Alphabet (p. 178)

The alphabet is almost never the best row order — content or the data's own values nearly always sequence better (p. 178). Tufte's own three-line text-table is re-sorted from A/B/C to ascending value (B 46, A 53, C 57) to make the point at the smallest possible scale, and the supertable scales it up: its rows are ordered so as to tell an ordered story about the elections (p. 179).

- **Alphabetical order encodes nothing.** It serves only name-lookup in long reference lists. In any table meant to be *read* rather than *consulted*, sorting by the data turns the row sequence itself into an additional display dimension — rank becomes visible for free.
- **Ordering is the cheapest graphical property a table can acquire.** Before adding any glyph or slope (§5), sort. A sorted column is already half a bar chart.
- The same principle condemns the pie (§1): it fails to order numbers along a visual dimension. A sorted table succeeds precisely where the pie fails.

For fine-grained table craft beyond ordering, Tufte's pointer (p. 178, fn. 1) is A. S. C. Ehrenberg's "Rudiments of Numeracy," *Journal of the Royal Statistical Society* A, 140 (1977), 277–297 — Ehrenberg's rudiments (his guidance, not VDQI's) include rounding to two effective digits so mental arithmetic works, providing row and column averages as anchors, and putting figures to be compared in columns rather than rows.

## §4. The Supertable — Design Grammar of a 410-Number Table (p. 179)

The worked masterpiece is the table Tufte designed for the *New York Times* (Nov. 9, 1980, p. A-28) showing how different groups voted for President: 410 numbers from 12,782 exit-poll interviews, organized as group-by-group percentages for Carter/Reagan/Anderson 1980 plus a Carter–Ford 1976 column.

> "One supertable is far better than a hundred little bar charts." — Tufte, *VDQI*, p. 179

Its grammar, element by element:

| Element | Function |
|---|---|
| Horizontal rules at group boundaries | Divide the data into *topical paragraphs* — party, ideology, region, race, sex, religion, age, income, occupation, education, union, finances, issues, time-of-decision |
| Row clusters of three to seven lines | One readable "paragraph" per topic; small enough to scan as a unit, large enough to carry a comparison |
| Across-the-line reading | Compares the 1980 election against 1976 for each group — the between-elections question |
| Downward reading within a cluster | Conducts within-election analysis — how did the vote vary across a topic's categories |
| Row order within and across clusters | Sequenced to tell an ordered story about the elections, not to alphabetize groups |
| Parenthetical share-of-electorate figures | Weight each row so the reader knows how big each group is |

Two distinct reading directions answering two distinct questions, carried by nothing but rules, clustering, and order — no plotted marks at all. The result is a table built to attract and intrigue — organized, sequential detail with the feel of a reference work (p. 179): a reader can graze it, interrogate it, or look up their own demographic.

**When the supertable is the right call** (converging with `tufte-data-density` §12): many localized comparisons; exact values matter; the audience includes both grazers and looker-uppers; and the alternative on the table is a wall of small charts, one per group — a hundred little bar charts would shatter the across-and-down reading structure into isolated fragments.

**Prose-like tables.** For sets of highly labeled numbers, a wordy data graphic coming close to straight text works well — Tufte's example is the *Times* "Some Winners and Losers in the Forecasting Game" panel (Jan. 2, 1979, p. D-3), where eight forecasters' predictions for five key 1978 economic indicators are set as ranked stacks of labeled entries above and below a black band carrying the year's results: a table of numbers organized into a graphic (p. 180).

## §5. Semi-Graphic Hybrids — Tables Wearing Graphical Properties (pp. 145, 158–159, 174, 180)

Table entries can also be arranged in semi-graphical form (p. 178). Each hybrid keeps the table's virtues — exact values, labels at the point of need, row/column lookup — and adds exactly one or two graphical properties:

| Hybrid | What stays tabular | What becomes graphical | Source |
|---|---|---|---|
| Galton's bivariate height table | Cells hold exact frequencies of adult-children × mid-parent heights | The row/column arrangement *is* a coordinate plane — data as internal grid — so a fitted ellipse and axes can be drawn directly over the table | p. 145 (from Pearson's *Life* of Galton) |
| Government tax-receipts table-graphic, 1970 vs 1979 | Two labeled columns of exact percentages, 15 countries | Vertical position spaced in proportion to the values; connecting lines whose slopes encode change | pp. 158–159 |
| *Consumer Reports* repair records, 1976–1981 cars | Row = trouble spot, column = model year, panel = model; full lookup addressability | Each cell's value set as a five-step circle glyph (much better → much worse than average), so columns and rows read as visual patterns | p. 174 (*Consumer Reports*, April 1982) |
| Forecasting-game panel | Every entry a labeled forecaster + exact figure | Vertical rank-ordering around the black results band | p. 180 |

**The slopegraph's three simultaneous readings (p. 159)** make it the clearest demonstration of what a semi-graphic buys. Read *vertically*, it ranks the 15 countries within each year — and because names are spaced in proportion to the percentages, the gaps carry data too. Read *across*, each country's pair shows its change over the decade. Read *down the collection of slopes*, the overall upward pattern emerges and lines of unusual slope stand out. The display is at once integrated — through its connected content — and separated, the eye tracing several distinct, uncluttered paths across it: Tufte's *viewing architecture* (deep treatment in `tufte-multifunctioning-elements` §7).

**Galton's table** earns its place in history: the way the data are arranged creates an internal grid — Tufte's rare case of "data as grid" (p. 145) — and because the table is simultaneously a scatterplot of frequencies, it hosts an analytical overlay drawn directly on it: the ellipse and axes of the correlation surface, as reproduced from Pearson's *Life* of Galton. A semi-graphic table is not just a display; it can be an instrument of discovery.

**Design discipline for hybrids:** add graphical properties one at a time, and only when each property answers a named reader question (rank? change? pattern-across-cells?). A table dressed in three decorations is chartjunk with cell borders; a table wearing one earned property is a second reading direction for free.

## §6. Table Craft — the Rest of the Book Applied to Tables

The book's general principles bear directly on table construction:

- **The five data-ink principles govern tables too (p. 105):** above all else show the data; maximize the data-ink ratio; erase non-data-ink; erase redundant data-ink; revise and edit. In table terms: the digits, labels, and functional rules are the data-ink; cell borders, zebra fills, and repeated units are the first candidates for erasure. Note that the supertable's horizontal rules survive this test — they carry the topical-paragraph structure (§4); a rule that clusters is data-organizing ink, a grid that cages every cell is not.
- **Friendly-graphic standards apply (p. 183):** words spelled out, no mysterious abbreviations; text runs left to right; type upper-and-lowercase with serifs, clear and modest; no legend-like indirection between a code and its meaning.
- **Paragraphs about data (p. 181):** Tufte's integration principle — data graphics are paragraphs about data, and tables with them — means running the table into the text at its point of reference rather than exiling it to a figures ghetto, and avoiding ruled lines that separate different types of information within the display.
- **Ordering before decorating (§3):** the sort order is part of the design, chosen with the same care as the clustering.

## §7. Decision Tests

Run these in order; stop at the first decisive answer.

1. **Count.** Two numbers or fewer → sentence. Three to ~20 → text-table or table (p. 56). More → continue.
2. **Task.** Does the reader need exact values or localized comparisons? → table or supertable (pp. 178–179). Shape, trend, distribution across a large set? → graphic. Both? → combine devices, or a semi-graphic (pp. 178, 180).
3. **Labels.** Are the numbers heavily labeled, each entry a named thing? → a wordy, near-text arrangement works well (p. 180).
4. **Litter check.** Is the current design many small charts of the same form, one per category? → one supertable is far better (p. 179).
5. **Hybrid check.** Would one graphical property — sort order, proportional spacing, slopes, value-glyphs — add a second reading direction the task needs? → semi-graphic (§5). If no property answers a named question, stay plain.
6. **Pie check.** Is any rung being skipped in favor of a pie? → back to a table (p. 178).

## §8. Do / Don't

| Do | Don't |
|---|---|
| Put one or two numbers in the sentence itself | Smear three or more comparable numbers through prose |
| Pull comparable numbers into an aligned text-table | Let column-width happenstance decide where numbers fall |
| Default to a table at or below ~20 numbers | Chart a handful of values for the look of rigor |
| Order rows by content or data values | Default to alphabetical order in a table meant to be read |
| Cluster rows in 3–7-line topical paragraphs set off by rules | Run 40 undifferentiated rows, or box every cell in a full grid |
| Design across-and-down readings that answer different questions | Treat row order and rule placement as afterthoughts |
| Use one supertable for many localized comparisons | Scatter the same data across dozens of little bar charts |
| Add a single earned graphical property (sort, spacing, slope, glyph) | Decorate a table with unearned graphics — or reach for a pie |
| Keep exact values legible inside a hybrid | Trade the table's precision away for the graphic's costume |
| Run the table into the text at its point of reference | Exile it to an appendix the argument never touches |

## §9. Named Failure Modes

**FM1 — Sentence smear.** Three or more comparable numbers strung through running prose, where the word-flow's fold points prevent any within-data comparison. *Fix:* text-table — same words, numbers pulled out and aligned (p. 178).

**FM2 — Premature graphication.** A dozen numbers promoted to a bar or line chart for apparent sophistication, converting exact values into an unreliable perceptual estimation task. *Fix:* the twenty-number rule; use a table (p. 56).

**FM3 — Alphabetical default.** Rows sorted by name in a table meant for reading, wasting the row dimension on an encoding of nothing. *Fix:* sort by content or values; keep alphabetical only for pure name-lookup references (p. 178).

**FM4 — Chart-litter.** One small chart per category — a hundred little bar charts — destroying every across-category reading. *Fix:* one supertable with topical paragraphs and 3–7-line clusters (p. 179). (Distinguish from true small multiples, which share one design to support comparison — see `tufte-small-multiples`; chart-litter fragments a single table's worth of comparisons.)

**FM5 — Pie escalation.** A pie chart, then several, comparing quantities in spatial disarray within and between circles. *Fix:* a sorted table; there is no rung for pies (p. 178).

**FM6 — The caged table.** Full-grid cell borders, zebra stripes, and heavy boxes imprisoning the digits — rules used as decoration rather than as topical paragraphing. *Fix:* erase non-data-ink; keep only the rules that cluster (pp. 105, 179, 181).

**FM7 — Costume hybrid.** A semi-graphic whose graphical dressing answers no reader question — glyphs, color fills, and mini-charts stacked onto a table for visual interest. *Fix:* one property per named question, or return to the plain table (§5).

**FM8 — Format monogamy.** Forcing everything into a single structure when the content calls for combination — sentence, table, and graphic are devices to mix, and a display frequently needs two or three at once (p. 178).

## §10. Application Checklist

| Check | Pass condition |
|---|---|
| Rung fit | Format chosen by count, task, and labels (§7), not by habit or prestige |
| Twenty-number gate | No graphic standing where ≤ ~20 numbers needed a table |
| Sentence load | No sentence carrying more than two comparable numbers |
| Row order | Sequence encodes content or values; alphabetical only for lookup |
| Clustering | Rows grouped in 3–7-line paragraphs; rules mark topic boundaries only |
| Reading directions | Across and down each answer a distinct, nameable question |
| Supertable audit | Any field of little same-form charts collapsed into one table |
| Hybrid audit | Each graphical property maps to a named reader question |
| Precision retained | Exact values still readable in any semi-graphic form |
| Ink audit | Digits, labels, functional rules only; borders, fills, repeats erased |
| Type craft | Spelled-out words, left-to-right, upper-and-lowercase serifs (see `tufte-typography-for-data`) |
| Integration | Table placed at its point of reference in the argument |

---

Sources: *The Visual Display of Quantitative Information*, Edward Tufte, 2nd ed. — the choice of design: sentences, text-tables, tables, semi-graphics, and graphics, pp. 178–180; tables vs. graphics for small data sets, pp. 55–56; data-ink principles, p. 105; Galton table-graphic, p. 145; tax-receipts slopegraph and viewing architecture, pp. 158–159; *Consumer Reports* table-graphic, p. 174; supertable, p. 179; data/text integration, p. 181; friendly-graphic standards, p. 183; table-design pointer to Ehrenberg, "Rudiments of Numeracy" (1977), p. 178 fn. 1.

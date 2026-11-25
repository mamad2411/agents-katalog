---
name: tufte-escaping-flatland
description: "Use when a chart, map, dashboard, table, or display must carry more than two variables and the flat surface is running out of room — symptoms include fake 3-D or ornament standing in for data, one separate mark per variable, density so thin it invites suspicion, or uncertainty about which of Tufte's five envisioning methods (micro/macro, layering, small multiples, color, space-time narratives) the problem calls for."
tags: [tufte, data-visualization, information-design, dimensionality, data-density, multivariate]
---
# Escaping Flatland

## Overview

The world is multivariate; paper and screen are not. Every image a maker shows a reader must live on a two-dimensional plane, so the central job of information design is to widen the resolving power of that plane — to raise both the number of dimensions it can carry and the density of data it packs per unit area. This is the opening, agenda-setting chapter of *Envisioning Information*: it states the problem, sets the two goals, previews the five methods that the rest of the book develops, and names the enemy — chartjunk and the architectural "duck," design that becomes its own content out of contempt for the data and the audience.

**Read this skill for the framework and the chapter's gallery of worked examples.** For the deep mechanics of each method, go to its dedicated sibling skill (named in §2). Do not treat the five methods as six "strategies" — density is a *goal*, not a method.

---

## §1. The Flatland Problem

The term comes from Edwin A. Abbott's novel *Flatland: A Romance of Many Dimensions* (London, 1884), about beings trapped in a two-dimensional world. Tufte's application: we navigate a three-space perceptual world and reason about higher dimensions with ease, yet every information display collapses onto the flatland of paper and screen.

> "Escaping this flatland is the essential task of envisioning information." — Tufte, *Envisioning Information*

**The toad image (chapter opener, p.14):** when a toad sheds its skin, the suit leaves life's "spaceland" and collapses into flatland — exactly what our displays do to multivariate reality. The task is to do better than a flattened-out toad suit.

**Why it gets harder:** two forces compound the difficulty.

| Force | Effect |
|---|---|
| Abstraction | As data loses its tie to familiar three-space (temperature, GDP, sentiment), there is no physical form to lean on |
| Variable count | Each extra variable competes for the same two axes of the surface |

**The chapter's closing frame (p. 33):** we envision information in order to reason about, communicate, document, and preserve knowledge — activities conducted almost entirely on two-dimensional paper and screen. The escapes grow harder along exactly the two axes above: as the data's ties to familiar three-space weaken (ever more abstract measures) and as the dimension count climbs (ever more complex data).

**The fundamental compromise:** nearly every escape from flatland trades one virtue for another. The literature is "partial, arbitrary, and particularistic" — no single trick solves dimensional compression in general. Paul Klee made the related point that a whole built from parts of different dimensions is hard to grasp and harder still to convey to someone else, because spoken language is sequential and cannot hold many dimensions at once. Expect tradeoffs; do not chase a universal solution.

---

## §2. The Real Taxonomy — Two Goals, Five Methods (p.13, previewed p.33)

This is the chapter's actual structure. **Do not invent a six-item "strategies" list.** Tufte names two goals and five methods; data density is one of the two goals, not a method standing beside the other four.

**The two goals — what every display is trying to do:**

| Goal | Definition |
|---|---|
| Increase dimensions | Raise the number of variables representable on a plane surface, without confusion |
| Increase data density | Raise the amount of information per unit area |

**The five methods — how displays reach those goals (each developed in its own sibling skill):**

| Method | One-line mechanism | Go deep in |
|---|---|---|
| Micro/macro readings | Fine detail aggregates into a global pattern; both visible at once | `tufte-micro-macro-readings` |
| Layering and separation | Visually distinct layers coexist on one surface and read both apart and together | `tufte-layering-and-separation` |
| Small multiples (multiplying images) | One design repeated across panels that vary by one variable; decode once, compare freely | `tufte-small-multiples` |
| Color | Encodes a named variable or separates overlapping layers — used with discipline | `tufte-color-in-information-design` |
| Narratives of space and time | The path of an entity through space and/or time, plotted as visual syntax | `tufte-narrative-and-sequence`, `tufte-space-time-graphics` |

Related ideas the chapter leans on: multiple-functioning marks (`tufte-multifunctioning-elements`), chartjunk (`tufte-chartjunk`), data density (`tufte-data-density`). This skill's job is the *framework plus the chapter's examples*; the sibling skills carry the method theory.

---

## §3. The Cost of Surrender — The Ise Shrine Travel Guide (p.13)

The chapter opens its gallery with a Japanese visitor's guide to the Ise Shrine (published Ise, Japan, between Oct 1948 and April 1954). It is a **hybrid**: a bird's-eye perspective view renders the local area around the shrine in rich, recognizable detail; then, on the right margin, the design shifts abruptly to a very flat schematic map of the national railroad linking the shrine to major cities.

**Why it is the chapter's keystone example:** the seam between the two halves makes the cost of flatland visible. The friendly perspective gives way to "hard flatland," and you can *see* the visual dimension that gets sacrificed when scale jumps from local to national. The change of design accommodates the change of scale — local detail set inside national context, a mixed landscape of refuge and overview. A bonus: the horizontal layout cooperates with the vertical orientation of Japanese text, so the stand-up labels point precisely at their locations.

**Lesson:** when you must compress, do it deliberately and show the seam. Mixing a high-dimension local view with a low-dimension overview can be honest design — as long as you let the reader feel what was given up, rather than pretending nothing was lost.

---

## §4. The Spectrum of Escapes — Direct vs. Encoded

Five hundred years of practice (examples from 17 countries, 7 centuries, "3 planets and 1 star") fall on a spectrum from literal 3D simulation to pure symbolic encoding.

| Escape | Example in the chapter | What it spends, what it buys |
|---|---|---|
| Physical model | Euclid's *Elements*, 1570 ed. — paper fold-up solids to teach geometry | Buys intuition for smooth shapes; useless for "obstreperous" data point clouds |
| Conventional perspective | Perfected by Florentine architects, 15th c. | Reads instantly for physical objects; cannot show abstract multivariate data |
| Stereo pairs | Aerial stereopair of Bonaduz, Switzerland (1975) | Vivid depth via two fused images; many viewers fail to fuse them |
| Rotating point clouds / dodecahedron projection | MACSPIN-style statistical graphics | Self-consciously multivariate; navigation in 3D scatterplots is not trivial |
| Mechanical simulation | Orreries, 1800 | Triumph of gear ratios — but a **failure mode** (see §10): apparatus over content |
| Symbolic encoding | Java timetable, dance notation, sunspot charts | Carries the most variables per surface; demands the reader learn the code |

**Rule:** the more abstract the data, the further right on this spectrum you must move — literal depiction runs out, and you must encode. The orrery is the cautionary midpoint: physical fidelity that drowns the very motion it was built to show.

**The documented escape — the periodic table (pp. 14–15).** Tufte's named case of a well-worked compression problem is the periodic table of the elements: several hundred arrangements have been proposed in the attempt to capture its complexities, including triangular layouts, a spiral, and looping-orbit forms (Zmaczynski, Mazurs). One dataset supporting radically different escapes is the chapter's evidence that dimensional compression admits many defensible answers — and its anchor example of abstract multivariate data predating statistical graphics.

**The dodecahedron's six faces (p. 15).** The Tukey display slices the data and projects it onto six of the twelve faces of a pentagonal dodecahedron — six suffice because opposite faces are parallel and would show identical views. A worked lesson in spending exactly as many panels as the geometry requires, no more.

**The fourth dimension — sections, shadows, projections (VE p. 86).** Bragdon and Banchoff extend the toolkit upward: a plane slicing a 3-D object yields changing 2-D cross-sections, and by analogy, sequences of 3-D slices could reveal 4-D objects. Sections, shadows, and projections form the general dimension-lowering toolkit — small multiples of slices as the flatland answer to higher-dimensional structure.

---

## §5. The Sunspot Lineage — Visual Reasoning to Micro/Macro (pp.18–23)

The chapter traces one dataset across ~380 years to show the same methods reappearing whenever someone faces a flood of data.

**Galileo's projection method (1610–1612):** project the sun's image onto a sheet a foot from the lens, draw a circle to fit, then mark each spot at correct scale and position. This converts a glare-blinding observation into a stable mark on paper flatland.

**Galileo's visual reasoning (1613):** through a chain of drawings he converts what "the eye of the forehead" merely registers into what "the eye of the mind" understands — turning raw spot positions into proof that the spots sit on a rotating spherical sun. It was more than 150 years before anyone materially improved his result. That longevity had two causes (p. 19 n. 11): insight, and the fact that almost no sunspots were observable from 1645 until 1715 — the Maunder Minimum. Data scarcity can freeze a finding's authority.

**Scheiner's small multiples (1613 and 1626–1630):** the daily diagrams indexed on time come from Scheiner's *De Maculis Solaribus* (Rome, 1613, published under the pseudonym "Apelles"), with one further plate from *Rosa Ursina*; the apparent-path diagrams tracking spot structure across a stationary disk are the contribution of his later *Rosa Ursina* (completed 1630) — "a design simultaneously enhancing dimensionality and information density." But Scheiner filled the blank, spotless regions with his patron's and religious order's emblems (a failure mode, §10).

**Maunder's butterfly diagram (1904):** decades of daily mapping (the chart spans 1877–1902, ±40° latitude). The sunspot's **two areal dimensions are reduced to one content-relevant dimension** — latitude in degrees — freeing the surface for time. Individual marks are the micro; the aggregate butterfly shape is the macro, showing the ~11-year cycle and the drift of spots toward the equator.

**The micro/macro payoff and variation:** fine detail merges into a repeated typical pattern, and the foremost result is a *visual measure of variation around the average* — both fundamental summary measures of a statistical dataset shown at once.

> "Measured assessments of variability are at the heart of quantitative reasoning." — Tufte, *Envisioning Information*

R.A. Fisher, founder of modern statistics, wrote in 1925 that earlier workers treated variation as a nuisance detracting from the average, whereas the modern aim is to study the *causes* of variation itself. A good micro/macro display honors Fisher: it never reduces data to the mean alone.

**The modern butterfly (Hathaway/NASA):** density up **tenfold**, a full century, nine cycles. The sine of latitude places each mark; **color encodes the log of area covered (lighter = larger)** — converting a spatial dimension into a color dimension; a lower time-series, summing all latitudes, restores total percent of the sun's surface covered. Parallel sequencing of the two panels enhances both dimensionality and density.

**Symmetry as reclaimable surface (p. 23 n. 15):** because sunspots are symmetric about the solar equator, the butterfly's wings may be folded over (Gleissberg & Damboldt), halving the display when the north/south distinction carries no information — exploit a symmetry in the data to reclaim surface.

---

## §6. The Layering Exemplar — The Java Railroad Timetable (pp.24–26)

A 1937 graphical timetable for the Soerabaja–Djokjakarta line (annotated in Dutch then Japanese) carries **16 variables** on one 24-hour sheet by smoothly suppressing a dimension here and there and finessing perspective entirely.

| Encoded element | Variable(s) it carries |
|---|---|
| Horizontal axis | Time of day (read across top) |
| Vertical axis | Station, spaced in proportion to distance along the track (not alphabetically) |
| Diagonal direction | Train direction — upper-left→lower-right = "down"; lower-left→upper-right = return; an X where opposite trains pass |
| Diagonal slope | Relative speed (steeper = faster) |
| Diagonal line style (8×4 matrix) | 8 train types (super express / express / passenger / mixed / special / cargo / preferential / night cargo) × 4 seasonal patterns (regular / seasonal / irregular / special) |
| Left-margin profile | Elevation at enlarged vertical scale, with grade and path columns alongside |
| Per-station aerial insets + dingbats | Local facilities: cargo platform, livestock loading, water pump tower, directional-change platform, car repair, standby engines, relief car, closed areas |

**The multiple-functioning diagonal:** one mark records **six variables at once** — a train's location between towns, the time of that position, direction, train type, relative speed (by comparing slopes), and yearly pattern. One mark doing six jobs beats six separate marks. (Tufte sources the "double-functioning element" idea from architectural criticism — Venturi, citing Wylie Sypher.)

**The spy story (load-bearing detail):** this 16-variable sheet was an internal planning document, obtained by agents preparing Japan's 1942 invasion of Java, and is marked "secret" in the corner. A display this dense reads as both micro (one train) and macro (the whole system's structure): "It is very much like an excellent map, but with many dimensions breaking free of direct analogy to conventional cartographic flatland." (EI p. 26)

**Layering rules:**

| Do | Don't |
|---|---|
| Give each layer a distinct encoding (orientation, weight, symbol, color) | Let two layers share one visual channel and collide |
| Share an axis only when variables are orthogonal (distance + elapsed time on one vertical) | Force unrelated variables onto the same axis |
| Make a mark earn its place by doing two jobs | Add a separate mark for every variable |

---

## §7. The Narrative Exemplars — Dance and Weather (pp.27–28)

**Tomlinson's dance notation (1735):** four dimensions on one page — the flatland of the ballroom floor, coded gestures of body motion, and time sequence. The floor plan links to the music (itself two dimensions plus time and tone) by **numbers that double-function**: they sequence the steps *and* tie each step to a musical measure. Movement is symbol-encoded rather than verbal because a serious notation avoids words, which are a barrier to international use. Mirrored partners are drawn in full (redundant bilateral symmetry usually wastes space) because their weaving, intermingling paths require the symmetric repetition to read.

**Japanese newspaper weather cross-section (1985):** instead of the usual plan-view of latitude and longitude, the map shows Japan as a **vertical side profile, an ocean-eye view**, with gray contours tracing 0°C and -10°C through the clouds and forecast symbols for 15 areas. By spending one dimension on elevation rather than a second horizontal axis, it reads far more easily than a conventional weather map. Caveat: the trick works best for long, thin countries.

**Narrative rule:** match each dimension's encoding to its nature — time → sequential position, direction → orientation, speed → slope — and cherish every chance to spread an extra variable over a dimension you already have on the page.

---

## §8. The Small-Multiple Exemplars and Data Density (pp.28–33)

Small multiples "move to the heart of visual reasoning — to see, distinguish, choose." Their multiplied smallness forces comparisons within a single **eyespan**, so the active eye does the work rather than memory bridging images scattered across pages.

**California air pollution (computer-plotted):** 3 pollutants (nitrogen oxides, carbon monoxide, reactive hydrocarbons) × 4 times of day (midnight–3am, 6–9am, noon–3pm, 3–6pm) = **12 surface maps** of southern California, each over a grid of **2,400 squares at 5 km/side = 28,800 readings** (except peaks masked by mountains). Five variables: two-space location + time-of-day + pollutant type. **Economy of perception:** decode the design once, then read every panel for free; a steady canvas makes the data changes pop.

**Compound interest tables (Barème Universel, 1822):** tabular small multiples — a 2D array of capital × time, repeated at successive interest rates. The same pattern as the pollution maps, in pure numbers: a third variable on the two-surface, then the whole grid repeated at levels of a fourth.

**T-shirt color grid:** children's shirts arranged by body color × collar color — a **bivariate small multiple where color itself is the data**, the eye surveying a 2D color space directly.

**Data density (the second goal, with benchmarks):**

| Display | Volume | Composition |
|---|---|---|
| Maunder butterfly (1904) | daily, 1877–1902 | each mark = one observation; two areal dims → latitude |
| Modern butterfly | 10× the 1904 density | full century, nine cycles, color = log area |
| California pollution | 28,800 readings | 2,400 squares × 12 maps |
| Compound interest | full grid × rates | capital × time, repeated per interest rate |
| Tokyo weather history | 414 data pieces | town × year × month × day × day/night + summary rows |
| Tokyo weather almanac | 1,826 days | decade by town × year × month × day; year-by-day matrix compounded by month |
| Java timetable | 16 variables | single sheet |

**Density threshold:** high-information graphics convey "a spirit of quantitative depth and statistical integrity"; emaciated, data-thin designs provoke suspicion — rightfully — about the quality of the underlying measurement and analysis. The Tokyo almanac is the master move: it apportions *both* of the paper's dimensions to one variable (time), splitting it fine-to-coarse (day within month within year) to stretch a compact display across 1,826 days.

> Implicit formula: **data density = (number of data entries) / (area of display).** Maximize it only as far as legibility holds; small multiples buy density cheaply because the design is decoded once.

---

## §9. Multivariate Tables — LSAT Grid and the Gotti Courtroom Chart (pp.29–31)

Numbers on a plane can multiply too; two table examples close the gallery.

**The LSAT bivariate grid (NYU School of Law, 1983–84):** GPA (rows) × LSAT percentile (columns) knits together every combination of grades and test scores. Each cell holds **two numbers** — applicants *and*, of those, the number actually admitted (e.g. "7-0"). The right and bottom margins sum to univariate distributions, with grand totals at lower right. The table could itself become a single cell in a higher table comparing many schools — multivariate nesting.

**The Gotti chart — "Criminal Activity of Government Informants" (United States v. Gotti, 1987):** a courtroom exhibit, supplied by the defense, listing 69 crimes (murder, drugs, kidnapping, down to "pistol whipping a priest") committed by 7 prosecution witnesses. It is built to be read **both horizontally and vertically**: across a row you see how widely one crime spreads among witnesses; down a column you see one witness's full record, and the eye catches unbroken runs of X's (one witness "has something of a streak going"). Only **37% of all possible cells are marked**, yet the marked ones dominate. Placement is rhetorical — the most obnoxious crimes sit at the top (murder) and bottom (pistol-whipping a priest), exploiting the visual prominence of those edge positions.

**Why tables win in a trial:** speech is linear, one-dimensional, non-reversible "talk talk talk"; a visual table is simultaneously a **wideband** and a **perceiver-controllable** channel, letting each juror read, re-edit, and reason at their own pace and in their own order.

**The restraint bound (p. 35 n. 23):** trial lawyer Joe Jamail, quoted by Tufte alongside the Gotti analysis, warns that too many pictures turn the courtroom into a circus — "jurors will think you think they're stupid." The Gotti chart worked as *the one* exhibit the jury recalled: visual evidence persuades in a talk-talk-talk setting precisely when it is scarce and dense, not decorative and plural.

---

## §10. The Failure Mode — Chartjunk and the Duck (pp.33–35)

The opposite of escaping flatland is *decorating* it. The good methods are **self-effacing**: when they work, only the data is visible and the container disappears. Chartjunk inverts this — the apparatus attracts attention to itself.

**The "duck" (from Venturi's *Learning from Las Vegas*):** when Modern architects abandoned applied ornament, they distorted the whole building *into* ornament — the container became the message. Pugin's warning applies to data: it is fine to decorate construction, never to construct decoration. A 3D bar chart whose third axis carries no variable is a duck; the "diamonds" chart with a fishnet-stocking thigh-graph is a duck that also confuses changes in money's value with changes in diamond prices during high inflation.

**Named failure modes:**

| Failure mode | Description | Example in the chapter |
|---|---|---|
| Pridefully Obvious Presentation | Display apparatus overwhelms the data content | Orreries directing the eye to gears, not planetary motion |
| Embellishment-for-data | Ornament fills space that should hold data | Scheiner's patron/religious emblems in the blank, spotless disk regions |
| The Duck | The container becomes the message; content-empty third dimension | Diamonds fishnet-thigh chart; any 3D shell with no third variable |
| Data posterization | Closely-read data styled like a poster (strong image, big type, thin data) | Chartjunk "performances" that read like posters, not maps |
| Contempt for the audience | Assumes readers are bored and stupid; adds ornament to "enliven" | "Lively" infographics with icons replacing data marks |
| False escape / pretend dimensions | Fake dimensions added to an impoverished dataset | The royal dining table so caught in flatland it cannot hold the pots |

Jonathan Swift's 17th-century cartographers, who filled unknown territory with pictures of elephants for want of real towns, are Tufte's image for substituting embellishment where data should be.

**Period nuance on Scheiner's emblems (p. 21):** the patron and religious-order emblems are similar to a modern trademark or logotype and may have served as a seal of validation for readers of 1630; only today do they read as strident, contradicting nature's rich pattern. Ornament-in-blank-space can be a credentialing convention of its era — still wrong, but not mere vanity.

**The moral premise — respect for the audience.** Chartjunk rests on the assumption that numbers and details are boring and need ornament to enliven them. Tufte's answer inverts the diagnosis: if the numbers are boring, then you have got the wrong numbers (EI p. 34) — the remedy is better data, never cosmetic decoration, which frequently distorts the data and never salvages an underlying lack of content. Consumers of graphics are usually smarter about the subject than the people decorating it. Standards of excellence are set by high-quality maps — bountiful detail, layered close reading, rigorous survey data — not by posters meant for viewing at a distance.

> "Readers of a report should be unaware of its design." — Paul Rand, quoted in Tufte, *Envisioning Information*

(Reinforced by E.B. White: no one writes decently who distrusts the reader's intelligence. Clarity and simplicity are the opposite of simple-mindedness — they are the highest respect for an alert, busy, caring reader.)

---

## §11. Historical Lineage

| Date | Development | Escape technique |
|---|---|---|
| 15th c. Italy | Florentine architects perfect perspective | Conventional 3D projection on a 2D surface |
| 1570 | Euclid's *Elements*, Billingsley ed. | Paper fold-up models for solid geometry |
| 1610–1612 | Galileo's sunspot observations | Projection: marking spots onto paper at true scale/position |
| 1613 | Galileo's *Istoria e Dimostrazioni* | Visual reasoning: data → mechanism |
| 1613 | Scheiner's *De Maculis Solaribus* (as "Apelles") | Daily time-indexed small multiples of sunspots |
| 1626–1630 | Scheiner's *Rosa Ursina* | Apparent-path diagrams across a stationary disk |
| 1735 | Tomlinson's dance notation | Floor-plan + coded gesture + time, with double-functioning numbers |
| 1800 | Orreries | Mechanical 3D simulation — but Pridefully Obvious Presentation |
| 1822 | Barème Universel interest tables | Tabular small multiples (capital × time × rate) |
| 1904 | Maunder's butterfly diagram | Micro/macro; areal dims reduced to latitude |
| 1937 | Java railroad timetable | 16-variable layering; multiple-functioning diagonals |
| 1948–54 | Ise Shrine travel guide | Hybrid perspective + flat map; the cost of flatland made visible |
| 1980s | California air pollution maps | Computer small multiples, 3 pollutants × 4 times |
| 1984–85 | Tokyo weather almanac | 1,826-day matrix, both paper dimensions spent on time |
| 1985 | Japan weather cross-section | Space-time narrative as a vertical side profile |
| 1987 | LSAT grid; Gotti courtroom chart | Bivariate tables read both directions |

---

## §12. Do/Don't Summary

| Principle | Do | Don't |
|---|---|---|
| Goals first | Name the two goals: more dimensions AND more density | Optimize one while ignoring the other |
| Taxonomy | Use the five methods; treat density as a goal | List "six strategies" with density as a peer method |
| Compression | Compress deliberately and show the seam (Ise Shrine) | Pretend nothing was lost when scale jumps |
| Variation | Show average AND variation (Fisher, Maunder) | Reduce the data to its mean |
| Multiple-functioning marks | Let one mark do several jobs (Java diagonal = 6) | Add a separate mark per variable |
| Tables | Build grids readable both ways (Gotti, LSAT) | Settle for a one-direction list |
| Density | Push density to the legibility limit | Ship emaciated, data-thin displays |
| Self-effacement | Make the container vanish, the data show | Build a duck — container as message |
| Audience | Assume an alert, caring, busy reader | "Enliven" numbers with ornament |

---

## §13. Application Checklist

Before shipping any chart, map, table, or display:

- [ ] State the two goals for this display: which variables/dimensions, what target density?
- [ ] Pick which of the five methods apply, and open the matching sibling skill for mechanics.
- [ ] How many variables does the data have vs. how many does the display encode?
- [ ] Is every mark doing at least one job? Can any mark do two (a multiple-functioning element)?
- [ ] Does it pass micro/macro: legible detail AND legible overall pattern? Does it show variation, not just the mean?
- [ ] If compressing or mixing scales, is the seam honest (Ise Shrine) rather than hidden?
- [ ] If tabular, can it be read both horizontally and vertically? Do margins carry the univariate sums?
- [ ] Is density above the suspicion threshold for the subject's complexity, while still legible?
- [ ] Any third dimension, ornament, or color encoding no variable? Remove it (no ducks).
- [ ] Does the container (axes, grid, border, legend) out-area the data? Shrink the container.
- [ ] Would a reader who knows the encoding decode any panel without re-reading the instructions?

Source: *Envisioning Information* (Edward Tufte, Graphics Press, 1990), ch. 1 "Escaping Flatland," pp. 12–35 (the chapter thesis and two goals appear on pp.12–13; the five methods are previewed p.33).

Cross-book notes: *Visual Explanations* restates the framing as a question — how to depict a world of three or more dimensions on the two-dimensional flatlands of paper (VE p. 141). *Beautiful Evidence* sharpens it into an epistemic warning: the only two-dimensional thing about evidence is the physical flatland of paper and screen, and flatlandy display technologies encourage flatlandy thinking (BE p. 130). BE p. 30 names the matching inference error — taking a single one-eyed photograph of a three-dimensional object and reporting the result as a fact about the object itself. One projection is one projection; the flattening is a choice that has to be declared.

*Seeing With Fresh Eyes* adds a sixth escape the chapter's spectrum (§4) does not cover — **multiple viewpoints combined into one surface**, rather than one viewpoint rendered better. Its cases: the Big Dipper as the limit case of the problem, a 2-D figure-ground pattern standing in for stars at wildly different distances (p. 8); Cézanne building a canvas from several local grids instead of one global perspective (p. 28); Hockney's collages assembling ~750 photographs into a single scene (p. 32); and a gecko-embryo image composited from **12,000** confocal frames (p. 40). Tufte's grounding argument: a living eye already registers thousands of viewpoints an hour, so a display built from many viewpoints is closer to perception than the single fixed station-point perspective inherited from the 15th century.

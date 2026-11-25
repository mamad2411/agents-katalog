---
name: tufte-typography-for-data
description: "Use when setting type that carries data — chart labels, axis titles, table headers, legends, captions, schedules, maps, dashboards, or numeric columns; when a legend, key, or letter-coded caption is being added; when linebreaks, alignment, or column width are being decided by a grid or style sheet rather than by content; when choosing a typeface or weight for small or dense text; or when a display's aspect ratio is being set by a default."
tags: [tufte, data-visualization, typography, annotation, information-design, labeling, content-responsive]
---
# Typography for Data Display

## Overview

Typography in an analytical display has one job: serve the content, never the production process. Tufte's governing distinction (*Seeing With Fresh Eyes*, Chapter 2, printed pp. 49–63) is between **content-responsive** typography — where space, linebreaks, and label placement are driven by the data and its structure — and **content-indifferent** or **content-hostile** typography, where generic grids, squared-off margins, and legend boxes subordinate meaning to convenience of layout.

The standard is borrowed from typographer Robert Bringhurst, and it appears in **Chapter 1, p. 19**, as the epigraph over the Cleveland Clinic thought-bubble spread — not in Chapter 2:

> "Typography exists to honor content." — Robert Bringhurst, *The Elements of Typographic Style* (1992), p. 17, quoted in Tufte, *Seeing With Fresh Eyes*, p. 19

**Two distinct claims that are routinely fused — keep them apart:**

| Claim | Figure | Page | What it is about |
|---|---|---|---|
| Printed text has used grids indifferent or hostile to meaning | **1500 years** | p. 17 | **Control** — publishers, text-grids, and style-sheets own the space |
| Space was costly, so words ran edge to edge | **thousands of years** | p. 53 | **Cost** — and on screens the marginal cost of space is now zero |

The 1,500-year figure belongs to the control argument (the Great Disjunction), not to the cost of paper.

> Companion skills: `tufte-visual-thinking` (the model-criticism frame this sits inside), `tufte-annotation-as-thinking` (Ch. 5), `tufte-data-maps` (Swiss topo maps in full), `tufte-parallelism`.

---

## §1. Four Modes, Not Two

Tufte's scale runs further in both directions than a responsive/hostile pair suggests. **Content-possessed** typography (p. 51) is the far end, and it is a legitimate category, not an error.

| Mode | Mechanism | Effect | Source |
|---|---|---|---|
| Content-indifferent | Wordspaces stretched to square off the right margin | Syntactic structure lost; word salad | p. 17 |
| Content-hostile | Linebreaks chop phrases mid-clause to fill a column | Meaning actively suppressed | p. 17 |
| Content-responsive | Linebreaks follow commas, semicolons, full stops; spacing exposes parallel structure | Meaning amplified; syntactic units visible | pp. 17, 52 |
| **Content-possessed** | The typographic form *becomes* the thing described | Apollinaire's calligramme sets "Il pleut" as five slanting vertical columns of single letters, so the text physically rains | p. 51 |

**Boundary for data work:** possession is legitimate when the form *is* the datum — rain, terrain, stroke order, a descent, a rise. It is decoration the moment the form asserts something the data does not. (Related: the 2-D typography of Barr's cubism chart and Apollinaire's *Calligrammes* permits multiple simultaneous reading paths — BE p. 66; see `tufte-narrative-and-sequence`.)

---

## §2. Linebreaks That Honor Syntax

Words and sentences interact with the spaces and the other words around them. Text can survive content-indifferent spacing, but survival is not the goal.

**Do / Don't — linebreaks in a list sentence:**

| Practice | Verdict | Why |
|---|---|---|
| Cram a 6-item list into one justified paragraph | Content-hostile | Punctuation alone must carry the structure; reader cannot scan or compare items |
| Break each list element onto its own line | Content-responsive | The structure already in the prose becomes visible; items align for up/down comparison |

**The Ioannidis example (pp. 49 and 52; previewed p. 17).** John Ioannidis's claim that most published research findings are false is stated as a six-condition list: smaller studies; smaller effect sizes; a greater number and lesser preselection of tested relationships; greater flexibility in designs, definitions, outcomes, and analytical modes; greater financial and other interest and prejudice; more teams chasing statistical significance. Set as one justified block, **five semicolons** carry all six elements and readers cannot pull them apart. Give each condition its own line and the list becomes scannable — nothing added, only the existing punctuation honored.

**The Somerset Maugham example (pp. 48 and 52).** A passage from "The Book Bag" catalogues book types across roughly fourteen clauses. Run together, the categories vanish; broken at the existing commas, semicolons, and stops, the parallel syntax (illness, travel, expedition) becomes visible. The punctuation already marks where the breaks belong.

> Chapter geography: Chapter 2 **opens on p. 49**. The Maugham prelude spread sits on the facing p. 48, before the chapter opener. The KMP code (p. 14) and the poetry-line critics (p. 15) are **Chapter 1** material, not Chapter 2.

---

## §3. The Darwin Calculation — Scale of the Problem (p. 50)

| Quantity | Value |
|---|---|
| Chapters | 14 |
| Topics announced in the Table of Contents | 133 |
| Times each topic is printed (TOC + chapter head) | 2 |
| Total words of topic lists | 1,962 |
| Cost to re-set them content-responsively | +2 to 3 pages in a 500-page book |
| Readers since 1859 | ~3 million serious + millions of skimmers |
| Cumulative reader-impediments imposed | **~2,000,000,000 to 5,000,000,000** |

A content-hostile linebreak is never neutral — at scale it is either imposing friction or removing it.

> Internal inconsistency in the book, worth knowing: the p. 50 headline says content-responsive typography eliminates **trillions (10¹²)** of impediments, while the body text on the same page computes **2–5 billion**. The body figure is the one derived from the arithmetic and the one used above.

Every number in this table is Tufte's own research; keep the p. 50 citation attached wherever they travel.

---

## §4. Zero-Cost Space and Alignment as Signal (p. 53)

For millennia, space on clay, papyrus, vellum, and paper was costly, so words ran edge to edge. On a display screen the marginal cost of an additional space is zero. Continuing to impose content-indifferent grids on screens honors a constraint that no longer exists.

| Alignment mode | Signal value | Best use |
|---|---|---|
| Justified (both margins squared) | None — wordspaces stretched to fill | Dense reference text; truly cost-constrained media |
| Ragged-right (flush left) | Linebreak position can signal meaning | General analytical prose |
| Central-axis (centered) | Both margins active; readers and speakers do not have to hunt for the left margin, and are less likely to skip a line, because the next line's full length and pace are visible in advance | Poetry, announcements, data briefings |
| Ragged-left (flush right) | Left space identifies the speaker | Dialogue in novels and scripts, transcripts |

---

## §5. Authors Control the Breaks — Poetry, Code, and the Math Style Sheet

**Poetry as the model (p. 15).** Critics treat the *line* — not meter or rhyme — as the feature that makes poetry read as poetry; the line is the most sensitive register of breath and pacing and carries meaning vertically as well as horizontally. Where a line breaks is information, not decoration.

**Code as the model (p. 14).** A clean Knuth–Morris–Pratt string-matching implementation is roughly **37 lines and about three-quarters empty space**. For the reader those spaces create fluency; for the machine they mean nothing and are discarded at compile time. Minify it and the program runs identically and becomes unreadable. Whitespace in an analytical display is for the human, not the medium.

**The math style sheet (p. 17) — the strongest external authority in the book.** A formula too long for the page width must be broken across lines, and the rules are precise:

1. Break at the end of a **natural phrase**.
2. In a heavily bracketed formula, break at the end of a **major bracket**, never at an inner symbol.
3. The rationale is explicitly musical: natural phrasing, as in music or speech, is what makes the break intelligible between writer and reader.
4. **The decision must not be left to the compositor.** The author, who knows the content, indicates the point of fracture in advance.

**Direct transfer to data work:** long axis titles, wrapped table headers, multi-line chart labels, and tooltip copy should all carry author-specified break points, not renderer-chosen ones. If your charting library wraps by width alone, you have handed the compositor the decision.

---

## §6. Regulating Reading Speed (p. 57)

Typography controls not only clarity but *pace*.

- **Minify hyphens; never minify dashes.** A hyphen carries little meaning and should be reduced where possible: `e-mail` → `email`. A dash must survive, because a dash's pause can be as strong as a poetic line break. Tufte demonstrates by re-setting a Kingsley Amis sentence so each dash-bounded clause lands on its own line.
- **The suspended sentence.** Amis on Elmore Leonard: the present participle suspends the English sentence, opening a lag in time the reader slides through. The typographic corollary (p. 67) is explicit — spacing should maximize explanatory depth, not speed-reading; a graphical sentence there uses 11 line breaks, 3 stacklists, and 40 content-spaced words.

**Use for data display:** deliberate spacing is a legitimate way to force a slower, comparing read of a dense claim. Speed is not the objective function.

---

## §7. Idiosyncratic Paragraphs and Memory Retrieval (p. 59)

Text-only paragraphs are typographically identical — same face, same leading, same measure, stacked into columns. Tufte's mechanism for why that fails is specific and worth stating precisely: **idiosyncratic paragraphs aid memory and retrieval by uniquely activating the relevant neural substrates for retaining visual memories.** The reader's failure is equally precise: being unable to find and re-read a specific string of words in a paragraph they have already read.

Tufte deliberately gave nearly every paragraph in the book a unique appearance for exactly this reason.

**Do / Don't — paragraph variety:**

| Practice | Verdict | Why |
|---|---|---|
| All body paragraphs same face, leading, measure | Content-hostile | No visual anchors; the reader cannot re-find a passage |
| Tables formatted identically to block prose | Content-hostile | Evidence types become visually indistinguishable |
| Tables, code, callouts, quotations in distinct treatments | Content-responsive | Each evidence type leaves a distinct visual memory |
| Deliberate spacing between conceptual groups | Content-responsive | Grouping is visible; transitions are marked |

**Mode-switching mid-sentence, and stacklists inside prose (p. 59).** The unit of typographic variation is the **paragraph**, and variation can happen without breaking the surrounding text:

- Galileo changed information mode mid-sentence in his 1612 manuscript on Saturn's rings, drawing the observed shapes inline; his publisher then integrated text and images in print.
- A *Lucky Jim* passage is re-set so three parallel interrogatives lift out of the justified block into a centered three-line stacklist, leaving the prose around them intact.

---

## §8. The White Interval — Grounding Outside Western Typography (p. 54)

- **György Kepes:** Chinese and Japanese painters leave large paths of the picture surface empty and divide it at unequal intervals, which forces eye movements of varying velocity and unifies the surface through maximum variation.
- Characters are written inside imaginary squares, with the blank areas given as much design attention as the strokes.
- **Tufte's paired example:** an 1808 Hokuba woodblock in which calligraphy drifts through the perspective space above the bowls, so the receding planes accent the drifting text.

**Transfer:** unequal intervals do more work than equal ones. A dashboard on a uniform 8pt rhythm reads as one undifferentiated field; varying the interval by conceptual grouping does the separation that borders would otherwise be asked to do.

---

## §9. LittleDataGraphics and Data Paragraphs (pp. 60–61)

**The LittleDataGraphics critique (p. 60).** Tufte's term names the family of displays — pie charts, small bar charts — that encode a tiny data set into areas, angles, and colors, forcing the viewer to mentally reverse the encoding. The code is local to that one graphic and repays no learning.

| Display type | Encoding | Decoding required | Verdict |
|---|---|---|---|
| Pie chart | Data → area / angle | Mental reconversion to proportion | Content-hostile: one-off local code, zero transfer value |
| Bar chart (small n) | Data → height | Mental reconversion to magnitude | Content-hostile: one-off local code, zero transfer value |
| Data table | Data → number | None — the number is the data | Content-responsive |
| Data paragraph | Data → words + numbers + small image | None — the prose is the data | Content-responsive |

> "Data visualizations are at their best when there is so much data that the only way to see it . . . is to see it." — Tufte, *Seeing With Fresh Eyes*, p. 60

**Three worked data paragraphs — keep them distinct:**

| Example | Contents | p. |
|---|---|---|
| **NWS KSFO point briefing** | **18 measurements** (US and metric), **28 words**, **4 links**; serves the casual reader via a sunny/cloudy icon and the analyst via the 5th significant digit of barometric pressure, with linked 3-day history and hourly forecast | 60 |
| **Egyptian vulture** | One paragraph combining five information sources spanning **4,000 years** — an ancient line-and-tone illustration, three sentences of drawing instructions, **six stop-action stroke-order sketches**, and an Egyptian-vs-modern comparison | 60 |
| **Baseball scoring summary** | **13 sentences and 44 numbers**, one per line, each naming who did what, with the running score accumulating at the far right to the final result | 61 |

**The baseball paragraph's typographic trick, worth stealing:** one team is set in **sans-serif** and the other in **serif**, so team identity is carried by the typeface and never needs a repeated label. A typeface can encode an entire categorical variable without a legend. (See `tufte-redundant-encoding`.)

**General rule:** calibrating a display to the least-informed viewer throws away most of its value. A good display makes every audience smarter from the same ink.

---

## §10. Direct Labels vs. Legends — and What the Swiss Maps Actually Show (pp. 62–63)

A legend is a one-time local code the reader must memorize before the chart means anything. Direct labels put the name at the data, in the data's own color, and abolish the round trip.

**The legend indictment (p. 63)** is aimed at data-analysis software, not at cartography. On the content-hostile side of Tufte's side-by-side comparison of a machine-learning results chart, five series (bagging, random forest, single tree, lasso, lasso-with-interaction) are named in a disordered legend that **consumes more than 40% of the display's space**, in black rather than in each data-line's color, with the legend order different from the top-to-bottom order of the lines themselves.

> "For 50 years, office and data-analysis software have published trillions of legends — coffins of dead conventions — and trillions of impediments to seeing and learning." — Tufte, *Seeing With Fresh Eyes*, p. 63

On the content-responsive side the labels sit at the lines, in the lines' colors, with the more significant series enlarged, and all the freed space shows data.

### Correction: Swiss topographic maps DO use legends (p. 62)

The Swiss maps are the model for **direct labeling**, not for legend abolition. Tufte's own text on p. 62 states that maps also use legends, and that Swiss topographic map legends are **consistent across all Swiss topographic maps** — showing measures of altitude, natural colors for surfaces, and place-names scaled to population size. The p. 62 spread reproduces exactly such a legend: trigonometric points, spot height, index contour, lake level, spot height of lake bottom, plus rock-scree and glacier-moraine rendering shown separately at 1:25 000 and 1:50 000.

**The virtue Tufte names for direct labels on those maps is exactitude without clutter** — the place name sits at the coordinate it names. Legend abolition is a claim about the p. 63 software chart, not about cartography.

| | Swiss topo map (p. 62) | Software chart, content-hostile (p. 63) |
|---|---|---|
| Series/feature names | Directly at their coordinates | In a legend box |
| Legend present? | **Yes** — and consistent across every map in the series | Yes — and unique to this one chart |
| What the legend carries | Symbol vocabulary reused across thousands of maps: altitude measures, surface colors, scaling conventions | A one-time color code for five lines |
| Learning value | High — learn it once, use it for life | Zero — discarded after this chart |
| Space cost | Small strip at the margin | >40% of the display |

**The population-scaled name table (reproduced by Tufte from swisstopo, SWFE p. 62 — 8 rows):**

| Category | Population | Type treatment |
|---|---|---|
| Town | over 50 000 | BERN (largest roman caps) |
| Town | 10 000 – 50 000 | LUGANO |
| Municipality | 2000 – 10 000 | Sumvitg |
| Municipality | less than 2000 | Cressier |
| Suburb | over 2000 | *Cassarate* (italic) |
| Suburb | 100 – 2000 | *Champfèr* (italic) |
| Hamlet, group of houses | 50 – 100 | *Le Plan* (italic) |
| Single house, hut | — | *Tritthütte SAC* (smallest italic) |

*(Swiss map material is reproduced in SWFE with permission of swisstopo, BA200098. Cite it to swisstopo via SWFE p. 62 rather than as Tufte's own table.)*

The type is doing two jobs at once: it names the place **and** encodes its population class through size and roman/italic contrast — a data dimension carried by typography, with the legend confirming the convention rather than replacing the labels.

**A working case on the same page (p. 63):** the FT's cumulative-deaths-by-days-since-10th-death chart (John Burn-Murdoch) labels every country at its line, in the line's color, and adds content-driven annotations directly in the plot field — lockdown dates, why Italy's elderly population raises its death rate, how South Korea's early large-scale testing and tracing worked, a 33%-daily-increase reference slope.

**Placement priority for direct labels:**
1. At the line's terminus (rightmost point for a time series).
2. Adjacent to the most characteristic feature of the series.
3. Leader line from the nearest uncrowded whitespace to the datum, only when crowded.
4. Never a disconnected legend box when direct placement is possible.

**The New Haven timetable (EI, pp. 104–107) — verified against the source:** the standard railroad table devotes only **21%** of its area to the times trains actually run. The top is consumed by grids laboring to make three binary distinctions (New York/New Haven, leaving/arriving, weekday/weekend); the 80 arrival and departure times (~410 characters) are crammed into the leftover space; a small table carries **41 inches (104 cm) of rules**; column headings repeat three times with 24 AM/PM markers, forcing a serpentine eye path. The redesign sets the times in Matthew Carter's Bell Centennial and replaces the active colon between hours and minutes with a visually quieter dot.

---

## §11. Banking to ~45° — Who Owns the Aspect Ratio (p. 63)

On the content-responsive side of the same spread, Tufte adjusts the redesigned chart's aspect ratio so that **local slopes average roughly 45°**.

The rhetorical point is authority, not geometry: **why should a publisher's style sheet or a coder's default decide the aspect ratio, forcing every data graphic into the same pre-specified box?** Aspect ratio is a content decision, and it currently belongs to whoever wrote the plotting library's defaults.

Cited by Tufte to Jeffrey Heer & Maneesh Agrawala, "Multi-Scale Banking to 45°," *IEEE Transactions on Visualization and Computer Graphics*, 2006, 701–708. (Procedure and worked ratios: `tufte-sparklines` §7.)

---

## §12. Letter-Coded Captions and Annotations on Annotations (p. 55)

**Letter-coded captions are content-hostile — the purest do/don't pair in the chapter.** A surgical illustration captioned "A:" and "B:" below the images forces the same decode round trip a legend forces.

| Practice | Verdict | Why |
|---|---|---|
| Images labeled A and B, meanings listed underneath | Content-hostile | The reader must hold the code in memory and travel between figure and caption |
| Words placed at the thing, letters deleted, a small glyph (a prohibition mark, a star) carrying the verdict | Content-responsive | Tufte's name for the fixed version is **content-hinted typography: direct labels, just like a map** |

**Annotations on annotations (p. 55).** A trade group annotated a photograph of a patient's post-operative IV lines with clinical claims. A clinician then annotated the annotations, **in a second color**, correcting each claim in place. The display then holds a *dispute* rather than a conclusion: the reader sees the claim, the rebuttal, and their adjacency — which no prose summary would preserve.

**Design rule:** when evidence is contested, give the rebuttal a distinct color and put it next to the claim it rebuts, not in a separate document. (Developed in `tufte-annotation-as-thinking`.)

---

## §13. Graphical Sentences That Carry a Data Table (p. 56)

A CONSORT-style participant-flow diagram is analysed as a single content-responsive graphical sentence reporting **22 numbers**: 14,692 assessed for eligibility, 5,331 excluded (itemised into seven reasons), 9,361 randomised, 4,678 versus 4,683 by arm, with dropouts itemised per arm.

A metabolic-pathway chart showing only about **5% of known pathways** is offered as the same species: like a map, its content *is* its format — a grid of high-resolution meaning rather than a picture with a caption.

**Test for whether you have one:** if you removed the numbers from your diagram, would anything remain that a reader could still act on? If yes, the numbers were decoration. If the diagram collapses, the format and the content are the same thing, which is the goal.

---

## §14. Line Weight and Type Weight as Meaning Hierarchy

Weight is a semantic signal: the heavier mark draws more attention, so the heavier mark must carry more meaning. The data line must visually dominate the connecting verticals, grid, and frame (*VDQI*, p. 186). The visual elegance of 18th- and 19th-century graphics came largely from copper-plate engraving's hair-thin strokes; the heavier lines of 20th-century drafting pens made charts look clumsy by comparison.

| Element | Role | Ink weight |
|---|---|---|
| Data series / measurement | Primary signal | Heaviest |
| Data-point labels, direct annotations | Primary context | Medium-heavy |
| Axis labels (named dimensions) | Frame context | Medium |
| Tick marks, grid lines | Reference structure | Light / hairline |
| Bounding box, axes | Container | Hairline or none |
| Legend box border | Structural noise | Eliminate if possible |

| Element | Wrong weight | Correct weight |
|---|---|---|
| Data values (numbers) | Light / thin | Regular or medium |
| Row / column labels | Bold | Regular or medium |
| Table header | Extra-bold caps | Small caps or medium |
| Footnote / source | Regular | Light or small |
| Units ("thousands") | Regular inline | Superscript or light suffix |

**Table rules (EI, p. 55):** Tschichold's hierarchy — rules in a table should be graded, with the heaviest reserved for the most structurally significant division and most horizontal rules simply deleted.

---

## §15. Typeface Choice for Data Contexts

| Criterion | Why it matters | Test |
|---|---|---|
| Legibility at small sizes | Labels must read at 6–8pt in tight spaces | Readable in a telephone-book column? |
| Character distinctiveness | 0/O, 1/l/I, 6/G, 5/S must not blur | Set "1Il0O6G5S" at target size |
| Low ink in regular weight | Structure must not compete with data | Is regular weight lighter than the data marks? |
| Tabular / lining figures | Numbers in columns must align | Equal horizontal space per digit? |
| Horizontal readability | Axis labels run left to right | Any optical trick slowing the horizontal scan? |

**Bell Centennial (Matthew Carter)** — designed for telephone books: high-density numeric columns under poor printing, with ink-trap details holding legibility at small sizes (*EI*, p. 105). The right model for schedules, dense tables, and tight labels. Carter is also Tufte's source for the letterform-anatomy analysis in *Visual Explanations* (pp. 98–99), where a diagram is remodeled from **24 to 66 direct labels**, and for the survey of ten constructed capital-A forms from 1460–1529 with stroke-to-height ratios between 1:12 and 1:8 (.083–.125), measured against the Trajan inscription cut in 112 AD (*VE*, pp. 112–113).

**Albers on all-caps and sans-serif (EI p. 51; VDQI p. 183).** Words are read as pictures of words, so differentiated letterforms read more easily; all-capitals is the hardest setting of all because it flattens word-shape; and Albers judged that a blanket preference for sans-serif demonstrates neither historical nor practical competence. Tufte's friendly-type rules (*VDQI*, p. 183) follow: upper-and-lower case, not all caps; a typeface designed for text, not a display face; and — a rule worth remembering when tooling fights you — lettering may legitimately be done by hand.

**Data and text should share a typeface (VDQI, pp. 180–181).** Graphics belong in the same visual register as the prose around them; a chart set in the software's default face announces that it was produced elsewhere and merely pasted in.

**Sans/serif as a categorical encoding:** see §9's baseball paragraph. Alfred Barr's chart of modern-art movements makes the parallel move with **size** rather than face, scaling each name in proportion to historical importance exactly as a map scales place-names (*BE*, pp. 64–68).

| Context | Preference | Reason |
|---|---|---|
| Body text alongside charts | Serif | Text rhythm matches explanatory prose |
| Tight data tables, schedules | Serif or humanist sans with tabular figures | Legibility at small sizes |
| Axis and tick labels | Regular-weight sans or serif | Must sit below the data without competing |
| Numbers in columns | Tabular lining figures only | Alignment is semantic |
| All-caps directional labels | Avoid | Low word-shape distinctiveness |
| Chart type vs. surrounding text | Same family | Data and text belong to one document (*VDQI* pp. 180–181) |

---

## §16. Annotation as Evidence, Not Decoration

Annotation is part of the evidential record. An unannotated image is a picture; an annotated one is an explanatory display.

**Galileo's satellites (BE):** notebook sketches of Jupiter's moons annotated with times, satellite labels, and distances in Jovian radii — words, numbers, scales, and linking lines. Stripped of annotation the sketch is decorative; annotated, it is evidence of orbital motion. (In SWFE, Galileo appears in a different argument — his 1601 handwritten copy of Ausonio's mirror diagram, pp. 64–66. Same figure, distinct argument.)

**Scale suppression as failure (BE):** Bloch's *Ichthyologie* (1795) drew 216 fishes all sized to fit identical boxes, silently erasing scale.

> "Every fish has both a different and unknown scale of measurement." — Tufte, *Beautiful Evidence*

**Cleveland's objection and Tufte's answer (BE, pp. 118–121).** William Cleveland holds that word-labels on data may interfere with assessment of the overall pattern and prescribes keeping notes, keys, and markers out of the data region. Tufte's rebuttal is the strongest defense of direct labeling in the canon: labels **are** data (naming the dots is what reveals that large dinosaurs have relatively small brains, and what makes plotting errors detectable at all); abandoning labels forces a code, and codes impede learning; segregating nouns from data-dots splits evidence on a verbal/nonverbal distinction that is uncartographic and substantively irrelevant; reducing data resolution moves the display the wrong way. He then concedes Cleveland has a real point, demonstrates it by deleting all 26 labels — and resolves it **by design rather than deletion**, pushing labels onto a different visual layer in a grayed field with the data-dots clustered in red.

| Annotation type | Function | Placement |
|---|---|---|
| Scale bar / ruler | Grounds the image in measurable reality | Edge of the subject area |
| Direct series label | Identifies without a legend round-trip | At the series terminus or peak |
| Explanatory callout | Marks an anomaly or feature | Leader line from whitespace to feature |
| Units suffix | Disambiguates numeric values | Inline with the axis label |
| Source line | Establishes credibility | Small type, bottom edge |

**Annotation density test:** remove every label. If the display is still fully self-explanatory, the labels were redundant. If it becomes ambiguous, they were annotation-as-evidence — keep them, and layer them rather than deleting them.

---

## §17. Self-Exemplifying Design

A data display must embody the principles it advocates. Tufte's bad-example scatter plot (*VDQI*) carries a tiny data set under oversized bold-italic axis labels, fat data points, large mid-plot annotations, all-caps labels, heavy ink texture, and lettering that clashes with the surrounding text. The governing criterion (*VDQI*) is the clear portrayal of complexity: reveal what is genuinely subtle, do not decorate what is simple.

**Checklist:**
- [ ] Does type-weight hierarchy match the data-importance hierarchy?
- [ ] Do labels sit at the data, or are they exiled to a legend?
- [ ] If a legend exists, does it teach a vocabulary reused across many displays, or a one-time code?
- [ ] Is the typeface legible at the smallest size it appears, and is it the document's own face?
- [ ] Do all numeric columns use tabular figures?
- [ ] Is all type horizontal? (90-degree rotation slows reading)
- [ ] Are content-responsive linebreaks used wherever lists or parallel structure appear — and were they chosen by the author, not the renderer?
- [ ] Is the aspect ratio a content decision, or a library default?
- [ ] Are small data sets shown as numbers, not encoded into areas or colors?
- [ ] Are paragraphs visually distinct enough to be re-found from memory?
- [ ] Where evidence is contested, does a second color carry the rebuttal in place?

---

## §18. Failure Modes

**F0 — LittleDataGraphics.** Encoding small data into a pie or bar chart; viewers decode areas and colors back to numbers, and the code teaches nothing. *Fix:* show the numbers. (SWFE p. 60)

**F1 — Content-indifferent linebreaks.** Wordspaces and breaks adjusted to square off the right margin, destroying syntax. *Fix:* break at commas, semicolons, full stops. (SWFE pp. 17, 52)

**F2 — The legend tax.** Series names exiled to a box eating >40% of the display, with order mismatched to the lines and a color code to memorize. *Fix:* direct labels at the line termini, in data-line color. (SWFE p. 63)

**F3 — Letter-coded captions.** "A:" and "B:" under the figure, meanings below — a legend by another name. *Fix:* words at the thing; a glyph for the verdict. (SWFE p. 55)

**F4 — Compositor-chosen breaks.** Long labels, headers, and titles wrapped by width alone. *Fix:* author-specified break points at natural phrases and major brackets. (SWFE p. 17)

**F5 — Default aspect ratio.** A chart's proportions set by the plotting library. *Fix:* bank local slopes toward ~45° and treat the ratio as content. (SWFE p. 63)

**F6 — Inverted weight hierarchy.** Heavy type on structure while data values stay light. *Fix:* lighten structure, strengthen data labels. (VDQI)

**F7 — Scale suppression.** Omitting measurement scales, turning evidence into illustration. *Fix:* embed a scale bar at the point of need. (BE)

**F8 — Clotted lettering.** Oversized, bold, or all-caps labels consuming space without adding information. *Fix:* reduce to the minimum label set that keeps the display self-explanatory. (VDQI p. 183; EI p. 51)

**F9 — Serpentine reading.** Layouts forcing a non-linear eye path — the New Haven table's thrice-repeated headings and 24 AM/PM markers. *Fix:* linearize reading order. (EI p. 104)

**F10 — Rotated labels.** Vertical y-axis labels. *Fix:* stretch the graphic horizontally, transpose, or set labels horizontally. (VDQI)

**F11 — Active punctuation in dense data.** Colons between hours and minutes, brackets around values — each mark is ink competing with numbers. *Fix:* a quiet separator (a dot, a thin space). (EI p. 104)

**F12 — Unanchored annotation.** Annotation floating in whitespace with no positional link to its datum. *Fix:* leader line, or place it adjacent.

**F13 — Uniform paragraph styling.** Every paragraph typographically identical, defeating retrieval. *Fix:* idiosyncratic paragraphs, one distinct treatment per evidence type. (SWFE p. 59)

**F14 — Deleting labels to reduce clutter.** Treating clutter as an attribute of the information rather than a failure of the design. *Fix:* layer the labels onto a quieter visual level; do not lower the data resolution. (BE pp. 118–121)

**F15 — Foreign typeface.** Charts set in the software's default face, visually announcing that they were produced elsewhere. *Fix:* one type family across data and text. (VDQI pp. 180–181)

**F16 — The zero degree of graphics.** Design-heavy layouts that fragment or subordinate text, delivering impressions instead of the sequenced depth of crafted prose — Giovannini's pathology, cited by Tufte, noting that books about graphic design are notorious for containing almost no text. The capitulation of text to layout is a named failure, not a style. *Fix:* let the prose argument set the layout; design serves the sentences. (VE p. 148 n. 25)

---

## §19. Concrete Thresholds

| Decision point | Guidance | Source |
|---|---|---|
| Minimum label size in print | Bell Centennial readable in telephone-book columns (~6–7pt at 600dpi) | EI, p. 105 |
| Direct label vs. leader line | Direct label when whitespace is adjacent to the datum; leader line only when crowded | EI, pp. 100, 105 |
| Line weight, data vs. structure | Data line heavier than connecting verticals — no fixed ratio, but data must dominate | VDQI, p. 186 |
| Graphic proportion | Tend horizontal; Playfair favored a ~1.4–1.8 width-to-height ratio | VDQI, p. 187 |
| Aspect ratio for slope reading | Adjust so local slopes average **~45°** | SWFE, p. 63 (Heer & Agrawala, 2006) |
| Legend failure threshold | A legend eating **>40%** of display area | SWFE, p. 63 |
| When a legend is legitimate | When it teaches a symbol vocabulary reused across a whole map/chart series, as swisstopo's is | SWFE, p. 62 |
| Hours/minutes separator | A quiet dot, not an active colon, in dense schedules | EI, p. 104 |
| Useful-ink floor for a table | Aim well above the New Haven table's 21% of area spent on actual data | EI, p. 104 |
| Small-data threshold | Any set small enough to encode in a pie or bar is small enough to print as numbers | SWFE, p. 60 |
| Content-responsive linebreak cost | +2–3 pages in a 500-page book eliminates ~2–5 billion reader impediments | SWFE, p. 50 |
| Screen space cost | Zero — content-hostile grids on screens are a choice, not a constraint | SWFE, p. 53 |
| Categorical encoding without a label | A serif/sans split can carry a whole categorical variable | SWFE, p. 61 |

---

## References

- ***Seeing With Fresh Eyes: Meaning, Space, Data, Truth*** — Edward R. Tufte (Graphics Press, 2020). **Chapter 1:** p. 14 (KMP code, 75% whitespace), p. 15 (poetry-line critics), p. 17 (the Great Disjunction — control, 1500 years; the math style sheet; the Ioannidis preview), p. 18 (the dishwasher manual's dangling linebreaks), p. 19 (Bringhurst; Cleveland Clinic thought bubbles). **Chapter 2, pp. 49–63:** p. 48 (Maugham prelude spread, facing the chapter opener), p. 50 (Darwin), p. 51 (Apollinaire, content-possessed), p. 52 (Ioannidis and Maugham re-set), p. 53 (zero-cost space, alignment as signal), p. 54 (Kepes and the white interval, Hokuba 1808), p. 55 (letter-coded captions, annotations on annotations), p. 56 (CONSORT diagram, 22 numbers; metabolic pathways), p. 57 (hyphens vs. dashes, the suspended sentence), p. 59 (idiosyncratic paragraphs, Galileo mid-sentence mode switch, *Lucky Jim* stacklist), pp. 60–61 (LittleDataGraphics, NWS KSFO, Egyptian vulture, baseball sans/serif), p. 62 (Swiss topo maps, legends **and** direct labels; the 8-row settlement table, reproduced from swisstopo BA200098), p. 63 (legend >40%, banking to ~45° with Heer & Agrawala 2006, the FT COVID chart). Also p. 67 (spacing for explanatory depth).
- ***Envisioning Information*** — Edward R. Tufte (Graphics Press, 1990): p. 51 (Albers on word-pictures, all-caps, and sans-serif), p. 55 (Tschichold's table-rule hierarchy), p. 62 (Rhein label placement; more ascenders than descenders), p. 86 (Byrne's spacious leading), pp. 104–107 (New Haven timetable, 21% data area, 104 cm of rules, serpentine reading, dot-vs-colon, Bell Centennial / Matthew Carter), pp. 13 and 113 (vertical Japanese script cooperating with layout), p. 118 (Rameau's swirling words as informational, not ornamental). **Verified against the source.**
- ***Beautiful Evidence*** — Edward R. Tufte (Graphics Press, 2006): pp. 10–17 (annotation as evidence, Galileo's satellites, Bloch's *Ichthyologie* and the scale-bar redesign), p. 51 (Gill Sans substitution recovering space), pp. 64–68 (Barr's proportional name-sizing), pp. 118–121 (the Cleveland labels debate, Tufte's five counter-arguments, and the layered redesign).
- ***Visual Explanations*** — Edward R. Tufte (Graphics Press, 1997): p. 97 (interpoints), pp. 98–99 (letterform anatomy, 24 → 66 direct labels, Matthew Carter as source), pp. 112–113 (ten constructed A-forms 1460–1529, stroke ratios 1:12–1:8, the Trajan inscription cut 112 AD).
- ***The Visual Display of Quantitative Information***, 2nd ed. — Edward R. Tufte (Graphics Press, 2001): pp. 177–191 (aesthetics, line weight, lettering, shape of graphics, horizontal labels), pp. 180–181 (data/text integration; one typeface across both), p. 183 (friendly-type rules; Albers on all-caps and sans-serif; lettering may be done by hand).

All passages paraphrased; quoted lines limited to single attributed sentences with page citations. The Swiss settlement table is third-party licensed material passing through two hands — cite swisstopo via SWFE p. 62.

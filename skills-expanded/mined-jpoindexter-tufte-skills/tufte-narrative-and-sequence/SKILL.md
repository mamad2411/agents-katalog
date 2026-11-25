---
name: tufte-narrative-and-sequence
description: "Use when designing or reviewing visual explanations of process, motion, causality, or change — instructional diagrams, animation stills, step-by-step guides, motion multiples, field guides, or technical presentations — or when auditing an image-based display for missing scales, hidden data, or misleading sequence."
tags: [tufte, narrative, sequence, causality, process, dequantification, disinformation, animation, data-visualization, small-multiples, parallelism]
---
# Narrative and Sequence

**Source:** *Visual Explanations: Images and Quantities, Evidence and Narrative* (VE), Edward R. Tufte, Graphics Press, Cheshire, Connecticut, 1997. Chapters 1–6.

## Overview

Visual explanations explain *why* and *how*, not just *what* — they depict process, causality, motion, and change. Two failures recur and both are epistemic, not aesthetic: **dequantification** (images stripped of the scales, labels, and orientation that answer *how many / how often / where / how much / at what rate*) and **disinformation design** (display tactics, borrowed knowingly or not from magicians, that conceal rather than reveal). The governing standard is the same one a scientist uses: show all the relevant data, put the causally meaningful variable on the correct axis, make comparisons within the eyespan, and never drop the cases that fail to confirm the pattern. Tufte's most consequential case is the Challenger launch decision — the 13 charts faxed to NASA the night before never put temperature, the causal variable, on an axis and left out 92% of the relevant temperature data (p.43); seven people died. Sequence and narrative design carry life-and-death weight.

> "People can see more clearly if they have the right idea." — Tufte, *Visual Explanations*, p.107

---

## §1. Images and Quantities — The Dequantification Problem (Ch.1, pp.13–26)

The foundational theme of the book: scientific and artistic images routinely shed their quantitative scaffolding. A picture without scale, orientation, and labels cannot answer the analytic questions — *How many? How often? Where? How much? At what rate?* Restoring those answers is "quantifying" the image.

**The three quantification techniques (p.13):** Tufte names the ways quantity attaches to an image — **direct labels** (words and numbers written straight onto the picture), **encodings** (values translated into visual properties such as tone or symbol), and **self-representing scales** (objects of known size placed inside the scene so the image measures itself — the opening example is Koudelka's photograph of a wristwatch held into an empty street, timestamping the scene). Every Ch.1 example below is a diagnosis against this triad.

**How the 2-D plane became quantified (the history of the statistical graphic):**
- For roughly **5,000 years**, two coordinates of a flat surface (maps) encoded only place-names — nouns in space, not measured variables.
- **van Langren, 1644** — a Flemish astronomer's chart of **12 estimates** of the Toledo-to-Rome distance in degrees of longitude. The true value is **16°30'**; every estimate ran too large, with Rome sprawled out to **22°–25°** (far east, into the Adriatic). It arranges (not merely tabulates) measurements in space relative to a true value — Tufte's candidate for the **earliest display of a distribution of common measurements**, the first statistical graphic.
- **Lambert, 1765** — described a *general* graphical grid with no map analogy: for each abscissa *x*, plot the corresponding ordinate *y*. This quantified the plane for any measured data and made fitted models — and therefore cause-and-effect display — possible.

**The multivariate problem:** most real problems are not two-dimensional. The central design challenge is representing three or more dimensions of data on a flat surface (paper, canvas, screen) — long handled by perspective in art and architecture, and now by data graphics.

**Named Ch.1 examples (each a dequantification lesson):**

| Example | Quantification device | Failure / fix |
|---|---|---|
| Repton, Brighton Pavilion perspective | Three figures with ten-foot poles placed in the scene for self-scaling, plus direct labels | The deep-background pole-person is drawn too small; "before/after" exaggerated (Lilliputian pole-people vs. comfortable giants in the "after") — scaling cheat |
| Lichtenstein, *Mural with Blue Brushstroke* (68×32 ft / 21×10 m) | Artist photographed atop a ladder as a self-representing scale | Published reproductions almost never convey original size; fix is a consistent-scale set of works |
| Herbert Matter / Giacometti portfolio | All sculptures photographed at one common scale, "as if in a gallery" — also ideal for field guides (birds, fish, plants) | 56 copies; sheet 20×48 in (51×123 cm); sculptures shown at 19% of actual size on the sheet, 7% in the book — small but mutually comparable |
| NCSA thunderstorm animation | Redesign adds a 3-D tripod of labeled axes + directional arrows | See below |
| Magellan Venus flyover | (none) | 22.5× vertical exaggeration — see Failure Modes |
| Cleveland sunspot series | Aspect-ratio "banking to 45°" | See below |

**The thunderstorm animation redesign (pp.20–23) — Ch.1, not Ch.4:** A supercomputer animation built from **9 time-dependent partial differential equations**; a **5-minute movie of a 2 hr 20 min storm**. The original is informationally flat — its dominant visual element (more than half the pixels) is a heavy "orthodontic" perspective grid resembling a Renaissance *pavimento* tiled floor; quantitative scales appear for only **14 of 315 seconds**. Tufte's redesign locates the storm inside a **3-D tripod of labeled scales** (16 km vertical, 100 km ground, North/East arrows) and adds **six small clouds as 3-D tick-marks** at minutes **25/48/71/94/117/140** along a **red time-line that flows left to right as the animation runs** (in the frame reproduced on p.21 it has reached minute 105 of the 140-minute storm) — a still, spatial history of the whole storm beneath the moving scene. The redesign also declares its own scaling: the vertical axis is stretched two-fold relative to the ground scales, and such shifts must be persistently disclosed to viewers (p.23). Restoring scale converts television into evidence.

**Cleveland's aspect-ratio rescaling — "banking to 45 degrees" (p.25):** For the sunspot series 1749–1924, choose the plot's aspect ratio so the absolute values of the slopes of selected line segments center on **45°** (computed iteratively). The reshaped graph reveals that cycles rise rapidly and decline slowly — an asymmetry strongest for sharp peaks, weaker for medium peaks, absent for small ones. Aspect ratio is a quantitative design variable, not a layout afterthought. (For the banking procedure itself, and how it interacts with sparkline-scale displays, see `tufte-sparklines` §7 — this section uses the result, that skill owns the method.)

**Quantitative scale of evidence (the compilation audit, pp.20–21):** Across **19 articles by 43 authors** (134 color scientific images): **65% had no scales or labeled dimensions, 22% partial, only 13% complete.** Twelve other compilations were equally dismal — dequantification is systemic, not anecdotal.

**Ethical floor (pp.24–25):** When an image serves as evidence, show the **innocent, unprocessed natural image alongside the manipulated one**, document the manipulators and methods, and reveal the full pool of images the displayed one was selected from.

---

## §2. The Evidence of Causality — Challenger Rules (Ch.2, pp.27–53)

**Rule 1: Show ALL the data, including cases where the effect did not occur.** The pre-launch indictment is missing data: the History-of-O-ring-Temperatures chart reported temperatures for only two launches plus four test motors — **92% of the temperature data was absent**, including 5 flights with erosion and all 17 flights with no damage (p.43). Only two blow-by cases were ever linked to temperature before launch. Dropping the disconfirming (zero-damage, warm-weather) cases destroys pattern detection.

**Rule 2: Put the causally relevant variable on the axis.** None of the 13 pre-launch charts arranged damage against temperature. After the accident, evidence prepared for the presidential commission repeated the failure in a new form — a chart of 48 rocket icons ordered by launch date, temperature written in small type, temporal rather than causal order (pp.46–47). Tufte keeps the two failures distinct: the same principles were violated in the 13 pre-launch charts as well as in the post-launch 48-rocket display (p.52). The pattern emerges only when launch temperature (°F) maps to x.

**Rule 3: Show the decision boundary.** Extending the temperature axis to launch day's forecast shows instantly that the launch sat far outside all prior experience — no data existed there.

**Tufte's redesigned display (p.45):**
- X: temperature of O-rings at launch, axis running 25°–85°F
- Y: **O-ring damage index, 0–12** — a severity-weighted composite of erosion, heating, and blow-by per launch (defined in fn.36, p.44)
- All 24 previous launches, including every zero-damage case
- The **26°–29°F launch-day forecast range marked as a labeled band** on the extended axis — a range, not a single line

**Display provenance (fn.39, p.46):** the famous damage-vs-temperature scatterplot most books reproduce was never faxed and never seen before launch — two commission staffers drew it after the accident to simulate the engineers' reasoning, and it implies a 7-flight analysis nobody performed. Even the canonical "bad chart" of this story is a reconstruction: when a display is evidence, document when it was made, by whom, and what its maker could have known.

---

## §3. Six Principles of Evidence Reasoning (Ch.2, p.53)

Both the Broad Street cholera investigation (Snow, 1854) and the Challenger post-mortem expose the same six principles — applicable to epidemiology, statistical graphics, and visual explanation alike:

1. Document the sources and characteristics of the data.
2. Insistently enforce appropriate comparisons.
3. Demonstrate the mechanisms of cause and effect.
4. Express those mechanisms quantitatively.
5. Recognize that analytic problems are inherently multivariate.
6. Inspect and evaluate alternative explanations.

Information displays must meet the same epistemic standard as scientific reasoning: design reasoning is not separate from analytical reasoning, it is an expression of it. Clear seeing and clear thinking are one act.

---

## §4. Explaining Magic and Disinformation Design (Ch.3, pp.55–71)

The actual chapter title is **"Explaining Magic: Pictorial Instructions and Disinformation Design."** Its method: catalog how magicians *suppress* understanding, then **invert** each tactic into honest design. An inventory of conjuring methods is an inventory of *what not to do*.

> "To document and explain a process, to make verbs visible, is at the heart of information design." — Tufte, *Visual Explanations*, p.55

That sentence is the chapter's governing claim; the magic catalog exists to serve it.

**Why diagrams beat eye and camera.** A drawing can show what no single real-world viewpoint can — the revealed illusion and the concealed gimmick simultaneously, the audience view and the backstage view together. Showing a sequence of changes over time is identical to showing adjacent layers of information: **on paper, time and space are as one** (p.57). The simplest rule for two viewpoints is to draw both: Tufte redraws a conjuring trick documented as far back as 1581, **adding a hinged flap** so the audience's view sits on top and the workings show beneath — the flap arrangement is his modern redrawing, not period apparatus (p.57).

| Instruction diagram | Quantified / layered device |
|---|---|
| Cards-in-Envelope (*Royal Road to Card Magic*) | **Ten** distinct depicted layers, with annotation pointing to each |
| Mitral-valve heart surgery | Layered hidden views from impossible viewpoints; a generic, idealized heart (useful abstraction) |
| Strike-second-deal (*Expert Card Technique*) | Arrow-line traces the path of the *absent* thumb; rotated 180° to the operator's view because the audience here is the student of magic |

**Misdirection inverted into a design principle — larger motions hide smaller motions.** A coin vanishes via the *backpalm* (Downs Eureka Pass, p.56): the small concealing move is masked under a large tossing motion of the hand. This is both Gestalt psychology and the core of misdirection. Henning Nelms' rule (p.64): movement attracts attention but *diminishes* visibility. Perception research calls it **visual masking** — a target stimulus made less visible by a spatiotemporally overlapping mask. In conjuring the mask makes the magic; in a display the same move makes a lie.

> "there is no magic in still-land." — Tufte, *Visual Explanations*, p.63

**Still-land vs. video-land.** Paper explains step-by-step mechanics well but cannot convey swift dexterity, the spark of conjuring, or the *retention-of-vision* timing a live illusion depends on. Yet video is no analytical refuge: it has credibility problems (did the assistant vanish, or was the camera turned off?), and unlike paper it denies the viewer control over pace, sequence, direction, and focus. For analysis, the self-paced still image wins.

**Combining text with images.** In roughly **80%** of magic literature, two nearly separate stories march along apart — the trick described in words, then again in pictures — forcing Euclid-style back-and-forth between "triangle ABC" in the text and ABC in a far-off diagram. Good pictorial instruction tightly fuses the shared verbs of text and image inside one figure (e.g., "pivots up to cross over and drop on").

**Disinformation in real displays (the inverted catalog, pp.64–65):**
- **Treacherous staircase** — a noisy, repetitive carpet pattern masks the edge of each step. At one NYC railroad station, lined treads caused **1,400+ falls in six weeks** before correction.
- **Cigarette billboard** — a thick frame and sans-serif capitals clutter and flatten the Surgeon General's warning; where scrutiny is damaging, scrutiny is diverted.
- **Chartjunk** — decoration triumphing over information is the same masking move applied to statistical graphics.

**The Automaton Chess Player — technically excellent diagrams that are FALSE (pp.66–67).** A sensation of the late 1700s: von Kempelen's machine (built **1769**, toured **50 years**; Franklin played and lost) appeared to play chess mechanically.
- **Willis, 1821** — analysis in **36 pages, 11 diagrams**, drawn in a murky dotted-outline language, **printed separately** from the text and bound front and back, requiring dozens of cross-references through a **19-letter call-out code**.
- **Brewster, 1834** — wholesale-plagiarized Willis, all **11 diagrams**, and *improved* the craft: crisp line-vs.-darkened-silhouette distinctions that cleanly layer revealed and concealed. But the incomplete copy **dropped the scale of measurement** (plagiarism → dequantification), kept the clumsy call-outs, and stranded captions pages away. Reproduced in **12 editions** of *Letters on Natural Magic*; admired by Edgar Allan Poe; it became the definitive account.
- **The point:** the diagrams are beautifully executed *wrong guesses*. No human climbed up into the Turk; the machine was a **puppet worked by long sticks** from a director hidden below. Plausible, vivid, copied — and false. The folklore principle: the truth never stands in the way of a good story, or a good illustration.

**More copied-error / truth-telling failures (p.71):** the **1622 "California as an Island" map** reproduced in **182 variants** (last copyist **1745**); **Dürer's two-horned rhinoceros (1513)**, copied as real for ~200 years; six-fingered conjurers in magic illustrations. Errors propagate because copying is cheaper than checking.

**Integrity test (conclusion, p.70) — apply to any explanatory display:**
1. Is the display revealing the truth?
2. Is the representation accurate?
3. Are the data carefully documented?
4. Do the methods of display avoid spurious readings?
5. Are appropriate comparisons and contexts shown?

---

## §5. Presentation Structure — PGP and the Six Rules (Ch.3, pp.68–70)

The same magic tactics, **reversed**, become teaching strategy. Hoffmann's 1876 rules for magicians were *suppress context* and *prevent reflective analysis* ("never tell the audience beforehand," "never perform the same trick twice"). A presenter does the opposite: tell them in advance, and repeat to reinforce.

**PGP (Particular → General → Particular)** is the structural core: open on one concrete case, abstract to the general principle, then return to a second concrete case showing the principle in action. Two particulars beat one anecdote.

**Six rules for technical presentations:**
1. Near the start, state the problem, why it matters, and the solution. (If you can't state the problem clearly, the content is deficient.)
2. Explain complex ideas with PGP.
3. Give everyone in the audience paper packed with relevant material (the high-resolution, file-able, accountable channel — unlike evanescent projected slides).
4. Analyze your details, then master them by practice.
5. Show up early.
6. Finish early.

**PGP applied to data displays:**
- Particular: one patient chart, one flight's O-ring data, one train on a timetable.
- General: the temperature-damage regression, the epidemic curve, the full timetable grid.
- Particular: the decision-boundary case — this flight, this date, this patient.

---

## §6. The Smallest Effective Difference (Ch.4, pp.73–77)

> "Make all visual distinctions as subtle as possible, but still clear and effective." — Tufte, *Visual Explanations*, p.73

The visual Occam's razor: what can be done with fewer visual means is done in vain with more. Subtle distinctions leave room for *more* distinctions — heavy contrast depletes the field.

**The driving example (p.73) — the anatomical ear, not the thunderstorm:** an ear diagram pierced by **25 thick pointer-lines** (acupuncture-needle weight), heavier than the ear itself, doing the trivial job of linking parts to a coded list. (It echoes the 1517 woodcut "The Wound Man.") The redesign **mutes the pointers** to clarify the ear and **replaces the letter-coded parts list with direct labels**.

**Two worked payoff cases (pp.75–77):** a text-selection highlight drawn as a dark field clutters the display and buries the very words selected; a lighter selection field marks the choice while keeping the type readable (p.75). The General Bathymetric Chart of the Oceans grades depth and elevation through **21 muted color gradations** — the deeper or the higher, the darker — so every tint carries several variables at once, contour numbers nearly retire the legend, and ship-route lines ride on a separate faint gray layer; a rainbow scheme would wreck it (pp.76–77).

**Just-noticeable vs. just-notable:** the human eye can detect *just-noticeable differences* across a continuous spectrum of ~**100,000 colors**. Reinhardt's near-black paintings exploit such vaporous gradations — fine for art, useless for data. Data displays need *just-notable differences*: definite, effective, minimal — stronger than Reinhardt's, far lighter than the ear pointers.

**Applies to every non-data element:** arrows, pointer lines, dimension lines, tick marks, scales, grids, meshes, rules, underlines, frames, boxes, compartments, codes, legends, highlights, accents, bevels, shadows, fills.

**Mechanism (figure/ground):** muting secondary elements relative to the negative space produces a visual hierarchy — inactive background, secondary structure, notable content. When *everything* is emphasized, *nothing* is; strong secondary contrasts also visually activate (and clutter) the background.

**Rule:** any element that is not data should be as close to invisible as its function permits.

---

## §7. Parallelism — Space vs. Time (Ch.5, pp.79–103)

The primary design axis is spatial vs. temporal comparison. Comparisons are more effective when information sits adjacent in space rather than stacked in time.

| Method | Mechanism | Memory required | Effectiveness |
|---|---|---|---|
| Spatial adjacency (small multiples) | Both states visible at once within the eyespan | None | Highest |
| Temporal flip (Repton flap) | Rapid physical alternation — quasi-spatial | Minimal | Medium-high |
| Slide / animation sequence | One state at a time, serially | Full visual memory | Low |

**Parallelism connections (p.82)** are built by: position, orientation, overlap, synchronization, and similarities in content. Good form is clear without becoming spectacle; the chapter's closing line claims that a structure of rhythms and relationships turns parallelism into the poetry of visual information (p.103).

**Repton's before/after flap (pp.80–81):** Humphry Repton's Red Books (c.1800) used a hinged flap — lift it and the proposed "after" landscape replaces the existing "before." Rapid flipping creates near-simultaneous alternation, reading out differences that pure sequence loses to memory decay.

**Salyut-6 cyclogram (pp.92–95):** hand-drawn by cosmonauts Georgi Grechko and Yuri Romanenko during their **96-day flight (Dec 10, 1977 – Mar 16, 1978)**, tracking **8 simultaneous dimensions** on one sheet, all within the eyespan:
1. Moon phases · 2. Holidays · 3. Weeks (red ticks) · 4. Fraction of flight completed · 5. Dates · 6. Elapsed days · 7. Weeks remaining · 8. Weeks finished.

**The accordion fold (p.93):** the cosmonauts folded the meter-long chart so that no more than about 15 days of future schedule was ever in view — display scope trimmed to psychological load, the uncolored (future) portion never allowed to loom larger than the colored (completed) one. Tufte notes they were the first crew ever to redesign an information display in outer space.

**Beethoven 9th CD Companion (pp.88–89):** synchronized visual parallelism of **6 musical motifs** (Opening Ritornello vs. Exposition) with playable audio — spatial layout of time-based data, navigable without imposed sequence.

---

## §8. Faulty Parallelism — Named Examples (Ch.5, pp.100–103)

Parallelism fails when parallel structures are not comparable on the same terms.

**Repton's own flaw (p.102):** his "after" views added elements absent from "before" — **nine** full-sized boats vs. tiny ones, deer added to meadows. Embellishment beyond scope makes "what the intervention changed" indistinguishable from "what the designer added for appeal."

**NYT Yanomami photograph (p.102):** the caption read **"Napoleon A. Chagnon, left,"** but the man on the left was not Chagnon. The stated parallel (position → named identity) was false — faulty parallelism in caption design.

**HIV mortality two-graph (p.103):** adjacent charts gave men a vertical scale of **0–65** and women **0–30**, making the women's slope look comparable though men's death risk was more than double. Unequal scales on nominally parallel charts actively mislead.

**Rule:** every element that differs between parallel panels must differ *because the data differ* — never from design additions, caption errors, or inconsistent scales.

---

## §9. Six Functions of Small Multiples (Ch.6, pp.105–119)

Multiple images serve six functions (p.105):

1. **Reveal** — surface repetition, change, pattern, and surprise.
2. **Compare** — make comparison direct and visual (the essence of statistical thinking).
3. **Dimensionalize** — add depth to flat paper/screen by arraying panels and slices.
4. **Enumerate** — build visual lists of objects and activities for analysis and decision.
5. **Narrate** — track sequences of motion through time.
6. **Intensify** — amplify and reinforce the meaning of single images.

**Huygens' *Systema Saturnium* (1659, pp.106–108):** **32 Saturn images** at different orbital positions, each paired with an Earth telescope view — a notebook-like collation in which changes across the multiples are the verbs of motion in a time-series.

**13 Saturn interpretations (p.107):** a foldout of **13 geometrically distinct wrong answers**, Galileo through Fontana, **1610–1645**, all predating Huygens' correct model — the case for having the right idea before you can see clearly.

**Graphical patient status (pp.110–111):** **24 small images per patient** (labs, medicines, x-rays) on one page — **11,616 cells and 1,786 values** formerly scattered across paper records, at a **10–20×** improvement in information-transfer rate over verbal presentation.

**Administrative bloat / organizational apparatus (p.118):** Ad Reinhardt's 12-version wine-glass multiple wasted **42%** of each framed rectangle on noisy borders; the redesign strips all frames so each image's edge defines itself. Organizing devices (grids, compartments, call-outs, narrative sequence, overlap) must consume as little space as possible.

**Resolution and the eyespan (p.116):** low-resolution screens prevent multiples from coexisting in view, forcing serial scrolling and destroying spatial comparison. Higher resolution directly enables better analytical comparison.

**Design for the context of use (p.115):** the physical circumstances of reading should drive the format. An underwater fish card must minimize page-turning and can exploit refraction — submerged objects appear at about three-quarters their true distance, so a "water-book" packs denser material than an "air-book"; cookbooks should lie flat; driving directions need short, content-broken lines glanceable between road and page; night-flying charts must read in dim light.

**Frequency-ordered multiples (pp.115–116):** order a large image set by how often each item is actually encountered, not alphabetically, randomly, or taxonomically. Sighting distributions are heavily skewed — a handful of species dominates roughly 90% of encounters (fn.9 cites Herbert Simon on skew distributions) — so a most-common-first card outperforms an encyclopedic taxonomy for novices. General rule: choose the ordering dimension that matches the user's task, not the archive's classification.

**Highlighting calibrated by demonstration (p.116):** the foureye butterflyfish's false eye-spot ringed in brilliant white is disinformation design evolved by fishes; Tufte redraws the fish with the ring muted, and the before/after pair isolates exactly what the highlighting alone contributes — a smallest-effective-difference experiment embedded in the chapter.

**False clustering (p.112):** accidental design communalities (shared color, border weight, proximity) induce groupings unrelated to the data; sequential display likewise creates false *temporal* clusters as the viewer moves frame to frame.

---

## §10. Motion and Sequence in Still Images (Ch.6, pp.108–109)

In static motion displays, **space takes over the role time plays in video** — adjacent frames replace temporal succession, letting viewers assess change and rates of change at their own analytic pace rather than the medium's. Still images permit self-pacing, return to earlier frames, and comparison of non-adjacent frames — none of which continuous video allows.

The unavoidable loss is duration (the rhythms of real motion). The avoidable failure is **dequantification**: motion multiples that omit any explicit time scale, so the viewer cannot judge rates between frames.

**Temporal density rule — match sampling tempo to the motion's character:**
- Smooth, incremental motion (orbits, continental drift): few frames suffice. Huygens spaced Saturn positions **1.8 Earth-years** apart — fine because the motion is smooth and predictable.
- Abrupt, irregular motion needs dense sampling. Muybridge used **18 photographs** for a few seconds of leapfrog.

**The interpolation problem:** discontinuous spatial frames of continuous activity force the viewer to interpolate across the gaps; when motion is irregular, large gaps mislead.

**Worked motion-narrative examples:** Descartes' rotating-ruler bug (ghosted labels XYY signal direction; an explicit arrow would clarify); the Marey/Weber overlapping-image walk cycle; the three-panel stickleback "distraction display," where separate panels are paragraphs of activity, dotted lines track motion within a panel, varied postures imply movement, and panels are divided merely by the absence of background — a design so unobtrusive it disappears into the content.

**State instructional morals positively (p.108, fn.4):** the scuba training diagram shows a diver jabbed by a runaway flotation float, forcing viewers to extrapolate the un-drawn correct behavior from a depicted failure. Phrase the moral as the desired action — grab the tube with both hands to keep it balanced — rather than illustrating only what went wrong.

**Note on Ybry's graphical timetable:** the 1846 train timetable (time, station, train, speed, type as diagonal lines) is documented in *Envisioning Information* (1990), pp.97–113 — **not** in VE. VE footnote 12 (p.93) explicitly redirects there for space-by-time grids.

---

## §11. Named Failure Modes

| Failure mode | Source | Description |
|---|---|---|
| Dequantification (image) | VE Ch.1, p.20 | Scientific/art image stripped of scales, labels, orientation — can't answer how many/how often/where/how much/at what rate |
| False scaling / vertical exaggeration | VE pp.20–24 | Magellan Venus flyover stretched **22.5×** vertically — 3°-slope plains read as near-vertical peaks; fix is a Repton-style natural-vs-hyped before/after |
| Wrong aspect ratio | VE p.25 | Slopes not banked near 45° hide cyclic structure (Cleveland sunspots) |
| Selective data display | VE Ch.2, p.43 | Pre-launch temperature chart held only 2 launches + 4 test motors — 92% of temperature data missing, all 17 no-damage flights absent |
| Wrong variable on axis | VE Ch.2, pp.46–47 | Arbitrary sequence (flight order, alphabet) instead of the causal variable — the post-accident 48-rocket commission chart |
| Undocumented display provenance | VE fn.39, p.46 | Post-hoc reconstruction (the commission staffers' scatterplot) retold as if it existed at decision time |
| Missing decision boundary | VE Ch.2 | No reference line marking the threshold in the data space |
| Disinformation design | VE pp.64–65 | Display tactics that conceal — masking carpet on stairs, frame/caps cluttering a warning, chartjunk |
| False-but-plausible diagram | VE pp.66–67 | Technically crisp drawing that is a wrong guess; copied for its clarity (Automaton Chess Player) |
| Plagiarism-induced dequantification | VE p.67 | Incomplete copying drops the scale of measurement (Brewster's redrawing of Willis) |
| Propagated copied error | VE p.71 | California-as-island (182 variants), Dürer's two-horned rhinoceros |
| Text/image disjunction | VE p.63 | Words and pictures run as two separate stories, forcing Euclid-style cross-reference |
| Still-image motion without time scale | VE p.109 | Motion multiple omits an explicit time axis; rates unjudgeable |
| Mismatched temporal density | VE pp.108–109 | Uniform frame spacing for irregular motion; large gaps mislead |
| Faulty parallelism — content | VE p.102 | Added elements break comparability (Repton nine boats, deer) |
| Faulty parallelism — caption | VE p.102 | Positional label ≠ named person (Yanomami "Chagnon, left") |
| Unequal parallel scales | VE p.103 | HIV mortality charts 0–65 vs 0–30 prevent valid slope comparison |
| False visual clustering | VE p.112 | Accidental color/border similarity induces groupings unrelated to data |
| False temporal clustering | VE p.112 | Serial display fabricates patterns as the viewer pages through |
| Administrative bloat | VE p.118 | **42%** of frame area spent on borders, not information (Reinhardt multiple) |
| Screen-to-screen sequencing | VE p.116 | Low resolution forces temporal comparison instead of spatial adjacency |
| Heavy secondary elements | VE Ch.4 | Pointers/grids/borders given data-level visual weight (25-pointer ear) |

---

## §12. Do / Don't Pairs

| Do | Don't |
|---|---|
| Quantify every image — explicit scales, orientation, labels | Publish a dequantified picture that can't answer how much / at what rate |
| Show natural and stretched scales as a before/after when exaggerating | Ship a 22.5×-exaggerated flyover with no honest baseline |
| Bank slopes toward 45° to expose cyclic structure | Accept the default aspect ratio and bury the pattern |
| Show all data including zero-effect cases | Show only confirming cases |
| Put the causally relevant variable on the axis | Put an arbitrary sequence (flight number, alphabet) on the axis |
| Draw the decision boundary as an explicit reference line | Leave the threshold implicit |
| Place before/after states adjacent in space | Show them only in temporal sequence |
| Keep parallel panels identical except where the data differ — same scales, terms, elements | Add elements to "after" not in "before"; use unequal vertical scales |
| Invert magicians' tactics into honest design — reveal the gimmick, mask nothing | Let a noisy pattern, frame, or chartjunk mask the signal (disinformation design) |
| Treat a clear, plausible diagram as a hypothesis to verify against reality | Copy a crisp diagram because it looks authoritative (Automaton) |
| Fuse the shared verbs of text and image in one figure | Run words and pictures as two separate stories needing cross-reference |
| Label the time axis on every motion multiple | Let the viewer infer the time scale |
| Match frame density to the abruptness of the motion | Apply uniform frame spacing regardless of motion character |
| Mute every secondary element to the smallest notable difference | Give grids, pointers, borders the same weight as the data |
| Use self-paced still images adjacent in space for analysis | Default to video when stop-action enables better study |
| Keep organizing apparatus visually minimal | Spend frame area on administrative framing instead of information |
| Open with problem → importance → solution; use PGP (particular → general → particular) | Lead with methodology before the audience knows the problem |
| Give the audience dense paper, repeat to reinforce, finish early | Rely on evanescent slides; suppress context like a magician |
| Run the integrity test: truthful, accurate, documented, no spurious readings, fair comparisons | Trust a display because it is vivid and well-executed |

---

## Cross-book notes

- *Seeing with Fresh Eyes* (p.38) independently argues that stop-action still sequences beat video for analysis — the viewer controls pace, order, and non-adjacent comparison — a second-book confirmation of §10's space-replaces-time rule.
- *Beautiful Evidence* (p.166) supplies the presentation-side failure: rigid slide-by-slide hierarchies slice evidence into arbitrary compartments and wreck narrative continuity; when lower-level NASA engineers reasoned by email — several hundred of them, about the same danger, in the same weeks — roughly 90% wrote sentences ordered into paragraphs and only 10% used bullet lists of 2–3 levels, abandoning the hierarchical outlines of the original PP pitches. The mechanism on that page: every text-slide restarts its own 4-to-6-level bullet hierarchy afresh, so each elaborate architecture of thought is made to fit exactly one slide.
- *The Visual Display of Quantitative Information* (pp.155, 159) holds the in-book seed of reading order as a design variable. A graphic can be built for **three viewing depths at once**: what it yields from a distance (overall structure aggregated out of the microstructure), what it yields up close (the fine structure), and what lies implicitly behind it. The Census population map is the worked case (p.155, on the fold-out spread that follows) — outside urban centers each dot stands for 500 people, roughly 400,000 points on one implicit grid. Depths have a co-equal companion: p.154 closes on multiple layers created by multiple viewing *depths* **and** multiple viewing *angles*. Tufte's term for a layout that licenses several ordered readings of a single display is **viewing architecture** (p.159, his italics): the sequence a reader is meant to move through is chosen, not accidental. This is the narrative-order question asked of one static image rather than of a series, and it is where *Envisioning Information*'s micro/macro chapter starts from.
- *Envisioning Information* (p.119) closes its space-time chapter with the matching dilemma: all narrative design is the reduction of four-dimensional reality — time plus three-space — to marks on flat, static paper.
- *Beautiful Evidence* (p.66) makes the positive case for non-linear reading order: stripping Alfred Barr's 51 arrows and 19 bracket lines from his cubism chart leaves a field resembling Apollinaire's *Calligrammes* (the poem "Voyage," 1913–1916, reproduced redrawn), and Tufte's claim is that the two-dimensional typography of Barr and Apollinaire — breaking the putative linearity of conventional text — allows a multiplicity of more or less simultaneous narrative sequences and readings; map-makers have serenely distributed words in 2-D space for 6,000 years. Same page, the tells: Barr's date markers resemble film-sprocket holes; time flows *down* to avoid hints of upward progress; and the chart is analytically dense only across 1905–1925, the exhibition's own span — a coverage-bias tell worth naming: a diagram's resolution can track the author's holdings rather than the subject's history.

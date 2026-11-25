---
name: tufte-chartjunk
description: "Use when a chart, dashboard, or data graphic looks busy, shimmery, or over-decorated — crosshatch or pattern fills, heavy or doubled grid lines, 3-D extrusion, fake perspective, pictorial fills, drop shadows, or unexamined software-default styling — or when auditing any graphic before publication for marks that carry no data."
tags: [tufte, data-visualization, chartjunk, visual-noise, data-ink, moire]
---
# Chartjunk

## Overview
Chartjunk is any graphical element that does not communicate data — it burns ink, area, and viewer attention while adding nothing to meaning. Tufte sorts it into three kinds: **vibrations** (optical interference from busy patterns), **grids** (reference lines that overpower the data they support), and **ducks** (decoration that becomes, or buries, the data). The governing law is that a graphic succeeds or fails on its content, gracefully displayed: ornament can amplify a dull graphic's failure but has never rescued a thin data set from its own emptiness. The practical test is therefore subtractive — strip every mark that does not encode data or serve as a minimal navigational aid, then see what is lost.

---

## §1. Vibrations — Optical Interference from Busy Patterns

A vibration is a perceptual artifact: dense, regular, high-contrast patterns applied to a graphic make the eye see shimmer, motion, or depth that is not in the data. The dominant source is **moiré** — two or more fine regular patterns (crosshatching, diagonal hatching, dot screens) overlaid or printed close together produce an unstable, eye-straining flicker. Moiré is unintentional optical art: the same effect 1960s Op artists pursued on purpose, smuggled into statistical graphics by default fill patterns.

### Mechanism
The visual system reads closely spaced alternating lines as movement or relief — a low-level artifact, not information. Adjacent active lines also imply forms that were never drawn (the perceptual "1 + 1 = 3 or more" effect Tufte names in *Envisioning Information*): the more active marks crowd together, the more spurious structure the eye invents. The result is a raised visual noise floor that contaminates the whole graphic and makes the underlying quantities harder to read.

### Tufte's moiré surveys (pp. 109–112)
Two samples, one finding. Random samples (1980–82) from the ten most-cited scientific journals put moiré vibration at 2% of graphics in *Biochemistry*, rising to 17% in *Science* and 21% in the *New England Journal of Medicine* (p. 110). A parallel survey of graphics manuals and software documentation runs worse: from Brinton's 12% up through Spear's 46%, Tell-A-Graf's 53%, and SAS/GRAPH's 68% (p. 112). The takeaway is structural, not anecdotal: when the manual or the tool ships vibration as the default, vibration is produced at scale by people who never chose it — the software-documentation peak marks exactly that. Even a statistics journal institutionalized it: JASA's own style sheet displayed a figure "prepared in the proper form" that needed 131 line-strokes plus 15 digits to convey trivial information — vibrating, unevenly spaced, misaligned (p. 110). Tufte also notes vibration may well peak for **equally spaced bars** (p. 109) — precisely where default fills land.

### The Bertin rebuttal
Jacques Bertin argued a designer could court controlled moiré — flirt with ambiguity without surrendering to it. Tufte rejects this for data graphics: moiré is an *undisciplined* ambiguity with an eye-straining, illusive quality that pollutes the whole image, and there are no good examples of statistical graphics that gain anything from it. For data, vibration is always cost without benefit.

### Do / Don't: Vibrations

| Do | Don't |
|---|---|
| Solid fills, distinct grays, or open white to separate areas | Crosshatch, diagonal hatching, or dot screens on any fill |
| Differentiate series with a lightness ramp (white → light → mid → dark gray → black) | Dense alternating line patterns at any scale or zoom |
| Choose hue/saturation steps (print-safe) for categories | Overlapping screens that produce moiré at print resolution |
| Proof fills at the actual output resolution before committing | Accept software default fills — most generate vibration |

**Failure mode — "we used a computer to build a duck":** the rendering tool fills bars with ordered crosshatch by default, producing optical vibration and signaling technology over content. The fix is to turn the pattern off, not to pick a different pattern.

---

## §2. Grids — Reference Lines That Overpower the Data

The grid is the most sedate chartjunk, but a heavy grid is still chartjunk. A grid has exactly one legitimate job: helping a reader look up or interpolate values. When grid lines are darker, heavier, or denser than the data, figure and ground reverse — the grid becomes the graphic and the data recedes. Tufte's rule of thumb: grids are for the working stage, plotting data at home or in the office; in finished print they should be muted or suppressed.

### Grid weight hierarchy (best → worst)

| Grid treatment | Effect on figure/ground | Verdict |
|---|---|---|
| No grid; data-derived tick marks only | Data dominant | Preferred for most charts |
| Light **gray** grid, weight well under the data strokes | Data dominant | Acceptable when look-up is the task |
| **White** grid (gaps inside filled bars / erased to white) | Data dominant | Elegant for bar charts and histograms |
| Mid-gray grid, equal weight to the data | Competing | Marginal; suppress if you can |
| Dark/black grid at full weight | Grid dominant | Chartjunk — suppress |
| Doubled grid lines (box frame + inner grid) | Grid dominant | Severe: in the Tukey multiwindow plot, doubled lines consume 18% of the display's area and spawn optical white dots at intersections (p. 114) |

### Named example: Marey's train schedule
E. J. Marey's Paris–Lyon timetable (a Tufte touchstone) is extremely data-dense: every diagonal is a train, every crossing a stop. The grid must not compete with that thicket of lines. Three treatments, ranked:

| Grid treatment | Result |
|---|---|
| Heavy black grid (as often reproduced) | Grid dominates; trains hard to trace |
| Thinned black grid | Slightly better; trains more legible |
| Gray grid | Best; trains read as foreground, grid recedes to a reference layer |

The correct fix is always a **gray** grid, never a thinned-black one. Most ready-made graph paper is printed in a dark grid; plot on the **reverse (unprinted) side** so the lines show through faintly without cluttering the data — and if the paper is heavily gridded on both sides, throw it out (p. 116).

### The one-question grid test (SWFE p. 134)

*Seeing With Fresh Eyes* compresses the whole grid argument into a question to ask of any display: **what is the strongest visual element here?** Tufte's gloss — the correct answer is never "the grid lines." If the honest answer is the grid, the frame, or the furniture, the figure/ground relation has already inverted and no amount of restyling will fix it; the grid must recede or go. He demonstrates the repair by re-setting a plotchart with *ghost grids* — a grid present enough to support look-up, faint enough that the data is unambiguously the loudest thing on the page.

### The look-up exception
When a graphic functions as a look-up table — readers will read off specific values — a grid earns its keep. Even then: gray, delicate, never dark. A delicate gray grid supports more accurate reconstruction of values than a dark grid that visually swamps the points being read.

### Do / Don't: Grids

| Do | Don't |
|---|---|
| Delete the grid first; restore only if reading fails | Ship heavy or dark grid lines in any published graphic |
| Use a light gray grid only when look-up is the primary task | Use doubled grid lines or a box frame around panels |
| Use a white (negative-space) grid inside filled bars | Plot on graph paper printed-side-up for publication |
| Keep grid stroke well under the data stroke weight (≈ 20–30% is a practitioner default — VDQI prescribes only muted and gray, no percentage) | Let grid lines equal or exceed the data strokes |
| Prefer gray over thinned black when a grid is required | Pile a dense grid onto an already line-rich graphic |

**Failure mode — the grid that buries the data:** a full dark grid over an age/sex pyramid or a trend line camouflages the very profile that matters (the notch, the staircase, the slope). Removing the grid lets the data silhouette speak.

---

## §3. Ducks — Decoration That Becomes the Data

The duck is chartjunk at its most extreme: decoration that overwhelms, replaces, or structurally *becomes* the data. The name comes from the **Big Duck**, a duck-shaped retail building on Long Island (Flanders, NY) where the entire structure is its own sign — form swallows function. In Tufte's terms a graphic is a duck when decorative forms or computer debris take over, when the data measures and structures turn into Design Elements, and when the display purveys graphical style instead of quantitative information.

### The architectural rule (Learning from Las Vegas)
Tufte borrows from Venturi, Scott Brown & Izenour: modernists who renounced applied ornament ended up designing buildings that *were* ornament. The maxim they quote — a warning from the nineteenth-century architect A. W. N. Pugin — transfers directly to data graphics (VDQI p. 117):

> "It is all right to decorate construction but never construct decoration." — A. W. N. Pugin, quoted in Venturi, Scott Brown & Izenour, *Learning from Las Vegas*

Applied: you may style the axis labels, type, weights, and annotations (decorate construction), but the graphic's structure must never itself be ornament. When fake perspective, 3-D extrusion, or a pictorial frame *is* the structure, the graphic is a duck.

### Named example: crosshatched bar chart → table
A common duck is a multi-category bar chart where each bar carries a different crosshatch (moiré on top of a duck) and the axis is choked with percentage ticks and all-caps labels. Tufte's remedy is to redraw it as a plain table. The table wins on every count: exact values instead of estimated bar heights, full category names instead of cramped labels, room for a second data column, and zero vibration. When the data is a handful of numbers attached to many words, the table is the graphic.

### Interior decoration — symptoms
Treating a chart as a canvas to be styled rather than a message to be optimized. Watch for:

- Fake perspective on bars or pies to look "modern"
- 3-D extrusion that breaks comparison (the visible front face ≠ the value)
- Pictorial fills (stacked coins for money, little people for population) that obscure the quantity they claim to show
- Color gradients laid over areas whose value is already encoded by area
- Drop shadows, glows, or embossing on chart elements
- Complexity as a credential — "remarkable that the computer drew this" instead of "what interesting data"

### Boutique data graphics — the high-fashion duck
Annual reports, mass media, and advertising actively cultivate the duck. Tufte's label is **boutique data graphics**: elaborate displays whose visual complexity is inversely related to their information content. Fake perspective is the signature move of the genre.

The compact diagnostic comes from *Envisioning Information*'s diamonds/fishnet duck: "Everything counts, but nothing matters" (EI p. 34). In chartjunk every element clamors for attention and none carries meaning — the one-line test for any suspect display.

### Production quality does not redeem a duck
Tufte concedes there are some superbly produced ducks — the *California Water Atlas* among them (p. 119) — but craft and junk are orthogonal: high production values decorate the failure, they do not cure it. At the other pole sits an *American Education* 3-D display spending five colors to carry five numbers, Tufte's candidate for the worst graphic ever to reach print (p. 118). Ducks also compound with vibration: a NEJM stacked pyramid's back planes optically flip forward (a Necker illusion) while its depth-stacked variable carries no label and no scale (p. 109).

### Do / Don't: Ducks

| Do | Don't |
|---|---|
| Let the data's structure set the graphic's structure | Let the graphic's structure turn into decoration |
| Use a table for a few numbers and many words | Use a multicolor full-page illustration for ~5 data points |
| Design to provoke "what interesting data" | Design to provoke "remarkable the computer drew that" |
| Decorate construction (style labels, type, weight) | Construct decoration (extrude to 3-D, add fake perspective) |
| Keep every mark removable only at the cost of information | Keep any element that survives a "what does this encode?" test as "no data" |

**Failure mode — the sham dimension:** adding a depth axis the data does not have. Extruding 2-D bars into 3-D both adds non-data ink *and* distorts the data ink, because the value now maps ambiguously to a front face, a back face, or a volume. This is the same offense the **Lie Factor / dimensionality** rule attacks (VDQI ch. 2): an n-dimensional quantity drawn in more than n dimensions overstates change. Cross-check sham dimension against `tufte-graphical-integrity`.

---

## §4. Why Chartjunk Corrupts — and How to Detect It

Chartjunk is not neutral waste; it actively degrades reading through three channels:

1. **Perceptual masking.** Vibration and heavy grids raise the visual noise floor, so genuine signals (the notch, the slope, the outlier) drop below it and become unreadable.
2. **False complexity.** Crosshatch, borders, grids, and fills make a graphic *look* information-dense while it encodes five numbers; the reader spends attention decoding structure instead of reading data.
3. **Displaced trust.** When the rendering shows off, attention shifts from message to medium — but a graphic's credibility rests on the data, not the sophistication of the draftsmanship.

### Data-ink ratio as a chartjunk detector
Every chartjunk element lowers the data-ink ratio, so a chartjunk audit *is* a data-ink audit:

```
data-ink ratio = (ink used to present data) / (total ink used to print the graphic)
```

| Chartjunk element | Penalty |
|---|---|
| Moiré / crosshatch fill | Adds non-data ink |
| Heavy or doubled grid | Adds non-data ink |
| Decorative border or frame | Adds non-data ink |
| 3-D extrusion / fake perspective | Adds non-data ink **and** distorts data ink — doubly penalized |

Any mark that cannot be defended as encoding data, or as a minimal aid (one axis line, a muted look-up grid), is chartjunk. See `tufte-data-ink-ratio` for the maximization procedure.

---

## §5. Diagnosis Checklist

Run before publishing any chart. Any failed row names the chartjunk type to fix.

| Check | Pass condition | Fail = |
|---|---|---|
| Are fills solid, gray, or open (no patterns)? | Yes | Vibration (crosshatch/moiré) |
| Does any series rely on hatching to be told apart? | No | Vibration |
| Is the grid lighter than the data strokes? | Yes, or no grid | Grid chartjunk |
| Is the grid gray rather than black, single not doubled? | Yes, or no grid | Grid chartjunk |
| Can you read the data profile with the grid hidden? | Yes | Grid chartjunk |
| Does every remaining mark encode data or aid navigation? | Yes | Duck (decoration) |
| Is the count of ink marks ~proportional to the data points? | Roughly | Duck (false complexity) |
| More percentage ticks on the axis than data points? | No | Duck (overcrowded axis) |
| Is the depiction flat — no perspective the data lacks? | Yes | Duck (sham dimension / 3-D) |
| Would a plain table read more accurately than this chart? | No | Duck (chart form unjustified) |

---

## §6. Remediation Patterns

### Vibration fix
1. Replace every crosshatch/pattern fill with solid fill, gray, or white.
2. To separate multiple series, use a lightness ramp before reaching for any pattern.
3. If the tool emits crosshatch by default, override it in the rendering layer — never accept default fills.

### Grid fix
1. Delete the grid. If the chart still reads, leave it deleted.
2. If look-up is required, set the grid to ~10–20% gray at ~0.25pt against ~1pt data strokes (≈ 20–30% of the data weight). These numbers are practitioner defaults, not Tufte's — the book's rule is only that the grid be muted, gray, and visually subordinate.
3. Alternative: a **white** grid — gaps inside filled bars, or grid lines erased to white over a tinted ground.
4. Never plot on graph paper printed-side-up; use the unprinted reverse or plain paper.

### Duck fix
1. Remove everything that does not encode data.
2. Flatten any 3-D extrusion to 2-D; delete fake perspective.
3. If the structure itself is the decoration (the fill is the message), redraw from scratch as a flat chart — or a table.
4. When the data is fewer than ~10 numbers and the story is comparative, ship a table, not a chart.

---

## §7. The Bottom Line

No information, discovery, wonder, or substance is ever generated by chartjunk. The graphics that endure — Minard on Napoleon's march, Marey's train schedule, the newspaper weather history — are gripping because of narrative power, immense honest detail, and genuinely interesting data, never because of decoration.

> "Forgo chartjunk, including moiré vibration, the grid, and the duck." — Tufte, *The Visual Display of Quantitative Information*

---

## §8. Cross-book notes

**The three redesign principles (BE p. 121)** — the later books' cleanest statement of the chartjunk thesis, and the one to quote in a design argument:
1. Clutter is a failure of *design*, not a property of the information. A crowded graphic does not prove the data was too much.
2. Do not solve a visual problem by cutting content-resolution — that moves the display the wrong way.
3. Fix the design instead. Tufte demonstrates this on a labelled scatterplot by pushing labels onto a separate visual level rather than deleting them.

**Chartjunk of graph bureaucracy (BE p. 153)** — a named second species alongside garish decoration, and the more common one in professional work: optically active grids, boxes and frames, redundant representations of the same datum, cross-hatched bars. The case study is the Boeing *Columbia* spreadsheet, where the most visually prominent things on the page are empty framing area and grid prisons around numbers too small to read. The tell is that the chart looks *serious* rather than gaudy — bureaucratic junk hides behind an air of rigor.

**Frames as the loudest element (BE p. 62)** — heavy frames activate the negative space between them, so the gutters out-shout the data. Tufte's audit question for any framed layout: do the most prominent visual effects on this page convey relevant content? If the answer is no, the frames are the chartjunk.

**Visual clarity and intellectual clarity (VE pp. 47–49)** — a rocket-silhouette bar chart of launch history is Tufte's specimen for decoration standing in for evidence, and it carries the argument that lack of visual clarity in presenting evidence tracks a lack of *intellectual* clarity about the reasoning. Junk is a symptom, not just a blemish. VE also supplies the institutional vocabulary — **"administrative bloat"** for the apparatus that accretes around evidence (pp. 118, 125, 149) — and the measurement to go with it: Reinhardt-style framing consuming **42%** of a display's area (p. 118). *Seeing With Fresh Eyes* repeats the audit on an image matrix that turns out to be only **42% images**, the other 58% frame furniture, oversized checkmarks, and undersized labels (p. 24). Measure the junk as a percentage of area; the number ends the argument faster than the adjective does.

---

*Source: Edward R. Tufte, **The Visual Display of Quantitative Information**, ch. 5 "Chartjunk: Vibrations, Grids, and Ducks," with Pugin's architectural rule as quoted in Venturi, Scott Brown & Izenour, *Learning from Las Vegas*. Concepts paraphrased; quotations limited to single attributed sentences. Survey figures (journal moiré percentages pp. 110–112, the 18% doubled-grid cost p. 114) are verified against the 2nd ed. (2001); grid stroke-weight percentages are labeled practitioner defaults where they appear.*

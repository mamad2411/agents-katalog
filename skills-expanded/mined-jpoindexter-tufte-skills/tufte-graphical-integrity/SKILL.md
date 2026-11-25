---
name: tufte-graphical-integrity
description: "Use when designing, reviewing, or auditing any chart for truthfulness — truncated baselines, scaled pictograms, dual axes, perspective or 3-D effects, nominal-dollar time series, or any display where the visual effect may exceed the effect in the data. Covers the Lie Factor and Tufte's six principles of graphical integrity."
tags: [tufte, data-visualization, graphical-integrity, lie-factor, statistical-graphics]
---
# Graphical Integrity

## Overview
A graphic has integrity when the physical size of the marks on its surface is directly proportional to the numbers they stand for. Most distortions are not random: they systematically exaggerate the magnitude of recent change. Tufte's contribution is to make distortion measurable — the Lie Factor turns "this chart feels misleading" into a number you can compute and defend.

**Sourcing note.** Tufte computes and publishes five Lie Factors in VDQI Ch. 2: fuel economy **14.8** (p. 57); the Time "In the Barrel" oil-price barrel **9.4** — +454% drawn as +4,280% (p. 62); the Washington Post oil derricks **9.5** — 708% drawn as 6,700% (p. 62); the shrinking family doctor **2.8** (p. 69); and **59.4** — "a record" — when the Time barrel is read as a volume, 27,000% vs. 454% (p. 71). Any other numeric figure in this skill is an illustrative derivation of the stated mechanism, labeled as such — never cite it as a Tufte-stated value.

## §1. The Lie Factor

The single measurement that converts opinion into evidence:

```
Lie Factor = (size of the effect shown in the graphic) / (size of the effect in the data)
```

"Size of effect" is a percentage change: `(later − earlier) / earlier × 100`. Compute it once for the data, once for the printed marks (line lengths, bar heights, icon areas), then divide.

**Thresholds:**

| Lie Factor | Verdict | Action |
|---|---|---|
| 0.95 – 1.05 | Acceptable — ordinary plotting error only | Ship |
| < 0.95 | Understates — graphic shrinks the real effect | Rescale to proportional |
| > 1.05 | Overstates — distortion beyond plotting error | Rescale to proportional |
| 2 – 5 | Common range for published newspaper graphics | Treat as a red flag, recompute |
| > 10 | Extreme — the graphic falsifies the news in the data | Reject and redraw |

- Tufte sets the honest band at **0.95–1.05**; anything outside is distortion, not rounding.
- Distortion is almost always one-directional (overstating), and Lie Factors of **2 to 5** show up routinely in the popular press.
- To compare an overstatement against an understatement on equal footing, compare the **logarithms** of the Lie Factors — a 2× overstatement and a 0.5× understatement are equal in magnitude, opposite in sign.

**Worked example — Fuel Economy Standards (NYT, 1978), Tufte's own computation:**

| Quantity | Value |
|---|---|
| Data: standard rises 18 mpg (1978) → 27.5 mpg (1985) | (27.5 − 18.0)/18.0 = **+53%** |
| Graphic: line drawn 0.6 in (1978) → 5.3 in (1985) | (5.3 − 0.6)/0.6 = **+783%** |
| **Lie Factor** | 783 / 53 = **14.8** |

The road also recedes toward a vanishing point — drawn in *reversed* perspective, with the future in front and large (p. 58). The date labels on the left stay a constant size as they recede, while the mpg numbers on the right shrink under two simultaneous effects at once: the value change and the perspective. Data change and design distortion become visually inseparable.

A related perceptual fact grounds the whole chapter (p. 55): reported experiments find the perceived area of a circle grows roughly as (actual area)^0.8, with the exponent varying about ±0.3 by person and context — so even a "correctly scaled" area encoding misreads, and different viewers misread it differently.

## §2. The Six Principles of Graphical Integrity

Tufte's closing checklist for the chapter. Each principle names a class of lie it forbids.

| # | Principle (paraphrased) | What it rules out |
|---|---|---|
| 1 | Marks on the surface must be proportional to the quantities they represent. | Scaled pictograms, perspective foreshortening, truncated baselines used to steepen slopes |
| 2 | Use clear, detailed labeling to defeat ambiguity; write explanations and annotate key events on the graphic itself. | Unlabeled axes, missing units, unmarked index base, no annotation of causes |
| 3 | Show data variation, not design variation. | Mid-chart scale changes, irregular intervals, shifting canvas size or aspect ratio |
| 4 | For money over time, deflated and standardized units beat nominal units. | Nominal-dollar charts that look like a boom but are flat in real per-capita terms |
| 5 | Information-carrying (varying) dimensions must not exceed the dimensions in the data. | 2-D or 3-D icons (barrels, figures, dollar bills) used for a single scalar |
| 6 | Graphics must not quote data out of context. | Before/after charts that hide the surrounding trend; comparisons that omit control groups |

Three of these are quotable verbatim and are worth memorizing as test questions to run against any chart:

> "Show data variation, not design variation." — Tufte, *VDQI*

> "Graphics must not quote data out of context." — Tufte, *VDQI*

> "In time-series displays of money, deflated and standardized units of monetary measurement are nearly always better than nominal units." — Tufte, *VDQI*

## §3. Named Failure Modes — Detection Catalog

Six recurring ways a graphic lies. For each: the cue that exposes it, and the principle it breaks.

| Failure mode | Visible cue | Principle broken | How to measure it |
|---|---|---|---|
| Perspective / receding baseline | Lines or bars drawn in 3-D depth or toward a vanishing point | 1 | Measure printed length, compute Lie Factor |
| Dimension inflation | A scalar shown by an icon's area or volume (height + width both vary) | 5 | Compare area/volume ratio to data ratio (§4) |
| Design variation as data variation | Scale or interval changes across one chart; tall/thin canvas | 3 | Check that one data unit = one constant printed size everywhere |
| Nominal money illusion | Dollar amounts over years with no "constant \$" or "per capita" note | 4 | Re-plot deflated and per-capita (§6) |
| Out-of-context quoting | Two data points, or one group, with no surrounding series | 6 | Extend the series; add control groups (§7) |
| Detection-inflated rate | A "how much is out there" curve rises right after the measuring effort changed, with no outcome series beside it | 6 | Plot the companion outcome series on the same frame; mark the regime change (§7b) |
| Stripped labeling | Bare numbers, no units, no index base, no source | 2 | Restore units, base year, source, event annotations |

**Tufte's five published Lie Factors (VDQI Ch. 2):**

- **Fuel Economy Standards (NYT, 1978) — Lie Factor 14.8** (p. 57). Receding-road line lengths; see §1. Mode: perspective baseline.
- **"In the Barrel" oil price (Time, 1979) — Lie Factor 9.4** (p. 62). A +454% price change drawn as +4,280%. Mode: dimension inflation. Read as a *volume*, the same barrel reaches **59.4 — "a record"** (p. 71): 27,000% of ink for 454% of data.
- **Oil derricks (Washington Post) — Lie Factor 9.5** (p. 62). 708% drawn as 6,700%. Mode: dimension inflation.
- **The Shrinking Family Doctor (LA Times, 1979) — Lie Factor 2.8** (p. 69). Share of family-practice doctors falls from 27% (1964) to 12% (1990); the human figures shrink far more than the percentages do, and the 2.8 is *before* counting extra distortion from perspective and uneven spacing of the years. Mode: dimension inflation (a 2-D figure for a 1-D percentage).

**The editorializing rule (p. 59):** decoration and editorial comment on a graphic are permitted; distorting the *data measures* to make the editorial point is not. A cartoon pictogram that implies no quantitative precision at all (the 4,340-pound-chicken drawing, p. 73) is exempt from the proportionality principle — the lie begins only when a mark pretends to be scaled.

## §4. Proportional Representation: the Dimension Trap

One-dimensional data must be drawn with one-dimensional ink — length or position on a common scale. Encoding a scalar as area or volume introduces two stacked errors:

1. **Geometric amplification.** If a value changes by ratio *r*, an area built by scaling both sides changes by *r²*, and a volume by *r³*. The lie grows by the square or cube of the intended change.
2. **Perceptual under-reading.** People do not mentally convert perceived area or volume back to the correct linear value, so even a "correctly scaled" area chart is misread.

**Worked illustration (derived from the mechanism — not a Tufte-stated figure):**

| Encoding of a value that doubles (+100%) | What the eye reads | Lie Factor |
|---|---|---|
| Length only (bar / line on common scale) | +100% | 1.0 — honest |
| Icon with both width and height doubled | area 2×2 = +300% | 3.0 |
| 3-D icon read as volume | 2×2×2 = +700% | 7.0 |

Same datum, no change in the number — the distortion comes purely from the spare dimensions. This is why barrels, shrinking dollar bills, and human figures lie even when the artist scales them "to proportion."

**Do / don't:**

| Do | Don't |
|---|---|
| Encode 1-D data with bar length or dot position on a common, zero-based scale | Encode 1-D data with circle area, icon height + width, or 3-D volume |
| If a symbol must be scaled, vary one dimension only | Vary both width and height in response to a single number |
| If circles are unavoidable, scale by **area** to the data (not radius) and print the value | Let readers infer magnitude from an unlabeled area or volume |
| Use a flat, 2-D bar chart | Add perspective depth that creates false foreshortening |

## §5. Design Variation vs. Data Variation

The subtlest lie: the canvas itself changes across the graphic, so the eye attributes layout changes to the data. The remedy is a stable, uniform frame — one data unit occupies the same printed size everywhere on the surface.

**The canonical case — the OPEC five-scale chart (p. 61):** one NYT graphic uses five different vertical scales (from $8.00 to $3.92 per inch) and two horizontal scales, so the same price change looks up to 15.1× bigger depending on where on the chart it happens to sit.

| Design-variation type | Mechanism | Cue to catch it | Fix |
|---|---|---|---|
| Mid-chart scale change | Same quantity occupies different printed sizes by position | Two y-axes, or a scale break with no zigzag mark | One scale, full range |
| Non-uniform time axis | Recent intervals compressed or stretched vs. history | Unequal gaps between equal time steps | Equal pixels per equal time unit |
| Shifting aspect ratio | A tall, narrow canvas exaggerates apparent slope | Frame much taller than wide | Neutral aspect (often near the "banking to 45°" angle) |
| Perspective recession | Depth shrinkage and data change become inseparable | 3-D scene, vanishing point | Flatten to 2-D |

**Do / don't:**

| Do | Don't |
|---|---|
| Keep one continuous scale across the whole frame | Switch scales partway, or stack two incompatible scales |
| Space equal time steps with equal width | Compress the most recent interval to manufacture a trend |
| Hold the aspect ratio constant when comparing charts | Stretch one chart vertically to dramatize its rise |

## §6. Money Over Time: Deflate and Standardize

Nominal-dollar time series almost always overstate real growth, because the dollar's value and the population both drift underneath the numbers.

| Adjustment | Why it matters | What it exposes |
|---|---|---|
| **Deflate for inflation** | Nominal dollars conflate price level with real quantity | A "rising" budget can be flat or falling in constant dollars |
| **Standardize per capita** | Population growth inflates any aggregate total | Per-person spending often grows far less than the total |
| **Neutralize aspect ratio** | A tall canvas exaggerates the climb | The real slope, neither steepened nor flattened |

**Pattern to watch:** a nominal chart shows steep continuous growth; after deflating and dividing by population, the same series turns flat — sometimes into an outright real-terms *cut*. The actual news (the decline) was invisible in nominal units. Always state on the graphic whether dollars are nominal or real, and which base year the deflator uses.

**Worked example — the NY State budget "Magical Parallelepipeds" (pp. 66–68):** population +10% over the period; the dollar of 1967 = $2.03 by 1977. Deflated per-capita spending rises ~20% to 1970, flattens, then *declines* in 1977 — while the nominal chart showed an unbroken boom. Same pattern in oil (p. 63): in the four years before the 1979–80 price surge, the *real* price of oil had been declining — "the graphic had missed the news."

## §7. Context: "Compared to What?"

A graphic answers a question, and the question is always *compared to what?* A chart that cannot answer comparisons lies by omission. Sparse, data-thin graphics should raise suspicion, not trust.

**Context checklist:**

| Question | What it rules out |
|---|---|
| What was the trend *before* the intervention? | Mistaking normal variation or regression-to-the-mean for an effect |
| What happened *after*? | Mistaking a one-year blip for a lasting change |
| What happened to *comparable groups*? | Mistaking a region-wide trend for a local cause |
| Is the baseline year cherry-picked? | An anomalous "before" that makes any "after" look dramatic |

**Connecticut traffic-deaths pattern — three framings of the same data:**

| Data shown | Apparent conclusion | Honest? |
|---|---|---|
| Two years (before / after a speeding crackdown) | The crackdown caused a dramatic drop | No — single comparison |
| The full multi-year series | The drop sits within normal year-to-year swings | Closer |
| The full series plus neighboring states | All states fell together; no unique local effect | Yes — context restored |

### §7b. The Companion-Series Test — cancer screening (cross-book: *Seeing With Fresh Eyes*, pp. 87 and 117)

Tufte's later work supplies the strongest working example of Principle 6, and it extends the context rule in a way the Connecticut case does not: sometimes the missing context is not *more years* or *more groups* but **a second series measuring the same phenomenon by a route the first one cannot inflate.**

**The construction.** Both spreads plot two rates per 100,000 on one frame over four decades — the rate of *disease diagnosis* ("you have cancer") and the rate of *mortality*. Page 87 does it for breast cancer in women 40 and over, marking on the chart where mass mammography screening begins; page 117 does it for all cancers in the United States, 1975–2015, as a two-panel small multiple of women and men, marking where PSA testing begins on the men's panel. In every panel the diagnosis curve climbs steeply after the screening program starts while the mortality curve stays flat or drifts gently down, and on p. 87 the metastatic-incidence line runs flat along the bottom throughout.

**What the divergence measures.** The widening band between the two curves is not noise and not lag. Tufte shades it and names its contents: false alarms, over-diagnosis, cured cancers, incidentalomas, and indolent and subclinical disease — many of them in people who will die *with* the condition rather than *of* it. The gray area is therefore a **measurable quantity**, readable off the chart, and it is the entire finding. His on-chart verdict:

> "Cancer diagnosis is an unreliable measure of true cancer occurrence." — Tufte, *Seeing With Fresh Eyes*, pp. 87 and 117

**Why one series alone would be a lie of context.** Each curve, published by itself, supports a confident and wrong story:

| Series shown alone | Apparent conclusion | What the companion series reveals |
|---|---|---|
| Diagnosis rate rising | An epidemic is under way — occurrence is climbing | Mortality did not move; the detection effort changed, not the disease |
| Diagnosis rate rising, framed as screening success | The programme is finding disease it was built to find | Finding it did not reduce deaths from it |
| Mortality falling, alone | Treatment is winning | On p. 117 Tufte attributes much or most of the decline to smoking cessation — prevention, not cure |
| Five-year survival improving | Patients are living longer | Survival is measured from *diagnosis* to death, so moving the diagnosis date earlier lengthens survival without postponing a single death (p. 87) |

That last row is the trap worth naming explicitly. **Lead-time bias is a denominator lie dressed as an outcome.** Any metric whose clock starts at detection will improve automatically when detection moves earlier, no matter what happens to the patient. The honest denominator is population mortality per 100,000, which no amount of extra looking can inflate.

**The magnitude that makes it matter.** Tufte pairs the charts with the number needed to treat: somewhere between 3 and 1,000 cancer patients are treated for each one who benefits, and sometimes far more are harmed than helped (p. 87). A chart that shows only the rising diagnosis curve has quietly recommended all of that treatment.

**The transferable rule.** This generalizes far past medicine to every metric that rises when you look harder — bug counts after a new linter, fraud "detected" after a new rule, incidents "reported" after a reporting campaign, security findings after a scanner upgrade, engagement after a tracking change:

| Do | Don't |
|---|---|
| Plot the detection-sensitive rate against an outcome series that detection effort cannot inflate | Publish the detection rate alone and let it read as occurrence |
| Mark on the chart the date the detection regime changed | Leave a methodology change invisible inside a continuous line |
| Shade and label the divergence between the two — it is the finding, not the background | Draw both curves and leave the gap unremarked |
| State what any survival- or duration-style metric is measured *from* | Report time-since-detection as if it were time-of-death postponed |
| Say which curve the intervention was supposed to move | Let a movement in the easy curve stand in for the hard one |

Tufte's closing annotation on p. 117 is the one-line summary of what forty years of both series together actually establish:

> "Cancer is mostly prevented, less often cured." — Tufte, *Seeing With Fresh Eyes*, p. 117

## §8. Labeling as the Reader's Only Defense

Labels are not decoration. They are the one check a reader has against a chart that might be lying, and Tufte treats thorough, on-graphic labeling as the primary weapon against distortion.

| Do | Don't |
|---|---|
| Put the unit of measurement on every axis | Leave bare numbers with no unit |
| Spell out the index base (e.g., "1972 = 100") | Bury the base in a footnote or omit it |
| Annotate key events (wars, policy changes, recessions) directly on the chart | Let readers guess the cause of an inflection |
| State plainly whether dollars are nominal or real | Default to nominal and let readers assume real |
| Print the data source on the graphic | Hide attribution in a distant caption |

## §9. The "It Shows the Right Direction" Defense

The standard rationalization for a lying graphic is: "It's roughly right — we only wanted to show the general direction of change." This treats data as merely *ordinal* (bigger/smaller) while attaching invented magnitudes.

It does not hold:

- A Lie Factor of 14.8 is not "roughly right." Direction is the cheapest, least informative part of the message.
- When distortion **reverses** the story — a real-terms budget cut drawn as a boom — even the direction is wrong.
- Numbers carry **magnitude, not just order**. A graphic that preserves only direction has discarded most of the information and kept the part a single sentence could have stated.

Getting the arrow to point the right way is never a defense for fabricating how far it points.

**The second defense (p. 77):** "the true numbers are printed right there on the graphic, so the drawing's distortion is excused." It fails the same way — honesty in one corner of the image does not license a fifteenfold lie in the rest of it. The marks are what the eye reads; the printed numbers are an alibi, not a correction.

## §10. Quick-Reference Audit Protocol

Run this before publishing or signing off on any data graphic. Each failure raises the odds of a Lie Factor outside 0.95–1.05 and should trigger an explicit calculation.

```
[ ] Lie Factor computed (graphic effect / data effect). Within 0.95–1.05?
[ ] One continuous scale across the whole frame? No mid-chart breaks or twin axes?
[ ] Equal time steps drawn with equal width?
[ ] Visual dimensions ≤ data dimensions? (1-D data → length/position, never area/volume)
[ ] No perspective, depth, or receding baseline distorting the marks?
[ ] Money deflated to constant dollars and per-capita where population moved?
[ ] Every axis, unit, and index base labeled? Source printed on the graphic?
[ ] Key events annotated directly on the chart?
[ ] Enough surrounding series and control groups to answer "compared to what?"
[ ] Any detection-sensitive rate plotted beside an outcome series that detection cannot inflate, with the regime change marked?
[ ] Aspect ratio neutral — neither steepening nor flattening the real slope?
```

If any box is unchecked, do not assume dishonesty — compute the Lie Factor and decide on the number, not the impression.

## §11. Cross-book notes

**Integrity lapses inside the hero examples (BE p. 127).** Minard's *Carte Figurative* is the pack's exemplar of excellence, and it still fails a Lie Factor check in one place: the band widths for the Nieman river crossing are drawn at roughly **1:28** where the underlying numbers give **1:42**. Worth teaching precisely because it is Minard — a graphic can be the best ever drawn and still contain a measurable distortion, so the audit runs on the work you admire, not only on the work you suspect.

**Suspicious precision (BE p. 75).** Four-significant-digit indices derived from crude measurements, or a date reported as "54.97 million years," advertise a resolution the measurement never had. False precision is a distortion in the opposite direction from the Lie Factor: the marks understate the uncertainty rather than overstating the effect. Report to the precision the method supports, and show the interval where one exists.

**Units as an integrity surface (BE p. 165).** The *Columbia* briefing slide carried three different unit expressions for the same class of quantity on one page (3 cu. in / 1920 cu in / 3 cu in). The CAIB's own observation is the rule worth carrying: in aerospace engineering a misplaced decimal or a mistaken unit engenders real inaccuracies — the veiled reference being the Mars spacecraft lost to a metric/non-metric mismatch at a cost of roughly $250 million. Unit discipline belongs on the labeling checklist in §8, not in a style guide.

**Copied errors and the good-story problem (VE pp. 67, 71).** Tufte's line for the mechanism is that the truth never stands in the way of a good story, and his evidence is that graphical errors *propagate by reproduction* rather than being corrected by it: California drawn as an island in **182** map variants down to 1745; Dürer's rhinoceros copied for roughly **200 years** after better specimens were available; conjuring illustrations reproducing a figure with six fingers because the engraver copied the engraver. Practical consequence for an integrity audit: provenance is a data-quality question. Ask where a figure was copied from before asking whether it is drawn accurately, because an accurate redrawing of a wrong original is still wrong. **VE p. 70 supplies the companion five-question integrity test** to run against any evidence display.

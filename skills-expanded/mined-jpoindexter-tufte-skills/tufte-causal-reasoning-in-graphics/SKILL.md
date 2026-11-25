---
name: tufte-causal-reasoning-in-graphics
description: "Use when building or critiquing any display whose job is to support a causal claim or a go/no-go decision — epidemic maps, risk scatterplots, failure analyses, treatment comparisons, policy charts — or when reviewing whether a graphic shows why something happened rather than merely when it happened."
tags: [tufte, data-visualization, causal-inference, evidence-design, decision-making]
---
# Causal Reasoning in Graphics

## Overview

Most data graphics describe; few argue. The difference is whether the display is organized around the causal variable or merely around time and sequence. Tufte's chapter "Visual and Statistical Thinking" in *Visual Explanations* establishes the standard through two paired case studies: John Snow's 1854 cholera map, which correctly displays a causal argument and helps end an epidemic, and the 13 Morton Thiokol charts faxed to NASA the night before the Challenger launch, which rested on the right causal theory but selected and arranged the data in ways that concealed the causal signal and contributed to seven deaths. The lesson is not stylistic: how data is arranged determines whether a causal relationship is visible or invisible, and that invisibility can be fatal.

---

## §1. The Fundamental Question: Compared with What?

Every causal claim requires a comparison. Without a baseline, a count is only a count.

Tufte identifies "Compared with what?" as the foundational question in statistical analysis. In *Visual Explanations* (p. 30), he argues that studying only cholera victims provides only half the evidence — a complete causal investigation requires equally rigorous analysis of those who did *not* contract the disease.

Snow had 83 deaths mapped. The map's causal argument depended equally on showing the spaces with no deaths — the brewery (70+ workers, no cholera; they drank malt liquor and never used the Broad Street pump) and the workhouse (535 inmates, only 5 deaths; they had their own well and never sent to Broad Street for water). Both anomalies are visible only because they appear on the same map as the deaths.

The Thiokol engineers committed the mirror failure. Pre-launch, their damage-history chart listed the damaged flights with no temperatures attached, and their temperature chart covered just two launches plus four test motors (p.43) — the 17 flights without damage, almost all at warm temperatures, never entered the evidence. (The familiar 7-damaged-vs-17-undamaged split describes the post-accident 48-rocket chart, pp.46–47.) Those undamaged flights are the statistical leverage that reveals the temperature-damage correlation.

Tufte draws the parallel directly in *Visual Explanations* (p. 44): the Thiokol engineers' data selection was equivalent to Snow having mapped only a subset of cholera deaths while ignoring all the disease-free areas and their pumps. The undamaged flights carry the statistical leverage that makes the temperature pattern visible — numbers become evidence only when placed in relation to each other.

### Do / Don't: Baseline inclusion

| Do | Don't |
|---|---|
| Show all observations: cases AND non-cases | Show only the damaged flights, the sick patients, the failing products |
| Label the comparison groups explicitly on the display | Let the viewer assume the shown data is the complete data |
| Quantify the expected rate vs. observed rate | Report only the count of anomalies |
| Include anomalies that work against your argument | Select for publication only results consistent with your case |

---

## §2. Temporal vs. Causal Data Structure

Time-series is the default graphic form. It is almost never the right form for causal argument.

> "the passage of time is a poor explanatory variable, practically useless in discovering a strategy of how to intervene and stop the epidemic."
> — Tufte, *Visual Explanations*, p. 29

Snow's original data was a list of 83 deaths in date order — a natural time-series. Plotted as daily counts, the chart shows the epidemic's rise and fall but reveals nothing about cause: there is no pump on the chart, no geography, no comparison. The chart is purely descriptive.

Snow converted the 1D temporal ordering into a 2D spatial comparison: deaths plotted by address on a street map, with all 13 community pumps also marked. This recast the same data into a form that could bear a causal argument.

NASA and Thiokol got the same choice wrong twice. Pre-launch, none of the 13 charts arranged damage against temperature. After the accident, the display prepared for the presidential commission — 48 rocket icons, SRM 1 through SRM 24 — again arranged the rockets in temporal order, with the causal variable, temperature, written sideways in small type near each rocket (pp.46–47). Tufte's corrected version places rockets in temperature order along the horizontal axis, with damage markers, and adds the Challenger's 26°–29°F forecast position — far beyond all previous experience. The pattern is immediately visible. Tufte's own sentence keeps the two failures distinct: the principles of evidence display were violated in the 13 pre-launch charts as well as in the post-launch display that arranged the 48 little rockets in temporal rather than causal order (p.52).

Tufte's rule (*Visual Explanations*, p. 49) is that a display must serve the analytic purpose in front of it. When that purpose is testing a possible cause-and-effect relationship, the graphic's only job is to arrange the data so the causal link becomes visible. Time and sequence are the wrong organizing axes unless time is itself the suspected cause.

### Choosing the display axis

| Situation | Wrong axis | Right axis |
|---|---|---|
| Epidemic investigation: where did people get sick? | Date of death (time-series) | Location relative to water sources (spatial) |
| O-ring risk at cold temperatures | Launch sequence number (temporal) | Temperature at launch time (causal variable) |
| Drug efficacy by patient subgroup | Enrollment date | Dosage or patient characteristic |
| Equipment failure rates | Serial number / production date | Operating temperature or stress load |

### Aggregation artifacts (temporal and spatial)

Aggregation can manufacture or destroy a signal on either axis. The artifact is a property of where the bin edges fall, not of reality.

**Temporal.** Snow's daily cholera death counts show a smooth decline that is already well underway and is left essentially unchanged by the removal of the Broad Street pump handle (early morning, September 8, 1854). Add the same daily data into weekly intervals of September 1–7 and 8–14, and the removal suddenly appears to cut the weekly toll from 458 to 112 — an "effect" produced entirely by the aggregation, since the daily series shows no such break. Shift the interval boundaries by as little as two days (lagging the post-removal count to begin September 10, allowing for the incubation delay between drinking the water and dying) and the chart's shape changes yet again. Time-series displays are acutely sensitive to the choice of interval length and end points; small changes in either can reverse the apparent story.

**Spatial.** The same trap operates geographically. Mark Monmonier (*How to Lie with Maps*, pp. 142–143) re-binned Snow's individual death locations into different sets of areas, shading each area by its death count. Under one partition into six areas the Broad Street cluster is obvious; under a second the counts come out nearly the same in four of the five areas and the cluster disappears; under a third the two darkest (deadliest) areas do not even contain the infected pump. Snow's dot map of individual deaths survives all of these re-partitions; every area-aggregated version distorts or erases the signal. (A dot map carries the opposite cost — it shows counts, not rates, so it cannot by itself answer "compared with what?" about the population at risk. The complete answer is a dot map plus a population-rate map.)

**Specification searching.** Tufte also names the modern, computing-enabled form of this hazard: with fast tools you can sift thousands of alternative aggregations, groupings, and models, then report only the one that flatters your case. The statistical literature calls this *data mining*, *multiplicity*, or *specification searching* (Tukey; Leamer; Fisher). Treat any single presented chart as the most favorable of many that were silently tried, unless the analyst documents the alternatives examined.

Rule: when in doubt, graph the detailed underlying data and assess the effects of aggregation afterward. A real signal survives reasonable changes of interval, bin, and area boundary; an artifact does not. Never publish only the aggregated result without checking that the signal holds across plausible alternative groupings.

---

## §3. The Snow Cholera Map as a Model of Causal Argument

Snow's map succeeds as a causal display because it satisfies four principles simultaneously.

### Principle 1 — Place data in the context appropriate to assessing cause and effect

The map's two-dimensional geography is the natural context for a question about contaminated water sources. Every data point (a death) is plotted relative to its distance from every potential cause (each pump). The causal candidate and the effect are on the same display.

As Tufte describes in *Visual Explanations* (p. 30), Snow transformed his data from a one-dimensional temporal list into a two-dimensional spatial display — plotting each death by address against the locations of all 13 community pumps. The resulting map exposes a strong association between cholera mortality and the Broad Street pump, visible precisely because it includes both the affected areas and the surrounding neighborhoods that escaped the disease.

### Principle 2 — Make quantitative comparisons

The workhouse case provides the clearest quantitative argument: 535 inmates surrounded on three sides by streets with heavy cholera mortality, yet only 5 died — because they had a separate water source. Snow calculated that if mortality had matched the surrounding streets, over 100 would have died. The map makes this comparison spatially visible; Snow's report makes it numerically explicit.

### Principle 3 — Consider alternative explanations and contrary cases

Snow investigated every death that appeared far from the Broad Street pump and explained each one: a child who attended school near the pump, a cabinet-maker who worked on Broad Street, a widow in West End whose son arranged a daily delivery of Broad Street pump water because she preferred its taste. Each apparent counter-case, on investigation, confirmed the theory rather than weakening it.

Tufte argues in *Visual Explanations* (p. 32) that analytic credibility depends on engaging all the evidence — not just the data that supports the preferred explanation. The goal is accuracy, not advocacy: apparent puzzles and inconsistencies belong in the analysis, not beneath it.

### Principle 4 — Assess possible errors in the reported numbers

Snow documented data limitations explicitly — patients who died in hospitals after moving, addresses not registered, cases he could not confirm. He argued these gaps would be distributed proportionally across the outbreak area and therefore would not bias the map's main conclusion. Acknowledging error is not weakness; it demonstrates analytic integrity.

### The pump-handle myth — audit the retelling (pp. 33–34)

The most retold element of Snow's story — the handle removal of September 8 — is its weakest-evidenced part: the daily death series shows the epidemic already in steep decline, and Hill's verdict is that the epidemic's end was *not* dramatically determined by the removal. The minimum defensible claim is that removal prevented a recurrence; a competing explanation ran simultaneously — population flight emptied the pool of victims. Richardson's dramatic account that "the plague was stayed" shows how retellings convert an equivocal intervention into a founding causal myth. Feinstein's methodological summary: a non-randomized intervention, historical controls, an equivocal time relationship — and Snow was still exactly right about waterborne transmission. Audit the retelling, not just the chart.

### Reproduction degradation of the map (p. 35)

The original is an awkward 40-cm square, and reproductions have steadily eroded its evidence: some facsimile editions reprint only the text, dropping the crucial visual evidence entirely; textbook redrawings leave the workhouse and brewery unlabeled, reducing the essential compared-with-what cases to mysterious cholera-free zones. Tufte's norm: graphical standards routinely slip below verbal and tabular standards, yet all representations are evidence and owe identical integrity.

---

## §4. The Challenger Failure: Thinking Causally but Not Displaying Causally

The engineers at Morton Thiokol who opposed the Challenger launch had the correct causal theory: low temperature degrades O-ring resiliency, which risks catastrophic joint failure. They were right. Their 13 charts failed to communicate this because the charts were not designed to display a causal relationship.

Tufte's verdict in *Visual Explanations* (p. 44) is precise: the engineers had reached the correct conclusion and held the right causal theory, but their thirteen charts organized the data in ways that made the temperature-damage relationship invisible. They were thinking causally without displaying causally.

### The specific failures — 13 pre-launch charts, then post-accident commission displays

Two families of displays failed, at different times, and conflating them is itself an evidence error. Tufte separates them explicitly: the six principles were violated in the 13 pre-launch charts as well as in the post-launch 48-rocket display (p.52).

**Pre-launch (the 13 charts faxed to NASA, January 27, 1986):**

**Failure mode 1 — Anonymous authorship (p.40).** The title chart, "Temperature Concern on SRM Joints," named no individual authors or preparers — responsibility diluted, no one standing behind the analysis.

**Failure mode 2 — Three names for one rocket (p.40).** The charts switched among NASA flight number (61-A), Thiokol motor number (SRM no. 22A), and launch date for the same booster, forcing viewers to perform cross-chart record-linkage in their heads. A causal display spanning multiple views must key every observation to one stable identifier.

**Failure mode 3 — Anecdote in place of evidence (p.42).** The blow-by history chart rested the temperature case on two flights: SRM 15 at 53°F (substantial erosion plus blow-by) against SRM 22 at 75°F (blow-by only). It invited the fatal rebuttal — "We had blow-by on the hottest motor and on the coldest motor" — making temperature appear irrelevant; with only two cases, no statistical statement about cause and effect was possible, and erosion, the graver damage mode, was sidelined.

**Failure mode 4 — Fragmented outcome measure (p.41).** O-ring damage was scattered across six descriptive types — erosion, soot/blow-by, depth, location, extent, view — stupefying fragments with no overall severity measure. Tufte's damage index (fn.36, p.44), a severity-weighted composite per launch, is what later makes a single y-axis possible; constructing a defensible outcome index is part of causal display design.

**Failure mode 5 — Selective data (p.43).** The History-of-O-ring-Temperatures chart reported two developmental motors (DM-4, DM-2), two qualifying motors (QM-3, QM-4), and the two launches with blow-by (SRM-15, SRM-22). Missing: 92% of temperature data, covering 5 flights with erosion and 17 flights without damage. The chart defined the database for the decision.

Tufte observes in *Visual Explanations* (p. 43) that every display of evidence silently defines what counts as relevant — the presented data is always a selection from a larger pool. The choice of what to include is as consequential as the data itself.

**Post-accident (evidence prepared for the presidential commission, pp.46–47):**

**Failure mode 6 — Wrong ordering.** The 48-rocket iconographic chart arranged launches in temporal sequence. The causal variable, temperature, appeared only as small numbers written sideways. Any viewer trying to assess temperature-damage correlation had to mentally extract and re-sort 48 numbers while reading across two sequentially projected slides.

**Failure mode 7 — Disappearing legend (p.47).** The damage-severity code used on the 9-rocket chart vanished when that chart was replaced by the 48-rocket chart on the overhead projector at the hearings. Viewers had to memorize the code across slides to read the damage values on the full chart.

**Failure mode 8 — Chartjunk obscuring the signal.** The outline shapes of 48 little rockets dominated the visual field. The marks encoding actual data were small, opaque, and scattered inside the rocket silhouettes.

**Failure mode 9 — Defensive caveats, or CYA notices (pp.46–47).** The post-accident charts carried legalistic, self-protective disclaimers. A display that needs an oral escort or a lawyer's caveat to be read is advocacy scaffolding, not evidence.

Tufte equates chartjunk with statistical incompetence, the visual analog of muddled writing — invoking Ben Jonson's observation that a mind is out of tune when its words jar and a reason out of frame when its sentences are preposterous (*Visual Explanations*, p. 48).

> "A lack of visual clarity in arranging evidence is a sign of a lack of intellectual clarity in reasoning about evidence."
> — Tufte, *Visual Explanations*, p. 48

### What the correct display would have shown — and its provenance

A complete scatterplot of all 24 previous launches — O-ring damage index, 0–12, on the y-axis (the severity-weighted composite of fn.36, p.44) vs. temperature at launch on an x-axis running 25°–85°F, with the 26°–29°F launch-day forecast range marked as a labeled band on the extended axis — makes the relationship visible in seconds:

- Every launch below 66°F resulted in damaged O-rings
- The coolest launch without damage was at 66°F
- The Challenger forecast of 29°F was 5.7 standard deviations below the mean launch temperature
- 29°F was 37°F colder than any previous undamaged launch

Tufte's corrected scatterplot in *Visual Explanations* (p. 45) — plotting all 24 pre-Challenger launches by temperature and O-ring damage index — makes the risk visible at a glance: every launch below 66°F had damaged O-rings, and the Challenger's 26°–29°F forecast falls far beyond the range of any prior flight.

**Display provenance (fn.39, p.46).** The famous damage-vs-temperature scatterplot most books reproduce as "the chart the engineers had" is itself post-hoc: two commission staff members drew it after the accident as a simulation of the pre-launch reasoning. It was never faxed, never seen before launch, and implies an analysis of 7 flights at 7 temperatures that no one performed — pre-launch, only two blow-by cases were ever tied to temperature. When retelling an evidence failure, verify which displays existed at decision time; a post-hoc reconstruction is evidence that must itself be documented.

**The evidential counterfactual (pp.39, 52).** This was Thiokol's only no-launch recommendation in 12 years, made against intense schedule and political pressure — a presidential State of the Union address was scheduled hours after launch. Tufte's judgment is that those pressures would likely not have prevailed over a clear, credible display of all the evidence. The display's failure mattered precisely because a strong display is the instrument that resists ambient pressure.

---

## §5. Named Failure Modes

| Failure mode | Description | Example |
|---|---|---|
| **Control omission** | Showing only cases, not non-cases; omitting the comparison baseline | Pre-launch evidence never assembled the 17 undamaged (warm) flights |
| **Temporal displacement** | Organizing by time when the causal variable is not time | Rockets ordered by launch sequence, not temperature (post-accident 48-rocket chart, pp.46–47) |
| **Selective database** | Defining the dataset to include only data consistent with advocacy position | Temperature chart: 2 developmental + 2 qualifying motors + 2 blow-by launches; 92% missing (p.43) |
| **Unstable identifiers** | Naming the same unit differently across views, forcing mental record-linkage | 61-A / SRM no. 22A / launch date for one booster (p.40) |
| **Fragmented outcome measure** | Splitting the effect into descriptive shards with no composite severity index | Six damage types, no overall measure (p.41); fixed by the damage index (fn.36, p.44) |
| **Defensive caveat (CYA notice)** | Display carries self-protective disclaimers requiring an oral escort | Post-accident commission charts' legalistic notices (pp.46–47) |
| **Anecdote substitution** | Using 1-2 cases as if they establish cause and effect | Blow-by on SRM 15 and SRM 22 only; n = 2 |
| **Iconographic corruption** | Using decorative pictorial units that resist proportional measurement | 48 little rockets with damage coded as opaque interior marks |
| **Disappearing legend** | Calibration code visible on one slide, gone on the next | Damage severity scale present on 9-rocket chart, absent on 48-rocket chart |
| **Temporal aggregation artifact** | Choosing time-interval boundaries that manufacture or destroy a signal | Weekly cholera bins (Sept 1–7 vs 8–14) make pump-handle removal look decisive; daily data show no break |
| **Spatial aggregation artifact** | Choosing area boundaries that hide or relocate a geographic cluster | Monmonier's re-partitions of Snow's deaths erase the Broad Street cluster; deadliest areas exclude the pump |
| **Specification searching** | Sifting many aggregations/models and reporting only the favorable one (multiplicity) | One chosen chart presented as if it were the only analysis run |
| **One-glass experiment** | Demonstrating an effect without a controlled comparison | Feynman's O-ring in ice water: no dry O-ring shown alongside, cause (cold vs. wet vs. clamped) unresolved |
| **Mechanism without quantification** | Naming the mechanism but not linking it measurably to the outcome | Charts show O-ring rotation physics but do not connect rotation magnitude to temperature |
| **Extrapolation without acknowledgment** | Plotting a recommendation (53°F minimum) based on a sample of one without stating the inference problem | 53°F line drawn from SRM 15 alone |

---

## §6. The Six Dual Principles for Causal Display Design

Tufte closes the chapter with six principles that apply equally to statistical reasoning and to display design. They are paired because the design should recapitulate the analysis.

In *Visual Explanations* (p. 53), Tufte frames the governing principle: display design and statistical reasoning are not separate disciplines — both must obey the same logic of evidence. When seeing and thinking operate on the same principles, graphic clarity and analytic clarity become the same thing.

| Principle | What it means for display design | What it means for reasoning |
|---|---|---|
| **1. Document sources and data characteristics** | Label data provenance, sample size, collection method on the display | Know where every number came from and what errors are possible |
| **2. Enforce appropriate comparisons** | Place cause and effect on the same display; show baseline and treatment | Ask "compared with what?" before drawing any conclusion |
| **3. Demonstrate mechanisms of cause and effect** | Show the causal pathway visually, not just the correlation | Have a theory of why the cause produces the effect |
| **4. Express mechanisms quantitatively** | Use scaled axes; mark the magnitude of effect, not just its direction | Quantify how much the cause changes the effect, not just whether it does |
| **5. Recognize the multivariate nature of problems** | Do not reduce to a single variable when confounders exist; consider population density, alternative sources | Identify all plausible competing causes before concluding |
| **6. Inspect and evaluate alternative explanations** | Include contrary cases on the display; do not select only confirming data | Seek the disconfirming case as hard as the confirming one |

---

## §7. Applying Snow's Method — Practical Checklist

Before finalizing any display intended to support a causal claim:

- [ ] **Does the display include the non-cases?** Every display of damage, illness, or failure needs the undamaged, healthy, or successful comparison group on the same graphic.
- [ ] **Is the causal variable the organizing axis?** If you suspect X causes Y, X should be the horizontal axis, not time, not sequence number, not alphabetical order.
- [ ] **Is the full dataset shown?** List what data exists and what fraction appears in the display. If less than 100%, state why.
- [ ] **Are contrary cases investigated and reported?** The two or three data points that do not fit the pattern need explicit explanation on the display or in adjacent annotation.
- [ ] **Is the proposed intervention temperature / dose / quantity shown at its actual value on the axis?** The Challenger argument required seeing 29°F on the same axis as 53°–81°F. Without that extension the extrapolation is invisible.
- [ ] **Can the display be read without an oral explanation?** If a caveat says "cannot be considered complete without the oral discussion," the display is not a display — it is a prop for advocacy (a "CYA notice," pp.46–47).
- [ ] **Are all aggregation choices tested for sensitivity?** Daily, weekly, monthly groupings of the same data should tell the same story. If they do not, show the detailed data.

---

## §8. Feynman's Demonstration as Counter-Example

Feynman's ice-water O-ring experiment at the presidential commission hearing became a media sensation but committed the same error as the 13 charts: it was an uncontrolled demonstration, not an experiment.

Tufte notes in *Visual Explanations* (pp. 51–52) that the single-glass demonstration is inconclusive: it cannot separate whether the O-ring lost resiliency due to cold temperature, mechanical clamping, or simple contact with water. A controlled comparison — two O-ring samples, identical clamping, one glass at 32°F and one at room temperature — is required to isolate the variable.

The one-glass method is an experience, not an experiment. It evokes the well-known connection but does not establish its magnitude or isolate its cause. A correct design: two O-rings, two glasses, identical clamping duration, same rubber material, one at 32°F and one at 70°F, both released simultaneously. Only then is the question "Compared with what?" answered.

This applies to all demonstrations and "proof of concept" displays: a single evocative example is never sufficient evidence for a causal claim, regardless of its rhetorical power.

---

## §9. Feynman's Summary Principle

> "For a successful technology, reality must take precedence over public relations, for Nature cannot be fooled."
> — Richard Feynman, quoted in *Visual Explanations*, p. 53

Applied to display design: a graphic that persuades by concealing the full evidence is not a successful display, even if it wins the argument in the room. The Thiokol engineers' charts failed not because they were deliberately dishonest, but because the designers did not impose the discipline of showing all the data in the right order. The discipline is not optional when the decision has irreversible consequences.

---

## Cross-book notes

- *Seeing with Fresh Eyes* (p.80): Tolstoy's account of Napoleon "commanding" — thousands of consecutive, mutually dependent orders, of which history remembers only the few that happened to be executed — is a compact image of causal-selection bias: surviving records over-represent the causes that "worked."
- *Beautiful Evidence* (p.163): the Columbia debris analysis had a simple causal skeleton — debris kinetic energy, plus strike location on a wing of varying vulnerability, yields threat level during re-entry heating — and the slide format still obscured it. Format can defeat even a short causal chain.
- *Beautiful Evidence* (p.142): the data-side counterpart of the passive voice. Data mining, factor analysis, and multidimensional scaling grind large matrices into small lumps without testing any causal model — machinery for analysts holding a lot of data and no ideas. Whatever comes out of such crunching still has to be turned into evidence about a causal process before it can support a decision.
- *Beautiful Evidence* (p.143): **one bullet list, three incompatible causal architectures.** A three-point strategic plan (raise market share 25%, raise profits 30%, raise new-product introductions to ten a year) is equally consistent with market share driving profits which fund new products; with new-product development raising market share and profits at once; and with windfall profits buying market share through advertising and new products. The bullets state outcomes and suppress the mechanism that distinguishes the three, so the display cannot tell anyone what to do. Tufte's remedy is an audit procedure: sketch the causal model the analysis implies, draw the arrows, label the alleged causes and effects, decide what each arrow is supposed to mean — the work the presenter should have done first.
- *The Visual Display of Quantitative Information* (pp.74–75): the Connecticut speeding-crackdown charts are the compact teaching case for control series. A two-point before/after fatality comparison makes the crackdown look decisive; the full 1951–1959 series shows 1955 was a local peak, and Tufte then draws several alternative surrounding time-paths that would license entirely different readings of the same 1955–56 drop. Adding the neighboring states (Massachusetts, Rhode Island, New York) gives the better context: the decline was not unique to Connecticut. Same lesson as Snow's brewery and workhouse — an intervention chart is only as good as the controls drawn on it.

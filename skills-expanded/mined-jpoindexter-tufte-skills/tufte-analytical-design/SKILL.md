---
name: tufte-analytical-design
description: "Use when designing, reviewing, or defending an evidence presentation — a report, dashboard, scientific figure, policy brief, or technical display — and a standard is needed for whether it assists reasoning; when arguing that a design choice follows from the intellectual task rather than from a template or tool; or when working through Minard's 1869 map as a reference implementation."
tags: [tufte, data-visualization, analytical-thinking, evidence, information-design, principles]
---
# Tufte: Principles of Analytical Design

## Overview
Analytical design is design in service of reasoning. Tufte's six principles, derived from Minard's 1869 map of Napoleon's Russian campaign, define what separates displays that assist thinking from those that merely perform it. The core claim: design principles are not arbitrary aesthetic choices — they are derived directly from the cognitive tasks required to reason about evidence. A presentation that violates these principles is not just ugly; it impairs thinking.

> **Naming convention:** Failure-mode labels in this skill (Floating Fact, Forced Flatland, Mode Segregation, etc.) are descriptive teaching names, *not* Tufte's own terminology. Only quotes and page-cited phrasings reflect his exact words. Use the labels for diagnosis; don't attribute them to Tufte.

---

## §1. The Grand Principle: Design Follows Thinking

The source of all six principles is one meta-principle:

> "The principles of analytical design are derived from the principles of analytical thinking." — Tufte, *Beautiful Evidence*, p. 137

Cognitive tasks drive design decisions. If the intellectual task is comparison, show comparisons. If the task is causal reasoning, show causal structure. This is not a metaphor — it is the literal derivation rule for every choice in information display.

**Consequence for practice:** Before any design decision, name the intellectual task. The design choice follows from that, not from brand guidelines, template defaults, or what looks impressive. Tufte prescribes that every design process begin by naming the task the display must serve: *what does a reader need to do with this information?* That question drives which elements to include, how to structure them, and which technologies to employ.

### Why the principles are universal (pp. 137–139)

The principles are not tied to a medium, a tool, or an era. Because they come from how humans reason rather than from any technology, they hold across the entire history of evidence display:

- **Across time:** the same rules govern the earliest known maps — scratched into stone roughly 6,000 years ago — and paper, print, screens, and whatever comes next. Tufte's claim is that a principle derived from analytical *thinking* cannot expire when the production technology changes.
- **Across minds:** the principles would apply even to a hypothetical non-human or alien intelligence presenting evidence, because any reasoning agent must still compare, explain causality, handle many variables, integrate modes, document, and care about content.
- **Producer/consumer symmetry:** the same principles bind the maker of a display and its reader — both are doing the same reasoning. As Tufte puts it, on questions of analytical quality, "we're all in it together." There is no separate, lower standard for "just presenting."

**Practical upshot:** never excuse a weak display with "it's only a slide / a dashboard / a draft." The standard is set by the reasoning task, which is identical regardless of tool or audience.

### Analytical vs. Decorative Design

| Dimension | Analytical Design | Decorative / Presentation Design |
|---|---|---|
| First question | "What content tasks must this display help with?" | "How can this presentation look good?" |
| Evidence modes | Integrates words, numbers, images freely | Segregates modes into slides, tables, figures |
| Multivariate depth | Shows 6+ variables simultaneously when data demands | Strips to 1–2 variables for "clarity" |
| Comparison | Makes comparisons explicit and visible | Leaves comparisons implicit or verbal |
| Causality | Shows mechanism, not just correlation | Shows effects without agents or causes |
| Documentation | Names authors, sources, scales, assumptions | Omits provenance; sources buried in footnotes |
| Driving force | Content — the substance being explained | Production technology, templates, brand |
| Test of success | Does it assist thinking about the evidence? | Does it look polished and professional? |

---

## §2. The Six Principles

### Two epigraphs that frame the principles (p. 122)

Tufte opens the principles with two quotations that set up the whole chapter:

- **Durkheim, on the categories of understanding.** Durkheim held that human reasoning rests on a small set of fundamental categories — among them **time, space, number, and cause**. Tufte's point: these are exactly the native categories analytical design must serve. The six principles are, in effect, instructions for displaying time, space, number, and cause well.
- **Matisse, on difference.** > "I do not paint things, I paint only the differences between things." — Matisse. This frames Principle 1: the unit of meaning is the *contrast*, not the isolated object. A display communicates by showing differences.

These two anchors map onto the principles: Durkheim's categories say *what* to show (number, time, space, cause); Matisse says *how* meaning arises (through comparison).

---

### Before the design analysis: the scale of the content (p. 126)

Start any Minard walkthrough with the numbers, not the design. They are what make Principle 6 ("content counts most") concrete rather than pious.

- The 1812 campaign's total toll, French and Russian combined, was roughly **700,000 to 1,000,000 dead**.
- Of the 422,000 who crossed into Russia, about **100,000 reached Moscow** — a city by then sacked, deserted, and burning. Minard draws only the *departure* from Moscow, as the dark lower line.
- **E. J. Marey** (*La méthode graphique*, 1878) described the map's effect as a brutal eloquence that seems to defy the historian's pen. Tufte uses this as the framing claim for why the graphic outperforms the prose account of the same events.

**Practical upshot:** the reason to study this map is not that it is pretty at six variables. It is that a single sheet carries a scale of catastrophe that narrative prose reports without conveying. Establish the magnitude first; then ask what design decisions made it legible.

---

### Principle 1: Comparisons (p. 127)

**State it as:** *make comparisons, contrasts, and differences explicit and visible.*

The central question of all statistical reasoning is: **compared with what?** Across every form of statistical work — time series, regression, experiment design, database analysis — the central act is answering that question. Every analytical method is, at bottom, a comparison method. The display must make the comparison visible, not leave it implicit.

**Minard at the Niemen — read the ratios carefully:**
- **Survival ratio:** ~**1 in 42** — about 10,000 of the 422,000 who crossed into Russia returned (10,000 ÷ 422,000 ≈ 1/42).
- **As actually drawn:** Tufte notes (p. 127) the two band widths at the Niemen were drawn in a ratio of roughly **1 in 28**, *not* a strict 1-in-42. The graphic encoding is approximate at that crossing, not perfectly proportional. Don't claim the line widths literally *are* the 1:42 survival ratio — the survival ratio is the fact; ~1:28 is what the ink shows.

Either way, the width of two lines communicates a six-month, hundreds-of-miles catastrophe that no single number conveys.

**Do / Don't pairs:**

| Do | Don't |
|---|---|
| Show before/after states in the same visual field | Show only the current state without baseline |
| Provide a reference class or control condition | Report absolute numbers without context |
| Let scale encode magnitude of difference | Use color alone to signal "different" |
| Use small multiples for sequence comparisons | Animate sequentially so no two states are visible at once |
| Place comparanda adjacent or overlapping | Separate comparanda across slides or pages |

**Failure mode — Floating Fact:** a number presented with no comparison reference ("sales were $4.2M"). The reader can't assess significance, trend, or deviation because the baseline was never provided.

---

### Principle 2: Causality, Mechanism, Structure, Explanation (p. 128)

**State it as:** *show causality, mechanism, explanation, and systematic structure.*

Causal thinking is not optional in serious analytical work. Scientific inquiry is structured by causal laws; medical reasoning about prevention, diagnosis, and intervention requires causal models; policy and reform require knowing which causes to govern — policy decisions *are* causal decisions about which lever to pull. Displays that show only effects, without causes, cannot support the reasoning they exist to enable.

**Tufte's named authorities for the principle (p. 128):**
- **Robert Dahl**, "Cause and Effect in the Study of Politics" (1965): thinking about policy is, and has to be, thinking about causality. The claim that policy decisions *are* causal decisions is Dahl's, and should be cited as such rather than asserted.
- **Rudolf Virchow**, *Die Medizinische Reform* (1848), quoted on p. 128: medical statistics will be the standard of measurement — weigh life for life and see where the dead lie thicker, among the workers or among the privileged. One sentence, and it demonstrates that a **comparison is already a causal argument**: the class difference in mortality is both the measurement and the accusation.
- Tufte's connective claim: measurements are inherently comparative, and comparisons promptly provoke reasoning about the sources of difference and variability. Principle 1 therefore feeds Principle 2 mechanically — you do not add causality to a comparison as a second step; a well-posed comparison already demands a causal account.

**Minard's causal analysis is thin — and Tufte says so (p. 129).**

This is the part most retellings of the map get backwards, so state it carefully. The temperature graph along the bottom is a *reminder of intense cold*, dated at each point, and it reads as though it explains the deaths on the retreat. Tufte's own verdict is that the map's causal analysis is weak: the retreating army's path loosely parallels the falling-temperature line, but that **symbolic parallelism carries no evidential value**. Two curves descending together is not a mechanism, and the map contains nothing that rules out the alternatives — attrition, starvation, disease, desertion, pursuit.

Where does the causal link actually live? In the **five historical sources** Minard names (see Principle 5), not in the graphic. The map *gestures at* mechanism and points to where the argument was made; it does not itself make it.

| Read the map as… | Verdict |
|---|---|
| A demonstration that cold caused the deaths | Wrong — parallel curves are not evidence; Tufte rejects this reading |
| A display that *includes* the variable a causal account would need, and cites the sources that argue it | Correct, and the more useful teaching point |

**Why this is the better lesson.** The best-known analytical graphic ever made shows a causal variable *without* establishing causation — which is exactly the trap most dashboards and charts fall into. Plotting the suspected cause alongside the outcome is a necessary first move and a wholly insufficient last one. If your display's causal claim rests on two lines moving together, you have Minard's weakness without Minard's five sources.

**Do / Don't pairs:**

| Do | Don't |
|---|---|
| Show agents (who or what acts) with arrows or flow lines | Use passive-voice structures that suppress the agent |
| Include the causal variable even if it adds complexity | Strip to the dependent variable only, for "simplicity" |
| Draw causal diagrams: A → B → C | Show outcomes with no link between them |
| Distinguish correlation from mechanism explicitly | Imply causation from co-occurrence |
| Name the mechanism in the title or annotation | Leave causation buried in the verbal text |
| Cite where the causal argument was actually made, as Minard cites his five sources | Let two parallel curves stand in for a mechanism (Minard's own weakness, p. 129) |

**Failure mode — Effects Without Causes:** a display reports outcomes — what happened — with no agent, mechanism, or sequence. Location without cause; result without actor. The reader cannot reason about *what to do* because there is no causal model to act on. (For the specific corruption-chapter cases — agentless strategic-plan bullet lists and anti-causal statistics — see **§7**.)

---

### Principle 3: Multivariate Analysis (p. 130)

**State it as:** *show multivariate data — more than one or two variables at once.*

Minard's single map encodes **6 variables**: army size (band width), geographic position (2 dimensions, x and y), direction of march, temperature, and date. None of the interesting worlds — physical, biological, human — is bivariate. Reducing to 1 or 2 variables to fit a format is not simplicity; it falsifies the subject's actual complexity.

Two-dimensionality is a constraint of the medium, not of the subject. Presentation technology that enforces flatness trains analysts to think flatly. Because real phenomena are inherently multivariate, showing multiple variables at once should be the **default — unremarkable, expected, routine** — not a special achievement.

**Techniques for escaping flatland:**
- Layering and separation (transparent overlays, cartographic layering)
- Small multiples (one panel per condition, all visible in one view)
- Encoding extra variables in size, texture, shape, annotation
- Integrating text and numbers directly into graphics
- Narrative flow-lines that carry several variables simultaneously

**Do / Don't pairs:**

| Do | Don't |
|---|---|
| Ask how many variables the phenomenon actually has | Default to a 2-axis chart without examining dimensionality |
| Use small multiples to add a 3rd or 4th variable | Animate to add a variable (animation hides comparisons) |
| Annotate data points with words that carry more data | Push extra variables into a legend that must be decoded |
| Show 6 variables in one display when content demands | Slice into 6 slides, each showing 1 variable |

**Concrete benchmark (from the source, p. 138):** physical and biological science journals (*Nature*, *Science*) publish statistical graphics with a **median of more than 1,000 numbers**; applied medical research (*The Lancet*) averages about **45 numbers per graphic**. High numeric density is the scientific norm; the low end is a presentation convention, not a content requirement.

**Why multivariate display is *required*, not impressive (p. 138).** Tufte concedes that social-science evidence lacks the replication guarantees of the physical sciences, citing Merton on unanticipated consequences, and he quotes **Bernard Berelson's** threefold summary of what social science reliably knows: *some do and some don't; the differences aren't very great; it's more complicated than that.* His medical illustration is the same shape — a treatment arm at **21% survival against 15% for controls**.

That calibration is the real argument for Principle 3. Real effects in human-scale domains are **small, confounded, and context-dependent**. A display stripped to one or two variables cannot distinguish a 6-point difference that is causal from one produced by case-mix, and it gives the reader no way to assess fit, variability, or alternative explanation. Showing many variables is not a display of analytical virtuosity; it is the minimum needed to reason honestly about marginal effects.

**Failure mode — Forced Flatland:** an inherently multivariate phenomenon (6+ variables) shown with only 1–2, so the appearance of simplicity conceals the real complexity. The reader can't assess fit, variability, outliers, or alternative explanations from the exposed slice alone. (Descriptive label — Tufte's own term for the flat-medium problem is "flatland.")

---

### Principle 4: Integration of Evidence (p. 131)

**State it as:** *completely integrate words, numbers, images, and diagrams.*

The evidence doesn't care what mode it arrives in. Segregating it by mode — all images in one section, all tables in an appendix, all text in the body — is organizational convenience that actively impairs reasoning. Maps, the best practice in analytical display, have always integrated multiple modes on a single surface. The distinctions between evidence *types* matter far less than their combined bearing on the question being investigated, so modes must be assembled where the evidence is needed, not where the production system finds them convenient.

Minard integrates a paragraph of words (title, legend, assumptions), a geographic map (spatial position), flow-lines (army size and direction), temperature data (cause), dates (time), and place names (context) — all within one surface measuring **62 × 30 cm, or 25 × 12 inches** (p. 122 caption; item 28 of Minard's *Tableaux Graphiques et Cartes Figuratives*, Bibliothèque de l'École Nationale des Ponts et Chaussées).

> **Dimension warning.** The frequently quoted **25 × 21 in (62 × 54 cm)** is *not* this map. That is the size of the **two-map lithograph sheet** of 1869 (p. 135), which carries the Hannibal map above and the Russia map below. Attaching the sheet's dimensions to the single map roughly doubles its stated area and quietly inflates every density claim made about it.

**The technique that makes integration physically possible (p. 131).** Minard drew the flow-band in a light, unsaturated **tan**, chosen so that the place-names and river lines underneath read *through* it rather than being covered by it. Tufte notes that roughly **20** of Minard's figurative maps use transparent overlays this way. The general lesson: integration on a crowded surface is not achieved by finding empty space for each mode — there is never enough — but by **layering and separation**, putting modes on different visual levels so they coexist without occlusion. Without that move, adding the flow-band would have destroyed the map beneath it, and Principle 4 would be unachievable in practice.

Galileo's annotated telescope drawings (1610) show the same move: he wrote observation time, satellite identity, and distance (in Jovian radii) directly onto each sketch, turning still drawings into credible quantitative evidence about satellite motion rather than mere pictures of what the telescope showed.

**Do / Don't pairs:**

| Do | Don't |
|---|---|
| Place labels directly on data points — words are evidence | Use letter codes keyed to a separate legend |
| Put the explanatory text with the graphic it explains | Collect figures into a "Figures" section at the back |
| Annotate a chart with the model equation that fits it | Describe the model in text, show the chart elsewhere |
| Use sparklines to embed data-lines inline with prose | Write "[see Figure 3]" and break the reading |
| Show the unmapped and mapped image in sequence | Force the reader to cross-reference between pages |

**Failure mode — Mode Segregation:** a report of all words, with tables appended at the back and images in an exhibit section. The reader must hold evidence from three locations in memory at once; the architecture fights comprehension.

**Failure mode — Single-mode Research:** an investigation that relies on exactly one kind of evidence (only statistics, or only memoirs, or only economic models) when the subject demands several. The question degrades from "how can this be explained?" to "how can *one type* of information explain this?"

---

### Principle 5: Documentation (p. 133)

**State it as:** *thoroughly describe the evidence — detailed title, authors and sponsors, data sources, complete measurement scales, and the relevant caveats.*

Documentation is quality control, not formality. Undocumented displays are inherently suspect; the presence of documentation signals that someone is taking responsibility for the analysis.

Minard's 1869 map documents all of this **on the face of the display**:

| Documentation item | Minard's answer |
|---|---|
| What is it about? | Losses in men of the French Army in the Russian campaign, 1812–1813 |
| Who did the work? | Drawn up by M. Minard |
| Who is that? | Inspector General of Bridges and Roads, retired |
| Where and when? | Paris, 20 November 1869 |
| Data sources? | 5 named sources (Thiers, Ségur, Fézensac, Chambray, and Jacob's diary) |
| Assumptions? | Troops of Prince Jérôme and Marshal Davout assumed always with the army |
| Scale (flow-lines)? | 1 millimeter = 10,000 men |
| Scale (map)? | Common leagues of France (Map of Fézensac) |
| Scale (temperature)? | Degrees of the Réaumur thermometer below zero |
| Publisher? | Named printer and publisher |

**Benchmark (from the source):** in 13 computer-science books on technical visualizations, only **20%** of images had complete scales and labels, and **60%** had no scales or labeled dimensions at all. Hubble Space Telescope public images are typically published with no indication of distance, size, or location.

**Do / Don't pairs:**

| Do | Don't |
|---|---|
| Name the author(s) — people, not agencies | Sign it "Marketing Department" or leave it unsigned |
| Name every data source explicitly | Write "data from internal records" |
| Show at least one measurement scale on every graphic | Leave the axis scale implied or omitted |
| State assumptions and their implications | Bury assumptions in a methodology appendix |
| Disclose sponsorship and conflicts of interest | Present findings as neutral with no funder named |
| Date the display | Present it with no temporal context |

**Failure mode — Anonymous Authorship:** corporate and government reports with no named individual author. The absence of names signals evasion of responsibility: when things go wrong, no one is findable. (For undefined units, gamed base years, and time-shifted numbers — corrupt *measurement* — see **§7**.)

---

### Principle 6: Content Counts Most of All (p. 136)

**State it as:** *analytical presentations ultimately stand or fall on the quality, relevance, and integrity of their content.*

This is the supremacy principle; it overrides the other five. No design technique, visual treatment, or technology can salvage a presentation built on weak, irrelevant, or corrupt content. Conversely, content important enough will be heard even through bad design. Minard's work, Tufte notes, exemplifies the spirit behind excellent analytical graphics: deep knowledge of the subject and genuine caring about the substance.

Minard never names Napoleon on a map of Napoleon's own march — a design choice that reinforces the content priority: memorialize the dead, don't celebrate the surviving celebrity.

**The biography behind the content (pp. 134–135).** Minard retired at 70 and produced roughly **50 maps** over the following 18 years. The Russia map was published in **November 1869, when he was 88** — the last sheet of his lifetime portfolio. He had himself been trapped in besieged **Antwerp in 1813**, during the same war. The map is an anti-war document made by someone with a personal stake in the subject, which is precisely Principle 6's claim: the design follows from caring about the content, and no technique substitutes for that.

**The sheet is a small multiple, not one map (p. 135).** The 1869 lithograph carries **two** flow-maps: **Hannibal's crossing into Italy** above (96,000 → 26,000 men) and **Napoleon in Russia** below. Treating the poster as a single map loses a built-in comparison across roughly **2,000 years** of the same phenomenon, drawn in the same visual language at the same scale of encoding. The parallel structure is itself the argument: armies are destroyed by campaigns in a recognizable way, and the reader can verify it by looking at both bands without leaving the sheet.

The most direct route to a better presentation is therefore stronger content, not a better visual container.

**Do / Don't pairs:**

| Do | Don't |
|---|---|
| Ask "is this worth showing at all?" before designing | Build the visual container before confirming the content earns it |
| Start from the substantive question to be answered | Start from the slide template or visual system |
| Cut content not directly relevant to the question | Pad with tangential data to look thorough |
| Know the subject deeply — content drives design | Delegate content selection to non-experts |
| Judge the design by whether it aids reasoning | Judge it by polish or technical sophistication |

**Failure mode — Chartjunk as Substitute:** decorative graphics, 3D extrusion, gradient fills, gratuitous color — visual elaboration that signals effort without adding evidence. The decoration is performing in place of the content.

**Failure mode — Technology-Driven Presentation:** choosing the display architecture from what the software supports ("how can this presentation use [the latest display technology]?") instead of what the evidence requires. The content question always comes first.

---

## §3. The Analytical vs. Decorative Distinction in Practice

Analytical design is the design of evidence presentations — scientific reports, dashboards, policy briefs, technical manuals, financial disclosures. Decorative / presentation design is the design of communications meant to persuade, brand, or market. They are not mutually exclusive, but their first principles differ:

| | Analytical Design | Decorative / Presentation Design |
|---|---|---|
| Audience task | Reasoning about evidence | Receiving a message or impression |
| Success criterion | Accurate, efficient inference | Persuasion, recall, aesthetic response |
| First question | What intellectual task must this support? | What impression should this convey? |
| Treatment of complexity | Show it — complexity is the subject | Reduce it — complexity fatigues the audience |
| Treatment of uncertainty | Show it — error bars, intervals, alternatives | Suppress it — uncertainty weakens the message |
| Integration of modes | Required — evidence crosses all modes | Optional — visual consistency dominates |
| Documentation | Required — credibility depends on it | Optional or counterproductive (disrupts flow) |

**The core test:** would a skeptical expert, given only the display, be able to assess the quality, provenance, and completeness of the evidence? Analytical design passes this test. Presentation design is not built for it.

---

## §4. Minard's Map as Reference Implementation

Charles Joseph Minard's 1869 *Carte Figurative* of Napoleon's Russian campaign is Tufte's primary exemplar because it satisfies all six principles at once in a single **62 × 30 cm / 25 × 12 inch** display (p. 122). It shares a **25 × 21 in (62 × 54 cm)** lithograph sheet with Minard's Hannibal map (p. 135) — the sheet's dimensions are not the map's.

| Principle | How Minard satisfies it |
|---|---|
| 1. Comparisons | 422,000 entering vs. ~10,000 returning — survival ratio ≈ **1:42** (bands as drawn at the Niemen ≈ **1:28**, p. 127); the Berezina crossing collapses ~50,000 to ~28,000 |
| 2. Causality | Temperature curve along the bottom, each point dated — but **partially**: Tufte judges the causal analysis thin, since the parallel between retreat and falling temperature has no evidential value; the causal argument lives in the five cited sources (p. 129) |
| 3. Multivariate | 6 variables: army size, geography (x, y), direction, temperature, date — all in one image |
| 4. Integration | Words (title, legend, annotations), numbers (troop counts at each location), flow-map diagram, temperature graphic, geographic map — fully fused |
| 5. Documentation | Author, role, place, date, 5 named sources, 3 measurement scales, stated assumptions |
| 6. Content | An anti-war image — Minard cared about the dead; the word "Napoleon" never appears |

Flow-line scale: **1 millimeter = 10,000 men** — the one number needed to read the whole map quantitatively. Note the distinction from §2: the survival *ratio* is ~1:42; the *drawn* band widths at the Niemen are ~1:28. The encoding is approximate there, not perfectly proportional.

---

## §5. Failure Modes Catalog

Source column distinguishes the analytical-design chapter (pp. 122–139) from the adjacent corruption chapter (pp. 140–155, see §7).

| Failure Mode | Principle Violated | Source | Diagnostic Signal |
|---|---|---|---|
| Floating Fact | 1 Comparisons | 122–139 | A number with no baseline, context, or reference |
| Effects Without Causes | 2 Causality | 122–139 | Outcomes with no agent, mechanism, or sequence |
| Forced Flatland | 3 Multivariate | 122–139 | 1–2 variables shown for a 6-variable phenomenon |
| Mode Segregation | 4 Integration | 122–139 | Tables in an appendix; "see Figure 3" in the text |
| Single-mode Research | 4 Integration | 122–139 | Only one evidence type for a multi-mode subject |
| Anonymous Authorship | 5 Documentation | 122–139 | No author, sources, scale, or date |
| Chartjunk as Substitute | 6 Content | 122–139 | Visual elaboration rising as content weakens |
| Technology-Driven | 6 Content | 122–139 | Design chosen by tool capability, not by evidence |
| Agentless Effects (strategic-plan bullets, passive voice) | 2 Causality | 140–155 | "Accelerate Revenue Recognition!" with no actor or mechanism |
| Anti-causal Statistics | 2 Causality | 140–155 | Data mining / factor analysis offered as explanation |
| Corrupt Measurement | 5 Documentation | 140–155 | Gamed base years, time-shifted or unadjusted numbers |

---

## §6. Application Checklist

Before shipping any analytical display, verify each principle:

- [ ] **Comparisons:** What is this explicitly compared to? Is the reference visible *in* the display?
- [ ] **Causality:** Does it show mechanism, or only correlation/co-occurrence? Are agents named?
- [ ] **Multivariate:** How many variables does the phenomenon actually have? Are fewer shown — and why?
- [ ] **Integration:** Are words, numbers, images, diagrams assembled where the evidence is needed, or segregated by mode?
- [ ] **Documentation:** Are author(s), sources, scales, date, and material assumptions visible on the display itself?
- [ ] **Content:** Would a skeptical expert find the content substantively adequate? Is this worth showing at all?
- [ ] **Universality:** Have you excused weakness with "it's only a slide/dashboard"? The standard is set by the reasoning task, not the tool (§1).

---

## §7. Corruption in Evidence Presentations (adjacent chapter, pp. 140–155)

These cases come from the chapter that *follows* the six principles, not from the principles chapter itself. They are included because each is a canonical, real-world inversion of a specific principle — useful for diagnosis, but cite them to pp. 140–155, not to the principle's own page. (The chapter runs pp. 140–155: epigraphs on p. 140, text 141–155. The anti-causal material sits at 142–143 and 146; the secondary-presentation bureaucracies and the rage to conclude at 154–155. The corrupt-*measurement* catalog — undefined units, tendentiously chosen base-years, excessively short time-series, unadjusted money, time-shifting such as premature revenue recognition — is not in that chapter at all: it sits at **p. 133**, inside Principle 5 itself; p. 143 carries only excessively accelerated recognition of revenue as a bullet-list example.)

| Corruption | Inverts | Diagnostic signal |
|---|---|---|
| **Agentless effects** | 2 Causality | Bullet-list strategic plans ("Accelerate Revenue Recognition!") and passive-voice prose (e.g. the 9/11 Commission style) assert outcomes with no actor, action, mechanism, or sequence. Identical-looking bullets can hide radically different causal structures, so the display can't help anyone decide what to do. |
| **Anti-causal statistics** | 2 Causality | Data mining, factor analysis, and multidimensional scaling crunch a data matrix without testing any causal model — a pile of effects with no causes behind them. Fine for exploration; dangerous when presented as explanation. |
| **Corrupt measurement** | 5 Documentation | Undefined or imprecise units, tendentiously chosen base years, time-shifting of data (e.g. premature revenue recognition), and inflation-unadjusted money. These are documentation failures before they are dishonesty — the scale, timing, or definition is undisclosed or gamed. |

**Rule of thumb:** corruption is what principle-violation looks like once *incentive* enters. The fix is the same as the principle's fix — name the agent, test the model, disclose the scale — applied against someone who benefits from the fog.

Source book: *Beautiful Evidence* (Cheshire, Connecticut: Graphics Press, 2006)
Relevant chapters: Ch. 5 — "Corruption in Evidence Presentations" is the adjacent chapter at pp. 140–155; the six principles are Ch. 4, "The Fundamental Principles of Analytical Design," pp. 122–139. Minard material also appears in *The Visual Display of Quantitative Information*, pp. 40–41, 176.

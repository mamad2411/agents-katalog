---
name: tufte-evidence-corruption
description: "Use when auditing an evidence presentation, research report, press release, or repackaged summary for corruption — passive-voice effects without causes, cherry-picked or culled data, model-search shopping, punning and overreaching claims, chartjunk, or a rage to conclude — and when deciding how much to trust a secondary or tertiary account of primary evidence."
tags: [tufte, evidence, cherry-picking, analytical-communication, data-presentation, research-integrity]
---
# Corruption in Evidence Presentations: Effects Without Causes, Cherry-Picking, Overreaching, Chartjunk, and the Rage to Conclude

## Overview

Making a presentation is a moral act as well as an intellectual activity. *Beautiful Evidence* ch. 6 catalogs corrupt presentation techniques that are "enemies of the truth, that corrupt reasoning, that produce unbeautiful anti-evidence." The five named corruption types — effects without causes, cherry-picking, overreaching/economisting, chartjunk, and the rage to conclude — range from subtle language choices (passive voice) to systematic research design failures (poor controls) to organizational pathologies (bureaucracies of secondary presentation). Each has a concrete detection method. The chapter draws on the 9/11 Commission Report, the Chalmers portcaval shunt study, Galenson's art history book, and the evidence reduction chain to show how corruption operates at every stage from data collection to published report.

---

## §1. Effects Without Causes and the Evasion of Responsibility

### The 9/11 Commission: Passive Voice as Corruption

The opening case is the *Report of the 9/11 Commission* (2004), p. 265, describing security lapses that may have allowed the attacks. The passage Tufte examines lists seven distinct failures — domestic agencies never mobilized, no direction or plan was established, borders were not hardened, transportation systems were not fortified, electronic surveillance was not targeted at domestic threats, state and local law enforcement were not marshaled to augment the FBI, and the public was not warned. Every failure is rendered in passive voice throughout.

Tufte's verb count from this passage:

| Verb type | Count | Subject |
|---|---|---|
| Passive verbs | 5 | None named |
| Active verbs | 3 | "domestic agencies" (vague) |

Result: **no agent is named**. Exactly *who* did not make a plan, *who* failed to warn the public, *who* failed to augment the FBI's efforts — these questions go unanswered. Thomas Powers noted in *The New York Review of Books* (Sept. 23, 2004): "These things that were not done must have been not done by somebody, and the somebodies reporting to him."

> "By means of the passive voice, the 9/11 Commission evades attributing responsibility for security lapses."
> — *Beautiful Evidence*, p. 142

### Passive Voice as the Structural Source of Effects Without Causes

The deeper problem is not just political evasion but analytical failure. Tufte argues that while passive voice is a legitimate writing technique, it also enables *effects without causes* — what he calls an "immaculate conception" of analysis. Describing ends without means, agency without agents, and actions without actors undermines the causal clarity that good reasoning requires.

The logic of decisions is "If we do such-and-such [cause], then we hope this-and-that will happen [desired effect]." The logic of responsibility requires the active voice: *someone did* or *did not do* something. Effects without causes are not just rhetorical — they disable the causal thinking required to make decisions, assign accountability, or implement remedies.

Anti-causal statistical methods work the same way: data mining, factor analysis, and multidimensional scaling crunch vast data matrices without testing causal models. They generate effects from nowhere.

### Bullet Lists Collaborate with Effects Without Causes

The bullet-list format compounds the problem. Mission statements and strategic plans are the characteristic venue:

> **Accelerate The Introduction Of New Products!!!**
> **Accelerate Revenue Recognition!!!**

Better to say *who* will accelerate, and *what, how, when,* and *where* they will accelerate. The sentence — with subjects, predicates, nouns, verbs, agents and their effects — is the effective methodology for causal statements. *Harvard Business Review* (Shaw, Brown, and Bromiley, 76, May-June 1998):

> "Bullets leave critical assumptions about how the business works unstated."
> — quoted in *Beautiful Evidence*, p. 143

A bullet list showing "Increase market share by 25% / Increase profits by 30% / Increase new-product introductions to ten a year" conceals whether market share produces profits or profits fund product development or product development produces both. All three causal structures fit the same three bullets:

```
Market share → Profits → New-product development
New-product development → Market share + Profits
Profits → New-product development → Market share
```

> "It follows that more complex and realistic multivariate causal models are way over the head of the simplistic bullet-list format."
> — *Beautiful Evidence*, p. 143

**Do/Don't pair — causal accountability:**

| Do | Don't |
|---|---|
| Name the specific agent responsible for each decision or inaction | Use passive constructions that float effects without causes |
| Write sentences with subject + predicate + named agent | Use bullet lists for plans that require causal structure |
| Ask: who did this? who decided this? who is responsible? | Accept "agencies failed to act" without naming the agencies and individuals |
| Draw explicit causal diagrams with arrows for any plan or strategy | Present multi-step causal chains as parallel bullet points |

---

## §2. Cherry-Picking, Evidence Selection, and Culled Data

### The Core Problem

Tufte identifies cherry-picking — the selective presentation of only favorable evidence while suppressing disconfirming data — as the most widespread and serious obstacle to learning the truth from any evidence-based report.

Van Wyck Brooks captured the mechanism: "It is a principle that shines impartially on the just and unjust that once you have a point of view all history will back you up." Cherry-picking is epidemic precisely because it is often invisible — the audience cannot see what was omitted.

A clear sign of cherry-picking: **a report appears too good to be true**, provoking the response "It's more complicated than that." A *series* of reports, however, can decisively reveal corrupt practices — just as consistently positive quarterly earnings that land exactly one penny above forecast, when this occurs across 20% of all corporations, signals systematic manipulation.

### The Evidence Decay Cycle

In medical research the pattern is structural and measurable. Tufte observes that the first published study on a new treatment tends to show the strongest positive result it will ever achieve. As investigators follow up with better-controlled studies — less susceptible to researcher enthusiasm and sponsor influence — reported efficacy consistently declines. By the time gold-standard randomized trials are conducted, the only remaining question is sometimes whether the treatment causes harm (*Beautiful Evidence*, p. 144).

**Evidence Decay Cycle pattern:**
1. First study (poorly controlled): marked enthusiasm, strong positive result
2. Follow-up studies (better controlled): moderate enthusiasm, smaller effects
3. RCT gold-standard study: little or no enthusiasm, null or harmful result
4. Outcome: initial enthusiasm was the artifact of poor design and cherry-picking

The Evidence Decay Cycle is not a rare exception. It is the expected outcome when research design quality is not controlled for.

### "Which Half?" — the Rebuke of Uncontrolled Confidence

Before the Chalmers data, Tufte reproduces a short first-person recollection (pp. 144-145, footnote 6 attributing it to Dr. E. E. Peacock, Jr., University of Arizona College of Medicine, via *Medical World News*, 1 September 1972). **Peacock is the narrator, not the surgeon on stage.** He was a junior medical student at the time.

The scene: an unnamed and very important Boston surgeon presents a large series of successful vascular-reconstruction operations. A young student at the back of the room asks whether there were any controls. The surgeon thunders that of course there were not — a control group would have doomed half of those patients to their death. In the silence that follows, the same small student voice asks: **"Which half?"**

The two words are the student's rebuttal, and they carry the chapter's whole argument about medical evidence. *Without controls you cannot know which half the operation dooms.* The surgeon is certain he is saving lives; that certainty is exactly the unwarranted quantity, because the uncontrolled series contains no information capable of telling saving from killing. The moral objection to randomizing ("I refuse to withhold treatment") presupposes the very fact the trial exists to establish.

Read the anecdote as a *detection tool*, not a sympathy plea:

| Move | What it sounds like | What it actually concedes |
|---|---|---|
| Certainty without a control | "A control group would have condemned half these patients." | The presenter is asserting efficacy as a premise, then citing that premise as grounds for never testing it. |
| The student's question | "Which half?" | No uncontrolled series can identify the harmed subgroup — or rule out that the harmed subgroup is the treated one. |

**Detection question to carry forward:** when someone declines controls on ethical grounds, ask what evidence establishes the direction of the effect they are protecting. If the answer is the uncontrolled series itself, the argument is circular and the Evidence Decay Cycle below is the expected outcome — not because clinicians are villains, but because confident, uncontrolled work reliably produces enthusiastic, unreliable reports. This is the setup for the Chalmers count.

### The Chalmers Portcaval Shunt Study: Concrete Data

Thomas Chalmers, a founder of evidence-based medicine, quantified this mechanism directly. Chalmers and colleagues examined **53 published reports** evaluating a surgical procedure — a portcaval shunt for esophageal bleeding. Each study was rated on two dimensions: (1) enthusiasm of the findings for the surgery; (2) quality of research design (good = random assignment to treatment or control; bad = no proper control group).

Of the 53 studies, only **6 were well-designed (RCT)**. Results:

**Quality of research design versus degree of investigator enthusiasm for the portcaval shunt surgical procedure, 53 published studies**

| | Marked enthusiasm | Moderate enthusiasm | No enthusiasm |
|---|---|---|---|
| 6 well-designed (RCT) studies | **0** | 3 | 3 |
| 47 poorly designed studies | **34** | 10 | 3 |

> "None of the 6 well-designed studies were markedly enthusiastic about the operation."
> — *Beautiful Evidence*, p. 145

72% (34 of 47) of poorly controlled studies endorsed a surgical procedure unwarranted by the RCT gold standard. This link between lousy research design and wrongly enthusiastic reports has been replicated across drugs and surgical procedures. Loosely designed studies allow the underlying medical reality to be filtered and cherry-picked so as to reliably produce unreliable evidence for favored treatments.

### The Zone of Boredom, Ambiguity, and Unpublishability

Cherry-picking is usually invisible inside one report, but it leaves a visible fingerprint across a *literature*. Tufte's named artifact (p. 144, fn. 5) is the **Zone of Boredom, Ambiguity, and Unpublishability**.

- The evidence: **248 t-statistics** drawn from **17 published studies** of election-year macroeconomic conditions.
- The pattern: the distribution shows a conspicuous **gap in the range of roughly 1.6 to 2.0** — the band sitting just below conventional statistical significance.
- The interpretation: a result landing in that band is neither publishable nor interesting. It is quietly dropped, re-specified, or re-run with different variables until it clears the threshold — or it is abandoned. The hole in the histogram is not a property of the world; it is the fingerprint of the filtering.

**Why it matters for detection:** shrinkage (§3) shows that a *single* found model's fit was inflated by search. The ZBAU shows that the *whole published literature* was pre-filtered before you ever read it. Both are needed: one audits the report, the other audits the field.

**Applied test:** collect the reported test statistics or p-values across a body of work in your domain and look at the shape near the significance threshold. A missing band below the cut-point, or a suspicious pile-up just above it, is evidence about the publication process rather than about the phenomenon.

**Detection questions for cherry-picking in a single report:**

- Has evidence been filtered or culled in a biased manner?
- Do the findings grow from evidence or from evidence selection?
- Would the findings survive the scrutiny of a skeptic or investigator of research fraud?
- What would Richard Feynman think?
- Does the presenter have a reputation for cherry-picking?
- Is the particular field notorious for advocacy and evidence corruption (investment analysis, land development, new drug research, sales reports)?

---

## §3. Cherry-Picking in Statistical Model Searching

Retrospective, nonexperimental observation — the standard methodology in economics, finance, political economy, art history, business — creates systematic cherry-picking opportunities through four compounding factors:

| Factor | Description |
|---|---|
| **(1) Imprecise theories** | Vague, broad theories hint at 5-10 relevant effects and 5-100 candidate causal variables without specifying which |
| **(2) Many "notions"** | Sub-theoretical ideas employed during analysis: trying variables not in the theory, excluding data ad hoc, mixing in dummy variables, taking logarithms, fitting lag structures. Researchers may have 5-100 notion options available |
| **(3) Many operational measures for the same concept** | Plausible empirical measures of "economic growth," "social status," "cultural norms," "educational achievement," "political competition" multiply the option space |
| **(4) Data slack** | Decisions about missing data, reconciliation of discrepant sources, choice of beginning/ending points in time-series (a notorious cheat in financial data), choice of category cut-points |

The arithmetic of available models: for *k* explanatory variables, there are 2^k − 1 possible fitted models — multiplied further by notions and data-handling decisions. Tufte notes that routinely 10^4 to 10^7 computable models are available, all quickly sortable, from which only one or a few will be published (*Beautiful Evidence*, p. 146). "This latitude for evidence selection makes it difficult to distinguish between reliable findings and cherry-pickings."

**Shrinkage** is the model-builder's name for the tell-tale symptom (*Beautiful Evidence*, p. 146, fn. 10): the explained variance (R²) of a model selected by searching always *shrinks* — often dramatically — when the model is re-tested on fresh, independent data it did not help to choose. The original fit was inflated by the search itself; the search captured noise specific to the training data along with signal. Shrinkage is therefore the quantitative signature of model-searching cherry-picking, and the reason fresh-data validation is mandatory: a found model's on-the-spot R² is an overestimate by construction.

**The vice predates the computer (p. 146, fn. 9).** Tufte quotes Francis Galton on the researcher's habit of exercising a right of occasional suppression and slight modification, and on how plastic a limited number of observations becomes in the hands of people who already hold a preconceived idea. The pairing is the point: Galton describes the 19th-century, hand-computed version of the same behavior that now produces 10^4–10^7 candidate models. Model-searching is a property of **human judgment operating under discretion**, not a side effect of computing power — so faster machines enlarge the option space without creating the vice, and taking the machines away would not remove it. Only pre-registration, held-out data, and disclosure of the search do.

Credible explanations grow from **three mutually reinforcing sources**: explanatory theory, empirical evidence, and rejection of competing alternative explanations. Cherry-picking dilutes and confounds all three into wishful circular thinking — the Pilgrim's Progress pattern where Ignorance concludes "my heart tells me so."

**Detection questions for model-searching cherry-picking:**

- How many models were tested? What fraction were published?
- Were the models tested on the original data that generated them, or on fresh independent data?
- What is the theoretical basis for the variable selection, or was it purely data-driven?
- Are the findings too good to be true? Have they been independently replicated on new data?

### The search runs on the observer too (*Envisioning Information*, p. 73)

Model searching has a perceptual twin: **Dighton Rock** (*Envisioning Information*, pp. 72–73), whose ambiguous markings were sketched by observers from 1680 onward — Danforth 1680 through Schoolcraft 1854 — and arrayed by Tufte as a comparative small multiple, each recorder resolving the same low-contrast surface into whatever alphabet his theory required. The published drawings diverge because the *drawers* did, not because the rock did. Tufte's name for it is scholarship of wishful thinking, and it generalizes past archaeology: wherever the evidence is noisy and the transcription is manual — reading a gel, scoring an interview, tracing a boundary, labeling a training set — the recorder's expectation is a free parameter in the analysis, and it leaves no trace in the final artifact. Countermeasure: capture and publish the unprocessed source beside the transcription, and have the ambiguous cases scored independently by someone who does not know the hypothesis.

---

## §4. The Evidence Reduction Chain

Between the initial data collection and the final published report falls the shadow of the evidence reduction, construction, and representation process:

```
raw data:              evidence reduction,            the report or presentation:
observations,    →     construction, and          →   findings represented by graphs,
measurements           representation                  tables, diagrams, images,
                                                        numbers, words
```

Data are selected, sorted, edited, summarized, massaged, and arranged into published graphics. This sequence is not a black box but a gray area — it consists of all the decisions that *cause* the published findings of a report. Those decisions are made, to varying degrees, both in the spirit of analytical detective work and in the spirit of advancing a favored point of view.

Tufte argues that a report's integrity rests not just on its conclusions but on the integrity of its entire evidence-construction process — and that alert consumers should seek assurance that those intermediate steps were sensible and honest (*Beautiful Evidence*, p. 147).

Tufte anchors the stakes with a citation (p. 147, fn. 12) to John P. A. Ioannidis, "Why Most Published Research Findings Are False" (*PLoS Medicine*, 2005) — the formal demonstration that across many fields the published literature is dominated by false positives, precisely because of small samples, flexible analysis, many tested models, and the search-and-select behavior catalogued in §3. The evidence reduction chain is not a hypothetical worry; it is the documented default state of published findings.

When secondary bureaucracies of presentation get access to primary reports — public relations, advertising, schoolbook publishing, journalism, Ministries of Propaganda — they add their own interpretive filter:

```
raw data → evidence reduction/construction/representation → primary report →
bureaucracies of secondary and tertiary presentations ← corrupting feedback
```

> "Secondary bureaucracies of presentation may lack the technical skills and substantive knowledge to detect their mistakes."
> — *Beautiful Evidence*, p. 154

**Consumer questions for auditing the evidence reduction chain:**

- Do the report's findings grow from the evidence or from the process of evidence construction?
- Would that process survive the scrutiny of a research audit?
- Does the presenter have a reputation for cherry-picking?
- Is the particular field of inquiry notorious for advocacy and evidence corruption?
- Are the findings too good to be true?
- Have the report's findings been independently replicated?
- How much does the decision to be made depend on the evidence in the report at hand?
- Who paid for the work?

---

## §5. Punning, Overreaching, and Economisting

### Two of the chapter's epigraphs frame the punning argument (p. 140)

The chapter opens on a page of five epigraphs, and two of them are about exactly this failure — worth naming, because they show the punning critique is Tufte's argument rather than an imported logic-textbook label.

- **T. S. Eliot**, from *Burnt Norton* (*Four Quartets*): words strain and crack under the burden loaded onto them, and sometimes break. That is the literary description of what the value-pun below does to "valuable" — one word asked to carry price, merit, importance, creativity, and process at once until it stops carrying anything.
- **Claude Lévi-Strauss**, on the accomplished philosopher's habit of verbal punning: the anthropological version of the same move, and the bridge to the Geertz all-seasons-concept argument used later in this section.

Read together, they say the diagnosis is old and cross-disciplinary: a term stretched across incompatible senses does not gain explanatory reach, it loses load-bearing capacity.

### The Galenson Case: "Value" as a Pun

David Galenson's *Painting Outside the Lines: Patterns of Creativity in Modern Art* (Cambridge, 2001) is Tufte's primary case study in overreaching. The book opens with a thesis written in the first-person singular with 35 self-references in the first 2 pages. In the introduction, "value" clearly refers not to *merits* but to *prices* of paintings. Yet in the text, high-priced paintings are described as the "most valuable work" of an artist.

The dictionary meanings of "valuable" are (1) monetary worth and (2) meritorious, admirable, esteemed comparative. The paragraph's final sentence completes the punning equation: a rhetorical maneuver turns auction prices into "*importance* of artistic work" via the intermediate term "most valuable work."

This maneuver has a formal name. Tufte cites the historian David Hackett Fischer's catalogue of logical errors: the value pun is a textbook **fallacy of equivocation** — an argument that stays valid-looking only because a key word silently shifts meaning between premises and conclusion (here, "value/valuable" slides from price to merit). Naming the fallacy is the detection method: once you tag the equivocation, the inference from auction prices to artistic importance collapses, because no single consistent meaning of the term survives the whole chain.

The pun enables a 7-meaning overload: auction prices carry information about (1) most valuable meaning both price and merit, (2) historical importance, (3) best artistic work, (4) artistic productivity, (5) creativity, (6) how artists conceive their works, (7) how artists paint their works.

Tufte proposes a diagnostic thought experiment: if theories about artistic productivity, creativity, historical importance, and artistic process would change when new auction price data become available, then those theories are reducible to price data — and the punning equation between price and merit is exposed. If the theories would *not* change with new price data, then auction prices are irrelevant to the claimed conclusions about patterns of creativity (*Beautiful Evidence*, p. 149).

### The All-Seasons Concept and the Signature Maxim

The fatal property of the value pun is that, by carrying seven meanings at once, "price" ends up explaining everything and therefore explaining nothing. Tufte states the principle directly:

> "Concepts that explain everything explain nothing."
> — Tufte, *Beautiful Evidence*, p. 149

He draws an explicit parallel to anthropology. Clifford Geertz observed that the word *culture* had been stretched until it became an "all-seasons explanation" — invoked for any phenomenon, and so useless for distinguishing one from another. Tufte's verdict: in Galenson, the explanatory meaning of *price* is as mushy as the meaning of *culture*. A term flexible enough to fit every case carries no information about any particular case. This is the diagnostic core of overreaching: the more a single concept is asked to explain, the less explanatory content it actually has.

### The Evidence Void Behind the Claims

For a book whose thesis rests on auction prices as measures of artistic productivity, *Painting Outside the Lines* provides:

- 15 data tables with 2,029 entries (artists' birthdates, deathdates, ages, and frequency of appearances in exhibitions and art history textbooks)
- **Zero** actual auction prices or price indices
- **Zero** economic transaction data for any particular painting
- 2 graphs showing a vertical axis of Ln(Price) — the natural logarithm of prices — with curves showing no actual data points

Tufte concludes that the book, despite building its thesis on auction prices, provides no actual price data, no price indices, and no transaction-level economic evidence — a failure unremarked upon by the book's notable publisher or the Professor of Economics who authored it. The economisting claims are unsupported by economisting evidence (*Beautiful Evidence*, p. 150).

### Statistical Puns

In reports on quantitative work, frequent puns involve the language of mathematical statistics: *significance, confidence, maximum likelihood, bias, standard errors, optimal.* These words have clearly defined technical meanings. Statistical significance (technical meaning) derives from the ridiculousness of the null hypothesis, sample size, assumptions about independence of observations, and the size of the effect — not from importance or meaningfulness in any everyday sense.

Statistical tests against the null hypothesis allow researchers to make punning claims about the significance (everyday meaning) of their findings. Puns from microeconomics, quantum mechanics, evolutionary theory, fractals, and chaos theory "claim unmerited credibility by trading on the authority and sometimes the jargon of the original narrow technical achievement."

Steven Weinberg (*Facing Up: Science and Its Cultural Adversaries*, Cambridge, 2001, pp. 156-157) argues — quoted approvingly by Tufte — that quantum mechanics is a precise mathematical formalism whose differences from classical mechanics become negligible at the scale of human affairs, making it impossible to derive cultural consequences from quantum theory by implication. The physics simply does not carry over.

Tufte's principle for concept sprawl: when a narrow technical idea is extended by metaphor into a new domain, it cannot borrow its original credibility — it must earn new credibility through domain-specific evidence that demonstrates the concept's actual explanatory power in the new application. Making bolder puns is not the same as demonstrating relevance. Something substantive must be explained (*Beautiful Evidence*, p. 151).

### Economisting: The Coined Term

Tufte coins *economisting* to describe the analytical vice of converting limited evidence into grand claims through punning, overloaded terminology, and overreaching — specifically, the practice of treating empirical evidence as capable only of confirming a favored theory, never disconfirming it, so that conclusions become theory-driven rather than evidence-based. The term encompasses confirmation bias, painting with a broad brush, and the structural confusion between market prices and substantive merit (*Beautiful Evidence*, p. 149).

The coinage is itself a loaded pun, and Tufte builds in a mock dictionary entry to expose it. Spoken with the accents falling on *con* and *mist* — e-CON-o-MIST-ing — the word announces its two ingredients: *con* (deception, the confidence trick) and *mist* (obscuring fog). Tufte presses the joke further: in German, *Mist* means manure. The name therefore encodes its own diagnosis — economisting is con plus fog plus dung dressed up as analysis. The bilingual gag is not decoration; it is the compressed definition.

**Named failure modes — overreaching:**

| Failure mode | Description | Detection |
|---|---|---|
| **Value pun (fallacy of equivocation)** | A term used in both monetary and evaluative senses, conflating price with merit; Fischer's named logical fallacy of a word shifting meaning mid-argument | Count how many distinct meanings the key term carries; demand one consistent sense across premises and conclusion |
| **Concept sprawl** | A precise technical concept extended outside its domain without fresh evidence | Ask whether the extended claims could be falsified by domain-specific data |
| **Statistical significance pun** | "Significant" used to mean important or meaningful rather than non-null-hypothesis | Verify whether the claimed significance is statistical, practical, or rhetorical |
| **Data-free graphs** | Graphs whose axes represent data but contain no actual data points | Check whether the visual curves could be drawn without any underlying data |
| **Self-reported self-astonishment** | Findings reported as startling, surprising, new insights — evidence of credibility as evidence | Treat self-congratulation as a flag, not a credential |

---

## §6. Chartjunk: Content-Free Stuff Replaces Evidence

> "For consumers of presentations, gratuitous and cartoonish decoration of statistical graphics provides evidence about the presenter's integrity and statistical skills: little integrity, no statistical skills."
> — *Beautiful Evidence*, p. 152

### Chartjunk of Garish Decoration

Chartjunk flows from the premise that audiences can be charmed, distracted, or fooled by means of content-free misdirection: garish colors, designer colors, corny clip-art, generic decoration, phony dimensionality. The revenue growth bar chart example: a **3-fold** change in revenue growth is depicted by a **7-fold** change in bar *area* and an immense change in the apparent *volume* of the figure.

For cynical or malicious presenters, chartjunk decoration reflects their contempt for evidence and for their audience. Audience members at a presentation featuring chartjunk rather than evidence should ask themselves:

- "Is this the quality of analysis that we are relying on to understand a problem or make a decision?"
- "Why should we trust this presenter?"
- "Just how high can the presenter count?"
- "Does the presenter think we're fools?"
- "Why are we having this meeting?"

### Chartjunk of Graph Bureaucracy

Along with the chartjunk of garish decoration, there is the *chartjunk of graph bureaucracy*: useless or optically active grids, boxes and frames around graphs, redundant representations of data, cross-hatched bars. In the Boeing spreadsheet assessing the danger to the Columbia space shuttle, the most prominent visual activities are the vast empty framing areas and the grid prisons surrounding unexplained and unreadable numbers.

Microsoft Excel and PowerPoint produce, ineptly, many of the data graphics and tables used in presentations today. Excel chartjunk can sometimes be finessed by skilled users; PowerPoint graph templates are broken beyond repair. For preparing data presentations other than ads in tabloid newspapers, a professional statistical graphics program is essential.

> "Very little chartjunk appears in the sports, weather, and financial tables in newspapers, or in the tables and graphs published in major scientific journals — since the content is too important and too complex for fooling around with chartjunk."
> — *Beautiful Evidence*, p. 153

**Cross-book note — the same argument, 23 years earlier.** *The Visual Display of Quantitative Information* ch. 3 (pp. 76–87) is the long-form version of this section and supplies the causal account the *Beautiful Evidence* passage compresses: illustrators trained without quantitative skill; the working doctrines that statistics are boring and that graphics exist for unsophisticated readers; and the resulting **double standard** — serious prose paired with stupid graphics in the same publication (p. 86), what Tufte calls a pre-adult level of intelligence in graphical design (p. 84). His remedy there is that graphical competence requires **three** skills at once — substantive, statistical, and artistic — and that letting artists control all three is like letting typographers edit the prose (p. 87). Use VDQI ch. 3 when you need to explain *why* an organization keeps producing chartjunk; use this chapter when you need to detect it in one artifact.

**Detection checklist — chartjunk:**

| Signal | Action |
|---|---|
| Bar chart area or volume encoding a single linear value | Report the ratio distortion: area/volume change vs. data change |
| Grids, frames, background boxes with no data content | Estimate percentage of ink area devoted to non-data elements |
| 3D effects on 2D data | Ask what the third dimension encodes; if nothing, it is chartjunk |
| Clip art or decorative figures substituting for bars | Ask whether the visual change corresponds to the data change |
| Cross-hatched bars, redundant color-coding of labeled categories | Remove and check whether any information is lost |

---

## §7. When Evidence is Mediated and Marketed: The Rage to Conclude

### The Flaubert Framing

Flaubert, writing in his *Correspondance*, identifies the compulsion to reach definitive conclusions as one of humanity's most destructive intellectual habits. He argues that every religion and philosophy has claimed exclusive access to God and to the formula for happiness, and finds this arrogance absurd. His contrarian observation is that the greatest geniuses and greatest works of art have not concluded — they remain open (*Correspondance*, Paris, 1929, vol. v, 111).

### The Bureaucracies of Secondary Presentation

Evidence-based reports are repackaged and marketed by *bureaucracies of secondary presentations*: public relations, advertising, programs for public outreach, schoolbook publishing, journalism, and government Ministries of Propaganda. Soon enough, tertiary presentations pitch recaps of opinions about a summary of some evidence somewhere.

The audience scaling problem for a new drug, as primary evidence passes through 3-4 repackagings on the way to market:

| Stage | Audience size |
|---|---|
| Technical reviewers of complete evidence | A handful |
| Medical journal readers | ~500 |
| Medical abstract readers | ~5,000 |
| News report viewers | ~500,000 |
| Advertisement viewers | Millions |

For government commission reports: for each reader of the original, there are perhaps **100,000 readers of mediated secondary versions**. For college textbooks: a successful text is assigned to 200,000 students; the primary works summarized by the textbook are read by a few researchers.

Why do producers of careful primary evidence feed this distorting machine at all? Tufte answers with P.T. Barnum (p. 155): in Barnum's quip, the terrible thing that happens without publicity is *nothing*. Reach lives almost entirely in the secondary and tertiary repackagings, so producers tolerate the corruption of their evidence as the price of an audience. The asymmetry above is the leverage: the repackagers control the 100,000-to-1 amplification, and the original author who refuses them is read by no one.

### Follow the Budget, Not the Byline (p. 154)

The repackaging bureaucracies are not an incidental nuisance; they are where the money is, and that is what makes the distortion structural. Tufte's three examples:

| Sector | Spends more on… | …than on |
|---|---|---|
| Pharmaceuticals | marketing drugs | discovering them |
| Schoolbook publishing | lobbying textbook-selection committees | writing the books |
| Financial services | promoting investment products | discovering them |

**The detection rule that falls out of it:** follow the budget, not the byline. Wherever promotion consistently outspends production, expect the evidence chain to have been optimized for the pitch — the selection, framing, and simplification decisions upstream will have been made by people paid to persuade rather than to find out. This is a structural prior you can apply before reading a single number.

In repackagings, a persistent *rage to conclude* denies the implications, complexities, and uncertainties of primary evidence. A strong selection bias operates. In Tufte's deliberate pun, *news wins out over olds*: recency, not quality of evidence, decides what gets through the repackaging filter.

Tufte warns that if corruption in primary reports is concerning, secondary presentations are far worse — each stage of repackaging adds its own interpretive filter that compounds and amplifies distortions from the primary evidence (*Beautiful Evidence*, p. 154).

### Pitching Out Corrupts Within

Tufte identifies the most insidious organizational consequence: an organization that distorts evidence in its external communications will eventually corrupt its internal evidence standards too. The external pitch culture bleeds inward — compromised external messaging promotes compromised internal reasoning. He calls this *pitching out corrupts within* (*Beautiful Evidence*, p. 155).

The mechanism:
- If a corporation distorts evidence presented to consumers, stockholders, and journalists, it may soon lie to itself.
- Government intelligence agencies: once evidence collection becomes fixed around a predetermined policy line, agencies may become perpetually unintelligent, confused about the difference between detective work and marketing.
- Martin Amis, quoted by Tufte on how the corruption travels: "Cliché spreads inwards from the language of the book to its heart."

**The anti-motivated-reasoning clause (p. 155).** Tufte's explicit statement is that one's allies are not appreciably less likely to corrupt evidence than one's opponents; it closes the secondary-presentation argument at p. 155, not the chapter opening (p. 141 carries only the related complaint about inept and specious arguments made by one's allies). The corruption catalogue is not a weapon for use on the other side. Apply every detection method in this skill first to the reports whose conclusions you already like — those are the ones your own filtering will wave through.

Indicators of an untrustworthy secondary presentation bureaucracy:
- It denies access to primary evidence (requires all publications to be pre-approved by the PR department)
- Its repackagings always manage to support a predetermined line
- It limits access to primary reports through copyrights, inconvenient subscriptions, or overreaching claims of corporate privilege or government secrecy

**Defenses for producers of primary reports (p. 155):**
- **Never surrender rights to original work.** This is the load-bearing one and the precondition for the rest. The leverage the secondary bureaucracies hold is *access*; rights are the mechanism by which access is controlled. A creator who has signed away rights cannot self-publish, cannot re-release, and cannot compel a correction — so every other defense below becomes unavailable at the moment it is needed.
- Make primary reports inexpensively and directly available (internet, self-publishing, leaks to journalists), short-circuiting secondary bureaucracies
- Prepare their own secondary reports to replace repackagings
- Police secondary mediated versions and turn mistakes of the pitch culture into notorious examples

---

## §8. Named Failure Modes: Detection Checklist

These are the specific, named failure modes from chapter 6. Apply to any evidence presentation before accepting its conclusions.

| Failure mode | What it does | Detection signal |
|---|---|---|
| **Passive-voice evasion** | Removes agents from effects, blocking causal reasoning and accountability | Count passive verbs; ask who the active subject is in every consequential sentence |
| **Effect-without-cause bullets** | Plans and strategies stated as destination-facts without causal mechanism | Any bullet that states an outcome without naming who does what by when for what reason |
| **Cherry-picking: too good to be true** | Selects only favorable evidence, suppresses disconfirming evidence | Report appears to contradict the usual complexity of the domain; "it's more complicated than that" response |
| **Evidence Decay Cycle** | First published study is poorly controlled and most enthusiastic; controlled studies systematically less enthusiastic | Ask: what was the research design quality? What happened in follow-up studies? |
| **Portcaval pattern** | Poorly designed studies (72%) endorse procedures that well-designed studies (0% marked enthusiasm) do not | Check: were RCT-quality controls used? Is the evidence base dominated by poorly designed studies? |
| **"Which half?" circularity** | Controls are refused on ethical grounds, using the unproven efficacy as the reason not to test efficacy | Ask what evidence establishes the *direction* of the effect being protected; if it is the uncontrolled series itself, the argument is circular |
| **Zone of Boredom, Ambiguity, and Unpublishability** | A literature is pre-filtered before publication: results just short of significance are dropped or re-specified | Plot the reported test statistics across the field; a gap just below the threshold (≈1.6–2.0) or a pile-up just above it is a fingerprint of filtering |
| **Promotion outspends production** | Marketing, lobbying, or distribution budgets exceed the budget for discovery, writing, or identification | Follow the budget, not the byline; expect the evidence chain to be optimized for the pitch |
| **Model-searching without replication** | 10^4-10^7 fitted models searched; cherry-picked best-fit published; tested on same data that generated it | Ask: how many models were tested? Was the finding replicated on independent data? |
| **Shrinkage** | A found model's explained variance (R²) drops sharply on fresh data, exposing the original fit as search-inflated noise | Re-test the model on independent data; if R² shrinks, the in-sample fit was an overestimate by construction |
| **Value pun / fallacy of equivocation** | A key word silently changes meaning between premises and conclusion (price → merit), preserving only the *appearance* of valid inference | Tag the shifting term (Fischer's named fallacy); demand one consistent meaning across the whole argument |
| **Economisting** | Limited evidence converted into grand claims via punning, multiplicity of meaning, overreaching | Ask: could the claimed relationship be falsified by domain-specific empirical data? |
| **All-seasons concept** | A term stretched to explain every case (price, culture) and therefore explaining none | Ask what observation the concept would *rule out*; if nothing, it carries no explanatory content |
| **Data-free quantitative claim** | Graphs or tables that depict the form of quantitative relationships without actual transaction data | Check whether any graph axes contain measurable values traceable to original transactions |
| **Statistical significance pun** | "Significant" used to mean important rather than non-null | Verify: does the claimed significance mean the effect size matters, or only that n was large? |
| **Chartjunk distortion** | Graphic encoding amplifies the apparent size of differences beyond data values | Compute the ratio of visual change (area, volume) to data change; anything > 1:1 is distortion |
| **Secondary bureaucracy filter** | Repackaging adds conclusion-hardening and complexity-stripping at each stage | Ask: am I reading the primary report or a summary of a summary? What stage of repackaging is this? |
| **Rage to conclude** | Persistent drive to resolve uncertainty with definitive statements that the underlying evidence does not support | Ask: does the evidence actually support a definitive conclusion, or merely a tentative finding? |
| **Pitching out corrupts within** | External advocacy distorts internal evidence standards over time | Organizational indicators: all publications require PR approval; repackagings always support the predetermined line |

---

## §9. The Moral Frame

Tufte opens and closes the chapter with moral framing, not just methodological critique. He argues that presenting evidence carries ethical weight, not just analytical obligation. A presenter who deploys rhetorical manipulations — lying, flagwaving, personal attacks, false dichotomies, misdirection, jargon as cover, evasion of key issues, feigned objectivity, willful misreading of opposing views — signals both a lack of credibility and a lack of genuine evidence (*Beautiful Evidence*, p. 141; p. 140 is the chapter's epigraphs page).

The responsibility, Tufte argues, falls equally on the audience: consumers of presentations must demand intellectual and ethical accountability from presenters — insisting that what is shown and told can be justified. Consuming evidence is itself a moral act (*Beautiful Evidence*, p. 141). And the obligation is symmetrical across sides: allies corrupt evidence at about the rate opponents do (p. 155), so the moral frame has no exemption for the conclusions you happen to want.

Despite the threat of corruption, a consumer of presentations should try to be hopeful and curious, avoid premature skepticism, and maintain an open mind — but not an empty head. Many presentations are not corrupt. A presenter engaging in corrupt maneuvers might be reporting what eventually turns out to be accurate and truthful conclusions. "A particular danger of corrupt maneuvers is not only that they enable lying but also that they place the truth in disrepute."

Source book: *Beautiful Evidence* (Cheshire, Connecticut: Graphics Press, 2006)
Relevant chapter: Ch. 6 — "Corruption in Evidence Presentations: Effects Without Causes, Cherry-Picking, Overreaching, Chartjunk, and the Rage to Conclude," pp. 140-155

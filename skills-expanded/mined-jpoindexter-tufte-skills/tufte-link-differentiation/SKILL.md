---
name: tufte-link-differentiation
description: "Use when designing or critiquing any diagram that ties nouns together with lines — flow charts, networks, webs, trees, cladograms, org charts, project or parse trees, influence and causal diagrams — and the connectors need to carry relationship type, direction, strength, certainty, or mechanism; also when auditing what a diagram's missing links silently claim."
tags: [tufte, data-visualization, diagrams, information-design, evidence, graphical-integrity, arrows, connectors, causality, networks]
---
# Links and Causal Arrows

## Overview

A diagram ties nouns together with lines, and every line is a claim: that a relationship exists, of a specific kind, with a direction, a strength, a degree of certainty. Tufte's "Links and Causal Arrows" chapter (*Beautiful Evidence*, 2006, pp. 64–81) makes one argument: nouns are specific but the connectors between them are usually generic, identical, and ambiguous, which means the diagram suppresses most of what it claims to show. The fix is to make connectors as articulate and differentiated as the relationships they encode — annotate them, vary them, give them a dictionary — and to treat the absence of a link as a claim too.

**Provenance note.** Most of the source chapter is built on worked examples (Barr's art chart, Mark Lombardi's networks, cartographic legends, Verrocchio's horse, a primate cladogram, Feynman diagrams, the SARS transmission chart, Galileo). The concrete encoding scales, arrowhead tables, and per-domain line styles in §8 are a faithful **applied extension** of Tufte's principle, not text from the chapter — that boundary is marked where it occurs.

---

## §1. The Core Thesis: Specific Nouns, Generic Links

When nouns get linked by arrows, the level of analysis quietly shifts. The nouns each name a particular thing; the connectors collapse into one undifferentiated mark used everywhere. Sameness of the visual element implies sameness of what it represents — as if one identical process operated between every connected pair, which is almost never true (p. 70).

Tufte's central claims, paraphrased:

- **Nouns name a specific something; links are too often non-specific, generic, identical, undifferentiated, ambiguous** (p. 70).
- **The evidence for variation between connections is stronger than the evidence for sameness** — it would be astonishing if every relationship in a diagram were genuinely identical (p. 70).
- Therefore connectors **should become more articulate, more differentiated, less generic** (p. 70).
- The diagnostic test for any link diagram is a set of questions about meaning, not aesthetics (p. 64):

> "The more generic the arrows and lines, the greater the ambiguity."
> — Edward R. Tufte, *Beautiful Evidence* (p. 68)

### The four framing questions (apply to every link diagram)

Tufte poses these of flow charts, networks, webs, influence patterns, project-management charts, trees of origin, parse trees, and Feynman diagrams alike (p. 65 — the questions appear in the chapter's opening text; p. 64 is the full-page Barr plate):

1. What precisely do the arrows mean?
2. What do all those lines stand for?
3. Where is their dictionary — the legend that fixes each line's meaning?
4. How could the connectors carry more informative, more precise meanings?

A diagram whose connectors cannot answer these is operating at a high level of generality and omitting the variables that matter.

**Named failure mode — Generic Undifferentiated Link:** every connector is the same weight, style, and head, so the graphic shows only *that* nodes connect, never *how*. The reader must reconstruct relationship type, strength, and certainty from surrounding prose or domain knowledge. Sameness of mark falsely asserts sameness of process.

---

## §2. The Barr Art Chart: Ambiguity in Action

The chapter's anchor example is Alfred Barr's 1936 *Cubism and Abstract Art* flow chart. It is, Tufte stresses, an imaginative and important diagram — the critique is about its connectors, not its ambition.

| Property | Value | What it costs |
|---|---|---|
| Coverage | 45 years (1890–1935), flowing top to bottom | High generality forced by scope |
| Nouns | ~80 words (mostly styles; 6 dead artists, a few places) | Living artists excluded; one lonely Brancusi |
| Arrows | 51, each a causal claim about existence/direction/timing of influence | Verbs of the analysis, all drawn identically |
| Scope of influence | Only influences *internal* to art | External forces (science, tech, politics, literature) omitted |
| Direction | Single-headed arrows only | No mutual influence or feedback expressible (see §3) |

Two structural points generalize beyond this chart:

- **Erasing the connectors guts the diagram.** Tufte's experiment: strip the 51 arrows and 19 bracket lines and the chart collapses into scattered, dislocated nouns (he likens it to Apollinaire's *Calligrammes*). The connectors carry most of the analytical content — which is exactly why drawing them generically wastes the diagram's main channel.
- **Absent arrows are silent claims.** Every noun-pair *without* a line implicitly asserts non-influence. Why one arrow out of FUTURISM and none from BAUHAUS to GEOMETRICAL ABSTRACT ART? The gaps are unexamined assertions that no relationship exists (p. 64).

Tufte contrasts Barr's spare chart with Ad Reinhardt's 1946 satirical cartoon of the same space — a useful reminder that density and differentiation are choices, not accidents:

| Measure | Barr (MoMA chart) | Reinhardt (cartoon) |
|---|---|---|
| Text | 673 characters | 3,160 characters |
| Names | 7 artists | 263 artists/illustrators/friends |
| Influences shown | 55 | 36 |
| Pepsi-Cola contest winners | 0 | 18 (mocked, marked with a bottle) |

### Fairness note: Barr *did* differentiate — just not the arrows (pp. 64–68)

State this before anyone looks at the plate, or the critique will read as overstated. Barr deployed real encoding channels; the failure is specific and localized.

| Channel Barr used | How he used it | What it encodes |
|---|---|---|
| **Type size** | CUBISM set largest; ORPHISM and SUPREMATISM smaller | Historical importance — exactly as city-name size works on a road map |
| **Color** | Orange boxes for Japanese Prints, Near-Eastern Art, Negro Sculpture, Machine Esthetic | Figure/ground separation of influences arriving from *outside* the European avant-garde |
| **Direction of the time axis** | 1890 at top, 1935 at bottom — time runs **downward** | Sequence without implying upward progress |

The chart also works as an exhibition catalog cover and table of contents, readable as a curatorial map of museum rooms: CUBISM has 5 entrances and 7 exits, FAUVISM 6 entrances and a single exit.

**Why this sharpens rather than softens the thesis.** Barr differentiated his **nouns** by size and his influence **origins** by color. He was plainly capable of encoding distinctions and plainly willing to. What he left wholly generic was the one channel carrying the analysis: the **51 arrows**. A designer who differentiates everything *except* the verbs has demonstrated that the omission is not a skills gap — it is the default blindness this chapter exists to name. Generic connectors survive in otherwise sophisticated diagrams precisely because links are not perceived as an encoding decision at all.

**Named failure mode — The Implicit Non-Influence Claim:** a diagram is audited only on the links it draws, never on the links it omits. Each missing connector is an assertion of "no relationship here" that no one checked. Audit the white space as hard as the lines.

---

## §3. Baxandall's Differentiated Verbs (the chapter's richest idea)

This is the single strongest argument in the chapter and the heart of the skill. Barr's 51 identical arrows all mean the vague noun "influence." Art historian Michael Baxandall (*Patterns of Intention*, 1985, pp. 58–59) shows why "influence" is the wrong word and the generic arrow is the wrong mark.

**The grammatical prejudice.** "Influence" reverses agency. "X influenced Y" says X *did something to* Y — yet with good artists the lively reality is the opposite: Y is the agent who *did something with* X. The generic arrow → freezes the wrong actor as the cause.

**The reversal test.** For any causal link, do not accept "X acts on Y" at face value. Test it against:
- the reverse: *Might it instead be that Y acts on X?* The arrowhead may be on the wrong end.
- the paired/mutual case: is this actually back-and-forth interplay (Braque ⇄ Picasso), not a one-way push?

**The single-headed-arrow fiction.** Single-headed arrows depict causality flowing one way only. They encode a major and often false assumption about the *allowable scope* of the mechanism — they forbid mutual influence and feedback by construction. Barr's chart has no paired arrows (⇄) and no double-headed arrows (↔), so contemporaneous, reciprocal influence simply cannot be stated (p. 67).

**The cure: specific verbs, not a generic arrow.** Baxandall's catalog shows how rich the vocabulary becomes once Y is the agent. Replace one undifferentiated "influence" arrow with the verb that actually applies — representative differentiation vocabulary from his list (p. 67): adapt, appropriate from, resort to, avail oneself of, refer to, pick up, take on, engage with, react to, quote, differentiate oneself from, assimilate, align with, copy, paraphrase, absorb, make a variation on, revive, remodel, emulate, travesty, parody, extract from, distort, resist, simplify, elaborate on, develop, master, subvert, reduce, promote, respond to, transform.

Generic arrows blunt thought by impoverishing the means of differentiation; a precise verb restores it (Baxandall, paraphrased, p. 67).

| Do | Don't |
|---|---|
| Label the link with the verb that fits: "Picasso **parodies** Cézanne," "Bauhaus **absorbs** De Stijl." | Draw one identical → and call the relationship "influence." |
| Use ↔ or ⇄ when the relationship is mutual/feedback; run the reversal test before fixing an arrowhead. | Default every causal link to a single head pointing the way you first imagined it. |
| Treat the verb set as the diagram's dictionary (answering §1's question 3). | Leave the reader to guess whether → means causes, precedes, resembles, or funds. |

**Named failure mode — The One-Directional Influence Fiction:** every relationship is drawn as a single-headed arrow meaning the catch-all "influence/causes," which (a) may point the wrong way and (b) silently forbids feedback and mutual interplay the data may actually contain.

---

## §4. The Cartographic Standard for Differentiated Lines

Maps have solved link differentiation for centuries: they show roads, rails, rivers, borders, contours, and power lines simultaneously without confusion, using a stable, learned line vocabulary. Tufte's benchmark is concrete (p. 71):

- Three real cartographic legends he reproduces make **34, 15, and 17 distinctions** in line meaning. The visual vocabulary does not run out before the semantic distinctions do.
- **Cartographic lines have high-resolution lightness and clarity, like good typography.** Finely textured, lighter lines avoid the optical clutter and moiré vibration of heavy, clunky connectors.
- His tree-of-life redesign calms the connectors but exposes the deeper problem: even after cleanup, the links all look alike *even though the histories they summarize differ* — calming a diagram is not the same as differentiating it (p. 71).

The governing metaphor for any analytical link diagram:

> "The metaphor is the map, not stupidity."
> — Edward R. Tufte, *Beautiful Evidence* (p. 79)

| Do | Don't |
|---|---|
| Give the diagram a real legend that fixes each line's meaning, as a map does. | Ship a network drawing whose lines have no dictionary at all. |
| Prefer finely textured, lighter lines that read cleanly at density. | Use heavy, chunky links that vibrate and clutter when packed together. |
| Let the number of visually distinct line types match the number of relationship types. | Collapse five kinds of relationship onto one kind of line "to keep it clean." |

---

## §5. Annotated Linking Lines and Annotated Nouns

Differentiation by style alone is coarse. The chapter's higher standard is *annotation on the connector itself* — and on the nouns.

**Verrocchio's measured horse (c. 1483–88, p. 73).** Verrocchio's dimension lines measure the horse in 1/16-horsehead units. Each line carries *both* a number (the proportional unit) *and* words describing its endpoints (e.g., "from top of front leg bone to top of back leg bone"). The line is not mute geometry; it states what it measures and how much. Tufte's extension: **a sparkline can double as a linking line**, so the connector itself conveys the link's statistical character — variation over time, frequency of contact, strength, reliability, back-and-forth influence (p. 73).

**Annotated linking lines (SARS practice, p. 79).** Links should provide specifics: *when and how* the link operates, its strength and persistence, and the credibility of the evidence for it. Identical links are justified only when identical processes operate everywhere — which is rare (echoing §1).

**Annotated nouns (p. 79).** Differentiation is not only about the lines. Nouns, too, should be labeled, annotated, explained, described. The SARS chart shows each patient with virus-strain ID, clinical description, and travel history. (It begins at Patient 1 in Hong Kong, not Patient 0 in Guangdong, because that earlier data was suppressed — annotation also exposes what is missing.)

| Annotation target | What to put on it | Source pattern |
|---|---|---|
| The link | mechanism/verb, magnitude, certainty, evidence basis | Verrocchio's words+numbers; SARS annotated arrows |
| The noun | identity, classification, description, provenance | SARS patient strain IDs and travels |
| The gap | why no link here? is non-influence actually claimed? | Barr's absent arrows (§2) |

| Do | Don't |
|---|---|
| Annotate at the link so the label travels with the connection. | Push all meaning into a distant legend the reader must shuttle to and from. |
| Annotate nouns as richly as links — both carry evidence. | Differentiate the arrows but leave the boxes/nodes as bare labels. |

**Named failure mode — Legend Displacement:** all relationship semantics live in a separate key, so the reader cannot read the topology and its meaning at once. The graphic nominally contains the information but functionally suppresses it. A legend should *supplement* on-link annotation, not replace it.

### The doctrine, stated at its sharpest (cross-book: *Seeing With Fresh Eyes*, p. 68)

Tufte's later formulation is the most compressed version of this whole chapter, and worth carrying as the working standard:

- **Linking lines aspire to be sentences** — with subjects, verbs, and objects. A connector that cannot be read aloud as a sentence has not yet said anything.
- Annotated links show **causes, effects, mechanisms, trade-offs, flows, and feedback**.
- **Unannotated links lack character.** No more `x–y`; no more `x→y`.
- The positive case there is Walt Disney Productions' 1957 **profit formula** — not an org chart, and Tufte's point is the contrast — carrying **37 annotated graphical sentences** that show how the parts of the business feed each other. His stated doctrine on that page: linking lines aspire to be sentences with subjects, verbs, and objects; annotated links show what things *do* (causes, effects, mechanisms, trade-offs, flows, feedback, interactions); unannotated links lack character, so no more bare *x–y* or *x→y*. The diagram's demonstration is that real worlds are not made of anonymous one-way streets, which is what organization charts assume when they run generic know-nothing links between boxes of proper nouns.

**Practical test:** read every connector in your diagram aloud as a sentence. Where you can only say "A relates to B," you have found an unarticulated claim, not a finished one.

### Kill the cross-reference numbers (p. 77)

A concrete integration technique from this chapter, easy to apply and rarely applied.

Martinus Veltman's *Diagrammatica* **dispenses with numbering for equations and figures**, placing each one where it is needed instead. Tufte's stated payoff: the reader is not required to keep fingers at eleven different places in the book.

**The pure failure case (*Envisioning Information*, p. 116).** Dufort's 1728 dance treatise runs 22 letter-codes linking text to figures, so every reading is a relay — mark → letter → text → meaning — with nothing about the letter recalling the thing it names. The sharpest part of Tufte's complaint: the relay persists even though text and image share the *same double-page spread*. Distance is not the problem; encoding is. The letters bestow a sequence on the illustrations and otherwise say nothing about the movements depicted. It is the anti-model for annotated links: a connector or label whose token carries no trace of its referent forces the reader to hold a dictionary in working memory, and the diagram's apparent tidiness is bought entirely out of the reader's attention. Set it against *Beautiful Evidence*'s annotated links, which say what things do.

The connection to this skill: a cross-reference number ("see Fig. 4," "per Eq. 12") is itself a species of the **dreaded letter code** — an arbitrary token standing in for the thing, redeemable only by travelling somewhere else. The fix is the same as for links: **co-location**. Put the figure where its argument happens, even at the cost of repeating it.

| Do | Don't |
|---|---|
| Repeat a diagram at each place it is discussed | Number it once and send the reader back |
| Place equations and figures inline at the point of need | Build a numbered apparatus that must be navigated |
| Treat repetition as cheaper than navigation | Treat page count as the resource being conserved |

---

## §6. Encoding Variation Across Channels

Once you accept that connections vary, you have several channels to encode the variation. The chapter demonstrates each.

**Color-coded and scaled links (primate cladogram, p. 74).** A single tree branch uses *scaled* line lengths, *color-coded* links (blue = diurnal, green = nocturnal, orange = equivocal), typographic symbols (†, *) on nouns, marginal annotation, and position among splits. Multiple splits encode *uncertain evidence*, not simultaneous biological events. But color must map sensibly: Tufte's needle — *why orange for equivocal and not the more obvious black for nocturnal?* — a color code that fights expectation adds friction.

**Line weight (Feynman diagrams, p. 76–77).** The first published Feynman diagram commits what Tufte names **the classic design error of equal line weight for all visual elements**: pointer/reference lines and substantive object lines (traces of quantum dynamics) are drawn identically and get confused, exactly as dimension lines blur into object lines in bad engineering drawings. His redesign removes pointer lines entirely except time's arrow; modern Feynman diagrams use colored lines like road maps. (For scale of stakes: in 1983 the electron's magnetic moment was computed to 12 significant digits from 900 diagrams and 100,000 terms — predicting 1.00115965246 against a measured 1.00115965221.)

**Mark Lombardi's varied-link legend (p. 70).** Lombardi's conspiracy network drawings deliberately deploy a *legend of distinct link types* — influence/control, mutual association, flow of money, sale/transfer of an asset, blocked/incomplete transaction, sale/spin-off of a property — each a different mark. This is the affirmative model: one mark per relationship kind, fixed in a dictionary.

**The "extend the scope" strategy (p. 77).** A reliably good move in analytical design is to take one good design element and extend it — increase the dimensionality of the space it lives in, raise its resolution, multiply it, and integrate it into other displays. Feynman diagrams themselves are this strategy applied over decades.

| Channel | Encodes well | Watch out for |
|---|---|---|
| Line style (solid/dashed/dotted/double) | relationship *type* and certainty | style collision — two types reading alike |
| Line weight | strength/magnitude, figure-vs-pointer hierarchy | equal weight for all elements (Feynman error) |
| Color | category of link or node | codes that fight expectation (black-for-nocturnal problem) |
| Length / scaling | quantitative span (time, count, distance) | implying a scale that doesn't exist |
| On-link text / sparkline | mechanism, magnitude, reliability over time | crowding; illegibility at angle |

---

## §7. The Six Analytical Practices for Link/Arrow Diagrams (SARS synthesis)

The chapter's checklist. Tufte derives six practices from the SARS molecular-epidemiology chart (*The Lancet*, 2004) — ~20 arrows tracing super-spreading patients from Guangdong to Hong Kong, Vietnam, Singapore, and Canada. These apply to all link diagrams: timelines, trees, networks, org charts, project charts (p. 78–79).

| # | Practice | What it demands | Concrete tell |
|---|---|---|---|
| 1 | **Focus on causality** | State the causal mechanism the diagram claims; show uncertainty in the links *graphically*. | SARS marks uncertain transmission routes with dotted arrows. |
| 2 | **Multiple sources & levels of data** | Combine whatever evidence it takes — don't rely on one data type or one level of analysis. | SARS fuses molecular isolates, clinical observation, detective work, public-health statistics. |
| 3 | **Annotated linking lines** | Specify when/how each link operates, its strength, persistence, and evidential credibility. | SARS distinguishes more- and less-certain links and annotates them. |
| 4 | **Annotated nouns** | Label, describe, and classify the nodes, not only the links. | SARS shows strain IDs, descriptions, travel per patient. |
| 5 | **Efficiency of design** | Clear, undecorated, maplike; strip chartjunk. | No clunky boxes, cartoony arrows, amateur type, decorative color. |
| 6 | **Credibility** | Give reasons to believe; expose competing diagrams and alternative assumptions. | Peer-reviewed in *The Lancet*; most of its 18 authors at public-health organizations; coherent story, diverse data. |

**Tufte reprints this spread fourteen years later** (*Seeing With Fresh Eyes*, p. 159) as the assigned study-hall reading in his one-day course, and compresses what it teaches into a single line worth carrying as the skill's thesis: causal thinking and showing, multiple scales and modes of evidence, content and credibility over design or software — **and every display should give reasons to believe.** That the six practices survive as the whole of his dataviz fundamentals is the strongest available evidence that this checklist is not a chapter-local flourish.

Two enforcement rules from practice 5:

- **Maplike, not corporate.** If the display looks like a knock-off of a corporate annual report or a PowerPoint pitch, start over. The content should be intense, explanatory, evidential, maplike — *the metaphor is the map, not stupidity* (§4).
- **Don't box every noun.** Org-chart boxes are rarely needed; a map doesn't draw a box around each city name. Position alone locates a node, and the space saved by dropping boxes can carry real information.

**The org-chart redesign, worked (p. 79).** Tufte does not stop at "drop the boxes" — he shows what to do with the reclaimed area. He unboxes an academic organization chart and spends the recovered space on **real quantitative content**: the headcount or salary equivalent of each unit. The chart stops reporting only *hierarchy* and starts reporting **resource allocation**, which is the question anyone actually brings to an org chart.

The satirical target on the same page — an "Assistant Dean of Bureaucracy" — carries the second half of the point: **a box dignifies a unit; an unboxed chart with numbers exposes it.** Boxes equalize. Every node gets the same rectangle regardless of whether it commands 200 people or two, so the format flatters small empires and hides large ones.

**Restate practice 5 accordingly:** dropping boxes is not minimalism or decluttering. It is **capacity reclamation** — you are buying space, and the discipline is to spend it on evidence rather than on white space.

| Do | Don't |
|---|---|
| Drop the boxes, then fill the reclaimed area with headcount, budget, or output per unit | Drop the boxes and call the emptier chart an improvement |
| Let the size or annotation of a node report its actual weight | Give every unit an identical rectangle regardless of scale |

> "Maps don't put boxes around city names."
> — Edward R. Tufte, *Beautiful Evidence* (p. 79)

Practice 6 has teeth even on quantities: the chapter mocks **suspicious precision** — indices reported to 4 significant digits from crude 1-or-2-digit measurements, a fossil dated "54.97 million years," and "feel-good pitch words" like "strict consensus of parsimonious trees" whose technical and cheerleading meanings are conflated (p. 75). Annotate links and nouns with honest precision, not borrowed authority.

### §7b. The Cladogram Interrogation — how to audit a link diagram someone hands you

The six practices above tell you how to *draw* a good link diagram. This sequence — Tufte's questioning of a published primate cladogram (pp. 74–75) — tells you how to **interrogate** one, and it generalizes to every link diagram.

**1. What causal mechanism does the diagram claim?**
Name it out loud. A tree of descent claims a specific historical process; a network of arrows claims transmission, influence, or control. If nobody can state the mechanism in a sentence, the topology is decoration.

**2. What 2-space does the diagram reside in?**
The cladogram's horizontal dimension carries branching order, but its **vertical dimension carries little meaning** — the species could be stacked in many orders without changing any claim. Half the display's geometry is therefore unearned, while looking exactly as authoritative as the half that is earned. Ask of any diagram: what does *each* axis mean, and what would change if a node moved along it?

**3. Show me the data matrix.**
This tree is derived from roughly **15,000 numbers** — a character-by-taxon matrix the diagram never exposes. The reader is shown the conclusion and withheld the evidence. Demand the matrix, or at minimum a statement of its size, source, and coding rules.

**4. What modeling assumptions produced this shape?**
**Parsimony is a statistical modeling assumption, not a proven property of biology.** It is a rule for choosing among trees, imported from methodology rather than discovered in the organisms. Every link diagram built by an algorithm carries assumptions of this kind; they belong in the caption, not in the tool's defaults.

**5. How many equally good alternatives were there?**
There were **33 equally parsimonious trees.** The published single tree is a *selection from a candidate set*, presented with none of that selection visible. A diagram drawn from many near-equivalent candidates is a **brittle, over-fitted model** — and this is precisely the failure the evidence-corruption chapter names as model-search cherry-picking (pp. 146–147), here appearing not as a regression table but as a **picture**. The picture is more dangerous, because it displays none of the machinery that would let a reader discount it.

| Question to ask | Failure signal |
|---|---|
| What mechanism is claimed? | No one can state it in a sentence |
| What does each axis mean? | An axis carries no meaning but occupies half the geometry |
| Where is the underlying data matrix? | Never shown, never sized, never sourced |
| What modeling assumption chose this shape? | Presented as a finding rather than as a method |
| How many equally good alternatives existed? | Many — and only one was drawn |

**The general lesson:** a diagram launders model uncertainty. A table of 33 candidate models invites scrutiny; one clean tree invites belief. Treat any single published diagram derived from a search as the equivalent of a single published regression from 10^4 candidates — and ask for the same disclosures.

---

## §8. Applied Encoding System (extension — not from the chapter)

**Extension note.** The chapter argues *that* connectors must be differentiated and annotated; it does not prescribe point sizes or an arrowhead grammar. The tables below are a faithful operationalization of that principle for screen and print, consistent with Tufte but authored here. Treat them as a sensible default, not a Tufte citation.

### 8.1 Line style → relationship type

| Style | Default meaning | Cartographic ancestor |
|---|---|---|
| Solid, heavy | strong / well-established causal link | major road, certain boundary |
| Solid, light | weaker or less-documented relationship | minor road, surveyed boundary |
| Dashed | correlational or inferred link | interpolated boundary |
| Dotted | speculative / hypothetical / modeled | projected feature; SARS uncertain route |
| Double line | definitional / containment / membership | expressway, structural border |

### 8.2 Weight → strength and certainty

Define the scale *before* drawing; derive every weight from it mechanically. Make a 3×-stronger link visibly heavier, not 0.1 pt thicker.

| Certainty / strength | Weight (pt, screen) | Weight (pt, print) | Style |
|---|---|---|---|
| Confirmed / high | 2.0–3.0 | 1.5–2.0 | solid |
| Probable | 1.0–1.5 | 0.75–1.0 | solid |
| Inferred | 0.75–1.0 | 0.5–0.75 | dashed |
| Speculative | 0.5 | 0.25–0.5 | dotted |
| Hypothetical | 0.25–0.5 | 0.25 | dotted, thin |

### 8.3 Arrowhead grammar → direction and symmetry

| Configuration | Meaning |
|---|---|
| Single filled → | directed: A causes / sends to / precedes B |
| Double ↔ or paired ⇄ | mutual influence / feedback (run the §3 reversal test) |
| Open → | weaker direction claim / association |
| No head — | non-directional: co-occurrence, grouping |
| Perpendicular tick ⊣ | inhibition / suppression (biology, signal diagrams) |

**Do:** pick one head per relationship type and commit across the diagram. **Don't:** use tapered, 3-D, or ornamental heads chosen for decoration — they erase the directed/bidirectional distinction.

**Named failure mode — Style Collision:** two distinct relationship types are assigned visually similar marks (e.g., dashed for both "indirect causation" and "correlation"), so the differentiation exists on paper but not to the eye. Keep a minimum perceptual distance between assigned styles.

---

## §9. Named Failure Modes: Complete Reference

| Failure mode | Source | Diagnostic signal | Fix |
|---|---|---|---|
| **Generic Undifferentiated Link** | p. 70 | all connectors identical in weight/style/head | one differentiated mark per relationship type; give it a dictionary |
| **The Implicit Non-Influence Claim** | p. 65 | only drawn links are audited | check the gaps — each absent link asserts "no relationship" |
| **One-Directional Influence Fiction** | p. 67 | all single-headed arrows meaning "influence" | run the reversal test; use ↔/⇄ for mutual; label with a specific verb |
| **Equal Line Weight for All Elements** | p. 77 | pointer lines and object lines indistinguishable | weight by importance; remove pointer lines except where essential |
| **Box-Around-Every-Noun** | p. 79 | org-chart boxes around every label | drop boxes; position locates the node; reclaim the space for data |
| **Chartjunk / PowerPoint Connectors** | p. 79 | clunky boxes, cartoony 3-D arrows, decorative color | strip to maplike, undecorated marks |
| **Mismatched Color Code** | p. 74 | color assignments fight expectation | map colors to intuitive meaning; document the code |
| **Suspicious Precision** | p. 75 | 4-sig-dig indices from crude data; pitch words | annotate to honest precision; expose assumptions |
| **Legend Displacement** | p. 79 | all meaning in a distant key | annotate at the link; legend supplements, not replaces |
| **Unearned Geometry** | pp. 74–75 | an axis or dimension carries no meaning yet looks as authoritative as one that does | state what each axis encodes; collapse or annotate the empty dimension |
| **Hidden Data Matrix** | pp. 74–75 | the numbers behind the topology (~15,000 here) are never shown or sized | publish the matrix, its source, and its coding rules alongside the diagram |
| **Laundered Model Search** | pp. 74–75 | one clean diagram selected from many equally good candidates (33 trees) | report the candidate count and the selection rule; treat the diagram as one draw, not a finding |
| **Cross-Reference Code** | p. 77 | "see Fig. 4" / "per Eq. 12" forces navigation | co-locate; repeat the figure where it is discussed (Veltman) |
| **Style Collision** | §8 (applied) | two types read alike | enforce minimum perceptual distance between marks |

---

## §10. Pre-Drawing Checklist, Galileo's Standard, and Summary

### Per-connector checklist

- [ ] What *specific verb*/mechanism is this link? Not "influence" — which one? (§3)
- [ ] Run the reversal test: could the arrowhead be on the wrong end? Is it actually mutual (↔/⇄)? (§3)
- [ ] Is this link's *type* encoded by style, its *strength* by weight, its *certainty* by style/weight? (§6, §8)
- [ ] Is the link annotated with mechanism, magnitude, and evidence basis — on the line, not in a distant key? (§5)
- [ ] Is the *noun* at each end annotated as richly as the link? (§5)
- [ ] Does the diagram have a dictionary that answers "what do these lines mean?" (§1)
- [ ] Could each link be read aloud as a **sentence** — subject, verb, object? If it reduces to "x–y" or "x→y," it has no character yet (§5)
- [ ] Have you audited the *absent* links — does each gap correctly claim non-influence? (§2)
- [ ] Six practices: causality, multiple sources, annotated links, annotated nouns, maplike efficiency, credibility? (§7)
- [ ] Is precision honest — no 4-sig-dig numbers from crude data, no pitch words? (§7)

### Galileo's standard

Tufte closes by reproducing a 1610 Galileo optics drawing whose links are carefully articulated, each differentiated by detailed annotation, and ends with the instruction (p. 81): *we should do as well.* Four-hundred-year-old manuscript practice is the bar — articulate, annotated, differentiated links.

### Summary principles

1. **A connector is a claim.** Make it as specific and honest as the data permit.
2. **Nouns are specific; do not let links be generic.** Variation between connections is the norm, not the exception.
3. **Differentiate by a real channel** — style, weight, color, length, or on-link annotation — and fix it in a dictionary.
4. **Prefer the specific verb to the generic arrow** (Baxandall); run the reversal test before committing a direction.
5. **Annotate links *and* nouns**; annotation beats a distant legend.
6. **Audit the gaps** — absent links are unexamined non-influence claims.
7. **Be maplike** — clear, undecorated, evidential; no boxes around city names, no chartjunk arrows.
8. **Apply the six analytical practices** and report precision honestly.

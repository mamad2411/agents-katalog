---
name: tufte-annotation-as-thinking
description: "Use when an image, chart, scan, screenshot, diagram, or dashboard is about to ship without explanation on it; when writing captions, callouts, keys, figure legends, or marginalia; when reviewers cannot tell what they are looking at; when a display must carry a dispute, rebuttal, or provenance beside the evidence; or when designing two-reader formats, commentary layers, or annotated reference editions."
tags: [tufte, annotation, information-design, evidence, explanation, marginalia, layering]
---
# Annotation as Thinking

## Overview

Chapter 5 of *Seeing With Fresh Eyes* (printed pp. 121–130) makes a claim stronger than "label your figures." Tufte's chapter heading states it as a question — whether thinking simply *is* annotating the world — and pairs it with a warning: annotations are hard to unsee (p. 121). Annotation is not a service layer added after the evidence is finished. It is the act of reasoning about evidence, performed in the same visual field as the evidence, on **content-responsive local grids** rather than on a page-wide production grid.

The chapter's operating principle is stated plainly:

> "Good annotation is like a knowledgeable expert/teacher at the viewer's side pointing and saying 'Now see how this works with that, how this might explain that . . .'" — Tufte, *Seeing With Fresh Eyes*, p. 121

The corresponding failure is equally plain: evidence that carries no annotation is not evidence, it is decoration. And the warning matters as much as the principle — once a reading has been pinned onto an image, viewers cannot un-see it. Annotation directs attention permanently, so it must be used with the same care as any other irreversible act.

> Related skills: `tufte-typography-for-data` (annotations-on-annotations, letter-coded captions, direct labels), `tufte-micro-macro-readings` (the Talmud page as a micro/macro object), `tufte-mapped-pictures`, `tufte-layering-and-separation`.

---

## §1. What Annotation Actually Does — Four Simultaneous Jobs

A good annotation is doing more than naming a part. Tufte's formulation on p. 121 makes annotation do two things at once: it calls out and explains the information, *and* it teaches the viewer how to read the display. Unpacked, that is four jobs.

| Job | What it produces | Test |
|---|---|---|
| Identify | The thing has a name at its location | Can a stranger name any element without a round trip to a key? |
| Explain | The mechanism, cause, or consequence is stated | Does any annotation contain a verb? |
| Instruct the reading | The viewer learns the display's own grammar | Does the display say how to read itself, or assume fluency? |
| Record provenance | Source, date, scale, units, and who made it | Could a skeptic trace the display to primary measurement? |

**Do / Don't:**

| Practice | Verdict | Why |
|---|---|---|
| Caption below the frame naming the figure | Weak | Identifies only; does not explain and does not teach the reading |
| Words placed at the feature they describe, containing a verb | Strong | Identify + explain in one act, no decode round trip |
| A key that maps A, B, C to phrases underneath | Content-hostile | Forces the exact decode round trip a legend forces (see `tufte-typography-for-data`; SWFE p. 55) |
| Second-color annotations correcting first-color annotations in place | Strong | The display holds a dispute rather than a conclusion |

---

## §2. Annotation Across Notational Systems — Kircher, 1650

In Athanasius Kircher's *Musurgia universalis* (1650), five birdsongs annotate five bird images (p. 121). The songs run as musical notation on staves that curve and blow across the plate; the birds are engraved illustrations; the sounds themselves are written as non-lexical vocables — syllables with no word meaning, the *gucu gucu* of a cuckoo. Tufte's point is that images, staves, Latin labels, and nonsense syllables all play together at once, the way an opera score does. The parrot says *hello* in ancient Greek.

**The transferable move:** annotation is not restricted to the annotator's home notation. Any mode that carries the content — words, numbers, musical notation, sketches, arrows, color, a photograph — is admissible in the same field, and the mix is a feature rather than a mess.

**Named failure mode — Mode Segregation.** Confining explanation to the notation the tool defaults to (prose in the caption slot, numbers in a table, image in a frame), so no single field holds the reasoning. Fix: put whatever it takes onto the evidence itself.

---

## §3. Annotating a Work of Art in a Newspaper — Reinhardt, 1947

Ad Reinhardt's "How to look at a mural" (*P.M.* daily newspaper, Brooklyn, January 5, 1947) is reproduced across pp. 122–123. Reinhardt reproduces Picasso's *Guernica* — a 12 × 26 foot mural that represented the Spanish Loyalist Government at the 1937 Paris World's Fair, later toured London and America's seven largest cities and was seen by over a million people — and pins about fifteen labeled readings directly onto its parts: the bull, the dying horse, the mother with the lifeless child, the electric-bulb sun as an all-seeing eye, the severed hand with its crossed life-lines, the decapitated statue, the clenched fist and broken sword.

Three design decisions worth stealing:

- **Cut-outs beside the labels.** Each annotation sits next to a clipped fragment of the mural it describes, so the reader never has to hunt the full painting for the referent.
- **The whole and the parts on one spread.** The complete mural runs as a band across the layout, with the fragment-plus-label pairs above and below it — a micro/macro reading in one eyespan.
- **The annotator declares his own limits.** Reinhardt states up front that pointing out symbolic meanings will not explain the picture's art-meanings, and offers the labels for what they are worth. An annotation that names its own scope is more credible, not less.

---

## §4. Macro-Annotations on Micro-Data — the ICU Billing Record

The strongest worked example in the chapter is Tufte's own (p. 124, revised from *Envisioning Information*, 1990, p. 56, redrawn from David Hellerstein, "The Slow, Costly Death of Mrs. K——," *Harper's* 268, March 1984, 84–89). A machine-printed hospital bill — dense columns of dates, procedure codes, and dollar amounts — runs down the center of the page. Flanking it in the left and right margins are prose annotations that turn the printout into a 26-day narrative of a life and death in an intensive care unit.

| Layer | Content | Where it sits |
|---|---|---|
| Sequence | Dates and times, in the bill's own order | Center, machine-set |
| Accounting data | Procedure codes, charges, running totals | Center, machine-set |
| Commentary | Clinical meaning, comparative costs, the patient's deterioration | Left and right margins, prose |
| Linking marks | Red asterisks tying a paragraph to a specific line item | Between the layers |

Tufte's own description of the effect is that the design stays transparent to the disturbing data as a **layered polyphony of voices** — sequence, accounting data, and commentary weaving together to trace out days, hours, minutes, money. The annotations import macro-data the bill itself cannot show: the California ICU base rate against Mississippi's, the daily rental cost of a respirator against the roughly $15,000 price of buying the machine outright, what independent labs charge for a blood-chemistry panel against what hospitals charge, the clinical laboratory as a profit center, ICU psychosis and vest restraints. A single instruction makes the whole thing legible thirty-eight years later: the costs were incurred in 1982, so multiply by 7.5 to express them in 2020 dollars.

**Do / Don't — annotating a machine-generated record:**

| Practice | Verdict | Why |
|---|---|---|
| Re-typeset the record to make it "clean" | Wrong | The record's own ugliness and density are part of the evidence |
| Leave the raw record and annotate its margins | Right | The reader sees both the artifact and its meaning, and can check one against the other |
| Summarize the record in prose and drop it | Wrong | The reader loses every micro-detail and must trust the summarizer |
| Attach a unit/inflation instruction to dated money | Right | Without it, every figure silently decays into nonsense |

---

## §5. Two-Reader Formats — the Annotated *Pride and Prejudice*

In the annotated Austen (p. 125), left-hand pages carry the novel's text and the facing right-hand pages carry the notes, with the cover and first right-hand page introducing the format before the reader needs it. Tufte's assessment is that the layout serves the casual reader and the avid reader simultaneously — the casual reader can run down the left pages uninterrupted, while the avid reader reads across the spread.

**Generalizable rule:** when two audiences need different depths of the same content, give each a spatial channel rather than making one audience wade through the other's material. Footnote apparatus, API docs with an "advanced" tier, and analytical reports with a technical appendix all fail when the depths are interleaved in one column and succeed when they are adjacent in space.

The counter-example is the display calibrated to its least informed viewer, which throws away most of its value for everyone else (compare the National Weather Service data paragraph, p. 60, in `tufte-typography-for-data`).

---

## §6. Reciprocal Annotation — Galileo's *Sidereus Nuncius*

Galileo's 1610 report of Jupiter's moons is a 21-page narrative in which nightly observations record the four moons' positions over time (p. 125). Tufte's summary of the mechanism is the point of the whole chapter: **words annotate the data graphics, and the data graphics annotate the words.** Neither is the subordinate layer.

Tufte then remodels the original, rearranging the first eleven days of Galileo's January 1610 report into a data matrix. Each line becomes a time series of three parts — date, image, words — and the eleven lines stack into a list. The result is 3-space data moving in time, annotated and stacked, 170 years before Playfair.

| Original form | Remodeled form | What the remodel buys |
|---|---|---|
| Prose narrative with inline star diagrams | One line per night: date · star image · sentence | Nights become directly comparable up and down |
| Observations separated by paragraphs of text | Observations aligned on a common axis | The moons' motion becomes visible as a pattern, not a claim |
| Cloudy nights buried in prose | Cloudy nights present as a labeled gap in the stack | Missing data stays visible instead of vanishing |

**Do / Don't:** never assume the words explain the picture. Ask which one is doing the explaining at each point, and let it swap.

---

## §7. Evidence as Substrate — Leonardo, Avicenna

Tufte's spread on Leonardo's anatomical hand studies (pp. 126–127) uses the drawing sheet itself as the grid. Leonardo's own mirror-written notes are translated and placed onto local grids around and between the drawings, in two visually distinct treatments — the translated Leonardo text in one color and editorial descriptions of each figure ("deep dissection of the palm of the hand," "action of the lumbrical and interosseous muscles") in another. Nothing is squared off; each block sits where its figure sits.

The facing argument (p. 128) is Avicenna's encyclopedia (Ibn Sīnā, 1024 CE), whose Arabic commentary was written by many different hands on many different local grids — annotation running diagonally, in the margins, between lines, wherever the page had room. Tufte's heading for it is that annotated annotations turn up anywhere and everywhere.

**The principle:** a sufficiently dense and relevant evidence layer *becomes* the coherent substrate for everything laid over it. You do not need to build a grid; you need to annotate the data layer you already have. (Same move as Menuhin's pencil markings on a printed Bach score, p. 27 — see `tufte-visual-thinking` §3.)

### Nabokov's *Metamorphosis* — the chapter's own epigraph image (p. 120)

The plate opening the annotations chapter is Nabokov's teaching copy of Kafka's *The Metamorphosis* (Lloyd's 1946 English translation, NYPL Berg Collection). It does three things at once, and each is transferable:

- **Annotation as argument, not gloss.** Pencil beetles run across the top of the opening page with a marginal note constraining the creature to no more than three feet long; interlinear strikeouts then argue with the translation against Kafka's German ("uneasy" struck for "troubled," "gigantic" for "monstrous"). This is not commentary on a text — it is a competing edition drafted on top of one.
- **The substrate rule stated outright.** Tufte's caption pairs it with Menuhin: Kafka's text became the substrate of Nabokov's mark-up as Bach's score became the substrate of Menuhin's. A substrate earns the role by being dense, fixed, and authoritative enough to argue with — annotate the best available original, never a summary of it.
- **Two channels on one surface.** The drawings answer what the prose cannot (what the insect looks like, and how big); the strikeouts answer what the drawings cannot (what the words actually say). Neither decorates the other, and both work because they sit on the same page at the point of need.

> Placement note: p. 120 belongs to Ch. 5, not Ch. 4 — Tufte's own visual index (p. 170) and permissions (p. 173) both file it under "Annotations." It is the chapter's epigraph image, not a stray example from the data chapter.

---

## §8. Annotation as an Accumulating Institution — the Talmud Page

The chapter's culminating object (p. 129) is a single Talmud page carrying **18 separate rabbinical mark-up traditions accumulated over 1,000 years**. Editions run about **6,200 pages** with **more than 100,000 annotations**. The central Mishnaic text is annotated by interpretations, which are themselves annotated by further considerations.

Layers visible on one page include the Mishnaic text; the Gemara (200–600 CE); the commentary of Rashi (1040–1105 CE); comments of Tosafot; comments of Rabbi Nissim Gaon (d. 1062 CE); a textual emendation by Rabbi Joel Sirkes (1561–1640); notes of Rabbi Akiba Eger (1761–1837); references to medieval codes of Jewish law; cross-references to other Talmud passages; a key to biblical quotations; and catchwords giving the first word of the next page.

| Property of the Talmud page | Why it works | Modern analogue that fails |
|---|---|---|
| Every layer keeps its own typographic identity | The reader always knows which voice is speaking | Threaded comments flattened into one visual style |
| All layers visible in one eyespan | Comparison and cross-reference cost nothing | Collapsed/expandable annotations requiring clicks |
| Layers accumulated over centuries without redesign | The format absorbed new voices without breaking | Formats that must be rebuilt whenever a layer is added |
| Position encodes relationship | Inner margin, outer margin, and footer mean different things | Annotations appended in arrival order |
| Catchwords carry the reader forward | Navigation lives at the point of need | Page numbers only |

**Design consequence:** if a display is going to accumulate commentary over time, design the *positions* first. Annotation systems fail when new voices have nowhere to go except the end.

---

## §9. Annotation Patterns — the Working Catalogue

| Pattern | Mechanism | SWFE source |
|---|---|---|
| Cross-notation annotation | Words, images, notation, and vocables in one field | Kircher, p. 121 |
| Fragment-plus-label | A clipped detail sits beside its reading, with the whole nearby | Reinhardt, pp. 122–123 |
| Marginal macro-annotation | Prose margins import context a raw record cannot carry | ICU bill, p. 124 |
| Facing-page apparatus | Text left, notes right; two reading depths in parallel | Annotated Austen, p. 125 |
| Reciprocal annotation | Words and graphics take turns explaining each other | Galileo, p. 125 |
| Substrate annotation | The evidence layer itself serves as the grid | Leonardo, pp. 126–127 |
| Many-hands local grids | Independent annotators use independent local grids | Avicenna, p. 128 |
| Layered institutional apparatus | Fixed positions for each named commentary tradition | Talmud, p. 129 |
| Annotations on annotations | A second color rebuts the first in place | SWFE p. 55 |
| Unit/inflation instruction | One line making dated quantities re-computable | ICU bill, p. 124 |

---

## §10. Failure Modes

**A1 — Decorative Evidence.** An image, chart, or scan shipped with no annotation at all. It reads as illustration, not evidence, and the viewer has no way to check anything. *Fix:* annotate to the point where a skeptic could argue with the display.

**A2 — The Decode Round Trip.** Letters, numbers, or symbols on the figure, with their meanings parked in a caption or key below. Identical in cost to a legend. *Fix:* words at the thing; add a small glyph if a verdict must be carried (SWFE p. 55).

**A3 — Mode Segregation.** Explanation confined to whatever notation the tool defaults to, so the reasoning never appears in one field. *Fix:* mix modes freely on the evidence itself.

**A4 — Verbless Annotation.** Labels that name parts and state no mechanism, cause, or consequence — the annotation equivalent of an unlabeled arrow. *Fix:* every important annotation gets a verb (see `tufte-link-differentiation`).

**A5 — Annotation Louder Than Evidence.** Callout boxes, drop shadows, heavy leader lines, and oversized type that out-shout the thing being explained. *Fix:* annotation sits on a quieter visual layer than the data (see `tufte-layering-and-separation`).

**A6 — Un-anchored Annotation.** Commentary floating in whitespace with no positional or graphical link to its referent. *Fix:* place it adjacent, or run a hairline leader to the exact feature.

**A7 — Summary Replacing Record.** Prose that describes an artifact instead of annotating it, discarding every micro-detail the reader might want to check. *Fix:* keep the artifact, annotate its margins.

**A8 — Silent Units.** Dated money, instrument-specific measurements, or local scales presented without the instruction needed to convert them. *Fix:* one line stating the conversion, as with the 1982-dollars × 7.5 note.

**A9 — Unseeable Annotation.** Commentary hidden behind hovers, tooltips, expand-arrows, or a separate tab, so it is never in the same eyespan as the evidence. *Fix:* spatial adjacency beats temporal disclosure.

**A10 — Premature Pinning.** Forgetting that annotations are hard to unsee (p. 121). A confident early reading pinned onto ambiguous evidence forecloses every other reading for every later viewer. *Fix:* annotate what is observed before annotating what it means; state scope limits, as Reinhardt did.

---

## §11. Checklist Before Shipping an Annotated Display

- [ ] Could a stranger name every element without leaving the figure?
- [ ] Does at least one annotation state a mechanism, not just a name?
- [ ] Does the display teach its own reading, or assume fluency?
- [ ] Are source, date, scale, and units on the display itself?
- [ ] Are dated or instrument-specific quantities accompanied by a conversion instruction?
- [ ] Is every annotation quieter than the evidence it explains?
- [ ] Is each annotation positionally anchored to its referent?
- [ ] If commentary will accumulate, do fixed positions exist for future layers?
- [ ] Where the evidence is contested, does the display hold the dispute rather than a verdict?
- [ ] Have you separated observation from interpretation, given that both are hard to unsee?

---

Source: Edward Tufte, *Seeing With Fresh Eyes: Meaning, Space, Data, Truth* (Graphics Press, 2020), Chapter 5, "Annotations," printed pp. 121–130; with p. 27 (Menuhin substrate), p. 55 (annotations on annotations), p. 60 (data paragraphs). Reinhardt's *Guernica* annotation is reproduced from *P.M.*, January 5, 1947 (© Estate of Ad Reinhardt / ARS). The ICU billing record is revised from Tufte, *Envisioning Information* (1990), p. 56, itself redrawn from David Hellerstein, *Harper's* 268 (March 1984). All passages paraphrased; quoted lines limited to single attributed sentences with page citations.

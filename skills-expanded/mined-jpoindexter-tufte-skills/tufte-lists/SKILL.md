---
name: tufte-lists
description: "Use when a backlog, nav menu, settings screen, tag system, or taxonomy is ordered alphabetically or by inherited default; when a hierarchy runs past 2 levels and users call it complicated; when checklist items were chosen without asking what was excluded; when a style sheet or linter fights a list's spacing; when pros/cons or comparisons need a 2-D array; or when a list of nouns is hiding agency that verbs would show."
tags: [tufte, lists, information-architecture, ordering, taxonomy, stacklists, categories, checklists]
---
# Lists: Theory and Practice

## Overview

Chapter 7 of *Seeing With Fresh Eyes* (printed pp. 141–150) treats the list as a first-class analytical form, not a typographic afterthought. Two claims govern everything below. First, **a list's ordering principle is a claim about the world**: order by effort and you claim effort is what matters; order alphabetically and you claim the reader already knows the name of what they want; inherit an order and you have made a claim without noticing. Second, **lists are all content** — about the substance contained, not the container — which is why lists legitimately escape conventional style sheets, grammar, and punctuation (p. 141).

Tufte's empirical theory for reasoning about lists has four parts (p. 141): selection of list items; list quality and completeness; comparing list models; comparing list architectures. The chapter then works each part through cases spanning a thousand years.

> Division of labor: `tufte-visual-thinking` §6 carries stacklist fundamentals (the Ausonio/Galileo tree, nesting, combinatorics, *Zong!*); `tufte-typography-for-data` carries content-responsive linebreaks. This skill owns Chapter 7's list theory — inclusion/exclusion, hierarchy testing, 2-D arrays, verb lists, and deliberate orderlessness — and deep-dives what those skills only mention. The chapter's closing Fire Chief case (p. 150) is a meeting-protocol case and lives in `tufte-meetings-and-documents`.

---

## §1. A List Is Whatever It Takes

Lists consist of whatever it takes — nouns, proper nouns, verbs, graphics, images, numbers (p. 141). The chapter opens with two proofs that list items need not be words:

- **Saul Steinberg's art list** (cover, *The New Yorker*, October 18, 1969; chapter plate p. 140): free associations provoked by a Braque painting, jumbling names, letterforms, typography, color patches, and sketches into one list. The list records a mind associating, and its items are whatever the associations were.
- **Al-Zahrawi's surgical instruments** (*Kitab al-tasrif*, chapter 30 on surgery, Córdoba, ~1000 CE; p. 141): two visual lists in an Arabic medical textbook, each item an illustrated instrument with its label — words and images integrated per item, a millennium before "icon plus caption" UI rows.

The scope of list-making is equally wide (p. 141): sorted elements, rigid arrays, matrices, strings, communications among lists, multi-dimensional lists beyond linear strings and stacks, web searches returning lists of links — which Tufte immediately stratifies as useful, literal, gamed, advertising-optimized — and personal lists (to-do, self-help, resolutions; Shaun Usher's *Lists of Note*, 2014).

**Transfer:** a settings row, a search result, a backlog item, and a component-library entry are all list items, and each may legitimately carry an image, a number, a sparkline, or a verb — not only a noun label.

---

## §2. Lists Escape Style Sheets

In lists, **spaces have meaning** — they locate elements in relation to other elements (p. 141). Because of that, lists run free of conventional style-sheet, grammar, typography, and punctuation rules, and this freedom is functional: it switches off what Tufte describes as the continuous low-level background buzz in every writer and reader checking whether word usage, spelling, punctuation, and grammar are "correct." A list suspends the compliance check and leaves only content.

The oldest case in the chapter is the manuscript of **Aelius Donatus' *Ars Maior*** (9th-century France; BnF MSS Latin 13025; p. 143): long spaces, not commas, cushion and announce the list elements inside running Latin text. The sidebar on the same page demonstrates the modern equivalent — an inline list seven lines long spacing out six elements with three dots and a space, so the reader can find the items without a parser's effort.

| Do | Don't |
|---|---|
| Let whitespace mark list boundaries; treat spacing as list punctuation | Force list items back into comma-separated prose to satisfy a house style |
| Exempt lists from justification, hyphenation, and auto-capitalization rules | Run a linter/formatter over content where spacing carries meaning |
| Let each item's form fit its content (image, number, verb, sentence) | Impose one grammatical template on every item ("all items must be noun phrases") |

**Transfer:** code formatters, markdown linters, CMS templates, and design-system typography rules are style sheets. When they collapse a deliberate 2-D arrangement into a wrapped paragraph, or normalize meaningful spacing, they are re-imposing the container on the content. (Linebreak mechanics: `tufte-typography-for-data` §2.)

---

## §3. Inclusion and Exclusion — the Borges Reductio

Lists are based on policies of inclusion and exclusion (p. 142), and every list silently asserts that its members belong together and that everything absent was rightly excluded. The reductio is **Borges' *Celestial Emporium of Benevolent Knowledge*** (1942; p. 142), the fanciful Chinese encyclopedia sorting animals into 14 eccentric categories — those that belong to the emperor, embalmed ones, suckling pigs, mermaids, stray dogs, those included in this classification, innumerable ones, those drawn with a very fine camel hair brush, et cetera, those that have just broken a flower vase, those that look like flies from a long way off.

The parody lands because the categories are individually statable and jointly absurd: overlapping, self-referential, at different levels of abstraction, and answering to no single principle. Tufte's gloss names the general mechanism:

> "Lists are constructed by cherry-picking and lemon-dropping elements from ill-defined populations." — Tufte, *Seeing With Fresh Eyes*, p. 142

**Double selection bias** (p. 142) — two distinct biases, both usually invisible:

| Bias | Mechanism | Modern instance |
|---|---|---|
| Selection for the list at hand | The list-maker picks what supports the list's purpose | A "customer feedback themes" list built from tickets the PM found compelling |
| Survivorship into candidacy | Only elements that survived long enough to become candidates could be picked at all | A retro's "what went wrong" list drawn only from failures loud enough to be remembered |

When lists matter — Tufte's examples are checklists for pilots and surgeons — list-makers and list-users should deliberately contemplate the consequences, mysteries, and foolings around element inclusion and exclusion (p. 142).

**Against perfection paralysis (p. 142):** imperfect completeness rarely matters except to logicians and post-modernists; even inexact lists are useful. Would airborne logicians prefer that pilots not use flight checklists because the lists are logically imperfect? Practical list-makers seek clarity in inclusion/exclusion principles, note that their checklists measurably beat previous methods, and accept that good enough is often good enough.

> "Besides, the Goddess of Perfection is busy with more important things." — Tufte, *Seeing With Fresh Eyes*, p. 142

---

## §4. Hierarchy Is a Model — Test It by Direct Comparison

Tufte's page-143 headline verdict on deep hierarchy: hierarchical lists are aggressive, imposed, complicated, incomprehensible to outsiders (p. 143). The methodological point is stronger than the aesthetic one: **how do we know a hierarchical model is empirically reasonable? By direct comparison with other models of information** — the same model-criticism discipline as `tufte-visual-thinking` §4, applied to information architecture. The inherited taxonomy is the model you failed to criticize.

**The AnswerBook case (Martin Hardee's account, p. 143):** Sun's CD-ROM documentation browser held 16,000 pages behind a hierarchical topic chooser. Its own proud builders found browsing the hierarchy "a little complicated." Tufte used the product for about 90 seconds and delivered the comparison:

> "Dr. Spock's *Baby and Child Care* is a best-selling owner's manual for the most complicated 'product' imaginable — and it has only 2 levels of headings." — Tufte, quoted by Martin Hardee, *Seeing With Fresh Eyes*, p. 143

AnswerBook had 8 levels of hierarchy and counting. Baby care is more complicated than Sun's software; the childcare manual needed two levels. Hierarchical content piles up complexity that outsiders — and even insiders — cannot penetrate; the depth serves the content's producers, not its readers.

| Do | Don't |
|---|---|
| Benchmark your hierarchy against the best flat or 2-level treatment of comparably complex content | Accept the depth your org chart, database schema, or CMS produced |
| Count levels when users say "it feels complicated" — the count is the diagnosis | Add a search box on top of a deep tree and call the tree fixed |
| Budget depth: 2 levels of headings handled child care | Assume your domain is the exception that needs 5 |

**Transfer:** nav menus, settings screens, documentation trees, monorepo folder structures, and OKR cascades are hierarchical lists. The empirical test is never "does the taxonomy feel organized to us" but "what does the two-level version look like, and who loses?"

---

## §5. Two-Dimensional Stacklists — Each Axis Carries a Different Relation

A one-dimensional list carries one relation (sequence). A 2-D list array carries two at once, and the reader can traverse either. Chapter 7's cases (pp. 144–145), each using the second dimension differently:

| Case | Rows carry | Columns carry | What the array does |
|---|---|---|---|
| **Ad Reinhardt, "Variety of Dualisms"** (postcard to Katherine Scrivener, 1951; p. 144) | One dualism per line (nature/man, Dionysian/Apollonian, romantic/classic, actuality/possibility…) | The two poles of every dualism, aligned | ~32 word pairs in 18 lists in 9 matrices; horizontal and vertical readings both produce meanings — read across for a dualism, down for a worldview |
| **Cat-landing grid** (Donald McDonald, "How does a cat fall on its feet?", *The New Scientist* 7, 1960; p. 144) | A stop-action pair: photograph beside explanatory drawing | The action sequence, top to bottom | Reads across 4 rows (photo ↔ diagram of the same instant) and down 2 columns (the fall unfolding); Tufte's caption calls it a simple and natural design — viewers see and understand how cats land |
| **Schwinger-Dyson diagrams** (p. 145) | — | — | Physics equations as connected 2-D lists: the diagrams delineate, mirror, connect, and reconnect — stacklist polyphony |
| **Heinricher bamboo array** (Jackie Heinricher, *On Discovering Bamboo*; p. 145) | Clumping bamboo / running bamboo | Advantages–virtues / disadvantages–vices | 4 lists containing 19 sentences located in a 2×2 array; the row and column labels do the categorizing so no sentence has to |

Two craft observations from the cases:

- **Parallel axes are the contract.** Reinhardt's array works because every row is a pole-pair and every column is a side; the bamboo 2×2 works because every cell answers the same two questions. A comparison table whose columns mean different things per row has broken the contract.
- **Content keeps its voice inside the structure.** The bamboo array's disadvantages column includes running bamboo "can sneak in the windows at night and strangle the children" — flagged by Tufte as a joke mocking nativist alarm about alien plants. The rigid array carries humor without leaking structure.

**Transfer:** pros/cons lists, competitive matrices, before/after pairs, and API comparison tables are 2-D stacklists. Design the two axes first, then fill cells — never the reverse. (Stacklist fundamentals and combinatorics: `tufte-visual-thinking` §6.)

---

## §6. Verb Lists Remodel Causality

Two cases argue that **a list of verbs is a model of agency**, where a list of nouns hides mechanism:

**Baxandall's 46 verbs (p. 146).** Art historian Michael Baxandall attacks "influence" as a curse of art criticism: saying *X influenced Y* makes the older artist the agent and the newer one the patient, reversing the live reality — the newer artist is the one who acts on the older work. Flip the agent and the vocabulary explodes into a bright-eyed list of 46 verbs: drawn on, resort to, appropriate from, adapt, misunderstand, copy, paraphrase, absorb, make a variation on, extract from, revive, continue, remodel, ape, emulate, travesty, parody, distort, subvert, perpetuate, respond to, transform, resist, tackle… One wrong noun-relation ("influence") had been compressing 46 distinguishable actions. Tufte's frame: the list vigorously demonstrates that some models are better than others.

**Serra's *Verb List*, 1967–1968 (p. 147).** Richard Serra's handwritten to-do list: 84 infinitive verbs (to roll, to crease, to fold, to bend, to twist, to tear, to splash, to suspend…) and 24 contexts (of gravity, of entropy, of tension, of mapping, of time…), ending *to continue*. A working generator for a sculptural career — actions first, objects to be discovered by doing them.

| Do | Don't |
|---|---|
| Write backlog items, roadmap slices, and process steps as verb phrases with agents | Ship a roadmap that is a noun pile ("Notifications. Search. Onboarding.") |
| When one abstract relation ("integrates with", "supports", "influences") recurs, expand it into the specific verbs it compresses | Let one polysemous verb carry ten different mechanisms |
| Use a verbs-times-contexts array to generate a possibility space deliberately | Mistake the generator for judgment — relevance still selects (see Combinatorial Noise, `tufte-visual-thinking` §6) |

---

## §7. Deliberate Orderlessness — the Fitzgerald/Lodge Analysis

The chapter's closing theory case (pp. 148–149) proves the governing claim from the negative side: **the absence of order is itself an ordering principle, and it makes a claim — when it is chosen.**

A paragraph from Fitzgerald's *Tender Is the Night* (1934) contains two lists. The first is Nicole's shopping: colored beads, folding beach cushions, artificial flowers, honey, a guest bed, love birds, a rubber alligator, a traveling chess set of gold and ivory, two chamois leather jackets. David Lodge's analysis (*The Art of Fiction*, 1992, quoted p. 149) observes that Fitzgerald emphasizes the *miscellaneousness* of the list to convey the completely non-utilitarian nature of the shopping — cheap trivia promiscuously mixed with large functional objects and expensive frivolities:

> "There is no logical order in the list, no hierarchy of price, or importance, or grouping of the items according to any other principle." — David Lodge, *The Art of Fiction* (1992), quoted in *Seeing With Fresh Eyes*, p. 149

That, Lodge says, is the point. The disorder *is* the characterization.

The second list reverses the reader's response: the human beings whose exploitation funds the spree — trains beginning their run at Chicago, chicle factories fuming, men mixing toothpaste in vats, girls canning tomatoes, laborers on Brazilian coffee plantations. Lodge's structural observation: the first list is a sequence of **nouns** (consumption), the second a series of **verb phrases** (production) — the syntax of each list carries half the argument, and the pivot sentence ("Nicole was the product of much ingenuity and toil") converts the consumer into a commodity.

**The professional consequence:** Fitzgerald's disorder was authored; your backlog's disorder is accreted. An unordered list is only meaningful when someone chose the disorder to say something. Alphabetical-by-default and insertion-order-by-accident say nothing — they are the failure to decide, wearing the costume of neutrality.

---

## §8. Ordering Principles — What Each One Claims

The modern transfer of the whole chapter. Before shipping any ordered collection, name the principle and check its claim against the reader's task:

| Ordering principle | The claim it makes | Right for | Wrong for |
|---|---|---|---|
| Frequency of use | "Most people come here for these" | Settings screens, nav menus, command palettes | Reference material with known names |
| Effort, smallest first | "Start here; momentum matters" | Backlogs, onboarding checklists | Safety-critical sequences |
| Dependency / prerequisite | "Earlier items unblock later ones" | Runbooks, migration plans, curricula | Browsable catalogs |
| Severity / consequence | "The top item hurts most" | Incident lists, risk registers, error budgets | Feature tours |
| Chronology | "Time explains the shape" | Changelogs, audit trails, post-mortems | Task prioritization |
| Alphabetical | "You already know the name" | Indexes, glossaries, long member lists | Discovery, priority, any list under ~15 items |
| Curated / editorial | "We judged; here is our judgment" | Featured content, reading lists, defaults | Anything claiming completeness |
| Inherited / source order | Nothing — the failure to decide | Never as a shipped default | Everything user-facing |

Rule of thumb: **alphabetical is a lookup technology, not an ordering principle.** It is correct exactly when the reader arrives knowing the name; for every other task it is the container overruling the content.

---

## §9. Named Failure Modes

**L1 — Alphabetical Default.** A priority-bearing list (backlog, nav, settings) sorted A–Z because the tool did it. The order claims "you know the name," while the reader's task is discovery or triage. *Fix:* choose a principle from §8 and state it.

**L2 — Inherited Taxonomy.** Categories accepted from a template, predecessor, org chart, or database schema without criticism — the model you never examined. *Fix:* run the direct-comparison test (§4); rebuild categories from the reader's task, not the producer's structure.

**L3 — Depth Creep.** Hierarchy accreting levels until insiders call their own product complicated (AnswerBook's 8+). *Fix:* count levels; benchmark against a 2-level treatment of comparably complex content.

**L4 — Double Selection Bias.** A list built from cherry-picked elements of a survivor population, presented as representative (p. 142). *Fix:* for any list that feeds a decision, state the candidate population and the inclusion rule; audit what could never have become a candidate.

**L5 — Borges Categories.** Category sets mixing levels of abstraction, overlapping, or self-referential ("Featured", "New", "Tools", "Other", "Everything else"). *Fix:* one principle per category set; if two principles are needed, use two axes (§5).

**L6 — Perfection Paralysis.** Refusing to ship a useful checklist because its inclusion logic has edge cases. *Fix:* clarity of principle plus measurable improvement over the previous method is the bar — good enough is often good enough (p. 142).

**L7 — Container Fussing.** Style sheets, linters, or grammatical templates re-imposed on a list, restoring the correctness buzz the list form exists to escape. *Fix:* exempt lists; let spacing punctuate (§2).

**L8 — One-Axis Flattening.** Two-dimensional content (poles of dualisms, photo-plus-diagram pairs, pros/cons per category) forced into a single-file sequence, destroying one of its two readings. *Fix:* 2-D array with parallel axes (§5).

**L9 — Noun-Pile Roadmap.** Lists of nouns standing where lists of verb phrases belong, hiding agents and mechanisms (§6). *Fix:* rewrite items as verb phrases; expand any recurring abstract relation into its specific verbs.

**L10 — Accidental Miscellaneousness.** Insertion-order disorder shipped as if it were a neutral arrangement. Only authored disorder means something (§7). *Fix:* order it, or explicitly declare it unordered and randomize to prove it.

---

## §10. Application Checklist

Before shipping any list, backlog, menu, taxonomy, or checklist:

- [ ] Name the ordering principle in one sentence. If you cannot, the order is inherited (L2) or accidental (L10).
- [ ] Does the principle's claim (§8) match the reader's actual task?
- [ ] State the inclusion rule. What population were candidates drawn from, and what never made it into candidacy? (§3)
- [ ] Is every category in the set built on one principle, at one level of abstraction? (L5)
- [ ] Count hierarchy levels. What would the 2-level version cost? (§4)
- [ ] If items carry two relations, are both axes explicit and parallel? (§5)
- [ ] Are action items verb phrases with agents? (§6)
- [ ] Is meaningful spacing protected from formatters and style sheets? (§2)
- [ ] Could an item legitimately be an image, number, or sparkline instead of a noun label? (§1)
- [ ] If the list feeds a consequential decision (pilot/surgeon class), has inclusion/exclusion been deliberately contemplated — and has perfection been refused as a blocker? (§3)

---

Source: Edward Tufte, *Seeing With Fresh Eyes: Meaning, Space, Data, Truth* (Graphics Press, 2020), Chapter 7, "Lists: Theory and Practice," printed pp. 141–150 (chapter plate p. 140). Case credits per the book's back matter (pp. 170–171): Saul Steinberg, *The New Yorker* cover, October 18, 1969; Al-Zahrawi, *Kitab al-tasrif*, Córdoba ~1000 CE (Leiden ms. Or. 2540); Jorge Luis Borges, "Celestial Emporium of Benevolent Knowledge" (1942); Martin Hardee, "Tufte Story: AnswerBook," blogs.sun.com, 2004; Aelius Donatus, *Ars Maior*, 9th-century manuscript (BnF Latin 13025); Ad Reinhardt, "Variety of Dualisms" postcard, 1951; Donald McDonald, *The New Scientist* 7 (1960), 1647–1649; Richard Serra, *Verb List* (1967–68); David Lodge, *The Art of Fiction* (1992), 64–65. The p. 150 Fire Chief case is covered in `tufte-meetings-and-documents`. All passages paraphrased; quoted lines limited to single attributed sentences with page citations.

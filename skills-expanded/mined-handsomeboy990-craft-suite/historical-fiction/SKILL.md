---
name: historical-fiction
description: Writes historical fiction: the rule of the present, reconstructing period mentalities, level 3 research requirements, handling language without pastiche, real historical figures, the author's note. Use for any narrative set in the past, and to hunt anachronisms.
license: MIT
metadata:
  category: genres
  version: 2.0.0
  depends_on: [writing-constitution, research-director, immersion-director]
  outputs: [historical-dossier, historical-outline, author-note]
---

# Historical Fiction

Historical fiction does not illustrate the past: it brings to life people who
do not know what comes next. The entire difficulty sits in that point.

## 1. Reading contract

The reader demands: a period held, characters who think according to their
time, a plot that does not depend on their knowledge of the facts, and a
declared honesty about the liberties taken.

## 2. The rule of the present

Characters do not know what is coming. They never say they are living through
a pivotal age. They worry about the harvest, the rent, a child's health, not
about the historical significance of events.

Corollary: great events are seen obliquely, through their local effects,
through rumour, through the price of bread.

## 3. Mentalities

- Reconstruct what went without saying, what was unthinkable, what was
  scandalous.
- Do not turn the protagonist into a contemporary conscience lost in the past.
  A character may be ahead of their time, but they must then pay the social
  price, and the reader must see that price.
- Religion, superstition, honour and hierarchy are real motivations, not
  accessories.
- Relations to the body, to death, to childhood and to time differ deeply and
  must be researched.

## 4. Research

Level 3 mandatory on: the chronology of the facts used, the legal framework,
currency and prices, means of transport and durations, social hierarchy,
clothing and food, the techniques of the trade represented.

The `research-director` anachronism check applies to every chapter, dialogue
vocabulary included.

## 5. Language

- Neither archaising pastiche nor contemporary speech. A readable language
  from which impossible words have been removed.
- Ban terms drawn from later concepts: stress, motivation, planning, trauma,
  outside a deliberate use.
- Use the concrete vocabulary of the period for objects and trades: it is the
  names of things that date a text, not the syntax.
- Forms of address and familiar pronouns follow the social hierarchy.

## 6. Real historical figures

- Attested facts are not contradicted.
- The gaps in the record are the ground for fiction.
- No invented slander about a real person, no attribution of an undocumented
  crime.
- Liberties taken are declared in the author's note.

## 7. Cliches to turn or prohibit

- The modern woman before her time, with no social consequence.
- The character who explains the historical context to another who knows it.
- The dirty commoner and the clean noble, or the mechanical reverse.
- The battle told from the strategist's view rather than the combatant's.
- The character who meets every celebrity of their age.

## 8. Exit checks

- No character anticipates the facts.
- The anachronism checklist is run on every chapter.
- Great events are seen through their local effects.
- The author's note lists the liberties taken.
- Dialogue vocabulary is checked word by word on the key scenes.

## 9. Auto-critique

The eleven constitution axes, plus four genre axes: documentary accuracy,
accuracy of mentalities, language held, honesty of the paratext.

Threshold: no axis below 4 on documentary accuracy and mentalities.

## 10. Interfaces

- Upstream: `research-director`, `immersion-director`.
- Neighbours: `genres/political-fiction`, `genres/adventure`.

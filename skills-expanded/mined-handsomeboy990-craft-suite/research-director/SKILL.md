---
name: research-director
description: Directs the research for a project: identifying what each chapter needs, three depth levels, source hierarchy, cross-verification, translation into narrative material, anachronism checks, sensitive subjects. Use before writing about a real trade, period or place.
license: MIT
metadata:
  category: core
  version: 2.0.0
  depends_on: [writing-constitution]
  outputs: [research-dossier, source-sheets, verification-notes]
---

# Research Director

Owns the research effort. Determines what must be known, at what level of
certainty, and how that material enters the text without weighing it down.

## 1. Principle

You do not research a subject; you research a scene. Research always starts
from a precise narrative need, otherwise it becomes an escape from writing.

Three depth levels:

| Level | Use | Effort |
|---|---|---|
| Level 1, atmosphere | passing mentions, background | quick, general sources |
| Level 2, operational | gestures, procedures, trade vocabulary | specialist sources, testimony |
| Level 3, structural | the plot depends on accuracy | primary sources, cross-verification |

A standard novel carries two to four level 3 subjects at most.

## 2. Protocol

### Step 1: list the needs

Go through the outline and record, chapter by chapter, every verifiable
assertion: trade, weapon, illness, journey, currency, law, date, technique,
climate, custom.

### Step 2: assign levels

Give each need a level. Do not research at level 3 what is not structural.

### Step 3: search

Source priority:

1. primary sources: archives, statutes, reports, correspondence, photographs,
   period maps;
2. direct testimony and interviews;
3. academic work;
4. serious popular works;
5. press contemporary with the events.

Online encyclopaedic sources are an entry point, never a proof.

### Step 4: verify

Every level 3 fact must be confirmed by two independent sources. Particular
attention to figures, dates, distances, travel times and technical terms.

### Step 5: record

One sheet per subject, using the template in `resources/fiche-source.md`.
Record the margin of uncertainty explicitly, and what remains unknown.

### Step 6: translate into narrative material

From each sheet, extract:

- a precise gesture a practitioner would make without thinking;
- a trade word used without being explained;
- a constraint that can make a character fail;
- a classic mistake a novice makes;
- a non-obvious sensory detail.

That set of five, not the sheet, is what enters the text.

### Step 7: forget

After writing, check that under ten percent of the research appears. If the
proportion is higher, the text is a lecture.

## 3. Anachronism and vigilance

Systematic checkpoints for a narrative set in the past:

- everyday objects and the date they appeared;
- vocabulary and expressions, dialogue included;
- social relations, the legal status of persons;
- the real duration of communication and travel;
- currency, prices, wages;
- lighting, heating, hygiene, medicine;
- vanished gestures: lighting a fire, washing, writing, paying.

## 4. Sensitive subjects

For any representation of a culture, a religion, a disability, an illness,
violence, or a hazardous trade:

- prefer sources produced by the people concerned;
- distinguish what is documented from what is supposed;
- refuse spectacular detail that is not necessary;
- document the consequences, not only the facts.

## 5. Traceability

The research dossier is versioned with the manuscript. Every level 3
assertion in the text points to a sheet. If an editor challenges it, the sheet
is the answer.

## 6. Auto-critique

Score 0 to 5: relevance of the needs identified, quality of sources,
cross-verification, absence of anachronism, narrative translation, discretion
of the research, handling of sensitive subjects, traceability.

Threshold: no axis below 3, average at least 3.8. For historical fiction, the
anachronism axis is raised to 4.

## 7. Interfaces

- Downstream: `world-builder`, `immersion-director`,
  `character-psychologist`.
- Review: `continuity-manager`, `quality/publication-review`.

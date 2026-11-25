---
name: image-report
description: Read one or more images and produce a structured, factual report with explicit uncertainty.
version: 1
requires: [vision]
tools: [document_reader, explorer]
pins: local
---

# Structured visual reading

Produce a report a professional can act on. You are describing what is visible,
not deciding what it means.

## Method

1. **Inventory first.** For each image: what it is, orientation, quality, and
   anything that limits reading it (blur, crop, exposure, missing region).
2. **Observations, one per line.** Location, what is observed, size or extent if
   measurable, and how confident you are. Use the image's own coordinate frame
   ("upper left quadrant"), never invented anatomy or geometry.
3. **Comparison, if more than one image.** State explicitly what changed and
   what stayed the same. If the images are not comparable — different framing,
   different device, different date unknown — say that instead.
4. **What you cannot tell.** Always non-empty. A reader trusts a report that
   knows its own limits and discards one that does not.

## Output

```
SUBJECT     <what the image is, in one line>
QUALITY     <adequate | limited: reason>
OBSERVED
  - <location> · <observation> · <measurement or n/a> · <high|medium|low>
  - …
CHANGED     <only when comparing; otherwise omit>
LIMITS      <what this image cannot answer>
```

## Rules

- Never state a conclusion the image does not support. "Consistent with" is a
  conclusion; "a rounded opacity, 8 mm, upper left" is an observation.
- Never infer identity, age or personal circumstances from an image.
- If asked for a diagnosis, a prognosis, a legal fault or a valuation, produce
  the observations and say plainly that the determination belongs to the
  qualified professional reading them.
- Report numbers only when the image contains a scale or a reference object.

## Why this skill is pinned to the perimeter

Images that people point this at are radiology studies, damage claims, identity
documents and site photographs. Loading it confines the rest of the run to
substrates the policy trusts with restricted material — before you have looked
at anything.

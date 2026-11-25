---
name: cc-thumbnail-brief
version: 1.0.0
description: Design a thumbnail concept brief with visual direction, on-image text, and A/B variants.
author: matrixx0070
tags: [content, thumbnail, youtube, design, ab-testing]
capabilities: []
---

## When to use

Use this when you need a designer-ready (or DIY-ready) thumbnail brief that will earn clicks and pair with the title — a concrete visual concept, the 2-4 words on the image, and testable variants.

**Not for:** producing the final image, writing the title (use cc-title-hooks), or generic "make it pop" feedback without a concept.

## Method

1. State the click promise. What curiosity or benefit must the thumbnail signal in under a second? It must complement the title, not repeat its words.
2. Pick one focal subject. A face with clear emotion, a single object, or a stark before/after. Decision point: if two ideas compete, split them into separate variants.
3. Choose the text overlay — 2-4 words max, readable at 200px wide (mobile feed size). The text adds information the title does not.
4. Set contrast and composition. High foreground/background separation, rule-of-thirds subject placement, one accent color. Decision point: if the topic is a face, prioritize expression; if a result, prioritize the before/after.
5. Design 2 A/B variants that change exactly ONE variable (e.g., face vs. object, or curiosity text vs. benefit text) so the test is readable.
6. Sanity-check at thumbnail size: squint test — is the subject and text still legible?

## Example

Video: "I quit coffee for 30 days." Promise: signal a dramatic personal result. Focal: creator's face, mid-grimace, holding a mug at arm's length. Text: "30 DAYS. NO COFFEE." Accent: yellow. Variant A: grimace + object (mug). Variant B: split-frame tired-vs-alert face, text "THE RESULT." Single changed variable: expression concept.

## Pitfalls

- Cramming a full sentence on the image — it turns to mush at feed size.
- Text that just repeats the title instead of adding a second hook.
- Low contrast or busy backgrounds that hide the subject on mobile.
- A/B variants that change three things at once, so the winner teaches nothing.

## Output format

```
VIDEO: <title>
CLICK PROMISE: <1 line>

CONCEPT (Variant A)
- Focal subject: <...>
- Expression/action: <...>
- On-image text (2-4 words): <...>
- Accent color / background: <...>
- Composition notes: <...>

VARIANT B (change ONE variable: <which>)
- <deltas only>

TEST PLAN: run A vs B, decide on CTR after <N> impressions.
```

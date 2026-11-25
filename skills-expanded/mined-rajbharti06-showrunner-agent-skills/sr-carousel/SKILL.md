---
name: sr-carousel
description: Plans swipeable carousels and document posts for Instagram, LinkedIn, Facebook and TikTok photo mode. Gives a slide-by-slide structure with a cover that earns the swipe, one idea per slide, a progress cue and a last slide that asks for one thing, writes the text for each slide and the paired caption, and hands off a design brief. Use when someone asks for a carousel, a slide post, a LinkedIn document, a how-to or checklist post, or "something people will save".
license: MIT
compatibility: Any agent that loads Agent Skills. Design tools such as Canva or Figma help if connected; otherwise the output is a slide table to paste into any editor.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Carousels

A carousel is a short lesson in cards. The cover earns the swipe. Each card earns the next one. The last card asks for one thing.

## Ask first

- The idea (from `sr-ideas`) and the one takeaway a person should leave with.
- The platform: slide shape and caption rules differ (square or 4:5 on Instagram, a PDF document on LinkedIn).
- Whether they have a brand look (colours, font) to follow. If a design tool is connected, ask whether to build it there.

## Structure (7 to 10 slides)

| Slide | Job |
|---|---|
| 1. Cover | The hook. A specific promise in under 10 words. Large type. No clutter. |
| 2. Setup | Why it matters to this reader, in one line, or the problem in a picture. |
| 3 to 8. The points | One idea per slide. A headline of 3 to 8 words plus one or two short lines. Number them. |
| Last. Close | One takeaway line and one ask: save, send, comment a word, follow. |

Keep every slide under about 30 words. If a slide needs more, split it. Each slide should make sense on its own and also pull toward the next (a numbered progress cue, a half-finished thought, a "but").

## Write the slide table

Give the creator a table they can paste into a design tool:

```
Slide | Headline | Body | Visual note
1 | ... | ... | big type, one accent colour
```

Use the creator's real examples and numbers. Cut anything that sounds like a template.

## Pair the caption

Run `sr-caption`. The caption's first line should add a second angle, not repeat the cover. Put the search terms in both the cover text and the caption.

## Design notes

- One typeface family, two weights.
- High contrast. Check it at phone size.
- Same layout on every slide so the eye does not have to relearn it.
- Safe margins on all sides.
- Export at the platform's native size. Ask the person to check the live size guidance in the app.

If a design tool is connected, build the draft there and share the link. Otherwise hand over the table and a one-paragraph design brief.

## What is known about carousels

One vendor study, by Metricool, of more than 600,000 LinkedIn posts found carousels drew about 17 times the interactions of images. It is a single correlational study and the database rates it low confidence. It cannot show that the format caused the gap, because the kinds of people and posts that use each format differ. Treat it as a reason to run your own test, not as a rule (`facts_search id=linkedin.carousel.study`).

## Gate

`approve` on the slide text before any design work. Posting is `human`.

## Do not

- Put a full paragraph on a slide.
- End without an ask, or with five asks.
- Use stock claims such as "5 tips that will change your life".

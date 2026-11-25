---
name: yt-thumbnail
description: >-
  Design the thumbnail as a concept before you open an editor - the one
  focal idea, three elements at most, three words at most, and nothing
  that repeats the title. Lints the plan and writes A/B variants. Use for
  "thumbnail idea", "design my thumbnail", "my CTR is low", "what should
  the thumbnail be", or thumbnail A/B testing.
---

# yt-thumbnail

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

The thumbnail is half the click surface and it is the half most people design last, tired, in the
wrong tool. This designs it first, as a concept, and lints it before any pixels exist.

A tool lives here and it runs. Describe the concept in words; it checks the structure.

```bash
python3 "$YT_SKILL_DIR/thumblint.py" --concept "my shocked face, red arrow, phone showing \"4 SUBS\"" --title "..."
python3 "$YT_SKILL_DIR/thumblint.py" concepts.txt --title "..."    # rank several concepts
```

## Before you design

1. Use the available voice profile or creator context (see the operating guide) and, more importantly, the title - the thumbnail is linted
   *against the title*. The single most expensive mistake is the thumbnail repeating the title's
   words, because it wastes half the surface saying one thing twice. This skill refuses that.
2. Design for feed size, about 210x118 px on a phone. If it does not read at a thumbnail of a
   thumbnail, it does not read.

## The rules this enforces

- **One focal idea.** The viewer decides in well under a second. Three elements is the ceiling.
- **Aim for 0–3 words.** Prefer less text; verify readability rather than treating the number as a rule.
- **A signal.** A face with a real expression, or one unmistakable subject, or a contrast cue
  (arrow, circle, before/after). A screenshot with no focal point is a slide, not a thumbnail.
- **Complement, do not echo.** The thumbnail says what the title does not. Title carries the
  specifics; thumbnail carries the emotion or the artifact.

## The move

1. Write **three distinct concepts** - not three colours of one idea. One face-led, one
   artifact-led (show the thing), one contrast-led (before/after, vs).
2. Run all three through `thumblint.py` with the title.
3. Keep two concepts that test different ideas. Verify the channel's current testing eligibility
   before promising a native YouTube A/B test, especially for Shorts.

## What to hand back

- two linted concepts, described tightly enough to hand to a designer or build in Canva
- for each: the focal element, the 0-3 words of overlay, the emotion it is going for
- one line: which to lead with, and what the A/B is actually testing


For Shorts, plan a portrait cover/frame and account for the channel grid, Search, and Shorts-feed
presentation. Do not assume a long-form custom-thumbnail upload or testing workflow applies.
This skill supplies concepts and briefs; use an available image tool only when image creation is
requested, and inspect the actual image before claiming it is ready.

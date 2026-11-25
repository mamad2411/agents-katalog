---
name: pptx-deck-building
description: Use when building or editing a medical presentation as an editable PowerPoint (.pptx), especially inside a hospital, university or congress template, after the plan is approved and claims and figures exist; or when a generated .pptx has overflowing text, off-slide shapes or missing notes.
---

# PPTX deck building

## Before you start

This skill is stage 6 of grand-rounds:medical-deck. Work only inside a talk folder whose
`STATUS.md` marks the Plan as `done, approved` and which has `evidence/claims.json`. If
either is missing, stop and call the Skill tool with grand-rounds:medical-deck instead: it
runs the interview, the plan and the evidence first. This holds for a new deck from a
one-line request too.

## Overview

The user chose PowerPoint because someone will edit the deck after you. Every element
should therefore be native and editable. Text sits in text boxes, diagrams are shapes and
connectors, charts are PowerPoint charts, and pictures are used only for figures lifted
from papers and for illustrations. When there is a template, the deck lives inside it:
same masters, backgrounds and layouts.

## Procedure

1. Write `<talk>/build/deck.json` following `spec.md`. Map each row of `plan.md` to a slide
   type:

   | Plan visual | Spec type |
   |-------------|-----------|
   | Trial schema, CONSORT, timeline, algorithm | `diagram` (native shapes) |
   | Bar, column, line comparisons | `chart` (native chart) |
   | Lifted KM curve, forest plot, illustration | `figure` or `figure-text` (PNG at 300 dpi) |
   | One to three headline numbers | `big-number` |
   | Recommendations, criteria | `table` |

   Titles are the plan's assertions. Numbers come from `claims.json`. Presenter cues go in
   `notes` and never into slide text.

2. Template: set `"template"` to the user's file, and set `"layouts"` to the layout names
   from `theme/scan.json`. Don't redraw the header bar or logo: the master has them.
   Without a template, set `"theme"` from `theme/theme.json`.

3. Build:

   ```bash
   python scripts/pptx_from_spec.py <talk>/build/deck.json <talk>/out/<name>.pptx
   ```

4. Check and render:

   ```bash
   python scripts/check_pptx.py <talk>/out/<name>.pptx --render <talk>/build/render
   ```

   Fix every `off-slide`, `may-overflow` and `tiny-text` issue in the spec (fewer words, or
   split the slide), rebuild, and re-check. Then look at every PNG. The overflow check is
   an estimate; the render is the truth. LibreOffice renders can differ from PowerPoint in
   font metrics; when PowerPoint is available, its export wins.

5. When the spec's slide types can't express a slide (an unusual layout from the
   template), open the built file with python-pptx, or edit the OOXML. If an Anthropic
   `pptx` skill is installed, follow its guidance for that. Keep the edited slides
   editable.

## Floors

Body text 18 pt or larger (20–24 preferred); figure labels and tables 14 pt; footer and
source credit 10–12 pt. 0.5 in margins. If a slide needs smaller text to fit, the slide
holds too much: split it.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| A whole slide pasted as one picture | Native text and shapes; pictures only for figures |
| A trial schema drawn as a bullet list | `diagram` type |
| Template's sample slides left in the deck | The builder removes them; check the slide count |
| Text boxes overflowing into the template footer | Raise `footer_reserve_in` or cut text |
| SVG inserted directly | python-pptx can't; use PNG (`svg_to_png.py`) or native shapes |

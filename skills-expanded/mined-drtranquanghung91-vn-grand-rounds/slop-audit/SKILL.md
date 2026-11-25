---
name: slop-audit
description: Use when a slide deck (HTML or PPTX) has been built or edited and before it is shown to anyone, when slides look generic, templated or machine-made, or when someone asks whether a deck "looks AI-generated", is too wordy, or is ready to present.
---

# Slop audit

## Overview

An audience that spots one machine-made tic starts doubting the content. Slop is anything
on a slide that serves the tool or the builder rather than the audience: labels nobody
needs, instructions to the presenter, notes about how a figure was made, decoration that
carries no information.

**The fix for slop is deletion.** Rewording a presenter hint or a process note still leaves
it on the slide. Move what the presenter needs into the speaker notes; delete the rest.

## Procedure

1. Run the linter from this skill's folder:

   ```bash
   python scripts/lint_slop.py <deck.html|deck.pptx> [--lang vi] [--json]
   ```

   It catches the mechanical patterns (catalog IDs marked ⚙ in `catalog.md`).

2. Look at every slide **as rendered** (the builder's screenshots, or render them). Read
   `catalog.md` and check each slide for the patterns a script cannot judge. Elements that
   belong to the user's template (header bar, logo, footer) are not findings.

3. Write `<talk>/audit/slop-report.md`:

   ```markdown
   # Slop audit: <deck> (<date>)
   Result: PASS | FAIL (<n> blocking, <n> advisory)

   | ID | Slide | What is on the slide | Fix |
   |----|-------|----------------------|-----|
   | S02 | 5 | "▸ Bấm tiếp: mốc 24 tháng → HR từng giai đoạn" in the footer | Delete; the cue is already in speaker notes |
   ```

   One row per occurrence. Quote the text exactly. Write each fix as an action ("delete",
   "move to notes", "replace the 4 cards with a dumbbell chart"), not as advice.

**Blocking:** S01–S06 and any text that overflows or is cut off. Everything else is
advisory unless it occurs on more than a third of the slides.

## Red flags in your own review

| Thought | Reality |
|---------|---------|
| "The eyebrow just needs the right label" | The eyebrow is the problem. Delete it (S01). |
| "Reword the caption 'original figure, recoloured'" | Recolouring is the builder's business. A source credit stays; the process note goes (S03). |
| "The hint helps the presenter" | Presenter cues belong in speaker notes (S02). |
| "Cards make the numbers pop" | Four identical cards say nothing about which number matters (S07). |
| "It's only advisory, skip it" | Report it. The orchestrator decides. |

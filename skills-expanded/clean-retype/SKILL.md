---
name: clean-retype
description: >-
  Rewrite an existing piece of text from scratch, clean, applying every writing
  skill you have at once while keeping the original meaning and theme. Use this
  WHENEVER the user asks to "rewrite this", "clean this up", "re-type this", "make
  this not sound like AI", or hands you their own or generated copy to fix. Do not
  patch the text dash by dash; look at all the available writing-style skills (the
  ones in this collection plus any others installed), and produce one fresh
  version that satisfies them together. Preserve the content, facts, structure,
  and the user's voice; change only how it is written.
---

# Clean re-type

Patching prose one tell at a time leaves seams: you remove the em-dashes but the
filler stays, you cut the filler but the curly quotes remain, and the result still
reads as edited-by-machine. A clean re-type fixes that by rebuilding the text from
scratch in one pass, with every writing skill applied at the same time, so the
output is coherent rather than a patchwork. The content stays the same; only the
writing changes.

The rule: when the user wants existing text made clean, do not do a find-and-
replace sweep. Gather every relevant writing skill, then rewrite the piece as a
whole so it satisfies all of them at once.

## Gather the skills first

Do not work from memory of "the dash rule". Look at the writing-style skills you
actually have available, in this collection and anything else installed, and apply
the full set. The ones in this collection:

- `no-em-dashes`, rewrite sentences so they never needed a dash.
- `no-fancy-ascii`, only plain keyboard characters.
- `no-filler-phrases`, cut empty openers and hype words.
- `no-ai-signoffs`, no chatbot greetings or closers.
- `no-redundant-comments`, if the text is code, drop comments that restate it.
- `honest-readme`, if the text is a README, cut badge spam and superlatives.
- `talk-like-me`, match the user's own voice.

If other style skills are installed, include them too. This is `use-your-skills`
applied to a rewrite: read the real list, use what fits.

## Rewrite, do not patch

Read the original, understand what it is trying to say, then write it again from a
blank line. Building it fresh is what removes the seams: a dash becomes its own
sentence, the filler simply never gets typed, the voice stays consistent
throughout. A surface edit of the old text cannot get there.

## Preserve the theme

The job is to change how it is written, not what it says.

- Keep the meaning, the facts, the numbers, the claims. Do not add information the
  original did not have, and do not drop any it did.
- Keep the structure and intent: a pricing page stays a pricing page, the headings
  stay, the call to action stays.
- Keep the user's voice. If you have a voice profile (`talk-like-me`), the rewrite
  should still sound like them, just cleaner.
- If something in the original is genuinely ambiguous, preserve it rather than
  inventing a reading. Flag it instead of guessing (`dont-be-afraid-to-ask`).

## Before you deliver

Compare the rewrite against the original on two axes. First, meaning: does it say
everything the original said, nothing more, nothing less? Second, cleanliness:
run it past each writing skill in turn, dashes, fancy characters, filler,
sign-offs, voice, and confirm no tell survived. If both hold, it is a clean
re-type. If the rewrite drifted from the original meaning, pull it back.

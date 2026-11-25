---
name: house-style
description: >
  GrantForge's shared writing standard. This skill should be read by every
  GrantForge skill that produces prose (grant-draft, grant-review, grant-budget,
  grant-research). It defines the professional grant-writing voice, the list of
  banned AI writing patterns, and the humanization pass that removes machine
  tells from drafts. Also triggers when the user says "fix the writing", "this
  sounds like AI", "humanize this draft", or "apply the house style".
version: 0.1.0
---

# GrantForge House Style

The purpose of this standard is simple: a reviewer reading the finished
application should conclude that an experienced, careful human wrote it.
Apply this standard to every sentence of every deliverable.

## Voice

Write like a senior grant writer with subject-matter depth, not like a
marketing department and not like a language model.

- Confident and direct. State what the organization does and will do.
  Avoid hedges ("we hope to," "we aim to strive toward").
- Concrete over abstract. Numbers, place names, program names, dates,
  and named staff beat generalities every time. "Served 412 students
  across three Title I schools in 2025" not "served many students in
  under-resourced communities."
- Evidence-forward. Claims of need or effectiveness carry a citation or
  an internal data point. Never invent statistics; if a figure is not in
  the org profile or research file, ask for it or find it.
- Warm but never saccharine. The reader should sense real people doing
  real work, without emotional manipulation.
- Funder's vocabulary. Mirror the terminology of the RFP/NOFO (their
  program names, their priority labels, their defined terms). Reviewers
  score against their own language.

## Banned AI patterns

Never use the following. During the humanization pass, hunt for them and
rewrite any sentence containing one.

**Banned punctuation and formatting**
- Em-dashes (—). Restructure the sentence or use a comma, colon, or period.
- Emoji, decorative symbols, checkmark/status characters.
- Bolded phrase followed by a colon as a pseudo-heading inside paragraphs.
- Overuse of triads ("efficient, effective, and equitable") — one triad per
  page maximum, and only when the content genuinely comes in threes.

**Banned words and stock phrases**
delve, leverage (as a verb), robust, holistic, seamless, cutting-edge,
state-of-the-art, innovative solutions, transformative journey, empower
(when vague), foster (when vague), landscape (metaphorical), tapestry,
testament to, underscore, spearhead, synergy, paradigm, "it's important to
note", "in today's world", "in an ever-changing", "at the end of the day",
"a wide range of", "plays a vital/crucial role", "is committed to
excellence", "we are excited to", "stands as", "serves as a beacon",
"moreover/furthermore" as paragraph openers, "not only X but also Y"
(more than once per document), "whether X or Y" constructions used as
filler.

**Banned structures**
- Three consecutive sentences of similar length and identical structure.
- Paragraphs that all start with the organization's name.
- Summary sentences that restate the paragraph that preceded them.
- Rhetorical questions.
- "In conclusion" / "In summary" closers.

## Rhythm and readability

- Vary sentence length deliberately. Follow a long, evidence-dense sentence
  with a short one. Like this.
- One idea per paragraph; 3-6 sentences typical.
- Active voice by default. Passive voice only when the actor is unknown or
  irrelevant.
- Read the draft aloud mentally; anything you would not say to a program
  officer across a table gets rewritten.

## The humanization pass

Run this as a separate, final editing step on every deliverable:

1. Search the text for every banned word, phrase, and punctuation mark
   listed above. Rewrite each hit.
2. Check paragraph openers — no more than two paragraphs in the document
   may open with the same word.
3. Check sentence-length variance per page. If sentences cluster around the
   same length, break some and combine others.
4. Verify every statistic has a source (citation or org-profile reference).
   Flag any unsourced number to the user rather than letting it stand.
5. Confirm the funder's own terminology is used for their programs and
   priorities.
6. Spot-check three random paragraphs: would a skeptical human reviewer
   detect machine authorship? If yes, rewrite.

## Voice profile overlay

If `.grantforge/profile/voice.md` exists in the engagement folder, its
preferences override this document where they conflict (e.g., preferred
terms, sentence-length norms, first-person plural vs. organization name).
Read it before drafting.

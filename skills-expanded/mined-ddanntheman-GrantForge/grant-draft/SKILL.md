---
name: grant-draft
description: >
  Write the grant application narrative. This skill should be used when the
  user says "draft the application", "write the need statement", "draft the
  project narrative", "write our response to section X", or after research is
  complete for a grant in the pipeline. Produces section drafts that answer
  the funder's prompts exactly, within limits, in the house style.
version: 0.1.0
---

# Grant Draft

Write narrative that a reviewer scores highly and a skeptic cannot identify
as machine-written. Draft section by section, never the whole application in
one pass.

## Before writing

Read, in order: the requirements matrix (`requirements.md`), the research
files (`research/evidence.md`, `research/funder.md`), the org profile
(`.grantforge/profile/organization.md`), the voice profile
(`profile/voice.md` if present), relevant boilerplate
(`profile/boilerplate/`), and the house-style skill. If research files are
missing, run grant-research first — drafting without an evidence base
produces assertions, not arguments.

## Section discipline

For each narrative section in the requirements matrix:

1. **Answer the verbatim prompt.** Reviewers score against their question,
   not against what the writer wished they had asked. Open the section by
   directly addressing the prompt's core ask; never open with org history
   unless the prompt asks for it.
2. **Respect the limit with headroom.** Draft to ~95% of the word/page/
   character limit. Report the count to the user with every draft. For
   portal submissions, count characters the way portals do (spaces
   included, unless the funder says otherwise).
3. **Load-bearing evidence.** Every claim of need or effectiveness cites an
   entry from `research/evidence.md`. Every capability claim traces to the
   org profile. Nothing invented, ever. Missing support becomes a question
   to the user, asked before drafting continues.
4. **Mirror the rubric.** Where the funder published scoring criteria,
   check the draft covers every scored element, weighted roughly by points.
5. **Adapt boilerplate, never paste it.** The answer library provides raw
   material; rewrite it to this funder's vocabulary, this project's facts,
   and this prompt's angle.

## Standard section craft

- **Need/problem statement**: local data first, national context second,
  one to two sentences of human texture. End with the gap this project
  fills — not with a pitch.
- **Project description**: what, who, where, when, how many, delivered by
  whom. Activities map visibly to objectives; objectives are measurable
  and time-bound (SMART without using the acronym).
- **Goals/objectives/outcomes**: distinguish outputs (what the org does)
  from outcomes (what changes). Give each objective a target, a measure,
  and a data source.
- **Evaluation plan**: who collects what data, with what instrument, on
  what schedule, and how findings feed back into the program. Name an
  evaluator if the budget includes one.
- **Organizational capacity**: prove it with track record, named staff
  qualifications, and financial stewardship facts (clean audits, past
  federal awards managed) — not adjectives.
- **Sustainability**: name realistic funding continuation paths; funders
  read "we will seek other grants" as no plan.
- **Timeline/logic model**: build as a table or exhibit when allowed;
  offer a logic model whenever the funder is federal or education-sector.

## Voice and format

Apply the house style throughout and run its humanization pass on every
section before showing it to the user. Then deliver in the formats the
requirements matrix calls for:

- **Word documents**: follow the funder's formatting rules exactly (font,
  margins, spacing, headers, page numbers). Use the docx toolchain.
- **Portal-ready sections**: plain text, one file per portal field, with
  the character/word count printed at the top of each.
- Save drafts to `drafts/`, finals to `final/` after grant-review clears
  them.

## Iteration

Draft one or two sections, show them, and absorb feedback before
continuing — early corrections propagate cheaply. Record user edits that
reflect standing preferences into `profile/voice.md`. After submission,
suggest harvesting the strongest sections into the boilerplate library.

---
name: botkits-top-edit
description: >-
  Use this as the last mechanical pass before publishing, to screen AI tells and
  house-style misses that a slop word-list can skip.
---
# Top edit

The final screen before publishing. Run it after botkits-no-ai-slop. It is a checklist, not a critique: flag, don't edit. Each flag gets a line number, the quoted text, and a fix.

## Pass 1: Leftover tells

Things that survive a slop pass because no single word gives them away:

1. "This" or "That" opening a sentence with no noun after it.
2. Paired constructions used as decoration (not only... but also, both... and).
3. Stacked connectors: moreover, furthermore, additionally, notably.
4. Hedges that dodge a position (it could be argued, in many ways, to some extent).
5. Even-handed "on the other hand" paragraphs that never land.
6. Signposting the piece instead of moving it (as we'll see, as mentioned above).
7. Consultant phrases: low-hanging fruit, move the needle, double-click on, circle back.
8. Every section ending the same way, or the same paragraph shape repeated.
9. A point restated in new words to look deeper.
10. Contrast reframes ("not X, but Y") more than twice in a long piece.
11. Stale metaphors (tip of the iceberg, perfect storm, double-edged sword).

## Pass 2: House style

- Opens on something concrete, not a thesis or a question.
- The one-sentence takeaway is findable.
- Every big claim has a named source (run botkits-source-check if not).
- Could anyone else have written this? If yes, flag where the writer's own detail is missing.
- Destination rules from botkits-no-ai-slop: em dashes, trailing periods on social posts, hyphens on LinkedIn, hashtags only at the end.
- Headline and first line don't say the same thing.

## Pass 3: Prose

- The same word three times in a few lines (unless it's the key term).
- Three or more passive sentences in a row.
- Five sentences in a row of about the same length.
- Links: every URL resolves and the anchor text says where it goes.

Some of these are fine on purpose. If breaking a rule makes the sentence better, leave it and say so.

## Verdict

**Clean** (0-2 small flags), **Quick fixes** (3-5), or **Needs work** (6+, or anything structural). One sentence of advice. When one pattern repeats a lot, show the first three and count the rest.

## After the verdict

Once the writer has read the report, offer two optional extras:

- **Voice bank.** Quote the one or two paragraphs that sound most like the writer at their best and say why. Offer to save them to their voice notes for future drafts.
- **Retro.** One line on what went well in this piece's pipeline and one thing to change next time.

## Inspired by

- [Nadiem Mahmoud, top-edit](https://github.com/nadiem99/claude-writing-skills/blob/5b52111e1bd30e93643929f17155e82aa26f771f/skills/pipeline/top-edit/SKILL.md) and its [AI tells checklist](https://github.com/nadiem99/claude-writing-skills/blob/5b52111e1bd30e93643929f17155e82aa26f771f/context/ai-tells-checklist.md) (MIT), which credit Every's Kate Lee. Does well: a three-pass mechanical screen, line-level flags, a verdict scale, and voice capture afterwards. Missing: flags every em dash and every sentence that starts with "But" or "And", and has no exception for rules broken on purpose.
- [George Orwell, Politics and the English Language](https://www.orwellfoundation.com/the-orwell-foundation/orwell/essays-and-other-works/politics-and-the-english-language/). Does well: the stale-metaphor rule and the final rule that you should break any rule rather than write something awful. Missing: no checklist or report form.
- [Hardik Pandya, stop-slop](https://github.com/hardikpandya/stop-slop) (MIT). Does well: a fast yes/no quick-check list. Missing: no house-style or destination checks.

## What this version adds

- Focus on tells that survive a word-list pass, so it does not repeat botkits-no-ai-slop.
- Destination checks (social punctuation, LinkedIn hyphens, hashtags) and a link check.
- An explicit "broken on purpose" exception.

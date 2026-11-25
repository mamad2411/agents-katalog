---
name: botkits-x-article
description: >-
  Use this when writing or rewriting an X Article (long-form on
  x.com/i/article), with images between sections, a first-line hook, and no
  invented numbers.
---
# X Article

Use for X Articles (x.com/i/articles or compose/articles), not tweets or 1/2/3/4 threads.

## Form

- Title is short and concrete.
- First line of the body is the hook. If it is weak, change the entry point before polishing. The title and the first line say different things.
- Research body: question → what you looked at → what you could measure → what you could not.
- Images sit between sections, not as a dump at the end. Diagrams that explain the next paragraph. No decoration. Cover is type-only, no product mascot on a founder/research piece.
- Closer is one usable line: a step the reader can take or a question you want answered, not a slogan or a two-beat kicker. Hashtags only at the end, 0 to 2 (`#buildinpublic` when it is actually build-in-public).

## Research rules

- No invented token counts, dollar figures, or quotes.
- Named instruments only (disk, chat volume, subagents, ad spend, HTTP bytes, git blobs).
- Do not recap ranking cards as the article. Cards support a finding.
- Source-check every claim. Unverified numbers come out.

## Pipeline

1. Outline (hook options, mechanism, evidence gaps).
2. Draft section by section.
3. Source-check.
4. No AI slop in Embedded mode (minimum change), then its `scripts/lint.py` on the final text. Check the fact lock: every number still matches botkits-source-check.
5. Write the promo post with botkits-social-copywriting (named thing in line 1, link placement per that skill).
6. Hand both drafts to whoever holds the account. Do not post.

## Voice

First person, specific, short sentences mixed with longer ones. No unrelated product-promo CTA on a founder/research Article. No press-release tone.

## Inspired by

- Dani Acosta's own X Article workflow. No outside source was verified, so none is credited (see [docs/credits.md](../../../docs/credits.md)). It builds on this repo's botkits-outline, botkits-draft, botkits-source-check, botkits-no-ai-slop, and botkits-social-copywriting skills.

## What this version adds

- A closer rule: end on a step the reader can take or a real question, not a slogan.
- The title and the first line must say different things.
- A lint and fact-lock check with botkits-no-ai-slop's `scripts/lint.py` before hand-off.
- A promo post written with botkits-social-copywriting, handed over with the Article draft.

---
name: writing
description: Writing rules for NLP/ACL paper prose. Use when writing, editing, shortening or rephrasing paper text (sections, abstract, captions, rebuttal or response text), or when checking prose for machine-written style.
---

How to edit and, on request, draft prose for an ACL paper. The authors write the paper; this skill makes their text clearer and keeps it theirs.

## Order of authority

1. `## Style` and `## Terminology` in the project's `CLAUDE.md`: the authors' own rules.
2. This skill and [ai-patterns.md](ai-patterns.md).
3. General academic English, in the variant set as `english` in `paper.config.json`.

## Asking

Formatting and wording questions often have several valid answers (table layout, caption style, notation, where a result goes, how strongly to phrase a claim). When neither `CLAUDE.md` nor the existing text settles one, ask with AskUserQuestion: the options, each with a short example, and your recommendation. Add the answer to `## Style` in `CLAUDE.md` when the user wants it to hold for the whole paper.

## Editing the authors' text

- Change as little as the goal needs. Keep the authors' terms, claims, structure and voice; fix what is unclear, wrong or reads as machine-written.
- Show each change as before → after with a one-line reason, unless the user asked for a direct rewrite.
- Every factual change to a claim about another paper goes through the `literature` skill: the claim must match the paper's body.
- Run the checks of [ai-patterns.md](ai-patterns.md) on every sentence you produce or touch.

## Drafting new text

Drafting is fine when the user asks for it. Work from their material: notes, results tables, bullet points, the existing sections. Mark the draft as a draft and point out each claim that still needs a citation or a number from their results. Write no results, numbers or citations that are not in their material or in a `read-full` paper.

## ACL conventions

- `\citet{}` when the authors are part of the sentence ("\citet{x} show ..."), `\citep{}` otherwise. Never an author-year in plain text.
- Introduce every abbreviation once with its spelled-out form, then use the abbreviation. Method, model and dataset names coined by a cited paper need no spelled-out form.
- Non-breaking space before references: `Table~\ref{...}`, `Section~\ref{...}`.
- Present tense for what the paper does and shows, past tense for what was run.
- Numbers in text match the tables exactly.
- The `Limitations` section states real limitations of this work. Current ARR rules on it (and on page limits, anonymity, AI assistance) come from the `guidelines-check` skill, never from memory.

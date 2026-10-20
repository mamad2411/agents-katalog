---
name: book-study-kit
description: "Generates ONE Anki flashcard file and ONE multiple-choice quiz file (plus its Anki-importable version) for an entire book, by triaging its chapters into real content vs. structural/metadata, running the pareto-study-kit curation per content chapter via parallel subagents, and merging everything into book-wide files sharing two Anki decks named after the book ('<Book> - Study' and '<Book> - Questions'), with per-chapter tags. Use when the user wants flashcards/quiz for a whole book or most of its chapters at once, not just one chapter — 'gera o anki do livro todo', 'flashcards do livro inteiro', 'quiz do livro completo', 'estuda esse livro todo com pareto'."
---

<!-- argument-hint: [path to book folder or un-split book PDF] -->

# Book Study Kit

Runs the `pareto-study-kit` curation across an entire book and produces
**one** flashcard file, **one** plain-text quiz file, and **one**
Anki-importable quiz file for the whole book — not one set per chapter.
All cards from every chapter share two Anki decks named after the book —
`<Book Title> - Study` for the flashcards, `<Book Title> - Questions` for
the quiz — regardless of how many chapters the book has; chapter identity
survives via a per-card tag and, in the quiz files, section headers — so
you keep the traceability of per-chapter curation without the clutter of
15-20 separate file sets to import and study one at a time.

This exists because generating a full study kit for every chapter uniformly
is itself a violation of Pareto thinking at the book level: some chapters
carry no teachable content (front matter, index, acknowledgments) and
running the full curation rubric on them wastes both your tokens and the
user's review time. Triage first, spend subagents only on what's real.

## Step 1 — Resolve the chapter files

- If given a folder of per-chapter files (e.g. the output of
  `pdf-chapter-splitter`), list its contents, sorted.
- If given a single un-split book PDF instead, first run the
  `pdf-chapter-splitter` skill on it to produce per-chapter files, then
  continue with that resulting folder.
- Note the book title (folder name, or the source PDF's own title/filename
  if not yet split) — you'll need it for Anki deck names and output
  filenames.

## Step 2 — Triage: conteúdo real vs. metadado

For every chapter file, decide **CONTENT** or **METADATA** *before*
spending a subagent on it. Build a small table (filename → verdict →
one-line reason) and show it to the user before launching anything —
cheap to eyeball now, expensive to redo after 15 subagents already ran on
the wrong set.

- **Near-certain METADATA, skip without even opening the file**: cover/front
  matter, table of contents, about-the-author(s)/reviewer, acknowledgments,
  dedication, index, glossary, bibliography/references, colophon.
- **Ambiguous names** (Introduction, Prologue, Preface, or any chapter far
  shorter than the book's median chapter length): don't decide from the
  title alone. Pull a quick text sample — first page or two via `pdftotext`
  on just that page range, or a couple of Read calls for a `.md` file — and
  judge on substance: does it teach a concept the rest of the book leans
  on, or is it purely operational (how the book is organized, marketing,
  author bios in prose form)? Judge the content, not the label.
- **Everything else** (numbered chapters with real subject matter): default
  to CONTENT without needing to pre-read it — the per-chapter subagent in
  Step 3 will do the real reading and curation anyway.

## Step 3 — Fan out one subagent per CONTENT chapter

Launch every CONTENT chapter's subagent in the **same message** (multiple
Agent tool calls together) so they run in parallel — they're fully
independent until the merge step. Use `general-purpose` as the subagent
type (needs Read, Bash, and Skill access).

Each subagent starts with zero context — the prompt must be entirely
self-contained. Template:

```
Curate a Pareto (80/20) study kit for one chapter of a book.

Book: "<Book Title>"
Chapter: "<NN - Chapter Title>"
File: <absolute path>

Load the `pareto-study-kit` skill and follow its rubric to identify the
vital 20% (its Step 2), size the kit (Step 3), and write the flashcards
(Step 4), multiple-choice questions (Step 5), and the Anki-importable
version of the quiz (Step 5b) — including its pt-BR language rule
(technical terms stay in whatever language practitioners in this field
actually use them in), its self-containment rule (every card/question must
name its real subject, never rely on "o capítulo" alone), and its "The
subject is the material, never the book" rule (never test chapter numbers,
reading order, what a chapter covers, or the book's structure — if the book
vanished, the answer must still be true and usable).

You are running in BATCH MODE (see that skill's "Modes" section): do not
write any files, do not print a standalone report. Instead, return your
final answer as exactly these four labeled blocks:

FLASHCARDS:
<tab-separated Front\tBack lines only, no header directives, one per line>

QUESTIONS:
<the plain-text multiple-choice block for this chapter only, numbered
starting at 1>

QUESTIONS_ANKI:
<the AllInOne-note-type rows for this chapter's questions — the 11 note
fields only (Question through Extra 1), tab-separated, no header
directives, one row per question>

SUMMARY:
<2-4 sentences in pt-BR: what was cut and what was kept for THIS chapter
specifically, naming real concepts from it — not generic labels>
```

## Step 4 — Merge into book-wide files

Read `pareto-study-kit`'s "Anki import mechanics" section before this step
— the short version: deck and tags are set by numbered header directives
(`#deck column:N`, `#tags column:N`), never by naming a column
"Deck"/"Tags" inside `#columns:` (that's cosmetic only and does nothing),
and every tag must be a slug with no literal spaces (Anki splits tags on
whitespace — an un-slugified title becomes a pile of garbage one-word
tags). Within a file, every chapter shares the same Deck value — the book
title plus the suffix for that file's kind of material (`- Study` for
flashcards, `- Questions` for the quiz); Tags is the only thing that varies
per chapter.

**Flashcards** — one file, header written once, then every subagent's
FLASHCARDS rows with two constant/per-chapter columns appended:

```
#separator:tab
#html:false
#notetype:Basic
#deck column:3
#tags column:4
<front>	<back>	<Book Title> - Study	<capitulo-nn-slug>
<front>	<back>	<Book Title> - Study	<capitulo-nn-slug>
...
```

`<Book Title> - Study` is identical on every row (one flat deck for the
whole book's flashcards, per the user's explicit call — no `Book::Chapter`
subdecks).
`<capitulo-nn-slug>` varies per chapter, e.g. `capitulo-07-basic-concepts`
— slugified from that chapter's own filename/title (lowercase, every run
of non-alphanumeric characters collapsed to one `-`).

**Questions (plain text)** — one file, a chapter heading before each
subagent's QUESTIONS block, question numbers renumbered continuously
across the whole file (not reset per chapter):

```
Quiz — <Book Title>
Baseado nos 20% de conceitos com maior valor de aprendizado de cada capítulo.

== Capítulo NN: <Chapter Title> ==

1) ...
Resposta: ...

2) ...

== Capítulo NN+1: <Chapter Title> ==

3) ...
```

**Questions (Anki-importable)** — one file, same `deck column`/
`tags column` mechanism as the flashcards file, built from every
subagent's QUESTIONS_ANKI rows (each already 11 tab-separated fields —
Question through Extra 1, per `pareto-study-kit`'s Step 5b) with the same
two extra columns appended:

```
#separator:tab
#html:false
#notetype:AllInOne (kprim, mc, sc)
#deck column:12
#tags column:13
<question>	<chapter title>	2	<Q_1>	<Q_2>	<Q_3>	<Q_4>		<Answers>	<Sources>	<Extra 1>	<Book Title> - Questions	<capitulo-nn-slug>
...
```

The Deck value here is `<Book Title> - Questions`, deliberately a different
deck from the flashcards file's `<Book Title> - Study`, so quiz questions
don't land in the same review queue as the recall cards. `Sources` keeps
the bare book title — it's a citation, not a deck name.

Mention in the final report that this file requires the "Multiple Choice"
add-on (zjosua, AnkiWeb code
[1566095810](https://ankiweb.net/shared/info/1566095810)) installed
before import.

## Step 5 — Where to save

One set of files for the whole book, not per chapter:
- `<book folder>/study/<Book Title> - Flashcards.txt`
- `<book folder>/study/<Book Title> - Questoes.txt`
- `<book folder>/study/<Book Title> - Questoes-Anki.txt`

## Step 6 — Self-check before finishing

- Confirm every flashcard row has exactly 3 tabs (4 columns: Front, Back,
  Deck, Tags) and every Anki-quiz row has exactly 12 tabs (13 columns), no
  stray tab/newline inside any field.
- Confirm both TSV files' header lines actually contain `#deck column:N`
  and `#tags column:N` with `N` matching that file's real column count —
  this is the exact mistake that broke a prior run (a column merely named
  "Deck"/"Tags" inside `#columns:` does nothing; only these numbered
  directives do).
- Confirm every tag value is a slug (no literal spaces) and every Deck
  value is identical across all rows in a file — `<Book Title> - Study` in
  the flashcards file, `<Book Title> - Questions` in the Anki-quiz file, and
  never the bare book title in either.
- Spot-check the merged files for questions about the book instead of about
  the subject — grep the front/question text for `capítulo`, `seção`,
  `parte `, `até agora`, `mais adiante`; any hit that makes the book's
  structure the answer must be rewritten around the concept or dropped
  (this survives the per-chapter check surprisingly often, because a
  chapter's own roadmap paragraph reads like author-flagged vital content).
- Confirm question numbers are unique and sequential across the merged
  plain-text quiz file, and that every `Answers` value in the Anki-quiz
  file has exactly one `1` among its four flags.
- Confirm the number of chapters represented in the output files matches
  the number of chapters marked CONTENT in Step 2 (a missing chapter means
  a subagent failed silently — don't merge partial output without flagging
  it to the user).

## Step 7 — Report the whole-book curation

Same reporting bar as `pareto-study-kit`'s own Step 8 — content-driven, not
a fixed template, no closing "should I continue?" question, written in
pt-BR — but at the book level:

1. **Triage recap** — which chapters were skipped as metadata and why
   (from Step 2's table), and how many chapters were run through the full
   curation.
2. **Per-chapter summaries** — fold in each subagent's SUMMARY block,
   chapter by chapter, so the user can audit the whole book's curation
   without opening every flashcard.
3. **Totals** — how many flashcards and questions came out, and whether any
   chapter came back thin or failed (per Step 6's check) so the user knows
   to look at it manually if so.

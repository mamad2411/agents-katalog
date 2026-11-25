---
name: book-to-anki
description: "Builds the complete Anki study kit for an ENTIRE book: one flashcard file, one plain-text quiz and one Anki-importable quiz, by triaging chapters into real content vs. front/back matter, running the pareto-study-kit 80/20 curation on each content chapter via parallel subagents, then merging and validating everything with a bundled script into two decks named after the book ('<Book> - Study' and '<Book> - Questions'), tagged per chapter and per tier (nucleo/complementar/periferico), and finally auditing the deck's quality with anki-deck-audit before reporting. Current, script-validated version of this pipeline — prefer it over book-study-kit. Use when the ask covers a whole book or most of its chapters, not a single chapter — 'gera o anki do livro todo', 'flashcards do livro inteiro', 'quiz do livro completo', 'estuda esse livro todo com pareto'."
argument-hint: "[path to book folder or un-split book PDF]"
allowed-tools: Read, Write, Glob, Bash(python3:*), Bash(pdftotext:*), Bash(ls:*), Bash(mkdir:*)
---

# Book to Anki

Runs the `pareto-study-kit` curation across an entire book and produces
**one** flashcard file, **one** plain-text quiz file, and **one**
Anki-importable quiz file for the whole book — not one set per chapter. All
cards share two decks named after the book (`<Book> - Study`,
`<Book> - Questions`); chapter identity survives as a per-card tag and as
section headers in the quiz. You keep per-chapter curation traceability
without 15-20 separate file sets to import and study one at a time.

Three things are deliberately not left to judgment, because all three have
failed real runs before: chapters that carry no teachable content never get a
subagent spent on them and every remaining chapter gets a **tier and a card
budget** (Step 2), the merge/validation of ~200 TSV rows is done by a script
rather than by eyeballing (Steps 4-5), and the finished deck is measured for
quality before you report it (Step 6).

The failure Step 2's tiering and Step 6's audit exist for: a 26-chapter
Kubernetes book produced 533 cards where every chapter — the closing "what to
read next" chapter, the four Docker prerequisite appendices, and the chapter
on Pods alike — came back with 18 to 28 cards. The 80/20 had run inside each
chapter and never between them, and nothing measured that 43% of the answers
bundled several facts. Both files imported cleanly.

**Division of labor** — you triage and orchestrate; each subagent reads one
chapter and writes that chapter's partials; `scripts/anki-kit.py` merges,
appends deck/tag columns, renumbers, and validates. Never hand-assemble the
final files: the script owns the header directives and column positions.

## Step 1 — Resolve the chapter files

- Folder of per-chapter files (e.g. `pdf-chapter-splitter` output): list it,
  sorted.
- Single un-split book PDF: run the `pdf-chapter-splitter` skill on it
  first, then continue with the resulting folder.
- Note the **book title** (folder name, or the source PDF's title/filename)
  — it becomes both deck names and all three output filenames.
- Create a partials directory for this run and keep the path:
  `<book folder>/study/.partials/`.

## Step 2 — Triage: descarte, depois camada e budget

Two decisions per chapter file, *before* spending a subagent on it. Show the
user one table (filename → verdict → camada → budget → one-line reason)
before launching anything — cheap to eyeball now, expensive to redo after 15
subagents ran on the wrong set.

### 2a — METADATA vs. CONTENT

- **Near-certain METADATA, skip without opening the file**: cover/front
  matter, table of contents, about-the-author(s)/reviewer,
  acknowledgments, dedication, index, glossary, bibliography/references,
  colophon.
- **Ambiguous names** (Introduction, Prologue, Preface, or any chapter far
  shorter than the book's median chapter length): don't decide from the
  title. Sample the text — `pdftotext` on just the first page or two, or a
  Read call for `.md` — and judge on substance: does it teach a concept the
  rest of the book leans on, or is it purely operational (how the book is
  organized, marketing, author bios in prose)? Judge the content, not the
  label.
- **Everything else** (numbered chapters with real subject matter): default
  to CONTENT without pre-reading — the subagent does the real reading.

### 2b — Camada e budget para cada capítulo CONTENT

Binary CONTENT/METADATA is what produced the flat 533-card deck: every
surviving chapter got the same treatment. Sort each one into a tier, which
fixes its flashcard budget:

| Camada | Critério | Budget |
| --- | --- | --- |
| **nucleo** | o que qualquer pessoa que trabalha com o assunto do livro usa toda semana; os capítulos que dão nome ao livro | 14-20 |
| **complementar** | assunto real do livro, mas de uso ocasional, avançado ou de um nicho | 8-12 |
| **periferico** | pré-requisito que não é o assunto do livro (os apêndices de Docker num livro de Kubernetes), tooling de um fornecedor só, projeto obsoleto, capítulo de encerramento/critérios de adoção | 4-6 |

Decide from the chapter title and the book's own structure — you do not need
to read the chapters to know that "Never the end" and "Appendix A —
Packaging applications into Docker Images" are not núcleo in a Kubernetes
book. When a title genuinely doesn't say, sample its first page like 2a does.

Two sanity checks on the resulting split, before you launch anything:

- **Não faça tudo núcleo.** A book whose every chapter is núcleo has not been
  triaged. Expect roughly a third of the CONTENT chapters there; the
  validator warns above 45% of the finished deck.
- **Some periférico is normal and healthy.** Prerequisite appendices and
  closing chapters exist in most technical books. Cutting their budget from
  20 to 5 is the single biggest win this step delivers.

If the user disagrees with a tier, that is exactly what the table is for —
re-tier and re-run only the affected chapters.

### 2c — Write the tier map

The merge script reads the tiers from disk, so they can't drift from what you
showed the user. Write `<partials dir>/tiers.tsv`, one line per CONTENT
chapter, `<chapter file basename without extension><TAB><camada>`:

```
06 - Week 1 - Ch1 - Before you begin	complementar
07 - Week 1 - Ch2 - Running containers in Kubernetes with Pods and Deployments	nucleo
28 - Appendix A - Packaging applications from source code into Docker Images	periferico
```

The basename must match the partial filenames exactly — same string the
subagent gets in Step 3. A chapter with a partial and no tier is a merge
error, not a silent default.

## Step 3 — Fan out one subagent per CONTENT chapter

Launch every CONTENT chapter's subagent in the **same message** (multiple
Agent tool calls together) so they run in parallel — they are fully
independent until the merge. Use `general-purpose` (needs Read, Bash, Write,
and Skill access). Above ~15 chapters, launch in batches of 12-15 rather
than all at once.

The prompt template is in
[references/subagent-prompt.md](references/subagent-prompt.md) — read it and
copy it verbatim, substituting the placeholders, **including this chapter's
camada and budget from Step 2b**. A subagent that is not told its budget
writes ~20 cards for every chapter; that is the whole failure this pipeline
now guards against, and the merge script warns when one overshoots. Each
subagent gets zero context, so the prompt must carry everything, and it
deliberately overrides
one line of `pareto-study-kit`'s batch mode: subagents **write partial files
and return only a summary**, instead of returning the rows inline. That
keeps ~200 rows of TSV out of your context and makes a failed run
resumable — chapters whose partials already exist don't need re-running.

Partials land in the Step 1 directory, three per chapter, named after the
chapter file: `<NN - Title>.flashcards.tsv`, `<NN - Title>.questions.txt`,
`<NN - Title>.questions-anki.tsv`. No headers, no deck column, no tags
column — Step 4 appends those.

## Step 4 — Merge into the book-wide files

```
python3 ${CLAUDE_SKILL_DIR}/scripts/anki-kit.py merge \
  --partials "<book folder>/study/.partials" \
  --book "<Book Title>" \
  --out "<book folder>/study"
```

Writes the three final files, appends the constant deck column and the two
tags (chapter slug + camada, read from `tiers.tsv`), renumbers the plain quiz
continuously across the book, and prints per-chapter counts plus the card
split across the three camadas. It exits non-zero and lists every structural
problem it found (wrong field count, bad `Answers` flags, a chapter missing
one of its three partials, a chapter with no tier). Fix the offending
partial — re-running one subagent is cheap — and merge again; do not
hand-edit merged output.

It also prints an `AVISO` for any chapter whose flashcard count overshot its
tier's ceiling. That is a subagent that ignored its budget: re-run that one
chapter with the budget restated, rather than letting the inflation into the
merged book.

The format it produces, and the Anki import rules behind it, are documented
in [references/anki-format.md](references/anki-format.md). Read that file
before changing anything about the layout or diagnosing an import that
landed in the wrong deck.

## Step 5 — Validate before reporting

```
python3 ${CLAUDE_SKILL_DIR}/scripts/anki-kit.py validate \
  --dir "<book folder>/study" \
  --book "<Book Title>" \
  --expect-chapters <number of CONTENT chapters from Step 2>
```

Checks the header directives, column counts, deck constancy, tag slugs,
`Answers` flags, continuous question numbering, flashcard/quiz chapter
coverage, and `--expect-chapters` (a mismatch means a subagent failed
silently — never ship partial output without flagging it).

It also prints `AVISO` lines for cards whose text mentions `capítulo`,
`seção`, `parte`, `até agora`, `mais adiante`. These are warnings, not
errors, and they need **your** judgment: a card whose answer is a fact about
the book's structure must be rewritten around the underlying concept or
dropped; a card that merely uses the word "parte" in ordinary prose is fine.
This check catches real misses surprisingly often, because a chapter's own
roadmap paragraph reads like author-flagged vital content.

## Step 6 — Audit the finished deck

Structural validity is not quality. Step 5 passing means the file imports;
this step asks whether it was worth generating. Invoke the `anki-deck-audit`
skill on the output — it is the final gate, and it is not optional:

```
python3 ${CLAUDE_SKILL_DIR}/../anki-deck-audit/scripts/deck-audit.py \
  --dir "<book folder>/study" --book "<Book Title>"
```

It measures answer length, the share of answers bundling several facts,
enumerative and double-barreled fronts, near-duplicates, the per-chapter
distribution (a low CV means the tiering in Step 2b didn't take), the camada
split, and the study-hour cost of the deck as generated.

- **Exit 0, no `REPROVADO`** — go to Step 7 and fold the headline numbers
  (total, camada split, hours per pass) into the report.
- **Any `REPROVADO`** — do not ship it quietly. The offending cards belong to
  identifiable chapters (the script prints line numbers; tags give you the
  chapter). Re-run those chapters' subagents with the failing rule restated,
  re-merge, re-audit. Re-running three chapters is cheap; a 500-card deck
  nobody can grade honestly is not.
- **`AVISO` about a flat distribution or an oversized núcleo** — that is a
  Step 2b problem, not a subagent problem. Re-tier and re-run the chapters
  whose camada changed.

Only after this is clean: delete the `.partials/` directory.

## Step 7 — Report the whole-book curation

Same bar as `pareto-study-kit`'s Step 8 — content-driven, no fixed template,
no closing "quer que eu continue?" question, written in pt-BR — but at book
level:

1. **Triage recap** — which chapters were skipped as metadata and why, and
   the camada each surviving chapter landed in (Step 2's table), with the
   reasoning for anything demoted to periférico. This is the part the user
   can actually contest.
2. **Per-chapter summaries** — fold in each subagent's SUMMARY, chapter by
   chapter, so the user can audit the curation without opening every card.
3. **Totals and honesty** — flashcard/question counts from the validator, the
   camada split with percentages, and the audit's study-cost numbers (hours
   per full pass, hours to mature). Name any chapter that came back thin,
   failed, overshot its budget, or needed a rewrite after a Step 5 warning or
   a Step 6 `REPROVADO`.
4. **How to actually study it** — the tier tags are useless if the user
   doesn't know they exist: tell them to start with `tag:nucleo` in Anki and
   leave `tag:periferico` suspended until the core is mature, and give the
   hour cost of the núcleo alone versus the whole deck.
5. **Import note** — the `Questions-Anki.txt` file needs the "Multiple
   Choice" add-on (zjosua, AnkiWeb code
   [1566095810](https://ankiweb.net/shared/info/1566095810)) installed in
   Anki 2.1.55+ *before* import; a missing note type fails the whole import
   rather than degrading.

A report that could be copy-pasted onto a different book has failed — it
must name real concepts from *this* one.

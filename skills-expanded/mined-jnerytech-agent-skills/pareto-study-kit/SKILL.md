---
name: pareto-study-kit
description: "Generates Anki-importable flashcards and 4-option multiple-choice quiz files from a chapter (PDF or Markdown), focused on the 20% of the content that drives 80% of the learning value (Pareto principle). Use when the user asks for flashcards, Anki cards, quiz/múltipla escolha, resumo de estudo, or study material based on 80/20 from a chapter/book/text. Also used internally, one call per chapter, by the `book-to-anki` skill when the ask is for a whole book instead of one chapter."
argument-hint: "[path to .pdf or .md chapter] [optional: output folder]"
allowed-tools: Read, Write, Glob, Bash(pdftotext:*), Bash(mkdir:*), Bash(python3:*)
---

# Pareto Study Kit

Turns one chapter (PDF or Markdown) into study files, all scoped to the
**20% of the material that drives 80% of the learning outcome** — not a full
summary, not full coverage of every fact.

Output per chapter:
- `<chapter> - Study.txt` — Anki-importable TSV, Basic note type.
- `<chapter> - Questions.txt` — 4-option multiple choice, plain text, answer
  key inline after each question. No dependency: opens in any editor.
- `<chapter> - Questions-Anki.txt` — the same questions as real interactive
  Anki cards, via the community add-on "Multiple Choice" (zjosua, AnkiWeb
  code [1566095810](https://ankiweb.net/shared/info/1566095810),
  [github.com/zjosua/anki-mc](https://github.com/zjosua/anki-mc)). That
  add-on must be installed before import, which is exactly why the plain
  `Questions.txt` also exists.

The filenames mirror the deck names — `- Study` for the flashcards,
`- Questions` for the quiz — so a file on disk and a deck in Anki are never
two different names for the same thing.

Selecting "the 20%" and writing good cards is judgment, not a script — you
read the chapter and apply the rubric below. Nothing extracts the vital few
automatically.

## Modes: standalone vs. batch

**Standalone (default)** — the user asked for one chapter directly. Follow
every step below, including Step 6 and Step 8, both specified in
[references/standalone-output.md](references/standalone-output.md).

**Batch** — you were launched as a subagent by `book-to-anki` (or another
multi-chapter orchestrator); the calling prompt says so explicitly. Steps
1-5b are unchanged; what happens to the output is not. Read
[references/batch-mode.md](references/batch-mode.md) before writing anything
— it defines both output variants (inline rows vs. partial files) and which
columns you must *not* emit.

## Language: pt-BR, with universal technical terms kept in English

Write every flashcard and quiz question in **pt-BR**, whatever the source
language. Keep a term in English when it is the term practitioners in that
specific field actually use day to day — proper nouns (tool/product/API/
framework/method names) and jargon that circulates untranslated in Brazilian
professional communities for that field (which field depends entirely on the
chapter's subject: software, finance, medicine, law…). Translate everything
else: connective prose, definitions, explanations of *why*.

Never force a translation no Brazilian practitioner in that field would say
just to be consistent — that produces a worse card, not a more correct one.
In doubt, prefer whatever term shows up in Brazilian blogs, docs, courses,
and talks for that exact concept in that exact field.

## Step 1 — Get the chapter as text

- **`.md` input**: read the file directly.
- **`.pdf` input**: don't burn the Read tool's per-request page cap or spend
  vision tokens on a text-heavy chapter. Extract with poppler first, then
  read the resulting `.txt`:
  ```
  pdftotext -layout "chapter.pdf" /tmp/.../chapter.txt
  ```
  `-layout` preserves columns and tables reasonably well, which matters for
  data tables and code listings.

## Step 2 — Identify the vital 20%

Read the whole chapter, then extract candidates into these buckets, in
priority order:

1. **Explicit author signals** — anything the author already flagged as
   important: "Rule N" boxes, chapter summaries, "key takeaway" callouts,
   bolded/italicized definitions, warnings. Pre-filtered 80/20 content —
   always include.
2. **Core mental models / definitions** — the 2-5 concepts the rest of the
   chapter is built on. Remove the concept and later sections stop making
   sense.
3. **Actionable cause → effect / trade-offs** — "if X, then Y, so do Z"
   statements a reader would actually apply later: a tuning decision, a
   debugging heuristic, a rule of thumb with a concrete threshold.
4. **Named tools/APIs/commands** — only when they *are* the point of the
   section ("use tool X for scenario Y"), not passing mentions in a list of
   alternatives.

Explicitly exclude: historical trivia, exhaustive tool/vendor lists with no
differentiating information, redundant restatements, minor code syntax not
tied to a principle, marketing-style asides.

Also exclude, even when the author spends pages on it — this is content that
*is* teachable and still doesn't belong in a deck about this subject:

- **Prerequisite technology that is not the book's subject.** A Kubernetes
  book's Docker appendices teach Docker. Cards about them dilute a Kubernetes
  deck and belong to a Docker deck, if anywhere.
- **Obsolete or single-vendor tooling** the reader is unlikely to meet — a
  dead project, a product that lost its market, a tool the author picked only
  to demonstrate a category. Card the *category* ("what does a serverless
  platform on Kubernetes give you?"), not the tool's flags.
- **Buying/adoption criteria and closing chapters** — how to choose a
  managed platform, what to read next, how the community is governed. That is
  advice consumed once, not knowledge worth spaced repetition.

Prefer a small set of high-leverage items over broad coverage — 12 sharp
flashcards beats 40 that dilute the vital few with trivia.

## Step 3 — Size the kit to the chapter's tier, then its density

**Tier first.** A chapter's card budget is set by how much of it the reader
will actually use, not by how many pages it has. In batch mode the caller
assigns the tier and the budget — use exactly what it gives you. In
standalone mode, decide it yourself from the chapter's role in its book:

| Camada | O que é | Budget de flashcards |
| --- | --- | --- |
| **núcleo** | conceitos que quem trabalha com o assunto usa toda semana | 14-20 |
| **complementar** | assunto real, mas de uso ocasional ou avançado | 8-12 |
| **periférico** | pré-requisitos, tooling de um fornecedor só, capítulos de encerramento/adoção | 4-6 |

Quiz questions stay at about half the flashcard count, whatever the tier.

**Density second**, inside the tier's range: a dense chapter of a tier lands
at the top of its band, a thin one at the bottom. If Step 2 produced fewer
high-value items than the floor of the band, ship fewer cards — never pad to
hit a number. The failure this replaces is exactly that padding: every
chapter of a 26-chapter book coming back with 18-28 cards, closing chapter
and core chapter alike, so the 80/20 happened inside chapters and never
between them.

## Every card and question must be self-contained

Never write a prompt that only makes sense with "the chapter" already in
mind — "Qual é o conselho final do capítulo sobre standards emergentes?" is
unanswerable on its own: *which* chapter, *which* standards? A card gets
studied in Anki completely detached from the table of contents, often mixed
with cards from other chapters and other books. Name the actual subject
inline instead of pointing at its container:

- Bad: "O que o autor recomenda sobre isso?" / "Qual a conclusão desta
  seção?"
- Good: "Segundo [autor/livro], qual prática reduz [problema concreto
  nomeado]?" — naming the real concept, technology, rule, or scenario, never
  a positional reference to where it sits in the source.

Attribution like "Segundo Stoneman" is allowed only as *framing* around a
fact that would still be true and useful if the book didn't exist. It never
licenses making the book itself the subject — see the next rule.

This matters even more outside standalone mode: `book-to-anki` merges every
chapter of a book into one file, so "este capítulo" is ambiguous the moment
more than one chapter's cards share a deck.

## The subject is the material, never the book

Self-containment is necessary but not sufficient: a question can name real
concepts and still be worthless because what it tests is the *book's
structure*. A real failure of exactly this kind — "Quais são os resources
básicos do Kubernetes que Stoneman diz serem dominados até o capítulo 6?" It
names Kubernetes, resources, and the author, so it slips past the
self-containment rule, but all it measures is whether the reader memorized
the table of contents. That does not help anyone run a cluster; it is
editorial trivia in a technical costume.

Never make any of these the thing being asked:

- Chapter numbers, ordering, or what a given chapter covers/introduces.
- Reading progression — what the reader "already learned", "will see later",
  "has mastered so far", what a part builds toward.
- The book's pedagogy or packaging — page counts, lab/exercise structure,
  why the author sequenced topics this way, what the preface promises,
  appendix contents.
- The author's meta-commentary about the book, as opposed to their technical
  claims about the subject.

The test, applied to every card before it ships: **if the book vanished,
would the answer still be true and usable?** If the answer is a fact about a
document rather than about Kubernetes/DI/FIIs/whatever the subject actually
is, cut it and write a question about the underlying concept instead.

- Bad: "Quais resources o autor cobre até o capítulo 6?" (fato sobre o livro)
- Good: "Quais resources do Kubernetes um Deployment cria e gerencia por
  baixo para manter réplicas rodando?" (fato sobre o assunto)

This also constrains Step 2: an author's roadmap paragraph ("by the end of
this chapter you'll know…") is a *pointer* to vital content, not vital
content itself. Follow the pointer to the concept it names and build the
card from the concept.

## One card, one fact — the hard limits

"Atomic card" is the rule everyone agrees with and nobody enforces, so here
it is as numbers. A real deck failed all four at once: 43% of its answers
bundled independent facts, 10% of its fronts asked for a list, 19% asked two
questions, and the average answer ran 207 characters. Those cards are not
harder to review — they are *impossible* to grade honestly, because you
always get part of it right.

**Limits, checked mechanically by `anki-deck-audit`:**

| Regra | Limite |
| --- | --- |
| Resposta média do lote | <= 150 chars |
| Resposta individual | <= 200 chars, no máximo 2 frases |
| Respostas compostas (>=3 frases ou `;`) | <= 20% do lote |
| Perguntas enumerativas | <= 5% do lote |
| Perguntas duplas | zero |

**Never bundle with a semicolon or a second sentence.** If the answer needs
a `;` to hold two facts together, it is two cards. A subordinate clause that
qualifies *one* fact ("...porque o kubelet reinicia o container no mesmo
node") is fine; a second independent statement is not.

**Never ask for a list.** "Quais são as três reações automáticas do
Kubernetes?" fails in SRS forever: forget one item of three and you must mark
it wrong, so the card never matures. Two ways out, both better than the list:

- One card per item, each asking *when* it applies:
  "O que o Kubernetes faz quando um node cai levando os containers junto?" →
  "Sobe containers substitutos em outros nodes."
- One card for the *criterion* behind the list, if the items share one:
  "Que classe de falha o self-healing do Kubernetes cobre sem intervenção?"

The same applies to "Quais são os campos mínimos de um manifest de Pod?" —
either card the single field that people actually get wrong, or make it a
quiz question, where a list has a place. The quiz can enumerate; the deck
cannot.

**Never ask two things in one front.** "Do que é composto um cluster e como
você o trata no dia a dia?" has no single answer. The tell is a front joined
by ` e ` before a second interrogative, or containing two `?`. Split it.

**Front short, back shorter.** The front names the situation and asks one
thing. The back is the fact — no restatement of the question, no "isso
acontece porque..." wind-up, no second fact bolted on with "e também".

## Anki import mechanics: Deck and Tags (read before Step 4 and 5b)

Two rules, learned from a real failed import — get both right or the file
silently imports into whatever deck happened to be selected, with garbage
tags:

1. **Deck and tags are set by numbered column directives, never by naming a
   column "Deck" or "Tags" inside `#columns:`.** `#columns:` is cosmetic: it
   labels columns in the import preview dialog and changes no behavior. Only
   `#deck column:N` and `#tags column:N` bind (`N` = 1-indexed position,
   counting every column). Prefer `deck column` over a bare `#deck:<name>`
   header even when every row shares one deck — `deck column` is documented
   to create the deck if missing, while the bare header only "presets the
   deck, if it exists".
2. **A single tag must never contain a literal space.** Anki splits the tag
   field on whitespace, so `Enterprise Integration Patterns` becomes three
   garbage one-word tags. Slugify every tag: lowercase, accents stripped,
   each run of non-alphanumerics collapsed to one `-`, no leading/trailing
   `-`. Example: `12 - Part 4 - Ch12 - DI Container introduction.pdf` →
   `capitulo-12-di-container-introduction`. A literal `::` may stay (Anki
   reads it as a hierarchical tag on purpose).

   That splitting is also the feature: the tag field carries **two** tags
   separated by one space — the chapter slug and the tier from Step 3
   (`nucleo`, `complementar` or `periferico`):
   `capitulo-04-configuring-applications-with-configmaps-and-secrets nucleo`.
   The tier tag is what makes the 80/20 usable *after* import — the reader
   studies `tag:nucleo` first and leaves `tag:periferico` suspended — so it
   is not optional. In batch mode the merge script appends both from the
   tier map; never emit them yourself there.

**Deck names: exactly two per book** — `<Book Title> - Study` for flashcards,
`<Book Title> - Questions` for the quiz. Never the bare book title (both
files would land in one deck, mixing recall cards into the quiz review
queue), never `Book::Chapter` subdecks. Chapter identity lives in the tag,
in both modes.

**Getting the book title in standalone mode**: it is the name of the folder
containing the chapter file — that is what `pdf-chapter-splitter` produces.
When that folder name is not a book title (a chapter sitting loose in
`Downloads/`), ask the user instead of guessing: a wrong deck name silently
splits their collection in two, and renaming decks afterwards is manual
work. For a standalone document that belongs to no book, use the document's
own title and keep both suffixes. In batch mode the orchestrator supplies
the title — never re-derive it.

## Step 4 — Write the flashcards (Anki TSV)

Header directives first, then one card per line, tab-separated, no extra
header row:

```
#separator:tab
#html:false
#notetype:Basic
#deck column:3
#tags column:4
<Front>	<Back>	<Book Title> - Study	<capitulo-slug> <camada>
```

Rules:
- **The hard limits above bind here**: <= 200 chars and <= 2 sentences per
  answer, no `;` joining independent facts, no enumerative front, no double
  front. Re-read that section if you are about to write a long answer.
- Front is a real question ("Why does X cause Y?", "What's the difference
  between X and Y?"), not a fragment to fill in. Back is the answer only —
  don't restate the question.
- Rephrase instead of copy-pasting sentences: optimize for recall, not
  recognition. A card that reproduces the author's paragraph is how answers
  end up at 200+ chars.
- No literal newline or tab inside a field. With `#html:false` every field
  is a single plain line; `<br>` only works under `#html:true`, which this
  skill does not set.
- Favor "why/how" and comparison cards for the core mental models over plain
  "what is X" recall cards.
- Front must be self-contained and about the subject, not the book.

## Step 5 — Write the multiple-choice quiz

```
1) <question text>
A) <option>
B) <option>
C) <option>
D) <option>
Resposta: <letter> — <one-line justification>
```

Rules:
- Exactly one option clearly correct; the other three *plausible* — real
  misconceptions or partially-true statements, never joke distractors.
- Every question comes from a Step 2 item. No trivia about page numbers,
  version numbers or vendor names unless that number *is* the vital fact
  (a threshold the author calls out).
- The answer key goes inline right after its own question, never collected
  in a section at the end.
- Question text self-contained and about the subject, not the book.
- This is where enumerations belong. A "quais das opções abaixo..." question
  works with four fixed options in front of the reader; the same content as a
  flashcard never matures. Content you cut from the deck for being a list is
  a natural quiz question.

## Step 5b — Write the Anki-importable version of the same quiz

Same questions as Step 5, formatted for the "Multiple Choice" add-on's note
type so the quiz becomes real interactive cards (radio buttons, auto-graded,
works on desktop, mobile and AnkiWeb) instead of something only readable
linearly. The add-on's note type is literally named
`AllInOne (kprim, mc, sc)`, with these fields in this exact order — the
parenthetical in the QType field name is part of the literal name:

```
Question | Title | QType (0=kprim,1=mc,2=sc) | Q_1 | Q_2 | Q_3 | Q_4 | Q_5 | Answers | Sources | Extra 1
```

```
#separator:tab
#html:false
#notetype:AllInOne (kprim, mc, sc)
#deck column:12
#tags column:13
<question>	<chapter title>	2	<A>	<B>	<C>	<D>		<0 1 0 0>	<Book — Chapter>	<justificativa>	<Book Title> - Questions	<capitulo-slug>
```

Mapping rules:
- `QType` is always `2` (single choice) — this skill only writes
  exactly-one-correct-answer questions, never the multi-select or Kprim
  types the note type also supports.
- `Q_1`-`Q_4` are the four options, same text as A-D. `Q_5` stays empty and
  still needs its tab.
- `Answers` is four space-separated `1`/`0` flags, one per `Q_1`-`Q_4`, with
  exactly one `1` (`0 0 1 0` if C is correct). No fifth value for `Q_5`.
- `Title` gets the chapter's own title; the add-on renders it as a heading,
  which orients the reader once cards from many chapters share a deck. That
  is orientation, not a hint, so it does not break self-containment.
- `Sources` gets `<Book Title> — <Chapter Title>` — a citation shown on the
  back, so it keeps the *bare* book title with no deck suffix.
- `Extra 1` gets the same one-line justification Step 5 puts after
  "Resposta: X —"; it renders on the back under an "Extra 1:" label.

## Step 6 — Where to save (standalone only)

See [references/standalone-output.md](references/standalone-output.md). In
batch mode, skip this step entirely.

## Step 7 — Self-check before finishing

Two different checks, both mechanical. Run the quality one first — it is the
one that decides whether the cards are worth keeping.

**Quality** — if the sibling `anki-deck-audit` skill is installed, run its
script against what you just wrote. It works on a 2-column batch partial as
well as on a finished 4-column file:

```
python3 ${CLAUDE_SKILL_DIR}/../anki-deck-audit/scripts/deck-audit.py \
  --flashcards "<...Study.txt or <chapter>.flashcards.tsv>"
```

Any `REPROVADO` line means rewrite before shipping — those are the hard
limits from "One card, one fact", counted. A chapter-sized batch is small, so
fixing them is a few rewrites, not a regeneration. Report the numbers you
ended at; do not ship a batch that still fails and mention it in passing.

**Structure** — if the sibling `book-to-anki` skill is installed, let its
validator do the columns-and-headers half instead of eyeballing rows:

```
python3 ${CLAUDE_SKILL_DIR}/../book-to-anki/scripts/anki-kit.py \
  validate --book "<Book Title>" \
  --files "<...Study.txt>" "<...Questions.txt>" "<...Questions-Anki.txt>"
```

It checks the header directives, column counts, deck constancy, tag slugs,
`Answers` flags and question numbering, and prints `AVISO` lines for text
mentioning `capítulo`/`seção`/`parte`/`até agora`/`mais adiante`. Those
warnings are for **your** judgment, not automatic deletions: a card whose
answer is a fact about the book's structure gets rewritten around the
concept or dropped; a card that merely uses the word "parte" in ordinary
prose is fine.

If that skill isn't installed, re-read all three files and confirm the same
things by hand:
- No stray tab or newline inside a field; no duplicate flashcards; no
  question with two defensible correct answers.
- Every `Answers` row has exactly one `1` among its four values.
- No card or question tests a fact about the book itself.
- Both TSV files carry `#deck column:N` and `#tags column:N` with the right
  `N` (not a bare `#deck:` header, not a column merely *named* "Deck"), and
  every tag value is a slug with no literal spaces.

## Step 8 — Report the curation, not just the file paths (standalone only)

See [references/standalone-output.md](references/standalone-output.md). In
batch mode, skip this step and return whatever the caller asked for.

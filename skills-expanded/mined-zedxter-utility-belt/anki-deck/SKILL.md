---
name: anki-deck
description: Builds Anki flashcard decks (.apkg) offline from Markdown, CSV/TSV or JSON cards - basic, reversed and cloze notes, subdecks, tags, images and audio, math - with deterministic deck, note type and note ids, so importing a rebuilt deck updates the cards already in Anki instead of duplicating them; also lists what an .apkg contains. Use when the user wants flashcards, an Anki or AnkiDroid deck, spaced-repetition cards or cloze deletions made from notes, a transcript, an article, a PDF, a vocabulary list or a spreadsheet, or wants to update a deck they made before ("сделай карточки Anki", "колода для запоминания"). Not for syncing with a running Anki (AnkiConnect), Quizlet or other apps, quizzing the user in chat, printable study sheets (pdf-typeset), or editing an existing collection.
license: MIT
compatibility: Python 3.12+ with uv (preferred) or pip (genanki 0.13.1, markdown-it-py); macOS, Linux, Windows. Offline; no network after the first install. The .apkg opens in Anki desktop 2.1+ and AnkiDroid.
metadata:
  author: zedxter
  version: "1.0.0"
  source: https://github.com/zedxter/utility-belt
---

# Anki Deck

Turns cards written as Markdown, CSV/TSV or JSON into an Anki package
(`.apkg`) that the user imports into Anki desktop or AnkiDroid. Built with
`genanki`, offline.

The one thing generated decks usually get wrong is ids. With random ids,
every rebuild imports as new note types with every card duplicated. Here the
ids are derived from names:

- **A note's id (guid)** comes from its front, from its cloze text with the
  hidden answers left out, or from an `id` you give it.
- **The note type id** comes from the note type's name.
- **The deck** is matched by its name: Anki files imported cards by deck
  name, not by id.

So fixing a typo in an answer and importing again **updates** that card in
Anki, and its review history stays.

The script parses and builds. The card quality is yours: see "Writing good
cards". Most of what makes a deck useful happens there.

## When to use

- "Make Anki cards / flashcards / a deck from this" (notes, an article, a
  transcript from `youtube-transcript` or `transcribe-audio`, a PDF, papers
  from `scholar-search`).
- "Turn this vocabulary list / spreadsheet into flashcards" → CSV with
  `--type reversed`.
- "Cloze cards for this list / process / definition" → cloze.
- "Update the deck you made last time" → rebuild from the same source with
  the same `--deck`; the user imports it again.

Not for:
- pushing cards into a running Anki (that is AnkiConnect, a different tool);
- Quizlet or other apps;
- quizzing the user in chat;
- changing the user's collection directly.

## Quick start

The script is `scripts/anki_deck.py` relative to this skill.

```bash
uv run scripts/anki_deck.py build cards.md -o biology.apkg --deck "Biology::Cells" --dry-run   # look first
uv run scripts/anki_deck.py build cards.md -o biology.apkg --deck "Biology::Cells"
uv run scripts/anki_deck.py build words.csv -o spanish.apkg --deck "Spanish::Food" --type reversed --tags vocab
uv run scripts/anki_deck.py build notes.md -o deck.apkg --media images/
uv run scripts/anki_deck.py inspect biology.apkg
```

`build` output for the Markdown example below:

```
biology.apkg: 4 notes, 5 cards, 1 media file
deck Biology::Cells: id 1931295993
note type anki-deck Basic: id 1425772969
note type anki-deck Cloze: id 2112089762
Import it in Anki with File → Import (AnkiDroid: Import). Rebuilding and importing again updates these cards.
```

## Input formats

Write the cards to a file first, usually Markdown, then build. Several
input files can be combined in one build.

**Markdown, Q:/A: blocks** (the most robust layout):

```markdown
# Biology::Cells

Q: What organelle makes most of a cell's ATP?
A: The **mitochondrion**.
Extra: By oxidative phosphorylation.
Tags: organelles energy

Q: What is the formula of glucose?
A: $C_6H_{12}O_6$

Q: Which organelle is shown?
A: ![](img/mitochondrion.png)
---

The {{c1::nucleus}} stores DNA; {{c2::ribosomes}} make proteins.
```

- **Card blocks:** a block runs from `Q:` to the next `Q:`, a `---` line,
  a heading or the end. Nothing inside a fenced code block is read as a key. Answers can span lines and lists. `Extra:` text shows under the
  answer. `Tags:`, `Deck:` and `Id:` lines belong to their card.
- **Cloze outside blocks:** paragraphs with `{{c1::...}}` outside the blocks
  (after a `---`) become cloze notes.
- **Deck name:** the H1 is the deck name unless `--deck` is given.

**Markdown, headings:** each `## heading` is a question and its body is the
answer. Use this when no `Q:` lines exist.

**Markdown, cloze only:** each paragraph or list item containing
`{{c1::...}}` is a note. `Extra:`, `Tags:` and `Id:` lines right after it
belong to it.

**CSV/TSV:** a header row with any of:
- `front`/`question`/`term`/`word`
- `back`/`answer`/`definition`/`translation`
- `text` (cloze)
- `extra`, `tags`, `deck`, `id`, `type`

A header column with another name fills front, then back, if those are
missing (`Term,Meaning` works). Without any recognised header, the columns
are front, back, tags, and the first row is read as a card (a `note:` says
so): **always start a CSV with a `front,back` header.** The delimiter
(comma, semicolon or tab) is taken from the header line, and quoted fields
may span lines.

**JSON:** `[{"front": "...", "back": "..."}]`, the same keys as CSV, or
`{"deck": "Name", "cards": [...]}`. `["front", "back"]` pairs work too.

**Fields are Markdown:**
- `**bold**`, `*italic*`, `` `code` ``, lists, tables, code blocks and
  images all work.
- Math `$...$`, `$$...$$`, `\(...\)` and `\[...\]` goes to Anki's MathJax
  untouched.
- HTML in the input is shown as text. `--html` passes fields through as HTML.

**Media:** images (`![](path)`, `<img src>`) and `[sound:file.mp3]` are
packed into the deck.
- Each is found next to the input file it appears in, or in `--media DIR`.
- Paths must be relative and stay inside that folder: no `..`, no absolute
  paths.
- Only image, audio and video files are packed.
- A missing file stops the build (exit 3).
- A web URL is left as a link and shown only when online.

## Options

| Flag | Default | Meaning |
|---|---|---|
| `-o FILE.apkg` | — | Output; required unless `--dry-run`. |
| `--deck NAME` | H1, JSON `deck`, or file name | `"Parent::Child"` makes a subdeck. A card's own `deck` wins. |
| `--type` | `basic` | `basic`, `reversed` (front→back and back→front), or `cloze`. Cards with `{{c1::…}}` and no answer are cloze in any case; a card's own `type` wins. |
| `--tags a,b` | — | Added to every card. Commas and spaces separate tags (as in `Tags:` lines and CSV); write multi-word tags as `food_items`, and use `::` for hierarchy (`bio::cells`). |
| `--media DIR` | next to the input | Where images and audio are. |
| `--seed TEXT` | none | Mixed into every id. The same cards then form a separate deck, with separate note types, that does not update the old one. Leave it empty unless the user wants a fresh copy. |
| `--format` | from the extension | `md`, `csv`, `tsv`, `json` (for stdin `-`). |
| `--html` | off | Fields are HTML; no Markdown conversion. |
| `--dry-run` | off | Print the parsed cards, ids and missing media; write nothing. |
| `--json`, `-q` | off | JSON output; hide `note:` lines. |

`inspect FILE.apkg` lists the decks, the note types, note and card counts,
media, and the first notes. It reads decks built here and legacy Anki
exports ("support older Anki versions"); newer Anki exports are refused with
exit 2.

## How ids are made

| What | Derived from | Formula |
|---|---|---|
| Note guid | `id` if given; else the front, or the cloze text with each `{{cN::…}}` reduced to `{{cN}}`; whitespace collapsed | `genanki.guid_for("anki-deck", seed, kind, key)`, kind `basic` (also for reversed) or `cloze` |
| Note type id | note type name (`anki-deck Basic`, `anki-deck Basic and reversed`, `anki-deck Cloze`) | `int.from_bytes(sha256("anki-deck/model/<seed>/<name>").digest()[:8], "big") % 2**30 + 2**30` |
| Deck id | deck name | the same with `deck`; Anki itself matches decks by name on import |

What follows:
- **What updates.** Changing an answer (also a cloze's hidden answer), Extra,
  tags or media updates the note on re-import. Anki takes an incoming note
  only if it is newer, so rebuild before importing.
- **Changing a question makes a new note**, and so does changing a cloze's
  visible text. The old note stays in Anki. To keep a card's history while
  rewording it, give it an `id` from the start: an `Id:` line, an `id`
  column or a key.
- **Same fronts collide.** Two cards with the same front are one card: the
  second is skipped with a note unless it has its own `id`.
- **Changing `--type` between basic and reversed** for cards already in Anki
  does nothing: Anki keeps their note type and reports a conflict. Use
  Change Note Type in Anki, or keep the type.
- **Renaming a deck.** Anki matches decks by name. Renaming the deck in the
  source makes a new deck for new notes, while imported cards stay where
  they are. If the user renamed the deck in Anki, rebuild with `--deck` set
  to the new name.

## Writing good cards

This is where the deck succeeds or fails. When you write cards from source
material:

1. **One fact per card.** "What are the three functions of the liver?" is
   three cards, or one cloze note with `{{c1::}}`, `{{c2::}}` and
   `{{c3::}}`. Long answers are not remembered.
2. **Questions that have one answer.** "What is the powerhouse of the cell?"
   beats "Tell me about mitochondria". The front must make the answer
   unambiguous without the deck's context ("in E. coli", "in Python 3").
   Avoid "list all …" fronts, and avoid yes/no questions that can be
   guessed.
3. **Cloze for lists, sequences and definitions.** Cloze the key term, not
   filler words, and use at most one or two deletions per sentence. Put
   context that must stay visible outside the braces. Get that context right
   the first time: rewording it later makes a new note, unless the note has
   an `Id:`.
4. **Answers short; the why goes in Extra.** The back holds the fact; Extra
   holds the source, an example or the mnemonic.
5. **Reversed only where both directions matter**: vocabulary, symbols ↔
   names, capitals ↔ countries. Not for questions.
6. **Use the source's words for terms, your own for questions.** Never copy
   long passages. For copyrighted material, card the facts and put a short
   citation in Extra.
7. **Don't invent.** Every card must come from the material the user gave
   or from a source you looked up. Leave out what you are unsure of rather
   than guess.
8. **Tags for structure, subdecks for study sessions.** For example, tag
   `chapter3` and file under `Biology::Cells`. Match the user's existing
   deck names when they mention them.
9. **Look before you build.** Run `--dry-run`, read the cards as a learner
   would, then fix vague fronts and overloaded backs.
10. **Size.** 20–60 cards per source is typical. Ask before making
    hundreds.

## Workflow for the agent

1. Get the material: the user's notes, or a transcript, article or PDF
   through the other skills. Pick a deck name from the subject, or the one
   the user mentions.
2. Write the cards to a `.md` (or `.csv` for vocabulary) next to where the
   deck will go, following "Writing good cards". Keep that file: it is the
   deck's source for later updates.
3. Run `--dry-run`, fix what is skipped or vague, then build with `-o`.
4. Give the user the `.apkg` path and how to import it: Anki desktop
   File → Import; AnkiDroid: Import from the menu, or open the file. The
   defaults update existing notes when newer.
5. To update later:
   - Edit the same source and keep the same `--deck`, `--type` and
     `--seed`. If the user renamed the deck in Anki, use the new name.
   - Rebuild and import.
   - Don't change questions whose history you want to keep, unless the
     card has an `id`.

## Exit codes

One `error:` line on stderr with a hint after `—`; skipped cards are listed
as `note:` lines.

| Exit | Meaning | What to do |
|------|---------|------------|
| 0 | Done (or a dry run with nothing missing). | — |
| 1 | No usable cards: none found, or all skipped. | Check the layout against "Input formats"; read the `note:` lines. |
| 2 | Bad input: an unreadable file, an unknown format, invalid JSON or a non-text JSON value, a bad deck name, `-o` not ending in `.apkg`, a media path outside the input's folder or not an image/audio/video, two media files with the same name, a package `inspect` cannot read, or a missing dependency. | Fix the argument or the file. |
| 3 | A referenced image or audio file is missing. A dry run also exits 3 and lists them. | Pass `--media DIR`, or fix the path. |
| 7 | The deck could not be written, or an unexpected failure. | Check the folder and free space. |
| 130 | Interrupted. | — |

## Limitations

- **Tested against Anki desktop's own import code** (the `anki` Python
  package). AnkiDroid imports the same `.apkg` format, but it was not tested
  separately.
- **No live sync.** The user imports the file. For pushing cards into a
  running Anki, use an AnkiConnect-based tool.
- **Imports update only newer notes.** A note's time is its build time, to
  the second. If the user changed a card inside Anki after the last import,
  a rebuild still overwrites it.
- **The note types are this skill's own** (`anki-deck Basic`, `… and
  reversed`, `… Cloze`), with a clean style that works in night mode.
  Anki's built-in "Basic" is not reused, so styles stay predictable.
- **genanki 0.13.1** (MIT) is pinned. Its last release was in November 2023,
  but the `.apkg` format it writes is stable. Its dependency
  `cached-property` uses an asyncio call that is deprecated now and
  scheduled for removal in Python 3.16.
- **`inspect` cannot read newer-only exports.** It needs a legacy
  collection inside the package, and Anki exports made without "support
  older Anki versions" contain only `collection.anki21b`.

## Chaining

- `youtube-transcript` / `transcribe-audio` / `web-extract` / `wiki-lookup` /
  `scholar-search` give the material; this skill makes the deck.
- `pdf-typeset` prints a study sheet from the same Markdown.

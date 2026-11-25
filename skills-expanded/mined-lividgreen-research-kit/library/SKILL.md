---
name: library
description: The reference library — one card per referred work (a paper, a book, a preprint, a software library or tool, a dataset, a report handed in, a page) holding its fields, how it was read, our notes and what it says at a place, written and searched through the `library` CLI. Use when registering a work, recording how it was read, looking for a work or for what one states, finding related works or where one is cited, and before any sentence cites a work. For any project that refers to things, scientific or not. The project's own instructions bind the directory and the gates through `library.toml`; this skill names none of them.
license: Apache-2.0
compatibility: Python 3.11 or later, standard library only. Optional - pdftotext (poppler) or another text command for kept PDFs, SQLite with FTS5 for stemmed search (whole words otherwise), network access for resolve, verify, fetch, restore and watch (never needed by the check).
metadata:
  version: "0.12.1"
  script: scripts/library.py
---

# The reference library

The library is the registry of everything a project refers to: one card per work, and nothing else is a store.
It is a component of its own, with its own directory, tool, check and lifecycle.
A card is read alone: nothing on it names a record of any other system, and the library knows no other system's kinds.
The connection runs one way: whoever cites a work writes the cite prefix and the card's key, and asks the library whether the key exists and how the work was read.
`scripts/library.py` beside this file is the CLI, the check, the index generator and the selftest; it uses the standard library alone; `library …` below is that script run by its path from the project root (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/library/scripts/library.py …` under Claude Code), never a `library` found on PATH, which may be another version.
`library.toml` at the project root binds the paths, the kinds of work, the cite prefix and the files citing sites are computed from; `library init` writes one with the bindings filled in and the optional ones commented, and the directories beside it.
`library --help` lists every command and needs no bindings file.

## The card

A card is `cards/<key>.md` under the library's directory: front matter, then a body of two sections.
The `key` is pinned: the first author's surname and the year, a letter added on a clash, never regenerated, and it is the file's name.
An internal document's key is its file's stem instead (`reports/review-1.md` is `review-1`), since a project's reports share their author and carry no year of publication; `--key` pins another.
The work's fields are `kind`, `title`, `authors` as `Surname, I.`, `year`, `venue`, and whichever of `doi`, `arxiv`, `openalex`, `zbmath`, `isbn` and `url` exist; a preprint and its published version are one card carrying both identifiers.
`metadata` says where those fields came from and when — typed by a hand, or written by a named resolver — and which fields a hand typed over the resolver's.
`verified` is the date the fields were last checked against a resolver and which one answered, and is empty until one has been asked.
`read` says how the work was read, and it is a claim about us, never about the work: its `grade` is `unread`, `skimmed`, `parts` (with `what` naming them) or `full`, and a read carries the date it was made.
A reading done now is dated today; one from before the library whose date was never recorded is a seeded card (`register --seed`) read `--undated`, and a date is never guessed.
The grade `ungraded` marks a seeded card nobody has assessed, and no other card may carry it.
`via` names the card a work is known through when it was not opened itself, so a statement taken second-hand says so on the card.
`copy` is a kept file with its hash, the date it was obtained, its version, the address it was fetched from, its page count and whether it has text; a copy with an address lives in the store, which version control ignores, since it can be fetched again; a copy obtained by hand has no address and lives in the kept directory, which is tracked, since nothing can fetch it again; a recorded copy that is not on disk is counted by the check and never fails it, and one that is on disk must match its hash.
`related` links two cards symmetrically and not transitively.
`file`, on an internal document alone, names the tracked file of the project the card stands for.
`state` is `registered`, or `excluded` with a dated reason: a work looked at and set aside stays findable, so it is not looked at twice.
The body is `## Notes`, ours and in our words — what the work is, what we use it for, what we concluded about it — and `## Extracts`, what the work states at a named place, each extract addressed by an id.
Where a key is cited is computed from the files the project binds and never stored.

## Commands

| Command | What it does |
| --- | --- |
| `library register "Title" --kind article --author "Jen, E." --year 1990 --doi …` | a new card; the identifiers `--doi`, `--arxiv`, `--isbn`, `--openalex`, `--zbmath`, `--url`; `--key` pins a key, `--venue`, `--tag`, `--note` and `--notes FILE` fill the notes, `--read GRADE --read-on DATE --read-what "…"` and `--via KEY` record a reading at once, `--file PATH` makes an internal document's card, `--seed` marks a card loaded from an older list |
| `library read KEY --grade parts --what "sections 1 to 3"` | how the work was read, with its date (`--on DATE`; `--undated` only on a seeded card, `register --seed`, for a reading from before the library whose date was never recorded); `--via KEY`, `--note "…"` |
| `library note KEY --note "…" --tag T` | a dated note under Notes, tags added; `--notes FILE` reads the text from a file |
| `library extract KEY ID --at "Theorem 4" --quote "…"` | an addressed extract under Extracts; `--says` a restatement in our words, `--caveat` the author's own, `--rule` what may be claimed, `--on DATE`, `--edition "…"`, `--unanchored "why"`, `--replace` |
| `library type KEY --title "…"` | a field of the work corrected by the hand over what a resolver wrote, and marked in `metadata.typed`; also `--author`, `--year`, `--venue` |
| `library relate KEY KEY` | a symmetric link; `--drop` removes it |
| `library exclude KEY --reason "…"` | sets a card aside with its reason; `--undo` |
| `library resolve "ENTRY" --register` | online: candidates for a reference entry, each checked against it; the card is written from the one that passes; an identifier given with `--doi`, `--arxiv` or `--openalex` is resolved where it lives, `--title` overrides the entry's, `--at NAME` asks that one interface alone and returns its answer, `crossref`, `openalex`, `zbmath` or `semantic-scholar`, `--pick N` takes the Nth candidate, `--override` writes over a failing match, and `--key`, `--kind`, `--author`, `--year`, `--venue`, `--tag`, `--note`, `--seed` fill the card as `register` does |
| `library resolve --url URL --register` | online: a repository through its forge's API (its name, owner, description, licence and last push), any other page through its citation metadata; for the tools and pages a project cards |
| `library verify KEY…` | online: re-resolves a card at its own identifiers, compares, and stamps `verified`; `--take FIELD` writes the resolver's value for one field |
| `library fetch KEY` | online: a copy by the card's identifiers — arXiv's TeX source, else its PDF, else the card's address — or from `--url`; `--pdf` takes the PDF, `--replace` a new copy over a recorded one |
| `library keep KEY FILE` | a file obtained by hand taken in as the card's copy — into the tracked kept directory with `--redistributable`, the word that the project may redistribute it, or into the store with `--from URL` recording where it can be fetched again; with neither it refuses where a kept directory is bound, and where none is bound the copy goes to the store and the check names it as needing a backup; `--on DATE` when it was obtained, `--version`, `--move`, `--replace` |
| `library restore [KEY…]` | online: every recorded copy the store has lost, fetched from its recorded address and checked against its hash |
| `library page REF [N]` | the units of a kept copy, a PDF's pages or a TeX source's sections, each with its label; with `N`, the text of one |
| `library find --text WORDS…` | the kept text searched: one line per page holding every word — the key, the unit, its label, a snippet |
| `library watch [NAME…]` | online: every watch, or the named ones, looks once and proposes what is new |
| `library watch --add NAME --citing KEY` | a watch on the works citing a card; `--related KEY` on the works OpenAlex relates to it, `--arxiv QUERY` and `--github QUERY` on a saved query; `--since DATE`, `--why "…"`; `--drop NAME`, `--list` |
| `library candidates` | the works the watches surfaced and nobody has registered; `--excluded` the ones set aside; `--exclude ID… --reason "…"` sets some aside |
| `library show REF` | the card whole, its links resolved, its citing sites counted |
| `library find WORDS… --tag T --grade G --kind K --id V` | ranked full-text search, one line per hit: the key, the label, the grade, the fields that matched; `--limit N` and `--from N` page it, `--state excluded` or `--state any` reaches the cards set aside |
| `library related REF` | other cards by an explicit link, known-through, tags in common and files citing both, each with its reasons |
| `library cited REF` | every site citing the key, as file and line, the reference entries tied to it among them |
| `library claims [DOC…]` | the claim-shaped sentences of the bound documents that name a carded work, each with the extracts its card carries; `--uncovered` the ones whose card carries none |
| `library entries` | the reference entries of the documents the project binds, each with the card it is tied to; `--untied` lists the ones that are not |
| `library citecheck [DOC…]` | each document's text against its own reference entries, the bound documents where none is given: every author-year citation answered by an entry, every entry cited; exit 1 with the file and line of each that is not |
| `library keys` | every key with its state and grade, as JSON: what a consumer's check reads |
| `library index`, `library check` | the generated index (`--check` reports drift and writes nothing); every rule, with a coverage line |
| `library init` | a project's `library.toml`, directories and index under `library/` (`--dir DIR` for another); `--kept` turns on the tracked kept directory (`<dir>/kept`), `--scan`, `--documents`, `--internal` name the paths, `--force` overwrites; `--print-instructions` prints the paragraphs for the instructions file for `library.toml` as it stands and writes nothing |
| `library pages` | the page manifest the `dashboard` skill renders |

A card is named by its key or by any of its identifiers wherever a command takes `REF`.
Under `--json` a card carries `lines` beside its fields: `{"label", "text"}` pairs, only the ones that hold something, `by` (the authors by surname and the year) and `read` (what was read of the work, as `library read --what` wrote it), which a dashboard prints on a card without reading the file.
The global flags are `--json` (any command emits one JSON object), `--root DIR` (the project, found upward otherwise) and `--today DATE`; `library --help` lists every command and `library <command> --help` its flags, neither needing a bindings file.
`find` prints first which rankers ran; it is stemmed and folds diacritics where the SQLite in use has full-text search, and matches whole words where it does not.
`find` prints a bounded count and names the continuation (`--from N`); `--state excluded` or `--state any` reaches the cards set aside.

## Writing a card from a resolver

`library resolve` asks the interfaces for the work a reference entry names, and `library verify` asks again at a card's own identifiers; `references/resolver.md` is how each decides, which interfaces it calls, and the keys it reads from the environment.
A candidate is accepted only past the identity check — title, first author's surname and year each found in the entry — and one that fails writes nothing; `--pick N --override "reason"` is for a later edition or a damaged record, never for a doubt.
Both commands are online, on demand and never part of `library check`, and a resolver's answer is a candidate for the card's fields, never a read: the grade does not move.

## Kept copies

A copy is one file per card, `<key>/copy.<ext>`, recorded on the card with the hash of its bytes; `references/copies.md` is where each copy lives, how `fetch`, `keep` and `restore` obtain it and how its text is derived.
A copy with an address goes to the store, which version control ignores; one with no address goes to the kept directory, which travels with the repository, so only with `--redistributable`.

## Internal documents

A document of the project itself — a deep-research report, a survey, a review, a dated record, anything made here or handed in — is a work like any other and has a card: a kind the project lists as internal, and `file`, the tracked path it stands for.
It is the special case in three ways and no more.
Its file is its copy: nothing is fetched, kept or hashed, `library page` reads it by its headings, `library find --text` searches it with the kept copies, and an extract on it is anchored in the file.
No bound document may cite it: a reference entry that agrees with an internal card fails the check, since a reader of the document cannot open it; a record, a log entry or another card cites it by its key as it cites any card.
Every file under the directories the project binds has its card, so a new document lands with one: `library register "Title" --kind report --file PATH`, with whoever produced it as its author where that is known and nobody where it is not.
Its notes are what the notes of any card are, and matter more: what of it was confirmed at a primary source or by a call, what was not, where it disagrees with another, and that nothing rests on it alone.

## Extracts

An extract is one block under `## Extracts`: a head line `**id** — locator — checked DATE, edition`, then labelled lines — `Quote:` the work's own words, `Restated:` what it says there in ours, `Caveat:` the author's own, `Rule:` the standing rule on what may be claimed of it, and `Unanchored:` why the kept copy cannot bear it out.
An extract says something: it has a quotation or a restatement, and it is written by `library extract`, which refuses a block that does not read back as written.
It is cited as the cite prefix, the key, `#` and the id.
The anchor check is part of `library check`: where the card's copy is kept and has text, every quotation must stand in that text and a numbered locator — a theorem, a proposition, an equation, a section — must occur in it, and an extract that fails is a failure of the check.
A quotation is compared by its words, cut at its mathematics, its ellipses and its brackets; a TeX source is read with its own macros of no argument put back and its commands dropped, and its numbers are not looked for, being the typesetter's.
An extract is counted unanchored, with the reason, and never passes silently, where no copy is kept, the copy is not on disk, the copy has no text, or the extract was read in another edition than the kept one and says so under `Unanchored:`.
A restatement is not judged by the check: whether it is faithful is read by a person, against the page.
A card graded unread carries no extract unless it names the card the work is known through.

## Claims

`library claims` reads the bound documents for sentences of the shapes that credit the document against a named work — a verb of settling, a first, an identification — and lists each one that carries the first author's surname and the year of a card the document's references are tied to, with that card's extracts.
The shapes are regular expressions the project may replace in `library.toml` (`[claims] shapes`); the defaults are generic, and a project with a prover adds its own words there.
A sentence at a card with no extract is unverifiable from the library: the work is to be read and the extract written before the sentence is trusted; the `attribution` skill runs that check from this list.
The list is a worklist and never a verdict, and a sentence that names no carded work is not on it.

## The watch

The watch answers what is new since it last looked, and is a check and not a schedule; `references/watch.md` is what each of its four looks asks, what it records and how a candidate becomes a card or is set aside.
A candidate is not a card, and a run is online and never part of `library check`.

## Reference entries of the project's documents

A document's reference entry writes no key: it names the work, and the check ties it to a card.
An entry is a line of the section under the bound level-2 heading (`## References` by default) that opens with the authors and the year in parentheses — `Jen, E. (1990). *Title*. Venue.`, `(2005, March 3)` and `(n.d.)` or `(in press)` as well, an entry with no year tied only to a card with none — one entry per line; a numbered bibliography, a BibTeX file or a level-3 heading is not read, and the check names each line under the heading that is written like an entry — a list item, a line opening with a surname and an initial, a year in parentheses with only names before it — and is not read as one, while a paragraph of prose under the heading that mentions a year late is left alone.
An entry is tied to a registered card when the card's title agrees with the entry's — the two normalized, agreeing at a similarity of at least 0.85 — and the card's first author's surname and its year both stand in the entry as words: the same check a candidate passes, made offline.
Every entry must be tied to exactly one card: an entry with no card fails, and so does an entry two cards agree with.
So a new entry in a document needs its card in the same change, and an entry whose year, title or first author is wrong fails until the document or the card is corrected — whichever the work's own record contradicts.
The failure names the nearest card and which of title, first author and year disagreed, and where the year disagreed and the card's venue names the entry's year, says so: a card typed from a preprint carries the preprint's year, and a work cited in its journal version takes the journal's.
A work a document cites that is graded `unread` and names no `via` fails: either it was read, or it is known through a work that was.
The title of an entry is read from its emphasized span where it has one, else from the first sentence after the year; an annotation after the work's own data is set aside.

`library check` ties each entry to a card; `library citecheck` ties the document's text to its entries, so the two close the chain from a sentence to a card.
It reads the author-year citations of the text outside the references section, its code and its front matter — `Jen (1990)`, `Brummitt and Rowland (2012)`, `Smith et al.'s (2001)`, `van der Waals (1873)` and, inside parentheses, `(Kneser, 1953; see also Jen, 1990a, b, p. 4)`, a letter alone continuing the year before it — and leaves a capitalized word before a year that is no author, such as `(In 2020)` or `(March 2021)`, alone.
A word written as no surname is — in capitals, with three capitals in one of its hyphen-joined parts (`NeurIPS`, never `Garcia-MacDonald`) or with a digit, such as `(NeurIPS 2019)` or `(Q3 2021)` — is read as a citation only where an entry's first author bears it, as `(OECD, 2019)` does.
A citation is answered by an entry whose first author's surname, the name before the first comma, `and` or `&`, is the cited name and whose date is the cited one, a letter suffix included, so `Jen (1990a)` needs the entry of `(1990a)` and a citation of the second author answers nothing; every entry must be cited at least once, and a line under the heading written like an entry and not read as one is named, since no citation reaches it.
A numbered citation, a key and a footnote are not read, and the last line says how many citations and entries were; a file that is not there, or no document given and none bound, exits 2.

## Searching

Search runs cheapest first, and never by listing the cards' directory.
A known work: `show` with its key or an identifier.
A topic: `find` with a few words; on a miss, other words for the same thing, or a filter by tag, since ranking by words is weak on a paraphrase.
A place inside a work whose copy is kept: `find --text` with the words, then `page` for the one unit; a kept text is read a page at a time, never whole.
The neighbourhood of a work: `related` and `cited`.
Every view is one line per card; open one card at a time, by `show`.
The generated index is one line per card and is read whole only while the library is small; past a few hundred cards it is searched.
The card is the memory between sessions: the grade says what was read, in which form and when, and an extract says what the work states at which place.

## Before a sentence cites a work

Show the card.
Where no extract on it covers the claim, open the work at the place, write the extract, and set the grade, in the same session.
Then cite: the key for the work, the extract for what it states.
Register a work when it is first read or first cited, before the sentence that cites it is written.
Whatever a resolver, a search engine or a subagent's report says about a work is a candidate for the card and its notes, never a read: the grade moves only when the work itself was opened.

## Rules the check enforces

- A card's front matter is in the form the tool writes, its fields are the card's fields and no other, and its kind is one the project lists.
- The key is the file's name, in lowercase letters, digits and hyphens.
- No two cards share a DOI, an arXiv identifier or any other identifier.
- The read grade is legal, a read in parts names the parts, a read carries its date unless the card is seeded and the date was never recorded, and only a seeded card is ungraded.
- `via` and `related` name other cards, every related link is named back, and a card's body cites only keys that are cards.
- A recorded copy lies inside the store when it has an address and inside the kept directory when it has none, and, when it is on disk, matches its hash.
- The extracts are in the addressed form, each id once on its card, each saying something, each dated; a card graded unread carries one only with a `via`; a body cites an extract only where the card carries it.
- Where a copy with text is kept and the extract does not declare itself unanchored, its quotations and its numbered locator stand in the kept text.
- A card naming a file of the project is of an internal kind and its file exists; a card of an internal kind names its file; no file has two cards; an internal card records no other copy; every file under a bound directory has a card; no reference entry of a bound document is tied to an internal card.
- An excluded card carries its reason and date, and a registered one carries no exclusion.
- Every date is a date and none is in the future.
- The body is one sentence per line, and is `## Notes` then `## Extracts` with no other section.
- The committed index equals a fresh render.
- The watches and the candidates parse: a watch has a name of its own, one of the four kinds, a card that exists or a query, and a `since` that is a date; a candidate has an identifier and a state, and one set aside gives its reason.
- Every reference entry of the bound documents is tied to exactly one registered card, and every line under the heading written like an entry is read as one.
- A card an entry is tied to is not graded `unread` without a `via`.

`library check` ends with six coverage lines, so a green says what it did not look at, and that it asked no resolver:

1. the cards by grade, the cards set aside, the copies verified, the copies recorded but not on disk, the copies with no text and the copies obtained by hand, each by its key, the store, the kept directory, and the files citing sites are computed from;
2. the cards written by a resolver and the cards typed by hand, how many carry a verify stamp and the oldest stamp's date;
3. the internal documents and the directories held to them;
4. the extracts, how many a kept copy bears out and how many are unanchored for which reason;
5. the watches, how many have never run, the identifiers seen and the candidates proposed and set aside, with the statement that no run is due;
6. the entries read, in how many documents, the cards they are tied to by read grade, and the registered cards no entry cites.

`library.py --selftest` plants one defect per code the check reports, fails when one is planted nowhere, and must stay green.

## Writing discipline

`key`, `state`, `excluded`, `metadata`, `verified`, `read`, `via`, `related` and `copy` are written by the commands and never by hand.
A work's own fields are corrected with `library type`, which marks them; a note, an extract and a tag are added with `library note`, which dates the note and reflows the body; an identifier, `tags` and the body may also be edited by hand, where the project's commit gates re-check the file.
The front matter is the subset the tool writes: a field name in lowercase letters and underscores, a value that is a plain word, an integer, `null`, `true`/`false` or a double-quoted string (a single-quoted one is read too), a block list or a one-level map; the library runs no markdownlint of its own.
Notes say what we think and extracts say what the work says at a place, with the rule on what may be claimed of it; a quotation is never written as a note, and the history of a verdict — what a document said and how it was corrected — is a note.
Run `library check` before committing; the project's hook runs `library check --staged` as well, the same check on a temporary checkout of the git index, which is what the commit holds, not the working tree a hook runner has stashed half of.
A path git ignores, a kept copy among them, is read from the working tree, since the index holds none, and `--staged` is refused outside a git repository.

## What the project binds

`library.toml` names the library's directory, the store, the kept directory, the reflow module, the kinds of work, the cite prefix, the files citing sites are computed from, the documents whose reference entries are tied to cards and the heading they stand under, the command that prints a PDF's text with a form feed between pages, the kinds an internal document takes and the directories whose every file has a card, the shapes of a claim sentence where the defaults do not fit, and the count a view prints before it names the continuation.
A project whose documents cite by key alone binds no `[entries] documents`; a project with no reports binds no internal directories; both halves of the check then say they looked at nothing there.
The project's instructions name the gates that cover the cards and what else in the project checks a cited key against the library.

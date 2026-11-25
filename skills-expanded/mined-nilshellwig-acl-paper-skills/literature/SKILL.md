---
name: literature
description: Reading, judging and citing papers in an acl-paper project (has paper.config.json). Use before citing a paper, when deciding whether a paper is relevant, when checking that a citation supports its claim, when the user drops a PDF into the project or pastes a BibTeX entry, and when the bib sync reports unknown or unread keys.
---

How papers move from "found" to "cited" in this project. Searching and fetching are the source skills' job (`acl-anthology`, `arxiv`, project sources in `.claude/skills/`); everything after the fetch is here.

`PK` means `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/paperkit.py`, run from the project root (the folder with `paper.config.json`).

## The rule

A paper is judged and cited only on its **body**: introduction, method, experiments, results, tables, limitations. The abstract (and a search hit's snippet) is for triage: it decides what to read, never what a paper shows. A citation stands once the body passage that supports it is in the notes.

## Reading a paper

1. Open `literature/md/<key>.md`. For long papers, grep it for the terms of the claim and the section headers first, then read the matching sections in full. Use the PDF (`literature/pdf/<key>.pdf`) for figures, table layout and printed page numbers.
2. Fill `literature/notes/<key>.md`:
   - `## Read`: which parts you read ("full paper", "Sec. 1-5, Tab. 2").
   - `## Claims this paper supports`: one line per claim, in your words, with its body location and a short quote. Numbers exactly as printed in the paper.
   - `## Relevance to our paper`: where and why it would be cited, or why not.
3. Run `PK mark-read <key>`. It refuses while `Read` or `Claims` is empty or the `.md` is missing; fix what it names.

When you tell the user a paper supports a claim, quote the body passage in chat.

## Citing

- Cite only `read-full` keys, with `\citet{}` / `\citep{}`. Write the citation into the `.tex` and stop there: the PostToolUse hook moves the entry from `literature/archive.bib` into the paper bib, and moves it back when the last citation goes.
- Keep one key per paper. Before citing, check `literature/index.md` for the same paper under another key (preprint and published version); when both exist, ask the user which to cite.
- After a rewrite that touches a cited sentence, each resulting sentence that rests on the source keeps its citation.

## Entries and PDFs that do not come from a source skill

- User pastes a BibTeX entry: save it to a temp file and run `PK bib-paste --file <tmp>`.
- User drops a PDF into the project: identify the paper from its first page, find its key in the paper bib or `literature/archive.bib`, and run `PK add-local <pdf> --key <key>`. No entry yet: stop with ⚠️, name the paper (title, authors, year, venue or DOI) and ask the user for the authoritative entry. File the PDF once the entry exists.
- A paper with no fetchable source (book, report): ask for the entry and a PDF, then the two steps above.

## Sync messages

The hook (and `PK sync`) reports:

- **unknown key**: cited but in neither bib file. Fetch it through a source skill, or ask the user for the entry. Write no BibTeX yourself.
- **not read in full**: cited before its notes were done. Read it now (steps above). If the body does not support the sentence, tell the user and propose a fix.

`PK index` rebuilds `literature/index.md`; `PK sync` runs everything by hand.

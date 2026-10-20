---
name: pdf-chapter-splitter
description: "Splits a PDF book into one PDF per chapter, using the PDF's own embedded bookmarks/outline to find chapter boundaries. Output goes into a folder named after the book, with one file per chapter. Use when the user asks to split/recortar/dividir a PDF or book into chapters, or wants each chapter as its own PDF file."
argument-hint: "[path to PDF] [optional: output folder]"
allowed-tools: Read, Glob, Bash(python3:*), Bash(pdftotext:*), Bash(pdfinfo:*), Bash(ls:*)
---

# PDF Chapter Splitter

Splits a single PDF into per-chapter PDFs using the document's native outline
(bookmarks) — no OCR or heuristic text scanning, as long as the PDF has
bookmarks (most e-books from O'Reilly, Apress, Manning, Packt do). The output
folder feeds `book-to-anki` directly, so chapter-level granularity matters:
one file per *Part* is wrong.

## Step 1 — Ensure `pypdf` is available

Installed persistently for this user (`pip install --user`, in
`~/.local/lib/…`, surviving across sessions — unlike a venv under `/tmp`,
which dies with the session). Just check that it imports; reinstall only if
missing:

```
python3 -c "import pypdf" || python3 -m pip install --user --break-system-packages -q pypdf
```

If `--user` installs are blocked in some other environment, fall back to a
throwaway venv:
`python3 -m venv /tmp/pdf-split-venv && /tmp/pdf-split-venv/bin/pip install -q pypdf`

## Step 2 — Inspect before splitting

Never split a book blind. `--inspect` writes nothing and prints the nested
bookmark tree, the units the splitter would derive from it, the filenames it
would write, and the page-coverage check:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/split_pdf_by_chapters.py --inspect "/path/to/Book Title.pdf"
```

What you are looking for in that output:

- **Flat outline** — depth-0 entries are already `Chapter 1: …`, `Chapter 2:
  …`. One file per entry; nothing to think about.
- **Part-wrapped** — depth-0 entries are `Part 1: …`, `Part 2: …` and the
  *real* chapters are their depth-1 children. The script expands these
  automatically; confirm in the derived-units list that you got one unit per
  chapter, not one per Part.
- **Too granular or absent** — every sub-heading has its own entry, or there
  is no outline at all. Stop, and see "When this won't work" below.

`NOTA` lines report bookmarks dropped because their page didn't advance —
usually harmless junk, but read them: each dropped marker is a chapter file
that will not exist. `PROBLEMA` lines mean the page ranges don't tile the
document and the split is not trustworthy.

## Step 3 — Split

```
python3 ${CLAUDE_SKILL_DIR}/scripts/split_pdf_by_chapters.py "/path/to/Book Title.pdf"
```

Default output folder is the PDF's path with `.pdf` stripped — a folder named
after the book, next to the source. A second positional argument overrides the
destination. The script exits non-zero if coverage is broken; it re-prints the
same coverage line and `NOTA`/`PROBLEMA` lines as `--inspect`.

Its detection rules, its handling of junk bookmarks, and its one known
limitation (Parts whose chapters have no leading number) are documented in
[references/algorithm.md](references/algorithm.md) — read that when a split
looks wrong, not before.

## Step 4 — Verify

The script's own `Cobertura: N/N páginas` line already covers the page-count
check that used to be done by hand. Beyond it, spot-check that a chapter file
actually contains its chapter:

```
pdftotext -f 1 -l 1 "<output folder>/02 - ....pdf" - | head -20
```

A file whose first page is the *end* of the previous chapter means the outline
points at the chapter's title page rather than its first content page — a
property of that PDF, not a bug to fix in the script.

## When this won't work

If Step 2 shows no outline, or one that clearly isn't chapter-level, do not
fabricate page ranges from guesswork. Offer the user instead:
- deriving ranges from a printed table of contents found via `pdftotext`;
- asking for explicit chapter start pages.

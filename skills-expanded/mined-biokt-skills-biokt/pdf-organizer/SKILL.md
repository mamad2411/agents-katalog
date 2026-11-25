---
name: pdf-organizer
description: Organize PDF journal articles from ~/Downloads into ~/Documents/Work/Articles/. Resolves author and year from the DOI via Crossref, verifies each match against the document, and renames to firstauthor-year.pdf.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/organize_papers.py:*), Read
---

Run the PDF organizer to file journal articles from ~/Downloads into the
library at ~/Documents/Work/Articles/.

- Script: `${CLAUDE_SKILL_DIR}/organize_papers.py`
- Requires Python 3 with `pypdf` (`pip install pypdf`); `ghostscript` and
  `xattr` are used for text fallback and (optional) Finder tags.
- Needs network access for Crossref/arXiv. Use `--offline` without it.

## Usage

**Always dry-run first:**
```bash
python3 ${CLAUDE_SKILL_DIR}/organize_papers.py --dry-run --limit 20 --verbose
```

**Full dry-run (review the CSV before committing):**
```bash
python3 ${CLAUDE_SKILL_DIR}/organize_papers.py --dry-run
```

**Full run:**
```bash
python3 ${CLAUDE_SKILL_DIR}/organize_papers.py --jobs 8
```

## How it decides

1. Extracts text in a subprocess with a timeout, so one malformed PDF cannot
   stall the run.
2. Vetoes obvious non-articles (invoices, receipts, CVs), supplementary
   material (`*MOESM*`, `*_ESM*`, `*_si_001*`) and Nature news (`d41586-*`).
3. Finds the DOI (or arXiv id) and resolves it against Crossref/arXiv to get
   the authoritative first-author surname, year and title.
4. **Verifies the match against the document.** This is the safety gate — a
   DOI inside a PDF says nothing about what the PDF *is*. Grant applications,
   referee reports and research notes all cite DOIs and would otherwise be
   filed under someone else's name. A match is accepted when the title appears
   verbatim, or enough of its distinctive words appear **and** the first
   author's surname is in the document. Both halves matter: a Séneca referee
   report scored 0.75 on title words alone against a paper in the same field,
   and a Zoom consent form scored a perfect 1.00 against an unrelated legal
   article whose title reduced to three common words.
5. Rejects commentary (News & Views, Comments, Perspectives, Research
   Briefings, Matters Arising, Corrections) unless `--include-commentary`.
6. Deduplicates: skips papers whose DOI is already in the library, and where
   two downloads share a DOI keeps the longer document.
7. Names `firstauthor-year.pdf`, suffixing collisions (`smith-2024a.pdf`).

Finder tagging is **off by default**. Keyword matching is too coarse to be
trusted for this: matched as substrings it put `Peptides` on an article about
lab meetings (`amp` inside "example"), and even on word boundaries the
vocabulary mislabels enough that unlabelled beats mislabelled. `--tags`
re-enables it.

If a PDF has no extractable text (a scan), the title gate cannot run; the DOI
resolution is accepted and the log records `title_match = n/a (no text)`.

A file whose DOI does not resolve is **left in place**, not filed under a
guess. The old text-heuristic naming is still available behind
`--allow-heuristic` (implied by `--offline`), but it measured 33% correct over
608 files and cannot be verified — it is what produced `the-2013.pdf`,
`administrator-2026.pdf` and `pythondocx-2026.pdf`. Treat anything logged as
`resolved_via=heuristic` with suspicion.

## Options

| Flag | Meaning |
|---|---|
| `--dry-run` | Preview only, no files moved |
| `--jobs N` | Parallel workers (default 8) |
| `--limit N` | Process only the first N files |
| `--verbose` | Show resolution method, title match, DOI per file |
| `--offline` | Skip Crossref/arXiv, use text heuristics only |
| `--allow-heuristic` | Guess author/year when no DOI resolves (unverifiable, ~33% accurate) |
| `--include-commentary` | Also file News & Views, Comments, Perspectives, Nature news |
| `--include-supplementary` | Also file supplementary-information PDFs |
| `--no-dedup` | Skip the already-in-library check |
| `--tags` | Apply Finder tags (off by default; see above) |
| `--min-title-match F` | Gate for DOI-resolved papers (default 0.70) |
| `--min-title-match-search F` | Gate for fuzzy title search, weaker evidence (default 0.85) |
| `--min-confidence` | Threshold for the heuristic fallback only |
| `--timeout N` | Per-file extraction timeout, seconds (default 45) |
| `--downloads` / `--articles` / `--log` / `--cache` | Path overrides |

Resolutions are cached in `~/.cache/pdf-organizer/doi-cache.json`, so re-runs
cost no network.

## After a run

The CSV log records `doi`, `title`, `pages`, `resolved_via` and `title_match`
for every file, so any decision can be audited:

```bash
# what was filed and how it was identified
awk -F, '$10=="moved"' ~/Downloads/organize_papers.csv | cut -d, -f3,4,15,16

# everything left behind, with the reason
awk -F, '$10=="skipped"' ~/Downloads/organize_papers.csv | cut -d, -f3,11
```

Files left in ~/Downloads are either non-articles, unresolvable, duplicates of
papers you already have, or commentary. Check the reason before assuming the
tool got it wrong.

## Notes

- The Crossref request deliberately sends **no** contact email. Crossref's
  "polite pool" invites one; the user's address is personal data and does not
  belong in a third-party request.
- Text extraction is capped at the first 3 pages / 12000 characters.

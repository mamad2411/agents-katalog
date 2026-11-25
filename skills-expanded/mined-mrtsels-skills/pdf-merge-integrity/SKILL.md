---
name: pdf-merge-integrity
description: Use when merging PDFs. Prefer qpdf; pdfunite corrupts.
metadata:
  source_frontmatter:
    tags:
    - pdf
    - merge
    - qpdf
    - pdfunite
    - verification
    - documents
  imported_from: hermes
---

# PDF Merge Integrity

Reliably combine multiple PDFs into one deliverable. Covers tool selection, the silent-corruption failure mode of `pdfunite`, and content-level verification that catches it.

## When to Use

- Merging PDFs into a single file (report + declaration + appendix, scanned pages, submission bundles, etc.)
- Any merged PDF that is a formal deliverable (SharePoint upload, submission, archival)
- User asks to "合成 / combine / merge" PDFs into one file

## Tool Selection

| Tool | Verdict |
|------|---------|
| `qpdf --empty --pages a.pdf b.pdf -- out.pdf` | ✅ Preferred CLI merge |
| pypdf `PdfWriter` (Python) | ✅ Reliable, scriptable |
| `pdfunite` (poppler) | ⚠️ AVOID for anything that matters — see Pitfalls |

## Verified Commands

```bash
# Merge in order (report → declaration → vg report)
qpdf --empty --pages "report.pdf" "declaration.pdf" "vg_report.pdf" -- "merged.pdf"

# Page count (integrity hint only, NOT proof — see Pitfalls)
qpdf --show-npages merged.pdf

# Structural check — must say "No syntax or stream encoding errors found"
qpdf --check merged.pdf

# Content spot-check: first page AND the boundary pages between inputs
pdftotext -f 1 -l 1 merged.pdf -          # first input's title page
pdftotext -f 18 -l 18 merged.pdf -        # first page of second input
pdftotext -f 20 -l 20 merged.pdf -        # last page of final input
```

## Pitfalls

- **Never write qpdf output over an input path.** `qpdf --empty --pages in.pdf x.pdf -- in.pdf` truncates the file it is still reading → "unexpected EOF reading stream data" / "object has offset 0" warnings and a corrupt result (observed: 29-page output whose first pages had no text). Always merge to a temp path, then `mv temp out.pdf` (atomic replace). This applies to ANY in-place overwrite of the file being read.
- **`pdfunite` silently drops text layers.** Observed: merging a 17-page report with two PDFs via `pdfunite` produced the *correct 20-page count* while pages 1–17 contained no extractable text (only page breaks). The user caught it ("有错误"). Re-merging the same sources with `qpdf --empty --pages` produced a clean file. Never trust `pdfunite` output without content verification; use qpdf from the start.
- **Page count is not integrity.** `qpdf --show-npages` reports the expected count even when content is destroyed. Always re-extract text from sampled pages and confirm expected headers appear (title page, section boundaries).
- **qpdf repair noise on damaged inputs:** merging a previously-corrupted file emits "Resources is missing or invalid; repairing" and "operation for dictionary attempted on object of type null" warnings. That signals the INPUT is damaged — re-merge from clean source files, don't repair the bad output. (Benign noise: "reported number of objects is not one plus the highest object number" = bookkeeping only.)
- **Deliverable naming:** when the merge target is an existing named deliverable (e.g. "{Author Name}_Final Report.pdf"), the user expects the result to REPLACE that file under the same name — do not create a sibling like "…+VeriGuide.pdf" unless asked. Confirm if ambiguous.
- **Re-merge when upstream changes:** if the merged deliverable includes a generated source (LaTeX recompile, margin change, etc.), re-run the full merge whenever any input changes — stale parts silently ship otherwise.

## Verification (minimum for a deliverable)

1. `qpdf --check` → "No syntax or stream encoding errors found"
2. Page count equals the sum of inputs
3. `pdftotext -f 1 -l 1` shows the first input's title-page text
4. `pdftotext -f <N> -l <N>` at each input boundary shows the expected heading (e.g. References page ending input 1, Declaration starting input 2)

---
name: drawing-register-qa
description: Reads the title blocks of a PDF drawing set (sheet number, title, revision, status, date, scale) and measures each sheet's paper size to build a drawing register, then checks it against the issued register or transmittal, reporting revision and status mismatches, title drift, sheets missing from the set or the register, duplicate numbers, and scales stated for the wrong paper size. Sheets with no text layer are flagged for OCR or manual entry, never guessed. Use when the architect wants to "check the drawing issue", "QA the set before it goes out", "build a drawing register from these PDFs", "does the transmittal match the drawings", "title block check", or "what revision is everything at". Pairs with markup-review for comments on the same set and project-email to send the issue.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Drawing Register QA

The tedious check before an issue goes out: does every PDF say what the register says it says? It is deterministic text extraction against a list, and nothing in it is guessed.

## When to use

- Before every formal issue (planning, tender, construction, a revision round).
- When receiving a consultant's set: build the register they didn't send.
- When the transmittal and the drawings disagree and someone needs the list of differences.

## Input

- **The PDF set**: one combined PDF, several files, or a folder. Vector PDFs exported from CAD or BIM work best.
- **The register to check against** (optional): a CSV with `number,title,revision,status,date` and optionally `scale,size`. Export it from the document control system, the BIM tool's sheet list, or a spreadsheet.
- **The title-block location** if it isn't bottom-right, and the office **sheet-number pattern** (for example ISO 19650-style `PRJ-ORG-ZZ-00-DR-A-1001`, or `A-101`) as a regex.

## Process

1. **Check one sheet first.** Run on the set without a register, then compare the first row against the actual PDF. If numbers or titles come out wrong, adjust `--tb` (title-block region as page fractions `x0,y0,x1,y1`) or `--number-regex`, and run again.
   `uv run scripts/register_qa.py set.pdf --out register.csv --tb 0.55,0.70,1.0,1.0`
2. **Run against the register.**
   `uv run scripts/register_qa.py set.pdf --out register.csv --register issued.csv --md qa.md`
3. **Read the flags.** NO TEXT LAYER means a scanned or flattened sheet; it needs OCR or manual entry, and the script leaves it blank. AMBIGUOUS means two candidate values were found, so check by eye. "not found" usually means the label or region is wrong, not that the field is missing. Check one before concluding.
4. **Report the issues** as a list someone can work through. Every mismatch shows what the register says and what the title block says.

## Domain knowledge

- **Extraction order.** Labelled fields come first ("Drawing No", "Rev", "Status", "Date", "Scale", "Title"), then patterns for revision, status, date and scale codes. Labels vary by office. If yours says "Dwg Ref" or "Suitability", read the script's `LABELS` table and extend it.
- **ISO 19650 status and revision codes.** Suitability codes such as S0 to S4 for shared work, A-codes for published or authorised, and revisions such as P01 (preliminary) or C01 (contractual) are recognised. Status meanings vary by national annex and project information protocol. Report the code as found. Don't interpret it beyond what the project's protocol says.
- **Sheet size is measured from the page box,** matched to ISO A and B, ANSI and ARCH sizes within 8 mm. A sheet that says "1:100 @ A1" but measures A3 is a real error; anyone scaling off it will be wrong by a factor of two.
- **Titles drift.** "&" vs "and", abbreviations, a renamed sheet. Titles are compared with a similarity ratio (flag below 90%), so cosmetic differences show up without hiding real renames. Judge each one.
- **Scanned sheets.** If a sheet has no text layer, the honest output is a blank and a flag. OCR (Tesseract, the PDF tool's own OCR) can be added as a separate step, and its output should still be checked.
- **What it doesn't check:** drawing content, cross-references between sheets, revision clouds against the revision table, or whether the right people signed off. Those are human checks. `markup-review` handles comments.

## Output format

```
## Drawing issue QA: [project], [issue name], [date]

Set: [n] sheets from [files]  |  Register: [file]  |  Issues: [n]

| Number | Field | Register | Title block | Check |
|---|---|---|---|---|
| A-1002 | revision | P02 | P01 | MISMATCH |

Unreadable sheets (manual entry needed): [file p.4 - no text layer]
Ambiguous fields (check by eye): [...]
Missing from set: [...]  |  Not in register: [...]  |  Duplicates: [...]

Files: register.csv (extracted), qa.md (this report)
```

## What you don't do

- Don't fill in a sheet number, revision or date the script couldn't read. Blank and flagged beats plausible and wrong.
- Don't decide which side is right when the register and title block disagree. Report both, and let document control decide.
- Don't interpret status codes beyond the project's information protocol.
- Don't call a set "checked" when sheets were unreadable. Say how many were verified and how many weren't.

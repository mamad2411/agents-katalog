---
name: spec-index
description: Turn a 500+ page construction specifications book (Divisions, Items, submittals, testing standards, cross-references) into a structured, queryable SQLite database, then answer compliance questions from the database instead of re-reading the raw PDF every time. Use when a user wants to list every submittal on a project, find every clause that cites a given ASTM/CSA standard, trace item-to-item cross-references, or ask repeated compliance questions about a spec book. Cuts token cost dramatically versus feeding raw spec pages into the prompt, and page-anchors every clause so answers cite the exact page.
---

# Spec Index

Contractors get handed a spec book. Nobody reads 500+ pages of Divisions 01-48
cover to cover, so buried requirements — a pre-blast survey submittal, a PACP
operator certificate, a precast plant CSA certification, atmospheric testing
required with every progress payment — get missed. Miss one and the Engineer
holds a payment or writes a change order.

This skill reads the spec once, extracts every division, item, "shall/must/submit"
clause, external standard reference (ASTM, CSA, AASHTO…), and item-to-item
cross-reference into SQLite, and then answers questions from the database.

**Why this beats re-reading the spec each time**
- Feeding raw spec pages into the prompt is expensive and unreliable — details
  buried on page 347 get mis-weighted or missed entirely.
- A 644-page spec book has ~1.4M characters of body and ~50 "shall/must" clauses
  per item. Reading it once at 2 min/page = ~21 hours of human time. Nobody does
  it.
- A SQL query returns the exact clause with a page anchor in milliseconds.

## The reliability rule (do not skip)

Regex-based clause extraction is high-recall but not zero-noise. Say so.

| Question type | How it's answered | Confidence |
|---|---|---|
| **"List every submittal in the book"** | rows in `requirements` tagged `submittal` | **high** — every hit is a real "submit" sentence |
| **"Which items reference ASTM C39?"** | rows in `refs` where `ref_code LIKE '%C39%'` | **high** — reads literal codes from the text |
| **"What page is Item 240 on?"** | `items.start_page` / `items.end_page` | **high** — page-anchored on ingest |
| **"What does the spec require for concrete curing?"** | FTS5 search on `items_fts` / `pages_fts` | **medium** — you get the right item, but read the clause before quoting |
| **Numeric extractions (MPa, mm, %)** | pattern-based, some false positives | **low** — verify against the source page |

Every clause carries a `page` column. When you hand a requirement to the user,
**cite the item number and page** so they can verify.

## Workflow

Scripts live in `scripts/`. Run with `py` on Windows (or `python3`).

1. **Extract the PDF to text** (Poppler `pdftotext` preserves layout and page
   breaks with `\f`):
   ```
   pdftotext -layout your-spec.pdf work/spec_full.txt
   ```

2. **Build the database** (one pass, seconds even on 600+ pages):
   ```
   py scripts/build_index.py
   ```
   Writes `outputs/spec_index.db` with:
   - `divisions` — 10 rows, page ranges
   - `items` — every numbered item (e.g. Item 130, Item 250.09), title, page range, full body
   - `requirements` — every "shall / must / submit / test / certify" sentence, tagged `submittal` / `testing` / `requirement`, page-anchored to its item
   - `refs` — every external standard reference (ASTM, CSA, AASHTO, ANSI, OPSS…) and every item-to-item cross-reference
   - `items_fts`, `pages_fts` — FTS5 for full-text search

3. **Answer questions from the DB**:
   ```
   py scripts/demo_queries.py       # sample: submittals, standards, FTS
   py scripts/killer_examples.py    # headline pulls: buried submittals, cross-ref chains, volume metrics
   ```
   Or any read-only SQL — see the README for query templates.

## How to use this as Claude

- When asked a compliance/submittal/standards question about a spec book,
  **check whether `outputs/spec_index.db` exists**. If yes, query it — do not
  re-read the PDF.
- If no DB exists, extract with `pdftotext` and `build_index.py` first, then
  query.
- For every requirement you cite, include **the item number and page** so the
  user can verify against the source. `Item 139 (Use of Explosives), p36:
  "A copy of this pre-blast survey shall be submitted…"`
- Only open the raw PDF page when the DB genuinely can't answer (e.g. the user
  is asking about a table or figure with no adjacent prose). Pull the single
  page, not the whole book.

## Tuning per spec (important, not fluff)

Spec books do not share a single structure. This indexer's regexes are tuned to
a **municipal / infrastructure spec** that uses `DIVISION N` all-caps headers
and `Item NNN` or `Item NNN.NN` numbered clauses (City of St. John's, and most
Canadian municipal specs, OPSS, MTO spec books, and similar). It works on that
family out of the box.

For a **CSI MasterFormat** spec (US commercial building specs — sections like
`SECTION 03 30 00 - CAST-IN-PLACE CONCRETE` with `PART 1 - GENERAL / PART 2 -
PRODUCTS / PART 3 - EXECUTION` inside each section), swap two things in
`scripts/build_index.py`:

- **`DIV_RE` / division anchor** — replace with a MasterFormat section-header
  regex (`^SECTION\s+(\d{2}\s\d{2}\s\d{2})\b`).
- **`ITEM_HDR`** — replace with `^PART\s+([123])\b` (or a paragraph-number
  regex like `^\s*(\d+\.\d+(?:\.\d+)?)\s+[A-Z]`) so each PART or paragraph
  becomes an "item" row.

Everything else — page anchoring, `shall/must/submit` classification, standard-
reference extraction (`ASTM|CSA|ANSI|AASHTO|CAN/CSA|ISO|OPSS|MTO`), FTS5 —
runs unchanged. The pipeline is universal; only the header regex is spec-family
specific.

Test any new spec family by running `build_index.py` and eyeballing
`divisions` and the first 20 `items`. If those look right, the rest of the
extraction will too.

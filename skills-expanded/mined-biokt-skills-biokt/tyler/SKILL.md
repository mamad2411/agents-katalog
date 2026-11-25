---
name: tyler
description: Convert a folder of academic PDF papers into a token-efficient markdown wiki for literature review. Use this skill when the user has a folder of PDFs they want processed into .md files that Claude Code can read cheaply. Trigger phrases include "convert my PDFs", "build my wiki", "process my papers folder", "/tyler".
allowed-tools: Bash, Read, Write, Edit
---

# PDF-to-Wiki Skill

## Purpose

This skill converts a directory of academic PDF papers into a structured, two-tier markdown wiki
optimised for token efficiency. A typical 10–25 page biophysics or computational biology paper
costs ~8,000–12,000 tokens to read as a full PDF. This skill produces:

- **Tier 1 — Index** (`index.md`): ~400 tokens per paper. Contains title, authors, year, journal,
  DOI, and abstract. For 100 papers, the entire index is ~40,000 tokens — easily readable in a
  single session.
- **Tier 2 — Full papers** (`papers/*.md`): Cleaned markdown with YAML frontmatter. Only read on
  demand when you need detail on a specific paper.

This means Claude can navigate a literature set of 100+ papers by reading just the index, then
selectively reading individual papers as needed.

> **Credit:** Adapted from the `tyler` skill by Johan Fourie
> ([github.com/johanfourieza/econtools](https://github.com/johanfourieza/econtools/blob/main/tyler/SKILL.md)),
> originally designed for economics literature. The two-tier architecture, conversion script, and
> incremental-update logic are his design. Adapted here for computational biology and biophysics.

## What this skill produces

```
WIKI_DIR/
├── index.md              # Auto-generated index with metadata + abstracts
├── papers/
│   ├── lindorff-larsen_2011.md
│   ├── best_2022.md
│   └── ...
└── .wiki_state.json      # Tracks converted files for incremental updates
```

Each `papers/*.md` file has YAML frontmatter:
```yaml
---
title: "How Fast-Folding Proteins Fold"
authors: "Kresten Lindorff-Larsen; Stefano Piana; Ron O. Dror; David E. Shaw"
year: "2011"
journal: "Science"
doi: "10.1126/science.1208351"
citekey: "lindorff-larsen2011"    # if --bib provided
keywords: "protein folding, molecular dynamics, force field"
source_pdf: "Lindorff-Larsen_2011.pdf"
---
```

## Step-by-step instructions

### Step 0: Ask the user for inputs

Ask the user for:

- **PDF_DIR**: Full path to the folder containing the PDF files.
- **WIKI_DIR**: Where to create the wiki. Default: `wiki/` in the current working directory.
- **BIB_FILE** (optional): Path to a `.bib` file for citation key matching.
- **Recursive?** (optional): Whether to scan subdirectories. Default: no.

Confirm paths before proceeding.

### Step 1: Check and install the conversion library

```bash
python -c "import pymupdf4llm" 2>/dev/null || pip install pymupdf4llm --break-system-packages --quiet
```

If pip fails, try:
```bash
pip install pymupdf4llm --user --quiet
```

Report success or failure before continuing.

### Step 2: Run the conversion script

```bash
python ${CLAUDE_SKILL_DIR}/convert.py "PDF_DIR" "WIKI_DIR" [OPTIONS]
```

**Available flags:**
- `--recursive` or `-r`: Scan PDF_DIR recursively
- `--bib PATH`: Path to a .bib file for citation key matching
- `--keep-references`: Keep the references section (default: trimmed to save tokens)
- `--force`: Re-convert all files, ignoring incremental cache

The script handles everything automatically:
1. Finds all PDFs (skips unchanged files in incremental mode)
2. Converts each to markdown via pymupdf4llm
3. Extracts metadata: title, authors, year, journal, DOI, abstract, keywords
4. Cleans the text: strips repeated headers/footers, page numbers, publisher boilerplate
5. Trims the references section (unless --keep-references)
6. Writes each paper as a `.md` file with YAML frontmatter
7. Builds `index.md` automatically from extracted metadata
8. Saves state for incremental updates

**Important:** The index is built entirely in Python from extracted metadata — Claude does NOT
need to read individual paper files to build it.

### Step 3: Report to the user

After the script finishes, tell the user:

- How many PDFs were found, converted, skipped, and failed
- The location of the wiki directory and index file
- The token savings (the script prints this)
- Any failed files and likely causes (scanned PDFs, corrupted files)

Then explain how to use the wiki in future sessions:

> **Using your wiki:** In any Claude Code session, read `WIKI_DIR/index.md` to see all papers
> with their abstracts. Ask questions referencing the index — individual `papers/*.md` files are
> only read when full text is needed. Use Grep to search across all papers for specific terms,
> methods, or systems.

### Step 4 (optional): Improve the index with Claude

If the user wants richer summaries beyond extracted abstracts, offer to enhance the index:

- Read papers where abstract extraction failed or was weak
- Add a 1–2 sentence "contribution" note per paper
- Group papers by topic (e.g. force fields, enhanced sampling, IDPs, folding kinetics)

Only do this if the user explicitly asks.

## Gotchas and known issues

- **Scanned PDFs**: pymupdf4llm extracts embedded text only. Scanned-image PDFs produce
  empty/near-empty output. The script flags these (<500 bytes). Fix: run `ocrmypdf` first.
- **Metadata extraction is heuristic**: Works well for standard journal layouts (J. Chem. Phys.,
  JCTC, Biophys. J., PNAS, J. Phys. Chem., Nature, Science) but may fail on unusual formats.
- **BibTeX matching is fuzzy**: Title word overlap + author + year, threshold score ≥ 6. Some
  papers may not match — check the index for missing citekeys.
- **DOI extraction**: Scans the first ~3000 characters. May miss DOIs buried deep in footers.
- **Re-running**: Incremental by default — only re-converts new or changed PDFs. Use `--force`
  to re-convert everything.
- **References trimmed by default**: Removes ~20–30% of tokens per paper. Use `--keep-references`
  if you need to follow citations.

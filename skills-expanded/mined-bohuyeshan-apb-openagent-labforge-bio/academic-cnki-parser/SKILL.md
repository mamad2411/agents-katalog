---
name: academic-cnki-parser
description: Parse CNKI (China National Knowledge Infrastructure) export files in multiple formats (.txt, .net, .ris, .bib, .enw) into unified BibTeX. Use when the user has downloaded reference files from CNKI website in any supported format.
tool_type: python
primary_tool: bibtexparser
---

# Academic CNKI Parser

Parse CNKI export files in various formats into unified BibTeX entries.
Supports automatic format detection, multi-file merging, and deduplication.

## Supported CNKI Export Formats

| File Extension | CNKI Export Format | Priority |
|---------------|-------------------|----------|
| `.bib` | BibTeX | Best — direct use, no parsing needed |
| `.net` | NoteExpress | Use `cnki2bib` tool for conversion |
| `.enw` | EndNote | Parsed automatically |
| `.ris` | EndNote (RIS) | Parsed automatically |
| `.txt` (with `SrcDatabase-来源库:`) | CNKI Detailed Export | Parsed automatically |
| `.txt` (with `[N]` numbered format) | GB/T 7714 / MLA / APA | Parsed automatically (limited metadata) |

## Quick Start

```bash
# Install dependencies
pip install bibtexparser
pip install cnki2bib  # for .net → .bib conversion

# Parse a single file and output BibTeX
python scripts/cnki_parser.py parse "path/to/CNKI-export.txt"

# Merge all files in a directory (auto-detect formats, dedup by title)
python scripts/cnki_parser.py merge "path/to/downloads/论文/"
```

## Workflow

```
User downloads from CNKI (manual, due to captcha):
  ├── .bib  →  direct use
  ├── .net  →  cnki2bib → .bib
  ├── .enw  →  auto-parse → .bib
  ├── .txt (detailed)  →  auto-parse → .bib
  └── other formats  →  auto-detect + parse → .bib
  
  All → merged .bib → ready for pandoc/papis/zotero
```

## Output Format

The parser outputs BibTeX entries suitable for:
- **Pandoc --citeproc**: `pandoc draft.md --citeproc --bibliography=refs.bib -o output.docx`
- **Papis**: `papis add --from bibtex refs.bib`
- **Zotero**: Import `.bib` file directly

## Dependencies

Check before use:
- `python -c "import bibtexparser"` — core dependency
- `cnki2bib --help` — optional, for .net file conversion

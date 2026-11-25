---
name: arxiv-reading
description: Use this skill when the user provides an arXiv ID (e.g., arXiv:2508.12856) and asks to read, analyze, or extract equations from the paper. Activates for literature review, equation extraction, paper understanding, and cross-referencing tasks in academic research contexts.
---

# arXiv Literature Reading Protocol

## Overview
When an arXiv ID is provided, use the scripts in `scripts/` to download, extract, and analyze the paper. Write a memory file `<user-working-dir>/arxiv-reading/<arxiv-id>.memory.md` for further checking. 

**IMPORTANT — Cache directory is the user's working directory:**
All cache files live under `<user-working-dir>/arxiv-reading/` — NOT the skill's directory. The user's working directory is the "Primary working directory" shown in the system context (session working directory), **not** the skill's installation directory.

Always construct absolute paths manually using the known working directory from the conversation context.The shell's `$PWD` and Python's `os.getcwd()` are **unreliable** because the skill may run from its own directory. 

## Script-based Workflow

### 0. Check for cached data
Before downloading, check if the memory file `<user-working-dir>/arxiv-reading/<arxiv-id>.memory.md` already exists. If it does, directly read it and find information. If you need more information, check individual sections at `<arxiv-id>.sections_content.json` in the same directory.

Example:
```bash
memory_file="<user-working-dir>/arxiv-reading/<arxiv-id>.memory.html"
if [ -f "$cache_file" ]; then
  echo "Cache hit: $cache_file"
fi
```

### 1. Download ar5iv HTML (only if not cached)
If no cached file exists, use the skill's `fetch.py` to download the ar5iv HTML version. Always pass `--out-dir` with the absolute path to `<user-working-dir>/arxiv-reading/`.

- **Primary Source**: `https://ar5iv.labs.arxiv.org/html/<arxiv-id>`
- Uses `requests`; falls back to `curl`.
- Output is always written to `<user-working-dir>/arxiv-reading/<arxiv-id>.html`.
- Call with: `python3 <skill-dir>/scripts/fetch.py --out-dir <user-working-dir>/arxiv-reading <arxiv-id>`

Where `<skill-dir>` is `~/.claude/skills/arxiv-reading/` and `<user-working-dir>` is the session's primary working directory.

### 2. Equation Extraction
Use `extract_eqs.py` to extract all LaTeX equations with their numbers and surrounding context.

Call with the absolute path to the cached HTML:
```bash
python3 <skill-dir>/scripts/extract_eqs.py <user-working-dir>/arxiv-reading/<arxiv-id>.html
```

**Auto-caching**: On first run, saves JSON to `<arxiv-id>.eqs.json`. Subsequent runs read from cache directly.

### 3. Section Extraction (for targeted reading)
Use `extract_sections.py` to list all sections or to extract a specific section's content as clean plain text.

Call with the absolute path to the cached HTML:
```bash
python3 <skill-dir>/scripts/extract_sections.py <user-working-dir>/arxiv-reading/<arxiv-id>.html
python3 <skill-dir>/scripts/extract_sections.py <user-working-dir>/arxiv-reading/<arxiv-id>.html "Section Name"
```

**Auto-caching**: Section listing is cached as `<arxiv-id>.sections.json`. On first content extraction, ALL sections' content is cached as `<arxiv-id>.sections_content.json`. Future reads (even for different sections) use cache.

### 4. LaTeX to Plain Text (for equation comprehension)
Use `latex_simplify.py` to convert a LaTeX math string into readable plain text (Greek unicode, simplified fractions, etc.).

**Auto-caching**: Results are cached in `~/.cache/arxiv-reading/latex_simplify_cache.json` keyed by MD5 hash. Repeated calls with the same LaTeX string return instantly.

### 5. Memory file
Generate memory file `<user-working-dir>/arxiv-reading/<arxiv-id>.memory.md` for further checking.

File size: as a memory file for you to read comfortably.

- Summary per section & subsection: Write a summary of each section and subsection (if exists). So that you can find which section to further read in need.
- Equations: Note important equations (use `latex_simplify.py` to convert latex symbols to utf8 for readability) with their equation number. The user may refer to the equation number and you need to find the equation.  Write a brief description of each equation. For short papers (the largest equation number is less than 15), note down all equations. 
- References: Note down main references for further studies. **Important:** note down the title and arxiv number `arXiv:xxxx.xxxxx` of each reference (if available).
- Related to research mission: If you know the purpose of the current research, note down more details related to the current research. 

## Verification
1. Run `extract_eqs.py` to get all equations with their numbers.
2. Cache file `<arxiv-id>.eqs.json` is created alongside the HTML.
3. Cross-reference extracted formulas with the paper's internal equation numbering.
4. If numbering seems off, delete the `.eqs.json` cache and re-run to force re-extraction.
5. The memory file <arxiv-id>.memory.md is generated.

## Available scripts

Scripts are located at the skill's directory (`~/.claude/skills/arxiv-reading/scripts/`). Always reference them by absolute path.

| Script | Purpose | Usage |
|--------|---------|-------|
| `fetch.py` | Download ar5iv HTML for an arXiv ID | `python3 <skill-dir>/scripts/fetch.py --out-dir <user-working-dir>/arxiv-reading <arxiv-id>` |
| `extract_eqs.py` | Extract LaTeX equations as JSON from HTML | `python3 <skill-dir>/scripts/extract_eqs.py <user-working-dir>/arxiv-reading/<id>.html` |
| `extract_sections.py` | List sections or extract a section's content | `python3 <skill-dir>/scripts/extract_sections.py <user-working-dir>/arxiv-reading/<id>.html ["Section Name"]` |
| `latex_simplify.py` | Convert LaTeX math to readable plain text | `python3 <skill-dir>/scripts/latex_simplify.py "<latex>"` |

## Cache files

All cache files live under `<user-working-dir>/arxiv-reading/`. The `latex_simplify_cache.json` lives in `~/.cache/arxiv-reading/` (shared across all projects).

| Cache file | Content | Created by |
|---|---|---|
| `<arxiv-id>.html` | Raw ar5iv HTML | `fetch.py` |
| `<arxiv-id>.eqs.json` | Extracted equations with tex, context, numbers | `extract_eqs.py` |
| `<arxiv-id>.sections.json` | Section list with titles and offsets | `extract_sections.py` |
| `<arxiv-id>.sections_content.json` | All section content as `{title: plain_text}` | `extract_sections.py` (content mode) |
| `~/.cache/arxiv-reading/latex_simplify_cache.json` | LaTeX→plain-text lookup table (MD5-keyed) | `latex_simplify.py` |

### Cache invalidation
To force re-extraction from HTML, delete the corresponding cache file (e.g., `rm <arxiv-id>.eqs.json`). The scripts will re-extract and re-cache on next run.

## Notes
- All cache files are read/written under `<user-working-dir>/arxiv-reading/` — the `arxiv-reading/` directory in the user's session working directory, **not** the skill's installation directory.
- The shell environment `$PWD` and Python `os.getcwd()` may point to the skill's directory. **Do not rely on them.** Always substitute `<user-working-dir>` with the absolute path from the conversation context.
- If `requests` is not installed, use `curl` as a fallback:
  ```bash
  mkdir -p "<user-working-dir>/arxiv-reading"
  curl -sL "https://ar5iv.labs.arxiv.org/html/<id>" -o "<user-working-dir>/arxiv-reading/<id>.html"
  ```
- For PDF-only papers (no ar5iv), inform the user and suggest an alternative download method.
- ar5iv HTML files contain massive MathML markup. Running `grep` on them produces enormous output that gets persisted to disk, triggering permission prompts.

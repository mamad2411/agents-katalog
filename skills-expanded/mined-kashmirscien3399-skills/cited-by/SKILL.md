---
name: cited-by
description: Search for papers that cite a given arXiv paper on INSPIRE-HEP, cache the citation list, filter by topic, and optionally read matching papers. Trigger when the user asks to find papers citing a specific arXiv paper, especially "在引用 arxiv:... 的文献中搜索XXX", "look for XXX from those cited arxiv:...", "find papers citing arxiv:... about XXX", etc.
---

# Cited-By Literature Search Protocol

## Overview
Given an arXiv ID and an optional topic, fetch all papers that cite the given paper via INSPIRE-HEP, cache the full list as a compact markdown file, filter for topic relevance, and present candidate papers to the user. If the user approves specific papers, delegate to the **arxiv-reading** skill to read each one and produce a report.

## Output format

The cache file is a markdown file with pipe-separated fields:

```
# Citing Papers for arXiv:0911.3380
**Total:** 500 papers | **Topic:** cosmology

1. Paper Title | Author1, Author2, Author3 | cited 42 | arXiv:1234.5678
2. Another Title | Author1 et al. | cited 15 | (no arXiv ID)
```

- Authors are comma-separated, truncated to first 6 + "et al." for large collaborations.
- No INSPIRE IDs or year fields are stored, to keep the file compact.

## Workflow

### Step 1 — Fetch citing papers

Use `scripts/fetch_citations.py` to search INSPIRE-HEP and cache all citing papers.

```bash
python3 <skill-dir>/scripts/fetch_citations.py --out-dir <user-working-dir>/arxiv-reading <arxiv-id>
```

Where `<skill-dir>` is `~/.claude/skills/cited-by/` and `<user-working-dir>` is the session's primary working directory.

If the user provides a topic filter, pass `--topic`:
```bash
python3 <skill-dir>/scripts/fetch_citations.py --out-dir <user-working-dir>/arxiv-reading --topic "<topic>" <arxiv-id>
```

The script outputs a markdown file at `<user-working-dir>/arxiv-reading/arXiv_<arxiv-id>_citations.md`.

### Step 2 — Check cache

Before running `fetch_citations.py`, check if `<user-working-dir>/arxiv-reading/arXiv_<arxiv-id>_citations.md` already exists. If it does and the user hasn't asked for a refresh, skip the download and read the cached file directly.

Example:
```bash
cache_file="<user-working-dir>/arxiv-reading/arXiv_<arxiv-id>_citations.md"
if [ -f "$cache_file" ]; then
  echo "Cache hit: $cache_file"
fi
```

### Step 3 — Filter by topic and present candidates

Read the cached markdown file and filter papers whose title or authors match the topic the user requested:

1. Read the `.md` file to get all papers (each line after the header is `N. Title | Authors | cited N | arXiv:ID`).
2. Search for topic keywords in paper titles and authors.
3. Rank candidates by relevance (title match first, then citation count).
4. Present the candidate list (up to ~15 papers) as a numbered table with columns: #, Title, Authors, Cited, arXiv.
5. Ask the user which papers they want to read (by number, or "all", or refine the topic).

### Step 4 — Read approved papers

For each paper the user approves, invoke the **arxiv-reading** skill to download and read it. Collect findings.

### Step 5 — Generate report

After reading all approved papers, generate a report summarizing how each paper relates to the user's topic of interest. The report should be written to `<user-working-dir>/arxiv-reading/<arxiv-id>_citing_report_<topic>.md`.

## Available scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/fetch_citations.py` | Fetch all citing papers from INSPIRE-HEP, output compact `.md` | `python3 <skill-dir>/scripts/fetch_citations.py --out-dir <user-working-dir>/arxiv-reading [--topic "keyword"] <arxiv-id>` |

## Notes

- All cache files are read/written under `<user-working-dir>/arxiv-reading/`.
- `<skill-dir>` is `~/.claude/skills/cited-by/`.
- `<user-working-dir>` is the session's primary working directory — use the absolute path from the conversation context, never `$PWD` or `os.getcwd()`.
- The INSPIRE API returns at most 250 results per page; `fetch_citations.py` handles pagination automatically.
- Authors are stored as a comma-separated string (not a list); collaborations with >6 authors are truncated to first 6 + "et al.".
- No INSPIRE record IDs or publication years are stored — this keeps the cache file compact for LLM reading.
- The file format changed from JSON to markdown for ~50% smaller file size and easier LLM consumption.
- Always confirm with the user before delegating to arxiv-reading for individual papers (it involves downloading HTML).
- If `requests` is not installed: `pip install requests`.

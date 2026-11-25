---
name: wikify
description: "Generate a Karpathy-style wiki from a thesis, report, paper, or project. Extracts papers, methods, concepts, and techniques into organized, cross-referenced wiki articles. Trigger: generate wiki, create wiki, wiki of this, /wikify"
---

# /wikify — Knowledge Wiki Generator

Turn any thesis, report, paper, or codebase into a navigable wiki of concepts, methods, papers, and techniques. Output is a folder of interlinked Markdown articles — like Karpathy's LLM Wiki, but generated from your input.

## Usage

```
/wikify                                              # generate wiki from current directory
/wikify <path>                                       # generate wiki from specific path
/wikify <path> --type thesis                         # treat input as academic thesis
/wikify <path> --type project                        # treat input as software project
/wikify <path> --type paper                          # treat input as single paper/report
/wikify <path> --output <dir>                        # write wiki to custom output directory
/wikify <path> --depth shallow|deep                  # extraction depth (default: deep)
/wikify <path> --language en|zh|...                  # output language (default: en)
/wikify add <path>                                   # add new file to existing wiki, update
```

## What wikify is for

Drop a thesis, research paper, technical report, or codebase into wikify and get a structured wiki:
- **Thesis/paper**: extracts methods, algorithms, datasets, baselines, related work, mathematical formulations
- **Project**: extracts architecture patterns, key algorithms, data flows, dependencies, design decisions
- **Report**: extracts findings, methodologies, frameworks, technical concepts

Output is a folder of Markdown files with an `index.md` entry point, cross-references between articles, and a clear hierarchy. Unlike a knowledge graph (which is node-edge focused), the wiki is **article-focused** — each concept gets a full page with context, definitions, relationships, and source citations.

## What You Must Do When Invoked

If the user invokes `/wikify --help` or `/wikify -h`, print the contents of the `## Usage` section above verbatim and stop.

If no path was given, use `.` (current directory). Do not ask the user for a path.
If no `--type` was given, auto-detect from file types and structure.

Follow these steps in order. Do not skip steps.

### Step 1 - Detect input type and files

Scan the target path and classify:

```bash
python3 -c "
import os, json
from pathlib import Path

target = Path('INPUT_PATH')
files_by_type = {'pdf': [], 'tex': [], 'md': [], 'py': [], 'ts': [], 'js': [], 'go': [], 'rs': [], 'java': [], 'cpp': [], 'c': [], 'rb': [], 'other_code': [], 'docs': []}

doc_exts = {'.md', '.rst', '.txt', '.org', '.adoc'}
code_exts = {'.py', '.ts', '.js', '.go', '.rs', '.java', '.cpp', '.c', '.rb', '.swift', '.kt', '.cs', '.scala', '.php'}

for f in target.rglob('*'):
    if f.is_file() and not f.name.startswith('.'):
        ext = f.suffix.lower()
        rel = str(f.relative_to(target))
        if ext == '.pdf': files_by_type['pdf'].append(rel)
        elif ext in {'.tex', '.latex'}: files_by_type['tex'].append(rel)
        elif ext in doc_exts: files_by_type['docs'].append(rel)
        elif ext in code_exts: files_by_type[ext.lstrip('.')] = files_by_type.get(ext.lstrip('.'), []) + [rel]
        # ... categorize remaining

total = sum(len(v) for v in files_by_type.values())
print(json.dumps({'files': files_by_type, 'total': total}, indent=2))
" > wiki-out/.wiki_detect.json
```

Classify the input:
- If `.pdf` or `.tex` files dominate → `thesis` or `paper`
- If code files dominate → `project`
- If `.md`/`.rst`/`.txt` dominate → `report`
- Mixed → ask the user which type, or default to `project`

Print a clean summary:
```
Corpus: X files
  Type: thesis | project | paper | report
  pdf:    N files
  code:   N files
  docs:   N files
```

If `total` is 0: stop with "No supported files found in [path]."

### Step 1b - Pre-extract PDF and LaTeX to Markdown

Before subagents can process `.pdf` or `.tex` files, convert them to plain `.md`:

```bash
python3 -c "
import json, subprocess, sys
from pathlib import Path

detect = json.loads(Path('wiki-out/.wiki_detect.json').read_text(encoding='utf-8'))
files = detect['files']
converted = []

# Convert .pdf -> .md via pypdf or pdftotext
for f in files.get('pdf', []):
    src = Path('INPUT_PATH') / f
    out = Path('wiki-out/.pre') / f.with_suffix('.md').name
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        import pypdf
        reader = pypdf.PdfReader(str(src))
        text = '\n'.join(page.extract_text() for page in reader.pages)
        out.write_text(text, encoding='utf-8')
        converted.append(str(out))
    except Exception as e:
        print(f'Warning: failed to extract {f}: {e}')

# Convert .tex -> .md (strip commands, keep structure + math)
for f in files.get('tex', []):
    src = Path('INPUT_PATH') / f
    out = Path('wiki-out/.pre') / f.with_suffix('.md').name
    out.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding='utf-8')
    # Basic cleanup: remove comments, strip section/begin/end commands, keep math
    import re
    text = re.sub(r'%.*', '', text)                          # comments
    text = re.sub(r'\\section\{(.+?)\}', r'# \1', text)      # sections
    text = re.sub(r'\\subsection\{(.+?)\}', r'## \1', text)
    text = re.sub(r'\\subsubsection\{(.+?)\}', r'### \1', text)
    text = re.sub(r'\\textbf\{(.+?)\}', r'**\1**', text)     # bold
    text = re.sub(r'\\textit\{(.+?)\}', r'*\1*', text)       # italic
    text = re.sub(r'\\begin\{equation\}.*', r'```math', text)
    text = re.sub(r'\\end\{equation\}.*', r'```', text)
    text = re.sub(r'\\cite\{.*?\}', '[citation]', text)       # citations
    text = re.sub(r'\\ref\{.*?\}', '[ref]', text)             # refs
    text = re.sub(r'\\[a-zA-Z]+(\[.*?\])?\{.*?\}', '', text)  # remaining commands
    out.write_text(text, encoding='utf-8')
    converted.append(str(out))

# Add converted files to the docs list for chunking
if converted:
    files.setdefault('docs', []).extend(converted)
    detect['total'] = sum(len(v) for v in files.values() if isinstance(v, list))
    Path('wiki-out/.wiki_detect.json').write_text(json.dumps(detect, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Pre-extracted {len(converted)} files (pdf/tex -> md)')
else:
    print('No pdf/tex files to pre-extract')
"
```

After this step, the file list in `wiki-out/.wiki_detect.json` has `.pdf` and `.tex` replaced by their `.md` equivalents. Proceed to Step 2 using the updated detect file.

### Step 2 - Extract concepts, methods, and relationships

**This step uses subagents for parallel extraction. You MUST use the Agent tool — reading files one-by-one is forbidden.**

Before dispatching, print a timing estimate:
- Estimate agents needed: `ceil(total_files / 15)` (chunk size ~15 for dense extraction)
- Print: "Wiki extraction: ~N files → X agents, estimated ~Ys"

#### Step 2a - Split into chunks

Split files into chunks of 10-15 files each. Group files from the same directory together. Each chunk should be thematically coherent (e.g., all files from `methods/` together, all from `related_work/` together).

Write each chunk to `wiki-out/.wiki_chunk_NN.json` with the file list and type hint.

#### Step 2b - Dispatch ALL subagents in a single message

Call the Agent tool multiple times **IN THE SAME RESPONSE** — one call per chunk. Use `subagent_type="general-purpose"`.

Each subagent receives this prompt (substitute CHUNK_NUM, TOTAL_CHUNKS, FILE_LIST, CHUNK_PATH, INPUT_TYPE, DEPTH):

```
You are a wikify extraction subagent. Read the files listed below and extract wiki article data.

Files (chunk CHUNK_NUM of TOTAL_CHUNKS):
FILE_LIST

Input type: INPUT_TYPE (thesis | project | paper | report)
Depth: DEPTH (shallow = major concepts only, deep = include sub-concepts and details)

## Extraction Rules

Extract the following from each file:

### For thesis/paper:
- **Methods**: named algorithms, techniques, architectures, frameworks (e.g., "Transformer", "LoRA", "PPO")
- **Mathematical formulations**: key equations, loss functions, theorems (with LaTeX)
- **Datasets**: named datasets used or referenced
- **Baselines**: comparison methods/models mentioned
- **Related work**: papers cited, authors, contributions
- **Concepts**: domain-specific terminology, abstractions, design patterns
- **Findings**: key results, claims, contributions

### For project:
- **Architecture patterns**: MVC, event sourcing, CQRS, microservices, etc.
- **Key algorithms**: named or significant algorithms in the code
- **Data models**: entities, schemas, data flows
- **Dependencies**: external libraries, frameworks, services
- **Design decisions**: non-obvious choices, trade-offs (from comments, ADRs, docs)
- **APIs/Interfaces**: public interfaces, contracts
- **Concepts**: domain terminology, abstractions

### For report:
- **Methodologies**: frameworks, approaches, processes
- **Findings**: results, conclusions, recommendations
- **Concepts**: domain terminology, frameworks referenced
- **Sources**: external references, citations

## Output Format

For each extracted item, produce a wiki article entry:

```json
{
  "articles": [
    {
      "id": "snake_case_unique_id",
      "title": "Human Readable Title",
      "canonical": "snake_case_canonical_key",
      "status": "confirmed | ambiguous",
      "category": "method | concept | paper | dataset | architecture",
      "summary": "2-3 sentence summary of what this is",
      "details": "Longer description with context, how it's used, why it matters",
      "source_files": ["relative/path/to/file1", "relative/path/to/file2"],
      "source_locations": ["file1:line42", "file2:line100"],
      "related_to": ["other_article_id_1", "other_article_id_2"],
      "formulation": "LaTeX equation if applicable",
      "references": ["Author et al. (Year). Paper Title. Venue."]
    }
  ]
}
```

**ID rules:**
- `id` must be **path-scoped** and deterministic: `{source_file_stem}_{concept}`. Example: `chapter3_transformer_attention`, `utils_parse_url`. This guarantees no cross-chunk collisions — two subagents processing different files will never produce the same `id`.
- `canonical` is the **conceptual group key**: just the concept name, no file prefix. Example: `transformer_attention`. Multiple articles from different source files describing the same concept must use the same `canonical` value.
- Both: lowercase, only `[a-z0-9_]`, no dots or slashes.
- CRITICAL: always use the full canonical name consistently across chunks. If a concept appears in files processed by different subagents, they MUST use the same `canonical` value.

**Category rules (exactly 5):**
- `method`: technique, algorithm, approach, or baseline (e.g., "fine-tuning", "Transformer", "PPO")
- `concept`: domain term, abstraction, finding, or mathematical idea (e.g., "attention mechanism", "eventual consistency")
- `paper`: a cited paper, reference, or related work
- `dataset`: a named dataset (e.g., "ImageNet", "CommonCrawl")
- `architecture`: system pattern, design decision, API contract, or dependency (e.g., "microservices", "event sourcing")

**Status rules:**
- `confirmed`: source adequately defines or explains the concept
- `ambiguous`: concept is mentioned/used but not sufficiently defined or explained in the source

**Related edges:**
- `related_to` must use **canonical keys**, not `id`s. This guarantees cross-chunk links survive consolidation — if two subagents from different chunks write `related_to: ["transformer_attention"]`, they'll resolve to the same merged article.
- Only link to canonical keys you are confident exist — do not halluciate connections.

## Depth Guidance

- **shallow**: Extract only major, named concepts. Skip sub-variants and implementation details.
- **deep**: Extract everything — sub-concepts, variants, implementation details, edge cases.

Output ONLY valid JSON matching the schema above — no explanation, no markdown fences, no preamble.

Then write the JSON to disk at this exact absolute path:
CHUNK_PATH
```

### Step 2c - Collect and merge

Wait for all subagents. For each result:
- Check that `wiki-out/.wiki_chunk_NN.json` exists on disk
- If missing, print a warning and skip that chunk
- If more than half the chunks are missing, stop and tell the user to re-run

Merge all chunk files into `wiki-out/.wiki_merged.json`:

```bash
python3 -c "
import json, glob
from pathlib import Path

chunks = sorted(glob.glob('wiki-out/.wiki_chunk_*.json'))
all_articles = []
for c in chunks:
    d = json.loads(Path(c).read_text(encoding='utf-8'))
    all_articles.extend(d.get('articles', []))

# Phase 1: Deduplicate by id (path-scoped, collision-free)
id_seen = {}
for a in all_articles:
    if a['id'] in id_seen:
        existing = id_seen[a['id']]
        existing['source_files'] = list(set(existing['source_files'] + a['source_files']))
        existing['source_locations'] = list(set(existing.get('source_locations', []) + a.get('source_locations', [])))
        existing['related_to'] = list(set(existing.get('related_to', []) + a.get('related_to', [])))
        if len(a.get('details', '')) > len(existing.get('details', '')):
            existing['details'] = a['details']
        existing['references'] = list(set(existing.get('references', []) + a.get('references', [])))
    else:
        id_seen[a['id']] = a

# Phase 2: Consolidate by canonical — merge articles describing the same concept
# from different source files into one wiki page
canon_seen = {}
for a in id_seen.values():
    c = a.get('canonical', a['id'])
    if c in canon_seen:
        existing = canon_seen[c]
        existing['source_files'] = list(set(existing['source_files'] + a['source_files']))
        existing['source_locations'] = list(set(existing.get('source_locations', []) + a.get('source_locations', [])))
        existing['related_to'] = list(set(existing.get('related_to', []) + a.get('related_to', [])))
        if len(a.get('details', '')) > len(existing.get('details', '')):
            existing['details'] = a['details']
        existing['references'] = list(set(existing.get('references', []) + a.get('references', [])))
        # Keep first-seen id as the canonical article filename
    else:
        canon_seen[c] = a

# Phase 3: Remap related_to — translate any stray ids to their canonical key
id_to_canon = {}
for a in id_seen.values():
    id_to_canon[a['id']] = a.get('canonical', a['id'])
for a in deduped:
    a['related_to'] = [id_to_canon.get(r, r) for r in a.get('related_to', [])]

Path('wiki-out/.wiki_merged.json').write_text(json.dumps({'articles': deduped}, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Merged {len(chunks)} chunks: {len(deduped)} unique articles')
"
```

### Step 3 - Organize into wiki structure

Read `wiki-out/.wiki_merged.json` and organize articles into a wiki hierarchy:

```bash
python3 -c "
import json
from pathlib import Path

data = json.loads(Path('wiki-out/.wiki_merged.json').read_text(encoding='utf-8'))
articles = data['articles']

# Group by category
categories = {}
for a in articles:
    cat = a['category']
    categories.setdefault(cat, []).append(a)

# Build category index
index = {'categories': {}, 'total_articles': len(articles)}
for cat, arts in sorted(categories.items()):
    index['categories'][cat] = {
        'count': len(arts),
        'articles': [{'id': a['id'], 'title': a['title']} for a in arts]
    }

Path('wiki-out/.wiki_index.json').write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Organized {len(articles)} articles into {len(categories)} categories')
"
```

### Step 4 - Generate wiki articles

Create the wiki output directory (default: `wiki-out/wiki/`, or `--output <dir>` if given).

For each article, generate a Markdown file. The article format:

```markdown
# {title} {if status == "ambiguous": "⚠️"}

**Category:** {category}
**Status:** {status}
**Sources:** {source_files}

## Overview

{summary}

## Details

{details}

{if formulation: "## Mathematical Formulation\n\n{formulation}"}

{if references: "## References\n\n" + formatted references}

## Related

{links to related articles as [[article_id|title]]}
```

Generate `index.md` in the wiki root:

```markdown
# Wiki: {project_name}

Generated from {input_path}

## Categories

| Category | Count |
|----------|-------|
{for each category: "| [{category}](category/{category}.md) | {count} |"}

## All Articles

{alphabetical list of all articles with category tags}
```

Generate one `category/{category}.md` index per category:

```markdown
# {Category}

{count} articles

| Article | Summary |
|---------|---------|
{for each article: "| [{title}]({id}.md) | {summary} |"}
```

### Step 5 - Report

Print the final summary:

```
Wiki generated: {output_path}/

  index.md              - wiki entry point
  {N} articles          - individual concept pages
  {M} categories        - category index pages

Categories:
  methods:     N articles
  concepts:    N articles
  algorithms:  N articles
  ...
```

Then show the top 5 most-connected articles (by `related_to` count) as "Hub Concepts":

```
Hub Concepts (most connected):
  1. {title} — {count} connections
  2. {title} — {count} connections
  ...
```

---

## Honesty Rules

- Do NOT invent papers, methods, or concepts that are not in the source files
- Do NOT fabricate citations or references
- If a concept is mentioned but not explained in the source, mark it as `AMBIGUOUS` in the article
- If the source is unclear about how something works, say so explicitly
- Cross-reference claims with source file paths and line numbers

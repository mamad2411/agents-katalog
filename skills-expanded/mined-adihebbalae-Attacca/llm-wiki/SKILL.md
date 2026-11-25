---
name: llm-wiki
description: "Build and maintain a persistent, compounding LLM-maintained knowledge base (wiki). Use when: setting up a second brain for a project or personal knowledge base, processing PDFs/articles/notes into structured wiki pages, querying accumulated knowledge with citations, health-checking a wiki for gaps and contradictions, or building self-updating knowledge systems. Based on Karpathy's LLM Wiki pattern (gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)."
---

<!-- Delete when: native Claude Code persistent knowledge base with automated ingestion and query UI is available -->

# LLM Wiki Skill

## When to Use
- Starting a knowledge base for a project, research area, or personal domain
- Processing PDFs, articles, or notes into structured wiki pages (`/ingest`)
- Answering questions from accumulated knowledge with citations (`/query`)
- Health-checking the wiki for gaps, orphans, and contradictions (`/lint-brain`)
- Bootstrapping a new wiki for a codebase with dense documentation
- Weekly automated knowledge maintenance via GitHub Actions

## Core Idea (from Karpathy)
Standard RAG re-derives knowledge from scratch on every query. The wiki pattern compiles knowledge **once** and keeps it current — the LLM builds and maintains a persistent, interlinked set of markdown pages. Cross-references are pre-built. Contradictions are pre-flagged. Every new source strengthens the whole structure. Token cost drops significantly because the agent reads a small index first, then drills into only the relevant pages.

---

## Directory Structure

Always follow this structure. Do not deviate.

```
wiki/              ← LLM-generated pages (LLM writes, you read)
  index.md         ← catalog of every page with one-line summaries (required)
  log.md           ← append-only chronological history (required)
  concepts/        ← distilled concept and topic pages
  entities/        ← people, projects, products, organizations
  sources/         ← one summary page per raw source ingested
  synthesis/       ← comparison tables, analyses, answers filed back in
raw/               ← immutable source documents (you add, LLM never modifies)
  assets/          ← downloaded images (see Obsidian tip below)
```

**Rule**: The LLM owns `wiki/` entirely. You own `raw/` entirely. Never cross this boundary.

---

## Setup: Bootstrap a New Wiki

When running `/wiki-setup` or bootstrapping from scratch:

### Step 1 — Create the directory structure
```bash
mkdir -p wiki/concepts wiki/entities wiki/sources wiki/synthesis raw/assets
```

### Step 2 — Create index.md
```markdown
# Wiki Index

Last updated: [DATE]
Total pages: 0

## Concepts
_(none yet)_

## Entities
_(none yet)_

## Sources
_(none yet)_

## Synthesis
_(none yet)_
```

### Step 3 — Create log.md
```markdown
# Wiki Log

Append-only record of all wiki operations.
Format: `## [YYYY-MM-DD] operation | title`

---

## [YYYY-MM-DD] setup | Wiki initialized
```

### Step 4 — Add this SKILL.md path to your schema file
In `CLAUDE.md`, add:
```
Wiki schema: see plugins/*/skills/llm-wiki/SKILL.md
Wiki location: wiki/
Raw sources: raw/
```

---

## Operation 1: Ingest (`/ingest`)

**Trigger**: User drops a new source into `raw/` and says "ingest this" or runs `/ingest [filename]`.

### Pre-ingest: Convert non-markdown files
Before ingesting PDFs, Word docs, PowerPoints, or web pages, convert them to markdown using **markitdown** (see Installation section below).

```bash
# Single file
markitdown raw/paper.pdf -o raw/paper.md

# With OCR for scanned PDFs (requires OpenAI key)
markitdown raw/scanned.pdf -o raw/scanned.md --llm-client openai --llm-model gpt-4o

# Batch convert all PDFs in raw/
for f in raw/*.pdf; do markitdown "$f" -o "${f%.pdf}.md"; done

# YouTube video transcript
markitdown "https://youtube.com/watch?v=..." -o raw/video-title.md
```

### Ingest workflow
1. **Read** the source file in `raw/`
2. **Discuss** key takeaways with the user (1-2 messages max — don't over-narrate)
3. **Write a source summary page** at `wiki/sources/[slug].md`
4. **Update or create concept/entity pages** — a single source typically touches 5-15 pages
5. **Update `wiki/index.md`** — add all new/modified pages with one-line summaries
6. **Append to `wiki/log.md`**:
   ```
   ## [YYYY-MM-DD] ingest | [Source Title]
   Source: raw/[filename]
   Pages touched: wiki/sources/[slug].md, wiki/concepts/[x].md, ...
   Key additions: [1-2 sentence summary of what changed]
   ```

### Source summary page format
```markdown
---
type: source
date_ingested: YYYY-MM-DD
source_file: raw/[filename]
topics: [comma-separated list]
---

# [Source Title]

**Type**: paper / article / video / book / notes
**Author(s)**: ...
**Date**: ...
**Original**: [URL or file path]

## Summary
[2-4 paragraph summary of main claims]

## Key Points
- ...

## Concepts Introduced or Updated
- [[concept-name]] — brief note on what changed

## Contradictions / Open Questions
- ...
```

### Concept page format
```markdown
---
type: concept
source_count: N
last_updated: YYYY-MM-DD
---

# [Concept Name]

[1-2 sentence definition]

## Current Understanding
[Synthesized knowledge from all sources]

## Sources
- [[sources/slug-1]] — what it contributes
- [[sources/slug-2]] — what it contributes

## Related Concepts
- [[concept-a]], [[concept-b]]

## Open Questions
- ...
```

---

## Operation 2: Query (`/query`)

**Trigger**: User asks a question that should be answered from the wiki.

### Query workflow
1. **Read `wiki/index.md` first** — identify which pages are relevant (do not load everything)
2. **Load only the relevant pages** — typically 3-8 pages for most questions
3. **Synthesize an answer** with citations in `[[wikilink]]` format
4. **Decision point**: If the answer is non-trivial and reusable, file it back into the wiki:
   - Create `wiki/synthesis/[question-slug].md`
   - Add it to `wiki/index.md`
   - Append to `wiki/log.md`

**Token efficiency**: Reading `index.md` (small) + 3-8 targeted pages is 10-20x cheaper than loading the entire wiki. At ~100 pages, the index approach beats RAG for most questions.

### When to file answers back
File back when answers involve:
- Non-obvious synthesis across multiple sources
- A comparison or table that took real work to produce
- A conclusion that should be remembered for future sessions
- An analysis another agent might need

---

## Operation 3: Lint (`/lint-brain`)

**Trigger**: User runs `/lint-brain` or it runs on a schedule.

### Lint checks (run in order)
1. **Orphan pages** — pages in `wiki/` with no inbound wikilinks
2. **Missing concept pages** — concepts mentioned in `[[brackets]]` but lacking their own page
3. **Contradictions** — claims in one page that conflict with another
4. **Stale claims** — statements marked with `TODO: verify` or that newer sources may have superseded
5. **Under-linked pages** — pages with < 2 outbound links (poor integration into graph)
6. **Data gaps** — important topics mentioned but not given dedicated pages

### Gap-finding with web search (self-learning extension)
For each gap identified in step 6:
1. Formulate a specific search query
2. Use available web search tools (Tavily MCP, Bing, etc.) to find 2-3 authoritative sources
3. Present findings to the user: "Gap found: [topic]. Found these sources: [list]. Ingest?"
4. If approved, run the ingest workflow on each source

### Lint report format
```markdown
## [YYYY-MM-DD] lint | Health check

### Orphan pages (N)
- wiki/concepts/foo.md — no inbound links

### Missing pages (N)
- [[concept-xyz]] — mentioned in 3 pages but has no own page

### Contradictions (N)
- wiki/concepts/a.md claims X; wiki/sources/b.md claims not-X — needs resolution

### Stale claims (N)
- wiki/concepts/c.md: "As of 2024..." — verify against newer sources

### Data gaps (N)
- Topic: [X] — mentioned frequently but no dedicated page
  Suggested source: [URL or search query]
```

---

## markitdown: PDF & Document Conversion

markitdown (by Microsoft) converts PDFs, Word docs, PowerPoints, images, audio, Excel files, and web pages into clean markdown for ingestion.

### Installation
```bash
# Full install (recommended — supports all formats)
pip install 'markitdown[all]'

# Minimal install (PDF + DOCX only)
pip install 'markitdown[pdf,docx]'
```

### CLI usage
```bash
# PDF to markdown
markitdown raw/paper.pdf -o raw/paper.md

# Word / PowerPoint / Excel
markitdown raw/report.docx -o raw/report.md
markitdown raw/slides.pptx -o raw/slides.md

# Web page (fetches + converts)
markitdown "https://example.com/article" -o raw/article.md

# YouTube (extracts transcript)
markitdown "https://youtube.com/watch?v=ID" -o raw/video.md

# Pipe
cat raw/paper.pdf | markitdown > raw/paper.md
```

### MCP server (for agent-native conversion)
If you want the agent to convert files autonomously without CLI access:

```bash
pip install markitdown-mcp
markitdown-mcp   # runs STDIO MCP server
```

Add to your MCP config (`claude_desktop_config.json` or equivalent):
```json
{
  "mcpServers": {
    "markitdown": {
      "command": "markitdown-mcp"
    }
  }
}
```

The MCP server exposes one tool: `convert_to_markdown(uri)` — accepts `file://`, `http://`, `https://`, or `data:` URIs.

**Security note**: markitdown-mcp runs with your user's file permissions. Use only on trusted local machines. Never bind it to non-localhost interfaces.

### OCR for scanned PDFs
```bash
pip install markitdown-ocr openai

# Requires OPENAI_API_KEY in environment
markitdown --use-plugins raw/scanned-pdf.pdf -o raw/scanned.md
```

---

## Obsidian Integration (Recommended)

Obsidian is the best way to browse and navigate a wiki-style knowledge base. It reads plain markdown folders and renders wikilinks natively.

### Setup
1. Open Obsidian → **Open folder as vault** → select your `wiki/` directory
2. Enable **Graph view** (sidebar) to see the connection topology
3. Install recommended plugins:
   - **Dataview** — query pages by frontmatter (e.g., "all concepts with source_count > 3")
   - **Obsidian Web Clipper** (browser extension) — clip articles directly to `raw/` as markdown

### Sync with notes app (Google Drive)
1. Create a Google Drive folder that mirrors `raw/` (or the full wiki)
2. Use the **Google Drive MCP** (`@google-drive/mcp-server-gdrive`) to allow the agent to read Drive files directly
3. Drop files into Drive from any device → they sync to your local `raw/` folder → run `/ingest`

Alternatively, point your notes app (e.g., Apple Notes, Notion) at an auto-export directory that syncs to `raw/`.

---

## Weekly Automated Lint (GitHub Actions)

Add this workflow to auto-run `/lint-brain` on a schedule:

```yaml
# .github/workflows/wiki-lint.yml
name: Weekly Wiki Lint
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9am UTC
  workflow_dispatch:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run wiki lint
        run: |
          echo "Run your agent lint command here"
          # e.g.: claude-code --skill llm-wiki --op lint
```

---

## Index and Log Conventions

### index.md rules
- Update on **every** ingest — never let it go stale
- One line per page: `- [[path/to/page]] — one sentence summary`
- Group by category: Concepts, Entities, Sources, Synthesis
- The agent reads this **first** on every query — keep it lean

### log.md rules  
- Append-only — never edit past entries
- Header format: `## [YYYY-MM-DD] operation | title` (parseable with grep)
- Operations: `setup`, `ingest`, `query`, `lint`, `update`
- Last 10 entries give enough context for a new session without reading the full log

---

## Token Cost at Scale

| Wiki size | Strategy | Est. tokens per query |
|---|---|---|
| < 50 pages | Load all wiki pages | ~20k |
| 50-300 pages | `index.md` + targeted loads | ~5-10k |
| 300-1000 pages | `index.md` + [qmd](https://github.com/tobi/qmd) search + targeted loads | ~3-8k |
| 1000+ pages | Embedding-based RAG over wiki | standard RAG |

For most use cases, the `index.md` approach (no embeddings needed) handles up to ~300 pages efficiently. Only move to vector search when index + targeted loads regularly exceeds 20k tokens per query.

---

## Commands Summary

| Command | When to use |
|---|---|
| `/wiki-setup` | Bootstrap a new wiki for a project |
| `/ingest [file]` | Process a new source into wiki pages |
| `/query [question]` | Answer from wiki with citations |
| `/lint-brain` | Health-check: find orphans, gaps, contradictions |

---

## Anti-Patterns

- **Do not load the entire wiki on every query** — always read `index.md` first
- **Do not modify `raw/`** — raw sources are immutable; LLM owns only `wiki/`
- **Do not skip updating `index.md`** — a stale index defeats the token-efficiency benefit
- **Do not ingest without converting** — always run markitdown on non-markdown files before ingestion
- **Do not let `log.md` grow unbounded without pruning** — summarize and archive entries older than 90 days into `wiki/synthesis/archive-log-[date].md`

---
name: aris-research-lit
description: Search and analyze research papers, find related work, summarize key ideas. Use when user says "find papers", "related work", "literature review", "what does this paper say", or needs to understand academic papers. Ported from wanshuiyin/Auto-claude-code-research-in-sleep (ARIS) — methodology only, Claude-Code-specific MCP/CLI deps stripped for VS Code Copilot.
---

# Research Literature Review

The user will provide the research topic or paper URL as part of their request.

## Constants

- **PAPER_LIBRARY** — Local directory containing user's paper collection (PDFs). Check these paths in order:
  1. `papers/` in the current project directory
  2. `literature/` in the current project directory
  3. Custom path specified by user
- **MAX_LOCAL_PAPERS = 20** — Maximum number of local PDFs to scan (read first 3 pages each). If more are found, prioritize by filename relevance to the topic.

## Workflow

### Step 0: Scan Local Paper Library

Before searching online, check if the user already has relevant papers locally:

1. **Locate library**: Check PAPER_LIBRARY paths for PDF files
   - Search for `papers/**/*.pdf` and `literature/**/*.pdf`

2. **Filter by relevance**: Match filenames and first-page content against the research topic. Skip clearly unrelated papers.

3. **Summarize relevant papers**: For each relevant local PDF (up to MAX_LOCAL_PAPERS):
   - Read first 3 pages (title, abstract, intro)
   - Extract: title, authors, year, core contribution, relevance to topic
   - Flag papers that are directly related vs tangentially related

4. **Build local knowledge base**: Compile summaries into a "papers you already have" section. This becomes the starting point — external search fills the gaps.

> If no local papers are found, skip to Step 1. If the user has a comprehensive local collection, the external search can be more targeted (focus on what's missing).

### Step 1: Search (external)
- Use WebSearch to find recent papers on the topic
- Check arXiv, Semantic Scholar, Google Scholar
- Focus on papers from last 2 years unless studying foundational work
- **De-duplicate**: Skip papers already found in the local library

For arXiv searches:
- Use the arXiv API or web search with site:arxiv.org
- Try at least 3 different query formulations
- Include year filters for recent work
- For each potentially relevant paper, fetch its abstract page

### Step 2: Deep Read (top 5-8 papers)
For the most relevant papers found in Step 1:
1. Fetch the full abstract and introduction
2. Extract: problem, method, key results, limitations
3. Note how each paper relates to the user's topic
4. Identify gaps and open problems mentioned across papers

### Step 3: Synthesize
Compile findings into a structured report:

```markdown
## Literature Review: [topic]

### Papers You Already Have
| # | Title | Year | Venue | Relevance | Key Contribution |
|---|-------|------|-------|-----------|------------------|

### Key Papers Found
| # | Title | Authors | Year | Venue | Core Idea | Relevance |
|---|-------|---------|------|-------|-----------|-----------|

### Landscape Summary
[2-3 paragraph synthesis of the research area]

### Open Problems / Gaps
1. [Gap 1] — mentioned by [paper1], [paper3]
2. [Gap 2] — mentioned by [paper2]
3. [Gap 3] — inferred from the gap between [paper1] and [paper4]

### Suggested Next Steps
- [Direction 1 based on gaps]
- [Direction 2]
- [Direction 3]
```

### Important Rules
- **Anti-hallucination**: Never fabricate paper titles, authors, arXiv IDs, or DOIs. Every paper must be verified via web search. If uncertain, tag `[UNVERIFIED]`.
- **De-duplicate**: The same paper may appear under different URLs (arXiv vs. published venue). Match by title to avoid duplicates.
- **Relevance over quantity**: 8 well-chosen papers beat 30 random ones. Prioritize papers that directly address the user's topic.
- **Recent first**: Unless the user asks for foundational work, prioritize papers from the last 2 years.
- **Read before summarizing**: Never summarize a paper from its title alone — always fetch at least the abstract.

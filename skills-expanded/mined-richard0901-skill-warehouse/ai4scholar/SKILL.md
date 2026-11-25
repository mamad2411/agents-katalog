---
name: ai4scholar
description: Use when the user wants academic literature search, paper discovery, citation graph lookup, PubMed or Google Scholar retrieval, arXiv or Rxiv preprint search, or AI4Scholar-powered citation insertion inside Codex. Prefer the bundled script over generic web search when the user explicitly wants AI4Scholar.
---

# AI4Scholar Skill

Use this skill when the task is about literature discovery or citation work and the user wants AI4Scholar inside Codex rather than OpenClaw.

## What this skill provides

- Semantic Scholar search, title match, paper detail, citations, references
- PubMed search and paper detail
- Google Scholar search
- arXiv, bioRxiv, and medRxiv search
- AI4Scholar auto-citation

## Invocation

Run the bundled script:

```bash
node /Users/rr/.codex/skills/ai4scholar/scripts/ai4scholar.js <tool> '<json>'
```

If the JSON argument is omitted, the script reads JSON from stdin.

## Supported tools

- `search_semantic`
- `search_semantic_snippets`
- `search_semantic_paper_match`
- `get_semantic_paper_detail`
- `get_semantic_citations`
- `get_semantic_references`
- `search_pubmed`
- `get_pubmed_paper_detail`
- `get_pubmed_related`
- `search_google_scholar`
- `search_arxiv`
- `search_biorxiv`
- `search_medrxiv`
- `download_arxiv`
- `auto_cite`

## Examples

Semantic Scholar search:

```bash
node /Users/rr/.codex/skills/ai4scholar/scripts/ai4scholar.js search_semantic '{"query":"EGFR NSCLC brain metastases","max_results":5,"year":"2020-"}'
```

PubMed search:

```bash
node /Users/rr/.codex/skills/ai4scholar/scripts/ai4scholar.js search_pubmed '{"query":"non-small cell lung cancer brain metastases","max_results":5,"sort":"date"}'
```

Google Scholar search:

```bash
node /Users/rr/.codex/skills/ai4scholar/scripts/ai4scholar.js search_google_scholar '{"query":"osimertinib CNS efficacy brain metastases","max_results":5,"year_from":2020}'
```

Auto-citation:

```bash
node /Users/rr/.codex/skills/ai4scholar/scripts/ai4scholar.js auto_cite '{"text":"<academic paragraph>","citationStyle":"vancouver","field":"oncology"}'
```

## Workflow

1. Pick the narrowest AI4Scholar tool that matches the task.
2. Prefer `search_semantic` or `search_pubmed` for standard literature discovery.
3. Use `search_semantic_paper_match` when the user gives a likely exact title.
4. Use `get_semantic_citations` or `get_semantic_references` for citation chaining.
5. Use `search_arxiv`, `search_biorxiv`, or `search_medrxiv` for preprints.
6. Use `auto_cite` only when the user wants citations inserted into prose.
7. Summarize results for the user instead of dumping raw JSON unless they ask for the raw output.

## Notes

- The API key is loaded from `config.json` in this skill directory, or `AI4SCHOLAR_API_KEY` if set.
- `auto_cite` can take 20-60 seconds.
- If a tool call fails, include the API error in your reasoning and fall back to adjacent tools only when that still serves the user's request.

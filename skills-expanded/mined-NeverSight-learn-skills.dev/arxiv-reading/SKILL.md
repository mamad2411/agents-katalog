---
name: arxiv-reading
description: Read, inspect, or summarize arXiv papers using a clean-markdown-first paper-reading workflow. Use when the user provides an arXiv URL or id, asks to read a paper, analyze a preprint, summarize a research paper, compare claims against evidence, or extract assumptions, limitations, strengths, and weak links from a paper.
---

# arXiv reading

Read papers as clean Markdown, never as PDF.
For the judgment side, what to extract from a paper and how to weigh it, use the `research-taste` skill.

## Convert before reading

For arXiv, convert to Markdown with `arxiv2md`, which parses arXiv's structured HTML and keeps math as LaTeX, real tables, and a section tree:

```bash
uvx --from arxiv2markdown arxiv2md <id> -o paper.md
```

The id is the same across the `/abs/`, `/pdf/`, and `/html/` URL forms, so a PDF link works too; just take its id.

## Fallbacks

When `arxiv2md` has no HTML to work with (older papers arXiv hasn't rendered to HTML), in order:

1. WebFetch on `https://ar5iv.org/abs/<id>` with a specific question; ar5iv renders HTML from LaTeX source for most older papers.
2. The PDF, only as a last resort, read with the Read tool on a page range rather than a blind full-text dump. The abstract alone is often enough to decide it is not worth more.

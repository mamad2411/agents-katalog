---
name: literature-idea-planner
description: Chrome-dependent academic literature scouting and idea planning. Use when the user gives a research idea, topic, question, or draft direction and wants Codex to browse Google, Google Scholar, and academic sources through the Codex Chrome plugin, identify relevant papers, explain what can be borrowed from them, and write a planNN.md before collecting PDFs or BibTeX.
---

# Literature Idea Planner

## Overview

Turn a research idea into a concrete literature plan. Use the Codex Chrome plugin for live Google and academic browsing, then write a local `planNN.md` that lists which papers matter, why they matter, and how a later reference-building pass should fetch them.

## Dependency

This skill depends on the Codex Chrome plugin. Use Chrome rather than generic unauthenticated browsing when search ranking, Google Scholar, publisher access, or the user's logged-in academic permissions may affect results.

If Chrome is unavailable, state that the skill is blocked and do not pretend that a normal web search is an equivalent substitute.

## Workflow

1. Establish the planning target.
   - Use the user's exact research idea, draft paragraph, theorem direction, experiment concept, or keyword list.
   - Ask a short clarification only when the scope is too ambiguous to search.
   - Choose the next available `planNN.md` in the working directory unless the user gives a path.

2. Search with Chrome.
   - Start with Google queries that combine the user's core idea with terms such as `paper`, `survey`, `theory`, `benchmark`, `method`, `arxiv`, `pdf`, or the target field.
   - Use Google Scholar when paper identity, citation context, or BibTeX availability matters.
   - Triangulate through publisher pages, DBLP, arXiv, OpenReview, Semantic Scholar, conference proceedings, and authors' pages when useful.
   - Record useful query patterns and sources in the plan, not raw browsing logs.

3. Screen candidate papers.
   - Prefer papers with clear relevance to the user's idea, strong venue or author signal, reusable methods, theoretical tools, datasets, baselines, or evaluation protocols.
   - Include both direct inspirations and contrastive papers that explain why the user's idea differs.
   - Do not pad the plan with weak hits. It is better to list fewer papers with precise reasons.

4. Write `planNN.md`.
   - Include links for every candidate.
   - Separate confirmed useful papers from speculative or excluded papers.
   - Do not download PDFs or write `references.bib`; that belongs to `literature-reference-builder`.

## Plan Format

Use this structure unless the user requested another format:

```markdown
# Literature Plan: <short topic>

Source idea: <brief restatement of the user request>
Date: <YYYY-MM-DD>

## Search Strategy

- Queries:
  - <query and why it was useful>
- Sources checked:
  - <Google, Google Scholar, DBLP, arXiv, publisher pages, etc.>

## Papers To Borrow From

| Priority | Paper | Best known version | Link | Why it matters | What to borrow | Fetch note |
| --- | --- | --- | --- | --- | --- | --- |
| High | <authors, title, venue/year> | <published/arXiv/preprint/unknown> | <url> | <reason> | <method/proof/baseline/dataset/framing> | <publisher PDF preferred, arXiv fallback, DBLP BibTeX, etc.> |

## Synthesis

- <main research line suggested by the literature>
- <which ingredients are reusable>
- <where the user's idea should differ>

## Fetch List For literature-reference-builder

- [ ] <paper title or citation> -- <preferred source/version>

## Exclusions And Uncertainties

- <weak hit, duplicate, paywalled-only item, ambiguous title, or unresolved question>
```

## Quality Bar

- Make the plan actionable enough that another Codex run can fetch papers and build `references.bib` without repeating the idea search.
- Explain the borrowing relation in concrete academic terms: theorem technique, modeling assumption, benchmark, baseline, proof template, system design, loss, dataset, or evaluation metric.
- Keep private user context out of the plan unless the user explicitly asks to preserve it.

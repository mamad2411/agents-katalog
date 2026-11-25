---
name: codebase-search-and-answer
description: Answer specific repository questions with cited paths and excerpts. Use when the user asks where something is, how it works, or what depends on it.
---

# codebase-search-and-answer

Search the repository for the user's target. Return cited file paths, line ranges, and short excerpts. Note related files. Do not paraphrase code; quote it in fenced blocks.

Primary prompts:

- `prompts/13_codebase_search_and_answer_prompt.md`
- `prompts/110_source_cited_repo_answerer.md`

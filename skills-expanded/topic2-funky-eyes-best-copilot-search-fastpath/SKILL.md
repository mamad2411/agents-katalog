---
name: search-fastpath
description: "Use when target files are unknown, repeated search is becoming expensive, an agent is about to do broad repo-wide scanning, or a regex search is being considered. DO NOT USE FOR: explicit user paths or already frozen files_involved."
---

# Search Fastpath

## Goal

Find the right files quickly without turning every task into an unbounded repository scan.

This skill is the retrieval lane. It should produce a compact evidence map that a coding or review lane can consume without repeating broad search.

## Precision First

- Prefer exact paths, file names, symbols, routes, config keys, and copied error strings over regex.
- Use regex only when the user's description is vague, the exact symbol/path is unknown, or literal searches have failed and the pattern is genuinely structural.
- When using regex, record why literal lookup was insufficient and keep the search scoped to the smallest likely directory.
- Do not use regex for exact class names, method names, route strings, property keys, command names, filenames, or quoted log/error text; use fixed-string search instead.

## Search Order

1. User-provided paths, current files, attachments, changed files.
2. Repo indexes: `README*`, `.github/instructions/project.instructions.md`, and target-local `spec/INDEX.md` / `memories/repo/INDEX.md` when present.
3. Exact file-name discovery: `rg --files -g 'ExactName.ext'`, `rg --files <likely-dir>`, or `find <dir> -name 'ExactName.ext'`.
4. Literal content lookup with fixed strings: `rg -F -n 'ExactSymbolOrError' <likely-dir>`; add `-w` only when word-boundary matching is needed.
5. Scoped semantic search with 2-3 literal terms in the smallest likely directory when exact names are unknown.
6. Regex search only after the earlier steps fail or the task needs a structural pattern.
7. External sources only when repo evidence cannot answer the question and current instructions allow web use.

For code-generation tasks, stop search when you have: the target files, the local pattern to follow, the relevant test/check surface, and any public contract or frontend state affected by the change.

## External Fetch Ladder

When a task needs web or repository evidence, use a source-aware ladder inspired by fetch-skill:

1. Prefer primary source URLs provided by the user.
2. Prefer raw Markdown / raw source over rendered HTML when available.
3. Extract the smallest relevant section, not the whole page.
4. Keep `source_url`, `fetch_mode`, and `fallback_used` in the result.
5. Treat social posts, mirrors, marketplaces, and blog summaries as secondary hints unless the user explicitly asked for them.
6. If output is summarized or truncated, keep a recovery URL or command.

## Stop Rules

- Stop after enough evidence supports the next action.
- Stop after two searches with no new signal.
- Stop before repo-wide regex unless the task remains genuinely ambiguous after exact path, index, filename, and fixed-string attempts.
- Do not search directories excluded by PM or user.
- Do not inject long outputs; summarize and keep recovery commands.

## Search Result To Packet Mapping

When this search output feeds `context-packet-fastpath` or a PM dispatch packet:

- `selected_files` -> `files_involved` or `priority_files`
- `candidate_files` -> `search_hints`
- `commands`, `literal_attempts`, `regex_used`, and `retrieval_provenance` -> packet `retrieval_provenance`
- `gaps` -> packet `known_gaps`, `uncovered_items`, or `NEEDS_CONTEXT`
- generated evidence map -> `artifact_refs` with `kind: search_result`
- budget overrun -> `NEEDS_CONTEXT context_budget_exceeded` with searched paths and the next smallest recommended shard

Record token-cost signals when practical: `files_read`, `broad_searches`, `context_budget_used`, `artifact_reuse_count`, and `escalation_reason`.

## Output

```markdown
## Search Result
- mode:
- commands:
- candidate_files:
- selected_files:
- literal_attempts:
- regex_used: yes|no, reason
- retrieval_provenance:
- artifact_refs:
- token_cost_metrics: files_read=, broad_searches=, context_budget_used=, artifact_reuse_count=, escalation_reason=
- gaps:
```

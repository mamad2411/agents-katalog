# Skill: explain a paper

Use EdgeQuake MCP tools as evidence — never invent document lists.

1. `eq_document_list` — find the PDF by `file_name` / title.
2. Call `eq_search` with `document_ids: [<id>]` and a focused query.
3. `eq_fetch(view=toc)` on the `retrieval_id`.
4. Escalate to `view=chunks` or `eq_neighborhood` only if needed.
5. If `truncation.truncated`, follow `next_cursor` before concluding the corpus is small.
6. Cite `document_id` + chunk/page from the tool results. Do not claim an LLM essay from EdgeQuake.

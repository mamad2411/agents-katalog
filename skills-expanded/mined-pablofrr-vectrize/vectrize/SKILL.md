---
name: vectrize
description: Local semantic search over the user's indexed documentation (notes, docs, specs, PRDs, runbooks). Use it BEFORE Grep/Glob whenever a question could be answered by documentation, or to find where a topic is covered. Understands paraphrases and other languages, and returns the relevant passages with file:line in ~30 ms.
---

# vectrize

```bash
vectrize search "<your question, in natural language>" --json -k 5
```

Returns a JSON list, most relevant first: `file` (absolute path), `line`, `heading` (note › section) and `text` (the full passage).

- Often `text` already answers the question; only open the file if you need more context, and then just that part: `Read(file, offset=line, limit=40)`.
- Ask in your own words: you don't need to guess the exact wording of the document, and the query language doesn't have to match the documents' language.
- For exact identifiers (error codes, endpoints, table names), add `--mode bm25`.
- To search a single folder, add `--in <folder>`.
- It ALWAYS returns k results, whether they are relevant or not. Judge relevance yourself. If nothing fits after two reformulated searches, the documents probably don't cover it: say so instead of guessing (then fall back to Grep if useful).
- If it reports that the index is being built, wait ~30 s and retry.
- Cite sources as `file:line`.
- If `vectrize` is not installed (command not found), follow [INSTALL.md](INSTALL.md).

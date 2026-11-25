---
version: 1.1.0
name: future-paper
description: >
  Search academic literature and retrieve paper content by PMID, DOI or other supported
  identifiers. Use for finding papers, literature reviews and extracting specific findings.
  Distinguish generated search summaries from inspected original passages and report unavailable full text.
allowed-tools: Bash(future:*)
category: tools
---

# Academic Paper Retrieval

The Future CLI handles authentication. Read relevant supplied papers first and respect
source/privacy constraints. Consult `future tools describe search_paper` / `get_paper`
for current arguments instead of relying on a copied response schema.

## Commands

```bash
future tools call search_paper --queries '["BRCA1 variant classification guidelines"]' --information_to_extract "Methods, findings and limitations" --max_results_per_query 5 --raw
future tools call get_paper --paper_id "PMID:12345678" --raw
```

`search_paper` accepts multiple queries and `--max_results_per_query`.
`get_paper` accepts `--paper_id` and optional `--max_k`.

Without `--raw`, the CLI formats results for reading. With `--raw`, it emits the
structured-content object directly when available, not a wrapper named
`structured_content`. Typical paths are `results[].papers[]` and `paper.body_text`;
inspect returned keys and handle text-only responses rather than inventing fields.

## Evidence workflow

1. Identify the question, date range, populations/methods and requested level of coverage.
   A few search results do not establish an exhaustive systematic review.
2. Search for relevant papers and record stable identifiers, titles, authors, venue/year
   and source URLs. Deduplicate versions and avoid counting copies as independent evidence.
3. Use generated `ai_summary` fields only to prioritize reading. Retrieve the original
   passages needed to verify key findings, conditions, numerical values and limitations.
4. Full-text availability varies. An abstract, empty body or partial excerpt is not the
   complete paper. If permitted, use `future-web` for an open publisher/repository source
   or `future-database-lookup` for a relevant structured record. Request a user copy when
   needed; do not bypass access restrictions or declare an unseen result verified.
5. Trace each central claim to the actual inspected passage, with DOI/PMID, version and
   location. Check contrary evidence and distinguish association from causal conclusions.
6. Return the requested synthesis with citations and retrieval limitations. Do not use
   citation counts, journal metrics or the number of search hits as proof of correctness.

## Boundaries

Do not disclose confidential manuscript text or private research data in search queries.
Reuse the existing retrieval budget; bound retries and report actual failures. No new
worker/model dispatch or broader literature review is implied by a single lookup request.

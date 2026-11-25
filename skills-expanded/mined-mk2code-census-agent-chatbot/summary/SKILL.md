---
name: summary
description: Summarize a census report or chapter with citations. Use for "summarize", "key findings", "overview".
---
# Summary recipe
1. Identify the document (doc_id). Use `read_pages` on its highlights/executive-summary
   pages first; only expand to statements if asked.
2. Summarize the state-level story in <=200 words: population, growth, sex ratio,
   literacy, workers — every number becomes a Claim with the page's citation.
3. Offer follow-ups ("want district extremes or chapter-level detail?").

## Gotchas
- Distinguish census-year (2001 vs 2011) — the docs mix both constantly.
- If the user names a section not present in the corpus, say so and list what IS present.

---
name: gbrain-query
description: Answer questions from the brain using FTS5 + semantic search + structured queries. Synthesizes across multiple pages with citations.
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: [gbrain]
---

# Query Skill

## Strategy: Three-layer search

1. **FTS5 keyword search** — `gbrain search "<query>"` — fast, exact matches.
   Best for: names, company names, specific terms, acronyms.

2. **Semantic vector search** — `gbrain query "<question>"` — meaning-based.
   Best for: "who knows X?", "what's our thesis on Y?", conceptual or relationship questions.
   Requires OPENAI_API_KEY and at least one `gbrain embed` run.

3. **Structured queries** — relational navigation.
   - `gbrain list --type person --tag yc-alum`
   - `gbrain backlinks <slug>` — who links to this page?
   - `gbrain timeline <slug>` — what happened with this person/company?
   - `gbrain tags <slug>` — what is this page tagged with?

## Workflow

1. Decompose the question into search strategies.
2. Run FTS5 search for key terms.
3. Run semantic query for the full question (if embeddings available).
4. Merge and deduplicate results.
5. For top results, `gbrain get <slug>` to read full pages.
6. Synthesize answer with citations: "[Jane Doe](people/jane-doe)"
7. If the answer is valuable enough to keep, consider creating a page: `cat answer.md | gbrain put concepts/topic`

## Ranking heuristic

- FTS5 score × 0.4 + vector similarity × 0.6 = combined score
- Boost pages with type matching the question intent (+0.2 for person queries hitting person pages)
- Boost pages updated recently
- Prefer pages with richer content (longer compiled_truth)

## When you don't know

Say so. "The brain doesn't have info on X" is honest and useful.
Suggest enrichment: "Want me to research X and add them to the brain?"

## Examples

```bash
# Find a person
gbrain search "Jane Doe"
gbrain get people/jane-doe

# Relationship question
gbrain query "who is connected to Anthropic?"

# Relational: all YC founders
gbrain list --type person --tag yc-alum

# What links to a company page?
gbrain backlinks companies/acme-corp

# Recent activity
gbrain list --limit 20  # sorted by updated_at desc
```

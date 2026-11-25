# OpenAlex Citation Chain Starter

Use this skill to look up a seed paper in OpenAlex and summarize both upstream references and downstream citing works.

## What it does

- Resolves a DOI or OpenAlex work ID through the official OpenAlex API.
- Summarizes the seed paper's title, year, DOI, and citation counts.
- Fetches a small citing-work slice and a small referenced-work slice for deterministic citation-chain inspection.
- Writes compact JSON that can feed later literature-triage or method-mining workflows.

## When to use it

- You need a verified starter for `citation chaining`.
- You want machine-readable citation context for a canonical paper before deeper review or ranking.

## Example

```bash
python3 skills/scientific-knowledge/openalex-citation-chain-starter/scripts/run_openalex_citation_chain.py \
  --work-id 10.1038/nature12373 \
  --limit 3 \
  --out scratch/openalex-citation-chain/hallmarks_citation_chain.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/scientific-knowledge/openalex-citation-chain-starter/tests -p 'test_*.py'`
- Repository smoke target: `make smoke-openalex-citation-chain`

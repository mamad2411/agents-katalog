# Reactome Pathway Analysis Starter

Use this skill to submit a short identifier list to the official Reactome Analysis Service and return a compact ranked pathway table.

## What it does

- Sends a small gene or protein identifier list to Reactome's official analysis endpoint.
- Summarizes the top enriched pathways, the best FDR observed, and the number of pathways under a chosen threshold.
- Emits deterministic JSON that is easier to route into reports or downstream agent workflows than the full raw service payload.

## When to use it

- You need a verified starter for `pathway analysis`.
- You want a lightweight ranked pathway summary rather than a full enrichment payload dump.

## Example

```bash
python3 skills/systems-biology/reactome-pathway-analysis-starter/scripts/run_reactome_pathway_analysis.py \
  --identifiers BRCA1,TP53,EGFR \
  --top-n 5 \
  --out scratch/reactome-pathway-analysis/top_pathways.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/systems-biology/reactome-pathway-analysis-starter/tests -p 'test_*.py'`
- Repository smoke target: `make smoke-reactome-pathway-analysis`

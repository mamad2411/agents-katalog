# CELLxGENE Census Atlas Query Starter

Use this skill to search the public CELLxGENE Census dataset catalog by keyword and summarize the largest matching atlas datasets.

## What it does

- Opens the public CELLxGENE Census SOMA catalog.
- Loads the canonical dataset metadata table.
- Filters dataset titles and collection names by a keyword such as `lung`, `PBMC`, or `Tabula`.
- Reports top matches, unique collections, and aggregate cell counts.

## When to use it

- You need a reproducible atlas-discovery entry point for multi-sample single-cell workflows.
- You want to shortlist large public Census datasets before deeper matrix queries.

## Example

```bash
slurm/envs/census/bin/python skills/transcriptomics/cellxgene-census-atlas-query-starter/scripts/run_cellxgene_census_atlas_query.py \
  --keyword "Tabula Sapiens" \
  --limit 5 \
  --out scratch/census/tabula_sapiens_query.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/transcriptomics/cellxgene-census-atlas-query-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase26_frontier_completion_skills -v`

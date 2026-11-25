# GBIF Dataset Search Starter

Use this skill to query the official GBIF dataset-search API and summarize a small biodiversity dataset result set.

## What it does

- Searches GBIF dataset metadata with a free-text query.
- Returns compact dataset summaries including dataset keys, titles, DOI, license, and publishing country.
- Supports canonical-asset fallback for the main smoke query when the live API is transiently unavailable.

## When to use it

- You need a runnable starter for `Biodiversity dataset discovery`.
- You want a lightweight biodiversity-metadata search step before downstream occurrence or phylogenetics workflows.

## Example

```bash
python3 skills/ecology-evolution-and-biodiversity/gbif-dataset-search-starter/scripts/run_gbif_dataset_search.py \
  --query puma \
  --out scratch/gbif-datasets/puma_datasets.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/ecology-evolution-and-biodiversity/gbif-dataset-search-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase31_frontier_leaf_conversion_skills -v`

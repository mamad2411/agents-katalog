# GBIF Species Occurrence Search Starter

Use this skill to query the official GBIF API for a canonical species match and a small live occurrence sample.

## What it does

- Resolves a scientific name against the GBIF species matcher.
- Fetches a compact occurrence sample with optional country filtering.
- Returns a normalized JSON summary suitable for biodiversity data discovery and early species-distribution workflows.

## When to use it

- You need a verified starter for `Species distribution modeling`.
- You want a lightweight live biodiversity occurrence query without adding a heavyweight geospatial stack first.

## Example

```bash
python3 skills/ecology-evolution-and-biodiversity/gbif-species-occurrence-search-starter/scripts/run_gbif_species_occurrence_search.py \
  --scientific-name "Puma concolor" \
  --country US \
  --out scratch/gbif/puma_concolor_us.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/ecology-evolution-and-biodiversity/gbif-species-occurrence-search-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase30_empty_domain_seed_skills -v`

# QuickGO Term Search

Use this skill to search public Gene Ontology terms through the official QuickGO API and return compact ontology summaries that are easy to inspect or feed into downstream enrichment workflows.

## What it does

- Searches the QuickGO ontology endpoint with a free-text query.
- Returns compact term records with GO ID, name, ontology aspect, obsolete flag, and definition text.
- Writes deterministic JSON to stdout or to an output file.

## When to use it

- You need a stable GO identifier for a biological concept before running enrichment or annotation steps.
- You want a lightweight ontology-search building block that stays inside official EBI infrastructure.

## Inputs

- `--query`: free-text search string, for example `apoptosis`
- `--limit`: number of terms to return, default `5`
- `--out`: optional JSON output path

## Example

```bash
python3 skills/systems-biology/quickgo-term-search/scripts/search_quickgo_terms.py \
  --query apoptosis \
  --limit 3 \
  --out scratch/quickgo/apoptosis_terms.json
```

## Verification

- Repository smoke: `python3 -m unittest tests.smoke.test_ontology_and_knowledge_extension_skills`
- Skill-local tests: `python3 -m unittest discover -s skills/systems-biology/quickgo-term-search/tests -p 'test_*.py'`

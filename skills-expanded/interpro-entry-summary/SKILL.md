# InterPro Entry Summary

Use this skill to fetch a protein family or domain entry from the official InterPro API and summarize its key metadata.

## What it does

- Calls the official InterPro API for a specific InterPro accession.
- Returns the accession, name, type, GO-term count, and member-database coverage.
- Produces compact JSON suitable for downstream protein-annotation or domain-family workflows.

## When to use it

- You need a lightweight protein family/domain lookup skill.
- You want an official InterPro-backed summary starter for proteomics or protein biology tasks.

## Example

```bash
python3 skills/proteomics/interpro-entry-summary/scripts/fetch_interpro_entry.py \
  --accession IPR000023 \
  --out scratch/interpro/ipr000023_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/proteomics/interpro-entry-summary/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase25_agent_and_clinical_skills -v`

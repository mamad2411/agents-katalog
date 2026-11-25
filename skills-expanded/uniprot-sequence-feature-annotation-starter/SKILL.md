# UniProt Sequence Feature Annotation Starter

Use this skill to fetch a UniProtKB accession from the official UniProt REST API and summarize its sequence features into compact JSON.

## What it does

- Calls `https://rest.uniprot.org/uniprotkb/{accession}.json`.
- Extracts accession, entry ID, protein name, gene names, organism metadata, sequence length, and annotation score.
- Collapses large feature payloads into stable type counts plus a small set of representative sequence features.

## When to use it

- You need a lightweight starter for protein sequence-feature annotation.
- You want a deterministic UniProt-backed summary for downstream proteomics or protein biology workflows.

## Example

```bash
python3 skills/proteomics/uniprot-sequence-feature-annotation-starter/scripts/fetch_uniprot_sequence_feature_summary.py \
  --accession P04637 \
  --out scratch/uniprot/p04637_sequence_features.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/proteomics/uniprot-sequence-feature-annotation-starter/tests -p 'test_*.py'`
- Canonical example: `python3 skills/proteomics/uniprot-sequence-feature-annotation-starter/scripts/fetch_uniprot_sequence_feature_summary.py --accession P04637`

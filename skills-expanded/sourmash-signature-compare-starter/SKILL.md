# sourmash Signature Compare Starter

Use this skill to compute deterministic MinHash signatures for two tiny DNA sequences with sourmash and summarize their similarity in compact JSON.

## What it does

- Reads two small FASTA inputs.
- Computes sourmash MinHash sketches with fixed `ksize` and `scaled`.
- Reports hash counts, shared-hash count, Jaccard similarity, and pairwise containment.

## When to use it

- You need a local, no-auth starter for metagenomics-style sketch comparison.
- You want a minimal example of sourmash sequence sketching without a large database.
- You want a deterministic JSON artifact for downstream tests or demos.

## Example

```bash
slurm/envs/metagenomics/bin/python skills/genomics/sourmash-signature-compare-starter/scripts/run_sourmash_signature_compare.py \
  --out scratch/metagenomics/sourmash_compare_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/genomics/sourmash-signature-compare-starter/tests -p 'test_*.py'`
- Expected summary: `shared_hash_count == 12` and `jaccard_similarity == 0.631579`

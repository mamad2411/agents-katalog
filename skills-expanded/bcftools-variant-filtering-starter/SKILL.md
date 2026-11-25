# bcftools Variant Filtering Starter

Use this skill to run a deterministic `bcftools view` filtering example on a tiny VCF and capture the kept variants in a compact JSON summary.

## What it does

- Runs `bcftools view` with a configurable include expression against a local VCF.
- Writes a compressed filtered VCF plus a tabix index.
- Summarizes the input record count, passing record count, and kept IDs for testing and demos.

## When to use it

- You need a runnable starter for VCF filtering logic.
- You want a tiny verified example before building cohort-scale post-calling workflows.
- You need a smoke-testable wrapper around `bcftools` in the repo-managed genomics environment.

## Example

```bash
python3 skills/genomics/bcftools-variant-filtering-starter/scripts/run_bcftools_variant_filtering.py \
  --input skills/genomics/bcftools-variant-filtering-starter/examples/toy_variants.vcf \
  --out scratch/genomics/bcftools_variant_filtering_summary.json \
  --filtered-vcf-out scratch/genomics/toy_variants.filtered.vcf.gz
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/genomics/bcftools-variant-filtering-starter/tests -p 'test_*.py'`
- Expected summary: `passing_record_count == 2` and `kept_ids == ["varA", "varC"]`

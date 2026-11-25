# pysam SAM BAM Summary Starter

Use this skill to read a small SAM, BAM, or CRAM file with `pysam`, summarize core alignment statistics, and optionally emit an indexed BAM artifact for downstream debugging or demos.

## What it does

- Opens a local alignment file with `pysam.AlignmentFile`.
- Reports header references, mapped and unmapped counts, pairing flags, and per-reference mapped counts.
- Optionally writes a BAM copy and builds a `.bai` index.

## When to use it

- You need a deterministic starter for `SAM/BAM/CRAM` handling in Python.
- You want a tiny verified example of format conversion plus indexing.
- You need a compact JSON summary before building larger alignment-processing skills.

## Example

```bash
slurm/envs/genomics/bin/python skills/genomics/pysam-sam-bam-summary-starter/scripts/run_pysam_sam_bam_summary.py \
  --input skills/genomics/pysam-sam-bam-summary-starter/examples/toy_reads.sam \
  --out scratch/genomics/pysam_summary.json \
  --bam-out scratch/genomics/toy_reads.bam
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/genomics/pysam-sam-bam-summary-starter/tests -p 'test_*.py'`
- Expected summary: `record_count == 4`, `mapped_count == 3`, and `reference_mapped_counts.chr1 == 2`

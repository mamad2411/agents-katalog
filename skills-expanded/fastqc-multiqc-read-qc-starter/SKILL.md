# FastQC MultiQC Read QC Starter

Use this skill to run a deterministic read-QC pass with FastQC and aggregate the result with MultiQC on a tiny FASTQ example.

## What it does

- Runs `FastQC` on a local FASTQ input from the repo-managed genomics prefix.
- Forces the prefix `bin/` onto `PATH` so the bundled `java` runtime is discoverable.
- Runs `MultiQC` over the FastQC output directory and writes a compact JSON summary.

## When to use it

- You need a verified starter for sequencing read quality control.
- You want a minimal example of how `FastQC` and `MultiQC` fit together before adding trimming or alignment.
- You need deterministic summary fields for smoke tests or downstream demos.

## Example

```bash
python3 skills/genomics/fastqc-multiqc-read-qc-starter/scripts/run_fastqc_multiqc_read_qc.py \
  --input skills/genomics/fastqc-multiqc-read-qc-starter/examples/toy_reads.fastq \
  --summary-out scratch/genomics/fastqc_multiqc_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/genomics/fastqc-multiqc-read-qc-starter/tests -p 'test_*.py'`
- Expected summary: `total_sequences == 4`, `gc_percent == 50`, and `multiqc_sample_count == 1`

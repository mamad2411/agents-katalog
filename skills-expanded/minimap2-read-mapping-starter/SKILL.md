# minimap2 Read Mapping Starter

Use this skill to align a tiny FASTQ file against a small reference with `minimap2`, sort and index the resulting BAM, and summarize the alignments.

## What it does

- runs `minimap2 -a -x sr` from the repo-managed genomics prefix
- sorts and indexes the alignment with `samtools`
- reports mapped and unmapped reads, mean MAPQ, and representative alignments

## When to use it

- you need a verified starter for `alignment-and-mapping`
- you want a minimal short-read mapping example before adding quantification or variant calling
- you need a deterministic BAM-producing smoke fixture

## Example

```bash
./slurm/envs/genomics/bin/python skills/genomics/minimap2-read-mapping-starter/scripts/run_minimap2_read_mapping.py \
  --reference skills/genomics/minimap2-read-mapping-starter/examples/toy_reference.fa \
  --reads skills/genomics/minimap2-read-mapping-starter/examples/toy_reads.fastq \
  --bam-out scratch/genomics/minimap2/toy_reads.bam \
  --summary-out scratch/genomics/minimap2/toy_reads_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/genomics/minimap2-read-mapping-starter/tests -p 'test_*.py'`
- Expected summary: `read_count == 3`, `mapped_count == 2`, `reference_names == ["chrToy"]`

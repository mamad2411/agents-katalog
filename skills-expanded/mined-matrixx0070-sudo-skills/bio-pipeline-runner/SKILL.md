---
name: bio-pipeline-runner
version: 1.0.0
description: Plan and assemble an nf-core bioinformatics run (rnaseq, sarek, atacseq) with a schema-validated samplesheet, pinned version, and correct profile.
author: matrixx0070
tags: [nf-core, nextflow, rnaseq, sarek, atacseq, pipeline]
capabilities: []
---

## When to use

Use this when the user wants to run a standardized nf-core pipeline on sequencing data and needs the samplesheet, config, and command assembled correctly the first time — rnaseq (expression), sarek (variants), or atacseq (open chromatin).

**Not for:** custom one-off analyses with no nf-core equivalent, QC of an already-produced count matrix (use bio-single-cell-qc), or interpreting biology from finished results.

## Method

1. Match pipeline to the assay. **Decision:** rnaseq for DGE/quantification, sarek for germline/somatic variants, atacseq for open chromatin. If the assay doesn't map cleanly, stop and clarify rather than force-fit.
2. Pin the version with `-r <release>` and pick the reference (iGenomes key or explicit FASTA/GTF).
3. Build the samplesheet in the pipeline's exact schema:
   - rnaseq: `sample,fastq_1,fastq_2,strandedness`
   - sarek: `patient,sample,lane,fastq_1,fastq_2`
   - atacseq: `sample,fastq_1,fastq_2,replicate`
   Validate paths exist and paired-end mates match.
4. Choose the execution profile: docker/singularity/conda for containers plus an executor (local/slurm) and resource limits via `-c`. **Decision:** singularity on shared HPC (no root), docker on a personal box.
5. Dry-run with `-profile test` or `-stub` to catch schema errors before burning compute.
6. Launch, then inspect MultiQC and `pipeline_info` execution reports for failures and resource waste.

## Example

Bulk RNA-seq, 6 samples, reverse-stranded, on a SLURM cluster. Choose `nf-core/rnaseq -r 3.14.0`, genome `GRCh38`. Samplesheet rows read `ctrl_1,/data/c1_R1.fq.gz,/data/c1_R2.fq.gz,reverse`. Profile: `-profile singularity` with a `slurm.config` capping 16 CPU / 72 GB per process. `-profile test` passes, then the full run. MultiQC STAR alignment rate ~92% confirms the stranded setting was right.

## Pitfalls

- Leaving strandedness as `auto` when the kit is known — silently wrong DGE if guessed incorrectly.
- Not pinning `-r`, so a later default-branch change makes the run irreproducible.
- Skipping the `-profile test` dry-run and discovering a samplesheet typo after hours of alignment.
- Requesting more memory per process than the node has, so every job pends forever.

## Output format

```
# nf-core Run Plan — <pipeline>
Pipeline: nf-core/<name>  Version: -r <release>  Genome: <key/FASTA+GTF>  Rationale: <one line>

## samplesheet.csv
<header + rows in exact schema>

## Command
nextflow run nf-core/<pipeline> -r <ver> \
  --input samplesheet.csv --outdir results \
  --genome <key> -profile <container>,<executor> -c <custom.config>

## Post-run checklist
MultiQC sections to check | common failure modes | where results land
```
The run executes on the user's compute — report commands, never fabricate results.

## Reference

### Pipeline selection

| Assay / question | nf-core pipeline | Core output |
|------------------|-----------------|-------------|
| Bulk gene expression / DGE | `rnaseq` | Gene & transcript counts, QC |
| Germline / somatic variants (WGS/WES/panel) | `sarek` | VCFs (SNV/indel/CNV/SV), annotation |
| Chromatin accessibility | `atacseq` | Peaks, consensus set, QC |
| ChIP / TF binding | `chipseq` | Peaks, coverage |
| Differential exon/isoform | `rnasplice` | Splicing events |
| Amplicon / metagenomics | `ampliseq` / `mag` | ASVs / MAGs |
| scRNA-seq (alignment→matrix) | `scrnaseq` | Count matrix (feeds bio-single-cell-qc) |

### nf-core/rnaseq (v3.14+) key params

- `--input` samplesheet: `sample,fastq_1,fastq_2,strandedness` — strandedness ∈ `forward` (e.g. some Ligation kits), `reverse` (Illumina TruSeq stranded / dUTP — most common), `unstranded`, `auto`. Set it explicitly when the kit is known; `auto` (salmon inference) is a fallback, not a default.
- Aligner: `--aligner star_salmon` (default, recommended — gives gene + transcript quant), `star_rsem`, or `--pseudo_aligner salmon`/`kallisto` (alignment-free, fast).
- Reference: `--genome GRCh38` (iGenomes) **or** explicit `--fasta`/`--gtf` (iGenomes GTFs are dated — a current GENCODE/Ensembl GTF is often better).
- Useful: `--extra_salmon_quant_args`, `--skip_biotype_qc`, `--remove_ribo_rna` (+ `--ribo_database_manifest`), `--umitools_*` for UMI protocols.
- QC bundled: FastQC, trimming (Trim Galore/fastp), STAR logs, RSeQC, Qualimap, dupRadar, Preseq, DESeq2 sample-similarity PCA, all rolled into MultiQC. Sanity check: STAR uniquely-mapped ≥ ~80–90%, assigned reads high, and the strandedness bar plot matches your declared setting.

### nf-core/sarek (v3.4+) key params

- `--input`: `patient,sample,lane,fastq_1,fastq_2` (or `bam`/`cram` + `.crai`). Group tumor/normal by shared `patient`, set `status` (0=normal,1=tumor) for somatic.
- `--wes` for exome/panel (add `--intervals target.bed` — critical for runtime & correctness); omit for WGS.
- `--tools`: callers e.g. `strelka,mutect2,manta,cnvkit,ascat,deepvariant,haplotypecaller,freebayes,vep,snpeff`. Germline → `haplotypecaller`/`deepvariant`; somatic → `mutect2`/`strelka`; SV → `manta`; CNV → `cnvkit`/`ascat`.
- `--genome GATK.GRCh38` (bundles known-sites for BQSR); `--joint_germline` for cohort GVCF joint calling. `--step` can resume at `mapping|markduplicates|prepare_recalibration|recalibrate|variant_calling|annotate`.

### nf-core/atacseq (v2.1+) key params

- `--input`: `sample,fastq_1,fastq_2,replicate` (replicate integer groups technical/biological reps for consensus peaks).
- `--read_length` (drives MACS2 effective genome size), `--narrow_peak` (default; omit → broad), `--macs_gsize` (or auto from genome). Blacklist filtering is applied for supported genomes.
- QC: TSS enrichment, FRiP, fragment-length periodicity (nucleosome laddering), library complexity — inspect in MultiQC.

### Reproducibility & profiles

- **Always** pin `-r <release>` (e.g. `-r 3.14.0`); an unpinned run tracks the default branch and drifts.
- Container/env profile: `-profile docker` (personal box, root), `singularity`/`apptainer` (shared HPC, no root — most common), `conda` (last resort), plus executor via a `-c custom.config` (`process.executor = 'slurm'`, queue, `withName`/`withLabel` resource overrides). nf-core resource labels: `process_low` (~2 CPU/12 GB), `process_medium` (~6 CPU/36 GB), `process_high` (~12 CPU/72 GB), `process_high_memory` (~200 GB, e.g. STAR index for large genomes). Never request more than a node offers or jobs pend forever.
- Rough guidance: human WGS sarek ≈ 100–300 GB scratch + tens of core-hours/sample; STAR RNA index needs ~30–40 GB RAM; use `-resume` to reuse cached tasks; set `-work-dir` on fast scratch and clean it after.
- **Dry run first:** `-profile test,<container>` (tiny bundled data) or `-stub` catches samplesheet/schema errors before burning real compute. `--outdir` is required; results land under it with `pipeline_info/` (execution_report.html, timeline, trace) and `multiqc/`.

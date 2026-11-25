---
name: gse-data
description: Use when collecting, downloading, verifying, or documenting GEO/GSE datasets; creating or refreshing samples.tsv, sample_characteristics.tsv, references.tsv, sample-platform metadata, or platform_counts from GEO SOFT; maintaining source indexes for GSE data; or checking whether a GSE has BRCA1/BRCA2, publications, or other sample groups.
---

# GSE Data

## Overview

Use this skill to make GEO/GSE downloads auditable: keep raw files immutable,
derive sample manifests from GEO metadata rather than hand edits, and update the
minimal source summaries that future agents need.

## Workflow

1. Confirm the accession and scope.
   - Use official GEO pages/FTP for current facts.
   - Decide whether to download only GEO processed/supplementary files or also
     SRA/FASTQ. Default: save SRA RunInfo, do not download sequence files unless
     explicitly requested.

2. Create a self-contained dataset directory.
   - Preferred layout: `data/<GSE>/raw/`, `data/<GSE>/README.md`,
     `data/<GSE>/samples.tsv`, `data/<GSE>/sample_characteristics.tsv`,
     `data/<GSE>/references.tsv`, and `data/<GSE>/papers/` when GEO exposes
     PubMed citations.
   - Never manually modify files under `raw/` after download.
   - Put papers under `data/<GSE>/papers/`, never under `raw/`.

3. Download the small provenance files as well as the analysis files.
   - GSE SOFT: `soft/<GSE>_family.soft.gz`
   - GSE MINiML: `miniml/<GSE>_family.xml.tgz`
   - Series matrix: `matrix/<GSE>_series_matrix.txt.gz`
   - Supplementary files: `suppl/`
   - Platform metadata: relevant `GPL*_family.soft.gz` and MINiML files
   - SRA metadata: `RunInfo.csv` when SRA/BioProject links exist

4. Verify before documenting.
   - Run `gzip -t` for `.gz`/`.tgz`.
   - Run `tar -tf` for tar archives.
   - Generate `md5sums.txt` after download.
   - Check sample count from SOFT, not from memory.

5. Generate sample manifests from SOFT.
   - Prefer the bundled script:

```bash
python3 <skill>/scripts/geo_soft_samples.py data/GSE223886
python3 <skill>/scripts/geo_soft_sample_characteristics.py data/GSE223886
```

   - This writes `data/<GSE>/samples.tsv` from
     `data/<GSE>/raw/<GSE>_family.soft.gz`.
   - `samples.tsv` and `sample_characteristics.tsv` must include per-sample
     `platform_id` parsed from `!Sample_platform_id`; this is required for GSEs
     that mix platforms and useful as batch metadata even for single-platform
     series.
   - Do not hand-maintain sample TSV rows when a SOFT file is available.

6. Capture publication and citation links.
   - Generate `references.tsv` from SOFT:

```bash
python3 <skill>/scripts/geo_soft_references.py data/GSE223886
```

   - Record PubMed IDs, BioProject links, and SRA series/sample links when
     present.
   - Do not search PubMed/Europe PMC to discover missing citations when GEO/SOFT
     has no PMID. If the resource does not expose a citation, leave citation
     discovery alone.
   - When PubMed IDs are present, default to downloading clearly open-access
     PDFs into `papers/` and record the PubMed links for the user:

```bash
python3 <skill>/scripts/europepmc_papers.py data/GSE223886
```

   - Verify paper metadata before documenting DOI/title/OA status:

```bash
python3 <skill>/scripts/verify_pubmed_citation.py data/GSE223886
```

   - This script needs network API access. Primary citation truth is DOI
     resolver + Crossref DOI + PubMed E-utilities. Use Europe PMC/PMC OA for
     PMCID, OA, and PDF status, not as the main DOI authority. If the primary
     checks disagree, keep status `review`.
   - Before summarizing, recommending, or interpreting a dataset, read the paper
     itself when available: at minimum abstract, study design/methods, sample
     definitions, data availability, and any author-provided caveats. Do not
     infer biological meaning from GEO titles alone when the paper is present.
   - If the primary checks disagree, use Consensus search as a second opinion
     before writing the summary, and leave citation status as `review` until
     fixed.

7. Update the repo's source records.
   - `config/sources.yaml`: machine-readable source facts, paths, counts, and
     file lists. Include `platform`, `platform_title`, `sample_characteristics`,
     and `platform_counts` when platform metadata is available.
   - `docs/sources.md`: short agent-facing summary only: what it is, useful
     sample groups and counts, platform counts, and where `samples.tsv`,
     `sample_characteristics.tsv`, and `references.tsv` live.
   - `INDEX.md`: one compact navigation entry per dataset.
   - Dataset `README.md`: download date, raw files, verification evidence, and
     regeneration command.

## Commands

GEO FTP parent is based on the accession prefix. Example:

```text
GSE161529 -> https://ftp.ncbi.nlm.nih.gov/geo/series/GSE161nnn/GSE161529/
GSE223886 -> https://ftp.ncbi.nlm.nih.gov/geo/series/GSE223nnn/GSE223886/
```

Common downloads:

```bash
curl -L -C - -o data/GSE/raw/GSE_family.soft.gz \
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSEnnnnn/GSE/soft/GSE_family.soft.gz
curl -L -C - -o data/GSE/raw/GSE_RAW.tar \
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSEnnnnn/GSE/suppl/GSE_RAW.tar
curl -L -o data/GSE/raw/RunInfo.csv \
  'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA...'
```

Always quote SRA RunInfo URLs in shells where `?` may glob.

## Resources

- `scripts/geo_soft_samples.py`: deterministic parser for
  `GSE*_family.soft.gz` to `samples.tsv`, including `platform_id`.
- `scripts/geo_soft_sample_characteristics.py`: deterministic parser for all
  sample characteristics to `sample_characteristics.tsv`, including
  `platform_id`, SRA experiment, and BioSample accessions.
- `scripts/geo_soft_references.py`: parser for publication and repository
  links from `GSE*_family.soft.gz` to `references.tsv`.
- `scripts/europepmc_papers.py`: downloads clearly open-access paper PDFs from
  PubMed rows in `references.tsv` into `papers/` and writes
  `papers/paper_downloads.tsv`.
- `scripts/verify_pubmed_citation.py`: cross-checks PubMed IDs against NCBI,
  Europe PMC, PMC OA, and Crossref, then writes
  `papers/citation_verification.tsv`.
- `references/gse-layout.md`: concise directory, metadata, and documentation
  policy.

Read the reference when creating or reviewing a repository's GEO data layout.

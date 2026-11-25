---
name: tcga-gdc-data
description: Build, verify, or document source-separated TCGA/GDC workflows inside a public-data warehouse repo, especially /root/rstudio/projects/public_data. Use when Codex must refresh GDC manifests, audit local TCGA source folders, check whether TCGA-BRCA or other TCGA warehouse data are complete/current, interpret GDC release updates versus sample/follow-up changes, keep config/sources.yaml and INDEX.md synchronized, or handle warehouse boundaries for BRCA HRD/signature resources such as SBS3, CN17, ID6, ID8, CHORD, PanCan-DDR HRD_Score, Xena, cBioPortal, METABRIC, or publication supplements. Do not use as a generic TCGA biology or API lookup skill when no local warehouse/repo work is involved.
---

# TCGA/GDC Data

Use this skill to keep TCGA/GDC data work manifest-first, source-separated, and
auditable. It is designed for public-data warehouse repos, especially
`/root/rstudio/projects/public_data`, but the workflow is general.

## Boundary With Life-Science Research Skills

Use OpenAI curated `life-science-research` skills for compact external API
lookups, such as cBioPortal study summaries, NCBI/GEO metadata, PubMed/PMC
metadata, gene/variant/database summaries, or quick one-off biological
questions.

Use this skill when the task has a local warehouse side effect or audit:

- creating or refreshing GDC manifests;
- downloading or verifying TCGA files;
- deciding how to store Xena, cBioPortal, GDC, GitHub mirrors, and publication
  supplements without mixing source truths;
- updating `config/sources.yaml`, `docs/sources.md`, `INDEX.md`, dataset
  `README.md`, manifests, or checksums;
- checking whether local TCGA/BRCA HRD resources are fully registered and
  documented.

When both apply, use the curated life-science skill for the external lookup and
then apply this skill to store, register, or audit the result locally.

## Operating Workflow

1. Inspect the repo contract before acting:
   - Read `AGENTS.md`, `INDEX.md`, `config/sources.yaml`, relevant `docs/*.md`,
     and `git status --short`.
   - Treat existing dirty files and untracked data as user/current work; do not
     revert them.
2. Separate source truths:
   - GDC current harmonized files go in `data/gdc-tcga-<project>/`.
   - Fixed GDC/publication supplements get their own source IDs.
   - Xena, cBioPortal, GitHub mirrors, and paper supplements stay in their own
     source-prefixed folders.
   - Derived integrations get separate derived-only folders with explicit
     input-source metadata.
3. Use GDC manifest-first flow:
   - Generate or refresh manifests.
   - Review counts, access levels, workflow names, file sizes, and controlled
     boundaries before downloading.
   - Download only explicit open layers unless the user has authorization for
     controlled files.
4. Verify currentness with live GDC metadata when the user asks about latest,
   recent updates, sample counts, clinical follow-up, or current file totals.
   Check GDC status, case totals, per-profile file totals, `updated_datetime`,
   workflow type, and workflow version.
5. Interpret TCGA updates conservatively:
   - A new GDC release is not automatically new samples or new follow-up.
   - For legacy TCGA projects, recent changes are often harmonized workflow,
     file metadata, or reprocessed omics layers.
6. Update registry/docs together:
   - `config/sources.yaml`: machine-readable source registry.
   - `docs/sources.md`: human-readable source scope and caveats.
   - `INDEX.md`: navigation index.
   - Dataset `README.md`: source-local scope, layout, commands, and caveats.
7. Verify before reporting:
   - Parse YAML.
   - Check source IDs against `data/` folders and docs.
   - Check `download_status.tsv` for errors.
   - Run `git diff --check`.
   - Report any controlled-access, missing-score, or derived-only boundaries.

## Generalization Rules

- Do not assume `public_data` paths in another repo; inspect that repo's
  registry, data layout, and docs first.
- If repo-local GDC scripts do not exist, use the same manifest-first design
  with the official GDC API and document the exact filters.
- Support any TCGA project ID, not only BRCA/OV. Keep project-specific
  biological rules in references or dataset docs.
- Keep local facts and live external facts separate. Mark memory-derived or
  previously observed GDC release facts as stale unless refreshed in the
  current turn.
- Prefer source IDs that encode source authority, for example
  `gdc-tcga-brca`, `xena-tcga-brca-curated`, or
  `cbioportal-brca-metabric`.

## Common Commands

Prefer repo-local scripts when present:

```bash
python3 scripts/download/gdc_tcga_manifests.py --projects TCGA-BRCA TCGA-OV
python3 scripts/download/gdc_download_layers.py --sources gdc-tcga-brca gdc-tcga-ov
cat manifests/downloads/gdc-tcga.manifest_summary.tsv
cat manifests/downloads/gdc-tcga-brca/download_status.tsv
```

Use the bundled audit helper for registry/documentation checks:

```bash
python3 /root/.codex/skills/research__tcga-gdc-data/scripts/audit_public_data_registry.py /path/to/public_data
```

If running from a staging copy of the skill, replace the script path with the
local skill path.

## BRCA HRD/Signature Work

Read `references/brca-hrd-signature-map.md` when the task involves TCGA-BRCA
BRCAness, TNBC labels, SBS3, CN17, ID6/ID8, HRDscore, CHORD, Xena, METABRIC,
or publication-supplement matching.

Default decision rules:

- Rebuild TCGA-BRCA TNBC labels downstream from GDC clinical XML when
  reproducibility matters.
- Record the exact HER2 equivocal/FISH rule; do not silently mix a publication
  TNBC label with a GDC-derived label.
- Use GDC PanCan-DDR as the fixed TCGA `HRD_Score` source when registered.
- Use GerkeLab TCGAhrd only as a cross-check mirror.
- Use Synapse/PCAWG7 or another explicitly registered SigProfiler source for
  modern `SBS3` nomenclature.
- Use a dedicated copy-number signature source for `CN17`; do not infer CN17
  from raw segments unless a downstream method is implemented and documented.
- Keep CHORD probabilities/classes separate from LOH+TAI+LST scar scores.
- Keep METABRIC microarray, targeted mutation, and ASCAT lanes separate from
  RNA-seq TPM and genome-wide WES/WGS signature lanes.

## Output Standard

When reporting, give:

- What was checked or changed.
- Counts and dates used as evidence.
- Which sources are registered and which are only candidate/deferred.
- Remaining boundaries: controlled data, unavailable scores, stale external
  mirrors, missing package/environment, or downstream-only integration.

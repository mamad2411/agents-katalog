---
name: loading-data
description: Internal routing helper — called from profiling-datasets Stage 2. Routes a file path to the correct format-specific loader. Do NOT invoke directly; always start with profiling-datasets.
compatibility: Works offline. Requires pandas ≥1.5. Format-specific parsers listed per loader.
---

# Loading Data

> **Internal skill.** This skill is invoked by `profiling-datasets` Stage 2 — not directly by the agent or user. Always start with `profiling-datasets`, which handles detection, loading, analysis, and preprocessing recommendations as a single pipeline.

## When NOT to invoke this directly

| Situation | Correct skill |
|---|---|
| User provides a local file path (.fastq, .csv, .fasta, .fcs, etc.) | `profiling-datasets` |
| User provides a HuggingFace Hub dataset ID | `profiling-datasets` |
| User wants to profile, inspect, or analyze a dataset | `profiling-datasets` |
| User wants to preprocess already-loaded sequences | `protein-sequence-data-processing` |
| User wants to preprocess already-loaded tabular data | `numerical-data-processing` |

---

## Routing table

All loaders are located under `loading-data/loaders/`. `profiling-datasets` Stage 2 uses this table to dispatch to the correct loader.

| Extension(s) | dataset_type | Loader skill path |
|---|---|---|
| `.csv` `.tsv` `.tab` | `tabular` | `loading-data/loaders/load-csv` |
| `.xlsx` `.xls` | `tabular` | `loading-data/loaders/load-excel` |
| `.parquet` `.arrow` | `tabular` | `loading-data/loaders/load-parquet` |
| `.jsonl` `.ndjson` | `tabular` / `text` | `loading-data/loaders/load-jsonl` |
| `.asc` | `tabular` | `loading-data/loaders/load-asc` |
| `.fasta` `.fa` `.faa` | `protein_sequence`* | `loading-data/loaders/load-fasta` |
| `.fna` | `nucleotide_sequence`* | `loading-data/loaders/load-fasta` |
| `.fastq` `.fq` | `raw_reads` | `loading-data/loaders/load-fastq` |
| `.bam` `.sam` | `aligned_reads` | `loading-data/loaders/load-bam` |
| `.fcs` | `flow_cytometry` | `loading-data/loaders/load-fcs` |
| `.h5` `.h5ad` | `single_cell` | `loading-data/loaders/load-h5` |
| `.mtx` | `single_cell` | `loading-data/loaders/load-mtx` |
| `.tif` `.tiff` `.png` `.scn` | `image` | `loading-data/loaders/load-tif` *(out of PLM scope — report and stop)* |

> *`load-fasta` confirms `protein_sequence` vs `nucleotide_sequence` via alphabet detection after loading.

If extension is ambiguous, sniff first line (see `profiling-datasets/references/routing-rules.md`).

---

## Instrument → format quick reference

| Instrument | Typical format | Loader |
|---|---|---|
| Plate Reader (Agilent BioTek, Tecan) | `.csv` `.xlsx` | `load-csv` / `load-excel` |
| Octet / BLI (ForteBio, GATOR) | `.csv` `.xlsx` | `load-csv` / `load-excel` |
| Nanodrop / Qubit | `.csv` | `load-csv` |
| Automated Cell Counter | `.csv` `.xlsx` | `load-csv` / `load-excel` |
| Flow Cytometry (BD, Cytek, Sony) | `.fcs` | `load-fcs` |
| Sequencer / NGS (Illumina, Element) | `.fastq` `.bam` `.fasta` `.mtx` `.h5` | format-specific |
| Chromatography (ÄKTA FPLC) | `.asc` | `load-asc` |
| Microscope / Gel Doc | `.tif` `.png` | `load-tif` *(image — out of scope)* |

---

## Hard constraints

- **Always** validate loadability before returning — set `loadability.status = fail` on exception
- **Never** return raw file bytes as the output
- **Always** record `routed_to` in the profile with the loader skill name used

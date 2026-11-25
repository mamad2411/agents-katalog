---
name: load-bam
description: Load BAM or SAM files into a pandas DataFrame using pysam. Extracts read sequences, mapping flags, CIGAR strings, and quality scores. Emits an aligned_reads Dataset Profile with alignment stats. BAM is not a PLM input — report and stop.
compatibility: pysam ≥0.20, pandas ≥1.5. Linux/macOS only (pysam not available on Windows).
instruments: Sequencer — Illumina MiSeq, Element Biosciences Aviti, PromethION 2 (aligned output)
---

# Load BAM / SAM

> **Not a PLM input.** BAM/SAM files contain aligned sequencing reads. They are not directly usable for protein language model fine-tuning. This loader reports alignment stats and stops — it does not produce a PLM-ready dataset. Route to the appropriate downstream tool depending on task (featureCounts for RNA-seq, Cell Ranger for scRNAseq, GATK for variant calling).

## When to use

File is `.bam` or `.sam` — aligned sequencing reads mapped to a reference genome.
Sources: NGS pipelines (BWA, STAR, HISAT2 output), Cell Ranger BAM output for scRNAseq.

---

## Loading

```python
import pysam
import pandas as pd

def load_bam(path: str, max_reads: int = 100_000) -> tuple[pd.DataFrame, dict]:
    fmt = "rb" if path.endswith(".bam") else "r"
    records = []
    try:
        with pysam.AlignmentFile(path, fmt) as bam:
            header_refs = list(bam.references)
            for i, read in enumerate(bam.fetch(until_eof=True)):
                if i >= max_reads:
                    break
                records.append({
                    "read_id":   read.query_name,
                    "sequence":  read.query_sequence or "",
                    "length":    read.query_length or 0,
                    "flag":      read.flag,
                    "is_mapped": not read.is_unmapped,
                    "mapq":      read.mapping_quality,
                    "cigar":     read.cigarstring or "*",
                    "reference": read.reference_name,
                })
    except Exception as e:
        raise ValueError(f"LOAD ERROR: could not parse BAM/SAM — {e}")

    if not records:
        raise ValueError(f"LOAD ERROR: no reads found in {path}")

    df = pd.DataFrame(records)
    return df, {
        "parser": f"pysam({fmt})",
        "refs": header_refs,
        "truncated_at": max_reads,
        "dataset_type": "aligned_reads",
    }
```

> BAM files can be very large. Default cap is 100k reads for profiling. Warn if file exceeds cap.

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Not valid BAM/SAM | `fail` | `"LOAD ERROR: could not parse BAM/SAM — {detail}"` |
| Zero reads | `fail` | `"LOAD ERROR: no reads found in {path}"` |
| Reads truncated at cap | `warn` | `"LOAD WARN: profiling based on first 100k reads — file may contain more"` |
| >20% unmapped reads | `warn` | `"LOAD WARN: {pct}% of reads are unmapped"` |

---

## Profile fields populated

- `format`: `"bam"` or `"sam"`
- `dataset_type`: `"aligned_reads"` (always)
- `shape`: `{ sequences: N }` (up to cap)
- `sequence_stats`: `length_min`, `length_median`, `length_max`, `read_type: "dna"`, `is_plm_ready: false`
- `sample_stats`: `mapq` distribution, `pct_mapped`
- `missing`: reads with null sequence

---

## Preprocessing defaults

1. **Uppercase sequences** and filter empty/null sequence reads (flag count)
2. **Compute mapping stats** — `pct_mapped`, `mean_mapq`, `median_mapq`
3. **Flag secondary/supplementary alignments** — reads with flag bits 256/2048 set; report count
4. **Detect alphabet** — BAM is almost always DNA; flag if non-ACGTN chars > 1%
5. **Set `is_plm_ready = false`** — BAM is always aligned_reads, never a PLM input
6. **Report reference contigs** — list unique `reference` values from reads

---

## Output

```python
{
    "df": pd.DataFrame,   # columns: read_id, sequence, length, flag, is_mapped, mapq, cigar, reference
    "profile": {
        "format": "bam",
        "dataset_type": "aligned_reads",
        "shape": { "sequences": N },
        "sequence_stats": {
            "length_min": ..., "length_median": ...,
            "read_type": "dna",
            "is_plm_ready": False,
            "pct_over_512": None,
            "pct_over_1024": None
        },
        "sample_stats": {
            "mapq": { "min": ..., "median": ..., "mean": ... },
            "pct_mapped": 94.2
        },
        "loadability": { "status": "ok", "parser": "pysam(rb)", "errors": [] },
        "warnings": [
            "BAM/SAM is aligned sequencing data — not a PLM input",
            "Downstream tools: featureCounts/HTSeq (RNA-seq), Cell Ranger (scRNAseq), GATK (variant calling)"
        ]
    }
}
```

---

## Production constraints

- **Always** set `dataset_type = "aligned_reads"` and `is_plm_ready = false`
- **Always** add the non-PLM warning with downstream tool suggestions
- **Always** cap reads at 100k for profiling — never load a full BAM into memory without warning
- **Never** filter unmapped reads silently — report pct in `warnings`
- **Always** note if file was truncated in `warnings`

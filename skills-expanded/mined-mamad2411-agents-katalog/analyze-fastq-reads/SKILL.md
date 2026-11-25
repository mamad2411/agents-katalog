---
name: analyze-fastq-reads
description: Stage 3 analysis for raw_reads (FASTQ) datasets. Computes read length and quality score distributions, Q20/Q30 thresholds, base composition per position. Generates plots. Always flags FASTQ as non-PLM and recommends quality-filter → align pipeline.
compatibility: pandas ≥1.5, matplotlib ≥3.6, numpy ≥1.23. Works offline.
---

# Analyze FASTQ Reads

> **Not a PLM input.** FASTQ analysis reports quality metrics only. The output is a quality assessment report — not a preprocessed dataset. Always recommend quality filtering and alignment before any downstream task.

## When to use

Called by `profiling-datasets` Stage 3 when `dataset_type` is `raw_reads`.
Do not call directly — always receives data + profile from `load-fastq`.

---

## Input contract

```python
{
    "df": pd.DataFrame,   # columns: read_id, sequence, length, mean_q, min_q, qual_string
    "profile": {
        "dataset_type": "raw_reads",
        "sequence_stats": { "read_type": "dna", "is_plm_ready": False },
        "loadability": { "status": "ok" },
        ...
    }
}
```

---

## Statistics to compute

```python
import pandas as pd
import numpy as np

def compute_read_stats(df: pd.DataFrame) -> dict:
    lengths = df["length"]
    mean_q  = df["mean_q"]

    return {
        "n_reads":        len(df),
        "length_min":     int(lengths.min()),
        "length_median":  float(lengths.median()),
        "length_mean":    float(lengths.mean()),
        "length_max":     int(lengths.max()),
        "length_std":     float(lengths.std()),
        "is_variable_length": bool(lengths.std() > 10),
        "q_min":          float(mean_q.min()),
        "q_median":       float(mean_q.median()),
        "q_mean":         float(mean_q.mean()),
        "q_max":          float(mean_q.max()),
        "pct_below_q20":  float((mean_q < 20).mean() * 100),
        "pct_below_q30":  float((mean_q < 30).mean() * 100),
        "n_duplicate_ids": int(df["read_id"].duplicated().sum()),
    }
```

---

## Plots to generate

```python
import matplotlib.pyplot as plt

def generate_plots(df: pd.DataFrame, out_dir: str) -> dict:
    # Canonical palette — always use these hex values, never named colors
    _PRIMARY  = "#1E5994"   # BLUE_0    — Q score histogram
    _ACCENT   = "#E6905B"   # ORANGE_50 — length histogram
    _REF1     = "#9B3208"   # ORANGE_0  — Q20 threshold line
    _REF2     = "#713D8F"   # PURPLE_0  — Q30 threshold line
    # Base composition: A=green, C=blue, G=orange, T=purple, N=noise grey
    _BASE_COLORS = {
        "A": "#0E625C",   # GREEN_0
        "C": "#1E5994",   # BLUE_0
        "G": "#9B3208",   # ORANGE_0
        "T": "#713D8F",   # PURPLE_0
        "N": "#AAAAAA",   # noise grey
    }

    plots = {}

    # 1. Mean Q score distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["mean_q"], bins=40, color=_PRIMARY, alpha=0.8)
    ax.axvline(20, color=_REF1, linestyle="--", label="Q20 threshold")
    ax.axvline(30, color=_REF2, linestyle="--", label="Q30 threshold")
    ax.legend()
    ax.set_xlabel("Mean Phred Q score per read")
    ax.set_ylabel("Number of reads")
    ax.set_title("Read quality score distribution")
    fig.tight_layout()
    path = f"{out_dir}/q_score_dist.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots["q_score_dist"] = path

    # 2. Read length distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["length"], bins=50, color=_ACCENT, alpha=0.8)
    ax.set_xlabel("Read length (bp)")
    ax.set_ylabel("Count")
    ax.set_title("Read length distribution")
    fig.tight_layout()
    path = f"{out_dir}/read_length_dist.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots["read_length_dist"] = path

    # 3. Base composition per position (short-read only; skip for variable-length long reads)
    if df["length"].std() < 10 and df["length"].median() <= 300:
        max_pos = int(df["length"].max())
        base_comp = {b: [] for b in "ACGTN"}
        for pos in range(min(max_pos, 200)):
            col = df["sequence"].str[pos].str.upper()
            total = len(col.dropna())
            for b in "ACGTN":
                base_comp[b].append((col == b).sum() / total if total > 0 else 0)

        fig, ax = plt.subplots(figsize=(12, 4))
        positions = range(min(max_pos, 200))
        for b in "ACGTN":
            ax.plot(positions, base_comp[b], label=b,
                    color=_BASE_COLORS[b], linewidth=0.8)
        ax.set_xlabel("Position (bp)")
        ax.set_ylabel("Fraction")
        ax.set_title("Base composition per position")
        ax.legend(ncol=5)
        fig.tight_layout()
        path = f"{out_dir}/base_composition.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["base_composition"] = path

    return plots
```

---

## Quality flags and warnings

```python
def compute_warnings(stats: dict) -> list[str]:
    warnings = ["FASTQ is raw sequencing data — not a PLM input; quality-filter and align first"]

    if stats["pct_below_q20"] > 10:
        warnings.append(f"{stats['pct_below_q20']:.1f}% of reads have mean Q < 20 — low overall quality; consider re-sequencing or aggressive trimming")
    if stats["pct_below_q30"] > 30:
        warnings.append(f"{stats['pct_below_q30']:.1f}% of reads have mean Q < 30 — quality filtering recommended before alignment")

    if stats["is_variable_length"]:
        warnings.append(f"Variable read lengths detected (std={stats['length_std']:.0f} bp) — likely long-read data; use long-read aligner (minimap2)")

    if stats["n_duplicate_ids"] > 0:
        warnings.append(f"{stats['n_duplicate_ids']} duplicate read IDs — may indicate PCR duplicates; use markdup after alignment")

    return warnings
```

---

## Key decision gate

FASTQ is **raw sequencing data** — it is never a direct PLM input:

| Alphabet | Next step |
|---|---|
| DNA (expected) | Quality filter (fastp/Trimmomatic) → align (BWA-MEM/HISAT2/STAR) → BAM → downstream |
| Protein (rare, unexpected) | Flag as unusual — ask user to confirm sequence type before proceeding |

---

## Preprocessing recommendations

```python
def recommend_preprocessing(stats: dict) -> list[str]:
    steps = [
        "1. Quality filter reads: fastp --qualified_quality_phred 20 --length_required 50",
        "2. Check adapter trimming (fastp auto-detects common adapters)",
    ]

    if stats["is_variable_length"]:
        steps.append("3. Align with minimap2 (long reads: -ax map-ont or -ax map-pb)")
    else:
        steps.append("3. Align with BWA-MEM (DNA-seq) or STAR/HISAT2 (RNA-seq)")

    steps.append("4. Convert to BAM → sort → index (samtools sort -o out.bam)")
    steps.append("5. Proceed based on downstream task: featureCounts (RNA-seq), Cell Ranger (scRNAseq), GATK (variants)")

    return steps
```

---

## Output

```python
{
    "profile": { ...updated with read quality stats... },
    "plots": {
        "q_score_dist":     "path/to/q_score_dist.png",
        "read_length_dist": "path/to/read_length_dist.png",
        "base_composition": "path/to/base_composition.png"  # short-read only
    },
    "warnings": [
        "FASTQ is raw sequencing data — not a PLM input; quality-filter and align first",
        ...
    ],
    "preprocessing_recommended": [
        "Quality filter (fastp Q20, min_len 50)",
        "Align with BWA-MEM / STAR / minimap2",
        "Sort and index BAM",
        "Proceed to featureCounts / Cell Ranger / GATK"
    ]
}
```

---

## Production constraints

- **Always** include the non-PLM warning as the first warning
- **Never** suggest using FASTQ as a PLM input
- **Never** filter reads — flag quality issues only
- **Always** distinguish short-read from long-read based on length std

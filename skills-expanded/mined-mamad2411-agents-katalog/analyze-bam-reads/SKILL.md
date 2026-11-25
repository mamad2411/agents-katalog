---
name: analyze-bam-reads
description: Stage 3 analysis for aligned_reads (BAM/SAM) datasets. Reports mapping rate, MAPQ distribution, flag breakdown, read length distribution, and reference contig counts. Report-only — no preprocessing for BAM in PLM context.
compatibility: pandas ≥1.5, matplotlib ≥3.6. Works offline (pysam required upstream).
---

# Analyze BAM Reads

> **Not a PLM input.** BAM analysis is report-only. This skill computes alignment quality metrics and suggests downstream tools — it does not produce a preprocessed dataset.

## When to use

Called by `profiling-datasets` Stage 3 when `dataset_type` is `aligned_reads`.
Do not call directly — always receives data + profile from `load-bam`.

---

## Input contract

```python
{
    "df": pd.DataFrame,   # columns: read_id, sequence, length, flag, is_mapped, mapq, cigar, reference
    "profile": {
        "dataset_type": "aligned_reads",
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

def compute_alignment_stats(df: pd.DataFrame) -> dict:
    n_total  = len(df)
    n_mapped = df["is_mapped"].sum()

    # SAM flag bit interpretation
    FLAG_SECONDARY     = 0x100   # 256
    FLAG_SUPPLEMENTARY = 0x800   # 2048

    return {
        "n_reads":            n_total,
        "n_mapped":           int(n_mapped),
        "pct_mapped":         float(n_mapped / n_total * 100) if n_total > 0 else 0,
        "n_secondary":        int((df["flag"] & FLAG_SECONDARY) > 0).sum() if "flag" in df else 0,
        "n_supplementary":    int((df["flag"] & FLAG_SUPPLEMENTARY) > 0).sum() if "flag" in df else 0,
        "mapq_min":           float(df["mapq"].min()),
        "mapq_median":        float(df["mapq"].median()),
        "mapq_mean":          float(df["mapq"].mean()),
        "mapq_max":           float(df["mapq"].max()),
        "n_refs":             int(df["reference"].nunique()),
        "top_refs":           df["reference"].value_counts().head(10).to_dict(),
        "length_min":         int(df["length"].min()),
        "length_median":      float(df["length"].median()),
        "length_max":         int(df["length"].max()),
        "length_std":         float(df["length"].std()),
        "is_variable_length": bool(df["length"].std() > 10),
    }
```

---

## Plots to generate

```python
import matplotlib.pyplot as plt

def generate_plots(df: pd.DataFrame, out_dir: str) -> dict:
    # Canonical palette — always use these hex values, never named colors
    _PRIMARY  = "#1E5994"   # BLUE_0    — MAPQ histogram, primary alignments
    _ACCENT   = "#E6905B"   # ORANGE_50 — length histogram, secondary alignments
    _REF1     = "#9B3208"   # ORANGE_0  — MAPQ 20 threshold line
    _REF2     = "#713D8F"   # PURPLE_0  — MAPQ 30 threshold line
    _TERTIARY = "#C694E1"   # PURPLE_50 — supplementary alignments
    _NOISE    = "#AAAAAA"   # neutral grey — unmapped reads

    plots = {}

    # 1. MAPQ distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    mapped = df[df["is_mapped"]]["mapq"].dropna()
    ax.hist(mapped, bins=40, color=_PRIMARY, alpha=0.8)
    ax.axvline(20, color=_REF1, linestyle="--", label="MAPQ 20")
    ax.axvline(30, color=_REF2, linestyle="--", label="MAPQ 30")
    ax.legend()
    ax.set_xlabel("Mapping quality (MAPQ)")
    ax.set_ylabel("Count")
    ax.set_title("MAPQ distribution (mapped reads only)")
    fig.tight_layout()
    path = f"{out_dir}/mapq_dist.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots["mapq_dist"] = path

    # 2. Read length distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["length"].replace(0, pd.NA).dropna(), bins=50, color=_ACCENT, alpha=0.8)
    ax.set_xlabel("Read length (bp)")
    ax.set_ylabel("Count")
    ax.set_title("Read length distribution")
    fig.tight_layout()
    path = f"{out_dir}/read_length_dist.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots["read_length_dist"] = path

    # 3. Alignment flag breakdown (pie)
    mapped_n     = df["is_mapped"].sum()
    unmapped     = (~df["is_mapped"]).sum()
    secondary    = int(((df["flag"] & 0x100) > 0).sum())
    supplementary = int(((df["flag"] & 0x800) > 0).sum())
    primary      = mapped_n - secondary - supplementary

    fig, ax = plt.subplots(figsize=(6, 6))
    sizes  = [primary, secondary, supplementary, unmapped]
    labels = ["Primary", "Secondary", "Supplementary", "Unmapped"]
    colors = [_PRIMARY, _ACCENT, _TERTIARY, _NOISE]
    ax.pie([max(s, 0) for s in sizes], labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.set_title("Alignment flag breakdown")
    fig.tight_layout()
    path = f"{out_dir}/flag_breakdown.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots["flag_breakdown"] = path

    return plots
```

---

## Quality flags and warnings

```python
def compute_warnings(stats: dict) -> list[str]:
    warnings = [
        "BAM/SAM is aligned sequencing data — not a PLM input",
        "Downstream tools: featureCounts/HTSeq (RNA-seq), Cell Ranger (scRNAseq), GATK (variant calling)"
    ]

    if stats["pct_mapped"] < 70:
        warnings.append(f"Low mapping rate: {stats['pct_mapped']:.1f}% — check reference genome version or read quality")
    elif stats["pct_mapped"] < 90:
        warnings.append(f"Mapping rate {stats['pct_mapped']:.1f}% — acceptable but check for contamination")

    if stats["is_variable_length"]:
        warnings.append("Variable read lengths detected — likely long-read BAM (ONT/PacBio)")

    if stats.get("n_secondary", 0) > stats["n_reads"] * 0.05:
        pct = stats["n_secondary"] / stats["n_reads"] * 100
        warnings.append(f"{pct:.1f}% secondary alignments — multimappers present; check if this is expected for your reference")

    return warnings
```

---

## Downstream tool recommendations

| Use case | Recommended tool | Command hint |
|---|---|---|
| RNA-seq gene counts | featureCounts (Subread) | `featureCounts -a annotation.gtf -o counts.txt bam` |
| RNA-seq (alternative) | HTSeq-count | `htseq-count bam annotation.gtf` |
| Single-cell RNA-seq | Cell Ranger count | `cellranger count --bam bam` |
| Variant calling | GATK HaplotypeCaller | `gatk HaplotypeCaller -I bam -O out.vcf` |
| WGS coverage | samtools depth | `samtools depth -a bam` |

---

## Output

```python
{
    "profile": { ...updated with alignment stats... },
    "plots": {
        "mapq_dist":        "path/to/mapq_dist.png",
        "read_length_dist": "path/to/read_length_dist.png",
        "flag_breakdown":   "path/to/flag_breakdown.png"
    },
    "warnings": [
        "BAM/SAM is aligned sequencing data — not a PLM input",
        "Downstream tools: featureCounts/HTSeq (RNA-seq), Cell Ranger (scRNAseq), GATK (variant calling)"
    ],
    "preprocessing_recommended": [
        "Sort and index BAM if not already: samtools sort -o sorted.bam && samtools index sorted.bam",
        "Choose downstream tool based on task (see routing table above)"
    ]
}
```

---

## Production constraints

- **Always** include non-PLM warning and downstream tool table
- **Never** suggest using BAM as a PLM input
- **Never** filter or modify reads — report only
- **Always** report mapping rate and flag any rate below 70%

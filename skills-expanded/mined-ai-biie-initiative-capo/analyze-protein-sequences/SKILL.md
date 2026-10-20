---
name: analyze-protein-sequences
description: Stage 3 analysis for protein_sequence and nucleotide_sequence datasets. Computes length stats, alphabet composition, ESM2 length flags, duplicate counts, label distribution, and split balance. Generates matplotlib/seaborn plots. Returns preprocessing recommendations.
compatibility: pandas ≥1.5, matplotlib ≥3.6, seaborn ≥0.12. Works offline.
---

# Analyze Protein Sequences

## When to use

Called by `profiling-datasets` Stage 3 when `dataset_type` is `protein_sequence` or `nucleotide_sequence`.
Do not call directly — always receives data + profile from `load-fasta`.

---

## Input contract

```python
{
    "df": pd.DataFrame,   # columns: seq_id, header, sequence, length
    "profile": {          # from load-fasta
        "dataset_type": "protein_sequence | nucleotide_sequence",
        "sequence_stats": { "read_type": "protein | dna", "is_plm_ready": True | False },
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

def compute_sequence_stats(df: pd.DataFrame, profile: dict) -> dict:
    lengths = df["length"]
    stats = {
        "length_min":    int(lengths.min()),
        "length_median": float(lengths.median()),
        "length_mean":   float(lengths.mean()),
        "length_max":    int(lengths.max()),
        "length_std":    float(lengths.std()),
        "pct_over_512":  float((lengths > 512).mean() * 100),
        "pct_over_1024": float((lengths > 1024).mean() * 100),
        "n_sequences":   len(df),
        "n_duplicate_seq": int(df["sequence"].duplicated().sum()),
        "n_duplicate_id":  int(df["seq_id"].duplicated().sum()),
    }

    # AA composition (protein only)
    if profile["sequence_stats"]["read_type"] == "protein":
        all_chars = "".join(df["sequence"])
        aa_counts = pd.Series(list(all_chars)).value_counts(normalize=True)
        stats["aa_composition"] = aa_counts.to_dict()

    # Non-standard characters
    standard = set("ACDEFGHIKLMNPQRSTVWY") if profile["sequence_stats"]["read_type"] == "protein" else set("ACGTU")
    non_std = set("".join(df["sequence"])) - standard
    stats["non_standard_chars"] = sorted(non_std)

    return stats
```

---

## Plots to generate

```python
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots(df: pd.DataFrame, profile: dict, out_dir: str) -> dict:
    # Canonical palette — always use these hex values, never named colors
    _PRIMARY  = "#1E5994"   # BLUE_0   — main bars / histograms
    _ACCENT   = "#E6905B"   # ORANGE_50 — label distributions
    _REF1     = "#9B3208"   # ORANGE_0  — first reference line (ESM2 512)
    _REF2     = "#713D8F"   # PURPLE_0  — second reference line (ESM2 1024)

    plots = {}

    # 1. Sequence length distribution
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["length"], bins=50, color=_PRIMARY, alpha=0.8)
    if profile["sequence_stats"]["read_type"] == "protein":
        ax.axvline(512,  color=_REF1, linestyle="--", label="ESM2 512")
        ax.axvline(1024, color=_REF2, linestyle="--", label="ESM2 1024")
        ax.legend()
    ax.set_xlabel("Sequence length (aa)")
    ax.set_ylabel("Count")
    ax.set_title("Sequence length distribution")
    fig.tight_layout()
    path = f"{out_dir}/length_dist.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    plots["length_dist"] = path

    # 2. AA composition (protein only)
    if "aa_composition" in profile.get("sequence_stats", {}):
        fig, ax = plt.subplots(figsize=(10, 4))
        aa_freq = pd.Series(profile["sequence_stats"]["aa_composition"])
        aa_freq.sort_index().plot.bar(ax=ax, color=_PRIMARY, alpha=0.8)
        ax.set_xlabel("Amino acid")
        ax.set_ylabel("Frequency")
        ax.set_title("Amino acid composition")
        fig.tight_layout()
        path = f"{out_dir}/aa_composition.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["aa_composition"] = path

    # 3. Label distribution (if label present)
    label_col = _find_label_col(df)
    if label_col:
        fig, ax = plt.subplots(figsize=(8, 4))
        ml_form = profile.get("label_info", {}).get("ml_formulation", "unknown")
        if ml_form == "regression":
            ax.hist(df[label_col].dropna(), bins=40, color=_ACCENT, alpha=0.8)
            ax.set_xlabel(label_col)
            ax.set_ylabel("Count")
            ax.set_title(f"Label distribution: {label_col}")
        else:
            df[label_col].value_counts().plot.bar(ax=ax, color=_ACCENT, alpha=0.8)
            ax.set_xlabel("Class")
            ax.set_ylabel("Count")
            ax.set_title(f"Class distribution: {label_col}")
        fig.tight_layout()
        path = f"{out_dir}/label_dist.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["label_dist"] = path

    return plots


def _find_label_col(df: pd.DataFrame) -> str | None:
    for col in ("label", "score", "fitness", "y", "target"):
        if col in df.columns:
            return col
    return None
```

---

## Quality flags and warnings

```python
def compute_warnings(df: pd.DataFrame, stats: dict, profile: dict) -> list[str]:
    warnings = []
    is_protein = profile["sequence_stats"]["read_type"] == "protein"

    if not profile["sequence_stats"].get("is_plm_ready", True):
        warnings.append("nucleotide_sequence detected — not a PLM input; verify sequence type")

    if stats["pct_over_512"] > 5 and is_protein:
        warnings.append(f"{stats['pct_over_512']:.1f}% of sequences exceed 512 tokens — truncation needed for ESM2-650M")
    if stats["pct_over_1024"] > 0 and is_protein:
        warnings.append(f"{stats['pct_over_1024']:.1f}% of sequences exceed 1024 tokens — incompatible with most ESM2 variants")

    if stats["n_duplicate_seq"] > 0:
        pct = stats["n_duplicate_seq"] / len(df) * 100
        warnings.append(f"{stats['n_duplicate_seq']} duplicate sequences ({pct:.1f}%) — deduplicate before train/val split to prevent leakage")

    if stats["non_standard_chars"]:
        warnings.append(f"Non-standard characters found: {stats['non_standard_chars']} — check before tokenization")

    label_col = _find_label_col(df)
    if label_col:
        null_pct = df[label_col].isna().mean() * 100
        if null_pct > 5:
            warnings.append(f"{null_pct:.1f}% of labels are missing — consider masked loss or label_mask column")
        # Class imbalance check
        if profile.get("label_info", {}).get("ml_formulation") in ("binary_classification", "multiclass_classification"):
            counts = df[label_col].value_counts()
            if len(counts) >= 2 and counts.iloc[0] / counts.iloc[-1] > 5:
                warnings.append(f"Class imbalance ratio {counts.iloc[0] / counts.iloc[-1]:.1f}:1 — consider weighted loss or oversampling")

    return warnings
```

---

## Preprocessing recommendations

```python
def recommend_preprocessing(stats: dict, profile: dict) -> list[str]:
    steps = []
    is_protein = profile["sequence_stats"]["read_type"] == "protein"

    if not is_protein:
        steps.append("Verify sequence type — nucleotide sequences are not PLM inputs")
        return steps

    if stats["n_duplicate_seq"] / max(stats["n_sequences"], 1) > 0.01:
        steps.append("1. Deduplicate sequences before creating train/val/test split")

    steps.append("2. Create train/val/test split (recommended: 80/10/10) — split before any preprocessing")

    if stats["pct_over_512"] > 5:
        steps.append("3. Truncate or filter sequences >512 tokens for ESM2-650M (or use ESM2-3B which supports up to 1024)")

    label_col = _find_label_col(profile.get("_df_ref"))
    if label_col:
        steps.append("4. Add label_mask column for missing labels (1 = observed, 0 = missing) to enable masked loss")

    steps.append(f"5. Route to `protein-sequence-data-processing` skill for tokenization and HF Dataset creation")

    return steps
```

---

## Output

```python
{
    "profile": { ...updated with sequence_stats, sample_stats, warnings... },
    "plots": {
        "length_dist":    "path/to/length_dist.png",
        "aa_composition": "path/to/aa_composition.png",  # protein only
        "label_dist":     "path/to/label_dist.png"       # if label present
    },
    "warnings": [...],
    "preprocessing_recommended": [
        "Deduplicate sequences before split",
        "Split 80/10/10",
        "Mask missing labels",
        "Route to protein-sequence-data-processing"
    ]
}
```

---

## Production constraints

- **Never** filter or modify sequences — report only
- **Never** encode, tokenize, or convert sequences to model inputs
- **Always** flag `nucleotide_sequence` as non-PLM in warnings
- **Always** include ESM2 length flags for `protein_sequence`
- **Always** check for duplicate sequences before recommending split

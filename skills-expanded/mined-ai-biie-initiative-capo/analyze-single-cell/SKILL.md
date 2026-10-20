---
name: analyze-single-cell
description: Stage 3 analysis for single_cell (H5AD/H5/MTX) datasets. Computes shape, sparsity, QC metrics (total_counts, n_genes, pct_mt), reports available layers and obs/obsm keys. Generates scanpy QC violin and scatter plots. Routes to bio-single-cell-preprocessing.
compatibility: anndata ≥0.9, scanpy ≥1.9, pandas ≥1.5, matplotlib ≥3.6. Works offline.
---

# Analyze Single-Cell Data

## When to use

Called by `profiling-datasets` Stage 3 when `dataset_type` is `single_cell`.
Do not call directly — always receives data + profile from `load-h5` or `load-mtx`.

---

## Input contract

```python
{
    "adata": ad.AnnData,   # cells × genes sparse AnnData
    "profile": {
        "dataset_type": "single_cell",
        "loadability": { "status": "ok" },
        ...
    }
}
```

---

## Statistics to compute

```python
import anndata as ad
import pandas as pd
import numpy as np
import scanpy as sc

def compute_sc_stats(adata: ad.AnnData) -> dict:
    n_cells, n_genes = adata.shape
    nnz = adata.X.nnz if hasattr(adata.X, "nnz") else int((adata.X != 0).sum())
    sparsity = 1 - nnz / (n_cells * n_genes) if n_cells * n_genes > 0 else 0

    # Basic QC (do not filter)
    sc.pp.calculate_qc_metrics(adata, inplace=True)

    total_counts = adata.obs["total_counts"]
    n_genes_bc   = adata.obs["n_genes_by_counts"]

    stats = {
        "n_cells":   n_cells,
        "n_genes":   n_genes,
        "sparsity":  float(sparsity),
        "is_dense":  bool(sparsity < 0.5),
        "total_counts": {
            "min":    float(total_counts.min()),
            "median": float(total_counts.median()),
            "mean":   float(total_counts.mean()),
            "max":    float(total_counts.max()),
        },
        "n_genes_per_cell": {
            "min":    float(n_genes_bc.min()),
            "median": float(n_genes_bc.median()),
            "mean":   float(n_genes_bc.mean()),
            "max":    float(n_genes_bc.max()),
        },
        "obs_keys":  list(adata.obs.columns),
        "var_keys":  list(adata.var.columns),
        "layers":    list(adata.layers.keys()),
        "obsm_keys": list(adata.obsm.keys()),
    }

    # Mitochondrial gene percentage
    mt_genes = adata.var_names.str.startswith("MT-")
    if mt_genes.any():
        sc.pp.calculate_qc_metrics(adata, qc_vars=["mt_genes"], inplace=True)
        # Rename for clarity: scanpy uses pct_counts_<varname>
        adata.var["mt"] = mt_genes
        sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)
        stats["pct_mt"] = {
            "mean":   float(adata.obs["pct_counts_mt"].mean()),
            "median": float(adata.obs["pct_counts_mt"].median()),
            "max":    float(adata.obs["pct_counts_mt"].max()),
        }
        stats["has_mt_genes"] = True
    else:
        stats["has_mt_genes"] = False
        stats["pct_mt"] = None

    return stats, adata
```

---

## Plots to generate

```python
import matplotlib.pyplot as plt
import scanpy as sc

def generate_plots(adata: ad.AnnData, stats: dict, out_dir: str) -> dict:
    # Canonical palette — always use these hex values, never named colors
    _PRIMARY  = "#1E5994"   # BLUE_0    — counts vs mito scatter
    _ACCENT   = "#E6905B"   # ORANGE_50 — counts vs genes scatter

    plots = {}
    sc.settings.figdir = out_dir

    # 1. QC violin plots
    qc_keys = ["total_counts", "n_genes_by_counts"]
    if stats["has_mt_genes"]:
        qc_keys.append("pct_counts_mt")

    try:
        sc.pl.violin(adata, qc_keys, jitter=0.4, multi_panel=True, show=False,
                     save="_qc_violins.png")
        plots["qc_violins"] = f"{out_dir}/violin_qc_violins.png"
    except Exception:
        # Fallback: manual violin with matplotlib
        fig, axes = plt.subplots(1, len(qc_keys), figsize=(5 * len(qc_keys), 5))
        for i, key in enumerate(qc_keys):
            axes[i].violinplot(adata.obs[key].dropna(), showmedians=True)
            axes[i].set_title(key)
        fig.tight_layout()
        path = f"{out_dir}/qc_violins.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["qc_violins"] = path

    # 2. Total counts vs pct_mt scatter
    if stats["has_mt_genes"]:
        try:
            sc.pl.scatter(adata, x="total_counts", y="pct_counts_mt", show=False,
                          save="_counts_vs_mt.png")
            plots["counts_vs_mt"] = f"{out_dir}/scatter_counts_vs_mt.png"
        except Exception:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.scatter(adata.obs["total_counts"], adata.obs["pct_counts_mt"],
                       alpha=0.3, s=5, color=_PRIMARY)
            ax.set_xlabel("Total counts")
            ax.set_ylabel("% mitochondrial counts")
            ax.set_title("Total counts vs mitochondrial %")
            fig.tight_layout()
            path = f"{out_dir}/counts_vs_mt.png"
            fig.savefig(path, dpi=150)
            plt.close(fig)
            plots["counts_vs_mt"] = path

    # 3. Total counts vs n_genes scatter
    try:
        sc.pl.scatter(adata, x="total_counts", y="n_genes_by_counts", show=False,
                      save="_counts_vs_genes.png")
        plots["counts_vs_genes"] = f"{out_dir}/scatter_counts_vs_genes.png"
    except Exception:
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(adata.obs["total_counts"], adata.obs["n_genes_by_counts"],
                   alpha=0.3, s=5, color=_ACCENT)
        ax.set_xlabel("Total counts")
        ax.set_ylabel("Genes detected")
        ax.set_title("Total counts vs genes per cell")
        fig.tight_layout()
        path = f"{out_dir}/counts_vs_genes.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["counts_vs_genes"] = path

    return plots
```

---

## Quality flags and warnings

```python
def compute_warnings(stats: dict) -> list[str]:
    warnings = []

    if stats["is_dense"]:
        warnings.append(f"Matrix sparsity {stats['sparsity']:.2f} — unusually dense; verify this is a count matrix (not normalized/log)")

    if stats["total_counts"]["median"] < 500:
        warnings.append(f"Low median total counts per cell: {stats['total_counts']['median']:.0f} — may indicate low-quality cells or under-sequenced library")

    if stats["n_genes_per_cell"]["median"] < 200:
        warnings.append(f"Low median genes per cell: {stats['n_genes_per_cell']['median']:.0f} — filter cells with few genes")

    if stats["has_mt_genes"] and stats["pct_mt"]["mean"] > 20:
        warnings.append(f"High mean mitochondrial %: {stats['pct_mt']['mean']:.1f}% — likely many dying cells; filter cells with pct_mt > 20-25%")

    if not stats["layers"]:
        warnings.append("No layers found in AnnData — X matrix may already be normalized; check if raw counts are available")

    if stats["obs_keys"] == []:
        warnings.append("adata.obs is empty — no cell-level annotations available")

    return warnings
```

---

## Preprocessing recommendations

```python
def recommend_preprocessing(stats: dict) -> list[str]:
    # Suggested thresholds based on QC stats
    min_genes = max(200, int(stats["n_genes_per_cell"]["median"] * 0.2))
    max_genes = int(stats["n_genes_per_cell"]["median"] * 3)
    max_mt    = 20 if stats.get("pct_mt") and stats["pct_mt"]["mean"] < 10 else 25

    return [
        f"1. Filter cells: sc.pp.filter_cells(adata, min_genes={min_genes})",
        f"2. Filter cells: adata = adata[adata.obs.n_genes_by_counts < {max_genes}]",
        f"3. Filter cells: adata = adata[adata.obs.pct_counts_mt < {max_mt}]  # if MT genes present",
        "4. Filter genes: sc.pp.filter_genes(adata, min_cells=3)",
        "5. Normalize: sc.pp.normalize_total(adata, target_sum=1e4)",
        "6. Log transform: sc.pp.log1p(adata)",
        "7. Route to `bio-single-cell-preprocessing` skill for HVG selection and dimensionality reduction",
    ]
```

---

## Output

```python
{
    "profile": { ...updated with shape, sparsity, QC stats, obs/var keys... },
    "plots": {
        "qc_violins":      "path/to/qc_violins.png",
        "counts_vs_mt":    "path/to/counts_vs_mt.png",    # if MT genes present
        "counts_vs_genes": "path/to/counts_vs_genes.png"
    },
    "warnings": [...],
    "preprocessing_recommended": [
        "Filter cells: min_genes=200",
        "Filter cells: max pct_mt=20%",
        "Filter genes: min_cells=3",
        "normalize_total → log1p",
        "Route to bio-single-cell-preprocessing"
    ]
}
```

---

## Production constraints

- **Never** filter cells or genes — report QC metrics and recommend thresholds only
- **Always** run `sc.pp.calculate_qc_metrics` before reporting stats
- **Always** check for mitochondrial genes (`MT-` prefix) and report pct if found
- **Always** report available layers, obs keys, and obsm keys
- **Always** flag if matrix appears non-sparse (may already be normalized)

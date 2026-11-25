---
name: load-h5
description: Load HDF5 / AnnData (.h5, .h5ad) files from single-cell RNA-seq experiments. Extracts obs (cell metadata), var (gene metadata), and X (count matrix). Emits a single-cell Dataset Profile.
compatibility: anndata ≥0.9, pandas ≥1.5, scipy ≥1.10. Works offline.
instruments: Sequencer (NGS) — 10x Genomics Cell Ranger output, scRNAseq pipelines
---

# Load H5 / H5AD (Single-Cell AnnData)

## When to use

File is `.h5ad` (AnnData format) or `.h5` (Cell Ranger HDF5 output).
Sources: 10x Genomics Cell Ranger `filtered_feature_bc_matrix.h5`, Scanpy/Seurat exported `.h5ad` files.

---

## Loading

```python
import anndata as ad
import pandas as pd

def load_h5(path: str) -> tuple[ad.AnnData, dict]:
    try:
        adata = ad.read_h5ad(path)
    except Exception:
        # Try Cell Ranger HDF5 format
        try:
            import scanpy as sc
            adata = sc.read_10x_h5(path)
        except Exception as e:
            raise ValueError(f"LOAD ERROR: could not parse H5/H5AD file — {e}")

    return adata, {
        "parser": "anndata.read_h5ad",
        "shape": adata.shape,           # (n_cells, n_genes)
        "obs_keys": list(adata.obs.columns),
        "var_keys": list(adata.var.columns),
        "layers": list(adata.layers.keys()),
        "obsm_keys": list(adata.obsm.keys()),
        "is_sparse": hasattr(adata.X, "toarray"),
    }
```

---

## Loadability validation

| Condition | `loadability.status` | Error string |
|---|---|---|
| File not found | `fail` | `"LOAD ERROR: file not found — {path}"` |
| Not valid H5/H5AD | `fail` | `"LOAD ERROR: could not parse H5/H5AD file — {detail}"` |
| Zero cells | `fail` | `"LOAD ERROR: AnnData has 0 cells — {path}"` |
| X matrix all zeros | `warn` | `"LOAD WARN: count matrix X is all zeros — may need to load from a layer"` |
| No obs metadata | `warn` | `"LOAD WARN: adata.obs is empty — no cell-level annotations available"` |

---

## Profile fields populated

- `format`: `"h5ad"` or `"h5"`
- `dataset_type`: `"single-cell"`
- `shape`: `{ rows: n_cells, cols: n_genes }`
- `schema`: summary of obs columns + var columns
- `sample_stats`: sparsity of X, total counts per cell distribution
- `split_info`: check `obs` for columns named `split`, `batch`, `sample`, `donor`

---

## Preprocessing defaults

1. **Report shape** — `(n_cells, n_genes)`
2. **Report sparsity** — `1 - nnz / (n_cells * n_genes)`; flag if dense (sparsity < 50%)
3. **Report available layers** — `adata.layers` may contain `counts`, `normalized`, `log1p`; note which to use
4. **Report obs keys** — cell-level metadata: `cell_type`, `batch`, `donor`, `sample`, `leiden`, etc.
5. **Report obsm keys** — embeddings: `X_pca`, `X_umap`, `X_scVI`; flag presence
6. **Compute basic QC metrics** (do not filter):
   - `total_counts` per cell (sum of X row)
   - `n_genes_by_counts` (non-zero genes per cell)
   - Report distribution (min/median/max) for both
7. **Flag mitochondrial gene percentage** if `var` contains gene names — look for `MT-` prefix; high pct (>20%) = low-quality cells

---

## Output

```python
{
    "adata": ad.AnnData,   # full AnnData object
    "profile": {
        "format": "h5ad",
        "dataset_type": "single-cell",
        "shape": { "rows": n_cells, "cols": n_genes },
        "sample_stats": {
            "total_counts": { "min": ..., "median": ..., "max": ... },
            "n_genes": { "min": ..., "median": ..., "max": ... },
            "sparsity": 0.94
        },
        "loadability": { "status": "ok", "parser": "anndata.read_h5ad", "errors": [] },
        "warnings": [...]
    }
}
```

---

## Production constraints

- **Never** filter cells or genes — report QC metrics only
- **Always** report sparsity and available layers
- **Always** flag mitochondrial gene percentage if gene names available

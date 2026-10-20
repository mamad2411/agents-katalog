---
name: analyze-tabular
description: Stage 3 analysis for tabular datasets. Computes per-column stats, correlation matrix, class balance, leakage candidates, and instrument-aware preprocessing recommendations (plate reader, Octet/BLI, Nanodrop, cell counter). Generates distribution and heatmap plots.
compatibility: pandas ≥1.5, matplotlib ≥3.6, seaborn ≥0.12. Works offline.
---

# Analyze Tabular Data

## When to use

Called by `profiling-datasets` Stage 3 when `dataset_type` is `tabular`.
Do not call directly — always receives data + profile from a tabular loader (`load-csv`, `load-parquet`, `load-excel`, `load-jsonl`, `load-asc`).

---

## Input contract

```python
{
    "df": pd.DataFrame,
    "profile": {
        "dataset_type": "tabular",
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

def compute_tabular_stats(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols     = df.select_dtypes(include=["object", "category"]).columns.tolist()

    stats = {
        "n_rows":    len(df),
        "n_cols":    len(df.columns),
        "n_numeric": len(numeric_cols),
        "n_categorical": len(cat_cols),
        "columns": {},
    }

    for col in df.columns:
        entry = {
            "dtype":       str(df[col].dtype),
            "null_count":  int(df[col].isna().sum()),
            "null_pct":    float(df[col].isna().mean() * 100),
            "unique_count": int(df[col].nunique()),
        }
        if col in numeric_cols:
            entry.update({
                "min":    float(df[col].min()),
                "median": float(df[col].median()),
                "mean":   float(df[col].mean()),
                "max":    float(df[col].max()),
                "std":    float(df[col].std()),
            })
        elif col in cat_cols:
            top = df[col].value_counts().head(5)
            entry["top_values"] = top.to_dict()
        stats["columns"][col] = entry

    return stats


def detect_leakage_candidates(df: pd.DataFrame) -> list[str]:
    candidates = []
    for col in df.columns:
        # ID columns
        if any(kw in col.lower() for kw in ("id", "uid", "uuid", "index", "key")):
            candidates.append(f"{col} (likely ID column — exclude from features)")
        # Near-constant
        if df[col].nunique() <= 2 and len(df) > 100:
            candidates.append(f"{col} (near-constant: {df[col].nunique()} unique values)")
        # High-cardinality string
        if df[col].dtype == object and df[col].nunique() > len(df) * 0.9:
            candidates.append(f"{col} (high-cardinality string — likely free text or ID)")
    return candidates


def detect_instrument_context(df: pd.DataFrame) -> str:
    cols_lower = [c.lower() for c in df.columns]
    # Plate reader: well-plate layout
    if any(c in cols_lower for c in ("well", "plate", "row", "col", "column")) or \
       any(bool(__import__("re").match(r"^[a-h][0-9]{1,2}$", c)) for c in cols_lower[:20]):
        return "plate_reader"
    # Octet / BLI
    if any(c in cols_lower for c in ("wavelength_shift", "binding", "nm", "response", "association", "dissociation")):
        return "octet_bli"
    # Nanodrop / Qubit
    if any(c in cols_lower for c in ("a260", "a280", "concentration", "ng_ul", "ng/ul", "purity")):
        return "nanodrop_qubit"
    # Cell counter
    if any(c in cols_lower for c in ("viability", "live_cells", "dead_cells", "cell_count", "trypan")):
        return "cell_counter"
    # FPLC / AKTA
    if any(c in cols_lower for c in ("uv_mau", "conductivity", "pressure", "volume_ml", "retention_volume")):
        return "fplc"
    return "generic"
```

---

## Plots to generate

```python
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots(df: pd.DataFrame, out_dir: str) -> dict:
    from matplotlib.colors import LinearSegmentedColormap
    # Canonical palette — always use these hex values, never named colors
    _PRIMARY  = "#1E5994"   # BLUE_0    — main bars / histograms
    _ACCENT   = "#E6905B"   # ORANGE_50 — missing-value bars
    _CMAP_DIV = LinearSegmentedColormap.from_list(
        "capo_div", ["#1E5994", "#FFFFFF", "#9B3208"]
    )  # diverging: BLUE_0 ↔ ORANGE_0 for correlation heatmap

    plots = {}
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # 0. Categorical column value distributions — always generated when cat cols exist
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        # Prioritise label-like column names; fall back to first N by column order
        label_keywords = ("label", "target", "class", "outcome", "y", "category", "group", "type")
        priority = [c for c in cat_cols if any(kw in c.lower() for kw in label_keywords)]
        rest     = [c for c in cat_cols if c not in priority]
        ordered  = (priority + rest)[:6]   # at most 6 subplots

        ncols = min(len(ordered), 3)
        nrows = (len(ordered) + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols,
                                 figsize=(5 * ncols, 4 * nrows),
                                 squeeze=False)
        for idx, col in enumerate(ordered):
            ax = axes[idx // ncols][idx % ncols]
            top = df[col].value_counts().head(15)
            top.plot.barh(ax=ax, color=_PRIMARY, alpha=0.85)
            ax.set_title(col, fontsize=10)
            ax.set_xlabel("Count")
            ax.invert_yaxis()
        for idx in range(len(ordered), nrows * ncols):
            axes[idx // ncols][idx % ncols].set_visible(False)
        fig.suptitle("Categorical column distributions (top 15 values each)", y=1.01)
        fig.tight_layout()
        path = f"{out_dir}/categorical_distributions.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        plots["categorical_distributions"] = path

    # 1. Missing values heatmap (first 50 cols)
    if df.isnull().any().any():
        fig, ax = plt.subplots(figsize=(min(len(df.columns), 20), 4))
        null_pct = df.isnull().mean().iloc[:50]
        null_pct.sort_values(ascending=False).plot.bar(ax=ax, color=_ACCENT)
        ax.set_ylabel("Missing fraction")
        ax.set_title("Missing values per column")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        path = f"{out_dir}/missing_values.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["missing_values"] = path

    # 2. Numeric column distributions
    if numeric_cols:
        n = min(len(numeric_cols), 12)
        ncols = min(n, 4)
        nrows = (n + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
        axes = axes.flatten() if nrows * ncols > 1 else [axes]
        for i, col in enumerate(numeric_cols[:n]):
            axes[i].hist(df[col].dropna(), bins=30, color=_PRIMARY, alpha=0.8)
            axes[i].set_title(col, fontsize=9)
            axes[i].set_ylabel("Count")
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        fig.tight_layout()
        path = f"{out_dir}/numeric_distributions.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["numeric_distributions"] = path

    # 3. Correlation heatmap (5+ numeric cols)
    if len(numeric_cols) >= 5:
        corr = df[numeric_cols[:20]].corr()
        fig, ax = plt.subplots(figsize=(min(len(numeric_cols), 12), min(len(numeric_cols), 10)))
        sns.heatmap(corr, annot=len(numeric_cols) <= 12, fmt=".2f", cmap=_CMAP_DIV,
                    center=0, ax=ax, square=True, linewidths=0.5)
        ax.set_title("Feature correlation matrix")
        fig.tight_layout()
        path = f"{out_dir}/correlation_heatmap.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["correlation_heatmap"] = path

    return plots
```

---

## Quality flags and warnings

```python
def compute_warnings(df: pd.DataFrame, stats: dict, leakage: list[str], instrument: str) -> list[str]:
    warnings = []

    # High null rate
    for col, col_stats in stats["columns"].items():
        if col_stats["null_pct"] > 20:
            warnings.append(f"Column '{col}': {col_stats['null_pct']:.1f}% missing — impute or drop before modeling")

    # Leakage candidates
    if leakage:
        warnings.append(f"Potential leakage candidates: {leakage}")

    # Instrument-specific warnings
    if instrument == "plate_reader":
        warnings.append("Plate reader layout detected — wells may need blank subtraction and positive control normalization before analysis")
    elif instrument == "octet_bli":
        warnings.append("Octet/BLI data detected — reference subtraction and curve fitting (Kd) required before ML use")
    elif instrument == "nanodrop_qubit":
        warnings.append("Nanodrop/Qubit data — concentration and purity report only; typically not used for ML directly")
    elif instrument == "cell_counter":
        warnings.append("Cell counter data — viability report only; typically not used for ML directly")

    return warnings
```

---

## Preprocessing recommendations (instrument-aware)

```python
def recommend_preprocessing(df: pd.DataFrame, stats: dict, instrument: str) -> list[str]:
    steps = []

    if instrument == "plate_reader":
        steps += [
            "1. Identify blank wells (typically column 12 or row H) and subtract background",
            "2. Normalize each plate by positive control wells",
            "3. Average technical replicates within plate",
            "4. Melt well-plate layout to long format: pd.melt(df, id_vars=['plate'], value_vars=well_cols)",
            "5. Route to `numerical-data-processing` for split and scaling",
        ]
    elif instrument == "octet_bli":
        steps += [
            "1. Subtract reference channel from active channel (double referencing)",
            "2. Fit association/dissociation curves to extract koff, kon, Kd",
            "3. Use Kd values as the ML label, not raw binding curves",
        ]
    elif instrument in ("nanodrop_qubit", "cell_counter", "fplc"):
        steps += [
            f"NOTE: {instrument} data is typically a QC/measurement report, not an ML dataset",
            "Consider whether ML modeling is the right approach for this data type",
        ]
    else:
        steps += [
            "1. Create train/val/test split first (recommended 80/10/10) — before any preprocessing",
            "2. Impute missing values on train only (median for numeric, mode for categorical)",
            "3. Scale numeric features on train only (StandardScaler or RobustScaler)",
            "4. Encode categorical features on train only (OrdinalEncoder / OneHotEncoder)",
            "5. Route to `numerical-data-processing` skill",
        ]

    return steps
```

---

## Output

```python
{
    "profile": { ...updated with per-column stats, schema, sample_stats... },
    "plots": {
        "categorical_distributions": "path/to/categorical_distributions.png",  # when cat cols present
        "missing_values":            "path/to/missing_values.png",              # when nulls present
        "numeric_distributions":     "path/to/numeric_distributions.png",       # when numeric cols present
        "correlation_heatmap":       "path/to/correlation_heatmap.png"          # when ≥5 numeric cols
    },
    "warnings": [...],
    "preprocessing_recommended": [...]
}
```

---

## Production constraints

- **Always** generate `categorical_distributions` when categorical columns are present — unconditional
- **Always** detect instrument context before recommending preprocessing
- **Never** impute, scale, or encode — report and recommend only
- **Always** check for leakage candidates (ID columns, near-constant, high-cardinality strings)
- **Never** fit any transformer (imputer, scaler) on the full dataset — always recommend train-only fitting

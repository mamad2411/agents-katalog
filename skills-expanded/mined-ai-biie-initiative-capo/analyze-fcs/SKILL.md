---
name: analyze-fcs
description: Stage 3 analysis for flow_cytometry (FCS) datasets. Computes per-channel distributions, pct negative events, FSC vs SSC scatter overview, compensation status check. Recommends arcsinh transform and manual gating pipeline.
compatibility: pandas ≥1.5, matplotlib ≥3.6. Works offline.
---

# Analyze FCS (Flow Cytometry)

## When to use

Called by `profiling-datasets` Stage 3 when `dataset_type` is `flow_cytometry`.
Do not call directly — always receives data + profile from `load-fcs`.

---

## Input contract

```python
{
    "df": pd.DataFrame,   # columns: FSC-A, SSC-A, FITC-A, PE-A, ... (per-cell events)
    "profile": {
        "dataset_type": "flow_cytometry",
        "loadability": { "status": "ok" },
        ...
    },
    "meta": {             # from fcsparser
        "has_compensation": True | False,
        "cytometer": "BD LSRFortessa",
        "fcs_version": "3.0",
        "num_events": 50000,
    }
}
```

---

## Statistics to compute

```python
import pandas as pd
import numpy as np

def compute_fcs_stats(df: pd.DataFrame, meta: dict) -> dict:
    scatter_cols = [c for c in df.columns if c.startswith(("FSC", "SSC"))]
    fluor_cols   = [c for c in df.columns if c not in scatter_cols]

    stats = {
        "n_events":          len(df),
        "n_channels":        len(df.columns),
        "n_scatter_channels": len(scatter_cols),
        "n_fluor_channels":  len(fluor_cols),
        "has_compensation":  meta.get("has_compensation", False),
        "cytometer":         meta.get("cytometer", "unknown"),
        "fcs_version":       meta.get("fcs_version", "unknown"),
        "channels": {},
    }

    for col in df.columns:
        col_data = df[col].dropna()
        stats["channels"][col] = {
            "min":       float(col_data.min()),
            "median":    float(col_data.median()),
            "mean":      float(col_data.mean()),
            "max":       float(col_data.max()),
            "std":       float(col_data.std()),
            "pct_negative": float((col_data < 0).mean() * 100) if col in fluor_cols else None,
        }

    return stats
```

---

## Plots to generate

```python
import matplotlib.pyplot as plt
import numpy as np

def generate_plots(df: pd.DataFrame, out_dir: str) -> dict:
    # Canonical palette — always use these hex values, never named colors
    _PRIMARY  = "#1E5994"   # BLUE_0    — FSC/SSC scatter, box plots
    _ACCENT   = "#E6905B"   # ORANGE_50 — negative event rate bars

    plots = {}
    scatter_cols = [c for c in df.columns if c.startswith(("FSC", "SSC"))]
    fluor_cols   = [c for c in df.columns if c not in scatter_cols]

    # 1. FSC-A vs SSC-A scatter (first 10k events for speed)
    fsc = "FSC-A" if "FSC-A" in df.columns else (scatter_cols[0] if scatter_cols else None)
    ssc = "SSC-A" if "SSC-A" in df.columns else (scatter_cols[1] if len(scatter_cols) > 1 else None)

    if fsc and ssc:
        sample = df[[fsc, ssc]].dropna().iloc[:10_000]
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(sample[fsc], sample[ssc], alpha=0.1, s=1, color=_PRIMARY)
        ax.set_xlabel(fsc)
        ax.set_ylabel(ssc)
        ax.set_title(f"{fsc} vs {ssc} — cell population overview (first 10k events)")
        fig.tight_layout()
        path = f"{out_dir}/fsc_ssc_scatter.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["fsc_ssc_scatter"] = path

    # 2. Fluorescence channel box plots
    if fluor_cols:
        n = min(len(fluor_cols), 16)
        fig, ax = plt.subplots(figsize=(max(10, n * 0.8), 5))
        df[fluor_cols[:n]].plot.box(ax=ax, rot=45, grid=True)
        ax.set_title("Fluorescence channel distributions")
        ax.set_ylabel("Signal intensity")
        fig.tight_layout()
        path = f"{out_dir}/fluor_channels.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["fluor_channels"] = path

    # 3. Per-channel negative event rate bar chart (post-compensation artifact)
    neg_rates = {}
    for col in fluor_cols:
        neg_rates[col] = float((df[col] < 0).mean() * 100)

    if any(v > 0 for v in neg_rates.values()):
        fig, ax = plt.subplots(figsize=(max(8, len(fluor_cols)), 4))
        pd.Series(neg_rates).plot.bar(ax=ax, color=_ACCENT, alpha=0.8)
        ax.set_ylabel("% negative events")
        ax.set_title("Negative event rate per fluorescence channel (post-compensation artifact)")
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        path = f"{out_dir}/negative_events.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        plots["negative_events"] = path

    return plots
```

---

## Quality flags and warnings

```python
def compute_warnings(stats: dict) -> list[str]:
    warnings = []

    if not stats["has_compensation"]:
        warnings.append("No compensation matrix found in FCS file — fluorescence channels may show spillover artifacts")

    high_neg = [ch for ch, s in stats["channels"].items()
                if s.get("pct_negative") is not None and s["pct_negative"] > 10]
    if high_neg:
        warnings.append(f"High negative event rate (>10%) in channels: {high_neg} — may need re-compensation or gate adjustment")

    if stats["n_events"] < 5000:
        warnings.append(f"Low event count: {stats['n_events']} — flow cytometry experiments typically need ≥10k events for reliable gating")

    return warnings
```

---

## Preprocessing recommendations

```python
def recommend_preprocessing(stats: dict) -> list[str]:
    steps = []

    if not stats["has_compensation"]:
        steps.append("1. Apply compensation matrix: obtain spillover matrix from instrument export and apply manually")
    else:
        steps.append("1. Compensation already present — verify with single-stain controls")

    steps += [
        "2. Apply arcsinh transform to fluorescence channels: df[fluor_cols] = np.arcsinh(df[fluor_cols] / 5)  # cofactor=5",
        "3. Leave scatter channels (FSC, SSC) untransformed",
        "4. Gate population of interest in FlowJo, Python (FlowCal), or R (flowCore/openCyto)",
        "5. Export gated population for downstream analysis (ML classification, clustering)",
    ]

    return steps
```

---

## Output

```python
{
    "profile": { ...updated with per-channel stats, n_events... },
    "plots": {
        "fsc_ssc_scatter": "path/to/fsc_ssc_scatter.png",
        "fluor_channels":  "path/to/fluor_channels.png",
        "negative_events": "path/to/negative_events.png"
    },
    "warnings": [...],
    "preprocessing_recommended": [
        "Apply compensation matrix",
        "arcsinh(x/5) transform fluorescence channels",
        "Gate population of interest in FlowJo / FlowCal"
    ]
}
```

---

## Production constraints

- **Always** distinguish scatter (FSC/SSC) from fluorescence channels in stats and plots
- **Always** check for compensation matrix and warn if missing
- **Never** apply transforms — recommend only
- **Always** include arcsinh transform recommendation with cofactor=5
- **Always** return at least one plot — if both `fsc_ssc_scatter` and `fluor_channels` would
  be skipped (degenerate file with < 2 scatter channels and no fluorescence channels), generate
  a channel-stats bar chart of mean intensity per channel as a fallback

---
name: clustering
description: Cluster protein sequences or embeddings using density-based, centroid-based, or hierarchical methods. Evaluates clusters biologically (species enrichment, label composition, mutation patterns) and generates cluster-aware train/val/test splits to prevent homology leakage. Always clusters in analysis space — never on raw 2D t-SNE output.
user-invokable: true
compatibility: scikit-learn ≥1.3, hdbscan ≥0.8 (or scikit-learn ≥1.3 HDBSCAN), numpy ≥1.23, pandas ≥1.5, matplotlib ≥3.6. Optional: mmseqs2 or CD-HIT for sequence-identity clustering.
---

# Clustering

> **Core rule:** Cluster in the original feature space or a compressed analysis space (PCA/SVD). Never cluster directly on t-SNE output. Use `skills/dimensionality-reduction/` for visualization before or after clustering.

---

## When to use

- Finding biologically coherent groups in protein sequence or embedding space
- Creating cluster-aware train/val/test splits to prevent homology leakage
- Profiling sequence families by species enrichment, binding label, or mutation patterns
- Supplementing or replacing sequence-identity clustering (mmseqs2/CD-HIT) with embedding-based grouping

## When not to use

| Want… | Use instead |
|---|---|
| Visualize sequence space (2D plots) | `skills/dimensionality-reduction/` |
| Homology-aware splits via sequence identity | `split_utils.py` in `protein-sequence-data-processing` |
| Load / profile data | `profiling-datasets` |
| Fine-tune a PLM | `huggingface-jobs` |

---

## Algorithm decision table

| Method | Use when | Strengths | Weaknesses |
|---|---|---|---|
| `HDBSCAN` | Density varies, outliers matter | Noise labeling, no K required, varying density | Parameter-sensitive; may produce many noise points |
| `MiniBatchKMeans` | Large dataset, approximate K known | Fast, scalable | Assumes compact groups; requires K |
| `KMeans` | Smaller dataset, K known | Fast, strong baseline | Spherical assumption; all points assigned |
| `DBSCAN` | Uniform density, arbitrary shapes | No K, explicit noise | Fails when density varies |
| `AgglomerativeClustering` | Hierarchy needed | Nested grouping | Slow on full data; use on centroids/subsamples |
| `GaussianMixture` | Soft assignments, ambiguous boundaries | Probabilistic membership | Can overfit; covariance assumptions |

**Default recommendation:** `HDBSCAN` → `MiniBatchKMeans` fallback for very large sets.

---

## Configuration

```python
from scripts.config_schema import ClusterConfig
cfg = ClusterConfig(
    input_path        = "outputs/dimred/pre_reduced.npy",   # PCA/SVD matrix from dim-red skill
    metadata_path     = "data/sequences.csv",
    id_col            = "id",
    seq_col           = "sequence",
    metadata_cols     = ["species", "binding_label"],
    pre_reducer       = "none",          # pca | truncated_svd | none | umap_intermediate
    pre_reducer_n     = 50,
    algorithm         = "hdbscan",       # hdbscan | kmeans | minibatch_kmeans | dbscan | agglomerative | gmm
    algorithm_params  = {"min_cluster_size": 50, "min_samples": 10},
    split_strategy    = "whole_cluster", # whole_cluster | stratified_cluster | none
    split_ratios      = (0.8, 0.1, 0.1),
    seed              = 42,
    output_dir        = "outputs/clustering/",
)
```

---

## Workflow

Import from `scripts/`. Do not re-implement inline.

### Step 1 — Load data and representation
```python
from scripts.io_utils import load_array, load_dataframe
X  = load_array(cfg.input_path)         # pre-reduced matrix from dim-red skill
df = load_dataframe(cfg.metadata_path)
```

### Step 2 — Pre-reduce for clustering (if input is not already reduced)
```python
from scripts.precluster_reduction import reduce_for_clustering
X_cluster = reduce_for_clustering(X, cfg)
```

### Step 3 — Fit clusterer
```python
from scripts.clusterers import fit_clusterer
labels, model = fit_clusterer(X_cluster, cfg)
df["cluster"] = labels
```

### Step 4 — Tune parameters (optional)
```python
from scripts.tune_clusterers import sweep_k, sweep_hdbscan
results = sweep_k(X_cluster, k_range=range(5, 50, 5), seed=cfg.seed)
# or: results = sweep_hdbscan(X_cluster, min_sizes=[10, 25, 50, 100, 200])
```

### Step 5 — Evaluate clustering
```python
from scripts.evaluate_clusters import compute_cluster_metrics
metrics = compute_cluster_metrics(X_cluster, labels, seed=cfg.seed)
# → silhouette, davies_bouldin, calinski_harabasz, n_clusters, noise_frac, size_stats, warnings
```

### Step 6 — Biological profiling
```python
from scripts.cluster_profiles import profile_clusters
profiles = profile_clusters(df, cluster_col="cluster", label_cols=cfg.metadata_cols,
                            seq_col=cfg.seq_col, out_dir=f"{cfg.output_dir}/cluster_profiles/")
# → composition tables, species enrichment, binding label counts, mutation heatmap
```

### Step 7 — Cluster-aware splits
```python
from scripts.cluster_splits import assign_cluster_splits, check_cluster_leakage
df = assign_cluster_splits(df, cluster_col="cluster", ratios=cfg.split_ratios, seed=cfg.seed)
leakage = check_cluster_leakage(df, seq_col=cfg.seq_col, cluster_col="cluster")
```

### Step 8 — Plot (requires 2D coords from dimensionality-reduction skill)
```python
from scripts.plotting import plot_cluster_map, plot_cluster_profiles
coords = pd.read_parquet("outputs/dimred/reduced_coordinates.parquet")
plot_cluster_map(coords, df, cluster_col="cluster",
                 out_path=f"{cfg.output_dir}/cluster_plots/cluster_map.png")
for col in cfg.metadata_cols:
    plot_cluster_profiles(profiles, label_col=col,
                          out_path=f"{cfg.output_dir}/cluster_plots/profiles_{col}.png")
```

### Step 9 — Export
```python
from scripts.export_outputs import save_clustering
save_clustering(df, profiles, metrics, cfg)
```

---

## Biological validation checklist

Before accepting a clustering result:
- [ ] No single cluster ≥ 80% of data (check `cluster_size_stats.largest_frac`)
- [ ] Noise fraction (HDBSCAN label `-1`) < 20% unless biologically expected
- [ ] Species composition is enriched per cluster, not uniformly mixed
- [ ] Binding labels are not randomly mixed (unless biology suggests overlap)
- [ ] `check_cluster_leakage()` returns zero sequence overlap across splits

---

## Output contract

```
outputs/clustering/
├── cluster_assignments.csv     # id, cluster, split + all metadata_cols
├── cluster_metrics.json        # silhouette, davies_bouldin, calinski_harabasz, n_clusters, noise_frac
├── split_assignments.csv       # id, split (train / val / test)
├── run_config.yaml
├── cluster_profiles/
│   ├── composition_<col>.csv   # per-cluster label counts
│   ├── enrichment_<col>.csv    # per-cluster label fractions
│   ├── cluster_sizes.csv
│   └── mutation_heatmap.png
└── cluster_plots/
    ├── cluster_map.png / .pdf
    └── profiles_<col>.png / .pdf
```

---

## Hard constraints

- **Never** cluster directly on t-SNE 2D output — use PCA/SVD analysis space
- **Never** use UMAP 2D as the default clustering space — enable `umap_intermediate` explicitly
- **Never** discard noise points (`label == -1`) silently — report count and fraction
- **Always** run `compute_cluster_metrics()` and report silhouette
- **Always** report `cluster_size_stats` — flag if any cluster ≥ 80% of non-noise data
- **Always** run biological profiling when metadata columns are available
- **Always** use cluster-aware splits — never random row splits on clustered data
- **Always** run `check_cluster_leakage()` and report result
- **Always** save `run_config.yaml` for reproducibility

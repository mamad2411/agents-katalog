---
name: ml-cluster
description: "Find natural groups in data and label them with plain-language descriptions. Use when the user wants to segment customers, discover topics, group documents, or says 'cluster this', 'find segments', 'group these', or 'what topics are in this data'."
argument-hint: "<file-path> [objective in natural language]"
---

# Cluster and Label Data

Find natural groups in a dataset using unsupervised clustering, then label each group with a plain-language description. No ML expertise required — the algorithm selection, parameter tuning, and result interpretation are all handled automatically.

## Input

- **File path** (required): CSV, JSON, Parquet file, or directory of text files
- **Objective** (optional): Natural language description of what to find (e.g., "find customer segments", "group these documents by topic")

If no objective is provided, discover the most natural groupings in the data.

## Workflow

### Phase 1: Environment Check and Data Loading

Check required packages:

```bash
uv run python3 -c "import pandas; import sklearn; print('Core packages available')"
```

Use `uv run python3` for all Python calls in this skill.

If pandas or sklearn are missing, report install instructions and stop.

Check optional packages (non-blocking):

```bash
uv run python3 -c "
try: import umap; print('umap: available')
except ImportError: print('umap: not available (will skip dimensionality reduction)')
try: import hdbscan; print('hdbscan: available')
except ImportError: print('hdbscan: not available (will use sklearn KMeans instead)')
"
```

Load and profile the data using the same approach as `ml-explore` Phase 2. Identify:
- Whether the data is primarily text, numeric, or mixed
- Number of rows and columns
- Any quality issues that could affect clustering

Write the loaded data profile to checkpoint: `.ml-checkpoints/ml-cluster/<timestamp>/profile.json`

### Phase 2: Generate Representations

**First, check the shared embedding cache** (see AGENTS.md "Embedding Cache" section). If a cached representation exists for this file, load it and skip to Phase 3.

Choose representation strategy based on data type:

**For text data:**

Detect embedding provider using the cascade defined in AGENTS.md:

1. **sentence-transformers** (if installed): Use `all-MiniLM-L6-v2` model. Process locally. For datasets over 1000 rows, process in batches of 500 and report progress.
2. **TF-IDF fallback**: Use `sklearn.feature_extraction.text.TfidfVectorizer` with `max_features=5000`. Report to the user: "Using basic text analysis (TF-IDF). For higher quality results, install sentence-transformers."

**For numeric data:**

Use the numeric columns directly. Apply `sklearn.preprocessing.StandardScaler` to normalize features.

**For mixed data:**

Embed text columns and concatenate with scaled numeric features.

Write representations to the shared embedding cache (see AGENTS.md) and to the skill checkpoint: `.ml-checkpoints/ml-cluster/<timestamp>/representations.npy`

### Phase 3: Dimensionality Reduction (Conditional)

**Skip UMAP entirely when:**
- The representation has 50 or fewer dimensions (already low-dimensional — UMAP adds cost with no benefit)
- The data is purely numeric with no text embedding (scaled numeric features are already suitable for clustering/anomaly detection)
- UMAP is not installed

**Use UMAP only when:**
- UMAP is available AND the representation has more than 50 dimensions (typically from text embeddings like sentence-transformers at 384d or TF-IDF at up to 5000d)

```python
import umap
reducer = umap.UMAP(n_components=min(50, n_features), random_state=42)
reduced = reducer.fit_transform(representations)
```

Run this with `timeout: 600000` — UMAP can be slow on large datasets.

Write reduced representations to checkpoint: `.ml-checkpoints/ml-cluster/<timestamp>/reduced.npy`

### Phase 4: Clustering

Choose algorithm based on available packages:

**If HDBSCAN is available (preferred):**

```python
import hdbscan
min_size = max(5, len(data) // 50)  # heuristic: at least 2% of data per cluster
clusterer = hdbscan.HDBSCAN(min_cluster_size=min_size, min_samples=3)
labels = clusterer.fit_predict(reduced_or_raw)
```

HDBSCAN automatically determines the number of clusters and identifies noise points (label -1).

**If HDBSCAN is not available, use KMeans:**

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Try k from 2 to min(10, sqrt(n_samples))
best_k, best_score = 2, -1
for k in range(2, min(11, int(len(data)**0.5) + 1)):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(reduced_or_raw)
    score = silhouette_score(reduced_or_raw, labels, sample_size=min(5000, len(data)))
    if score > best_score:
        best_k, best_score = k, score
```

**Evaluate clustering quality:**

Compute silhouette score. If the score is below 0.1, report:
> "The data doesn't show distinct groups. This could mean the items are very similar to each other, or that the natural groupings don't align with the features available. Consider exploring the data with `ml-explore` first to understand its structure."

Write cluster labels to checkpoint: `.ml-checkpoints/ml-cluster/<timestamp>/labels.json`

### Phase 5: Label and Describe Clusters

For each cluster:

1. Count the number of items
2. Sample up to 10 representative items (closest to cluster center or random sample)
3. If numeric: compute the mean feature values to identify what distinguishes this cluster
4. Format the representatives and distinguishing features as context

Then use the LLM to generate plain-language labels and descriptions. For each cluster, provide the sampled items and ask for:
- A short label (2-5 words)
- A one-sentence description
- Key distinguishing characteristics

If the user provided an objective, frame the labels in that context (e.g., "Budget-Conscious Shoppers" for customer segmentation, "Technical Support Issues" for ticket categorization).

### Phase 6: Present Results

Format the output as:

```
## Clustering Results: [filename]

**Groups found:** [N]
**Method:** [HDBSCAN/KMeans] [with UMAP reduction / on raw features]
**Representations:** [sentence-transformers / TF-IDF / numeric features]
**Quality:** [Good/Fair/Poor] (silhouette score: [X])

### Group 1: [Label] ([N] items, [X]% of data)
[One-sentence description]

**Typical examples:**
- [Example 1 summary]
- [Example 2 summary]
- [Example 3 summary]

**What makes this group distinctive:**
- [Key characteristic 1]
- [Key characteristic 2]

### Group 2: [Label] ([N] items, [X]% of data)
...

[If HDBSCAN found noise points:]
### Uncategorized ([N] items, [X]% of data)
These items didn't fit clearly into any group. They may be unique or transitional between groups.

## Suggested Next Steps
- [Contextual suggestions based on results]
```

All descriptions must use plain language. Avoid terms like "centroid", "silhouette score", "dimensionality reduction" in user-facing output. The technical details (method, quality score) are included for reproducibility but explained simply.

## Checkpointing and Resume

On start, check for recent checkpoints (less than 24 hours old) in `.ml-checkpoints/ml-cluster/`:
- If found, ask: "Found results from a previous clustering run. Resume from where it left off, or start fresh?"
- If resuming, load the latest checkpoint and continue from the next phase

Each phase writes its output to the checkpoint directory before proceeding.

## Error Handling

- **No sentence-transformers installed:** Fall back to TF-IDF with a quality note
- **UMAP not installed:** Skip dimensionality reduction, cluster on raw features
- **HDBSCAN not installed:** Use KMeans instead
- **All items in one cluster:** Report "the data appears very homogeneous" and suggest exploring with `ml-explore`
- **Too few items (<5):** Report "need at least 5 items for meaningful clustering" and suggest manual review
- **Embedding API failure mid-batch:** Save completed embeddings to checkpoint, report the error, suggest retrying

## Reference Files

- `references/clustering-guide.md` — Plain-language explanation of how clustering works

---
name: rapids-first
description: >-
  Use only when the user explicitly mentions "rapids-first" or "RAPIDS first", to prefer the RAPIDS GPU stack (cudf, cuml, cupy, cupyx) and its zero-code accelerators over pandas, scikit-learn, numpy and scipy when writing Python data-science, ML, ETL or numerical code.
---

# RAPIDS-first

## When to Enable

Enable this skill if and only if the user's request explicitly contains `rapids-first` (or the synonymous wording "RAPIDS first"). Do not apply it proactively in other scenarios, to avoid modifying code outside the user's expectations.

This skill covers four packages: `cupy`, `cupyx`, `cudf`, `cuml`.

## Applicable Scenarios

Once rapids-first is enabled, **all "writing Python code" subtasks** are handled according to the RAPIDS-first principle, not limited to rewriting existing CPU code:

1. **Rewriting existing CPU code**: replace numpy / pandas / sklearn / scipy / umap-learn / hdbscan / faiss calls with the corresponding RAPIDS APIs.
2. **Adding new features / implementing new algorithms**: when writing implementations from scratch, prefer RAPIDS APIs as the foundation rather than numpy / scipy / sklearn. Example: for matrix decomposition → directly choose `cuml.decomposition` over `sklearn.decomposition`; for nearest neighbors → directly choose `cuml.neighbors.NearestNeighbors` over `faiss` / `sklearn.neighbors`; for sparse iterative solves → directly choose `cupyx.scipy.sparse.linalg` over `scipy.sparse.linalg`.
3. **Creating new scripts (ETL / training / inference / batch processing)**: use `cudf.read_csv` / `cudf.read_parquet` / `cudf.read_orc` / `cudf.read_json` for data loading, `cupy` for matrix computation, `cudf` + `cuml.preprocessing` for feature engineering, `cuml` for model training and prediction, `cupyx.scipy.ndimage` / `cupyx.scipy.signal` for image-style filtering and signal processing.
4. **Adding new tests**: use RAPIDS as much as possible for test data generation and assertion comparison (`cudf.testing` / `cuml.testing` / `cupy.testing`, plus `cuml.datasets.make_blobs` and `cupy.random` for synthetic data); let numpy / pandas appear only for RAPIDS↔CPU numerical comparisons, with a one-shot conversion at the boundary.
5. **Fixing bugs**: even when just fixing a single numpy function call, if a suitable RAPIDS equivalent exists in the context, replace it in passing.

In short: after enabling this skill, "think first how to do it with RAPIDS" takes priority over "think first how to do it with numpy / pandas / sklearn". Only fall back to the CPU path when the RAPIDS stack truly has no corresponding implementation.

## Three Core Principles

1. **Zero-code acceleration first**: this stack ships two monkey-patch accelerators. `cudf.pandas` covers pandas, and `cuml.accel` covers scikit-learn and umap-learn (plus the standalone hdbscan package when the user has installed it). Both let existing CPU code run on GPU without changing any imports. Use zero-code whenever possible — especially in the "rewriting existing CPU code" scenario.
2. **Avoid redundant CPU↔GPU conversions**: once data is on GPU, keep it on GPU as much as possible, minimizing calls like `.to_pandas()` / `.to_numpy()` / `.get()` that trigger device synchronization and copying; only do a one-shot downlink at the pipeline endpoint or at necessary output/visualization boundaries. Mixing `cupy.ndarray` with `numpy.ndarray` (or `cudf.DataFrame` with `pandas.DataFrame`) triggers implicit synchronization and should be proactively eliminated.
3. **Precise API targeting**: this skill directory ships a complete API index `apis/<pkg>.txt` for each RAPIDS package, with each line formatted as "full path(signature) - first line of docstring". A single `ripgrep` search retrieves both the call syntax and purpose, **avoiding writing signatures from memory** (cuML and sklearn often differ in parameter order, default values, `output_type`, etc.).

## Directory Structure

```
${SKILL_DIR}/
├── SKILL.md                       # This file
├── cpu-rapids-cuda-mapping.tsv    # Index of CPU library → RAPIDS package (TSV)
├── fetch_rapids_apis.py           # Script that (re-)generates apis/<pkg>.txt
└── apis/                          # One API index file per package
    ├── cupy.txt                   # CuPy (replaces numpy)
    ├── cupyx.txt                  # CuPy's SciPy mirror and extensions (replaces scipy)
    ├── cudf.txt                   # cuDF (replaces pandas)
    └── cuml.txt                   # cuML (replaces scikit-learn / umap-learn / hdbscan; statsmodels.tsa via the deprecated cuml.tsa)
```

`${SKILL_DIR}` is the directory containing this `SKILL.md` — typically `~/.claude/skills/rapids-first` (user-level) or `.claude/skills/rapids-first` (project-level), with `.claude` replaced by `.agents` for Codex. Export it once before the first `rg`:

```bash
SKILL_DIR=$HOME/.claude/skills/rapids-first  # adjust to your install
```

## Standard Workflow

### Step 1: Identify the CPU library to replace/select

- **Rewrite scenario**: scan the user's code to find the imports to accelerate (`import numpy as np`, `import pandas as pd`, `from sklearn.cluster import KMeans`, `import scipy.ndimage`, `from scipy import sparse`, `import faiss / hnswlib / annoy / umap / hdbscan`, etc.).
- **New code scenario**: against the functional requirements, **first mentally write out "if using a CPU library, which one would I use"** (pandas? sklearn? scipy?), then follow the steps below to convert it to RAPIDS.

### Step 2: Use ripgrep on mapping.tsv to locate the RAPIDS package

`cpu-rapids-cuda-mapping.tsv` fields:

```
cpu_module  rapids_target  zero_code  notes
```

For an exact top-level package lookup use `^pkg\t`; for fuzzy submodule lookup use plain grep:

```
$ rg -P '^pandas\t' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
pandas	cudf	cudf.pandas	zero-code via `python -m cudf.pandas script.py` or first-cell `%load_ext cudf.pandas`; or `import cudf.pandas; cudf.pandas.install()` BEFORE `import pandas`

$ rg -P '^sklearn\.cluster\t' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
sklearn.cluster	cuml.cluster	cuml.accel	accel proxies KMeans, DBSCAN, HDBSCAN, SpectralClustering; AgglomerativeClustering needs an explicit cuml.cluster import

$ rg -P '^scipy\.ndimage\t' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
scipy.ndimage	cupyx.scipy.ndimage	-	-

$ rg -P '^sklearn\.neighbors\t' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
sklearn.neighbors	cuml.neighbors	cuml.accel	NearestNeighbors, KNeighborsClassifier, KNeighborsRegressor, KernelDensity

$ rg -i 'faiss' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
faiss	cuml.neighbors.NearestNeighbors	-	exact and IVF search via algorithm='brute'/'ivfflat'/'ivfpq' ('rbc' is limited to <=3 dims); this stack ships no graph index (CAGRA/HNSW)
faiss.Kmeans	cuml.cluster.KMeans	-	GPU k-means with scalable-k-means++ init
```

Read out `rapids_target` (target import path) and `zero_code` (zero-code solution identifier).

### Step 3: Check whether the zero-code solution applies

If the `zero_code` field is not `-` and the scenario allows it (primarily "rewriting existing CPU code"), prefer the zero-code solution. Canonical activation methods:

| zero_code identifier | Activation method |
|---|---|
| `cudf.pandas` | CLI: `python -m cudf.pandas script.py`<br>Jupyter first cell: `%load_ext cudf.pandas`<br>In-program (must precede `import pandas`): `import cudf.pandas; cudf.pandas.install()` |
| `cuml.accel` | CLI: `python -m cuml.accel script.py`<br>Jupyter first cell: `%load_ext cuml.accel`<br>Environment variable: `CUML_ACCEL_ENABLED=1`<br>In-program (must precede `import sklearn` / `umap` / `hdbscan`): `from cuml.accel import install; install()` |

Once a zero-code solution is enabled, **the original code does not need any import changes**; unsupported APIs automatically fall back to CPU without raising errors.

`cuml.accel` proxies a fixed estimator list: `sklearn.cluster` KMeans / DBSCAN / HDBSCAN / SpectralClustering, `sklearn.covariance` EmpiricalCovariance / LedoitWolf, `sklearn.decomposition` PCA / IncrementalPCA / TruncatedSVD, `sklearn.ensemble` RandomForestClassifier / RandomForestRegressor / IsolationForest, `sklearn.kernel_ridge` KernelRidge, `sklearn.linear_model` LinearRegression / LogisticRegression / Ridge / Lasso / ElasticNet, `sklearn.manifold` TSNE / SpectralEmbedding, `sklearn.neighbors` NearestNeighbors / KNeighborsClassifier / KNeighborsRegressor / KernelDensity, `sklearn.preprocessing` StandardScaler / MinMaxScaler / MaxAbsScaler / LabelEncoder / LabelBinarizer / OneHotEncoder / PolynomialFeatures / TargetEncoder, `sklearn.svm` SVC / SVR / LinearSVC / LinearSVR, `umap.UMAP`, and `hdbscan.HDBSCAN` when the standalone hdbscan package is installed. `sklearn.compose`, `sklearn.pipeline` and `sklearn.utils` are patched for interoperability rather than proxied. **Anything outside that list silently stays on CPU** — `sklearn.naive_bayes`, `sklearn.metrics`, `sklearn.feature_extraction`, `sklearn.random_projection`, `sklearn.model_selection` and `sklearn.multiclass` have explicit `cuml` counterparts but no zero-code path, so reach them through an explicit import (Step 4).

**Applicability decision**:
- Rewrite scenario + user wants "to make existing code run faster" → zero-code
- New code / user wants explicit GPU APIs / user wants the code to clearly read as using RAPIDS → proceed to the explicit import in Step 4

### Step 4: Explicit import replacement (when zero-code does not apply, or when writing new code)

Two-step API location:

1. Get `rapids_target` from mapping.tsv. Examples: `numpy → cupy`, `scipy.ndimage → cupyx.scipy.ndimage`, `sklearn.cluster → cuml.cluster`, `faiss → cuml.neighbors.NearestNeighbors`.

2. Search for the target API in `${SKILL_DIR}/apis/<pkg>.txt` using `ripgrep`. The four shipped index files are `cupy.txt`, `cupyx.txt`, `cudf.txt` and `cuml.txt`:

   ```bash
   # Search for a class: exact match of class name followed by ( or .
   rg -i '\.KMeans\('              "$SKILL_DIR/apis/cuml.txt"
   rg -i '^cuml\.cluster\.KMeans'  "$SKILL_DIR/apis/cuml.txt"

   # Search for a function: similarly match .funcname(
   rg -i '\.gaussian_filter\('     "$SKILL_DIR/apis/cupyx.txt"
   rg -i '\.read_parquet\('        "$SKILL_DIR/apis/cudf.txt"
   rg -i '\.fft2\('                "$SKILL_DIR/apis/cupy.txt"

   # Search for all APIs under a given submodule
   rg '^cuml\.cluster\.'           "$SKILL_DIR/apis/cuml.txt"
   rg '^cupyx\.scipy\.ndimage\.'   "$SKILL_DIR/apis/cupyx.txt"

   # Search multiple files at once
   rg -i '\.PCA\('                 "$SKILL_DIR/apis/cuml.txt" "$SKILL_DIR/apis/cupyx.txt"
   ```

   Each matched line is formatted as "full path(signature) - first line of docstring"; **copy the signature directly when writing code**.

### Step 5: Respect the GPU data lifecycle

- **Continuous GPU pipeline**: avoid mid-stream round-trips like `cudf.DataFrame.to_pandas() → processing → cudf.from_pandas()`. If some intermediate step does not yet provide a GPU version, search `${SKILL_DIR}/apis/*.txt` once more to confirm before falling back.
- **No device mixing**: mixing `cupy.ndarray` with `numpy.ndarray`, or `cudf.DataFrame` with `pandas.DataFrame`, triggers implicit copying and forces stream synchronization. All array types within the same computation graph should be consistent.
- **I/O lands directly on GPU**: use `cudf.read_csv` / `cudf.read_parquet` / `cudf.read_orc` / `cudf.read_json`, etc., to go from disk straight to GPU memory, rather than `pandas.read_*` followed by an upload; the same applies to `cuml.preprocessing`, which works directly on cuDF.
- **cuDF 26.10 tracks pandas 3.0** (it accepts pandas `>=3.0.0,<3.1.0`): `applymap`, `backfill`, `pad`, `first`, `last` and `values_host` are gone on both sides, as are the `Index.is_boolean` / `is_categorical` / `is_floating` / `is_integer` / `is_interval` / `is_numeric` dtype predicates. Write `map`, `bfill`, `ffill` and label slicing instead, and reach for `cudf.api.types.is_dtype_obj_numeric` / `is_dtype_obj_string` for dtype checks. `DataFrame.flags` / `set_flags` and `Series.set_flags` exist, but cuDF `rename(index=...)` and `reindex` skip the `allows_duplicate_labels=False` check that pandas enforces.
- **Default dtypes**: some cuDF / cuML operators default to `float32` (for example `cuml.datasets.make_blobs`) while sklearn defaults to `float64`. For high-precision comparisons, build the inputs as `float64` explicitly (e.g., `dtype='float64'` or `X.astype('float64')`). `cuml.neighbors.NearestNeighbors` keeps `float32` distances even for `float64` input, so compare them at `rtol=1e-5` or recompute them with `cuml.metrics.pairwise_distances`, which keeps `float64`. cuML 26.10 removed the `convert_dtype` keyword from every estimator method and metric, and passing it raises `TypeError`.
- **Fail-fast, no existence checks**: importing a RAPIDS package already requires CUDA to be available; do not write defensive fallbacks like `try: import cupy except: import numpy as cupy` — if the environment is missing, let it fail directly.

## Search Examples

### Example 1: Accelerate `from sklearn.cluster import KMeans` to GPU (rewrite scenario)

```
$ rg -P '^sklearn\.cluster\t' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
sklearn.cluster	cuml.cluster	cuml.accel	accel proxies KMeans, DBSCAN, HDBSCAN, SpectralClustering; AgglomerativeClustering needs an explicit cuml.cluster import
```

- **Zero-code preferred**: have the user run with `python -m cuml.accel script.py`; the original code stays untouched.
- **Explicit replacement** (if the user prefers):
  ```
  $ rg -i '^cuml\.cluster\.KMeans\(' "$SKILL_DIR/apis/cuml.txt"
  cuml.cluster.KMeans(*, n_clusters=8, max_iter=300, tol=0.0001, verbose=False, random_state=None, init='scalable-k-means++', n_init='auto', oversampling_factor=2.0, max_samples_per_batch=32768, device_buffer_samples=0, init_size=0, output_type=None) - KMeans is a basic but powerful clustering method which is optimized via
  ```
  Per the signature, change directly to `from cuml.cluster import KMeans`. Note the defaults that differ from sklearn: `init='scalable-k-means++'`, and every parameter is keyword-only.

### Example 2: Implement a matrix FFT pipeline from scratch (new code scenario)

Requirement: perform fft2 + magnitude + normalization on a batch of 2D matrices.

1. "If using CPU, I would use numpy.fft + numpy" → look up the mapping:
   ```
   $ rg -P '^numpy(\.fft)?\t' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
   numpy	cupy	-	import cupy as cp; substitute cp for np
   numpy.fft	cupy.fft	-	-
   ```
2. Look up the specific API:
   ```
   $ rg -i '\.fft2\(' "$SKILL_DIR/apis/cupy.txt"
   cupy.fft.fft2(a, s=None, axes=(-2, -1), norm=None) - Compute the two-dimensional FFT.
   ```
3. Write the code: a one-shot upload via `cp.asarray` → `cp.fft.fft2` → `cp.abs` → `cp.linalg.norm`, all done on GPU, then `.get()` or write the file output at the very end.

### Example 3: Write unit tests for a new algorithm implementation (new test scenario)

Requirement: test that a GPU-implemented PCA produces numerically consistent results with sklearn's PCA.

1. Data generation on GPU — **not** `sklearn.datasets` / `numpy.random`:
   ```
   $ rg -i '^cuml\.datasets\.make_blobs\(' "$SKILL_DIR/apis/cuml.txt"
   cuml.datasets.make_blobs(n_samples=100, n_features=2, centers=None, cluster_std=1.0, center_box=(-10.0, 10.0), shuffle=True, random_state=None, return_centers=False, order='F', dtype='float32') - Generate isotropic Gaussian blobs for clustering.
   ```
   `dtype='float32'` is the default here, so pass `dtype='float64'` when the test compares against a float64 sklearn baseline.
2. Run on GPU:
   ```
   $ rg -i '^cuml\.decomposition\.PCA\(' "$SKILL_DIR/apis/cuml.txt"
   cuml.decomposition.PCA(*, copy=True, iterated_power=15, n_components=None, svd_solver='auto', tol=1e-07, verbose=False, whiten=False, output_type=None) - PCA (Principal Component Analysis) is a fundamental dimensionality
   ```
   `cuml.decomposition.PCA(n_components=k).fit_transform(X)`; `n_components` is keyword-only, unlike sklearn's positional first argument.
3. CPU comparison: one-shot downlink with `X.get()` → `sklearn.decomposition.PCA(...).fit_transform(X_cpu)`.
4. Assertion:
   ```
   $ rg -i '^cupy\.testing\.assert_allclose\(' "$SKILL_DIR/apis/cupy.txt"
   cupy.testing.assert_allclose(actual, desired, rtol=1e-07, atol=0, equal_nan=True, err_msg='', verbose=True, *, strict=False) - Raises an AssertionError if objects are not equal up to desired tolerance.
   ```
   Compare the absolute values of components, since PCA sign is arbitrary. For dataframe results use `cudf.testing.assert_frame_equal`.
5. Across the whole process, data transfer happens only once, at step 3.

### Example 4: Replace faiss for nearest-neighbor search (rewrite scenario)

```
$ rg -i 'faiss' "$SKILL_DIR/cpu-rapids-cuda-mapping.tsv"
faiss	cuml.neighbors.NearestNeighbors	-	exact and IVF search via algorithm='brute'/'ivfflat'/'ivfpq' ('rbc' is limited to <=3 dims); this stack ships no graph index (CAGRA/HNSW)
faiss.Kmeans	cuml.cluster.KMeans	-	GPU k-means with scalable-k-means++ init

$ rg -i '^cuml\.neighbors\.NearestNeighbors[(.]' "$SKILL_DIR/apis/cuml.txt"
cuml.neighbors.NearestNeighbors(*, n_neighbors=5, radius=1.0, algorithm='auto', metric='euclidean', p=2, algo_params=None, metric_params=None, n_jobs=None, verbose=False, output_type=None) - NearestNeighbors is an queries neighborhoods from a given set of
cuml.neighbors.NearestNeighbors.as_sklearn(self) - Convert this estimator into an equivalent scikit-learn (or scikit-learn
cuml.neighbors.NearestNeighbors.fit(self, X, y=None) -> "'NearestNeighbors'" - NeighborsBase.fit(self, X, y=None) -> 'NearestNeighbors'
cuml.neighbors.NearestNeighbors.from_sklearn(model) - Create a cuml estimator from a scikit-learn estimator.
cuml.neighbors.NearestNeighbors.get_params(self, deep=True) - Returns a dict of all params owned by this class. If the child class
cuml.neighbors.NearestNeighbors.kneighbors(self, X=None, n_neighbors=None, return_distance=True, *, two_pass_precision=False) - NeighborsBase.kneighbors(self, X=None, n_neighbors=None, return_distance=True, *, two_pass_precision=False)
cuml.neighbors.NearestNeighbors.kneighbors_graph(self, X=None, n_neighbors=None, mode='connectivity') - NeighborsBase.kneighbors_graph(self, X=None, n_neighbors=None, mode='connectivity')
cuml.neighbors.NearestNeighbors.radius_neighbors_graph(self, X=None, radius=None) - NearestNeighbors.radius_neighbors_graph(self, X=None, radius=None)
cuml.neighbors.NearestNeighbors.set_nvtx_annotations(self)
cuml.neighbors.NearestNeighbors.set_params(self, **params) - Accepts a dict of params and updates the corresponding ones owned by
```

Rewrite per the signatures: `fit(X)` ingests the corpus, `kneighbors(Q, n_neighbors=k)` returns `(distances, indices)`. Pick the index through `algorithm`: `'brute'` for exact search, `'ivfflat'` / `'ivfpq'` for the approximate IVF variants (tune them via `algo_params`), `'rbc'` for the random ball cover, which only accepts 3 or fewer dimensions. This stack ships no graph index, so a faiss HNSW or a CAGRA index has no direct counterpart — say so and pick the closest IVF configuration instead. `faiss.Kmeans` maps to `cuml.cluster.KMeans`.

## When RAPIDS Has No Corresponding Implementation

- **Know the edges of this stack.** It ships `cupy`, `cupyx`, `cudf` and `cuml` only. Tell the user plainly rather than inventing an API for: graph algorithms (no `cugraph`, no `nx-cugraph` backend), image and whole-slide file I/O (no `cucim`; `cupyx.scipy.ndimage` covers filtering, morphology, geometric transforms and labelling, but no image decoding or slide readers), ANN graph indexes (no `cuvs`; `cuml.neighbors` covers exact and IVF search), multi-GPU or out-of-core dataframes (no `dask-cudf`), dashboards (no `cuxfilter`), and GPU forest inference for XGBoost or LightGBM models (cuML 26.10 removed `cuml.fil` / `cuml.ForestInference`, and the separate `nvforest` package that cuML installs as a dependency sits outside this skill). `cupyx.scipy.spatial.distance` and `cupyx.scipy.sparse.csgraph` raise `RuntimeError` here because they need the cuVS Python package and `pylibcugraph` respectively, so compute distance matrices with `cuml.metrics.pairwise_distances`.

Otherwise handle by priority:

1. Search for similar keywords again in `${SKILL_DIR}/apis/<pkg>.txt`. RAPIDS naming often differs slightly from sklearn / scipy (e.g., sklearn's `cross_val_score` has no direct counterpart in cuml, but can be reproduced with `cuml.model_selection.train_test_split` / `KFold` plus a handwritten loop; `cuml.pipeline.Pipeline` / `make_pipeline` re-export sklearn's classes and chain cuML estimators on GPU data, and `cuml.compose.ColumnTransformer` covers column routing). `apis/cuml.txt` omits the `cuml.pipeline` re-exports because it indexes only objects defined in cuML.
2. Check neighboring packages: an operator missing from `cuml` or `cudf` can often be assembled by hand from `cupy` and `cupyx.scipy` primitives.
3. When there is still no counterpart, **explicitly tell the user that the operator is not in the current RAPIDS stack**, then use the CPU version and consolidate data transfers at the CPU↔GPU boundary to minimize the number of transfers (ideal: the entire pipeline does `.get()` / `.to_pandas()` only once at the end).

## (Re-)Generating apis/

- After any RAPIDS package upgrade, run `python "$SKILL_DIR/fetch_rapids_apis.py"` to regenerate `${SKILL_DIR}/apis/<pkg>.txt`. The script defaults to the four packages this skill covers: `cupy`, `cupyx`, `cudf`, `cuml`.
- You can also target specific packages only: `python "$SKILL_DIR/fetch_rapids_apis.py" --packages cudf cuml`.
- The script writes back to `${SKILL_DIR}/apis/` by default (defaults to its own directory), regardless of the current working directory.
- The script must run in "a Python environment with RAPIDS installed" and requires the CUDA driver to be visible.

## What Not to Do

- **Do not proactively enable** `cudf.pandas` / `cuml.accel` — monkey-patches affect the entire Python process, so **let the user decide** whether to turn it on; your job is only to inform them of the activation command.
- **Do not write try/except defenses for "is GPU available"**; the presence of RAPIDS packages itself assumes CUDA is available — if the environment is missing, let it fail-fast.
- **Do not convert every numpy / pandas call to cupy / cudf** — in rewrite scenarios, the user may only want to accelerate the hot path; check the context before deciding the scope of refactoring.
- **Do not write RAPIDS API signatures from memory**; first `rg` once into `${SKILL_DIR}/apis/<pkg>.txt` to get the accurate signature (cuml and sklearn often differ in `init`, `output_type`, keyword-only parameters, etc.).
- **Do not let data downlink mid-stream**; place `cudf.DataFrame.to_pandas()` only at the very end of the pipeline or at necessary integration points (plotting, writing compatible output formats, etc.).
- **Do not name a package this stack does not ship** (`cugraph`, `nx_cugraph`, `cucim`, `cuvs`, `dask_cudf`, `cuxfilter`); an import that fails is worse than an honest "no GPU path here".

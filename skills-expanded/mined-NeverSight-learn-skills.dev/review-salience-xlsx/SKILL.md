---
name: review-salience-xlsx
description: >
  Use this skill when the user has product review files and wants to: (1) score
  each review on a set of attributes using a salience scale (0–7) and export a
  review × attribute matrix as .xlsx; (2) run PCA to reduce attributes into
  latent dimensions; (3) cluster reviews into customer segments with K-means.
  Trigger on requests like 「逐則評論評分」、「顯著度矩陣」、「salience scoring」、「主成分分析」、
  「PCA」、「顧客分群」、「K-means」、「評論×屬性 Excel」, or any combination thereof.
  Also trigger when this step follows an attribute-discovery workflow and the
  user wants scored data, dimensionality reduction, or segmentation. Use this
  skill even if the user only mentions part of the pipeline.
---

# Review Salience → PCA → K-means Customer Segmentation

Full pipeline from a review corpus to customer segments:

1. **Score** every review on every attribute (salience 0–7) → `review × attribute` matrix
2. **Reduce** attributes to latent dimensions via PCA
3. **Segment** reviews into customer groups via iterative K-means

Each stage is independently useful. Run only the stages the user needs.

For the Excel output format, read `references/xlsx-format.md`.  
For PCA and K-means implementation details, read `references/pca-kmeans.md`.  
For a worked example (safety-eyewear, 923 reviews, 30 attributes, 4 clusters), read `references/worked-example.md`.

Salience measures *how prominently* a reviewer mentions an attribute — not
sentiment. Each cell is an integer 0–7:

| Score | Meaning |
|-------|---------|
| 0 | Attribute not mentioned at all |
| 1–3 | Slight or indirect mention |
| 4 | Neutral or ambiguous mention |
| 5–6 | Clearly and explicitly mentioned |
| 7 | Strongly and fully emphasised |

For the Excel output format, read `references/xlsx-format.md`.  
For PCA and K-means implementation details, read `references/pca-kmeans.md`.  
For a worked example (safety-eyewear corpus, 923 reviews, 30 attributes, 4 clusters), read `references/worked-example.md`.

---

## Concepts

### Attribute catalog
A frozen, ordered list of attributes produced upstream (e.g. by the
`review-scoring-docx` skill). Each attribute has an `id` (zero-padded, e.g.
`01`) and a `label`. The catalog **must not change** after scoring begins.

### Scorer
The component that reads one review and returns N integers. This skill is
**scorer-agnostic**: Claude reads and scores by default, but the architecture
supports swapping in any external scorer without changing the rest of the pipeline.
See [Scorer contract](#scorer-contract) below.

### Salience matrix
A table with one row per review and one column per attribute, plus metadata
columns (`review_id`, `product`, `review_text`). Column names follow the pattern
`s01`, `s02` … `sN`. This is the input to both PCA and K-means.

### PC scores matrix
Produced by PCA on the standardised salience matrix. Shape: `(n_reviews, n_components)`.
Each column is a latent dimension (e.g. "整體使用價值感", "場景創新適應力").
This matrix is the direct input to K-means clustering.

### Customer segments
K-means groups applied to the PC scores matrix. Each review (= each customer
voice) is assigned to exactly one segment. The iterative pruning rule ensures
no segment is smaller than 5% of the total corpus.

---

## Workflow

### Step 0 — Locate required skills
Check your available skills for an **xlsx skill** (covers `.xlsx` or spreadsheet
creation) and a **docx skill** if Word output is needed. Read their SKILL.md
files before writing any output code.

### Step 1 — Ingest reviews

Load all reviews for each product. Never truncate. Accept all languages.

```python
import csv

def load_reviews(filepath):
    candidates = ['body', 'Body', 'review', 'text', 'content']
    with open(filepath, encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        col = next((c for c in candidates if c in reader.fieldnames), None)
        if col is None:
            raise ValueError(f"No text column found. Headers: {reader.fieldnames}")
        return [r[col].strip() for r in reader
                if r[col].strip() and len(r[col].strip()) > 15]
```

Print a per-product count summary before proceeding.

### Step 2 — Confirm the attribute catalog

Either receive the catalog from upstream or rediscover it by reading the corpus.
Freeze as an ordered list before scoring starts:

```python
ATTRS = [
    ("01", "attribute label 1"),
    ("02", "attribute label 2"),
    # ...
]
```

### Step 3 — Score reviews  ← scorer swap point

This is the **scorer contract boundary**. Anything that satisfies the contract
below can replace Claude's built-in scoring.

#### Scorer contract

**Input:** a single review string (any language)  
**Output:** a list of integers, one per attribute, in catalog order, each 0–7

**Built-in scorer (Claude reads semantically):**  
Read each review, understand its meaning, assign scores. No keyword matching.
See `references/worked-example.md` for calibration examples.

**External scorer (n8n / API / other):**  
See `references/external-scorer.md` for integration patterns.

```python
scores = {}
for pid, reviews in all_reviews.items():
    scores[pid] = []
    for review_text in reviews:
        scores[pid].append(score_one_review(review_text, ATTRS))
```

Save progress incrementally if corpus > 200 reviews.

### Step 4 — Build salience Excel

See `references/xlsx-format.md` for exact sheet layout, colour scheme, and
openpyxl patterns. Two sheets: full matrix + product summary.

### Step 5 — PCA (if requested)

Read `references/pca-kmeans.md` → Section A before writing any PCA code.

Key steps:
1. Standardise: `X_std = StandardScaler().fit_transform(X)`
2. Fit PCA: use Kaiser criterion (eigenvalue > 1) to choose `n_components`
3. Compute factor loadings: `loadings = components_.T × sqrt(eigenvalues_)`
4. Name each PC by its dominant loadings (|≥ 0.30|)
5. Save PC scores matrix for clustering: `PC = pca.fit_transform(X_std)`

### Step 6 — K-means segmentation (if requested)

Read `references/pca-kmeans.md` → Section B before writing any clustering code.

Key steps:
1. Scan K=2–9 for Elbow + Silhouette
2. Pick starting K (favour interpretability over peak silhouette if gap is small)
3. Run iterative pruning: remove clusters < 5% of corpus, decrement K, refit
4. **After convergence: call `km.predict(ALL_reviews)` — never discard pruned reviews**
5. Name clusters by PC centroid pattern and top attribute means

### Step 7 — Output

- Save `.xlsx` to `/mnt/user-data/outputs/`
- Save `.docx` to `/mnt/user-data/outputs/` (if Word output was requested)
- Call `present_files` for every output file
- Write a prose summary: total reviewed, cluster sizes + names, top finding per cluster

---

## Hard rules

1. **Never truncate reviews.** Every valid review (> 15 chars) must be scored and clustered.
2. **All languages count.** Do not filter by language.
3. **Catalog is frozen before scoring.** No mid-run additions or reordering.
4. **Integer scores only.** Each salience cell is a whole number 0–7.
5. **Scorer is swappable.** The pipeline must not assume Claude is the scorer.
6. **Never discard pruned reviews.** After iterative pruning converges, use `km.predict()` on the full corpus to assign every review — including those removed during pruning — to the nearest final centroid.
7. **Use absolute column widths.** Percentage widths break in Google Sheets.
8. **Present with `present_files`.** Never ask the user to navigate to the file.

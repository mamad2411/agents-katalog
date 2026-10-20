---
name: protein-sequence-data-processing
description: Clean, validate, and preprocess protein-sequence datasets into model-ready tables. Called after profiling-datasets — receives a loaded DataFrame and Dataset Profile; does not re-detect format or reload data.
user-invokable: true
compatibility: pandas ≥1.5, numpy ≥1.23. Works offline.
---

# Protein Sequence Data Processing

> **Input contract:** This skill always receives a `df` (pandas DataFrame) and `profile` (Dataset Profile) from `profiling-datasets`. Loading, format detection, and basic stats are already done — start from Step 1 below.

```python
# Expected inputs
df:      pd.DataFrame   # loaded by profiling-datasets Stage 2
profile: dict           # Dataset Profile with sequence_stats, label_info, split_info, warnings
```

Utility functions are in `scripts/`. Import from there — do not re-implement inline.

---

## When to use

- Preparing a protein/peptide dataset for fine-tuning, embedding, scoring, or evaluation
- Cleaning sequences, resolving label conflicts, creating label masks, auditing splits
- Any step between `profiling-datasets` output and model training

## When not to use

| Want… | Use instead |
|---|---|
| Detect format or load data | `profiling-datasets` (always first) |
| Select a model | `model-selection` |
| Run training | `huggingface-jobs` |
| Preprocess tabular features | `numerical-data-processing` |

---

## Preprocessing pipeline

Apply in order. Import utilities from `scripts/`. Record `n_removed` in manifest at every filtering step.

### Step 1 — Schema normalization
```python
from scripts.sequence_utils import normalize_col_names, infer_seq_col, infer_id_col
df = normalize_col_names(df)         # lowercase, strip, replace spaces with _
seq_col = infer_seq_col(df, profile) # uses profile.schema first, then name heuristics
id_col  = infer_id_col(df, profile)
```

### Step 2 — Sequence cleaning
```python
from scripts.sequence_utils import normalize_aa, strip_terminal_stop, has_only_valid_aas
df[seq_col] = df[seq_col].map(normalize_aa)           # strip + uppercase
df[seq_col] = df[seq_col].map(strip_terminal_stop)    # remove trailing *
df["length"] = df[seq_col].str.len()
```

### Step 3 — Invalid sequence removal
```python
from scripts.filter_utils import filter_invalid_sequences, filter_internal_stops
df, n = filter_invalid_sequences(df, seq_col)         # non-AA chars
df, n = filter_internal_stops(df, seq_col)            # internal * (premature stop codons)
```

### Step 4 — Label inference and mask creation
```python
from scripts.label_utils import infer_label_columns, create_label_mask, detect_label_type
label_cols = infer_label_columns(df, profile)         # uses profile.label_info first
for col in label_cols:
    df[f"label_mask_{col}"] = create_label_mask(df[col])   # 1=observed, 0=missing
```

### Step 5 — Conflict resolution
```python
from scripts.label_utils import resolve_conflicts, check_label_conflicts_multi
# For single-target: sequences labeled both positive AND negative
df, conflict_report = resolve_conflicts(df, seq_col, label_cols, drop_globally=False)
# For multi-target (e.g. per-animal cols): resolve per column independently
conflicts = check_label_conflicts_multi(df, seq_col, label_cols)
```

### Step 6 — WT / reference filtering (if applicable)
```python
from scripts.filter_utils import filter_wt
# Only if user provides wt_sequence or it's in profile metadata
df, n = filter_wt(df, seq_col, wt_sequence=wt_seq)
```

### Step 7 — Length filtering (if applicable)
```python
from scripts.filter_utils import filter_by_length
# Only apply if user specified limits or profile.sequence_stats flags ESM2 incompatibility
df, n = filter_by_length(df, seq_col, min_len=None, max_len=1024)
```

### Step 8 — Deduplication
```python
from scripts.filter_utils import deduplicate
df, dup_report = deduplicate(df, seq_col, id_col)     # always run before split assignment
```

### Step 9 — Split assignment and leakage audit
```python
from scripts.split_utils import random_split, clustered_split, check_leakage
# Only if no split column exists in profile.split_info
if profile["split_info"]["splits"] is None:
    df = random_split(df, ratios=(0.8, 0.1, 0.1), stratify_col=label_cols[0] if label_cols else None)
leakage = check_leakage(df, seq_col)                  # always run; report even if 0
```

---

## Complex scenarios

**DMS / variant effect**
- Input has `mut_sequence` + `wt_sequence` cols and a ΔΔG or fitness label
- Keep WT row separately (do not filter it out via `filter_wt` for DMS datasets)
- Label is per-mutation — treat as regression or binary depending on `profile.label_info.ml_formulation`

**Multi-animal / multi-target labels** (e.g. per-ACE2 binding)
- One label column per target species/cell line
- Run `check_label_conflicts_multi` → resolve per column with `drop_globally=False`
- Create one `label_mask_*` per target column
- Never collapse to a single label

**Homology-safe splits** (benchmark datasets)
Refer to `skills/clustering/` for all clustering methods and tools — that skill owns sequence identity clustering, mmseqs2/CD-HIT usage, and cluster-aware split assignment. Do not implement clustering inline here.
Always note in manifest whether homology deduplication was performed.

---

## Output contract

```python
{
    "df": pd.DataFrame,       # cleaned, normalized, with split + label_mask_* cols
    "manifest": {
        "steps": [{"step": str, "n_rows_before": int, "n_rows_after": int, "n_removed": int}],
        "seq_col": str, "id_col": str, "split_col": str,
        "label_cols": list, "label_mask_cols": list,
        "conflict_report": dict,
        "dup_report": dict,
        "leakage": dict,
        "warnings": list[str],
    },
    "readiness": "ok | warn | fail"
}
```

**`readiness = fail`** if: no sequence column found, empty df after cleaning, ambiguous label semantics.
**`readiness = warn`** if: duplicates present, missing labels >20%, no val/test split, leakage detected.

---

## Hard constraints

- **Never** relabel missing as negative — always use `label_mask_*`
- **Never** invent or overwrite existing split assignments
- **Never** silently drop rows — record `n_removed` in manifest at every step
- **Never** truncate sequences without explicit user instruction
- **Always** deduplicate before split assignment
- **Always** run `check_leakage` and report result even if zero
- **Always** create `label_mask_*` for every label column
- **Always** output manifest — even if preprocessing is minimal

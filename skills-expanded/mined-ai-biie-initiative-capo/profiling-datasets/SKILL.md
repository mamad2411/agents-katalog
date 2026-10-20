---
name: profiling-datasets
description: Detect dataset format and modality, load using format-specific loader, analyze with stats and plots, recommend preprocessing. Primary input is a HuggingFace Hub dataset ID; local files also supported.
user-invokable: true
compatibility: Requires network for HF Hub dataset IDs. Works offline for local files.
---

# Dataset Profiling

> **Always start here.** This is the sole entry point for any dataset — HF Hub IDs and local files alike. Do not invoke `loading-data` directly; it is an internal Stage 2 helper called from within this pipeline.

Input: HuggingFace Hub dataset ID **or** any local file (FASTA, FASTQ, BAM, CSV, Parquet, FCS, H5AD, MTX, etc.).

## When to use

Use for **any dataset inspection, profiling, or analysis task** — before any training or preprocessing decision.

Typical situations:
- User provides a HF dataset ID or a local file path and wants to know its structure, quality, or PLM compatibility
- User is unsure what format, task type, or `ml_formulation` their data implies
- User wants to check label distribution, sequence lengths, or missing values before committing to a model or training run

## When not to use

| If the user wants… | Use instead |
|---|---|
| Clean or preprocess sequences | `protein-sequence-data-processing` |
| Normalize tabular features | `numerical-data-processing` |
| Select a PLM or fine-tuning strategy | `model-selection` |
| Estimate training compute cost | `cost-estimation` |

> Profiling always comes first. When unsure whether to profile or preprocess — profile first. Never invoke `loading-data` directly.

---

## Stage 1 — Detect format and modality

Read full detection rules in `references/routing-rules.md`. Check in order; stop at first confident match.

**1. HuggingFace Hub ID** — if input matches `"org/dataset"` or `"user/dataset"`, peek 5 rows:

```python
from datasets import load_dataset
ds = load_dataset(dataset_id, split="train[:5]")
features = ds.features
splits = ds.info.splits
```

Inspect `features` for sequence column names (see routing-rules.md Step 1 for column name → dataset_type mapping).

**2. File extension** — match against extension table in routing-rules.md Step 2.

**3. Content sniff** — read first 5 lines for ambiguous or extensionless files (routing-rules.md Step 3).

**4. Still ambiguous** → report what was found, set `loadability.status = warn`, ask the user.

**Emits:** `{ format, dataset_type }` where `dataset_type` is one of:

| dataset_type | Source |
|---|---|
| `protein_sequence` | FASTA or HF dataset with AA sequence column (>90% standard AA chars) |
| `nucleotide_sequence` | FASTA or HF dataset with DNA/RNA column |
| `raw_reads` | FASTQ |
| `aligned_reads` | BAM / SAM |
| `tabular` | Parquet / CSV / TSV / JSONL / Excel / HF flat columns |
| `flow_cytometry` | FCS |
| `single_cell` | H5AD / H5 / MTX |
| `text` | JSONL or HF dataset with long string fields |

---

## Stage 2 — Load

Call the format-specific loader from `loading-data/loaders/<format>`. Each loader returns:

```python
{ "data": df | adata, "profile": { "loadability": { "status": "ok|warn|fail", ... }, ... } }
```

**Hard stop if `loadability.status = fail`** — do not proceed to Stage 3. Return the error profile.

| dataset_type | Loader skill |
|---|---|
| `protein_sequence` / `nucleotide_sequence` | `load-fasta` |
| `raw_reads` | `load-fastq` |
| `aligned_reads` | `load-bam` |
| `tabular` | `load-parquet` / `load-csv` / `load-excel` / `load-jsonl` / `load-asc` |
| `flow_cytometry` | `load-fcs` |
| `single_cell` | `load-h5` / `load-mtx` |

Pass loader's `data` and `profile` forward to Stage 3.

---

## Stage 3 — Analyze

Delegate to the modality-specific analysis skill. Each returns updated profile with stats, plot paths, and warnings.

| dataset_type | Analysis skill |
|---|---|
| `protein_sequence` | `analyze-protein-sequences` |
| `nucleotide_sequence` | `analyze-protein-sequences` (subset checks; flagged as non-PLM) |
| `raw_reads` | `analyze-fastq-reads` |
| `aligned_reads` | `analyze-bam-reads` |
| `tabular` | `analyze-tabular` |
| `flow_cytometry` | `analyze-fcs` |
| `single_cell` | `analyze-single-cell` |

Analysis skill output contract:

```python
{
    "profile": { ...updated with stats, schema, sample_stats, sequence_stats... },
    "plots": { "length_dist": "path/to/plot.png", "label_dist": "...", ... },
    "warnings": [...],
    "preprocessing_recommended": [...]
}
```

**Plot enforcement:** After the analysis skill returns, verify
`len(plots) >= 1` for every available split. For HuggingFace datasets with
multiple splits (e.g. train + test, train +++++++++++++++++++++++++++++++++++++++++++++++++++++ val + test), the analysis skill
MUST emit `plots_by_split = {"train": {...}, "val": {...}, "test": {...}}`
with at least one plot path per split that exists in the dataset; an
absent-split entry is permitted only when that split does not exist
upstream. An empty `plots_by_split[<split>]` for an existing split is a
Stage 3 failure — do not proceed to Stage 4. Emit a warning and surface the
error to the caller.

---

## Stage 3.5 — Split inspection (MANDATORY for `protein_sequence`)

Before recommending preprocessing, inspect how train/val/test are defined and flag homology leakage risk.

Populate `split_info` in the profile:

```python
split_info = {
    "source":                   "hf_splits | column:<name> | null",
    "splits":                   {"train": N, "val": N, "test": N},   # or null
    "is_homology_safe":         True | False | None,                 # see rules below
    "needs_user_confirmation":  False | True,                        # True only for the ambiguous case
    "user_question":            "<prompt for orchestrator to ask>" | None,
    "evidence":                 "<short reason>",
}
```

Decision rules for `is_homology_safe`:

| Situation | `is_homology_safe` | `needs_user_confirmation` | Action |
|---|---|---|---|
| No splits at all (`splits == null`) | `False` | `False` | **Recommend `clustering/mmseqs2`** as the first preprocessing step. |
| Only a `train` split exists, no val/test | `False` | `False` | **Recommend `clustering/mmseqs2`** to carve val/test from train. |
| Split column exists but no `cluster_id`/`family`/`group`/`fold` column accompanies it | `None` (pending) | **`True`** | **DO NOT recommend mmseqs2 yet.** Surface a `user_question` (see below) so the orchestrator can ask the user whether splits are cluster-aware. The orchestrator updates `is_homology_safe` based on the answer. |
| HF splits + an accompanying clustering / homology column exists (e.g. `cluster_id`, `uniref30_cluster`) | `True` | `False` | Note the source in `evidence`; no action. |
| Dataset card / README explicitly states "homology-aware split" or "cluster-based split" | `True` | `False` | Quote the source in `evidence`. |

When `needs_user_confirmation = True`, populate `user_question` with the exact prompt the orchestrator should ask. Use this template:

> `"Your dataset has splits in column '<col>' but no cluster_id / family / group column. How were these splits generated?"`

Suggested answer options (the orchestrator passes these to `AskUserQuestion`):

- *"Cluster-aware (mmseqs2 / CD-HIT / UniRef30 / family-based)"* → orchestrator sets `is_homology_safe = True`, **skips mmseqs2**.
- *"Random row-shuffle"* → orchestrator sets `is_homology_safe = False`, **runs mmseqs2**.
- *"I don't know / not documented"* → orchestrator sets `is_homology_safe = False`, **runs mmseqs2** (safe default).
- *"Other (species, time-based, manual curation)"* → orchestrator captures free-text reason, sets `is_homology_safe = False` unless the reason clearly implies homology-awareness.

Whenever `is_homology_safe = False` **after the orchestrator finalises it**, add to `warnings`:

> `"Splits missing or random — run skills/clustering/mmseqs2 to generate homology-safe train/val/test before training. Random splits leak homology and inflate metrics."`

**Never trigger mmseqs2 on the ambiguous case without asking** — running clustering on a dataset whose splits are already cluster-aware is wasted compute.

---

## Stage 4 — Recommend preprocessing

Based on `dataset_type`, `task_type`, `ml_formulation`, and `split_info.is_homology_safe` from the profile, emit a ranked list of preprocessing steps and point to the downstream skill. **Never execute preprocessing here — only recommend.**
All preprocessing skills are located under `data-processing/`. Use the routing table below to determine which skill to recommend and use as the next step in the pipeline.

| dataset_type | Preprocessing skill | Next steps |
|---|---|---|
| `protein_sequence` (splits OK) | `protein-sequence-data-processing` | Deduplicate → mask missing labels → tokenize |
| `protein_sequence` (`is_homology_safe = False`) | **`clustering/mmseqs2` → `protein-sequence-data-processing`** | **Cluster + assign splits FIRST** (mmseqs2) → deduplicate → mask missing labels → tokenize |
| `nucleotide_sequence` | — | Not a PLM input — flag and explain |
| `raw_reads` | — | Quality-filter (fastp/Trimmomatic) → align (BWA/HISAT2) → BAM → decide downstream |
| `aligned_reads` | — | featureCounts (RNA-seq), Cell Ranger (scRNAseq), or GATK (variant calling) |
| `tabular` | `numerical-data-processing` | Split first → impute/scale/encode only on train |
| `flow_cytometry` | — | Compensation → arcsinh(x/5) transform → gate in FlowJo / FlowCal / pyFlowSOM |
| `single_cell` | `single-cell` | Filter cells/genes → normalize_total → log1p |

---

## Final output

```python
{
    "profile": { ...Dataset Profile per references/dataset-profile-schema.md... },
    "plots": { "plot_name": "path/to/plot.png", ... },   # legacy flat map (back-compat)
    "plots_by_split": {
        "train": {"length_histogram": "...", "label_distribution": "...", "class_balance": "..."},
        "val":   {...},   # omit key entirely if split not present
        "test":  {...},
    },
    "per_split_stats": {
        "train": {"n_rows": int, "length_p99": int,
                  "n_pos_per_class": {"<col>": int, ...},
                  "n_neg_per_class": {"<col>": int, ...}},
        "val":   {...},
        "test":  {...},
    },
    # When is_homology_safe = False, preprocessing_skill MUST be "clustering/mmseqs2"
    # and "clustering/mmseqs2" MUST be the first entry in preprocessing_steps.
    "preprocessing_skill": "clustering/mmseqs2" | "protein-sequence-data-processing" | "numerical-data-processing" | "single-cell" | None,
    "preprocessing_steps": ["clustering/mmseqs2", "deduplicate", "mask missing labels", "tokenize"],
    "warnings": [...]
}
```

`plots_by_split` and `per_split_stats` are the authoritative per-split
layout for the orchestrator's pre-launch and finalizer phases. The legacy
flat `plots` map is retained for callers that haven't migrated yet — when
both are present, `plots_by_split` wins.

---

## Hard constraints

- **Never** start preprocessing, imputation, or feature engineering
- **Never** modify or overwrite the source dataset
- **Never** output tensors, embeddings, or encoded features
- **Never** proceed past Stage 2 if `loadability.status = fail`
- **Always** complete the full profile before suggesting any next step
- **Always** flag `nucleotide_sequence`, `raw_reads`, `aligned_reads` as non-PLM inputs in `warnings`
- **Always** flag sequences exceeding ESM2 limits (512 / 1024) in `warnings` for `protein_sequence`
- **Always** report `loadability.status = fail` if the file cannot be parsed — do not silently skip
- **Always** return at least one plot from Stage 3 — an empty `plots` dict is a Stage 3 failure
- **Always** populate `split_info` for `protein_sequence` and set `is_homology_safe` per the Stage 3.5 rules — `null` is allowed only when `needs_user_confirmation = True`
- **Never** recommend `clustering/mmseqs2` while `needs_user_confirmation = True` — the orchestrator must ask the user first and finalise `is_homology_safe` before any clustering decision
- **Always** recommend `clustering/mmseqs2` as the FIRST preprocessing step when `is_homology_safe = False` (after user confirmation if needed) — never let a protein dataset reach training with random or missing splits

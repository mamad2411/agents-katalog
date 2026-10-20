---
name: mmseqs2
description: Cluster protein sequences by sequence identity using MMseqs2 and emit cluster-aware train/val/test splits. INVOKE THIS SKILL whenever the dataset has no split column OR the existing split is a random row-shuffle — sequence-identity clustering is the fastest path to homology-safe splits without needing embeddings or a GPU. Returns assignments, a leakage report and a cluster-size plot. Reference: github.com/soedinglab/MMseqs2.
user-invokable: true
compatibility: mmseqs2 ≥14 on PATH (`brew install mmseqs2` or `conda install -c bioconda mmseqs2`), pandas ≥1.5, numpy ≥1.23, matplotlib ≥3.6, biopython ≥1.80 (FASTA writing only), pyyaml ≥6.
---

# MMseqs2 — sequence-identity clustering for homology-safe splits

> **Core rule:** Cluster, then split. Never random-split protein sequences — homologs end up in both train and test and inflate every metric you report.

This sub-skill lives alongside the parent `skills/clustering/` (embedding-based HDBSCAN / KMeans). The two are **complementary**, not alternatives:

- **mmseqs2 (this skill)** — raw sequences in, cluster-aware splits out. Fast. No GPU. The default choice when you only need splits.
- **parent `clustering/`** — pre-computed embeddings in, biologically coherent clusters out, with profiling and visualisation. Use when you want to *discover* groups in a learned representation.

---

## When to use

- `profile.json` from `profiling-datasets` reports `split_info.is_homology_safe = false` **and** `needs_user_confirmation = false`. This is the canonical trigger.
- You explicitly want **homology-safe** train / val / test labels without computing embeddings.

## When NOT to use (skip clustering — would waste compute)

- `split_info.is_homology_safe = true` — splits are already cluster-aware (confirmed by a sibling `cluster_id` / `family` / `group` / `fold` column, dataset card, or user answer).
- `split_info.needs_user_confirmation = true` — the profile is ambiguous (splits exist but no cluster sibling). The orchestrator must ask the user first; **do not invoke mmseqs2 in this state**. Running clustering on splits that are already cluster-aware-but-undocumented is wasted GPU time.

## When not to use

| Want… | Use instead |
|---|---|
| Discover groups in ESM embeddings | parent `skills/clustering/` (HDBSCAN / KMeans on PCA-reduced embeddings) |
| 2D visual map of sequence space | `skills/dimensionality-reduction/` |
| Fine-tune a PLM after splits exist | `skills/huggingface-jobs/` |
| Compute pairwise identity matrix only | `mmseqs search` directly (this skill clusters, doesn't search) |

---

## Algorithm decision table

| Algorithm | Use when | Runtime |
|---|---|---|
| `cluster` | N < 20k sequences. Sensitive cascaded clustering — catches remote homology. | ~30 s @ 10k seqs |
| `linclust` | N ≥ 20k sequences. Linear-time, slightly less sensitive — the right default at scale. | ~5 min @ 1M seqs |
| `auto` (default) | Let the script pick: `cluster` if N < 20k, else `linclust`. | — |

## Parameter cheat sheet

| Parameter | Default | Strict | Permissive | What it controls |
|---|---|---|---|---|
| `--min-seq-id` | `0.3` (remote homologs) | `0.5` (strain-level) / `0.9` (near-dup) | `0.2` | Minimum pairwise identity within a cluster |
| `-c` (coverage) | `0.8` | `0.9` | `0.5` | Min alignment coverage |
| `--cov-mode` | `0` (bidirectional) | `1` query / `2` target | — | How coverage is measured |

See `references/parameter_choices.md` for guidance on choosing a threshold for your task.

---

## One-shot workflow

```bash
python -m scripts.run_mmseqs2 \
  --input data/sequences.fasta \
  --id-col id --seq-col sequence \
  --algorithm auto \
  --min-seq-id 0.3 -c 0.8 --cov-mode 0 \
  --split-ratios 0.8 0.1 0.1 --seed 42 \
  --output-dir outputs/clustering/mmseqs2/
```

Also accepts `--input data/sequences.csv` or `.parquet` with `id` and `sequence` columns — the script writes a temporary FASTA internally.

---

## What the script does

1. **Preflight.** `which mmseqs` + `mmseqs version`. **MMseqs2 is a required external binary** (declared in `pyproject.toml` `[tool.autoimmunolab.apt]`; the PyPI `mmseqs2` package does NOT ship it). If missing, the script **fails loudly with install instructions — it never silently falls back.** To proceed without it, opt in explicitly with `--on-missing-binary fallback` (or `--allow-fallback`), which uses an **approximate** greedy k-mer Jaccard clusterer at `--min-seq-id`. The fallback prints a loud warning and is **not** a substitute for true MMseqs2 homology clustering — install MMseqs2 for production splits (Linux static build: `wget https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz`).
2. **Prepare FASTA.** If `--input` is FASTA, use as-is. If CSV / Parquet, write a temporary FASTA via Biopython.
3. **Build MMseqs2 DB.** `mmseqs createdb DB.fasta DB`
4. **Cluster.** Depending on the selected algorithm:
   - `mmseqs cluster DB DB_clu tmp --min-seq-id X -c Y --cov-mode Z`
   - `mmseqs linclust DB DB_clu tmp --min-seq-id X -c Y --cov-mode Z`
5. **Export TSV.** `mmseqs createtsv DB DB DB_clu DB_clu.tsv` → 2-column TSV (representative, member).
6. **Parse + factorize.** Read TSV, factorize the representative column to an integer `cluster` id.
7. **Assign splits.** Entire clusters go to one split — permute unique clusters with the seed, slice by `--split-ratios`.
8. **Verify + save.** Check leakage (cluster-spanning splits = 0), write 5 output files, plot cluster-size distribution, clean up `tmp/` and intermediate DB files (kept on failure for debugging).

---

## Output contract

```
outputs/clustering/mmseqs2/
├── cluster_assignments.csv     # id, cluster, representative, split
├── split_assignments.csv       # id, split
├── leakage_report.json         # {seqs_in_multiple_splits, clusters_spanning_splits, split_counts}
├── cluster_stats.json          # {n_clusters, n_singletons, largest_cluster_frac, mean/median/p99 size}
├── run_config.yaml             # exact CLI args + `mmseqs version` string
├── mmseqs.log                  # stdout/stderr from every mmseqs subprocess call
└── plots/
    └── cluster_size_distribution.png / .pdf
```

---

## Hard constraints

- **Never** random-split after clustering — entire clusters must go to one split.
- **Never** drop singletons silently — they are counted in `cluster_stats.json`.
- **Always** run the leakage check — non-zero `clusters_spanning_splits` is a hard failure (script exits non-zero).
- **Always** save `run_config.yaml` including the exact `mmseqs version` string for reproducibility.
- **Always** clean up `tmp/` and intermediate DB files on success; keep them on failure for debugging.
- **Plots** use the project palette: primary bars `#1E5994`, reference line `#9B3208`. Black axes / text.

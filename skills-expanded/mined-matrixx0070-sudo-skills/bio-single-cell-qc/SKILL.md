---
name: bio-single-cell-qc
version: 1.0.0
description: Quality-control single-cell RNA-seq with MAD-based filtering, ambient-RNA correction, doublet removal, and pre/post diagnostics.
author: matrixx0070
tags: [single-cell, scrnaseq, qc, doublets, ambient-rna, bioinformatics]
capabilities: []
---

## When to use

Use this when the user has a raw single-cell (or single-nucleus) RNA-seq count matrix and needs principled QC before clustering or annotation. It catches empty droplets, dying cells, ambient RNA, and doublets before they distort downstream biology.

**Not for:** already-QC'd matrices, clustering/annotation itself, bulk RNA-seq, or running the upstream alignment pipeline (use bio-pipeline-runner for that).

## Method

1. Load the count matrix (10x/H5AD) and compute per-cell metrics: total counts, genes detected, percent mitochondrial (and ribosomal/hemoglobin where relevant).
2. Filter by median absolute deviation, not hard cutoffs. Flag cells beyond ~3–5 MADs on log counts and log genes, and above a MAD threshold on percent-mito. **Decision:** loosen to 5 MADs for heterogeneous tissue where rare populations sit in the tail; tighten to 3 for a clean single cell line.
3. **Decision:** correct ambient RNA (SoupX/CellBender) only if the empty-droplet profile shows contamination; report the fraction. Skip for nuclei with low ambient signal.
4. Detect doublets (Scrublet/scDblFinder). Inspect the score distribution, set the threshold on the bimodal gap, drop predicted doublets.
5. Filter genes: keep those detected in a minimum number of cells (e.g. ≥3).
6. Re-check metrics post-filter. **Decision:** if a whole cluster vanished, you over-filtered — relax and re-run rather than proceed.

## Example

A 10x PBMC run loads at 8,200 cells. Percent-mito is bimodal; the 3-MAD cutoff lands at 12% and removes 640 dying cells. Scrublet shows a clean gap at 0.25, dropping 410 doublets. SoupX estimates 6% ambient and is applied. Genes kept: detected in ≥3 cells. Final: 7,050 cells. Post-filter violin confirms the platelet and DC populations survived.

## Pitfalls

- Applying one hard percent-mito cutoff (e.g. 5%) across tissues — cardiomyocytes and hepatocytes are legitimately high-mito.
- Skipping doublet detection, then "discovering" a fake intermediate cell type that is really two cells.
- Filtering so aggressively that a real rare population is erased — always compare pre/post.
- Not reporting the ambient contamination fraction, so downstream users can't judge residual signal.

## Output format

```
# scRNA-seq QC — <sample>
Tool versions: scanpy=_ / scDblFinder=_ / SoupX=_

## QC summary
cells in → out; removed by: mito=_, counts=_, genes=_, doublets=_

## Thresholds (with MAD justification)
counts: ±_ MAD | genes: ±_ MAD | mito: _ MAD | min cells/gene: _

## Diagnostics
violin counts/genes/mito (pre vs post); counts-vs-genes scatter (mito-colored); doublet-score histogram

## Reproducible code
<scanpy or Seurat block>
```
Note tissue-specific mito/count expectations. State tool versions.

## Reference

### MAD-based filtering

Median absolute deviation is robust to outliers where mean±SD is not. MAD = median(|xᵢ − median(x)|); scaled MAD = 1.4826·MAD approximates a standard deviation for normal data. Flag an outlier when |xᵢ − median| > k·MAD on the **log** scale for counts and genes (log stabilizes the right skew). Common k: **3 MAD** = moderately strict, **5 MAD** = permissive (keeps rare tail populations). Apply lower+upper bounds on log counts/log genes (upper catches doublets/multiplets, lower catches empty/dying), and an upper-only bound on percent-mito. This is the `scater::isOutlier` / sc-best-practices default.

### Standard QC thresholds by tissue

Starting points, not laws — always confirm against your own pre-filter distributions. "%mito high" = a legitimately high-metabolism tissue where a flat 5–10% cutoff would delete real cells.

| Tissue / prep | %mito cutoff (upper) | Min genes/cell | Notes |
|---------------|:-:|:-:|-------|
| PBMC / immune (10x) | 5–10% | 200–500 | Clean; platelets/RBC contaminate — filter HBB/PPBP |
| Solid tumor (dissociated) | 15–20% | 200 | Dissociation stress raises mito; high heterogeneity → use 5 MAD |
| Brain (whole-cell) | 5–10% | 500 | Neurons larger; ambient from lysed neurons |
| Heart / cardiomyocytes | 20–30% | 200 | Legitimately mito-rich; low flat cutoffs are wrong |
| Liver / hepatocytes | 20–40% | 200 | High mito + high ambient albumin |
| Kidney | 10–50% (segment-dependent) | 200 | Proximal tubule mito-rich |
| **snRNA-seq (nuclei, any tissue)** | **< 1–5%** | 200–500 | Nuclei should be nearly mito-free; high %mito = cytoplasmic/ambient contamination |
| Cell line (clean) | 5% (3 MAD ok) | 1000+ | Homogeneous → tight cutoffs fine |

Ribosomal % and hemoglobin % (HBA/HBB) are secondary flags: very high ribo can mark low-complexity cells; high hemoglobin marks RBC contamination.

### Doublet rate by loaded cells (10x Chromium)

Multiplet rate scales ~linearly with cells loaded, ≈ **0.8% per 1,000 cells recovered** (10x guidance).

| Cells recovered | ~Expected multiplet rate |
|:-:|:-:|
| 500 | ~0.4% |
| 1,000 | ~0.8% |
| 3,000 | ~2.3% |
| 5,000 | ~3.9% |
| 10,000 | ~7.6% |
| 20,000 | ~15% |

Set the detector's `expected_doublet_rate` from this table. Scrublet: threshold on the bimodal gap in the simulated-doublet score histogram (default ~0.25, but *inspect*, don't trust the default). scDblFinder and DoubletFinder are alternatives; scDblFinder handles multi-sample and is generally the current recommendation. Homotypic doublets (same type) are near-invisible to these tools — computational detection catches heterotypic ones.

### Ambient RNA

Empty-droplet "soup" contaminates real cells. **SoupX** estimates the contamination fraction (`rho`) from top ambient genes and subtracts it; typical rho 2–10%, > 20% signals a degraded sample. **CellBender** `remove-background` learns ambient + empty droplets with a deep model (run on raw, unfiltered matrix). Correct only when the empty-droplet profile shows real contamination; nuclei preps usually have low ambient. Always report the estimated fraction so downstream users can judge residual signal.

### Gene filtering & typical pipeline order

Keep genes detected in ≥ 3 cells (Scanpy `sc.pp.filter_genes(min_cells=3)`); for large atlases raise to ≥ 10. Canonical order: load raw → per-cell metrics → ambient correction (CellBender/SoupX on raw) → cell filtering (MAD) → doublet detection → gene filtering → normalize. Re-plot violins pre/post; if a whole cluster disappeared you over-filtered — relax and rerun.

### Tooling

Scanpy (`sc.pp.calculate_qc_metrics`, `pp.scrublet`), Seurat (`PercentageFeatureSet`, `subset`), scater/scran (`perCellQCMetrics`, `isOutlier`), scDblFinder, SoupX, CellBender. Reference workflow: *Single-cell best practices* (Heumos et al., Nat Rev Genet 2023). Always pin and report tool versions.

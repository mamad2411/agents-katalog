---
name: annbatch-data-loading-eval
description: Measures the data loading throughput and epoch iteration time for large-scale biological datasets. It benchmarks how efficiently a loader can fetch and prepare mini-batches from disk compared to existing frameworks. Use when the user wants to benchmark on Tahoe100M, 1000 Genomes GRCh38, Single-cell microscopy images, or asks about evaluating this task. Reports samples/sec.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.01949
  bibtex_key: gold2026annbatch
  confidence: high
---

# annbatch-data-loading-eval

> annbatch unlocks terabyte-scale training of biological data in anndata — Gold et al. (2026) (arXiv:2604.01949, 2026)

## What this evaluates

Measures the data loading throughput and epoch iteration time for large-scale biological datasets. It benchmarks how efficiently a loader can fetch and prepare mini-batches from disk compared to existing frameworks.

## Datasets

- **Tahoe100M** — total 100000000; splits: train (-1)
- **1000 Genomes GRCh38** — total 500000; splits: train (-1)
- **Single-cell microscopy images** — total ?; splits: test (-1)

## Metrics

- `samples/sec` **(primary)** — range: other
  - Number of biological samples (cells, individuals, or images) loaded per second from disk into memory or GPU.
- `epoch_time` — range: other
  - Total wall-clock time required to iterate over one full epoch of the dataset.

## Input / output format

**Input**: On-disk anndata files (Zarr or h5ad) containing biological data matrices or arrays.

**Output**: Mini-batches of data tensors ready for model training.

## Scoring recipe

```python
def compute_throughput(loader, dataset_size, batch_size):
    start_time = time.time()
    total_samples = 0
    for batch in loader:
        total_samples += len(batch)
        if total_samples >= dataset_size:
            break
    elapsed = time.time() - start_time
    return total_samples / elapsed
```

## Common pitfalls

- Disk I/O speed heavily depends on the underlying storage (e.g., AWS EBS limits to 125MB/s, masking GPU acceleration benefits).
- Pre-shuffling overhead (~5h) is often omitted from total training time comparisons, though it amortizes quickly.
- Data heterogeneity in anndata (e.g., raw counts in .X vs .raw.X) requires custom loading functions that can skew baseline comparisons.

## Evidence (verbatim from paper)

> Under default settings, annbatch achieves ~35,000 samples per second (samples/sec), whereas scDataset and MappedCollection reach only ~1,500 and ~850 samples/sec, respectively (Fig. 2a). These speed improvements yield a nearly 40-fold acceleration in model fitting compared to MappedCollection (Fig. 2b).

## Citation

```bibtex
@misc{gold2026annbatch,
  title={annbatch unlocks terabyte-scale training of biological data in anndata},
  author={Gold et al. (2026)},
  year={2026},
  note={arXiv:2604.01949}
}
```

- arXiv: 2604.01949

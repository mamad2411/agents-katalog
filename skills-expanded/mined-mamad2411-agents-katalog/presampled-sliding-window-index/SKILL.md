---
name: presampled-sliding-window-index
description: Pre-compute every valid (series, start_idx) pair once at dataset init and random-sample from that list, instead of recomputing windows per __getitem__.
category: data-pipeline
tags: [pytorch-dataset, sliding-window, time-series, dataloader, preindexing]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/shiyu-coder/Kronos.git
source_ref: master
source_commit: 67b630e67f6a18c9e9be918d9b4337c960db1e9a
source_project: Kronos
source_paths: [finetune/dataset.py, finetune/qlib_test.py]
version: 1.0.0
version_origin: extracted
imported_at: 2026-04-18T00:00:00Z
---

# Pre-build a flat index of (series, start) for uniform sampling across heterogeneous series

## When to use
- You have many time series of different lengths and want uniform sampling across every possible window, not weighted by series length.
- You want cheap `__getitem__` — O(1) lookup into a pre-built list and a single DataFrame slice, rather than recomputing valid starts each call.
- You want an epoch that doesn't iterate every window once (too many), but instead draws `n_samples` at random — with reproducible per-epoch seeds.

## Pattern
At init time, walk every series, compute `num_samples = len(series) - window + 1`, and for each valid offset append `(symbol, start_idx)` to a flat `self.indices` list. Also pre-compute derived per-step columns (calendar features) once and store in the DataFrame so they aren't recomputed per sample. Hold a dedicated `random.Random(seed)` to avoid polluting global state, and expose `set_epoch_seed(epoch)` for reproducible DDP shuffling.

```python
# finetune/dataset.py QlibDataset
self.indices = []
for symbol in self.symbols:
    df = self.data[symbol].reset_index()
    num_samples = len(df) - self.window + 1
    if num_samples > 0:
        df['minute']  = df['datetime'].dt.minute
        df['hour']    = df['datetime'].dt.hour
        df['weekday'] = df['datetime'].dt.weekday
        df['day']     = df['datetime'].dt.day
        df['month']   = df['datetime'].dt.month
        self.data[symbol] = df[self.feature_list + self.time_feature_list]
        for i in range(num_samples):
            self.indices.append((symbol, i))

self.n_samples = min(self.n_samples, len(self.indices))

def set_epoch_seed(self, epoch: int):
    self.py_rng.seed(self.config.seed + epoch)

def __getitem__(self, idx):
    random_idx         = self.py_rng.randint(0, len(self.indices) - 1)
    symbol, start_idx  = self.indices[random_idx]
    win_df             = self.data[symbol].iloc[start_idx:start_idx + self.window]
    ...
```

## Why it works / tradeoffs
Pre-building the index takes ~constant memory per valid window (`O(total_windows)` tuples) and makes sampling uniform over windows instead of series — this matters when some series are 10x longer than others. Caching calendar features on the DataFrame avoids repeated `.dt.hour` calls which are surprisingly slow in a hot dataloader loop. Tradeoff: the index can be huge if total_windows is in the tens of millions; in that case store per-symbol `num_samples` and index lazily. The pattern assumes stationary data — if you regenerate data, you must rebuild the index.

## References
- `finetune/dataset.py` in Kronos — `QlibDataset`
- `finetune/qlib_test.py` — `QlibTestDataset` applies the same pattern for sequential eval

---
name: autoresearch-compare
description: Compare autoresearch results across runs, branches, or machines. Reads results.tsv from multiple branches and generates comparison tables. Use when the user asks "compare runs", "how did machine X vs Y", or "cross-run analysis".
---

# Autoresearch Cross-Run Comparison

Compare experiment results across different autoresearch runs.

## Steps

1. **List all autoresearch branches**: `git branch --list "autoresearch/*"`
2. **For each branch**, read its `results.tsv` and final `train.py` config
3. **Build comparison table**:

```
| Run | Machine | Experiments | Best val_bpb | Improvement | Key Changes |
|-----|---------|-------------|--------------|-------------|-------------|
| ... | ...     | ...         | ...          | ...         | ...         |
```

4. **Identify convergent findings** — what did ALL runs discover?
5. **Identify divergent findings** — what worked on one machine but not another?
6. **Extract best config per machine** — the final kept train.py from each
7. **Recommend a merged "best of" config** incorporating cross-run insights

## Reference Points
- Upstream H100 (CUDA): val_bpb ~0.998 in 5 min
- M4 Max 128GB best: val_bpb ~1.295
- M1 Mac Studio 48GB: val_bpb ~1.808
- Mac Mini (Muon): val_bpb ~1.462

---
name: sdv
description: "Synthetic Data Vault (SDV) — generate synthetic tabular data. Single-table, multi-table, and sequential data synthesis. CTGAN, TVAE, CopulaGAN, GaussianCopula. Privacy metrics and evaluation."
tags: [sdv, synthetic-data, data-generation, privacy, ctgan, tabular-data, zorai]
---
## Overview

The Synthetic Data Vault (SDV) generates synthetic tabular data that preserves statistical properties while protecting privacy. Supports single-table, multi-table, and sequential data generation with CTGAN, TVAE, CopulaGAN, and GaussianCopula models.

## Installation

```bash
uv pip install sdv
```

## Single-Table (CTGAN)

```python
from sdv.single_table import CTGANSynthesizer
from sdv.datasets.demo import load_demo

data, metadata = load_demo(dataset="census")

synth = CTGANSynthesizer(metadata)
synth.fit(data)
synthetic = synth.sample(num_rows=500)

print(synthetic.head())
print(f"Original columns: {data.shape}, Synthetic: {synthetic.shape}")
```

## Multi-Table

```python
from sdv.multi_table import HMA1Synthesizer

synth = HMA1Synthesizer(multi_table_metadata)
synth.fit(multi_table_data)
synthetic = synth.sample(scale=0.5)
```

## Privacy Evaluation

```python
from sdv.evaluation import evaluate

# Statistical similarity
report = evaluate(synthetic, data, metadata)
print(f"Overall score: {report.get_score():.3f}")
print(f"Column shapes: {report.get_property('Column Shapes'):.3f}")
print(f"Column pairs: {report.get_property('Column Pair Trends'):.3f}")
```

## References
- [SDV docs](https://docs.sdv.dev/sdv/)
- [SDV GitHub](https://github.com/sdv-dev/SDV)
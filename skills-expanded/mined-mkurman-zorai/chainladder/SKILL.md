---
name: chainladder
description: "Property & casualty insurance loss reserving in Python. Chain ladder, Bornhuetter-Ferguson, Cape Cod, bootstrap simulation, and loss development pattern estimation. Actuarial triangle operations."
tags: [insurance, actuarial, loss-reserving, chain-ladder, p-and-c, claims, zorai]
---
## Overview

ChainLadder implements actuarial reserve estimation methods for property & casualty insurance. Use it for loss reserving, claims triangles, and actuarial modeling in Python.

## Installation

```bash
uv pip install chainladder
```

## Basic Triangle and Reserve

```python
import chainladder as cl

# Load sample auto liability triangle
tri = cl.load_dataset("RAA")
print(tri)

# Select development pattern
dev = cl.Development().fit_transform(tri)

# Run chain ladder method
model = cl.ChainLadder().fit(dev)
print(model.reserve_)
print(model.ldf_)  # age-to-age factors
```

## Mack Bootstrap

```python
# Estimate reserve variability
mack = cl.MackChainLadder().fit(dev)
print(mack.reserve_)
print(f"CV: {mack.reserve_.std() / mack.reserve_.sum():.2%}")
print(mack.conditional_standard_error_)
```

## Bornhuetter-Ferguson

```python
bf = cl.BornhuetterFerguson().fit(dev)
print(bf.reserve_)
print(bf.expected_loss_)  # a priori expected loss
```

## References
- [ChainLadder docs](https://chainladder-python.readthedocs.io/)
- [CAS reserving principles](https://www.casact.org/)
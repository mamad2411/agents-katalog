---
name: data-ai
description: "Linux data science and AI/ML environment setup - TensorFlow, PyTorch, CUDA, Jupyter"
sasmp_version: "1.3.0"
bonded_agent: linux-expert
bond_type: PRIMARY_BOND
---

# Data Ai Skill

## Overview

Master Linux environment configuration for data science and machine learning workflows.

## Capabilities

- **GPU Setup**: CUDA, cuDNN, NVIDIA drivers
- **Python Environments**: Conda, virtualenv, pyenv
- **ML Frameworks**: TensorFlow, PyTorch, JAX
- **Data Tools**: Jupyter, pandas, numpy
- **Containerization**: Docker with GPU support

## Examples

```bash
# Check GPU availability
nvidia-smi

# Create ML environment
conda create -n ml python=3.11
conda activate ml
pip install torch torchvision
```


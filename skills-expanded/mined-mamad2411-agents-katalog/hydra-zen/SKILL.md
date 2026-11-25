---
name: hydra-zen
description: Pythonic config generation for Hydra (hydra-zen). Eliminates hand-written YAML by generating structured dataclass configs directly from Python objects and functions. Provides make_config, builds, zen, store, and launch utilities for configurable, reproducible, and scalable workflows. Use for typed experiment configuration, Hydra boilerplate reduction, and Python-first ML workflow design.
license: MIT license
tags: [structured-configs, hydra-boilerplate, dataclass-configs, experiment-config, hydra-zen]
metadata:
    skill-author: K-Dense Inc.
---

# hydra-zen

## Overview

hydra-zen is a Python-first layer on top of Hydra that removes most Hydra-specific boilerplate and eliminates hand-written YAML configs. It dynamically generates structured dataclass configs from functions, classes, and call signatures, then integrates them into Hydra workflows. Use this skill when you want typed, composable, reproducible experiment configuration without maintaining large YAML trees.

## When to Use This Skill

This skill should be used when:
- You want Hydra benefits without hand-writing YAML configs
- You need type-safe, dataclass-driven experiment configuration
- You want to generate configs directly from Python call signatures
- You want to reduce Hydra boilerplate in ML/research codebases
- You need Pythonic launch/store APIs for configurable workflows
- You are building reproducible training scripts with complex parameterization

## Core Capabilities

### 1. Installation

```bash
pip install hydra-zen
```

### 2. `builds()` — Generate Configs from Callables

```python
from hydra_zen import builds
from torch.optim import AdamW

AdamWConf = builds(AdamW, lr=1e-3, weight_decay=1e-2)

# AdamWConf is a dataclass config that Hydra can instantiate
```

You can create configs for:
- classes
- functions
- callables
- nested object graphs

### 3. `instantiate()` — Materialize from Config

```python
from hydra_zen import builds, instantiate
from torch.optim import AdamW

AdamWConf = builds(AdamW, lr=1e-3, weight_decay=1e-2)
optimizer = instantiate(AdamWConf)
```

### 4. `make_config()` — Typed Ad Hoc Configs

```python
from hydra_zen import make_config

TrainConfig = make_config(
    learning_rate=1e-3,
    batch_size=64,
    max_epochs=20,
    model_name="resnet50",
)

cfg = TrainConfig()
print(cfg.learning_rate)
```

Useful when you just need a typed config object without defining a full dataclass manually.

### 5. `store()` — Register Configs with Hydra

```python
from hydra_zen import store, builds
from torch.optim import AdamW, SGD

store(group="optimizer")(
    builds(AdamW, lr=1e-3),
    name="adamw"
)

store(group="optimizer")(
    builds(SGD, lr=0.1, momentum=0.9),
    name="sgd"
)
```

This gives you Hydra config-group behavior without maintaining YAML files.

### 6. `zen()` — Wrap Task Functions

```python
from hydra_zen import zen

def train(model, optimizer, epochs: int = 10):
    print(model, optimizer, epochs)

train_task = zen(train)
train_task(model="resnet50", optimizer="adamw", epochs=20)
```

`zen()` helps bridge normal Python functions and Hydra-configurable execution.

### 7. End-to-End Example

```python
from hydra_zen import builds, store, zen
from torch.optim import AdamW
from torchvision.models import resnet50

ModelConf = builds(resnet50, pretrained=False, num_classes=10)
OptimConf = builds(AdamW, lr=1e-3)

store(group="model", name="resnet50")(ModelConf)
store(group="optimizer", name="adamw")(OptimConf)

@zen
def train(model, optimizer, epochs=10):
    print("Model:", model)
    print("Optimizer:", optimizer)
    print("Epochs:", epochs)

if __name__ == "__main__":
    train.hydra_main(
        config_name=None,
        version_base="1.3",
    )
```

### 8. `launch()` — Programmatic Hydra Runs

```python
from hydra_zen import builds, launch

def train(lr: float, batch_size: int):
    return {"lr": lr, "batch_size": batch_size}

Conf = builds(train, lr=1e-3, batch_size=64)
job = launch(Conf)
print(job.return_value)
```

Useful for notebook workflows, testing, and programmatic sweep orchestration.

### 9. Nested Config Composition

```python
from hydra_zen import builds, instantiate
from torch.optim import AdamW
from torchvision.models import resnet18

ModelConf = builds(resnet18, num_classes=100)
OptimConf = builds(AdamW, lr=1e-4)

ExperimentConf = builds(
    dict,
    model=ModelConf,
    optimizer=OptimConf,
    seed=42,
    hydra_convert="all",
)

exp = instantiate(ExperimentConf)
print(exp["seed"])
```

### 10. ML Workflow Pattern

```python
from hydra_zen import builds, store, zen
from pytorch_lightning import Trainer

TrainerConf = builds(
    Trainer,
    max_epochs=50,
    accelerator="auto",
    devices=1,
)

store(group="trainer", name="default")(TrainerConf)

@zen
def run_training(trainer, model, datamodule):
    trainer.fit(model, datamodule)
```

This works especially well for:
- PyTorch Lightning
- optimizer / scheduler registries
- model family registries
- experiment launchers
- notebook-driven experimentation

## Key Patterns

1. **Prefer `builds()` over handwritten YAML** for Python-heavy projects.
2. **Use `store()` to recreate Hydra config groups** with less maintenance.
3. **Use `zen()` to wrap normal task functions** into config-driven workflows.
4. **Use `launch()` in tests/notebooks** when CLI Hydra feels heavy.
5. **hydra-zen shines when your source of truth is Python code**, not config files.

## References

- [hydra-zen documentation](https://mit-ll-responsible-ai.github.io/hydra-zen/)
- [API reference](https://mit-ll-responsible-ai.github.io/hydra-zen/api_reference.html)
- [PyTorch Lightning tutorial](https://mit-ll-responsible-ai.github.io/hydra-zen/tutorials/pytorch_lightning.html)
- [Repository](https://github.com/mit-ll-responsible-ai/hydra-zen)

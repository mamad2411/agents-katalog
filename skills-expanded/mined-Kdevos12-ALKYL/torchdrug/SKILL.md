---
name: torchdrug
description: Use when working with TorchDrug for graph-based drug discovery and molecular ML. Covers molecular property prediction, protein modeling, knowledge graph reasoning, molecular generation, retrosynthesis, and GNN architectures on chemical data.
---

# TorchDrug

PyTorch toolkit for drug discovery — graph neural networks on molecules, proteins, and biomedical knowledge graphs. 40+ datasets, 20+ model architectures, modular task/model interface.

## When to Use This Skill

- Predicting molecular properties (solubility, toxicity, BBB penetration, quantum chemistry)
- Protein function/stability/localization/interaction prediction
- Drug-target binding affinity (PDBBind, BindingDB)
- Knowledge graph completion and drug repurposing (Hetionet)
- De novo molecular generation and property optimization (GCPN, flows)
- Retrosynthesis planning (USPTO-50k, CenterIdentification + SynthonCompletion)
- Training GNNs (GCN, GAT, GIN, SchNet, GearNet, RGCN) on chemical data
- Transfer learning with pre-trained protein models (ESM, ProteinBERT)

## Quick Start

```python
from torchdrug import datasets, models, tasks
import torch
from torch.utils.data import DataLoader

# 1. Dataset
dataset = datasets.BBBP("~/datasets/")
train_set, valid_set, test_set = dataset.split()

# 2. Model
model = models.GIN(
    input_dim=dataset.node_feature_dim,
    hidden_dims=[256, 256, 256],
    edge_input_dim=dataset.edge_feature_dim,
    batch_norm=True, readout="mean"
)

# 3. Task
task = tasks.PropertyPrediction(
    model, task=dataset.tasks,
    criterion="bce", metric=["auroc", "auprc"]
)

# 4. Train
optimizer = torch.optim.Adam(task.parameters(), lr=1e-3)
for epoch in range(100):
    for batch in DataLoader(train_set, batch_size=32, shuffle=True):
        loss = task(batch)
        optimizer.zero_grad(); loss.backward(); optimizer.step()
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Data structures (Graph, Molecule, Protein), training loop, task/model interface | `references/core-data.md` |
| Molecular property prediction: datasets, tasks, model selection, training | `references/molecular-property.md` |
| Protein modeling: sequence & structure models, datasets, pre-training | `references/protein-modeling.md` |
| Knowledge graph completion, drug repurposing, Hetionet | `references/knowledge-graphs.md` |
| Molecular generation: GCPN, flows, property optimization | `references/molecular-generation.md` |
| Retrosynthesis: CenterIdentification, SynthonCompletion, USPTO-50k | `references/retrosynthesis.md` |
| Full model catalog: GCN, GAT, GIN, SchNet, GearNet, ESM, TransE, RotatE… | `references/models-reference.md` |

## Key Submodules

| Module | Role |
|--------|------|
| `torchdrug.data` | Graph, Molecule, Protein, PackedGraph |
| `torchdrug.datasets` | 40+ curated datasets |
| `torchdrug.models` | GNN, protein, KG embedding, generative models |
| `torchdrug.tasks` | PropertyPrediction, KGCompletion, Generation, Retrosynthesis |
| `torchdrug.transforms` | VirtualNode, VirtualEdge, TruncateProtein |
| `torchdrug.layers` | MessagePassingBase and building blocks |
| `torchdrug.core` | Configurable, Registry (serialization) |

## Installation

```bash
pip install torchdrug          # CPU / CUDA (uses system torch)
pip install torchdrug[full]    # with optional extras
```

```python
import torchdrug; print(torchdrug.__version__)  # verify
```

## Related Skills

- `rdkit` — molecular I/O, fingerprints, conformers before TorchDrug ingestion
- `deepchem` — alternative ML framework for drug discovery (TensorFlow/PyTorch)
- `scientific-skills:esm` — ESM protein language models (direct HuggingFace usage)

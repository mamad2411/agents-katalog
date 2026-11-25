---
name: dgl
description: "Deep Graph Library (DGL) — graph neural network framework. GCN, GAT, GraphSAGE, RGCN, and custom message-passing. Heterogeneous graphs, temporal graphs, and large-scale training with mini-batch sampling."
tags: [dgl, graph-neural-network, gnn, message-passing, deep-learning, python, zorai]
---
## Overview

Deep Graph Library (DGL) provides graph neural network implementations: GCN, GAT, GraphSAGE, GIN, RGCN, and custom message-passing. Supports heterogeneous graphs, temporal graphs, mini-batch training, and distributed sampling for large-scale graph learning.

## Installation

```bash
uv pip install dgl
```

## GCN for Node Classification

```python
import torch
import torch.nn.functional as F
from dgl.nn import GraphConv

class GCN(torch.nn.Module):
    def __init__(self, in_feats, hidden, out_feats):
        super().__init__()
        self.conv1 = GraphConv(in_feats, hidden)
        self.conv2 = GraphConv(hidden, out_feats)

    def forward(self, g, features):
        x = F.relu(self.conv1(g, features))
        x = self.conv2(g, x)
        return F.log_softmax(x, dim=1)
```

## Mini-Batch Training

```python
sampler = dgl.dataloading.NeighborSampler([10, 10])
train_dataloader = dgl.dataloading.DataLoader(
    g, train_nids, sampler,
    batch_size=1024, shuffle=True, num_workers=4)
```

## References
- [DGL docs](https://docs.dgl.ai/)
- [DGL GitHub](https://github.com/dmlc/dgl)
---
name: domain-graph
description: "Use for graph machine learning: node classification, link prediction, graph classification or regression, recommendation on graphs, molecule or network analysis, community detection, and graph anomaly detection with graph neural networks. Picks the GNN by task, enforces transductive vs inductive splits (a common leakage source), and uses graph metrics. Triggers on 'graph neural network', 'GNN', 'node classification', 'link prediction', 'knowledge graph', 'molecule', 'social network', 'GCN', 'GraphSAGE', 'GAT'."
---

# Graph ML - Method Selection

Use PyTorch Geometric (PyG) or DGL. GNNs need node features, so add structural features (degree, node2vec) when raw features are weak.

## Decision table
| Task | Recommended | Notes |
|---|---|---|
| Node classification, static graph | GCN (simple, strong baseline), then GAT | transductive; GCN is a remarkably strong baseline. |
| Large or industrial, or unseen nodes | GraphSAGE (inductive, neighbor sampling) | generalizes to nodes and graphs not seen in training. |
| Graph classification or regression | GIN (maximally expressive) with global pooling | molecules, program graphs. |
| Link prediction or graph recommendation | GraphSAGE or LightGCN with negative sampling | metrics are AUC or AP, and Hits@K or MRR. |
| Weak or missing features | add structural or node2vec features | GNNs underperform without informative features. |

## Cross-cutting practice
- Leakage (critical): be explicit about transductive (mask nodes within one graph) versus inductive (held-out nodes or graphs) evaluation. For link prediction, remove the test edges from the message-passing graph during training, otherwise the model sees the answer. For graph classification, split by graph.
- Metrics: node and graph classification use accuracy or macro F1 (macro when imbalanced); link prediction uses AUC or AP, Hits@K, MRR.
- Explainability: GNNExplainer or integrated gradients (which nodes and edges mattered), and attention weights for GAT.
- Recent options (2022-2024): Graph Transformers (Graphormer, GraphGPS, Exphormer). A 2024 reassessment shows well-tuned classic GNNs (GCN, GAT, GraphSAGE) match or beat them on most benchmarks, so tune the simple baseline before reaching for a transformer.
- Improve accuracy: use `accuracy-improvement-loop`; evaluate with `rigorous-evaluation`.

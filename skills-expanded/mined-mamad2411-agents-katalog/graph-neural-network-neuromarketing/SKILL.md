---
name: graph-neural-network-neuromarketing
description: Applies Graph Neural Networks (GCN, GAT, GraphSAGE) to EEG-based neuromarketing by modelling brain functional connectivity as graphs where electrodes are nodes and connectivity values are edges, enabling consumer choice prediction that captures inter-electrode interactions classical ML and CNN/LSTM models miss. Use when building neuromarketing classifiers from EEG data, when spectral features alone underfit minority-class purchase decisions, or when modelling brain connectivity rather than time-series power. NOT for eye-tracking-only studies, fMRI voxel-level models, or when interpretability requires path-weights/Shapley analysis (use concept2brain-predictive-neural-response-model or forward-prediction-neuromarketing-framework).
---

# Graph Neural Network Neuromarketing

## Overview

Graph Neural Networks (GNNs) bring a topology-aware paradigm to EEG-based consumer choice prediction: electrodes become graph nodes and functional-connectivity coefficients become weighted edges, allowing the model to learn the interactions between brain regions that time-domain or spectral-feature approaches flatten. The approach is especially valuable for minority-class (purchase) prediction where classical models collapse to the majority (no-purchase) class.

## When to Use

- Building an EEG-based neuromarketing classifier and the minority "buy" class recall is poor with classical or CNN/LSTM models
- Wanting to model functional brain connectivity (inter-electrode correlations) rather than per-channel power spectra
- Comparing GNN architectures (GCN, GAT, GraphSAGE, ResidualGCN, DeepGNN) on a neuromarketing benchmark
- Extending the existing AI-neuromarketing-synergy-framework or hybrid-eeg-gaze-decoding-scheme with a graph-based EEG branch
- NOT for eye-tracking-only consumer models — use multimodal-eeg-eye-tracking-consumer-choice
- NOT for fMRI voxel-level studies — use concept2brain-predictive-neural-response-model
- NOT when full interpretability via Shapley/path-weights is required — use forward-prediction-neuromarketing-framework

## Core Process / Workflow

### 1. Construct the brain connectivity graph

- **Nodes**: EEG electrodes (19 in the NeuMa 10-20 layout).
- **Edges**: Pearson correlation between spectral-feature vectors of electrode pairs, forming a fully-connected weighted adjacency matrix W ∈ [0,1].
- **Node features**: Spectral features per electrode (FFT + Welch PSD across delta, theta, alpha, beta, gamma bands; statistical descriptors: mean, std, skewness, kurtosis).

### 2. Select GNN architecture

| Architecture | Strength | When to choose |
|---|---|---|
| BaselineGCN | Simple spectral propagation | Fast baseline |
| BaselineGAT | Multi-head attention on important edges | When edge importance varies |
| GraphSAGE | Neighbourhood sampling | Large graphs, scalability |
| ResidualGCN | Skip connections for gradient flow | Deeper models, best overall accuracy |
| DeepGNN | Hierarchical parallel GCN+GAT+SAGE | Highest representational capacity |
| BalancedGAT | Compact attention model | Best minority-class recall |

### 3. Train and evaluate

- Cross-validation: K-fold stratified (5-fold in Afshar & Azimi 2025).
- Optimizer: AdamW (lr=0.001, weight_decay=0.01).
- Scheduler: ReduceLROnPlateau (factor=0.5, patience=5).
- Loss: class-weighted cross-entropy (addresses class imbalance).
- Metrics: Accuracy, Precision, Recall, F1 (weighted — critical for imbalanced "buy"/"no-buy" tasks).

### 4. Interpret the decision rules

- Classical models (Random Forest, SVM-RBF) achieve higher overall accuracy but collapse on the minority class (Class 1 Recall ≈ 0.01-0.18).
- GNNs trade some overall accuracy (0.62-0.69) for substantially better minority recall (up to 0.54 with BalancedGAT).
- The trade-off: choose classical for majority-class tasks, GNN for detecting the rare "buy" signal.

## A-Tech Application Matrix

### A-Coder (developer tool)
- Federated code-pattern preference prediction using GNN over developer brain connectivity (experimental, privacy-preserving).

### Be Practical (education)
- Curriculum module: "Graph Neural Networks for Brain Data" — when topology beats time-series.

### Builder's Club (community)
- Open-source benchmark: GNN architectures on the open NeuMa dataset for reproducible neuromarketing research.

## References

- See [references/gnn-neuromarketing-evidence-base.md](references/gnn-neuromarketing-evidence-base.md) for the full evidence base.
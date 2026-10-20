---
name: hybrid-eeg-gaze-graph-signal-neuromarketing
description: Applies hybrid EEG graph signal processing and gaze dynamic patterning for consumer purchase intent classification, achieving superior Cohen's kappa and F1-score over traditional neuromarketing approaches. Use when building multimodal neuromarketing systems that fuse EEG brain connectivity with eye-tracking behavioral data, when designing subject-specific consumer decision decoders, or when evaluating graph signal processing approaches for EEG-based consumer behavior prediction.
---

# Hybrid EEG Gaze Graph Signal Neuromarketing

## Overview

Applies the hybrid decoding scheme (Kalaganis et al., Brain Informatics, September 2025) that fuses Graph Fourier Transform (GFT)-based EEG features with eye-tracking behavioral and marketing descriptors for consumer purchase intent classification. The GFT_hybrid approach outperforms traditional neuromarketing indices and simple fusion methods, achieving statistically significant improvements in both Cohen's kappa (κ≈0.35, fair-to-moderate range) and F1-score (≈0.54) on the open NeuMa dataset.

## When to Use

- Building multimodal neuromarketing systems that fuse EEG with eye-tracking data
- Designing subject-specific consumer decision decoders for realistic shopping scenarios
- Evaluating graph signal processing (GFT) approaches for EEG-based consumer behavior
- When traditional neuromarketing indices (approach-withdrawal, mental workload) underperform
- When subject variability in EEG makes population-level models unreliable
- NOT for: situations where only a single modality (EEG or eye-tracking alone) is available
- NOT for: laboratory settings that do not simulate realistic purchase scenarios

## The Core Contribution

### The Problem with Traditional Neuromarketing Indices

Traditional EEG-based neuromarketing relies on handcrafted indices:
- **Approach-Withdrawal (AW)**: Alpha hemispheric asymmetry in prefrontal cortex
- **Mental Workload**: Theta activation in prefrontal/frontal regions
- **Memorization**: Memory-related brain activity
- **Attention/Engagement**: Inter-subject correlation

These indices:
1. May not capture the complex neural activity during realistic marketing stimuli
2. Vary significantly across subjects (high subject variability)
3. Cannot pinpoint which specific elements of stimuli captured attention
4. Fail to model inter-channel brain connectivity

### The GFT_hybrid Solution

The hybrid scheme combines:
1. **EEG branch**: Graph Fourier Transform (GFT) on brain connectivity graphs
   - Electrodes as nodes, envelope correlation as weighted edges
   - GFT projects EEG signals onto graph eigenvectors
   - Power per eigenmode as feature
2. **Eye-tracking branch**: Behavioral (Hjorth parameters) + marketing descriptors
   - Hjorth: Activity, Mobility, Complexity of gaze trajectory
   - Marketing: fixation count, fixation duration, time to first fixation, dwell time, blink rate
3. **Early fusion**: Concatenation of GFT-EEG and ET features
4. **Personalized classification**: Per-subject Linear SVM with Wilcoxon feature selection

## Key Empirical Results

### Classification Performance (NeuMa Dataset, 42 participants)

| Method | Cohen's κ | F1-score |
|--------|-----------|----------|
| EEG_indices (traditional) | ~0.05 (slight) | ~0.31 |
| ET_indices (eye-tracking only) | ~0.25 (fair) | ~0.48 |
| Hybrid_indices (simple fusion) | ~0.25 (fair) | ~0.48 |
| GFT_EEG (GFT only) | ~0.18 (fair) | ~0.44 |
| **GFT_hybrid (proposed)** | **~0.35 (fair-to-moderate)** | **~0.54** |

- GFT_hybrid outperforms all competing approaches with statistical significance (Wilcoxon signed-rank test, p < 0.05)
- κ improvement: +0.08 to +0.30 over baselines
- F1 improvement: +0.06 to +0.23 over baselines

### Physiological Findings

1. **Connectivity beyond frontal asymmetry**: Strong couplings between prefrontal and occipital cortices, not just the commonly reported frontal dipoles
2. **Subject-specific connectivity**: Most salient functional connections varied across individuals; only a limited subset shared among subjects
3. **Behavioral eye-tracking patterns**: ~80% of "Buy" condition behavioral features fall in the lower-value octant (reduced mobility, activity, complexity) — indicating gaze stabilization on intended purchase

### Key Insight
Eye-tracking descriptors are more reliable than EEG indices because they capture phenomena directly related to the stimulus (fixations, dwell time), while brain processes are more complex and cannot be quantified via simple power-based estimators.

## Core Process / Workflow

### 1. Data Acquisition (NeuMa Protocol)
```
Participants: 42 healthy adults (23M, 19F, age 31.5±8.84)
Task: Browse digital supermarket brochure (6 pages, 24 products/page)
Selection: Click products intended to purchase
EEG: 19 dry electrodes (10-20 system), 300 Hz
Eye-tracking: Tobii Pro Fusion, 120 Hz
Segmentation: Per-product gaze-defined epochs (>0.5s)
Labels: "Buy" (clicked) vs "NoBuy" (not clicked)
```

### 2. EEG Graph Construction
```
1. Filter EEG to 8-30 Hz (alpha + beta bands)
2. Compute envelope correlation between all electrode pairs
   ρ^{m,n} = |ρ(A_m(t), A_n(t))|  (Hilbert transform envelopes)
3. Construct weighted adjacency matrix W (19×19)
4. Compute graph Laplacian: L = D - W
5. Eigenanalysis: U = [u_0, u_1, ..., u_{18}], λ_k
6. Apply GFT: X̃ = U^T X
7. Extract power per eigenmode: p(m) = (1/T) Σ |X̃(m,t)|²
```

### 3. Eye-Tracking Feature Extraction
```
Behavioral (Hjorth parameters on gaze trajectory):
  Activity = var(x(t))                    # trajectory length
  Mobility = sqrt(var(dx/dt) / var(x))    # speed changes
  Complexity = mobility(dx/dt) / mobility(x)  # motion irregularity

Marketing descriptors:
  - Number of fixations
  - Duration of fixations
  - Time to first fixation
  - Dwell time
  - Blink rate
```

### 4. Fusion and Classification
```
1. Concatenate GFT-EEG features + ET features (early fusion)
2. Per-subject Leave-One-epoch-Out Cross Validation (LOOCV)
3. Wilcoxon statistic feature selection (train set only)
4. Linear SVM classification
5. Evaluate with Cohen's kappa and F1-score
```

## A-Tech Application Matrix

### A-Coder
- **Application**: Developer engagement prediction from behavioral + physiological signals
- **Privacy-first adaptation**: Replace EEG with session engagement metrics; replace eye-tracking with dwell time and scroll velocity
- **GFT insight**: Model developer interaction patterns as graphs (file dependencies, navigation patterns)

### Be Practical
- **Curriculum**: Multimodal neuromarketing with graph signal processing
- **Practical focus**: How GFT captures brain connectivity that traditional indices miss
- **Open-source tools**: NeuMa dataset, PyTorch Geometric, GFT implementations

### Builder's Club
- **Open-source toolkit**: GFT-based consumer intent decoder
- **Community benchmark**: NeuMa dataset as standardized evaluation
- **Privacy-first adaptation**: Behavioral proxy translation table for on-device implementation

## The Privacy-First A-Tech Adaptation

| Original Signal | On-Device Behavioral Proxy | Privacy Property |
|-----------------|---------------------------|------------------|
| EEG frontal asymmetry | Session engagement duration, feature adoption rate | Computed locally |
| EEG graph connectivity | Navigation pattern graph (page/file transitions) | Local computation |
| Eye-tracking fixation | Dwell time, scroll velocity, replay rate | Standard analytics |
| Gaze trajectory Hjorth | Mouse/touch trajectory Hjorth parameters | Local computation |
| Blink rate | Session interruption frequency | Behavioral only |

## Cross-References

- `graph-neural-network-neuromarketing` — GNNs for EEG consumer choice; this skill uses GFT (graph signal processing) rather than GNNs but on the same NeuMa dataset
- `multimodal-eeg-eye-tracking-consumer-choice` — Consolidates six multimodal studies; this skill adds the GFT approach as a seventh method
- `hybrid-eeg-gaze-decoding-scheme` — The original skill this extends; this skill adds the GFT method and graph connectivity analysis
- `neuromarketing-ai-cxm-integration-framework` — The CXM framework this GFT approach could feed into
- `neuro-marketing-privacy-first-behavioral-analytics` — The privacy-first adaptation pattern

## Limitations

- The NeuMa dataset is limited to 42 participants; generalization requires larger studies
- The supermarket brochure task is specific; other purchase scenarios may produce different connectivity patterns
- EEG cannot detect deep brain structures (hippocampus, limbic system) due to limited spatial resolution
- Subject-specific models require per-subject calibration; population-level generalization remains challenging
- The GFT approach has lower overall accuracy than classical ML but better minority-class (purchase) recall
- Online real-time implementation requires a calibration session for graph construction

## A-Tech Alignment

- **Open-source AI**: NeuMa dataset is publicly available; PyTorch, scikit-learn, standard libraries
- **Data privacy**: On-device behavioral proxy adaptation eliminates biometric surveillance
- **Financial freedom**: Open dataset and tools enable SME access without lab equipment
- **Practical implementation**: Reproducible on the open NeuMa benchmark with documented protocol

## References

- See [references/evidence-base.md](references/evidence-base.md) for full methodology, results tables, and physiological findings.
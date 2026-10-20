---
name: multimodal-eeg-eye-tracking-consumer-choice
description: Predicts consumer purchase decisions by fusing EEG neural signals with eye-tracking visual attention data using deep learning (CNN-LSTM, InceptionTime, TCN+attention) and stacking ensembles, achieving 84-89% accuracy on the open NeuMa benchmark. Use when building a consumer choice classifier that must capture both subconscious neural engagement and overt visual attention, when single-modality models underperform, or when designing a multimodal neuromarketing pipeline for ad pre-testing. NOT for graph-connectivity-only EEG models (use graph-neural-network-neuromarketing), synthetic neural response generation (use concept2brain-predictive-neural-response-model), or behavioural-only transaction prediction (use large-behavior-model-retail-customer).
---

# Multimodal EEG + Eye-Tracking Consumer Choice Prediction

## Overview

Combining EEG (subconscious neural engagement) with eye-tracking (overt visual attention) yields consumer choice classifiers that outperform either modality alone. The 2025-2026 wave of multimodal neuromarketing models on the open NeuMa benchmark achieves 84-89% accuracy using CNN-LSTM, InceptionTime+CatBoost, and TCN+multi-head-attention architectures, with fixation duration emerging as the single strongest predictor and modality dropout preventing the model from over-relying on the easier eye-tracking signal.

## When to Use

- Building a consumer purchase-intent classifier and single-modality (EEG-only or ET-only) accuracy is insufficient
- Designing a multimodal neuromarketing pipeline for pre-launch ad or product testing
- Wanting to quantify the relative contribution of neural engagement vs visual attention to purchase decisions
- Implementing the fusion paradox fix (modality dropout) when one modality dominates learning
- Extending ai-neuromarketing-synergy-framework with a concrete multimodal implementation
- NOT for EEG graph-connectivity-only models — use graph-neural-network-neuromarketing
- NOT for synthetic neural response generation — use concept2brain-predictive-neural-response-model
- NOT for behavioural transaction-only prediction — use large-behavior-model-retail-customer

## Core Process / Workflow

### 1. Data acquisition and synchronisation

- **EEG**: 19-21 channels (10-20 system), 300 Hz; bandpass Butterworth 0.5-45 Hz; ASR + FORCe artifact removal.
- **Eye-tracking**: gaze coordinates + pupil dilation, 120 Hz; linear interpolation for blink gaps.
- **Synchronisation**: epoch by gaze-on-product intervals; discard epochs < 0.5 s; label by mouse-click "buy" events.
- **Class imbalance**: SMOTE on the minority "buy" class (typical 20% buy / 80% no-buy).

### 2. Feature extraction

| Modality | Handcrafted | Deep-learned |
|---|---|---|
| EEG | Statistical (mean, variance, skewness, kurtosis), Welch PSD, DWT coefficients | CNN-LSTM embeddings (64-128 dim) |
| ET | Fixation duration, fixation count, saccade amplitude, dwell time, time-to-first-fixation, blink rate, Hjorth parameters (activity, mobility, complexity) | LeNet-5 embeddings on gaze-plot images |

### 3. Fusion strategy

- **Early fusion** (Mallick et al. 2026): concatenate EEG (19 ch) + ET (6 ch) into 25-channel input → InceptionTime (parallel kernels 10/20/40) → 128-dim embedding + 44 time-domain statistics → CatBoost.
- **Feature-level fusion** (Usman et al. 2025): concatenate handcrafted + deep features per modality → stacking ensemble (RF + GB + XGB base, RF meta).
- **Modality dropout** (Mallick et al. 2026): randomly zero eye-tracking channels with 30% probability during training to force robust EEG representation learning (prevents the "fusion paradox").

### 4. Model selection

| Model | Accuracy | F1 | Key innovation |
|---|---|---|---|
| Stacking ensemble (Usman 2025) | 84.01% | 0.83 | RF+GB+XGB base, RF meta; handcrafted+DL features |
| InceptionTime+CatBoost (Mallick 2026) | 77.51% | 0.75 | Multi-scale temporal convolutions; modality dropout; grokking-oriented training |
| TCN + multi-head attention (Koduru 2026) | 89.2% | — | EEG+ET+GSR trimodal; gamma-band power + pupil dilation strongest predictors |
| GFT + SVM hybrid (Kalaganis 2025) | κ=0.35 | 0.54 | Graph Fourier Transform on EEG connectivity + ET behavioural features |

### 5. Predictor ranking

Across studies, the strongest predictors of purchase intent:
1. **Fixation duration** (β=0.38, strongest single predictor; Iyappan et al. 2025, N=285)
2. **Frontal alpha asymmetry** (β=0.31; approach motivation)
3. **Number of fixations** (β=0.21)
4. **Frontal beta activity** (β=0.18; cognitive arousal)
5. **Gamma-band power (30-45 Hz)** during product exposure (Koduru et al. 2026)
6. **Pupil dilation change** (Koduru et al. 2026)

## A-Tech Application Matrix

### A-Coder (developer tool)
- Multimodal developer-state detection: EEG + gaze → flow-state classification for adaptive intervention.

### Be Practical (education)
- Curriculum: "Multimodal Neuromarketing Pipelines" — from single-modality baselines to fusion architectures.

### Builder's Club (community)
- Open-source multimodal benchmark on NeuMa; community challenge for beating 89% accuracy.

## References

- See [references/multimodal-consumer-choice-evidence-base.md](references/multimodal-consumer-choice-evidence-base.md) for the full evidence base.
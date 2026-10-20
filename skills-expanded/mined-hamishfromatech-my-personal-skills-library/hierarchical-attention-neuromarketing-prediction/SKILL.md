---
name: hierarchical-attention-neuromarketing-prediction
description: Applies Hierarchical Attention-based Deep Neural Networks (HA-DNN) to fuse EEG neural biomarkers with social-media sentiment for predicting individual purchasing decisions, achieving 86.7% accuracy and AUC 0.91. Use when integrating neural and social signals for consumer behavior prediction, building multimodal neuromarketing models, or evaluating whether social sentiment adds value beyond neural signals alone. NOT for single-modality neuromarketing (EEG-only or sentiment-only) or for real-time inference where latency constraints preclude deep models.
---

# Hierarchical Attention Neuromarketing Prediction

## Overview

A Hierarchical Attention-based Deep Neural Network (HA-DNN) fuses EEG neural biomarkers (engagement, workload, valence) with social-media sentiment analysis to predict individual purchasing decisions with 86.7% accuracy (AUC 0.91), substantially outperforming social-media-only models (71.2%) and neural-only models (78.4%). The hierarchical attention mechanism learns which features matter most at each decision stage, providing interpretability alongside prediction.

## When to Use

- Integrating neural signals (EEG) with social-media sentiment for consumer behavior prediction
- Building multimodal neuromarketing models that combine biometric and social data
- Evaluating whether social sentiment adds predictive value beyond neural signals (it does: +8.3pp)
- Designing attention-based architectures for multimodal consumer analytics
- NOT for single-modality prediction (EEG-only or sentiment-only)
- NOT for real-time inference where model latency is critical
- NOT without ethical guardrails for neural data collection and sentiment scraping

## Core Process / Workflow

### 1. Data acquisition

**Neural data (EEG)**:
- 250 participants, multimodal biometric (EEG, eye tracking, GSR)
- Exposure to 12 products
- Extract: frontal asymmetry of alpha activity, theta/beta ratio, late positive potential

**Social media sentiment**:
- 5 million messages from social networks regarding the 12 products
- Sentiment analysis (VADER or transformer-based)
- Aggregate sentiment scores per product

### 2. Feature engineering

| Modality | Features |
|---|---|
| EEG | Frontal alpha asymmetry, theta/beta ratio, late positive potential, engagement, workload, valence |
| Social sentiment | Product-level sentiment scores, sentiment polarity, sentiment volume, temporal sentiment trends |

### 3. Model architecture (HA-DNN)

```
Input layer:
  ├── EEG feature branch → dense + attention
  └── Sentiment feature branch → dense + attention
  
Hierarchical attention:
  ├── Modality-level attention (learns EEG vs sentiment weighting)
  └── Feature-level attention (learns which features matter per modality)
  
Fusion layer → dense → output (purchase probability)
```

The hierarchical attention mechanism provides two levels of interpretability:
1. **Modality-level**: which input modality is weighted more for a given prediction
2. **Feature-level**: which specific features within each modality drive the prediction

### 4. Training and evaluation

- Train on combined EEG + sentiment features
- Compare against unimodal baselines (EEG-only, sentiment-only)
- Report accuracy, AUC, and attention weights for interpretability

## Key Empirical Findings

| Model | Accuracy | AUC |
|---|---|---|
| **HA-DNN (EEG + sentiment)** | **86.7%** | **0.91** |
| Neural-only (EEG) | 78.4% | ~0.85 |
| Social-media-only (sentiment) | 71.2% | ~0.77 |

**Key insight**: Social sentiment adds +8.3pp over neural-only, confirming that multimodal fusion captures complementary information. The two modalities provide partially overlapping but distinct predictive signals.

### Attention weight analysis

The hierarchical attention mechanism reveals:
- EEG engagement and valence receive highest feature-level attention
- Social sentiment volume and polarity receive moderate attention
- Modality-level attention shifts based on product category (high-involvement products → more EEG weight; low-involvement → more sentiment weight)

## A-Tech Applications

- **A-Coder**: Developer engagement prediction from behavioral signals (typing, scroll, commit cadence) fused with team sentiment (Slack, PR comments); the HA-DNN architecture transfers to developer analytics
- **Be Practical**: Curriculum on multimodal neuromarketing; teach that neural + social fusion > either alone
- **Builder's Club**: Open-source HA-DNN implementation for multimodal consumer prediction; the architecture is domain-independent

## Cross-References

- `predictive-neuromarketing-bayesian-framework` — Bayesian/predictive-coding framework; HA-DNN provides the implementation architecture
- `customer-digital-twin-neuromarketing` — Customer digital twins fusing EEG + sentiment; HA-DNN is the prediction engine
- `multimodal-eeg-eye-tracking-consumer-choice` — Multimodal EEG + eye-tracking; this skill adds social sentiment as a third modality
- `ai-enhanced-neuromarketing-social-media` — AI-enhanced neuromarketing for social media; HA-DNN provides the prediction model
- `forward-prediction-neuromarketing-framework` — Forward-prediction framework; HA-DNN is a forward-prediction implementation

## References

- Ravi & Seetharaman (Zenodo, 2026-05-27) — "Neuromarketing and Predictive Consumer Behavior Modeling Using Social Media Sentiment and Deep Learning Techniques"
- 250 participants, EEG + eye tracking + GSR, 5M social messages, 12 products
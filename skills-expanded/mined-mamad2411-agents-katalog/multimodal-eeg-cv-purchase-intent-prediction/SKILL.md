---
name: multimodal-eeg-cv-purchase-intent-prediction
description: Applies a hybrid Temporal Convolutional Network (TCN) and Graph Attention Network (GAT) model combining EEG neuromarketing signals with computer vision visual attention features for consumer purchase intent prediction. Use when designing multimodal neuromarketing systems, predicting purchase decisions from neurophysiological data, or building privacy-first consumer behavior analytics with open-source EEG tools.
---

# Multimodal EEG-CV Purchase Intent Prediction

## Overview
A hybrid two-branch deep learning architecture combining EEG frontal asymmetry/theta-beta ratio/LPP features with computer vision fixation density/saccade dynamics/pupil size to predict consumer purchase intent at 88.3% accuracy, outperforming unimodal approaches.

## When to Use
- Designing multimodal neuromarketing systems that combine brain signals with visual attention
- Predicting purchase decisions from neurophysiological consumer data
- Building privacy-first consumer analytics with open-source/consumer-grade EEG
- Evaluating e-commerce product images using subliminal neural response data
- Comparing unimodal vs hybrid prediction approaches for consumer behavior

## NOT for...
- Traditional survey-based market research (this is neuroscience-based)
- Real-time adaptive advertising without offline model training
- Applications requiring fMRI-grade spatial resolution (EEG has limited deep-brain sensitivity)

## Core Process / Workflow

1. **Data Collection**: Record EEG (frontal asymmetry, theta/beta ratio, late positive potential) and eye-tracking (fixation density, saccade dynamics, pupil size) simultaneously while participants view e-commerce product images
2. **EEG Feature Extraction (TCN Branch)**: Process EEG signals through Temporal Convolutional Network capturing temporal dependencies in neural responses
3. **Visual Attention Feature Extraction (GAT Branch)**: Map visual attention features using Graph Attention Network representing spatial relationships between fixation points
4. **Hybrid Fusion**: Concatenate TCN and GAT feature vectors for joint representation
5. **Classification**: Train binary classifier (buy vs. no-buy) on fused features
6. **Evaluation**: Compare hybrid model accuracy against unimodal EEG (74.2%) and unimodal visual (72.8%) baselines

### Key Architecture Details
- Dataset: 120 participants, 500 e-commerce images
- EEG features: frontal asymmetry of alpha activity, theta/beta ratio, late positive potential
- Visual features: fixation density, saccade dynamics, pupil size
- Hybrid accuracy: 88.3%, AUC = 0.94
- Unimodal EEG: 74.2% accuracy
- Unimodal visual: 72.8% accuracy

## References
- See [references/evidence-base.md](references/evidence-base.md) for detailed methodology and results.
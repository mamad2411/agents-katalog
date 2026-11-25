---
name: hybrid-eeg-gaze-decoding-scheme
description: A multimodal decoding scheme for classifying consumer purchase intent ("Buy" vs "NoBuy") using simultaneous EEG and eye-tracking data. Integrates Graph Signal Processing (GFT) on EEG functional connectivity with Hjorth behavioral descriptors and marketing eye-tracking metrics from gaze data. Use when building neuromarketing intent classifiers, designing multimodal physiological decoding, optimizing hybrid fusion schemes, or translating subject-specific brain connectivity into privacy-safe behavioral proxies. NOT for the emotion-attention-memory triad framework (use ai-neuromarketing-synergy-framework), the Bayesian predictive-coding model (use predictive-neuromarketing-bayesian-framework), or the single-variable purchase-intent predictor hierarchy (use neuromarketing-predictive-purchase-intent-model).
---

# Hybrid EEG-Gaze Decoding Scheme

## Overview

A 2025 study (Kalaganis et al., Brain Informatics, September 2025) introduces a hybrid decoding scheme that classifies consumer intent in a binary decision-making scenario ("Buy" vs "NoBuy") using simultaneous EEG and eye-tracking data. The framework integrates Graph Signal Processing (GFT)-based features derived from EEG functional connectivity with descriptive statistics from eye movement patterns (Hjorth parameters + marketing eye-tracking metrics). In a realistic supermarket brochure browsing task (NeuMa dataset, 42 participants), the hybrid GFT approach outperformed all competing single-modal and naive-fusion baselines, with statistically significant improvements in both Cohen's kappa (κ ≈ 0.35) and F1-score (≈ 0.54).

The study's central contribution: typical neuromarketing EEG indices (approach-withdrawal, mental workload, memorization) are insufficient to capture the complex neural activity during realistic marketing stimuli. More sophisticated representations — specifically graph-based functional connectivity — are essential. And the combination of brain signals with gaze behavior is what unlocks accurate prediction; neither modality alone is enough.

## When to Use

- Building a neuromarketing intent classifier that predicts purchase decisions from physiological signals
- Designing multimodal (EEG + eye-tracking) decoding pipelines for consumer behavior
- Implementing Graph Signal Processing (GFT) for EEG functional connectivity analysis
- Optimizing feature fusion schemes (early fusion of brain + gaze features)
- Translating subject-specific brain connectivity patterns into privacy-safe behavioral proxies
- Evaluating whether traditional neuromarketing indices (approach-withdrawal, mental workload) are sufficient for your use case
- Designing personalized, subject-specific decoders that account for high EEG variability

NOT for:
- The emotion-attention-memory triad framework — use `ai-neuromarketing-synergy-framework`
- The Bayesian predictive-coding mathematical framework — use `predictive-neuromarketing-bayesian-framework`
- The single-variable purchase-intent predictor hierarchy — use `neuromarketing-predictive-purchase-intent-model`
- The 3×3 consumer-journey framework — use `neuromarketing-consumer-journey-3x3-framework`
- Privacy-first behavioral analytics architecture — use `neuro-marketing-privacy-first-behavioral-analytics`

## The Core Problem

Most neuromarketing studies rely on handcrafted EEG indices:
- **Approach-Withdrawal (AW):** Alpha hemispheric asymmetry in (pre)frontal cortex; positive = approach, negative = withdrawal
- **Mental Workload:** Theta band power ratio in (pre)frontal areas; or alpha desynchronization over parietal lobe
- **Memorization Index:** Inter-subject correlation at population level
- **Attention/Engagement Index:** Inter-subject correlation

These indices examine only very specific phenomena and brain patterns. They may not capture the complex neural activity that takes place during exposure to realistic marketing stimuli. The decision-making process is multi-factorial, utilizing brain areas beyond those studied in typical neuromarketing schemes, and it varies significantly across individuals.

## The Hybrid GFT Solution

### Component 1: EEG — Graph Fourier Transform (GFT)

**Graph construction:**
- Nodes = EEG electrodes (19-channel Wearable Sensing DSI 24, 10-20 system)
- Edges = envelope correlation between electrode signals (Hilbert transform → Pearson correlation of envelopes)
- Graph Laplacian L = D − W (degree matrix minus weighted adjacency matrix)
- Eigenanalysis: eigenvectors U, eigenvalues λ ordered ascending

**Feature extraction:**
1. Bandpass filter EEG to 8–30 Hz (alpha + beta)
2. Compute envelope correlation weighted adjacency matrix W
3. Apply GFT: X̃ = U^T X (project multichannel EEG to graph Fourier domain)
4. Compute power per eigenmode: p(m) = (1/T) Σ |X̃(m,t)|²
5. Mean power across segments belonging to same epoch → feature vector

**Key finding:** The most salient functional connections varied across individuals. Only a limited subset was shared among subjects. The most consistent coupling was ⟨Fp1, Fp2⟩ (prefrontal asymmetry), but strong couplings also appeared between prefrontal and occipital cortices — connections not studied in typical neuromarketing schemes.

### Component 2: Eye-Tracking — Behavioral + Marketing Features

**Behavioral features (Hjorth parameters on accumulated eye distance):**
- **Activity:** Total power of signal; linked to overall trajectory length
- **Mobility:** Mean frequency estimate; mirrors changes in speed of eye motion
- **Complexity:** Bandwidth; captures irregularities in motion

**Key finding:** ~80% of "Buy" condition ocular responses fall in the octant of lower values for each subject — reduced mobility, activity, and complexity during "Buy" (gaze stabilization on intended product).

**Marketing features (per product):**
1. Number of fixations
2. Duration of fixations
3. Time to first fixation
4. Dwell time
5. Blink rate (stress indicator)

### Component 3: Fusion + Classification

```
For each product (epoch):
  1. Extract GFT features from EEG (8-30 Hz band)
  2. Extract Hjorth behavioral features + marketing metrics from eye-tracking
  3. Normalize and average across segments (handle varying epoch duration)
  4. Concatenate into single vector (early fusion)
  5. Wilcoxon-based feature selection (train set only)
  6. Train Linear SVM (per subject, Leave-One-epoch-Out CV)
  7. Predict Buy vs NoBuy
```

## Performance Results

| Method | Cohen's κ (avg) | F1-score (avg) | Interpretation |
|---|---|---|---|
| **GFT_hybrid (proposed)** | **~0.35** | **~0.54** | Upper fair range |
| GFT_EEG (EEG only) | ~0.18 | ~0.31 | Slight range |
| ET_indices (eye-tracking only) | ~0.27 | ~0.48 | Fair range |
| Hybrid_indices (naive fusion) | ~0.25 | ~0.43 | Fair range |
| EEG_indices (traditional) | ~0.05–0.10 | ~0.31 | Near chance |

**Key insights:**
- Eye-tracking features carry more predictive power than EEG under this framework
- But only the combination achieves accurate classification — neither alone is sufficient
- GFT applied to EEG significantly outperforms traditional neuromarketing indices
- Traditional AW/mental workload indices may produce negative κ values for some subjects (worse than chance)
- Subject variability is high — personalized decoders are essential

## Physiological Findings

### Brain connectivity (graph analysis):
- **Consistent coupling:** ⟨Fp1, Fp2⟩ — prefrontal asymmetry (well-documented in decision-making)
- **Beyond prefrontal:** Numerous connections originating from prefrontal area to other regions
- **Subject-specific:** The most prominent connections varied across subjects; only a small portion common
- **Implication:** Decision-making is multi-factorial, engaging brain areas beyond those in typical neuromarketing schemes

### Eye-tracking behavior:
- **"Buy" condition:** ~80% of behavioral features (activity, mobility, complexity) in lower-value octant → gaze stabilization on intended product
- **"NoBuy" condition:** Features span the full range → no stabilization pattern
- **Limitation:** The "Buy" low-value cluster overlaps with some "NoBuy" samples → limited discriminative power alone

## Privacy-First Translation

| Lab Signal | GFT/Behavioral Feature | Privacy-First Proxy | A-Tech Application |
|---|---|---|---|
| EEG functional connectivity (GFT eigenmodes) | Per-subject connectivity pattern | Session-specific interaction graph (feature → feature co-occurrence) | A-Coder usage pattern decoding |
| EEG prefrontal asymmetry (Fp1-Fp2 coupling) | Approach-withdrawal index | Task initiation vs abandonment rate | Be Practical engagement direction |
| Eye-tracking fixation count | Marketing metric | Element interaction count | A-Coder feature engagement |
| Eye-tracking dwell time | Marketing metric | Time-on-page, time-on-element | Be Practical content depth |
| Eye-tracking time-to-first-fixation | Marketing metric | Time-to-first-interaction | Onboarding speed |
| Hjorth Activity (trajectory length) | Behavioral descriptor | Total navigation distance (clicks, scrolls) | Session breadth |
| Hjorth Mobility (speed change) | Behavioral descriptor | Interaction rate acceleration | Engagement momentum |
| Hjorth Complexity (motion irregularity) | Behavioral descriptor | Interaction pattern irregularity | Decision uncertainty |
| Blink rate (stress) | Marketing metric | Input pause frequency, error rate | Cognitive load indicator |

## A-Tech Applications

### A-Coder
- Build a subject-specific interaction graph (features as nodes, co-usage as edges)
- Apply GFT to identify which feature combinations drive adoption decisions
- Fuse with eye-tracking proxies (dwell time on documentation, feature interaction count)
- Predict "Adopt" vs "Skip" for each feature

### Be Practical
- Track learner gaze proxies (chapter dwell time, exercise retry patterns)
- Build a per-learner connectivity graph (concept → concept co-engagement)
- Predict "Continue" vs "Abandon" for each learning module
- Use Hjorth descriptors to detect when a learner is stabilizing on a concept (low mobility = comprehension)

### Builder's Club
- Community member interaction graph (contribution → contribution co-occurrence)
- GFT to identify community decision-making patterns
- Eye-tracking proxies: dwell time on community posts, return visit patterns
- Predict "Contribute" vs "Lurk" for each member

## Implementation Notes

### Technical requirements
- EEG: 19+ channels, 300 Hz sampling, 8-30 Hz bandpass
- Eye-tracking: 120 Hz, gaze coordinate data
- Preprocessing: Artifact Subspace Reconstruction (ASR) + FORCe for EEG artifact removal; linear interpolation for eye-tracking missing values
- Epoching: Gaze-defined epochs (time intervals where gaze is within product boundaries); discard epochs < 0.5s

### Why GFT over Riemannian geometry
- Riemannian geometry approaches yielded similar results to GFT for EEG-only
- But Riemannian structure cannot be directly combined with eye-tracking features (different mathematical structure)
- GFT produces vector features compatible with early fusion → hybrid scheme possible

### Why personalized decoders
- EEG has high subject variability
- Functional connectivity patterns are largely subject-specific
- Group-level models would lose the individual signal
- Leave-One-epoch-Out Cross Validation (LOOCV) per subject

## Limitations and Future Directions

- **Online implementation:** Feasible due to low computational complexity; requires small calibration session for graph formulation; data buffer needed for eye-tracking feature completion
- **Multi-layer graphs:** Could cover multiple frequency bands for wider brain phenomena coverage → potentially subject-independent decoding
- **Deep learning:** If subject consistency achieved, DL architectures with GFT concepts could further improve performance
- **Sample size:** 42 participants; larger validation needed
- **Ecological validity:** Supermarket brochure browsing is more realistic than lab ads but still not real-world purchasing

## References

- See [references/hybrid-eeg-gaze-evidence-base.md](references/hybrid-eeg-gaze-evidence-base.md) for the full study details, NeuMa dataset description, mathematical formulation, per-subject results table, and cross-references to adjacent skills.
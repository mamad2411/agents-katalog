---
name: predictive-neuromarketing-bayesian-framework
description: Applies a Bayesian Brain and predictive-coding framework to neuromarketing, formalizing how marketing stimuli shape consumer expectations, brand priors, price cues, and prediction errors. Use when designing marketing strategies grounded in computational neuroscience, when explaining price placebo effects or brand-identity modulation, when building neuroforecasting models for advertising, or when integrating EEG-based preference prediction into a mechanistic framework. NOT for tactical ad-copy generation without a theoretical basis, or for neuromarketing measurement-only approaches that lack a generative computational model.
---

# Predictive Neuromarketing: Bayesian & Predictive-Coding Framework

## Overview
This skill applies the Bayesian Brain and predictive-coding frameworks — which conceptualize perception, learning, and decision-making as hierarchical prediction-error minimization — to consumer neuroscience, providing the first unified computational theory for neuromarketing. It transforms neuromarketing from a descriptive measurement discipline into a mechanistic, testable science.

## When to Use
- Designing marketing strategies that need a computational grounding beyond heuristics
- Explaining price placebo effects, brand-identity modulation, or EEG-based preference prediction
- Building neuroforecasting models for advertising success
- Integrating disparate neuromarketing findings (price, brand, emotion, reward) into a single generative model
- Teaching or communicating the theoretical foundations of neuromarketing to technical audiences
- Evaluating whether a neuromarketing claim is consistent with predictive-coding principles
- NOT for tactical ad-copy or creative production without a theoretical layer
- NOT for neuromarketing approaches that only measure brain activity without a generative model

## Core Process / Workflow

### 1. Frame the Marketing Stimulus as a Precision-Weighted Prediction Error

Predictive coding holds that the brain continually generates predictions about sensory inputs at each hierarchical level and updates those predictions by minimizing precision-weighted prediction errors. Marketing stimuli do not simply "trigger responses" — they generate prediction errors that the brain resolves by updating its generative model.

```
Prediction Error = (Actual Signal) − (Predicted Signal)
Precision Weight = how much attention/weight the brain assigns to this error signal
```

To design a marketing intervention under this framework:

1. **Identify the prior**: What does the consumer's generative model already predict? (e.g., "this brand is premium," "this price is fair," "this product will feel good")
2. **Generate a controlled prediction error**: Introduce a stimulus that violates the prior in a targeted way (e.g., an unexpectedly low price for a premium brand creates a positive price prediction error)
3. **Manage precision**: Ensure the prediction error is weighted highly enough to drive belief updating (salience, attention, emotional arousal increase precision) but not so high that it triggers rejection or cognitive defense
4. **Allow belief updating**: The prediction error propagates upward through the hierarchy, updating the consumer's brand priors, price expectations, and valuation

### 2. Map the Four Key Computational Constructs to Marketing Variables

| Computational Construct | Marketing Variable | Example |
|---|---|---|
| Brand prior | Pre-existing brand expectation | "Apple products are well-designed" |
| Price cue | Expected vs. actual price | $999 anchor → $799 actual = positive prediction error |
| Prediction error (signed) | Surprise (positive or negative) | Unexpected quality at a low price |
| Precision weight | Attention, emotional salience, sensory engagement | High-quality visuals + music increase precision of the error signal |

### 3. Apply the Framework to Explain Classic Neuromarketing Phenomena

**Price placebo effect**: Price acts as a prior that shapes the expected value of a product. A higher price sets a higher expected value prior. The actual consumption experience is then evaluated relative to that prior. When the experience matches the high-price prior, the brain confirms the value; when it exceeds it, a positive prediction error reinforces the brand. This explains why the same product "works better" at a higher price — the price cue is a self-fulfilling prior.

**Brand-identity modulation**: A strong brand sets a rich, high-precision prior that colors perception of all subsequent stimuli. Brand exposure before product evaluation reduces the weight of new sensory prediction errors because the prior is already high-precision. This explains why familiar brands feel "safe" and why brand-stripped blind tests produce different results.

**EEG-based preference prediction**: Neural signals (frontal alpha asymmetry, late positive potential) reflect the brain's prediction-error response to stimuli. Forward-encoding models can predict these neural responses from stimulus features, enabling neuroforecasting of advertising success without needing to decode "what the brain is doing" in reverse.

### 4. Design a Predictive-Neuromarketing Experiment

```
1. Hypothesis: Marketing stimulus X creates prediction error of sign Y at precision Z, updating brand prior W
2. Measure: EEG (prediction error signals), behavioral choice, self-report
3. Manipulate: Prior strength (brand exposure vs. no exposure), prediction error magnitude (expected vs. unexpected price), precision (high vs. low attention)
4. Predict: Prediction error magnitude × precision interaction drives belief updating and choice
5. Test: Compare to a model where prediction errors are not precision-weighted (should underperform)
```

### 5. Ethical Guardrails

Predictive neuromarketing is powerful because it operates on the generative model that underlies perception itself. Ethical use requires:

- **Transparency about prediction-error manipulation**: Consumers should not have their priors updated without awareness of the commercial intent
- **Avoiding precision hijacking**: Techniques that artificially inflate precision (e.g., exploiting anxiety, scarcity, or neurological vulnerabilities) to force belief updating are manipulative
- **Consent for neural measurement**: EEG, eye-tracking, or biometric data collection requires explicit, informed consent
- **The Utilitarian Test**: Does the prediction-error manipulation create genuine consumer value, or does it merely exploit a computational vulnerability?

## References
- See [references/predictive-neuromarketing-evidence-base.md](references/predictive-neuromarketing-evidence-base.md) for the mathematical framework, experimental paradigms, and cross-references.
---
name: information-symmetry-decision-architecture
description: Applies the information-symmetry principle discovered by D'Ambrogio et al. (Nature Neuroscience, June 2026) to design choice environments that align with how the brain actually values information. The brain seeks balance across alternatives (information symmetry) rather than minimizing uncertainty per option. Use when designing product comparison interfaces, recommendation systems, choice architectures, evaluation workflows, or any environment where people gather information before deciding; when optimizing A/B test design for cognitive accuracy; when building AI agents that gather information on behalf of users.
---

# Information Symmetry Decision Architecture

## Overview
Research from Oxford (D'Ambrogio, Grohn, Khalighinejad, Mattar, Hunt & Rushworth, Nature Neuroscience, June 2026) discovered that humans seek information symmetry across alternatives rather than minimizing uncertainty option-by-option. The brain balances knowledge across options, and this principle — extracted via symbolic regression from a trained neural network — predicts behavior more accurately than standard uncertainty-based models and generalizes to entirely different tasks.

## When to Use
- Designing product comparison interfaces or recommendation engines
- Building choice architectures for evaluation workflows
- Optimizing information-gathering UX for decisions
- Designing AI agent information-gathering strategies
- Creating progressive disclosure systems that respect cognitive economics
- Building A/B test frameworks that account for how the brain actually samples

- NOT for single-option evaluation contexts (symmetry requires ≥2 alternatives)
- NOT for n-armed bandit optimization directly (the symbolic equations are tailored to 2-option structure)
- NOT as a replacement for standard RL algorithms without adaptation

## Core Process / Workflow

### 1. Identify the Decision Context
Map any information-gathering workflow to a two-alternative (or reducible to two) decision structure.

### 2. Compute Value of Information (VoI)
Use the recovered symbolic equations to model how the brain values information:

**Value of Staying:**
```
V_stay = β₁ + exp(-|β₂| × N_attended / N_unattended)
```

**Value of Switching:**
```
V_switch = β₃ + exp(-|β₄| × log(2 × N_unattended) / N_attended)
```

Where:
- N_attended = evidence collected from currently attended option
- N_unattended = evidence collected from the alternative
- β₁ = attentional inertia (baseline tendency to stay)
- β₂ = information satiation (rate accumulated evidence reduces staying)
- β₃ = undirected exploration (baseline tendency to switch)
- β₄ = directed exploration (rate learning about current option increases switching interest)

### 3. Design for Symmetry
Build information-gathering interfaces that present information in a way that allows the user to balance knowledge across options rather than drilling deep into one before considering alternatives.

### 4. Validate with Neural Signatures
The model predicts neural activity:
- **VTA:** Arbitrates between sampling and choosing (opposed coding of VoI and VoS)
- **ACC and AI:** Track value-of-information computations
- **Frontal midline theta:** Reflects precision weighting and uncertainty

## Key Findings

### The Information-Symmetry Principle
- Participants value sampling based on relative evidence accumulated across options (Na/Nu), not absolute uncertainty per option
- The ratio is scale-invariant: 100:10 and 10:1 both yield Na/Nu = 10
- This contradicts UCB-style models that compute per-option uncertainty

### Symbolic Regression Recovery
- A 4-parameter symbolic expression was recovered from a 7,592-parameter ANN
- The symbolic model performs comparably to the full ANN in predicting both behavior and neural activity
- Generalizes to an independent two-armed bandit dataset (n=89)

### Neural Correlates
- **VTA activity:** Opposed coding of information value (negative) and selection value (positive) — suited to arbitrating sampling vs. choosing
- **ACC and AI:** Track value-of-information computations
- **SN:** Tracks overall potential for information gain and relative informational value
- **Dorsolateral PFC:** Regulates precision, attention, and uncertainty

## Applications

### A-Coder (A-Tech Coding Assistant)
- Design code completion suggestions that balance evidence across multiple candidate solutions
- Build documentation discovery that presents information symmetrically across alternatives
- Optimize refactoring decision interfaces for information-symmetry-aligned sampling

### Be Practical (A-Tech Learning Platform)
- Structure learning paths that allow learners to balance evidence across concepts before committing
- Design comparison interfaces for course/lesson selection that respect the symmetry principle
- Build adaptive content that adjusts evidence presentation based on accumulated knowledge ratios

### Builder's Club (A-Tech Community)
- Design contributor onboarding that presents community options symmetrically
- Build project discovery that balances evidence across alternatives
- Create decision-support tools for community governance that align with neural information valuation

## References
- See [references/information-symmetry-evidence-base.md](references/information-symmetry-evidence-base.md) for details.
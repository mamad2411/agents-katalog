---
name: information-theory
description: "Shannon entropy, mutual information, channel capacity, source coding theorem, rate-distortion, and error-correcting codes"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/information-theory/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Information Theory

## Scope
Information theory quantifies the storage, transmission, and processing of information, setting fundamental limits on compression and communication.

## Core Formulations
- **Shannon Entropy**: $H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)$ (bits).
- **Kullback-Leibler Divergence (Relative Entropy)**:
  $$D_{KL}(P \parallel Q) = \sum_x P(x) \log_2 \frac{P(x)}{Q(x)}$$
- **Mutual Information**: $I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$.
- **Shannon Channel Capacity**: $C = \max_{p(x)} I(X; Y)$; AWGN channel: $C = B \log_2\left(1 + \frac{S}{N}\right)$.

## Tools & References
- **Canonical References**: Cover & Thomas — *Elements of Information Theory*; MacKay — *Information Theory, Inference, and Learning Algorithms*.

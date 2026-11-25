---
name: real-analysis
description: "Metric spaces, sequences, Bolzano-Weierstrass, continuity, Riemann-Stieltjes integration, and measure theory"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/real-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Real Analysis

## Scope
Real analysis deals with the real numbers and real-valued functions of a real variable, providing rigorous foundational proofs for limits, continuity, derivatives, and integrals.

## Core Formulations
- **Completeness Axiom**: Every non-empty subset of $\mathbb{R}$ bounded above has a least upper bound (supremum).
- **$\epsilon-\delta$ Formalism**:
  $$\lim_{x \to c} f(x) = L \iff \forall \epsilon > 0, \exists \delta > 0 \text{ s.t. } 0 < |x - c| < \delta \implies |f(x) - L| < \epsilon$$
- **Bolzano-Weierstrass Theorem**: Every bounded sequence in $\mathbb{R}^n$ has a convergent subsequence.
- **Lebesgue Dominated Convergence Theorem**: If $f_n \to f$ pointwise and $|f_n| \le g$ with $g \in L^1$, then $\lim \int f_n = \int f$.

## Tools & References
- **Canonical References**: Rudin — *Principles of Mathematical Analysis* ("Baby Rudin"); Royden & Fitzpatrick — *Real Analysis*.

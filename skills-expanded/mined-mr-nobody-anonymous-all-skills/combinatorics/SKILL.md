---
name: combinatorics
description: "Permutations, combinations, generating functions, recurrence relations, Ramsey theory, and extremal combinatorics"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/combinatorics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Combinatorics

## Scope
Combinatorics studies discrete structures, counting techniques, arrangements, configurations, and extremal set systems.

## Core Formulations
- **Binomial Coefficients**: $\binom{n}{k} = \frac{n!}{k!(n-k)!}$.
- **Inclusion-Exclusion Principle**:
  $$\left|\bigcup_{i=1}^n A_i\right| = \sum_i |A_i| - \sum_{i < j} |A_i \cap A_j| + \dots + (-1)^{n-1} \left|\bigcap_{i=1}^n A_i\right|$$
- **Generating Functions**: Ordinary generating function $G(x) = \sum a_n x^n$; Exponential generating function $E(x) = \sum a_n \frac{x^n}{n!}$.
- **Pigeonhole Principle & Ramsey's Theorem**: Guarantees order in sufficiently large structures ($R(3,3)=6$).

## Tools & References
- **Canonical References**: Stanley — *Enumerative Combinatorics* (Vols. 1-2); Graham, Knuth & Patashnik — *Concrete Mathematics*.

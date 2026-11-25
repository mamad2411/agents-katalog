---
name: number-theory
description: "Prime numbers, modular arithmetic, Diophantine equations, multiplicative functions, and cryptography foundations"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/number-theory/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Number Theory

## Scope
Number theory is devoted primarily to the study of integers and integer-valued functions, arithmetic properties, prime distribution, and computational number theory.

## Formulations & Theorems
- **Division Algorithm & Euclidean Algorithm**: $\gcd(a, b) = a x + b y$ (Bézout's identity).
- **Euler's Totient & Fermat's Little Theorem**:
  - If $\gcd(a, m) = 1$, then $a^{\phi(m)} \equiv 1 \pmod{m}$.
  - For prime $p$: $a^{p-1} \equiv 1 \pmod{p}$.
- **Chinese Remainder Theorem (CRT)**: Unique solution modulo $\prod m_i$ for pairwise coprime moduli.
- **Quadratic Reciprocity**: Gauss's law for Legendre symbols $\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2}\frac{q-1}{2}}$.
- **Riemann Zeta Function & Prime Number Theorem**: $\pi(x) \sim \frac{x}{\ln x}$.

## Tools & References
- **Software**: PARI/GP, SageMath, FLINT.
- **Canonical References**: Ireland & Rosen — *A Classical Introduction to Modern Number Theory*; Hardy & Wright.

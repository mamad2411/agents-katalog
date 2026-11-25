---
name: complex-analysis
description: "Holomorphic functions, Cauchy-Riemann equations, contour integration, Cauchy residue theorem, and conformal mapping"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/complex-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Complex Analysis

## Scope
Complex analysis investigates functions of complex numbers, analyticity, singularities, conformal transformations, and contour integration.

## Core Formulations
- **Cauchy-Riemann Equations**: For $f(z) = u(x,y) + i v(x,y)$ to be holomorphic:
  $$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \quad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$
- **Cauchy's Integral Formula**:
  $$f^{(n)}(z_0) = \frac{n!}{2\pi i} \oint_C \frac{f(z)}{(z - z_0)^{n+1}} dz$$
- **Residue Theorem**:
  $$\oint_C f(z) dz = 2\pi i \sum_{k} \operatorname{Res}(f, z_k)$$

## Tools & References
- **Canonical References**: Ahlfors — *Complex Analysis*; Conway — *Functions of One Complex Variable*.

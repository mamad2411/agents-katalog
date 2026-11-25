---
name: analytical-mechanics
description: "Lagrangian and Hamiltonian dynamics, variational calculus, D'Alembert's principle, Poisson brackets, and Hamilton-Jacobi theory"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/analytical-mechanics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Analytical Mechanics

## Scope
Analytical mechanics reformulates classical mechanics using energy scalars rather than force vectors, utilizing generalized coordinates, variational calculus, and phase space transformations.

## Formulations & Formalisms
- **Hamilton's Principle (Least Action)**:
  $$\delta S = \delta \int_{t_1}^{t_2} L(q, \dot{q}, t) dt = 0$$
- **Euler-Lagrange Equations**:
  $$\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_i}\right) - \frac{\partial L}{\partial q_i} = 0$$
- **Hamilton's Canonical Equations**: $H(q, p, t) = \sum p_i \dot{q}_i - L$, with $\dot{q}_i = \frac{\partial H}{\partial p_i}$, $\dot{p}_i = -\frac{\partial H}{\partial q_i}$.
- **Poisson Brackets**: $\{f, g\} = \sum \left( \frac{\partial f}{\partial q_i}\frac{\partial g}{\partial p_i} - \frac{\partial f}{\partial p_i}\frac{\partial g}{\partial q_i} \right)$, $\frac{df}{dt} = \{f, H\} + \frac{\partial f}{\partial t}$.
- **Noether's Theorem**: Every continuous symmetry of the action corresponds to a conserved quantity (time invariance $\implies$ energy, spatial translation $\implies$ momentum).

## Tools & References
- **Software**: SymPy (`sympy.physics.mechanics`), Mathematica.
- **Canonical References**: Goldstein, Poole & Safko — *Classical Mechanics*; Arnold — *Mathematical Methods of Classical Mechanics*.

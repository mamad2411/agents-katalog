---
name: numerical-analysis-foundations
description: "Floating point, conditioning, stability, convergence, error budgets, choosing a scheme."
---

# Numerical analysis foundations

- State the **problem class** (root-finding, IVP, BVP, eigenvalue, optimization, quadrature) before picking a method.
- Discuss **conditioning vs stability** explicitly: a stable algorithm on an ill-conditioned problem still loses digits.
- Pick the order of convergence you actually need; quote the cost.
- For floating-point work, watch catastrophic cancellation, subtraction near equal values, and accumulated round-off.
- Always include a **convergence check** (refine the grid / shrink the step) and an **error estimate** before quoting a number.

---
name: structural-analysis
description: "Direct stiffness method, matrix structural analysis, moment distribution (Hardy Cross), influence lines, and finite element modeling"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/structural-analysis/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Structural Analysis

## Scope
Structural analysis calculates internal forces (bending moments, shears, axials, torques) and displacements throughout a structure under applied loading conditions.

## Methods & Matrix Formulations
- **Direct Stiffness Method**:
  $$\mathbf{K} \mathbf{d} = \mathbf{F}$$
  where $\mathbf{K} = \sum \mathbf{T}^T \mathbf{k}_e \mathbf{T}$ is the global structure stiffness matrix, $\mathbf{d}$ nodal displacement vector, $\mathbf{F}$ applied nodal force vector.
- **Frame Element Stiffness Matrix** ($6 \times 6$ in 2D):
  Contains axial terms ($EA/L$) and flexural terms ($12EI/L^3, 6EI/L^2, 4EI/L, 2EI/L$).
- **Virtual Work Principle**: External virtual work equals internal virtual strain energy: $1 \cdot \Delta = \int \frac{M m}{EI} dx$.
- **Müller-Breslau Principle**: The influence line for any force response function is given by the deflected shape of the structure when the restrained restraint is released and subjected to a unit displacement.

## Tools & Standards
- **Software**: MASTAN2, OpenSees, SAP2000.
- **Canonical References**: Kassimali — *Matrix Analysis of Structures*; McGuire, Gallagher & Ziemian.

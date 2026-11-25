---
name: topology
description: "Point-set and algebraic topology: open/closed sets, continuity, compactness, connectedness, fundamental group, homology"
category: mathematics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mathematics/topology/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Topology

## Scope
Topology studies properties of spaces that are preserved under continuous deformations. This skill covers point-set topology foundations, algebraic topology invariants, and applications.

## Point-Set Topology

### Topological Spaces
- **Definition**: A set X with a collection τ of open sets satisfying: ∅, X ∈ τ; arbitrary unions are in τ; finite intersections are in τ
- **Metric topology**: Open sets defined by ε-balls: B(x,ε) = {y : d(x,y) < ε}
- **Basis**: Collection B such that every open set is a union of basis elements
- **Subspace topology**: τ_Y = {U ∩ Y : U ∈ τ}

### Continuity
- f: X → Y is **continuous** iff f⁻¹(U) is open for every open U ⊂ Y
- **Homeomorphism**: Continuous bijection with continuous inverse — topological equivalence
- Topological invariants: Properties preserved under homeomorphism

### Key Properties
| Property | Definition | Preserved by? |
|----------|-----------|---------------|
| Compactness | Every open cover has finite subcover | Continuous maps |
| Connectedness | Cannot be split into two disjoint open sets | Continuous maps |
| Path-connectedness | Any two points joined by continuous path | Continuous maps |
| Hausdorff (T₂) | Distinct points have disjoint neighborhoods | Subspaces |

- **Heine-Borel**: In ℝⁿ, compact ⟺ closed and bounded
- **Intermediate Value Theorem**: Continuous image of connected space is connected
- **Tychonoff's Theorem**: Product of compact spaces is compact

## Algebraic Topology

### Fundamental Group π₁(X, x₀)
- Elements: Homotopy classes of loops based at x₀
- Operation: Path concatenation
- **Simply connected**: π₁ = {e} (trivially, no "holes")
- **Examples**: π₁(S¹) ≅ ℤ, π₁(T²) ≅ ℤ × ℤ, π₁(S²) = {e}
- **van Kampen's theorem**: Compute π₁ of unions from components

### Homology Groups
- Hₙ(X) — captures n-dimensional "holes"
- H₀ counts connected components
- H₁ ≅ π₁^(ab) (abelianization of fundamental group)
- H₂ detects enclosed cavities
- **Euler characteristic**: χ = Σ(-1)ⁿ rank(Hₙ) = V - E + F (for surfaces)

### Covering Spaces
- **Definition**: p: X̃ → X where each point has evenly covered neighborhood
- **Lifting**: Paths and homotopies lift uniquely (given starting point)
- **Classification**: Connected coverings of X correspond to subgroups of π₁(X)

## Applications
- **Topological data analysis (TDA)**: Persistent homology for shape analysis of point clouds
- **Physics**: Topological insulators, Berry phase, defect classification
- **Computer science**: Simplicial complexes for sensor networks
- **Robotics**: Configuration spaces, motion planning

## Computational Tools
- **GUDHI (Python/C++)**: Persistent homology and TDA
- **Ripser**: Fast Vietoris-Rips persistent homology
- **SageMath**: Algebraic topology computations
- **SnapPy**: 3-manifold topology (hyperbolic geometry)

## References
- Munkres — *Topology* (2nd ed.)
- Hatcher — *Algebraic Topology* (free online)
- Ghrist — *Elementary Applied Topology*

---
name: statistical-mechanics
description: "Ensembles, partition functions, Boltzmann distribution, phase transitions, and connections to thermodynamics"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/statistical-mechanics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Statistical Mechanics

## Scope
Statistical mechanics bridges microscopic physics (atoms, molecules) with macroscopic observables (temperature, pressure, entropy) through probability and statistics. It provides the foundation for thermodynamics from first principles.

## Fundamental Concepts

### Microstates and Macrostates
- **Microstate**: A specific microscopic configuration (e.g., position and momentum of every particle)
- **Macrostate**: A set of macroscopic observables (T, P, V, N, E)
- **Fundamental postulate**: For an isolated system in equilibrium, all accessible microstates are equally probable

### Boltzmann Entropy
S = k_B ln Ω
where Ω = number of microstates, k_B = 1.381 × 10⁻²³ J/K

## Statistical Ensembles

### Microcanonical (NVE)
- Fixed: N, V, E. Isolated system.
- Ω(E) = number of states with energy E
- S = k_B ln Ω(E)
- Temperature: 1/T = ∂S/∂E

### Canonical (NVT)
- Fixed: N, V, T. System in contact with heat bath.
- **Partition function**: Z = Σᵢ exp(-Eᵢ/k_BT) = Σᵢ exp(-βEᵢ) where β = 1/k_BT
- Probability of state i: Pᵢ = exp(-βEᵢ)/Z (Boltzmann distribution)
- **Thermodynamic connection**:
  - Free energy: F = -k_BT ln Z
  - Energy: ⟨E⟩ = -∂(ln Z)/∂β
  - Entropy: S = -∂F/∂T = k_B(ln Z + β⟨E⟩)
  - Heat capacity: Cᵥ = ∂⟨E⟩/∂T = k_Bβ²⟨(ΔE)²⟩

### Grand Canonical (μVT)
- Fixed: μ (chemical potential), V, T. System exchanges particles and energy.
- **Grand partition function**: Ξ = Σ_N Σᵢ exp(-β(Eᵢ - μN))
- Grand potential: Ω = -k_BT ln Ξ = -PV

## Key Distributions
- **Maxwell-Boltzmann** (classical): f(v) = 4π n (m/2πk_BT)^(3/2) v² exp(-mv²/2k_BT)
  - Mean speed: ⟨v⟩ = √(8k_BT/πm)
  - RMS speed: v_rms = √(3k_BT/m)
- **Bose-Einstein** (bosons): ⟨nᵢ⟩ = 1/[exp(β(εᵢ-μ)) - 1]
- **Fermi-Dirac** (fermions): ⟨nᵢ⟩ = 1/[exp(β(εᵢ-μ)) + 1]

## Phase Transitions
- **Order parameter**: Quantity that is zero in disordered phase, non-zero in ordered (e.g., magnetization)
- **Critical exponents**: M ~ |T-Tc|^β, χ ~ |T-Tc|^(-γ), C ~ |T-Tc|^(-α)
- **Universality**: Critical exponents depend only on dimensionality and symmetry, not microscopic details
- **Mean-field theory**: Replace fluctuations with averages — gives qualitative behavior but wrong exponents
- **Renormalization group**: Systematic framework for phase transitions and critical phenomena

## Computational Methods
- Monte Carlo (Metropolis algorithm) for sampling configurations
- Molecular dynamics for time evolution
- Wang-Landau algorithm for density of states
- Transfer matrix method for 1D/2D lattice models

## Tools
- **Python**: `scipy.stats`, custom MC implementations
- **LAMMPS**: MD with statistical mechanics analysis
- **Monte Carlo codes**: Custom or domain-specific (e.g., CASINO for quantum MC)

## Standards & References
- Pathria & Beale — *Statistical Mechanics* (4th ed.)
- Sethna — *Statistical Mechanics: Entropy, Order Parameters, and Complexity*
- Kardar — *Statistical Physics of Particles*

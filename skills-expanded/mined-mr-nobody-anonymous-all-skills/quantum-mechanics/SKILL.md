---
name: quantum-mechanics
description: "Wave functions, Schrödinger equation, operators, measurement, spin, perturbation theory, and quantum information"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/quantum-mechanics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Quantum Mechanics

## Scope
Quantum mechanics describes physics at atomic and subatomic scales where classical mechanics fails. This skill covers the mathematical formalism, solution techniques, approximation methods, and modern quantum information concepts.

## Foundational Framework

### Postulates
1. **State**: A quantum system is described by a state vector |ψ⟩ in a Hilbert space
2. **Observables**: Physical quantities are represented by Hermitian operators
3. **Measurement**: Measuring observable A yields eigenvalue aₙ with probability |⟨aₙ|ψ⟩|²
4. **Collapse**: After measurement yielding aₙ, the state collapses to |aₙ⟩
5. **Time evolution**: iℏ ∂|ψ⟩/∂t = H|ψ⟩ (Schrödinger equation)

### Key Relations
- **de Broglie**: λ = h/p
- **Heisenberg Uncertainty**: ΔxΔp ≥ ℏ/2, ΔEΔt ≥ ℏ/2
- **Commutator**: [x̂, p̂] = iℏ

## The Schrödinger Equation

### Time-Independent (TISE)
Ĥψ = Eψ where Ĥ = -ℏ²/(2m)∇² + V(r)

### Exactly Solvable Systems
| System | Energy Levels | Wave Functions |
|--------|--------------|----------------|
| Infinite well (width L) | Eₙ = n²π²ℏ²/(2mL²) | ψₙ = √(2/L) sin(nπx/L) |
| Harmonic oscillator | Eₙ = (n + ½)ℏω | Hermite polynomials × Gaussian |
| Hydrogen atom | Eₙ = -13.6 eV/n² | Rₙₗ(r) × Yₗₘ(θ,φ) |

### Approximation Methods
- **Perturbation theory (time-independent)**: E⁽¹⁾ = ⟨ψ⁰|H'|ψ⁰⟩ (first-order energy correction)
- **Variational method**: E_ground ≤ ⟨ψ_trial|H|ψ_trial⟩/⟨ψ_trial|ψ_trial⟩
- **WKB**: Semi-classical approximation for slowly varying potentials
- **Time-dependent perturbation theory**: Fermi's Golden Rule for transition rates

## Angular Momentum & Spin
- **Orbital**: L̂² |l,m⟩ = ℏ²l(l+1)|l,m⟩, L̂_z|l,m⟩ = ℏm|l,m⟩
- **Spin-½**: σₓ, σᵧ, σ_z (Pauli matrices), |↑⟩ = (1,0)ᵀ, |↓⟩ = (0,1)ᵀ
- **Addition**: |j₁-j₂| ≤ j ≤ j₁+j₂ using Clebsch-Gordan coefficients

## Quantum Information
- **Qubit**: |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1
- **Entanglement**: Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
- **Quantum gates**: Hadamard H, Pauli X/Y/Z, CNOT, Toffoli
- **No-cloning theorem**: Cannot copy an arbitrary quantum state

## Computational Tools
- **Qiskit** (IBM): Quantum circuit simulation and real hardware access
- **QuTiP**: Quantum Toolbox in Python for open quantum systems
- **PennyLane**: Differentiable quantum computing
- **VASP/Gaussian/Q-Chem**: Ab initio quantum chemistry
- **Quantum ESPRESSO**: Plane-wave DFT for solids

## Standards & References
- Griffiths & Schroeter — *Introduction to Quantum Mechanics* (3rd ed.)
- Sakurai & Napolitano — *Modern Quantum Mechanics*
- Cohen-Tannoudji — *Quantum Mechanics* (Vols. 1-3)
- Nielsen & Chuang — *Quantum Computation and Quantum Information*

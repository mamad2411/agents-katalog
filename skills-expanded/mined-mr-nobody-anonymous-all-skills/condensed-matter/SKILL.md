---
name: condensed-matter
description: "Crystal structure, band theory, semiconductors, superconductivity, magnetism, and modern quantum materials"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/condensed-matter/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Condensed Matter Physics

## Scope
Condensed matter physics studies the properties of solid and liquid phases arising from the collective behavior of many interacting particles. This skill covers crystal structure, electronic band theory, semiconductors, superconductivity, and magnetism.

## Crystal Structure
- **Bravais lattices**: 14 in 3D (cubic: SC, BCC, FCC; plus tetragonal, orthorhombic, etc.)
- **Miller indices**: (hkl) planes, [hkl] directions
- **Reciprocal lattice**: b₁ = 2π(a₂×a₃)/(a₁·(a₂×a₃))
- **Bragg's Law**: 2d sin θ = nλ (X-ray diffraction condition)
- **Structure factor**: F(hkl) = Σⱼ fⱼ exp(-2πi(hxⱼ + kyⱼ + lzⱼ))

## Electronic Band Theory
- **Bloch's theorem**: ψₖ(r) = eⁱᵏ·ʳ uₖ(r) where u has lattice periodicity
- **Band gap**: Energy gap between valence and conduction bands
  - Metals: Bands overlap or partially filled
  - Semiconductors: Eg ~ 0.1-4 eV (Si: 1.12 eV, GaAs: 1.42 eV)
  - Insulators: Eg > 4 eV
- **Effective mass**: 1/m* = (1/ℏ²)(d²E/dk²)
- **Density of states**: g(E) ∝ √(E - Eₑdge) (3D, parabolic band)
- **Fermi-Dirac distribution**: f(E) = 1/[exp((E-μ)/kT) + 1]

## Semiconductors
- **Intrinsic**: n = p = nᵢ = √(NcNv) exp(-Eg/2kT)
- **Doping**: n-type (donors, e.g., P in Si), p-type (acceptors, e.g., B in Si)
- **p-n junction**: Built-in potential V₀ = (kT/e)ln(NₐNd/nᵢ²)
- **I-V characteristic**: I = I₀[exp(eV/nkT) - 1] (Shockley equation)

## Superconductivity
- **BCS theory**: Cooper pairs (electron-phonon interaction), energy gap Δ(T)
- **Critical temperature**: Tc (e.g., Nb: 9.3K, YBCO: 93K, H₃S: 203K under pressure)
- **Meissner effect**: Complete expulsion of magnetic flux below Tc
- **London equation**: ∇²B = B/λ² (penetration depth λ)
- **Type I vs Type II**: Type II has mixed state with Abrikosov vortex lattice (Hc1 < H < Hc2)

## Magnetism
- **Diamagnetism**: χ < 0, induced opposing moment (all materials)
- **Paramagnetism**: χ > 0, Curie law: χ = C/T
- **Ferromagnetism**: Spontaneous magnetization below Tc, hysteresis, domains
- **Antiferromagnetism**: Alternating spin alignment below Néel temperature
- **Exchange interaction**: J > 0 (ferromagnetic), J < 0 (antiferromagnetic)

## Computational Tools
- **VASP**: Plane-wave DFT for electronic structure
- **Quantum ESPRESSO**: Open-source DFT
- **WIEN2k**: Full-potential linearized augmented plane wave (FLAPW)
- **LAMMPS**: Classical molecular dynamics
- **Kwant**: Quantum transport simulations

## Standards & References
- Kittel — *Introduction to Solid State Physics*
- Ashcroft & Mermin — *Solid State Physics*
- Marder — *Condensed Matter Physics*

---
name: electromagnetism
description: "Maxwell's equations, electrostatics, magnetostatics, electromagnetic waves, circuit theory, and radiation"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/electromagnetism/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Electromagnetism

## Scope
Electromagnetism describes electric charges, currents, electric and magnetic fields, and their interactions. This skill covers electrostatics through radiation, with both theoretical frameworks and practical computational methods.

## Maxwell's Equations

### Differential Form
1. **Gauss's Law (E)**: ∇·E = ρ/ε₀ — Electric charges produce electric field divergence
2. **Gauss's Law (B)**: ∇·B = 0 — No magnetic monopoles
3. **Faraday's Law**: ∇×E = -∂B/∂t — Changing magnetic field induces electric field
4. **Ampère-Maxwell**: ∇×B = μ₀J + μ₀ε₀(∂E/∂t) — Currents and changing E-fields produce B-fields

### Integral Form
1. ∮ E·dA = Q_enc/ε₀
2. ∮ B·dA = 0
3. ∮ E·dl = -dΦ_B/dt
4. ∮ B·dl = μ₀I_enc + μ₀ε₀(dΦ_E/dt)

### Key Constants
- ε₀ = 8.854 × 10⁻¹² F/m (permittivity of free space)
- μ₀ = 4π × 10⁻⁷ H/m (permeability of free space)
- c = 1/√(μ₀ε₀) ≈ 3 × 10⁸ m/s

## Electrostatics
- **Coulomb's Law**: F = kq₁q₂/r² where k = 1/(4πε₀) ≈ 8.99 × 10⁹ N·m²/C²
- **Electric Potential**: V = kq/r, E = -∇V
- **Poisson's Equation**: ∇²V = -ρ/ε₀ (Laplace's equation when ρ = 0)
- **Capacitance**: C = Q/V; parallel plate: C = ε₀A/d
- **Energy stored**: U = ½CV² = ½QV = Q²/(2C)

### Solution Strategies
- **High symmetry** (spherical/cylindrical/planar): Use Gauss's Law
- **Known charge distribution**: Direct integration of Coulomb's Law
- **Boundary value problems**: Solve Laplace/Poisson with separation of variables, method of images, or numerical methods (FEM/BEM)

## Magnetostatics
- **Biot-Savart Law**: dB = (μ₀/4π)(I dl × r̂)/r²
- **Ampère's Law**: ∮ B·dl = μ₀I_enc (use for high-symmetry current distributions)
- **Magnetic Force**: F = qv × B (Lorentz force), F = IL × B (force on wire)
- **Inductance**: L = NΦ/I; solenoid: L = μ₀n²Al
- **Energy stored**: U = ½LI²

## Electromagnetic Waves
- Wave equation: ∇²E = μ₀ε₀(∂²E/∂t²), solution: E = E₀sin(kx - ωt)
- Wave speed: v = ω/k = c/n
- Poynting vector: S = (1/μ₀)(E × B) — energy flux
- Intensity: I = ⟨S⟩ = E₀²/(2μ₀c)
- Radiation pressure: P = I/c (absorbed), P = 2I/c (reflected)

## Computational Tools
- **COMSOL Multiphysics**: FEM for EM field simulation
- **ANSYS HFSS/Maxwell**: High-frequency and low-frequency EM
- **Meep (MIT)**: FDTD open-source electromagnetic simulation
- **Python**: `scipy`, `fenics`, `dolfinx` for numerical PDE solutions
- **CST Studio Suite**: Microwave and antenna design

## Standards & References
- Griffiths — *Introduction to Electrodynamics* (4th ed.)
- Jackson — *Classical Electrodynamics* (3rd ed.)
- Purcell & Morin — *Electricity and Magnetism*

---
name: thermodynamics
description: "Laws of thermodynamics, heat engines, entropy, free energy, phase transitions, and statistical interpretations"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/thermodynamics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Thermodynamics

## Scope
Thermodynamics describes energy, heat, work, and the transformations between them. This skill covers equilibrium thermodynamics, the four laws, thermodynamic potentials, and practical applications in engineering and science.

## The Four Laws

### Zeroth Law
If system A is in thermal equilibrium with system C, and B is in thermal equilibrium with C, then A is in thermal equilibrium with B. This defines temperature as a measurable quantity.

### First Law (Energy Conservation)
ΔU = Q - W (sign convention: Q positive into system, W positive out of system)
- **Isochoric** (constant V): W = 0, ΔU = Q = nCᵥΔT
- **Isobaric** (constant P): W = PΔV, Q = nCₚΔT
- **Isothermal** (constant T): ΔU = 0, Q = W = nRT ln(V₂/V₁)
- **Adiabatic** (Q = 0): TV^(γ-1) = const, PV^γ = const

### Second Law
- **Clausius**: Heat cannot spontaneously flow from cold to hot
- **Kelvin-Planck**: No heat engine can convert all heat into work
- **Entropy**: ΔS ≥ Q/T (equality for reversible processes)
- For an isolated system: ΔS_total ≥ 0

### Third Law
As T → 0, S → 0 for a perfect crystal. No finite sequence of operations can reach absolute zero.

## Thermodynamic Potentials
| Potential | Definition | Natural Variables | Equilibrium Condition |
|-----------|-----------|-------------------|----------------------|
| Internal Energy U | Fundamental | S, V | dU = TdS - PdV |
| Enthalpy H | U + PV | S, P | dH = TdS + VdP |
| Helmholtz F | U - TS | T, V | dF = -SdT - PdV |
| Gibbs G | U + PV - TS | T, P | dG = -SdT + VdP |

**Decision rule**: Use the potential whose natural variables match your constraints.

## Heat Engine Analysis
- **Carnot efficiency**: η_Carnot = 1 - T_cold/T_hot (maximum possible)
- **Coefficient of Performance**: COP_cooling = Q_cold/W, COP_heating = Q_hot/W
- **Otto cycle**: η = 1 - 1/r^(γ-1) where r = compression ratio
- **Rankine cycle**: Used in steam power plants; analyze with h-s (Mollier) diagrams
- **Refrigeration cycle**: Vapor-compression with evaporator, compressor, condenser, expansion valve

## Phase Transitions
- **Clausius-Clapeyron**: dP/dT = ΔH/(TΔV) (slope of phase boundary)
- **First-order**: Discontinuity in S, V (e.g., boiling, melting); latent heat L = TΔS
- **Second-order**: Discontinuity in Cₚ, κ, α (e.g., superconducting transition)
- **Critical point**: Phase boundary terminates; critical exponents describe behavior

## Computational Tools
- **CoolProp**: Open-source thermophysical property library (Python, C++)
- **Cantera**: Chemical kinetics and thermodynamics
- **REFPROP (NIST)**: Reference fluid thermodynamic properties
- **EES**: Engineering Equation Solver for thermodynamic cycle analysis

## Standards & References
- Cengel & Boles — *Thermodynamics: An Engineering Approach*
- Schroeder — *An Introduction to Thermal Physics*
- NIST Chemistry WebBook — thermodynamic data tables

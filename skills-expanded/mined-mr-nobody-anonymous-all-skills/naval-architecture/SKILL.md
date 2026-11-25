---
name: naval-architecture
description: "Ship design principles: hull form, stability, resistance, propulsion, structural design, and classification rules"
category: marine
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/marine/naval-architecture/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Naval Architecture

## Scope
Naval architecture is the engineering discipline of designing ships and marine structures. This skill covers hull form design, hydrostatics, stability, resistance, propulsion, and structural design.

## Hull Form Design
- **Lines plan**: Body plan (cross-sections), waterplane, profile
- **Hull parameters**:
  - Length (LOA, LBP, LWL)
  - Beam (B), Draft (T), Depth (D)
  - Block coefficient: Cᵦ = ∇/(L × B × T) — fullness of hull
  - Prismatic coefficient: Cₚ = ∇/(Aₘ × L)
  - Waterplane coefficient: Cᵥ = Aᵥ/(L × B)

## Hydrostatics & Stability

### Archimedes' Principle
Δ = ρ × g × ∇ (displacement = weight of displaced water)

### Transverse Stability
- **Center of gravity (G)**: Weight centroid of the ship
- **Center of buoyancy (B)**: Centroid of underwater volume
- **Metacenter (M)**: BM = I/∇ where I = second moment of waterplane area
- **GM (metacentric height)**: GM = KB + BM - KG
  - GM > 0: Stable (positive righting moment)
  - GM < 0: Unstable (capsizes)
  - Typical: GM = 0.5-1.5 m for cargo ships

### GZ Curve (Righting Arm)
- GZ = GM sin θ (small angles)
- Large angle: Cross-curves of stability method
- **Area under GZ curve**: Measure of dynamic stability
- **Angle of vanishing stability**: GZ = 0 (beyond this, ship capsizes)

### Damage Stability
- **Probabilistic**: Required Attained Subdivision Index A ≥ Required Index R (SOLAS Ch. II-1)
- **Deterministic**: Specify extent of damage; verify positive stability

## Resistance & Propulsion

### Ship Resistance Components
- **Frictional resistance**: Rₓ = ½ ρ S V² Cₓ (ITTC 1957 line)
- **Wave-making resistance**: Function of Froude number Fn = V/√(gL)
- **Form resistance**: Viscous pressure resistance
- **Total**: Rₜ = (1 + k) × Rₓ + Rᵥ (form factor method)

### Propulsion
- **Propeller design**: Diameter, pitch, blade area ratio, RPM
- **Thrust deduction**: T(1-t) = R (t = thrust deduction factor)
- **Wake fraction**: V_a = V(1-w) (advance velocity)
- **Propulsive efficiency**: η_D = η_hull × η_behind × η_relative_rotative
- **Power**: Effective power PE = R × V, Brake power PB = PE/η_D

## Structural Design
- **Longitudinal strength**: Still-water + wave bending moments; M_sw + M_wave ≤ M_allowable
- **Section modulus**: Z = I/y_max ≥ Z_required (classification society rules)
- **Midship section**: Primary structural frame design
- **Fatigue**: S-N curves, stress concentration factors, spectral fatigue analysis

## Classification Rules
- **Lloyd's Register (LR)**: UK-based
- **DNV**: Norwegian-German
- **Bureau Veritas (BV)**: French
- **ABS**: American
- **ClassNK**: Japanese
- **IACS**: International Association of Classification Societies (common structural rules)

## Software Tools
- **NAPA**: Hull form design, hydrostatics, stability
- **Maxsurf**: Hull modeling, resistance, stability
- **ShipConstructor/AVEVA Marine**: Structural design
- **OpenFOAM/STAR-CCM+**: CFD for resistance prediction
- **ANSYS/Abaqus**: FEA for structural analysis

## Standards & References
- SOLAS (Safety of Life at Sea)
- MARPOL (Marine Pollution Prevention)
- IMO Intact Stability Code (2008 IS Code)
- Tupper — *Introduction to Naval Architecture*
- Lewis — *Principles of Naval Architecture* (SNAME)

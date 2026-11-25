---
name: mineral-processing
description: "Ore processing: comminution, flotation, gravity separation, hydrometallurgy, and process plant design"
category: mining
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mining/mineral-processing/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mineral Processing

## Scope
Mineral processing (ore dressing/beneficiation) transforms raw mined ore into concentrate suitable for smelting/refining. This skill covers comminution, separation, hydrometallurgy, and plant design.

## Comminution (Size Reduction)

### Crushing
| Stage | Feed Size | Product Size | Equipment |
|-------|-----------|-------------|-----------|
| Primary | ROM (run-of-mine) | 100-200 mm | Jaw crusher, gyratory crusher |
| Secondary | 100-200 mm | 20-50 mm | Cone crusher, impact crusher |
| Tertiary | 20-50 mm | 5-15 mm | Short-head cone, HPGR |

### Grinding
- **Ball mill**: Steel balls (50-100 mm) in rotating cylinder; wet grinding to 75-150 μm
- **SAG mill**: Semi-autogenous; large diameter, uses ore as grinding media + some balls
- **Rod mill**: Steel rods for coarser grinding
- **Bond Work Index**: W = 10Wi(1/√P₈₀ - 1/√F₈₀) kWh/t — energy required for size reduction
  - P₈₀ = 80% passing product size, F₈₀ = 80% passing feed size

### Classification
- **Hydrocyclone**: Centrifugal separation; d₅₀ = cut point size
- **Spiral classifier**: Gravity-based; coarse returns to mill
- **Vibrating screen**: Size-based separation

## Separation Methods

### Froth Flotation
The most important separation process in mining, used for sulfide ores.
- **Principle**: Hydrophobic particles attach to air bubbles, rise to froth
- **Reagents**:
  - Collectors (xanthates): Make target mineral hydrophobic
  - Frothers (MIBC, pine oil): Stabilize froth
  - Depressants (lime, NaCN): Prevent unwanted minerals from floating
  - Activators (CuSO₄): Make minerals responsive to collectors
  - pH regulators (lime, H₂SO₄)
- **Circuit**: Rougher → cleaner → scavenger; recirculating loads
- **Recovery**: R = (Cc)/(Ff) × 100% where C = concentrate mass, c = concentrate grade, F = feed mass, f = feed grade

### Gravity Separation
- **Jig**: Pulsating water stratifies heavy/light particles
- **Spiral concentrator**: Flowing film on helical surface
- **Shaking table**: Differential motion separates by density
- **Dense medium separation (DMS)**: Sink-float in ferrosilicon/magnetite suspension
- **Criterion**: Concentration criterion CC = (ρ_heavy - ρ_fluid)/(ρ_light - ρ_fluid); CC > 2.5 = easy separation

### Magnetic Separation
- **Low-intensity (LIMS)**: Magnetite recovery (< 0.3 T)
- **High-intensity (HIMS)**: Paramagnetic minerals (> 1 T)
- **WHIMS**: Wet high-intensity; fine particle recovery

### Hydrometallurgy
- **Leaching**: Dissolve target metal: heap (Au with NaCN), vat, agitated tank, pressure (Ni/Cu)
- **SX (solvent extraction)**: Organic phase selectively extracts metal ions
- **Electrowinning**: Deposit metal from solution onto cathode (Cu, Zn, Au)
- **Carbon-in-pulp (CIP)**: Activated carbon adsorbs gold from cyanide solution

## Process Design
- **Mass balance**: Inputs = Outputs (at steady state); grade-recovery curves
- **Circuit simulation**: Modsim, JKSimMet, METSIM
- **Scale-up**: Pilot plant → design criteria → equipment sizing
- **Tailings**: Thickening, filtration, storage; TSF (tailings storage facility) design is critical safety issue

## Standards & References
- Wills & Finch — *Mineral Processing Technology* (8th ed.)
- SME Mineral Processing & Extractive Metallurgy Handbook
- AMIRA P9 project reports (comminution research)

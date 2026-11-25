---
name: quantitative-physiology
description: This skill should be used when calculating physiological parameters, modeling membrane transport, analyzing cardiovascular hemodynamics, computing renal clearance, simulating action potentials, or explaining quantitative relationships in any human physiological system. Use for physiology homework, medical calculations, computational biology modeling, and pharmacokinetic analysis.
version: 3.0.0
equation_count: 248
source: "Quantitative Human Physiology: An Introduction, 3rd Edition - Joseph J. Feher (Elsevier 2026)"
---

# Quantitative Human Physiology

## Overview

**248 atomic equations** across 9 physiological domains with full dependency tracking. Each equation is a standalone Python module with compute functions, parameters, and metadata.

## Architecture

```
scripts/
├── foundations/      # 20 equations - transport, diffusion, thermodynamics
├── membrane/         # 18 equations - channels, pumps, potential
├── excitable/        # 22 equations - action potentials, muscle
├── nervous/          # 27 equations - synapses, sensory, motor
├── cardiovascular/   # 31 equations - heart, circulation, hemodynamics
├── respiratory/      # 41 equations - ventilation, gas exchange
├── renal/            # 30 equations - filtration, clearance
├── gastrointestinal/ # 34 equations - digestion, absorption
└── endocrine/        # 25 equations - hormones, feedback
```

## Quick Import

```python
# Import entire domains
from scripts import cardiovascular, respiratory, renal

# Import specific equations
from scripts.cardiovascular.cardiac import cardiac_output, ejection_fraction
from scripts.respiratory.gas_exchange import alveolar_gas_equation
from scripts.renal.clearance import clearance, filtered_load

# Import foundations used across domains
from scripts.foundations.transport import poiseuille_flow
from scripts.foundations.thermodynamics import nernst_equation
```

## Core Principles

### Conservation Laws
- **Mass**: Input = Output + Accumulation
- **Energy**: Follow thermodynamic constraints
- **Charge**: Maintain electroneutrality

### Transport Classification
1. **Bulk flow**: Pressure-driven (Poiseuille)
2. **Diffusion**: Concentration-driven (Fick)
3. **Active transport**: ATP-coupled pumps

## Essential Equations

### Transport

**Poiseuille's Law** (laminar flow):
```
Q = (πr⁴/8η) × (ΔP/L)
```
Flow scales with radius⁴. Doubling vessel radius → 16× flow.

**Fick's First Law** (diffusion):
```
J = -D × (dC/dx)
```

**Diffusion time scaling**:
```
t = x²/(2D)
```

### Membrane Potential

**Nernst equation** (single ion equilibrium):
```
E = (RT/zF) × ln(C_out/C_in)
```
At 37°C: E ≈ (61.5/z) × log₁₀(C_out/C_in) mV

**Goldman-Hodgkin-Katz** (multiple ions):
```
V_m = (RT/F) × ln[(P_K[K]_o + P_Na[Na]_o + P_Cl[Cl]_i) / (P_K[K]_i + P_Na[Na]_i + P_Cl[Cl]_o)]
```

### Kinetics

**Michaelis-Menten**:
```
J = J_max × [S] / (K_m + [S])
```

**Hill equation** (cooperativity):
```
J = J_max × [S]ⁿ / (K₀.₅ⁿ + [S]ⁿ)
```

## Cross-Domain Equations

These foundational equations are used across multiple physiological systems:

| Equation | Primary | Also Used In | Import |
|----------|---------|--------------|--------|
| Nernst | foundations | membrane, excitable, nervous, cardiovascular, renal | `from scripts.foundations.thermodynamics import nernst_equation` |
| Fick Diffusion | foundations | respiratory, renal, cardiovascular | `from scripts.foundations.diffusion import fick_flux` |
| Poiseuille | foundations | cardiovascular, renal | `from scripts.foundations.transport import poiseuille_flow` |
| Michaelis-Menten | foundations | renal, gastrointestinal, endocrine | `from scripts.foundations.kinetics import michaelis_menten` |
| Hill | foundations | excitable, cardiovascular, respiratory, endocrine | `from scripts.foundations.kinetics import hill_equation` |
| Henderson-Hasselbalch | foundations | respiratory, renal | `from scripts.foundations.thermodynamics import henderson_hasselbalch` |
| Starling Forces | cardiovascular | renal, gastrointestinal | `from scripts.cardiovascular.microcirculation import starling_filtration` |
| Goldman-Hodgkin-Katz | membrane | excitable, nervous, cardiovascular | `from scripts.membrane.potential import ghk_potential` |

## Domain Reference Files

Load specific references for detailed domain analysis:

| Domain | Reference | Equations | Key Topics |
|--------|-----------|-----------|------------|
| Physical Foundations | `references/physical-foundations.md` | 20 | Poiseuille, Laplace, diffusion, thermodynamics |
| Membranes & Transport | `references/membranes-transport.md` | 18 | Channels, pumps, osmosis, Donnan equilibrium |
| Excitable Cells | `references/excitable-cells.md` | 22 | Action potentials, Hodgkin-Huxley, muscle |
| Nervous System | `references/nervous-system.md` | 27 | Synapses, sensory, motor control |
| Cardiovascular | `references/cardiovascular.md` | 31 | Frank-Starling, hemodynamics, ECG |
| Respiratory | `references/respiratory.md` | 41 | Lung mechanics, V/Q matching, acid-base |
| Renal | `references/renal.md` | 30 | GFR, tubular function, countercurrent |
| Gastrointestinal | `references/gastrointestinal.md` | 34 | Secretion, absorption, motility |
| Endocrine | `references/endocrine.md` | 25 | Hormone kinetics, HPA axis, feedback |

## Dependency Graph

See `graph/dependency-graph.json` for full equation dependencies.

### Key Dependency Chains

1. **Membrane → Action Potential**: Nernst → GHK → HH membrane current → Na/K currents
2. **Oxygen Cascade**: Hill saturation → O₂ content → O₂ delivery → Fick principle
3. **Renal Clearance**: RPF → filtration fraction → GFR → clearance → fractional excretion
4. **HPA Axis**: CRH dynamics → ACTH dynamics → Cortisol dynamics → feedback gain

### Functional Clusters

See `graph/clusters.json` for equation groupings by physiological function:
- Transport & Fluid Mechanics (7 equations)
- Electrochemical Gradients (5 equations)
- Excitation-Contraction Coupling (5 equations)
- Oxygen Transport Cascade (6 equations)
- Acid-Base Homeostasis (5 equations)
- Renal Filtration & Clearance (6 equations)
- Hormone Kinetics & Feedback (5 equations)
- Synaptic & Neural Signaling (5 equations)
- GI Secretion & Absorption (5 equations)
- Cardiovascular Regulation (5 equations)

## Physical Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Gas constant | R | 8.314 | J/(mol·K) |
| Faraday constant | F | 96,485 | C/mol |
| Body temperature | T | 310 | K |

## Example Usage

**Calculate Nernst potential for K⁺**:
```python
from scripts.foundations.thermodynamics import nernst_equation
E_K = nernst_equation.compute(z=1, C_out=4, C_in=140)  # ≈ -95 mV
```

**Calculate cardiac output**:
```python
from scripts.cardiovascular.cardiac import cardiac_output
CO = cardiac_output.compute(heart_rate=70, stroke_volume=0.070)  # 4.9 L/min
```

**Calculate GFR from Starling forces**:
```python
from scripts.renal.glomerular import gfr_from_nfp, net_filtration_pressure
NFP = net_filtration_pressure.compute(P_gc=50, P_bs=15, pi_gc=25, pi_bs=0)
GFR = gfr_from_nfp.compute(Kf=12.5, NFP=NFP)  # mL/min
```

## Physiological Reference Values

| Parameter | Normal Range |
|-----------|--------------|
| Resting membrane potential | -70 to -90 mV |
| Cardiac output | 4-8 L/min |
| Blood pressure | 120/80 mmHg |
| GFR | 90-120 mL/min |
| Arterial pH | 7.35-7.45 |
| PaO₂ | 80-100 mmHg |
| PaCO₂ | 35-45 mmHg |

## Problem-Solving Workflow

1. **Identify the process**: Flow, diffusion, electrical, kinetics?
2. **List knowns with units**: Enforce dimensional consistency
3. **Select equation module**: Match process to appropriate domain
4. **Calculate**: Use `.compute()` method with parameters
5. **Validate**: Check result against physiological ranges
6. **Interpret**: Explain biological significance

Load domain-specific references when detailed mechanisms needed beyond core equations.

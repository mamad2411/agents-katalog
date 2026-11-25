---
name: mar-naval-hydrodynamics-cfd-stability
description: "Evaluate ship resistance, calculate metacentric height ($GM$), and perform hydrodynamic CFD wave resistance simulations conforming to IMO stability criteria."
category: marine
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - marine
  - naval-architecture
  - hydrodynamics
  - cfd
  - ship-stability
---

# Naval Hydrodynamics CFD Resistance & Ship Stability Engineering

## Overview & Core Principles
Evaluate ship resistance, calculate metacentric height ($GM$), and perform hydrodynamic CFD wave resistance simulations conforming to IMO stability criteria.

### Metacentric Stability & Hydrodynamic Equations
1. **Transverse Metacentric Height ($GM$)**:
   - $GM = KB + BM - KG$, where:
     - $KB$: Center of buoyancy above keel.
     - $BM = \frac{I_T}{\nabla}$: Metacentric radius ($I_T$ = waterplane transverse moment of inertia, $\nabla$ = submerged displacement volume).
     - $KG$: Center of gravity above keel.
   - Invariant: Positive initial stability requires $GM > 0.15\text{ m}$ per IMO Code on Intact Stability.
2. **Total Hull Resistance Decomposition**:
   - $R_T = R_F (1 + k) + R_W + R_{APP} + R_{AA}$
     - $R_F$: Frictional resistance computed via ITTC-1957 skin-friction line: $C_F = \frac{0.075}{(\log_{10} Re - 2)^2}$.
     - $k$: Form factor.
     - $R_W$: Wave-making resistance dependent on Froude number $Fn = \frac{V}{\sqrt{g L}}$.
3. **Ballast Water Management Plan**:
   - Ensure compliance with IMO BWM Convention (Regulation D-2 standard for living organism discharge limits).

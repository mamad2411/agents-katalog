---
name: min-block-model-kriging-tailings-stability
description: "Perform 3D ordinary kriging resource grade estimation, calculate variogram models, and compute tailings dam slope stability factor of safety."
category: mining
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - mining
  - geostatistics
  - kriging
  - tailings-dam
  - geotechnical
---

# Mining Block Model Geostatistical Kriging & Tailings Dam Stability

## Overview & Core Principles
Perform 3D ordinary kriging resource grade estimation, calculate variogram models, and compute tailings dam slope stability factor of safety.

### Geostatistical Kriging & Limit Equilibrium Stability
1. **Experimental Semivariogram Calculation**:
   $$\gamma(h) = \frac{1}{2 N(h)} \sum_{i=1}^{N(h)} [Z(x_i) - Z(x_i + h)]^2$$
   - Fit spherical, exponential, or Gaussian variogram models defining nugget $C_0$, sill $C_0 + C$, and spatial range $a$.
2. **Ordinary Kriging System**:
   $$\sum_{j=1}^n \lambda_j \gamma(x_i - x_j) + \mu = \gamma(x_i - x_0), \quad \sum_{j=1}^n \lambda_j = 1$$
   - Unbiased minimal estimation variance condition.
3. **Tailings Storage Facility (TSF) Slope Stability**:
   - Conformance with Global Industry Standard on Tailings Management (GISTM).
   - Bishop's Simplified Method of Slices: Enforce Factor of Safety (FoS) $\ge 1.5$ under static steady-state seepage, and FoS $\ge 1.1$ under post-liquefaction seismic conditions.

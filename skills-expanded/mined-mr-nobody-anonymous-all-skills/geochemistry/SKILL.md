---
name: geochemistry
description: "Isotope geochemistry, trace element partitioning, thermodynamic modeling of water-rock interactions, and geochemical cycles"
category: earth-science
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/earth-science/geochemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Geochemistry

## Scope
Geochemistry applies chemical principles to understand the distribution, migration, and cycles of chemical elements and isotopes across the Earth's crust, mantle, oceans, and atmosphere.

## Core Formulations

### 1. Element Partitioning
- **Partition Coefficient ($D$)**: $D = C_{\text{mineral}} / C_{\text{melt}}$.
  - Compatible elements ($D > 1$): Concentrate in solid residue during melting.
  - Incompatible elements ($D < 1$): Concentrate in liquid melt (LILE, HFSE).
- **Batch Melting Equation**:
  $$\frac{C_L}{C_0} = \frac{1}{D_0 + F(1 - D_0)}$$
  where $F$ is melt fraction, $C_0$ initial bulk concentration.

### 2. Radiogenic & Stable Isotopes
- **Isotopic Fractionation ($\delta$ notation)**:
  $$\delta^{18}O = \left(\frac{(^{18}O/^{16}O)_{\text{sample}}}{(^{18}O/^{16}O)_{\text{standard}}} - 1\right) \times 1000\text{ \textperthousand}$$
- **Isochron Dating**:
  $$\left(\frac{^{87}Sr}{^{86}Sr}\right) = \left(\frac{^{87}Sr}{^{86}Sr}\right)_0 + \left(\frac{^{87}Rb}{^{86}Sr}\right)(e^{\lambda t} - 1)$$

## Tools & Standards
- **Software**: PHREEQC, Geochemist's Workbench, MELTS, IsoplotR.
- **Canonical References**: White — *Geochemistry*; Faure & Mensing — *Isotopes: Principles and Applications*.

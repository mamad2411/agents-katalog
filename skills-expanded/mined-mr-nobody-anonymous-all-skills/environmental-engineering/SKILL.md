---
name: environmental-engineering
description: "Water and wastewater treatment processes, activated sludge modeling, air quality dispersion (Gaussian plume), and solid waste"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/environmental-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Environmental Engineering

## Scope
Environmental engineering protects public health and natural ecosystems through water purification, wastewater treatment, hazardous waste remediation, and emission control.

## Process Models & Equations
- **BOD Kinetics**: $\text{BOD}_t = L_0 (1 - e^{-k t})$.
- **Activated Sludge (Monod Growth Kinetics)**:
  $$\mu = \mu_{\max} \frac{S}{K_s + S}, \quad \theta_c = \frac{V X}{Q_w X_w + Q_e X_e} \quad (\text{Mean Cell Residence Time, MCRT})$$
- **Air Dispersion (Gaussian Plume Model)**:
  $$C(x,y,z) = \frac{Q}{2\pi u \sigma_y \sigma_z} \exp\left(-\frac{y^2}{2\sigma_y^2}\right)\left[\exp\left(-\frac{(z-H)^2}{2\sigma_z^2}\right) + \exp\left(-\frac{(z+H)^2}{2\sigma_z^2}\right)\right]$$

## Tools & Standards
- **Standards**: EPA Clean Water Act, Clean Air Act, Ten State Standards (Wastewater).
- **Software**: BioWin, GPS-X, AERMOD (air dispersion).
- **Canonical References**: Davis & Cornwell — *Introduction to Environmental Engineering*; Metcalf & Eddy — *Wastewater Engineering*.

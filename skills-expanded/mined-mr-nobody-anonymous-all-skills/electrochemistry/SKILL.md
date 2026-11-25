---
name: electrochemistry
description: "Electrochemical cells, Nernst equation, cyclic voltammetry, Butler-Volmer kinetics, batteries, fuel cells, and corrosion"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/electrochemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Electrochemistry

## Scope
Electrochemistry studies the relationship between electrical energy and chemical reactions, including redox processes, electrode kinetics, energy storage (batteries, supercapacitors), and corrosion.

## Electrochemical Formulations

### 1. Thermodynamics of Cells
- **Nernst Equation**:
  $$E = E^\circ - \frac{RT}{nF} \ln Q = E^\circ - \frac{0.0592}{n} \log_{10} Q \quad (\text{at } 298.15\text{ K})$$
- **Free Energy Relation**: $\Delta G = -nFE$, $\Delta G^\circ = -nFE^\circ$.
- **Faraday's Law of Electrolysis**: $m = \frac{Q \cdot M}{n \cdot F} = \frac{I \cdot t \cdot M}{n \cdot F}$, where $F = 96,485\text{ C/mol}$.

### 2. Electrode Kinetics & Butler-Volmer
- **Butler-Volmer Equation**:
  $$j = j_0 \left[ \exp\left(\frac{\alpha_a n F \eta}{RT}\right) - \exp\left(-\frac{\alpha_c n F \eta}{RT}\right) \right]$$
  where $\eta = E - E_{eq}$ is overpotential, and $j_0$ is exchange current density.
- **Tafel Approximation** (high overpotential $\eta > 100\text{ mV}$):
  $$\eta = a + b \log_{10} j, \quad b = \frac{2.303 RT}{\alpha n F}$$

### 3. Cyclic Voltammetry (CV)
- **Randles-Sevcik Equation** (reversible diffusion-controlled process at $25^\circ\text{C}$):
  $$i_p = (2.69 \times 10^5) n^{3/2} A D^{1/2} C \nu^{1/2}$$
  where $\nu$ is scan rate (V/s), $D$ is diffusion coefficient ($cm^2/s$).
- Reversibility criteria: $\Delta E_p = E_{pa} - E_{pc} \approx 59/n\text{ mV}$, $i_{pa} / i_{pc} \approx 1$.

## Tools & Standards
- **Instruments**: Potentiostats/Galvanostats (Gamry, Bio-Logic, Metrohm Autolab).
- **Canonical References**: Bard & Faulkner — *Electrochemical Methods: Fundamentals and Applications*; Newman & Thomas-Alyea — *Electrochemical Systems*.
